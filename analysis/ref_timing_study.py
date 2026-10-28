"""Reference follower current vs DAC waits of decisions 5..7 (issue #35, option (c)).

    python analysis/ref_timing_study.py            # table to stdout

System model with the reference charge at the DAC drive (NonIdeal.t_bit / t_drv).
For every candidate (follower bias, wait change) and corner (temperature x timing
scale) it reports the noise-free ENOB loss against an ideal reference (calibrated
weights), the VREFP deviation at each decision against the end of the conversion
over its tolerance (env_ratio, the quantity tb_ref_replay reports), the conversion
time, power, and the all-limits worst-corner ENOB of analysis/noise_budget.py.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "analysis"))
from adcflow import model as m  # noqa: E402
from adcflow.arch import Arch  # noqa: E402
import noise_budget as nb  # noqa: E402

A = Arch.load()
N_FFT = 2048
TEMPS = (-40.0, 27.0, 125.0)
SCALES = (0.8, 1.0, 1.6)
I_CDAC = 0.2e-3          # average CDAC current from VREFP (A)
P_OTHER = 0.435e-3       # AVDD + DVDD of the behavioral top at TT (W), scales with V^2


@dataclass(frozen=True)
class Cand:
    name: str
    i_ref: float
    n_fast: int = 6
    add: tuple = ()      # extra wait (s) after DAC steps 1, 2, ...
    c_dec: float = 3e-12


def tolerance() -> np.ndarray:
    """VREFP tolerance per decision (V): redundancy (>= 0.25 LSB) x LSB x VREF / FS."""
    red = np.concatenate([A.redundancy(), [0.0]])
    return np.maximum(red, 0.25) * A.lsb * A.vref / A.fs_peak


def timing(ni: m.NonIdeal, s: float, c: Cand) -> m.NonIdeal:
    ni = replace(ni, n_fast=c.n_fast, t_dac_add=tuple(x * s for x in c.add) or None)
    return nb.slow(ni, s) if s != 1.0 else ni


def ref_only(c: Cand, temp: float, s: float, ideal_ref: bool = False) -> m.NonIdeal:
    ni = m.ideal(temp_c=temp, tau_dac=12e-12, tau_start=12e-12)
    if not ideal_ref:
        ni = replace(ni, ref_follower=m.Follower(i_bias=c.i_ref, c_node=c.c_dec + 1.2e-12, gamma=0.0),
                     ref_signal_coupling=True)
    return timing(ni, s, c)


def corner(c: Cand, temp: float, s: float) -> dict:
    met0, _, _, _ = m.sine_test_cal(A, ref_only(c, temp, s, ideal_ref=True), n_fft=N_FFT, fin_target=49.9e6)
    met, _, _, r = m.sine_test_cal(A, ref_only(c, temp, s), n_fft=N_FFT, fin_target=49.9e6)
    dv = r.info["dvref"]
    dev = np.abs(dv - dv[:, -1:]).max(0)
    ratio = dev / tolerance()
    return {"loss": met0["enob"] - met["enob"], "dev": dev, "ratio": ratio, "t_conv": float(r.t_conv.max())}


def power(c: Cand, v18: float, k: float) -> tuple[float, float]:
    p18 = (c.i_ref + I_CDAC) * v18
    return p18, p18 + P_OTHER * k**2


def worst_all_limits(c: Cand) -> float:
    e = []
    for s in SCALES:
        case = replace(nb.V03_WORST, i_ref=c.i_ref, c_dec=c.c_dec, timing=1.0)
        ni = timing(case.nonideal(), s, c)
        res = []
        for chip in range(4):
            met, _, _, _ = m.sine_test_cal(case.arch, replace(ni, seed=2000 + chip), n_fft=nb.N_FFT, fin_target=nb.FIN)
            res.append(met["enob"])
        e.append(np.mean(res))
    return float(min(e))


def waits(*spec) -> tuple:
    """Extra DAC waits: waits((steps, ps), ...) -> per-step tuple (s); step k follows decision k."""
    out = [0.0] * 13
    for steps, ps in spec:
        for k in steps:
            out[k - 1] += ps * 1e-12
    return tuple(out)


CANDS = [
    Cand("4 mA, 3 pF (today)", 4e-3),
    Cand("8 mA, 3 pF", 8e-3),
    Cand("8 mA, 6 pF, n_fast 3, +15 ps after dec. 9", 8e-3, n_fast=3, c_dec=6e-12, add=waits(((9,), 15))),
    Cand("**8 mA, 6 pF, +20 ps after dec. 4, 5, 6, 9**", 8e-3, c_dec=6e-12, add=waits(((4, 5, 6, 9), 20))),
    Cand("9 mA, 6 pF, +15 ps after dec. 4, 5, 6, 9", 9e-3, c_dec=6e-12, add=waits(((4, 5, 6, 9), 15))),
    Cand("10 mA, 6 pF, +10 ps after dec. 4, 5, 6, 9", 10e-3, c_dec=6e-12, add=waits(((4, 5, 6, 9), 10))),
    Cand("12 mA, 3 pF", 12e-3),
]
REGIMES = ((125.0, 1.0), (125.0, 0.8), (-40.0, 0.8), (27.0, 1.0), (125.0, 1.6))


def main(cands=CANDS, all_limits: bool = True) -> None:
    t_avail = float(A.raw["timing"]["t_conv_max"])
    print("| Candidate | env_ratio dec. 1-11: 125 C x1.0 / 125 C x0.8 / -40 C x0.8 / 27 C x1.0 / 125 C x1.6 | "
          "ratio dec. 4..8, 125 C x1.0 | tail dec. 12-14 (uV) | ENOB loss, worst | t_conv TT / x1.6 (ns) | "
          "slow margin (ns) | AVDD18 / total, nominal (mW) | +10 % (mW) | all-limits worst ENOB |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    t_conv_base = None
    for c in cands:
        rows = {(T, s): corner(c, T, s) for T in TEMPS for s in SCALES}
        loss = max(r["loss"] for r in rows.values())
        env = " / ".join(f"{rows[k]['ratio'][:11].max():.2f}" for k in REGIMES)
        tail = max(r["dev"][11:].max() for r in rows.values())
        r10 = rows[(125.0, 1.0)]["ratio"][3:8]
        tc_tt, tc_slow = rows[(27.0, 1.0)]["t_conv"], rows[(125.0, 1.6)]["t_conv"]
        t_conv_base = t_conv_base or tc_tt
        pn, ptn = power(c, 1.8, 1.0)
        ph, pth = power(c, 1.98, 1.1)
        wa = f"{worst_all_limits(c):.2f}" if all_limits else "-"
        print(f"| {c.name} | {env} | {' '.join(f'{x:.2f}' for x in r10)} | {tail*1e6:.0f} | {loss:.3f} | "
              f"{tc_tt*1e9:.2f} (+{(tc_tt - t_conv_base)*1e12:.0f} ps) / {tc_slow*1e9:.2f} | {(t_avail - tc_slow)*1e9:+.2f} | "
              f"{pn*1e3:.1f} / {ptn*1e3:.1f} | {ph*1e3:.1f} / {pth*1e3:.1f} | {wa} |", flush=True)


if __name__ == "__main__":
    main(all_limits="--quick" not in sys.argv)
