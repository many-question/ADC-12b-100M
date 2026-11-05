# Independent boosted-reset experiment

This is an authorized diagnostic experiment, separate from the frozen V29 candidate.
Only the booster driver is idealized; the TOP-to-VCM switch is a real core ULVT NMOS.
The canonical source, formal failures and completed attribution study remain frozen at
[e73442f](https://github.com/many-question/ADC-12b-100M/blob/e73442f8a456822f0ba8c313eb3afaa42cdf447d/design/xtor/adc_cdac/many-question-codex/validation-status.md). The candidate remains WIP.

## Circuit and assumptions

`mq_cdac_reset_booster(CLKB BST DVDD VB VSS)` is a separate replaceable subcircuit.
Each P/N CDAC instantiates the same definition as `XBOOST`; it is outside XCAP/XSW.
`CLKB=PHI_SB` is active low, `VB=VCM`, and `BST` drives only the real reset gate.
The 37 external ports, all array/control instances and the official top load remain unchanged.
MTP is removed. The primary omits MTD; a 3 um MTD with the original gate polarity is a
deliberate compensation comparison, not inherited proof that the old dummy remains suitable.

| Model parameter | First-stage setting |
|---|---|
| Command high / low | VCM + 0.9*DVDD / 0 V; high=1.179 V at hot SS |
| Input threshold | 0.5*DVDD on actual PHI_SB |
| Delay / rise / fall | 2 ps / 10 ps / 10 ps |
| Output resistance | 100 ohm, driving actual MOS gate capacitance |
| Reset geometry | 6 um / nf3 or 12 um / nf6; L=30 nm |
| Optional dummy | 3 um / nf2; L=30 nm; source/drain tied to TOP |

All three geometries passed ordered callback evaluation without warnings. The macro
invocation retains the original w/l/nf convention; full callback outputs are private evidence.
VB, DVDD and CLKB are sense-only ports in this ideal model: it draws no bias charge,
supply current or input-clock load. Output energy and Rout loss can be measured, but
do not represent real booster efficiency, total power, area or bias-drive feasibility.
The model provides maintained high level and ideal internal replenishment through finite Rout.
It includes neither CB droop/leakage nor internal MOS stress. These must be assessed in
a later transistor implementation only after a useful real-switch window is demonstrated.

![Reset hierarchy](boosted-reset-schematic.svg)

![Ideal driver wrapper](boosted-reset-wrapper.svg)

## Reproducible source

[VA model](boosted-reset-model.txt) and [source patches](boosted-reset-patches.txt) are
diagnostic text artifacts, not the submitted transistor candidate. Apply the first patch
to the frozen V29 source; each following delta starts from n6_k09, independently.
The experiment deck supplies the VA include outside the candidate netlist.

| Variant | Source SHA-256 |
|---|---|
| n6_k09 | `582d69bfe4203fa9cee9995321b959889ddd43dedb0fb8bb09e29b45e2deeb4f` |
| n12_k09 | `12fb8cc3a1e7f747513da6a0416a997a29885a74e8c7432c4833bb2032744dbd` |
| n6_k09_d3 | `f36e0924f5794478ff28ddcbc63c5c6cf363fd686b98cdce3ce2879ad5c93c66` |

VA SHA-256: `d7c6ce43d97e4946cee348eeb53b63605b93f7759a9dec071e0af8a4a441f365`.
Frozen canonical SHA-256: `a57472585adc914ab1b2fc9fcf67fc9ecae4e0ffdad1649a87c5a72fdc9e4981`.
All full hierarchy RNL checks report zero errors/warnings; drawings were visually reviewed.
The local drawing tool was 0.5.5. The canonical netlist is unchanged.

## Validation status

Official APS precision remains conservative, effective reltol 1e-7 and vabstol 10 nV.
Short records cover 80 ns and only four samples; they are functional/stress prechecks,
never spectral acceptance. Full tracking requires all 256 samples at hot SS. The
crosscheck changes to traponly/1 ps on the same frozen source. Dense saved waves for
full runs cover the first 100 ns, so those waves alone do not establish full-run SOA.
Reset stresses use actual Vgs/Vgd/Vds and the project 1.1 V / transient 1.29 V,
100 ps per sliding 10 ns allowance. Other-device and corner qualification stays unmeasured
until explicitly reported. A single hot-corner result cannot establish readiness.

| Variant | 80 ns reset SOA | Full256 SFDR / SNDR | Status |
|---|---|---|---|
| n6_k09 | Not yet measured | Not yet measured | In progress |
| n12_k09 | Not yet measured | Not yet measured | Prepared |
| n6_k09_d3 | Not yet measured | Not yet measured | Prepared |

Baseline full256 hot-SS SFDR/SNDR: 63.13694 / 63.06129 dB; H3/H5:
545.389 / 71.487 uV. Targets remain 85 / 80 dB. No formal pass or source promotion
is claimed by the present stage. Raw evidence is retained privately with hashes.
