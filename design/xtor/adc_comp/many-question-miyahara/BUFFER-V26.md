# BUFFER-V26: buffer-node slew experiment

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

[B25](BUFFER-V25.md) passes five baseline deterministic corners and dedicated TT loading, but its tighter FS/high/-40 transient repeatedly fails with SPECTRE-16929 at 137.816 ps. Both attempts preserve the same source, exact testbench, numerical settings and normalized job deck; each retains 1260 accepted samples through 137.8159453449029 ps. The failed Newton iterate is not represented by the saved trace. B25 has no complete tighter gate or noise result.

B26 increases only the two BP/BN MOMs from 44 to 48 physical fingers (12.8604 to 14.0604 fF). All 43 MOS devices and the other seven MOMs remain exactly B25. More buffer-node capacitance tests a slower transition into the output pull-up and a larger edge-stress margin. It does not establish the underlying model/convergence cause or guarantee a repair. Added delay and reset loading must be measured against the unchanged limits; no noise benefit is assumed.

The fresh zero-warning callback uses the same provider/release as B25, with complete geometry, verified retrieval hashes and the exact owned callback directory absent. No model export, ideal clamp, tolerance relaxation or global numerical capacitance is introduced.

Repeat the five baseline deterministic corners, dedicated TT capacitance/kickback, and four critical tighter corners. All actual decisions, reset intervals, output validity and unrounded terminal pairs remain required. Full physical FS/low/125 noise follows only if these gates pass. Every stochastic source remains enabled; outputs use exact selected signals or the original monitor-only policy, with at most six session-wide Spectre jobs.

Callback SHA-256 `d37ce7f8401b61121c2bd6d773ece9522b51820fb6fa421c9d3633e3f22f2728`; each accepted MOM is 1.40604e-14 F. Electrical SHA-256 `13c455d69c414b141aa94d910b1adc256d7929e67997eb366a71d77660a59797`. The [complete RNL source](BUFFER-V26.txt) passes check/render with zero errors or warnings; the full inspected drawing remains in local evidence. The predecessor is pinned at [published commit 855618b](https://github.com/many-question/ADC-12b-100M/blob/855618b7d6ad7aeed2b909dfbd70e4b86975e99a/design/xtor/adc_comp/many-question-miyahara/BUFFER-V25.txt) and in verified archives. Canonical B20 and formal records remain unchanged.
