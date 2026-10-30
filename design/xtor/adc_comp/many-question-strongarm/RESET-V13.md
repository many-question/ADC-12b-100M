# RESET-V13: strengthen only the external output pull-down

V12 passes six-corner output validity but retains a 1.00002 V SF Q peak and 35.861626 ps SS reset. This experiment changes only MOPN and MONN from N3 to N4 um, L=30 nm, with 4 fingers. Complete geometry and parasitics are copied from an identical previously validated canonical device. Stronger output discharge and a lower inverter trip point may improve the physical reset metric; the added gate load also changes the upstream waveform, so delay, output validity and all-device stress must be measured again. No Q-shunt or weak pull-up is strengthened.

The [independent source](RESET-V13.txt) has electrical SHA-256 `7b82aa1b9cb951e5dce10db119d62ba9403dbf7905f742b385479bbbe4abfa96`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the rendered schematic was inspected.

![External output pull-down change](reset-v13.png)

The six-key-corner screen retains the same complete transient checks and current probes. Any passing revision proceeds to further qualification; failed revisions retain their evidence and stop their own expansion. [Energy comparison](ENERGY-COMPARISON.md) reports the measured persistent-current costs of the preceding implementations; no new performance or efficiency pass is assumed.
