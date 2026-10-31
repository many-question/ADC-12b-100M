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

Four further representative corners are under test. Dedicated input/clock loading, physical 17 x 512 noise, mismatch and full formal corner coverage remain open.
