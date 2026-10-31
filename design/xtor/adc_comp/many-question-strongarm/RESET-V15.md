# RESET-V15: release the Q shunts earlier

V14 fails the genuine official TT noise gate at 2094.115400 uV rms. Its short instrumented diagnosis reproduces the broad decision errors at both default and fine numerical settings, with complete reset and stable early-to-final decisions. Q-node differential noise grows during the initial common-mode drop while transfer of the input difference is weak; this supports investigating the release trajectory, without attributing the failure to one device noise source.

This source changes only the CKB MOM from 48 to 16 fingers, nominally 14.06 to 4.46 fF. The smaller clock load is intended to turn the reset-only Q shunts off earlier on a rising CLKC edge, reducing the initial Q-node drop and the interval of weak input coupling. It also changes falling-edge behavior, so terminal stress, reset and output validity must be measured again. The full capacitor geometry exactly reuses a previously callback-validated instance; all MOS dimensions and other electrical statements are unchanged.

Electrical SHA-256: `34e60d7b2afcb0d9a6c3ed8743189c704399b31612824baf26ca7cf621689a44`. The [source](RESET-V15.txt) has 23 MOS and 3 MOM devices, with complete RNL and a byte-identical validation mirror. The canonical V14 source and its recorded failure are preserved.

First screen SF/high/-40 and FS/high/-40 with full-trace terminal voltages, physical decisions and reset. If they pass, check TT timing and a short noise diagnosis early before wider characterization. Promotion and formal qualification require the complete gates; no noise, capacitance or SOA pass is inherited.

![Physical circuit with the smaller clock capacitor](https://raw.githubusercontent.com/many-question/ADC-12b-100M/0a7534091e86e24fff3105bdbf4977eb84bc1bce/design/xtor/adc_comp/many-question-strongarm/reset-v15.png)

## Completed screen 20261031-061543-strongarm-reset-v15-screen

Both mixed high-voltage cold corners pass all terminal pairs, physical validity and timing. All 72 decisions including 10 uV and all 72 resets are correct. This deterministic screen does not establish noise qualification.

Actual clean source commit: `defccc3c3c5dd899b4ef3faeebf23aa15097f670`. Electrical SHA-256: `34e60d7b2afcb0d9a6c3ed8743189c704399b31612824baf26ca7cf621689a44`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fs_high_m40 | 52.220420 / 43.170127 | 21.954303 | 777.869924 | 36 / 36 | 0 | 0 | 0.99794 | 0 / 69 |
| sf_high_m40 | 65.884900 / 53.261265 | 20.064666 | 734.241238 | 36 / 36 | 0 | 0 | 0.99674 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | fs_high_m40 | sf_high_m40 |
|---|---:|---:|
| MINP | 0.68973 | 0.75753 |
| MINN | 0.68983 | 0.75771 |
| MTAIL | 0.99000 | 0.99000 |
| MRDP | 0.99333 | 0.99211 |
| MRDN | 0.99333 | 0.99210 |
| MLNP | 0.99120 | 0.99014 |
| MLNN | 0.99120 | 0.99014 |
| MLPP | 0.99349 | 0.99237 |
| MLPN | 0.99349 | 0.99237 |
| MRQP | 0.99349 | 0.99237 |
| MRQN | 0.99349 | 0.99237 |
| MOPN | 0.99512 | 0.99674 |
| MOPP | 0.99793 | 0.99644 |
| MONN | 0.99512 | 0.99674 |
| MONP | 0.99794 | 0.99644 |
| MDQP | 0.99512 | 0.99673 |
| MDQN | 0.99512 | 0.99673 |
| MDDP | 0.98352 | 0.98519 |
| MDDN | 0.98662 | 0.98767 |
| MCKN | 0.99493 | 0.99616 |
| MCKP | 0.99000 | 0.99000 |
| MBLEED | 0.99493 | 0.99616 |
| MUP | 0.99493 | 0.99616 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Completed screen 20261031-062713-strongarm-reset-v15-screen

TT passes timing, full-trace stress, all 36 decisions including 10 uV and all 36 resets. Saved-current AVDD energy is 570.028171809 fJ/cycle: evaluation 100.982707603 and reset 469.045464205; initial reset current is 2077.522376 uA. Noise remains an independent gate.

Actual clean source commit: `defccc3c3c5dd899b4ef3faeebf23aa15097f670`. Electrical SHA-256: `34e60d7b2afcb0d9a6c3ed8743189c704399b31612824baf26ca7cf621689a44`. The canonical netlist and 274 official result/figure files are unchanged.

| Corner | 1 mV / 30 mV delay (ps) | Reset (ps) | AVDD (fJ/cycle) | Decided / cycles | Wrong | CMP-15 | Max stress (V) | Failed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 59.973740 / 47.870137 | 24.559161 | 570.027526 | 36 / 36 | 0 | 0 | 0.90728 | 0 / 69 |

The entire trace, including clock edges and reset, is checked for every MOS |Vgs|, |Vgd| and |Vds|. Each job uses +aps, no explicit +mt, traponly, maxstep=0.5p, reltol=1e-6 and vabstol=1e-8. The observed batch peak is 1 concurrent jobs; logs report effective single-thread simulation. All raw/deck hashes were verified, and the exact owned remote run was removed with absence confirmed.

Per-device maximum over all three terminal pairs (V):

| Device | tt_nom_27 |
|---|---:|
| MINP | 0.59528 |
| MINN | 0.59535 |
| MTAIL | 0.90000 |
| MRDP | 0.90140 |
| MRDN | 0.90140 |
| MLNP | 0.89902 |
| MLNN | 0.89902 |
| MLPP | 0.90157 |
| MLPN | 0.90157 |
| MRQP | 0.90157 |
| MRQN | 0.90157 |
| MOPN | 0.90505 |
| MOPP | 0.90477 |
| MONN | 0.90505 |
| MONP | 0.90477 |
| MDQP | 0.90728 |
| MDQN | 0.90728 |
| MDDP | 0.89729 |
| MDDN | 0.90043 |
| MCKN | 0.90728 |
| MCKP | 0.90000 |
| MBLEED | 0.90728 |
| MUP | 0.90728 |

Clock charge from the mixed delay sequence is a supplemental diagnostic, not the official CMP-14 input-capacitance result. No all-corner, noise, Monte Carlo or mixed-top qualification is inferred from this screen.

## Matched short noise diagnosis: expansion stopped

Run `20261031-063328-strongarm-reset-v15-noise-numerics-diagnostic-screen` uses clean source `defccc3c3c5dd899b4ef3faeebf23aa15097f670`, the V15 TXT source, and the same physical short diagnostic as the V14 fine control: +/-800 uV, 128 cycles each, 0.5 ps/reltol 1e-6/vabstol 1e-8, 50 GHz, seed 1 and all MOS terminal voltages. The shorter low-frequency cutoff (9.7561 MHz) and added sampling event points remain explicit limitations; this is not a formal sigma measurement.

OUTP-positive counts are 23/128 at -800 uV and 99/128 at +800 uV, versus V14 fine-control 41/128 and 78/128. Thus wrong polarity falls from 91 to 52 of 256 decisions but remains far too common to justify expanded characterization. All 256 reset cycles complete (maximum 23.623146 ps); all late-reset samples are low; no 80 ps/150 ps-to-final sign changes or physical-validity violations occur. All 69 terminal pairs pass, maximum 0.90793 V. At +5 ps QP is about 0.586 V, versus about 0.551 V for V14. At +30 ps Q differential standard deviation falls to 2.505/2.653 mV but still exceeds the small, initially opposite-polarity signal mean -0.227/+0.477 mV.

The observation supports the release-timing direction but does not establish sufficient noise margin or a single-device noise attribution. V15 does not proceed to the remaining seven key corners, formal promotion or Monte Carlo. V16 adjusts the clock-inverter drive ratio while retaining the 4.46 fF damping capacitor.

All raw/deck hashes match; +aps/no explicit +mt/effective single-thread execution and source provenance are retained. The verified archive SHA-256 is `b374d4a5a09afbf7989de284ae44ce88a6b547c3650eaa510c28a2534560e6c8`; the exact owned remote run is removed and absence confirmed. Canonical V14 and its genuine formal failure remain unchanged.
