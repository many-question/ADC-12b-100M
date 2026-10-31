# BUFFER-V4: direct input precharge and stronger clocked reset

B3 still shows input-drain overshoot during the delayed CKR rising edge and negative raw-output excursions during reset. This experiment returns to the B2 physical buffer and changes the reset path. It removes the CKR inverter and its input-precharge PMOS pair; the remaining direct-CLKC input precharge uses P1.6 um on each side. Each input drain receives a diode-connected N0.5 um / 500 nm load to create high-level headroom. These are actual PDK devices whose current is included in energy.

The raw-output reset NMOS increases from N2 to N8. CKB retains one physical CMOS inverter, with its damping MOM increased from 4.46051 to 14.06 fF. The first output-buffer NMOS becomes N2 while the output inverter remains P4/N2. This should strengthen the reset clamp and reduce clock feedthrough, while the earlier input-precharge release may recover delay. Timing, output validity, all-terminal stress and energy must establish the result; none is inherited from earlier versions.

The [independent source](BUFFER-V4.txt) has 29 MOS and three MOM capacitors. All geometries exactly reuse successful warning-free callbacks. Electrical SHA-256: `91f4c449bd4406e30da73e25fe881a2c2d2816c8cfb47d0e9ab43b920fdbb1fb`. RNL core 0.5.2 checks the byte-identical Spectre mirror with 0 errors, 0 warnings and 0 hints.

![Direct input precharge and physical clocked reset](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fe173f9df274e8fa4fdddfbdb14f20208dc441fb/design/xtor/adc_comp/many-question-miyahara/buffer-v4.png)

The first screen uses TT nominal 27 C, FF high/-40 C and SF low/-40 C, checking all 87 MOS terminal pairs over the entire trace, actual decisions, CMP-15, delay, reset and AVDD energy. This source-freeze commit makes no pass claim. The canonical source and its official records remain unchanged.

## Completed screen 20261031-034523-miyahara-buffer-v4-screen

Rejected for expansion because cold-FF stress still fails. Direct precharge plus input diode loads removes input-drain overshoot: DN peaks at 0.985811 V. Timing and physical validity pass, with TT30mV 43.714 ps and reset 16.589 ps. The dominant peak shifts to the external output at reset (1.021897 V); the raw node also dips to -24.295 mV during evaluation-clock release, and the buffer node reaches -27.834 mV during reset. Smaller residual excursions remain on the clock and intermediate inverter nodes.

Actual clean source commit: `8d99d664cdd9c7139b3dd57f4b26f64d36038512`. Electrical SHA-256: `91f4c449bd4406e30da73e25fe881a2c2d2816c8cfb47d0e9ab43b920fdbb1fb`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 41.858925 / 33.038392 | 12.604160 | 330.189458 | 36 / 36 | 0 | 0 | 1.02190 | 26 / 87 |
| sf_low_m40 | 68.982012 / 53.604120 | 19.019993 | 179.007044 | 36 / 36 | 0 | 0 | 0.85530 | 0 / 87 |
| tt_nom_27 | 55.896331 / 43.714417 | 16.588879 | 264.350715 | 36 / 36 | 0 | 0 | 0.93715 | 0 / 87 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_m40 | sf_low_m40 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.68787 | 0.59469 | 0.59739 |
| MINN | 0.68797 | 0.59480 | 0.59744 |
| MTAIL | 0.99000 | 0.81000 | 0.90000 |
| M14 | 1.00133 | 0.82030 | 0.90983 |
| M15 | 1.00139 | 0.82026 | 0.90985 |
| M12 | 0.99548 | 0.81846 | 0.90524 |
| M13 | 0.99548 | 0.81846 | 0.90524 |
| M10 | 0.99075 | 0.81803 | 0.90059 |
| M11 | 0.99075 | 0.81803 | 0.90059 |
| M6 | 0.99964 | 0.82521 | 0.90904 |
| M7 | 0.99964 | 0.82521 | 0.90904 |
| M8 | 0.99964 | 0.82521 | 0.90904 |
| M9 | 0.99964 | 0.82521 | 0.90904 |
| MCKN | 1.00024 | 0.82561 | 0.91174 |
| MCKP | 1.00365 | 0.82635 | 0.91378 |
| MRQP | 1.00267 | 0.82566 | 0.91237 |
| MRQN | 1.00267 | 0.82566 | 0.91237 |
| MAP | 0.99187 | 0.81187 | 0.90184 |
| MAN | 0.99187 | 0.81266 | 0.90184 |
| MBPP | 1.01783 | 0.84981 | 0.93176 |
| MBPN | 1.01419 | 0.82984 | 0.92108 |
| MOPP | 1.01783 | 0.84981 | 0.93176 |
| MOPN | 1.02190 | 0.85530 | 0.93715 |
| MBNP | 1.01783 | 0.84981 | 0.93176 |
| MBNN | 1.01415 | 0.82973 | 0.92103 |
| MONP | 1.01783 | 0.84981 | 0.93176 |
| MONN | 1.02190 | 0.85530 | 0.93715 |
| MDDP | 0.98233 | 0.80936 | 0.89483 |
| MDDN | 0.98581 | 0.81266 | 0.89835 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
