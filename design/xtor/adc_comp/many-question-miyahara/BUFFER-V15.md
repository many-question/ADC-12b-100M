# BUFFER-V15: restore buffer-node edge margin

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

B14's first SF/high/-40 and FS/high/-40 screens pass all 72 actual polarities, resets and output-validity checks, but FS fails six terminal-stress pairs. The actual BN maximum is 1.000091633924 V at 23.997853 ps after a rising midpoint, with CLKC=0.99 V and CKB=0.129335 V. BP similarly reaches 1.000089066299 V. SF peaks at 0.99991 V. B14 stops before TT and noise; no noise improvement has yet been demonstrated for its stronger interstage PMOS drive.

This source changes only CBP/CBN, the physical buffer-node MOMs, from 16 to 20 fingers, nominally 4.46 to 5.66049 fF. It tests additional edge-charge storage at the two observed overvoltage nodes. All 43 MOS devices, including B14's M14/M15 P6 drivers, and the other seven MOMs are electrically unchanged. This repairs an observed edge-margin problem; it does not assume that added capacitance fixes the B13 noise mechanism. Added buffer delay and reset charge must be measured.

The new capacitor callback succeeds without warnings; its SHA-256 is `613c7aa6a617bd67d2699ba18a547794f801dbaee33aeab31e6b964b5ba9cc5d`. Electrical SHA-256: `5006ef01a47d58de546a7925aa88a7ea9d7730b43632efcaf676d28974223d94`. The [source](BUFFER-V15.txt) contains 43 MOS and 9 MOMs, with complete RNL checked on a byte-identical mirror. Canonical B13, its four formal hot noise failures and the B14 stress failure remain preserved.

First repeat SF/high/-40 and FS/high/-40. If they pass, TT and FS/low/125 deterministic screens precede the matched TT/worst-corner noise diagnosis. Broader known-corner coverage, actual-worst convergence, canonical promotion and genuine original formal gates remain to establish.

![Physical comparator with larger buffer-node MOMs](https://raw.githubusercontent.com/many-question/ADC-12b-100M/1c82358bd327c795fc38a0b3ac1e63faf73429e5/design/xtor/adc_comp/many-question-miyahara/buffer-v15.png)

## Completed screen 20261031-082247-miyahara-buffer-v15-screen

Both initial high-voltage cold corners pass all 72 actual polarities, including 10 uV, all resets, timing, physical output validity and all 129 terminal pairs. The approximately 20 uV FS stress margin motivates tighter numerics before considering promotion.

Actual clean source commit: `51a243cefebb4ae383a1e738c4786fff4a18bbd1`. Electrical SHA-256: `5006ef01a47d58de546a7925aa88a7ea9d7730b43632efcaf676d28974223d94`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 50.640570 / 41.822053 | 20.982410 | 744.198121 | 36 / 36 | 0 | 0 | 0.99998 | 0 / 129 |
| sf_high_m40 | 54.930659 / 45.180408 | 21.597744 | 800.939434 | 36 / 36 | 0 | 0 | 0.99984 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70380 | 0.76899 |
| MINN | 0.70391 | 0.76917 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99304 | 0.99194 |
| M15 | 0.99304 | 0.99194 |
| M12 | 0.99294 | 0.99294 |
| M13 | 0.99294 | 0.99294 |
| M10 | 0.98686 | 0.98183 |
| M11 | 0.98686 | 0.98183 |
| M6 | 0.99391 | 0.99509 |
| M7 | 0.99391 | 0.99509 |
| M8 | 0.99391 | 0.99509 |
| M9 | 0.99391 | 0.99509 |
| MCKN | 0.99000 | 0.99151 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99391 | 0.99509 |
| MRQN | 0.99391 | 0.99509 |
| MAP | 0.99304 | 0.99194 |
| MAN | 0.99304 | 0.99194 |
| MBPP | 0.98773 | 0.98281 |
| MBPN | 0.99998 | 0.99984 |
| MOPP | 0.98746 | 0.97907 |
| MOPN | 0.99998 | 0.99984 |
| MBNP | 0.98773 | 0.98278 |
| MBNN | 0.99997 | 0.99983 |
| MONP | 0.98746 | 0.97907 |
| MONN | 0.99997 | 0.99983 |
| MDDP | 0.98425 | 0.98640 |
| MDDN | 0.98703 | 0.98796 |
| MUPRP1 | 0.99391 | 0.99509 |
| MUPRN1 | 0.99391 | 0.99509 |
| MUPBP1 | 0.99998 | 0.99984 |
| MUPBN1 | 0.99997 | 0.99983 |
| MUPOUTP1 | 0.99000 | 0.99197 |
| MUPOUTN1 | 0.99000 | 0.99197 |
| MDNOUTP1 | 0.98763 | 0.99197 |
| MDNOUTP2 | 0.98763 | 0.99197 |
| MDNOUTN1 | 0.98763 | 0.99197 |
| MDNOUTN2 | 0.98763 | 0.99197 |
| MCKUP | 0.99000 | 0.99151 |
| MBLEED | 0.99000 | 0.99151 |
| MUPXP | 0.99222 | 0.99294 |
| MUPXN | 0.99222 | 0.99294 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-082954-miyahara-buffer-v15-screen

TT and the known worst B13 noise corner FS/low/125 pass all 72 actual polarities, resets, timing, physical output validity and all 129 terminal pairs. These noiseless checks do not establish any noise benefit.

Actual clean source commit: `51a243cefebb4ae383a1e738c4786fff4a18bbd1`. Electrical SHA-256: `5006ef01a47d58de546a7925aa88a7ea9d7730b43632efcaf676d28974223d94`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_low_125 | 69.070684 / 53.412240 | 26.136200 | 448.534099 | 36 / 36 | 0 | 0 | 0.81248 | 0 / 129 |
| tt_nom_27 | 57.546945 / 46.641150 | 23.988784 | 573.034820 | 36 / 36 | 0 | 0 | 0.90877 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_low_125 | tt_nom_27 |
|---|---:|---:|
| MINP | 0.54155 | 0.60585 |
| MINN | 0.54155 | 0.60594 |
| MTAIL | 0.81000 | 0.90000 |
| M14 | 0.81121 | 0.90190 |
| M15 | 0.81121 | 0.90190 |
| M12 | 0.81069 | 0.90202 |
| M13 | 0.81134 | 0.90202 |
| M10 | 0.80012 | 0.89284 |
| M11 | 0.80012 | 0.89284 |
| M6 | 0.79862 | 0.90196 |
| M7 | 0.79862 | 0.90196 |
| M8 | 0.80796 | 0.90196 |
| M9 | 0.81134 | 0.90196 |
| MCKN | 0.81000 | 0.90169 |
| MCKP | 0.81000 | 0.90000 |
| MRQP | 0.80950 | 0.90196 |
| MRQN | 0.80950 | 0.90196 |
| MAP | 0.81121 | 0.90190 |
| MAN | 0.81134 | 0.90190 |
| MBPP | 0.80787 | 0.89538 |
| MBPN | 0.81248 | 0.90877 |
| MOPP | 0.80346 | 0.89337 |
| MOPN | 0.81248 | 0.90877 |
| MBNP | 0.80786 | 0.89536 |
| MBNN | 0.81248 | 0.90876 |
| MONP | 0.80346 | 0.89337 |
| MONN | 0.81248 | 0.90876 |
| MDDP | 0.80796 | 0.89764 |
| MDDN | 0.81134 | 0.90045 |
| MUPRP1 | 0.81000 | 0.90196 |
| MUPRN1 | 0.81000 | 0.90196 |
| MUPBP1 | 0.81248 | 0.90877 |
| MUPBN1 | 0.81248 | 0.90876 |
| MUPOUTP1 | 0.81000 | 0.90000 |
| MUPOUTN1 | 0.81000 | 0.90000 |
| MDNOUTP1 | 0.80251 | 0.89973 |
| MDNOUTP2 | 0.80251 | 0.89973 |
| MDNOUTN1 | 0.80251 | 0.89973 |
| MDNOUTN2 | 0.80251 | 0.89973 |
| MCKUP | 0.81000 | 0.90169 |
| MBLEED | 0.81000 | 0.90169 |
| MUPXP | 0.81069 | 0.90202 |
| MUPXN | 0.81069 | 0.90202 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-083004-miyahara-buffer-v15-screen

The tighter FS/high/-40 run passes all 36 actual polarities, resets, timing, physical validity and all terminal pairs. Its very small stress margin is retained as an unresolved robustness concern; no canonical promotion follows from these screens.

Actual clean source commit: `51a243cefebb4ae383a1e738c4786fff4a18bbd1`. Electrical SHA-256: `5006ef01a47d58de546a7925aa88a7ea9d7730b43632efcaf676d28974223d94`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 50.641584 / 41.821896 | 20.940190 | 744.201121 | 36 / 36 | 0 | 0 | 0.99999 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 |
|---|---:|
| MINP | 0.70379 |
| MINN | 0.70391 |
| MTAIL | 0.99000 |
| M14 | 0.99305 |
| M15 | 0.99305 |
| M12 | 0.99295 |
| M13 | 0.99295 |
| M10 | 0.98687 |
| M11 | 0.98687 |
| M6 | 0.99391 |
| M7 | 0.99391 |
| M8 | 0.99391 |
| M9 | 0.99391 |
| MCKN | 0.99000 |
| MCKP | 0.99000 |
| MRQP | 0.99391 |
| MRQN | 0.99391 |
| MAP | 0.99305 |
| MAN | 0.99305 |
| MBPP | 0.98773 |
| MBPN | 0.99999 |
| MOPP | 0.98747 |
| MOPN | 0.99999 |
| MBNP | 0.98773 |
| MBNN | 0.99998 |
| MONP | 0.98746 |
| MONN | 0.99998 |
| MDDP | 0.98425 |
| MDDN | 0.98703 |
| MUPRP1 | 0.99391 |
| MUPRN1 | 0.99391 |
| MUPBP1 | 0.99999 |
| MUPBN1 | 0.99998 |
| MUPOUTP1 | 0.99000 |
| MUPOUTN1 | 0.99000 |
| MDNOUTP1 | 0.98765 |
| MDNOUTP2 | 0.98765 |
| MDNOUTN1 | 0.98765 |
| MDNOUTN2 | 0.98765 |
| MCKUP | 0.99000 |
| MBLEED | 0.99000 |
| MUPXP | 0.99223 |
| MUPXN | 0.99223 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Numerical margin and next diagnostic

The unrounded maximum over all 129 terminal pairs at 0.125 ps / 1e-7 / 1e-9 is 0.999986654921 V (MBPN ds), only 13.345079 uV below 1 V, at 23.906897971 ps from the nearest rising midpoint. This independent raw calculation agrees with the shared SOA evaluator's rounded 0.99999 V maximum; the earlier near-plateau annotation is not substituted for the peak.

Relative to 0.5 ps / 1e-6 / 1e-8, the largest change across the full rounded pair table is 20.000 uV, with a 10 uV table resolution. Tight-minus-reference changes are +0.001014098 ps at 1 mV, -0.000157645 ps at 30 mV, -0.042219911 ps reset and +0.003000096 fJ/cycle. Both settings pass, but this does not demonstrate broad voltage margin. If the early noise diagnosis is useful, this narrow point requires further convergence assessment before promotion, in addition to all remaining known corners.

The next private diagnosis compares TT and FS/low/125 with the same short +/-800 uV, 128 cycles per level, 50 GHz, seed-1 protocol used for B13. It retains the input, interstage, regeneration and output phases plus all device currents. No result is yet available for this source, and no B13 formal pass transfers.

## Matched TT and worst-corner noise phase diagnosis

Run `20261031-084454-miyahara-buffer-v15-noise-phase-diagnostic-screen` uses clean source `6f4090883bd5bfa9de75ff7d823f0be19c6aae27`, electrical SHA-256 `5006ef01a47d58de546a7925aa88a7ea9d7730b43632efcaf676d28974223d94`. Both corners retain the B13 short diagnostic's +/-800 uV, 128 decisions per level, 50 GHz bandwidth, seed 1, 0.5 ps / 1e-6 / 1e-8 integration, 10 fF load and VCM 0.49 V. The comparator source changes, while the testbench hash, numerical settings and protocol match the earlier diagnostic exactly.

| Corner | OUTP at -800 / +800 uV | Wrong / 256 | Reset max (ps) | Max MOS stress (V) |
|---|---:|---:|---:|---:|
| tt_nom_27 | 0 / 128 | 0 | 23.942245420 | 0.90525 |
| fs_low_125 | 5 / 127 | 6 | 26.223278556 | 0.81178 |

All 256 resets complete in each corner. There are zero +80 ps or +150 ps to final sign changes, late-reset, output-validity or full-trace stress violations. All 129 terminal pairs are checked. The six FS errors occur at cycles 10, 53, 58, 70, 77 and 157, with all samples retained. At +50 ps RP-RN already has those six errors and its sign matches every final decision. This sample does not show new late interface errors, but it does not rule out earlier coupled interface contributions.

B13 had 0/256 TT and 11/256 FS errors. These finite counts and the following phase statistics show a partial improvement; they do not establish a formal noise limit or isolate the PMOS-driver contribution from the buffer-capacitor change. Gains are two-level secants. SNR is the average of each level’s absolute differential mean divided by its sample standard deviation.

| Phase and node | TT gain B13 / B15 | FS gain B13 / B15 | TT SNR B13 / B15 | FS SNR B13 / B15 |
|---|---:|---:|---:|---:|
| +20 ps DP_minus_DN | -3.584914 / -3.506789 | -3.021849 / -2.956183 | 4.114767 / 4.014832 | 3.308228 / 3.194453 |
| +30 ps DP_minus_DN | -4.702372 / -4.553212 | -2.090033 / -2.249823 | 4.964894 / 4.945071 | 3.480239 / 3.561494 |
| +30 ps XP_minus_XN | 12.159094 / 11.979471 | 6.680821 / 6.881498 | 3.852014 / 3.869898 | 2.423817 / 2.577531 |
| +30 ps RP_minus_RN | 1.089267 / 2.020416 | 0.714084 / 1.441994 | 1.182964 / 1.990195 | 0.703461 / 1.252984 |
| +40 ps RP_minus_RN | 28.295436 / 40.142838 | 7.557355 / 12.734365 | 4.247585 / 4.390070 | 1.852117 / 2.265981 |
| +50 ps RP_minus_RN | 197.918410 / 322.821752 | 28.558021 / 59.577713 | 4.337550 / 4.675992 | 1.706169 / 2.198461 |

At FS +20 and +30 ps, the input-stage differential sign is correct for every cycle, including the six whose final output is wrong. B15 improves RP transfer at +30/+40 ps, but much of the input discrimination is still lost before the settled internal decision. CKB normalized trajectories remain similar. The stage and time dependence supports a release-path loading test; it does not identify an isolated physical noise source.

| +30 ps drain-current mean (uA) | TT | FS low/hot |
|---|---:|---:|
| M14 | -517.956963 | -553.247631 |
| M12 | 211.656027 | 196.877403 |
| M10 | -105.799836 | -135.640959 |
| M8 | 153.366691 | 112.167711 |
| MRQP | 31.770434 | 47.350521 |
| MUPRP1 | -155.866855 | -100.008746 |

These are terminal currents with displacement contributions, not isolated channel-current or noise estimates. [BUFFER-V16](BUFFER-V16.md) tests only MRQP/MRQN N4-to-N2 geometry with all capacitors and other devices fixed. Reset speed, changed CKB loading and terminal excursions must be rechecked. B15 remains unpromoted; its six residual worst-corner errors and separate 13.345 uV cold stress margin are preserved.

| Device | TT maximum stress (V) | FS low/hot maximum stress (V) |
|---|---:|---:|
| MINP | 0.59558 | 0.49230 |
| MINN | 0.59595 | 0.49236 |
| MTAIL | 0.90017 | 0.81000 |
| M14 | 0.90238 | 0.81178 |
| M15 | 0.90234 | 0.81164 |
| M12 | 0.90240 | 0.81139 |
| M13 | 0.90249 | 0.81148 |
| M10 | 0.89328 | 0.80104 |
| M11 | 0.89330 | 0.80102 |
| M6 | 0.90253 | 0.79950 |
| M7 | 0.90253 | 0.79950 |
| M8 | 0.90253 | 0.80640 |
| M9 | 0.90243 | 0.80637 |
| MCKN | 0.90225 | 0.81022 |
| MCKP | 0.90000 | 0.81000 |
| MRQP | 0.90253 | 0.81022 |
| MRQN | 0.90243 | 0.81022 |
| MAP | 0.90238 | 0.81178 |
| MAN | 0.90226 | 0.81164 |
| MBPP | 0.89581 | 0.80814 |
| MBPN | 0.90525 | 0.81176 |
| MOPP | 0.89008 | 0.80067 |
| MOPN | 0.90525 | 0.81176 |
| MBNP | 0.89589 | 0.80823 |
| MBNN | 0.90517 | 0.81170 |
| MONP | 0.88964 | 0.80016 |
| MONN | 0.90517 | 0.81170 |
| MDDP | 0.89754 | 0.80640 |
| MDDN | 0.89751 | 0.80637 |
| MUPRP1 | 0.90253 | 0.81000 |
| MUPRN1 | 0.90243 | 0.81000 |
| MUPBP1 | 0.90525 | 0.81176 |
| MUPBN1 | 0.90517 | 0.81170 |
| MUPOUTP1 | 0.90028 | 0.81000 |
| MUPOUTN1 | 0.90019 | 0.81000 |
| MDNOUTP1 | 0.90028 | 0.80323 |
| MDNOUTP2 | 0.90028 | 0.80323 |
| MDNOUTN1 | 0.90019 | 0.80316 |
| MDNOUTN2 | 0.90019 | 0.80316 |
| MCKUP | 0.90225 | 0.81022 |
| MBLEED | 0.90225 | 0.81022 |
| MUPXP | 0.90240 | 0.81139 |
| MUPXN | 0.90249 | 0.81148 |

Raw/deck hashes and every archive member are verified; archive SHA-256 `6b78f39c18c050006136ccd82cff98e3510732f0988b87e654ca1dd2374a7b7b` includes the full phase comparison and all error-cycle indices. The exact owned remote run is confirmed absent. Original canonical and formal result/figure files are unchanged.

The 102.5 ns duration sets noisefmin near 9.7561 MHz, versus 287.216 kHz in the original formal test, and read-only samplers add time points. This two-level experiment is not a formal 240 uV result. B13’s four actual formal failures remain unchanged; no new formal pass or failure is fabricated.
