# BUFFER-V23: stronger physical second stage

[B22](BUFFER-V22.md) passes selected deterministic gates but its complete FS/low/125 noise fails at 342.51175741522553 uV rms against 240 uV. Its artificial source trials show sensitivity to both front drivers and latch/DP-controlled devices. These diagnostics are not independent additive noise components and do not predict that this new physical source passes.

B23 doubles the widths of the ten second-stage MOS devices while retaining their length and relative ratios: M14/M15 P8 to P16, M12/M13 N1 to N2, M10/M11 P4 to P8, and M6/M7/M8/M9 N2 to N4. Larger differential-stage transconductance is the noise hypothesis. Added loading on DP/DN and the regenerative nodes can alter timing, offset, stress and noise correlations; those effects must be measured. The other 33 MOS devices and all nine MOMs remain exactly B22, including the input pair, 3 um tail, clock/reset devices, 16-finger RP/RN loads and output buffers. All physical noise sources remain enabled.

Each accepted N2/N4/P8/P16 geometry has a zero-warning callback with complete terminal parasitics; provider/release is identical across requests. Retrieved files are SHA-verified and the exact owned remote callback directory is absent. No Virtuoso or PDK model export is used.

| Callback | SHA-256 |
|---|---|
| n2 | `d899f4fdf621dad61d7ca1a5c55d8f8022b122be5a201a46befb1154bb160c86` |
| n4 | `fe7a637ebeb7d2815ed8fa061820fba88a02a76c77d7e40b3a7b2a0b9cbf0b15` |
| p16 | `fc2f39f5c0343dd28043426e39316c1a00dae056fa81e9cecdd2db591148806b` |
| p8 | `20855415d9559ad00227138e98d1e759f6c67857f07cd4c5123d67502d0fec87` |

Electrical SHA-256: `af10c79df6868e2672614361b50d9e476e2992da4e5ffda3a5e5a09ccaf2595a`. The [complete RNL source](BUFFER-V23.txt) was checked and rendered with zero errors/warnings from a byte-identical mirror; the full drawing stays with local source-preparation evidence. To keep the candidate within its size budget, the prior independent B22 source is pinned at [published commit 2db9f93](https://github.com/many-question/ADC-12b-100M/blob/2db9f93848412c520ab08fb6218adf376ff2cd50/design/xtor/adc_comp/many-question-miyahara/BUFFER-V22.txt) and retained in its raw evidence, while this working file advances to B23. Canonical B20 and formal results are unchanged.

Selected-corner delay/reset/validity/full-device SOA and dedicated capacitance/kickback gates precede full FS noise. All simulations explicitly save only required DUT terminal nodes and measurement/current probes, or preserve the existing monitor-only noise protocol. No stimulus, tolerance, measurement or acceptance limit is changed, and no pass or promotion is assumed.
