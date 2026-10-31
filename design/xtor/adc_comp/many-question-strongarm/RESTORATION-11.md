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

Four further representative corners are under test. Dedicated input/clock loading, physical 17 x 512 noise, mismatch and full formal corner coverage remain open.
