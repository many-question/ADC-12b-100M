# Independent numerical supplement to PR #106

Reviewed result commit: [`0cfb540`](https://github.com/many-question/ADC-12b-100M/pull/106). Circuit electrical hash: `f9330137569bdf81`.

**Status:** the applicable electrical limits and source-consistency checks pass. Numerical-evidence interpretation and reproducible-source confirmation are being handled in [the PR discussion](https://github.com/many-question/ADC-12b-100M/pull/106#issuecomment-6539813568). This candidate-author supplement is not a lead verification record or mixed-top qualification. No duplicate full-results PR or further duplicate full-corner batch is planned.

## Public-record audit

All 90 records at the reviewed commit were read and re-judged with the unchanged official flow: 45 DC and 45 tracking, no stale/error records, 317 applicable limited specification/corner passes, and the required reported BST-07 value. Prepared parameters and globals, reachable dependencies, candidate hash, clean recorded source, APS mode, actual primary numerics, and the prescribed crosscheck settings and arithmetic agree. Each DC JSON has all 21 devices / 63 terminal pairs, with no recorded voltage violation.

The public records report clean source `c6152d2`, conservative, gear2only, relref=alllocal and lteratio=10. DC uses effective reltol=1e-6 and default voltage tolerance; tracking uses effective reltol=1e-7 and 10 nV. Neither official primary testbench explicitly sets maxstep. Prescribed comparisons retain conservative and use traponly / 1 ps; the DC alternate has effective reltol=1e-8 and 10 nV.

The reviewed PR contains eight DC crosschecks (TT, FF-low-hot, FF-high-hot, FS-high-hot, FS-high-cold, SS-high-cold, SS-low-hot and SS-low-cold) and three tracking crosschecks (FF-high-hot, SS-low-hot and SS-low-cold).

## Independent repeatability

Nine independently rerun primary records have exactly identical complete metrics to their PR #106 counterparts: six DC and three tracking. All eight shared crosschecks have identical requested settings, actual numerics, metric values/differences and sample comparisons; the six DC comparisons also have identical recorded SOA summaries. This compares values, without rewriting the different original Git/date or runtime provenance. The independent TT tracking crosscheck is additional evidence outside PR #106.

| DC corner | Primary turn-off (ps) | Alternate turn-off (ps) | Primary turn-on (ps) | Alternate turn-on (ps) |
|---|---:|---:|---:|---:|
| ff_high_125 | 35.784500652 | 35.807431072 | 144.739348311 | 143.502689993 |
| ff_low_125 | 41.209575828 | 40.947852315 | 167.276904988 | 167.614319045 |
| fs_high_125 | 39.370808784 | 39.348446482 | 171.599150825 | 169.719570153 |
| ss_low_125 | 59.602078035 | 59.524580635 | 222.850690289 | 220.429607173 |
| ss_low_m40 | 55.366460976 | 55.423499298 | 231.272349235 | 229.944229313 |
| tt_nom_27 | 41.413486024 | 41.379383591 | 157.825677012 | 156.666046925 |

| Tracking corner | SFDR primary / alternate (dBc) | SNDR primary / alternate (dB) |
|---|---:|---:|
| ss_low_125 | 84.999742997 / 85.102349812 | 84.700539890 / 84.764205017 |
| ss_low_m40 | 88.157280937 / 87.846066829 | 84.650908110 / 84.497773215 |
| tt_nom_27 | 90.623188629 / 90.761905704 | 88.707698506 / 88.755597605 |

## BST-03 sensitivity and evidence interpretation

| SS-low-hot quantity | Value |
|---|---:|
| Primary turn-off | 59.60207803534621 ps |
| Prescribed crosscheck | 59.52458063508565 ps |
| Absolute difference | 0.07749740026056 ps |
| Primary margin to 60 ps | 0.39792196465379 ps |
| Difference / primary margin | 19.475527% |

Both settings pass the electrical limit. This ratio describes sensitivity and introduces no new threshold. [Verification section 2](https://github.com/many-question/ADC-12b-100M/blob/c6152d236e525793ecc4809b9a6c9dfb9fd0ad77/docs/verification.md) requires cross-setting differences to be negligible relative to margin. This supplement requests the maintainer's interpretation; it does not automatically call 19.4755% negligible or reclassify the result as an electrical failure.

## Full-transient unrounded SOA scope

The independent TT and five DC risk-corner pairs cover 12 complete saved transients from 0 to 290 ns: 21 MOS and 63 gs/gd/ds pairs per run, 756 unrounded peak checks and 378 primary/alternate pair comparisons. Every saved point was included. The largest absolute peak in this scope is **0.9986832482812585 V**, FS-high-hot, MPRE gd. All five risk alternates and the TT alternate have no saved interval over 1 ps beyond floating-point tolerance; the unconstrained primaries have largest saved intervals of about 1.530–1.599 ns.

| Corner | Device/pair | Primary peak (V) | Alternate peak (V) | Difference / smaller margin |
|---|---|---:|---:|---:|
| ss_low_m40 | XDUT.MTRK ds | 0.996925556018503 | 0.996974146832296 | 1.605855% |
| ss_low_m40 | XDUT.MAUX ds | 0.996925556018503 | 0.996974146832296 | 1.605855% |
| tt_nom_27 | XDUT.MDMID ds | 0.977724923225303 | 0.977999302572467 | 1.247139% |

Within these six independently audited DC corners, no per-pair peak difference exceeds the smaller remaining voltage margin, as occurred in the clkgen evidence discussed in #103. This statement is scoped to these raw audits. Reading all 45 complete rounded public SOA tables is a separate check and is not a claim that this reviewer independently opened all 45 project-side raw traces.

## Sources and retained evidence

| Independent batch | Frozen source commit | Simulations | Peak jobs | Returned files |
|---|---|---:|---:|---:|
| 20261031-125329-6cae-tb_bootstrap_dc | [`c6152d2`](https://github.com/many-question/ADC-12b-100M/commit/c6152d236e525793ecc4809b9a6c9dfb9fd0ad77) | 2 | 1 | 16 |
| 20261031-130102-3b4b-tb_bootstrap_track | [`c6152d2`](https://github.com/many-question/ADC-12b-100M/commit/c6152d236e525793ecc4809b9a6c9dfb9fd0ad77) | 2 | 1 | 14 |
| 20261031-132356-3e6e-tb_bootstrap_dc | [`9bd1048`](https://github.com/many-question/ADC-12b-100M/commit/9bd104867af7cb04dcfb140fb68d77d87e8c11a5) | 10 | 6 | 80 |
| 20261031-134147-9abf-tb_bootstrap_track | [`a3c6137`](https://github.com/many-question/ADC-12b-100M/commit/a3c61377397f2d3369227a29352e20bd23cca6ee) | 4 | 3 | 28 |

All batches used +aps, no explicit +mt, and logs state multithreading was disabled for the small circuit, establishing one solver thread per simulation. OS thread counts are distinct. The session job ceiling was six. The first serial TT DC batch had failed process-monitor probes; its peak of one is established by the serial runner and completed logs, not a zero-job observation. Later batch peaks were directly observed. Those probe errors remain in the original private state.

Each batch retained its original official result JSON, source/driver snapshot, logs, captures, inputs and per-file SHA256 values. Transport hashes were verified before removing its unique remote run directory. The completed risk-DC archive was additionally checked member-by-member and for gzip CRC before releasing only its ten extracted raw duplicates; original bytes remain in the archive. Raw data and site information stay private.

| Batch | Original evidence archive SHA256 |
|---|---|
| 20261031-125329-6cae-tb_bootstrap_dc | `e4b3ac10354633b09d0678fac0322893be0fae0e6d1d19e39183f2f3ed2509f6` |
| 20261031-130102-3b4b-tb_bootstrap_track | `8413a7d68cf8ae607385596f3d9dd6a8eda8a9cfae8ea7dee5181c2238bfca98` |
| 20261031-132356-3e6e-tb_bootstrap_dc | `b3c00c29aa0f19a1f681459d8d02b688afc92d903a53571afe021fc3a07ea2c5` |
| 20261031-134147-9abf-tb_bootstrap_track | `42e28c25be535f196988fc67c47ade377e98955a57ca98535d8a9c3074a8f9a9` |

The fixed private JSON review snapshot covering all 90 public records, all nine overlaps and all 378 unrounded pair comparisons has SHA256 `daee2a2fee5934abc4e6c5792eecd8fae3604050c543cdc8b9b544028c23ca65`. It and the underlying evidence can be supplied for authorized reproduction.

## Dependency and source confirmation

The official dependency declaration pins ADCToolbox to `cd72061ff3b7a977163dac540da126ae22f5e38d`. The independent isolated environment verified that installed full Git revision and reproduced #96: SFDR 79.99999999927381 dB (80.00 dB). Its SNDR is 80.79195722958374 dB, consistent with the documented adjacent-spur limitation; the official measurement was not patched.

The project-side public JSON records the expected short commit/version label. That label is emitted by a constant in `adcflow.spectrum.PROVENANCE`; by itself it is not an attestation of the installed runtime revision. The PR discussion requests reproducible-source confirmation: direct_url or source checksum plus the #96 self-check, and whether original waveform archive hashes and full-terminal-pair audit material are available for authorized review. Private provision is sufficient; no PDK or raw upload to the public repository is requested. The scope of materials not yet inspected here is not a claim that they do not exist.

Prior lead verification and mixed-top qualification remain historical. The formal result entry is PR #106; this supplement keeps its own original provenance and leaves the PR author's sources and results unchanged.
