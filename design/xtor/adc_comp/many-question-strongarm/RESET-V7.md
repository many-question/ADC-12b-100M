# RESET-V7: physical diode-connected shunt loads

V6 retains a reset peak caused by charge arriving while the opposite Q node and the compensation clock rise. This experiment returns to V2 direct-clock precharge and removes the compensation clock path. Each Q node receives a diode-connected N1 um / 30 nm load, and each input drain receives a weaker N0.5 um / 500 nm load. Their high-level conduction is intended to create voltage headroom and dissipate edge-coupled charge. Gate and drain are physically connected, so these are nonlinear MOS loads, not ideal voltage clamps.

The loads may change common-mode evolution, noise, decision gain and static energy. All of these remain unestablished for this source. The NMOS geometries exactly reuse successful warning-free callbacks; no circuit performance is inherited. The [independent source](RESET-V7.txt) contains 19 MOS and two MOM capacitors. Electrical SHA-256: `a62049295cc9343d260d27b6cbfdba646d1c6ce8d02643de7fea1bed2a46e0e0`. The byte-identical Spectre mirror passes full RNL core 0.5.2 checks with 0 errors, 0 warnings and 0 hints.

![Diode-loaded direct-clock StrongARM](https://raw.githubusercontent.com/many-question/ADC-12b-100M/596782536a7b43a5a893660a926aa339927ea784/design/xtor/adc_comp/many-question-strongarm/reset-v7.png)

The first screen checks TT, FF high cold/hot and SS low/hot, with all 57 terminal pairs over the entire trace, actual decisions, output validity, timing and exact AVDD energy. No performance pass is claimed at source freeze.

## Completed screen 20261031-034235-strongarm-reset-v7-screen

Rejected for expansion despite passing every full-trace terminal-stress check at the four screened corners. Persistent Q shunt current changes the common-mode decision trajectory: CMP-15 fails 12/20/12/8 cycles at TT/FF cold/FF hot/SS, respectively, with losing peaks up to 37.175 percent of VDD. All 36 cycles per corner decide correctly, so this is a physical losing-output excursion, not an undecided result. TT 30mV delay also fails at 50.759 ps. Q headroom is useful, but loading during evaluation must be removed.

Actual clean source commit: `a2574835cbc338c1a9660e234451c6d550951091`. Electrical SHA-256: `a62049295cc9343d260d27b6cbfdba646d1c6ce8d02643de7fea1bed2a46e0e0`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 43.241601 / 32.277376 | 16.969802 | 1001.804205 | 36 / 36 | 0 | 12 | 0.99000 | 0 / 57 |
| ff_high_m40 | 47.486131 / 40.180154 | 14.729184 | 970.069657 | 36 / 36 | 0 | 20 | 0.99631 | 0 / 57 |
| ss_low_125 | 82.965342 / 65.335442 | 25.969466 | 437.171815 | 36 / 36 | 0 | 8 | 0.81750 | 0 / 57 |
| tt_nom_27 | 62.267044 / 50.759125 | 19.037287 | 648.450061 | 36 / 36 | 0 | 12 | 0.90808 | 0 / 57 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.56466 | 0.68133 | 0.53583 | 0.59302 |
| MINN | 0.56470 | 0.68156 | 0.53582 | 0.59319 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99277 | 0.81000 | 0.90192 |
| MRDN | 0.99000 | 0.99277 | 0.81198 | 0.90192 |
| MLNP | 0.90989 | 0.95139 | 0.76632 | 0.86294 |
| MLNN | 0.90989 | 0.95139 | 0.76630 | 0.86294 |
| MLPP | 0.95872 | 0.99371 | 0.80607 | 0.90284 |
| MLPN | 0.95872 | 0.99371 | 0.80607 | 0.90284 |
| MRQP | 0.99000 | 0.99371 | 0.81000 | 0.90284 |
| MRQN | 0.99000 | 0.99371 | 0.81000 | 0.90284 |
| MOPN | 0.98971 | 0.99631 | 0.81750 | 0.90808 |
| MOPP | 0.98520 | 0.99626 | 0.81326 | 0.90561 |
| MONN | 0.98971 | 0.99631 | 0.81750 | 0.90808 |
| MONP | 0.98520 | 0.99626 | 0.81326 | 0.90562 |
| MDQP | 0.97330 | 0.99071 | 0.80199 | 0.89675 |
| MDQN | 0.97330 | 0.99071 | 0.80199 | 0.89675 |
| MDDP | 0.98605 | 0.98549 | 0.80878 | 0.89790 |
| MDDN | 0.98910 | 0.98818 | 0.81198 | 0.90086 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
