"""Readers for the files the testbench Verilog-A monitors write."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .. import psf


def read_capture(path: Path) -> dict:
    """capture.txt -> {'bits': (N,14) uint8, 't_rdy', 't_conv', 'clk_falls', 'rdy_rises'}."""
    bits, t_rdy, t_conv = [], [], []
    clk_falls = rdy_rises = None
    for line in Path(path).read_text().splitlines():
        if line.startswith("# clk_falls"):
            f = line.split()
            clk_falls, rdy_rises = int(f[2]), int(f[4])
            continue
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split()
        t_rdy.append(float(f[1]))
        t_conv.append(float(f[2]))
        bits.append([int(c) for c in f[3]])
    return {"bits": np.asarray(bits, dtype=np.uint8).reshape(-1, 14), "t_rdy": np.asarray(t_rdy),
            "t_conv": np.asarray(t_conv), "clk_falls": clk_falls, "rdy_rises": rdy_rises}


def read_meters(path: Path) -> dict[str, float]:
    out = {}
    if Path(path).exists():
        for line in Path(path).read_text().splitlines():
            f = line.split()
            if len(f) >= 2:
                out[f[0]] = float(f[1])
    return out


def read_samples(path: Path) -> np.ndarray:
    """tb_sampler_va file -> (N, 3) array of index, time, value."""
    rows = [list(map(float, ln.split())) for ln in Path(path).read_text().splitlines() if ln.strip()]
    return np.asarray(rows).reshape(-1, 3)


def tran(job_dir: Path) -> dict[str, np.ndarray]:
    """The transient PSF-ASCII waveforms of a job (first tran analysis)."""
    raw = Path(job_dir) / "deck.raw"
    f = psf.find(raw, "*.tran.tran") or psf.find(raw, "*.tran")
    if f is None:
        raise FileNotFoundError(f"no transient results in {raw}")
    return psf.read(f)


QMETER_UNIT = 1e-15     # tb_qmeter_va: V(Q) in fC


def edge_cin(t: np.ndarray, v: np.ndarray, q: np.ndarray, vdd: float,
             before: float = 50e-12, after: float = 200e-12) -> np.ndarray:
    """Input capacitance of a pin from a transient: for every rising edge of its voltage v, the
    charge into the pin (q in C, from the tb_qmeter_va in series with it) over the edge divided by
    the voltage step. The window runs from `before` the 50 % crossing to `after` it, at most halfway
    to the neighbouring falling crossings; edges whose window spans less than 80 % of vdd are skipped.
    This is the switched capacitance the driver charges (gate capacitance over the whole swing,
    Miller coupling included). Returns the capacitance (F) of every rising edge."""
    rises = psf.crossings(t, v, vdd / 2, +1)
    falls = psf.crossings(t, v, vdd / 2, -1)
    out = []
    for r in rises:
        prev, nxt = falls[falls < r], falls[falls > r]
        ta = max(r - before, (prev[-1] + r) / 2 if len(prev) else t[0])
        tb = min(r + after, (r + nxt[0]) / 2 if len(nxt) else t[-1])
        dv = np.interp(tb, t, v) - np.interp(ta, t, v)
        if dv >= 0.8 * vdd:
            out.append((np.interp(tb, t, q) - np.interp(ta, t, q)) / dv)
    return np.asarray(out)


def pin_cins(w: dict, vdd: float, pins: dict[str, tuple[str, str]]) -> dict[str, np.ndarray]:
    """edge_cin for several pins of one transient: {metric: (voltage signal, charge-meter signal)}.
    Pins whose signals were not saved are left out."""
    return {k: edge_cin(w["time"], w[v], w[q] * QMETER_UNIT, vdd) for k, (v, q) in pins.items()
            if v in w and q in w}


def fig_cin(fg, ctx: dict, cins: dict[str, np.ndarray], panels: list[tuple[str, str, str]],
            tag: str = "cin") -> None:
    """Input capacitance of every rising edge against its limit, one panel per (key of cins, title,
    metric whose spec limit applies)."""
    from ..figures import C1, hline, limits, note

    panels = [pn for pn in panels if len(cins.get(pn[0], ()))]
    if not panels:
        return
    fig, axs = fg.new(1, len(panels), size=(3.9 * len(panels) + 1.0, 3.6))
    for ax, (k, title, metric) in zip(axs.ravel(), panels):
        c = cins[k] * 1e15
        ax.plot(np.arange(1, len(c) + 1), c, "o", color=C1, ms=4)
        hi = limits(ctx, metric)[1]
        hline(ax, hi, f"limit {hi:g} fF" if hi else None)
        ax.set(xlabel="rising edge", ylabel="charge / voltage step (fF)", title=title,
               ylim=(0, max(hi or 0, c.max()) * 1.3))
        note(ax, f"mean {c.mean():.2f} fF over {len(c)} edges", loc="lower right")
    fg.save(fig, tag, "Input capacitance of the clock and digital inputs: the charge each pin draws over every "
            "rising edge (charge meter in series with it) divided by the voltage step, against the limit; the "
            "metric is the mean over the edges.")


def spectrum(codes: np.ndarray, fs: float, full_scale: float | None) -> dict:
    from adctoolbox import analyze_spectrum

    r = analyze_spectrum(np.asarray(codes, dtype=float), fs=fs, max_scale_range=full_scale, create_plot=False)
    return {"enob": float(r["enob"]), "sndr_dBc": float(r["sndr_dbc"]), "sfdr_dBc": float(r["sfdr_dbc"]),
            "snr_dBc": float(r["snr_dbc"]), "thd_dBc": float(r.get("thd_dbc", np.nan))}
