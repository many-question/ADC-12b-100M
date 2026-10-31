# BUFFER-V1: physical output-validity experiment

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

The baseline's raw outputs rise together before regeneration, with losing peaks above 50% VDD in the failing SF waveform. This experiment renames those nodes RP/RN and inserts two actual CMOS inverters per output. The first inverter uses P6 um / N0.5 um at 30 nm to move its switching region above the raw common-mode excursion; the second uses P4 um / N2 um to drive the unchanged 10 fF external load. The original core, reset and clock devices retain their geometries and connections apart from the output-node renaming.

This is a transistor-level threshold-restoration hypothesis, not a verified gate threshold. The smaller first-stage NMOS may add delay; the changed core loading may alter regeneration, noise and reset feedthrough. Every internal terminal and actual external output is included in the screen. No ideal event latch, decision detector or behavioral masking is added.

The independent [BUFFER-V1.txt](BUFFER-V1.txt) has 31 MOS and four MOM capacitors. Its electrical SHA-256 is `f7279257a3306d1219214e389fb1ae40106fb03253641590e4f4d9196327511f`. The new 0.5 um / nf1 NMOS geometry was solved by a successful, warning-free callback. Existing buffer geometries reuse successful callback results without hand scaling. Full RNL passes core 0.5.2 with 0 errors, 0 warnings and 0 hints on a byte-identical `.scs` mirror.

![Physical output buffers](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fe173f9df274e8fa4fdddfbdb14f20208dc441fb/design/xtor/adc_comp/many-question-miyahara/buffer-v1.png)

The first screen is planned for TT nominal 27 C, FF high -40 C, FF high 125 C, SS low 125 C, SF low -40 C and SF high 27 C. It uses the current v0.7.0 delay stimulus and meter with maxstep 0.5 ps, traponly, reltol 1e-6 and vabstol 1e-8. The two SF cases target the observed simultaneous-rise and losing-peak failures. Physical validity, full-trace |Vgs|/|Vgd|/|Vds|, delay, reset and energy gate any expansion. No validation is claimed in this source-freeze commit.

Canonical `adc_comp.scs` and its official baseline results are preserved. Failed screens stop expansion of this version while subsequent evidence-based iterations continue.

## Completed six-corner screen

Actual source commit: `53cad4a`. All six jobs completed successfully. CMP-15 is 0/216 cycles and every cycle decides with correct first-event polarity. The external losing peak remains below 0.564% VDD, including both targeted SF corners. The new physical interface fixes the screened overlap behavior, but this version fails TT 30 mV delay and high-voltage device stress.

| Corner | 1 mV delay ps | 30 mV delay ps | Reset ps | AVDD fJ | Losing peak % VDD | Maximum terminal V | Failed pairs / 93 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 63.289752 | 52.984285 | 22.385679 | 203.560623 | 0.055678 | 0.922060 | 0 |
| ff_high_m40 | 48.061515 | 40.450315 | 17.102326 | 239.290879 | 0.051326 | 1.017480 | 50 |
| ff_high_125 | 55.493384 | 44.981727 | 17.724726 | 416.912099 | 0.563232 | 1.007590 | 10 |
| ss_low_125 | 86.534771 | 71.592997 | 29.336216 | 187.304946 | 0.108200 | 0.833300 | 0 |
| sf_low_m40 | 77.781390 | 64.221178 | 25.605163 | 146.698718 | 0.075269 | 0.847310 | 0 |
| sf_high_27 | 60.424096 | 50.868284 | 20.624037 | 258.020344 | 0.091665 | 1.019410 | 44 |

Cold FF has raw RP/RN reset undershoot to -0.027481 V; at the RP minimum (716.620240 ps), CKB is 0.987748 V, RP is -0.027481 V and BP is 0.989615 V. This overstresses the first buffer PMOS gate-source pair. Other failures occur in the two clock stages, input-drain controlled devices and buffer switching nodes. They are checked independently; fixing the external output rule does not qualify internal voltage stress. The slow first-stage pull-down also motivates a faster threshold stage, subject to preserving the SF losing-peak margin.

Full-scope terminal maxima across the six traces:

| Device | Max Vgs V | Max Vgd V | Max Vds V |
|---|---:|---:|---:|
| MINP | 0.54235 | 0.56144 | 0.75523 |
| MINN | 0.54235 | 0.56979 | 0.75556 |
| MTAIL | 0.99000 | 0.98991 | 0.63351 |
| MRDP | 1.00516 | 1.00781 | 0.99194 |
| MRDN | 1.00516 | 1.00780 | 0.99194 |
| M14 | 0.99194 | 1.00073 | 1.00170 |
| M15 | 0.99194 | 1.00878 | 1.00065 |
| M12 | 1.00144 | 1.00073 | 0.99276 |
| M13 | 1.00979 | 1.00878 | 0.99276 |
| M10 | 0.99229 | 0.99360 | 0.99897 |
| M11 | 0.99229 | 0.99360 | 0.99897 |
| M6 | 0.99410 | 0.99360 | 0.99410 |
| M7 | 0.99410 | 0.99360 | 0.99410 |
| M8 | 1.00144 | 1.00766 | 0.99410 |
| M9 | 1.00979 | 1.01511 | 0.99410 |
| MCKN | 0.99000 | 0.99022 | 1.00277 |
| MCKP | 0.99000 | 0.99022 | 1.00487 |
| MCK2N | 1.00277 | 1.00448 | 1.01083 |
| MCK2P | 1.00487 | 1.00448 | 1.00516 |
| MRQP | 1.00277 | 1.01692 | 0.99410 |
| MRQN | 1.00277 | 1.01692 | 0.99410 |
| MAP | 0.99000 | 0.99282 | 0.99194 |
| MAN | 0.99000 | 0.99441 | 0.99194 |
| MBPP | 1.01941 | 1.01915 | 1.01209 |
| MBPN | 0.99410 | 1.01915 | 1.00316 |
| MOPP | 1.01209 | 1.01141 | 1.00013 |
| MOPN | 1.00316 | 1.01141 | 1.00637 |
| MBNP | 1.01941 | 1.01915 | 1.01209 |
| MBNN | 0.99410 | 1.01915 | 1.00316 |
| MONP | 1.01209 | 1.01141 | 1.00013 |
| MONN | 1.00316 | 1.01141 | 1.00637 |

Actual peak simultaneous jobs: 5. Commands used +aps, no ++aps or explicit +mt; every log disabled solver multithreading. All raw/deck evidence was retrieved and SHA-256 checked before exact-owned remote cleanup. This version is not expanded to all corners, noise or MC. Canonical baseline records remain byte-identical and retain their own source provenance.
