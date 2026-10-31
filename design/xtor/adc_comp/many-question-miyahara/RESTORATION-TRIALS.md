# Isolated physical restoration trials

Each frozen revision changes one symmetric device pair from the original V2/B2 source, preserving physical output isolation and full device noise. These private screens do not promote a canonical circuit or replace formal results. The [mechanism report](RESTORATION-MECHANISM.md) motivated the changes but does not predict success.

## B2-C52

[Complete frozen source](RESTORE-B2-C52.txt), raw SHA-256 `b06b77a5c33a3e65dbccd2b3467de7f204359b04fe15190380f8df3d001f5264`; electrical SHA-256 `5a3bed89a0ee024014a2604d65b80cbc12d350cd09e17afe5253044de5561f29`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only CDP/CDN MOM finger count changes from 48 to 52; callback nominal capacitance 15.26030 fF per node. Length, width, spacing, metal stack and multiplicity remain the parent values.

Callback receipt SHA-256 `b7ce79bbb6ee753c7660876650ee783af37a20aaca6a17cd8b39e0e949704c7f`. Provider tsmc-n28-hpcplus-ull-mmwave-1.8-2p2a-20190531, adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`. Ordered request: `[['Nfinger', '52'], ['Lfinger', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

| Kind / corner | Measured result |
|---|---|
| delay / tt_nom_27 | tdelay_1mV_ps=59.38457851754137, tdelay_30mV_ps=48.91773165391922, treset_ps=23.196196716858225, validity_violations=0, soa_max_V=0.92062, energy_fJ=208.01462608799997; limited gate PASS |
| delay / fs_low_125 | tdelay_1mV_ps=71.0364962145742, tdelay_30mV_ps=56.88001533401471, treset_ps=24.890701273261044, validity_violations=0, soa_max_V=0.82601, energy_fJ=217.42472952000006; limited gate PASS |
| delay / ss_low_125 | tdelay_1mV_ps=81.06697889017653, tdelay_30mV_ps=65.85387662004703, treset_ps=30.328161271679672, validity_violations=0, soa_max_V=0.83233, energy_fJ=191.71782351000002; limited gate PASS |
| delay / ff_high_m40 | tdelay_1mV_ps=45.0331938829977, tdelay_30mV_ps=37.34178146236071, treset_ps=17.604585434071996, validity_violations=0, soa_max_V=1.01689, energy_fJ=244.25183910599998; limited gate PASS |
| delay / sf_high_m40 | tdelay_1mV_ps=58.24301645787593, tdelay_30mV_ps=48.58893885452085, treset_ps=20.563556730457286, validity_violations=0, soa_max_V=1.01787, energy_fJ=234.59507545320002; limited gate PASS |
| kickback / tt_nom_27 | cin_fF=19.31090586511203, cin_clkc_fF=14.9214190114932, kickback_uV=8.650640013346811e-05; PASS |

Reported deterministic/loading gates are limited screening; physical FS noise is the next conditional gate.

Retained noise-off waveform markers (mean of four +/-100 uV cycles; exact saved traces and per-cycle values retained privately). These are descriptive thresholds, not gm/loop-gain activation points or individual noise contributions.

| Corner | Core reaches 1 mV: parent / trial (ps) | D differential at that event: parent / trial (mV) | Max saved D differential before that event: parent / trial (mV) |
|---|---|---|---|
| tt_nom_27 | 34.646518 / 35.198916 | 0.542460 / 0.541726 | 0.536524 / 0.540756 |
| fs_low_125 | 41.360939 / 41.820928 | 0.020730 / 0.022854 | 0.338202 / 0.338370 |

| Archived run | Own wrapper (s) | Own Spectre elapsed / CPU (s) | Runner elapsed (s) | Upload / execute / fetch / parse / cleanup / other guards (s) |
|---|---|---|---:|---|
| 20261101-051413-soa11-physical-tt | 15.0 | 11.6/13.1 | 278.001 | 21.562 / 63.906 / 44.922 / 3.328 / 21.063 / 123.220 |
| 20261101-051814-soa11-physical-corners | 17.0, 17.0, 16.0, 18.0 | 12.0/13.6, 11.9/13.3, 11.4/13.2, 12.4/13.4 | 347.053 | 21.656 / 112.594 / 56.609 / 12.547 / 21.156 / 122.491 |
| 20261101-051824-soa11-physical-loading | 19.0 | 14.0/15.5 | 284.824 | 21.953 / 72.204 / 45.265 / 0.766 / 21.062 / 123.574 |

20261101-051413-soa11-physical-tt archive SHA-256 `ffc71a19d556d5cdce394b627e119cf594bf8cb7637be24002dc921b11024d1d`.

20261101-051814-soa11-physical-corners archive SHA-256 `99902c48342ad0c38943c768c2b8d0a4bc8a931104ffb669474472c36e4cf389`.

20261101-051824-soa11-physical-loading archive SHA-256 `b049d3a30b216a81cc694a1bc8c158f2baa39ef174b4cc630c99930044952659`.
## B2-P5

[Complete frozen source](RESTORE-B2-P5.txt), raw SHA-256 `82c32d30eb380f185bcd4d4cc67be1cf81697ebc76c05f62ff389bd15f9ba01c`; electrical SHA-256 `0242a27c4d8b3ccccaf712ab242fee68e77d872f3424c4b87a064934b5d38282`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only M14/M15 changes from W=4 um / nf=4 to W=5 um / nf=5, L=30 nm; all terminal geometry/parasitic parameters come from the successful callback. M12/M13 and DP/DN capacitance remain the parent values.

Callback receipt SHA-256 `e0a6e29486c6fe53f2f3dd8c92c47f81bfa5cdf3c6b89023cf699835120771ba`. Provider tsmc-n28-hpcplus-ull-mmwave-1.8-2p2a-20190531, adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`. Ordered request: `[['l', '30n'], ['fingers', '5'], ['Wfg', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

| Kind / corner | Measured result |
|---|---|
| delay / tt_nom_27 | tdelay_1mV_ps=57.27004598259445, tdelay_30mV_ps=47.30434996657332, treset_ps=23.379663321914855, validity_violations=0, soa_max_V=0.92062, energy_fJ=209.40410955600007; limited gate PASS |
| delay / fs_low_125 | tdelay_1mV_ps=67.39339632876168, tdelay_30mV_ps=53.999527268177836, treset_ps=25.139991150534236, validity_violations=0, soa_max_V=0.82602, energy_fJ=218.90835947519997; limited gate PASS |
| delay / ss_low_125 | tdelay_1mV_ps=77.51444753481984, tdelay_30mV_ps=63.09647879011634, treset_ps=31.149982711764974, validity_violations=0, soa_max_V=0.83249, energy_fJ=192.55408396919998; limited gate PASS |
| delay / ff_high_m40 | tdelay_1mV_ps=43.59064500589525, tdelay_30mV_ps=36.22034289218469, treset_ps=18.289564784830443, validity_violations=0, soa_max_V=1.01808, energy_fJ=247.01423464079997; limited gate PASS |
| delay / sf_high_m40 | tdelay_1mV_ps=56.306410892332686, tdelay_30mV_ps=47.018943844032606, treset_ps=20.94203238190305, validity_violations=0, soa_max_V=1.01947, energy_fJ=236.31809081759997; limited gate PASS |
| kickback / tt_nom_27 | cin_fF=19.31090586511203, cin_clkc_fF=14.922185522591375, kickback_uV=8.651269999861155e-05; PASS |

Reported deterministic/loading gates are limited screening; physical FS noise is the next conditional gate.

Retained noise-off waveform markers (mean of four +/-100 uV cycles; exact saved traces and per-cycle values retained privately). These are descriptive thresholds, not gm/loop-gain activation points or individual noise contributions.

| Corner | Core reaches 1 mV: parent / trial (ps) | D differential at that event: parent / trial (mV) | Max saved D differential before that event: parent / trial (mV) |
|---|---|---|---|
| tt_nom_27 | 34.646518 / 34.019794 | 0.542460 / 0.534634 | 0.536524 / 0.528058 |
| fs_low_125 | 41.360939 / 38.833182 | 0.020730 / 0.048833 | 0.338202 / 0.335481 |

| Archived run | Own wrapper (s) | Own Spectre elapsed / CPU (s) | Runner elapsed (s) | Upload / execute / fetch / parse / cleanup / other guards (s) |
|---|---|---|---:|---|
| 20261101-051413-soa11-physical-tt | 16.0 | 11.6/13.1 | 278.001 | 21.562 / 63.906 / 44.922 / 3.328 / 21.063 / 123.220 |
| 20261101-051814-soa11-physical-corners | 16.0, 15.0, 16.0, 17.0 | 11.4/13.2, 11.4/13.1, 11.6/13.2, 12.4/14.1 | 347.053 | 21.656 / 112.594 / 56.609 / 12.547 / 21.156 / 122.491 |
| 20261101-051824-soa11-physical-loading | 18.0 | 13.3/15.1 | 284.824 | 21.953 / 72.204 / 45.265 / 0.766 / 21.062 / 123.574 |

20261101-051413-soa11-physical-tt archive SHA-256 `ffc71a19d556d5cdce394b627e119cf594bf8cb7637be24002dc921b11024d1d`.

20261101-051814-soa11-physical-corners archive SHA-256 `99902c48342ad0c38943c768c2b8d0a4bc8a931104ffb669474472c36e4cf389`.

20261101-051824-soa11-physical-loading archive SHA-256 `b049d3a30b216a81cc694a1bc8c158f2baa39ef174b4cc630c99930044952659`.

All listed completed archives passed CRC/member SHA checks and exact remote-path absence checks. Batch timers include other variants in a shared run; overlapping durations are not campaign wall time. Archive/report time was not instrumented. Noise CIs are conditional on the binomial probit model and do not establish independent samples or seed robustness. Non-TT 30 mV delay and energy are report-only.

The initial PMOS request used w before fingers and returned 15 um total width; it was rejected before any netlist/simulation. A corrected l/fingers/Wfg request produced and verified 5 um. Two local checker setup attempts (text-format recognition, then missing copied RNL packages) were corrected using an exact .scs copy and complete project RNL package set; no circuit change was used to hide diagnostics.
