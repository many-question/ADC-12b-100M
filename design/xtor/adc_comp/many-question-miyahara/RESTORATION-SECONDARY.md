# Historical r0t3c1: current-rule screening

Frozen historical source, with no electrical edits. UTF-8 LF source SHA-256 `96ac36380266059b7b02a3b3ccf7e5844e2d6c74ca10229d60cb7ee5cf313511`; electrical SHA-256 `fc3a55e2b23375a0d7661e0b6f1b7df5cbc3f332624462e66b37735aebacb838`. Historical dispatch text was byte-verified after reproducing the original CRLF-to-LF normalization. The source, current adc_comp 0.9.0 TB/deck and all measurements are retained privately; canonical circuit and formal results are unchanged.

| TT metric | Value |
|---|---:|
| tdelay_1mV_ps | 47.69161879160601 |
| tdelay_30mV_ps | 38.88993683020809 |
| treset_ps | 14.009674322999338 |
| validity_violations | 24 |
| loser_peak_pct | 48.65117985640362 |
| soa_pairs | 63 |
| soa_max_V | 0.92516 |
| energy_fJ | 186.457192668 |

All 36 actual decision directions (including 10 uV) and all 36 reset intervals are correct. The output-validity gate is separate from decision direction.

**CMP-15 FAIL: 24 cycles have losing-output peaks at or above 0.3 VDD**, reaching 48.65117985640362% VDD. Neither output pair crosses 0.5 VDD simultaneously in these violations, but the 0.3 VDD loser limit is already binding. Violations span +/-3 mV through +/-10 uV in both repetitions. This historical source exposes the regenerative output directly and has no B2-style physical isolation buffer; correct winner polarity does not make its common-mode excursion acceptable. Noise/loading/full-corner/MC expansion stops. Any future redesign must restore a physical output interface and is a new frozen source.

Runtime and archives (seconds; batch quantities include both TT sources where applicable):

| Batch | Own wrapper | Own Spectre elapsed / CPU | Upload | Execute | Fetch | Parse | Cleanup | Other guards | Runner elapsed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| soa11-secondary-tt | 15.0 | 10.6 / 12.3 | 21.516 | 63.094 | 44.031 | 1.968 | 21.047 | 122.399 | 274.055 |

Execution includes solver wrapper plus orchestration; other guards include inventory/identity/hash/absence checks. Overlapping batches are not summed as wall time. Local archive verification and report generation were not instrumented. No simulation retries were needed.

- 20261101-045535-soa11-secondary-tt: `5d8efcd2de08f36612f7dba93896a48aded2265f449f1dcbd15529cda68630fa`.

All listed archives passed CRC/member SHA verification and exact remote-path absence checks. Raw waveforms, failures and sources are retained; no source is promoted.
