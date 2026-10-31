# V32 artificial noise-source diagnostics at FS/low/125

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

**Diagnostic only; ineligible for qualification.** Full physical V32 noise remains the failed 371.83932552901155 uV rms [359.5,384.82] against 240 uV. Only the stated native transient noiseoff selectors change stochastic excitation; physical devices, dimensions, loads and actual numerical settings are unchanged. Source is `3b7108921859eba3a1514cb5f91f2d42c94472bd`, electrical SHA-256 `0611d6028825bf29c02983e7e337a09e4627884b7aef22e20130770b72d7c557`.

| Suppressed sources | Width uV | 95% interval uV | Max abs standardized fit residual |
|---|---:|---|---:|
| input_pair | 308.7949611886685 | [298.32, 319.77] | 2.4673923168731244 |
| q_shunts | 346.9162603711897 | [335.35, 359.06] | 1.4871968394544695 |
| regenerative_stage | 342.61237751642614 | [331.18, 354.62] | 2.9324116454871154 |

Input pair means MINP/MINN; Q shunts means MDQP/MDQN. Each trial retains every finite sample from the original 17 levels x 512, 50 GHz bandwidth, actual 287.216 kHz low cutoff and seed 1. Actual settings are conservative/gear2only/reltol 1e-4/vabstol 1e-6/relref alllocal/lteratio 10; monitor-only save=none, no explicit maxstep or method. Native selector validation reports no selection-related warning.

| Input uV | Physical OUTP/512 | Input pair suppressed | Q shunts suppressed | Regenerative stage suppressed |
|---:|---:|---:|---:|---:|
| -800 | 14 | 1 | 6 | 4 |
| -700 | 21 | 8 | 12 | 9 |
| -600 | 24 | 22 | 17 | 25 |
| -500 | 45 | 28 | 36 | 43 |
| -400 | 77 | 51 | 67 | 60 |
| -300 | 120 | 81 | 102 | 104 |
| -200 | 140 | 134 | 138 | 139 |
| -100 | 164 | 225 | 211 | 175 |
| 0 | 270 | 254 | 251 | 245 |
| 100 | 307 | 314 | 303 | 312 |
| 200 | 364 | 367 | 377 | 342 |
| 300 | 398 | 445 | 411 | 403 |
| 400 | 440 | 465 | 445 | 448 |
| 500 | 479 | 492 | 469 | 491 |
| 600 | 486 | 499 | 494 | 502 |
| 700 | 496 | 506 | 497 | 501 |
| 800 | 507 | 511 | 510 | 503 |

These counterfactual fitted widths cannot be variance-subtracted into independent additive device contributions. Nonlinear regeneration, correlations and changed random-number consumption remain; profile intervals are conditional on the Gaussian fit. Further source diagnostics may guide physical changes, but every physical candidate restores all noise sources and must pass its own unchanged gates.

- `20261031-155740-strongarm-reset-v32-spec08-noiseoff-input_pair-screen`: archive SHA-256 `05b5044e82b47ab655a53877a0441ec24641b7606076d1f808a2254426de94f4`; every member passed CRC/SHA readback and the exact owned remote directory is absent. Later tested-TB comparison SHA-256 `91e4e5b68534eb5ccc164e603ed1686fea042a01e03b8147529989f413dae5bf`.

- `20261031-155750-strongarm-reset-v32-spec08-noiseoff-q_shunts-screen`: archive SHA-256 `af2285073d6bc33d99eebcdd7d0e1ad760405a80d89c2f7f4acd19ae60baf5aa`; every member passed CRC/SHA readback and the exact owned remote directory is absent. Later tested-TB comparison SHA-256 `9f4447f7d2df1e6539b8b36f07f18ee082093b771119c590536db13e419d46ba`.

The supplemental comparison verifies that the two actual tested benches match exactly after removing the native noiseoff clause and normalizing line endings. It postdates the immutable raw archive and is retained separately under the hash above. The earlier audit flag comparing against the unadapted official TB is false because the explicit output-only policy is an additional adapter step; source, stimulus and actual numerical equality were independently verified.

Regenerative stage means MLNP/MLNN/MLPP/MLPN. Its frozen source is `eac8e8c280d5c0220b4412a1f7622b93a3148e8f` with the same electrical hash. Run `20261031-161219-strongarm-reset-v32-spec08-noiseoff-regenerative_stage-screen`, archive SHA-256 `9bbd31d6641b33c9dbe7062887ec2b454ef3a8a6b2d829c1aa31c01acbb5c77f`, retains the exact tested-bench comparison (only native noiseoff differs), all 8704 finite decisions and final guards. CRC/SHA readback and exact remote absence pass. The modest fitted-width change does not justify a unique device-noise attribution.

## Deterministic trajectory diagnostic

At 100 uV, averaged over both polarities and repetitions, when Q common mode falls through 0.9 VDD:

| Corner | After clock rise ps | D differential / input |
|---|---:|---:|
| tt_nom_27 | 21.8510467980339 | 3.659111803293036 |
| ss_low_125 | 27.36491682257592 | 2.97009339099652 |
| fs_low_125 | 13.690922168003933 | 2.0311709551129598 |

These are trajectory ratios, not local small-signal derivatives or noise powers. Existing V32 deterministic raw was read from verified archives; no simulation settings changed. The complete milestone/cycle audit is retained locally under SHA-256 `d167057dafe74429c15408a4a989a47c81e2c343d94655474d5bfa966a5be4ea`. Lower FS amplification before the Q transition motivates a physical latch-strength trial; this is a hypothesis.
