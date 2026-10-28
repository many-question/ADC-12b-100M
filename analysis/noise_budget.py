"""Noise budget at the worst corner: arch v0.2 against v0.3 (system model).

    python analysis/noise_budget.py                  # tables to stdout (docs/noise-budget.md)
    python analysis/noise_budget.py --sweep          # also the C_S / comparator-noise sweep

Every contributor is run alone through ``adcflow.model`` (49.9 MHz, -1 dBFS, 8192
points) and turned into an input-referred rms from the SNDR it leaves, minus the
quantization noise; "all" runs everything together. Records are decoded with
calibrated weights as in the acceptance tests (``adcflow.calib``: weights fitted
on a calibration record of the same chip, ENOB judged on an independent record);
the nominal-weight ENOB is reported for information. The worst corner of the
model is 125 C (kT/C, follower g_s and noise) with the comparator, logic and DAC
timing 0.8, 1.0 or 1.6 x TT, whichever is worst (slow timing costs settling and
conversion time, fast timing leaves the reference less time to recover between
decisions, issue #35), the comparator noise at its all-corner limit, the
VREFP noise at the REF-08 limit, a static HD3 allowance for the sampling network
and random capacitor mismatch (relative sigma 0.5 % for a 1 fF unit, averaging
over the units of a weight).

C_S scales by scaling the unit capacitor cu: weights, redundancy, LSB, full scale
and the top-plate gain stay as in v0.2. The behavioral reference (an open-loop
follower) scales with the CDAC charge: bias current and node capacitance x k
keep the VREFP waveform and the recovery time constant unchanged.
"""

from __future__ import annotations

import argparse
import copy
import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from adcflow import model as m  # noqa: E402
from adcflow.arch import K_BOLTZMANN, Arch  # noqa: E402

BASE = Arch.load()
N_FFT = 8192
FIN = 49.9e6
SIG_RMS = BASE.fs_peak * 10 ** (-1 / 20) / np.sqrt(2)
ENOB_MIN = 10.5
CU_V02 = 0.5e-15
SIGMA_1F = 0.005         # relative sigma of a 1 fF unit capacitor


def arch_k(k: float) -> Arch:
    """The (unchanged) weights with the v0.2 unit capacitor scaled by k (C_S, C_DAC x k)."""
    raw = copy.deepcopy(BASE.raw)
    raw["cdac"]["cu"] = CU_V02 * k
    return Arch(raw)


def sigma_cu(k: float) -> float:
    """Relative mismatch of one unit at cu = 0.5 fF x k (Pelgrom: sigma ~ 1 / sqrt(area))."""
    return SIGMA_1F * float(np.sqrt(1e-15 / (CU_V02 * k)))


def slow(ni: m.NonIdeal, s: float) -> m.NonIdeal:
    """Comparator, loop and DAC timing s x the TT values (as budget.timing_table)."""
    return replace(ni, t_cmp0=ni.t_cmp0 * s, tau_reg=ni.tau_reg * s, t_loop=ni.t_loop * s, t_bit=ni.t_bit * s, t_drv=ni.t_drv * s,
                   t_dac=ni.t_dac * s, t_dac_fast=ni.t_dac_fast * s, tau_dac=ni.tau_dac * s,
                   t_start=0.1e-9 + (ni.t_start - 0.1e-9) * s)


@dataclass
class Case:
    """One budget: architecture scale and the block limits it assumes."""
    name: str
    k: float                 # C_S / C_S(v0.2)
    cmp_top: float           # comparator noise at its input (top plate), V rms
    temp_c: float = 125.0
    timing: float = 1.6      # timing scale vs TT
    i_ref: float = 2e-3      # behavioral follower bias (A)
    c_dec: float = 1.5e-12   # behavioral VREFP decap; the node adds 0.6 pF x k of CDAC bottom plates
    ref_noise: float = 120e-6  # VREFP noise at 27 C (REF-08 limit); sets the follower's gamma
    jitter: float = 100e-15
    hd3_dbc: float | None = -82.0
    mismatch: bool = True    # random unit mismatch, sigma_cu(k)

    @property
    def arch(self) -> Arch:
        return arch_k(self.k)

    @property
    def sigma_cu(self) -> float:
        return sigma_cu(self.k) if self.mismatch else 0.0

    def follower(self) -> m.Follower:
        """Behavioral follower, its white noise raised to the REF-08 limit at 27 C (sqrt(gamma kT / C))."""
        c = self.c_dec + 0.6e-12 * self.k
        return m.Follower(i_bias=self.i_ref, c_node=c, gamma=self.ref_noise**2 * c / (K_BOLTZMANN * 300.15))

    def nonideal(self) -> m.NonIdeal:
        ni = m.NonIdeal(temp_c=self.temp_c, sigma_cmp_top=self.cmp_top, jitter_rms=self.jitter,
                        hd3_track_dbc=self.hd3_dbc, sigma_cu=self.sigma_cu, ref_follower=self.follower())
        return slow(ni, self.timing)


def sndr(a: Arch, ni: m.NonIdeal, seeds=(1, 2, 3), nominal: bool = False) -> tuple[float, float]:
    """Mean SNDR (dBc) and ENOB over seeds (chips), calibrated weights unless ``nominal``."""
    s = []
    for sd in seeds:
        met_cal, met_nom, _, _ = m.sine_test_cal(a, replace(ni, seed=sd), n_fft=N_FFT, fin_target=FIN)
        s.append((met_nom if nominal else met_cal)["sndr_dbc"])
    sd = float(np.mean(s))
    return sd, (sd - 1.76) / 6.02


def rms_of(sndr_db: float) -> float:
    """Input-referred error rms (V) for an SNDR at -1 dBFS."""
    return float(SIG_RMS / 10 ** (sndr_db / 20))


Q_RMS = rms_of(sndr(BASE, m.ideal(), seeds=(1,))[0])     # quantization alone, from the model


def rows(c: Case) -> list[tuple[str, float, str]]:
    """(contributor, input-referred rms in V, note) for every budget line of case c."""
    a, base = c.arch, m.ideal(temp_c=c.temp_c)
    spec = [
        ("Sampled kT/C (incl. switch and 50 ohm source noise)", replace(base, ktc=True),
         f"2kT C_tot / C_S^2, C_S = {a.c_s*1e12:.3f} pF, {c.temp_c:.0f} C"),
        ("Comparator", replace(base, sigma_cmp_top=c.cmp_top),
         f"{c.cmp_top*1e6:.0f} uV at its input, top-plate gain {a.gain_top:.3f}"),
        ("VREFP (behavioral follower, droop + noise)", replace(base, ref_follower=c.follower(), ref_signal_coupling=True),
         f"{c.i_ref*1e3:.1f} mA, node {c.follower().c_node*1e12:.1f} pF, noise {c.ref_noise*1e6:.0f} uV at 27 C"),
        ("Aperture jitter", replace(base, jitter_rms=c.jitter), f"{c.jitter*1e15:.0f} fs rms"),
        ("DAC settling", slow(replace(base, tau_dac=15e-12, tau_start=20e-12), c.timing),
         f"tau 15 ps, 40/75 ps waits, timing x{c.timing:g}"),
    ]
    if c.hd3_dbc is not None:
        spec.append(("Distortion allowance (sampling network)", replace(base, hd3_track_dbc=c.hd3_dbc),
                     f"HD3 {c.hd3_dbc:.0f} dBc"))
    if c.sigma_cu > 0:
        spec.append(("Capacitor mismatch, residual after calibration", replace(base, sigma_cu=c.sigma_cu),
                     f"sigma(cu) {c.sigma_cu*100:.2f} % at cu = {a.cu*1e15:.2f} fF, 16 chips rms"))
    out = []
    for name, ni, note in spec:
        if "mismatch" in name:
            p = np.mean([rms_of(sndr(a, ni, (s,))[0]) ** 2 for s in range(1000, 1016)])
        else:
            p = rms_of(sndr(a, ni)[0]) ** 2
        out.append((name, float(np.sqrt(max(p - Q_RMS**2, 0.0))), note))
    return out


def mismatch_nominal(c: Case) -> float:
    """For information: mismatch alone decoded with the nominal weights (V rms, 16 chips)."""
    ni = replace(m.ideal(temp_c=c.temp_c), sigma_cu=c.sigma_cu)
    p = np.mean([rms_of(sndr(c.arch, ni, (s,), nominal=True)[0]) ** 2 for s in range(1000, 1016)])
    return float(np.sqrt(max(p - Q_RMS**2, 0.0)))


def total(c: Case, chips: int = 8) -> dict:
    """All impairments together over chips (seeds): calibrated mean / min ENOB and rms,
    and the nominal-weight ENOB for information."""
    e, en, p = [], [], []
    for s in range(chips):
        met_cal, met_nom, _, _ = m.sine_test_cal(c.arch, replace(c.nonideal(), seed=2000 + s),
                                                 n_fft=N_FFT, fin_target=FIN)
        e.append(met_cal["enob"])
        en.append(met_nom["enob"])
        p.append(rms_of(met_cal["sndr_dbc"]) ** 2)
    return {"mean": float(np.mean(e)), "min": float(np.min(e)), "rms": float(np.sqrt(np.mean(p))),
            "nominal": float(np.mean(en)), "nominal_min": float(np.min(en))}


def table(c: Case) -> str:
    rs = rows(c)
    nq = sum(v**2 for _, v, _ in rs)
    cmp_p = dict((n, v) for n, v, _ in rs)["Comparator"] ** 2
    lines = [f"**{c.name}**", "",
             "| Contributor | Input-referred rms (uV) | Share of non-quantization power | Assumption |",
             "|---|---|---|---|",
             f"| Quantization ({c.arch.n_codes} levels) | {Q_RMS*1e6:.1f} | – | model |"]
    for n, v, note in rs:
        lines.append(f"| {n} | {v*1e6:.1f} | {v**2/nq*100:.0f} % | {note} |")
    rss = np.sqrt(nq + Q_RMS**2)
    en_rss = (20 * np.log10(SIG_RMS / rss) - 1.76) / 6.02
    t = total(c)
    lines.append(f"| Sum of squares | {rss*1e6:.1f} | comparator {cmp_p/nq*100:.0f} % | ENOB {en_rss:.2f} |")
    lines.append(f"| **All together (model, 8 chips, calibrated)** | **{t['rms']*1e6:.1f}** | | "
                 f"**ENOB {t['mean']:.2f} mean / {t['min']:.2f} min, margin {t['mean']-ENOB_MIN:.2f} / "
                 f"{t['min']-ENOB_MIN:.2f} bit** |")
    if c.sigma_cu > 0:
        lines.append(f"| (information) nominal weights | mismatch alone {mismatch_nominal(c)*1e6:.1f} | | "
                     f"ENOB {t['nominal']:.2f} mean / {t['nominal_min']:.2f} min |")
    return "\n".join(lines)


V02_WORST = Case("v0.2 limits, worst corner", k=1.0, cmp_top=80e-6)
V02_ISSUE = Case("v0.2 sizing, comparator 240 uV (all-corner)", k=1.0, cmp_top=240e-6)
V03_WORST = Case("v0.3, worst corner", k=2.0, cmp_top=240e-6, i_ref=4e-3, c_dec=3e-12)
V03_TT = replace(V03_WORST, name="v0.3, TT (27 C, TT timing, comparator at its TT limit)",
                 cmp_top=200e-6, temp_c=27.0, timing=1.0)
V03_TT_BEHAV = replace(V03_TT, name="v0.3, TT, behavioral conditions (no mismatch, no HD3, follower gamma = 2)",
                       hd3_dbc=None, mismatch=False, ref_noise=float(np.sqrt(2 * K_BOLTZMANN * 300.15 / 4.2e-12)))

CMP_SWEEP = (180, 200, 220, 240, 260)


def sweep() -> str:
    out = ["| C_S (pF) | k | kT/C 125 C (uV) | " + " | ".join(f"cmp {c} uV" for c in CMP_SWEEP) + " |",
           "|---|---|---|" + "---|" * len(CMP_SWEEP)]
    for k in (1.0, 1.5, 2.0, 3.0):
        cells = []
        for c in CMP_SWEEP:
            cs = Case("", k=k, cmp_top=c * 1e-6, i_ref=2e-3 * k, c_dec=1.5e-12 * k)
            cells.append(f"{min(total(replace(cs, timing=s), chips=4)['mean'] for s in WORST_TIMINGS):.2f}")
        a = arch_k(k)
        out.append(f"| {a.c_s*1e12:.2f} | {k:g} | {a.ktc_noise(125)*1e6:.1f} | " + " | ".join(cells) + " |")
    return "\n".join(out)


WORST_TIMINGS = (0.8, 1.0, 1.6)


def worst(c: Case) -> Case:
    """The case at the timing scale (WORST_TIMINGS) with the lowest all-together mean ENOB."""
    if c.temp_c != 125.0:
        return c
    cases = [replace(c, timing=s, name=f"{c.name} (binding timing x{s:g})") for s in WORST_TIMINGS]
    return min(cases, key=lambda x: total(x, chips=4)["mean"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", action="store_true")
    args = ap.parse_args()
    for c in (V02_WORST, V02_ISSUE, V03_WORST):
        print(f"{c.name}, all items at their limits: " + ", ".join(
            f"timing x{s:g} ENOB {total(replace(c, timing=s), chips=4)['mean']:.2f}" for s in WORST_TIMINGS), flush=True)
    for c in (V02_WORST, V02_ISSUE, V03_WORST, V03_TT):
        print(table(worst(c)), "\n", flush=True)
    t = total(V03_TT_BEHAV, chips=4)
    print(f"{V03_TT_BEHAV.name}: ENOB {t['mean']:.2f} calibrated, {t['nominal']:.2f} nominal\n", flush=True)
    if args.sweep:
        print("Mean calibrated ENOB, worst corner, 4 chips (follower x k, REF-08 120 uV):\n")
        print(sweep())


if __name__ == "__main__":
    main()
