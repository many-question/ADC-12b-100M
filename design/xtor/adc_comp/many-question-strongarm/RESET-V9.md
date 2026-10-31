# RESET-V9: increase conductance of the reset-gated Q shunts

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

V8 recovers valid outputs and timing at all four screened corners, and only cold FF retains terminal stress. At its 1.00737 V reset peak, CKB is already 0.506 V while the opposite Q is 0.290 V. This experiment doubles only each Q shunt from N1/nf1 to N2/nf2 with the complete validated geometry and parasitics. Clock generation, Q precharge, input loads and all other electrical connections remain V8.

The stronger shunts may absorb more of the measured reset charge, but their extra clock capacitance and DC current can slow reset or alter initial conditions. Those effects must be measured on this source. The [independent source](RESET-V9.txt) has 22 MOS and three MOM capacitors. Electrical SHA-256: `0342611e100bfc38b994734e0038c985cc57cf503e55be09e18c468106f8c21c`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Stronger reset-gated Q shunts](https://raw.githubusercontent.com/many-question/ADC-12b-100M/596782536a7b43a5a893660a926aa339927ea784/design/xtor/adc_comp/many-question-strongarm/reset-v9.png)

The first screen uses TT, FF high cold/hot and SS low/hot, with all 66 terminal pairs over the entire trace, actual decisions and CMP-15, delay, reset, and exact AVDD energy. It makes no inherited performance claim.

## Completed screen 20261031-035514-strongarm-reset-v9-screen

Rejected for expansion. Increasing Q shunt conductance preserves correct decisions and CMP-15, but cold-FF stress remains at 1.00238 V and SS low/hot reset now fails at 36.251 ps. TT energy rises to 875.242 fJ/cycle. The conductance-only change therefore consumes reset and energy margin without bounding the earliest coupled peak. The next source returns to V8 N1 Q loads and targets their clock turn-on timing.

Actual clean source commit: `17c016aaaed4b24e8c9af66cc55cbd9ba0439e66`. Electrical SHA-256: `0342611e100bfc38b994734e0038c985cc57cf503e55be09e18c468106f8c21c`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 42.891655 / 32.529175 | 26.203867 | 1349.565376 | 36 / 36 | 0 | 0 | 0.99374 | 0 / 66 |
| ff_high_m40 | 43.963543 / 35.778516 | 20.860110 | 1279.725734 | 36 / 36 | 0 | 0 | 1.00238 | 10 / 66 |
| ss_low_125 | 77.974609 / 61.386951 | 36.250634 | 594.042585 | 36 / 36 | 0 | 0 | 0.82514 | 0 / 66 |
| tt_nom_27 | 58.886275 / 47.427189 | 26.363446 | 875.242369 | 36 / 36 | 0 | 0 | 0.91759 | 0 / 66 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|
| MINP | 0.56900 | 0.68995 | 0.53607 | 0.59778 |
| MINN | 0.56918 | 0.69000 | 0.53606 | 0.59781 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 0.99000 | 0.99244 | 0.81000 | 0.90166 |
| MRDN | 0.99000 | 0.99244 | 0.81160 | 0.90166 |
| MLNP | 0.95866 | 0.98987 | 0.80184 | 0.89868 |
| MLNN | 0.95866 | 0.98987 | 0.80183 | 0.89868 |
| MLPP | 0.96471 | 0.99290 | 0.80584 | 0.90210 |
| MLPN | 0.96471 | 0.99290 | 0.80584 | 0.90210 |
| MRQP | 0.99026 | 1.00211 | 0.82514 | 0.91759 |
| MRQN | 0.99026 | 1.00211 | 0.82514 | 0.91759 |
| MOPN | 0.99263 | 1.00238 | 0.82514 | 0.91759 |
| MOPP | 0.98837 | 1.00204 | 0.82411 | 0.91686 |
| MONN | 0.99263 | 1.00238 | 0.82514 | 0.91759 |
| MONP | 0.98837 | 1.00204 | 0.82411 | 0.91686 |
| MDQP | 0.99263 | 1.00238 | 0.82514 | 0.91759 |
| MDQN | 0.99263 | 1.00238 | 0.82514 | 0.91759 |
| MDDP | 0.98531 | 0.98548 | 0.80845 | 0.89786 |
| MDDN | 0.98833 | 0.98816 | 0.81160 | 0.90080 |
| MCKN | 0.99000 | 0.99080 | 0.81023 | 0.90056 |
| MCKP | 0.99374 | 0.99889 | 0.81800 | 0.90906 |
| MBLEED | 0.99374 | 0.99889 | 0.81800 | 0.90906 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
