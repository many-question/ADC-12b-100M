# RESET-V25: restore reset stress margin with N16 coupling devices

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

V24 retains all 72 actual decisions/resets and output validity in its first two corners, but SF/high/-40 fails ten terminal pairs. The raw QP peak is 1.003007138068 V at 12.971441 ps after the falling clock midpoint, with CLKC at zero and CKB already 0.982878276 V. [RESET-V24.md](RESET-V24.md) preserves the failure and complete waveform context. This is a measured reset-phase excursion; V24 has no TT or noise result.

This experiment retains V24's N16 input-to-latch devices and changes only MDQP/MDQN width from 0.5 to 0.6 um, with **30 nm length and nf1 directly verified in both sources**. A successful zero-warning N0.6 callback supplies full geometry and parasitics, SHA-256 `ccfef9d9791477066b24dc0de5813cab07a124a26c6dae5e9ced0468b2b41116`. All other 21 MOS devices and all five MOMs remain electrically identical to V24, including the 3 um tail, N4/P2.7 clock inverter and 20-finger Q capacitors.

The stronger reset pull-down tests whether more sink strength suppresses the observed peak while retaining the larger coupling devices. It will also change the reset common mode, loading, clock trajectory, current and noise. No noise benefit is assumed or inherited, and the lower shunt-width experiments on a different coupling geometry do not establish its performance. Complete AVDD cost, including persistent reset current, must be measured.

Electrical SHA-256: `6209fed9ad21a8f92ce471c5e762260227b0d820c22cba8396cd6c637b543cdf`. The [source](RESET-V25.txt) contains 23 MOS and 5 MOMs with complete RNL checked on a byte-identical mirror. SF/FS high/-40 are checked first for stress, polarity, reset and output validity. TT and a matched short phase diagnosis follow only on a useful pass. Remaining known corners, actual-worst convergence, source-preserving canonical promotion and original formal tests remain open. Canonical V19 and every genuine formal result remain unchanged.

![Physical comparator with stronger Q reset pull-downs](https://raw.githubusercontent.com/many-question/ADC-12b-100M/8728841e7a6946263fb953d45599cb4afef59ce7/design/xtor/adc_comp/many-question-strongarm/reset-v25.png)

## Completed screen 20261031-100338-strongarm-reset-v25-screen

All 72 actual polarities including 10 uV and all 72 resets pass, with timing, physical output validity and every one of 69 MOS terminal pairs passing at every tested corner. These private deterministic results do not establish noise qualification.

Actual clean source commit: `0a7534091e86e24fff3105bdbf4977eb84bc1bce`. Electrical SHA-256: `6209fed9ad21a8f92ce471c5e762260227b0d820c22cba8396cd6c637b543cdf`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 55.119992 / 43.792854 | 22.195165 | 597.624740 | 36 / 36 | 0 | 0 | 0.99825 | 0 / 69 |
| sf_high_m40 | 70.527271 / 54.361897 | 20.695709 | 563.207091 | 36 / 36 | 0 | 0 | 0.99986 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69727 | 0.76355 |
| MINN | 0.69739 | 0.76374 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99309 | 0.99169 |
| MRDN | 0.99309 | 0.99169 |
| MLNP | 0.99076 | 0.98961 |
| MLNN | 0.99076 | 0.98961 |
| MLPP | 0.99313 | 0.99176 |
| MLPN | 0.99313 | 0.99176 |
| MRQP | 0.99736 | 0.99873 |
| MRQN | 0.99736 | 0.99873 |
| MOPN | 0.99825 | 0.99986 |
| MOPP | 0.99805 | 0.99961 |
| MONN | 0.99825 | 0.99986 |
| MONP | 0.99805 | 0.99961 |
| MDQP | 0.99825 | 0.99986 |
| MDQN | 0.99825 | 0.99986 |
| MDDP | 0.98344 | 0.98514 |
| MDDN | 0.98651 | 0.98759 |
| MCKN | 0.99335 | 0.99589 |
| MCKP | 0.99031 | 0.99000 |
| MBLEED | 0.99335 | 0.99589 |
| MUP | 0.99335 | 0.99589 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-100951-strongarm-reset-v25-screen

All 36 actual polarities including 10 uV and all 36 resets pass, with timing, physical output validity and every one of 69 MOS terminal pairs passing at every tested corner. These private deterministic results do not establish noise qualification.

Actual clean source commit: `0a7534091e86e24fff3105bdbf4977eb84bc1bce`. Electrical SHA-256: `6209fed9ad21a8f92ce471c5e762260227b0d820c22cba8396cd6c637b543cdf`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 63.616262 / 49.007296 | 24.958945 | 447.254687 | 36 / 36 | 0 | 0 | 0.90862 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.60077 |
| MINN | 0.60086 |
| MTAIL | 0.90000 |
| MRDP | 0.90090 |
| MRDN | 0.90089 |
| MLNP | 0.89839 |
| MLNN | 0.89839 |
| MLPP | 0.90091 |
| MLPN | 0.90091 |
| MRQP | 0.90862 |
| MRQN | 0.90862 |
| MOPN | 0.90862 |
| MOPP | 0.90845 |
| MONN | 0.90862 |
| MONP | 0.90845 |
| MDQP | 0.90862 |
| MDQN | 0.90862 |
| MDDP | 0.89719 |
| MDDN | 0.90030 |
| MCKN | 0.90601 |
| MCKP | 0.90063 |
| MBLEED | 0.90601 |
| MUP | 0.90601 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


Across these initial corners, 108 actual polarities and resets pass. TT 1/30 mV delay is 63.616261871/49.007296131 ps, reset 24.958945456 ps, and mixed-sequence clock capacitance 15.716168619 fF. This clock estimate is diagnostic and does not replace the original formal capacitance test. A matched short phase diagnosis follows before broader expansion; no formal noise pass or canonical promotion is claimed.

The independently recomputed unrounded maxima at the two initial high-voltage cold corners are:

| Corner | Worst device pair | Peak V | Margin uV | Since rise ps | Since fall ps |
|---|---|---:|---:|---:|---:|
| fs_high_m40 | MOPN gs | 0.998251953114 | 1748.046886426 | -195.964741682 | 4.035258318 |
| sf_high_m40 | MOPN gs | 0.999855286288 | 144.713712192 | 203.455657585 | 3.455657585 |

These 0.5 ps results require actual-worst tighter integration if the source advances. Full AVDD waveform integrals include physical reset and weak rail loads over all 36 cycles and the same 100 ps–14.5 ns window. All supply probes are present and KCL closes to numerical precision.

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 597.625246607 | 107.949144184 | 489.676102423 | 1888.580786208 |
| sf_high_m40 | 563.207735218 | 125.450483635 | 437.757251582 | 1624.016331704 |
| tt_nom_27 | 447.255148884 | 96.948720675 | 350.306428209 | 1358.730461855 |

Every archived entry was read back with CRC and SHA-256 verification before duplicate local raw files were removed; owned remote runs are absent.

- `20261031-100338-strongarm-reset-v25-screen`: `e0f659fe04f0fc2d0174e8e2f9a2a3719b6579403429ef0af36f22cad0f93f9f`.
- `20261031-100951-strongarm-reset-v25-screen`: `e6621c0129a8dab29af8caacea1167c23e21da79e7fe1be24b92d85d630f9c28`.


## Matched short phase result

Run `20261031-101638-strongarm-reset-v25-noise-numerics-diagnostic-screen`, clean source `e5e6773efe635e934b962053bae26c5affef3f3c`, matches V20's short two-level protocol, instrumented testbench hash, +/-800 uV, 128 cycles per level, seed 1, 50 GHz and 0.5 ps/1e-6/1e-8 integration. V25 retains one wrong polarity, again at cycle 54: OUTP 1/128 at -800 uV and 128/128 at +800 uV. All 256 samples remain included. Identical error counts and a shared seed do not establish equal underlying noise or independent trials.

All 256 resets complete, maximum 24.138468340 ps, with no +80/+150 ps to final sign changes, late-reset or output-validity violations. All 69 terminal pairs pass, maximum 0.90924 V.

| Phase | Quantity | V20 secant gain | V25 secant gain | V20 descriptive SNR | V25 descriptive SNR |
|---|---|---:|---:|---:|---:|
| +20 ps | DP_minus_DN | -3.650071549 | -3.593551767 | 4.099704178 | 4.093796413 |
| +20 ps | QP_minus_QN | 0.208661496 | 0.276959481 | 0.305432364 | 0.404569680 |
| +30 ps | DP_minus_DN | -2.957057553 | -3.377928863 | 4.112015332 | 4.482905719 |
| +30 ps | QP_minus_QN | -2.258471023 | -1.365841608 | 1.896073158 | 1.362273050 |
| +40 ps | DP_minus_DN | 1.097011210 | 0.483815843 | 0.976058759 | 0.490915431 |
| +40 ps | QP_minus_QN | -10.653248828 | -8.364798338 | 3.346147610 | 3.165669523 |

These are two-level waveform means and within-level variation, not formal input-referred noise. Early feedthrough can reverse internal signs, and late regeneration saturates. At +30 ps, DP signs match the input in every cycle, while Q signs disagree in 25 cycles versus eight for V20. At +40 ps Q signs already match every final decision, including the one error. The wrong cycle has the following measured differentials:

| Phase | DP-DN mV | QP-QN mV |
|---|---:|---:|
| +20 ps | 0.951726871 | -1.512187500 |
| +30 ps | 1.789306042 | -1.490023227 |
| +40 ps | 2.246800431 | -2.051523227 |
| +60 ps | 10.427864114 | -47.907537231 |

V25 combines N16 coupling devices and 0.6 um Q reset pull-downs relative to V20, so these observations cannot isolate either change. The combination lowers early Q SNR and increases full TT AVDD cost; it supplies no evidence to expand as the noise repair. V25 remains unpromoted, with further corners and formal noise stopped. V26 branches from V20 and tests only smaller N8 coupling devices, retaining its original 0.5 um shunts.

| Device | max abs(Vgs) V | max abs(Vgd) V | max abs(Vds) V |
|---|---:|---:|---:|
| MINP | 0.49161 | 0.49120 | 0.59036 |
| MINN | 0.49160 | 0.49122 | 0.59062 |
| MTAIL | 0.90000 | 0.89844 | 0.56812 |
| MRDP | 0.90000 | 0.89841 | 0.90080 |
| MRDN | 0.90000 | 0.89833 | 0.90082 |
| MLNP | 0.89839 | 0.89841 | 0.89852 |
| MLNN | 0.89845 | 0.89841 | 0.89839 |
| MLPP | 0.90094 | 0.89841 | 0.90091 |
| MLPN | 0.90091 | 0.89841 | 0.90094 |
| MRQP | 0.90000 | 0.90889 | 0.90091 |
| MRQN | 0.90000 | 0.90902 | 0.90094 |
| MOPN | 0.90889 | 0.90924 | 0.90522 |
| MOPP | 0.90091 | 0.90924 | 0.90260 |
| MONN | 0.90902 | 0.90918 | 0.90517 |
| MONP | 0.90094 | 0.90918 | 0.90253 |
| MDQP | 0.90659 | 0.89884 | 0.90889 |
| MDQN | 0.90659 | 0.89870 | 0.90902 |
| MDDP | 0.89494 | 0.00000 | 0.89494 |
| MDDN | 0.89556 | 0.00000 | 0.89556 |
| MCKN | 0.90000 | 0.89425 | 0.90659 |
| MCKP | 0.90000 | 0.89425 | 0.90131 |
| MBLEED | 0.90000 | 0.90131 | 0.90659 |
| MUP | 0.90000 | 0.90659 | 0.90131 |

Archive SHA-256 `c6bd30283dc5a5e6ceba6553e8f3054c64c749063d7947e7d25f16c0017626da` preserves raw data, all error indices, phase signs and the matched V20/V25 comparison; every entry was read back with CRC and SHA-256 verification. The owned remote run is absent. The 102.5 ns duration raises noisefmin to 9.7561 MHz versus the original 287.216 kHz. No formal V25 noise result is claimed. Canonical V19 and every original record remain unchanged.
