# V32 method runtime ledger

All times below are measured seconds; runner elapsed is run-ID timestamp to final receipt mtime. Parallel batches overlap: sums are resource/accounting totals, not campaign wall time. Execute includes wrapper plus orchestration; analysis timers are nested in Spectre totals and must not be added to them. Local archive creation/readback and report preparation were not instrumented.

| Batch suffix | Jobs | Upload | Execute | Fetch/unpack | Parse | Cleanup | Other guards | Runner elapsed | Sum wrapper | Sum Spectre elapsed | Sum Spectre CPU |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v32-pss-orbit | 2 | 21.469 | 58.484 | 44.469 | 0.015 | 21.562 | 122.516 | 268.515 | 36.000 | 28.500 | 26.200 |
| v32-sampled-phase70 | 6 | 21.734 | 74.297 | 47.375 | 0.093 | 21.110 | 124.700 | 289.309 | 98.000 | 72.300 | 77.100 |
| v32-sampled-probe | 2 | 21.406 | 64.484 | 50.657 | 0.015 | 21.390 | 123.562 | 281.514 | 43.000 | 34.400 | 51.100 |
| v32-sampled-convergence | 14 | 21.515 | 144.360 | 199.812 | 0.094 | 21.063 | 140.985 | 527.829 | 279.000 | 217.800 | 425.400 |
| sampled-noise-rc-calibration | 1 | 21.407 | 30.312 | 45.547 | 0.000 | 21.063 | 121.622 | 239.951 | 8.000 | 4.120 | 11.100 |
| v32-sampled-sensitivity | 12 | 21.422 | 262.094 | 63.328 | 0.156 | 21.047 | 123.066 | 491.113 | 423.000 | 374.100 | 1324.100 |
| v32-sensitivity-fd | 12 | 21.438 | 151.265 | 51.875 | 0.062 | 21.078 | 123.893 | 369.611 | 221.000 | 172.500 | 190.000 |
| v32-settling-fine | 4 | 21.406 | 221.828 | 60.860 | 0.047 | 21.031 | 122.117 | 447.289 | 287.000 | 268.700 | 269.100 |

Observed interval from first method dispatch to last final receipt: 2091.289 s; it includes inter-batch analysis/preparation gaps and overlapping design work, so it is not dedicated solver time. Sum of runner durations: 2915.131 s. Total jobs: 53.

Two initial PXF jobs failed with SPCRTRF-15162 (missing sampleprobe), costing TT/FS wrapper 14/15 s and Spectre elapsed 10.3/10.2 s. Corrected jobs are a separate batch. The high 199.812 s fetch time in the convergence batch includes 1913 archived files. Later PXF requests retain only sideband zero; PNoise folding is unchanged. APS was enabled with no explicit thread-count setting; CPU/elapsed values show internal parallelism for some analyses.

- 20261101-042239-v32-pss-orbit: `a85a2629614d43d54ba4486aafbd0e6274109facb6cc10d7dd245a065790f121` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-042737-v32-sampled-phase70: `457b81f240e4ea112e4482a4cd7993dfbd5a719a9a1e94a902308bcd44e6966c` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-043148-v32-sampled-probe: `917c0b9f3351b10b2b5b79892d4ac629f8ef875e471f6ab97e7e577388f5f36e` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-043609-v32-sampled-convergence: `dc9a7eecf5286b88f56aedb1bb61abc4bbf9c7cbe0cd83a839d2f1057ab3f5f2` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-043809-sampled-noise-rc-calibration: `8ebec4a4f9b3dc24784e4340f902747469126b685468a1c8c4ec9996d3f22a10` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-044409-v32-sampled-sensitivity: `5d50735ec979b59a46ed41b6808a34a5580f8e1043fd6c76bbddaf6ba7551698` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-044715-v32-sensitivity-fd: `1d00acd4993855c387776888a05d03e32d791aa583763369b202cf548e5b4110` (CRC/member SHA verified, exact remote absence confirmed).
- 20261101-045003-v32-settling-fine: `aedb0140e305ae36fa18578fa820f5645962b7c176d3efff452aa056eca0008f` (CRC/member SHA verified, exact remote absence confirmed).
