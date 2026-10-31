# RESET-V20: test Q release-stage charge storage

Canonical V19 passes all ten private key corners, actual-worst numerical convergence and the original TT input/clock capacitance and kickback tests. Its original 17 x 512 TT noise run fails at 218.770058633 uV rms, with a 95% profile interval of 210.31–227.64 uV against 200 uV. All 8704 samples are present and resolved; the largest Gaussian-fit standardized residual is 3.784980, so a purely Gaussian mechanism is not established. The genuine failure remains in [FORMAL-RESET-V19.md](FORMAL-RESET-V19.md), and V19 qualification expansion stops.

Earlier full physical observations identified the reset-release Q trajectory as a decision-sensitive stage. V19's short matched diagnostic has one wrong polarity at cycle 54, with complete reset and no new early-to-final sign changes. At +30 ps the two input levels have Q differential standard deviations about 0.983/0.930 mV. The V16-to-V18 improvement changed both Q shunts and capacitors, so it did not isolate a capacitor effect. This revision now tests only Q-node charge storage, without assuming a kT/C scaling law or transferring the Miyahara noise conclusion.

Only CQP/CQN change from 16 to 20 fingers, nominally 4.46 to 5.66049 fF. The existing successful, zero-warning capacitor callback is reused exactly, SHA-256 `613c7aa6a617bd67d2699ba18a547794f801dbaee33aeab31e6b964b5ba9cc5d`. All 23 MOS devices and the other three MOMs remain electrically identical, including MCKN N4, MCKP P2.7 and both N0.5 Q shunts. Additional Q loading can delay regeneration and increase reset charge; those costs and the actual differential mean/variance must be measured.

Electrical SHA-256: `fb5dcf65ea818e14a24913b753c01226796d8f3f06aa9136fd779f9298cb6b60`. The [source](RESET-V20.txt) contains 23 MOS and 5 MOMs, with complete RNL checked on a byte-identical mirror. First test SF/high/-40 and FS/high/-40, then TT timing and a matched short phase diagnosis. Only a useful result warrants remaining known corners, actual-worst convergence, source-preserving promotion and genuine original formal tests. Canonical V19 and every older result remain preserved; no previous pass transfers.

![Physical comparator with larger Q capacitors](reset-v20.png)

## Completed screen 20261031-084147-strongarm-reset-v20-screen

Both high-voltage cold corners pass all 72 actual polarities including 10 uV, all 72 resets, timing, physical output validity and all 69 terminal pairs. No formal noise benefit is inferred.

Actual clean source commit: `810b72da43f53a5907bbedc3d55a890a24a98c67`. Electrical SHA-256: `fb5dcf65ea818e14a24913b753c01226796d8f3f06aa9136fd779f9298cb6b60`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 53.756647 / 42.642013 | 21.054437 | 541.343381 | 36 / 36 | 0 | 0 | 0.99693 | 0 / 69 |
| sf_high_m40 | 68.764171 / 52.868261 | 19.467656 | 510.985212 | 36 / 36 | 0 | 0 | 0.99840 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69838 | 0.76432 |
| MINN | 0.69850 | 0.76452 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99323 | 0.99192 |
| MRDN | 0.99323 | 0.99192 |
| MLNP | 0.99097 | 0.98990 |
| MLNN | 0.99097 | 0.98990 |
| MLPP | 0.99334 | 0.99209 |
| MLPN | 0.99334 | 0.99209 |
| MRQP | 0.99607 | 0.99831 |
| MRQN | 0.99607 | 0.99831 |
| MOPN | 0.99693 | 0.99840 |
| MOPP | 0.99675 | 0.99828 |
| MONN | 0.99693 | 0.99840 |
| MONP | 0.99675 | 0.99828 |
| MDQP | 0.99693 | 0.99840 |
| MDQN | 0.99693 | 0.99840 |
| MDDP | 0.98352 | 0.98520 |
| MDDN | 0.98664 | 0.98767 |
| MCKN | 0.99345 | 0.99595 |
| MCKP | 0.99031 | 0.99000 |
| MBLEED | 0.99345 | 0.99595 |
| MUP | 0.99345 | 0.99595 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-084834-strongarm-reset-v20-screen

TT passes all 36 actual polarities including 10 uV, all resets, timing, physical output validity and all 69 terminal pairs. The next step is the matched short Q-phase noise diagnosis before broader expansion.

Actual clean source commit: `810b72da43f53a5907bbedc3d55a890a24a98c67`. Electrical SHA-256: `fb5dcf65ea818e14a24913b753c01226796d8f3f06aa9136fd779f9298cb6b60`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 62.091895 / 47.862333 | 23.672701 | 406.390516 | 36 / 36 | 0 | 0 | 0.90741 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.60150 |
| MINN | 0.60158 |
| MTAIL | 0.90000 |
| MRDP | 0.90124 |
| MRDN | 0.90124 |
| MLNP | 0.89882 |
| MLNN | 0.89882 |
| MLPP | 0.90133 |
| MLPN | 0.90133 |
| MRQP | 0.90741 |
| MRQN | 0.90741 |
| MOPN | 0.90741 |
| MOPP | 0.90725 |
| MONN | 0.90741 |
| MONP | 0.90725 |
| MDQP | 0.90741 |
| MDQN | 0.90741 |
| MDDP | 0.89730 |
| MDDN | 0.90045 |
| MCKN | 0.90609 |
| MCKP | 0.90065 |
| MBLEED | 0.90609 |
| MUP | 0.90609 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
