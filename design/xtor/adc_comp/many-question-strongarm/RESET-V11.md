# RESET-V11: slightly stronger input precharge

V10 passes all-device stress and physical output validity at four key corners, but its SS low/hot reset takes 35.044926 ps against a 35 ps limit. This experiment changes only MRDP/MRDN from P2 to P2.2 um, with two fingers and L=30 nm. A new successful zero-warning callback supplies all geometry and parasitics. The lighter reset-gated Q loads, physical clock circuit and weak clock-floor load remain unchanged.

The [independent source](RESET-V11.txt) has 23 MOS and three MOM capacitors. Electrical SHA-256: `d04b9edb8a3d5b781494660d243866fb975b56be53a8d4c22da030ca694e2f5f`. Full RNL on its byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the rendered schematic was inspected.

![Slightly stronger input precharge](https://raw.githubusercontent.com/many-question/ADC-12b-100M/596782536a7b43a5a893660a926aa339927ea784/design/xtor/adc_comp/many-question-strongarm/reset-v11.png)

The four-key-corner screen checks all 69 MOS terminal pairs over the entire trace, actual decisions, CMP-15, delay/reset and AVDD energy. More input precharge also increases external clock load, so the clock-charge diagnostic remains under review and does not replace official CMP-14. No previous source performance is inherited.

## Completed screen 20261031-042049-strongarm-reset-v11-screen

All four initial corners pass full-trace device stress, delay/reset, actual decisions and CMP-15. SS low/hot reset is 34.241004 ps and cold-FF peak stress is 0.99845 V. TT 30 mV delay is 46.417214 ps. The remaining SF low/cold and SF high/27 key corners are being screened on this same electrical source before qualification expands. TT mixed-sequence clock charge is 15.743659 fF; this remains a diagnostic and does not establish official CMP-14.

Actual clean source commit: `49ca8a50c97c0584ebf73081b104a27c1d8f01e6`. Electrical SHA-256: `d04b9edb8a3d5b781494660d243866fb975b56be53a8d4c22da030ca694e2f5f`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 42.353244 / 32.076378 | 22.469423 | 875.715983 | 36 / 36 | 0 | 0 | 0.99046 | 0 / 69 |
| ff_high_m40 | 43.216930 / 34.978123 | 19.050707 | 820.648260 | 36 / 36 | 0 | 0 | 0.99845 | 0 / 69 |
| ss_low_125 | 76.687582 / 60.076386 | 34.241004 | 401.004981 | 36 / 36 | 0 | 0 | 0.82317 | 0 / 69 |
| tt_nom_27 | 57.956394 / 46.417214 | 24.653820 | 571.537169 | 36 / 36 | 0 | 0 | 0.91274 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.56507 | 0.68172 | 0.53616 | 0.59235 |
| MINN | 0.56515 | 0.68183 | 0.53615 | 0.59240 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99241 | 0.81000 | 0.90163 |
| MRDN | 0.99000 | 0.99241 | 0.81099 | 0.90163 |
| MLNP | 0.95938 | 0.98992 | 0.80205 | 0.89869 |
| MLNN | 0.95938 | 0.98992 | 0.80203 | 0.89869 |
| MLPP | 0.96513 | 0.99285 | 0.80594 | 0.90206 |
| MLPN | 0.96513 | 0.99285 | 0.80594 | 0.90206 |
| MRQP | 0.99000 | 0.99377 | 0.82317 | 0.91274 |
| MRQN | 0.99000 | 0.99377 | 0.82317 | 0.91274 |
| MOPN | 0.99046 | 0.99845 | 0.82317 | 0.91274 |
| MOPP | 0.98642 | 0.99812 | 0.82204 | 0.91218 |
| MONN | 0.99046 | 0.99845 | 0.82317 | 0.91274 |
| MONP | 0.98642 | 0.99812 | 0.82204 | 0.91218 |
| MDQP | 0.99046 | 0.99845 | 0.82317 | 0.91274 |
| MDQN | 0.99046 | 0.99845 | 0.82317 | 0.91274 |
| MDDP | 0.98497 | 0.98477 | 0.80767 | 0.89732 |
| MDDN | 0.98828 | 0.98770 | 0.81099 | 0.90049 |
| MCKN | 0.99000 | 0.99095 | 0.81276 | 0.90257 |
| MCKP | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MBLEED | 0.99000 | 0.99095 | 0.81276 | 0.90257 |
| MUP | 0.99000 | 0.99095 | 0.81276 | 0.90257 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-042452-strongarm-reset-v11-screen

The two additional SF corners reject V11 for expansion. SF low/cold has eight CMP-15 violations at small inputs, with a 33.300656 percent losing peak during regeneration. SF high/27 reaches 1.00281 V at Q during reset, failing ten terminal pairs. Thus the initial four-corner pass does not establish qualification. Timing/reset pass at both additional corners. No noise or full-corner sweep is launched for this failed version.

Actual clean source commit: `49ca8a50c97c0584ebf73081b104a27c1d8f01e6`. Electrical SHA-256: `d04b9edb8a3d5b781494660d243866fb975b56be53a8d4c22da030ca694e2f5f`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_27 | 57.830226 / 45.944297 | 21.697081 | 721.030932 | 36 / 36 | 0 | 0 | 1.00281 | 10 / 69 |
| sf_low_m40 | 83.658320 / 68.647366 | 24.736436 | 396.280198 | 36 / 36 | 0 | 8 | 0.82756 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_27 | sf_low_m40 |
|---|---:|---:|
| MINP | 0.70801 | 0.58895 |
| MINN | 0.70811 | 0.58906 |
| MTAIL | 0.99000 | 0.81000 |
| MRDP | 0.99007 | 0.81201 |
| MRDN | 0.99007 | 0.81320 |
| MLNP | 0.98791 | 0.80963 |
| MLNN | 0.98791 | 0.80963 |
| MLPP | 0.99043 | 0.81256 |
| MLPN | 0.99043 | 0.81256 |
| MRQP | 1.00281 | 0.82756 |
| MRQN | 1.00281 | 0.82756 |
| MOPN | 1.00281 | 0.82756 |
| MOPP | 1.00213 | 0.82682 |
| MONN | 1.00281 | 0.82756 |
| MONP | 1.00213 | 0.82682 |
| MDQP | 1.00281 | 0.82756 |
| MDQN | 1.00281 | 0.82756 |
| MDDP | 0.98560 | 0.81031 |
| MDDN | 0.98826 | 0.81320 |
| MCKN | 0.99267 | 0.81647 |
| MCKP | 0.99000 | 0.81000 |
| MBLEED | 0.99267 | 0.81647 |
| MUP | 0.99267 | 0.81647 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
