# BUFFER-V5: damp measured raw and buffer excursions

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

B4 removes input-drain overvoltage and gains timing margin, but its stronger N8 reset injects a negative step into RP/RN as CKB falls. The buffer transition also produces external-output overshoot during reset. This experiment reduces raw reset to N4 and the physical clock driver to P4/N2. It adds one validated 2.06055 fF MOM at each XP/XN, RP/RN and BP/BN node, the three node families with measured undershoot or excessive slew. External 10 fF loads and all testbench stimuli remain unchanged.

The capacitors and slower reset/clock edges may reduce voltage peaks while adding decision delay. The previous TT 30 mV delay of 43.714 ps provides a measured margin for this experiment; it is not inherited as a pass. All capacitances are real PDK MOM instances. No ideal clamp, latch or event capture is used.

The [independent source](BUFFER-V5.txt) contains 29 MOS and nine MOM capacitors; all geometries reuse successful warning-free callbacks. Electrical SHA-256: `ecfaae10a0ad2b33a7c5fea90bcb4fc4d00dff60662c20f1c534ce3f0b9578ad`. The complete byte-identical Spectre mirror passes RNL core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Physical node damping](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fe173f9df274e8fa4fdddfbdb14f20208dc441fb/design/xtor/adc_comp/many-question-miyahara/buffer-v5.png)

The first TT, FF high/-40 C and SF low/-40 C screen checks all 87 terminal pairs throughout the trace, actual decisions/outputs, delay/reset and AVDD energy. This source-freeze commit makes no performance claim.

## Completed screen 20261031-035219-miyahara-buffer-v5-screen

Rejected for expansion: cold-FF stress improves from 1.02190 V to 1.00833 V, but 23 terminal pairs still exceed the limit. All three corners pass timing and physical output validity. Measured cold minima are CKB -11.367 mV, XP/XN about -10.3 mV, RP/RN about -15.5 mV and BP/BN -16.992 mV. External-output minimum and maximum are about -14.78 mV and 1.00833 V. The remaining problem is edge-coupled slew at these nodes; B6 weakens clock edges and increases the intermediate/buffer damping capacitors.

Actual clean source commit: `0912fa38298e63a4d53fb9f818181e62709195b6`. Electrical SHA-256: `ecfaae10a0ad2b33a7c5fea90bcb4fc4d00dff60662c20f1c534ce3f0b9578ad`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 42.340616 / 33.764138 | 16.367102 | 307.825376 | 36 / 36 | 0 | 0 | 1.00833 | 23 / 87 |
| sf_low_m40 | 70.904893 / 55.659550 | 25.390303 | 166.819631 | 36 / 36 | 0 | 0 | 0.83820 | 0 / 87 |
| tt_nom_27 | 57.406077 / 45.405801 | 21.883798 | 247.987723 | 36 / 36 | 0 | 0 | 0.92025 | 0 / 87 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_m40 | sf_low_m40 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.68797 | 0.59483 | 0.59749 |
| MINN | 0.68808 | 0.59494 | 0.59756 |
| MTAIL | 0.99000 | 0.81000 | 0.90000 |
| M14 | 1.00025 | 0.81960 | 0.90874 |
| M15 | 1.00029 | 0.81960 | 0.90875 |
| M12 | 0.99301 | 0.81448 | 0.90276 |
| M13 | 0.99301 | 0.81448 | 0.90276 |
| M10 | 0.99044 | 0.81723 | 0.90196 |
| M11 | 0.99044 | 0.81723 | 0.90196 |
| M6 | 0.99479 | 0.81723 | 0.90415 |
| M7 | 0.99479 | 0.81723 | 0.90415 |
| M8 | 0.99479 | 0.81721 | 0.90415 |
| M9 | 0.99479 | 0.81721 | 0.90415 |
| MCKN | 0.99965 | 0.82388 | 0.91039 |
| MCKP | 1.00137 | 0.82306 | 0.91117 |
| MRQP | 1.00087 | 0.82388 | 0.91040 |
| MRQN | 1.00087 | 0.82388 | 0.91040 |
| MAP | 0.99187 | 0.81187 | 0.90184 |
| MAN | 0.99187 | 0.81266 | 0.90184 |
| MBPP | 1.00699 | 0.83033 | 0.91714 |
| MBPN | 1.00540 | 0.82449 | 0.91335 |
| MOPP | 1.00699 | 0.83033 | 0.91714 |
| MOPN | 1.00833 | 0.83820 | 0.92025 |
| MBNP | 1.00699 | 0.83033 | 0.91714 |
| MBNN | 1.00537 | 0.82449 | 0.91331 |
| MONP | 1.00699 | 0.83033 | 0.91714 |
| MONN | 1.00833 | 0.83820 | 0.92025 |
| MDDP | 0.98233 | 0.80936 | 0.89482 |
| MDDN | 0.98581 | 0.81266 | 0.89835 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
