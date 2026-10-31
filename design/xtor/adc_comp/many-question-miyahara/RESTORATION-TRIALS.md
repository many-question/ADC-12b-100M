# Isolated physical restoration trials

Each frozen revision changes one symmetric device pair from the original V2/B2 source, preserving physical output isolation and full device noise. These private screens do not promote a canonical circuit or replace formal results. The [mechanism report](RESTORATION-MECHANISM.md) motivated the changes but does not predict success.

## B2-C52

[Complete frozen source](RESTORE-B2-C52.txt), raw SHA-256 `b06b77a5c33a3e65dbccd2b3467de7f204359b04fe15190380f8df3d001f5264`; electrical SHA-256 `5a3bed89a0ee024014a2604d65b80cbc12d350cd09e17afe5253044de5561f29`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only CDP/CDN MOM finger count changes from 48 to 52; callback nominal capacitance 15.26030 fF per node. Length, width, spacing, metal stack and multiplicity remain the parent values.

Callback receipt SHA-256 `b7ce79bbb6ee753c7660876650ee783af37a20aaca6a17cd8b39e0e949704c7f`. 28 nm HPC+ adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`; exact provider/release identity is retained in the private receipt. Ordered request: `[['Nfinger', '52'], ['Lfinger', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

| Kind / corner | Measured result |
|---|---|
| delay / tt_nom_27 | tdelay_1mV_ps=59.38457851754137, tdelay_30mV_ps=48.91773165391922, treset_ps=23.196196716858225, validity_violations=0, soa_max_V=0.92062, energy_fJ=208.01462608799997; limited gate PASS |
| delay / fs_low_125 | tdelay_1mV_ps=71.0364962145742, tdelay_30mV_ps=56.88001533401471, treset_ps=24.890701273261044, validity_violations=0, soa_max_V=0.82601, energy_fJ=217.42472952000006; limited gate PASS |
| delay / ss_low_125 | tdelay_1mV_ps=81.06697889017653, tdelay_30mV_ps=65.85387662004703, treset_ps=30.328161271679672, validity_violations=0, soa_max_V=0.83233, energy_fJ=191.71782351000002; limited gate PASS |
| delay / ff_high_m40 | tdelay_1mV_ps=45.0331938829977, tdelay_30mV_ps=37.34178146236071, treset_ps=17.604585434071996, validity_violations=0, soa_max_V=1.01689, energy_fJ=244.25183910599998; limited gate PASS |
| delay / sf_high_m40 | tdelay_1mV_ps=58.24301645787593, tdelay_30mV_ps=48.58893885452085, treset_ps=20.563556730457286, validity_violations=0, soa_max_V=1.01787, energy_fJ=234.59507545320002; limited gate PASS |
| kickback / tt_nom_27 | cin_fF=19.31090586511203, cin_clkc_fF=14.9214190114932, kickback_uV=8.650640013346811e-05; PASS |
| noise / fs_low_125 | 463.74178616731064 uV rms; unrounded 95% profile CI [447.78862513183816, 480.6659066590029]; FAIL 240 uV, finite 17 x 512 samples |

A required gate fails: stop long-noise or further qualification expansion for this source.

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
| 20261101-052318-soa11-b2c52-noise-fs | 641.0 | 636.0/625.0 | 872.543 | 22.078 / 662.188 / 43.281 / 0.922 / 21.032 / 123.042 |

20261101-051413-soa11-physical-tt archive SHA-256 `ffc71a19d556d5cdce394b627e119cf594bf8cb7637be24002dc921b11024d1d`.

20261101-051814-soa11-physical-corners archive SHA-256 `99902c48342ad0c38943c768c2b8d0a4bc8a931104ffb669474472c36e4cf389`.

20261101-051824-soa11-physical-loading archive SHA-256 `b049d3a30b216a81cc694a1bc8c158f2baa39ef174b4cc630c99930044952659`.

20261101-052318-soa11-b2c52-noise-fs archive SHA-256 `832c3217640a2a8d5cc6742a96f828f447e86ec2139022b08a5fb0cbe37fcaa1`.
## B2-P5

[Complete frozen source](RESTORE-B2-P5.txt), raw SHA-256 `82c32d30eb380f185bcd4d4cc67be1cf81697ebc76c05f62ff389bd15f9ba01c`; electrical SHA-256 `0242a27c4d8b3ccccaf712ab242fee68e77d872f3424c4b87a064934b5d38282`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only M14/M15 changes from W=4 um / nf=4 to W=5 um / nf=5, L=30 nm; all terminal geometry/parasitic parameters come from the successful callback. M12/M13 and DP/DN capacitance remain the parent values.

Callback receipt SHA-256 `e0a6e29486c6fe53f2f3dd8c92c47f81bfa5cdf3c6b89023cf699835120771ba`. 28 nm HPC+ adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`; exact provider/release identity is retained in the private receipt. Ordered request: `[['l', '30n'], ['fingers', '5'], ['Wfg', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

| Kind / corner | Measured result |
|---|---|
| delay / tt_nom_27 | tdelay_1mV_ps=57.27004598259445, tdelay_30mV_ps=47.30434996657332, treset_ps=23.379663321914855, validity_violations=0, soa_max_V=0.92062, energy_fJ=209.40410955600007; limited gate PASS |
| delay / fs_low_125 | tdelay_1mV_ps=67.39339632876168, tdelay_30mV_ps=53.999527268177836, treset_ps=25.139991150534236, validity_violations=0, soa_max_V=0.82602, energy_fJ=218.90835947519997; limited gate PASS |
| delay / ss_low_125 | tdelay_1mV_ps=77.51444753481984, tdelay_30mV_ps=63.09647879011634, treset_ps=31.149982711764974, validity_violations=0, soa_max_V=0.83249, energy_fJ=192.55408396919998; limited gate PASS |
| delay / ff_high_m40 | tdelay_1mV_ps=43.59064500589525, tdelay_30mV_ps=36.22034289218469, treset_ps=18.289564784830443, validity_violations=0, soa_max_V=1.01808, energy_fJ=247.01423464079997; limited gate PASS |
| delay / sf_high_m40 | tdelay_1mV_ps=56.306410892332686, tdelay_30mV_ps=47.018943844032606, treset_ps=20.94203238190305, validity_violations=0, soa_max_V=1.01947, energy_fJ=236.31809081759997; limited gate PASS |
| kickback / tt_nom_27 | cin_fF=19.31090586511203, cin_clkc_fF=14.922185522591375, kickback_uV=8.651269999861155e-05; PASS |
| noise / fs_low_125 | 395.8138409185866 uV rms; unrounded 95% profile CI [382.61143680702924, 409.73629421135746]; FAIL 240 uV, finite 17 x 512 samples |

A required gate fails: stop long-noise or further qualification expansion for this source.

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
| 20261101-052328-soa11-b2p5-noise-fs | 640.0 | 636.0/625.0 | 871.897 | 21.610 / 662.078 / 43.156 / 1.422 / 21.062 / 122.569 |

20261101-051413-soa11-physical-tt archive SHA-256 `ffc71a19d556d5cdce394b627e119cf594bf8cb7637be24002dc921b11024d1d`.

20261101-051814-soa11-physical-corners archive SHA-256 `99902c48342ad0c38943c768c2b8d0a4bc8a931104ffb669474472c36e4cf389`.

20261101-051824-soa11-physical-loading archive SHA-256 `b049d3a30b216a81cc694a1bc8c158f2baa39ef174b4cc630c99930044952659`.

20261101-052328-soa11-b2p5-noise-fs archive SHA-256 `8607ec4cce3f34156a6025adc941fd6fd8ea9f8db92f8f72170b128d390bb49e`.
## B2-P6

[Complete frozen source](RESTORE-B2-P6.txt), raw SHA-256 `9b2d74bf5a900271e2c0e93ba5dfdac4ad0f25bb350b2dd6a21cd4a52105ebe8`; electrical SHA-256 `993e1d7e900ad08470a928e335dcb3017181fe3691fd9e864602775e8955734e`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only M14/M15 changes from W=4 um / nf=4 to W=6 um / nf=6, L=30 nm; all terminal geometry/parasitic parameters come from the successful callback. M12/M13 and DP/DN capacitance remain the parent values.

This bounded second PMOS step follows the complete P5 FS-noise reduction from 469.46 to 395.81 uV and its earlier core response. It retains the original B2 capacitors and N-device geometry; no capacitance change is combined with this test.

Callback receipt SHA-256 `1e49a1b0563f362e75683c62f62fbf54a6c2d9339d1a2111f0f1df00cc8bfad6`. 28 nm HPC+ adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`; exact provider/release identity is retained in the private receipt. Ordered request: `[['l', '30n'], ['fingers', '6'], ['Wfg', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

| Kind / corner | Measured result |
|---|---|
| delay / tt_nom_27 | tdelay_1mV_ps=56.287759093705006, tdelay_30mV_ps=46.58894180415552, treset_ps=23.784679574030374, validity_violations=0, soa_max_V=0.92061, energy_fJ=212.76100148400002; limited gate PASS |
| delay / fs_low_125 | tdelay_1mV_ps=65.2484875194895, tdelay_30mV_ps=52.35531734195987, treset_ps=25.977376363541104, validity_violations=0, soa_max_V=0.82602, energy_fJ=222.0476161788; limited gate PASS |
| delay / ss_low_125 | tdelay_1mV_ps=75.68506977444133, tdelay_30mV_ps=61.7320796434656, treset_ps=31.78379530794168, validity_violations=0, soa_max_V=0.83243, energy_fJ=195.39406261799996; limited gate PASS |
| delay / ff_high_m40 | tdelay_1mV_ps=42.92576491568427, tdelay_30mV_ps=35.715598285861404, treset_ps=18.43058546945801, validity_violations=0, soa_max_V=1.01871, energy_fJ=251.56960119720003; limited gate PASS |
| delay / sf_high_m40 | tdelay_1mV_ps=55.55957598457285, tdelay_30mV_ps=46.39047759699909, treset_ps=21.004803368777942, validity_violations=0, soa_max_V=1.02034, energy_fJ=240.50166596279996; limited gate PASS |
| kickback / tt_nom_27 | cin_fF=19.31090586511203, cin_clkc_fF=14.920381242967167, kickback_uV=8.622179988211631e-05; PASS |

Reported deterministic/loading gates are limited screening; physical FS noise is the next conditional gate.

Retained noise-off waveform markers (mean of four +/-100 uV cycles; exact saved traces and per-cycle values retained privately). These are descriptive thresholds, not gm/loop-gain activation points or individual noise contributions.

| Corner | Core reaches 1 mV: parent / trial (ps) | D differential at that event: parent / trial (mV) | Max saved D differential before that event: parent / trial (mV) |
|---|---|---|---|
| tt_nom_27 | 34.646518 / 33.555915 | 0.542460 / 0.527044 | 0.536524 / 0.522286 |
| fs_low_125 | 41.360939 / 37.075604 | 0.020730 / 0.086748 | 0.338202 / 0.332287 |

| Archived run | Own wrapper (s) | Own Spectre elapsed / CPU (s) | Runner elapsed (s) | Upload / execute / fetch / parse / cleanup / other guards (s) |
|---|---|---|---:|---|
| 20261101-054750-soa11-physical-p6-tt | 27.0 | 23.8/14.2 | 264.804 | 21.531 / 49.734 / 43.641 / 2.094 / 21.031 / 126.773 |
| 20261101-055149-soa11-physical-p6-corners | 17.0, 27.0, 17.0, 16.0 | 12.6/14.5, 23.6/14.1, 12.5/14.2, 12.3/14.1 | 283.872 | 21.469 / 66.969 / 45.750 / 4.656 / 21.016 / 124.012 |
| 20261101-055159-soa11-physical-p6-loading | 34.0 | 29.7/14.8 | 265.570 | 21.468 / 55.438 / 43.250 / 0.140 / 21.000 / 124.274 |

20261101-054750-soa11-physical-p6-tt archive SHA-256 `0b659467c1f01590be48598fce635a719a6ef6a1fe1de7c77aed5b48f9de5a00`.

20261101-055149-soa11-physical-p6-corners archive SHA-256 `ed70b261bf3c546c0a6647da90c3fcc0cb9f0ede14649c0eb08222149efad95a`.

20261101-055159-soa11-physical-p6-loading archive SHA-256 `5e1bf7259c9295a46cba58aa29b2965547522c27ac995f2b30e52646678ba591`.

All listed completed archives passed CRC/member SHA checks and exact remote-path absence checks. Batch timers include other variants in a shared run; overlapping durations are not campaign wall time. Archive/report time was not instrumented. Noise CIs are conditional on the binomial probit model and do not establish independent samples or seed robustness. Non-TT 30 mV delay and energy are report-only.

The initial PMOS request used w before fingers and returned 15 um total width; it was rejected before any netlist/simulation. A corrected l/fingers/Wfg request produced and verified 5 um. Two local checker setup attempts (text-format recognition, then missing copied RNL packages) were corrected using an exact .scs copy and complete project RNL package set; no circuit change was used to hide diagnostics.
