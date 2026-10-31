# RESET-V16: change the clock-inverter drive ratio

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

V15 reduces wrong polarity in the matched short noise diagnosis from V14 fine-control 91/256 to 52/256 at +/-800 uV, but this is still a gross error rate and does not support wider qualification. At +5 ps after the clock midpoint QP remains near 0.586 V; Q differential noise still grows while signal transfer is weak. Complete reset and stable 80 ps-to-final signs persist. This is diagnostic evidence, not a new official noise estimate.

This experiment changes only MCKN N2 to N4 and MCKP P4 to P3, retaining the 4.46 fF CKB capacitor and every other electrical statement. The stronger pull-down and shifted inverter trip point are intended to release the Q shunts before Q precharge is lost. The smaller PMOS also limits the added input clock-gate load. Both full geometries exactly reuse validated devices already in V15. Clock capacitance and falling-edge stress must be remeasured; neither is assumed to pass.

Electrical SHA-256: `ef4549caa57c005bae663d6473866eea5da81db4db57dbabb4f0f4acb814d4c9`. The [source](RESET-V16.txt) retains 23 MOS and 3 MOM devices and complete RNL, checked through a byte-identical mirror. Canonical V14 and all V14/V15 failures remain preserved. First screen SF/high/-40 and FS/high/-40, then TT timing and short noise if those pass. No expanded corners or formal qualification is claimed at source freeze.

![Physical circuit with revised clock inverter](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0a7534091e86e24fff3105bdbf4977eb84bc1bce/design/xtor/adc_comp/many-question-strongarm/reset-v16.png)

## Completed screen 20261031-064414-strongarm-reset-v16-screen

This deterministic screen passes every actual polarity including 10 uV, every reset, timing, physical output validity and all 69 MOS terminal pairs. Short noise diagnosis remains a separate gate.

Actual clean source commit: `80e84b1414b1fbed8ee68a97a4330ca337a9e64a`. Electrical SHA-256: `ef4549caa57c005bae663d6473866eea5da81db4db57dbabb4f0f4acb814d4c9`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 51.875232 / 42.628118 | 21.880119 | 768.319267 | 36 / 36 | 0 | 0 | 0.99701 | 0 / 69 |
| sf_high_m40 | 65.650216 / 52.772215 | 19.988842 | 723.454392 | 36 / 36 | 0 | 0 | 0.99863 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.69271 | 0.75980 |
| MINN | 0.69283 | 0.76000 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99333 | 0.99211 |
| MRDN | 0.99333 | 0.99211 |
| MLNP | 0.99117 | 0.99013 |
| MLNN | 0.99117 | 0.99013 |
| MLPP | 0.99349 | 0.99237 |
| MLPN | 0.99349 | 0.99237 |
| MRQP | 0.99349 | 0.99236 |
| MRQN | 0.99349 | 0.99237 |
| MOPN | 0.99701 | 0.99863 |
| MOPP | 0.99689 | 0.99836 |
| MONN | 0.99701 | 0.99863 |
| MONP | 0.99689 | 0.99836 |
| MDQP | 0.99701 | 0.99863 |
| MDQN | 0.99701 | 0.99863 |
| MDDP | 0.98352 | 0.98519 |
| MDDN | 0.98663 | 0.98767 |
| MCKN | 0.99393 | 0.99626 |
| MCKP | 0.99059 | 0.99000 |
| MBLEED | 0.99393 | 0.99626 |
| MUP | 0.99393 | 0.99626 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-065210-strongarm-reset-v16-screen

This deterministic screen passes every actual polarity including 10 uV, every reset, timing, physical output validity and all 69 MOS terminal pairs. Short noise diagnosis remains a separate gate.

Actual clean source commit: `80e84b1414b1fbed8ee68a97a4330ca337a9e64a`. Electrical SHA-256: `ef4549caa57c005bae663d6473866eea5da81db4db57dbabb4f0f4acb814d4c9`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 59.697582 / 47.483058 | 24.395669 | 563.307007 | 36 / 36 | 0 | 0 | 0.90705 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.59751 |
| MINN | 0.59759 |
| MTAIL | 0.90000 |
| MRDP | 0.90140 |
| MRDN | 0.90140 |
| MLNP | 0.89901 |
| MLNN | 0.89901 |
| MLPP | 0.90157 |
| MLPN | 0.90157 |
| MRQP | 0.90323 |
| MRQN | 0.90323 |
| MOPN | 0.90705 |
| MOPP | 0.90676 |
| MONN | 0.90705 |
| MONP | 0.90676 |
| MDQP | 0.90705 |
| MDQN | 0.90705 |
| MDDP | 0.89729 |
| MDDN | 0.90043 |
| MCKN | 0.90640 |
| MCKP | 0.90085 |
| MBLEED | 0.90640 |
| MUP | 0.90640 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Matched short noise diagnosis: reject expansion

Run `20261031-065637-strongarm-reset-v16-noise-numerics-diagnostic-screen` uses the same clean source `80e84b1414b1fbed8ee68a97a4330ca337a9e64a`, physical 23-MOS circuit, +/-800 uV x 128 decisions, 50 GHz bandwidth, seed 1, traponly and 0.5 ps / 1e-6 / 1e-8 settings as the previous fine diagnosis. No formal record is written.

| Source | OUTP count at -800 uV | OUTP count at +800 uV | Wrong / 256 |
|---|---:|---:|---:|
| V14 fine control | 41 / 128 | 78 / 128 | 91 |
| V15 | 23 / 128 | 99 / 128 | 52 |
| V16 | 6 / 128 | 121 / 128 | 13 |

All 256 resets pass (maximum 23.584084455 ps), with zero early-80-ps/mid-150-ps to final sign changes, zero late reset failures, zero output-validity violations and all 69 terminal pairs passing (maximum 0.90735 V). The release improvement is real in the measured trajectory: QP at +5 ps is about 0.649 V versus V15's 0.586 V, and +30 ps Q differential standard deviation falls to 1.341/1.523 mV from 2.505/2.653 mV. The remaining 13 wrong decisions are still gross at these inputs, so no remaining-corner, promotion, official-noise or Monte Carlo expansion is justified. This supports the release-region mechanism; it does not isolate a device's noise contribution.

The shortened duration raises the effective low noise frequency to 9.7561 MHz versus the official 287.216 kHz, and the added samplers introduce event time points. These two-level diagnostic counts do not replace the official 17 x 512 probit estimate. Full raw/deck/source hashes, reset traces and MOS stress are retained in the verified archive `7ea4f1a8db40873f2943cd539380c3df4fdfa480e820b891deb68adebd862b75`; the exact owned remote run is absent.

The TT deterministic current integral is 563.307481184 fJ/cycle = 95.327309523 evaluation + 467.980171661 reset, with initial reset current 2072.978454 uA. All probes are present and the supply-sum residual is zero. Mixed-sequence clock charge implies 15.909314 fF, close to the 16 fF gate; this diagnostic is not the formal capacitance measurement. No power limit is inferred.
