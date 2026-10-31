# BUFFER-V20: stronger CKB rise for hot slow reset

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

B19 repairs the buffer-node high-voltage cold stress but fails SS/low/125 reset at 36.016839 ps against 35 ps. All 180 actual polarities and completed resets, output validity and terminal stress pass across its five initial corners; the reset-time failure still stops noise and broader expansion. At its worst SS cycle, CKB reaches 50%/90% after 8.523814/17.044882 ps, both RP/RN fall below 30% after 22.157436 ps, both BP/BN exceed 90% after 30.059430 ps, and the external outputs reset after 36.016839 ps. [BUFFER-V19.md](BUFFER-V19.md) preserves the source, failure and measured path.

This source retains all B19 P8 interstage drivers, N2 clock pull-down, N4 regeneration reset assists and 40-finger buffer capacitors. Only the CKB inverter PMOS MCKP changes from 3 um/nf3 to 4 um/nf4, with 30 nm length and 1 um finger width fixed. All other 42 MOS devices and all nine MOMs are electrically identical to B19.

The stronger pull-up tests earlier CKB assertion and reset-assist conduction while retaining the repaired BP/BN capacitance. Its added loading and changed drive also affect input clock charge, release, stress and noise, so the reset benefit is not assumed. This does not establish a P8 interstage noise benefit.

The successful zero-warning callback supplies the full geometry and parasitics, SHA-256 `8d2096c6b74343943491aeda9c02802217e12d4ab27360776cf0eeff75c274cd`. Electrical SHA-256: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The [source](BUFFER-V20.txt) contains 43 MOS and 9 MOMs with complete RNL checked on a byte-identical mirror.

The first batch covers the failing SS/low/125 corner and both SF/FS high/-40 stress corners. TT and FS/low/125 follow only if that batch passes, before a matched short noise-phase diagnosis. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and original formal tests remain open. The canonical source and every genuine original record remain unchanged.

![Physical comparator experiment](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fc05ec9b504909d82e993df12fa475fd234cba5b/design/xtor/adc_comp/many-question-miyahara/buffer-v20.png)

## Completed screen 20261031-102938-miyahara-buffer-v20-screen

All 108 actual polarities including 10 uV and all 108 resets pass, with timing, physical output validity and every one of 129 MOS terminal pairs passing at every tested corner. These private deterministic results do not establish noise qualification.

Actual clean source commit: `18c95a63fd5c79496565103539273796c5bcbc19`. Electrical SHA-256: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 51.558055 / 43.016245 | 21.391235 | 764.629714 | 36 / 36 | 0 | 0 | 0.99963 | 0 / 129 |
| sf_high_m40 | 55.860299 / 46.287336 | 22.270989 | 822.625707 | 36 / 36 | 0 | 0 | 0.99974 | 0 / 129 |
| ss_low_125 | 81.506934 / 65.856608 | 33.697683 | 423.235972 | 36 / 36 | 0 | 0 | 0.81640 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 | ss_low_125 |
|---|---:|---:|---:|
| MINP | 0.70397 | 0.76921 | 0.53997 |
| MINN | 0.70408 | 0.76937 | 0.53996 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 |
| M14 | 0.99299 | 0.99187 | 0.80955 |
| M15 | 0.99299 | 0.99187 | 0.80955 |
| M12 | 0.99290 | 0.99295 | 0.81191 |
| M13 | 0.99290 | 0.99295 | 0.81191 |
| M10 | 0.98740 | 0.98227 | 0.80270 |
| M11 | 0.98740 | 0.98227 | 0.80271 |
| M6 | 0.99393 | 0.99516 | 0.81033 |
| M7 | 0.99393 | 0.99516 | 0.81033 |
| M8 | 0.99393 | 0.99516 | 0.81033 |
| M9 | 0.99393 | 0.99516 | 0.81033 |
| MCKN | 0.99216 | 0.99457 | 0.81485 |
| MCKP | 0.99000 | 0.99000 | 0.81000 |
| MRQP | 0.99393 | 0.99516 | 0.81485 |
| MRQN | 0.99393 | 0.99516 | 0.81485 |
| MAP | 0.99299 | 0.99187 | 0.81000 |
| MAN | 0.99299 | 0.99187 | 0.81005 |
| MBPP | 0.98879 | 0.98527 | 0.80796 |
| MBPN | 0.99962 | 0.99974 | 0.81640 |
| MOPP | 0.98520 | 0.97896 | 0.80274 |
| MOPN | 0.99962 | 0.99974 | 0.81640 |
| MBNP | 0.98876 | 0.98524 | 0.80795 |
| MBNN | 0.99963 | 0.99974 | 0.81639 |
| MONP | 0.98520 | 0.97895 | 0.80274 |
| MONN | 0.99963 | 0.99974 | 0.81639 |
| MDDP | 0.98421 | 0.98632 | 0.80829 |
| MDDN | 0.98697 | 0.98792 | 0.81005 |
| MUPRP1 | 0.99393 | 0.99516 | 0.81033 |
| MUPRN1 | 0.99393 | 0.99516 | 0.81033 |
| MUPBP1 | 0.99962 | 0.99974 | 0.81640 |
| MUPBN1 | 0.99963 | 0.99974 | 0.81639 |
| MUPOUTP1 | 0.99000 | 0.99000 | 0.81000 |
| MUPOUTN1 | 0.99000 | 0.99000 | 0.81000 |
| MDNOUTP1 | 0.98572 | 0.98944 | 0.80717 |
| MDNOUTP2 | 0.98572 | 0.98944 | 0.80717 |
| MDNOUTN1 | 0.98572 | 0.98944 | 0.80717 |
| MDNOUTN2 | 0.98572 | 0.98944 | 0.80717 |
| MCKUP | 0.99216 | 0.99457 | 0.81485 |
| MBLEED | 0.99216 | 0.99457 | 0.81485 |
| MUPXP | 0.99239 | 0.99295 | 0.81191 |
| MUPXN | 0.99239 | 0.99295 | 0.81191 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-103735-miyahara-buffer-v20-screen

All 72 actual polarities including 10 uV and all 72 resets pass, with timing, physical output validity and every one of 129 MOS terminal pairs passing at every tested corner. These private deterministic results do not establish noise qualification.

Actual clean source commit: `18c95a63fd5c79496565103539273796c5bcbc19`. Electrical SHA-256: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_low_125 | 67.978960 / 53.559049 | 26.681001 | 463.986884 | 36 / 36 | 0 | 0 | 0.81245 | 0 / 129 |
| tt_nom_27 | 58.345753 / 47.855950 | 24.623750 | 590.833389 | 36 / 36 | 0 | 0 | 0.90849 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_low_125 | tt_nom_27 |
|---|---:|---:|
| MINP | 0.54148 | 0.60605 |
| MINN | 0.54148 | 0.60613 |
| MTAIL | 0.81000 | 0.90000 |
| M14 | 0.81114 | 0.90184 |
| M15 | 0.81114 | 0.90184 |
| M12 | 0.81092 | 0.90204 |
| M13 | 0.81109 | 0.90204 |
| M10 | 0.80140 | 0.89353 |
| M11 | 0.80140 | 0.89353 |
| M6 | 0.80160 | 0.90296 |
| M7 | 0.80160 | 0.90296 |
| M8 | 0.80776 | 0.90296 |
| M9 | 0.81109 | 0.90296 |
| MCKN | 0.81107 | 0.90440 |
| MCKP | 0.81000 | 0.90000 |
| MRQP | 0.81107 | 0.90440 |
| MRQN | 0.81107 | 0.90440 |
| MAP | 0.81114 | 0.90184 |
| MAN | 0.81114 | 0.90184 |
| MBPP | 0.81041 | 0.89782 |
| MBPN | 0.81245 | 0.90849 |
| MOPP | 0.80299 | 0.89255 |
| MOPN | 0.81245 | 0.90849 |
| MBNP | 0.81040 | 0.89780 |
| MBNN | 0.81245 | 0.90849 |
| MONP | 0.80299 | 0.89255 |
| MONN | 0.81245 | 0.90849 |
| MDDP | 0.80776 | 0.89759 |
| MDDN | 0.81109 | 0.90037 |
| MUPRP1 | 0.81041 | 0.90296 |
| MUPRN1 | 0.81040 | 0.90296 |
| MUPBP1 | 0.81245 | 0.90849 |
| MUPBN1 | 0.81245 | 0.90849 |
| MUPOUTP1 | 0.81000 | 0.90000 |
| MUPOUTN1 | 0.81000 | 0.90000 |
| MDNOUTP1 | 0.80210 | 0.89809 |
| MDNOUTP2 | 0.80210 | 0.89809 |
| MDNOUTN1 | 0.80210 | 0.89809 |
| MDNOUTN2 | 0.80210 | 0.89809 |
| MCKUP | 0.81107 | 0.90440 |
| MBLEED | 0.81107 | 0.90440 |
| MUPXP | 0.81092 | 0.90204 |
| MUPXN | 0.81092 | 0.90204 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


Across these initial corners, 180 actual polarities and resets pass. TT 1/30 mV delay is 58.345753123/47.855950073 ps, reset 24.623749574 ps, and mixed-sequence clock capacitance 11.281624839 fF. This clock estimate is diagnostic and does not replace the original formal capacitance test. A matched short phase diagnosis follows before broader expansion; no formal noise pass or canonical promotion is claimed.

The independently recomputed unrounded maxima at the initial screened corners are:

| Corner | Worst device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| fs_high_m40 | MBNN ds | 0.999626855694 | 373.144305913 | 23.738486161 | -176.261513839 |
| sf_high_m40 | MBNN ds | 0.999739956101 | 260.043899005 | 25.990030297 | -174.009969703 |
| ss_low_125 | MBPN ds | 0.816395903000 | 183604.097000176 | 35.670503541 | -164.329496459 |

These 0.5 ps results require actual-worst tighter integration if the source advances. Full AVDD waveform integrals include physical reset and weak rail loads over all 36 cycles and the same 100 ps–14.5 ns window. All supply probes are present and KCL closes to numerical precision.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 764.630123210 | 281.581625446 | 483.048497764 | 1491.783730647 |
| sf_high_m40 | 822.625982495 | 314.737451927 | 507.888530568 | 1659.189744730 |
| ss_low_125 | 423.236301444 | 147.933948895 | 275.302352549 | 741.666725612 |
| fs_low_125 | 463.987205185 | 173.966889380 | 290.020315805 | 819.483631885 |
| tt_nom_27 | 590.833742059 | 217.092116290 | 373.741625769 | 1155.452499163 |

Every archived entry was read back with CRC and SHA-256 verification before duplicate local raw files were removed; owned remote runs are absent.

- `20261031-102938-miyahara-buffer-v20-screen`: `949055c9cb427837121ceb84c34a74118cf4cb6e6e2c94e52e8f7516b86cfc72`.
- `20261031-103735-miyahara-buffer-v20-screen`: `c562cccaa123be0ca480ba1bcae70736078bbada5f19b0003e5144c8cfd5c39f`.


Matched SS/low/125 traces compare all 36 reset cycles directly with B19. Only MCKP geometry changes between the electrical sources. Worst external reset changes from 36.016838870 to 33.697682808 ps. The following per-cycle timing deltas retain every cycle; negative means earlier.

| Threshold | Minimum delta ps | Mean delta ps | Maximum delta ps |
|---|---:|---:|---:|
| CKB_rise50 | -1.443375112 | -1.436683211 | -1.409493002 |
| CKB_rise90 | -3.415724912 | -3.407083964 | -3.389557523 |
| RP_RN_fall30 | -2.404253388 | -2.383426039 | -2.375088598 |
| RP_RN_fall10 | -0.711664240 | -0.585286364 | -0.544849087 |
| BP_BN_rise50 | -2.376593695 | -2.349927001 | -2.342437691 |
| BP_BN_rise90 | -2.235266574 | -2.047339733 | -2.018593287 |
| OUT_reset10 | -2.363354926 | -2.189100201 | -2.143760784 |

These waveform timings establish the measured reset change without separating drive, capacitance and transient bias or inferring a channel-noise benefit.


## Matched short noise-phase diagnosis

Run `20261031-104845-miyahara-buffer-v20-noise-phase-diagnostic-screen` uses clean report source `3f355984d8d699235698aea12287085e1834d464` and matches B17's short testbench, +/-800 uV, 128 cycles per level, seed 1, 50 GHz and 0.5 ps/1e-6/1e-8 integration. All 256 samples at each corner are retained. TT has zero wrong polarities, and FS/low/125 has one at cycle 90, compared with B17's zero and four. The sources differ in three respects: P8 interstage drivers, 40-finger buffer capacitors and the P4 clock pull-up. The noise-phase comparison cannot isolate one change, and B19 has no noise run.

| Corner | B17 errors / 256 | B20 errors / 256 | B20 max reset ps | B20 full-trace stress max V |
|---|---:|---:|---:|---:|
| fs_low_125 | 4 | 1 | 26.727982072 | 0.81187 |
| tt_nom_27 | 0 | 0 | 24.509463400 | 0.90509 |

All 512 resets complete. Each corner has zero +80/+150 ps to final sign changes, late resets, physical output-validity violations or terminal stress violations. All 129 terminal pairs are retained per corner. Internal DP signs at +20/+30 ps remain correct in all cycles. In FS, RP at +40 ps already matches every final decision, including cycle 90. Internal phase signs are not completed output decisions.

| Corner | Phase | Quantity | B17 secant gain | B20 secant gain | B17 descriptive SNR | B20 descriptive SNR |
|---|---|---|---:|---:|---:|---:|
| fs_low_125 | +20 ps | DP_minus_DN | -2.956662453 | -2.914792306 | 3.195179258 | 3.304776722 |
| fs_low_125 | +30 ps | DP_minus_DN | -2.248841899 | -2.412605335 | 3.561315001 | 3.683677980 |
| fs_low_125 | +30 ps | RP_minus_RN | 1.451648488 | 2.102596898 | 1.243383953 | 1.599191355 |
| fs_low_125 | +40 ps | RP_minus_RN | 13.415481745 | 18.221802599 | 2.290627063 | 2.417807670 |
| fs_low_125 | +50 ps | RP_minus_RN | 63.782637276 | 97.895809119 | 2.232008419 | 2.381413779 |
| tt_nom_27 | +20 ps | DP_minus_DN | -3.506716777 | -3.448740607 | 4.015653799 | 4.109964216 |
| tt_nom_27 | +30 ps | DP_minus_DN | -4.547373865 | -4.437873426 | 4.944206576 | 4.997977473 |
| tt_nom_27 | +30 ps | RP_minus_RN | 2.013317210 | 2.725748598 | 1.992883387 | 2.358429583 |
| tt_nom_27 | +40 ps | RP_minus_RN | 40.558435837 | 49.480209871 | 4.395448234 | 4.292202927 |
| tt_nom_27 | +50 ps | RP_minus_RN | 326.456392859 | 434.019955908 | 4.690827751 | 4.927262694 |

At FS +40 ps the descriptive RP SNR rises from 2.290627 to 2.417808, about 5.6%; at +50 ps it rises from 2.232008 to 2.381414. TT +40 ps falls from 4.395448 to 4.292203. These two-level statistics include changing transfer and regeneration and are not formal input-referred noise. The single remaining hot-corner error and modest SNR change leave the 240 uV requirement unresolved. Shared seeds and finite counts do not establish noise equality, independence or a pass.

B20 has repaired the known deterministic stress and reset failures. The remaining five known risk corners and actual-worst tighter stress convergence will therefore be completed before deciding source-preserving canonical promotion. Only the unchanged original full tests can establish formal noise performance; B20 is currently unpromoted and no formal noise pass is claimed.

### Full-trace terminal pairs: fs_low_125

| Device | max abs(Vgs) V | max abs(Vgd) V | max abs(Vds) V |
|---|---:|---:|---:|
| MINP | 0.49224 | 0.49194 | 0.40557 |
| MINN | 0.49229 | 0.49196 | 0.40487 |
| MTAIL | 0.81000 | 0.80976 | 0.59121 |
| M14 | 0.81169 | 0.81127 | 0.77973 |
| M15 | 0.81157 | 0.81120 | 0.78004 |
| M12 | 0.80664 | 0.81127 | 0.81154 |
| M13 | 0.80596 | 0.81120 | 0.81159 |
| M10 | 0.79007 | 0.78413 | 0.80221 |
| M11 | 0.79009 | 0.78413 | 0.80225 |
| M6 | 0.80236 | 0.78413 | 0.80244 |
| M7 | 0.80244 | 0.78413 | 0.80236 |
| M8 | 0.80664 | 0.80286 | 0.80244 |
| M9 | 0.80596 | 0.80276 | 0.80236 |
| MCKN | 0.81000 | 0.80518 | 0.81187 |
| MCKP | 0.81000 | 0.80518 | 0.80132 |
| MRQP | 0.81187 | 0.80630 | 0.80244 |
| MRQN | 0.81187 | 0.80612 | 0.80236 |
| MAP | 0.81000 | 0.80986 | 0.81169 |
| MAN | 0.81000 | 0.80977 | 0.81157 |
| MBPP | 0.81085 | 0.81024 | 0.79926 |
| MBPN | 0.80244 | 0.81024 | 0.81143 |
| MOPP | 0.79926 | 0.80031 | 0.79981 |
| MOPN | 0.81143 | 0.80031 | 0.80298 |
| MBNP | 0.81078 | 0.81017 | 0.79930 |
| MBNN | 0.80236 | 0.81017 | 0.81148 |
| MONP | 0.79930 | 0.80022 | 0.79982 |
| MONN | 0.81148 | 0.80022 | 0.80303 |
| MDDP | 0.80664 | 0.00000 | 0.80664 |
| MDDN | 0.80596 | 0.00000 | 0.80596 |
| MUPRP1 | 0.81000 | 0.80244 | 0.81085 |
| MUPRN1 | 0.81000 | 0.80236 | 0.81078 |
| MUPBP1 | 0.81000 | 0.81143 | 0.79926 |
| MUPBN1 | 0.81000 | 0.81148 | 0.79930 |
| MUPOUTP1 | 0.81000 | 0.80298 | 0.79981 |
| MUPOUTN1 | 0.81000 | 0.80303 | 0.79982 |
| MDNOUTP1 | 0.80298 | 0.00000 | 0.80298 |
| MDNOUTP2 | 0.80298 | 0.00000 | 0.80298 |
| MDNOUTN1 | 0.80303 | 0.00000 | 0.80303 |
| MDNOUTN2 | 0.80303 | 0.00000 | 0.80303 |
| MCKUP | 0.81000 | 0.81187 | 0.80132 |
| MBLEED | 0.81000 | 0.80132 | 0.81187 |
| MUPXP | 0.81000 | 0.81154 | 0.77973 |
| MUPXN | 0.81000 | 0.81159 | 0.78004 |

### Full-trace terminal pairs: tt_nom_27

| Device | max abs(Vgs) V | max abs(Vgd) V | max abs(Vds) V |
|---|---:|---:|---:|
| MINP | 0.49294 | 0.49258 | 0.59614 |
| MINN | 0.49298 | 0.49257 | 0.59611 |
| MTAIL | 0.90000 | 0.90014 | 0.56819 |
| M14 | 0.90231 | 0.90229 | 0.85830 |
| M15 | 0.90220 | 0.90224 | 0.85867 |
| M12 | 0.89766 | 0.90229 | 0.90241 |
| M13 | 0.89703 | 0.90224 | 0.90245 |
| M10 | 0.87675 | 0.87661 | 0.89393 |
| M11 | 0.87680 | 0.87661 | 0.89395 |
| M6 | 0.90358 | 0.87661 | 0.90363 |
| M7 | 0.90363 | 0.87661 | 0.90358 |
| M8 | 0.89766 | 0.90185 | 0.90363 |
| M9 | 0.89703 | 0.90193 | 0.90358 |
| MCKN | 0.90000 | 0.89594 | 0.90503 |
| MCKP | 0.90000 | 0.89594 | 0.88624 |
| MRQP | 0.90503 | 0.89733 | 0.90363 |
| MRQN | 0.90503 | 0.89714 | 0.90358 |
| MAP | 0.90000 | 0.90026 | 0.90231 |
| MAN | 0.90000 | 0.90016 | 0.90220 |
| MBPP | 0.89821 | 0.89830 | 0.88579 |
| MBPN | 0.90363 | 0.89830 | 0.90509 |
| MOPP | 0.88579 | 0.88952 | 0.88754 |
| MOPN | 0.90509 | 0.88952 | 0.89874 |
| MBNP | 0.89815 | 0.89822 | 0.88586 |
| MBNN | 0.90358 | 0.89822 | 0.90498 |
| MONP | 0.88586 | 0.88943 | 0.88766 |
| MONN | 0.90498 | 0.88943 | 0.89877 |
| MDDP | 0.89766 | 0.00000 | 0.89766 |
| MDDN | 0.89703 | 0.00000 | 0.89703 |
| MUPRP1 | 0.90000 | 0.90363 | 0.89821 |
| MUPRN1 | 0.90000 | 0.90358 | 0.89815 |
| MUPBP1 | 0.90000 | 0.90509 | 0.88579 |
| MUPBN1 | 0.90000 | 0.90498 | 0.88586 |
| MUPOUTP1 | 0.90000 | 0.89874 | 0.88754 |
| MUPOUTN1 | 0.90000 | 0.89877 | 0.88766 |
| MDNOUTP1 | 0.89874 | 0.00000 | 0.89874 |
| MDNOUTP2 | 0.89874 | 0.00000 | 0.89874 |
| MDNOUTN1 | 0.89877 | 0.00000 | 0.89877 |
| MDNOUTN2 | 0.89877 | 0.00000 | 0.89877 |
| MCKUP | 0.90000 | 0.90503 | 0.88624 |
| MBLEED | 0.90000 | 0.88624 | 0.90503 |
| MUPXP | 0.90000 | 0.90241 | 0.85830 |
| MUPXN | 0.90000 | 0.90245 | 0.85867 |

Archive SHA-256 `c8a74ccede6235c327f18a07859b6212db81ef8ef240a8c695fe06fe96ccf653` retains both complete raws, phase distributions, saved drain-terminal currents, every error index and the matched B17 comparison. Every member was read back with CRC and SHA-256 verification; the owned remote run is absent. The 102.5 ns duration gives noisefmin 9.7561 MHz instead of the original 287.216 kHz. Terminal currents include dynamic displacement and do not isolate channel noise. Canonical B13 and every genuine original record remain unchanged.

## Completed screen 20261031-110714-miyahara-buffer-v20-screen

All 180 actual polarities including 10 uV and all 180 resets pass, together with timing, physical output validity and all 129 terminal pairs at each corner. These deterministic gates do not establish formal noise.

Actual clean source commit: `2ec8da8a83bf225c0456bf5261a44b0f37984b66`. Electrical SHA-256: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 47.819600 / 36.762230 | 19.404313 | 967.080370 | 36 / 36 | 0 | 0 | 0.99186 | 0 / 129 |
| ff_high_m40 | 42.532224 / 34.976358 | 18.148558 | 857.454823 | 36 / 36 | 0 | 0 | 0.99793 | 0 / 129 |
| sf_high_125 | 55.754687 / 44.873251 | 23.816062 | 869.004428 | 36 / 36 | 0 | 0 | 0.99485 | 0 / 129 |
| sf_high_27 | 54.562836 / 44.975383 | 23.078308 | 822.217758 | 36 / 36 | 0 | 0 | 0.99784 | 0 / 129 |
| sf_low_m40 | 73.406252 / 58.622438 | 28.332520 | 424.409353 | 36 / 36 | 0 | 0 | 0.82264 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | sf_high_125 | sf_high_27 | sf_low_m40 |
|---|---:|---:|---:|---:|---:|
| MINP | 0.57859 | 0.69755 | 0.65134 | 0.72083 | 0.60121 |
| MINN | 0.57864 | 0.69766 | 0.65139 | 0.72094 | 0.60133 |
| MTAIL | 0.99000 | 0.99000 | 0.99000 | 0.99000 | 0.81000 |
| M14 | 0.98719 | 0.99200 | 0.98707 | 0.99084 | 0.81179 |
| M15 | 0.98719 | 0.99200 | 0.98707 | 0.99084 | 0.81179 |
| M12 | 0.98938 | 0.99206 | 0.99077 | 0.99228 | 0.81331 |
| M13 | 0.98938 | 0.99206 | 0.99077 | 0.99228 | 0.81331 |
| M10 | 0.96085 | 0.98004 | 0.96378 | 0.97556 | 0.80876 |
| M11 | 0.96085 | 0.98004 | 0.96378 | 0.97556 | 0.80876 |
| M6 | 0.97734 | 0.99338 | 0.98872 | 0.99352 | 0.81576 |
| M7 | 0.97734 | 0.99338 | 0.98872 | 0.99352 | 0.81576 |
| M8 | 0.98702 | 0.99338 | 0.98872 | 0.99352 | 0.81576 |
| M9 | 0.98888 | 0.99338 | 0.98872 | 0.99352 | 0.81576 |
| MCKN | 0.99000 | 0.99269 | 0.99358 | 0.99446 | 0.81815 |
| MCKP | 0.99000 | 0.99000 | 0.99000 | 0.99000 | 0.81000 |
| MRQP | 0.98993 | 0.99338 | 0.99358 | 0.99446 | 0.81815 |
| MRQN | 0.98993 | 0.99338 | 0.99358 | 0.99446 | 0.81815 |
| MAP | 0.99000 | 0.99200 | 0.99000 | 0.99084 | 0.81179 |
| MAN | 0.99000 | 0.99200 | 0.99000 | 0.99084 | 0.81283 |
| MBPP | 0.98819 | 0.98784 | 0.98536 | 0.98513 | 0.80771 |
| MBPN | 0.99186 | 0.99793 | 0.99485 | 0.99784 | 0.82264 |
| MOPP | 0.97055 | 0.98113 | 0.97108 | 0.97623 | 0.80789 |
| MOPN | 0.99186 | 0.99793 | 0.99485 | 0.99784 | 0.82264 |
| MBNP | 0.98818 | 0.98781 | 0.98534 | 0.98511 | 0.80771 |
| MBNN | 0.99185 | 0.99792 | 0.99484 | 0.99783 | 0.82263 |
| MONP | 0.97055 | 0.98112 | 0.97108 | 0.97623 | 0.80788 |
| MONN | 0.99185 | 0.99792 | 0.99484 | 0.99783 | 0.82263 |
| MDDP | 0.98702 | 0.98535 | 0.98825 | 0.98736 | 0.81029 |
| MDDN | 0.98888 | 0.98793 | 0.98865 | 0.98840 | 0.81283 |
| MUPRP1 | 0.99000 | 0.99338 | 0.99000 | 0.99352 | 0.81576 |
| MUPRN1 | 0.99000 | 0.99338 | 0.99000 | 0.99352 | 0.81576 |
| MUPBP1 | 0.99186 | 0.99793 | 0.99485 | 0.99784 | 0.82264 |
| MUPBN1 | 0.99185 | 0.99792 | 0.99484 | 0.99783 | 0.82263 |
| MUPOUTP1 | 0.99000 | 0.99000 | 0.99000 | 0.99000 | 0.81542 |
| MUPOUTN1 | 0.99000 | 0.99000 | 0.99000 | 0.99000 | 0.81542 |
| MDNOUTP1 | 0.97749 | 0.98641 | 0.98376 | 0.98731 | 0.81542 |
| MDNOUTP2 | 0.97749 | 0.98641 | 0.98376 | 0.98731 | 0.81542 |
| MDNOUTN1 | 0.97749 | 0.98641 | 0.98376 | 0.98731 | 0.81542 |
| MDNOUTN2 | 0.97749 | 0.98641 | 0.98376 | 0.98731 | 0.81542 |
| MCKUP | 0.99000 | 0.99269 | 0.99358 | 0.99446 | 0.81815 |
| MBLEED | 0.99000 | 0.99269 | 0.99358 | 0.99446 | 0.81815 |
| MUPXP | 0.99000 | 0.99206 | 0.99077 | 0.99228 | 0.81331 |
| MUPXN | 0.99000 | 0.99206 | 0.99077 | 0.99228 | 0.81331 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-111631-miyahara-buffer-v20-screen

All 36 actual polarities including 10 uV and all 36 resets pass, together with timing, physical output validity and all 129 terminal pairs at each corner. These deterministic gates do not establish formal noise.

Actual clean source commit: `2ec8da8a83bf225c0456bf5261a44b0f37984b66`. Electrical SHA-256: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_m40 | 55.861230 / 46.287308 | 22.265960 | 822.628409 | 36 / 36 | 0 | 0 | 0.99975 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_m40 |
|---|---:|
| MINP | 0.76920 |
| MINN | 0.76938 |
| MTAIL | 0.99000 |
| M14 | 0.99188 |
| M15 | 0.99188 |
| M12 | 0.99296 |
| M13 | 0.99296 |
| M10 | 0.98227 |
| M11 | 0.98228 |
| M6 | 0.99516 |
| M7 | 0.99516 |
| M8 | 0.99516 |
| M9 | 0.99516 |
| MCKN | 0.99457 |
| MCKP | 0.99000 |
| MRQP | 0.99516 |
| MRQN | 0.99516 |
| MAP | 0.99188 |
| MAN | 0.99188 |
| MBPP | 0.98527 |
| MBPN | 0.99975 |
| MOPP | 0.97896 |
| MOPN | 0.99975 |
| MBNP | 0.98524 |
| MBNN | 0.99974 |
| MONP | 0.97896 |
| MONN | 0.99974 |
| MDDP | 0.98632 |
| MDDN | 0.98792 |
| MUPRP1 | 0.99516 |
| MUPRN1 | 0.99516 |
| MUPBP1 | 0.99975 |
| MUPBN1 | 0.99974 |
| MUPOUTP1 | 0.99000 |
| MUPOUTN1 | 0.99000 |
| MDNOUTP1 | 0.98945 |
| MDNOUTP2 | 0.98945 |
| MDNOUTN1 | 0.98945 |
| MDNOUTN2 | 0.98945 |
| MCKUP | 0.99457 |
| MBLEED | 0.99457 |
| MUPXP | 0.99296 |
| MUPXN | 0.99296 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


### Raw peak and complete-supply audits for the new gates

Run `20261031-110714-miyahara-buffer-v20-screen` has the following independently recomputed, unrounded full-trace maxima.

| Corner | Device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| ff_high_125 | MBPN ds | 0.991855736010 | 8144.263990151 | 16.551013372 | -183.448986628 |
| ff_high_m40 | MBPN ds | 0.997928250789 | 2071.749210570 | 18.706265160 | -181.293734840 |
| sf_high_125 | MBPN ds | 0.994852816115 | 5147.183884750 | 22.948994845 | -177.051005155 |
| sf_high_27 | MBPN ds | 0.997842065679 | 2157.934321459 | 24.618358968 | -175.381641032 |
| sf_low_m40 | MBPN ds | 0.822636486487 | 177363.513513286 | 33.437499588 | -166.562500412 |

All supply probes are present and KCL closes to numerical precision. The complete AVDD integrals cover all 36 mixed cycles from 100 ps to 14.5 ns, including reset and physical weak loads.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| ff_high_125 | 967.080724071 | 409.752303556 | 557.328420515 | 1660.928858352 |
| ff_high_m40 | 857.455137514 | 332.158132955 | 525.297004559 | 1727.909573834 |
| sf_high_125 | 869.004798916 | 345.764322996 | 523.240475921 | 1514.458054744 |
| sf_high_27 | 822.218126818 | 316.760649069 | 505.457477749 | 1557.159591169 |
| sf_low_m40 | 424.409534883 | 153.665167758 | 270.744367125 | 944.061512462 |

Raw/deck evidence and every audit are preserved under archive SHA-256 `f9927a23a9c6c577ce8cdc58423cd87a4f177ca3aed81b1842b6879f64f599b2`. Every entry was read back with CRC and SHA-256 verification before duplicate raw files were removed; the owned remote run is absent.

Run `20261031-111631-miyahara-buffer-v20-screen` has the following independently recomputed, unrounded full-trace maxima.

| Corner | Device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| sf_high_m40 | MBPN ds | 0.999746509088 | 253.490912065 | 25.827698663 | -174.172301337 |

All supply probes are present and KCL closes to numerical precision. The complete AVDD integrals cover all 36 mixed cycles from 100 ps to 14.5 ns, including reset and physical weak loads.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| sf_high_m40 | 822.628481193 | 314.737971757 | 507.890509436 | 1659.189744730 |

Raw/deck evidence and every audit are preserved under archive SHA-256 `cdbd356bc74cfeea22f91a99d490a2758acda20fd1f31eae0f5bc09ce0df6fa5`. Every entry was read back with CRC and SHA-256 verification before duplicate raw files were removed; the owned remote run is absent.

### Numerical convergence

The same electrical source is repeated with 0.125 ps, reltol 1e-7 and vabstol 1e-9. All actual polarities, resets, output validity, timing and terminal pairs still pass. Deltas below are tighter minus initial; all per-pair changes are retained in the archived comparison.

| Corner | 1 mV delay delta ps | 30 mV delay delta ps | Reset delta ps | Largest absolute pair-peak change V |
|---|---:|---:|---:|---:|
| sf_high_m40 | +0.000930803 | -0.000027855 | -0.005028260 | 0.00002 |

Together with the earlier five corners, B20 now passes all ten known risk corners, all 360 nominal-cycle polarities/resets and the 36-cycle tighter actual-worst stress repeat. Source-preserving canonical promotion and original TT capacitance/full-noise gates are next. B13 remains canonical until that explicit preservation and copy step. No B20 noise pass is inferred from these screens.
