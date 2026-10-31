# BUFFER-V23: stronger physical second stage

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

**B23 fails the deterministic gate:** TT 30 mV delay is 50.14965558025553 ps against 50 ps; SS/low/125 reset is 46.1394172594504 ps and FS/low/125 reset is 35.69263848338459 ps against 35 ps. No B23 noise run, promotion or qualification expansion follows these failures.

[B22](BUFFER-V22.md) passes selected deterministic gates but its complete FS/low/125 noise fails at 342.51175741522553 uV rms against 240 uV. Its artificial source trials show sensitivity to both front drivers and latch/DP-controlled devices. These diagnostics are not independent additive noise components and do not predict that this new physical source passes.

B23 doubles the widths of the ten second-stage MOS devices while retaining their length and relative ratios: M14/M15 P8 to P16, M12/M13 N1 to N2, M10/M11 P4 to P8, and M6/M7/M8/M9 N2 to N4. Larger differential-stage transconductance is the noise hypothesis. Added loading on DP/DN and the regenerative nodes can alter timing, offset, stress and noise correlations; those effects must be measured. The other 33 MOS devices and all nine MOMs remain exactly B22, including the input pair, 3 um tail, clock/reset devices, 16-finger RP/RN loads and output buffers. All physical noise sources remain enabled.

Each accepted N2/N4/P8/P16 geometry has a zero-warning callback with complete terminal parasitics; provider/release is identical across requests. Retrieved files are SHA-verified and the exact owned remote callback directory is absent. No Virtuoso or PDK model export is used.

| Callback | SHA-256 |
|---|---|
| n2 | `d899f4fdf621dad61d7ca1a5c55d8f8022b122be5a201a46befb1154bb160c86` |
| n4 | `fe7a637ebeb7d2815ed8fa061820fba88a02a76c77d7e40b3a7b2a0b9cbf0b15` |
| p16 | `fc2f39f5c0343dd28043426e39316c1a00dae056fa81e9cecdd2db591148806b` |
| p8 | `20855415d9559ad00227138e98d1e759f6c67857f07cd4c5123d67502d0fec87` |

Electrical SHA-256: `af10c79df6868e2672614361b50d9e476e2992da4e5ffda3a5e5a09ccaf2595a`. The [complete RNL source](https://github.com/many-question/ADC-12b-100M/blob/01524e4bc95e7a6eb73f09ae6d4f2fb1a99d3e88/design/xtor/adc_comp/many-question-miyahara/BUFFER-V23.txt) was checked and rendered with zero errors/warnings from a byte-identical mirror; the full drawing stays with local source-preparation evidence. To keep the candidate within its size budget, the prior independent B22 source is pinned at [published commit 2db9f93](https://github.com/many-question/ADC-12b-100M/blob/2db9f93848412c520ab08fb6218adf376ff2cd50/design/xtor/adc_comp/many-question-miyahara/BUFFER-V22.txt) and retained in its raw evidence, while this working file advances to B23. Canonical B20 and formal results are unchanged.

Selected-corner delay/reset/validity/full-device SOA and dedicated capacitance/kickback gates precede full FS noise. All simulations explicitly save only required DUT terminal nodes and measurement/current probes, or preserve the existing monitor-only noise protocol. No stimulus, tolerance, measurement or acceptance limit is changed, and no pass or promotion is assumed.


## Completed physical failure

The five-corner screen uses frozen clean source `c3b7afee025c8c97fb22bcd4dbea1b3fe75d7bff` on the merged 0.8.0 baseline. Explicit selected saves are an output-only change; stimuli, loads, sampler definitions, actual baseline numerics and limits are unchanged. All 180 actual polarities (including 10 uV) and resets complete correctly; output validity and all 129 terminal pairs per corner pass. Completed reset cycles do not override the reset-time failures.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Maximum unrounded stress V | Gate |
|---|---:|---:|---:|---:|---|
| fs_high_m40 | 53.232886398 | 45.255767742 | 29.806597490 | 0.999776145263 | PASS |
| fs_low_125 | 66.220278649 | 54.591661601 | 35.692638483 | 0.813230740423 | CMP-08 |
| sf_high_m40 | 59.188555215 | 49.578186747 | 30.661744750 | 0.999439615188 | PASS |
| ss_low_125 | 80.757598217 | 67.380901503 | 46.139417259 | 0.816904192418 | CMP-08 |
| tt_nom_27 | 59.657300543 | 50.149655580 | 34.646199388 | 0.908492882231 | CMP-06 |

The smallest measured stress margin is only 223.8547368253 uV at FS/high/-40. No tighter-numerics stress clearance is claimed for this failing source. TT full-cycle AVDD meter energy is 667.7330886000001 fJ; the independent waveform integral and all named supply probes close KCL. [NUMERICS-94](NUMERICS-94.md) retains the energy partition and measurement difference.

The B22-to-B23 path comparison verifies equal non-output testbench statements and actual numerical settings, with every cycle retained. Evaluation crossings are interpolated; reset milestones use the first saved sample meeting the stated condition, matching the official reset convention.

| SS/low/125 worst-reset milestone | B22 ps | B23 ps |
|---|---:|---:|
| CKB_above90 | 11.691430471 | 12.077896200 |
| D_both_above90 | 61.786726872 | 68.186142175 |
| X_both_below10 | 64.409763755 | 61.479258904 |
| R_both_below30 | 19.753870867 | 33.540249871 |
| B_both_above90 | 28.121451423 | 39.539231858 |
| OUT_both_below10 | 34.071442459 | 46.139417259 |

CKB assertion changes little while RP/RN discharge is substantially later. The two unchanged N4 reset assists now act against a doubled physical second stage. This observation motivates stronger reset assistance and a smaller RP/RN MOM load, with the clock release, timing, stress, capacitance and all-source noise measured again. It does not isolate capacitance from drive or prove any noise benefit.

At TT and 30 mV, the mean DP/DN 70% crossing shifts from 17.35053396017961 to 18.771087164619814 ps; RP/RN 50% shifts from 35.04666047442337 to 36.73773981699318 ps. The external 50% crossing therefore still requires a timing repair.

The dedicated TT input and clock capacitances are 19.328731218738323 and 12.105070079022973 fF, passing 20/16 fF. Net per-cycle kickback is 8.310719994131244e-05 uV, while separate instantaneous differential/common-mode excursions reach 28.669688034964768 uV and 7.418294723631758 mV in evaluation. These quantities remain distinct; actual CDAC decision-phase validation is open.

- `20261031-151621-miyahara-buffer-v23-spec08-delay-baseline-screen`: archive SHA-256 `fa9c7f2c759ee3be53dd4ce7daf89cfcc4179781830004362fa4a6b6984b21aa`, every member CRC/SHA verified, exact remote directory absent.

- `20261031-151635-miyahara-buffer-v23-spec08-kickback-baseline-screen`: archive SHA-256 `340e1463aa7f293ec8c20a0cf4816d56a674e52f96eb51384ec328a9c7e087e6`, every member CRC/SHA verified, exact remote directory absent.

B23 has no physical noise result. Canonical B20 and its genuine failed formal noise record remain unchanged.
