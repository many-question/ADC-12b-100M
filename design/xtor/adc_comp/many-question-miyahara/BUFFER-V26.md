# BUFFER-V26: buffer-node slew experiment

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

[B25](BUFFER-V25.md) passes five baseline deterministic corners and dedicated TT loading, but its tighter FS/high/-40 transient repeatedly fails with SPECTRE-16929 at 137.816 ps. Both attempts preserve the same source, exact testbench, numerical settings and normalized job deck; each retains 1260 accepted samples through 137.8159453449029 ps. The failed Newton iterate is not represented by the saved trace. B25 has no complete tighter gate or noise result.

B26 increases only the two BP/BN MOMs from 44 to 48 physical fingers (12.8604 to 14.0604 fF). All 43 MOS devices and the other seven MOMs remain exactly B25. More buffer-node capacitance tests a slower transition into the output pull-up and a larger edge-stress margin. It does not establish the underlying model/convergence cause or guarantee a repair. Added delay and reset loading must be measured against the unchanged limits; no noise benefit is assumed.

The fresh zero-warning callback uses the same provider/release as B25, with complete geometry, verified retrieval hashes and the exact owned callback directory absent. No model export, ideal clamp, tolerance relaxation or global numerical capacitance is introduced.

Five baseline corners, four critical tighter corners and dedicated TT loading pass. Full physical FS/low/125 noise then fails; qualification expansion stops at CMP-13. Exact selected or monitor-only saves, all physical stochastic sources and the six-job ceiling are preserved.

Callback SHA-256 `d37ce7f8401b61121c2bd6d773ece9522b51820fb6fa421c9d3633e3f22f2728`; each accepted MOM is 1.40604e-14 F. Electrical SHA-256 `13c455d69c414b141aa94d910b1adc256d7929e67997eb366a71d77660a59797`. The [complete RNL source](BUFFER-V26.txt) passes check/render with zero errors or warnings; the full inspected drawing remains in local evidence. The predecessor is pinned at [published commit 855618b](https://github.com/many-question/ADC-12b-100M/blob/855618b7d6ad7aeed2b909dfbd70e4b86975e99a/design/xtor/adc_comp/many-question-miyahara/BUFFER-V25.txt) and in verified archives. Canonical B20 and formal records remain unchanged.

## Completed physical result

**FS/low/125 noise is 270.61635250554104 uV rms, FAIL 240**, with model-conditional 95% profile interval [261.07, 280.6]. All 17 levels x 512 finite decisions are retained at 50 GHz and seed 1, with every physical noise source enabled. This is below B22's 342.51175741522553 uV point estimate, but remains outside the limit. There is no B26 TT noise result or promotion.

Frozen source `3dd17927ddcb842b4e28289270fa76436dcb4ab1` passes all 324 actual decisions/reset intervals across five baseline and four tighter corners, output validity, 129 full-trace unrounded MOS terminal pairs per corner and AVDD KCL. TT baseline/tighter 1 mV delay is 58.36318101711513/58.54117412412848 ps; 30 mV delay is 48.97788988704756/48.99406817867042 ps. SS reset is 33.11462822753791/32.88904249976513 ps. Worst stress is 0.9994063398192367 V baseline and 0.9997484829720795 V tighter; tighter FS margin is only 251.51702792047814 uV. All four tighter logs are free of min-step/convergence warnings; this does not identify the earlier B25 failure mechanism.

Dedicated TT input/clock capacitance is 19.328731218738323/12.105038071102172 fF. Net cycle kickback is 8.382100005407955e-05 uV; distinct instantaneous differential/common-mode peaks are 30.645660529801145 uV in reset and 7.418243573274141 mV in evaluation. They are not compared to the net 40 uV limit. Actual-CDAC validation remains open.

NUMERICS-94 preserves every exact run ID, setting, metric and archive hash. All four runs passed retrieval/final-source guards, archive CRC/SHA readback and exact remote absence. The physical-noise failure remains in the verified archive `65d55d31f54cd762c3ffb8b547e078fa79b23ea3ab26f2ca67f5eebeb0dd85e1`. Canonical B20 and its formal failure are unchanged; further physical design requires new evidence.
