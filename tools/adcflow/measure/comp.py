"""adc_comp acceptance measurements (tb/comp/*)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .. import psf
from ..figures import C1, C2, C3, INK2, LIMIT, MUTED, hline, limit_label, limits, note, sink_of, vline
from ..figures import GRID as GRIDLINE
from .common import fig_cin, pin_cins, read_meters, read_samples, tran

TCYC = 400e-12
DELAY_LEVELS = [100e-3, -100e-3, 30e-3, -30e-3, 10e-3, -10e-3, 3e-3, -3e-3, 1e-3, -1e-3,
                300e-6, -300e-6, 100e-6, -100e-6, 30e-6, -30e-6, 10e-6, -10e-6]
NOISE_LEVELS = [round(-800e-6 + 100e-6 * i, 9) for i in range(17)]   # +/-3.3 sigma at the 240 uV limit
NOISE_REPEAT = 512                    # 1-sigma error of sigma <= 2.7 % for 120..300 uV (binomial ML)
# tb_comp_offset_mc: offset search per Monte Carlo sample (tb_offset_search_va)
MC_TCYC = 1e-9                        # one decision per 1 ns: no metastable miss even within 1 uV of the offset
MC_RANGE = 25e-3                      # search range +/-25 mV (5 sigma at the CMP-03 limit)
MC_BITS = 13                          # 50 mV / 2^13 = 6.1 uV
MC_CHECK = 50e-6                      # re-check of the result at +/-50 uV
MC_VOS_BEH = 2e-3                     # behavioral stand-in for device mismatch (not a design value)
# status of a sample: R-line codes of tb_offset_search_va, and what the measurement adds
MC_STATUS = {0: "ok", 1: "out of range", 2: "no valid decision", 3: "re-check failed", 4: "search incomplete"}
MC_ABORTED, MC_MISSING = "simulation aborted", "missing"


def delay(job_dir: Path, ctx: dict) -> dict:
    vdd = float(ctx["globals"]["vdd"])
    w = tran(job_dir)
    t = w["time"]
    clk, op, on = w["CLKC"], w["OUTP"], w["OUTN"]
    vds = DELAY_LEVELS * 2
    t_rise = psf.crossings(t, clk, vdd / 2, +1)
    t_fall = psf.crossings(t, clk, vdd / 2, -1)
    op_r = psf.crossings(t, op, vdd / 2, +1)
    on_r = psf.crossings(t, on, vdd / 2, +1)
    delays, wrong, pts = {}, 0, []
    for k, tc in enumerate(t_rise[: len(vds)]):
        win = tc + TCYC / 2
        p = op_r[(op_r > tc) & (op_r < win)]
        n = on_r[(on_r > tc) & (on_r < win)]
        if len(p) == 0 and len(n) == 0:
            if abs(vds[k]) >= 100e-6:
                wrong += 1
            continue
        if len(p) and (not len(n) or p[0] < n[0]):
            dec, td = 1, p[0] - tc
        else:
            dec, td = 0, n[0] - tc
        if abs(vds[k]) >= 100e-6 and dec != (vds[k] > 0):
            wrong += 1
        delays.setdefault(abs(vds[k]), []).append(td)
        pts.append((k, vds[k], td))
    m = {"wrong_decisions": wrong}
    if 1e-3 in delays:
        m["tdelay_1mV_ps"] = float(np.mean(delays[1e-3]) * 1e12)
    if 30e-3 in delays:
        m["tdelay_30mV_ps"] = float(np.mean(delays[30e-3]) * 1e12)
    small = sorted(v for v in delays if v <= 1e-3)
    if len(small) >= 3:
        x = np.log(1 / np.asarray(small))
        y = np.asarray([np.mean(delays[v]) for v in small])
        m["tau_reg_ps"] = float(np.polyfit(x, y, 1)[0] * 1e12)
    # reset: CLKC fall -> both outputs below 10 % VDD
    resets = []
    hi = np.maximum(op, on)
    for tf in t_fall[: len(vds)]:
        idx = np.nonzero((t > tf) & (t < tf + TCYC / 2) & (hi < 0.1 * vdd))[0]
        if len(idx):
            resets.append(t[idx[0]] - tf)
    if resets:
        m["treset_ps"] = float(np.max(resets) * 1e12)
    meters = read_meters(Path(job_dir) / "power.txt")
    if "AVDD" in meters:
        m["energy_fJ"] = float(meters["AVDD"] * vdd * TCYC * 1e15)
    fg = sink_of(ctx)
    if fg:
        _fig_delay(fg, ctx, w, vdd, vds, t_rise, t_fall, pts, m)
    return m


def probit_fit(vd, k, n) -> dict:
    """Binomial maximum-likelihood probit fit of P(OUTP = 1) = Phi((vd - mu) / sigma).

    ``k`` of ``n`` decisions were OUTP = 1 at each level ``vd`` (V). Returns mu, sigma
    (V) and the 95 % profile-likelihood interval of sigma (mu re-optimised at every
    sigma; 2 * delta log L = 3.84), or {"error": ...}.
    """
    from scipy.optimize import brentq, minimize, minimize_scalar
    from scipy.stats import chi2, norm

    vd, k, n = (np.asarray(x, dtype=float) for x in (vd, k, n))

    def nll(mu, sig):
        z = (vd - mu) / sig
        return -float(np.sum(k * norm.logcdf(z) + (n - k) * norm.logcdf(-z)))

    # start from the empirical CDF: the 16 / 50 / 84 % crossings
    p = np.maximum.accumulate(k / np.maximum(n, 1))
    q16, q50, q84 = (float(np.interp(x, p + np.arange(p.size) * 1e-9, vd)) for x in (0.16, 0.5, 0.84))
    sig0 = max((q84 - q16) / 2, float(np.min(np.diff(vd))) / 4)
    x0 = [q50 * 1e6, np.log(sig0)]
    for _ in range(3):        # restart from the last point: Nelder-Mead may stop early on the flat log-sigma axis
        r = minimize(lambda x: nll(x[0] * 1e-6, np.exp(x[1])), x0, method="Nelder-Mead",
                     options={"xatol": 1e-7, "fatol": 1e-10, "maxiter": 4000})
        if r.success and np.allclose(r.x, x0, rtol=0, atol=1e-6):
            break
        x0 = r.x
    if not (r.success and np.isfinite(r.fun)):
        return {"error": f"probit fit did not converge: {r.message}"}
    mu, sig = r.x[0] * 1e-6, float(np.exp(r.x[1]))
    l0, span = r.fun, float(np.ptp(vd))

    def excess(s_):       # 2 * (profile negative log-likelihood - minimum) - chi2(1) 95 % point
        q = minimize_scalar(lambda m_: nll(m_, s_), bounds=(mu - span, mu + span), method="bounded",
                            options={"xatol": 1e-10})
        return 2 * (min(q.fun, nll(mu, s_)) - l0) - chi2.ppf(0.95, 1)

    lo = brentq(excess, sig * 0.3, sig, xtol=1e-11) if excess(sig * 0.3) > 0 else float("nan")
    hi = brentq(excess, sig, sig * 3.0, xtol=1e-11) if excess(sig * 3.0) > 0 else float("nan")
    return {"mu": mu, "sigma": sig, "ci95": (lo, hi)}


def noise(job_dir: Path, ctx: dict) -> dict:
    s = read_samples(Path(job_dir) / "decisions.txt")
    t, v = s[:, 1], s[:, 2]
    level = np.floor((t - 100e-12) / (TCYC * NOISE_REPEAT)).astype(int)
    vd = np.asarray(NOISE_LEVELS)
    n = np.array([np.sum(level == i) for i in range(len(vd))])
    k = np.array([np.sum(v[level == i] > 0) for i in range(len(vd))])
    ok = n > 0
    m = {"p1": [round(float(k_ / n_), 4) if n_ else None for k_, n_ in zip(k, n)],
         "n_per_level": int(n.max()) if n.size else 0}
    f = probit_fit(vd[ok], k[ok], n[ok])
    if "error" in f:
        m["error"] = f["error"]
        return m
    mu, sig = f["mu"], f["sigma"]
    m["noise_uV"] = float(sig * 1e6)
    m["noise_ci95_uV"] = [round(float(x) * 1e6, 2) for x in f["ci95"]]
    m["offset_abs_mV"] = float(abs(mu) * 1e3)
    m["offset_mV"] = float(mu * 1e3)
    fg = sink_of(ctx)
    if fg:
        _fig_noise(fg, ctx, vd[ok], k[ok] / n[ok], mu, sig, int(n.max()), f["ci95"])
    return m


def read_offset_samples(path: Path, runs: int, firstrun: int = 1) -> list[dict]:
    """The samples of one tb_comp_offset_mc run in iteration order, from the file that
    tb_offset_search_va appends to (one B ... R block per sample; the montecarlo analysis runs
    its iterations in order in one process, so block k is iteration firstrun + k - 1).

    Every one of the `runs` samples is returned: {run, status, offset (V, None unless ok), lo,
    hi, search: [(cycle, vd, decision)]}; a block without its R line is MC_ABORTED (the
    transient stopped), a sample without a block MC_MISSING. More blocks than runs is an error
    (the file is not of this run)."""
    blocks: list[dict] = []
    text = Path(path).read_text() if Path(path).exists() else ""
    for line in text.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == "B":
            blocks.append({"status": MC_ABORTED, "offset": None, "lo": None, "hi": None, "search": []})
        elif not blocks:
            raise ValueError(f"{Path(path).name}: {f[0]} line before the first sample")
        elif f[0] == "D":
            blocks[-1]["search"].append((int(f[1]), float(f[2]), int(f[3])))
        elif f[0] == "R":
            st = int(f[1])
            b = blocks[-1]
            b.update(status=MC_STATUS.get(st, f"status {st}"), lo=float(f[3]), hi=float(f[4]))
            if st == 0:
                b["offset"] = float(f[2])
    if len(blocks) > runs:
        raise ValueError(f"{Path(path).name}: {len(blocks)} samples for {runs} Monte Carlo runs")
    blocks += [{"status": MC_MISSING, "offset": None, "lo": None, "hi": None, "search": []}
               for _ in range(runs - len(blocks))]
    return [{"run": firstrun + i, **b} for i, b in enumerate(blocks)]


def offset_stats(samples: list[dict]) -> dict:
    """Metrics of the samples: offset_sigma_mV = sample standard deviation (n - 1) of the valid
    offsets, their mean and largest magnitude, mc_runs / mc_ok / mc_failed (failed and missing
    samples are counted, never dropped: Spec.judge fails a Monte Carlo spec on any of them), the
    reasons of the failures, and the offset (mV, None when failed) and status of every sample."""
    ok = np.array([s["offset"] for s in samples if s["status"] == "ok"], dtype=float)
    m = {"mc_runs": len(samples), "mc_ok": int(ok.size), "mc_failed": len(samples) - int(ok.size)}
    if ok.size >= 2:
        m["offset_sigma_mV"] = float(np.std(ok, ddof=1) * 1e3)
    if ok.size:
        m["offset_mean_mV"] = float(np.mean(ok) * 1e3)
        m["offset_max_abs_mV"] = float(np.max(np.abs(ok)) * 1e3)
    reasons: dict[str, int] = {}
    for s in samples:
        if s["status"] != "ok":
            reasons[s["status"]] = reasons.get(s["status"], 0) + 1
    if reasons:
        m["mc_fail_reasons"] = reasons
    m["offsets_mV"] = [None if s["offset"] is None else round(s["offset"] * 1e3, 6) for s in samples]
    m["sample_status"] = [s["status"] for s in samples]
    return m


def offset_mc(job_dir: Path, ctx: dict) -> dict:
    """tb_comp_offset_mc: the offset of every Monte Carlo sample and their spread (CMP-03)."""
    mc = ctx.get("mc") or {}
    runs = int(mc.get("runs") or ctx["params"].get("mc_runs") or 0)
    samples = read_offset_samples(Path(job_dir) / "offset.txt", runs, int(mc.get("firstrun") or 1))
    m = offset_stats(samples)
    head = next((s["search"] for s in samples if s["search"]), None)
    ctx.setdefault("provenance", {})["offset_search"] = {
        "method": "successive approximation per sample (tb_offset_search_va), transient noise off",
        "range_mV": MC_RANGE * 1e3, "bits": MC_BITS, "lsb_uV": round(2 * MC_RANGE / 2 ** MC_BITS * 1e6, 3),
        "recheck_uV": MC_CHECK * 1e6, "cycle_ns": MC_TCYC * 1e9,
        "sigma": "sample standard deviation (n - 1) of the valid samples; any failed sample fails the spec"}
    fg = sink_of(ctx)
    if fg and head is not None:
        _fig_offset_mc(fg, ctx, samples, m)
    return m


def kickback(job_dir: Path, ctx: dict) -> dict:
    s = read_samples(Path(job_dir) / "vdiff.txt")
    vd = s[:, 2]
    m = {}
    if len(vd) >= 3:
        m["kickback_uV"] = float(np.max(np.abs(np.diff(vd[1:]))) * 1e6)
        m["vdiff_uV"] = [round(float(x) * 1e6, 3) for x in vd]
    ac = psf.read(psf.find(Path(job_dir) / "deck.raw", "ac1.ac*"))
    i = ac.get("VAC:p")
    if i is not None:
        m["cin_fF"] = float(abs(np.imag(i[0])) / (2 * np.pi * 100e6) * 1e15)
    cins = pin_cins(tran(job_dir), float(ctx["globals"]["vdd"]), {"cin_clkc_fF": ("CLKC", "QCK")})
    m.update({k: float(c.mean() * 1e15) for k, c in cins.items() if len(c)})
    fg = sink_of(ctx)
    if fg and "vdiff_uV" in m:
        _fig_kickback(fg, ctx, m)
    if fg:
        fig_cin(fg, ctx, cins, [("cin_clkc_fF", "CLKC", "cin_clkc_fF")])
    return m


# ------------------------------------------------------------------ figures
def _fig_delay(fg, ctx, w, vdd, vds, t_rise, t_fall, pts, m) -> None:
    t, clk, op, on = w["time"], w["CLKC"], w["OUTP"], w["OUTN"]
    fig, axs = fg.new(1, 3, size=(15.0, 3.9))
    ax = axs[0, 0]
    k_, vd_, td_ = (np.asarray(x) for x in zip(*pts))
    for sign, c, name in ((1, C1, "vd > 0"), (-1, C2, "vd < 0")):
        sel = np.sign(vd_) == sign
        ax.semilogx(np.abs(vd_[sel]), td_[sel] * 1e12, "o", ms=5, mfc="none", color=c, label=name)
    small = [v for v in sorted(set(np.abs(vd_))) if v <= 1e-3]
    if "tau_reg_ps" in m and len(small) >= 3:
        y = [np.mean(td_[np.abs(vd_) == v]) for v in small]
        b0, a0 = np.polyfit(np.log(1 / np.asarray(small)), y, 1)
        xs = np.logspace(-5, -3, 20)
        ax.semilogx(xs, (a0 + b0 * np.log(1 / xs)) * 1e12, color=MUTED, lw=1.2,
                    label=f"fit t0 + tau ln(1/|vd|), tau = {m['tau_reg_ps']:.1f} ps")
    for metric, at, what in (("tdelay_1mV_ps", 1e-3, "1 mV"), ("tdelay_30mV_ps", 30e-3, "30 mV")):
        hi = limits(ctx, metric)[1]
        if hi is not None:
            ax.plot([at], [hi], "v", color=LIMIT, ms=7, label=f"limit {hi:g} ps at {what}")
    ax.set(xlabel="|vd| (V)", ylabel="CLKC rise -> output rise (ps)", title="Decision delay vs input")
    ax.legend(loc="upper right", fontsize=7.5)
    # transient of the +1 mV decision and the reset after it
    cand = [x for x in pts if x[1] > 0 and abs(x[1] - 1e-3) < 1e-9]
    if cand:
        k1, _, td = cand[0]
        tr, tf = t_rise[k1], t_fall[k1]
        ax = axs[0, 1]
        sel = (t > tr - 30e-12) & (t < tr + 150e-12)
        for sig, c, name in ((clk, C1, "CLKC"), (op, C3, "OUTP"), (on, C2, "OUTN")):
            ax.plot((t[sel] - tr) * 1e12, sig[sel], color=c, label=name)
        ax.annotate("", (td * 1e12, vdd / 2), (0, vdd / 2), arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.1))
        ax.text(td * 5e11, vdd / 2 + 0.03, f"{td * 1e12:.0f} ps", ha="center", fontsize=8, color=INK2)
        ax.axhline(vdd / 2, color=GRIDLINE, lw=0.8)
        ax.set(xlabel="time from CLKC rise (ps)", ylabel="voltage (V)", title="Decision at vd = +1 mV")
        ax.legend(loc="center right")
        ax = axs[0, 2]
        sel = (t > tf - 30e-12) & (t < tf + 90e-12)
        for sig, c, name in ((clk, C1, "CLKC"), (op, C3, "OUTP"), (on, C2, "OUTN")):
            ax.plot((t[sel] - tf) * 1e12, sig[sel], color=c, label=name)
        ax.axhline(0.1 * vdd, color=GRIDLINE, lw=0.8)
        ax.text(88, 0.1 * vdd + 0.02, "10 % VDD", ha="right", fontsize=7.5, color=MUTED)
        idx = np.nonzero((t > tf) & (t < tf + 200e-12) & (np.maximum(op, on) < 0.1 * vdd))[0]
        if len(idx):
            tres = (t[idx[0]] - tf) * 1e12
            ax.plot([tres], [0.1 * vdd], "o", color=INK2, ms=4)
            ax.annotate(f"{tres:.0f} ps", (tres, 0.1 * vdd), (tres + 8, 0.3), fontsize=8, color=INK2,
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
        hi = limits(ctx, "treset_ps")[1]
        vline(ax, hi, f"limit {hi:g} ps" if hi else None)
        note(ax, f"worst over all cycles {m.get('treset_ps', float('nan')):.1f} ps", loc="upper right")
        ax.set(xlabel="time from CLKC fall (ps)", ylabel="voltage (V)", title="Reset after the decision")
        ax.legend(loc="center right")
    fg.save(fig, "delay", "Comparator delay versus input difference with the log fit and limits, the +1 mV "
            "decision with its delay marked, and the reset to 10 % VDD.")


def _fig_noise(fg, ctx, vd, p1, mu, sig, n, ci) -> None:
    from scipy.stats import norm

    fig, axs = fg.new(1, 2, size=(11.2, 3.9))
    ax = axs[0, 0]
    xx = np.linspace(vd[0], vd[-1], 300)
    hi = limits(ctx, "noise_uV")[1]
    if hi is not None:
        ax.plot(xx * 1e6, norm.cdf((xx - mu) / (hi * 1e-6)), color=LIMIT, lw=1.1, ls="--",
                label=f"curve at the limit, sigma = {hi:g} uV")
    if np.all(np.isfinite(ci)):
        ax.fill_between(xx * 1e6, norm.cdf((xx - mu) / ci[0]), norm.cdf((xx - mu) / ci[1]), color=GRIDLINE,
                        alpha=0.8, lw=0, label="95 % interval of sigma")
    ax.plot(xx * 1e6, norm.cdf((xx - mu) / sig), color=MUTED, lw=1.4, label="probit fit (binomial ML)")
    ax.plot(vd * 1e6, p1, "o", ms=6, color=C1, label=f"{n} decisions per level")
    ax.set(xlabel="differential input vd (uV)", ylabel="P(OUTP = 1)", ylim=(-0.03, 1.03),
           title="Decision probability and Gaussian fit")
    ax.legend(loc="upper left")
    note(ax, f"sigma {sig * 1e6:.1f} uV (95 %: {ci[0] * 1e6:.1f} .. {ci[1] * 1e6:.1f})"
             + (f", limit {hi:g}" if hi is not None else "") + f"\noffset {mu * 1e6:.1f} uV", loc="lower right")
    ax = axs[0, 1]
    ax.plot(vd * 1e6, p1 - norm.cdf((vd - mu) / sig), "o-", ms=5, color=C1)
    binom = np.sqrt(0.25 / max(n, 1))
    ax.axhspan(-binom, binom, color=GRIDLINE, alpha=0.7, label=f"+/-1 binomial sigma at P = 0.5 (n = {n})")
    ax.set(xlabel="differential input vd (uV)", ylabel="P(measured) - P(fit)", title="Fit residual")
    ax.legend(loc="upper right")
    fg.save(fig, "noise", "Probability of OUTP = 1 against input difference with the binomial maximum-likelihood "
            "probit fit that gives the input-referred noise and offset, the 95 % interval of the noise and the "
            "curve at the noise limit; fit residuals against the binomial scatter.")


def _fig_offset_mc(fg, ctx, samples, m) -> None:
    from scipy.stats import norm

    fig, axs = fg.new(1, 3, size=(15.0, 3.9))
    ok = [s for s in samples if s["status"] == "ok"]
    bad = [s for s in samples if s["status"] != "ok"]
    x = np.array([s["offset"] for s in ok]) * 1e3
    hi = limits(ctx, "offset_sigma_mV")[1]
    sig, mu = m.get("offset_sigma_mV"), m.get("offset_mean_mV")
    ax = axs[0, 0]
    if x.size:
        span = max(np.max(np.abs(x)) * 1.15, 3 * (hi or 0), 3 * (sig or 0), 0.05)
        ax.hist(x, bins=np.linspace(-span, span, 25), color=C1, alpha=0.75, label=f"{x.size} valid samples")
        xx = np.linspace(-span, span, 300)
        width = 2 * span / 24
        if sig:
            ax.plot(xx, x.size * width * norm.pdf(xx, mu, sig), color=MUTED, lw=1.4,
                    label=f"normal, mean {mu:.3g} mV, sigma {sig:.3g} mV")
        if hi is not None:
            ax.plot(xx, x.size * width * norm.pdf(xx, 0, hi), color=LIMIT, ls="--", lw=1.1,
                    label=f"sigma at the limit, {hi:g} mV")
    ax.set(xlabel="input offset (mV)", ylabel="samples", title="Offset over the Monte Carlo samples")
    ax.legend(loc="upper left")
    note(ax, f"sigma (n - 1) {sig:.3g} mV" if sig is not None else "sigma: fewer than 2 valid samples",
         loc="upper right")
    ax = axs[0, 1]
    runs = [s["run"] for s in ok]
    ax.plot(runs, x, "o", color=C1, ms=4, label="offset")
    for k, s in enumerate(bad):
        ax.axvline(s["run"], color=LIMIT, lw=1.0, alpha=0.6, label="failed sample" if k == 0 else None)
    ax.axhline(0, color=GRIDLINE, lw=0.8)
    ax.set(xlabel="Monte Carlo iteration", ylabel="input offset (mV)", title="Offset of every sample",
           xlim=(0.5, max([s["run"] for s in samples] + [1]) + 0.5))
    reasons = ", ".join(f"{v} {k}" for k, v in (m.get("mc_fail_reasons") or {}).items())
    note(ax, f"{m['mc_ok']} of {m['mc_runs']} samples valid, {m['mc_failed']} failed"
         + (f" ({reasons})" if reasons else "") + (f"\nCMP-03 needs {s_need(ctx)} valid, 0 failed" if s_need(ctx) else ""),
         loc="lower right")
    if bad:
        ax.legend(loc="upper right")
    ax = axs[0, 2]
    pick = sorted(ok, key=lambda s: abs(s["offset"] * 1e3 - (mu or 0)))[0] if ok else next(s for s in samples if s["search"])
    cyc = np.array([c for c, _, _ in pick["search"]])
    vd = np.array([v for _, v, _ in pick["search"]])
    dec = np.array([d for _, _, d in pick["search"]])
    ref = pick["offset"] if pick["offset"] is not None else 0.0
    lsb = 2 * MC_RANGE / 2 ** MC_BITS
    for d, c, name in ((1, C3, "OUTP"), (0, C2, "OUTN"), (-1, LIMIT, "none / both")):
        sel = (dec == d) if d >= 0 else (dec < 0) | (dec > 1)
        if sel.any():
            ax.plot(cyc[sel], (vd[sel] - ref) * 1e6, "o", ms=6, color=c, label=name)
    ax.plot(cyc, (vd - ref) * 1e6, color=MUTED, lw=0.8, zorder=0)
    ax.set_yscale("symlog", linthresh=10)
    ax.set_yticks([-1e4, -1e3, -1e2, -1e1, 0, 1e1, 1e2, 1e3, 1e4])
    ax.axhline(0, color=GRIDLINE, lw=0.8)
    ax.set(xlabel="decision (CLKC cycle)", ylabel="vd - result (uV)",
           title=f"Search of iteration {pick['run']} ({pick['status']})")
    ax.legend(loc="upper right")
    note(ax, f"+/-{MC_RANGE * 1e3:g} mV range checks, {MC_BITS} halvings ({lsb * 1e6:.1f} uV),\n"
             f"re-check at +/-{MC_CHECK * 1e6:g} uV; result {ref * 1e3:.4f} mV", loc="lower right")
    fg.save(fig, "offset_mc", "Input offset of the Monte Carlo samples: histogram with the normal curve of the "
            "sample mean and standard deviation (n - 1) and the curve at the CMP-03 limit, the offset of every "
            "iteration with failed samples marked, and the successive-approximation search of the sample nearest "
            "the mean (range checks, halvings, re-check).")


def s_need(ctx) -> int | None:
    """Samples the Monte Carlo spec of this test needs (CMP-03: mc: 50)."""
    from ..specs import blocks

    b = blocks().get(ctx.get("block"))
    return next((s.mc for s in (b.specs if b else []) if s.test == ctx.get("test") and s.mc), None)


def _fig_kickback(fg, ctx, m) -> None:
    vd = np.asarray(m["vdiff_uV"])
    fig, axs = fg.new(1, 2, size=(11.2, 3.9))
    ax = axs[0, 0]
    ax.plot(np.arange(len(vd)), vd, "o-", color=C1, ms=5)
    cs = ctx.get("params", {}).get("cs", "C_tot")
    ax.set(xlabel="evaluate / reset cycle", ylabel=f"differential input on {cs}F (uV)",
           title="Input difference after each cycle")
    ax = axs[0, 1]
    step = np.abs(np.diff(vd[1:]))
    ax.bar(np.arange(len(step)), step, color=C1, width=0.6)
    hi = limits(ctx, "kickback_uV")[1]
    hline(ax, hi, limit_label(None, hi, "uV"))
    ax.set(xlabel="cycle", ylabel="|change of the difference| (uV)", title="Kickback per cycle",
           ylim=(0, max(hi or 0, step.max()) * 1.3))
    lines = [f"largest change {step.max():.2g} uV"]
    if "cin_fF" in m:
        hi = limits(ctx, "cin_fF")[1]
        lines.append(f"Cin {m['cin_fF']:.2f} fF per input" + (f" (limit {hi:g})" if hi else ""))
    if "cin_clkc_fF" in m:
        hi = limits(ctx, "cin_clkc_fF")[1]
        lines.append(f"CLKC {m['cin_clkc_fF']:.2f} fF" + (f" (limit {hi:g})" if hi else ""))
    note(ax, "\n".join(lines), loc="upper left")
    fg.save(fig, "kickback", "Differential input of the floating top-plate-sized nodes after each evaluate and reset "
            "cycle, and the change per cycle against the kickback limit.")
