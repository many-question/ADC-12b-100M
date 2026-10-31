# RESET-V27: larger Q storage with N8 coupling devices

V26 passes its three initial deterministic corners, but its matched short noise diagnosis retains the same wrong cycle 54 as V20. Descriptive Q SNR changes from 1.896073 to 1.917068 at +30 ps and from 3.346148 to 3.261936 at +40 ps. At -20 ps, Q differential standard deviations remain 0.361281/0.373230 mV across the two input levels; the wrong cycle already has -0.812609 mV Q differential. These phase observations do not establish a noise source or completed decision. [RESET-V26.md](RESET-V26.md) preserves the full result.

This experiment changes only CQP/CQN from 20 to 44 fingers, nominally 5.66049 to 12.86040 fF. All 23 MOS devices and the other three MOMs remain electrically identical to V26, including its N8 coupling devices, 0.5 um/30 nm Q reset shunts and 3 um tail. Finger length, width, spacing and metal range are unchanged. The zero-warning capacitor callback SHA-256 is `7c980b3d9fa9ea317087d837feea5cab285a7ff84a9de34c7d0fe95f6b90b851`.

The added storage tests whether early Q variation and release disturbance decrease enough to improve signal-to-noise after transfer. It may also attenuate the signal and slow regeneration and reset. V26 has 2.823328 ps of TT 30 mV delay margin; an earlier smaller capacitance step on V19 is not a guarantee for this source. TT and SS/low/125 timing and reset are therefore checked together with both high-voltage cold stress corners before any short noise run. No noise improvement is assumed.

Electrical SHA-256: `7b20b19a2434da94d732f9785a3a8f1a2138d17ed4f4854dbdc5ab1a6cff18df`. The [source](RESET-V27.txt) contains 23 MOS and 5 MOMs with complete RNL checked on a byte-identical mirror. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and original formal tests remain open. Canonical V19 and every genuine original record are unchanged.

![Physical comparator with larger Q capacitors](reset-v27.png)

## Completed screen 20261031-110456-strongarm-reset-v27-screen

All 144 actual polarities including 10 uV and all 144 resets pass, together with timing, physical output validity and all 69 terminal pairs at each corner. These deterministic gates do not establish formal noise.

Actual clean source commit: `ca508316feb0325caaf9ab043a080b82d773c74a`. Electrical SHA-256: `7b20b19a2434da94d732f9785a3a8f1a2138d17ed4f4854dbdc5ab1a6cff18df`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 57.265711 / 44.110802 | 21.125640 | 544.329934 | 36 / 36 | 0 | 0 | 0.99542 | 0 / 69 |
| sf_high_m40 | 73.039179 / 54.721762 | 19.676703 | 514.538705 | 36 / 36 | 0 | 0 | 0.99680 | 0 / 69 |
| ss_low_125 | 91.658688 / 67.183973 | 33.257508 | 303.827011 | 36 / 36 | 0 | 0 | 0.81632 | 0 / 69 |
| tt_nom_27 | 66.385960 / 49.837598 | 23.747424 | 408.901925 | 36 / 36 | 0 | 0 | 0.90609 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.69914 | 0.76477 | 0.53566 | 0.60191 |
| MINN | 0.69927 | 0.76498 | 0.53565 | 0.60200 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99323 | 0.99186 | 0.81000 | 0.90135 |
| MRDN | 0.99323 | 0.99186 | 0.81108 | 0.90135 |
| MLNP | 0.99110 | 0.99000 | 0.80203 | 0.89915 |
| MLNN | 0.99110 | 0.99000 | 0.80201 | 0.89915 |
| MLPP | 0.99341 | 0.99207 | 0.80468 | 0.90146 |
| MLPN | 0.99341 | 0.99207 | 0.80468 | 0.90146 |
| MRQP | 0.99341 | 0.99353 | 0.81593 | 0.90440 |
| MRQN | 0.99341 | 0.99353 | 0.81593 | 0.90440 |
| MOPN | 0.99542 | 0.99680 | 0.81593 | 0.90494 |
| MOPP | 0.99438 | 0.99561 | 0.81540 | 0.90450 |
| MONN | 0.99542 | 0.99680 | 0.81593 | 0.90494 |
| MONP | 0.99438 | 0.99561 | 0.81540 | 0.90450 |
| MDQP | 0.99453 | 0.99595 | 0.81632 | 0.90609 |
| MDQN | 0.99453 | 0.99595 | 0.81632 | 0.90609 |
| MDDP | 0.98360 | 0.98524 | 0.80775 | 0.89739 |
| MDDN | 0.98674 | 0.98774 | 0.81108 | 0.90057 |
| MCKN | 0.99345 | 0.99595 | 0.81632 | 0.90609 |
| MCKP | 0.99031 | 0.99000 | 0.81334 | 0.90065 |
| MBLEED | 0.99345 | 0.99595 | 0.81632 | 0.90609 |
| MUP | 0.99345 | 0.99595 | 0.81632 | 0.90609 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-111217-strongarm-reset-v27-screen

All 72 actual polarities including 10 uV and all 72 resets pass, together with timing, physical output validity and all 69 terminal pairs at each corner. These deterministic gates do not establish formal noise.

Actual clean source commit: `ca508316feb0325caaf9ab043a080b82d773c74a`. Electrical SHA-256: `7b20b19a2434da94d732f9785a3a8f1a2138d17ed4f4854dbdc5ab1a6cff18df`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_m40 | 73.045047 / 54.722633 | 19.629803 | 514.554669 | 36 / 36 | 0 | 0 | 0.99680 | 0 / 69 |
| tt_nom_27 | 66.393754 / 49.838320 | 23.660077 | 408.916654 | 36 / 36 | 0 | 0 | 0.90609 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_m40 | tt_nom_27 |
|---|---:|---:|
| MINP | 0.76476 | 0.60191 |
| MINN | 0.76498 | 0.60201 |
| MTAIL | 0.99000 | 0.90000 |
| MRDP | 0.99186 | 0.90135 |
| MRDN | 0.99186 | 0.90135 |
| MLNP | 0.99000 | 0.89915 |
| MLNN | 0.99000 | 0.89915 |
| MLPP | 0.99208 | 0.90147 |
| MLPN | 0.99208 | 0.90147 |
| MRQP | 0.99353 | 0.90440 |
| MRQN | 0.99353 | 0.90440 |
| MOPN | 0.99680 | 0.90495 |
| MOPP | 0.99561 | 0.90450 |
| MONN | 0.99680 | 0.90495 |
| MONP | 0.99561 | 0.90450 |
| MDQP | 0.99595 | 0.90609 |
| MDQN | 0.99595 | 0.90609 |
| MDDP | 0.98524 | 0.89739 |
| MDDN | 0.98774 | 0.90057 |
| MCKN | 0.99595 | 0.90609 |
| MCKP | 0.99000 | 0.90065 |
| MBLEED | 0.99595 | 0.90609 |
| MUP | 0.99595 | 0.90609 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


### Raw peak and complete-supply audits for the new gates

Run `20261031-110456-strongarm-reset-v27-screen` has the following independently recomputed, unrounded full-trace maxima.

| Corner | Device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| fs_high_m40 | MOPN ds | 0.995415857972 | 4584.142027607 | -194.651170963 | 5.348829037 |
| sf_high_m40 | MONN ds | 0.996799525655 | 3200.474345289 | -194.124344149 | 5.875655851 |
| ss_low_125 | MDQP gs | 0.816315253099 | 183684.746900604 | -2.768910398 | 197.231089602 |
| tt_nom_27 | MDQP gs | 0.906088107932 | 93911.892068075 | -3.122926088 | -203.122926088 |

All supply probes are present and KCL closes to numerical precision. The complete AVDD integrals cover all 36 mixed cycles from 100 ps to 14.5 ns, including reset and physical weak loads.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 544.330428181 | 100.009300760 | 444.321127421 | 1640.915033862 |
| sf_high_m40 | 514.539256094 | 117.140554262 | 397.398701832 | 1407.687495035 |
| ss_low_125 | 303.827601621 | 72.878757573 | 230.948844048 | 797.179790241 |
| tt_nom_27 | 408.902291928 | 89.282426247 | 319.619865681 | 1174.561976866 |

Raw/deck evidence and every audit are preserved under archive SHA-256 `16e93730ade5dbacd5701c08f9812ba1044514881b13e2353a937e4e44a8f574`. Every entry was read back with CRC and SHA-256 verification before duplicate raw files were removed; the owned remote run is absent.

Run `20261031-111217-strongarm-reset-v27-screen` has the following independently recomputed, unrounded full-trace maxima.

| Corner | Device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| sf_high_m40 | MOPN ds | 0.996799425196 | 3200.574804420 | -194.132467015 | 5.867532985 |
| tt_nom_27 | MDQP gs | 0.906088215042 | 93911.784958343 | -3.113159744 | 196.886840256 |

All supply probes are present and KCL closes to numerical precision. The complete AVDD integrals cover all 36 mixed cycles from 100 ps to 14.5 ns, including reset and physical weak loads.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| sf_high_m40 | 514.554759614 | 117.156433942 | 397.398325672 | 1407.687495035 |
| tt_nom_27 | 408.916728932 | 89.296691225 | 319.620037707 | 1174.561976866 |

Raw/deck evidence and every audit are preserved under archive SHA-256 `99bd68a940558c3fbbe417e4fc18b16a89b769c550242a355c8510a636f88264`. Every entry was read back with CRC and SHA-256 verification before duplicate raw files were removed; the owned remote run is absent.

### Numerical convergence

The same electrical source is repeated with 0.125 ps, reltol 1e-7 and vabstol 1e-9. All actual polarities, resets, output validity, timing and terminal pairs still pass. Deltas below are tighter minus initial; all per-pair changes are retained in the archived comparison.

| Corner | 1 mV delay delta ps | 30 mV delay delta ps | Reset delta ps | Largest absolute pair-peak change V |
|---|---:|---:|---:|---:|
| sf_high_m40 | +0.005868151 | +0.000870216 | -0.046899604 | 0.00001 |
| tt_nom_27 | +0.007794814 | +0.000721559 | -0.087347257 | 0.00001 |

Tighter TT 30 mV delay is 49.838319918 ps, leaving 0.161680082 ps to 50 ps. This remains a thin measured margin. The four initial corners retain all 144 nominal-cycle polarities and resets, followed by 72 tighter repeats. A matched short diagnosis against V26 follows; no capacitance, noise or full-corner qualification is inherited.
