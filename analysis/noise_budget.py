"""Noise budget at the worst corner: arch v0.2 against the v0.3 proposal (system model).

    python analysis/noise_budget.py                  # tables to stdout (docs/noise-budget.md)
    python analysis/noise_budget.py --sweep          # also the C_S / comparator-noise sweeps

Every contributor is run alone through ``adcflow.model`` (49.9 MHz, -1 dBFS, 8192
points) and turned into an input-referred rms from the SNDR it leaves, minus the
quantization noise; "all" runs everything together. The worst corner of the model
is 125 C (kT/C, follower g_s and noise) with the comparator, logic and DAC timing
1.6 x slower than TT, the comparator noise at its all-corner limit, and the
allowances for distortion (static HD3 of the sampling network) and capacitor
mismatch (random unit mismatch, nominal weights) switched on.

C_S scales by scaling the unit capacitor cu: weights, redundancy, LSB, full scale
and the top-plate gain stay as in v0.2. The behavioral reference (an open-loop
follower) scales with the CDAC charge: bias current and node capacitance x k
keep the VREFP waveform and the recovery time constant unchanged.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import io
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


def arch_k(k: float) -> Arch:
    """v0.2 weights with the unit capacitor scaled by k (C_S, C_DAC x k)."""
    raw = copy.deepcopy(BASE.raw)
    raw["cdac"]["cu"] = BASE.cu * k
    return Arch(raw)


def slow(ni: m.NonIdeal, s: float) -> m.NonIdeal:
    """Comparator, loop and DAC timing s x the TT values (as budget.timing_table)."""
    return replace(ni, t_cmp0=ni.t_cmp0 * s, tau_reg=ni.tau_reg * s, t_loop=ni.t_loop * s,
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
    sigma_cu: float = 0.0    # random unit mismatch (relative, of one cu)

    @property
    def arch(self) -> Arch:
        return arch_k(self.k)

    def follower(self) -> m.Follower:
        """Behavioral follower, its white noise raised to the REF-08 limit at 27 C (sqrt(gamma kT / C))."""
        c = self.c_dec + 0.6e-12 * self.k
        return m.Follower(i_bias=self.i_ref, c_node=c, gamma=self.ref_noise**2 * c / (K_BOLTZMANN * 300.15))

    def nonideal(self) -> m.NonIdeal:
        ni = m.NonIdeal(temp_c=self.temp_c, sigma_cmp_top=self.cmp_top, jitter_rms=self.jitter,
                        hd3_track_dbc=self.hd3_dbc, sigma_cu=self.sigma_cu, ref_follower=self.follower())
        return slow(ni, self.timing)


def sndr(a: Arch, ni: m.NonIdeal, seeds=(1, 2, 3)) -> tuple[float, float]:
    """Mean SNDR (dBc) and ENOB over seeds."""
    s = []
    for sd in seeds:
        with contextlib.redirect_stdout(io.StringIO()):
            r, _, _ = m.sine_test(a, replace(ni, seed=sd), n_fft=N_FFT, fin_target=FIN)
            met = m.spectrum_metrics(r.codes, a.fs, a.n_codes)
        s.append(met["sndr_dbc"])
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
        spec.append(("Mismatch allowance (nominal weights)", replace(base, sigma_cu=c.sigma_cu),
                     f"sigma(cu) {c.sigma_cu*100:.2f} % at cu = {a.cu*1e15:.2f} fF, 16 chips rms"))
    out = []
    for name, ni, note in spec:
        seeds = tuple(range(1000, 1016)) if "Mismatch" in name else (1, 2, 3)
        if "Mismatch" in name:
            p = np.mean([rms_of(sndr(a, ni, (s,))[0]) ** 2 for s in seeds])
        else:
            p = rms_of(sndr(a, ni, seeds)[0]) ** 2
        out.append((name, float(np.sqrt(max(p - Q_RMS**2, 0.0))), note))
    return out


def total(c: Case, chips: int = 8) -> tuple[float, float, float]:
    """All impairments together: mean ENOB, min ENOB, rms (V) over chips (seeds)."""
    e, p = [], []
    for s in range(chips):
        sd, en = sndr(c.arch, replace(c.nonideal(), seed=2000 + s), seeds=(2000 + s,))
        e.append(en)
        p.append(rms_of(sd) ** 2)
    return float(np.mean(e)), float(np.min(e)), float(np.sqrt(np.mean(p)))


def table(c: Case) -> str:
    rs = rows(c)
    nq = sum(v**2 for _, v, _ in rs)
    cmp_p = dict((n, v) for n, v, _ in rs)["Comparator"] ** 2
    lines = [f"**{c.name}**", "",
             "| Contributor | Input-referred rms (uV) | Share of non-quantization power | Assumption |",
             "|---|---|---|---|",
             f"| Quantization ({c.arch.n_codes} levels) | {Q_RMS*1e6:.1f} | – | model, nominal weights |"]
    for n, v, note in rs:
        lines.append(f"| {n} | {v*1e6:.1f} | {v**2/nq*100:.0f} % | {note} |")
    rss = np.sqrt(nq + Q_RMS**2)
    en_rss = (20 * np.log10(SIG_RMS / rss) - 1.76) / 6.02
    e_mean, e_min, r_all = total(c)
    lines.append(f"| Sum of squares | {rss*1e6:.1f} | comparator {cmp_p/nq*100:.0f} % | ENOB {en_rss:.2f} |")
    lines.append(f"| **All together (model, 8 chips)** | **{r_all*1e6:.1f}** | | "
                 f"**ENOB {e_mean:.2f} mean / {e_min:.2f} min, margin {e_min-ENOB_MIN:.2f} bit** |")
    return "\n".join(lines)


V02_WORST = Case("v0.2 limits, worst corner", k=1.0, cmp_top=80e-6, sigma_cu=0.01)
V02_ISSUE = Case("v0.2 sizing, comparator 240 uV (all-corner)", k=1.0, cmp_top=240e-6, sigma_cu=0.01)
V03_WORST = Case("v0.3 proposal, worst corner", k=2.0, cmp_top=240e-6, i_ref=4e-3, c_dec=3e-12,
                 ref_noise=80e-6, sigma_cu=0.01 / np.sqrt(2))
V03_TT = replace(V03_WORST, name="v0.3 proposal, TT (27 C, TT timing, comparator at its TT limit)",
                 cmp_top=200e-6, temp_c=27.0, timing=1.0)


CMP_SWEEP = (180, 200, 220, 240, 260)


def sweep() -> str:
    out = ["| C_S (pF) | k | kT/C 125 C (uV) | " + " | ".join(f"cmp {c} uV" for c in CMP_SWEEP) + " |",
           "|---|---|---|" + "---|" * 5]
    for k in (1.0, 1.5, 2.0, 3.0):
        cells = []
        for c in CMP_SWEEP:
            cs = Case("", k=k, cmp_top=c * 1e-6, i_ref=2e-3 * k, c_dec=1.5e-12 * k, ref_noise=80e-6,
                      sigma_cu=0.01 / np.sqrt(k))
            cells.append(f"{total(cs, chips=4)[0]:.2f}")
        a = arch_k(k)
        out.append(f"| {a.c_s*1e12:.2f} | {k:g} | {a.ktc_noise(125)*1e6:.1f} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", action="store_true")
    args = ap.parse_args()
    for c in (V02_WORST, V02_ISSUE, V03_WORST, V03_TT):
        print(table(c), "\n", flush=True)
    if args.sweep:
        print("Mean ENOB, worst corner, 4 chips (sigma(cu) 1 % at 0.5 fF, Pelgrom-scaled; follower x k, 80 uV):\n")
        print(sweep())


if __name__ == "__main__":
    main()
