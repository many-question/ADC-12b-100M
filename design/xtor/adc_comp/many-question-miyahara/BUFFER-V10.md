# BUFFER-V10: strengthen only the external output pull-down

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

Current disposition: rejected for expansion after the additional cold high-voltage corners. See the final completed-screen section below.

B9 passes six-corner terminal stress and output validity, but SS reset is 36.120741 ps. Its SF clock peak already reaches 0.99996 V, leaving little room to strengthen the clock further. This experiment changes only MOPN and MONN from N2 to N3 um, L=30 nm, with 3 fingers. Complete geometry and parasitics are copied from an identical previously validated canonical device. Stronger output discharge and a lower inverter trip point may improve the physical reset metric; the added gate load also changes the upstream waveform, so delay, output validity and all-device stress must be measured again. No Q-shunt or weak pull-up is strengthened.

The [independent source](BUFFER-V10.txt) has electrical SHA-256 `4eae39dc8dd9e629aeb066adca6a1cba564a99e6ea9de6d8580a6dc5ac77df9b`. Full RNL on a byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the rendered schematic was inspected.

![External output pull-down change](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0c799462e700c1f74a9448031e14abdd56ec18e7/design/xtor/adc_comp/many-question-miyahara/buffer-v10.png)

The six-key-corner screen retains the same complete transient checks and current probes. Any passing revision proceeds to further qualification; failed revisions retain their evidence and stop their own expansion. [Energy comparison](ENERGY-COMPARISON.md) reports the measured persistent-current costs of the preceding implementations; no new performance or efficiency pass is assumed.

## Completed screen 20261031-045056-miyahara-buffer-v10-screen

All six initial key corners pass full-trace terminal stress, actual polarity, output validity, delay/reset and regeneration time. Each has 36 correct decisions including 10 uV and 36 recorded resets. SS low/hot reset is 31.734685 ps and TT 30 mV delay 47.891630 ps. SF high/27 stress is 0.99996 V, so additional SF temperature-endpoint/FS corners and targeted numerical convergence precede further qualification. Old-circuit capacitance, noise and mismatch are not inherited.

Actual clean source commit: `55e47d9408969297f49322c920b20db27f98e2da`. Electrical SHA-256: `4eae39dc8dd9e629aeb066adca6a1cba564a99e6ea9de6d8580a6dc5ac77df9b`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 51.718866 / 38.901451 | 18.252107 | 766.174343 | 36 / 36 | 0 | 0 | 0.99635 | 0 / 117 |
| ff_high_m40 | 43.467163 / 35.258658 | 17.084198 | 653.629194 | 36 / 36 | 0 | 0 | 0.99957 | 0 / 117 |
| sf_high_27 | 55.569521 / 45.316156 | 21.500096 | 628.915766 | 36 / 36 | 0 | 0 | 0.99996 | 0 / 117 |
| sf_low_m40 | 74.035487 / 58.160578 | 26.022523 | 327.484816 | 36 / 36 | 0 | 0 | 0.82262 | 0 / 117 |
| ss_low_125 | 84.968543 / 67.049990 | 31.734685 | 336.687735 | 36 / 36 | 0 | 0 | 0.81926 | 0 / 117 |
| tt_nom_27 | 59.443851 / 47.891630 | 23.118961 | 457.451059 | 36 / 36 | 0 | 0 | 0.90964 | 0 / 117 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | sf_high_27 | sf_low_m40 | ss_low_125 | tt_nom_27 |
|---|---:|---:|---:|---:|---:|---:|
| MINP | 0.57704 | 0.69652 | 0.71949 | 0.60052 | 0.54079 | 0.60493 |
| MINN | 0.57710 | 0.69664 | 0.71963 | 0.60065 | 0.54079 | 0.60502 |
| MTAIL | 0.99000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 | 0.90000 |
| M14 | 0.98726 | 0.99957 | 0.99459 | 0.81880 | 0.81443 | 0.90792 |
| M15 | 0.98726 | 0.99949 | 0.99461 | 0.81880 | 0.81434 | 0.90792 |
| M12 | 0.98763 | 0.99317 | 0.99338 | 0.81495 | 0.81193 | 0.90298 |
| M13 | 0.98921 | 0.99317 | 0.99338 | 0.81495 | 0.81193 | 0.90298 |
| M10 | 0.95594 | 0.97917 | 0.97399 | 0.80797 | 0.80020 | 0.89188 |
| M11 | 0.95594 | 0.97917 | 0.97399 | 0.80797 | 0.80020 | 0.89188 |
| M6 | 0.97581 | 0.99446 | 0.99453 | 0.81693 | 0.81058 | 0.90383 |
| M7 | 0.97581 | 0.99446 | 0.99453 | 0.81693 | 0.81058 | 0.90383 |
| M8 | 0.98747 | 0.99446 | 0.99453 | 0.81693 | 0.81058 | 0.90383 |
| M9 | 0.98921 | 0.99446 | 0.99453 | 0.81693 | 0.81127 | 0.90383 |
| MCKN | 0.99635 | 0.99890 | 0.99996 | 0.82262 | 0.81926 | 0.90964 |
| MCKP | 0.99000 | 0.99908 | 0.99585 | 0.81982 | 0.81593 | 0.90832 |
| MRQP | 0.99635 | 0.99890 | 0.99996 | 0.82262 | 0.81926 | 0.90964 |
| MRQN | 0.99635 | 0.99890 | 0.99996 | 0.82262 | 0.81926 | 0.90964 |
| MAP | 0.99000 | 0.99211 | 0.99105 | 0.81213 | 0.81035 | 0.90204 |
| MAN | 0.99000 | 0.99211 | 0.99104 | 0.81310 | 0.81127 | 0.90203 |
| MBPP | 0.98576 | 0.98572 | 0.98304 | 0.81043 | 0.80654 | 0.89678 |
| MBPN | 0.99206 | 0.99782 | 0.99788 | 0.82224 | 0.81553 | 0.90805 |
| MOPP | 0.97040 | 0.98221 | 0.97627 | 0.80753 | 0.80192 | 0.89294 |
| MOPN | 0.99206 | 0.99782 | 0.99788 | 0.82224 | 0.81553 | 0.90805 |
| MBNP | 0.98575 | 0.98571 | 0.98301 | 0.81043 | 0.80654 | 0.89678 |
| MBNN | 0.99206 | 0.99782 | 0.99787 | 0.82223 | 0.81553 | 0.90805 |
| MONP | 0.97040 | 0.98221 | 0.97627 | 0.80753 | 0.80192 | 0.89294 |
| MONN | 0.99206 | 0.99782 | 0.99787 | 0.82223 | 0.81553 | 0.90805 |
| MDDP | 0.98747 | 0.98546 | 0.98776 | 0.81047 | 0.80877 | 0.89782 |
| MDDN | 0.98921 | 0.98812 | 0.98864 | 0.81310 | 0.81127 | 0.90071 |
| MUPRP1 | 0.99000 | 0.99446 | 0.99453 | 0.81693 | 0.81058 | 0.90383 |
| MUPRN1 | 0.99000 | 0.99446 | 0.99453 | 0.81693 | 0.81058 | 0.90383 |
| MUPBP1 | 0.99206 | 0.99782 | 0.99788 | 0.82224 | 0.81553 | 0.90805 |
| MUPBN1 | 0.99206 | 0.99782 | 0.99787 | 0.82223 | 0.81553 | 0.90805 |
| MUPOUTP1 | 0.99000 | 0.99000 | 0.99083 | 0.82159 | 0.81011 | 0.90159 |
| MUPOUTN1 | 0.99000 | 0.99000 | 0.99083 | 0.82159 | 0.81011 | 0.90159 |
| MDNOUTP1 | 0.97788 | 0.98904 | 0.99083 | 0.82159 | 0.81011 | 0.90159 |
| MDNOUTP2 | 0.97788 | 0.98904 | 0.99083 | 0.82159 | 0.81011 | 0.90159 |
| MDNOUTN1 | 0.97788 | 0.98904 | 0.99083 | 0.82159 | 0.81011 | 0.90159 |
| MDNOUTN2 | 0.97788 | 0.98904 | 0.99083 | 0.82159 | 0.81011 | 0.90159 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-045842-miyahara-buffer-v10-screen

B10 is rejected for expansion: SF/high/-40 reaches CKB=1.000656171 V, failing 3 terminal pairs; FS/high/-40 reaches CKB=-0.011143791 V, producing 1.001143791 V maximum terminal stress and failing 5 pairs. The upper peak is 1.038279 ps before the rising 50% clock crossing; the lower peak is 1.571604 ps before the falling crossing. The other two added corners pass. All four added corners have 36 correct polarities including 10 uV, 36 completed resets, and passing delay, reset, regeneration and output validity. Across ten measured corners, FS/high/-40 is the actual worst stress; six earlier passing corners do not qualify this source. No further corner, noise, MC or canonical promotion is performed for B10.

Actual clean source commit: `55e47d9408969297f49322c920b20db27f98e2da`. Electrical SHA-256: `4eae39dc8dd9e629aeb066adca6a1cba564a99e6ea9de6d8580a6dc5ac77df9b`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 51.972159 / 42.676909 | 20.251623 | 585.417311 | 36 / 36 | 0 | 0 | 1.00114 | 5 / 117 |
| fs_low_125 | 74.307822 / 56.850039 | 25.233103 | 374.256732 | 36 / 36 | 0 | 0 | 0.81644 | 0 / 117 |
| sf_high_125 | 58.080440 / 45.970891 | 22.195191 | 677.673728 | 36 / 36 | 0 | 0 | 0.99891 | 0 / 117 |
| sf_high_m40 | 56.253586 / 46.278801 | 20.777609 | 622.772546 | 36 / 36 | 0 | 0 | 1.00066 | 3 / 117 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5 ps, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 3 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | fs_low_125 | sf_high_125 | sf_high_m40 |
|---|---:|---:|---:|---:|
| MINP | 0.70288 | 0.54169 | 0.64969 | 0.76805 |
| MINN | 0.70301 | 0.54169 | 0.64974 | 0.76825 |
| MTAIL | 0.99000 | 0.81000 | 0.99000 | 0.99000 |
| M14 | 1.00091 | 0.81540 | 0.98733 | 0.99802 |
| M15 | 1.00092 | 0.81531 | 0.98733 | 0.99802 |
| M12 | 0.99360 | 0.81031 | 0.99033 | 0.99444 |
| M13 | 0.99360 | 0.81202 | 0.99033 | 0.99444 |
| M10 | 0.98627 | 0.79794 | 0.96020 | 0.98129 |
| M11 | 0.98627 | 0.79794 | 0.96020 | 0.98129 |
| M6 | 0.99496 | 0.80012 | 0.98910 | 0.99688 |
| M7 | 0.99496 | 0.80012 | 0.98910 | 0.99688 |
| M8 | 0.99496 | 0.80849 | 0.98910 | 0.99688 |
| M9 | 0.99496 | 0.81202 | 0.98914 | 0.99687 |
| MCKN | 0.99945 | 0.81644 | 0.99891 | 1.00066 |
| MCKP | 1.00114 | 0.81630 | 0.99000 | 0.99868 |
| MRQP | 1.00073 | 0.81644 | 0.99891 | 1.00066 |
| MRQN | 1.00073 | 0.81644 | 0.99891 | 1.00066 |
| MAP | 0.99316 | 0.81136 | 0.99000 | 0.99208 |
| MAN | 0.99316 | 0.81202 | 0.99000 | 0.99208 |
| MBPP | 0.98998 | 0.80825 | 0.98316 | 0.98382 |
| MBPN | 0.99917 | 0.81173 | 0.99529 | 0.99935 |
| MOPP | 0.98707 | 0.80278 | 0.97152 | 0.97876 |
| MOPN | 0.99917 | 0.81173 | 0.99529 | 0.99935 |
| MBNP | 0.98998 | 0.80824 | 0.98314 | 0.98382 |
| MBNN | 0.99917 | 0.81173 | 0.99528 | 0.99935 |
| MONP | 0.98707 | 0.80278 | 0.97152 | 0.97876 |
| MONN | 0.99917 | 0.81173 | 0.99528 | 0.99935 |
| MDDP | 0.98440 | 0.80849 | 0.98876 | 0.98665 |
| MDDN | 0.98724 | 0.81202 | 0.98914 | 0.98811 |
| MUPRP1 | 0.99496 | 0.81000 | 0.99000 | 0.99688 |
| MUPRN1 | 0.99496 | 0.81000 | 0.99000 | 0.99687 |
| MUPBP1 | 0.99917 | 0.81173 | 0.99529 | 0.99935 |
| MUPBN1 | 0.99917 | 0.81173 | 0.99528 | 0.99935 |
| MUPOUTP1 | 0.99000 | 0.81000 | 0.99000 | 0.99462 |
| MUPOUTN1 | 0.99000 | 0.81000 | 0.99000 | 0.99462 |
| MDNOUTP1 | 0.98954 | 0.80344 | 0.98535 | 0.99462 |
| MDNOUTP2 | 0.98954 | 0.80344 | 0.98535 | 0.99462 |
| MDNOUTN1 | 0.98954 | 0.80344 | 0.98535 | 0.99462 |
| MDNOUTN2 | 0.98954 | 0.80344 | 0.98535 | 0.99462 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.
