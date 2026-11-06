# CDAC qualification under spec 0.11.0

The formal WIP source is the all-physical reference L40 variant. Its SHA-256 is `42645fb6930b8f673c29fd3b62c26a79159669f27249987c21e2a6288b5cf281` and its circuit dependency hash is `13f9ef85f31580d6`. The external ports, XCAP, XSW and separate XBOOST hierarchy remain in the RNL netlist. V29 and its failed runs are available at [the pre-qualification commit](https://github.com/many-question/ADC-12b-100M/tree/7fb3ce84ae0f7e8ea161cd7ec514895f8276ec20).

## Requirements and evidence

| Test | All 45 PVT | Additional TT limits | Current coverage |
| --- | --- | --- | --- |
| `tb_cdac_track` | DAC-09 SFDR ≥84 dBc, DAC-10 SNDR ≥80 dB | Same limits | 1 pass, 1 solver error, 43 pending |
| `tb_cdac_soa` | DAC-18 zero violations over the 70 ns stimulus | Same limits | 4 pass, 41 pending |
| `tb_cdac_settle` | DAC-05/06/07/08/11 settling, time constant, start and hold | DAC-12 Qref, DAC-13 and DAC-15/16/17 input loads | 1 pass, 2 fail, 42 pending |
| `tb_cdac_weights` | DAC-02 full scale | DAC-01/03/04/14 Cs, calibratability, gain and calibrated ENOB | 1 pass, 44 pending |

The CDAC spec defines Qref and the control loads. Its acceptance suite has no separate CDAC energy limit. The integrated reference load and system power require the mixed top-level verification.

### Spectrum

The prior hot SS records each have 256 coherent samples at 100 MS/s and 48.828125 MHz. Both archives contain the exact formal source. The generated stimulus, model includes, inputs and reachable circuit dependencies match. The archived bench changes save settings and includes 111 electrically unloaded edge observers which add solver breakpoints. Both staged bench hashes and the observation overlay are recorded with the result. Remeasurement with the current ADCToolbox 0.9.2 pin reproduces both results.

| `ss_low_125` | SFDR (dBc) | SNDR (dB) | Archive SHA-256 |
| --- | ---: | ---: | --- |
| Gear2 primary, `035325-c6cd` | 84.830062 | 82.970966 | `39c6e122b82f20ba78332a4e32f8ee27eb5abb1c3f7a6c23a9233fa968b5dbc5` |
| Traponly, 1 ps, `071639-469b` | 84.872576 | 83.066325 | `7588ed4b5f99f308a8765eec43e7deb2fb94d033bb1376eb1314fc843312921f` |

H5 remains largest. Both logs include CMI-2753 (main switch Vgb) and CMI-2755 (booster M1 Vbd). The crosscheck logs five LTE relaxation and companion warning pairs at one reported control event. The 0.043 dB SFDR method difference, all 111 matching control sequences and 1.160 uV RMS paired nonfundamental residual are numerical evidence for this hot corner. PDK range warnings remain for lead review separately from the project Vgs/Vgd/Vds checks.

The unmodified official `ss_low_m40` Gear2 track run stops at 60.0983 ns with SPECTRE-16928 and exit 1. It saves 2 of 256 samples. SFDR and SNDR are unavailable. The 60-file archive for `143652-4a0d` has SHA-256 `5ba3b8dd3abbe07da2d2b55b48bfe1b525245ea7b699bc1fff60ec756d23e666`. V29 stopped at 60.1007 ns. The close times motivate a targeted investigation of the control event.

### Settling, weights and SOA

| Corner | RL12 (ps), ≤40 | RL5 (ps), ≤75 | Start (ps), ≤100 | Qref (pC) |
| --- | ---: | ---: | ---: | ---: |
| `tt_nom_27` | 32.8 | 40.7 | 74.4 | 1.285, limit 1.35 |
| `ss_low_125` | **43.3** | 60.3 | **103.7** | 1.976, reported |
| `ss_low_m40` | **43.1** | 53.9 | 92.3 | 1.367, reported |

TT phase loads PHI_S / PHI_SB / CONV are 17.72 / 21.46 / 14.77 fF and DH5 load is 0.831 fF. TT weights pass all five limits, with Cs 2.0651 pF, full scale 0.99369 V and calibration margin 0.36925 LSB. TT settle and the two archived SS cold SOA runs use the same source and matching stimulus. The settle bench adds three saved booster nodes. The SOA bench saves the same full set of device nodes and retains three extra booster traces in the reduced output. All original settle metrics and SOA pair values reproduce on remeasurement.

An observation-only settle replay reproduces the official metrics on both SS corners. Actual RL12 half-height is 3 fs after the specified start, which is 1.005 ns after the third CONV half-height. The L-branch GP/GN reach half-height at +19/+20 ps and TOP reaches 90% at +40.4/+40.6 ps (hot/cold). At hot conversion start, the bit-12 reference gates reach half-height at +33 to +34 ps. The bit-12/11 bottom plates take about 106–108 ps to reach 99% of their swing and the bit-0 lower plate takes 51 ps. The archived replay `144234-a39c` has SHA-256 `f9c9e4b8004f1d5cc7db3e36cfe904c11e514d16db555bc08de529a68de5d983`.

| SOA corner | Pair violations | Peak (V) | Worst 10 ns occupancy above 1.1 V (ps) |
| --- | ---: | ---: | ---: |
| `ss_low_m40` | 0/1797 | 1.19649 | 28.788 |
| `ss_high_m40` | 0/1797 | 1.17754 | 49.820 |
| `ff_high_125` | 0/1797 | 1.21414 | 19.000 |
| `ff_high_m40` | 0/1797 | 1.11192 | 5.775 |

The FF hot SOA log prints one LTE relaxation. The source-specific representative SOA crosscheck remains pending. The available crosscheck for the earlier v3 source used different reference output lengths.

| Evidence | Run | Archive SHA-256 |
| --- | --- | --- |
| TT settle | `034711-f2f2` | `dec1fcdba1edbdb6c87e542c82edae4c78c333b0779e06c87b6f97c4683a334f` |
| SS low/high cold SOA | `034711-c31d` / `034711-2106` | `17029fe5c9e46a80ca3c6876e6cbce1bc67721894afa7d35957a2a3d67f9d210` / `99041a188583108c3da69bd4eaccf812fc35033b8fb279757c33608ca89f333b` |
| SS low hot/cold settle | `143651-ec47` | `f217b313a81a4ad6923c8c4b9a61d7791b5d1123dfa1927bf2cc5ca0675d5c4a` |
| TT weights | `143651-e022` | `11629791d7ce18c323e393a5abca023feb26d92a1c29933f6ec863abb99154ed` |
| FF high hot/cold SOA | `143651-f6c7` | `65b1eca9ad072de5ff82f919cf4b686888eded9752c64012732b715a62f6be9e` |

## Bounded timing repair and cold convergence diagnosis

The private trial increased reference-output finger counts from 10/20 to 12/24 on bit 12 and from 6/12 to 7/14 on bit 11 (NMOS/PMOS), with the 40 nm length and finger widths held. The PDK callback returned all four requested geometries. Its source SHA-256 is `1c79a8e35c6d9c3580b67a901d19891c7aa805eb0f7461f845d95d57dbb14335`.

| Metric | Formal source | Finger-count trial | Limit |
| --- | ---: | ---: | ---: |
| SS hot RL12 (ps) | 43.3 | 40.1 | ≤40 |
| SS cold RL12 (ps) | 43.1 | 40.1 | ≤40 |
| SS hot start (ps) | 103.7 | 96.5 | ≤100 |
| TT Qref (pC) | 1.285 | 1.321 | ≤1.35 |

The additional output gate load delays bit-12 GP/GN half-height by 0.3–0.4 ps. The L bottom plate reaches 95% 4.7 ps sooner at hot SS and 4.1 ps sooner at cold SS. At hot SS and VIN = 0.65 V, the steady-track off drain current magnitudes rise from 0.3935/0.2868 uA to 0.4722/0.3442 uA (H-branch NMOS/L-branch PMOS). TT control and phase loads stay within limits. Both SS RL12 failures remain, so the formal source stays at its original geometry.

The two cold diagnosis runs retain APS Gear2 and effective 1e-7 / 10 nV tolerances and use an 80 ns diagnostic stop, selected probes and `+diagnose`. Both terminate with SPECTRE-16928. The formal-source diagnosis reproduces the official failure at 60.098333 ns (2 samples). The finger-count trial stops at 20.101283 ns (0 samples) and logs SPECTRE-16266 for local truncation error. The smallest saved steps are approximately 8e-22 s in both. Neither diagnostic yields an acceptance spectrum.

Both events occur about 100 ps into a sampling cycle, with CONV low, PHI_S and PHI_B high, and APGATE and SAMP_ON transitioning. The final step diagnostics repeatedly name bit-12 `XDL.BN`; Newton failure messages also name the supply current and ideal PHI_S branch. The diagnostic logs flag behavioral clock contributions and MOM model conductance. These observations identify the operating phase and signals for investigation. The root cause remains unresolved.

For the next diagnostic, replay the formal source at cold SS with the same Gear2 tolerances and an 80 ns bound. Save `XDL.BN`, the two stack device currents and gates, the phase-source branch currents and the observed switching nodes on both sides. Compare the failing edge with the previous completed edge at the same phase. This separates a device-stack transition from a residual in the ideal stimulus or the supply branches. Qualification still requires the unmodified official 256-point Gear2 run and the prescribed convergence check. RL12 remains a separate timing gate on the same candidate.

| Diagnostic archive | Run | SHA-256 |
| --- | --- | --- |
| Finger-count trial settling, three corners | `145059-b2aa` | `1ccce0401596bcd4be9e945b341d8abde649a8c6cb8d9f283b5106e657f5f686` |
| Formal source cold failure replay | `145009-b1d5` | `8b93556110d07984518cce739b2989e4736eceb71dd6060a43f0891b92e3d085` |
| Finger-count trial cold failure | `145100-d9a7` | `e2eacc47dc62eda056374d7d080df4674519dbeb5b851dce3902fe02e20490cc` |

## PVT matrix

Pass and fail refer to applicable checks on this source. Pending cells require current-source results. The V29 results use a different source hash and remain in the historical record.

| Corner | Track | SOA | Settle | Weights |
| --- | --- | --- | --- | --- |
| tt_low_m40 | Pending | Pending | Pending | Pending |
| tt_low_27 | Pending | Pending | Pending | Pending |
| tt_low_125 | Pending | Pending | Pending | Pending |
| tt_nom_m40 | Pending | Pending | Pending | Pending |
| tt_nom_27 | Pending | Pending | Pass | Pass |
| tt_nom_125 | Pending | Pending | Pending | Pending |
| tt_high_m40 | Pending | Pending | Pending | Pending |
| tt_high_27 | Pending | Pending | Pending | Pending |
| tt_high_125 | Pending | Pending | Pending | Pending |
| ff_low_m40 | Pending | Pending | Pending | Pending |
| ff_low_27 | Pending | Pending | Pending | Pending |
| ff_low_125 | Pending | Pending | Pending | Pending |
| ff_nom_m40 | Pending | Pending | Pending | Pending |
| ff_nom_27 | Pending | Pending | Pending | Pending |
| ff_nom_125 | Pending | Pending | Pending | Pending |
| ff_high_m40 | Pending | Pass | Pending | Pending |
| ff_high_27 | Pending | Pending | Pending | Pending |
| ff_high_125 | Pending | Pass | Pending | Pending |
| ss_low_m40 | Error | Pass | Fail DAC-06 | Pending |
| ss_low_27 | Pending | Pending | Pending | Pending |
| ss_low_125 | Pass | Pending | Fail DAC-06, DAC-08 | Pending |
| ss_nom_m40 | Pending | Pending | Pending | Pending |
| ss_nom_27 | Pending | Pending | Pending | Pending |
| ss_nom_125 | Pending | Pending | Pending | Pending |
| ss_high_m40 | Pending | Pass | Pending | Pending |
| ss_high_27 | Pending | Pending | Pending | Pending |
| ss_high_125 | Pending | Pending | Pending | Pending |
| fs_low_m40 | Pending | Pending | Pending | Pending |
| fs_low_27 | Pending | Pending | Pending | Pending |
| fs_low_125 | Pending | Pending | Pending | Pending |
| fs_nom_m40 | Pending | Pending | Pending | Pending |
| fs_nom_27 | Pending | Pending | Pending | Pending |
| fs_nom_125 | Pending | Pending | Pending | Pending |
| fs_high_m40 | Pending | Pending | Pending | Pending |
| fs_high_27 | Pending | Pending | Pending | Pending |
| fs_high_125 | Pending | Pending | Pending | Pending |
| sf_low_m40 | Pending | Pending | Pending | Pending |
| sf_low_27 | Pending | Pending | Pending | Pending |
| sf_low_125 | Pending | Pending | Pending | Pending |
| sf_nom_m40 | Pending | Pending | Pending | Pending |
| sf_nom_27 | Pending | Pending | Pending | Pending |
| sf_nom_125 | Pending | Pending | Pending | Pending |
| sf_high_m40 | Pending | Pending | Pending | Pending |
| sf_high_27 | Pending | Pending | Pending | Pending |
| sf_high_125 | Pending | Pending | Pending | Pending |
