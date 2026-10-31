# RESET-V32: reduce local clock loading

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

**Selected private gates pass.** Complete TT noise measures `194.23325209435865` uV rms against 200 uV, with a conditional 95% profile interval of `[186.32, 202.54]` uV. The interval crosses the limit, so this point-estimate pass does not establish robust margin. Four baseline and four tighter deterministic corners, plus dedicated TT capacitance, pass their gates. Further noise convergence, hot corners and full qualification remain open; canonical V27 is unchanged.

[V31](RESET-V31.md) repairs the SS reset gate but fails dedicated TT clock-input capacitance at 16.65232415714863 fF against 16 fF. V32 changes only MCKN from 4 um/nf4 to 3 um/nf3, MCKP from 2.7 to 2.4 um/nf3, and the CKB MOM from 8 to 6 fingers. All lengths, port stimuli, Q precharge devices, input pair, 3 um tail, P8/N4 output buffers, other 21 MOS devices and other four MOMs remain V31.

Smaller CKB driver gates target external clock capacitance. Reducing the local CKB load partly offsets their lower drive strength; actual clock timing, output validity and unrounded device stress must be measured. No capacitance, timing or noise pass is assumed. Four critical deterministic corners and a dedicated TT capacitance/kickback measurement precede any noise expansion.

The initial 4-finger MOM request was rejected by the PDK constraint (minimum 6 fingers) and is retained as a failed geometry request. It was never used in a simulated source. An explicit 6-finger request passes with zero warnings, giving callback capacitance 1.46055 fF. Both MOS requests also pass without warnings and preserve complete callback geometry/terminal parasitics. All three accepted callbacks share the verified provider/release; their exact owned remote directories are absent.

| Callback | SHA-256 |
|---|---|
| N3 | `789ebd4902cc3560584cc5cbd0bfc8a94170a37d574f7b64190f41fce0d43be2` |
| P2.4 | `fbd2ae501149d9e263c33ae9c7ea35093767bb3d159beabba77b0ddf3bfb7344` |
| 6-finger MOM | `5203e49d3fdbdd21901ae4d33fe1937969ddacb2d55bce81580f8548ebb6a240` |

Electrical SHA-256: `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`. The [complete RNL source](RESET-V32.txt) was checked and rendered from a byte-identical mirror. The full local drawing is retained with the source-preparation evidence; a duplicate PNG is not added to the bounded candidate folder. Canonical V27 and all formal records remain unchanged.

Future runs use an explicit selected-signal policy retaining every required DUT SOA node and named energy/clock probes. Full noise uses the unchanged 17 x 512 sampler-only protocol. Output-policy differences are recorded separately from unchanged stimuli, numerical tolerances and measurement code.

## Completed selected-corner evidence

All four runs use frozen clean source `d283d2014a3bad62f98f98bc03603f0199c11a55`. [NUMERICS-94](NUMERICS-94.md) preserves the exact run IDs, measurements, output policy, numerical settings, all 17 noise counts and verified archive hashes. Each exact remote directory is absent. No formal record is written.

Across baseline and tighter TT, SS/low/125, SF/high/-40 and FS/high/-40, all 288 actual polarities (including 10 uV) and resets complete correctly. Output validity and every one of 69 full-trace MOS terminal pairs pass at each corner. Baseline/tighter TT 1 mV delay is 64.55221687004101/65.45016907839273 ps and 30 mV delay is 47.45520452743283/47.5529928125527 ps. SS reset is 33.47228406675874/32.868603674579965 ps. The worst unrounded stress is 0.9969054930196231 V baseline and 0.9968970199321535 V tighter, both SF/high/-40. Tighter effective reltol is 1e-6 and vabstol 1e-8 V; no explicit maxstep or method is introduced. The largest 1 mV delay change is +1.5166163652092166 ps at SS.

Dedicated TT input capacitance is 19.331118542884703 fF; clock capacitance is 15.563277108467373 fF, repairing V31's 16.65232415714863 fF failure. Net per-cycle kickback is 5.950139990093528e-05 uV. Separate instantaneous differential/common-mode peaks are 364.4625954699607 uV and 7.403170004551985 mV, both during evaluation. They are not judged against the net 40 uV limit; actual-CDAC decision-phase disturbance remains open.

Full physical TT noise retains all 17 levels and 512 finite decisions per level, 50 GHz bandwidth, seed 1 and actual low-frequency cutoff 287.216 kHz. No sample or physical stochastic source is omitted. Absolute fitted offset is 0.009772337759811343 mV. Actual baseline numerics remain conservative/gear2only/reltol 1e-4/vabstol 1e-6/relref alllocal/lteratio 10. The sampler-only trace does not establish reset history or full-trace stress; those are checked separately above. Earlier genuine failures remain failures, and overlapping fit intervals do not establish a statistically resolved improvement over V28.
