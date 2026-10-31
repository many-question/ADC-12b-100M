# RESET-V24: test input-to-latch coupling devices

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

V23 retains complete polarity, reset, output validity and terminal-stress checks, but its weaker tail increases TT 30 mV delay to 55.258398 ps, failing the 50 ps gate. [RESET-V23.md](RESET-V23.md) preserves the stopped source, complete deterministic evidence and its comparison with V20. No noise benefit is claimed for that failed timing experiment.

V24 branches electrically from V20, restoring the 3 um tail and keeping its 0.5 um/30 nm Q shunts, clock and all five MOMs. Only MLNP/MLNN change from 12 um/30 nm/nf12 to 16 um/30 nm/nf16. Channel length and 1 um finger width remain fixed; total width and finger count both increase. The complete zero-warning N16 callback geometry is used, SHA-256 `f7dd3061987c03157e7411ed97c5554d5d6981d377691e3da1413bee8298ef85`. All other 21 MOS devices and every capacitor remain electrically identical to V20.

These two NMOS devices connect the input drains to Q and also participate in cross-coupled regeneration. V20's own short phase data show DP discrimination before appreciable correct Q transfer, with CKB already near its low value by +10 ps. Increasing these devices tests the coupling and regeneration trajectory while preserving the original tail drive. The change also increases capacitances and alters feedback and noise; no isolated transconductance or device-noise improvement is assumed.

Electrical SHA-256: `d1f39f9752433bf61e8c6d6727d0096a73c5b86e545e4317c7590a733411847d`. The [source](RESET-V24.txt) contains 23 MOS and 5 MOMs with complete RNL checked on a byte-identical mirror. SF/FS high/-40 are screened first, then TT on a useful pass, including the 50 ps delay limit at 30 mV. A matched short phase diagnosis follows only after those gates. Remaining known corners, actual-worst convergence, source-preserving promotion and original formal tests remain open. Canonical V19 and all genuine original records remain unchanged.

![Physical comparator with larger input-to-latch NMOS devices](https://raw.githubusercontent.com/many-question/ADC-12b-100M/e6c95aadd9ec412bcca1a03d4b1a625321630588/design/xtor/adc_comp/many-question-strongarm/reset-v24.png)

## Completed screen 20261031-094545-strongarm-reset-v24-screen

SF/high/-40 fails ten terminal pairs at the strict 1 V limit. FS/high/-40 passes. All 72 actual polarities including 10 uV, resets, timing and physical output-validity checks pass, but do not override the stress failure. V24 stops before TT, noise and further-corner expansion.

Actual clean source commit: `2c1aef96a2606ff4fc47dfaa81ec1c639faa586f`. Electrical SHA-256: `d1f39f9752433bf61e8c6d6727d0096a73c5b86e545e4317c7590a733411847d`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 55.198770 / 43.791040 | 21.861516 | 550.156856 | 36 / 36 | 0 | 0 | 0.99848 | 0 / 69 |
| sf_high_m40 | 70.660530 / 54.228602 | 20.368651 | 520.634761 | 36 / 36 | 0 | 0 | 1.00301 | 10 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69819 | 0.76429 |
| MINN | 0.69830 | 0.76448 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99309 | 0.99169 |
| MRDN | 0.99309 | 0.99168 |
| MLNP | 0.99076 | 0.98961 |
| MLNN | 0.99076 | 0.98960 |
| MLPP | 0.99313 | 0.99175 |
| MLPN | 0.99313 | 0.99175 |
| MRQP | 0.99836 | 1.00301 |
| MRQN | 0.99836 | 1.00301 |
| MOPN | 0.99848 | 1.00301 |
| MOPP | 0.99830 | 1.00295 |
| MONN | 0.99848 | 1.00301 |
| MONP | 0.99830 | 1.00295 |
| MDQP | 0.99848 | 1.00301 |
| MDQN | 0.99848 | 1.00301 |
| MDDP | 0.98344 | 0.98514 |
| MDDN | 0.98652 | 0.98759 |
| MCKN | 0.99346 | 0.99595 |
| MCKP | 0.99031 | 0.99000 |
| MBLEED | 0.99346 | 0.99595 |
| MUP | 0.99346 | 0.99595 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


The raw Q maxima are during reset after the falling clock crossing:

| Node | Peak V | Time ps | Since fall ps | CLKC V | CKB V |
|---|---:|---:|---:|---:|---:|
| QP | 1.003007138068 | 7117.971441243 | 12.971441243 | 0.000000000 | 0.982878275744 |
| QN | 1.003007134452 | 6717.971757045 | 12.971757045 | 0.000000000 | 0.982878276952 |

CKB is already near its high rail at the peak. The next source retains the N16 coupling devices and tests only Q reset-pull-down width 0.5 to 0.6 um at fixed 30 nm/nf1. The resulting reset level, stress, clock charge, full supply cost and noise must all be measured; this failed source establishes no coupling-stage noise benefit.

Full AVDD integrals over the same 36 cycles and 100 ps–14.5 ns window include physical reset and weak loads. Every supply probe is present and KCL closes. External ideal clock delivery remains outside this boundary.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 550.157436018 | 107.136820692 | 443.020615326 | 1640.915016955 |
| sf_high_m40 | 520.635305522 | 124.111669379 | 396.523636143 | 1407.687528636 |

Archive SHA-256: `246e2fd42e9be276d053a3d68b92d35d48ac6519fbd3922aa4abc3a0e61d78d4`. Every member was read back with CRC and SHA-256 verification before duplicate local raw files were removed; the owned remote run is absent. Power is reported only. Canonical V19 and every original formal result remain unchanged.
