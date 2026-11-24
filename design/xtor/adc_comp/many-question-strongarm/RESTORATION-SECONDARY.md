# Historical l16t3c1: current-rule screening

Frozen historical source, with no electrical edits. UTF-8 LF source SHA-256 `4c1417fb771024fc1c4568a2d0a1329d7031567df7edeccf5b4a9c34afaef44f`; electrical SHA-256 `56e3dddc5148fa35041f391de76c820e9e15927221bfc58dc79bea4bc7744577`. Historical dispatch text was byte-verified after reproducing the original CRLF-to-LF normalization. The source, current adc_comp 0.9.0 TB/deck and all measurements are retained privately; canonical circuit and formal results are unchanged.

| TT metric | Value |
|---|---:|
| tdelay_1mV_ps | 61.56277345045652 |
| tdelay_30mV_ps | 47.71403968897317 |
| treset_ps | 22.157642960118128 |
| validity_violations | 0 |
| loser_peak_pct | 15.598058449787503 |
| soa_pairs | 57 |
| soa_max_V | 0.98843 |
| energy_fJ | 203.492731932 |

All 36 actual decision directions (including 10 uV) and all 36 reset intervals are correct. The output-validity gate is separate from decision direction.

Four additional representative corners pass applicable delay/reset/CMP-15 and 1.1 V terminal stress. Across five corners all 180 decisions and resets are correct. The 50 ps 30 mV limit applies at TT; other 30 mV delays are reported only.

| Corner | 1 mV delay (ps) | 30 mV delay (ps) | Reset (ps) | Peak terminal V |
|---|---:|---:|---:|---:|
| fs_low_125 | 60.94492164941044 | 47.965740743566265 | 25.499179422630448 | 0.86447 |
| ss_low_125 | 79.48228504190989 | 61.207244403460294 | 29.05254681544481 | 0.88059 |
| ff_high_m40 | 47.363728262139546 | 36.72741184799997 | 17.430399421699146 | 1.08612 |
| sf_high_m40 | 69.45841146189919 | 51.87156183838869 | 19.32103158148344 | 1.09394 |

Dedicated TT Cin = 19.311701639827493 fF and CLKC = 7.256641126623195 fF pass. Net differential change after evaluation plus reset = 0.0001097096001285297 uV; this is not instantaneous decision disturbance. Actual loading reltol/vabstol = 1e-6/1e-8, conservative gear2only. Smallest baseline terminal margin is 6.06 mV at SF/high/-40.

Full physical FS/low/125 17 x 512 noise: **274.20498833482293 uV rms**, unrounded model-conditional 95% profile CI [264.5703918658524, 284.28656376278826] uV. All 8704 samples are finite with 512 at each level; seed 1 and 50 GHz noisefmax are retained. **FAIL 240 uV**. Stop TT-noise/full-corner/mismatch expansion and retain this source as rejected.

Runtime and archives (seconds; batch quantities include both TT sources where applicable):

| Batch | Own wrapper | Own Spectre elapsed / CPU | Upload | Execute | Fetch | Parse | Cleanup | Other guards | Runner elapsed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| soa11-secondary-tt | 27.0 | 22.5 / 12.8 | 21.516 | 63.094 | 44.031 | 1.968 | 21.047 | 122.399 | 274.055 |
| soa11-l16-loading | 33.0 | 29.1 / 13.4 | 21.531 | 54.907 | 43.234 | 0.156 | 21.046 | 121.858 | 262.732 |
| soa11-l16-corners | 16.0, 28.0, 15.0, 16.0 | 11.7 / 13.6, 23.8 / 13.5, 11.2 / 13.1, 11.6 / 13.5 | 21.563 | 81.171 | 45.532 | 4.625 | 21.047 | 121.819 | 295.757 |
| soa11-l16-noise-fs | 361.0 | 357.0 / 347.0 | 21.469 | 382.266 | 43.296 | 6.000 | 21.031 | 121.590 | 595.652 |

Execution includes solver wrapper plus orchestration; other guards include inventory/identity/hash/absence checks. Overlapping batches are not summed as wall time. Local archive verification and report generation were not instrumented. No simulation retries were needed.

- 20261101-045535-soa11-secondary-tt: `5d8efcd2de08f36612f7dba93896a48aded2265f449f1dcbd15529cda68630fa`.
- 20261101-050044-soa11-l16-loading: `a08e62a87d8fe68d63ab932ead56f60f9a4ff19a4c62bfae478530bff8b41744`.
- 20261101-050054-soa11-l16-corners: `179f65a36fa692e0bee140c946c6f605f51534668cf937c418bbb7c412b88de3`.
- 20261101-050500-soa11-l16-noise-fs: `eeb13f080b266e1da5929fcb27984530a968d798d14e9721a4eec03ca6c3835f`.

All listed archives passed CRC/member SHA verification and exact remote-path absence checks. Raw waveforms, failures and sources are retained; no source is promoted.
