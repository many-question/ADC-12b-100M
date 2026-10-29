# adc_clkgen candidate many-question

A 60-MOS static CMOS phase generator with feedback from the loaded PHI_B and CONV outputs. MOS gate loads shape internal voltage excursions; smaller output stages retain the current budget. All five RNL levels are complete, and the 19 used device geometries retain their callback verification.

**Status: wip.** The mixed-top SS low-voltage / 125 C ENOB failure remains open in [#35](https://github.com/many-question/ADC-12b-100M/issues/35). This candidate has not been selected or signed off.

Electrical content hash: `878752080031c251`. Current netlist SHA256: `7dbeabe408e25b960281545139f02c7e736807b30210db72edbed59cc81ce3bd`.

## Current module evidence

45/45 timing/SOA corners have current inputs after [#53](https://github.com/many-question/ADC-12b-100M/pull/53). All 46 module records have current inputs. The TT jitter input hashes are unchanged, so its existing result is retained.

Timing covers the complete 0–161 ns waveform: startup, eight 50% cycles, four 45% cycles and four 55% cycles, with 530 fF output load. Every current timing run checks 60 devices / 180 Vgs, Vgd and Vds pairs. CLK-10 uses the whole AVDD branch over 10–80 ns and applies only at TT.

Requested settings are 1 ps / traponly / conservative, reltol=1e-7 and vabstol=1e-8. The five representative comparisons change only maxstep to 0.5 ps. Their logs report effective transient reltol=1e-8, voltage abstol=1e-8 and lteratio=10; the complete waveforms confirm the respective maximum steps.

The table uses only records with current inputs; ranges describe the evaluated corners.

| Spec | Metric | Current value or range | Unit | Fresh coverage | Failures |
|---|---|---:|---|---:|---:|
| CLK-01 | td_s_ps | 28.9438986 to 49.3358605 | ps | 45/45 | 0 |
| CLK-02 | skew_sb_ps | 32.3964476 to 60.3045487 | ps | 45/45 | 0 |
| CLK-03 | nov_bc_ps | 51.8129726 to 86.8205253 | ps | 45/45 | 0 |
| CLK-04 | td_conv_ps | 113.153312 to 196.460932 | ps | 45/45 | 0 |
| CLK-05 | nov_cb_ps | 71.5851153 to 131.124127 | ps | 45/45 | 0 |
| CLK-06 | tf_s_ps | 8.05509429 to 12.6687664 | ps | 45/45 | 0 |
| CLK-07 | skew_ssb_ps | 4.12699066 to 6.47457617 | ps | 45/45 | 0 |
| CLK-08 | duty_errors | 0 | count | 45/45 | 0 |
| CLK-09 | jitter_fs | 41.3761389 | fs | 1/1 | 0 |
| CLK-10 | iavg_uA | 79.6718147 | uA | 1/1 | 0 |
| CLK-11 | soa_violations | 0 | count | 45/45 | 0 |

The timing results retain their actual clean source commits: `5c87359` (40 corners), `cef765f` (5 corners). All complete raw waveforms (8,694,913,518 bytes including convergence alternates) were audited locally and matched the remote SHA256 hashes before the exact owned run directories were removed. No new limiting corner required another convergence comparison.

The limiting CLK-07 corner moved from `sf_low_125` to `ss_low_125`, which is already covered by the five convergence comparisons.

## Representative convergence checks

The five primary runs and five alternate runs were simulated from clean commit `cef765f`, then migrated with their original provenance. All applicable metrics pass in both runs; each run has zero SOA violations over all 180 pairs.

| Corner | Largest absolute change of any pair peak (uV) | Primary / alternate worst peak (V) |
|---|---:|---:|
| fs_high_27 | 0.300591 | 0.999686196530 / 0.999686190622 |
| ss_high_125 | 0.517178 | 0.999926114761 / 0.999926104455 |
| ss_high_m40 | 0.810857 | 0.999807377060 / 0.999807636281 |
| ss_low_125 | 0.347342 | 0.818803991939 / 0.818803969951 |
| tt_nom_27 | 0.279965 | 0.908202871022 / 0.908202870113 |

These peak differences come from the same complete raw waveforms without rounding. The official, rounded `meta.crosscheck` remains unchanged. The largest change divided by the corresponding pair's closer voltage margin is 0.135% across the five comparisons. The limiting SS high-voltage / 125 C primary peak is 0.999926114761 V, leaving 73.885239 uV; its alternate changes by only -0.010306 uV. No voltage or duration waiver is used.

## Preserved private top-level evidence

The seven-corner mixed-top run `20261029-001710-fcf5-tb_top_sine` used the same electrical circuit from clean `75e7a0f` on main `11fe593`, with the other blocks behavioral. All seven returned rc=0 with complete capture indices and zero missing RDY in the required records. Six corners pass all applicable metrics. SS low-voltage / 125 C fails TOP-01: **ENOB 10.348264814 < 10.5 bit**.

The matched all-behavioral SS control `20261029-013758-current-behav-ss-0059c9` also fails: **ENOB 10.324003109 bit**. Seventeen common source inputs, parameters, globals and seed were matched. This single-seed comparison does not isolate a noise contribution or waive the mixed-top failure. [Comparison and provenance](https://github.com/many-question/ADC-12b-100M/issues/35#issuecomment-6476475531).

The #50 redraw used the official periodic-Hann implementation and preserved every metric and raw hash. #53 and this directory migration do not change top or jitter electrical inputs. Original private captures, summaries and simulation provenance are retained; public top results are not part of this candidate.

## Migration and history

The official `migrate-candidate` operation preserves all 46 original result metrics, verdicts, `meta.git`, `meta.git_clean` and content hashes, remaps the source keys and records `meta.migrated`. All 91 evidence PNGs were byte-identical at migration. The sole netlist text edit is the RNL package path comment (`../../rnl/adc28.rnl` to `../../../rnl/adc28.rnl`); its electrical hash is unchanged. The original netlist SHA256 is `a7dce7b4cb6a47787aa9b27d3df676c2464ec22976025de396640c359b0e79b7`.

Published tags under `history/adc_clkgen/` retain `legacy-before-candidates`, `legacy-before-numerics53`, `legacy-before-main50`, `legacy-before-main43` and `legacy-52mos-soa-failure`. Earlier failures and old numerical settings remain historical evidence.

Acknowledged notices: [#18](https://github.com/many-question/ADC-12b-100M/issues/18), [#27](https://github.com/many-question/ADC-12b-100M/issues/27), [#29](https://github.com/many-question/ADC-12b-100M/issues/29), [#49](https://github.com/many-question/ADC-12b-100M/issues/49).
