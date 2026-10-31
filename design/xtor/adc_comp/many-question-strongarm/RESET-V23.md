# RESET-V23: test the input integration interval

The fixed-length Q-shunt width experiment V22 fails ten terminal pairs at SF/high/-40, with a rounded 1.00398 V peak; FS/high/-40 passes. [RESET-V22.md](RESET-V22.md) preserves the actual raw peak, full checks and stopped expansion. V23 therefore branches electrically from V20, restoring its 0.5 um/30 nm Q shunts and retaining all five MOMs and physical clock devices.

StrongARM's own V20 phase evidence shows mean CKB near 74.77 mV at +5 ps and 11.57 mV at +10 ps, staying near 11.4 mV through +30 ps. Input-drain differential means at +20 ps are +2.88739/-2.95272 mV with about 0.712 mV within-level deviation; Q transfer remains small and opposed there. By +30 ps the DP difference has fallen to +2.34277/-2.38852 mV while Q differential transfer develops, and DP reverses sign by +40 ps as the latch takes over. These observations motivate testing the input integration interval. They do not identify a unique device-noise source or justify transferring a Miyahara clock conclusion.

Only MTAIL width changes from 3.0 to 2.4 um, at directly verified **30 nm length and nf3 in both sources**. A successful zero-warning N2.4 callback supplies the full geometry and parasitics, SHA-256 `a7a4e1951d17fc356e11127031f818e63a49ab55052d17b2561b540392255598`. All other 22 MOS devices and all five MOMs are electrically identical to V20. The hypothesis is that a weaker tail can extend input integration before strong regeneration; the actual signal, variance and delay response must be measured. No improvement is presumed from device sizing alone.

Electrical SHA-256: `a3d21ee7163a19a881abc0592038e318efe8ee8fd75977c236608ca5aa711116`. The [source](RESET-V23.txt) contains 23 MOS and 5 MOMs, with complete RNL checked on a byte-identical mirror. SF/FS high/-40 are screened first for stress and validity. TT follows on a useful pass, particularly its 50 ps limit at 30 mV, before a matched short phase diagnosis. Remaining known corners, actual-worst convergence, source-preserving promotion and original formal tests remain open. Canonical V19 and all genuine original records remain unchanged.

![Physical comparator with a 2.4 um tail at fixed length and finger count](https://raw.githubusercontent.com/many-question/ADC-12b-100M/e6c95aadd9ec412bcca1a03d4b1a625321630588/design/xtor/adc_comp/many-question-strongarm/reset-v23.png)

## Completed screen 20261031-093138-strongarm-reset-v23-screen

Both initial high-voltage cold corners pass all 72 actual polarities including 10 uV, resets, timing, output validity and every one of 69 MOS terminal pairs. Their 1 mV delay is about 8–10 ps slower than V20, requiring explicit TT timing verification.

Actual clean source commit: `4ab0c4b642835570163b69007d2b89e49d7d22ff`. Electrical SHA-256: `a3d21ee7163a19a881abc0592038e318efe8ee8fd75977c236608ca5aa711116`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 61.916809 / 49.399174 | 20.977897 | 541.667096 | 36 / 36 | 0 | 0 | 0.99698 | 0 / 69 |
| sf_high_m40 | 78.989037 / 60.787102 | 19.418091 | 511.624700 | 36 / 36 | 0 | 0 | 0.99855 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.68900 | 0.75482 |
| MINN | 0.68920 | 0.75508 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99259 | 0.99000 |
| MRDN | 0.99259 | 0.99000 |
| MLNP | 0.99035 | 0.98794 |
| MLNN | 0.99035 | 0.98794 |
| MLPP | 0.99277 | 0.99014 |
| MLPN | 0.99277 | 0.99014 |
| MRQP | 0.99614 | 0.99834 |
| MRQN | 0.99614 | 0.99834 |
| MOPN | 0.99698 | 0.99855 |
| MOPP | 0.99680 | 0.99833 |
| MONN | 0.99698 | 0.99855 |
| MONP | 0.99680 | 0.99833 |
| MDQP | 0.99698 | 0.99855 |
| MDQN | 0.99698 | 0.99855 |
| MDDP | 0.98352 | 0.98520 |
| MDDN | 0.98664 | 0.98768 |
| MCKN | 0.99345 | 0.99595 |
| MCKP | 0.99031 | 0.99000 |
| MBLEED | 0.99345 | 0.99595 |
| MUP | 0.99345 | 0.99595 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-093657-strongarm-reset-v23-screen

TT fails the 30 mV delay limit: 55.258398 ps exceeds 50 ps. All 36 actual polarities including 10 uV, resets, 1 mV delay, output validity and full terminal-stress checks pass, but do not override that timing failure. V23 stops before noise or further-corner expansion.

Actual clean source commit: `4ab0c4b642835570163b69007d2b89e49d7d22ff`. Electrical SHA-256: `a3d21ee7163a19a881abc0592038e318efe8ee8fd75977c236608ca5aa711116`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 71.198518 / 55.258398 | 23.598070 | 406.442194 | 36 / 36 | 0 | 0 | 0.90751 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.59124 |
| MINN | 0.59137 |
| MTAIL | 0.90000 |
| MRDP | 0.90000 |
| MRDN | 0.90046 |
| MLNP | 0.89689 |
| MLNN | 0.89689 |
| MLPP | 0.89942 |
| MLPN | 0.89942 |
| MRQP | 0.90751 |
| MRQN | 0.90751 |
| MOPN | 0.90751 |
| MOPP | 0.90735 |
| MONN | 0.90751 |
| MONP | 0.90735 |
| MDQP | 0.90751 |
| MDQN | 0.90751 |
| MDDP | 0.89731 |
| MDDN | 0.90046 |
| MCKN | 0.90609 |
| MCKP | 0.90065 |
| MBLEED | 0.90609 |
| MUP | 0.90609 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.


### Preserved deterministic transfer comparison

The existing V20 TT trace and this V23 TT trace use the same stimulus hash and numerical settings. Four actual cycles at +/-1 mV are sampled relative to each rising 50% clock crossing. The old raw archive and each raw waveform SHA-256 were verified before analysis; no new simulation or sample selection is involved. These two-level deterministic secant gains are not noise or linear gain through regeneration.

| Phase ps | V20 DP gain | V23 DP gain | V20 Q gain | V23 Q gain |
|---:|---:|---:|---:|---:|
| 10 | -1.355423833 | -1.013702829 | 0.080094233 | 0.059378048 |
| 20 | -3.599349594 | -3.136590632 | 0.163422076 | 0.178537204 |
| 25 | -3.869390832 | -3.785101197 | -0.363399967 | 0.093241091 |
| 30 | -2.934937183 | -3.775858005 | -2.311971290 | -0.610727829 |
| 35 | -1.206968744 | -2.858953642 | -5.625441239 | -2.454590191 |
| 40 | 1.087504057 | -1.367445581 | -10.780334766 | -5.318655430 |
| 50 | 9.810445380 | 3.128898803 | -49.425881877 | -16.825466487 |

TT 30 mV delay increases by 7.396064282 ps. The source is not expanded to a noise measurement after failing timing. The next experiment branches from V20, retains its original tail drive, and changes only the input-to-Q NMOS pair.

Full TT AVDD energy is 406.442585969 fJ/cycle = 90.409899018 evaluation + 316.032686951 reset over the same 36 cycles and 100 ps–14.5 ns window. Initial reset current is 1174.503967847 uA. Every supply probe is present and KCL closes. Physical reset/weak-load costs are included, external ideal clock delivery excluded, and power remains reported only.

- `20261031-093138-strongarm-reset-v23-screen` archive SHA-256: `ab4204a4193050205801bd7e3695f751badba995949e0d1c82c16f51dba00000`.
- `20261031-093657-strongarm-reset-v23-screen` archive SHA-256: `76f2f2c30256bd4253c807910e714f47042f63c77c415cf76cb518bd8ec5dc58`.

Every archive member was read back with CRC and SHA-256 verification before local raw duplicates were removed. Canonical V19 and every original result remain unchanged.
