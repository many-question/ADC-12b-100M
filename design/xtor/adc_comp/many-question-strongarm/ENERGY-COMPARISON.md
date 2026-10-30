# Energy cost of the physical repairs

This compares the complete implemented candidates at TT, 0.9 V, 27 C, VCM=0.49 V, identical 10 fF output loads and the same 36-decision mixed +/-100 mV through +/-10 uV sequence. AVDD charge is integrated from 100 ps to 14.5 ns and divided by 36. All local clock, output, damping and rail-offset circuitry is inside the AVDD boundary; the external ideal clock source is outside it. Energy is reported-only, without an acceptance threshold.

| Implemented candidate | Canonical baseline (fJ/cycle) | Current experiment (fJ/cycle) | Increase |
|---|---:|---:|---:|
| StrongARM V11 | 188.590270 | 571.537169 | 203.06% |
| Miyahara B8 | 187.647444 | 464.617369 | 147.60% |

The standard baseline records use the original moderate numerical settings; the new screens use maxstep=0.5 ps, traponly, reltol=1e-6 and vabstol=1e-8. The stimulus, integration window and supply boundary match, but numerical settings differ, so the entire difference cannot be assigned exactly to the circuit change. An existing fully matched fine-step StrongARM baseline gives **190.686419 fJ/cycle**, making V11 **199.73% higher** even with the same numerical settings. The older fixed +/-1 mV measurements use a different stimulus and are not mixed into this table.

For the current complete implementations, Miyahara B8 uses 18.71% less AVDD energy than StrongARM V11 under the same fine settings. Both fail a key-corner requirement; this is not a comparison of qualified designs or of the bare topologies. StrongARM includes reset-gated Q shunts that conduct throughout reset, while Miyahara includes weak PMOS rail-offset loads and output diode loads. Their different repair circuitry is part of the measured cost.

A controlled Miyahara comparison isolates a useful portion of that cost: B6, before the added rail-offset loads, used 241.043727 fJ/cycle; B7 used 668.924396 fJ/cycle; halving only the six PMOS pull-up pairs in B8 reduced energy by 204.307027 fJ/cycle to 464.617369. These are matched fine-step runs with the same AVDD meter. They demonstrate the cost of the added physical loads and their interactions, not a transistor-by-transistor power allocation.

The stored V11/B8 transient signals contain VCK:p but no AVDD-current or per-device-current waveform. The existing power.txt stores only the full-window integral. Consequently, reset/evaluation energy and individual contention-current contributions cannot be recovered reliably from these completed runs. Voltage traces establish conducting paths, but do not quantify their currents. No separate rerun is launched merely to fill this gap: the next necessary repair screens save total AVDD current and explicit MOS terminal currents, and will report phase integrals plus branch-current evidence. Historical total-energy measurements remain unchanged.
