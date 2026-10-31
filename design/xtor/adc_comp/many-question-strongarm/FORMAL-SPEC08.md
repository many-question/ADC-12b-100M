# Official adc_comp 0.8.0 validation

These are genuine canonical-view runs through the merged official runner, testbench, measurement and recorder. Each section names the actual simulated source and links byte-verified committed results. Failures remain evidence; no all-corner qualification is implied.

[Formal notice #100](https://github.com/many-question/ADC-12b-100M/issues/100) is acknowledged. Its required settings match the original run below; the later acknowledgement does not change the actual simulated source. The isolated runtime also passes the exact [#96 installation self-check](https://github.com/many-question/ADC-12b-100M/issues/96): `79.999999999274` dB, consistent with 80.00 dB. Official measurements remain those produced by the merged flow. The stated adjacent-spur SNDR limitation is retained; the installation self-check is not comparator performance evidence.


## Original run 20261031-125724-e0ac-tb_comp_noise

Variant `RESET-V27`, actual clean simulation source `e4e941abe120c230ce391cde0cbfd4ab9cd59121`, electrical SHA-256 `7b20b19a2434da94d732f9785a3a8f1a2138d17ed4f4854dbdc5ab1a6cff18df`. The recorded JSON and figures are preserved at result commit `9852ae5003232b10ec733336e89ff0fa73243980`. The wrapper makes no numerical, source, testbench, sampler, measurement or recorder overrides; it only validates provenance, accounts for resources and preserves evidence.

### tt_nom_27: FAIL: CMP-01

Noise `210.1008609253812` uV rms; 95% profile interval `[201.81, 218.79]` uV; absolute offset `0.005125216450116011` mV. All 8704 finite samples are retained, exactly 512 at each of 17 levels. Minimum sampled output magnitude is `0.8997415767549` V and maximum absolute standardized Gaussian-fit residual is `3.4462251318913335`.

- CMP-01: 210.1008609253812, <= 200, FAIL.
- CMP-13: 210.1008609253812, <= 240, PASS.
- CMP-02: 0.005125216450116011, <= 2, PASS.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 2 |
| -400 | 13 |
| -300 | 38 |
| -200 | 89 |
| -100 | 143 |
| 0 | 290 |
| 100 | 343 |
| 200 | 406 |
| 300 | 470 |
| 400 | 495 |
| 500 | 506 |
| 600 | 512 |
| 700 | 512 |
| 800 | 512 |

Actual Spectre log: gear2only, conservative, reltol 0.0001, vabstol 1e-06 V, relref alllocal, lteratio 10. The original deck has no explicit maxstep or method override. APS has no explicit thread-count override; actual thread use is retained in the execution audit.

The Gaussian-CDF interval and residuals are model-conditional. The original outputstart=tstop waveform cannot establish full reset coverage or whole-transient terminal stress; those require separate checks.

[Exact original record](https://github.com/many-question/ADC-12b-100M/blob/9852ae5003232b10ec733336e89ff0fa73243980/results/adc_comp/tb_comp_noise/xtor-many-question-strongarm/tt_nom_27.json)

![Original noise evidence](https://raw.githubusercontent.com/many-question/ADC-12b-100M/9852ae5003232b10ec733336e89ff0fa73243980/results/adc_comp/tb_comp_noise/xtor-many-question-strongarm/tt_nom_27.noise.png)

Raw data, original staged source/deck, original results/figures and diagnostics are preserved in archive SHA-256 `19b0deda49f6e53d8eafe8bf1253318697550b4cf1a6f1d88b9b04ecd8c14277`. Every entry was read back with CRC and SHA-256 verification; the exact owned remote run is absent. The isolated runtime verifies installed ADCToolbox commit `cd72061ff3b7a977163dac540da126ae22f5e38d`. No old/private record was relabeled.

At this checkpoint, 1 of 92 formal records have current dependency hashes; 91 are stale. Freshness is independent of passing. Known failures stop broader qualification expansion while physical design continues.
