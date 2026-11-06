# Official validation: BUFFER-V20

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

**Old-settings records:** [issue #94](NUMERICS-94.md) requires new-settings revalidation. All results here preserve the original source and numerical protocol. The sub-microvolt kickback value is not an established physical conclusion; the earlier expansion plan below is superseded by private prechecks and formal reruns after merge.

Canonical electrical SHA-256 is `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. Only genuine runs through the unchanged original runner update formal records. Fine-step deterministic screens and shorter phase diagnostics remain supplemental.


## Original run 20261031-113139-5118-tb_comp_kickback

Actual clean source commit: `b60845b1101f1e27319fed36fdc2447b323f5b1f`. The canonical view, original testbench, sampler, numerical settings, measurement and recorder are unchanged. The private wrapper only accounts for resources, directs temporary data to SSD, verifies retrieved hashes and removes the exact owned run.

### tt_nom_27: PASS

| Metric | Measured | Limit |
|---|---:|---:|
| Input capacitance per input | 19.328731219 fF | 20 fF |
| CLKC input capacitance | 11.287775424 fF | 16 fF |
| Differential kickback | 0.004586038 uV | 40 uV |

This formal capacitance result is separate from the mixed-delay clock-charge diagnostic.

The [genuine result JSON](https://github.com/many-question/ADC-12b-100M/blob/a1d163133ac6c59acdc2ed46523023e16c80949e/results/adc_comp/tb_comp_kickback/xtor-many-question-miyahara/tt_nom_27.json) retains its original clean-source metadata.

The run uses +aps with no explicit +mt; execution logs retain the actual threading evidence. Fetched raw/deck hashes match the owned remote run, now absent. Archive SHA-256 `75f2b4097cbe8bc3b43cf080290b29fe897dccb5fc052ca27eab6f226ea00941` preserves byte-exact result/figure snapshots and every retained audit, verified by reading every member back with CRC and SHA-256 checks.

At this checkpoint, 1 of 96 official records match this source and 95 retain older source hashes. Source matching does not imply passing. The next gate is the original complete TT noise test. Remaining-corner SOA, all formal coverage, mismatch, operating-range checks, mixed-top qualification and lead review remain open. No source is selected or qualified.


## Original run 20261031-114009-5475-tb_comp_noise

Actual clean source commit: `2b1190fab874bd1324fa44abb7a8ff8c480e7c7b`. The canonical view, original testbench, sampler, numerical settings, measurement and recorder are unchanged. The private wrapper only accounts for resources, directs temporary data to SSD, verifies retrieved hashes and removes the exact owned run.

### tt_nom_27: PASS

The original 17 input levels, 512 decisions per level, 50 GHz bandwidth, seed 1 and Gaussian-CDF fit are retained. All 8704 samples are finite, with exactly 512 per level and no omitted or out-of-sequence samples.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Input-referred noise | 191.159437353 uV rms | 200 uV | PASS |
| Noise 95% profile interval | 183.31 to 199.41 uV | — | reported |
| Absolute systematic offset | 0.000545420 mV | 2 mV | PASS |

The minimum sampled absolute output difference is 0.873759109 V. Largest standardized Gaussian-fit residual is 1.996061; intervals and residuals are conditional on that model. The original outputstart=tstop waveform does not establish reset history or full-trace terminal stress. Separate private full-trace checks are retained.

| Input uV | OUTP / 512 |
|---:|---:|
| -800 | 0 |
| -700 | 0 |
| -600 | 0 |
| -500 | 1 |
| -400 | 10 |
| -300 | 35 |
| -200 | 71 |
| -100 | 136 |
| 0 | 278 |
| 100 | 355 |
| 200 | 444 |
| 300 | 477 |
| 400 | 500 |
| 500 | 509 |
| 600 | 512 |
| 700 | 512 |
| 800 | 512 |

![Original noise curve and residual](https://raw.githubusercontent.com/many-question/ADC-12b-100M/a1d163133ac6c59acdc2ed46523023e16c80949e/results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/tt_nom_27.noise.png)

The [genuine result JSON](https://github.com/many-question/ADC-12b-100M/blob/a1d163133ac6c59acdc2ed46523023e16c80949e/results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/tt_nom_27.json) retains its original clean-source metadata.

The run uses +aps with no explicit +mt; execution logs retain the actual threading evidence. Fetched raw/deck hashes match the owned remote run, now absent. Archive SHA-256 `670a0852afeab4d946dc9b712b26e1b741ebfea8f85b0771b3b406173f501b9c` preserves byte-exact result/figure snapshots and every retained audit, verified by reading every member back with CRC and SHA-256 checks.

At this checkpoint, 2 of 96 official records match this source and 94 retain older source hashes. Source matching does not imply passing. This is preserved old-settings evidence. Issue #94 supersedes the previous expansion plan: new-settings private prechecks come first; required formal reruns will use the merged official flow. No further old-settings full-corner qualification is being launched. Remaining-corner SOA, all formal coverage, mismatch, operating-range checks, mixed-top qualification and lead review remain open. No source is selected or qualified.

Historical result and figure links are pinned to byte-verified published commit `a1d163133ac6c59acdc2ed46523023e16c80949e` so future genuine runs cannot change the evidence shown by this report.
