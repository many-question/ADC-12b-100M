# Completed combined energy and output-validity refresh

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

Completed against comparator spec v0.7.0, including merged PR #82 (`a95aa0c`), notices [#78](https://github.com/many-question/ADC-12b-100M/issues/78) and [#84](https://github.com/many-question/ADC-12b-100M/issues/84). The clean simulated source is `a2e3509597563d607d2a873ed9cc5e9d667ccfff`. Main was merged to preserve original clean source commits and historical result commits.

| Test | Current records | Fresh | Stale | Action |
|---|---:|---:|---:|---|
| tb_comp_delay | 45 | 45 | 0 | 45 new physical simulations, current official meter and validity extraction |
| tb_comp_kickback | 45 | 45 | 0 | Preserved byte-for-byte |
| tb_comp_noise | 1 | 1 | 0 | Preserved byte-for-byte |
| tb_comp_offset_mc | 1 | 1 | 0 | Preserved byte-for-byte, 50 valid samples |

Before refresh, the current dependency checker identified only the 45 delay records as stale: `tb/comp/tb_comp_delay.scs` changed from `c9bbdac040c91a1f` to `ca754d0b9373b04c`. All other 47 records remain valid against their actual reached dependencies, and their 139 JSON/PNG files match the before-run SHA-256 snapshot. They were neither rerun nor rehashed.

Seven completed corners were retained in the original staged run. At a completed-job boundary the local per-corner dispatcher was stopped, and only the remaining 38 corners were dispatched serially on the server. No completed corner was rerun. Each original staged testbench and deck was compared exactly with the current official generator. All 45 records use the current official measurement/record APIs, with the real original clean source. Their execution metadata identifies original versus continued dispatch and the actual deck, waveform and rc-file SHA-256 per corner. The batch wall time includes the dispatch pause; it is not summed across JSONs.

All 45 jobs completed with rc=0 and no simulator ERROR. Current official measurement produced 36 evaluation intervals and 36 losing-peak entries in every record. Actual remote output files and staged inputs were retrieved and matched against server SHA-256 before the exact owned run directory was removed. Private raw archives retain original inputs, logs, numerical settings, measurements and dispatch provenance; private site paths and PDK data are not published.

Electrical SHA-256 is unchanged: `e8a0e3d3dc1366cd20f72c291397b352c8b9a6eeb87df618e41c49199372597a`. The earlier v0.5.0 JSONs and figures remain in Git history, and their private raw archives remain intact. The new results are freshly measured evidence under the new definition, not a metadata-only refresh of old evidence.

The current failure baseline is 45/45 CMP-15-failing corners (1084/1620 cycles), 0/45 reset-failing corners and the preserved fine-step SOA failures. [VALIDITY.md](VALIDITY.md) gives every corner/cycle and the priority structural direction. The candidate remains WIP and unselected.
