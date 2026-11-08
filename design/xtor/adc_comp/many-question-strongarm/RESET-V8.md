# RESET-V8: enable Q shunt loads only during reset

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

V7 passes full-trace stress at four key corners, but its persistent Q loads cause losing-output peaks above 30 percent of VDD. This experiment changes only the Q-load control mechanism: each N1 um shunt gate is driven by a physical inverted clock CKB, so the current should turn off during evaluation. The input-drain diode loads remain. A P2/N2 inverter generates CKB, with a 14.06 fF MOM and the previously validated weak N0.5 um / 500 nm clock load. Q precharge changes from P6 to P4 to offset the added external clock-gate load. The resulting reset speed and actual phase overlap require measurement.

This is real transistor control, with every device included in stress and energy. It adds no ideal timing source or external bias. The [independent source](RESET-V8.txt) contains 22 MOS and three MOM capacitors, all with previously validated geometries. Electrical SHA-256: `61c0cc313cf8ac00cfda7e84f0371d8d50ed76e57faef057001ccc8c380bd71a`. Full RNL on its byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Reset-gated shunt loads](https://raw.githubusercontent.com/many-question/ADC-12b-100M/596782536a7b43a5a893660a926aa339927ea784/design/xtor/adc_comp/many-question-strongarm/reset-v8.png)

The first screen checks TT, FF high cold/hot and SS low/hot, all 66 terminal pairs over the entire trace, actual decisions/output validity, delay, reset and exact AVDD energy. Clock charge is monitored separately and cannot substitute for official CMP-14. No performance pass is claimed at source freeze.

## Completed screen 20261031-034921-strongarm-reset-v8-screen

Rejected for expansion due to the remaining cold-FF Q reset peak of 1.00737 V. All four corners pass actual decisions, CMP-15 and timing; the reset-gated load therefore removes the V7 evaluation-phase failure. Only cold FF fails stress. At the Q peak, CKB is 0.506 V and the opposite Q is 0.290 V; the reset shunt is already turning on but does not yet absorb enough coupled charge. Clock and input-drain excursions now remain within the limit. The next experiment changes only the Q shunt conductance.

Actual clean source commit: `93136b26fcec4475a7370053a0a35ca089772988`. Electrical SHA-256: `61c0cc313cf8ac00cfda7e84f0371d8d50ed76e57faef057001ccc8c380bd71a`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 42.467227 / 32.188244 | 21.346133 | 823.924236 | 36 / 36 | 0 | 0 | 0.99711 | 0 / 66 |
| ff_high_m40 | 43.309078 / 35.018264 | 18.066492 | 763.395600 | 36 / 36 | 0 | 0 | 1.00737 | 10 / 66 |
| ss_low_125 | 76.801056 / 60.144856 | 32.217744 | 376.996682 | 36 / 36 | 0 | 0 | 0.82568 | 0 / 66 |
| tt_nom_27 | 58.081929 / 46.488974 | 23.377281 | 534.159162 | 36 / 36 | 0 | 0 | 0.91888 | 0 / 66 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.56849 | 0.68499 | 0.53615 | 0.59479 |
| MINN | 0.56855 | 0.68509 | 0.53614 | 0.59487 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99244 | 0.81000 | 0.90167 |
| MRDN | 0.99000 | 0.99244 | 0.81178 | 0.90167 |
| MLNP | 0.95910 | 0.98988 | 0.80200 | 0.89872 |
| MLNN | 0.95910 | 0.98988 | 0.80199 | 0.89872 |
| MLPP | 0.96469 | 0.99289 | 0.80592 | 0.90210 |
| MLPN | 0.96469 | 0.99289 | 0.80592 | 0.90210 |
| MRQP | 0.99711 | 1.00737 | 0.82568 | 0.91888 |
| MRQN | 0.99711 | 1.00737 | 0.82568 | 0.91888 |
| MOPN | 0.99711 | 1.00737 | 0.82568 | 0.91888 |
| MOPP | 0.99303 | 1.00689 | 0.82488 | 0.91828 |
| MONN | 0.99711 | 1.00737 | 0.82568 | 0.91888 |
| MONP | 0.99303 | 1.00689 | 0.82488 | 0.91828 |
| MDQP | 0.99711 | 1.00737 | 0.82568 | 0.91888 |
| MDQN | 0.99711 | 1.00737 | 0.82568 | 0.91888 |
| MDDP | 0.98582 | 0.98548 | 0.80862 | 0.89788 |
| MDDN | 0.98885 | 0.98816 | 0.81178 | 0.90082 |
| MCKN | 0.99000 | 0.99043 | 0.81001 | 0.90027 |
| MCKP | 0.99392 | 0.99911 | 0.81817 | 0.90926 |
| MBLEED | 0.99392 | 0.99911 | 0.81817 | 0.90926 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
