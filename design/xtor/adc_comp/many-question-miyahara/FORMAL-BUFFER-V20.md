# Official validation: BUFFER-V20

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

The [genuine result JSON](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-miyahara/tt_nom_27.json) retains its original clean-source metadata.

The run uses +aps with no explicit +mt; execution logs retain the actual threading evidence. Fetched raw/deck hashes match the owned remote run, now absent. Archive SHA-256 `75f2b4097cbe8bc3b43cf080290b29fe897dccb5fc052ca27eab6f226ea00941` preserves byte-exact result/figure snapshots and every retained audit, verified by reading every member back with CRC and SHA-256 checks.

At this checkpoint, 1 of 96 official records match this source and 95 retain older source hashes. Source matching does not imply passing. The next gate is the original complete TT noise test. Remaining-corner SOA, all formal coverage, mismatch, operating-range checks, mixed-top qualification and lead review remain open. No source is selected or qualified.
