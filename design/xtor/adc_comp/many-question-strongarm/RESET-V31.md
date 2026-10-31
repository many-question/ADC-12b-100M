# RESET-V31: stronger Q precharge for reset

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

**V31 fails the dedicated TT clock-input capacitance gate:** 16.65232415714863 fF exceeds 16 fF. Four-corner delay/reset/output-validity and all unrounded MOS terminal checks pass, including SS reset at 33.33299224307328 ps. Qualification expansion stops at CMP-14; no V31 noise run or promotion is claimed.

[V30](RESET-V30.md) gains useful TT 30 mV timing at 47.35514490849851 ps but fails SS/low/125 reset at 36.646221657802904 ps. The worst reset cycle's Q90 diagnostic is 46.433287549044344 ps after the clock fall. All 144 actual decisions/resets, output validity and every unrounded terminal pair are retained; the reset-time failure stops qualification expansion.

V31 changes only MRQP/MRQN from 3 to 3.6 um, with length 30 nm and three fingers retained; finger width becomes 1.2 um. The other 21 MOS devices and all five MOMs remain exactly V30, including P8/N4 output inverters, input pair and 3 um tail. The zero-warning callback supplies all geometry and terminal parasitics, SHA-256 `9e7e41eba5150991ae03d24448efc5c44411fd5e004808caa7a075aa18ab3827`; its provider/release matches the existing verified geometry and its exact owned remote directory is absent. All physical noise sources remain enabled.

The first independent private checks use the merged 0.8.0 baseline at TT, SS/low/125 and SF/FS high-voltage cold corners. All actual polarities, resets, full output validity, unrounded MOS terminal stress and whole-cycle AVDD energy are audited. Stronger precharge adds clock loading and alters feedthrough and reset current, so a dedicated TT capacitance/kickback test is required before noise expansion. The 16 fF clock limit is unchanged. Tighter critical-corner repeats are separate convergence diagnostics. No timing, noise, loading or qualification pass is assumed; no input-tail reduction is included.

Electrical SHA-256: `49527ccb78676fcf1bc519dea363e7151da21e1fa671fb87a985061d36dadb29`. The [source](RESET-V31.txt) contains complete RNL checked on a byte-identical mirror. Canonical V27 and all formal records remain unchanged.

![Stronger physical Q precharge](reset-v31.png)


## Completed timing gates and clock-capacitance failure

Both completed private baseline runs use frozen clean source `59d298a829e2b07341286e3d0868895aa9fc93df`, with no numerical overrides. These are original runs completed before the disk-retention pause; the new explicit-save wrapper was not applied retroactively.

| Corner | 1 mV ps | 30 mV ps | Reset ps | Unrounded peak V | Actual/reset cycles |
|---|---:|---:|---:|---:|---:|
| fs_high_m40 | 56.055124193001674 | 42.01754179810593 | 21.103877139051278 | 0.9954836221920864 | 36 / 36 |
| sf_high_m40 | 71.95662266311642 | 52.77482883559615 | 20.045380302817012 | 0.9968883837550861 | 36 / 36 |
| ss_low_125 | 88.01879169292506 | 63.33993040600623 | 33.33299224307328 | 0.8184052503268058 | 36 / 36 |
| tt_nom_27 | 64.58426326243782 | 47.47388068441786 | 23.930863640254003 | 0.9074001904642198 | 36 / 36 |

Every actual polarity down to 10 uV, all resets and all 69 gs/gd/ds pairs per corner are checked. Whole-cycle AVDD waveform energy is `424.817112136437` fJ/cycle: `102.79441834963569` evaluation and `322.0226937868013` reset. All supply probes are present and KCL closes; power is report-only.

The dedicated TT test gives input capacitance `19.331118542884703` fF and clock-input capacitance `16.65232415714863` fF. Its specified net per-cycle differential change is `6.151410002035174e-05` uV; this small number is within numerical drift and does not describe the evaluation-phase disturbance.

Separate raw-trace diagnostics retain instantaneous differential excursion `364.65801587939734` uV at +`70.21352053439826` ps in evaluation, and maximum common-mode excursion `7.403152283855963` mV. These instantaneous values are not compared to the net metric's 40 uV limit. Conditions are TT 0.9 V, initial CM 0.49 V/differential 1 mV, 2.50 pF per floating input, 10 fF per output and a 400 ps clock with 10 ps edges. Actual-CDAC decision-phase validation remains open.

The measured clock-loading failure motivates a smaller local CKB driver and reduced local MOM load, while retaining the stronger Q precharge that repaired reset. Any new physical source must recheck timing, reset, all terminal stress and dedicated clock capacitance before noise expansion. No limit or stimulus changes.

- `20261031-142506-strongarm-reset-v31-spec08-delay-baseline-screen`: retained archive SHA-256 `16675cf85040eef16b2f1408798ec477e25d271b376798f0cc202b1f35485e36`. Original raw/deck hashes and ZIP member CRC/SHA verification passed; exact owned remote directory absent.

- `20261031-142603-strongarm-reset-v31-spec08-kickback-baseline-screen`: retained archive SHA-256 `de2075791bc9a9be8109c4cb4db32f66c4f9c90fc6a3779ea0e10a1d04b9bd0e`. Original raw/deck hashes and ZIP member CRC/SHA verification passed; exact owned remote directory absent.
