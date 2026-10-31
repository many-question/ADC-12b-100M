# Numerical-settings transition: issue #94

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

## Merged workflow update, 2026-10-31

[PR #95](https://github.com/many-question/ADC-12b-100M/pull/95) merged at 12:44:34 into main as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`; adc_comp is now 0.8.0. The actual comparator testbench and specification patches match the precheck settings. The private runs below retain their original source and pre-merge status. Key evidence will be refreshed through the merged official runner and testbenches with the exact ADCToolbox commit `cd72061ff3b7a977163dac540da126ae22f5e38d`; no private result or old metadata is relabeled. A stale warning still means ineligible. Final merged per-test crosscheck rules apply where specified. New formal module notices are checked before subsequent batches.

The following transition plan records the earlier, unmerged checkpoint; it is superseded by the merged update above.

At the 2026-10-31 checkpoint, [issue #94](https://github.com/many-question/ADC-12b-100M/issues/94) is an unmerged announcement, with no comments or corresponding open workflow PR. Fetched main is `3b0c002a507b5f5fba1dfbc7059db5ef103e2860`. The existing deterministic screens, phase diagnostics and original formal records use the preceding settings. Their source hashes and measured results remain preserved; they do not establish compliance with the announced settings.

The next private checks use APS, `errpreset=conservative`, and no explicit `maxstep`. Ordinary transient logs are expected to show gear2only, reltol 1e-4, relref alllocal and lteratio 10. Kickback requires effective reltol 1e-6 and vabstol 10 nV. Requested and effective tolerances are recorded separately because conservative tightens reltol. The actual Spectre log determines whether the intended protocol ran. Prior sub-microvolt kickback numbers are historical numerical outputs, not established physical kickback.

RESET-V27 has 23 MOS and five MOM capacitors. Its ten known risk corners and targeted tighter runs passed under the old private settings; the tighter TT 30 mV delay was 49.838320 ps. This thin margin needs rechecking. No formal record yet matches V27: all 92 preserved records refer to earlier electrical sources. Promotion preserves electrical content and is not qualification.

Old-settings full-corner formal expansion is paused while circuit development continues. First priority is private critical-corner timing, all-cycle reset/output validity and whole-transient terminal stress, followed by kickback and noise checks. These private runs do not write formal records or alter shared testbenches, tools, specifications or thresholds.

After the flow merges, affected delay, kickback, noise and mismatch tests must be rerun through the merged official runner and testbenches on frozen actual sources. Rehash cannot restore old evidence. The announced ADCToolbox dependency is upstream commit `cd72061`, not the same-version PyPI 0.9.1 package. Merge status and formal module notices are checked before each batch and PR update; the announcement itself requests no acknowledgment. Qualification, remaining-corner coverage, operating-range checks, mixed-top regression and lead review remain open.


Shared reporting convention: the automatic maxstep bound in a log is not an explicit deck setting. Each archived run records actual APS threading and the six-job session ceiling. The compact wording below preserves every run heading, requested/effective setting, metric table, failure and archive hash. The [unabridged earlier wording](https://github.com/many-question/ADC-12b-100M/blob/3b7108921859eba3a1514cb5f91f2d42c94472bd/design/xtor/adc_comp/many-question-strongarm/NUMERICS-94.md) remains fixed in published history. Present raw availability is governed by EVIDENCE-RETENTION, including superseded archives that were released.

Shared repeated audit statements: each reference below applies the following complete statement to that specific run. Only repeated prose is consolidated; all original run headings, metric/numerics tables, failure rows and archive hashes remain.

**C1.** Every actual polarity down to 10 uV, all reset intervals, full evaluation output validity and every MOS gs/gd/ds pair are checked. The AVDD audit spans all 36 complete cycles; all supply probes are present and KCL closes. Reported power has no acceptance limit.

**C2.** The tiny values previously produced with old settings are not used as physical conclusions. This private value remains distinct from an official rerun and from further tolerance-convergence evidence.

**C3.** Load/stimulus conditions verified against the archived staged testbench: each input floats on 2.50 pF, initialized to common mode 0.49 V and differential 1 mV; each output has 10 fF. TT supply is 0.9 V, the clock period is 400 ps, and rise/fall times are 10 ps.

**C4.** The full original 17 levels, 512 samples per level, 50 GHz bandwidth and seed 1 are preserved. Every sample is finite and none is omitted. The original outputstart=tstop waveform cannot establish reset history or full-trace terminal stress; those are separate checks. The noise interval is conditional on the Gaussian-CDF fit.

**C5.** This electrical source fails the private experimental gate on the merged 0.8.0 baseline. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.

**C6.** Explicit output policy: `save=selected` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

## Private precheck 20261031-115725-strongarm-reset-v27-notice94-delay-announced-screen

Test `tb_comp_delay`, accuracy `announced`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.520043338 | 44.044297203 | 21.480771214 | 0.995404895798 | 36 / 36 | PASS |
| sf_high_m40 | 72.104932166 | 54.584095666 | 20.176357943 | 0.996806248659 | 36 / 36 | PASS |
| ss_low_125 | 89.881821460 | 67.032533726 | 34.083059100 | 0.816333032969 | 36 / 36 | PASS |
| tt_nom_27 | 65.381597902 | 49.727161527 | 24.077135846 | 0.906104108056 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 406.328839435 fJ/cycle: 86.844638589 evaluation and 319.484200846 reset. The original meter gives 406.821567240 fJ/cycle; the waveform-integral difference is -0.121116%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `709c4647e9ae4608dd04f2e74014101290032f4a7018554808d9be46dcd39375` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-120336-strongarm-reset-v27-notice94-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| sf_high_m40 | 73.005073352 | 54.717508029 | 19.700503312 | 0.996800000299 | 36 / 36 | PASS |
| ss_low_125 | 91.585393981 | 67.179651139 | 33.318872126 | 0.816328198383 | 36 / 36 | PASS |
| tt_nom_27 | 66.349849218 | 49.835069740 | 23.736431481 | 0.906090197265 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 408.778397819 fJ/cycle: 89.170539589 evaluation and 319.607858229 reset. The original meter gives 408.812747040 fJ/cycle; the waveform-integral difference is -0.008402%. Both values are preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.900141187 ps, 30 mV delay +0.133412363 ps, reset -0.475854631 ps. Largest per-pair stress change is 210.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +1.703572521 ps, 30 mV delay +0.147117412 ps, reset -0.764186974 ps. Largest per-pair stress change is 570.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.968251317 ps, 30 mV delay +0.107908212 ps, reset -0.340704365 ps. Largest per-pair stress change is 230.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `a0ee84791027375a03ad3e0f1a33f66e58c2e2b1f4a3bad6c27a91b99ce2fc83` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-120357-strongarm-reset-v27-notice94-kickback-announced-screen

Test `tb_comp_kickback`, accuracy `announced`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118543 | 15.782208772 | 0.000050251 | PASS |

Common audit statement C2 applies to this run.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 354.571903 uV instantaneous differential change and 7.405379 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Common audit statement C3 applies to this run.

Unrounded recorded values: net per-cycle metric `5.025120011943607e-05` uV; instantaneous differential peak magnitude `354.57190254149543` uV (signed change `0.00035457190254149546` V), cycle 8, `66.96310955267225` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99997500000055` ps. Maximum common-mode excursion is `7.405379196107786` mV, in evaluation at `198.20486963065588` ps after its cycle-1 sample.

The supplemental phase/load context was derived from the SHA-verified archive without rewriting it; context-file SHA-256 is `cd50e6b191698acbc704578b46892cacd9193ec6073073c3372a858df228b25b`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 33.0 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `d41c26241ccccdf79ce60560e804c431b7e6ea9280cccf0366a875c2856773ed` passed every-member CRC/SHA readback. Full qualification remains open.

The later phase/load supplement is also preserved in a separate verified archive, SHA-256 `d644c7aaa33e654444ec8aff293aa78f07e9a7db885e3d80ca1f53c6f6a91288`; the original run archive remains unchanged.


## Private precheck 20261031-121037-strongarm-reset-v27-notice94-kickback-tighter-screen

Test `tb_comp_kickback`, accuracy `tighter`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-6", "vabstol": "1e-9"}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118543 | 15.782118507 | 0.000037492 | PASS |

Common audit statement C2 applies to this run.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 354.618788 uV instantaneous differential change and 7.405457 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

| Quantity | Announced precision | Tighter precision | Difference |
|---|---:|---:|---:|
| kickback_uV | 5.02512001194e-05 | 3.74916001022e-05 | -1.27596000172e-05 |
| cin_fF | 19.3311185429 | 19.3311185429 | +0 |
| cin_clkc_fF | 15.7822087719 | 15.7821185072 | -9.02646988621e-05 |
| max_instantaneous_differential_change_uV | 354.571902541 | 354.618787923 | +0.0468853815375 |
| max_instantaneous_common_mode_change_mV | 7.40537919611 | 7.40545699018 | +7.77940705188e-05 |

Common audit statement C3 applies to this run.

Unrounded recorded values: net per-cycle metric `3.749160010224628e-05` uV; instantaneous differential peak magnitude `354.6187879230329` uV (signed change `0.00035461878792303293` V), cycle 2, `67.06524039163574` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99999749999998` ps. Maximum common-mode excursion is `7.405456990178305` mV, in evaluation at `198.18385786003088` ps after its cycle-1 sample.

The supplemental phase/load context was derived from the SHA-verified archive without rewriting it; context-file SHA-256 is `1d48415a5754a3088a1b125b3c37820c03a074d10327be0a9dde55b1df8682ba`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-07 | 1e-09 | gear2only / conservative / alllocal / 10 | 27.4104 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `acf992e2f6b53a93232ab9b9c5dd0418c61c4bf4c7641151943423a6abd0cd89` passed every-member CRC/SHA readback. Full qualification remains open.

The later phase/load supplement is also preserved in a separate verified archive, SHA-256 `d644c7aaa33e654444ec8aff293aa78f07e9a7db885e3d80ca1f53c6f6a91288`; the original run archive remains unchanged.


## Private precheck 20261031-121026-strongarm-reset-v27-notice94-noise-announced-screen

Test `tb_comp_noise`, accuracy `announced`, frozen clean source `f727f91aa5b0acaf3ced8a962aae3a6a56237d73`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| tt_nom_27 | 210.100860925 | 201.81 to 218.79 | 0.005125216 | 8704 | FAIL: CMP-01 |

Common audit statement C4 applies to this run.

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

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `94ace46b19d543b73f691f45523fbfe9ed28bec34660fe3350ca9929c5c800e3` passed every-member CRC/SHA readback. Full qualification remains open.

This electrical source fails the private proposed-settings gate. Qualification expansion stops at the failure; diagnosis and further circuit design continue. Every failure is retained.


## Private precheck 20261031-123312-strongarm-reset-v28-notice94-delay-announced-screen

Test `tb_comp_delay`, accuracy `announced`, frozen clean source `dfc2832c1d7f090b07567b6fc6e26eca6db912ba`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.582803438 | 44.075924180 | 21.495257778 | 0.995305503669 | 36 / 36 | PASS |
| sf_high_m40 | 72.278673274 | 54.577426176 | 20.162389672 | 0.996877996481 | 36 / 36 | PASS |
| ss_low_125 | 89.866670935 | 67.006659578 | 34.411335410 | 0.818327031759 | 36 / 36 | PASS |
| tt_nom_27 | 65.415524302 | 49.755692630 | 24.360297461 | 0.907419789847 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 404.738024185 fJ/cycle: 86.585263384 evaluation and 318.152760800 reset. The original meter gives 405.213707160 fJ/cycle; the waveform-integral difference is -0.117391%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `f484e3b196258aecfdfa34454478cb5ba73b773a6f8563cc9b4c3fe002e75f6d` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-123949-strongarm-reset-v28-notice94-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `dfc2832c1d7f090b07567b6fc6e26eca6db912ba`. Private testbench; no formal writes. Physical stimuli, loads, samplers and measurements are preserved. The requested settings are `{"errpreset": "conservative", "reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| sf_high_m40 | 73.117766966 | 54.704950365 | 19.683189667 | 0.996789224921 | 36 / 36 | PASS |
| ss_low_125 | 91.563479404 | 67.143122043 | 33.364877544 | 0.818330767507 | 36 / 36 | PASS |
| tt_nom_27 | 66.398976012 | 49.849673666 | 23.805388540 | 0.907280420320 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 407.190387962 fJ/cycle: 88.923567373 evaluation and 318.266820589 reset. The original meter gives 407.223780480 fJ/cycle; the waveform-integral difference is -0.008200%. Both values are preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.839093693 ps, 30 mV delay +0.127524190 ps, reset -0.479200005 ps. Largest per-pair stress change is 370.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +1.696808468 ps, 30 mV delay +0.136462465 ps, reset -1.046457865 ps. Largest per-pair stress change is 590.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.983451710 ps, 30 mV delay +0.093981036 ps, reset -0.554908921 ps. Largest per-pair stress change is 370.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `40b24099b53e19956827a279a85cb61d416e27b42fee805ba8253efbb7bb9b5a` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-131451-strongarm-reset-v28-spec08-noise-baseline-screen

Test `tb_comp_noise`, accuracy `baseline`, frozen clean source `274a6dd469cbda33ea68538be2ab9bc1e1c46c21`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| tt_nom_27 | 206.449562493 | 198.24 to 215.06 | 0.006645089 | 8704 | FAIL: CMP-01 |

Common audit statement C4 applies to this run.

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

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `54ff6269212616fd41dc09b383f106a78132651e58a2dbbb69c8717e6c296b92` passed every-member CRC/SHA readback. Full qualification remains open.

Common audit statement C5 applies to this run.


## Private precheck 20261031-135907-strongarm-reset-v29-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `9090cd1297a489aee0bac058ce5347d1a04c5115`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 59.099983046 | 44.691524101 | 20.609129130 | 0.995250119148 | 36 / 36 | PASS |
| sf_high_m40 | 76.083784011 | 55.900866579 | 19.306941259 | 0.996918138292 | 36 / 36 | PASS |
| ss_low_125 | 93.418906051 | 67.647388810 | 32.076531064 | 0.818252380280 | 36 / 36 | PASS |
| tt_nom_27 | 68.393376701 | 50.538410349 | 23.036918142 | 0.907368119469 | 36 / 36 | FAIL: CMP-06 |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 440.609095778 fJ/cycle: 114.220839307 evaluation and 326.388256470 reset. The original meter gives 441.179372520 fJ/cycle; the waveform-integral difference is -0.129262%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `9a9b64993366a0709af81b7d359c4a98bfbf93052eb8240a1f9ab0ce221bd8f1` passed every-member CRC/SHA readback. Full qualification remains open.

Common audit statement C5 applies to this run.


## Private precheck 20261031-141113-strongarm-reset-v30-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `750a09c5e82ed0febef9a66e29081d76f4719fbe`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 55.751314309 | 41.911261475 | 22.770878143 | 0.995129570219 | 36 / 36 | PASS |
| sf_high_m40 | 71.518875218 | 52.714657529 | 21.284408768 | 0.996882849297 | 36 / 36 | PASS |
| ss_low_125 | 87.777671376 | 63.269679667 | 36.646221658 | 0.818330456270 | 36 / 36 | FAIL: CMP-08 |
| tt_nom_27 | 64.285197900 | 47.355144908 | 26.072820144 | 0.907418434478 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 424.265963860 fJ/cycle: 102.839857634 evaluation and 321.426106225 reset. The original meter gives 424.747399680 fJ/cycle; the waveform-integral difference is -0.113346%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `411d569d438bf1ed3242e65420057a2140c6c8f276887753170fa8bba1cc03b4` passed every-member CRC/SHA readback. Full qualification remains open.

Common audit statement C5 applies to this run.


## Private precheck 20261031-142506-strongarm-reset-v31-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `59d298a829e2b07341286e3d0868895aa9fc93df`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.055124193 | 42.017541798 | 21.103877139 | 0.995483622192 | 36 / 36 | PASS |
| sf_high_m40 | 71.956622663 | 52.774828836 | 20.045380303 | 0.996888383755 | 36 / 36 | PASS |
| ss_low_125 | 88.018791693 | 63.339930406 | 33.332992243 | 0.818405250327 | 36 / 36 | PASS |
| tt_nom_27 | 64.584263262 | 47.473880684 | 23.930863640 | 0.907400190464 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 424.817112136 fJ/cycle: 102.794418350 evaluation and 322.022693787 reset. The original meter gives 425.326360680 fJ/cycle; the waveform-integral difference is -0.119731%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `16675cf85040eef16b2f1408798ec477e25d271b376798f0cc202b1f35485e36` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-142603-strongarm-reset-v31-spec08-kickback-baseline-screen

Test `tb_comp_kickback`, accuracy `baseline`, frozen clean source `59d298a829e2b07341286e3d0868895aa9fc93df`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Baseline accuracy appends only saved probes; any tighter tolerances are explicitly listed. The requested settings are `{}`; no explicit maxstep or method is set.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118543 | 16.652324157 | 0.000061514 | FAIL: CMP-14 |

Common audit statement C2 applies to this run.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 364.658016 uV instantaneous differential change and 7.403152 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Common audit statement C3 applies to this run.

Unrounded recorded values: net per-cycle metric `6.151410002035174e-05` uV; instantaneous differential peak magnitude `364.65801587939734` uV (signed change `0.0003646580158793973` V), cycle 8, `70.21352053439826` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99997500000055` ps. Maximum common-mode excursion is `7.403152283855963` mV, in evaluation at `198.2363112925205` ps after its cycle-1 sample.

The phase/load context was derived from SHA-verified raw evidence without modifying the traces; context-file SHA-256 is `3008ddaa61dd342d85665a98289670af6eb655c8255873d9b337c26880b21cf0`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 33.0 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `de2075791bc9a9be8109c4cb4db32f66c4f9c90fc6a3779ea0e10a1d04b9bd0e` passed every-member CRC/SHA readback. Full qualification remains open.

The complete phase/load context is included in this run's verified archive.

Common audit statement C5 applies to this run.


## Private precheck 20261031-150826-strongarm-reset-v32-spec08-delay-baseline-screen

Test `tb_comp_delay`, accuracy `baseline`, frozen clean source `d283d2014a3bad62f98f98bc03603f0199c11a55`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Common audit statement C6 applies to this run.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.041570238 | 42.005244400 | 20.961647044 | 0.995466853153 | 36 / 36 | PASS |
| sf_high_m40 | 71.841790991 | 52.779690705 | 19.931921873 | 0.996905493020 | 36 / 36 | PASS |
| ss_low_125 | 88.018324387 | 63.343722647 | 33.472284067 | 0.817609123230 | 36 / 36 | PASS |
| tt_nom_27 | 64.552216870 | 47.455204527 | 23.908415648 | 0.905975996674 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 423.715629138 fJ/cycle: 102.791056661 evaluation and 320.924572477 reset. The original meter gives 424.199206800 fJ/cycle; the waveform-integral difference is -0.113998%. Both values are preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `23ee62d872be40a886206f848c96f2c53e80a9a728ff60bdfabd9b33daafef6c` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-150826-strongarm-reset-v32-spec08-kickback-baseline-screen

Test `tb_comp_kickback`, accuracy `baseline`, frozen clean source `d283d2014a3bad62f98f98bc03603f0199c11a55`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Common audit statement C6 applies to this run.

| Corner | Input fF | CLKC fF | Kickback uV | Private gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118543 | 15.563277108 | 0.000059501 | PASS |

Common audit statement C2 applies to this run.

A separate full-input-trace diagnostic at tt_nom_27 finds up to 364.462595 uV instantaneous differential change and 7.403170 mV common-mode change relative to that cycle's pre-evaluation sample. These are distinct from the specified net per-cycle kickback metric and are not judged against its 40 uV limit. A nearly zero per-cycle value does not imply an undisturbed input during evaluation and reset.

Common audit statement C3 applies to this run.

Unrounded recorded values: net per-cycle metric `5.950139990093528e-05` uV; instantaneous differential peak magnitude `364.4625954699607` uV (signed change `0.00036446259546996074` V), cycle 2, `70.17635571444133` ps after its pre-evaluation sample. The peak is in **evaluation**, whose measured window runs from that sample to `199.99997499999992` ps. Maximum common-mode excursion is `7.403170004551985` mV, in evaluation at `198.229137663919` ps after its cycle-1 sample.

The phase/load context was derived from SHA-verified raw evidence without modifying the traces; context-file SHA-256 is `6bf38391bcbaca7774468f836d10d85b3f6fd521566b5de474adb000684ad8e7`. The specified metric concerns net change after evaluation plus reset; these instantaneous peaks describe disturbance during that interval. Future validation with the actual CDAC must check decision-phase differential and common-mode effects. No shared rule or limit changes.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 33.0 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `119356f766a5c8d477f1f64477319260ee36483383bd69ca869c7bebccae5d56` passed every-member CRC/SHA readback. Full qualification remains open.

The complete phase/load context is included in this run's verified archive.


## Private precheck 20261031-151652-strongarm-reset-v32-spec08-delay-tighter-screen

Test `tb_comp_delay`, accuracy `tighter`, frozen clean source `d283d2014a3bad62f98f98bc03603f0199c11a55`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{"reltol": "1e-5", "vabstol": "1e-8"}`; no explicit maxstep or method is set.

Common audit statement C6 applies to this run.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Raw max stress V | Actual / reset cycles | Private gate |
|---|---:|---:|---:|---:|---:|---|
| fs_high_m40 | 56.733366371 | 42.057941595 | 20.903248500 | 0.995472779817 | 36 / 36 | PASS |
| sf_high_m40 | 72.656321131 | 52.895502633 | 19.446476506 | 0.996897019932 | 36 / 36 | PASS |
| ss_low_125 | 89.534940753 | 63.487463121 | 32.868603675 | 0.817505725550 | 36 / 36 | PASS |
| tt_nom_27 | 65.450169078 | 47.552992813 | 23.506670414 | 0.905873326049 | 36 / 36 | PASS |

Common audit statement C1 applies to this run.

TT full AVDD waveform integral is 426.788018970 fJ/cycle: 105.798579821 evaluation and 320.989439149 reset. The original meter gives 426.823903440 fJ/cycle; the waveform-integral difference is -0.008407%. Both values are preserved.

Same-source tighter-minus-announced comparison at fs_high_m40: 1 mV delay +0.691796133 ps, 30 mV delay +0.052697195 ps, reset -0.058398544 ps. Largest per-pair stress change is 460.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at sf_high_m40: 1 mV delay +0.814530140 ps, 30 mV delay +0.115811928 ps, reset -0.485445368 ps. Largest per-pair stress change is 420.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at ss_low_125: 1 mV delay +1.516616365 ps, 30 mV delay +0.143740474 ps, reset -0.603680392 ps. Largest per-pair stress change is 590.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

Same-source tighter-minus-announced comparison at tt_nom_27: 1 mV delay +0.897952208 ps, 30 mV delay +0.097788285 ps, reset -0.401745234 ps. Largest per-pair stress change is 260.000 uV at the table's 10 uV resolution; all unrounded peaks are separately preserved.

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| fs_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| sf_high_m40 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| ss_low_125 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 | 56.5 |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `4bff292951732887e803079a71fd3dfb81ef1ce1fc3a8bb64c98865579695f34` passed every-member CRC/SHA readback. Full qualification remains open.


## Private precheck 20261031-151715-strongarm-reset-v32-spec08-noise-baseline-screen

Test `tb_comp_noise`, accuracy `baseline`, frozen clean source `d283d2014a3bad62f98f98bc03603f0199c11a55`. Private testbench; no formal writes. Independent source on the merged 0.8.0 baseline; not a canonical result. Physical stimuli, loads, samplers and measurements are preserved. Output selections and any tighter tolerances are recorded separately. The requested numerical settings are `{}`; no explicit maxstep or method is set.

Explicit output policy: `save=none` with named DUT/SOA voltage signals and required metric/current probes, or the preserved monitor-only noise protocol. No global or wildcard expansion is used. The exact selected signal lists, policy source and before/after testbench hashes are retained with this run; earlier runs are not relabeled with this policy.

| Corner | Noise uV rms | 95% profile interval uV | Offset mV | Samples | Private gate |
|---|---:|---|---:|---:|---|
| tt_nom_27 | 194.233252094 | 186.32 to 202.54 | 0.009772338 | 8704 | PASS |

Common audit statement C4 applies to this run.

At tt_nom_27, minimum sampled output magnitude is 0.899771677 V and maximum absolute standardized Gaussian-fit residual is 4.004778. These residuals are diagnostic, not a proof that the physical distribution is Gaussian.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 2 |
| -400 | 15 |
| -300 | 25 |
| -200 | 69 |
| -100 | 113 |
| 0 | 291 |
| 100 | 349 |
| 200 | 420 |
| 300 | 477 |
| 400 | 498 |
| 500 | 509 |
| 600 | 512 |
| 700 | 512 |
| 800 | 512 |

| Corner | Effective reltol | Effective vabstol V | Method / preset / relref / lteratio | Largest saved step ps |
|---|---:|---:|---|---:|
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 | None |

Fetched raw/deck hashes match; the exact owned remote run is absent. Archive SHA-256 `62d74c2b9aef0cd0b6cc1808caeab81d0cfb551390bb10bdd1917177aee24988` passed every-member CRC/SHA readback. Full qualification remains open.

## Private precheck 20261031-153022-strongarm-reset-v32-spec08-delay-baseline-screen

Private `tb_comp_delay`, `baseline`, clean frozen commit `3b7108921859eba3a1514cb5f91f2d42c94472bd`; electrical SHA-256 `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`. Merged 0.8.0 stimuli, loads, measurements and limits are preserved. Explicit output-only selected saves or the original monitor-only save=none apply; no wildcards, explicit maxstep or method override. No formal records or canonical source change.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Unrounded stress V | Gate |
|---|---:|---:|---:|---:|---|
| ff_high_125 | 47.27746346337113 | 33.98350812544957 | 21.442855882313317 | 0.99 | PASS |
| ff_high_m40 | 47.26479508138647 | 35.29652233301355 | 18.30010634016058 | 0.9943467576631665 | PASS |
| ff_low_125 | 55.37111701006521 | 39.45701042213123 | 25.054309002785846 | 0.813409865387113 | PASS |
| fs_low_125 | 65.16977215217723 | 47.393873574281734 | 30.126708251658034 | 0.8120452388053727 | PASS |
| sf_low_125 | 74.78037133471436 | 53.408952279107815 | 27.411163033048492 | 0.8169081217081842 | PASS |

All 180 actual decisions (including 10 uV) and 180 reset intervals are retained; [69] full-trace MOS gs/gd/ds pairs per corner, output validity and full-cycle AVDD KCL are independently checked. Complete per-cycle/path and terminal-pair data remain in the archive. Energy is report-only.

| Corner | Actual reltol | vabstol V | Method / preset / relref / lteratio |
|---|---:|---:|---|
| ff_high_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| ff_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| ff_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| sf_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |

Archive SHA-256 `36976bd7ac9f7e3cb626bb470b288578e35202692865f81dd7f4ce0cef264e31`: every member passed CRC/SHA readback. Fetched files match remote hashes, the exact owned remote directory is absent, and the six-job session ceiling is retained. Raw availability is indexed in [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md). Full qualification remains open.

## Private precheck 20261031-153036-strongarm-reset-v32-spec08-noise-tighter-screen

Private `tb_comp_noise`, `tighter`, clean frozen commit `3b7108921859eba3a1514cb5f91f2d42c94472bd`; electrical SHA-256 `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`. Merged 0.8.0 stimuli, loads, measurements and limits are preserved. Explicit output-only selected saves or the original monitor-only save=none apply; no wildcards, explicit maxstep or method override. No formal records or canonical source change.

| Corner | Noise uV rms | 95% profile interval uV | Abs offset mV | Gate |
|---|---:|---|---:|---|
| tt_nom_27 | 196.19021968049825 | [188.25, 204.52] | 0.010228299140700985 | PASS |

Each corner retains every finite decision from the original 17 levels x 512 samples, 50 GHz bandwidth and seed 1, with all physical noise sources enabled. All level counts and Gaussian-fit residuals are archived. Profile intervals are conditional on that fit; point-estimate passage does not establish robust margin. Monitor-only output cannot establish full reset history or full-trace SOA.

tt_nom_27: minimum sampled output magnitude 0.89978091365 V; maximum absolute standardized fit residual 4.214829068093892 (diagnostic only).

Matched precision comparison: baseline 194.23325209435865 uV, tighter 196.19021968049825 uV, difference 1.9569675861395979 uV; 10 of 17 level counts change. Only reltol/vabstol differ in the tested bench. Adaptive steps can change stochastic sequences despite the same seed; this is not proof of a statistically resolved difference or a new convergence tolerance.

| Corner | Actual reltol | vabstol V | Method / preset / relref / lteratio |
|---|---:|---:|---|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 |

Archive SHA-256 `68b379d689a8eb810ffcb1341375a60afc3bbae44ea761e9f9130cb58a89fe1c`: every member passed CRC/SHA readback. Fetched files match remote hashes, the exact owned remote directory is absent, and the six-job session ceiling is retained. Raw availability is indexed in [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md). Full qualification remains open.

## Private precheck 20261031-153652-strongarm-reset-v32-spec08-noise-baseline-screen

Private `tb_comp_noise`, `baseline`, clean frozen commit `3b7108921859eba3a1514cb5f91f2d42c94472bd`; electrical SHA-256 `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`. Merged 0.8.0 stimuli, loads, measurements and limits are preserved. Explicit output-only selected saves or the original monitor-only save=none apply; no wildcards, explicit maxstep or method override. No formal records or canonical source change.

| Corner | Noise uV rms | 95% profile interval uV | Abs offset mV | Gate |
|---|---:|---|---:|---|
| fs_low_125 | 371.83932552901155 | [359.5, 384.82] | 0.001885833969101262 | FAIL CMP-13 |
| ss_low_125 | 299.6542222063326 | [289.43, 310.36] | 0.011372399257592595 | FAIL CMP-13 |

Each corner retains every finite decision from the original 17 levels x 512 samples, 50 GHz bandwidth and seed 1, with all physical noise sources enabled. All level counts and Gaussian-fit residuals are archived. Profile intervals are conditional on that fit; point-estimate passage does not establish robust margin. Monitor-only output cannot establish full reset history or full-trace SOA.

fs_low_125: minimum sampled output magnitude 0.8072275291529 V; maximum absolute standardized fit residual 3.4992740803871762 (diagnostic only).

ss_low_125: minimum sampled output magnitude 0.8083717114481 V; maximum absolute standardized fit residual 3.4266282039718137 (diagnostic only).

| Corner | Actual reltol | vabstol V | Method / preset / relref / lteratio |
|---|---:|---:|---|
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |

Archive SHA-256 `b6aca8e051c7a481eb59604c06c987bc6518d64c090e0ac73ddfcfbe9dad91e0`: every member passed CRC/SHA readback. Fetched files match remote hashes, the exact owned remote directory is absent, and the six-job session ceiling is retained. Raw availability is indexed in [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md). Full qualification remains open.

**This physical source fails the private gate.** Qualification expansion stops at the failure; diagnosis and circuit design continue. No failed point is discarded.

## Private precheck 20261031-162854-strongarm-reset-v33-spec08-delay-baseline-screen

Private `tb_comp_delay`, `baseline`, clean frozen commit `15fa827572d71887fd3b3d7abf05be81cdf64900`; electrical SHA-256 `e859347340abfbe7f5e42e0a9c3a831f378bce9bea727177b4e214ef60a1b0cf`. Merged 0.8.0 stimuli, loads, measurements and limits are preserved. Explicit output-only selected saves or the original monitor-only save=none apply; no wildcards, explicit maxstep or method override. No formal records or canonical source change.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Unrounded stress V | Gate |
|---|---:|---:|---:|---:|---|
| fs_high_m40 | 58.34821931809706 | 43.025580844881745 | 19.886606866434303 | 0.9962216274226721 | PASS |
| fs_low_125 | 71.50480536061406 | 51.24481920934392 | 27.297439709688422 | 0.8124081955670862 | PASS |
| sf_high_m40 | 73.84963705288624 | 54.127289955425816 | 18.700291247345966 | 0.9975641708765174 | PASS |
| ss_low_125 | 96.1574321689984 | 68.31035257475426 | 30.94352557878534 | 0.8176100499995239 | PASS |
| tt_nom_27 | 68.32301083919458 | 49.433499354741386 | 22.469322350940356 | 0.9061405186680825 | PASS |

All 180 actual decisions (including 10 uV) and 180 reset intervals are retained; [69] full-trace MOS gs/gd/ds pairs per corner, output validity and full-cycle AVDD KCL are independently checked. Complete per-cycle/path and terminal-pair data remain in the archive. Energy is report-only.

TT energy: meter 418.99250844000005 fJ/cycle; independent integral 418.5560781300873, evaluation 99.60640215064876, reset 318.94967597943855 fJ/cycle. All named supply probes are present and KCL closes.

| Corner | Actual reltol | vabstol V | Method / preset / relref / lteratio |
|---|---:|---:|---|
| fs_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| fs_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| sf_high_m40 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| ss_low_125 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |
| tt_nom_27 | 0.0001 | 1e-06 | gear2only / conservative / alllocal / 10 |

Archive SHA-256 `f6841cb22529eb80b7aa356500442964175076e59ef893b3416d3586ad6608f3`: every member passed CRC/SHA readback. Fetched files match remote hashes, the exact owned remote directory is absent, and the six-job session ceiling is retained. Raw availability is indexed in [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md). Full qualification remains open.

## Private precheck 20261031-162854-strongarm-reset-v33-spec08-kickback-baseline-screen

Private `tb_comp_kickback`, `baseline`, clean frozen commit `15fa827572d71887fd3b3d7abf05be81cdf64900`; electrical SHA-256 `e859347340abfbe7f5e42e0a9c3a831f378bce9bea727177b4e214ef60a1b0cf`. Merged 0.8.0 stimuli, loads, measurements and limits are preserved. Explicit output-only selected saves or the original monitor-only save=none apply; no wildcards, explicit maxstep or method override. No formal records or canonical source change.

| Corner | Input fF | CLKC fF | Net per-cycle kickback uV | Gate |
|---|---:|---:|---:|---|
| tt_nom_27 | 19.331118542884703 | 15.570038425100613 | 3.715300007749167e-05 | PASS |

Verified conditions: 0.9 V supply, 0.49 V initial CM, 1 mV initial differential, 2.5 pF floating capacitance per input, 10 fF per output, 400 ps clock with 10 ps edges.

Distinct instantaneous peaks: differential magnitude 325.0966563028508 uV, signed change 0.0003250966563028508 V, cycle 3, 216.25520001149206 ps after its pre-evaluation sample in reset; common-mode magnitude 7.409436530136704 mV, cycle 1, 198.1990725400085 ps in evaluation.

CMP-11 measures net change after evaluation plus reset. These instantaneous peaks are not compared to its 40 uV limit; a tiny net residual does not mean an undisturbed input. Actual-CDAC decision-phase differential/common-mode validation remains open.

The full raw-derived phase/load context is included in the verified archive; its SHA-256 is `2e228e344fb6aadc5f5c8784e4ee105680e3279d8a3df0f392f0efb4f15d7e9c`.

| Corner | Actual reltol | vabstol V | Method / preset / relref / lteratio |
|---|---:|---:|---|
| tt_nom_27 | 1e-06 | 1e-08 | gear2only / conservative / alllocal / 10 |

Archive SHA-256 `5eeb930f26b032d56e04e497a6991757048d537366b8b6776b6d12bb178a1124`: every member passed CRC/SHA readback. Fetched files match remote hashes, the exact owned remote directory is absent, and the six-job session ceiling is retained. Raw availability is indexed in [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md). Full qualification remains open.

## Private precheck 20261031-163620-strongarm-reset-v33-spec08-delay-tighter-screen

Private `tb_comp_delay` / `tighter`; clean frozen source `7f50c0a41ca222f1c6885eb5eb8b3d02f639524e`, electrical SHA-256 `e859347340abfbe7f5e42e0a9c3a831f378bce9bea727177b4e214ef60a1b0cf`. Merged 0.8.0 physical stimuli/loads, measurements and limits are preserved; named selected or original monitor-only saves, no wildcards. No formal writes or canonical change.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Unrounded stress V | Gate |
|---|---:|---:|---:|---:|---|
| fs_high_m40 | 59.09184111214865 | 43.09257999401472 | 19.65999981832592 | 0.9962239923785982 | PASS |
| fs_low_125 | 72.92185339667094 | 51.36032817109835 | 27.158465592390176 | 0.8122309401200808 | PASS |
| sf_high_m40 | 74.70111153472892 | 54.24797438397259 | 18.12030242619273 | 0.9975848355205003 | PASS |
| ss_low_125 | 97.95372399624229 | 68.51077582019597 | 30.09058932978041 | 0.8175045478374987 | PASS |
| tt_nom_27 | 69.26059763072612 | 49.54324517079809 | 21.777180303898454 | 0.9061428281142265 | PASS |

All 180 actual decisions (including 10 uV) and 180 reset intervals are retained; [69] full-trace MOS gs/gd/ds pairs per corner, output validity and full-cycle AVDD KCL are independently checked. Complete per-cycle/path and terminal-pair data remain in the archive. Energy is report-only.

TT energy: meter 421.41099276000006 fJ/cycle; independent integral 421.378144182793, evaluation 102.34928290663143, reset 319.0288612761616 fJ/cycle. All named supply probes are present and KCL closes.

| Tighter minus same-source baseline | 1 mV ps | 30 mV ps | Reset ps |
|---|---:|---:|---:|
| fs_high_m40 | +0.743621794 | +0.066999149 | -0.226607048 |
| fs_low_125 | +1.417048036 | +0.115508962 | -0.138974117 |
| sf_high_m40 | +0.851474482 | +0.120684429 | -0.579988821 |
| ss_low_125 | +1.796291827 | +0.200423245 | -0.852936249 |
| tt_nom_27 | +0.937586792 | +0.109745816 | -0.692142047 |

The archive retains all per-pair comparisons and unrounded stress peaks; rounded comparison-table precision does not replace strict SOA checks.

Actual settings (fs_high_m40, fs_low_125, sf_high_m40, ss_low_125, tt_nom_27): reltol 1e-06, vabstol 1e-08 V, gear2only/conservative/alllocal, lteratio 10; no explicit maxstep or method override.

Verified ZIP SHA-256 `a90c8bd026911efdf2cc93b2d26443f2b106b31cbc22ba34d5449eb55116553a`; every member passed CRC/SHA readback, retrieval/final-source guards and exact remote absence passed; session ceiling six jobs. [Retention](EVIDENCE-RETENTION.md) governs raw availability. Full qualification remains open.

## Private precheck 20261031-164248-strongarm-reset-v33-spec08-noise-baseline-screen

Private `tb_comp_noise` / `baseline`; clean frozen source `7f50c0a41ca222f1c6885eb5eb8b3d02f639524e`, electrical SHA-256 `e859347340abfbe7f5e42e0a9c3a831f378bce9bea727177b4e214ef60a1b0cf`. Merged 0.8.0 physical stimuli/loads, measurements and limits are preserved; named selected or original monitor-only saves, no wildcards. No formal writes or canonical change.

| Corner | Noise uV rms | 95% profile interval uV | Abs offset mV | Gate |
|---|---:|---|---:|---|
| fs_low_125 | 483.2613219887676 | [466.39, 501.2] | 0.006339582663946007 | FAIL CMP-13 |

Each corner retains every finite decision from the original 17 levels x 512 samples, 50 GHz bandwidth and seed 1, with all physical noise sources enabled. All level counts and Gaussian-fit residuals are archived. Profile intervals are conditional on that fit; point-estimate passage does not establish robust margin. Monitor-only output cannot establish full reset history or full-trace SOA.

fs_low_125: minimum sampled output magnitude 0.8077121304859 V; maximum absolute standardized fit residual 2.5636001085200824 (diagnostic only).

Actual settings (fs_low_125): reltol 0.0001, vabstol 1e-06 V, gear2only/conservative/alllocal, lteratio 10; no explicit maxstep or method override.

Verified ZIP SHA-256 `922ca2521ff7295a2352c9fbcb6244b96e60f297aa5854fe6b7b8b8da4f05539`; every member passed CRC/SHA readback, retrieval/final-source guards and exact remote absence passed; session ceiling six jobs. [Retention](EVIDENCE-RETENTION.md) governs raw availability. Full qualification remains open.

**This physical source fails the private gate.** Qualification expansion stops at the failure; diagnosis and circuit design continue. No failed point is discarded.
