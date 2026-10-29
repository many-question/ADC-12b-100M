"""Top-level sine test: ENOB with calibrated weights (acceptance) and nominal weights, FS, timing, power.

The testbench captures ncal + npts conversions of one coherent sine. The first
ncal are the calibration record: the bit weights are fitted to them
(``adcflow.calib.weights``). The next npts are the judged record, decoded with
those weights: ``enob``, ``sndr_dBc``, ``sfdr_dBc`` ... are the acceptance values
(docs/verification.md section 2); the same record decoded with the nominal
weights gives ``enob_nom`` etc. for information.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import numpy as np

from .. import calib
from ..arch import Arch
from ..figures import C1, C3, C7, GRID, LIMIT, MUTED, limits, note, plot_spectrum, sink_of
from .common import read_capture, read_meters, spectrum


def prepare(params: dict) -> dict:
    """Replace fin_target by the coherent input frequency for npts samples.

    The tone is kept at least 3 bins below Nyquist so that the window main lobe
    does not touch bin N/2 (otherwise the spectrum analysis reports the lobe as
    a spur): for N = 1024 at 100 MS/s a 49.9 MHz target becomes 49.71 MHz.
    """
    from adctoolbox import find_coherent_frequency

    fs = float(params.get("fsamp", 1 / float(params.get("tper", 10e-9))))
    n = int(float(params.get("npts", 1024)))
    if "fin_target" in params:
        target = min(float(params.pop("fin_target")), (n / 2 - 3) * fs / n)
        with contextlib.redirect_stdout(io.StringIO()):
            fin, k = find_coherent_frequency(fs, target, n)
        if k > n / 2 - 3:
            fin, k = find_coherent_frequency(fs, (k - 2) * fs / n, n)
        params["fin"] = f"{fin:.9e}"
    return params


SPIKE_LSB = 3.0          # TOP-10: a judged conversion further than this from the sine fit is a spike


def spikes(codes: np.ndarray, fitted: np.ndarray) -> dict:
    """TOP-10: judged conversions whose calibrated code is more than SPIKE_LSB from the sine fit.

    Noise and quantization stay well below 3 LSB (rms ~0.6 LSB); a spike is a decision error
    that the redundancy did not absorb, e.g. VREFP not recovered for a near-full-scale code (#35).
    """
    err = np.asarray(codes, dtype=float) - np.asarray(fitted, dtype=float)
    idx = np.nonzero(np.abs(err) > SPIKE_LSB)[0]
    return {"spike_count": int(idx.size), "spike_max_lsb": float(np.abs(err).max()),
            "spike_index": [int(i) for i in idx[:50]]}


def sine(job_dir: Path, ctx: dict) -> dict:
    from adctoolbox import fit_sine_4param

    a = Arch.load()
    p = ctx["params"]
    g = ctx["globals"]
    npts = int(float(p.get("npts", 1024)))
    ncal = int(float(p.get("ncal", 0)))
    fs = float(p.get("fsamp", 100e6))
    fin = float(p["fin"])
    amp_v = a.fs_peak * 10 ** (float(p.get("amp_dbfs", -1)) / 20)
    cap = read_capture(Path(job_dir) / "capture.txt")
    bits = cap["bits"]
    m: dict = {"n_samples": int(len(bits))}
    m["missing_rdy"] = int(max(ncal + npts - len(bits), 0))
    if len(bits) < ncal + npts:
        m["error"] = f"only {len(bits)} conversions captured (expected {ncal + npts})"
        return m
    tconv = cap["t_conv"][:ncal + npts]
    m["t_conv_max_ns"] = float(tconv.max() * 1e9)
    m["t_conv_mean_ns"] = float(tconv.mean() * 1e9)
    bits_cal, bits = bits[:ncal], bits[ncal:ncal + npts]
    # calibrated weights from the calibration record (or, without one, from the judged record itself)
    w = calib.weights(bits_cal if ncal else bits, fin / fs, a.out_weights)
    m["cal_independent"] = bool(ncal)
    m["weights_cal"] = [round(float(x), 3) for x in w]
    codes_nom = bits.astype(float) @ a.out_weights
    codes = bits.astype(float) @ w
    with contextlib.redirect_stdout(io.StringIO()):
        m.update(spectrum(codes, fs, a.n_codes, ctx))
        m.update({f"{k.replace('_dBc', '')}_nom" + ("_dBc" if k.endswith("_dBc") else ""): v
                  for k, v in spectrum(codes_nom, fs, a.n_codes, ctx).items()})
        fit = fit_sine_4param(codes, frequency_estimate=fin / fs, max_iterations=5)
    amp_codes = float(fit["amplitude"])
    m["amp_codes"] = amp_codes
    m["fs_peak_V"] = float(amp_v * a.code_offset / amp_codes) if amp_codes > 0 else None
    m["code_min"] = int(codes.min())
    m["code_max"] = int(codes.max())
    m.update(spikes(codes, fit["fitted_signal"]))
    meters = read_meters(Path(job_dir) / "power.txt")
    vdd, vdd18 = float(g["vdd"]), float(g["vdd18"])
    pw = {"AVDD": vdd, "DVDD": vdd, "AVDD18": vdd18}
    for k, v in pw.items():
        if k in meters:
            m[f"p_{k.lower()}_mW"] = meters[k] * v * 1e3
    if meters:
        m["power_mW"] = sum(m.get(f"p_{k.lower()}_mW", 0.0) for k in pw)
    np.save(Path(job_dir) / "bits.npy", bits)
    fg = sink_of(ctx)
    if fg:
        _figs(fg, ctx, a, fs, fin, codes, codes_nom, fit, tconv, m, ncal)
    return m


def _figs(fg, ctx, a, fs, fin, codes, codes_nom, fit, tconv, m, ncal) -> None:
    n = len(codes)
    head = f"fin {fin / 1e6:.2f} MHz, {n} points, {ctx['params'].get('amp_dbfs', -1):g} dBFS"
    src = f"weights from the preceding {ncal} conversions" if ncal else "weights fitted on this record"
    fig, axs = fg.new(1, 2, size=(13.0, 4.4))
    plot_spectrum(axs[0, 0], codes, fs, a.n_codes / 2, m, sfdr_min=limits(ctx, "sfdr_dBc")[0],
                  enob_min=limits(ctx, "enob")[0], ylim=(-140, 5), label=f"Calibrated ({src}): acceptance")
    plot_spectrum(axs[0, 1], codes_nom, fs, a.n_codes / 2,
                  {"enob": m["enob_nom"], "sfdr_dBc": m["sfdr_nom_dBc"]}, ylim=(-140, 5),
                  label="Nominal weights (information)")
    fg.save(fig, "spectrum", f"Output spectrum of the judged record ({head}) with ENOB, SNDR and SFDR against "
            f"their limits, decoded with calibrated weights ({src}) and, for information, with the nominal weights.")
    fig, axs = fg.new(1, 3, size=(15.0, 4.2))
    ax = axs[0, 0]
    # fin is close to fs/2, so consecutive samples alternate: fold them on the sine phase
    ph = np.mod(2 * np.pi * fit["frequency"] * np.arange(n) + fit["phase"] + np.pi / 2, 2 * np.pi)
    order = np.argsort(ph)
    ax.plot(ph[order], np.asarray(fit["fitted_signal"])[order], color=MUTED, lw=1.4, label="sine fit")
    ax.plot(ph, codes, "o", ms=2.2, color=C1, alpha=0.8, label="output code (calibrated)")
    ax.set(xlabel="phase of the input sine (rad)", ylabel=f"code (0 .. {a.n_codes - 1})",
           title="Codes folded on the input phase", xlim=(0, 2 * np.pi))
    ax.legend(loc="lower left")
    note(ax, f"codes {int(codes.min())} .. {int(codes.max())}", loc="upper right")
    ax = axs[0, 1]
    err = codes - np.asarray(fit["fitted_signal"])
    ax.plot(np.arange(n), err, ".", color=C3, ms=3)
    ax.axhspan(-SPIKE_LSB, SPIKE_LSB, color=GRID, alpha=0.5, lw=0, label=f"+/-{SPIKE_LSB:g} LSB (TOP-10)")
    big = np.abs(err) > SPIKE_LSB
    if big.any():
        ax.plot(np.nonzero(big)[0], err[big], "o", ms=7, mfc="none", color=LIMIT, label="spike")
    ax.set(xlabel="sample", ylabel="code - sine fit (LSB)", title="Error against the fitted sine",
           ylim=(-max(5.0, np.abs(err).max() * 1.2), max(5.0, np.abs(err).max() * 1.2)))
    ax.legend(loc="lower left", fontsize=7.5)
    note(ax, f"rms {err.std():.2f} LSB, peak {np.abs(err).max():.1f} LSB\n"
             f"spikes > {SPIKE_LSB:g} LSB: {int(big.sum())}", loc="upper right")
    ax = axs[0, 2]
    tc = np.asarray(tconv) * 1e9
    ax.hist(tc, bins=40, color=C7, edgecolor="white", linewidth=0.3)
    hi = limits(ctx, "t_conv_max_ns")[1]
    ax.set(xlabel="CLK fall to RDY rise (ns)", ylabel="conversions", title="Conversion time")
    note(ax, f"mean {tc.mean():.3f} ns, max {tc.max():.3f} ns" + (f"\nlimit on the maximum {hi:g} ns" if hi else ""),
         loc="upper right")
    fg.save(fig, "codes", "Calibrated output codes of the judged record folded on the phase of the input sine "
            "with the fit, the error against the fit for every sample with the spikes beyond 3 LSB marked "
            "(TOP-10), and the conversion-time histogram "
            "(calibration and judged records) against its limit.")
