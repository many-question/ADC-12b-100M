# RESET-V22: isolate Q reset-shunt width at fixed length

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

V20 retains one wrong polarity at cycle 54 in the matched short noise diagnosis, with only small Q-stage descriptive SNR improvements over V19. V21 then changes Q reset shunts from 0.5 um/30 nm to 0.3 um/100 nm and fails both high-voltage cold stress screens. Its initial prose incorrectly described the predecessor length; [RESET-V21.md](RESET-V21.md) corrects that statement against the actual preserved source and explicitly retains both geometry changes and the failed result. V21 provides no isolated width or noise conclusion.

This experiment branches electrically from V20. Only MDQP/MDQN width changes from 0.5 to 0.4 um; **channel length remains 30 nm and nf remains 1 in both sources**, checked directly from the electrical statements. A successful zero-warning N0.4/30 nm callback supplies the complete geometry and parasitics, SHA-256 `57db486ef0b21a4e4dd1b787480db987b7d06343a1a5bde6750da8925ee45d57`. All other 21 MOS devices and all five MOMs remain identical to V20, including the 5.66049 fF Q capacitors and N4/P2.7 clock inverter.

The 20% width reduction tests a smaller change in physical Q reset strength and loading at fixed length. It still changes drive, capacitance, trajectory and noise together; no isolated channel-noise mechanism is assumed. SF/high/-40 and FS/high/-40 come first because the weaker V21 geometry restores Q overshoot. A useful pass is followed by TT and a matched short phase diagnosis, with reset, complete output validity, full terminal stress and full AVDD cost measured throughout.

Electrical SHA-256: `67137adab331fb3243cb50939afde1e6ff3bb6f733888439348b3dc85380202e`. The [source](RESET-V22.txt) contains 23 MOS and 5 MOMs, with complete RNL checked on a byte-identical mirror. Remaining known corners, actual-worst convergence, electrically identical canonical promotion and original formal tests remain open. Canonical V19 and all genuine original records remain unchanged.

![Physical comparator with fixed-length 0.4 um Q reset shunts](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fc09a938d5e73830ff7ad6e293ca46d66fff2671/design/xtor/adc_comp/many-question-strongarm/reset-v22.png)

## Completed screen 20261031-092126-strongarm-reset-v22-screen

SF/high/-40 fails ten terminal pairs at the strict 1 V limit. FS/high/-40 passes stress. All 72 actual polarities including 10 uV, resets, timing and physical output-validity checks pass, but they do not override the stress failure. This source stops before TT, noise or remaining-corner expansion.

Actual clean source commit: `596782536a7b43a5a893660a926aa339927ea784`. Electrical SHA-256: `67137adab331fb3243cb50939afde1e6ff3bb6f733888439348b3dc85380202e`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 53.844365 / 42.630347 | 20.731105 | 493.566770 | 36 / 36 | 0 | 0 | 0.99723 | 0 / 69 |
| sf_high_m40 | 68.907423 / 52.711981 | 19.170704 | 468.634821 | 36 / 36 | 0 | 0 | 1.00398 | 10 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69912 | 0.76490 |
| MINN | 0.69925 | 0.76512 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99323 | 0.99192 |
| MRDN | 0.99323 | 0.99192 |
| MLNP | 0.99097 | 0.98990 |
| MLNN | 0.99097 | 0.98990 |
| MLPP | 0.99335 | 0.99209 |
| MLPN | 0.99335 | 0.99209 |
| MRQP | 0.99723 | 1.00398 |
| MRQN | 0.99723 | 1.00398 |
| MOPN | 0.99723 | 1.00398 |
| MOPP | 0.99716 | 1.00389 |
| MONN | 0.99723 | 1.00398 |
| MONP | 0.99716 | 1.00389 |
| MDQP | 0.99723 | 1.00398 |
| MDQN | 0.99723 | 1.00398 |
| MDDP | 0.98352 | 0.98520 |
| MDDN | 0.98664 | 0.98767 |
| MCKN | 0.99354 | 0.99599 |
| MCKP | 0.99032 | 0.99000 |
| MBLEED | 0.99354 | 0.99599 |
| MUP | 0.99354 | 0.99599 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


The actual Q-node maxima in the failing SF corner occur during reset after the falling clock edge:

| Node | Peak V | Time ps | Since fall ps | CLKC V | CKB V |
|---|---:|---:|---:|---:|---:|
| QP | 1.003976665176 | 7117.662491322 | 12.662491322 | 0.000000000 | 0.982841557187 |
| QN | 1.003976664095 | 13917.662522523 | 12.662522523 | 0.000000000 | 0.982841557424 |

This test directly verifies a width-only input geometry change at fixed 30 nm length and nf1, including the resulting callback-derived parasitics. The 20% reduction still violates stress. No noise benefit is measured for this failed source. The next experiment branches from V20, retains its Q-shunt strength and changes only the tail device to test the input integration interval.

Full AVDD waveform integrals over the same 36 cycles and 100 ps–14.5 ns window include physical reset and weak-load cost. Every supply probe is present and KCL closes; external ideal clock delivery is outside this boundary:

| Corner | Total fJ/cycle | Evaluation | Reset | Initial reset current uA |
|---|---:|---:|---:|---:|
| fs_high_m40 | 493.567270371 | 99.979133084 | 393.588137287 | 1391.127409624 |
| sf_high_m40 | 468.635438382 | 116.093574983 | 352.541863399 | 1191.081373385 |

Archive SHA-256: `3c6dfdc333d4ca3653664621fbca3e1e11a2d1c8232b917d597cc197f4700d54`. Every member was read back with CRC and SHA-256 verification before local raw duplicates were removed. Power remains reported only; canonical V19 and every genuine result remain unchanged.
