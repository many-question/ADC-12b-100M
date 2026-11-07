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

### Cold follow-up with stack and phase probes

The 80 ns `ss_low_m40` controls used the same APS Gear2 tolerances as the formal test. Current probes include the two BN stack MOS terminal currents and the ideal phase, VDDA and VREFP source branches. The voltage-only control retains the same voltage probes. The clamp control adds ideal 0 V sources to bit-12 `XDL.BN` on both sides.

| Diagnostic | Result | Archive SHA-256 |
| --- | --- | --- |
| Formal source, voltage only `163546-a53e` | RC1, SPECTRE-16928 at 60.098333264 ns, 2 samples | `39eed2da3807d9a22506782c7ece2ba33a77ba78302809f14c21544392885edc` |
| Formal source, voltage and current `163014-7621` | RC1, SPECTRE-16928 at 40.098623121 ns, 0 samples | `b2130ff9c4c18b89414748cca8afb48fafbf2a4e7f007b4183a667ba8a4c2f53` |
| Finger-count trial, voltage and current `163014-ccdc` | RC0 at 80 ns, 4 samples | `2de264b22d11bdff7b49105cda5fbc7ba0f08a9c368348ff52d69ab1d73a075e` |
| Formal source, current probes plus BN clamps `163214-83d7` | RC0 at 80 ns, 4 samples | `74a8443c75d13295136d87434c093e7e1e678f5a7c687a36afefe89cacd68952` |

The voltage-only replay matches the earlier diagnostic's stop and reproduces the two formal samples within 4 pV. Relative to the rising CLK midpoint, CONV falls at +46.00 ps, PHI_S and PHI_B rise at +76.00 ps, SAMP_ON rises at +83.79 to +83.81 ps and APGATE falls at +84.62 to +84.67 ps. Step collapse follows at +88.33 ps, before the boost gate reaches its rising threshold. The N-side bit-12 BN is 2.08 uV, with HIB at 0.809 V and EN at 0.148 mV. These gates have already settled. Both formal controls reach a minimum saved step of about `7.94e-22 s`.

The current-probe run reports sub-microamp BN terminal currents at the last regular step and erratic current spikes after step collapse. At the clamp, BN holds at 0 V. KCL from the two saved MOS terminal currents gives a peak clamp current of 0.514 uA in the half-picosecond windows around the observed failing phases and 1.320 mA at a conversion edge. The clamp changes the node equation and carries switching current. Step limiters in the completed clamp and wider runs still include other BN nodes and the assist driver. The wider source had failed at 20.101283 ns with the prior voltage probe set. These results show sensitivity to the probe set and circuit constraint. They leave the physical origin of the convergence failure unresolved and provide no acceptance spectrum.

The initial `162315-450e` and `162315-2e99` runs inherited an operating-system temporary directory outside job scratch. An escaping-only correction still left the `162655-f006` and `162655-c6d4` runs outside job scratch. The first formal run reproduced the current-probe failure at 40.098623121 ns. The other three were stopped after detecting the setting and their partial records were archived. The controls in the table use the corrected absolute job temporary directory, verified together with the Verilog-A build and library paths.

### Reduced replay

Three paired replays used the original PDK sections, device geometries, bulk connections and APS Gear2 at effective reltol `1e-7` and vabstol `10 nV`. The N-side normal edge at 40.010 ns and the failing edge at 60.010 ns were both placed at the same absolute time. Each replay drove the captured histories from 59.750 to 60.098317928 ns. This ends 15.3 fs before the observed collapse and holds the boundary values afterward. The 80 ns stop bounds the diagnostic and only the recorded interval is used to judge reproduction.

| Replay circuit | Boundary kept ideal | Min step in the recorded interval, normal / failing history (s) | Printed LTE, normal / failing | Archive SHA-256 |
| --- | --- | ---: | ---: | --- |
| Two BN stack MOS, `164511` | EN, HIB and NOFF PWL | `8.28e-17` / `8.09e-17` | 5 / 5 | `598f3f0fb438d63676a9c3ce105bd8aaeb24f4c1739f2e5e1f69fd56087f2562` |
| Full bit-12 reference driver with the AP load, `164815` | EN, ENB, HIB and BPL12 PWL, original ideal supply and reference | `8.09e-17` / `8.33e-17` | 1 / 5 | `f153fb433a46e4959c99f918e8f4db14f98d1cb8a59e606752eac9dfab31f9de` |
| Same driver with the real L bottom-plate MOM, Cp and three connected switches, `165208` | EN, ENB, HIB, VIN, VG, EQBUS, APGATE, SAMP_ON and TOP PWL, original ideal supply and reference | `8.24e-17` / `8.34e-17` | 4 / 5 | `00fef112ebb49a436d72a0dd019b531d452a9710cd3825aabf100731e6c22b6a` |

All six diagnostic jobs return RC0. The full driver reproduces the failing-history BN voltage within 0.012 uV RMS over the last 13.3 ps of recorded drive. With the bottom-plate feedback restored, BN and BPL12 reproduce that window within 0.010 uV and 0.774 uV RMS respectively. The minimum time steps are about five orders of magnitude above the formal collapse. These are trajectory comparisons before the cutoff. The later output is a response to held boundary values. The ideal replay boundaries omit the full circuit feedback, including VIN through the 50 ohm source, the phase generator and the two-sided array. PWL drive also changes the solver breakpoints and produces LTE warnings. The necessary reproduction conditions remain unresolved.

### Full-circuit Traponly observation

The unmodified Gear2 failure and full-circuit voltage-only replay are the reproducible cases for lead and model review. The archive audit found the two previous cold tracking Traponly decks on V29. The exact formal source had no equivalent full-circuit cold record.

The single same-source `ss_low_m40` diagnostic `170814-3c36` runs from normal initialization to 61 ns with APS Traponly, 1 ps maximum step and effective reltol `1e-7` and vabstol `10 nV`. The original phase generator, 50 ohm inputs, references and both CDACs are connected as on the formal bench. The diagnostic changes the method, maximum step, stop time and voltage output window. Its 62-file archive has SHA-256 `7e057ff30c3869c69ecc357edaf46ff7439b2ee3e83bbd5560280a90a31f34e6`.

The solver returns RC0, with 2,664 saved points from 59.75 to 61 ns spanning the Gear2 stop at 60.098333264 ns. The minimum saved interval within 1 ps on either side of that stop is 29.8 fs, versus the Gear2 collapse at `7.94e-22 s`. The Traponly log prints model range and setup warnings. Its printed log has zero LTE relaxation messages. VDDA, VREFP and VCM hold at the ideal 0.81, 0.90 and 0.45 V values.

| Compared before the Gear2 collapse | Traponly vs Gear2 |
| --- | --- |
| CLK, CONV, PHI_S, PHI_B, SAMP_ON and APGATE threshold crossings | Largest shift 0.085 fs |
| Bit-12 XDL.BN, P / N sides | 0.040 / 0.041 uV RMS |
| Bit-12 L bottom plate, P / N sides | 0.744 / 0.725 uV RMS |
| TOPP / TOPN | 1.60 / 3.53 uV RMS |

The voltage comparisons use 60.085 to 60.098317928 ns, through the last regular Gear2 step. Near the stop, Gear2 records 41 P-side BN zero crossings from -0.75 to -0.55 ps relative to its stop, spanning about -156 to +165 nV. Traponly resolves one crossing in that interval with six interior samples. On the N side Gear2 resolves three crossings near -0.39 ps and Traponly resolves one. The coarser Traponly sampling limits a comparison of the short-period alternation. The logs show the preceding clock-generator breakpoint and provide no evidence of a new ideal-drive breakpoint at the stop. In Traponly the N bottom plate continues from 30.57 mV at the Gear2 stop to 190.63 mV 20 ps later, while the boost gate is still rising. These results establish sensitivity to the transient setup and provide a full-feedback post-event trajectory for model review. The two sampler records are diagnostic only. The official Gear2 256-point requirement and the separate RL12 gate remain open.

| Diagnostic archive | Run | SHA-256 |
| --- | --- | --- |
| Finger-count trial settling, three corners | `145059-b2aa` | `1ccce0401596bcd4be9e945b341d8abde649a8c6cb8d9f283b5106e657f5f686` |
| Formal source cold failure replay | `145009-b1d5` | `8b93556110d07984518cce739b2989e4736eceb71dd6060a43f0891b92e3d085` |
| Finger-count trial cold failure | `145100-d9a7` | `e2eacc47dc62eda056374d7d080df4674519dbeb5b851dce3902fe02e20490cc` |

### Cold numerical controls

The same-source 95 ns study uses APS Gear2, normal DC, the full physical network, zero cmin and the same 55 voltage probes. The matched control uses effective reltol `1e-7`, vabstol `10 nV`, iabstol `1 pA`, lteratio 10 and an 800 ps maximum step. The combined trial pairs the two intermediate tolerance settings. The source hash is `42645fb6…cf281`.

| Change | RC and last time | LTE / Newton rejects | Min step | Samples |
| --- | --- | ---: | ---: | ---: |
| Matched control `603c` | 1 at 60.098333266 ns | 395 / 426 | 9.53e-22 s | 2 |
| Approach protection 300 → 600 `e2c3` | 1 at 60.098333279 ns | 408 / 758 | 9.53e-22 s | 2 |
| Maxstep 1 ps `fdee` | 1 at 10.1018 ns | 90 / 415 | 9.50e-22 s | 0 |
| Effective reltol `1e-6` `5b66` | 0 at 95 ns | 843 / 30 | 1.67e-16 s | 5 |
| Vabstol 100 nV `b7b9` | 0 at 95 ns | 541 / 47 | 3.89e-16 s | 5 |
| Lteratio 30 `0655` | 0 at 95 ns | 639 / 29 | 5.09e-16 s | 5 |
| Lteratio 20 `e75e` | 0 at 95 ns | 560 / 29 | 3.51e-16 s | 5 |
| Effective reltol `3e-7` `7fee` | 0 at 95 ns | 627 / 29 | 1.90e-16 s | 5 |
| Lteratio 20 and effective reltol `3e-7` `6fd1` | 0 at 95 ns | 689 / 29 | 3.52e-16 s | 5 |
| Maxiters 12 `d04b` | 1 at 30.0978 ns | 213 / 375 | 9.53e-22 s | 0 |
| Tran pivot check enabled `d714` | 1 at 60.098333264 ns | 399 / 418 | 9.53e-22 s | 2 |

The RC1 cases end with SPECTRE-16928. A failed Newton trial immediately precedes the protection in the matched control. Doubling the approach budget advances the transient by about 13 as. The transient pivot check still reports a late VCM Jacobian warning and stops on the same edge. The combined relative and LTE change uses fewer accepted steps than either intermediate setting alone but increases the two-sample RMS difference from the archived 61 ns Traponly record to 14.01 µV. The lteratio 30 case differs by 4.85 µV and retains the Newton tolerances. The reference's two samples precede the collapse. The separate 0.1 fF global shunt diagnostic `278b` ends at 60.097137255 ns with the same protection and two samples.

### Full-length cold numerical crosscheck

Three same-source diagnostics complete 2.605 µs with 256 samples each. All use normal startup, effective reltol `1e-7`, vabstol 10 nV, iabstol 1 pA and the default minimum-step protections. The two Gear2 records keep the 800 ps step cap. The Traponly record uses a 1 ps cap and lteratio 10. The same pinned project estimator gives the results below.

| Cold diagnostic | SFDR (dBc) | SNDR (dB) | THD (dBc) | Solver job wall | Verified ZIP SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| Gear2, lteratio 20, `0452` | 80.360118 | 78.597295 | -79.958151 | 2365 s | `a3e222272b6daf6d1217eeb94ee6b2138d6a5b7aaeac593084aae3afd5a85692` |
| Gear2, lteratio 30, `ddd0` | 80.329202 | 78.576754 | -79.964778 | 2122 s | `ad6871421b12af014d7ed9da320a333e8cd2f2d55a1ac02aae29107d2bc27d4a` |
| Traponly, 1 ps, `6421` | 80.277304 | 78.512213 | -79.873446 | 7497 s | `e18e016a78c1307cfd95560fbf62f5e63e0249d230b12c748899c099c90a5a1e` |

The two Gear2 records differ by 2.30 µV RMS across all samples. Relative to Traponly, the Gear2 differences are 4.31 and 4.38 µV RMS with peaks of 9.15 and 10.79 µV. The printed sample time differences are at most 1 fs. Folded H5 at bin 113 is the largest spur in all three. The crosscheck spreads of 0.083 dB SFDR and 0.085 dB SNDR are small compared with the deficits to the 84 dBc and 80 dB limits. The finite-step Traponly run supplies an independent numerical comparison. Gear2 with lteratio 20 is the tighter of the tested LTE alternatives for continued diagnosis. The physical cause of the original collapse and the cold tracking distortion remain open. The official Gear2 baseline and the PVT matrix below retain their existing qualification status.

### Local timing repair screen

The private timing screen uses APS Gear2 with lteratio 20 and effective 1e-7 / 10 nV. The hot matched control measures RL12 at 43.3 ps and conversion start at 104.3 ps. The original formal settings give 43.3 and 103.7 ps. Changing only the lower bit-12 controller pull-down from 2 to 4 µm reduces RL12 to 38.9 ps. Changing only the shared enable predriver pull-down from 6 to 10 µm reduces hot start to 98.3 ps. Both use 30 nm ULVT NMOS with the original 2 µm finger width. The output devices keep their original geometry.

The same combined source `4a2a3149…e7e1` gives RL12/start of 38.9/98.3 ps at hot SS and 38.6/86.7 ps at cold SS. The hot CONV load changes from 14.34 to 17.57 fF and measured VREFP charge from 1.976 to 1.977 pC. The combined source is a timing candidate pending joint cold H5, SOA and coverage verification. The official matrix continues to describe the current formal source.

The formal-source phase observer records all 256 cycles. The TOP H5 magnitude is 50.3 µV at 5.040 ns within a cycle, 120.3 µV at 5.055 ns, 254.7 µV at 5.078 ns around reset and sharing release, 147.2 µV just before reference enable, and 76.8 µV after reference settling. The final sample is 77.1 µV. These are changes of a coherent vector at fixed phases. The observer changes the final sample residual by 1.78 µV RMS after removal of DC and the fundamental. Matched reference timing and input slew shifts affect transient peaks and move the final 20-point residual by 0.024 and 0.002 µV RMS respectively. Smaller top-two sharing devices lower the 32-point residual from 73.1 to 65.7 µV RMS on the timing candidate. That exact source retains 38.8/98.1 ps hot RL12/start and 38.5/86.5 ps cold. Full candidate spectrum is pending.

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
