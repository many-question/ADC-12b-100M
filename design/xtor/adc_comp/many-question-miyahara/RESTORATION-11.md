# B2 restoration under the 1.1 V project rule

Frozen historical circuit, no device or geometry edits. Source commit `c4c736318f2d05a1fd3eb59f8d4e739a77ba5ebd`; electrical SHA-256 `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`. This private screen uses current main `17b3a0c`, adc_comp 0.9.0, unchanged delay stimuli/measurements and explicit DUT terminal saves. It does not replace canonical/formal results or establish full qualification.

| TT metric | Measured |
|---|---:|
| tdelay_1mV_ps | 58.71536240521146 |
| tdelay_30mV_ps | 48.3119004101247 |
| tau_reg_ps | 3.3775051422075144 |
| treset_ps | 23.070396581014712 |
| wrong_decisions | 0 |
| validity_violations | 0 |
| loser_peak_pct | 0.1260620391503392 |
| energy_fJ | 205.710367428 |
| soa_max_V | 0.92063 |
| soa_violations | 0 |

All 36 actual decisions, including 10 uV inputs, and all 36 resets are correct. Full-trace stress covers 93 Vgs/Vgd/Vds pairs with the 1.1 V limit. Energy is reported only. Actual reltol is 0.0001, method gear2only, errpreset conservative.

The successful two-job batch retained all source/TB/deck/log/waveform hashes, verified exact remote absence, and passed archive CRC/member SHA checks. Archive SHA-256: `372533cafa9ea446ad9dc9db15f8e308c7b32b0d535668274452441d97cbf315`. The initial attempt failed at a missing generated Verilog-A include before circuit simulation; it is retained separately and is not a failed circuit result.

This job used 15.0 s in the remote Spectre wrapper. Whole-batch upload 21.735 s, execution dispatch 65.281 s, download plus unpack 44.578 s, local parse/measurement 2.094 s. Dispatch includes orchestration overhead; these batch times are not per-job solver CPU times.

The four additional representative corners also pass the applicable timing/reset/validity and 1.1 V stress limits. The 30 mV / 50 ps limit applies at TT; non-TT 30 mV values below are reported only. Across these five corners there are 180 correct actual decisions and reset intervals, with no missing reset or invalid output.

| Additional corner | 1 mV delay (ps) | 30 mV delay (ps) | Reset (ps) | Peak terminal V |
|---|---:|---:|---:|---:|
| ff_high_m40 | 44.6046003801277 | 36.953345290971015 | 17.770730324410078 | 1.01719 |
| ss_low_125 | 80.14304082796518 | 64.99546187822142 | 30.20474684787858 | 0.83252 |
| fs_low_125 | 70.45297779461855 | 56.302918121818394 | 24.851951064565085 | 0.82603 |
| sf_high_m40 | 57.45524768539558 | 47.916651679647536 | 20.52586884501902 | 1.01829 |

Five corners are a private screening subset, not the full formal corner set. The additional-corner archive passed CRC/member SHA verification and exact remote absence: `48a1b0264fded9768059d1f566911ebdc229193a73291c2522cfdd5c07e4cd9c`.

Dedicated TT loading also passes: input capacitance 19.31090586511203 fF, CLKC 14.923913393745476 fF. The specified differential change after evaluation plus reset is 8.708380002352134e-05 uV; this near-zero net value is not the instantaneous decision-phase disturbance. Actual reltol/vabstol are 1e-6/1e-8 with conservative gear2only.

Full physical 17 x 512 noise now gives the results below. Both corners have all 8704 finite decisions, 512 at each of 17 levels; full physical device noise, 50 GHz maximum noise frequency and seed 1 are retained. These are private measurements on the exact restored source, not canonical/formal result replacements.

| Physical noise corner | Fitted width (uV rms) | Model-conditional 95% profile interval (uV) | Limit (uV) | Result |
|---|---:|---|---:|---|
| tt_nom_27 | 186.69549406194517 | [178.94, 194.85] | 200 | PASS |
| fs_low_125 | 469.46007668614965 | [453.25, 486.67] | 240 | FAIL |

FS/low/125 fails, so full-corner and mismatch expansion is stopped for this restored source. TT timing/loading/energy improvements do not waive this noise failure. The fit intervals assume the binomial probit model and do not certify independence or seed robustness. No candidate source is promoted.

The original decisions were refit to retain unrounded intervals (uV): TT [178.94183487217296, 194.84612080900868]; FS/low/125 [453.24796094190555, 486.6679688646446]. The rounded table above is only for display.

| Noise run | Wrapper (s) | Spectre elapsed / CPU (s) | Upload | Execute dispatch | Fetch/unpack | Parse | Cleanup | Other guards | Runner elapsed |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| TT | 675.000 | 672.000 / 659.000 | 21.438 | 697.484 | 43.016 | 1.016 | 21.157 | 121.351 | 905.462 |
| FS/low/125 | 648.000 | 643.000 / 632.000 | 21.735 | 669.375 | 43.078 | 0.984 | 21.047 | 121.702 | 877.921 |

Each row is a separate single-job runner; overlapping runner elapsed times must not be summed as campaign wall time. Execute dispatch contains wrapper time plus transport/orchestration. Other guards include process inventory, remote identity, hashes and absence checks. Archive creation/readback and reporting were not timed. No physical-noise retries were needed.

TT noise archive SHA-256: `d66ffae3eea63d95dbef69bedeb9a6cb957e9d3cd07fdbb00e513b63cde54267`. CRC, every member SHA and exact remote absence passed.

FS/low/125 noise archive SHA-256: `b6234ffa795ac3c6c8548e49c23505251b4f4bebf49a7b2cc3a9ee5e87c70134`. CRC, every member SHA and exact remote absence passed.

TT loading archive SHA-256: `94a351fb2dcedb812a20b910a9b8f712cf3e17829b3ec231d0289c4e352345a8`. Sources, deck/TB, logs and original decisions remain retained privately.
