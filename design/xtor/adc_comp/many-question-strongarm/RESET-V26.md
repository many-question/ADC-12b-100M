# RESET-V26: smaller input-to-latch coupling devices

V25 passes its three initial deterministic corners but retains the same short-diagnostic error at cycle 54 as V20. Its Q descriptive SNR falls from 1.896073 to 1.362273 at +30 ps and from 3.346148 to 3.165670 at +40 ps. At +30 ps all 256 DP signs are correct while 25 Q signs disagree with the input, versus eight for V20. By +40 ps only the final wrong Q sign remains. The source, complete data and comparison are preserved in [RESET-V25.md](RESET-V25.md). V25 stops broader expansion without a formal noise claim.

This experiment branches electrically from V20, retaining its original 0.5 um/30 nm Q reset pull-downs, 3 um tail, clock inverter and all five MOMs. Only MLNP/MLNN change from 12 um/nf12 to 8 um/nf8, with 30 nm length and 1 um finger width fixed. All other 21 MOS devices and every capacitor are electrically identical to V20.

These two devices connect input drains to Q and participate in regeneration. Reducing their size tests lower loading and feedthrough against weaker conduction. V25 differs from V20 in both coupling devices and reset pull-downs, so its phase result cannot identify the contribution of either change alone. No device-noise or transconductance benefit is assumed for V26.

The successful zero-warning callback supplies the full geometry and parasitics, SHA-256 `e705ebc2985cc3b6bbbe232cb188f1b0c155751d55a7a5aeaeec5df014a19f6a`. Electrical SHA-256: `b998df98508db1d2ee4ce09c29501dc78ed54f93ce5b7416002dd934b4b5ab8d`. The [source](RESET-V26.txt) contains 23 MOS and 5 MOMs with complete RNL checked on a byte-identical mirror.

SF/FS high/-40 are checked first, then TT and a matched short phase diagnosis on a useful pass. Timing, full AVDD cost, reset, output validity and every terminal pair must be measured again. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and original formal tests remain open. The canonical source and every genuine original record remain unchanged.

![Physical comparator experiment](reset-v26.png)

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
