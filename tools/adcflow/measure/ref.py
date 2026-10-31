"""adc_ref acceptance measurements (tb/ref/*)."""

from __future__ import annotations

import contextlib
import io
from dataclasses import replace
from pathlib import Path

import numpy as np

from .. import model, psf
from ..arch import Arch
from ..corners import supply_envelope
from ..figures import C1, C2, C3, C4, C7, GRID, INK2, LIMIT, hline, limits, note, sink_of, spec_table, vline
from ..specs import blocks
from .common import read_samples, spectrum, tran

# charge replay (tb_ref_replay): the system model converts a near-Nyquist sine with an
# ideal reference at TT timing; its per-conversion CDAC charges and decision instants
# are played into adc_ref, and the VREFP sampled at those instants goes back into the
# same model conversion
REPLAY_SEED = 11
REPLAY_TW = 20e-12            # width of every charge pulse (CDAC switch RC ~ 15 ps)


def _replay_ni() -> model.NonIdeal:
    return model.NonIdeal(ref_follower=None, ref_net=None, c_dec=1.0, ref_periodic=False, seed=REPLAY_SEED)


def replay_pattern(npts: int, nwarm: int, fin: float):
    """(arch, vin, dvdt, result) of the pattern conversion: nwarm + npts samples."""
    a = Arch.load()
    amp = a.fs_peak * 10 ** (-1 / 20)
    tn = (np.arange(nwarm + npts) - nwarm) / a.fs
    vin = amp * np.sin(2 * np.pi * fin * tn + 0.1)
    dvdt = amp * 2 * np.pi * fin * np.cos(2 * np.pi * fin * tn + 0.1)
    return a, vin, dvdt, model.convert(vin, a, _replay_ni(), dvdt=dvdt)


def replay_prepare(params: dict) -> dict:
    """Coherent fin for npts, and the load / sampling waveforms of tb_ref_replay."""
    from adctoolbox import find_coherent_frequency

    npts, nwarm = int(float(params.get("npts", 1024))), int(float(params.get("nwarm", 32)))
    a = Arch.load()
    target = min(float(params.pop("fin_target", 49.7e6)), (npts / 2 - 3) * a.fs / npts)
    with contextlib.redirect_stdout(io.StringIO()):
        fin, _ = find_coherent_frequency(a.fs, target, npts)
    params["fin"] = f"{fin:.9e}"
    _, _, _, r = replay_pattern(npts, nwarm, fin)
    tper = 1 / a.fs
    q0 = a.c_s * (a.vref - float(a.raw["reference"]["vin_cm"]))
    iload, trig, level = ["0 0"], ["0 0"], 0
    for m in range(nwarm + npts):
        t0 = (m + 1) * tper                      # conversion m: CLK falls at (m + 1) * 10 ns
        ev = [(r.info["t_ref"], q0)] + list(zip(r.info["t_sw"][m], r.info["q_sw"][m]))
        for t, q in ev:
            ts, i = t0 + t, q / REPLAY_TW
            iload += [f"{ts:.12e} 0", f"{ts + 2e-12:.12e} {i:.6e}", f"{ts + REPLAY_TW:.12e} {i:.6e}",
                      f"{ts + REPLAY_TW + 2e-12:.12e} 0"]
        for t in [r.info["t_ref"] - 10e-12] + list(r.info["t_dec"][m]):
            ts = t0 + t
            trig += [f"{ts - 0.5e-12:.12e} {level}", f"{ts + 0.5e-12:.12e} {1 - level}"]
            level = 1 - level
    params["_files"] = {"iload.pwl": "\n".join(iload) + "\n", "trig.pwl": "\n".join(trig) + "\n"}
    return params


def replay(job_dir: Path, ctx: dict) -> dict:
    p = ctx["params"]
    npts, nwarm, fin = int(float(p["npts"])), int(float(p["nwarm"])), float(p["fin"])
    s = read_samples(Path(job_dir) / "vdec.txt")
    n = nwarm + npts
    m: dict = {"n_samples": int(len(s))}
    if len(s) < 15 * n:
        m["error"] = f"only {len(s)} VREFP samples (expected {15 * n})"
        return m
    v = s[: 15 * n, 2].reshape(n, 15)
    pre, dec = v[:, 0], v[:, 1:]
    dv = dec - pre[nwarm:].mean()                # deviation from the recovered VREFP (gain-neutral)
    a, vin, dvdt, _ = replay_pattern(npts, nwarm, fin)
    with contextlib.redirect_stdout(io.StringIO()):
        r0 = model.convert(vin, a, replace(_replay_ni(), ref_trace=np.zeros_like(dv)), dvdt=dvdt)
        r1 = model.convert(vin, a, replace(_replay_ni(), ref_trace=dv), dvdt=dvdt)
        m0 = spectrum(r0.codes[nwarm:], a.fs, a.n_codes, ctx)
        m1 = spectrum(r1.codes[nwarm:], a.fs, a.n_codes, ctx)
    m["enob_ideal_ref"] = m0["enob"]
    m["enob_ref"] = m1["enob"]
    m["sfdr_ref_dBc"] = m1["sfdr_dBc"]
    m["enob_loss_bit"] = float(m0["enob"] - m1["enob"])
    d, w = dv[nwarm:], dv[nwarm:] - dv[nwarm:, -1:]
    m["tail_dev_uV"] = float(np.abs(w[:, 11:]).max() * 1e6)          # decisions 12..14 (no redundancy)
    tol = np.maximum(np.concatenate([a.redundancy(), [0.0]]), 0.25) * a.lsb * a.vref / a.fs_peak
    # REF-21: decisions with redundancy (k = 1 .. 11, delta_k >= 1); 12 .. 14 are REF-13
    ratio = env_ratios(a, w)
    m["env_ratio"] = float(ratio.max())
    m["env_ratio_per_decision"] = [round(float(x), 4) for x in ratio]
    m["env_ratio_decision"] = int(np.argmax(ratio)) + 1
    m["start_pp_uV"] = float(np.ptp(pre[nwarm:]) * 1e6)
    m["droop_max_mV"] = float(np.abs(d).max() * 1e3)
    m["vrefp_V"] = float(pre[nwarm:].mean())
    fg = sink_of(ctx)
    if fg:
        _fig_replay(fg, ctx, pre[nwarm:], d, w, tol, ratio, m)
    return m


def _dc(job_dir: Path, name: str) -> dict:
    f = psf.find(Path(job_dir) / "deck.raw", f"{name}.dc*")
    if f is None:
        raise FileNotFoundError(f"{name} results missing")
    return psf.read(f)


def dc(job_dir: Path, ctx: dict) -> dict:
    vref_in = float(ctx["globals"]["vref_in"])
    op = _dc(job_dir, "dcop")
    m = {"vrefp_err_mV": float((op["VREFP"][0] - vref_in) * 1e3),
         "vcm_V": float(op["VCM"][0]),
         "i18_uA": float(-op["VH:p"][0] * 1e6),
         "i09_uA": float(-op["VA:p"][0] * 1e6),
         "iin_uA": float(abs(op["VREF:p"][0]) * 1e6)}
    ld = _dc(job_dir, "dcload")
    m["loadreg_mV"] = float(abs(ld["VREFP"][0] - ld["VREFP"][-1]) * 1e3)
    ln = _dc(job_dir, "dcline")
    sweep = [k for k in ln if k not in ("VREFP", "VCM") and ":" not in k]
    x = ln[sweep[0]] if sweep else np.linspace(*supply_envelope("vdd18"), len(ln["VREFP"]))   # dcline of tb_ref_dc
    m["line_mV_per_V"] = float(abs(np.polyfit(x, ln["VREFP"], 1)[0]) * 1e3)
    fg = sink_of(ctx)
    if fg:
        _fig_dc(fg, ctx, vref_in, op, ld, x, ln, m)
    return m


NOISE_F_SPLIT = 10e3   # below: slow gain wander under the FFT resolution of a long record (no ENOB cost)


def startup_times() -> dict[str, float]:
    """Instants (s) of tb_ref_startup from adc_ref.yaml operating.power_up (issue #34), used by
    gen_tb.py for the stimulus and by `startup` for the windows: the supplies ramp together from
    sup0 to sup1, VREF_IN stays at 0 V for vref_dwell and ramps from ref0 to ref1, ready follows
    the end of the ramp by `ready`, the run ends 4 us after ready."""
    pu = blocks()["adc_ref"].raw["operating"]["power_up"]
    t = {"sup0": 0.1e-6}
    t["sup1"] = t["sup0"] + pu["supply_ramp"]
    t["ref0"] = t["sup1"] + pu["vref_dwell"]
    t["ref1"] = t["ref0"] + pu["vref_ramp"]
    t["ready"] = t["ref1"] + pu["ready"]
    t["stop"] = t["ready"] + 4e-6
    return t


def startup(job_dir: Path, ctx: dict) -> dict:
    """tb_ref_startup: VREFP / VCM excursions over the supported power-up, VREFP and VCM from ready on."""
    w = tran(job_dir)
    t, vp, vc, vin = w["time"], w["VREFP"], w["VCM"], w["VREF_IN"]
    ts = startup_times()
    m: dict = {"vrefp_max_V": float(vp.max()), "vrefp_min_V": float(vp.min()),
               "vcm_max_V": float(vc.max()), "vcm_min_V": float(vc.min()),
               "vrefp_max_t_us": float(t[np.argmax(vp)] * 1e6), "vcm_max_t_us": float(t[np.argmax(vc)] * 1e6)}
    if t[-1] < ts["stop"] - 1e-9:
        m["error"] = f"run ended at {t[-1] * 1e6:.3f} us, before {ts['stop'] * 1e6:g} us"
        return m
    dwell = (t >= ts["sup1"]) & (t <= ts["ref0"])          # supplies up, VREF_IN still 0 V
    m["vrefp_dwell_max_V"] = float(vp[dwell].max())
    m["vcm_dwell_max_V"] = float(vc[dwell].max())
    after = t >= ts["ready"]
    m["ready_err_mV"] = float(np.max(np.abs(vp[after] - vin[after])) * 1e3)          # REF-19
    lo, hi = limits(ctx, "vcm_ready_V")
    mid = (lo + hi) / 2 if lo is not None and hi is not None else 0.45
    m["vcm_ready_V"] = float(vc[after][np.argmax(np.abs(vc[after] - mid))])         # REF-20
    vend = float(vp[-1])
    m["ready_dev_mV"] = float(np.max(np.abs(vp[after] - vend)) * 1e3)
    m["vrefp_final_err_mV"] = float((vend - vin[-1]) * 1e3)
    m["vcm_final_V"] = float(vc[-1])
    ramp = (t >= ts["ref0"]) & (t <= ts["ref1"])
    m["ramp_lag_mV"] = float(np.max(np.abs(vp[ramp] - vin[ramp])) * 1e3)
    tol = (limits(ctx, "ready_err_mV")[1] or 5.0) * 1e-3
    out = (t >= ts["ref1"]) & (np.abs(vp - vin) > tol)
    m["t_settle_us"] = float(((t[out][-1] if out.any() else ts["ref1"]) - ts["ref1"]) * 1e6)
    fg = sink_of(ctx)
    if fg:
        _fig_startup(fg, ctx, w, ts, m, mid)
    return m


def noise(job_dir: Path, ctx: dict) -> dict:
    """VREFP / VCM noise: above NOISE_F_SPLIT (the part ENOB sees), below it, and in total."""
    m = {}
    psd = {}
    for name, key in (("noise1", "noise_uV"), ("noise2", "vcm_noise_uV")):
        f = psf.find(Path(job_dir) / "deck.raw", f"{name}.noise*")
        if f is None:
            continue
        d = psf.read(f)
        freq = d.get("freq")
        out = d.get("out")
        if freq is None or out is None:
            continue
        freq, p = np.asarray(freq, float), np.abs(out) ** 2
        fg = np.concatenate([freq[freq < NOISE_F_SPLIT], [NOISE_F_SPLIT], freq[freq > NOISE_F_SPLIT]])
        pg = np.exp(np.interp(np.log(fg), np.log(freq), np.log(np.maximum(p, 1e-60))))
        lo = fg <= NOISE_F_SPLIT
        m[key] = float(np.sqrt(np.trapezoid(pg[~lo | (fg == NOISE_F_SPLIT)], fg[~lo | (fg == NOISE_F_SPLIT)])) * 1e6)
        m[key.replace("_uV", "_lf_uV")] = float(np.sqrt(np.trapezoid(pg[lo], fg[lo])) * 1e6)
        m[key.replace("_uV", "_total_uV")] = float(np.sqrt(np.trapezoid(p, freq)) * 1e6)
        psd[key] = (freq, p)
    fg = sink_of(ctx)
    if fg and "noise_uV" in psd:
        _fig_noise(fg, ctx, psd, m)
    return m


# ------------------------------------------------------------------ figures
def _fig_dc(fg, ctx, vref_in, op, ld, x, ln, m) -> None:
    fig, axs = fg.new(2, 2, size=(11.2, 7.4))
    il = np.asarray(ld["iload"]) * 1e6
    ax = axs[0, 0]
    ax.plot(il, ld["VREFP"] * 1e3, "o-", color=C1, ms=5, label="VREFP")
    lo, hi = limits(ctx, "vrefp_err_mV")
    if lo is not None and hi is not None:
        ax.axhspan(vref_in * 1e3 + lo, vref_in * 1e3 + hi, color=GRID, alpha=0.7,
                   label=f"VREF_IN {vref_in * 1e3:.0f} mV, window {lo:g} .. +{hi:g} mV")
    iop = blocks()["adc_ref"].raw["operating"]["load_vrefp_dc"] * 1e6      # the tb's iload (gen_tb)
    ax.plot([iop], [op["VREFP"][0] * 1e3], "s", color=C2, ms=7,
            label=f"operating point ({iop:g} uA), error {m['vrefp_err_mV']:.2f} mV")
    ax.set(xlabel="load current (uA)", ylabel="VREFP (mV)", title="Load regulation")
    ax.legend(loc="lower left", fontsize=7.5)
    note(ax, f"{m['loadreg_mV']:.2f} mV over {il.min():g} .. {il.max():g} uA (reported)", loc="upper right")
    ax = axs[0, 1]
    ax.plot(x, ln["VREFP"] * 1e3, "o-", color=C1, ms=5, label="VREFP")
    hi = limits(ctx, "line_mV_per_V")[1]
    if hi is not None:
        x0, y0 = float(np.mean(x)), float(np.mean(ln["VREFP"])) * 1e3
        ax.plot(x, y0 + hi * (np.asarray(x) - x0), color=LIMIT, ls="--", lw=1.1,
                label=f"slope at the limit ({hi:g} mV/V)")
    ax.set(xlabel="AVDD18 (V)", ylabel="VREFP (mV)", title="Supply sensitivity")
    ax.legend(loc="upper left", fontsize=7.5)
    note(ax, f"{m['line_mV_per_V']:.3f} mV/V", loc="lower right")
    ax = axs[1, 0]
    ax.plot(il, ld["VCM"] * 1e3, "o-", color=C7, ms=5)
    lo, hi = limits(ctx, "vcm_V")
    if lo is not None and hi is not None:
        ax.axhspan(lo * 1e3, hi * 1e3, color=GRID, alpha=0.7, label=f"window {lo * 1e3:g} .. {hi * 1e3:g} mV")
        ax.legend(loc="lower left", fontsize=7.5)
    ax.set(xlabel="load current (uA)", ylabel="VCM (mV)", title="Common-mode voltage")
    note(ax, f"operating point {m['vcm_V'] * 1e3:.1f} mV", loc="upper right")
    spec_table(axs[1, 1], ctx, m, ["vrefp_err_mV", "vcm_V", "line_mV_per_V", "iin_uA"])
    axs[1, 1].text(0.0, 0.42, "supply currents at the operating point (reported):\n"
                   f"AVDD18 branch {m['i18_uA']:.1f} uA, AVDD branch {m['i09_uA']:.1f} uA", fontsize=8,
                   color=INK2, transform=axs[1, 1].transAxes, va="top")
    fg.save(fig, "dc", "VREFP against load current and against the 1.8 V supply, VCM against load, and the "
            "operating-point values against their limits.")


def _fig_startup(fg, ctx, w, ts, m, vcm_mid) -> None:
    t, vp, vc, vin = w["time"], w["VREFP"], w["VCM"], w["VREF_IN"]
    us = t * 1e6
    fig, axs = fg.new(2, 3, size=(15.0, 7.4))
    ax = axs[0, 0]
    for n, c in (("AVDD18", C4), ("AVDD", INK2)):
        if n in w:
            ax.plot(us, w[n], color=c, lw=1.0, ls="--", label=n)
    ax.plot(us, vin, color=C3, lw=1.0, label="VREF_IN")
    ax.plot(us, vp, color=C1, lw=1.3, label="VREFP")
    ax.plot(us, vc, color=C7, lw=1.3, label="VCM")
    hi, lo = limits(ctx, "vrefp_max_V")[1], limits(ctx, "vrefp_min_V")[0]
    hline(ax, hi, f"limit {hi:g} V" if hi is not None else None)
    hline(ax, lo, f"limit {lo:g} V" if lo is not None else None)
    vline(ax, ts["ready"] * 1e6, "ready", color=INK2)
    ax.set(xlabel="time (us)", ylabel="voltage (V)", title="Supported power-up sequence")
    ax.legend(loc="center right", fontsize=7.5)
    note(ax, f"VREFP {m['vrefp_min_V']:.3f} .. {m['vrefp_max_V']:.3f} V\n"
         f"VCM {m['vcm_min_V']:.3f} .. {m['vcm_max_V']:.3f} V", loc="upper left")
    ax = axs[0, 1]
    sel = t <= ts["ref0"] + 0.5e-6
    for n, c in (("AVDD18", C4), ("AVDD", INK2)):
        if n in w:
            ax.plot(us[sel], w[n][sel] * 1e3, color=c, lw=1.0, ls="--", label=n)
    ax.plot(us[sel], vin[sel] * 1e3, color=C3, lw=1.0, label="VREF_IN")
    ax.plot(us[sel], vp[sel] * 1e3, color=C1, lw=1.3, label="VREFP")
    ax.plot(us[sel], vc[sel] * 1e3, color=C7, lw=1.3, label="VCM")
    ax.axvspan(ts["sup1"] * 1e6, ts["ref0"] * 1e6, color=GRID, alpha=0.5, label="VREF_IN 0 V, supplies up")
    ax.set(xlabel="time (us)", ylabel="voltage (mV)", title="Supplies up, no reference yet",
           ylim=(-50, max(100.0, m["vrefp_dwell_max_V"] * 1.3e3, m["vcm_dwell_max_V"] * 1.3e3)))
    ax.legend(loc="upper right", fontsize=7.0)
    note(ax, f"during the dwell: VREFP <= {m['vrefp_dwell_max_V'] * 1e3:.3g} mV, VCM <= {m['vcm_dwell_max_V'] * 1e3:.3g} mV",
         loc="lower right")
    ax = axs[0, 2]
    ax.plot(us, (vp - vin) * 1e3, color=C1, lw=1.0, label="VREFP - VREF_IN")
    ax.plot(us, (vc - vin / 2) * 1e3, color=C7, lw=1.0, label="VCM - VREF_IN / 2")
    for k in ("ref0", "ref1"):
        vline(ax, ts[k] * 1e6, None, color=GRID)
    ax.set(xlabel="time (us)", ylabel="error (mV)", title="Tracking of VREF_IN")
    ax.legend(loc="lower right", fontsize=7.5)
    note(ax, f"largest |VREFP - VREF_IN| during the ramp {m['ramp_lag_mV']:.3g} mV", loc="upper left")
    ax = axs[1, 0]
    sel = t >= ts["ref1"] - 0.5e-6
    ax.plot(us[sel], (vp[sel] - vin[sel]) * 1e3, color=C1, lw=1.2)
    tol = limits(ctx, "ready_err_mV")[1]
    if tol is not None:
        ax.axhspan(-tol, tol, color=GRID, alpha=0.6, label=f"+/-{tol:g} mV (REF-19)")
        ax.legend(loc="lower right", fontsize=7.5)
    vline(ax, ts["ready"] * 1e6, "ready", color=LIMIT)
    vline(ax, ts["ref1"] * 1e6 + m["t_settle_us"], f"within {tol or 5:g} mV", color=C3, y=0.6)
    span = max(m["ready_err_mV"], tol or 5.0) * 2
    ax.set(xlabel="time (us)", ylabel="VREFP - VREF_IN (mV)", title="VREFP after the VREF_IN ramp",
           ylim=(-span, span))
    note(ax, f"from ready on: {m['ready_err_mV']:.3g} mV\nwithin the band {m['t_settle_us']:.3g} us after the ramp",
         loc="upper left")
    ax = axs[1, 1]
    ax.plot(us[sel], vc[sel] * 1e3, color=C7, lw=1.2)
    lo, hi = limits(ctx, "vcm_ready_V")
    if lo is not None and hi is not None:
        ax.axhspan(lo * 1e3, hi * 1e3, color=GRID, alpha=0.6, label=f"{lo * 1e3:g} .. {hi * 1e3:g} mV (REF-20)")
        ax.legend(loc="lower right", fontsize=7.5)
    vline(ax, ts["ready"] * 1e6, "ready", color=LIMIT)
    ax.set(xlabel="time (us)", ylabel="VCM (mV)", title="VCM after the VREF_IN ramp",
           ylim=(vcm_mid * 1e3 - 25, vcm_mid * 1e3 + 25))
    note(ax, f"from ready on, furthest from {vcm_mid * 1e3:g} mV: {m['vcm_ready_V'] * 1e3:.2f} mV", loc="upper left")
    spec_table(axs[1, 2], ctx, m, ["vrefp_max_V", "vrefp_min_V", "vcm_max_V", "vcm_min_V", "ready_err_mV",
                                   "vcm_ready_V"])
    axs[1, 2].text(0.0, 0.42, "reported:\n"
                   f"VREFP(end) - VREF_IN {m['vrefp_final_err_mV']:.2f} mV, VCM(end) {m['vcm_final_V'] * 1e3:.1f} mV\n"
                   f"max |VREFP - VREFP(end)| from ready {m['ready_dev_mV']:.3g} mV", fontsize=8,
                   color=INK2, transform=axs[1, 2].transAxes, va="top")
    fg.save(fig, "startup", "Supplies, VREF_IN, VREFP and VCM over the supported power-up sequence against the "
            f"{limits(ctx, 'vrefp_min_V')[0]:g} .. {limits(ctx, 'vrefp_max_V')[1]:g} V window, the outputs while the supplies are up and VREF_IN is still 0 V, the tracking "
            "error during the VREF_IN ramp, VREFP against VREF_IN and VCM against its range after the ramp with the "
            "ready instant, and the specification table.")


def _fig_noise(fg, ctx, psd, m) -> None:
    fig, axs = fg.new(1, 2, size=(11.2, 4.1))
    ax = axs[0, 0]
    freq = psd["noise_uV"][0]
    for key, name, c in (("noise_uV", "VREFP", C1), ("vcm_noise_uV", "VCM", C7)):
        if key in psd and np.max(psd[key][1]) > 1e-40:
            ax.loglog(psd[key][0], np.sqrt(psd[key][1]) * 1e9, color=c, label=name)
    dens = np.sqrt(psd["noise_uV"][1]) * 1e9
    ax.set_ylim(dens.min() / 3, dens.max() * 3)
    ax.axvspan(freq.min(), NOISE_F_SPLIT, color=GRID, alpha=0.7)
    vline(ax, NOISE_F_SPLIT, "10 kHz: integration starts", color=INK2)
    ax.set(xlabel="frequency (Hz)", ylabel="noise density (nV/sqrt(Hz))", title="Output noise spectral density")
    ax.legend(loc="lower left")
    ax = axs[0, 1]
    p = psd["noise_uV"][1]
    sel = freq >= NOISE_F_SPLIT
    f, pp = freq[sel], p[sel]
    cum = np.sqrt(np.concatenate([[0.0], np.cumsum(0.5 * (pp[1:] + pp[:-1]) * np.diff(f))])) * 1e6
    ax.semilogx(f, cum, color=C1, label="VREFP, integrated from 10 kHz")
    hi = limits(ctx, "noise_uV")[1]
    hline(ax, hi, f"limit {hi:g} uV" if hi else None)
    ax.set(xlabel="upper integration limit (Hz)", ylabel="integrated rms noise (uV)",
           title="Integrated noise", ylim=(0, max(hi or 0, cum.max()) * 1.25))
    note(ax, f"10 kHz .. 100 GHz: {m['noise_uV']:.1f} uV\n1 .. 10 kHz: {m['noise_lf_uV']:.1f} uV (not in the spec)",
         loc="center left")
    ax.legend(loc="lower right")
    fg.save(fig, "psd", "Noise spectral density of VREFP and VCM with the 10 kHz start of the integration "
            "band, and the integrated rms noise against the limit.")


def env_ratios(a: Arch, w: np.ndarray) -> np.ndarray:
    """REF-21: per decision k with redundancy (delta_k >= 1, k = 1 .. 11), the largest |VREFP(k) - VREFP(14)|
    over the record (``w``: conversions x 14 decisions, V) divided by tolerance_k = delta_k * LSB * VREF / FS,
    the VREFP error that a full-scale DAC level turns into a delta_k LSB decision error."""
    red = a.redundancy()
    n = int(np.sum(red >= 1))
    return np.abs(w[:, :n]).max(0) / (red[:n] * a.lsb * a.vref / a.fs_peak)


def _fig_replay(fg, ctx, pre, d, w, tol, ratio, m) -> None:
    fig, axs = fg.new(2, 3, size=(16.0, 7.4))
    k = np.arange(1, w.shape[1] + 1)
    kd = k[:-1]                                   # decision 14 is the reference of the deviation
    ax = axs[0, 0]
    for row in w[:: max(len(w) // 60, 1)]:
        ax.semilogy(kd, np.maximum(np.abs(row[:-1]) * 1e3, 1e-4), color=C1, lw=0.5, alpha=0.3)
    ax.semilogy(kd, np.maximum(np.abs(w[:, :-1]).max(0) * 1e3, 1e-4), "o-", color=C1, ms=3.5,
                label="max over all conversions")
    ax.step(kd, tol[:-1] * 1e3, where="mid", color=INK2, lw=1.6, label="allowed by the redundancy (or 0.25 LSB)")
    lim = limits(ctx, "tail_dev_uV")[1]
    if lim is not None:
        ax.plot([12, 13], [lim * 1e-3] * 2, color=LIMIT, ls="--", lw=1.3, label=f"limit {lim:g} uV, decisions 12 .. 14")
    ax.set(xlabel="decision k", ylabel="|VREFP(k) - VREFP(14)| (mV)", ylim=(1e-3, 300),
           title="VREFP at the decision instants")
    ax.set_xticks(kd)
    ax.legend(loc="upper right", fontsize=7.5)
    ax = axs[0, 1]
    kr = np.arange(1, len(ratio) + 1)
    ax.bar(kr, ratio, color=[LIMIT if r > 1 else C1 for r in ratio], width=0.6)
    hi = limits(ctx, "env_ratio")[1]
    hline(ax, hi if hi is not None else 1.0, f"limit {hi:g} (REF-21)" if hi is not None else "1")
    ax.set(xlabel="decision k (redundancy >= 1 LSB)", ylabel="max |VREFP(k) - VREFP(14)| / tolerance_k",
           title="REF-21: deviation over the redundancy tolerance", ylim=(0, max(1.2, ratio.max() * 1.15)))
    ax.set_xticks(kr)
    note(ax, f"env_ratio {m['env_ratio']:.2f} at decision {m['env_ratio_decision']}\n"
             "tolerance_k = delta_k x LSB x VREF / FS", loc="upper left")
    ax = axs[0, 2]
    ax.plot(np.arange(1, len(pre) + 1), (pre - pre.mean()) * 1e6, color=C3, lw=0.9)
    hi = limits(ctx, "start_pp_uV")[1]
    if hi is not None:
        ax.axhspan(-hi / 2, hi / 2, color=GRID, alpha=0.7, label=f"limit: {hi:g} uV peak-to-peak")
        ax.legend(loc="upper right", fontsize=7.5)
    ax.set(xlabel="conversion", ylabel="VREFP before the conversion start (uV)", title="Memory between conversions")
    note(ax, f"peak-to-peak {m['start_pp_uV']:.1f} uV", loc="lower left")
    ax = axs[1, 0]
    ax.fill_between(k, d.min(0) * 1e3, d.max(0) * 1e3, color=C1, alpha=0.25, label="min .. max over conversions")
    ax.plot(k, d.mean(0) * 1e3, "o-", color=C1, ms=3.5, label="mean")
    ax.set(xlabel="decision k", ylabel="VREFP - recovered VREFP (mV)", title="Droop during the conversion")
    ax.set_xticks(k)
    ax.legend(loc="lower left", fontsize=7.5)
    note(ax, f"largest drop {m['droop_max_mV']:.1f} mV", loc="upper right")
    axs[1, 2].axis("off")
    spec_table(axs[1, 1], ctx, m, ["enob_loss_bit", "tail_dev_uV", "start_pp_uV", "env_ratio"])
    axs[1, 1].text(0.0, 0.62, f"ENOB with an ideal reference {m['enob_ideal_ref']:.2f} bit\n"
                   f"ENOB with the simulated VREFP {m['enob_ref']:.2f} bit, SFDR {m['sfdr_ref_dBc']:.1f} dBc\n"
                   f"recovered VREFP {m['vrefp_V']:.4f} V", fontsize=8, color=INK2,
                   transform=axs[1, 1].transAxes, va="top")
    fg.save(fig, "replay", "VREFP deviation at each decision against the redundancy tolerance envelope, the "
            "per-decision ratio to the tolerance against its limit (REF-21), the memory of VREFP before each "
            "conversion, the droop during a conversion, and the ENOB cost.")
