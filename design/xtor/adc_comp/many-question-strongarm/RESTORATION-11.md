# V2 restoration under the 1.1 V project rule

Frozen historical circuit, no device or geometry edits. Source commit `8d67a75c40bb99dd5066e64ae8e8db687c7daa1f`; electrical SHA-256 `608dfd3e547ee65738662bf62ef9c9cb548b0b7ea1000b21c22087ee0c958db8`. This private screen uses current main `17b3a0c`, adc_comp 0.9.0, unchanged delay stimuli/measurements and explicit DUT terminal saves. It does not replace canonical/formal results or establish full qualification.

| TT metric | Measured |
|---|---:|
| tdelay_1mV_ps | 56.473600243332776 |
| tdelay_30mV_ps | 44.169527137588915 |
| tau_reg_ps | 2.795395282448056 |
| treset_ps | 19.03776955021709 |
| wrong_decisions | 0 |
| validity_violations | 0 |
| loser_peak_pct | 15.39445600950082 |
| energy_fJ | 149.865117912 |
| soa_max_V | 0.95608 |
| soa_violations | 0 |

All 36 actual decisions, including 10 uV inputs, and all 36 resets are correct. Full-trace stress covers 45 Vgs/Vgd/Vds pairs with the 1.1 V limit. Energy is reported only. Actual reltol is 0.0001, method gear2only, errpreset conservative.

The successful two-job batch retained all source/TB/deck/log/waveform hashes, verified exact remote absence, and passed archive CRC/member SHA checks. Archive SHA-256: `372533cafa9ea446ad9dc9db15f8e308c7b32b0d535668274452441d97cbf315`. The initial attempt failed at a missing generated Verilog-A include before circuit simulation; it is retained separately and is not a failed circuit result.

This job used 27.0 s in the remote Spectre wrapper. Whole-batch upload 21.735 s, execution dispatch 65.281 s, download plus unpack 44.578 s, local parse/measurement 2.094 s. Dispatch includes orchestration overhead; these batch times are not per-job solver CPU times.

The four additional representative corners also pass the applicable timing/reset/validity and 1.1 V stress limits. The 30 mV / 50 ps limit applies at TT; non-TT 30 mV values below are reported only. Across these five corners there are 180 correct actual decisions and reset intervals, with no missing reset or invalid output.

| Additional corner | 1 mV delay (ps) | 30 mV delay (ps) | Reset (ps) | Peak terminal V |
|---|---:|---:|---:|---:|
| ff_high_m40 | 42.78731792558143 | 33.692718499082495 | 14.949531906783154 | 1.04827 |
| ss_low_125 | 73.4552743056128 | 56.98086685038607 | 26.131516851629243 | 0.86216 |
| fs_low_125 | 55.81191568545478 | 44.10673676044039 | 23.438010267870965 | 0.86052 |
| sf_high_m40 | 63.64340180468108 | 48.83260785221261 | 16.20052206822155 | 1.04869 |

Five corners are a private screening subset, not the full formal corner set. The additional-corner archive passed CRC/member SHA verification and exact remote absence: `48a1b0264fded9768059d1f566911ebdc229193a73291c2522cfdd5c07e4cd9c`.

Dedicated TT loading also passes: input capacitance 19.313134034315315 fF, CLKC 15.223158372781954 fF. The specified differential change after evaluation plus reset is 0.00018185579995014245 uV; this near-zero net value is not the instantaneous decision-phase disturbance. Actual reltol/vabstol are 1e-6/1e-8 with conservative gear2only.

Full physical 17 x 512 noise now gives the results below. Both corners have all 8704 finite decisions, 512 at each of 17 levels; full physical device noise, 50 GHz maximum noise frequency and seed 1 are retained. These are private measurements on the exact restored source, not canonical/formal result replacements.

| Physical noise corner | Fitted width (uV rms) | Model-conditional 95% profile interval (uV) | Limit (uV) | Result |
|---|---:|---|---:|---|
| tt_nom_27 | 184.174455388682 | [176.43, 192.32] | 200 | PASS |
| fs_low_125 | 317.00025134117095 | [306.35, 328.17] | 240 | FAIL |

FS/low/125 fails, so full-corner and mismatch expansion is stopped for this restored source. TT timing/loading/energy improvements do not waive this noise failure. The fit intervals assume the binomial probit model and do not certify independence or seed robustness. No candidate source is promoted.

The original decisions were refit to retain unrounded intervals (uV): TT [176.42559432971512, 192.3212211902768]; FS/low/125 [306.34969032134103, 328.16576805722093]. The rounded table above is only for display.

| Noise run | Wrapper (s) | Spectre elapsed / CPU (s) | Upload | Execute dispatch | Fetch/unpack | Parse | Cleanup | Other guards | Runner elapsed |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| TT | 276.000 | 272.000 / 260.000 | 21.453 | 297.672 | 43.094 | 1.531 | 21.094 | 123.527 | 508.371 |
| FS/low/125 | 267.000 | 262.000 / 252.000 | 21.453 | 288.953 | 43.047 | 0.969 | 20.984 | 121.793 | 497.199 |

Each row is a separate single-job runner; overlapping runner elapsed times must not be summed as campaign wall time. Execute dispatch contains wrapper time plus transport/orchestration. Other guards include process inventory, remote identity, hashes and absence checks. Archive creation/readback and reporting were not timed. No physical-noise retries were needed.

TT noise archive SHA-256: `77c0e401d40ec3f206967173de5a16cf7a413ef9c1c69dd0210f13faeb1bd5d6`. CRC, every member SHA and exact remote absence passed.

FS/low/125 noise archive SHA-256: `403021f99eeae8020bcffd2ab8818a506a0487e607e862a8455e8421969cbd19`. CRC, every member SHA and exact remote absence passed.

TT loading archive SHA-256: `94a351fb2dcedb812a20b910a9b8f712cf3e17829b3ec231d0289c4e352345a8`. Sources, deck/TB, logs and original decisions remain retained privately.

[Retained-waveform mechanism analysis](RESTORATION-MECHANISM.md) distinguishes observations from untested physical hypotheses and proposes a small number of isolated changes.
