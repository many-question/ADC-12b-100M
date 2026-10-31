# RESET-V26: smaller input-to-latch coupling devices

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

V25 passes its three initial deterministic corners but retains the same short-diagnostic error at cycle 54 as V20. Its Q descriptive SNR falls from 1.896073 to 1.362273 at +30 ps and from 3.346148 to 3.165670 at +40 ps. At +30 ps all 256 DP signs are correct while 25 Q signs disagree with the input, versus eight for V20. By +40 ps only the final wrong Q sign remains. The source, complete data and comparison are preserved in [RESET-V25.md](RESET-V25.md). V25 stops broader expansion without a formal noise claim.

This experiment branches electrically from V20, retaining its original 0.5 um/30 nm Q reset pull-downs, 3 um tail, clock inverter and all five MOMs. Only MLNP/MLNN change from 12 um/nf12 to 8 um/nf8, with 30 nm length and 1 um finger width fixed. All other 21 MOS devices and every capacitor are electrically identical to V20.

These two devices connect input drains to Q and participate in regeneration. Reducing their size tests lower loading and feedthrough against weaker conduction. V25 differs from V20 in both coupling devices and reset pull-downs, so its phase result cannot identify the contribution of either change alone. No device-noise or transconductance benefit is assumed for V26.

The successful zero-warning callback supplies the full geometry and parasitics, SHA-256 `e705ebc2985cc3b6bbbe232cb188f1b0c155751d55a7a5aeaeec5df014a19f6a`. Electrical SHA-256: `b998df98508db1d2ee4ce09c29501dc78ed54f93ce5b7416002dd934b4b5ab8d`. The [source](RESET-V26.txt) contains 23 MOS and 5 MOMs with complete RNL checked on a byte-identical mirror.

SF/FS high/-40 are checked first, then TT and a matched short phase diagnosis on a useful pass. Timing, full AVDD cost, reset, output validity and every terminal pair must be measured again. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and original formal tests remain open. The canonical source and every genuine original record remain unchanged.

![Physical comparator experiment](https://raw.githubusercontent.com/many-question/ADC-12b-100M/8728841e7a6946263fb953d45599cb4afef59ce7/design/xtor/adc_comp/many-question-strongarm/reset-v26.png)

## Completed screen 20261031-102928-strongarm-reset-v26-screen

All 72 actual polarities including 10 uV and all 72 resets pass, with timing, physical output validity and every one of 69 MOS terminal pairs passing at every tested corner. These private deterministic results do not establish noise qualification.

Actual clean source commit: `9dc9b87c386183be5ca41b735460da8683cbe8f4`. Electrical SHA-256: `b998df98508db1d2ee4ce09c29501dc78ed54f93ce5b7416002dd934b4b5ab8d`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 52.889611 / 41.740818 | 20.093162 | 532.977486 | 36 / 36 | 0 | 0 | 0.99567 | 0 / 69 |
| sf_high_m40 | 67.543399 / 51.923804 | 18.375541 | 501.836178 | 36 / 36 | 0 | 0 | 0.99729 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69865 | 0.76439 |
| MINN | 0.69878 | 0.76461 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99336 | 0.99210 |
| MRDN | 0.99336 | 0.99210 |
| MLNP | 0.99128 | 0.99030 |
| MLNN | 0.99128 | 0.99030 |
| MLPP | 0.99365 | 0.99248 |
| MLPN | 0.99365 | 0.99248 |
| MRQP | 0.99365 | 0.99469 |
| MRQN | 0.99365 | 0.99469 |
| MOPN | 0.99567 | 0.99729 |
| MOPP | 0.99527 | 0.99656 |
| MONN | 0.99567 | 0.99729 |
| MONP | 0.99527 | 0.99656 |
| MDQP | 0.99543 | 0.99676 |
| MDQN | 0.99543 | 0.99676 |
| MDDP | 0.98360 | 0.98525 |
| MDDN | 0.98676 | 0.98775 |
| MCKN | 0.99345 | 0.99595 |
| MCKP | 0.99031 | 0.99000 |
| MBLEED | 0.99345 | 0.99595 |
| MUP | 0.99345 | 0.99595 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-103621-strongarm-reset-v26-screen

All 36 actual polarities including 10 uV and all 36 resets pass, with timing, physical output validity and every one of 69 MOS terminal pairs passing at every tested corner. These private deterministic results do not establish noise qualification.

Actual clean source commit: `9dc9b87c386183be5ca41b735460da8683cbe8f4`. Electrical SHA-256: `b998df98508db1d2ee4ce09c29501dc78ed54f93ce5b7416002dd934b4b5ab8d`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 61.365647 / 47.176672 | 22.502805 | 398.516283 | 36 / 36 | 0 | 0 | 0.90609 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.60156 |
| MINN | 0.60165 |
| MTAIL | 0.90000 |
| MRDP | 0.90156 |
| MRDN | 0.90156 |
| MLNP | 0.89937 |
| MLNN | 0.89937 |
| MLPP | 0.90183 |
| MLPN | 0.90183 |
| MRQP | 0.90526 |
| MRQN | 0.90526 |
| MOPN | 0.90566 |
| MOPP | 0.90544 |
| MONN | 0.90566 |
| MONP | 0.90544 |
| MDQP | 0.90609 |
| MDQN | 0.90609 |
| MDDP | 0.89740 |
| MDDN | 0.90059 |
| MCKN | 0.90609 |
| MCKP | 0.90065 |
| MBLEED | 0.90609 |
| MUP | 0.90609 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


Across these initial corners, 108 actual polarities and resets pass. TT 1/30 mV delay is 61.365646515/47.176672294 ps, reset 22.502805277 ps, and mixed-sequence clock capacitance 15.802015488 fF. This clock estimate is diagnostic and does not replace the original formal capacitance test. A matched short phase diagnosis follows before broader expansion; no formal noise pass or canonical promotion is claimed.

The independently recomputed unrounded maxima at the initial screened corners are:

| Corner | Worst device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| fs_high_m40 | MOPN ds | 0.995674947664 | 4325.052335807 | -194.731624428 | 5.268375572 |
| sf_high_m40 | MOPN ds | 0.997294420103 | 2705.579896646 | -194.362262720 | 5.637737280 |

These 0.5 ps results require actual-worst tighter integration if the source advances. Full AVDD waveform integrals include physical reset and weak rail loads over all 36 cycles and the same 100 ps–14.5 ns window. All supply probes are present and KCL closes to numerical precision.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 532.977944354 | 94.426546127 | 438.551398228 | 1640.915033862 |
| sf_high_m40 | 501.836788562 | 110.526321583 | 391.310466980 | 1407.687495035 |
| tt_nom_27 | 398.516712298 | 83.862647693 | 314.654064605 | 1174.561976866 |

Every archived entry was read back with CRC and SHA-256 verification before duplicate local raw files were removed; owned remote runs are absent.

- `20261031-102928-strongarm-reset-v26-screen`: `ff01d7a2dfdf2ab3c928440d79ed193453c5529ae092584ba3dcd317b77eade3`.
- `20261031-103621-strongarm-reset-v26-screen`: `16dea2efd747e0993f40faa4ac73060a1dafac87de52f24af49b96526ad0d913`.


## Matched short phase result

Run `20261031-104525-strongarm-reset-v26-noise-numerics-diagnostic-screen`, clean source `451dc6004aba5727e9aecd8ce16df9d9465d71f4`, matches V20's instrumented short testbench, +/-800 uV, 128 cycles per level, seed 1, 50 GHz and 0.5 ps/1e-6/1e-8 integration. V26 retains one wrong polarity at cycle 54: OUTP 1/128 at -800 uV and 128/128 at +800 uV. All 256 samples remain included. Shared seeds and equal error counts do not establish equal underlying noise or independent trials.

All 256 resets complete, maximum 21.685153076 ps. There are no +80/+150 ps to final sign changes, late-reset or output-validity violations. All 69 terminal pairs pass, maximum 0.90667 V.

| Phase | Quantity | V20 secant gain | V26 secant gain | V20 descriptive SNR | V26 descriptive SNR |
|---|---|---:|---:|---:|---:|
| +20 ps | DP_minus_DN | -3.650071549 | -3.737213241 | 4.099704178 | 4.103276767 |
| +20 ps | QP_minus_QN | 0.208661496 | 0.157514921 | 0.305432364 | 0.216591685 |
| +30 ps | DP_minus_DN | -2.957057553 | -3.102577705 | 4.112015332 | 4.119998153 |
| +30 ps | QP_minus_QN | -2.258471023 | -2.505933692 | 1.896073158 | 1.917068000 |
| +40 ps | DP_minus_DN | 1.097011210 | 0.951521206 | 0.976058759 | 0.844930207 |
| +40 ps | QP_minus_QN | -10.653248828 | -11.751703200 | 3.346147610 | 3.261935628 |

These waveform means and within-level variation are descriptive, not formal input-referred noise. Early feedthrough can reverse internal signs and late regeneration saturates. The exact mismatch counts are retained below; internal signs are not completed output decisions.

| Phase | DP input-sign mismatches | Q input-sign mismatches | Q final-sign mismatches |
|---|---:|---:|---:|
| +20 ps | 0 | 147 | 146 |
| +30 ps | 0 | 9 | 8 |
| +40 ps | 214 | 1 | 0 |

At -20 ps, Q differential standard deviations are 0.361281/0.373230 mV across the two levels, versus V20 0.356192/0.364912 mV. At +20 ps they are 0.565746/0.591128 mV, versus 0.534098/0.555201 mV. Cycle 54 retains the following differentials:

| Phase | DP-DN mV | QP-QN mV |
|---|---:|---:|
| -20 ps | -0.005695590 | -0.812609459 |
| +5 ps | -0.198022951 | -1.385587688 |
| +10 ps | 0.385074946 | -1.444416445 |
| +20 ps | 0.987254261 | -1.478310322 |
| +30 ps | 1.806141214 | -1.318657131 |
| +40 ps | 2.129363350 | -1.996134628 |
| +60 ps | 11.608600830 | -83.886379660 |

Q SNR improves about 1.1% at +30 ps and falls about 2.5% at +40 ps. This limited change does not support broader noise qualification. V26 remains unpromoted. V27 retains its MOS devices and tests only larger Q storage; its signal attenuation, delay, reset, stress and noise remain to be measured.

| Device | max abs(Vgs) V | max abs(Vgd) V | max abs(Vds) V |
|---|---:|---:|---:|
| MINP | 0.49246 | 0.49209 | 0.59046 |
| MINN | 0.49245 | 0.49211 | 0.59075 |
| MTAIL | 0.90000 | 0.89928 | 0.56812 |
| MRDP | 0.90000 | 0.89927 | 0.90169 |
| MRDN | 0.90000 | 0.89922 | 0.90171 |
| MLNP | 0.89944 | 0.89972 | 0.89958 |
| MLNN | 0.89949 | 0.89972 | 0.89943 |
| MLPP | 0.90218 | 0.89972 | 0.90216 |
| MLPN | 0.90216 | 0.89972 | 0.90218 |
| MRQP | 0.90000 | 0.90555 | 0.90216 |
| MRQN | 0.90000 | 0.90569 | 0.90218 |
| MOPN | 0.90595 | 0.90612 | 0.90598 |
| MOPP | 0.90216 | 0.90612 | 0.90247 |
| MONN | 0.90600 | 0.90612 | 0.90591 |
| MONP | 0.90218 | 0.90612 | 0.90240 |
| MDQP | 0.90667 | 0.89896 | 0.90595 |
| MDQN | 0.90667 | 0.89881 | 0.90600 |
| MDDP | 0.89565 | 0.00000 | 0.89565 |
| MDDN | 0.89632 | 0.00000 | 0.89632 |
| MCKN | 0.90000 | 0.89423 | 0.90667 |
| MCKP | 0.90000 | 0.89423 | 0.90133 |
| MBLEED | 0.90000 | 0.90133 | 0.90667 |
| MUP | 0.90000 | 0.90667 | 0.90133 |

Archive SHA-256 `b0c6cc3121a8832fc0f54befe1a71097c69464699afca51c578f6a82445b07bf` preserves raw data, all indices, phase signs and the matched comparison. Every entry was read back with CRC and SHA-256 verification, and the owned remote run is absent. The 102.5 ns duration raises noisefmin to 9.7561 MHz versus the original 287.216 kHz. No formal V26 noise result is claimed; canonical V19 and all genuine original records remain unchanged.
