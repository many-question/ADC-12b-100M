# V14 noise mechanism diagnosis

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

The genuine official TT failure remains 2094.115400 uV rms from clean source `3482a5e501a99ba6cedfe8415827c25c338f27fd`. All 17 levels have 512 samples. The smallest sampled output difference is 0.899716 V, and the shallow, nonmonotonic S-curve has a largest Gaussian-fit residual of 4.59 binomial standard deviations. A purely Gaussian noise mechanism is not established by that fit. The original test saves its analog trace only at the end, so reset coverage cannot be recovered from that run.

## Instrumented short comparison

Run `20261031-060605-strongarm-noise-numerics-diagnostic-screen` uses clean commit `99bf3b8b675b33c148706b8fc81cafb033f2f191` and the identical canonical circuit, electrical SHA-256 `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. Both jobs use 10 fF output loads, VCM 0.49 V, TT 0.9 V/27 C, 400 ps clock, 50 GHz upper noise frequency and seed 1. Inputs are -800 and +800 uV, 128 cycles each. The test adds read-only samplers at 80/150 ps after the rising 50% crossing, at the normal falling crossing, and 150 ps into reset; all MOS terminal voltages are saved.

The 102.5 ns duration raises the effective lower noise frequency to 9.7561 MHz, versus 287.216 kHz in the official run. Instrumentation also adds event time points. These limitations prevent substituting this diagnostic for the official result or estimating a new specification-grade sigma from two levels.

| Observation | Default tolerances | Fine tolerances |
|---|---:|---:|
| maxstep / reltol / vabstol | 69.634 ns / 1e-3 / 1e-6 | 0.5 ps / 1e-6 / 1e-8 |
| OUTP-positive count at -800 uV | 43 / 128 | 41 / 128 |
| OUTP-positive count at +800 uV | 79 / 128 | 78 / 128 |
| Sign changes, 80 ps sample to falling-edge sample | 0 / 256 | 0 / 256 |
| Sign changes, 150 ps sample to falling-edge sample | 0 / 256 | 0 / 256 |
| Completed reset cycles | 256 / 256 | 256 / 256 |
| Largest reset time | 23.636938 ps | 23.471510 ps |
| Both outputs below 10% VDD at late-reset samples | 256 / 256 | 256 / 256 |
| Physical output validity violations | 0 | 0 |
| Full-trace MOS stress violations | 0 / 69 pairs | 0 / 69 pairs |
| Maximum terminal-pair voltage | 0.90798 V | 0.90835 V |

Both integrations reproduce substantial wrong polarity at an input magnitude four times the 200 uV noise limit. Fine integration does not remove the errors. The sampled signs are already stable by 80 ps, and reset completes in every cycle, which argues against late sampling or incomplete external reset as the main explanation in this diagnostic.

The existing noiseless fine-step waveform shows QP/QN near 0.78993 V before evaluation, falling to about 0.55138 V at 5 ps after the clock midpoint while DP/DN are still about 0.8768 V. Q common mode then recovers before normal regeneration. In the fine noisy diagnostic, QP-minus-QN standard deviation grows from 0.456/0.466 mV in late reset to 4.361/4.604 mV at +30 ps for the two input signs. At +30 ps the DP-minus-DN mean is +3.798/-3.907 mV, with standard deviation 0.816/0.841 mV, while QP-minus-QN still has only -0.376/+0.848 mV mean of the opposite polarity to the eventual decision. This locates strong differential-noise growth in the release interval with weak, initially opposing input transfer. It does not yet identify a single device as the dominant noise generator.

The next physical experiment reduces only the CKB load to release the Q shunts earlier. Its purpose is to test whether avoiding the initial Q common-mode drop restores useful input transfer before noise grows. Falling-edge stress and reset are rechecked first, and noise is checked early if those gates pass. V14 expansion remains stopped.

Raw/deck SHA checks, full source provenance and effective single-thread +aps execution are retained. Both jobs ran sequentially while warming the shared model cache; observed batch peak is one job. The verified archive SHA-256 is `1436f6b932dfe0b78e4ef3a5266e42a8ebb5c5fcad0010fb941efbff31bd02f0`; the owned remote run is removed and absence confirmed.
