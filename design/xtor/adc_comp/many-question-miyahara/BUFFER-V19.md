# BUFFER-V19: buffer-node capacitance repair with P8 interstage drive

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

B18 fails six terminal pairs at each of SF/high/-40 and FS/high/-40. The raw BN peaks are 1.000148479010 V and 1.000274971668 V, respectively, at about 26 ps and 24 ps after rising clock midpoints. All 72 actual decisions, resets and output-validity checks pass, but do not override the strict stress failure. [BUFFER-V18.md](BUFFER-V18.md) retains the failed source and complete waveform evidence; B18 stops before TT or noise.

This experiment changes only CBP/CBN from 20 to 40 fingers, nominally 5.66049 to 11.66040 fF, while retaining B18's P8 interstage drivers, N2 clock pull-down and N4 reset assists. All 43 MOS devices and the other seven MOMs remain electrically identical to B18. The zero-warning capacitor callback is `4bc15f8a37163feb5d1e8333ee1c148f7b5251d005c3a4cff620995266a433b7`; the finger length, width, spacing and metal range are unchanged.

The larger MOMs test more storage for the observed BP/BN edge excursion. The earlier 16-to-20-finger change on a different driver/clock source bought only about 100 uV of peak reduction, so its margin cannot be transferred here. Added buffer delay and reset charge must be measured. This change assumes no noise benefit; B17's clock-release improvement produced only about 1.09% higher FS RP signal-to-noise ratio at +40 ps in the matched short experiment.

Electrical SHA-256: `80b52d592af5f3f92260a40206a5aa08793031e29a1cdecf1f9f9cf508e9b710`. The [source](BUFFER-V19.txt) contains 43 MOS and 9 MOMs, with complete RNL checked on a byte-identical mirror. SF/FS high/-40 are checked first. On a pass, TT and FS/SS low/125 deterministic screens precede a matched short noise-phase diagnosis, to expose the reset-speed cost early. The remaining known corners, actual-worst convergence, source-preserving canonical promotion and genuine original formal tests remain open. Canonical B13 and all original failures remain unchanged.

![Physical comparator with larger buffer-node capacitors](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fc05ec9b504909d82e993df12fa475fd234cba5b/design/xtor/adc_comp/many-question-miyahara/buffer-v19.png)

## Completed screen 20261031-100609-miyahara-buffer-v19-screen

The two high-voltage cold corners pass all 72 actual polarities, completed resets, timing, physical output validity and all 129 terminal pairs.

Actual clean source commit: `1c82358bd327c795fc38a0b3ac1e63faf73429e5`. Electrical SHA-256: `80b52d592af5f3f92260a40206a5aa08793031e29a1cdecf1f9f9cf508e9b710`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 51.558010 / 43.016032 | 22.796391 | 759.809180 | 36 / 36 | 0 | 0 | 0.99962 | 0 / 129 |
| sf_high_m40 | 55.860271 / 46.287167 | 23.572638 | 817.322697 | 36 / 36 | 0 | 0 | 0.99974 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70397 | 0.76922 |
| MINN | 0.70408 | 0.76939 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99299 | 0.99187 |
| M15 | 0.99299 | 0.99187 |
| M12 | 0.99290 | 0.99330 |
| M13 | 0.99290 | 0.99330 |
| M10 | 0.98712 | 0.98220 |
| M11 | 0.98712 | 0.98220 |
| M6 | 0.99375 | 0.99495 |
| M7 | 0.99375 | 0.99495 |
| M8 | 0.99375 | 0.99495 |
| M9 | 0.99375 | 0.99495 |
| MCKN | 0.99000 | 0.99202 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99375 | 0.99495 |
| MRQN | 0.99375 | 0.99495 |
| MAP | 0.99299 | 0.99187 |
| MAN | 0.99299 | 0.99187 |
| MBPP | 0.98878 | 0.98528 |
| MBPN | 0.99962 | 0.99974 |
| MOPP | 0.98520 | 0.97895 |
| MOPN | 0.99962 | 0.99974 |
| MBNP | 0.98876 | 0.98524 |
| MBNN | 0.99962 | 0.99974 |
| MONP | 0.98520 | 0.97895 |
| MONN | 0.99962 | 0.99974 |
| MDDP | 0.98421 | 0.98632 |
| MDDN | 0.98697 | 0.98792 |
| MUPRP1 | 0.99375 | 0.99495 |
| MUPRN1 | 0.99375 | 0.99495 |
| MUPBP1 | 0.99962 | 0.99974 |
| MUPBN1 | 0.99962 | 0.99974 |
| MUPOUTP1 | 0.99000 | 0.99000 |
| MUPOUTN1 | 0.99000 | 0.99000 |
| MDNOUTP1 | 0.98559 | 0.98980 |
| MDNOUTP2 | 0.98559 | 0.98980 |
| MDNOUTN1 | 0.98559 | 0.98980 |
| MDNOUTN2 | 0.98559 | 0.98980 |
| MCKUP | 0.99000 | 0.99202 |
| MBLEED | 0.99000 | 0.99202 |
| MUPXP | 0.99247 | 0.99330 |
| MUPXN | 0.99247 | 0.99330 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-101315-miyahara-buffer-v19-screen

SS/low/125 fails the 35 ps reset-time limit at 36.016839 ps. TT and FS/low/125 pass. All 108 actual polarities and completed resets, output validity and terminal stress pass, but do not override the SS timing failure. B19 stops before noise and broader expansion.

Actual clean source commit: `1c82358bd327c795fc38a0b3ac1e63faf73429e5`. Electrical SHA-256: `80b52d592af5f3f92260a40206a5aa08793031e29a1cdecf1f9f9cf508e9b710`. The canonical netlist and 282 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_low_125 | 67.977193 / 53.557504 | 28.453455 | 460.735986 | 36 / 36 | 0 | 0 | 0.81244 | 0 / 129 |
| ss_low_125 | 81.505955 / 65.855276 | 36.016839 | 419.482811 | 36 / 36 | 0 | 0 | 0.81639 | 0 / 129 |
| tt_nom_27 | 58.345485 / 47.855464 | 26.050019 | 586.627371 | 36 / 36 | 0 | 0 | 0.90848 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 2 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_low_125 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|
| MINP | 0.54148 | 0.53997 | 0.60605 |
| MINN | 0.54148 | 0.53996 | 0.60613 |
| MTAIL | 0.81000 | 0.81000 | 0.90000 |
| M14 | 0.81114 | 0.80955 | 0.90184 |
| M15 | 0.81114 | 0.80955 | 0.90184 |
| M12 | 0.81120 | 0.81206 | 0.90233 |
| M13 | 0.81120 | 0.81206 | 0.90233 |
| M10 | 0.80113 | 0.80228 | 0.89336 |
| M11 | 0.80113 | 0.80228 | 0.89336 |
| M6 | 0.80153 | 0.81021 | 0.90282 |
| M7 | 0.80153 | 0.81021 | 0.90282 |
| M8 | 0.80776 | 0.81021 | 0.90282 |
| M9 | 0.81109 | 0.81021 | 0.90282 |
| MCKN | 0.81000 | 0.81186 | 0.90167 |
| MCKP | 0.81000 | 0.81000 | 0.90000 |
| MRQP | 0.80788 | 0.81186 | 0.90282 |
| MRQN | 0.80788 | 0.81186 | 0.90282 |
| MAP | 0.81114 | 0.81000 | 0.90184 |
| MAN | 0.81114 | 0.81005 | 0.90184 |
| MBPP | 0.81042 | 0.80798 | 0.89783 |
| MBPN | 0.81244 | 0.81639 | 0.90848 |
| MOPP | 0.80299 | 0.80274 | 0.89254 |
| MOPN | 0.81244 | 0.81639 | 0.90848 |
| MBNP | 0.81041 | 0.80796 | 0.89780 |
| MBNN | 0.81244 | 0.81639 | 0.90848 |
| MONP | 0.80299 | 0.80274 | 0.89254 |
| MONN | 0.81244 | 0.81639 | 0.90848 |
| MDDP | 0.80776 | 0.80829 | 0.89759 |
| MDDN | 0.81109 | 0.81005 | 0.90037 |
| MUPRP1 | 0.81042 | 0.81021 | 0.90282 |
| MUPRN1 | 0.81041 | 0.81021 | 0.90282 |
| MUPBP1 | 0.81244 | 0.81639 | 0.90848 |
| MUPBN1 | 0.81244 | 0.81639 | 0.90848 |
| MUPOUTP1 | 0.81000 | 0.81000 | 0.90000 |
| MUPOUTN1 | 0.81000 | 0.81000 | 0.90000 |
| MDNOUTP1 | 0.80160 | 0.80692 | 0.89793 |
| MDNOUTP2 | 0.80160 | 0.80692 | 0.89793 |
| MDNOUTN1 | 0.80160 | 0.80692 | 0.89793 |
| MDNOUTN2 | 0.80160 | 0.80692 | 0.89793 |
| MCKUP | 0.81000 | 0.81186 | 0.90167 |
| MBLEED | 0.81000 | 0.81186 | 0.90167 |
| MUPXP | 0.81120 | 0.81206 | 0.90233 |
| MUPXN | 0.81120 | 0.81206 | 0.90233 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


All 180 actual decisions and completed resets are retained across five corners. The SS/low/125 reset time of 36.016838870 ps still fails the 35 ps gate. TT 1/30 mV delay is 58.345484607/47.855463559 ps, reset 26.050018811 ps, and diagnostic mixed clock capacitance 10.437109095 fF. There is no B19 noise result or canonical promotion.

The unrounded high-voltage cold maxima are:

| Corner | Device pair | Peak V | Margin uV |
|---|---|---:|---:|
| fs_high_m40 | MBNN ds | 0.999621468294 | 378.531706211 |
| sf_high_m40 | MBNN ds | 0.999738339831 | 261.660169182 |

A read-only decomposition of each worst reset cycle, with times measured after the falling 50% clock crossing, gives:

| Corner | CKB 50% ps | CKB 90% ps | both RP/RN below 30% ps | both BP/BN above 90% ps | both OUT below 10% ps |
|---|---:|---:|---:|---:|---:|
| fs_low_125 | 7.752943009 | 15.233390808 | 17.157658848 | 24.205183583 | 28.453454786 |
| ss_low_125 | 8.523813508 | 17.044882373 | 22.157435895 | 30.059430359 | 36.016838870 |
| tt_nom_27 | 6.049960045 | 11.633365187 | 16.883596786 | 21.238035182 | 26.050018811 |

This path motivates testing stronger CKB pull-up with all reset-assist and buffer capacitances retained. B20 changes only MCKP P3/nf3 to P4/nf4 at fixed 30 nm and 1 um finger width; no timing benefit is inherited. Stress, release, clock input charge and noise must be measured again.

Full AVDD waveform integrals include reset and weak loads over 36 cycles and 100 ps–14.5 ns. Every supply-terminal probe is present and KCL closes.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 759.809545625 | 281.395217664 | 478.414327961 | 1491.776783064 |
| sf_high_m40 | 817.323055602 | 314.359845006 | 502.963210596 | 1659.186143996 |
| fs_low_125 | 460.736410858 | 173.681975689 | 287.054435169 | 819.439168711 |
| ss_low_125 | 419.483174826 | 147.691359992 | 271.791814834 | 741.659720814 |
| tt_nom_27 | 586.627714584 | 216.843607244 | 369.784107340 | 1155.447210661 |

Every raw archive member was read back with CRC and SHA-256 verification before duplicate local raw files were removed; owned remote runs are absent.

- `20261031-100609-miyahara-buffer-v19-screen`: `ec2de334d8c6f7f77aaf97c40459d0082e5c7bae9f13cac9629d44bdbb394df0`.
- `20261031-101315-miyahara-buffer-v19-screen`: `1fde6fa2607fb2bd68d289c464fe75bcd37d499c1eb87767df12f4173cca39aa`.
