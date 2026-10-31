# BUFFER-V6: slower reset-clock edges and stronger buffer damping

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

B5 retains correct physical decisions and TT timing, but its cold-FF clock release, raw output and buffer nodes still cross below ground by 11 to 17 mV; the external output reaches 1.00833 V at reset. This experiment halves the clock driver from P4/N2 to P2/N1. The slower CKB edges are intended to reduce clock feedthrough and soften the clocked reset. XP/XN and BP/BN MOM capacitance increases from 2.06055 to 4.46051 fF; raw-node MOM capacitance remains 2.06055 fF. No other electrical change is made.

The changes consume delay and reset margin, so the first screen checks them together with terminal stress and physical output validity. All geometries reuse successful callbacks. The [independent source](BUFFER-V6.txt) has 29 MOS and nine MOM capacitors. Electrical SHA-256: `c0ac4c8d5b9dd4e9c552a20786159864e97d275efce7174e43fb89642f4924a1`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Slower clock edges and buffer damping](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fe173f9df274e8fa4fdddfbdb14f20208dc441fb/design/xtor/adc_comp/many-question-miyahara/buffer-v6.png)

The first screen uses TT, FF high/-40 C and SF low/-40 C, checking all 87 terminal pairs throughout the trace, actual decisions/outputs, delay/reset and measured AVDD energy. No performance claim is made at source freeze.

## Completed screen 20261031-035931-miyahara-buffer-v6-screen

Rejected for expansion. All three corners retain timing and physical validity, and CKB/XP/XN now pass cold-FF stress. Remaining negative extrema are RP/RN about -12.293 mV, BP/BN -12.208 mV and outputs about -13.736 mV; output positive peak is 1.004900 V. Eighteen terminal pairs fail. TT30mV is 47.197 ps and SF low/cold reset is 30.735 ps, so further blanket slew reduction would consume the remaining timing margin. The next experiment targets small steady-state rail offsets with physical transistor loads.

Actual clean source commit: `a5c8cea5ac85fc965a80e086a3d89c437e79c881`. Electrical SHA-256: `c0ac4c8d5b9dd4e9c552a20786159864e97d275efce7174e43fb89642f4924a1`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 42.988044 / 34.661852 | 19.689515 | 298.425987 | 36 / 36 | 0 | 0 | 1.00490 | 18 / 87 |
| sf_low_m40 | 72.558705 / 57.780686 | 30.735011 | 162.428110 | 36 / 36 | 0 | 0 | 0.83719 | 0 / 87 |
| tt_nom_27 | 58.768501 / 47.197390 | 26.965295 | 241.043727 | 36 / 36 | 0 | 0 | 0.91655 | 0 / 87 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_m40 | sf_low_m40 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.68810 | 0.59494 | 0.59760 |
| MINN | 0.68820 | 0.59504 | 0.59765 |
| MTAIL | 0.99000 | 0.81000 | 0.90000 |
| M14 | 0.99943 | 0.81893 | 0.90784 |
| M15 | 0.99926 | 0.81894 | 0.90778 |
| M12 | 0.99276 | 0.81419 | 0.90252 |
| M13 | 0.99276 | 0.81419 | 0.90252 |
| M10 | 0.99302 | 0.81645 | 0.90320 |
| M11 | 0.99302 | 0.81645 | 0.90320 |
| M6 | 0.99409 | 0.81645 | 0.90340 |
| M7 | 0.99409 | 0.81645 | 0.90340 |
| M8 | 0.99409 | 0.81629 | 0.90340 |
| M9 | 0.99409 | 0.81629 | 0.90340 |
| MCKN | 0.99757 | 0.82015 | 0.90763 |
| MCKP | 0.99758 | 0.81817 | 0.90706 |
| MRQP | 0.99757 | 0.82015 | 0.90763 |
| MRQN | 0.99757 | 0.82015 | 0.90763 |
| MAP | 0.99187 | 0.81187 | 0.90184 |
| MAN | 0.99187 | 0.81266 | 0.90184 |
| MBPP | 1.00229 | 0.82583 | 0.91227 |
| MBPN | 1.00225 | 0.82577 | 0.91219 |
| MOPP | 1.00374 | 0.82519 | 0.91259 |
| MOPN | 1.00490 | 0.83719 | 0.91655 |
| MBNP | 1.00229 | 0.82580 | 0.91228 |
| MBNN | 1.00225 | 0.82574 | 0.91220 |
| MONP | 1.00373 | 0.82519 | 0.91258 |
| MONN | 1.00490 | 0.83719 | 0.91655 |
| MDDP | 0.98233 | 0.80936 | 0.89482 |
| MDDN | 0.98581 | 0.81266 | 0.89835 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
