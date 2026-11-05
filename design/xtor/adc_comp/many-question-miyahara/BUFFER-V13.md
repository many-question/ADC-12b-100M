# BUFFER-V13: increase input-drain integration capacitance

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

B12 fails the genuine official TT noise gate at 201.879919 uV rms against 200 uV. The 95% interval crosses the limit, but the prescribed point estimate is a failure. Its S-curve and complete samples show no gross anomaly; the old baseline interval overlaps, so no precise noise penalty is assigned to a particular repair.

This source changes only the physical CDP/CDN MOMs from 48 to 56 fingers, nominally 14.06 to 16.4603 fF. Longer front-end integration is intended to improve differential signal development before the later stage decides, and to increase noise margin without widening the input transistors whose official input capacitance is already 19.328731 fF. This is a hypothesis requiring measurement. Extra capacitance costs delay and reset charge; the TT 30 mV delay limit remains 50 ps and all stress/reset gates still apply. No measured noise improvement is claimed at source freeze.

The new capacitor callback succeeds without warnings, with result SHA-256 `f553a09aa0a859e87a377f0522eb6653774ef645a8e8fd75d37e131fce9a7560`. All other capacitor dimensions and all 43 MOS instances are unchanged. Electrical SHA-256: `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`. The [source](BUFFER-V13.txt) has 43 MOS and 9 MOM devices and complete RNL; its byte-identical validation mirror passes with zero errors, warnings and hints. Canonical B12 and its formal failure remain preserved.

First screen SF/high/-40 and FS/high/-40, then TT speed/validity and the remaining key corners if those pass. Formal noise must establish useful margin on a frozen new source before expensive qualification expansion. The old noise result and successful private deterministic screens are not adopted as new formal measurements.

![Physical comparator with larger input-drain capacitors](https://raw.githubusercontent.com/many-question/ADC-12b-100M/a7ade027755ab3be3793b3da4c6d6a38388d15e0/design/xtor/adc_comp/many-question-miyahara/buffer-v13.png)

## Completed screen 20261031-062838-miyahara-buffer-v13-screen

Every measured corner passes timing, reset, physical output validity and all 129 MOS terminal-pair stress checks. The independent all-cycle audit confirms every one of the 36 polarities, including 10 uV, and all 36 resets.

Actual clean source commit: `8895876ee62ed8145982ba5d8e800488da1178b0`. Electrical SHA-256: `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 52.001966 / 42.701764 | 20.139151 | 732.218056 | 36 / 36 | 0 | 0 | 0.99901 | 0 / 129 |
| sf_high_m40 | 56.197458 / 46.106888 | 20.635049 | 788.509774 | 36 / 36 | 0 | 0 | 0.99904 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70358 | 0.76876 |
| MINN | 0.70370 | 0.76894 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99309 | 0.99200 |
| M15 | 0.99309 | 0.99200 |
| M12 | 0.99298 | 0.99331 |
| M13 | 0.99298 | 0.99331 |
| M10 | 0.98612 | 0.98100 |
| M11 | 0.98612 | 0.98100 |
| M6 | 0.99315 | 0.99588 |
| M7 | 0.99315 | 0.99588 |
| M8 | 0.99315 | 0.99588 |
| M9 | 0.99315 | 0.99588 |
| MCKN | 0.99000 | 0.99151 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99315 | 0.99588 |
| MRQN | 0.99315 | 0.99588 |
| MAP | 0.99309 | 0.99200 |
| MAN | 0.99309 | 0.99200 |
| MBPP | 0.98934 | 0.98325 |
| MBPN | 0.99901 | 0.99904 |
| MOPP | 0.98718 | 0.97871 |
| MOPN | 0.99901 | 0.99904 |
| MBNP | 0.98934 | 0.98325 |
| MBNN | 0.99900 | 0.99904 |
| MONP | 0.98718 | 0.97870 |
| MONN | 0.99900 | 0.99904 |
| MDDP | 0.98429 | 0.98646 |
| MDDN | 0.98710 | 0.98801 |
| MUPRP1 | 0.99315 | 0.99588 |
| MUPRN1 | 0.99315 | 0.99588 |
| MUPBP1 | 0.99901 | 0.99904 |
| MUPBN1 | 0.99900 | 0.99904 |
| MUPOUTP1 | 0.99000 | 0.99369 |
| MUPOUTN1 | 0.99000 | 0.99369 |
| MDNOUTP1 | 0.98903 | 0.99369 |
| MDNOUTP2 | 0.98903 | 0.99369 |
| MDNOUTN1 | 0.98903 | 0.99369 |
| MDNOUTN2 | 0.98903 | 0.99369 |
| MCKUP | 0.99000 | 0.99151 |
| MBLEED | 0.99000 | 0.99151 |
| MUPXP | 0.99240 | 0.99331 |
| MUPXN | 0.99240 | 0.99331 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-063446-miyahara-buffer-v13-screen

Every measured corner passes timing, reset, physical output validity and all 129 MOS terminal-pair stress checks. The independent all-cycle audit confirms every one of the 36 polarities, including 10 uV, and all 36 resets.

Actual clean source commit: `8895876ee62ed8145982ba5d8e800488da1178b0`. Electrical SHA-256: `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 59.412537 / 47.831273 | 22.960213 | 562.264008 | 36 / 36 | 0 | 0 | 0.90786 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.60562 |
| MINN | 0.60572 |
| MTAIL | 0.90000 |
| M14 | 0.90196 |
| M15 | 0.90196 |
| M12 | 0.90181 |
| M13 | 0.90181 |
| M10 | 0.89182 |
| M11 | 0.89182 |
| M6 | 0.90193 |
| M7 | 0.90193 |
| M8 | 0.90193 |
| M9 | 0.90193 |
| MCKN | 0.90169 |
| MCKP | 0.90000 |
| MRQP | 0.90193 |
| MRQN | 0.90193 |
| MAP | 0.90196 |
| MAN | 0.90196 |
| MBPP | 0.89630 |
| MBPN | 0.90786 |
| MOPP | 0.89299 |
| MOPN | 0.90786 |
| MBNP | 0.89630 |
| MBNN | 0.90786 |
| MONP | 0.89299 |
| MONN | 0.90786 |
| MDDP | 0.89770 |
| MDDN | 0.90052 |
| MUPRP1 | 0.90193 |
| MUPRN1 | 0.90193 |
| MUPBP1 | 0.90786 |
| MUPBN1 | 0.90786 |
| MUPOUTP1 | 0.90112 |
| MUPOUTN1 | 0.90112 |
| MDNOUTP1 | 0.90112 |
| MDNOUTP2 | 0.90112 |
| MDNOUTN1 | 0.90112 |
| MDNOUTN2 | 0.90112 |
| MCKUP | 0.90169 |
| MBLEED | 0.90169 |
| MUPXP | 0.90181 |
| MUPXN | 0.90181 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-064247-miyahara-buffer-v13-screen

Every measured corner passes timing, reset, physical output validity and all 129 MOS terminal-pair stress checks. The independent all-cycle audit confirms every one of the 36 polarities, including 10 uV, and all 36 resets.

Actual clean source commit: `8895876ee62ed8145982ba5d8e800488da1178b0`. Electrical SHA-256: `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 52.075747 / 39.213480 | 18.130102 | 913.968993 | 36 / 36 | 0 | 0 | 0.99154 | 0 / 129 |
| ff_high_m40 | 43.385510 / 35.150028 | 17.025482 | 821.949895 | 36 / 36 | 0 | 0 | 0.99756 | 0 / 129 |
| fs_low_125 | 73.825437 / 56.567865 | 25.134774 | 437.974655 | 36 / 36 | 0 | 0 | 0.81178 | 0 / 129 |
| sf_high_125 | 58.409903 / 46.241595 | 22.049305 | 816.778921 | 36 / 36 | 0 | 0 | 0.99474 | 0 / 129 |
| sf_high_27 | 55.620284 / 45.243614 | 21.350962 | 782.899650 | 36 / 36 | 0 | 0 | 0.99749 | 0 / 129 |
| sf_low_m40 | 73.691767 / 57.871706 | 26.040687 | 405.985021 | 36 / 36 | 0 | 0 | 0.82186 | 0 / 129 |
| ss_low_125 | 84.668818 / 66.825812 | 31.426516 | 397.736855 | 36 / 36 | 0 | 0 | 0.81549 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 4 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | fs_low_125 | sf_high_125 | sf_high_27 | sf_low_m40 | ss_low_125 |
|---|---:|---:|---:|---:|---:|---:|---:|
| MINP | 0.57788 | 0.69709 | 0.54161 | 0.65069 | 0.72032 | 0.60092 | 0.54043 |
| MINN | 0.57794 | 0.69720 | 0.54161 | 0.65075 | 0.72043 | 0.60106 | 0.54043 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 |
| M14 | 0.98724 | 0.99207 | 0.81128 | 0.98724 | 0.99097 | 0.81200 | 0.81000 |
| M15 | 0.98724 | 0.99207 | 0.81127 | 0.98724 | 0.99097 | 0.81201 | 0.81000 |
| M12 | 0.98733 | 0.99197 | 0.81016 | 0.98963 | 0.99212 | 0.81392 | 0.81159 |
| M13 | 0.98907 | 0.99197 | 0.81156 | 0.98963 | 0.99212 | 0.81392 | 0.81159 |
| M10 | 0.95619 | 0.97894 | 0.79822 | 0.96030 | 0.97380 | 0.80757 | 0.80036 |
| M11 | 0.95619 | 0.97894 | 0.79822 | 0.96030 | 0.97380 | 0.80757 | 0.80036 |
| M6 | 0.96879 | 0.99254 | 0.79651 | 0.98584 | 0.99257 | 0.81554 | 0.80848 |
| M7 | 0.96879 | 0.99254 | 0.79651 | 0.98584 | 0.99257 | 0.81554 | 0.80848 |
| M8 | 0.98726 | 0.99254 | 0.80814 | 0.98849 | 0.99257 | 0.81554 | 0.80848 |
| M9 | 0.98907 | 0.99254 | 0.81156 | 0.98886 | 0.99257 | 0.81554 | 0.81064 |
| MCKN | 0.99000 | 0.99000 | 0.81000 | 0.99123 | 0.99167 | 0.81529 | 0.81247 |
| MCKP | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 |
| MRQP | 0.98836 | 0.99254 | 0.80950 | 0.99123 | 0.99257 | 0.81554 | 0.81247 |
| MRQN | 0.98836 | 0.99254 | 0.80950 | 0.99123 | 0.99257 | 0.81554 | 0.81247 |
| MAP | 0.99000 | 0.99207 | 0.81128 | 0.99000 | 0.99097 | 0.81200 | 0.81000 |
| MAN | 0.99000 | 0.99207 | 0.81156 | 0.99000 | 0.99097 | 0.81296 | 0.81064 |
| MBPP | 0.98517 | 0.98519 | 0.80788 | 0.98269 | 0.98261 | 0.80966 | 0.80614 |
| MBPN | 0.99154 | 0.99756 | 0.81178 | 0.99474 | 0.99749 | 0.82186 | 0.81549 |
| MOPP | 0.96989 | 0.98223 | 0.80276 | 0.97098 | 0.97591 | 0.80718 | 0.80188 |
| MOPN | 0.99154 | 0.99756 | 0.81178 | 0.99474 | 0.99749 | 0.82186 | 0.81549 |
| MBNP | 0.98516 | 0.98517 | 0.80788 | 0.98267 | 0.98259 | 0.80966 | 0.80614 |
| MBNN | 0.99153 | 0.99756 | 0.81178 | 0.99474 | 0.99749 | 0.82186 | 0.81548 |
| MONP | 0.96988 | 0.98222 | 0.80277 | 0.97097 | 0.97590 | 0.80718 | 0.80188 |
| MONN | 0.99153 | 0.99756 | 0.81178 | 0.99474 | 0.99749 | 0.82186 | 0.81548 |
| MDDP | 0.98726 | 0.98541 | 0.80814 | 0.98849 | 0.98754 | 0.81037 | 0.80847 |
| MDDN | 0.98907 | 0.98803 | 0.81156 | 0.98886 | 0.98852 | 0.81296 | 0.81064 |
| MUPRP1 | 0.99000 | 0.99254 | 0.81000 | 0.99000 | 0.99257 | 0.81554 | 0.81000 |
| MUPRN1 | 0.99000 | 0.99254 | 0.81000 | 0.99000 | 0.99257 | 0.81554 | 0.81000 |
| MUPBP1 | 0.99154 | 0.99756 | 0.81178 | 0.99474 | 0.99749 | 0.82186 | 0.81549 |
| MUPBN1 | 0.99153 | 0.99756 | 0.81178 | 0.99474 | 0.99749 | 0.82186 | 0.81548 |
| MUPOUTP1 | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99024 | 0.82056 | 0.81000 |
| MUPOUTN1 | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99024 | 0.82056 | 0.81000 |
| MDNOUTP1 | 0.97753 | 0.98863 | 0.80320 | 0.98503 | 0.99024 | 0.82056 | 0.80974 |
| MDNOUTP2 | 0.97753 | 0.98863 | 0.80320 | 0.98503 | 0.99024 | 0.82056 | 0.80974 |
| MDNOUTN1 | 0.97753 | 0.98863 | 0.80320 | 0.98503 | 0.99024 | 0.82056 | 0.80974 |
| MDNOUTN2 | 0.97753 | 0.98863 | 0.80320 | 0.98503 | 0.99024 | 0.82056 | 0.80974 |
| MCKUP | 0.99000 | 0.99000 | 0.81000 | 0.99123 | 0.99167 | 0.81529 | 0.81247 |
| MBLEED | 0.99000 | 0.99000 | 0.81000 | 0.99123 | 0.99167 | 0.81529 | 0.81247 |
| MUPXP | 0.99000 | 0.99197 | 0.81006 | 0.99000 | 0.99212 | 0.81392 | 0.81159 |
| MUPXN | 0.99000 | 0.99197 | 0.81006 | 0.99000 | 0.99212 | 0.81392 | 0.81159 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

Across these ten distinct key corners, all 360 decisions (including 10 uV) and 360 resets pass. The actual highest stress is 0.99904 V at sf_high_m40; a targeted 0.125 ps / 1e-7 / 1e-9 convergence run at that corner is the next gate. No new-source formal cap or noise result is available yet.

## Completed screen 20261031-065521-miyahara-buffer-v13-screen

The actual worst stress corner passes the tighter numerical repeat. All 36 polarities including 10 uV and all 36 resets pass independently; no output-validity or MOS stress failure appears.

Actual clean source commit: `d490e9f66a59e0b147a72f3f9175d2305f487bf1`. Electrical SHA-256: `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_m40 | 56.198939 / 46.106945 | 20.630348 | 788.513102 | 36 / 36 | 0 | 0 | 0.99904 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_m40 |
|---|---:|
| MINP | 0.76875 |
| MINN | 0.76894 |
| MTAIL | 0.99000 |
| M14 | 0.99201 |
| M15 | 0.99201 |
| M12 | 0.99332 |
| M13 | 0.99332 |
| M10 | 0.98100 |
| M11 | 0.98100 |
| M6 | 0.99588 |
| M7 | 0.99588 |
| M8 | 0.99588 |
| M9 | 0.99588 |
| MCKN | 0.99151 |
| MCKP | 0.99000 |
| MRQP | 0.99588 |
| MRQN | 0.99588 |
| MAP | 0.99201 |
| MAN | 0.99201 |
| MBPP | 0.98325 |
| MBPN | 0.99904 |
| MOPP | 0.97871 |
| MOPN | 0.99904 |
| MBNP | 0.98325 |
| MBNN | 0.99904 |
| MONP | 0.97871 |
| MONN | 0.99904 |
| MDDP | 0.98646 |
| MDDN | 0.98801 |
| MUPRP1 | 0.99588 |
| MUPRN1 | 0.99588 |
| MUPBP1 | 0.99904 |
| MUPBN1 | 0.99904 |
| MUPOUTP1 | 0.99371 |
| MUPOUTN1 | 0.99371 |
| MDNOUTP1 | 0.99371 |
| MDNOUTP2 | 0.99371 |
| MDNOUTN1 | 0.99371 |
| MDNOUTN2 | 0.99371 |
| MCKUP | 0.99151 |
| MBLEED | 0.99151 |
| MUPXP | 0.99332 |
| MUPXN | 0.99332 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

The maximum absolute change in any of the 129 tabulated terminal-pair peaks is 20.000 uV, at the 10 uV table precision. Global maximum stress stays 0.99904 V. Tight-minus-reference changes are 1 mV delay +0.001481261 ps, 30 mV delay +0.000056892 ps, reset -0.004701680 ps and AVDD energy +0.003328380 fJ/cycle. The source is electrically identical. This supports targeted numerical convergence at the screened worst corner, not all-corner qualification. Normal canonical promotion may now preserve the prior source and all mixed-source records, followed by genuine new-source official TT capacitance/kickback and noise.
