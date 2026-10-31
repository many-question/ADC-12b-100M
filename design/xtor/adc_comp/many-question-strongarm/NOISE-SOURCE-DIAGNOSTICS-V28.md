# V28 artificial noise-source diagnostics

These simulations selectively suppress stochastic sources in an otherwise unchanged circuit. **They are not physical comparator performance and cannot establish compliance.** The actual all-noise V28 result remains a TT failure at 206.44956249285457 uV rms, with a model-conditional 95% profile interval of 198.24 to 215.06 uV. [RESET-V28](RESET-V28.md) retains that failure.

The native Spectre `tran noiseoff` parameter is documented by the installed simulator's help. Each tested deck contains the named instance list, and no selection-related warning occurs. The archived circuit source and all other testbench bytes match the all-noise reference. Both artificial trials use clean source `a991aba96dc3e6987f39335d7105c78943c9a8c8`, APS, conservative/gear2only, actual reltol 1e-4, default vabstol, alllocal and lteratio 10; no explicit maxstep or method. The full 17 levels and 512 finite samples per level are retained, along with 50 GHz bandwidth, actual 287.216 kHz low-frequency cutoff and seed 1. No formal records are written, and physical gate/report helpers explicitly reject this diagnostic class.

| Artificial source suppression | Fitted width uV | 95% profile interval uV | Changed input-level counts vs all-noise | Max standardized residual |
|---|---:|---|---:|---:|
| XDUT.MINP / XDUT.MINN | 143.69178503038893 | [136.88, 150.9] | 11 | 1.2150480431457997 |
| XDUT.MDQP / XDUT.MDQN | 187.75199804064 | [179.95, 195.95] | 11 | 1.061253825480928 |

| Input uV | All-noise OUTP / 512 | Input-pair noise suppressed | Q-shunt noise suppressed |
|---:|---:|---:|---:|
| -800 | 0 | 0 | 0 |
| -700 | 0 | 0 | 0 |
| -600 | 0 | 0 | 0 |
| -500 | 2 | 0 | 3 |
| -400 | 12 | 2 | 6 |
| -300 | 37 | 11 | 24 |
| -200 | 85 | 40 | 64 |
| -100 | 135 | 146 | 148 |
| 0 | 290 | 267 | 243 |
| 100 | 341 | 394 | 348 |
| 200 | 408 | 472 | 430 |
| 300 | 473 | 503 | 478 |
| 400 | 497 | 512 | 502 |
| 500 | 506 | 512 | 510 |
| 600 | 512 | 512 | 512 |
| 700 | 512 | 512 | 512 |
| 800 | 512 | 512 | 512 |

The input-pair suppression gives a larger change in fitted width than Q-shunt suppression in these trials. This is an inference for prioritizing circuit work, not a unique device-noise decomposition. Nonlinear regeneration, correlations and changed random-number consumption prevent treating variance differences as independent additive contributions. Profile intervals remain conditional on the Gaussian-CDF model. [Cadence's explanation of transient-noise diagnostics](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/36394/print-noise-summary-after-analysis-during-tran/1348522) describes this distinction and the use of selective noise-source trials.

The next physical experiment will first test stronger output drivers for timing headroom before considering a lower input-stage tail current. An earlier tail-current reduction failed delay, so it is not repeated without checking this tradeoff. All physical experiments restore every noise source and recheck delay, reset, full terminal stress, output validity and loading. No noise improvement is assumed from output sizing alone.

- `20261031-133339-strongarm-reset-v28-spec08-noiseoff-input_pair-screen`: archive SHA-256 `035d439a1c6bc6c9cb3a1bb1996b02cb3f914247ef7e95b8f0803a61f20f0f82`, all members read back with CRC/SHA-256 verification and the exact owned remote run absent.
- `20261031-133342-strongarm-reset-v28-spec08-noiseoff-q_shunts-screen`: archive SHA-256 `a56de68b166db74a927671dd5ef6261a42d99c9bbfc9c59994ccf430ff15d8ec`, all members read back with CRC/SHA-256 verification and the exact owned remote run absent.
