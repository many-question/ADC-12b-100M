# Official new-source validation: RESET-V14

The promoted canonical source has electrical SHA-256 `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. These are new simulations through the existing official runner and recorder. The independent screening data remains supplemental.

## TT capacitance and kickback

Actual clean source commit: `116b758630b902a077ff23776658695eba92893e`. Official run: `20261031-053903-de6e-tb_comp_kickback`. The existing `runner.run_test` uses the canonical view, mode `aps`, one job, `keep=True` and normal recording; no source, testbench, numeric, measurement or record replacement is used. The private execution wrapper only adds resource accounting, SSD temporary paths and evidence verification/cleanup.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Differential kickback | 1.063399 uV | 40 uV | pass |
| Input capacitance per input | 19.330482 fF | 20 fF | pass |
| CLKC input capacitance | 15.099419 fF | 16 fF | pass |

The genuine result is [TT kickback JSON](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-strongarm/tt_nom_27.json). Its metadata records `git_clean=true`, mode `aps`, and the canonical source's electrical hash prefix `dd44da2a98a529e3`. Official testbench numerical settings are unchanged: reltol 0.001, traponly, configured maxstep 66 ps; the log reports a largest accepted step of 50.5 ps. This capacitance result is separate from the fine-step mixed-delay clock-charge diagnostic.

The job uses `+aps` with no explicit `+mt` and effective single-thread simulation. All retrieved raw/deck hashes match the owned remote run, which was removed with absence confirmed. The verified archive SHA-256 is `f7b422baede35e005e268d2cd89700f2ecaa20cbe586d686ffd724986451d0c5`; it also contains a byte-exact snapshot of the actual recorded JSON and figures.

One official case is now fresh for V14; 91 old-source records remain stale. TT noise is the next gate. Remaining-corner stress, full official coverage, mismatch and mixed-top qualification remain open. No old-source performance is inherited.
