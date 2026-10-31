# RESET-V21: test weaker Q reset shunts

V20 passes the first SF/FS high/-40 and TT deterministic screens, but its matched short noise diagnosis retains the same one wrong polarity at cycle 54 as V19. At +30/+40 ps the descriptive Q differential SNR improves only about 3.16%/1.18%, with both signal and variation changing. This does not establish enough benefit to solve V19's genuine 218.770059 uV TT noise failure. [RESET-V20.md](RESET-V20.md) preserves the measured cost and phase evidence; V20 remains an unpromoted experiment.

In the independent StrongARM phase evidence, input-drain discrimination is already present at +20 ps while Q differential transfer remains small and initially opposed. The Q reset/load release trajectory remains a testable sensitivity. This experiment changes only the two physical Q reset shunts MDQP/MDQN from 0.5 um/30 nm to 0.3 um/100 nm, with one finger in both versions. Both width and length change, so this is not an isolated width test. It tests how lower shunt drive/loading changes Q initialization and release, rather than increasing the capacitors again. The result may also change clock loading, bias trajectory and device noise; no isolated channel-noise cause is assumed.

The new N0.3 callback succeeds with zero warnings; its complete geometry and terminal parasitics are used, SHA-256 `dff23b2714ce7c9d7cd5ceece462347b619b63183c1d6b00179932e71b6fc62d`. All other 21 MOS devices and all five MOMs remain electrically identical to V20, including the two 5.66049 fF Q capacitors and N4/P2.7 physical clock devices. Reduced shunt strength may restore Q voltage overshoot; the two known high-voltage cold corners therefore come first. Reset, output validity, full terminal stress and complete AVDD costs must be measured along with the phase response.

Electrical SHA-256: `51e0735f2471b3edbfc79f641438d016320d096a689b9e45bd7265661944a90e`. The [source](RESET-V21.txt) contains 23 MOS and 5 MOMs, with complete RNL checked on a byte-identical mirror. After the first stress corners, TT and a matched short phase diagnosis determine whether broader known-corner coverage and actual-worst convergence are useful. Original formal capacitance and noise gates require an electrically identical frozen canonical promotion; no private result substitutes for them. Canonical V19 and all original results remain unchanged.

![Physical comparator with weaker Q reset shunts](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fc09a938d5e73830ff7ad6e293ca46d66fff2671/design/xtor/adc_comp/many-question-strongarm/reset-v21.png)

## Completed screen 20261031-091145-strongarm-reset-v21-screen

Both initial high-voltage cold corners fail ten terminal pairs. All 72 actual polarities including 10 uV, resets, timing and physical output-validity checks pass, but they do not override the strict 1 V stress failure. This source stops before TT, noise or remaining-corner expansion.

Actual clean source commit: `e0d2bf5b82470606ba2f624e65b4081f87ac5e22`. Electrical SHA-256: `51e0735f2471b3edbfc79f641438d016320d096a689b9e45bd7265661944a90e`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 54.157715 / 42.728953 | 20.131131 | 375.218096 | 36 / 36 | 0 | 0 | 1.01890 | 10 / 69 |
| sf_high_m40 | 69.304909 / 52.429676 | 18.687909 | 369.123283 | 36 / 36 | 0 | 0 | 1.02020 | 10 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.70077 | 0.76609 |
| MINN | 0.70089 | 0.76629 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99323 | 0.99191 |
| MRDN | 0.99323 | 0.99191 |
| MLNP | 0.99097 | 0.98988 |
| MLNN | 0.99097 | 0.98988 |
| MLPP | 0.99334 | 0.99207 |
| MLPN | 0.99334 | 0.99207 |
| MRQP | 1.01890 | 1.02020 |
| MRQN | 1.01890 | 1.02020 |
| MOPN | 1.01890 | 1.02020 |
| MOPP | 1.01880 | 1.02002 |
| MONN | 1.01890 | 1.02020 |
| MONP | 1.01880 | 1.02002 |
| MDQP | 1.01890 | 1.02020 |
| MDQN | 1.01890 | 1.02020 |
| MDDP | 0.98353 | 0.98520 |
| MDDN | 0.98665 | 0.98768 |
| MCKN | 0.99330 | 0.99588 |
| MCKP | 0.99032 | 0.99000 |
| MBLEED | 0.99330 | 0.99588 |
| MUP | 0.99330 | 0.99588 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


### Geometry-description correction and raw failure

The initial prose incorrectly described the predecessor as having 100 nm channel length. The preserved V20 and V21 electrical source statements, callback and run hashes establish the actual change: **0.5 um/30 nm to 0.3 um/100 nm**. The source used for the simulation is unchanged. The drawing already shows the actual V21 geometry. This correction prevents attributing the result to width alone; no result, run metadata or source hash has been rewritten.

Raw Q-node maxima occur during reset after the falling clock edge. Both nearest 50% clock-crossing offsets are retained:

| Corner | Node | Peak V | Time ps | Since nearest rise ps | Since fall ps | CLKC V | CKB V |
|---|---|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | QP | 1.018903296972 | 7121.801333719 | -183.198666281 | 16.801333719 | 0.000000000 | 0.980515422179 |
| fs_high_m40 | QN | 1.018903396412 | 5921.872205242 | -183.127794758 | 16.872205242 | 0.000000000 | 0.980514363194 |
| sf_high_m40 | QP | 1.020197206911 | 14318.951989890 | 213.951989890 | 13.951989890 | 0.000000000 | 0.982796435931 |
| sf_high_m40 | QN | 1.020197172376 | 13918.951535184 | -186.048464816 | 13.951535184 | 0.000000000 | 0.982796442740 |

The next experiment branches from V20 and retains 30 nm length, reducing only width from 0.5 to 0.4 um with complete callback-derived parasitics. This smaller, explicitly checked change tests width sensitivity. The V21 stress failure provides no noise result for that different source.

Full AVDD waveform integrals over the same 36 cycles and 100 ps–14.5 ns boundary retain physical reset and weak-load cost. All supply probes are present and KCL closes. External ideal clock delivery remains outside this boundary:

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 375.218672122 | 98.879172867 | 276.339499254 | 768.851926667 |
| sf_high_m40 | 369.123940019 | 114.501277685 | 254.622662334 | 676.812746736 |

Archive SHA-256: `9c2afdb1d1ea0a0cfe10318c8ec05c9c9598384ae7715107ef6e2026f26cee6b`. Every member was read back with CRC and SHA-256 verification before local raw duplicates were removed. Reduced AVDD cost in this failed source is not a qualified efficiency result. Canonical V19 and all original records remain unchanged.
