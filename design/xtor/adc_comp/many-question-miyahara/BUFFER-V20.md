# BUFFER-V20: stronger CKB rise for hot slow reset

B19 repairs the buffer-node high-voltage cold stress but fails SS/low/125 reset at 36.016839 ps against 35 ps. All 180 actual polarities and completed resets, output validity and terminal stress pass across its five initial corners; the reset-time failure still stops noise and broader expansion. At its worst SS cycle, CKB reaches 50%/90% after 8.523814/17.044882 ps, both RP/RN fall below 30% after 22.157436 ps, both BP/BN exceed 90% after 30.059430 ps, and the external outputs reset after 36.016839 ps. [BUFFER-V19.md](BUFFER-V19.md) preserves the source, failure and measured path.

This source retains all B19 P8 interstage drivers, N2 clock pull-down, N4 regeneration reset assists and 40-finger buffer capacitors. Only the CKB inverter PMOS MCKP changes from 3 um/nf3 to 4 um/nf4, with 30 nm length and 1 um finger width fixed. All other 42 MOS devices and all nine MOMs are electrically identical to B19.

The stronger pull-up tests earlier CKB assertion and reset-assist conduction while retaining the repaired BP/BN capacitance. Its added loading and changed drive also affect input clock charge, release, stress and noise, so the reset benefit is not assumed. This does not establish a P8 interstage noise benefit.

The successful zero-warning callback supplies the full geometry and parasitics, SHA-256 `8d2096c6b74343943491aeda9c02802217e12d4ab27360776cf0eeff75c274cd`. Electrical SHA-256: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. The [source](BUFFER-V20.txt) contains 43 MOS and 9 MOMs with complete RNL checked on a byte-identical mirror.

The first batch covers the failing SS/low/125 corner and both SF/FS high/-40 stress corners. TT and FS/low/125 follow only if that batch passes, before a matched short noise-phase diagnosis. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and original formal tests remain open. The canonical source and every genuine original record remain unchanged.

![Physical comparator experiment](buffer-v20.png)

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
