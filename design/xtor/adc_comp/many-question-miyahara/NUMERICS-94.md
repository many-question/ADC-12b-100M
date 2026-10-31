# Numerical-settings transition: issue #94

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

## Merged workflow update, 2026-10-31

[PR #95](https://github.com/many-question/ADC-12b-100M/pull/95) merged at 12:44:34 into main as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`; adc_comp is now 0.8.0. The actual comparator testbench and specification patches match the precheck settings. The private runs below retain their original pre-merge source and status. Necessary key evidence will be refreshed through the merged official runner and testbenches with exact ADCToolbox commit `cd72061ff3b7a977163dac540da126ae22f5e38d`. No rehash or private-result relabeling restores formal evidence. Stale warnings still mean ineligible; final merged per-test crosscheck rules apply where specified. New formal notices are checked before subsequent batches.

The following transition plan records the earlier, unmerged checkpoint and is superseded by the merged update above.

At the 2026-10-31 checkpoint, [issue #94](https://github.com/many-question/ADC-12b-100M/issues/94) is an unmerged announcement, with no comments or corresponding open workflow PR. Fetched main is `3b0c002a507b5f5fba1dfbc7059db5ef103e2860`. All existing deterministic screens, phase diagnostics and original formal records use the preceding settings. They remain preserved and do not establish compliance with the announced settings.

The previously started original TT noise run completed from clean source `2b1190fab874bd1324fa44abb7a8ff8c480e7c7b`: 191.159437 uV rms, 95% profile interval 183.31 to 199.41 uV, all 8704 finite samples and exactly 512 at each of 17 levels. Its original JSON and figure remain unchanged. The complete evidence archive has SHA-256 `670a0852afeab4d946dc9b712b26e1b741ebfea8f85b0771b3b406173f501b9c`, with every member read back using CRC and SHA checks. This is old-settings evidence; hot-corner formal expansion does not follow until the revised flow is available.

Two of 96 formal records match B20 electrically and 94 retain earlier source hashes. Electrical matching does not establish freshness under the announced numerical settings. The old TT kickback value of 0.004586 uV is retained as the numerical output actually recorded, not as an established physical kickback value.

Private prechecks use APS, `errpreset=conservative`, and no explicit `maxstep`. Ordinary logs are expected to show gear2only, reltol 1e-4, relref alllocal and lteratio 10. Kickback requires effective reltol 1e-6 and vabstol 10 nV. Requested and effective tolerances are checked separately because conservative tightens reltol; the actual Spectre log is decisive. Priority goes to the B20 high-voltage cold-corner terminal stress, slow/hot reset and new-settings kickback/noise. The old tight SF stress margin was only 253.490912 uV.

These private runs do not update formal records or change shared tools, testbenches, specifications or thresholds. After merge, affected delay, kickback, noise and mismatch tests will be rerun through the merged official flow on frozen actual sources, preserving failures. Rehash cannot restore old evidence. The announced ADCToolbox dependency is upstream commit `cd72061`, not PyPI 0.9.1. Merge status and formal module notices are checked before each batch and PR update; #94 itself requests no acknowledgment. Full qualification, remaining corners, operating-range checks, mixed-top regression and lead review remain open.


Shared reporting convention: the automatic maxstep bound in a log is not an explicit deck setting. Each archived run records actual APS threading and the six-job session ceiling. The compact wording below preserves every run heading, requested/effective setting, metric table, failure and archive hash. The [unabridged earlier wording](https://github.com/many-question/ADC-12b-100M/blob/855618b7d6ad7aeed2b909dfbd70e4b86975e99a/design/xtor/adc_comp/many-question-miyahara/NUMERICS-94.md) remains fixed in published history. Present raw availability is governed by EVIDENCE-RETENTION, including superseded archives that were released.

## Private precheck 20261031-115735-miyahara-buffer-v20-notice94-delay-announced-screen

Test `tb_comp_delay`, accuracy `announced`, frozen clean source `b52372eaf0c4cd4b8ed2e2cc628ff1707a693750`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 51.454206176 | 43.026751042 | 21.690059446 | 0.999354260763 | 36 / 36 | PASS |
| sf_high_m40 | 55.714198671 | 46.281542964 | 22.740937084 | 0.999498574260 | 36 / 36 | PASS |
| ss_low_125 | 81.243858209 | 65.852219364 | 34.565290945 | 0.816233054312 | 36 / 36 | PASS |
| tt_nom_27 | 58.178086741 | 47.852823183 | 25.122445139 | 0.908277825263 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 590.097391547 fJ/cycle: 216.634245588 evaluation and 373.463145959 reset. The original meter gives 590.568141960 fJ/cycle; the waveform-integral difference is -0.079711%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 37.4606 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 34.2641 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `5a809cda2066594b69c0d9805a6569eb37ebb14bb6e1ab27d8b532401e08fbf2` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-120346-miyahara-buffer-v20-notice94-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `b52372eaf0c4cd4b8ed2e2cc628ff1707a693750`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| sf_high_m40 | 55.856387696 | 46.288072849 | 22.314435186 | 0.999738104927 | 36 / 36 | PASS |
| ss_low_125 | 81.497004707 | 65.857671854 | 33.744693617 | 0.816389325007 | 36 / 36 | PASS |
| tt_nom_27 | 58.340296634 | 47.856914989 | 24.593307457 | 0.908484695228 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 590.793397012 fJ/cycle: 217.068560428 evaluation and 373.724836584 reset. The original meter gives 590.822127720 fJ/cycle; the waveform-integral difference is -0.004863%. Both values are preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.142189025 ps, 30 mV delay +0.006529884 ps, reset -0.426501898 ps. Largest per-pair stress change is 670.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +0.253146499 ps, 30 mV delay +0.005452491 ps, reset -0.820597328 ps. Largest per-pair stress change is 580.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.162209893 ps, 30 mV delay +0.004091805 ps, reset -0.529137682 ps. Largest per-pair stress change is 920.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 29.0 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `9c99f9d3e95a58aa01317d6612e6ea9600d18f0d48b8296273daa98e6a1d44c6` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-120406-miyahara-buffer-v20-notice94-kickback-announced-screen

Test `tb_comp_kickback`, accuracy `announced`, frozen clean source `b52372eaf0c4cd4b8ed2e2cc628ff1707a693750`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.328731219 | 11.288522979 | 0.000089411 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 25.236375 uV instantaneous differential change and 7.425379 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `8.94110998347214e-05` uV; instantaneous differential peak magnitude `25.236375154639003` uV (signed change `-2.5236375154639003e-05` V), cycle 1, `41.6474902437462` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99997500000003` ps. Maximum common-mode excursion is `7.425379036375523` mV, in evaluation at `198.14281503283968` ps after its cycle-1 sample.

The supplemental phase/load context was derived from the SHA-verified archive without rewriting it; context-file SHA-256 is `284411ab7c10b9fab4d36b4d72c1a4a67db88294f61765a5e28fc2b0a20a2c6e`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 26.8193 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `2e0838caf0728f66bec688744cc43111b543cf0318151a1678830f635d79d6a0` passed every-member CRC/SHA readback. Full qualification remains open.

The later phase/load supplement is also preserved in a separate verified archive, SHA-256 `d644c7aaa33e654444ec8aff293aa78f07e9a7db885e3d80ca1f53c6f6a91288`; the original run archive remains unchanged.


## Private precheck 20261031-121047-miyahara-buffer-v20-notice94-kickback-tighter-screen

Test `tb_comp_kickback`, accuracy `tighter`, frozen clean source `b52372eaf0c4cd4b8ed2e2cc628ff1707a693750`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-6", "vabstol": "1e-9"}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.328731219 | 11.288471705 | 0.000084992 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 25.237841 uV instantaneous differential change and 7.425734 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

| Quantity | Announced precision | Tighter precision | Difference |
|---|---:|---:|---:|
| kickback_uV | 8.94110998347e-05 | 8.4991999983e-05 | -4.41909985167e-06 |
| cin_fF | 19.3287312187 | 19.3287312187 | +0 |
| cin_clkc_fF | 11.2885229791 | 11.2884717051 | -5.12740421623e-05 |
| max_instantaneous_differential_change_uV | 25.2363751546 | 25.237840953 | +0.00146579832798 |
| max_instantaneous_common_mode_change_mV | 7.42537903638 | 7.42573364601 | +0.000354609633546 |

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `8.49919999830473e-05` uV; instantaneous differential peak magnitude `25.237840952966987` uV (signed change `-2.5237840952966988e-05` V), cycle 1, `41.586452909315604` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99999750000003` ps. Maximum common-mode excursion is `7.4257336460090695` mV, in evaluation at `198.20392799531726` ps after its cycle-1 sample.

The supplemental phase/load context was derived from the SHA-verified archive without rewriting it; context-file SHA-256 is `f73ad44f778fef416be5c2ac3c42cc17c36a7352cedc0cfe8e3a5c3fa7b5eb26`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-07 | 1e-09 | gear2only / conservative / alllocal / 10 | 33.0 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `609e2f4eb3a968ab272ee6e746ca1bb638e56aebe97a21e8b9657894202ccc8d` passed every-member CRC/SHA readback. Full qualification remains open.

The later phase/load supplement is also preserved in a separate verified archive, SHA-256 `d644c7aaa33e654444ec8aff293aa78f07e9a7db885e3d80ca1f53c6f6a91288`; the original run archive remains unchanged.


## Private precheck 20261031-121123-miyahara-buffer-v20-notice94-noise-announced-screen

Test `tb_comp_noise`, accuracy `announced`, frozen clean source `b52372eaf0c4cd4b8ed2e2cc628ff1707a693750`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| fs_low_125 | 343.494401429 | 332.03 to 355.53 | 0.005967231 | 8704 | FAIL: CMP-13 |
| tt_nom_27 | 191.438003120 | 183.58 to 199.69 | 0.000473353 | 8704 | PASS |

The full original 17 levels, 512 samples per level, 50 GHz bandwidth and seed 1 are preserved. Every sample is finite and none is omitted. The original outputstart=tstop waveform cannot establish reset history or full-trace terminal stress; those are separate checks. The noise interval is conditional on the Gaussian-CDF fit.

At fs_low_125, minimum sampled output magnitude is 0.785370696 V and maximum absolute standardized Gaussian-fit residual is 1.454285. These residuals are diagnostic, not a proof that the physical distribution is Gaussian.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 3 |
| -700 | 7 |
| -600 | 20 |
| -500 | 42 |
| -400 | 72 |
| -300 | 98 |
| -200 | 142 |
| -100 | 194 |
| 0 | 276 |
| 100 | 333 |
| 200 | 373 |
| 300 | 405 |
| 400 | 451 |
| 500 | 470 |
| 600 | 491 |
| 700 | 501 |
| 800 | 509 |

At tt_nom_27, minimum sampled output magnitude is 0.873756545 V and maximum absolute standardized Gaussian-fit residual is 2.061121. These residuals are diagnostic, not a proof that the physical distribution is Gaussian.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 2 |
| -400 | 12 |
| -300 | 35 |
| -200 | 73 |
| -100 | 133 |
| 0 | 275 |
| 100 | 355 |
| 200 | 444 |
| 300 | 478 |
| 400 | 501 |
| 500 | 510 |
| 600 | 512 |
| 700 | 512 |
| 800 | 512 |

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | None |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | None |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `4286f1b5f0c5e16cf7624bbebcdbb51551f3ebc3c92f2c6bce32c5a7ad0f916c` passed every-member CRC/SHA readback. Full qualification remains open.

This electrical source fails the private proposed-settings gate. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-124258-miyahara-buffer-v21-notice94-delay-announced-screen

Test `tb_comp_delay`, accuracy `announced`, frozen clean source `a1d163133ac6c59acdc2ed46523023e16c80949e`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 52.924993560 | 43.715370887 | 22.322850363 | 0.998807387238 | 36 / 36 | PASS |
| fs_low_125 | 70.676098865 | 54.868882292 | 28.078949273 | 0.812121767974 | 36 / 36 | PASS |
| sf_high_m40 | 57.162607398 | 47.004619246 | 23.370321774 | 0.998853677474 | 36 / 36 | PASS |
| ss_low_125 | 85.032597165 | 67.427196831 | 35.420692191 | 0.815689155525 | 36 / 36 | FAIL: CMP-08 |
| tt_nom_27 | 60.040523314 | 48.663763208 | 25.702909526 | 0.907732905178 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 593.221215187 fJ/cycle: 220.643949039 evaluation and 372.577266148 reset. The original meter gives 593.706592440 fJ/cycle; the waveform-integral difference is -0.081754%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 34.0812 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 35.9325 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `15f17579b154b710df0b0f74b6995236d69403baf66e398f64f79f039990e0de` passed every-member CRC/SHA readback. Full qualification remains open.

This electrical source fails the private proposed-settings gate. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Proposed-settings short B20 phase baseline

Run `20261031-124307-miyahara-buffer-v20-notice94-noise-phase-diagnostic-screen` uses clean source `a1d163133ac6c59acdc2ed46523023e16c80949e` and the unchanged B20 electrical source. It is a diagnostic with 128 cycles at each of -800 and +800 uV, 400 ps clock, original physical source/load conditions and seed 1. Actual logs confirm conservative, gear2only, reltol 1e-4, vabstol 1e-6, alllocal and lteratio 10, with no explicit maxstep. The 102.5 ns duration raises noisefmin to 9.7561 MHz, versus 287.216 kHz for the full test; it does not replace the full 343.4944014285115 uV FS noise failure.

All 256 finite samples per corner are retained. TT has 0/256 incorrect decisions; FS/low/125 has 1/256. Both corners complete all 256 resets with no early/middle-to-final sign changes, late reset violations, output-validity violations or reported terminal-stress violations. All original waveforms and phase/current statistics remain in verified archive `960476031e070fdc487dca44e41de7c7f1d98becf7b3c7031a0f19602020c24b`; owned remote data is removed and absence confirmed.

| Corner | RP descriptive SNR at +30 ps | At +40 ps | RP sign errors at +50 ps | Max sampled reset ps |
|---|---:|---:|---:|---:|
| fs_low_125 | 1.638003632 | 2.429985495 | 1 | 27.211536904 |
| tt_nom_27 | 2.487977226 | 4.318435978 | 0 | 25.000000002 |

These two-level phase ratios include nonlinear regeneration and saturation; they are not linear gain or formal input-referred noise. Differences between TT and FS/low/125 combine process, supply and temperature and do not isolate one cause.


## Private precheck 20261031-131817-miyahara-buffer-v22-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `d8f3002c6dec07fb8fa03646e07997a38397a666`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 52.933697611 | 43.719053386 | 21.408865583 | 0.998768988475 | 36 / 36 | PASS |
| fs_low_125 | 70.677521297 | 54.872768350 | 26.694289076 | 0.813249658736 | 36 / 36 | PASS |
| sf_high_m40 | 57.150642403 | 46.995379297 | 22.399532917 | 0.998832382737 | 36 / 36 | PASS |
| ss_low_125 | 85.033180602 | 67.429036855 | 34.071442459 | 0.816829614447 | 36 / 36 | PASS |
| tt_nom_27 | 60.047639458 | 48.661348937 | 24.725165065 | 0.907738971948 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 596.185510717 fJ/cycle: 221.046003124 evaluation and 375.139507593 reset. The original meter gives 596.682927000 fJ/cycle; the waveform-integral difference is -0.083364%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 32.1617 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 33.8064 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `5f94e2debe4a8f549c57e17719cfd46eeb8936fbbb6f0c957640cb56059d4c6d` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-132625-miyahara-buffer-v22-spec08-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `d8f3002c6dec07fb8fa03646e07997a38397a666`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{"reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 53.041135620 | 43.707294983 | 20.986455394 | 0.998985153921 | 36 / 36 | PASS |
| sf_high_m40 | 57.306128210 | 47.007581885 | 22.012690782 | 0.999115811074 | 36 / 36 | PASS |
| ss_low_125 | 85.339954989 | 67.427282291 | 33.300871031 | 0.817047340394 | 36 / 36 | PASS |
| tt_nom_27 | 60.215271388 | 48.666272117 | 24.282080927 | 0.907907863342 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 596.920364186 fJ/cycle: 221.547545466 evaluation and 375.372818720 reset. The original meter gives 596.949467040 fJ/cycle; the waveform-integral difference is -0.004875%. Both values are preserved.

Same-source tighter-minus-announced comparison at fs_high_m40: 1 mV delay +0.107438009 ps, 30 mV delay -0.011758403 ps, reset -0.422410188 ps. Largest per-pair stress change is 560.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.155485806 ps, 30 mV delay +0.012202588 ps, reset -0.386842135 ps. Largest per-pair stress change is 760.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +0.306774387 ps, 30 mV delay -0.001754564 ps, reset -0.770571428 ps. Largest per-pair stress change is 550.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.167631930 ps, 30 mV delay +0.004923180 ps, reset -0.443084138 ps. Largest per-pair stress change is 970.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 29.0 |
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 29.0 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `a964a42812482b2f92e4d57f789d3e10c0c987b7d8b93ffa6cfdfb9c8980f1da` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-134338-miyahara-buffer-v22-spec08-noise-baseline-screen

Test `tb_comp_noise`, accuracy `baseline`, frozen clean source `7c5afe3be0b5553506c216181995eb07d6fd8bb1`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| fs_low_125 | 342.511757415 | 331.11 to 354.49 | 0.012396837 | 8704 | FAIL: CMP-13 |

The full original 17 levels, 512 samples per level, 50 GHz bandwidth and seed 1 are preserved. Every sample is finite and none is omitted. The original outputstart=tstop waveform cannot establish reset history or full-trace terminal stress; those are separate checks. The noise interval is conditional on the Gaussian-CDF fit.

At fs_low_125, minimum sampled output magnitude is 0.785375010 V and maximum absolute standardized Gaussian-fit residual is 3.054453. These residuals are diagnostic, not a proof that the physical distribution is Gaussian.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 4 |
| -700 | 5 |
| -600 | 21 |
| -500 | 33 |
| -400 | 76 |
| -300 | 66 |
| -200 | 137 |
| -100 | 184 |
| 0 | 267 |
| 100 | 318 |
| 200 | 378 |
| 300 | 405 |
| 400 | 438 |
| 500 | 469 |
| 600 | 493 |
| 700 | 491 |
| 800 | 510 |

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | None |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `26e302577d4bb1e1ba873aa319be231f6edc2458770a06bc2ab6fc7215845240` passed every-member CRC/SHA readback. Full qualification remains open.

This electrical source fails the private experimental gate on the merged 0.8.0 baseline. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-151621-miyahara-buffer-v23-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `c3b7afee025c8c97fb22bcd4dbea1b3fe75d7bff`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 53.232886398 | 45.255767742 | 29.806597490 | 0.999776145263 | 36 / 36 | PASS |
| fs_low_125 | 66.220278649 | 54.591661601 | 35.692638483 | 0.813230740423 | 36 / 36 | FAIL: CMP-08 |
| sf_high_m40 | 59.188555215 | 49.578186747 | 30.661744750 | 0.999439615188 | 36 / 36 | PASS |
| ss_low_125 | 80.757598217 | 67.380901503 | 46.139417259 | 0.816904192418 | 36 / 36 | FAIL: CMP-08 |
| tt_nom_27 | 59.657300543 | 50.149655580 | 34.646199388 | 0.908492882231 | 36 / 36 | FAIL: CMP-06 |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 667.197031713 fJ/cycle: 256.218888413 evaluation and 410.978143301 reset. The original meter gives 667.733088600 fJ/cycle; the waveform-integral difference is -0.080280%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 31.7257 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 30.9084 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `fa9c7f2c759ee3be53dd4ce7daf89cfcc4179781830004362fa4a6b6984b21aa` passed every-member CRC/SHA readback. Full qualification remains open.

This electrical source fails the private experimental gate on the merged 0.8.0 baseline. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-151635-miyahara-buffer-v23-spec08-kickback-baseline-screen

Test `tb_comp_kickback`, accuracy `baseline`, frozen clean source `c3b7afee025c8c97fb22bcd4dbea1b3fe75d7bff`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.328731219 | 12.105070079 | 0.000083107 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 28.669688 uV instantaneous differential change and 7.418295 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `8.310719994131244e-05` uV; instantaneous differential peak magnitude `28.669688034964768` uV (signed change `-2.866968803496477e-05` V), cycle 1, `49.1687119340883` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99997500000003` ps. Maximum common-mode excursion is `7.418294723631758` mV, in evaluation at `198.177560250713` ps after its cycle-1 sample.

The phase/load context was derived from SHA-verified raw evidence without modifying the traces; context-file SHA-256 is `8b31c188751e0f48c2776fabda5a459caf702f9f450c2f0bf53ef70a309ea01d`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 25.5745 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `340e1463aa7f293ec8c20a0cf4816d56a674e52f96eb51384ec328a9c7e087e6` passed every-member CRC/SHA readback. Full qualification remains open.

The complete phase/load context is included in this run's verified archive.


## Private precheck 20261031-152741-miyahara-buffer-v24-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `892fe664af7c0764ed93b689b28da4514b64dd63`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 52.978266530 | 45.123006144 | 20.874809018 | 0.999952399581 | 36 / 36 | PASS |
| fs_low_125 | 65.962846545 | 54.516492777 | 26.158008924 | 0.813181441882 | 36 / 36 | PASS |
| sf_high_m40 | 58.944266845 | 49.452350536 | 21.636937465 | 0.999618401246 | 36 / 36 | PASS |
| ss_low_125 | 79.984397129 | 67.044100250 | 32.178941962 | 0.817080371476 | 36 / 36 | PASS |
| tt_nom_27 | 59.359488787 | 50.004977456 | 24.027469464 | 0.908611903035 | 36 / 36 | FAIL: CMP-06 |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 699.364658662 fJ/cycle: 255.420517725 evaluation and 443.944140937 reset. The original meter gives 699.939986400 fJ/cycle; the waveform-integral difference is -0.082197%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 29.1954 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 29.0 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `2cd8f43a2829e19f19c91bc9cf7ab356afb08692e9dfe466c652dbd901e08c3e` passed every-member CRC/SHA readback. Full qualification remains open.

This electrical source fails the private experimental gate on the merged 0.8.0 baseline. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-152755-miyahara-buffer-v24-spec08-kickback-baseline-screen

Test `tb_comp_kickback`, accuracy `baseline`, frozen clean source `892fe664af7c0764ed93b689b28da4514b64dd63`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.328731219 | 12.105033731 | 0.000082911 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 30.673205 uV instantaneous differential change and 7.418208 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `8.291090015065394e-05` uV; instantaneous differential peak magnitude `30.67320509575933` uV (signed change `-3.067320509575933e-05` V), cycle 1, `208.77303347348487` ps after its pre-evaluation sample. The peak is in **reset**, whose measured window runs from that sample to `199.99997499999992` ps. Maximum common-mode excursion is `7.418207759610773` mV, in evaluation at `198.12496019318317` ps after its cycle-1 sample.

The phase/load context was derived from SHA-verified raw evidence without modifying the traces; context-file SHA-256 is `308d3ccccb75a15b709f67e8bb1872e6b9e94e3b82d4676e7a4500730e12716d`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 25.5745 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `755525d32f379a3891466cd6bfe5c08e5f3412ff9992c3258d5643dd1ba5ca7b` passed every-member CRC/SHA readback. Full qualification remains open.

The complete phase/load context is included in this run's verified archive.


## Private precheck 20261031-153955-miyahara-buffer-v25-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `0768f17556b497d222a2b9d07bb9d72a63e5ed4e`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 51.871911574 | 43.981568001 | 21.139312732 | 0.999575073364 | 36 / 36 | PASS |
| fs_low_125 | 64.442167516 | 52.849720192 | 26.455164313 | 0.813181656341 | 36 / 36 | PASS |
| sf_high_m40 | 57.770698046 | 48.239524480 | 22.040497636 | 0.999311850708 | 36 / 36 | PASS |
| ss_low_125 | 78.059647901 | 65.011445755 | 32.647276881 | 0.816437679775 | 36 / 36 | PASS |
| tt_nom_27 | 58.046803629 | 48.652311810 | 24.449384612 | 0.908208501608 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 702.356656497 fJ/cycle: 257.200838026 evaluation and 445.155818471 reset. The original meter gives 702.937018800 fJ/cycle; the waveform-integral difference is -0.082562%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 32.9684 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `be67008f1cb9c7d2bf5aee8d1cfa72fe3b964ca1c6dbd36e460d9fbdf26a8ad0` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-154013-miyahara-buffer-v25-spec08-kickback-baseline-screen

Test `tb_comp_kickback`, accuracy `baseline`, frozen clean source `0768f17556b497d222a2b9d07bb9d72a63e5ed4e`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.328731219 | 12.105047338 | 0.000085876 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 30.643116 uV instantaneous differential change and 7.418206 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `8.58761000678554e-05` uV; instantaneous differential peak magnitude `30.64311606267001` uV (signed change `-3.064311606267001e-05` V), cycle 1, `208.81896388285887` ps after its pre-evaluation sample. The peak is in **reset**, whose measured window runs from that sample to `199.99997499999998` ps. Maximum common-mode excursion is `7.418206202436939` mV, in evaluation at `198.1180368403619` ps after its cycle-1 sample.

The phase/load context was derived from SHA-verified raw evidence without modifying the traces; context-file SHA-256 is `4653ea836cce6e758d56656911e39a78aa6cfe79dcfbe8537a143f52779b4260`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 25.5745 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `4d8c53ec7d1ef654934df795ba0a471deaae6bb0aa46a33f1cb6ceecd88a695d` passed every-member CRC/SHA readback. Full qualification remains open.

The complete phase/load context is included in this run's verified archive.
