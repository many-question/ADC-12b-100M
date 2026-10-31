# B22 artificial noise-source diagnostics at FS/low/125

These simulations suppress selected stochastic sources in an otherwise unchanged B22 circuit. **They are not physical comparator performance and cannot establish compliance.** The full physical B22 FS/low/125 result remains a failure at 342.51175741522553 uV rms, against 240 uV, with a model-conditional 95% profile interval of 331.11 to 354.49 uV. [BUFFER-V22](BUFFER-V22.md) preserves that failure and its separately passing deterministic checks.

One trial disables only MINP/MINN noise. The other disables only the ten regenerative-stage devices M14/M15/M12/M13/M10/M11/M6/M7/M8/M9. Physical devices, dimensions, loads, clocking, capacitances and bias are unchanged; all other stochastic sources remain enabled. The exact native Spectre `tran noiseoff` list is present, with no selector-related warning. All other tested testbench bytes and the physical source match the all-noise reference. Physical gate/report helpers explicitly reject this diagnostic class.

Both trials use clean source 4595a1426a830ecc9673c376600851c2fe094e8c, the merged 0.8.0 baseline, APS, actual conservative/gear2only/reltol 1e-4/vabstol 1e-6/relref alllocal/lteratio 10, and no explicit maxstep or method. The original 17 levels, 512 finite samples per level, 50 GHz bandwidth, actual low-frequency cutoff 287.216 kHz and seed 1 are retained. No decisions are discarded, and no formal record is written.

| Artificial source suppression | Fitted width uV | 95% profile interval uV | Changed level counts | Max standardized residual |
|---|---:|---|---:|---:|
| input_pair | 262.0129545745118 | [252.68, 271.78] | 17 | 2.039901077473558 |
| regenerative_stage | 226.7958027287217 | [218.17, 235.83] | 17 | 2.6568717246255766 |

| Input uV | All-noise OUTP / 512 | Input-pair noise suppressed | Regenerative-stage noise suppressed |
|---:|---:|---:|---:|
| -800 | 4 | 0 | 1 |
| -700 | 5 | 3 | 0 |
| -600 | 21 | 5 | 2 |
| -500 | 33 | 13 | 9 |
| -400 | 76 | 40 | 15 |
| -300 | 66 | 71 | 48 |
| -200 | 137 | 130 | 103 |
| -100 | 184 | 203 | 164 |
| 0 | 267 | 281 | 278 |
| 100 | 318 | 337 | 348 |
| 200 | 378 | 424 | 402 |
| 300 | 405 | 453 | 455 |
| 400 | 438 | 485 | 497 |
| 500 | 469 | 501 | 507 |
| 600 | 493 | 504 | 511 |
| 700 | 491 | 508 | 512 |
| 800 | 510 | 512 | 512 |

The response to source suppression is a diagnostic for selecting physical circuit changes. It is not a unique device-noise decomposition: nonlinear regeneration, correlations and changed random-number consumption prevent interpreting squared-width differences as independent additive contributions. Fit intervals remain conditional on the Gaussian-CDF model. [Cadence's discussion of transient-noise diagnostics](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/36394/print-noise-summary-after-analysis-during-tran/1348522) explains this distinction and selective source trials. Actual installed Spectre help is retained with the earlier V28 diagnostic evidence.

Any subsequent physical candidate restores every stochastic source and rechecks timing, reset, output validity, full terminal stress and loading before the full physical noise protocol. These artificial results neither replace the failed B22 run nor authorize qualification expansion.

- `20261031-140219-miyahara-buffer-v22-spec08-noiseoff-input_pair-screen`: archive SHA-256 `2c8ee924b8d0ba57d92c7f1108d479d61e1f20d2673977d8571f0a454cd00db3`, all members read back with CRC/SHA-256 verification and the exact owned remote run absent.
- `20261031-140219-miyahara-buffer-v22-spec08-noiseoff-regenerative_stage-screen`: archive SHA-256 `eba42669875cc48d8208cb70cefb6007a9292c316890846c52c2c9f8119b3b7a`, all members read back with CRC/SHA-256 verification and the exact owned remote run absent.
