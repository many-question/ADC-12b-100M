# RESET-V3: output-controlled weak keepers

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

RESET-V2's remaining peak is QP/QN overshoot at the end of the rising clock edge, while its four-corner delay, reset and output validity pass. This experiment reduces each clocked Q precharge PMOS from 6 um to 2 um and adds a weak inverter from the external output back to its internal Q node: P2 um / N0.5 um, all at 30 nm. The PMOS keeper conducts while that output is low and may absorb positive clock feedthrough. The small NMOS keeper conducts while the output is high. The original output inverter and its external load remain physical circuit elements.

The keeper introduces contention during evaluation and reset. Those delay, reset and energy costs must be measured; no successful validation is inherited. The input precharge, tail, core and two MOM capacitors are unchanged from V2. Existing callback-derived P2 geometry and the new successful N0.5 callback are used without scaling parasitics.

[RESET-V3.txt](RESET-V3.txt) is the independent 19-MOS/two-MOM source. Electrical SHA-256: `b4446fa108ea819712f441abe31a8be623c0eb8a904c8e27b2458260b41f8902`. Its byte-identical `.scs` RNL mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints.

![Weak keeper experiment](https://raw.githubusercontent.com/many-question/ADC-12b-100M/e45f2ad7bea3b45f5822eae18549b326c19fc727/design/xtor/adc_comp/many-question-strongarm/reset-v3.png)

The first screen uses the same four key corners and 0.5 ps settings as V2, with all MOS terminal pairs, actual output validity, delay, reset, AVDD energy and supplemental clock charge. This source-freeze commit makes no performance claim. The canonical source and baseline official records remain unchanged.

## Completed screen: rejected

Actual source commit: `9d3892c3655d00130d08c81c79ae873d693895fd`. The P2 keeper strongly opposes evaluation. TT makes only 8/36 decisions; the official wrong/failed-decision metric is 20, and no 1 mV delay can be measured. Zero CMP-15 excursions cannot qualify undecided outputs. The feedback keeper direction is rejected; no noise/MC or broader corner run is warranted.

| Corner | 1 mV ps | 30 mV ps | Reset ps | AVDD fJ | Wrong/failed decisions | Decided / 36 | Max terminal V | Failed pairs / 57 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | absent | 123.798614 | 30.918225 | 293.831230 | 20 | 8 | 0.92959 | 0 |
| ff_high_m40 | absent | 103.065093 | 23.630200 | 392.283491 | 20 | 8 | 1.02243 | 14 |
| ff_high_125 | 124.910324 | 60.613426 | 27.130324 | 485.268774 | 0 | 32 | 1.02414 | 14 |
| ss_low_125 | 174.421516 | 99.308927 | 42.987047 | 217.801355 | 4 | 24 | 0.83659 | 0 |

The screen checked all 57 terminal pairs over each full trace. A local console-print KeyError occurred because the failed TT decision had no 1 mV delay field. All four simulator jobs had already completed successfully and raw data had been fetched. Analysis was resumed from those exact files, with missing delay retained as absent; no simulation was repeated. Raw/source/deck hashes were verified before exact-owned remote cleanup. Commands used +aps with no ++aps or explicit +mt; logs disabled multithreading and actual job peak was 3. Canonical sources and official records remain unchanged.
