# RESET-V6: bound the compensated clock and input recharge

V5 separates three remaining events: early clock/Q excursions, a reset Q peak while CKB is still rising, and DP/DN injection at an input transition during reset. This experiment changes the input precharge PMOS from 1 to 1.6 um, reduces the clock inverter PMOS from 1 to 0.5 um, and adds a weak CKB discharge NMOS (W=0.5 um, L=500 nm, gate tied to AVDD). All three new geometries have successful, warning-free callbacks.

The weak discharge gives CKB a defined DC load and may create high-level headroom; the smaller PMOS slows its rising edge and advances its falling edge relative to the input clock. Both changes aim to reduce positive compensation current during reset while improving early cancellation. Stronger input precharge targets the separate input-step excursion. The reduced clock PMOS also offsets some of the added direct input capacitance. DC current, clock swing, delay and exact device peaks are measured, not assumed. There is no extra supply, behavioral control or Q-node keeper.

The independent [RESET-V6.txt](RESET-V6.txt) has 18 MOS and five MOM capacitors. Electrical SHA-256: `195e42741ebe64933fc373400bcc375fb4f3b4aba823ac4b188b721ff6359ec5`. Full RNL on a byte-identical `.scs` mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Clock-load and input-precharge revision](https://raw.githubusercontent.com/many-question/ADC-12b-100M/e45f2ad7bea3b45f5822eae18549b326c19fc727/design/xtor/adc_comp/many-question-strongarm/reset-v6.png)

The first screen uses TT, FF high cold/hot and SS low/hot at the same 0.5 ps settings, checking all 54 MOS terminal pairs, actual decisions and output validity, delay, reset and total AVDD energy. This source-freeze commit makes no performance claim.

## Completed screen 20261031-032658-strongarm-reset-v6-screen

Rejected for expansion: timing and actual output validity pass, but high-voltage stress remains. Cold FF reaches 1.02210 V at the Q reset event, worse than V5. At that peak the opposite Q is still rising and CKB is near 0.40 V. The weaker clock pull-up does not eliminate the coupled charge. Input-transition DN stress also remains at 1.00149 V.

Actual clean source commit: `6535ec4e6615ed6332af20fffcfbc9284b394c1b`. Electrical SHA-256: `195e42741ebe64933fc373400bcc375fb4f3b4aba823ac4b188b721ff6359ec5`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 43.145834 / 32.495118 | 17.400581 | 303.193286 | 36 / 36 | 0 | 0 | 1.00306 | 5 / 54 |
| ff_high_m40 | 43.451560 / 33.929474 | 15.293783 | 200.431810 | 36 / 36 | 0 | 0 | 1.02210 | 9 / 54 |
| ss_low_125 | 76.287784 / 58.054526 | 27.227975 | 154.461701 | 36 / 36 | 0 | 0 | 0.83204 | 0 / 54 |
| tt_nom_27 | 57.780618 / 44.671346 | 19.887633 | 170.594449 | 36 / 36 | 0 | 0 | 0.92808 | 0 / 54 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.59085 | 0.71785 | 0.53628 | 0.61923 |
| MINN | 0.59120 | 0.71801 | 0.53627 | 0.61929 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99756 | 0.99770 | 0.81467 | 0.90762 |
| MRDN | 1.00170 | 1.00149 | 0.81861 | 0.91156 |
| MLNP | 0.95907 | 0.98959 | 0.80194 | 0.89864 |
| MLNN | 0.95907 | 0.98959 | 0.80193 | 0.89864 |
| MLPP | 0.96484 | 0.99376 | 0.80683 | 0.90305 |
| MLPN | 0.96484 | 0.99376 | 0.80683 | 0.90305 |
| MRQP | 1.00305 | 1.02209 | 0.82917 | 0.92808 |
| MRQN | 1.00306 | 1.02210 | 0.82917 | 0.92808 |
| MOPN | 1.00305 | 1.02209 | 0.83204 | 0.92808 |
| MOPP | 0.99953 | 1.02156 | 0.83109 | 0.92763 |
| MONN | 1.00306 | 1.02210 | 0.83203 | 0.92808 |
| MONP | 0.99953 | 1.02156 | 0.83108 | 0.92763 |
| MCKN | 0.99953 | 0.99950 | 0.82179 | 0.91144 |
| MCKP | 0.99953 | 0.99950 | 0.82179 | 0.91144 |
| MBLEED | 0.99953 | 0.99950 | 0.82179 | 0.91144 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
