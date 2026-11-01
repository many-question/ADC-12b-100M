# Historical comparator noise and delay audit

This read-only audit supports [issue 124](https://github.com/many-question/ADC-12b-100M/issues/124). Noise and delay take priority; conflicting auxiliary requirements need a top-level decision. No specification is changed, no source is promoted, and no new simulation is authorized by this report. The already dispatched A6 FS physical-noise job has now finished and been archived; no further job follows. TT noise, additional corners, mismatch, diagnostics and new variants remain paused.

The completed evidence below contains **no full 45-corner physical-noise pass and no demonstrated full-physical FS/low/125 result at or below 240 uV**. A TT pass cannot establish either. Historical raw retention varies; pinned reports and records are evidence of completed measurements, not a promise that every old waveform remains available. [A6 has now completed at 325.0388413768936 uV with a model-fit warning and an official FAIL](A6-NOISE.md); it does not change that conclusion.

## Full physical TT noise evidence

All rows in this table use 17 levels x 512 decisions, seed 1 and 50 GHz maximum device-noise frequency, with no noise-source masks. Intervals are model-conditional 95% profile intervals; a point-estimate pass with an interval crossing 200 uV is not robust margin. Private measurements of the full official protocol are distinguished from canonical result records.

| Exact electrical source | TT noise, uV rms | 95% interval, uV | Numerical regime / record | Same-source non-TT noise evidence |
|---|---:|---|---|---|
| Original StrongARM p56 | 187.10820152492354 | 179.33–195.28 | Old moderate/traponly, reltol 1e-3; formal | No FS or full-45 noise proof |
| Original Miyahara x56 | 193.75846454733392 | 185.84–202.07 | Old moderate/traponly, reltol 1e-3; formal | No FS or full-45 noise proof |
| Restored StrongARM V2 | 184.174455388682 | 176.42559432971512–192.3212211902768 | Current conservative/gear2only, reltol 1e-4; private full protocol | FS 317.00025134117095, CI 306.34969032134103–328.16576805722093; FAIL |
| StrongARM V32 | 194.23325209435865 | 186.32–202.54 | Current conservative/gear2only, reltol 1e-4; private full protocol | FS 371.83932552901155; SS 299.6542222063326; both FAIL |
| V32, same source tighter | 196.19021968049825 | 188.25–204.52 | Conservative/gear2only, reltol 1e-6, vabstol 1e-8; private | Same source as preceding row |
| Miyahara B13 | 198.728193916 | 190.74–207.11 | Old moderate/traponly, reltol 1e-3; formal | FS 488.025277828; SS 294.826930752; FF 302.386218452; SF 259.281840989; all FAIL |
| Miyahara B20 | 191.15943735314053 | 183.31–199.41 | Old moderate/traponly, reltol 1e-3; formal | See current-regime measurement below |
| B20, same electrical source | 191.43800312001045 | 183.58–199.69 | Current conservative/gear2only, reltol 1e-4; private full protocol | FS 343.4944014285115, CI 332.03–355.53; FAIL |

Baseline vabstol is 1e-6 V. Current full-noise runs use alllocal, lteratio 10, stop 3.4817 us and implicit noisefmin 287.216 kHz. Old moderate runs used lteratio 3.5; they are not current-numerics qualification. Effective maximum step is a ceiling, not the actual adaptive step. Seed reuse does not imply the same stochastic trajectory when adaptive stepping changes.

Early **l16t3c1 = 144.5726273534707 uV**, CI 126.30252277862628–166.00976135822572, is only a **17 x 64 TT pilot under old numerics**. No full 17 x 512 TT result was found for l16. Its unchanged source, restored under current rules, gives full FS noise **274.20498833482293 uV**, CI **264.5703918658524–284.28656376278826**, failing 240 uV. The reset-gate-only l16 split trial gives 276.50080267196466 uV with overlapping CI. These are not evidence of an auxiliary repair destroying a 144 uV full-corner design.

Miyahara B26 has full FS noise **270.61635250554104 uV**, CI **261.07–280.60**, also failing 240 uV; its TT full noise is unmeasured. Artificial noise-off results and short fixed-input diagnostics are excluded from this pass table. V27 current full TT 210.1008609253812 uV and V28 206.44956249285457 uV are failures, even where noise-off experiments pass.

## Delay, interface and auxiliary constraints

| Source | TT d30 / d1, ps | TT energy, fJ/cycle | Completed relevant evidence and actual blocker |
|---|---|---:|---|
| p56 | 44.92117435144679 / 56.936992094856556 | 188.590269708 | All 45 timing cases pass; maximum d1 96.11781935273085 ps. CMP15 0/1620. Reset fails four SS cases; worst 39.88879537614763 ps versus 35 ps. |
| x56 | 38.75484849515665 / 47.51293291433307 | 187.647444288 | All 45 timing/reset cases pass; maximum d1 76.79340994330079 ps. CMP15 fails 1084/1620 cycles in all 45 corners; 108 cycles have both outputs crossing 50%; worst loser 52.820335321404684% VDD. |
| Restored V2 | 44.169527137588915 / 56.473600243332776 | 149.865117912 | Five representative corners pass timing/reset/CMP15/1.1 V stress. TT reset 19.03776955021709 ps. Full FS noise is the demonstrated blocker. |
| Restored l16 | 47.71403968897317 / 61.56277345045652 | 203.492731932 | Five representative corners pass timing/reset/CMP15/1.1 V stress; SF peak 1.09394 V leaves only 6.06 mV baseline margin. Full FS noise fails; full TT noise unknown. |
| V32 | 47.45520452743283 / 64.55221687004101 | Not ranked here | Nine unique baseline corners plus four tighter repeats pass; SS reset 33.47228406675874 ps. Full FS/SS noise fails. |

TT Cin / CLKC capacitance, fF, respectively: p56 **19.312815724429136 / 15.156427300314368**; x56 **19.310269245339665 / 14.924420279883684**; V2 **19.313134034315315 / 15.223158372781954**; l16 **19.311701639827493 / 7.256641126623195**; V32 **19.331118542884703 / 15.563277108467373**. All these measured TT loading values pass the 20 / 16 fF limits. Their specified net per-cycle differential kickback values also pass 40 uV. Near-zero net kickback is not a measurement of instantaneous disturbance on the actual SAR CDAC.

p56's four failing resets are SS/low/125 39.88879537614763 ps, SS/low/27 38.85402330265327 ps, SS/low/-40 37.07116300818039 ps and SS/nom/125 35.644217449105554 ps. It is a concrete reset-budget negotiation candidate. x56 needs an actual SAR receiver/validity decision; correct differential polarity does not waive dual-high or loser-level violations.

The old 1.0 V stress gate rejected fine-screen peaks around 1.0538 V for p56, 1.016 V for x56 and 1.04856 V for early V2. Those particular peaks are below today's 1.1 V project limit, but that observation is not a full 45-corner SOA certificate. Restored V2 measured a five-corner maximum of 1.04869 V. It is inappropriate to retain the old 1.0 V rejection as its current blocker.

## What the repair history does and does not show

The strongest controlled penalty is energy. Under matched fine-step settings, the complete p56 implementation uses **190.686419 fJ/cycle**, versus **571.537169 fJ/cycle** for V11, a 199.73% increase. V12 measured 574.029291 fJ/cycle, with **81.97% during reset**, about **2.087527 mA late-reset current**, and 340.102472 fJ supplied through Q precharge paths. Simultaneously enabled Q shunts and precharge devices establish persistent contention. V14 remains at 580.511994 fJ/cycle and its old full TT noise is 2094.115400 uV, versus p56's 187.108201525 uV. This is a genuine multi-revision degradation, but does not isolate a single auxiliary requirement or device as the entire noise cause.

The Miyahara controlled sequence is B6 **241.043727** to B7 **668.924396 fJ/cycle** after adding rail-offset loads; halving six PMOS pull-up pairs in B8 reduces energy to **464.617369**. B9 branch currents attribute 212.772185 fJ/cycle, 46.69% of total AVDD delivery, to weak rail loads, with persistent reset/evaluate current. These are whole-implementation tradeoffs, not a qualified bare-topology efficiency ranking. Energy is reported-only; no new power acceptance limit is imposed.

x56's 193.758 uV, B12's 201.880 uV and B13's 198.728 uV TT intervals overlap; the history does **not** establish monotonic noise harm. B13 TT versus B13 FS is a corner comparison, as are V2 TT versus FS and V32 TT versus FS. B13 FS versus B20 FS also changes numerical regime and cannot cleanly isolate the circuit revision. B20/B22/B26 current-regime FS results improve from 343.494 to 342.512 to 270.616 uV, contrary to a blanket claim that every repair worsens noise.

V31-to-V32 repairs CLKC capacitance from 16.65232415714863 to 15.563277108467373 fF by changing only clock-driver widths and the CKB MOM. There is no paired full V31 noise result, so noise damage from this repair is unproved. V32-to-V33 does worsen same-corner, same-protocol FS noise from 371.839 to 483.261 uV after reducing regeneration NMOS size; that was a noise hypothesis, not an isolated auxiliary-gate repair.

## Candidates for top-level tradeoff

These are useful tradeoff candidates rather than a statistically established global Pareto front: noise intervals overlap, numerical regimes differ, and corner coverage is unequal.

- **x56:** fastest demonstrated TT/45-corner timing with a TT full-noise point pass. Negotiate the receiver/CMP15 interface explicitly; FS noise and current-numerics confirmation are missing.
- **p56:** strong historical TT noise and timing, no CMP15 failures in the 45-corner audit. Negotiate the measured SS reset extension; FS noise and current-numerics confirmation are missing.
- **Restored V2:** strongest current-regime TT noise/energy tradeoff among these fully measured TT sources, with representative deterministic gates passing. Its real FS 317 uV failure needs a top-level noise-budget or architecture decision.
- **l16 and B26:** useful lower-FS-noise comparison points at 274.205 / 270.616 uV, still above 240 uV; neither has a full TT-noise pass for that exact restored source. l16 also has limited SF stress margin.
- **V32:** a well-audited counterexample to equating auxiliary-gate success with noise qualification. Its TT point pass is narrow and its FS/SS failures are substantial.

No future job is implied. The top-level decision should set the allowable reset window, SAR output acceptance, and corner noise budget before more local repair work.

## Fixed public provenance and exact source identities

The source hashes below refer to exact LF source bytes; the electrical hash removes non-electrical drawing/comment differences. Historical canonical p56/x56 source hashes differ from earlier private variant files even when their electrical hashes match.

| Source | Fixed source commit | Source SHA-256 | Electrical SHA-256 |
|---|---|---|---|
| p56 canonical | `5089a93549d84f5bf26207670343df6a6ceb544a` | `b428bab815754af4e064aacad9b64347f3fdade4777279869b3106f8b7625f81` | `0e9fac7cfb8de71896777a2bcd685cde9291ac0752fb97f21d028fb32ca83988` |
| x56 canonical | `fcf5c09e4b5adfc055fd7ebc65fc1c74f7f2c582` | `40cf3172acd0929ccd148080e36ca698bd3fdcc852413da339b6c2d7efc50a2e` | `0c75b7ae007ac6b370c50c937b9c29fcc90ef93c0547f3df39d47af48a416ef4` |
| V2 RESET-V2.txt | `8d67a75c40bb99dd5066e64ae8e8db687c7daa1f` | `d62a127b6c1d50cf37f0e2320dc98f6be7c45002418f7be618fc8d57bd5386de` | `608dfd3e547ee65738662bf62ef9c9cb548b0b7ea1000b21c22087ee0c958db8` |
| l16 frozen private variant | Historical run `20261029-235836-strongarm-reset-size` | `4c1417fb771024fc1c4568a2d0a1329d7031567df7edeccf5b4a9c34afaef44f` | `56e3dddc5148fa35041f391de76c820e9e15927221bfc58dc79bea4bc7744577` |
| V32 RESET-V32.txt | `d283d2014a3bad62f98f98bc03603f0199c11a55` | `23a335e46b15f5f1b4a3c427371fd218743ec3928bf6eb2f7c32cd175571f760` | `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557` |
| B13 canonical | `78ab776553b77383cb642956e43ed6ac203a3749` | `1ae59a175d23a8fd19a2eaf47f0d6b8d2a4a44282f18210c72bd13bf97d6c31a` | `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0` |
| B20 canonical, old formal | `2b1190fab874bd1324fa44abb7a8ff8c480e7c7b` | `260765517bbe06d09a0c03126cd84911b81688ef3ee83d06aca7d421d4d4f22a` | `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f` |
| B20 current-regime frozen variant | `b52372eaf0c4cd4b8ed2e2cc628ff1707a693750` | `c2f8ab2e92d53cce19da0a26bd47baf8f5dcb019bd5779711cbe6a4416798f56` | `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f` |

- [p56 baseline and repair history](https://github.com/many-question/ADC-12b-100M/blob/d2dd7184b0f435b46b351b948eb1ca4bdbeeb99b/design/xtor/adc_comp/many-question-strongarm/BASELINE-BEFORE-RESET-V14.md) and [exact p56 source](https://github.com/many-question/ADC-12b-100M/blob/5089a93549d84f5bf26207670343df6a6ceb544a/design/xtor/adc_comp/many-question-strongarm/adc_comp.scs).
- [x56 baseline and repair history](https://github.com/many-question/ADC-12b-100M/blob/c412c651b6d3e2578fbc43b01a963fbb81ddfcfd/design/xtor/adc_comp/many-question-miyahara/BASELINE-BEFORE-BUFFER-V12.md) and [exact x56 source](https://github.com/many-question/ADC-12b-100M/blob/fcf5c09e4b5adfc055fd7ebc65fc1c74f7f2c582/design/xtor/adc_comp/many-question-miyahara/adc_comp.scs).
- [V2 restored measurements, unrounded CIs and archive hashes](https://github.com/many-question/ADC-12b-100M/blob/76d9d0278d089a47b7dba6baf2c5782309e7460e/design/xtor/adc_comp/many-question-strongarm/RESTORATION-11.md) and [exact V2 source](https://github.com/many-question/ADC-12b-100M/blob/8d67a75c40bb99dd5066e64ae8e8db687c7daa1f/design/xtor/adc_comp/many-question-strongarm/RESET-V2.txt).
- [l16 current-rule measurements, exact source hash and archive hashes](https://github.com/many-question/ADC-12b-100M/blob/76d9d0278d089a47b7dba6baf2c5782309e7460e/design/xtor/adc_comp/many-question-strongarm/RESTORATION-SECONDARY.md). Its 144.57 uV pilot remains explicitly separate from this full-FS measurement.
- [V32 complete scope and failures](https://github.com/many-question/ADC-12b-100M/blob/d2dd7184b0f435b46b351b948eb1ca4bdbeeb99b/design/xtor/adc_comp/many-question-strongarm/RESET-V32.md).
- [B13 formal TT and four hot-corner results](https://github.com/many-question/ADC-12b-100M/blob/c412c651b6d3e2578fbc43b01a963fbb81ddfcfd/design/xtor/adc_comp/many-question-miyahara/FORMAL-BUFFER-V13.md) and [Miyahara current-numerics evidence](https://github.com/many-question/ADC-12b-100M/blob/52145b84a2bb73ed7a177c01cb32ba0eac006139/design/xtor/adc_comp/many-question-miyahara/NUMERICS-94.md).
- [Matched energy comparisons and measured branch currents](https://github.com/many-question/ADC-12b-100M/blob/d2dd7184b0f435b46b351b948eb1ca4bdbeeb99b/design/xtor/adc_comp/many-question-strongarm/ENERGY-COMPARISON.md).
