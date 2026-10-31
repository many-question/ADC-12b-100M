# Official validation: RESET-V19

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

The canonical electrical SHA-256 is `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. Only actual runs through the unchanged official runner update the result records. The fine-step private screens remain supplemental evidence.

## TT capacitance and kickback

Run `20261031-082118-4f95-tb_comp_kickback` uses clean source `e8ebf8600b1d09b80c3fa6806717c14ab7303fc1`. The original canonical view, testbench, numerical settings, measurement and recorder are unchanged. The private wrapper only accounts for resources, redirects temporary files to SSD and verifies evidence retrieval and owned-run cleanup.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Input capacitance per input | 19.330641078 fF | 20 fF | pass |
| CLKC input capacitance | 15.807766245 fF | 16 fF | pass |
| Differential kickback | 0.930826062 uV | 40 uV | pass |

The genuine [TT record](https://github.com/many-question/ADC-12b-100M/blob/8f31c7e6ca7aca61e37cb579c6d35eb67d709b2b/results/adc_comp/tb_comp_kickback/xtor-many-question-strongarm/tt_nom_27.json) records `git_clean=true`, `aps`, and the new electrical hash prefix. The CLKC margin is 0.192233755 fF. It is a TT gate, and this official result is separate from the fine-step mixed-delay clock-charge diagnostic. Numerical settings remain reltol 0.001, traponly and configured maxstep 66 ps; the log reports a largest accepted step of 50.5 ps.

The job used +aps with no explicit +mt and effective single-thread execution. All fetched raw/deck hashes match the owned remote run, which was removed with absence confirmed. The archive SHA-256 is `dd5788ff2844a31047a95d1c793da97042b1e19fa7a3749b3123f56de03d942a`; its byte-exact result/figure snapshots and every archive member were read back and verified.

At completion of this capacitance run, one of 92 records matched V19. The following section records the subsequent genuine noise run. Remaining-corner SOA, required formal corners, mismatch, operating-range and mixed-top qualification remain open. No previous-source result transfers.


## TT transient noise: fail

Run `20261031-082818-6cec-tb_comp_noise` uses actual clean source `cd870c295d3b361df37f897a702e57bb544837e5`. The original 17 levels, 512 decisions per level, 50 GHz noise bandwidth, seed 1, sampler, numerical settings, Gaussian-CDF fit and recorder are unchanged. All 8704 samples are finite, exactly 512 at every level, with none outside the expected sequence.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Input-referred noise | 218.770058633 uV rms | 200 uV at TT | fail |
| Noise 95% profile-likelihood interval | 210.31 to 227.64 uV | — | reported |
| Absolute systematic offset | 0.011555686 mV | 2 mV | pass |

The genuine [TT noise JSON](https://github.com/many-question/ADC-12b-100M/blob/8f31c7e6ca7aca61e37cb579c6d35eb67d709b2b/results/adc_comp/tb_comp_noise/xtor-many-question-strongarm/tt_nom_27.json) retains its actual source metadata. The minimum sampled absolute output difference is 0.899668058 V. The largest standardized residual from the fitted Gaussian CDF is 3.784980; intervals and residuals are conditional on that model. The original outputstart=tstop does not establish reset history, intermediate dynamic behavior or full-trace terminal stress. Private physical checks remain separate.

| Input (uV) | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 3 |
| -400 | 17 |
| -300 | 40 |
| -200 | 87 |
| -100 | 140 |
| 0 | 288 |
| 100 | 328 |
| 200 | 401 |
| 300 | 462 |
| 400 | 492 |
| 500 | 504 |
| 600 | 511 |
| 700 | 512 |
| 800 | 512 |

![Original TT noise curve](https://raw.githubusercontent.com/many-question/ADC-12b-100M/8f31c7e6ca7aca61e37cb579c6d35eb67d709b2b/results/adc_comp/tb_comp_noise/xtor-many-question-strongarm/tt_nom_27.noise.png)

The run used +aps with no explicit +mt and effective single-thread execution. Fetched raw/deck hashes match; the exact owned remote directory is confirmed absent. Archive SHA-256 `bf04b3529675aa6a1e0ac9f5d30a7c95ef3c4b48054dfb5eb065a098fb58e65d` includes byte-exact genuine result/figure snapshots and the separate sample/shape audit, with every member read back and verified.

Two of the 92 current official cases now match V19 and 90 remain stale. Freshness does not imply passing. V19 qualification expansion stops at this failure; physical diagnosis and a subsequent circuit revision remain active. Remaining-corner SOA, all required formal cases, mismatch, operating-range and mixed-top qualification remain open. No source is selected or qualified.

Historical result and figure links are pinned to byte-verified published commit `8f31c7e6ca7aca61e37cb579c6d35eb67d709b2b` so future genuine runs cannot change the evidence shown by this report.
