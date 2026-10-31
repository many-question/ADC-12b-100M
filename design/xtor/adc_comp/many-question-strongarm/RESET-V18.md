# RESET-V18: physical Q-node capacitance

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

V17 passes all 72 polarities/resets and output-validity checks in its first two corners, but SF/high/-40 reaches 1.001079522 V at Q during reset, about 11.653 ps after the clock falling midpoint. CKB is already 0.98355 V and CLKC is zero, so the weak shunt is on at the failing peak. Ten terminal pairs fail. The FS corner passes at 0.99735 V. V17 therefore stops before TT, noise or broader qualification.

This experiment adds only CQP/CQN, each a physical 4.46 fF MOM from QP/QN to VSS, copying the exact validated CCB geometry. All 23 MOS, the N0.5 reset shunts, clock controls, and three existing capacitors are unchanged. The added capacitance tests whether storing the coupled edge charge can reduce the reset peak and release droop without restoring the large shunt current. It also loads regeneration and reset; the TT 30 mV delay limit remains 50 ps and must be rechecked. No stress or noise benefit is assumed.

Electrical SHA-256: `eba5b9f0cb2409b69dc660dd433da7ec13ca3a809c4de9d2817602a51b21d11c`. The [source](RESET-V18.txt) contains 23 MOS and 5 MOM devices, with complete RNL checked through a byte-identical mirror. First screen SF/high/-40 and FS/high/-40. TT speed and matched short noise follow only after these pass; wider qualification remains gated. Canonical V14 and all prior failures stay preserved.

![Comparator with matched Q-node MOM capacitors](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0a7534091e86e24fff3105bdbf4977eb84bc1bce/design/xtor/adc_comp/many-question-strongarm/reset-v18.png)

## Completed screen 20261031-071527-strongarm-reset-v18-screen

All actual polarities including 10 uV, resets, timing, physical output-validity checks and all 69 MOS terminal pairs pass in this deterministic screen. Mixed-sequence clock capacitance remains supplemental.

Actual clean source commit: `7587fc32a0cb72d740fcf4e7078bf28490d7037a`. Electrical SHA-256: `eba5b9f0cb2409b69dc660dd433da7ec13ca3a809c4de9d2817602a51b21d11c`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 53.102266 / 42.295124 | 20.883160 | 540.299536 | 36 / 36 | 0 | 0 | 0.99671 | 0 / 69 |
| sf_high_m40 | 67.919090 / 52.475171 | 19.271956 | 509.691887 | 36 / 36 | 0 | 0 | 0.99878 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69815 | 0.76415 |
| MINN | 0.69828 | 0.76435 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99325 | 0.99197 |
| MRDN | 0.99325 | 0.99196 |
| MLNP | 0.99101 | 0.98994 |
| MLNN | 0.99101 | 0.98994 |
| MLPP | 0.99338 | 0.99215 |
| MLPN | 0.99338 | 0.99215 |
| MRQP | 0.99517 | 0.99878 |
| MRQN | 0.99517 | 0.99878 |
| MOPN | 0.99671 | 0.99878 |
| MOPP | 0.99653 | 0.99874 |
| MONN | 0.99671 | 0.99878 |
| MONP | 0.99653 | 0.99874 |
| MDQP | 0.99671 | 0.99878 |
| MDQN | 0.99671 | 0.99878 |
| MDDP | 0.98352 | 0.98520 |
| MDDN | 0.98664 | 0.98767 |
| MCKN | 0.99441 | 0.99657 |
| MCKP | 0.99061 | 0.99000 |
| MBLEED | 0.99441 | 0.99657 |
| MUP | 0.99441 | 0.99657 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-072204-strongarm-reset-v18-screen

All actual polarities including 10 uV, resets, timing, physical output-validity checks and all 69 MOS terminal pairs pass in this deterministic screen. Mixed-sequence clock capacitance remains supplemental.

Actual clean source commit: `7587fc32a0cb72d740fcf4e7078bf28490d7037a`. Electrical SHA-256: `eba5b9f0cb2409b69dc660dd433da7ec13ca3a809c4de9d2817602a51b21d11c`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 61.343944 / 47.475090 | 23.445657 | 405.325821 | 36 / 36 | 0 | 0 | 0.90691 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.60132 |
| MINN | 0.60143 |
| MTAIL | 0.90000 |
| MRDP | 0.90128 |
| MRDN | 0.90128 |
| MLNP | 0.89886 |
| MLNN | 0.89886 |
| MLPP | 0.90139 |
| MLPN | 0.90139 |
| MRQP | 0.90672 |
| MRQN | 0.90672 |
| MOPN | 0.90691 |
| MOPP | 0.90666 |
| MONN | 0.90691 |
| MONP | 0.90666 |
| MDQP | 0.90691 |
| MDQN | 0.90691 |
| MDDP | 0.89730 |
| MDDN | 0.90045 |
| MCKN | 0.90684 |
| MCKP | 0.90093 |
| MBLEED | 0.90684 |
| MUP | 0.90684 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Matched short noise diagnosis

Run `20261031-072644-strongarm-reset-v18-noise-numerics-diagnostic-screen` uses clean source `7587fc32a0cb72d740fcf4e7078bf28490d7037a`, the same +/-800 uV x 128 sequence, 50 GHz bandwidth, seed 1, traponly and 0.5 ps / 1e-6 / 1e-8 settings as the earlier fine diagnostics. OUTP counts are 0/128 at -800 uV and 128/128 at +800 uV: **0/256 wrong polarities**, compared with 13/256 for V16. All 256 resets pass, maximum 22.614674056 ps; there are no early-80-ps or mid-150-ps to final sign changes, late-reset errors, output-validity violations or failed MOS terminal pairs. Maximum stress is 0.90760 V.

QP at rising midpoint +5 ps is now about 0.8032 V, versus V16's 0.6489 V. At +30 ps the Q differential mean is +1.713/-1.796 mV for negative/positive input, now the correct polarity; its standard deviation is 0.822/0.952 mV. Relative to V16 both the smaller shunts and Q capacitors changed, so the noise improvement is not assigned to either device change alone. The V17-to-V18 deterministic stress comparison separately changes only the capacitors.

The shorter record has a 9.7561 MHz low noise frequency, versus the official 287.216 kHz, and extra sampling events. Zero errors at two extreme input levels does not establish a 200 uV rms noise value or replace the official 17 x 512 fit. Archive `7321759cd55ce0faa4c97204cb0763a5b10f5595fdc7ff3b4eda5118ad422a3a` retains the full physical waveform and source/deck hashes; the owned remote run is absent.

TT mixed-sequence clock capacitance is **16.037833 fF**, slightly above the 16 fF formal gate. The stimuli differ from the official capacitance test, so this is not a formal failure record, but it does not justify expansion of a marginal clock load. V18 remains private; V19 changes only MCKP to reduce that load before wider validation.
