# BUFFER-V3: cross-output discharge and clock damping

B2 passes the six key corners' decision, output-validity and timing checks but retains raw-output reset undershoot and clock-node excursions. This experiment adds an 8 um NMOS from each raw node to ground, gated by the opposite physical external output. Once one output wins, it can hold the opposite raw node low through the observed reset-coupling interval. Both clamp gates are low during initial evaluation; this differs electrically from a keeper that continuously opposes the winning node. The feedback is implemented with actual transistors and is itself subject to validity and timing checks.

Each clock node also gets an N1 um discharge device with gate at AVDD and another 2.06055 fF physical MOM capacitor in parallel with its existing damping capacitor. Their DC current and reduced swing are included in measured AVDD energy. To drive the added clamp-gate loads, the output inverter becomes P6/N3 and the first buffer pull-down becomes N2. These changes can alter threshold behavior, races and reset speed; none is assumed safe merely because B2 passed output validity.

All MOS and capacitor geometries use successful callback outputs. The new N8 geometry has zero callback warnings. The independent [BUFFER-V3.txt](BUFFER-V3.txt) contains 35 MOS and six MOM capacitors. Electrical SHA-256: `ee0e3ce105af6fc5be92e3f23d90812e854cee53296eaa3b83b9c1bac9937aca`. Full RNL checks on a byte-identical `.scs` mirror pass core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Physical cross-output discharge and clock damping](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fe173f9df274e8fa4fdddfbdb14f20208dc441fb/design/xtor/adc_comp/many-question-miyahara/buffer-v3.png)

The first screen is TT nominal 27 C, FF high/-40 C and SF low/-40 C at 0.5 ps, with all 105 terminal pairs, actual decisions/outputs, delay, reset and energy. These three cases gate further key-corner work. No ideal event capture, extra bias port or inherited validation is used. This source-freeze commit has no performance result.

## Completed screen 20261031-033024-miyahara-buffer-v3-screen

Rejected for expansion. The three corners retain correct decisions, CMP-15 and timing, but cold-FF stress remains at 1.01805 V and TT energy rises to 570.474 fJ/cycle. The raw-output minimum improves only to -17.461 mV; the cross-output feedback also creates output excursions beyond the rails. Clock bleeders consume substantial DC energy without solving all negative excursions. The next experiment targets the clocked reset and input-precharge path instead.

Actual clean source commit: `c903ea83d4b0c8cf6e3a7a70b231b274f61eaa97`. Electrical SHA-256: `ee0e3ce105af6fc5be92e3f23d90812e854cee53296eaa3b83b9c1bac9937aca`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 45.090996 / 35.984325 | 18.794891 | 792.420414 | 36 / 36 | 0 | 0 | 1.01805 | 45 / 105 |
| sf_low_m40 | 73.630125 / 57.503259 | 27.438900 | 387.814198 | 36 / 36 | 0 | 0 | 0.84650 | 0 / 105 |
| tt_nom_27 | 59.808278 / 47.209204 | 24.616542 | 570.473846 | 36 / 36 | 0 | 0 | 0.92554 | 0 / 105 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_m40 | sf_low_m40 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.73502 | 0.62585 | 0.63456 |
| MINN | 0.73614 | 0.62591 | 0.63536 |
| MTAIL | 0.99000 | 0.81000 | 0.90000 |
| MRDP | 1.00394 | 0.82573 | 0.91442 |
| MRDN | 1.00395 | 0.82573 | 0.91446 |
| M14 | 1.00466 | 0.82430 | 0.90999 |
| M15 | 1.01200 | 0.82950 | 0.91500 |
| M12 | 1.00539 | 0.82539 | 0.90932 |
| M13 | 1.01301 | 0.83015 | 0.91597 |
| M10 | 0.99621 | 0.82417 | 0.90508 |
| M11 | 0.99621 | 0.82417 | 0.90508 |
| M6 | 0.99241 | 0.81767 | 0.90182 |
| M7 | 0.99241 | 0.81767 | 0.90182 |
| M8 | 1.01176 | 0.82886 | 0.91552 |
| M9 | 1.01805 | 0.83259 | 0.92067 |
| MCKN | 0.99108 | 0.81100 | 0.90066 |
| MCKP | 1.00188 | 0.82471 | 0.91265 |
| MCK2N | 0.96147 | 0.79913 | 0.87430 |
| MCK2P | 1.00188 | 0.82471 | 0.91265 |
| MRQP | 1.00137 | 0.82449 | 0.91160 |
| MRQN | 1.00137 | 0.82449 | 0.91160 |
| MAP | 0.99248 | 0.81262 | 0.90288 |
| MAN | 0.99379 | 0.81399 | 0.90440 |
| MBPP | 1.00757 | 0.82550 | 0.91707 |
| MBPN | 1.00757 | 0.82550 | 0.91707 |
| MOPP | 1.00527 | 0.82787 | 0.91461 |
| MOPN | 1.00801 | 0.84152 | 0.92010 |
| MBNP | 1.00757 | 0.82550 | 0.91707 |
| MBNN | 1.00757 | 0.82550 | 0.91707 |
| MONP | 1.00527 | 0.82787 | 0.91461 |
| MONN | 1.00801 | 0.84152 | 0.92010 |
| MCLP | 1.01662 | 0.84650 | 0.92554 |
| MCLN | 1.01662 | 0.84649 | 0.92554 |
| MBLCB | 1.00188 | 0.82471 | 0.91265 |
| MBLCR | 1.00085 | 0.82332 | 0.91122 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
