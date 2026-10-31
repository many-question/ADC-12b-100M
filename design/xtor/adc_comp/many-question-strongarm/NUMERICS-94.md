# Numerical-settings transition: issue #94

## Merged workflow update, 2026-10-31

[PR #95](https://github.com/many-question/ADC-12b-100M/pull/95) merged at 12:44:34 into main as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`; adc_comp is now 0.8.0. The actual comparator testbench and specification patches match the precheck settings. The private runs below retain their original source and pre-merge status. Key evidence will be refreshed through the merged official runner and testbenches with the exact ADCToolbox commit `cd72061ff3b7a977163dac540da126ae22f5e38d`; no private result or old metadata is relabeled. A stale warning still means ineligible. Final merged per-test crosscheck rules apply where specified. New formal module notices are checked before subsequent batches.

The following transition plan records the earlier, unmerged checkpoint; it is superseded by the merged update above.

At the 2026-10-31 checkpoint, [issue #94](https://github.com/many-question/ADC-12b-100M/issues/94) is an unmerged announcement, with no comments or corresponding open workflow PR. Fetched main is `3b0c002a507b5f5fba1dfbc7059db5ef103e2860`. The existing deterministic screens, phase diagnostics and original formal records use the preceding settings. Their source hashes and measured results remain preserved; they do not establish compliance with the announced settings.

The next private checks use APS, `errpreset=conservative`, and no explicit `maxstep`. Ordinary transient logs are expected to show gear2only, reltol 1e-4, relref alllocal and lteratio 10. Kickback requires effective reltol 1e-6 and vabstol 10 nV. Requested and effective tolerances are recorded separately because conservative tightens reltol. The actual Spectre log determines whether the intended protocol ran. Prior sub-microvolt kickback numbers are historical numerical outputs, not established physical kickback.

RESET-V27 has 23 MOS and five MOM capacitors. Its ten known risk corners and targeted tighter runs passed under the old private settings; the tighter TT 30 mV delay was 49.838320 ps. This thin margin needs rechecking. No formal record yet matches V27: all 92 preserved records refer to earlier electrical sources. Promotion preserves electrical content and is not qualification.

Old-settings full-corner formal expansion is paused while circuit development continues. First priority is private critical-corner timing, all-cycle reset/output validity and whole-transient terminal stress, followed by kickback and noise checks. These private runs do not write formal records or alter shared testbenches, tools, specifications or thresholds.

After the flow merges, affected delay, kickback, noise and mismatch tests must be rerun through the merged official runner and testbenches on frozen actual sources. Rehash cannot restore old evidence. The announced ADCToolbox dependency is upstream commit `cd72061`, not the same-version PyPI 0.9.1 package. Merge status and formal module notices are checked before each batch and PR update; the announcement itself requests no acknowledgment. Qualification, remaining-corner coverage, operating-range checks, mixed-top regression and lead review remain open.


## Private precheck 20261031-115725-strongarm-reset-v27-notice94-delay-announced-screen

Test `tb_comp_delay`, accuracy `announced`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.520043338 | 44.044297203 | 21.480771214 | 0.995404895798 | 36 / 36 | PASS |
| sf_high_m40 | 72.104932166 | 54.584095666 | 20.176357943 | 0.996806248659 | 36 / 36 | PASS |
| ss_low_125 | 89.881821460 | 67.032533726 | 34.083059100 | 0.816333032969 | 36 / 36 | PASS |
| tt_nom_27 | 65.381597902 | 49.727161527 | 24.077135846 | 0.906104108056 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 406.328839435 fJ/cycle: 86.844638589 evaluation and 319.484200846 reset. The original meter gives 406.821567240 fJ/cycle; the waveform-integral difference is -0.121116%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `709c4647e9ae4608dd04f2e74014101290032f4a7018554808d9be46dcd39375` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.


## Private precheck 20261031-120336-strongarm-reset-v27-notice94-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| sf_high_m40 | 73.005073352 | 54.717508029 | 19.700503312 | 0.996800000299 | 36 / 36 | PASS |
| ss_low_125 | 91.585393981 | 67.179651139 | 33.318872126 | 0.816328198383 | 36 / 36 | PASS |
| tt_nom_27 | 66.349849218 | 49.835069740 | 23.736431481 | 0.906090197265 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 408.778397819 fJ/cycle: 89.170539589 evaluation and 319.607858229 reset. The original meter gives 408.812747040 fJ/cycle; the waveform-integral difference is -0.008402%. Both values are preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.900141187 ps, 30 mV delay +0.133412363 ps, reset -0.475854631 ps. Largest per-pair stress change is 210.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +1.703572521 ps, 30 mV delay +0.147117412 ps, reset -0.764186974 ps. Largest per-pair stress change is 570.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.968251317 ps, 30 mV delay +0.107908212 ps, reset -0.340704365 ps. Largest per-pair stress change is 230.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `a0ee84791027375a03ad3e0f1a33f66e58c2e2b1f4a3bad6c27a91b99ce2fc83` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.


## Private precheck 20261031-120357-strongarm-reset-v27-notice94-kickback-announced-screen

Test `tb_comp_kickback`, accuracy `announced`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118543 | 15.782208772 | 0.000050251 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 354.571903 uV instantaneous differential change and 7.405379 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `5.025120011943607e-05` uV; instantaneous differential peak magnitude `354.57190254149543` uV (signed change `0.00035457190254149546` V), cycle 8, `66.96310955267225` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99997500000055` ps. Maximum common-mode excursion is `7.405379196107786` mV, in evaluation at `198.20486963065588` ps after its cycle-1 sample.

The supplemental phase/load context was derived from the SHA-verified archive without rewriting it; context-file SHA-256 is `cd50e6b191698acbc704578b46892cacd9193ec6073073c3372a858df228b25b`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 33.0 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `d41c26241ccccdf79ce60560e804c431b7e6ea9280cccf0366a875c2856773ed` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.

The later phase/load supplement is also preserved in a separate verified archive, SHA-256 `d644c7aaa33e654444ec8aff293aa78f07e9a7db885e3d80ca1f53c6f6a91288`; the original run archive remains unchanged.


## Private precheck 20261031-121037-strongarm-reset-v27-notice94-kickback-tighter-screen

Test `tb_comp_kickback`, accuracy `tighter`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-6", "vabstol": "1e-9"}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118543 | 15.782118507 | 0.000037492 | PASS |

The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 354.618788 uV instantaneous differential change and 7.405457 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

| Quantity | Announced precision | Tighter precision | Difference |
|---|---:|---:|---:|
| kickback_uV | 5.02512001194e-05 | 3.74916001022e-05 | -1.27596000172e-05 |
| cin_fF | 19.3311185429 | 19.3311185429 | +0 |
| cin_clkc_fF | 15.7822087719 | 15.7821185072 | -9.02646988621e-05 |
| max_instantaneous_differential_change_uV | 354.571902541 | 354.618787923 | +0.0468853815375 |
| max_instantaneous_common_mode_change_mV | 7.40537919611 | 7.40545699018 | +7.77940705188e-05 |

Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

Unrounded recorded values: net per-cycle metric `3.749160010224628e-05` uV; instantaneous differential peak magnitude `354.6187879230329` uV (signed change `0.00035461878792303293` V), cycle 2, `67.06524039163574` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99999749999998` ps. Maximum common-mode excursion is `7.405456990178305` mV, in evaluation at `198.18385786003088` ps after its cycle-1 sample.

The supplemental phase/load context was derived from the SHA-verified archive without rewriting it; context-file SHA-256 is `1d48415a5754a3088a1b125b3c37820c03a074d10327be0a9dde55b1df8682ba`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-07 | 1e-09 | gear2only / conservative / alllocal / 10 | 27.4104 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `acf992e2f6b53a93232ab9b9c5dd0418c61c4bf4c7641151943423a6abd0cd89` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.

The later phase/load supplement is also preserved in a separate verified archive, SHA-256 `d644c7aaa33e654444ec8aff293aa78f07e9a7db885e3d80ca1f53c6f6a91288`; the original run archive remains unchanged.


## Private precheck 20261031-121026-strongarm-reset-v27-notice94-noise-announced-screen

Test `tb_comp_noise`, accuracy `announced`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| tt_nom_27 | 210.100860925 | 201.81 to 218.79 | 0.005125216 | 8704 | FAIL: CMP-01 |

The full original 17 levels, 512 samples per level, 50 GHz bandwidth and seed 1 are preserved. Every sample is finite and none is omitted. The original outputstart=tstop waveform cannot establish reset history or full-trace terminal stress; those are separate checks. The noise interval is conditional on the Gaussian-CDF fit.

At tt_nom_27, minimum sampled output magnitude is 0.899741577 V and maximum absolute standardized Gaussian-fit residual is 3.446225. These residuals are diagnostic, not a proof that the physical distribution is Gaussian.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 2 |
| -400 | 13 |
| -300 | 38 |
| -200 | 89 |
| -100 | 143 |
| 0 | 290 |
| 100 | 343 |
| 200 | 406 |
| 300 | 470 |
| 400 | 495 |
| 500 | 506 |
| 600 | 512 |
| 700 | 512 |
| 800 | 512 |

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | None |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `94ace46b19d543b73f691f45523fbfe9ed28bec34660fe3350ca9929c5c800e3` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.

This electrical source fails the private proposed-settings gate. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-123312-strongarm-reset-v28-notice94-delay-announced-screen

Test `tb_comp_delay`, accuracy `announced`, frozen clean source `dfc2832c1d7f090b07567b6fc6e26eca6db912ba`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.582803438 | 44.075924180 | 21.495257778 | 0.995305503669 | 36 / 36 | PASS |
| sf_high_m40 | 72.278673274 | 54.577426176 | 20.162389672 | 0.996877996481 | 36 / 36 | PASS |
| ss_low_125 | 89.866670935 | 67.006659578 | 34.411335410 | 0.818327031759 | 36 / 36 | PASS |
| tt_nom_27 | 65.415524302 | 49.755692630 | 24.360297461 | 0.907419789847 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 404.738024185 fJ/cycle: 86.585263384 evaluation and 318.152760800 reset. The original meter gives 405.213707160 fJ/cycle; the waveform-integral difference is -0.117391%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `f484e3b196258aecfdfa34454478cb5ba73b773a6f8563cc9b4c3fe002e75f6d` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.


## Private precheck 20261031-123949-strongarm-reset-v28-notice94-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `dfc2832c1d7f090b07567b6fc6e26eca6db912ba`. These results use a private copy of the testbench and do not write formal records. All physical stimuli, loads, samplers and measurement code are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| sf_high_m40 | 73.117766966 | 54.704950365 | 19.683189667 | 0.996789224921 | 36 / 36 | PASS |
| ss_low_125 | 91.563479404 | 67.143122043 | 33.364877544 | 0.818330767507 | 36 / 36 | PASS |
| tt_nom_27 | 66.398976012 | 49.849673666 | 23.805388540 | 0.907280420320 | 36 / 36 | PASS |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 407.190387962 fJ/cycle: 88.923567373 evaluation and 318.266820589 reset. The original meter gives 407.223780480 fJ/cycle; the waveform-integral difference is -0.008200%. Both values are preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.839093693 ps, 30 mV delay +0.127524190 ps, reset -0.479200005 ps. Largest per-pair stress change is 370.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +1.696808468 ps, 30 mV delay +0.136462465 ps, reset -1.046457865 ps. Largest per-pair stress change is 590.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.983451710 ps, 30 mV delay +0.093981036 ps, reset -0.554908921 ps. Largest per-pair stress change is 370.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `40b24099b53e19956827a279a85cb61d416e27b42fee805ba8253efbb7bb9b5a` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.


## Private precheck 20261031-131451-strongarm-reset-v28-spec08-noise-baseline-screen

Test `tb_comp_noise`, accuracy `baseline`, frozen clean source `274a6dd469cbda33ea68538be2ab9bc1e1c46c21`. These results use a private copy of the testbench and do not write formal records. This is an independent experimental source using the merged official 0.8.0 testbench baseline, not a formal canonical-view result. All physical stimuli, loads, samplers and measurement code are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| tt_nom_27 | 206.449562493 | 198.24 to 215.06 | 0.006645089 | 8704 | FAIL: CMP-01 |

The full original 17 levels, 512 samples per level, 50 GHz bandwidth and seed 1 are preserved. Every sample is finite and none is omitted. The original outputstart=tstop waveform cannot establish reset history or full-trace terminal stress; those are separate checks. The noise interval is conditional on the Gaussian-CDF fit.

At tt_nom_27, minimum sampled output magnitude is 0.899743608 V and maximum absolute standardized Gaussian-fit residual is 3.587401. These residuals are diagnostic, not a proof that the physical distribution is Gaussian.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 2 |
| -400 | 12 |
| -300 | 37 |
| -200 | 85 |
| -100 | 135 |
| 0 | 290 |
| 100 | 341 |
| 200 | 408 |
| 300 | 473 |
| 400 | 497 |
| 500 | 506 |
| 600 | 512 |
| 700 | 512 |
| 800 | 512 |

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | None |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `54ff6269212616fd41dc09b383f106a78132651e58a2dbbb69c8717e6c296b92` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.

This electrical source fails the private experimental gate on the merged 0.8.0 baseline. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-135907-strongarm-reset-v29-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `9090cd1297a489aee0bac058ce5347d1a04c5115`. These results use a private copy of the testbench and do not write formal records. This is an independent experimental source using the merged official 0.8.0 testbench baseline, not a formal canonical-view result. All physical stimuli, loads, samplers and measurement code are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 59.099983046 | 44.691524101 | 20.609129130 | 0.995250119148 | 36 / 36 | PASS |
| sf_high_m40 | 76.083784011 | 55.900866579 | 19.306941259 | 0.996918138292 | 36 / 36 | PASS |
| ss_low_125 | 93.418906051 | 67.647388810 | 32.076531064 | 0.818252380280 | 36 / 36 | PASS |
| tt_nom_27 | 68.393376701 | 50.538410349 | 23.036918142 | 0.907368119469 | 36 / 36 | FAIL: CMP-06 |

Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

TT full AVDD waveform integral is 440.609095778 fJ/cycle: 114.220839307 evaluation and 326.388256470 reset. The original meter gives 441.179372520 fJ/cycle; the waveform-integral difference is -0.129262%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

The log's automatic maxstep bound is not an explicit job-deck setting. Actual APS thread information and the six-job session ceiling are recorded separately. Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `9a9b64993366a0709af81b7d359c4a98bfbf93052eb8240a1f9ab0ce221bd8f1` was checked by reading every member back with CRC and SHA-256. Full qualification remains open.

This electrical source fails the private experimental gate on the merged 0.8.0 baseline. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.
