# RESET-V19: reduce clock-gate load

V18 passes SF/high/-40, FS/high/-40 and TT timing, reset, output validity and all 69 MOS terminal pairs. The two Q MOMs reduce the previously failing reset peak to 0.99878 V. TT 1/30 mV delay is 61.343944/47.475090 ps. Its matched short fine-step diagnosis records 0/256 wrong polarities at +/-800 uV (OUTP counts 0/128 and 128/128). This remains a short diagnostic with a different low noise frequency, not an official noise estimate.

V18's TT mixed-sequence CLK charge gives 16.037833 fF, slightly above the 16 fF gate. The mixed sequence is not the official capacitance test, but it provides insufficient confidence to expand a marginal clock load. This source changes only MCKP from 3.0 um to 2.7 um at 30 nm, retaining three fingers, N4 clock pull-down, both N0.5 Q shunts and all five MOMs. The new callback succeeds without warnings; all terminal parasitics come from its result, SHA-256 `4c95992b12488f02b405cc506443cde9dc0bb5750de45d19aff81a133bffa2e5`. No other electrical statement changes.

The smaller PMOS should reduce external clock-gate charge but may delay shunt turn-on and restore reset overshoot. SF/high/-40 and FS/high/-40 therefore come first, followed by TT and the matched noise diagnosis only if those pass. Electrical SHA-256: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. The [source](RESET-V19.txt) contains 23 MOS and 5 MOMs, with complete RNL checked on a byte-identical mirror. Canonical V14 and all older evidence remain preserved. Formal capacitance, noise and qualification do not transfer.

![Physical comparator with smaller clock PMOS](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fc09a938d5e73830ff7ad6e293ca46d66fff2671/design/xtor/adc_comp/many-question-strongarm/reset-v19.png)

## Completed screen 20261031-073542-strongarm-reset-v19-screen

Both first stress corners pass every timing, reset, output-validity and terminal-stress gate. All 72 actual polarities, including 10 uV, and all 72 resets pass the independent waveform audit.

Actual clean source commit: `0b026e2487d815e377ff0de99e28ad3a38a039ab`. Electrical SHA-256: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 53.107302 / 42.294168 | 20.867012 | 539.540167 | 36 / 36 | 0 | 0 | 0.99709 | 0 / 69 |
| sf_high_m40 | 67.927064 / 52.467425 | 19.288777 | 508.991202 | 36 / 36 | 0 | 0 | 0.99882 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69823 | 0.76421 |
| MINN | 0.69835 | 0.76441 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99325 | 0.99197 |
| MRDN | 0.99325 | 0.99196 |
| MLNP | 0.99100 | 0.98994 |
| MLNN | 0.99100 | 0.98994 |
| MLPP | 0.99338 | 0.99215 |
| MLPN | 0.99338 | 0.99215 |
| MRQP | 0.99622 | 0.99882 |
| MRQN | 0.99622 | 0.99882 |
| MOPN | 0.99709 | 0.99882 |
| MOPP | 0.99692 | 0.99879 |
| MONN | 0.99709 | 0.99882 |
| MONP | 0.99692 | 0.99879 |
| MDQP | 0.99709 | 0.99882 |
| MDQN | 0.99709 | 0.99882 |
| MDDP | 0.98352 | 0.98520 |
| MDDN | 0.98664 | 0.98767 |
| MCKN | 0.99345 | 0.99595 |
| MCKP | 0.99031 | 0.99000 |
| MBLEED | 0.99345 | 0.99595 |
| MUP | 0.99345 | 0.99595 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-074310-strongarm-reset-v19-screen

TT passes all timing, reset, validity and full-trace stress gates, with all 36 actual polarities and resets independently audited. The mixed CLK charge diagnostic falls to 15.783664 fF; official capacitance and noise remain unestablished for this source.

Actual clean source commit: `0b026e2487d815e377ff0de99e28ad3a38a039ab`. Electrical SHA-256: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 61.345488 / 47.472377 | 23.498218 | 404.753296 | 36 / 36 | 0 | 0 | 0.90758 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.60139 |
| MINN | 0.60147 |
| MTAIL | 0.90000 |
| MRDP | 0.90128 |
| MRDN | 0.90128 |
| MLNP | 0.89886 |
| MLNN | 0.89886 |
| MLPP | 0.90139 |
| MLPN | 0.90139 |
| MRQP | 0.90758 |
| MRQN | 0.90758 |
| MOPN | 0.90758 |
| MOPP | 0.90742 |
| MONN | 0.90758 |
| MONP | 0.90742 |
| MDQP | 0.90758 |
| MDQN | 0.90758 |
| MDDP | 0.89730 |
| MDDN | 0.90045 |
| MCKN | 0.90609 |
| MCKP | 0.90065 |
| MBLEED | 0.90609 |
| MUP | 0.90609 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Matched short physical noise diagnosis

Run `20261031-074942-strongarm-reset-v19-noise-numerics-diagnostic-screen` uses actual clean source `70e17c44051c89446c32d2ba22235a8884181ac5` with the same physical V19 source, fine 0.5 ps integration, reltol=1e-6, vabstol=1e-8, 50 GHz bandwidth and seed 1. It records OUTP counts 1/128 at -800 uV and 128/128 at +800 uV: one wrong polarity in 256 decisions. That error is retained. V18 had zero in the matched short sample; these small two-level counts do not establish either a formal sigma or a statistically isolated clock-device effect.

All 256 resets complete, maximum 22.618032995 ps. There are zero early (+80 ps) or middle (+150 ps) to final sign changes, late-reset violations and physical output-validity violations. All 69 MOS terminal pairs pass over the full trace, maximum 0.90821 V. At rise +30 ps QP-QN means are +1.758495/-1.754884 mV, with standard deviations 0.983277/0.929692 mV; at +40 ps the means are +8.649103/-8.818842 mV and standard deviations 2.767018/2.527898 mV. This retains useful signal transfer but does not establish the 200 uV requirement.

The 102.5 ns duration raises noisefmin to 9.7561 MHz, compared with 287.216 kHz in the original full test, and the read-only samplers add time points. All original formal files remain unchanged. Raw/deck hashes and the private archive are verified; the exact owned remote directory is absent. The other known deterministic corners and actual-worst convergence are next prerequisites before canonical promotion and the unchanged original formal capacitance/noise tests.

| Device | Maximum terminal stress (V) |
|---|---:|
| MINP | 0.59064 |
| MINN | 0.59092 |
| MTAIL | 0.90000 |
| MRDP | 0.90134 |
| MRDN | 0.90137 |
| MLNP | 0.89915 |
| MLNN | 0.89909 |
| MLPP | 0.90163 |
| MLPN | 0.90163 |
| MRQP | 0.90786 |
| MRQN | 0.90800 |
| MOPN | 0.90821 |
| MOPP | 0.90821 |
| MONN | 0.90816 |
| MONP | 0.90816 |
| MDQP | 0.90786 |
| MDQN | 0.90800 |
| MDDP | 0.89535 |
| MDDN | 0.89599 |
| MCKN | 0.90667 |
| MCKP | 0.90133 |
| MBLEED | 0.90667 |
| MUP | 0.90667 |

## Completed screen 20261031-075638-strongarm-reset-v19-screen

All seven additional known corners pass the deterministic timing, reset, physical output-validity and full MOS stress gates. The independent waveform audit confirms all 252 actual polarities, including 10 uV, and all 252 resets. Across all ten known corners, all 360 decisions and resets pass; the largest stress remains SF/high/-40 at 0.99882 V.

Actual clean source commit: `325690f67de2dfd6454da5a6c4e0ec59006ab7af`. Electrical SHA-256: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_125 | 48.180396 / 36.894109 | 20.268147 | 667.848346 | 36 / 36 | 0 | 0 | 0.99147 | 0 / 69 |
| ff_high_m40 | 46.050334 / 36.251640 | 17.814561 | 568.932057 | 36 / 36 | 0 | 0 | 0.99692 | 0 / 69 |
| fs_low_125 | 62.667902 / 48.710937 | 28.813280 | 353.228924 | 36 / 36 | 0 | 0 | 0.81343 | 0 / 69 |
| sf_high_125 | 60.705373 / 46.444895 | 22.252943 | 562.637091 | 36 / 36 | 0 | 0 | 0.99681 | 0 / 69 |
| sf_high_27 | 62.465857 / 48.140579 | 20.421396 | 514.061352 | 36 / 36 | 0 | 0 | 0.99811 | 0 / 69 |
| sf_low_m40 | 85.273131 / 64.927800 | 23.477504 | 279.412611 | 36 / 36 | 0 | 0 | 0.82092 | 0 / 69 |
| ss_low_125 | 81.995016 / 62.392235 | 32.620883 | 298.394573 | 36 / 36 | 0 | 0 | 0.81903 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 4 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | ff_high_125 | ff_high_m40 | fs_low_125 | sf_high_125 | sf_high_27 | sf_low_m40 | ss_low_125 |
|---|---:|---:|---:|---:|---:|---:|---:|
| MINP | 0.57378 | 0.69263 | 0.53146 | 0.64692 | 0.71622 | 0.59705 | 0.53543 |
| MINN | 0.57384 | 0.69277 | 0.53146 | 0.64699 | 0.71637 | 0.59719 | 0.53542 |
| MTAIL | 0.99000 | 0.99000 | 0.81000 | 0.99000 | 0.99000 | 0.81000 | 0.81000 |
| MRDP | 0.99000 | 0.99212 | 0.81000 | 0.99000 | 0.99000 | 0.81146 | 0.81000 |
| MRDN | 0.99000 | 0.99212 | 0.81126 | 0.99000 | 0.99000 | 0.81318 | 0.81082 |
| MLNP | 0.96024 | 0.99004 | 0.79453 | 0.97465 | 0.98784 | 0.80946 | 0.80148 |
| MLNN | 0.96024 | 0.99004 | 0.79452 | 0.97465 | 0.98783 | 0.80947 | 0.80146 |
| MLPP | 0.96537 | 0.99227 | 0.80114 | 0.97547 | 0.98978 | 0.81166 | 0.80476 |
| MLPN | 0.96537 | 0.99227 | 0.80114 | 0.97547 | 0.98978 | 0.81166 | 0.80476 |
| MRQP | 0.99000 | 0.99540 | 0.81343 | 0.99628 | 0.99805 | 0.82092 | 0.81903 |
| MRQN | 0.99000 | 0.99540 | 0.81343 | 0.99628 | 0.99805 | 0.82092 | 0.81903 |
| MOPN | 0.99147 | 0.99692 | 0.81343 | 0.99681 | 0.99811 | 0.82092 | 0.81903 |
| MOPP | 0.98937 | 0.99674 | 0.81292 | 0.99495 | 0.99784 | 0.82082 | 0.81841 |
| MONN | 0.99147 | 0.99692 | 0.81343 | 0.99681 | 0.99811 | 0.82092 | 0.81903 |
| MONP | 0.98937 | 0.99674 | 0.81292 | 0.99495 | 0.99784 | 0.82082 | 0.81841 |
| MDQP | 0.99147 | 0.99692 | 0.81343 | 0.99681 | 0.99811 | 0.82092 | 0.81903 |
| MDQN | 0.99147 | 0.99692 | 0.81343 | 0.99681 | 0.99811 | 0.82092 | 0.81903 |
| MDDP | 0.98512 | 0.98477 | 0.80744 | 0.98628 | 0.98559 | 0.81030 | 0.80754 |
| MDDN | 0.98841 | 0.98768 | 0.81126 | 0.98850 | 0.98823 | 0.81318 | 0.81082 |
| MCKN | 0.99000 | 0.99367 | 0.81000 | 0.99383 | 0.99589 | 0.82082 | 0.81632 |
| MCKP | 0.99000 | 0.99000 | 0.81326 | 0.99000 | 0.99000 | 0.81196 | 0.81334 |
| MBLEED | 0.99000 | 0.99367 | 0.81326 | 0.99383 | 0.99589 | 0.82082 | 0.81632 |
| MUP | 0.99000 | 0.99367 | 0.81326 | 0.99383 | 0.99589 | 0.82082 | 0.81632 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-080710-strongarm-reset-v19-screen

The targeted 0.125 ps, reltol=1e-7, vabstol=1e-9 repeat at the actual worst stress corner passes all 36 polarities and resets, physical validity and every one of the 69 terminal pairs. The maximum stress remains 0.99882 V.

Actual clean source commit: `325690f67de2dfd6454da5a6c4e0ec59006ab7af`. Electrical SHA-256: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sf_high_m40 | 67.933414 / 52.468467 | 19.215253 | 509.009601 | 36 / 36 | 0 | 0 | 0.99882 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.125p, reltol=1e-7 and vabstol=1e-9. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | sf_high_m40 |
|---|---:|
| MINP | 0.76420 |
| MINN | 0.76441 |
| MTAIL | 0.99000 |
| MRDP | 0.99197 |
| MRDN | 0.99197 |
| MLNP | 0.98995 |
| MLNN | 0.98995 |
| MLPP | 0.99216 |
| MLPN | 0.99216 |
| MRQP | 0.99882 |
| MRQN | 0.99882 |
| MOPN | 0.99882 |
| MOPP | 0.99879 |
| MONN | 0.99882 |
| MONP | 0.99879 |
| MDQP | 0.99882 |
| MDQN | 0.99882 |
| MDDP | 0.98519 |
| MDDN | 0.98767 |
| MCKN | 0.99595 |
| MCKP | 0.99000 |
| MBLEED | 0.99595 |
| MUP | 0.99595 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Convergence and promotion prerequisites

All ten known key corners pass all 360 actual polarities, 360 resets, physical output validity and full-trace stress. The actual worst SF/high/-40 repeat retains a 0.99882 V maximum. Across all 69 terminal pairs, the largest absolute change in the peak table is 20.000 uV, with table resolution 10 uV. Tight minus reference changes are +0.006349740 ps at 1 mV, +0.001042041 ps at 30 mV, -0.073523978 ps reset, +0.004108392 ps regeneration time constant and +0.018398952 fJ/cycle. The complete raw/deck and diagnostic evidence is SHA-archived and each owned remote run is absent.

These results establish the known deterministic prerequisites for an electrically identical canonical promotion. The 1/256 short noise error remains recorded (cycle 54); no formal noise pass is inferred. The original full TT capacitance/kickback and, if it passes, original 17 x 512 TT noise test must supply genuine new-source results. Remaining-corner stress, all formal coverage, mismatch, operating-range and mixed-top qualification remain open.
