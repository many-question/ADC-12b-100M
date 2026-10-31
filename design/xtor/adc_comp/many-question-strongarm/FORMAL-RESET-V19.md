# Official validation: RESET-V19

The canonical electrical SHA-256 is `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. Only actual runs through the unchanged official runner update the result records. The fine-step private screens remain supplemental evidence.

## TT capacitance and kickback

Run `20261031-082118-4f95-tb_comp_kickback` uses clean source `e8ebf8600b1d09b80c3fa6806717c14ab7303fc1`. The original canonical view, testbench, numerical settings, measurement and recorder are unchanged. The private wrapper only accounts for resources, redirects temporary files to SSD and verifies evidence retrieval and owned-run cleanup.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Input capacitance per input | 19.330641078 fF | 20 fF | pass |
| CLKC input capacitance | 15.807766245 fF | 16 fF | pass |
| Differential kickback | 0.930826062 uV | 40 uV | pass |

The genuine [TT record](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-strongarm/tt_nom_27.json) records `git_clean=true`, `aps`, and the new electrical hash prefix. The CLKC margin is 0.192233755 fF. It is a TT gate, and this official result is separate from the fine-step mixed-delay clock-charge diagnostic. Numerical settings remain reltol 0.001, traponly and configured maxstep 66 ps; the log reports a largest accepted step of 50.5 ps.

The job used +aps with no explicit +mt and effective single-thread execution. All fetched raw/deck hashes match the owned remote run, which was removed with absence confirmed. The archive SHA-256 is `dd5788ff2844a31047a95d1c793da97042b1e19fa7a3749b3123f56de03d942a`; its byte-exact result/figure snapshots and every archive member were read back and verified.

One of the 92 current official records matches V19; 91 remain stale. The original complete TT noise protocol is the next gate. Remaining-corner SOA, required formal corners, mismatch, operating-range and mixed-top qualification remain open. No previous-source result transfers.
