# Conservative numerics revalidation — adc_ref 0.9.0

The unchanged main28/gate16 candidate was rerun with the official flow merged in [PR #95](https://github.com/many-question/ADC-12b-100M/pull/95), based on `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`. This replaces the transient acceptance evidence from before that change. Earlier reports remain historical evidence.

All **136 module records are fresh and pass 631 applicable specification/corner checks**: 45 startup and 45 replay records were rerun; 45 DC and one noise record remain unchanged. The 92 exempt JSON/PNG files are byte-identical. Four startup convergence comparisons add four simulation jobs, for 94 new simulation jobs in total.

The circuit and RNL drawing are unchanged. Electrical hash: `2b1163f0eb481376`; full source SHA256: `146b30ff01111e2a83d36b42aa812301f97b842d4e808b002763a808a3784d95`.

## Settings and provenance

Every primary formal transient used APS, `errpreset=conservative`, effective `method=gear2only`, `reltol=1e-4`, `relref=alllocal` and `lteratio=10`, confirmed from simulator logs. Startup retains `maxstep=1n`; replay has no explicit maxstep. All records were produced from a clean committed source using the unmodified official runner, testbench generation and measurement functions.

Spectrum metrics come directly from ADCToolbox `compute_spectrum` at upstream commit `cd72061ff3b7a977163dac540da126ae22f5e38d`. The isolated installation records that exact Git commit, and its installed Python sources were checked against the pinned checkout. No premerge private adapter or rehash was used. The installation check from [#96](https://github.com/many-question/ADC-12b-100M/issues/96) returns 80.000000 dBc. The documented upstream SNDR bias of about 0.8 dB for a spur touching the signal bins remains; no alternate spectral estimator is used for acceptance.

The measured peak was 6 concurrent simulation jobs. Each job used one APS solver thread; no explicit `+mt` was supplied. Input and returned evidence hashes were verified, and raw evidence was retained privately.

## Replay worst cases

| Check | Worst corner | Value | Limit |
|---|---|---:|---:|
| REF-12 | fs_high_m40 | 0.045329539 bit | <= 0.1 |
| REF-13 | ss_low_125 | 134.38813 uV | <= 200 |
| REF-14 | tt_nom_125 | 49.0909602 uV | <= 100 |
| REF-21 | ss_low_125 | 0.9423357  | <= 1 |

## Startup worst cases

| Check | Worst corner | Value | Limit |
|---|---|---:|---:|
| REF-15 | ss_high_m40 | 0.955515047 V | <= 1 |
| REF-16 | ss_low_m40 | -2.74242752e-17 V | >= -0.1 |
| REF-17 | ss_high_m40 | 0.477757566 V | <= 1 |
| REF-18 | ss_low_m40 | -3.86784758e-19 V | >= -0.1 |
| REF-19 | ff_low_125 | 1.04604194 mV | <= 5 |
| REF-20 | all 45 corners | 0.450129621 to 0.450523053 V | 0.44 to 0.46 V |

## Startup convergence comparisons

The official crosscheck uses `traponly` and `maxstep=0.1n`; the primary run uses `gear2only` and `maxstep=1n`. Both actual settings are stored in each result. The table gives crosscheck minus primary; both runs pass the same limits.

| Corner | VREFP peak difference (mV) | VCM peak difference (mV) | Ready-error difference (mV) |
|---|---:|---:|---:|
| ff_low_125 | -0.00225271 | -0.00156741 | -0.00129934 |
| fs_low_m40 | 0.00291529 | 0.0014483 | 0.00291528 |
| sf_nom_m40 | -0.0162337 | -0.00384889 | -0.00481371 |
| ss_high_m40 | -0.00610352 | -0.00345628 | 0.000562823 |

## Eligibility

This establishes current candidate-owned module evidence. Renewed lead verification and mixed-top regression remain separate requirements; old verification and mixed-top records are not inherited. A strict stale warning is not an eligibility pass.
