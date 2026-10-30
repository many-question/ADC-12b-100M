# Energy cost of the physical repairs

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
