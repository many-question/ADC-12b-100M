"""adc_bootstrap acceptance measurements (tb/bootstrap/*)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .. import psf, soa
from ..figures import C1, C2, C3, C7, GRID, INK2, LIMIT, MUTED, hline, limits, note, plot_spectrum, sink_of, spec_table, vline
from .common import fig_cin, pin_cins, read_meters, read_samples, spectrum, tran

LEVEL_CYCLES = 4
VIN_STEP = 0.15          # tb_bootstrap_dc: input level k is k * 0.15 V


def dc(job_dir: Path, ctx: dict) -> dict:
    vdd = float(ctx["globals"]["vdd"])
    s = read_samples(Path(job_dir) / "vgs.txt")[:, 2]
    per_level = s[LEVEL_CYCLES - 1::LEVEL_CYCLES]          # last sample of every input level
    m: dict = {"vgs_levels_V": [round(float(x), 4) for x in per_level]}
    if len(per_level):
        m["vgs_min_V"] = float(per_level.min())
        m["vgs_var_mV"] = float((per_level.max() - per_level.min()) * 1e3)
    w = tran(job_dir)
    t, vg, vin, phb, bp = w["time"], w["VG"], w["VIN"], w["PHI_B"], w["BP"]
    t_off, t_on = [], []                                   # (edge time, delay)
    for tf in psf.crossings(t, phb, vdd / 2, -1):
        idx = np.nonzero((t > tf) & (vg < 0.1))[0]
        if len(idx):
            t_off.append((tf, t[idx[0]] - tf))
    rises = psf.crossings(t, phb, vdd / 2, +1)
    falls = psf.crossings(t, phb, vdd / 2, -1)
    for tr in rises:
        nf = falls[falls > tr]
        if not len(nf):
            continue
        final = np.interp(nf[0] - 20e-12, t, vg - vin)
        idx = np.nonzero((t > tr) & (t < nf[0]) & ((vg - vin) >= 0.95 * final))[0]
        if len(idx):
            t_on.append((tr, t[idx[0]] - tr, final))
    if t_off:
        m["t_off_ps"] = float(max(d for _, d in t_off) * 1e12)
    if t_on:
        m["t_on_ps"] = float(max(d for _, d, _ in t_on) * 1e12)
    soa.measure(ctx, w, m)                                 # BST-08: per-device SOA (error if unverified)
    meters = read_meters(Path(job_dir) / "power.txt")
    if "AVDD" in meters:
        m["iavg_uA"] = float(meters["AVDD"] * 1e6)
    cins = pin_cins(w, vdd, {"cin_phb_fF": ("PHI_B", "QPB"), "cin_phbb_fF": ("PHI_BB", "QPBB")})
    m.update({k: float(c.mean() * 1e15) for k, c in cins.items() if len(c)})
    fg = sink_of(ctx)
    if fg:
        _fig_dc(fg, ctx, w, per_level, t_off, t_on, m)
        if "soa_table" in m:
            soa.figure(fg, ctx, m, w)
        fig_cin(fg, ctx, cins, [("cin_phb_fF", "PHI_B", "cin_phb_fF"), ("cin_phbb_fF", "PHI_BB", "cin_phbb_fF")])
    return m


def track(job_dir: Path, ctx: dict) -> dict:
    p = ctx["params"]
    npts = int(float(p.get("npts", 256)))
    s = read_samples(Path(job_dir) / "samples.txt")[:, 2][:npts]
    if len(s) < npts:
        return {"error": f"only {len(s)} samples"}
    fs = 1 / float(p.get("tper", 10e-9))
    sp = spectrum(s - s.mean(), fs, None, ctx)
    m = {"sfdr_dBc": sp["sfdr_dBc"], "sndr_dB": sp["sndr_dBc"], "thd_dBc": sp["thd_dBc"]}
    fg = sink_of(ctx)
    if fg:
        fig, axs = fg.new(1, 1, size=(8.2, 4.2))
        plot_spectrum(axs[0, 0], s - s.mean(), fs, None, m, sfdr_min=limits(ctx, "sfdr_dBc")[0],
                      sndr_min=limits(ctx, "sndr_dB")[0])
        fg.save(fig, "spectrum", "Spectrum of the voltage sampled through the bootstrapped switch for a "
                "full-scale tracking input, with SFDR and SNDR against their limits.")
    return m


# ------------------------------------------------------------------ figures
def _fig_dc(fg, ctx, w, per_level, t_off, t_on, m) -> None:
    t, vg, vin, phb, bp = w["time"], w["VG"], w["VIN"], w["PHI_B"], w["BP"]
    fig, axs = fg.new(2, 3, size=(15.0, 7.4))
    ax = axs[0, 0]
    x = np.arange(len(per_level)) * VIN_STEP
    ax.plot(x, per_level, "o-", color=C1, ms=6)
    lo = limits(ctx, "vgs_min_V")[0]
    hline(ax, lo, f"limit >= {lo:g} V" if lo else None)
    ax.set(xlabel="input level VIN (V)", ylabel="VG - VIN at the sampling instant (V)",
           title="Boosted gate voltage over the input range", ylim=(min(per_level.min(), lo or 1) - 0.03,
                                                                    per_level.max() + 0.03))
    hi = limits(ctx, "vgs_var_mV")[1]
    note(ax, f"variation {m.get('vgs_var_mV', float('nan')):.1f} mV" + (f" (limit {hi:g})" if hi else ""),
         loc="lower left")
    # worst turn-off and turn-on edges
    ax = axs[0, 1]
    if t_off:
        tf, d = max(t_off, key=lambda e: e[1])
        sel = (t > tf - 60e-12) & (t < tf + 160e-12)
        ax.plot((t[sel] - tf) * 1e12, phb[sel], color=C2, label="PHI_B")
        ax.plot((t[sel] - tf) * 1e12, vg[sel], color=C1, label="VG")
        ax.axhline(0.1, color=GRID, lw=0.8)
        ax.plot([d * 1e12], [0.1], "o", color=INK2, ms=4)
        ax.annotate(f"VG < 0.1 V after {d * 1e12:.0f} ps", (d * 1e12, 0.1), (d * 1e12 + 15, 0.5), fontsize=8,
                    color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
        hi = limits(ctx, "t_off_ps")[1]
        vline(ax, hi, f"limit {hi:g} ps" if hi else None)
    ax.set(xlabel="time from the PHI_B falling edge (ps)", ylabel="voltage (V)", title="Turn-off (worst edge)")
    ax.legend(loc="center right")
    ax = axs[0, 2]
    if t_on:
        tr, d, final = max(t_on, key=lambda e: e[1])
        sel = (t > tr - 60e-12) & (t < tr + max(4 * d, 400e-12))
        ax.plot((t[sel] - tr) * 1e12, phb[sel], color=C2, label="PHI_B")
        ax.plot((t[sel] - tr) * 1e12, (vg - vin)[sel], color=C1, label="VG - VIN")
        ax.axhline(0.95 * final, color=GRID, lw=0.8)
        ax.plot([d * 1e12], [0.95 * final], "o", color=INK2, ms=4)
        ax.annotate(f"95 % of {final:.2f} V after {d * 1e12:.0f} ps", (d * 1e12, 0.95 * final),
                    (d * 1e12 + 30, 0.3 * final), fontsize=8, color=INK2,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
        hi = limits(ctx, "t_on_ps")[1]
        vline(ax, hi, f"limit {hi:g} ps" if hi else None)
    ax.set(xlabel="time from the PHI_B rising edge (ps)", ylabel="voltage (V)", title="Turn-on (worst edge)")
    ax.legend(loc="center right")
    ax = axs[1, 0]
    lim = soa.config()["limit_V"]
    ax.plot(t * 1e9, vg - vin, color=C1, lw=0.9, label="VG - VIN (gs)")
    ax.plot(t * 1e9, vg - bp, color=C7, lw=0.9, label="VG - BP (gd)")
    ax.plot(t * 1e9, bp - vin, color=C3, lw=0.9, label="BP - VIN (ds)")
    hline(ax, lim, f"SOA +{lim:.1f} V")
    hline(ax, -lim, f"SOA -{lim:.1f} V")
    ax.set(xlabel="time (ns)", ylabel="terminal voltage (V)", title="Reference switch MSWP over the whole run",
           ylim=(-1.25 * lim, 1.25 * lim))
    ax.legend(loc="lower left", ncol=3)
    if "soa_violations" in m:
        note(ax, f"BST-08: {m['soa_violations']} violation(s), scope {m['soa_scope']}\n"
             f"max |V| {m['soa_max_V']:.3f} V over {m['soa_devices']} device(s)", loc="upper right")
    else:
        note(ax, "BST-08 unverified", loc="upper right")
    ax = axs[1, 1]
    ax.plot(t * 1e9, vin, color=C3, lw=0.9, label="VIN")
    ax.plot(t * 1e9, vg, color=C1, lw=0.9, label="VG")
    ax.plot(t * 1e9, phb, color=C2, lw=0.9, label="PHI_B")
    ax.set(xlabel="time (ns)", ylabel="voltage (V)", title="Stimulus and gate")
    ax.legend(loc="upper left", ncol=3)
    spec_table(axs[1, 2], ctx, m, ["vgs_min_V", "vgs_var_mV", "t_off_ps", "t_on_ps", "iavg_uA", "soa_violations",
                                   "cin_phb_fF", "cin_phbb_fF"])
    fg.save(fig, "switch", "Boosted gate voltage over the input range, the worst turn-off and turn-on edge "
            "with their delays and limits, the three terminal voltages of the reference switch against the "
            "+/-1.0 V SOA limit, and the specification table.")
