# Supplemental characterization

The following historical private experiments keep their original energy definitions. Merged spec v0.6.0 changed the official mixed-sequence meter and removed its energy acceptance limit; these private results are not relabeled as new CMP-10 evidence. See [REFRESH.md](REFRESH.md).

These are private exploration runs using frozen netlist copies and the standard excitation and 10 fF loads. They are not official acceptance records. Every completed variant, including failures, is retained here. Each noise pilot uses 17 levels, 64 decisions per level, seed 1 and a 50 GHz bandwidth. Fine transient checks use 0.5 ps maximum step (unless a smaller step is listed), traponly, reltol = 1e-6 and vabstol = 1e-8. Noise pilots retain the standard numerical settings. Unless explicitly labeled as a fixed-1mV probe, energy uses the mixed-amplitude delay sequence and the 14.5 ns window-average power multiplied by 400 ps; see [issue #75](https://github.com/many-question/ADC-12b-100M/issues/75).

| Variant / corner | Test | Result |
|---|---|---|
| b0 / tt_nom_27 | delay (fine) | 1 mV 44.93 ps; 30 mV 34.52 ps; reset 22.99 ps; energy 124.59 fJ; wrong 0; SOA violations 0 / 57; max 0.9553 V; simultaneous high points 0 |
| b0 / tt_nom_27 | noise | noise 255.79 uV (95% CI 230.99–284.01); offset -0.0184 mV; weak decisions 0 |
| b0 / tt_nom_27 | kickback (fine) | Cin 16.412 fF; CLKC 5.063 fF; kickback 0.000 uV |
| d0c2 / tt_nom_27 | delay (fine) | 1 mV 52.91 ps; 30 mV 39.73 ps; reset 18.50 ps; energy 138.95 fJ; wrong 0; SOA violations 0 / 45; max 0.9447 V; simultaneous high points 0 |
| d0c2 / tt_nom_27 | kickback (fine) | Cin 16.413 fF; CLKC 12.787 fF; kickback 0.000 uV |
| d0c2 / tt_nom_27 | noise | noise 258.23 uV (95% CI 233.06–286.84); offset 0.0209 mV; weak decisions 0 |
| d0t2c2 / tt_nom_27 | delay (fine) | 1 mV 81.76 ps; 30 mV 62.05 ps; reset 18.31 ps; energy 137.63 fJ; wrong 0; SOA violations 0 / 45; max 0.9447 V; simultaneous high points 0 |
| d0t2c2 / tt_nom_27 | kickback (fine) | Cin 16.602 fF; CLKC 10.969 fF; kickback 0.000 uV |
| d0t2c2 / tt_nom_27 | noise | noise 244.62 uV (95% CI 220.50–272.08); offset -0.0124 mV; weak decisions 0 |
| s12t3c1 / tt_nom_27 | delay (fine) | 1 mV 54.74 ps; 30 mV 42.62 ps; reset 22.39 ps; energy 140.61 fJ; wrong 0; SOA violations 0 / 45; max 0.9749 V; simultaneous high points 0 |
| s12t3c1 / tt_nom_27 | noise | noise 221.23 uV (95% CI 198.40–247.28); offset -0.0006 mV; weak decisions 0 |
| s12t3c2 / tt_nom_27 | delay (fine) | 1 mV 63.28 ps; 30 mV 49.44 ps; reset 23.97 ps; energy 161.39 fJ; wrong 0; SOA violations 0 / 45; max 0.9676 V; simultaneous high points 0 |
| s12t3c2 / tt_nom_27 | noise | noise 206.63 uV (95% CI 184.63–231.82); offset -0.0083 mV; weak decisions 0 |
| s4t3c2 / tt_nom_27 | delay (fine) | 1 mV 59.73 ps; 30 mV 45.77 ps; reset 20.24 ps; energy 141.59 fJ; wrong 0; SOA violations 0 / 45; max 0.9422 V; simultaneous high points 0 |
| s4t3c2 / tt_nom_27 | noise | noise 234.48 uV (95% CI 210.87–261.37); offset 0.0016 mV; weak decisions 0 |
| hvtn-c14 / tt_nom_27 | delay (fine) | 1 mV 63.41 ps; 30 mV 46.79 ps; reset 17.71 ps; energy 118.12 fJ; wrong 0; SOA violations 0 / 45; max 0.9459 V; simultaneous high points 0 |
| hvtn-c14 / tt_nom_27 | noise | noise 260.03 uV (95% CI 234.78–288.74); offset -0.0155 mV; weak decisions 0 |
| svtn-c0 / tt_nom_27 | delay (fine) | 1 mV 47.13 ps; 30 mV 34.33 ps; reset 17.35 ps; energy 96.73 fJ; wrong 0; SOA violations 0 / 45; max 0.9541 V; simultaneous high points 0 |
| svtn-c0 / tt_nom_27 | noise | noise 301.23 uV (95% CI 273.31–333.07); offset 0.0112 mV; weak decisions 0 |
| svtn-c14 / ff_high_125 | delay (fine) | 1 mV 40.57 ps; 30 mV 30.55 ps; reset 16.53 ps; energy 199.63 fJ; wrong 0; SOA violations 8 / 45; max 1.0367 V; simultaneous high points 0 |
| svtn-c14 / tt_nom_27 | delay (fine) | 1 mV 57.27 ps; 30 mV 42.84 ps; reset 18.38 ps; energy 118.83 fJ; wrong 0; SOA violations 0 / 45; max 0.9476 V; simultaneous high points 0 |
| svtn-c14 / tt_nom_27 | noise | noise 261.44 uV (95% CI 236.16–290.19); offset 0.0070 mV; weak decisions 0 |
| svtnp-c14 / tt_nom_27 | delay (fine) | 1 mV 59.72 ps; 30 mV 43.01 ps; reset 18.42 ps; energy 122.37 fJ; wrong 0; SOA violations 0 / 45; max 0.9519 V; simultaneous high points 0 |
| svtnp-c14 / tt_nom_27 | noise | noise 262.53 uV (95% CI 237.17–291.36); offset -0.0005 mV; weak decisions 0 |
| k56t3c2 / ff_high_125 | delay (fine) | 1 mV 47.09 ps; 30 mV 36.82 ps; reset 20.63 ps; energy 358.66 fJ; wrong 0; SOA violations 8 / 57; max 1.0374 V; simultaneous high points 0 |
| k56t3c2 / ss_low_125 | delay (fine) | 1 mV 86.03 ps; 30 mV 66.78 ps; reset 32.37 ps; energy 180.02 fJ; wrong 0; SOA violations 0 / 57; max 0.8514 V; simultaneous high points 0 |
| k56t3c2 / tt_nom_27 | delay (fine) | 1 mV 65.85 ps; 30 mV 51.31 ps; reset 23.70 ps; energy 195.26 fJ; wrong 0; SOA violations 0 / 57; max 0.9512 V; simultaneous high points 0 |
| k56t3c2 / tt_nom_27 | kickback (fine) | Cin 19.312 fF; CLKC 13.192 fF; kickback 0.000 uV |
| k56t3c2 / tt_nom_27 | noise | noise 158.97 uV (95% CI 139.61–181.53); offset 0.0021 mV; weak decisions 0 |
| s56t3c2 / ff_high_125 | delay (fine) | 1 mV 45.97 ps; 30 mV 35.94 ps; reset 21.35 ps; energy 288.28 fJ; wrong 0; SOA violations 8 / 45; max 1.0506 V; simultaneous high points 0 |
| s56t3c2 / ss_low_125 | delay (fine) | 1 mV 85.06 ps; 30 mV 66.20 ps; reset 34.27 ps; energy 158.42 fJ; wrong 0; SOA violations 0 / 45; max 0.8628 V; simultaneous high points 0 |
| s56t3c2 / tt_nom_27 | delay (fine) | 1 mV 65.04 ps; 30 mV 50.87 ps; reset 24.82 ps; energy 170.20 fJ; wrong 0; SOA violations 0 / 45; max 0.9656 V; simultaneous high points 0 |
| s56t3c2 / tt_nom_27 | kickback (fine) | Cin 19.312 fF; CLKC 11.841 fF; kickback 0.000 uV |
| s56t3c2 / tt_nom_27 | noise | noise 195.27 uV (95% CI 173.93–219.80); offset -0.0126 mV; weak decisions 0 |
| l16t3c1 / ff_high_125 | delay (fine) | 1 mV 48.07 ps; 30 mV 36.62 ps; reset 18.60 ps; energy 388.51 fJ; wrong 0; SOA violations 6 / 57; max 1.0459 V; simultaneous high points 0 |
| l16t3c1 / ff_high_m40 | delay (fine) | 1 mV 47.83 ps; 30 mV 36.74 ps; reset 16.89 ps; energy 237.61 fJ; wrong 0; SOA violations 32 / 57; max 1.0862 V; simultaneous high points 0 |
| l16t3c1 / ss_low_125 | delay (fine) | 1 mV 80.65 ps; 30 mV 61.27 ps; reset 28.70 ps; energy 183.18 fJ; wrong 0; SOA violations 0 / 57; max 0.8807 V; simultaneous high points 0 |
| l16t3c1 / tt_nom_27 | delay (fine) | 1 mV 62.35 ps; 30 mV 47.75 ps; reset 21.78 ps; energy 203.44 fJ; wrong 0; SOA violations 0 / 57; max 0.9884 V; simultaneous high points 0 |
| l16t3c1 / tt_nom_27 | kickback (fine) | Cin 19.312 fF; CLKC 7.257 fF; kickback 0.000 uV |
| l16t3c1 / tt_nom_27 | noise | noise 144.57 uV (95% CI 126.30–166.01); offset 0.0186 mV; weak decisions 0 |
| l24t3c1 / ff_high_125 | delay (fine) | 1 mV 51.27 ps; 30 mV 38.76 ps; reset 18.48 ps; energy 419.20 fJ; wrong 0; SOA violations 6 / 57; max 1.0421 V; simultaneous high points 0 |
| l24t3c1 / ff_high_m40 | delay (fine) | 1 mV 50.60 ps; 30 mV 38.51 ps; reset 16.98 ps; energy 258.03 fJ; wrong 0; SOA violations 29 / 57; max 1.0911 V; simultaneous high points 0 |
| l24t3c1 / ss_low_125 | delay (fine) | 1 mV 84.62 ps; 30 mV 63.83 ps; reset 28.93 ps; energy 196.06 fJ; wrong 0; SOA violations 0 / 57; max 0.8800 V; simultaneous high points 0 |
| l24t3c1 / tt_nom_27 | delay (fine) | 1 mV 65.60 ps; 30 mV 49.89 ps; reset 21.93 ps; energy 219.60 fJ; wrong 0; SOA violations 0 / 57; max 0.9912 V; simultaneous high points 0 |
| l24t3c1 / tt_nom_27 | kickback (fine) | Cin 19.312 fF; CLKC 7.244 fF; kickback 0.000 uV |
| l24t3c1 / tt_nom_27 | noise | noise 146.28 uV (95% CI 127.82–167.92); offset 0.0136 mV; weak decisions 0 |
| p56t3c1 / ff_high_125 | delay (fine) | 1 mV 43.63 ps; 30 mV 33.40 ps; reset 24.03 ps; energy 351.70 fJ; wrong 0; SOA violations 8 / 69; max 1.0208 V; simultaneous high points 0 |
| p56t3c1 / ff_high_m40 | delay (fine) | 1 mV 44.03 ps; 30 mV 34.36 ps; reset 21.19 ps; energy 217.54 fJ; wrong 0; SOA violations 21 / 69; max 1.0538 V; simultaneous high points 0 |
| p56t3c1 / ss_low_125 | delay (fine) | 1 mV 75.63 ps; 30 mV 57.97 ps; reset 38.44 ps; energy 173.52 fJ; wrong 0; SOA violations 0 / 69; max 0.8405 V; simultaneous high points 0 |
| p56t3c1 / tt_nom_27 | delay (fine) | 1 mV 58.12 ps; 30 mV 44.99 ps; reset 27.90 ps; energy 189.38 fJ; wrong 0; SOA violations 0 / 69; max 0.9482 V; simultaneous high points 0 |
| p56t3c1 / tt_nom_27 | kickback (fine) | Cin 19.313 fF; CLKC 15.151 fF; kickback 0.000 uV |
| p56t3c1 / tt_nom_27 | noise | noise 199.11 uV (95% CI 177.35–224.05); offset 0.0316 mV; weak decisions 0 |
| p56t3c1 / ff_high_m40 / maxstep 0.25p | delay (fine) | 1 mV 44.03 ps; 30 mV 34.36 ps; reset 21.16 ps; energy 217.55 fJ; wrong 0; SOA violations 21 / 69; max 1.0538 V; simultaneous high points 0 |
| p56t3c1 / tt_nom_27 / fixed |vd| = 1 mV, 36-cycle meter window | delay (fine) | energy 188.069 fJ; wrong 0; SOA violations 0 / 69; max 0.9435 V |

Variant notation: `b0` uses 48 um / 30 nm input devices; `b1` uses 48 um / 60 nm. Prefix `d` instead of `b` removes the four-MOS local clock buffer and drives the core directly from CLKC. The default tail width is 4 um; `t3`, `t2` and `t1` use 3 um, 2 um and 1 um. Prefix `g` uses clock-precharged output sensing nodes (a failed experiment with invalid fast-corner outputs). Prefix `u` removes the output buffers, directly loads the core with 10 fF per output and uses 2 um M8/M9. Prefix `v` additionally enlarges M8/M9 to 4 um and reduces input-drain precharge PMOS to 2 um; this fails slow-corner reset. Prefix `r` instead keeps 2 um M8/M9, uses 6 um input-drain precharge PMOS controlled by a two-inverter delayed clock, and adds two 4 um output-reset NMOS controlled by the inverted clock. Its tail remains driven directly by CLKC. Prefix `q` further changes the first clock inverter NMOS to 1 um and the second inverter NMOS to 8 um. Miyahara `w0` and `w56` split input precharge into 4 um delayed-clock and 2 um direct-clock PMOS in parallel, use a 4 um first clock NMOS, and have 48 or 56 um input devices. `x56` instead uses 3 um first-clock and 2 um output-reset NMOS, and adds 4.46051 fF nominal MOM capacitors to CKB and CKR. StrongARM prefixes `s4` and `s12` set the regenerative NMOS pair to 4 um or 12 um; the corresponding PMOS widths are 4 um and 8 um. StrongARM `svtn`, `svtnp` and `hvtn` use, respectively, SVT NMOS, SVT NMOS/PMOS, and HVT NMOS in the regenerative pair, with 4 um regenerative devices and a 3 um tail. Their `c14` suffix is 14.06 fF per input drain and `c0` adds no capacitor. StrongARM `s56` uses 56 um input NMOS, a 12 um / 8 um regenerative pair and direct clocking; `k56` adds a two-inverter delay on the input-drain precharge PMOS gates and enlarges the directly clocked output-node precharge PMOS to 4 um. StrongARM `l16` and `l24` use 16 or 24 um output precharge PMOS driven by the same delayed clock as input precharge, with 56 um inputs. StrongARM `p56` uses 56 um inputs, series 4/6 um input-drain precharge, parallel 2/4 um output precharge, direct/delayed clock controls, and 4.46051 fF nominal MOM capacitors on CKB and CKD. Suffixes `c1`, `c2`, `c4`, `c6` add a PDK MOM device from each input drain to ground, with nominal callback values 14.06, 27.42, 54.12 and 80.83 fF per side. The modeled device geometry, rather than an ideal capacitance, is simulated.

| Frozen netlist variant | SHA-256 |
|---|---|
| b0 | `56f176b60569c4e57a56b844e00cdef84e607e26878972df4fd8f6795fb4878a` |
| d0c2 | `0cc4d00d2e78e338930f65e94b82b46ba66be3c16649f0741d1132d34acb6bb1` |
| d0t2c2 | `b4c296fc5193f428c3337d0e90ed377b4c3983b96f7484755fd8092e63c6232b` |
| s12t3c1 | `94a6f645530a56b7c0692a651be9fe074782be6e71ef0858e020cda258d46510` |
| s12t3c2 | `126725589f3ec9ecb3cc7fb3fd5a602de213dd5ac746d02bb09b0dba977b5530` |
| s4t3c2 | `59e249f838c9a19495c52f41987191f25cbe099a15f9e2f59165215bd86f8996` |
| hvtn-c14 | `5e24ae8b9d2765d622f4acc3b815318b8bb04a27f74ec8594662ce52bac7ce69` |
| svtn-c0 | `1e675218ee9749e070c4337e4b21c451807943aebb21b76556d334c35736f349` |
| svtn-c14 | `c33d1832bbe7973745af37c87cbf8e54828ad902d9c0983d91d7e31f7353cdfc` |
| svtnp-c14 | `18c220ae0574500ab49d33789976bdccfa79e8cef5df805baf08d55ad3908da9` |
| k56t3c2 | `9970de2947f743af91ace1cd1142f1dbfbe6d639ab49c89d0d46a39ad3f293da` |
| s56t3c2 | `1c9baa1cb1badec0ab0390c23dc9d4d5d3fb20306cac47be8c7e265dd9434be4` |
| l16t3c1 | `4c1417fb771024fc1c4568a2d0a1329d7031567df7edeccf5b4a9c34afaef44f` |
| l24t3c1 | `a03a5aaff519b70ecec5f1e4312c2cfa9dc89a375f9bf05c6a64187117677d33` |
| p56t3c1 | `1b6c812a2dbdcdaef57b727194822dc179fbd934b519d932a3586225ebc74ff5` |

A lower energy number is not a qualified comparison unless the same noise, timing, reset, input-load, kickback and SOA requirements are met. The table is exploratory evidence only; see the candidate README and repository results for the separately frozen formal run status.
