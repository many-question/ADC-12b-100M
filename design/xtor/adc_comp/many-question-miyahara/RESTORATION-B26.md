# Original B26 restoration under adc_comp 0.11.0

The current canonical source is the original physical B26: 43 MOS devices and nine MOM capacitors. No dimensions, parasitics, connections or numerical settings were changed to restore it. All required block measurements now pass with **181/181 fresh records**, zero failures, errors or stale records. **All 22 required candidate mixed-top reference cases also pass**, with complete-record recomputation and retained raw evidence. The candidate is **ready** for contributor review; maintainer independent verification, eligibility and selection remain pending. The sections below preserve each checkpoint; the final section records complete mixed-top coverage.

The exact source was recovered independently from historical simulation commit `3dd17927ddcb842b4e28289270fa76436dcb4ab1` and published commit `9036f74f024088185398717989ed589784d1d151`, path `design/xtor/adc_comp/many-question-miyahara/BUFFER-V26.txt`; both Git objects are byte-identical to the restored `adc_comp.scs`.

- Full-file SHA-256: `c418be8ea46331a424b823cfc4991ec3b3a27124ff3ed6d26fbf383c5f3fee02`.
- Electrical SHA-256 (adcflow logical lines, no trailing newline): `13c455d69c414b141aa94d910b1adc256d7929e67997eb366a71d77660a59797`.
- Complete RNL checked with core 0.5.2: zero errors, warnings and hints. The canonical schematic is regenerated from this exact source.
- Previous B20 canonical source and all historical formal records are preserved at published commit `2579cdf3c91b81599ca5f9f74a1744495ddfc1ea` and in a verified 367-member archive. Archive SHA-256: `8c2b5cb4233470f4e2932b1bb33d71d894119d87fdd7b582643f2d934959c794`; every member passed CRC and SHA-256 readback. Historical records are not relabeled as B26 results.

## Why this source is being retested

[The original B26 report](BUFFER-V26.md) records FS/low/125 noise of 270.61635250554104 uV rms, profile interval [261.07, 280.60], under the then-current 240 uV limit. That old failure is preserved. Its point estimate is below the current 280 uV limit, but it does not establish current qualification or statistical margin. B26 had no complete TT or FF noise evidence and no full-corner qualification.

Historical TT baseline/tighter 30 mV delay is 48.97788988704756/48.99406817867042 ps against 50 ps. Input capacitance is 19.328731218738323 fF against 20 fF. These narrow margins are explicit first-round checks. Historical convergence failures of B25 and B27 are not attributed to B26.

## Restoration plan and source freeze

Main `ac9f7a3bd2c788345464e292a74271d7febe2f8c` is incorporated. Issues #131 and #136 are acknowledged for this candidate: CMP-13 280 uV, CMP-08 45 ps, unchanged TT CMP-01 200 uV and CMP-15, plus official per-device CMP-17 SOA including startup and the sliding-window short-overvoltage rule.

First run fresh official full 17 x 512 physical noise at TT, FF/low/125 and FS/low/125; TT delay/loading; representative official SOA and supporting 43/38/69 ps short-reset windows. Keep exact conservative numerical settings, physical stochastic sources and selective saves. If these gates pass, continue full 45-corner noise, delay, kickback and SOA, TT 50-sample mismatch, then mixed-top reference regression. A measured failure stops qualification expansion for this source and is retained with its raw evidence; no limit adjustment is requested by this restoration.

The source freeze is commit `3b2ed12336c037a478050173fb0df1bbb0524093`. Local `check all` passes with historical stale/failure warnings retained; unit tests: 507 passed, 1 deselected. The same head passes CI contracts, drawings, results and slow model budget; its latest site build passes (an earlier overlapping site event was cancelled).

## Fresh first-round support results

| Check | New measurement | Result |
|---|---|---|
| TT delay, 1 / 30 mV | 58.363019310610724 / 48.97788006995525 ps | PASS |
| TT reset / validity | 24.599628490454425 ps / zero violations | PASS |
| TT input / CLKC capacitance | 19.328731218738323 / 12.105038071102172 fF | PASS |
| TT net cycle kickback | 8.382100005407955e-5 uV | PASS |
| TT energy | 703.83253716 fJ | Reported only |

The official TT delay trace independently gives 36/36 correct decisions, including 10 uV, and 36/36 complete resets. Supporting shortened reset windows at TT (43 ps), FF/high/-40 (38 ps) and SS/low/125 (69 ps) give 108/108 correct decisions and complete resets, zero CMP-15 violations; largest measured reset times are respectively 24.708322433830446, 18.361194795382787 and 33.1894333450634 ps.

Private tighter delay repeats at TT, FS/high/-40 and SS/low/125 also give 108/108 correct decisions and complete resets. Effective reltol is 1e-6, vabstol 1e-8, conservative/gear2only, with no explicit maxstep. TT 30 mV delay is 48.99406814791336 ps, only 0.01618807795811 ps above the official baseline. These repeats do not overwrite official delay records.

Official SOA at TT and FS/SS/FF high/-40 checks 43 MOS devices and 129 terminal pairs at each corner. Peaks are respectively 0.96973, 1.05447, 1.04523 and 1.05162 V; zero violations and zero time above 1.1 V. The official FS/high/-40 crosscheck uses effective reltol 1e-8, vabstol 1e-8, traponly and maxstep 1 ps: peak 1.05395 V, zero violations; maximum pair-peak change is 0.77 mV across all 129 pairs.

All six completed support runs passed remote file SHA-256 matching and local ZIP CRC/member SHA-256 readback before exact owned remote-directory removal and absence confirmation. The retained archive SHA-256 values are:

| Run suffix (20261104) | Archive SHA-256 |
|---|---|
| 020312-b3ba-tb_comp_delay | `be25423a14d0d372adf342017d4226e00d991a8df3d38f95937eef3c4eb95350` |
| 020536-9d0e-tb_comp_kickback | `ca5a8a28efdf93333d5232b0a633fb4e76841cfbe354d96ce7458e84587a12d1` |
| 020740-fab1-tb_comp_soa | `780201174dd1c0e04b43635e20ee8c2cc3c0e2b6e289bc225363102c027f549e` |
| 021120-b26-short-reset | `62354e68326e2acbf30db4767b49a352ffe1edbbae549a51f798751a71d4e521` |
| 021536-51a8-tb_comp_delay | `e71badf782e00e93417662af8dece3bb31653e20284565a4ec0796505e8af41c` |
| 022006-81df-tb_comp_soa | `0eeeea08f4c0ee9b2495bb1bc6240f9c4113847a47a62f8b56e716cbff1f9816` |

## Fresh complete first-round noise

Official run `20261104-020301-0afb-tb_comp_noise`, source frozen at `3b2ed123`, completes all three corners with rc 0, 8704 finite decisions per corner and 512 at each of the 17 levels. Physical noise sources remain enabled at 50 GHz, seed 1; effective conservative/gear2only, reltol 1e-4, vabstol 1e-6.

| Corner | Noise uV rms | Profile 95% interval uV | Absolute offset mV | Verdict |
|---|---:|---|---:|---|
| tt_nom_27 | 171.1689355211837 | [163.72, 179.02] | 0.0015589625565931731 | PASS 200 / 280 |
| ff_low_125 | 265.46714680943654 | [256.03, 275.34] | 0.005122773432378509 | PASS 280 |
| fs_low_125 | 270.61635250554104 | [261.07, 280.60] | 0.005423585462778105 | PASS 280 |

The fresh FS point estimate exactly matches historical B26. Its confidence-interval upper bound exceeds 280 uV: passing the specified point-estimate criterion does not establish statistical margin. No historical data was reused to create these new records.

The noise run passed remote file SHA-256, local ZIP CRC/member SHA-256 and all per-level sample-count checks before exact remote removal and absence confirmation. Retained archive SHA-256: `b4d20a0aea22c7158326e919904485035627a85efa720ba6e30e92a0b754d612`.

All first-round gates pass. At that checkpoint the official records are 9 fresh / 101 total, with zero fresh errors or failures; the other 92 remain historical and stale. Full coverage has started on the same unchanged source: remaining 42 noise, 44 delay, 44 kickback and 41 SOA corners, followed by TT 50-sample mismatch. Mixed-top reference regression and lead verification are still outstanding. No full-corner qualification or eligibility is claimed.

## Full-corner progress

**All 45 delay corners pass.** Run `20261104-023424-9635-tb_comp_delay` adds the other 44 corners to the first-round TT record. The independent raw-trace audit checks all 1584 additional decisions, including 10 uV, and 1584 resets: all correct and complete. Combined with TT this is 1620/1620 correct decisions and complete resets; CMP-15 is zero at every corner.

| All-corner delay metric | Worst value | Corner | Limit |
|---|---:|---|---:|
| 1 mV delay | 95.93315453604286 ps | ss_low_m40 | 120 ps |
| Regeneration time constant | 5.956538105471581 ps | ss_low_m40 | 15 ps |
| Reset | 33.67068023981794 ps | ss_low_m40 | 45 ps |
| Losing-output peak | 3.3991580192599535 % VDD | ff_high_125 | Reported |

The delay checkpoint has 53 fresh / 101 total records, zero fresh errors or failures. Remaining noise, kickback, SOA and mismatch coverage is still running at that checkpoint. Passing delay does not substitute for those missing results.

The additional 44-corner delay run passed remote SHA-256 matching, ZIP CRC/member SHA-256 readback and exact remote absence checks. Retained archive SHA-256: `f077cc085ac97641740a316f36b6af6d471b5f59d5c4572cf332f3c444beb62c`. Together with the first-round archive, all 45 delay raw traces remain retained.

**All 45 kickback corners pass.** Run `20261104-025241-6c85-tb_comp_kickback` adds the remaining 44 corners. The maximum specified net cycle change is 0.00019991329988991446 uV at ff_high_125, against 40 uV. The independent audit checks all 360 finite samples across the two runs and exactly reproduces every formal kickback metric. These post-reset samples do not establish instantaneous differential or common-mode disturbance peaks. The largest first-to-second sample change, which is outside the formal cycle-difference calculation, is 0.21312963850001443 uV at ss_low_m40.

Input and CLKC capacitance limits apply at TT only: 19.328731218738323 fF against 20 fF and 12.105038071102172 fF against 16 fF. Across all corners the maxima are 20.6920524612635 fF at ff_low_m40 and 13.188213874014059 fF at ff_high_125, respectively; these non-TT values are reported without applying the TT acceptance limit.

The kickback checkpoint has **97 fresh / 101 total records**, zero fresh errors or failures. Remaining noise, SOA and mismatch coverage continues on unchanged B26. The additional kickback run passed remote SHA-256 matching, ZIP CRC/member SHA-256 readback, independent retention and exact remote absence checks. Retained archive SHA-256: `3cea078b673ce057594e89c2bf8870934d9bf950cb5aaf387bcd2b95cc524102`.

**All 45 official device-SOA corners pass.** Run `20261104-031039-87d3-tb_comp_soa` adds the remaining 41 corners. Every corner checks all 43 MOS devices and 129 unique terminal pairs; every pair passes, with zero time above 1.1 V. The largest absolute terminal voltage is **1.06660 V at fs_high_125**, below 1.1 V. A numerical crosscheck of this new all-corner maximum also passes; the first-round cold-corner crosscheck remains independently retained.

The SOA checkpoint has **138 fresh / 142 total records**, zero fresh errors or failures. The 41-corner SOA archive passed remote SHA-256 matching, local ZIP CRC/member SHA-256 readback, independent retention and exact remote absence checks. Retained archive SHA-256: `05ef545c9ed1f498e3a88cdbe1acca25feb0af856046bd3190f4debfdcbb301e`.

**TT mismatch passes with all 50 samples valid.** Official run `20261104-032902-58fd-tb_comp_offset_mc` uses local mismatch, seed 6303, samples 1..50 and no nominal sample. Sample standard deviation is **1.8476284955369302 mV** against 5 mV; mean is -0.6240234374804 mV and maximum absolute offset 4.647827147999999 mV. No sample is removed. An independent raw-text audit checks all 850 valid decisions, all 50 +/-25 mV range checks and +/-50 uV rechecks, and exactly reproduces the sample standard deviation.

The mismatch archive passed remote SHA-256 matching, ZIP CRC/member SHA-256 readback, independent retention and exact remote absence checks. Retained archive SHA-256: `604bc20f5d180abe211c636d3b1188e098abd0f0e16a3561551c71e2876edb21`. The checkpoint now has **139 fresh / 142 total records**, zero fresh errors or failures. Complete full-corner noise, mixed-top reference regression and lead verification remain outstanding.

The official fs_high_125 SOA crosscheck run `20261104-033222-7851-tb_comp_soa` repeats the unchanged baseline and tighter settings. Baseline peak is 1.06660 V; tighter peak **1.06636 V**, both with zero violations and zero time above 1.1 V. Effective tighter settings are reltol 1e-8, vabstol 1e-8, conservative/traponly, maxstep 1 ps; 84766 accepted points. The maximum peak change over all 129 terminal pairs is **0.52 mV** at XDUT.M15 ds. The original 41-corner raw batch remains retained alongside this repeat.

The worst-SOA crosscheck also passed remote SHA-256 matching, ZIP CRC/member SHA-256 readback, independent retention and exact remote absence checks. Retained archive SHA-256: `eab05c211b0c8c92d285cbc9962741e9755ba53ca0c6daa3cc3ccf9834568b35`.

## Analysis dependency update before mixed-top

Main `8838a8ed` (PR #144) replaces the ADCToolbox Git pin with the PyPI release 0.9.2. It changes no comparator source, specification or testbench. The update is merged before mixed-top work; the in-flight noise process retains its original environment. A separate 0.9.2 environment keeps the same NumPy, SciPy and Matplotlib versions. All 36 spectrum tests pass, the 80 dB SFDR self-check returns 79.99999999927381 dBc, and recomputing all metrics from the first three noise raw records gives exact matches. `adcflow check all` also passes on the updated baseline. Historical provenance remains unchanged.

## Complete block coverage: all 181 records pass

Run `20261104-023413-0c91-tb_comp_noise` completes the remaining 42 noise corners on the original frozen B26. Together with the first three corners, all **45 corners / 391680 decisions** are complete and finite, with exactly 512 samples at each of 17 input levels. All sample IDs are sequential and timestamps increase. Recomputing every noise metric from all 45 raw records in the current 0.9.2 analysis environment exactly reproduces the official records. The smallest sampled absolute output difference is 0.9623218632731313 VDD; no sample is below half VDD. This is a sampled-output diagnostic, not a substitute for full transient CMP-15 checks.

| Complete coverage | Result | Required limit |
|---|---:|---:|
| TT noise | 171.1689355211837 uV rms | 200 uV |
| Worst all-corner noise, fs_low_125 | 270.61635250554104 uV rms | 280 uV |
| Largest systematic absolute offset | 0.007260706202395702 mV | 2 mV |
| Delay / kickback / noise / device SOA | 45 fresh passing corners each | All 45 |
| TT local mismatch | 50 valid, 0 failed samples; sigma 1.8476284955369302 mV | 50 valid; sigma <= 5 mV |

The worst-noise profile interval remains [261.07, 280.60] uV: the upper endpoint exceeds 280 uV, so this is a pass of the specified point-estimate criterion, not proof of statistical margin. The source has not changed during qualification. There are now **181 fresh / 181 total official records**, zero stale records, errors or failed criteria. Mixed-top reference regression and lead verification are still required; block-test completion does not confer eligibility or selection.

The additional 42-corner noise run passed remote SHA-256 matching, all sample-count checks, local ZIP CRC/member SHA-256 readback, independent retention and exact remote absence checks. Retained archive SHA-256: `c70d84aa07e68b749ac2b90097792f2d21581a87bc7a5d1b9d5f6cb3b382d596`. All 13 completed block/support run archives remain independently retained; no active run was removed.

## Complete TT mixed-top reference

Private run `20261104-050042-e8e3-tb_top_sine`, dispatched at commit `5a495da13ac7308de6744e17b11b5f3f51886d56`, passes every applicable TT top-level criterion. Only the comparator is physical; the other blocks use their behavioral views. The B26 source is unchanged. The official test uses physical noise enabled, noisefmax 20 GHz, seed 1, 100 MS/s and a coherent 49.70703125 MHz input at -1 dBFS. Actual numerics are APS, conservative/gear2only, reltol 1e-4 and vabstol 1e-6, with no explicit maxstep.

| TT mixed-top metric | Complete-record result | Limit |
|---|---:|---:|
| Calibrated ENOB | 11.105496107814995 bit | 10.75 bit |
| SNDR | 68.61508656904627 dBc | Reported |
| SFDR | 84.96467972941828 dBc | 75 dBc |
| Fitted differential full-scale peak | 0.9936242025926828 V | 0.95 V |
| Maximum / mean conversion time | 2.591142 / 2.553408580078125 ns | Maximum 4.4 ns |
| Missing conversions / spikes beyond 3 LSB | 0 / 0 | 0 / 0 |
| Largest judged sine-fit deviation | 1.9025885121482133 LSB | Spike threshold 3 LSB |
| Nominal-weight ENOB | 11.049781362784447 bit | Reported |

The first 1024 conversions calibrate the bit weights; the next independent 1024 conversions form the judged record. All 2049 raw captures, including the final unused capture, have sequential IDs, binary 14-bit data and finite increasing times. The complete-record audit verifies the inferred clock intervals, the exact judged bit matrix, source and staged-file SHA-256, actual numerics and ADCToolbox 0.9.2 provenance. Remeasuring the complete raw record reproduces every reported metric exactly; the spectrum and code/error plots have also been inspected.

The raw archive passes remote SHA-256 matching, ZIP CRC and every member's SHA-256. A separately retained copy is verified before exact owned remote-directory removal and confirmed absence. Archive SHA-256: `489cffa177a89ae9fe715979cb9392f8f28cc7e75069cb3d66d8cdc772a1308d`.

This is candidate reference evidence with `do_record=False`; it creates no lead verification or formal top-level result. The remaining six high-frequency corners, TT low-frequency case and seven corners at both 45% and 55% duty (21 simulations) are in progress in a pool capped at six simulations. A measured failure stops new corner dispatches. WIP, qualification and selection status remain unchanged pending this coverage and lead review.

## Complete candidate mixed-top reference: all 22 jobs pass

The unchanged original B26 completes the required candidate reference coverage: seven quick corners of high-frequency sine, all seven quick corners at both 45% and 55% duty, and TT low-frequency sine. All 22 applicable verdict sets pass; every complete raw record has been audited and all 15 mixed-run archives independently retained. These are candidate reference runs with do_record=False, not lead verification or formal top-level records. The candidate is ready for contributor review; maintainer independent verification, eligibility and selection remain pending.

Every job uses 1024 calibration conversions and a separate 1024-conversion judged record: 22528 calibration and 22528 judged samples in total. There are 45071 raw captures including unused end captures. Raw IDs are sequential, times are finite and monotonic, and all 14 output bits are binary. Judged bit matrices, inferred clock intervals, source and staged-file hashes, actual numerics and ADCToolbox 0.9.2 provenance pass audit. Recomputing all complete-record metrics reproduces the saved values exactly. Across all jobs, missing conversions total 0 and reported spikes total 0.

Only the comparator is physical; the other blocks remain behavioral. Official physical noise is enabled at 20 GHz, seed 1. Effective numerics remain APS, conservative/gear2only, reltol 1e-4 and vabstol 1e-6, with no explicit maxstep. No source dimensions or electrical connections changed.

### High-frequency sine: seven quick corners

Each uses a coherent 49.70703125 MHz input at 100 MS/s. Acceptance is ENOB >= 10.5 bit (TT target >= 10.75), SFDR >= 75 dBc, differential full-scale peak >= 0.95 V, maximum conversion time <= 4.4 ns, and zero missing conversions or spikes.

| Corner | ENOB bit | SFDR dBc | Full-scale peak V | Maximum conversion ns |
|---|---:|---:|---:|---:|
| tt_nom_27 | 11.105496108 | 84.964679729 | 0.993624203 | 2.591142000 |
| ss_low_m40 | 11.188769425 | 85.177672240 | 0.993617718 | 3.106433000 |
| ss_low_125 | 10.877927674 | 82.899987440 | 0.993618331 | 2.798922000 |
| ff_high_m40 | 11.288915487 | 85.592107530 | 0.993559270 | 2.401017000 |
| ff_high_125 | 10.892905787 | 82.229925292 | 0.993740639 | 2.423909000 |
| fs_nom_27 | 11.102398660 | 85.170654602 | 0.993570387 | 2.556893000 |
| sf_nom_27 | 11.094569712 | 84.910536570 | 0.993636512 | 2.631593000 |

Unrounded limiting values: ENOB 10.877927674397561 bit at ss_low_125; SFDR 82.2299252917858 dBc at ff_high_125; maximum conversion time 3.106433 ns at ss_low_m40.

### Duty and low-frequency coverage

The duty acceptance limit is ENOB >= 10.5 bit for each variant.

| Corner | 45% duty ENOB bit | 55% duty ENOB bit |
|---|---:|---:|
| tt_nom_27 | 11.126948827 | 11.113336574 |
| ss_low_m40 | 11.258260620 | 11.303489512 |
| ss_low_125 | 10.883836508 | 10.893940501 |
| ff_high_m40 | 11.224664426 | 11.219388637 |
| ff_high_125 | 10.888871432 | 10.893641889 |
| fs_nom_27 | 11.145127888 | 11.195254040 |
| sf_nom_27 | 11.086628407 | 11.121538301 |

Minimum duty ENOB is 10.883836508214506 bit at ss_low_125, duty 0.45. TT low-frequency input is 1.074218750 MHz; ENOB is 11.244763346361777 bit against 10.8. Its SFDR is 86.76991379714964 dBc and maximum conversion time is 2.590921 ns (reported).

### Retained original mixed-run evidence

All runs passed remote file SHA-256 matching, ZIP CRC and every archive member SHA-256. A separate retained copy was verified before exact owned remote-directory removal, followed by confirmed remote absence. The 13 earlier block/support archives remain retained alongside these 15 mixed-run archives.

| Run | Archive SHA-256 |
|---|---|
| 20261104-050042-e8e3-tb_top_sine | `489cffa177a89ae9fe715979cb9392f8f28cc7e75069cb3d66d8cdc772a1308d` |
| 20261104-060550-1fee-tb_top_duty | `8276825b166c611b783e9e51993d1b2ccbfb6655467f9250de558a4a678cb7d5` |
| 20261104-060550-2fe7-tb_top_duty | `b51d29098e0ac7f7243ceaa8aaa5a9564725d8005b62a4a455c5986234df4d8f` |
| 20261104-060550-4e1e-tb_top_sine | `d465bac5ed4b7d9cd9bc970befb51b70c6dc6fd0a011e50d763e228b0562a7ce` |
| 20261104-060550-da8f-tb_top_duty | `a82559c9e2e56b496a0a7b6977289ed96018a6b69c6497e30e80a2c1fc1ddc8f` |
| 20261104-060550-e409-tb_top_sine | `de92c9c44666bbe1a268a36111264ac5fcc0ac3580cf7983b2eb91934f5c7fad` |
| 20261104-060550-f9c3-tb_top_duty | `30a353b63a24b7d2e2b87285608617bba0a1986475755622466a4269667301eb` |
| 20261104-070345-498b-tb_top_duty | `ef9814caf83f5f4eb4ae244300684baa9078b9593b2c53ea604e894e6ad5b6fd` |
| 20261104-070806-5cac-tb_top_duty | `bdcb48b3045579c57a6740d13ac8c69f5a14f50241be8c0738d6e0dac8763749` |
| 20261104-075912-b7e8-tb_top_duty | `887b47815dc5628aa0f5fd703f1d323ea2ed01ea8bba93fa11fadcab4510a851` |
| 20261104-080025-6156-tb_top_sine | `5803b8198c24e92ed5ab086b75f4222efb558f8901628c61c3a13b4d060b6246` |
| 20261104-080059-89d2-tb_top_sine | `404a1f77b37c90e7223513d030e371945c81bf5bee68a3e68198c729c9c69fd3` |
| 20261104-080059-a8a1-tb_top_sine | `e72f9e8792dd264c0543f774d3738550bd3b3a6426bbe25550dd5d106d742af9` |
| 20261104-090315-f2a6-tb_top_sine | `27f95cd2a63a154d7c902890e8ad40936c4cd9477532b552f81c0a237e73577a` |
| 20261104-090447-6c9c-tb_top_sine_lf | `d74336798022b767bd715ef841ea5dbb4a11b74031f931b4681b89a67ccb448a` |
