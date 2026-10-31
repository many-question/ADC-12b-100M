# Official adc_comp 0.8.0 validation

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

These are genuine canonical-view runs through the merged official runner, testbench, measurement and recorder. Each section names the actual simulated source and links byte-verified committed results. Failures remain evidence; no all-corner qualification is implied.

[Formal notice #100](https://github.com/many-question/ADC-12b-100M/issues/100) is acknowledged. Its required settings match the original run below; the later acknowledgement does not change the actual simulated source. The isolated runtime also passes the exact [#96 installation self-check](https://github.com/many-question/ADC-12b-100M/issues/96): `79.999999999274` dB, consistent with 80.00 dB. Official measurements remain those produced by the merged flow. The stated adjacent-spur SNDR limitation is retained; the installation self-check is not comparator performance evidence.


## Original run 20261031-125734-f562-tb_comp_noise

Variant `BUFFER-V20`, actual clean simulation source `8692cc3f774f618ae68791a90fbfa92a5fa4f545`, electrical SHA-256 `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The recorded JSON and figures are preserved at result commit `06df501d9d0894bbd3ea41e8be136ae03e8b5e96`. The wrapper makes no numerical, source, testbench, sampler, measurement or recorder overrides; it only validates provenance, accounts for resources and preserves evidence.

### fs_low_125: FAIL: CMP-13

Noise `343.4944014285115` uV rms; 95% profile interval `[332.03, 355.53]` uV; absolute offset `0.005967230596725428` mV. All 8704 finite samples are retained, exactly 512 at each of 17 levels. Minimum sampled output magnitude is `0.7853706958079` V and maximum absolute standardized Gaussian-fit residual is `1.454284767070063`.

- CMP-13: 343.4944014285115, <= 240, FAIL.
- CMP-02: 0.005967230596725428, <= 2, PASS.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 3 |
| -700 | 7 |
| -600 | 20 |
| -500 | 42 |
| -400 | 72 |
| -300 | 98 |
| -200 | 142 |
| -100 | 194 |
| 0 | 276 |
| 100 | 333 |
| 200 | 373 |
| 300 | 405 |
| 400 | 451 |
| 500 | 470 |
| 600 | 491 |
| 700 | 501 |
| 800 | 509 |

Actual Spectre log: gear2only, conservative, reltol 0.0001, vabstol 1e-06 V, relref alllocal, lteratio 10. The original deck has no explicit maxstep or method override. APS has no explicit thread-count override; actual thread use is retained in the execution audit.

The Gaussian-CDF interval and residuals are model-conditional. The original outputstart=tstop waveform cannot establish full reset coverage or whole-transient terminal stress; those require separate checks.

[Exact original record](https://github.com/many-question/ADC-12b-100M/blob/06df501d9d0894bbd3ea41e8be136ae03e8b5e96/results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/fs_low_125.json)

![Original noise evidence](https://raw.githubusercontent.com/many-question/ADC-12b-100M/06df501d9d0894bbd3ea41e8be136ae03e8b5e96/results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/fs_low_125.noise.png)

Raw data, original staged source/deck, original results/figures and diagnostics are preserved in archive SHA-256 `eff1264f038ec86dbf56e337b531c2e22f627d5fc795ef21219e5a087f015d6d`. Every entry was read back with CRC and SHA-256 verification; the exact owned remote run is absent. The isolated runtime verifies installed ADCToolbox commit `cd72061ff3b7a977163dac540da126ae22f5e38d`. No old/private record was relabeled.

At this checkpoint, 1 of 96 formal records have current dependency hashes; 95 are stale. Freshness is independent of passing. Known failures stop broader qualification expansion while physical design continues.
