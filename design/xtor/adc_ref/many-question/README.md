# adc_ref candidate: many-question

Status: **wip**. Author: **Codex adc_ref (@many-question)**.

This candidate uses a native thick-oxide source follower with a 1:16 scaled
replica servo, a reference-absent startup clamp, and a MOS divider for VCM.
The v8 compensation uses `CGATE multi=8`, with `MPUV multi=2`,
`MPOUT multi=16`, and six MOM-unit equivalents of servo compensation (4+1+1).
Its tradeoff is substantial
quiescent power and gate capacitance for settling robustness. It is not selected
or signed off; the archived mixed-top SS-hot ENOB result remains a failure.

## Module evidence

The candidate retains 136 original result JSONs and 136 original figures:
45 DC, 45 startup, 45 reference replay, and one TT noise result. All applicable
module limits pass with full required corner coverage against current main
`17205ec66d7265da5bf1e4a603ea514f34e99c09` (adc_ref spec 0.6.0).
These are self-reported results, not project-lead verification.

| Measurement | Recorded result |
|---|---:|
| Worst absolute VREFP DC error | 1.97724253 mV |
| VCM DC range | 0.44898278 to 0.44973694 V |
| Worst line regulation | 0.44162944 mV/V |
| Worst load regulation | 2.46118869 mV |
| TT / maximum DC supply power | 28.10870 / 47.76554 mW |
| TT VREFP noise, 10 kHz to 100 GHz | 76.11196 uV rms |
| Maximum startup VREFP / VCM | 0.95606908 / 0.47803299 V |
| Worst ready-time error | 1.02240612 mV |
| Maximum replay ENOB loss | 0.06730221 bit |
| Maximum replay tail / start error | 144.28187 / 66.23732 uV |

The DC evidence already uses the corrected 1.62, 1.71, 1.80, 1.89, 1.98 V
sweep from [#46](https://github.com/many-question/ADC-12b-100M/issues/46).
Startup uses the supported supply/reference sequence with static clock,
1.2 pF VREFP and 5 pF VCM loads. Four official startup cross-checks are retained
in their result metadata; their largest peak difference is 15.93610 uV and
largest ready-error difference is 0.00797382 mV.

Replay uses N=1024 after 32 warmup conversions, 100 MS/s and
49.70703125 MHz (k=509), with no extra DC load. The 15,840 decision samples per
corner are contiguous. The recorded worst envelope ratio is 1.45532317 and
worst droop is 49.18182677 mV; envelope ratio is diagnostic under this main,
not a newly imposed REF-21 acceptance limit. Metrics retain ADCToolbox 0.6.4.

## Archived mixed-top failure

The seven legacy mixed-top records and fourteen figures are retained unchanged
in [the complete pre-migration commit](https://github.com/many-question/ADC-12b-100M/commit/e46427cec6f0d5c4abe29cfa2da27f831e8784c1)
and its reachable tag `archive/adc-ref-v8-legacy-e46427c`. The
[original result directory](https://github.com/many-question/ADC-12b-100M/tree/e46427cec6f0d5c4abe29cfa2da27f831e8784c1/results/adc_top/tb_top_sine/xtor-ref)
contains the original JSON provenance and both spectrum and code figures.
Top-level results are outside this candidate PR's allowed paths and are not
relabeled as candidate measurements. Original raw evidence is also retained.

These runs used source commit `a8fc5117fe648bfe3213c9fdb7edea7ff1302264`,
100 MS/s, k=509, N=1024 calibration plus an independent N=1024 judged record,
noise enabled and seed 1. Six corners pass all recorded top limits;
**SS / low supply / 125 C fails TOP-01: 10.4655729645 < 10.5 bit**.

| Corner | ENOB (bit) | SFDR (dB) | Maximum conversion (ns) | Power (mW) | TOP-01 |
|---|---:|---:|---:|---:|---|
| ff_high_125 | 10.70115066 | 83.67649901 | 2.700794 | 42.94597160 | PASS |
| ff_high_m40 | 10.81752231 | 85.43488245 | 2.694165 | 48.23021209 | PASS |
| fs_nom_27 | 10.88168710 | 84.60701142 | 2.683331 | 37.77735484 | PASS |
| sf_nom_27 | 10.72195352 | 83.47272954 | 2.706632 | 21.53198363 | PASS |
| **ss_low_125** | **10.46557296** | 81.32549932 | 2.706319 | 18.17445476 | **FAIL** |
| ss_low_m40 | 10.80878592 | 83.19806402 | 2.682849 | 15.87055924 | PASS |
| tt_nom_27 | 10.82838024 | 84.64926494 | 2.685418 | 28.56524408 | PASS |

The matched archived behavioral control also fails at SS-hot
(10.32400310896 bit); the mixed-view difference is +0.14156985557 bit.
That comparison is neither an isolated reference-noise contribution nor a
waiver of the failure. Its original provenance and raw evidence are retained.
System diagnosis and follow-up remain under
[#35](https://github.com/many-question/ADC-12b-100M/issues/35).

## Migration and provenance

The official `adcflow migrate-candidate` command moved the module source and
results to this candidate. It changed result `view`, relocated `meta.files`
keys, and added `meta.migrated`. All metrics, original simulation git IDs,
`git_clean`, input-hash values, numerics, startup cross-check metadata, and
figure bytes are preserved. No simulation was run for the migration.

The only source-text change is the RNL package comment's relative path:
`../../rnl/adc28.rnl` becomes `../../../rnl/adc28.rnl` after the directory move.
Ports, devices, parameters and simulator logical input are identical.

| Source identity | Before | After |
|---|---|---|
| Electrical content hash | `380f10b05b0af622` | `380f10b05b0af622` |
| File SHA-256 | `0abeb03f4214bc1943ccf0378888487e6d1d025dd7a0f8f26c6c452431e8be21` | `1ca5f3143f4845e043416e8262d622e0556d4c060df175e21b448ed7991c6913` |

The migration audit finds zero stale module results against the stated main.
The earlier v7 results, including its four FF replay failures, remain reachable
at commit `5cafd1afb17b883f2b2b29556b24e8687f290848` through the archive tag.

## Pending shared changes

[PR #48](https://github.com/many-question/ADC-12b-100M/pull/48) is unmerged at
reviewed head `1b37045b7f858c16e7dc74437d27fffc21d1c66e`. It changes DAC charge
timing in the model (and therefore reference replay stimulus), CDAC behavioral
break-before-make switching, and top-level source-noise accounting. The current
records have not been validated against those pending semantics. All 136
module records track the CDAC behavioral source that PR changes, so they will
require a fresh stale audit if that change merges; replay and mixed-top evidence
also need renewed physical interpretation. No pending bias, decoupling, wait,
or acceptance-limit choice is applied by this candidate migration.
