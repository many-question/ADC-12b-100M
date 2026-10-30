# Official new-source validation: BUFFER-V12

The canonical electrical SHA-256 is `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. These results come from actual new simulations through the existing official runner and recorder. Private screening remains supplemental.

## TT capacitance and kickback

Actual clean source commit: `7e6d4dede3c74ef0554fe425fe16148f8a8230df`. Run: `20261031-055648-7ca5-tb_comp_kickback`. The canonical view, official testbench, numerical settings, measurements and recording are unchanged. The private wrapper adds resource accounting, evidence verification and owned-run cleanup only.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Differential kickback | 0.002025736 uV | 40 uV | pass |
| Input capacitance per input | 19.328731219 fF | 20 fF | pass |
| CLKC capacitance | 9.609324821 fF | 16 fF | pass |

The genuine [TT kickback JSON](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-miyahara/tt_nom_27.json) records `git_clean=true`, mode `aps`, and source electrical hash prefix `e64f215d6bd941a8`. Numerics remain reltol 0.001, traponly, configured maxstep 66 ps; largest accepted step is 50.5 ps. This official capacitance test is separate from the mixed-delay clock-charge diagnostic.

One job used +aps, no explicit +mt and effective single-thread execution. All fetched raw/deck hashes match, and the owned remote run is removed with absence confirmed. Verified archive SHA-256: `b4d31c289c9e1eb95a19722428d716a6d192cef31592654599c0053fe05ade90`. The archive contains a byte-exact snapshot of the genuine JSON and figures.

One official case is fresh for B12; 91 old-source records remain stale. TT noise is the next gate. Remaining-corner stress, full official coverage, mismatch and mixed-top qualification remain open. No old-source performance is inherited.
