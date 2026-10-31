# Official new-source validation: RESET-V14

The promoted canonical source has electrical SHA-256 `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. These are new simulations through the existing official runner and recorder. The independent screening data remains supplemental.

## TT capacitance and kickback

Actual clean source commit: `116b758630b902a077ff23776658695eba92893e`. Official run: `20261031-053903-de6e-tb_comp_kickback`. The existing `runner.run_test` uses the canonical view, mode `aps`, one job, `keep=True` and normal recording; no source, testbench, numeric, measurement or record replacement is used. The private execution wrapper only adds resource accounting, SSD temporary paths and evidence verification/cleanup.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Differential kickback | 1.063399 uV | 40 uV | pass |
| Input capacitance per input | 19.330482 fF | 20 fF | pass |
| CLKC input capacitance | 15.099419 fF | 16 fF | pass |

The genuine result is [TT kickback JSON](https://github.com/many-question/ADC-12b-100M/blob/8c0d2666ccb0e135e5799e3c2390bbd4db3dfe12/results/adc_comp/tb_comp_kickback/xtor-many-question-strongarm/tt_nom_27.json). Its metadata records `git_clean=true`, mode `aps`, and the canonical source's electrical hash prefix `dd44da2a98a529e3`. Official testbench numerical settings are unchanged: reltol 0.001, traponly, configured maxstep 66 ps; the log reports a largest accepted step of 50.5 ps. This capacitance result is separate from the fine-step mixed-delay clock-charge diagnostic.

The job uses `+aps` with no explicit `+mt` and effective single-thread simulation. All retrieved raw/deck hashes match the owned remote run, which was removed with absence confirmed. The verified archive SHA-256 is `f7b422baede35e005e268d2cd89700f2ecaa20cbe586d686ffd724986451d0c5`; it also contains a byte-exact snapshot of the actual recorded JSON and figures.

## TT transient noise: failed gate

Actual clean source commit: `3482a5e501a99ba6cedfe8415827c25c338f27fd`. Official run: `20261031-054530-3bb5-tb_comp_noise`. The original 17 input levels and 512 decisions per level, 50 GHz noise bandwidth, seed 1, sampler, numerical settings and official measurement are unchanged. All 8,704 samples are present, with exactly 512 at every level.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Input-referred noise | 2094.115400 uV rms | 200 uV at TT | fail |
| Noise 95% profile-likelihood interval | 1878.31 to 2365.39 uV | — | reported |
| Absolute systematic offset | 0.085448 mV | 2 mV | pass |

The genuine [TT noise JSON](https://github.com/many-question/ADC-12b-100M/blob/8c0d2666ccb0e135e5799e3c2390bbd4db3dfe12/results/adc_comp/tb_comp_noise/xtor-many-question-strongarm/tt_nom_27.json) records `git_clean=true`, mode `aps`, and electrical hash prefix `dd44da2a98a529e3`. Every sampled output difference has magnitude at least 0.899716 V. Thus the samples are resolved; the decision-probability curve is too shallow. Its largest standardized residual from the fitted Gaussian CDF is 4.59 binomial standard deviations, so the fitted number should not be taken as proof of a purely Gaussian mechanism. The official failure is retained unchanged.

The run completed with zero simulator errors, +aps, no explicit +mt and effective single-thread execution. All fetched raw/deck hashes match; the owned remote directory is removed and absence confirmed. The verified archive SHA-256 is `991cbaff30ded8b8fee3fa6f3daf9f50e95e1b6278b8604cdce96d3faf7614a1`, including the actual recorded JSON/figure and an independent sample-count/shape diagnostic.

Two official cases are now fresh for V14; 90 old-source records remain stale. V14 fails the TT noise gate and its expensive qualification expansion is stopped. Root-cause diagnostics and a subsequent circuit revision remain active. Remaining-corner stress, full official coverage, mismatch and mixed-top qualification remain open. No old-source performance is inherited.

Historical result links are pinned to the preserved pre-V19 commit so later official runs cannot change the evidence shown by this report.
