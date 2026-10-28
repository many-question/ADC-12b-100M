"""Noise / timing budget of the architecture, printed as Markdown tables.

    python -m adcflow budget            # writes the tables used in docs/architecture.md

ENOB is taken with calibrated weights as in the acceptance tests (``adcflow.calib``:
weights fitted on a calibration record, ENOB judged on an independent record of
the same chip). The full worst-corner budget with the allowances is
analysis/noise_budget.py (docs/noise-budget.md).
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np

from .arch import Arch
from . import model as m


def cmp_limit(corners: str) -> float:
    """Comparator noise limit (V rms at its input) of adc_comp for the corner set ``corners``."""
    from .specs import blocks

    return next(s.max for s in blocks()["adc_comp"].specs
                if s.metric == "noise_uV" and s.corners == corners) * 1e-6


def _sine(arch: Arch, ni: m.NonIdeal, n: int = 8192, fin: float = 49.9e6):
    met, met_nom, _, r = m.sine_test_cal(arch, ni, n_fft=n, fin_target=fin)
    return r, met, met_nom


def noise_table(arch: Arch) -> str:
    a = arch
    sig = a.fs_peak * 10 ** (-1 / 20) / np.sqrt(2)
    cmp_all = cmp_limit("all")
    base = m.ideal()
    f = m.Follower()
    rows = [
        (f"Quantization ({a.n_codes} levels)", a.lsb / np.sqrt(12), base),
        ("Sampled kT/C, 125 C", a.ktc_noise(125), replace(base, ktc=True, temp_c=125)),
        (f"Comparator, {cmp_all*1e6:.0f} uV at top plate (all-corner limit)", None,
         replace(base, sigma_cmp_top=cmp_all)),
        ("Aperture jitter 100 fs @ 49.9 MHz", sig * 2 * np.pi * 49.9e6 * 100e-15, replace(base, jitter_rms=100e-15)),
        ("DAC settling tau 15 ps, 40/75 ps waits", None, replace(base, tau_dac=15e-12, tau_start=20e-12)),
        (f"VREFP: on-chip follower {f.i_bias*1e3:g} mA, {f.c_node*1e12:g} pF, with its noise, 125 C", None,
         replace(base, ref_follower=f, ref_signal_coupling=True, temp_c=125)),
        (f"Capacitor mismatch sigma(cu) {a.sigma_cu*100:.2f} %, after calibration", None,
         replace(base, sigma_cu=a.sigma_cu)),
    ]
    out = ["| Contributor | Input-referred rms (uV) | SNDR alone (dB) | ENOB alone |",
           "|---|---|---|---|"]
    tot = 0.0
    for name, vn, ni in rows:
        _, met, _ = _sine(a, ni)
        if vn is None:
            p_sig = sig**2
            p_n = p_sig / 10 ** (met["sndr_dbc"] / 10) - (a.lsb**2 / 12)
            vn = float(np.sqrt(max(p_n, 0.0)))
        tot += vn**2
        out.append(f"| {name} | {vn*1e6:.1f} | {met['sndr_dbc']:.1f} | {met['enob']:.2f} |")
    _, met_all, met_nom = _sine(a, m.NonIdeal(temp_c=125, sigma_cmp_top=cmp_all, sigma_cu=a.sigma_cu))
    out.append(f"| **All of the above (model, 125 C)** | {np.sqrt(tot)*1e6:.1f} | "
               f"**{met_all['sndr_dbc']:.1f}** | **{met_all['enob']:.2f}** (nominal weights {met_nom['enob']:.2f}) |")
    return "\n".join(out)


def timing_table(arch: Arch) -> str:
    out = ["| Timing scale vs TT | t_conv median (ns) | t_conv max (ns) | Incomplete | ENOB |",
           "|---|---|---|---|---|"]
    ni0 = m.NonIdeal(temp_c=125, sigma_cmp_top=cmp_limit("all"))
    for s in (1.0, 1.4, 1.6, 1.8):
        ni = replace(ni0, t_cmp0=ni0.t_cmp0 * s, tau_reg=ni0.tau_reg * s, t_loop=ni0.t_loop * s, t_bit=ni0.t_bit * s, t_drv=ni0.t_drv * s,
                     t_dac=ni0.t_dac * s, t_dac_fast=ni0.t_dac_fast * s, tau_dac=ni0.tau_dac * s,
                     t_start=0.1e-9 + (ni0.t_start - 0.1e-9) * s)
        r, met, _ = _sine(arch, ni)
        out.append(f"| x{s:.1f} | {np.median(r.t_conv)*1e9:.2f} | {r.t_conv.max()*1e9:.2f} | "
                   f"{int(r.incomplete.sum())} | {met['enob']:.2f} |")
    return "\n".join(out)


def mismatch_table(arch: Arch, sigmas_1f=(0.0025, 0.005, 0.01, 0.02), runs: int = 8) -> str:
    out = ["| sigma of a 1 fF unit | sigma(cu) | ENOB nominal weights (min / mean) | SFDR nominal (min) | "
           "ENOB calibrated (min / mean) |",
           "|---|---|---|---|---|"]
    for s1 in sigmas_1f:
        s = s1 * np.sqrt(1e-15 / arch.cu)
        e_nom, sf_nom, e_cal = [], [], []
        for k in range(runs):
            ni = replace(m.NonIdeal(), sigma_cu=s, seed=1000 + k)
            _, met, met_nom = _sine(arch, ni)
            e_nom.append(met_nom["enob"]); sf_nom.append(met_nom["sfdr_dbc"]); e_cal.append(met["enob"])
        out.append(f"| {s1*100:.2f} % | {s*100:.2f} % | {min(e_nom):.2f} / {np.mean(e_nom):.2f} | {min(sf_nom):.1f} | "
                   f"{min(e_cal):.2f} / {np.mean(e_cal):.2f} |")
    return "\n".join(out)


def main() -> None:
    a = Arch.load()
    print("## Derived architecture numbers\n")
    for k, v in a.summary().items():
        print(f"- {k}: {v if not isinstance(v, float) else round(v, 4)}")
    print("\n## Noise budget (fin = 49.9 MHz, -1 dBFS, calibrated weights)\n")
    print(noise_table(a))
    print("\n## Timing margin (all impairments, 125 C, comparator at its all-corner limit)\n")
    print(timing_table(a))
    print("\n## CDAC unit mismatch (TT impairments, 8 chips)\n")
    print(mismatch_table(a))


if __name__ == "__main__":
    main()
