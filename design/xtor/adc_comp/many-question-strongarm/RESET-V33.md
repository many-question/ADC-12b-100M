# V33: weaker N latch pair

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

Private, unqualified physical trial. Only MLNP/MLNN change from N8 to N4 (30 nm, four 1 um fingers), reusing the exact verified V32 output-N4 geometry and all terminal parasitics. The other 21 MOS devices and all five MOMs are unchanged. The V32 trajectory diagnostic suggests less input amplification before the Q transition at FS/low/125; weakening the N latch tests that timing hypothesis. Delay, reset, SOA, capacitance and full physical noise require fresh measurements. No benefit is assumed.

Electrical SHA-256 `e859347340abfbe7f5e42e0a9c3a831f378bce9bea727177b4e214ef60a1b0cf`. The [complete RNL source](RESET-V33.txt) passes check/render with zero errors or warnings; the inspected drawing is retained locally. V32 is pinned at [published eac8e8c](https://github.com/many-question/ADC-12b-100M/blob/eac8e8c280d5c0220b4412a1f7622b93a3148e8f/design/xtor/adc_comp/many-question-strongarm/RESET-V32.txt) and in verified archives. Canonical V27 and genuine formal failures are unchanged.

Completed baseline at `15fa827572d71887fd3b3d7abf05be81cdf64900`: all five corners pass 180 actual decisions/reset intervals, output validity, 69 full-trace unrounded MOS pairs per corner and AVDD KCL. TT 1 mV/30 mV delay is 68.32301083919458/49.433499354741386 ps; SS reset is 30.94352557878534 ps. Worst stress is 0.9975641708765174 V. Dedicated TT input/clock capacitance is 19.331118542884703/15.570038425100613 fF. Exact measurements, kickback context and archive hashes are in NUMERICS-94.

The archived matched trajectory audit shows FS Q-common 0.9 VDD crossing moving from 13.690922168003933 to 15.771117266559811 ps, and D differential/input ratio rising from 2.0311709551129598 to 2.4486975121798538. This supports the timing hypothesis, not a noise conclusion. The thin TT delay margin requires tighter checks before full physical noise.
