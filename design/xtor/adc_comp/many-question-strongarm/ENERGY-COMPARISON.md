# Energy cost of the physical repairs

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

This compares the complete implemented candidates at TT, 0.9 V, 27 C, VCM=0.49 V, identical 10 fF output loads and the same 36-decision mixed +/-100 mV through +/-10 uV sequence. AVDD charge is integrated from 100 ps to 14.5 ns and divided by 36. All local clock, output, damping and rail-offset circuitry is inside the AVDD boundary; the external ideal clock source is outside it. Energy is reported-only, without an acceptance threshold.

| Implemented candidate | Canonical baseline (fJ/cycle) | Compared experiment (fJ/cycle) | Increase |
|---|---:|---:|---:|
| StrongARM V11 | 188.590270 | 571.537169 | 203.06% |
| Miyahara B8 | 187.647444 | 464.617369 | 147.60% |

The standard baseline records use the original moderate numerical settings; the new screens use maxstep=0.5 ps, traponly, reltol=1e-6 and vabstol=1e-8. The stimulus, integration window and supply boundary match, but numerical settings differ, so the entire difference cannot be assigned exactly to the circuit change. An existing fully matched fine-step StrongARM baseline gives **190.686419 fJ/cycle**, making V11 **199.73% higher** even with the same numerical settings. The older fixed +/-1 mV measurements use a different stimulus and are not mixed into this table.

For these two complete implementations, Miyahara B8 uses 18.71% less AVDD energy than StrongARM V11 under the same fine settings. Both fail a key-corner requirement; this is not a comparison of qualified designs or of the bare topologies. StrongARM includes reset-gated Q shunts that conduct throughout reset, while Miyahara includes weak PMOS rail-offset loads and output diode loads. Their different repair circuitry is part of the measured cost.

A controlled Miyahara comparison isolates a useful portion of that cost: B6, before the added rail-offset loads, used 241.043727 fJ/cycle; B7 used 668.924396 fJ/cycle; halving only the six PMOS pull-up pairs in B8 reduced energy by 204.307027 fJ/cycle to 464.617369. These are matched fine-step runs with the same AVDD meter. They demonstrate the cost of the added physical loads and their interactions, not a transistor-by-transistor power allocation.

The stored V11/B8 transient signals contain VCK:p but no AVDD-current or per-device-current waveform. The existing power.txt stores only the full-window integral. Consequently, reset/evaluation energy and individual contention-current contributions cannot be recovered reliably from these completed runs. Voltage traces establish conducting paths, but do not quantify their currents. No separate rerun is launched merely to fill this gap: the next necessary repair screens save total AVDD current and explicit MOS terminal currents, and will report phase integrals plus branch-current evidence. Historical total-energy measurements remain unchanged.

## Measured phase and supply-branch energy: V12 and B9

The necessary six-corner repair simulations saved AVDD source current and every MOS terminal tied to AVDD, plus selected NMOS shunt currents. No requested probe is missing. At TT the independent waveform integral agrees with the existing AVDD meter within 0.00012%; summed AVDD-terminal charge accounts for the entire measured supply charge. The values below are net delivered AVDD energy, including charge returned to the supply; they are not individual transistor heat dissipation.

Evaluation is the interval between each CLKC 50% rising and falling crossing. Reset is its complement within the unchanged 100 ps–14.5 ns meter window, including the initial 5 ps fragment. All 36 cycles contribute.

| TT implemented source | AVDD total (fJ/cycle) | Evaluation | Reset | Late evaluation current (uA) | Late reset current (uA) |
|---|---:|---:|---:|---:|---:|
| StrongARM V12 | 574.029291 | 103.518452 | 470.510840 | 173.892 | 2087.527 |
| Miyahara B9 | 455.719625 | 173.719701 | 281.999924 | 613.796 | 785.838 |

Late evaluation averages CLKC falling-edge minus 60 to minus 10 ps; late reset averages falling-edge plus 100 to plus 190 ps. These specified windows expose persistent current after the transition rather than attributing the whole reset energy to a switching event.

| AVDD-connected terminal group, TT | StrongARM V12 (fJ/cycle) | Miyahara B9 (fJ/cycle) |
|---|---:|---:|
| Q precharge/reset | 340.102472 | 0.000000 |
| external output inverters | 38.250216 | 29.171607 |
| first output buffer | 0.000000 | 19.167951 |
| input precharge | 107.262671 | 121.890543 |
| physical clock | 55.378476 | 18.713344 |
| regenerative core | 33.035457 | 54.003994 |
| weak PMOS rail loads | 0.000000 | 212.772185 |

StrongARM spends **81.97%** of its net supply energy during reset. The two Q-precharge PMOS paths deliver **340.102472 fJ/cycle**, almost entirely during reset. Each Q-shunt NMOS carries about **935.912 uA** in the late-reset window; its precharge PMOS is simultaneously enabled. This directly confirms a substantial persistent reset contention path. Input-drain diode loads each carry about **61.47 uA** late in reset. The weak physical clock-floor PMOS draws about **160.28 uA** late in evaluation and receives **30.432772 fJ/cycle** through its supply terminals.

Miyahara's six weak PMOS rail loads receive **212.772185 fJ/cycle**, **46.69%** of its TT AVDD total: **98.390611 fJ** during evaluation and **114.381574 fJ** during reset. The buffers and diode loads change the rest of the circuit's currents as well; subtracting this branch allocation does not recreate an unloaded topology. Both implementations have significant persistent current and must not be described as zero-static-current versions of their original cores.

These sources still fail key-corner requirements: V12 reaches 1.00002 V at SF high/27 and has 35.861626 ps SS reset; B9 has 36.120741 ps SS reset. Their power results are measured implementation tradeoffs, not a qualified topology winner. The source, all six corner phase tables and individual saved-current records are retained with the raw evidence.

## Six-key-corner passing sources V13 and B10

These complete implementations pass the initial six key corners; further corner and convergence checks remain in progress. The output NMOS changes retain the same energy boundary and saved-current protocol.

| TT source | Meter energy (fJ/cycle) | Waveform evaluation (fJ/cycle) | Waveform reset (fJ/cycle) | Initial CLKC-low operating-point AVDD current (uA) | Initial reset power (mW) |
|---|---:|---:|---:|---:|---:|
| StrongARM V13 | 577.098910 | 105.670475 | 471.429129 | 2072.416 | 1.865174 |
| Miyahara B10 | 457.451059 | 174.578897 | 282.872453 | 770.966 | 0.693869 |

The initial current is the simulator's saved DC operating-point current with CLKC low, before the first edge, at the specified initial inputs. It is not an extrapolated ADC power estimate. Persistent reset consumption matters when the surrounding SAR holds the comparator in reset for longer than the characterization duty cycle. A complete converter energy estimate would need its actual active/reset timing. Both sources remain provisional; the lower B10 AVDD number is a comparison of these implemented circuits, not a qualified or topology-only efficiency conclusion.

## V14 measured TT supply phases

All ten measured key corners pass screening, with targeted voltage convergence and formal qualification still pending. The same TT stimulus, 100 ps–14.5 ns meter and complete AVDD boundary give the following saved-current integrals.

| Total (fJ/cycle) | Evaluation | Reset | Initial reset current (uA) | Initial reset power (mW) | Late reset current (uA) |
|---:|---:|---:|---:|---:|---:|
| 580.512581 | 106.486586 | 474.025995 | 2077.522376 | 1.869770139 | 2092.666284 |

The original meter is 580.511994 fJ/cycle; waveform integration differs by 0.00010101%. All probes are present and the AVDD terminal-sum residual is numerical zero. Against the matched fine-step canonical control (190.686419 fJ), this complete implementation uses about 204.43% more AVDD energy. The existing persistent Q-reset contention remains. No power limit or bare-topology efficiency conclusion is introduced.


## V18 measured TT supply phases

The exact same 100 ps–14.5 ns, 36-cycle full-AVDD boundary gives:

| Total (fJ/cycle) | Evaluation | Reset | Initial reset current (uA) | Initial reset power (mW) |
|---:|---:|---:|---:|---:|
| 405.326281445 | 89.061121796 | 316.265159648 | 1175.655018883 | 1.058089517 |

The original meter is 405.325820880 fJ/cycle. All probes are present; the terminal-sum residual is numerical zero. The mixed-sequence clock diagnostic is 16.037833 fF and formal noise remains unmeasured for V18. This is a partial-screen implementation measurement, not a qualified power ranking. Persistent reset current remains substantial.

| Net supply delivery group | Whole cycle (fJ) | Evaluation (fJ) | Reset (fJ) |
|---|---:|---:|---:|
| input precharge | 106.585001964 | 1.705606176 | 104.879395788 |
| regenerative core | 24.856916691 | 28.664393293 | -3.807476602 |
| Q precharge/reset | 196.545479108 | 1.292470254 | 195.253008854 |
| external output inverters | 28.037938141 | 26.478225661 | 1.559712480 |
| physical clock | 49.300945541 | 30.920426412 | 18.380519129 |

These are net supply-delivery allocations, including returned charge and circuit interactions, not isolated device heat. Power is reported only.
## V19 complete-circuit TT energy

The unchanged mixed sequence and 100 ps to 14.5 ns boundary give 404.753683 fJ/cycle from the complete AVDD trace, partitioned into 88.903251 fJ evaluation and 315.850433 fJ reset. The original meter gives 404.753296 fJ; relative integration difference is 0.000096%. All AVDD terminal probes are present and the supply allocation residual is zero. Initial reset current is 1174.561664 uA (1.057105 mW); late reset current is 1189.646551 uA. These physical reset costs are included. The result is reported-only, not a qualified efficiency ranking. It comes from clean source `0b026e2487d815e377ff0de99e28ad3a38a039ab`, run `20261031-074310-strongarm-reset-v19-screen`.



## V20 measured TT supply phases

Run `20261031-084834-strongarm-reset-v20-screen` measures V20 with the same full-circuit AVDD boundary and the same 36-cycle 100 ps–14.5 ns window. Only the two Q-node capacitor geometries differ from V19.

| Total (fJ/cycle) | Evaluation | Reset | Initial reset current (uA) | Initial reset power (mW) |
|---:|---:|---:|---:|---:|
| 406.390975180 | 89.714530132 | 316.676445047 | 1174.561664158 | 1.057105498 |

The original meter gives 406.390516200 fJ/cycle; the waveform integral differs by 0.000112941%. All probes are present and their AVDD terminal sum closes to numerical precision. The net change from V19 is +1.637291916 fJ/cycle (+0.404516%).

| Net supply delivery group | Whole cycle (fJ) | Evaluation (fJ) | Reset (fJ) |
|---|---:|---:|---:|
| input precharge | 106.838943822 | 1.705417883 | 105.133525939 |
| regenerative core | 25.321462752 | 29.177433952 | -3.855971200 |
| Q precharge/reset | 196.799370107 | 1.291695008 | 195.507675099 |
| external output inverters | 28.322515582 | 26.726318500 | 1.596197083 |
| physical clock | 49.108682916 | 30.813664789 | 18.295018127 |

Physical reset and weak-load costs are included. Net returned charge can make an individual phase allocation negative; these allocations are not isolated device dissipation. Power is reported only. No noise or qualification benefit is established by this cost comparison.


## V25 measured TT supply phases

Run `20261031-100951-strongarm-reset-v25-screen` uses the same complete AVDD boundary and 36-cycle 100 ps–14.5 ns window as V20. This source has larger N16 coupling devices and stronger 0.6 um Q reset pull-downs; a comparison to V20 does not isolate the two changes.

| Total fJ/cycle | Evaluation | Reset | Initial reset current uA | Initial reset power mW |
|---:|---:|---:|---:|---:|
| 447.255148884 | 96.948720675 | 350.306428209 | 1358.730461855 | 1.222857416 |

The complete waveform integral changes by +40.864173704 fJ/cycle (+10.055384%) from V20. The original meter is 447.254687160 fJ/cycle; its relative difference from the waveform integral is 0.000103235%. All supply-terminal probes are present and their sum closes to numerical precision.

| Net supply delivery group | Whole cycle fJ | Evaluation | Reset |
|---|---:|---:|---:|
| input precharge | 109.561904335 | 1.703289352 | 107.858614983 |
| regenerative core | 30.336388990 | 34.176880110 | -3.840491120 |
| Q precharge/reset | 227.189420805 | 1.291818318 | 225.897602487 |
| external output inverters | 30.980316448 | 28.964836881 | 2.015479567 |
| physical clock | 49.187118306 | 30.811896014 | 18.375222292 |

Physical weak loads and reset are included. Net returned charge can make a phase allocation negative; these are supply-delivery allocations rather than isolated device dissipation. Ideal external-clock delivery is outside this boundary. Power is reported only and does not establish a qualified topology ranking.


## V26 measured TT supply phases

Run `20261031-103621-strongarm-reset-v26-screen` uses the same complete AVDD boundary and 36-cycle 100 ps–14.5 ns window as V20. The only geometry change relative to V20 is smaller N8 input-to-Q coupling devices. Capacitance, drive, transient bias and noise effects remain coupled.

| Total fJ/cycle | Evaluation | Reset | Initial reset current uA | Initial reset power mW |
|---:|---:|---:|---:|---:|
| 398.516712298 | 83.862647693 | 314.654064605 | 1174.561976866 | 1.057105779 |

The complete waveform integral changes by -7.874262881 fJ/cycle (-1.937608%) from V20. The original meter is 398.516283000 fJ/cycle; its relative difference from the waveform integral is 0.000107724%. All supply-terminal probes are present and their sum closes to numerical precision.

| Net supply delivery group | Whole cycle fJ | Evaluation | Reset |
|---|---:|---:|---:|
| input precharge | 104.894718352 | 1.707883394 | 103.186834958 |
| regenerative core | 21.568086279 | 24.787404929 | -3.219318650 |
| Q precharge/reset | 196.208573149 | 1.292769894 | 194.915803255 |
| external output inverters | 26.736479066 | 25.260963073 | 1.475515993 |
| physical clock | 49.108855452 | 30.813626403 | 18.295229049 |

Physical weak loads and reset are included. Net returned charge can make a phase allocation negative; these are supply-delivery allocations rather than isolated device dissipation. Ideal external-clock delivery is outside this boundary. Power is reported only and does not establish a qualified topology ranking.


## V27 measured TT supply phases

Only CQP/CQN increase from 5.66049 to 12.8604 fF relative to V26. The complete 36-cycle 100 ps–14.5 ns AVDD integral is 408.902291928 fJ/cycle: 89.282426247 evaluation and 319.619865681 reset. Initial reset current is 1174.561976866 uA. Total energy changes by +10.385579630 fJ/cycle from V26. The original meter gives 408.901925160 fJ/cycle; relative waveform-integral difference is 0.000089696%. All supply probes are present and KCL closes.

| Net supply-delivery group | Whole cycle fJ | Evaluation | Reset |
|---|---:|---:|---:|
| input precharge | 106.422759938 | 1.704425791 | 104.718334146 |
| regenerative core | 25.194418280 | 28.227213944 | -3.032795665 |
| Q precharge/reset | 199.222046975 | 1.287885104 | 197.934161870 |
| external output inverters | 28.954666276 | 27.249213809 | 1.705452466 |
| physical clock | 49.108400461 | 30.813687598 | 18.294712863 |

Physical weak loads and reset are included; external ideal-clock delivery is outside the AVDD boundary. Net returned charge can make an allocation negative, so these are not isolated device-dissipation values. Power is reported only, and noise qualification remains unresolved.
