# BUFFER-V12: suppress input-stage negative feedthrough

B11 removes the clock-rail stress failure but retains the two M14/M15 Vds failures already present in B10. At FS/high/-40, XP reaches -10.919713 mV at 11.480779 ps after the rising clock 50% crossing, producing 1.00092 V maximum stress. CKB is now bounded between 0.037750 and 0.988618 V. Both targeted corners otherwise pass timing, reset, regeneration and physical output validity, with all 36 correct decisions and resets.

This experiment adds one P0.5um/100nm weak pull-up to each XP/XN node. Its complete geometry and terminal parasitics are identical to the existing callback-validated MUPRP1 device. All earlier electrical statements remain unchanged. Each of the resulting 43 MOS and 9 MOM capacitors is represented physically; the new devices' persistent current and AVDD energy are included.

The [independent source](BUFFER-V12.txt) has electrical SHA-256 `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the rendered schematic was inspected.

![XP and XN physical weak pull-ups](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0c799462e700c1f74a9448031e14abdd56ec18e7/design/xtor/adc_comp/many-question-miyahara/buffer-v12.png)

Screen SF/high/-40 and FS/high/-40 first. Passing these permits the remaining eight known key corners, followed by motivated numerical convergence and new-source qualification. All-terminal trace checks, all 36 polarities and resets, output validity, delay and energy remain mandatory. The entire session stays within six simultaneous simulation jobs. No prior capacitance, noise or mismatch result is inherited. Canonical promotion uses the existing official runner and preserves the older records honestly.

## Completed screen 20261031-052208-miyahara-buffer-v12-screen

Both previously failing cold high-voltage target corners now pass full-trace stress, delay, reset, regeneration and physical output validity. SF/high/-40 maximum stress is 0.99933 V and FS/high/-40 is 0.99928 V across all 129 terminal pairs. Each has 36 correct polarities including 10 uV and 36 completed resets. These passes permit the remaining eight known key corners, not noise/MC or canonical qualification. Actual AVDD energy includes the added persistent loads: SF/high/-40 is 781.830407 fJ/cycle and FS/high/-40 is 726.099595 fJ/cycle.

Actual clean source commit: `a45447f150df87c462ae3446c25a2dc9e5bb009c`. Electrical SHA-256: `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 50.831852 / 41.643234 | 20.144064 | 726.099595 | 36 / 36 | 0 | 0 | 0.99928 | 0 / 129 |
| sf_high_m40 | 54.807656 / 44.913904 | 20.655792 | 781.830407 | 36 / 36 | 0 | 0 | 0.99933 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70289 | 0.76807 |
| MINN | 0.70301 | 0.76827 |
| MTAIL | 0.99000 | 0.99000 |
| M14 | 0.99317 | 0.99208 |
| M15 | 0.99317 | 0.99208 |
| M12 | 0.99305 | 0.99337 |
| M13 | 0.99305 | 0.99337 |
| M10 | 0.98622 | 0.98119 |
| M11 | 0.98622 | 0.98119 |
| M6 | 0.99317 | 0.99598 |
| M7 | 0.99317 | 0.99598 |
| M8 | 0.99317 | 0.99598 |
| M9 | 0.99317 | 0.99598 |
| MCKN | 0.99000 | 0.99151 |
| MCKP | 0.99000 | 0.99000 |
| MRQP | 0.99317 | 0.99598 |
| MRQN | 0.99317 | 0.99598 |
| MAP | 0.99317 | 0.99208 |
| MAN | 0.99317 | 0.99208 |
| MBPP | 0.98937 | 0.98327 |
| MBPN | 0.99928 | 0.99933 |
| MOPP | 0.98726 | 0.97883 |
| MOPN | 0.99928 | 0.99933 |
| MBNP | 0.98938 | 0.98327 |
| MBNN | 0.99928 | 0.99933 |
| MONP | 0.98726 | 0.97883 |
| MONN | 0.99928 | 0.99933 |
| MDDP | 0.98439 | 0.98665 |
| MDDN | 0.98724 | 0.98811 |
| MUPRP1 | 0.99317 | 0.99598 |
| MUPRN1 | 0.99317 | 0.99598 |
| MUPBP1 | 0.99928 | 0.99933 |
| MUPBN1 | 0.99928 | 0.99933 |
| MUPOUTP1 | 0.99000 | 0.99390 |
| MUPOUTN1 | 0.99000 | 0.99390 |
| MDNOUTP1 | 0.98912 | 0.99390 |
| MDNOUTP2 | 0.98912 | 0.99390 |
| MDNOUTN1 | 0.98912 | 0.99390 |
| MDNOUTN2 | 0.98912 | 0.99390 |
| MCKUP | 0.99000 | 0.99151 |
| MBLEED | 0.99000 | 0.99151 |
| MUPXP | 0.99244 | 0.99337 |
| MUPXN | 0.99244 | 0.99337 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-052907-miyahara-buffer-v12-screen

All eight remaining key corners pass timing, reset, regeneration, output validity and full-trace stress, completing ten passing known key corners. Each of all ten corners has 36 correct polarities including 10 uV and 36 completed resets. Actual worst stress is SF/high/-40 at 0.99933 V from the first batch. TT 1/30 mV delays are 58.218513/46.737852 ps; the worst measured reset is SS/low/125 at 31.410030 ps. TT AVDD energy is 557.022328 fJ/cycle. A targeted 0.125 ps/reltol 1e-7/vabstol 1e-9 run at SF/high/-40 precedes any canonical promotion. No prior capacitance/noise/MC qualification is inherited.

Actual clean source commit: `a45447f150df87c462ae3446c25a2dc9e5bb009c`. Electrical SHA-256: `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 51.457846 / 38.595592 | 18.098160 | 908.427336 | 36 / 36 | 0 | 0 | 0.99164 | 0 / 129 |
| ff_high_m40 | 42.599174 / 34.447499 | 17.073465 | 816.748318 | 36 / 36 | 0 | 0 | 0.99779 | 0 / 129 |
| fs_low_125 | 72.857807 / 55.592791 | 25.087641 | 433.846325 | 36 / 36 | 0 | 0 | 0.81201 | 0 / 129 |
| sf_high_125 | 57.331922 / 45.230312 | 22.002503 | 809.462063 | 36 / 36 | 0 | 0 | 0.99496 | 0 / 129 |
| sf_high_27 | 54.374436 / 44.138929 | 21.287830 | 775.884474 | 36 / 36 | 0 | 0 | 0.99779 | 0 / 129 |
| sf_low_m40 | 72.113409 / 56.509268 | 25.945820 | 402.122603 | 36 / 36 | 0 | 0 | 0.82223 | 0 / 129 |
| ss_low_125 | 83.094622 / 65.309773 | 31.410030 | 392.710929 | 36 / 36 | 0 | 0 | 0.81565 | 0 / 129 |
| tt_nom_27 | 58.218513 / 46.737852 | 22.892378 | 557.022328 | 36 / 36 | 0 | 0 | 0.90811 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 4 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | fs_low_125 | sf_high_125 | sf_high_27 | sf_low_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MINP | 0.57704 | 0.69653 | 0.54169 | 0.64970 | 0.71951 | 0.60053 | 0.54080 | 0.60494 |
| MINN | 0.57709 | 0.69666 | 0.54169 | 0.64975 | 0.71964 | 0.60066 | 0.54079 | 0.60502 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| M14 | 0.98726 | 0.99211 | 0.81136 | 0.98733 | 0.99104 | 0.81213 | 0.81035 | 0.90203 |
| M15 | 0.98726 | 0.99211 | 0.81136 | 0.98733 | 0.99104 | 0.81214 | 0.81036 | 0.90203 |
| M12 | 0.98746 | 0.99199 | 0.81025 | 0.98968 | 0.99216 | 0.81398 | 0.81167 | 0.90188 |
| M13 | 0.98921 | 0.99199 | 0.81201 | 0.98968 | 0.99216 | 0.81398 | 0.81167 | 0.90188 |
| M10 | 0.95620 | 0.97903 | 0.79821 | 0.96035 | 0.97394 | 0.80781 | 0.80040 | 0.89191 |
| M11 | 0.95620 | 0.97903 | 0.79821 | 0.96035 | 0.97394 | 0.80781 | 0.80040 | 0.89191 |
| M6 | 0.96879 | 0.99256 | 0.79651 | 0.98585 | 0.99260 | 0.81559 | 0.80850 | 0.90196 |
| M7 | 0.96879 | 0.99256 | 0.79651 | 0.98585 | 0.99260 | 0.81559 | 0.80850 | 0.90196 |
| M8 | 0.98746 | 0.99256 | 0.80849 | 0.98875 | 0.99260 | 0.81559 | 0.80877 | 0.90196 |
| M9 | 0.98921 | 0.99256 | 0.81201 | 0.98913 | 0.99260 | 0.81559 | 0.81126 | 0.90196 |
| MCKN | 0.99000 | 0.99000 | 0.81000 | 0.99123 | 0.99167 | 0.81529 | 0.81248 | 0.90169 |
| MCKP | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| MRQP | 0.98836 | 0.99256 | 0.80950 | 0.99123 | 0.99260 | 0.81559 | 0.81248 | 0.90196 |
| MRQN | 0.98836 | 0.99256 | 0.80950 | 0.99123 | 0.99260 | 0.81559 | 0.81248 | 0.90196 |
| MAP | 0.99000 | 0.99211 | 0.81136 | 0.99000 | 0.99104 | 0.81213 | 0.81035 | 0.90203 |
| MAN | 0.99000 | 0.99211 | 0.81201 | 0.99000 | 0.99104 | 0.81309 | 0.81126 | 0.90203 |
| MBPP | 0.98522 | 0.98525 | 0.80795 | 0.98273 | 0.98265 | 0.80977 | 0.80617 | 0.89632 |
| MBPN | 0.99164 | 0.99779 | 0.81187 | 0.99496 | 0.99779 | 0.82223 | 0.81565 | 0.90811 |
| MOPP | 0.96999 | 0.98230 | 0.80284 | 0.97121 | 0.97620 | 0.80752 | 0.80204 | 0.89307 |
| MOPN | 0.99164 | 0.99779 | 0.81187 | 0.99496 | 0.99779 | 0.82223 | 0.81565 | 0.90811 |
| MBNP | 0.98522 | 0.98523 | 0.80794 | 0.98272 | 0.98263 | 0.80977 | 0.80617 | 0.89632 |
| MBNN | 0.99163 | 0.99778 | 0.81187 | 0.99496 | 0.99779 | 0.82222 | 0.81565 | 0.90811 |
| MONP | 0.96998 | 0.98230 | 0.80283 | 0.97120 | 0.97619 | 0.80752 | 0.80204 | 0.89306 |
| MONN | 0.99163 | 0.99778 | 0.81187 | 0.99496 | 0.99779 | 0.82222 | 0.81565 | 0.90811 |
| MDDP | 0.98746 | 0.98546 | 0.80849 | 0.98875 | 0.98775 | 0.81047 | 0.80877 | 0.89782 |
| MDDN | 0.98921 | 0.98811 | 0.81201 | 0.98913 | 0.98864 | 0.81309 | 0.81126 | 0.90070 |
| MUPRP1 | 0.99000 | 0.99256 | 0.81000 | 0.99000 | 0.99260 | 0.81559 | 0.81000 | 0.90196 |
| MUPRN1 | 0.99000 | 0.99256 | 0.81000 | 0.99000 | 0.99260 | 0.81559 | 0.81000 | 0.90196 |
| MUPBP1 | 0.99164 | 0.99779 | 0.81187 | 0.99496 | 0.99779 | 0.82223 | 0.81565 | 0.90811 |
| MUPBN1 | 0.99163 | 0.99778 | 0.81187 | 0.99496 | 0.99779 | 0.82222 | 0.81565 | 0.90811 |
| MUPOUTP1 | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99034 | 0.82084 | 0.81000 | 0.90119 |
| MUPOUTN1 | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99034 | 0.82084 | 0.81000 | 0.90119 |
| MDNOUTP1 | 0.97753 | 0.98867 | 0.80322 | 0.98505 | 0.99034 | 0.82084 | 0.80980 | 0.90119 |
| MDNOUTP2 | 0.97753 | 0.98867 | 0.80322 | 0.98505 | 0.99034 | 0.82084 | 0.80980 | 0.90119 |
| MDNOUTN1 | 0.97753 | 0.98867 | 0.80322 | 0.98505 | 0.99034 | 0.82084 | 0.80980 | 0.90119 |
| MDNOUTN2 | 0.97753 | 0.98867 | 0.80322 | 0.98505 | 0.99034 | 0.82084 | 0.80980 | 0.90119 |
| MCKUP | 0.99000 | 0.99000 | 0.81000 | 0.99123 | 0.99167 | 0.81529 | 0.81248 | 0.90169 |
| MBLEED | 0.99000 | 0.99000 | 0.81000 | 0.99123 | 0.99167 | 0.81529 | 0.81248 | 0.90169 |
| MUPXP | 0.99000 | 0.99199 | 0.81010 | 0.99000 | 0.99216 | 0.81398 | 0.81167 | 0.90188 |
| MUPXN | 0.99000 | 0.99199 | 0.81010 | 0.99000 | 0.99216 | 0.81398 | 0.81167 | 0.90188 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-054307-miyahara-buffer-v12-screen

The actual worst of the ten screened corners, SF/high/-40, remains below the strict 1 V terminal-pair limit at 0.125 ps / reltol 1e-7 / vabstol 1e-9: maximum stress 0.99933 V. All 36 decisions including 10 uV and all 36 reset cycles pass. Compared with 0.5 ps, the largest tabulated terminal-pair peak change is 20 uV (10 uV reporting precision); delay changes are +0.001458616 ps at 1 mV and +0.000063354 ps at 30 mV, reset changes -0.065925590 ps, and AVDD energy changes +0.003250368 fJ/cycle. The convergence comparison, full-cycle audit and saved-current phase audit are retained with this private evidence. This supports source promotion for new official tests; it does not establish formal qualification.

Actual clean source commit: `d9a026defa6c7c3cdaa948e8a82abbe1afcefe72`. Electrical SHA-256: `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_m40 | 54.809115 / 44.913968 | 20.589866 | 781.833658 | 36 / 36 | 0 | 0 | 0.99933 | 0 / 129 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_m40 |
|---|---:|
| MINP | 0.76806 |
| MINN | 0.76826 |
| MTAIL | 0.99000 |
| M14 | 0.99209 |
| M15 | 0.99209 |
| M12 | 0.99337 |
| M13 | 0.99337 |
| M10 | 0.98119 |
| M11 | 0.98119 |
| M6 | 0.99598 |
| M7 | 0.99598 |
| M8 | 0.99598 |
| M9 | 0.99597 |
| MCKN | 0.99151 |
| MCKP | 0.99000 |
| MRQP | 0.99598 |
| MRQN | 0.99597 |
| MAP | 0.99209 |
| MAN | 0.99209 |
| MBPP | 0.98327 |
| MBPN | 0.99933 |
| MOPP | 0.97884 |
| MOPN | 0.99933 |
| MBNP | 0.98327 |
| MBNN | 0.99933 |
| MONP | 0.97884 |
| MONN | 0.99933 |
| MDDP | 0.98665 |
| MDDN | 0.98811 |
| MUPRP1 | 0.99598 |
| MUPRN1 | 0.99597 |
| MUPBP1 | 0.99933 |
| MUPBN1 | 0.99933 |
| MUPOUTP1 | 0.99392 |
| MUPOUTN1 | 0.99392 |
| MDNOUTP1 | 0.99392 |
| MDNOUTP2 | 0.99392 |
| MDNOUTN1 | 0.99392 |
| MDNOUTN2 | 0.99392 |
| MCKUP | 0.99151 |
| MBLEED | 0.99151 |
| MUPXP | 0.99337 |
| MUPXN | 0.99337 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
