# B13: worst-corner physical phase diagnosis

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

The original formal four-corner failures remain in [FORMAL-BUFFER-V13.md](FORMAL-BUFFER-V13.md), including FS/low/125 at 488.025278 uV rms. This independent diagnostic uses actual clean source `bfeddcb74f6ee3ec0dfc6ab26c05d1fd0936f00f`, electrical SHA-256 `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`, run `20261031-074723-miyahara-noise-phase-diagnostic-screen`. The physical source, 10 fF output load, VCM 0.49 V, +/-800 uV levels with 128 cycles each, seed 1, 50 GHz bandwidth and fine 0.5 ps/1e-6/1e-8 integration match between TT/0.9 V/27 C and FS/0.81 V/125 C. Voltage thresholds and normalized statistics use each corner's actual VDD.

## Sample, reset and output checks

| Corner | OUTP at -800 / +800 uV | Wrong / 256 | Reset max (ps) | Early/mid to final sign changes | Max MOS stress (V) |
|---|---:|---:|---:|---:|---:|
| tt_nom_27 | 0 / 128 | 0 | 22.909270842 | 0 / 0 | 0.90500 |
| fs_low_125 | 7 / 124 | 11 | 25.233515862 | 0 / 0 | 0.81182 |

Every one of the 256 resets completes in each corner. Both have zero late-reset, physical output-validity and full-trace terminal-stress violations (129 MOS terminal pairs). All cycles are retained. The 11 FS errors occur at cycles 3, 10, 26, 33, 53, 95, 96, 169, 177, 205 and 217. They are distributed across both input polarities rather than confined to the first cycle. At +50 ps, RP-RN already has the same 11 errors and its sign agrees with the final output in all 256 cycles. This sample gives no evidence of new errors originating after that internal decision; it does not rule out earlier coupled interface noise.

## Signal transfer during integration and regeneration

The following gains are two-level secants, not linear small-signal gain. SNR here means the mean of the two levels' absolute differential mean divided by its sample standard deviation; it is descriptive, not a formal input-noise estimate.

| Phase after rising midpoint | Quantity | TT gain | FS low/hot gain | TT SNR | FS low/hot SNR |
|---|---|---:|---:|---:|---:|
| +20 ps | DP minus DN | -3.584914 | -3.021849 | 4.114767 | 3.308228 |
| +30 ps | DP minus DN | -4.702372 | -2.090033 | 4.964894 | 3.480239 |
| +30 ps | XP minus XN | 12.159094 | 6.680821 | 3.852014 | 2.423817 |
| +40 ps | DP minus DN | -4.795048 | -0.248519 | 5.053293 | 0.833231 |
| +40 ps | RP minus RN | 28.295436 | 7.557355 | 4.247585 | 1.852117 |

At +30 ps the DP differential standard deviations average 0.758334 mV at TT and 0.480719 mV at FS low/hot; at +40 ps RP values are 5.331901 and 3.268885 mV. The worst corner has smaller absolute node fluctuation at these phases but much less signal transfer. The existing SHA-verified noiseless B13 traces, using +/-1 mV rather than +/-800 uV, show the same early decay: DP gain at +30 ps is -4.6699 TT versus -2.0741 FS, XP +12.1418 versus +6.6852, and RP gain at +40 ps +27.9470 versus +7.3133. These reused traces require no simulation retry.

Normalized CKB is similar at +15 ps (about 0.483 VDD in both), +30 ps (0.13214 TT, 0.14394 FS) and +40 ps (0.08340 TT, 0.08238 FS). At +30 ps the measured reset-device drain current averages 24.960675 uA TT and 36.567343 uA FS; the weak RP PMOS drain current is -157.014158/-101.454737 uA. Drain currents include displacement terms and do not by themselves prove channel contention or identify a noise source. All 43 device drain currents are retained in the private phase data.

The evidence supports testing the timing and strength of transfer into regeneration, with the input difference disappearing earlier at FS low/hot. It does not isolate process, voltage and temperature effects or assign all noise to a device or capacitor. [BUFFER-V14](BUFFER-V14.md) therefore tests only the interstage PMOS drive, with the known worst noise corner included early.

## Scope and provenance

The 102.5 ns duration raises noisefmin to 9.7561 MHz versus 287.216 kHz in the original full test, and read-only samplers add time points. These observations cannot replace the official failure or establish a 240 uV pass. No seed or sample is discarded. Original official files are unchanged; raw/deck hashes and a private archive are SHA-verified, and the exact owned remote directory is absent.
