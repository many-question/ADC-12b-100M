# RESET-V32: reduce local clock loading

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

**V32 fails full physical noise at both tested low-hot corners:** FS/low/125 is `371.83932552901155` uV rms and SS/low/125 is `299.6542222063326` uV rms against 240 uV. Further qualification expansion stops. TT baseline/tighter point estimates pass 200 uV, but both conditional confidence intervals cross that limit. Nine unique baseline deterministic corners, four tighter repeats and dedicated TT loading pass; those results do not clear the noise failure. Canonical V27 is unchanged.

[V31](RESET-V31.md) repairs the SS reset gate but fails dedicated TT clock-input capacitance at 16.65232415714863 fF against 16 fF. V32 changes only MCKN from 4 um/nf4 to 3 um/nf3, MCKP from 2.7 to 2.4 um/nf3, and the CKB MOM from 8 to 6 fingers. All lengths, port stimuli, Q precharge devices, input pair, 3 um tail, P8/N4 output buffers, other 21 MOS devices and other four MOMs remain V31.

Smaller CKB driver gates target external clock capacitance. Reducing the local CKB load partly offsets their lower drive strength; actual clock timing, output validity and unrounded device stress must be measured. No capacitance, timing or noise pass is assumed. Four critical deterministic corners and a dedicated TT capacitance/kickback measurement precede any noise expansion.

The initial 4-finger MOM request was rejected by the PDK constraint (minimum 6 fingers) and is retained as a failed geometry request. It was never used in a simulated source. An explicit 6-finger request passes with zero warnings, giving callback capacitance 1.46055 fF. Both MOS requests also pass without warnings and preserve complete callback geometry/terminal parasitics. All three accepted callbacks share the verified provider/release; their exact owned remote directories are absent.

| Callback | SHA-256 |
|---|---|
| N3 | `789ebd4902cc3560584cc5cbd0bfc8a94170a37d574f7b64190f41fce0d43be2` |
| P2.4 | `fbd2ae501149d9e263c33ae9c7ea35093767bb3d159beabba77b0ddf3bfb7344` |
| 6-finger MOM | `5203e49d3fdbdd21901ae4d33fe1937969ddacb2d55bce81580f8548ebb6a240` |

Electrical SHA-256: `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`. The [complete RNL source](https://github.com/many-question/ADC-12b-100M/blob/eac8e8c280d5c0220b4412a1f7622b93a3148e8f/design/xtor/adc_comp/many-question-strongarm/RESET-V32.txt) was checked and rendered from a byte-identical mirror. The full local drawing is retained with the source-preparation evidence; a duplicate PNG is not added to the bounded candidate folder. Canonical V27 and all formal records remain unchanged.

Future runs use an explicit selected-signal policy retaining every required DUT SOA node and named energy/clock probes. Full noise uses the unchanged 17 x 512 sampler-only protocol. Output-policy differences are recorded separately from unchanged stimuli, numerical tolerances and measurement code.

## Completed selected-corner evidence

All four runs use frozen clean source `d283d2014a3bad62f98f98bc03603f0199c11a55`. [NUMERICS-94](NUMERICS-94.md) preserves the exact run IDs, measurements, output policy, numerical settings, all 17 noise counts and verified archive hashes. Each exact remote directory is absent. No formal record is written.

Across baseline and tighter TT, SS/low/125, SF/high/-40 and FS/high/-40, all 288 actual polarities (including 10 uV) and resets complete correctly. Output validity and every one of 69 full-trace MOS terminal pairs pass at each corner. Baseline/tighter TT 1 mV delay is 64.55221687004101/65.45016907839273 ps and 30 mV delay is 47.45520452743283/47.5529928125527 ps. SS reset is 33.47228406675874/32.868603674579965 ps. The worst unrounded stress is 0.9969054930196231 V baseline and 0.9968970199321535 V tighter, both SF/high/-40. Tighter effective reltol is 1e-6 and vabstol 1e-8 V; no explicit maxstep or method is introduced. The largest 1 mV delay change is +1.5166163652092166 ps at SS.

Dedicated TT input capacitance is 19.331118542884703 fF; clock capacitance is 15.563277108467373 fF, repairing V31's 16.65232415714863 fF failure. Net per-cycle kickback is 5.950139990093528e-05 uV. Separate instantaneous differential/common-mode peaks are 364.4625954699607 uV and 7.403170004551985 mV, both during evaluation. They are not judged against the net 40 uV limit; actual-CDAC decision-phase disturbance remains open.

Full physical TT noise retains all 17 levels and 512 finite decisions per level, 50 GHz bandwidth, seed 1 and actual low-frequency cutoff 287.216 kHz. No sample or physical stochastic source is omitted. Absolute fitted offset is 0.009772337759811343 mV. Actual baseline numerics remain conservative/gear2only/reltol 1e-4/vabstol 1e-6/relref alllocal/lteratio 10. The sampler-only trace does not establish reset history or full-trace stress; those are checked separately above. Earlier genuine failures remain failures, and overlapping fit intervals do not establish a statistically resolved improvement over V28.

## Additional deterministic and completed noise evidence

At frozen source `3b7108921859eba3a1514cb5f91f2d42c94472bd`, FS/low/125, SF/low/125, FF/low/125, FF/high/-40 and FF/high/125 all pass 180 actual decisions/reset intervals, output validity, every 69 unrounded terminal pairs per corner and AVDD KCL. This makes nine distinct baseline deterministic corners; the exact tables are in NUMERICS-94. Mixed-delay clock charge remains diagnostic; dedicated capacitance limits apply at typ only.

TT tighter noise is `196.19021968049825` uV rms, interval `[188.25, 204.52]`, absolute offset `0.010228299140700985` mV. Source and tested bench match baseline except reltol/vabstol; actual tighter values are 1e-6/1e-8 V. The fitted width changes by `1.9569675861395979` uV and 10 of 17 count bins change. Adaptive steps can alter the stochastic sequence despite the same seed; these overlapping fit intervals do not establish a statistically resolved improvement or robust margin.

FS/low/125 and SS/low/125 intervals are `[359.5, 384.82]` and `[289.43, 310.36]` uV. Each physical noise corner retains every finite sample from 17 x 512 decisions and all enabled noise sources; both fail only CMP-13. Retrieval hashes, final source guards, ZIP CRC/SHA readback and exact remote absence pass. The failed physical results remain unchanged while [artificial source diagnostics](NOISE-SOURCE-DIAGNOSTICS-V32.md) guide further circuit work.
