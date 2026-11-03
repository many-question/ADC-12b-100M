# Original B26 restoration under adc_comp 0.11.0

The current canonical source is the original physical B26: 43 MOS devices and nine MOM capacitors. No dimensions, parasitics, connections or numerical settings were changed to restore it. It remains **WIP, unqualified and unselected** pending fresh measurements.

The exact source was recovered independently from historical simulation commit `3dd17927ddcb842b4e28289270fa76436dcb4ab1` and published commit `9036f74f024088185398717989ed589784d1d151`, path `design/xtor/adc_comp/many-question-miyahara/BUFFER-V26.txt`; both Git objects are byte-identical to the restored `adc_comp.scs`.

- Full-file SHA-256: `c418be8ea46331a424b823cfc4991ec3b3a27124ff3ed6d26fbf383c5f3fee02`.
- Electrical SHA-256 (adcflow logical lines, no trailing newline): `13c455d69c414b141aa94d910b1adc256d7929e67997eb366a71d77660a59797`.
- Complete RNL checked with core 0.5.2: zero errors, warnings and hints. The canonical schematic is regenerated from this exact source.
- Previous B20 canonical source and all historical formal records are preserved at published commit `2579cdf3c91b81599ca5f9f74a1744495ddfc1ea` and in a verified 367-member archive. Archive SHA-256: `8c2b5cb4233470f4e2932b1bb33d71d894119d87fdd7b582643f2d934959c794`; every member passed CRC and SHA-256 readback. Historical records are not relabeled as B26 results.

## Why this source is being retested

[The original B26 report](BUFFER-V26.md) records FS/low/125 noise of 270.61635250554104 uV rms, profile interval [261.07, 280.60], under the then-current 240 uV limit. That old failure is preserved. Its point estimate is below the current 280 uV limit, but it does not establish current qualification or statistical margin. B26 had no complete TT or FF noise evidence and no full-corner qualification.

Historical TT baseline/tighter 30 mV delay is 48.97788988704756/48.99406817867042 ps against 50 ps. Input capacitance is 19.328731218738323 fF against 20 fF. These narrow margins are explicit first-round checks. Historical convergence failures of B25 and B27 are not attributed to B26.

## Current qualification plan

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
