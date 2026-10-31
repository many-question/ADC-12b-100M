# BUFFER-V11: constrain clock feedthrough at both rails

Current disposition: rejected for expansion because two FS/high/-40 input-stage terminal pairs remain above 1.0 V.

B10 passes delay, reset and output validity at all ten measured corners, but CKB feedthrough fails stress at two newly measured corners. SF/high/-40 reaches 1.000656171 V, 1.038279 ps before the rising clock 50% crossing. FS/high/-40 reaches -11.143791 mV, 1.571604 ps before the falling crossing, producing 1.001143791 V terminal stress. The latter is the actual worst measured stress.

This experiment adds a weak P0.5um/100nm pull-up and N0.5um/500nm pull-down to CKB. Both use complete previously successful callback geometries with no warnings. The original 39 MOS and 9 MOM remain unchanged; all 41 MOS are checked individually. The persistent currents and any delay cost of these two new loads are included in the measured AVDD energy. They are physical devices, not ideal clamps.

The [independent source](BUFFER-V11.txt) has electrical SHA-256 `75fde3433404b4ab69723528ed5b66e47e7a2e2822c5bc73526a5b7b875259c6`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the schematic was inspected. The new drawing also corrects the inherited MAP/MAN label to the actual nf3 and updates its summary dimensions; these annotation corrections do not change those devices electrically.

![Physical CKB rail loads](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0c799462e700c1f74a9448031e14abdd56ec18e7/design/xtor/adc_comp/many-question-miyahara/buffer-v11.png)

Screen SF/high/-40 and FS/high/-40 first. Only after they pass, complete TT, SS low/hot, SF low/cold, FF high/cold and high/hot, SF high/27 and high/hot, and FS low/hot. Check every MOS terminal voltage over the complete trace, all 36 physical polarities and resets, validity, delay, regeneration time and AVDD energy. Keep the total session concurrency at or below six jobs. No prior noise, mismatch or capacitance performance is inherited.

Passing screening would be supplemental evidence. Canonical promotion and qualification use the existing official runner, with old records preserved and honestly marked stale until replaced.

## Completed screen 20261031-051303-miyahara-buffer-v11-screen

B11 fixes the two clock-rail feedthrough failures but still fails the FS/high/-40 internal-stage stress: M14 and M15 Vds reach 1.00092 V and 1.00091 V, respectively. XP reaches -10.919713 mV at rising-clock50%+11.480779 ps. These two pairs also failed in B10; removing its larger clock failure exposes this remaining limitation. CKB now remains within 0.037750 to 0.988618 V at that corner. SF/high/-40 passes full-trace stress at 0.99937 V. Both corners pass delay, reset, regeneration, output validity, all 36 correct polarities including 10 uV, and all 36 resets. No expansion, noise, MC or canonical promotion for B11.

Actual clean source commit: `6aee02ebec2902a33ede291fbd98397031ea582b`. Electrical SHA-256: `75fde3433404b4ab69723528ed5b66e47e7a2e2822c5bc73526a5b7b875259c6`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 51.982448 / 42.686405 | 19.976651 | 644.835334 | 36 / 36 | 0 | 0 | 1.00092 | 2 / 123 |
| sf_high_m40 | 56.264000 / 46.289691 | 20.475037 | 685.727757 | 36 / 36 | 0 | 0 | 0.99937 | 0 / 123 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70288 | 0.76806 |
| MINN | 0.70300 | 0.76826 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 1.00092 | 0.99802 |
| M15 | 1.00091 | 0.99801 |
| M12 | 0.99305 | 0.99354 |
| M13 | 0.99305 | 0.99354 |
| M10 | 0.98632 | 0.98133 |
| M11 | 0.98633 | 0.98133 |
| M6 | 0.99324 | 0.99684 |
| M7 | 0.99324 | 0.99684 |
| M8 | 0.99324 | 0.99684 |
| M9 | 0.99324 | 0.99684 |
| MCKN | 0.99000 | 0.99151 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99324 | 0.99684 |
| MRQN | 0.99324 | 0.99684 |
| MAP | 0.99317 | 0.99208 |
| MAN | 0.99317 | 0.99208 |
| MBPP | 0.98979 | 0.98364 |
| MBPN | 0.99919 | 0.99937 |
| MOPP | 0.98706 | 0.97876 |
| MOPN | 0.99919 | 0.99937 |
| MBNP | 0.98978 | 0.98364 |
| MBNN | 0.99918 | 0.99937 |
| MONP | 0.98707 | 0.97876 |
| MONN | 0.99918 | 0.99937 |
| MDDP | 0.98440 | 0.98665 |
| MDDN | 0.98724 | 0.98811 |
| MUPRP1 | 0.99324 | 0.99684 |
| MUPRN1 | 0.99324 | 0.99684 |
| MUPBP1 | 0.99919 | 0.99937 |
| MUPBN1 | 0.99918 | 0.99937 |
| MUPOUTP1 | 0.99000 | 0.99427 |
| MUPOUTN1 | 0.99000 | 0.99427 |
| MDNOUTP1 | 0.98936 | 0.99427 |
| MDNOUTP2 | 0.98936 | 0.99427 |
| MDNOUTN1 | 0.98937 | 0.99427 |
| MDNOUTN2 | 0.98937 | 0.99427 |
| MCKUP | 0.99000 | 0.99151 |
| MBLEED | 0.99000 | 0.99151 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
