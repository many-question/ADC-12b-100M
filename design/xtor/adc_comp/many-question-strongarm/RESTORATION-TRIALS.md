# Isolated physical restoration trials

Each frozen revision changes one symmetric device pair from the original V2/B2 source, preserving physical output isolation and full device noise. These private screens do not promote a canonical circuit or replace formal results. The [mechanism report](RESTORATION-MECHANISM.md) motivated the changes but does not predict success.

## V2-C56

[Complete frozen source](RESTORE-V2-C56.txt), raw SHA-256 `6b6c7aecf59235f1fd3e6eb19f17b8b1096f50a2af69a3bb53c163368bd68391`; electrical SHA-256 `daa991386afa21c7a615c6bdee674c8b298e40303a2fb734c8be02ccbec2e9dc`. Parent restore-v2: `608dfd3e547ee65738662bf62ef9c9cb548b0b7ea1000b21c22087ee0c958db8`.

Only CDP/CDN MOM finger count changes from 48 to 56; callback nominal capacitance 16.46030 fF per node. Length, width, spacing, metal stack and multiplicity remain the parent values.

Callback receipt SHA-256 `c6778b1e6296559ad3dd87ad5289a2b4aea41d1cd6c60be66fc78a4241944f5c`. 28 nm HPC+ adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`; exact provider/release identity is retained in the private receipt. Ordered request: `[['Nfinger', '56'], ['Lfinger', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

| Kind / corner | Measured result |
|---|---|
| delay / tt_nom_27 | tdelay_1mV_ps=57.922747430769256, tdelay_30mV_ps=45.34740658599547, treset_ps=19.24002491897356, validity_violations=0, soa_max_V=0.95602, energy_fJ=153.54561049199998; limited gate PASS |
| delay / fs_low_125 | tdelay_1mV_ps=56.93389044118287, tdelay_30mV_ps=45.17450426045007, treset_ps=23.710937833033775, validity_violations=0, soa_max_V=0.86049, energy_fJ=155.37416500800003; limited gate PASS |
| delay / ss_low_125 | tdelay_1mV_ps=75.40844141551379, tdelay_30mV_ps=58.63601881341132, treset_ps=26.031970407259532, validity_violations=0, soa_max_V=0.86218, energy_fJ=142.5546085752; limited gate PASS |
| delay / ff_high_m40 | tdelay_1mV_ps=43.70358586483936, tdelay_30mV_ps=34.439893625728395, treset_ps=15.07084351064613, validity_violations=0, soa_max_V=1.04819, energy_fJ=172.9595062008; limited gate PASS |
| delay / sf_high_m40 | tdelay_1mV_ps=65.54298814130557, tdelay_30mV_ps=50.270603760503924, treset_ps=16.12440135547688, validity_violations=0, soa_max_V=1.04862, energy_fJ=170.04933071279999; limited gate PASS |
| kickback / tt_nom_27 | cin_fF=19.313134034315315, cin_clkc_fF=15.207198943660638, kickback_uV=0.00017268070003420566; PASS |
| noise / fs_low_125 | 315.26264313649045 uV rms; unrounded 95% profile CI [304.65758490716047, 326.3792557323575]; FAIL 240 uV, finite 17 x 512 samples |

A required gate fails: stop long-noise or further qualification expansion for this source.

Retained noise-off waveform markers (mean of four +/-100 uV cycles; exact saved traces and per-cycle values retained privately). These are descriptive thresholds, not gm/loop-gain activation points or individual noise contributions.

| Corner | Core reaches 1 mV: parent / trial (ps) | D differential at that event: parent / trial (mV) | Max saved D differential before that event: parent / trial (mV) |
|---|---|---|---|
| tt_nom_27 | 33.482846 / 34.297014 | 0.040920 / 0.022161 | 0.316247 / 0.317219 |
| fs_low_125 | 32.630726 / 33.290238 | 0.070869 / 0.060014 | 0.201010 / 0.201245 |

| Archived run | Own wrapper (s) | Own Spectre elapsed / CPU (s) | Runner elapsed (s) | Upload / execute / fetch / parse / cleanup / other guards (s) |
|---|---|---|---:|---|
| 20261101-051413-soa11-physical-tt | 26.0 | 22.2/12.7 | 278.001 | 21.562 / 63.906 / 44.922 / 3.328 / 21.063 / 123.220 |
| 20261101-051814-soa11-physical-corners | 15.0, 25.0, 15.0, 15.0 | 10.8/12.5, 21.5/12.2, 10.8/12.5, 10.9/12.4 | 347.053 | 21.656 / 112.594 / 56.609 / 12.547 / 21.156 / 122.491 |
| 20261101-051824-soa11-physical-loading | 31.0 | 26.9/12.4 | 284.824 | 21.953 / 72.204 / 45.265 / 0.766 / 21.062 / 123.574 |
| 20261101-052307-soa11-v2c56-noise-fs | 254.0 | 250.0/240.0 | 491.069 | 21.718 / 276.078 / 43.235 / 5.907 / 21.281 / 122.850 |

20261101-051413-soa11-physical-tt archive SHA-256 `ffc71a19d556d5cdce394b627e119cf594bf8cb7637be24002dc921b11024d1d`.

20261101-051814-soa11-physical-corners archive SHA-256 `99902c48342ad0c38943c768c2b8d0a4bc8a931104ffb669474472c36e4cf389`.

20261101-051824-soa11-physical-loading archive SHA-256 `b049d3a30b216a81cc694a1bc8c158f2baa39ef174b4cc630c99930044952659`.

20261101-052307-soa11-v2c56-noise-fs archive SHA-256 `25aa5a2282d6623a27291b1ac310220689cd95d79895d9e3f2d1f6c38518244e`.

All listed completed archives passed CRC/member SHA checks and exact remote-path absence checks. Batch timers include other variants in a shared run; overlapping durations are not campaign wall time. Archive/report time was not instrumented. Noise CIs are conditional on the binomial probit model and do not establish independent samples or seed robustness. Non-TT 30 mV delay and energy are report-only.

The initial PMOS request used w before fingers and returned 15 um total width; it was rejected before any netlist/simulation. A corrected l/fingers/Wfg request produced and verified 5 um. Two local checker setup attempts (text-format recognition, then missing copied RNL packages) were corrected using an exact .scs copy and complete project RNL package set; no circuit change was used to hide diagnostics.
