# Supplemental characterization

These are private exploration runs using frozen netlist copies and the standard excitation and 10 fF loads. They are not official acceptance records. Every completed variant, including failures, is retained here. Each noise pilot uses 17 levels, 64 decisions per level, seed 1 and a 50 GHz bandwidth. Fine transient checks use 0.5 ps maximum step (unless a smaller step is listed), traponly, reltol = 1e-6 and vabstol = 1e-8. Noise pilots retain the standard numerical settings.

| Variant / corner | Test | Result |
|---|---|---|
| b0 / tt_nom_27 | delay (fine) | 1 mV 41.89 ps; 30 mV 35.33 ps; reset 33.66 ps; energy 138.19 fJ; wrong 0; SOA violations 0 / 81; max 0.9764 V; simultaneous high points 0 |
| b0 / tt_nom_27 | noise | noise 237.44 uV (95% CI 213.43–264.76); offset -0.0058 mV; weak decisions 0 |
| b0c2 / tt_nom_27 | delay (fine) | 1 mV 53.71 ps; 30 mV 46.15 ps; reset 39.25 ps; energy 185.76 fJ; wrong 0; SOA violations 0 / 81; max 0.9676 V; simultaneous high points 0 |
| b0c2 / tt_nom_27 | noise | noise 215.17 uV (95% CI 192.35–241.22); offset -0.0075 mV; weak decisions 0 |
| b0 / tt_nom_27 | kickback (fine) | Cin 16.412 fF; CLKC 5.063 fF; kickback 0.000 uV |
| d0c2 / tt_nom_27 | delay (fine) | 1 mV 47.32 ps; 30 mV 39.77 ps; reset 33.42 ps; energy 159.51 fJ; wrong 0; SOA violations 0 / 69; max 0.9677 V; simultaneous high points 0 |
| d0c2 / tt_nom_27 | kickback (fine) | Cin 16.413 fF; CLKC 9.790 fF; kickback 0.000 uV |
| d0c2 / tt_nom_27 | noise | noise 200.04 uV (95% CI 178.21–225.05); offset 0.0437 mV; weak decisions 0 |
| d0t2c2 / tt_nom_27 | delay (fine) | 1 mV 70.49 ps; 30 mV 60.19 ps; reset 33.13 ps; energy 164.10 fJ; wrong 0; SOA violations 0 / 69; max 0.9677 V; simultaneous high points 0 |
| d0t2c2 / tt_nom_27 | kickback (fine) | Cin 16.602 fF; CLKC 8.068 fF; kickback 0.000 uV |
| d0t2c2 / tt_nom_27 | noise | noise 168.91 uV (95% CI 148.75–192.25); offset 0.0134 mV; weak decisions 0 |
| d0t3c2 / ff_high_125 | delay (fine) | 1 mV 42.74 ps; 30 mV 34.80 ps; reset 28.04 ps; energy 294.45 fJ; wrong 0; SOA violations 12 / 69; max 1.0623 V; simultaneous high points 0 |
| d0t3c2 / ss_low_125 | delay (fine) | 1 mV 74.42 ps; 30 mV 62.62 ps; reset 47.34 ps; energy 151.04 fJ; wrong 0; SOA violations 0 / 69; max 0.8687 V; simultaneous high points 0 |
| d0t3c2 / tt_nom_27 | delay (fine) | 1 mV 55.14 ps; 30 mV 46.75 ps; reset 33.36 ps; energy 161.01 fJ; wrong 0; SOA violations 0 / 69; max 0.9677 V; simultaneous high points 0 |
| d0t3c2 / tt_nom_27 | kickback (fine) | Cin 16.524 fF; CLKC 8.994 fF; kickback 0.000 uV |
| d0t3c2 / tt_nom_27 | noise | noise 197.52 uV (95% CI 175.93–222.29); offset 0.0381 mV; weak decisions 0 |
| g0t3c2 / ff_high_125 | delay (fine) | 1 mV 38.22 ps; 30 mV 33.13 ps; reset 11.26 ps; energy 388.68 fJ; wrong 0; SOA violations 16 / 69; max 1.0757 V; simultaneous high points 7240 |
| g0t3c2 / ss_low_125 | delay (fine) | 1 mV 72.01 ps; 30 mV 62.14 ps; reset 17.07 ps; energy 168.16 fJ; wrong 0; SOA violations 0 / 69; max 0.8852 V; simultaneous high points 0 |
| g0t3c2 / tt_nom_27 | delay (fine) | 1 mV 53.76 ps; 30 mV 46.52 ps; reset 12.97 ps; energy 183.60 fJ; wrong 0; SOA violations 0 / 69; max 0.9845 V; simultaneous high points 0 |
| g0t3c2 / tt_nom_27 | kickback (fine) | Cin 16.524 fF; CLKC 15.071 fF; kickback 0.000 uV |
| g0t3c2 / tt_nom_27 | noise | noise 197.11 uV (95% CI 175.38–222.04); offset 0.0193 mV; weak decisions 3 |
| u0c2 / tt_nom_27 | delay (fine) | 1 mV 43.27 ps; 30 mV 35.01 ps; reset 27.33 ps; energy 152.61 fJ; wrong 0; SOA violations 0 / 45; max 0.9173 V; simultaneous high points 0 |
| u0c2 / tt_nom_27 | noise | noise 186.28 uV (95% CI 165.29–210.45); offset -0.0124 mV; weak decisions 0 |
| u0t3c1 / tt_nom_27 | delay (fine) | 1 mV 43.73 ps; 30 mV 35.46 ps; reset 24.50 ps; energy 130.28 fJ; wrong 0; SOA violations 0 / 45; max 0.9226 V; simultaneous high points 0 |
| u0t3c1 / tt_nom_27 | noise | noise 192.11 uV (95% CI 170.76–216.65); offset -0.0088 mV; weak decisions 0 |
| u0t3c2 / ff_high_125 | delay (fine) | 1 mV 41.03 ps; 30 mV 31.54 ps; reset 22.54 ps; energy 255.72 fJ; wrong 0; SOA violations 6 / 45; max 1.0059 V; simultaneous high points 0 |
| u0t3c2 / ss_low_125 | delay (fine) | 1 mV 71.12 ps; 30 mV 56.73 ps; reset 39.06 ps; energy 144.61 fJ; wrong 0; SOA violations 0 / 45; max 0.8243 V; simultaneous high points 0 |
| u0t3c2 / tt_nom_27 | delay (fine) | 1 mV 51.76 ps; 30 mV 42.33 ps; reset 27.36 ps; energy 154.22 fJ; wrong 0; SOA violations 0 / 45; max 0.9178 V; simultaneous high points 0 |
| u0t3c2 / tt_nom_27 | kickback (fine) | Cin 16.524 fF; CLKC 8.991 fF; kickback 0.000 uV |
| u0t3c2 / tt_nom_27 | noise | noise 176.57 uV (95% CI 156.10–200.20); offset -0.0085 mV; weak decisions 0 |
| v0t3c1 / ff_high_125 | delay (fine) | 1 mV 39.62 ps; 30 mV 29.78 ps; reset 27.55 ps; energy 255.91 fJ; wrong 0; SOA violations 6 / 45; max 1.0006 V; simultaneous high points 0 |
| v0t3c1 / ss_low_125 | delay (fine) | 1 mV 62.42 ps; 30 mV 48.30 ps; reset 46.78 ps; energy 126.65 fJ; wrong 0; SOA violations 0 / 45; max 0.8202 V; simultaneous high points 0 |
| v0t3c1 / tt_nom_27 | delay (fine) | 1 mV 45.03 ps; 30 mV 36.15 ps; reset 32.68 ps; energy 135.96 fJ; wrong 0; SOA violations 0 / 45; max 0.9126 V; simultaneous high points 0 |
| v0t3c1 / tt_nom_27 | kickback (fine) | Cin 16.526 fF; CLKC 5.638 fF; kickback 0.000 uV |
| v0t3c1 / tt_nom_27 | noise | noise 193.50 uV (95% CI 172.02–218.15); offset 0.0017 mV; weak decisions 0 |
| v0t3c2 / ff_high_125 | delay (fine) | 1 mV 44.99 ps; 30 mV 34.33 ps; reset 30.68 ps; energy 287.02 fJ; wrong 0; SOA violations 0 / 45; max 0.9988 V; simultaneous high points 0 |
| v0t3c2 / ss_low_125 | delay (fine) | 1 mV 74.04 ps; 30 mV 58.28 ps; reset 54.00 ps; energy 152.09 fJ; wrong 0; SOA violations 0 / 45; max 0.8175 V; simultaneous high points 0 |
| v0t3c2 / tt_nom_27 | delay (fine) | 1 mV 53.37 ps; 30 mV 43.23 ps; reset 37.32 ps; energy 161.53 fJ; wrong 0; SOA violations 0 / 45; max 0.9097 V; simultaneous high points 0 |
| v0t3c2 / tt_nom_27 | kickback (fine) | Cin 16.526 fF; CLKC 5.609 fF; kickback 0.000 uV |
| v0t3c2 / tt_nom_27 | noise | noise 186.07 uV (95% CI 165.05–210.27); offset -0.0085 mV; weak decisions 0 |
| r0t3c1 / ff_high_125 | delay (fine) | 1 mV 40.83 ps; 30 mV 31.42 ps; reset 12.03 ps; energy 360.62 fJ; wrong 0; SOA violations 0 / 63; max 0.9999 V; simultaneous high points 0 |
| r0t3c1 / ss_low_125 | delay (fine) | 1 mV 65.12 ps; 30 mV 51.13 ps; reset 18.03 ps; energy 168.05 fJ; wrong 0; SOA violations 0 / 63; max 0.8375 V; simultaneous high points 0 |
| r0t3c1 / tt_nom_27 | delay (fine) | 1 mV 47.80 ps; 30 mV 38.90 ps; reset 13.82 ps; energy 185.22 fJ; wrong 0; SOA violations 0 / 63; max 0.9259 V; simultaneous high points 0 |
| r0t3c1 / tt_nom_27 | kickback (fine) | Cin 16.523 fF; CLKC 10.707 fF; kickback 0.000 uV |
| r0t3c1 / tt_nom_27 | noise | noise 181.41 uV (95% CI 160.64–205.36); offset -0.0314 mV; weak decisions 0 |
| r0t3c2 / ff_high_125 | delay (fine) | 1 mV 45.47 ps; 30 mV 35.27 ps; reset 12.55 ps; energy 387.42 fJ; wrong 0; SOA violations 0 / 63; max 0.9999 V; simultaneous high points 0 |
| r0t3c2 / ss_low_125 | delay (fine) | 1 mV 75.91 ps; 30 mV 60.50 ps; reset 18.93 ps; energy 193.33 fJ; wrong 0; SOA violations 0 / 63; max 0.8361 V; simultaneous high points 0 |
| r0t3c2 / tt_nom_27 | delay (fine) | 1 mV 55.57 ps; 30 mV 45.54 ps; reset 14.51 ps; energy 211.03 fJ; wrong 0; SOA violations 0 / 63; max 0.9254 V; simultaneous high points 0 |
| r0t3c2 / tt_nom_27 | kickback (fine) | Cin 16.523 fF; CLKC 10.687 fF; kickback 0.000 uV |
| r0t3c2 / tt_nom_27 | noise | noise 170.37 uV (95% CI 150.29–193.65); offset -0.0229 mV; weak decisions 0 |
| q0t3c1 / ff_high_125 | delay (fine) | 1 mV 48.22 ps; 30 mV 38.74 ps; reset 11.21 ps; energy 410.84 fJ; wrong 0; SOA violations 6 / 63; max 1.0004 V; simultaneous high points 0 |
| q0t3c1 / ff_high_27 | delay (fine) | 1 mV 43.43 ps; 30 mV 36.44 ps; reset 10.64 ps; energy 284.52 fJ; wrong 0; SOA violations 11 / 63; max 1.0028 V; simultaneous high points 0 |
| q0t3c1 / ff_high_m40 | delay (fine) | 1 mV 42.29 ps; 30 mV 35.90 ps; reset 10.16 ps; energy 243.80 fJ; wrong 0; SOA violations 13 / 63; max 1.0096 V; simultaneous high points 0 |
| q0t3c1 / ss_low_125 | delay (fine) | 1 mV 73.35 ps; 30 mV 59.32 ps; reset 17.11 ps; energy 182.79 fJ; wrong 0; SOA violations 0 / 63; max 0.8320 V; simultaneous high points 0 |
| q0t3c1 / tt_nom_27 | delay (fine) | 1 mV 54.51 ps; 30 mV 45.58 ps; reset 13.15 ps; energy 202.11 fJ; wrong 0; SOA violations 0 / 63; max 0.9235 V; simultaneous high points 0 |
| q0t3c1 / tt_nom_27 | kickback (fine) | Cin 16.523 fF; CLKC 9.875 fF; kickback 0.000 uV |
| q0t3c1 / tt_nom_27 | noise | noise 206.63 uV (95% CI 184.71–231.71); offset -0.0105 mV; weak decisions 0 |
| r0t3c1 / ff_high_m40 | delay (fine) | 1 mV 36.55 ps; 30 mV 30.18 ps; reset 10.74 ps; energy 219.89 fJ; wrong 0; SOA violations 29 / 63; max 1.0121 V; simultaneous high points 0 |
| w0t3c1 / ff_high_125 | delay (fine) | 1 mV 38.57 ps; 30 mV 29.21 ps; reset 11.19 ps; energy 352.49 fJ; wrong 0; SOA violations 2 / 69; max 1.0129 V; simultaneous high points 0 |
| w0t3c1 / ff_high_m40 | delay (fine) | 1 mV 34.60 ps; 30 mV 28.28 ps; reset 9.94 ps; energy 208.01 fJ; wrong 0; SOA violations 28 / 69; max 1.0304 V; simultaneous high points 0 |
| w0t3c1 / ss_low_125 | delay (fine) | 1 mV 63.12 ps; 30 mV 49.17 ps; reset 16.52 ps; energy 160.83 fJ; wrong 0; SOA violations 0 / 69; max 0.8379 V; simultaneous high points 0 |
| w0t3c1 / tt_nom_27 | delay (fine) | 1 mV 45.85 ps; 30 mV 37.00 ps; reset 12.65 ps; energy 175.62 fJ; wrong 0; SOA violations 0 / 69; max 0.9339 V; simultaneous high points 0 |
| w0t3c1 / tt_nom_27 | kickback (fine) | Cin 16.523 fF; CLKC 15.769 fF; kickback 0.000 uV |
| w0t3c1 / tt_nom_27 | noise | noise 192.50 uV (95% CI 170.93–217.27); offset 0.0297 mV; weak decisions 0 |
| w56t3c1 / ff_high_125 | delay (fine) | 1 mV 40.50 ps; 30 mV 30.71 ps; reset 11.58 ps; energy 368.48 fJ; wrong 0; SOA violations 4 / 69; max 1.0160 V; simultaneous high points 0 |
| w56t3c1 / ff_high_m40 | delay (fine) | 1 mV 36.26 ps; 30 mV 29.70 ps; reset 10.29 ps; energy 220.55 fJ; wrong 0; SOA violations 28 / 69; max 1.0306 V; simultaneous high points 0 |
| w56t3c1 / ss_low_125 | delay (fine) | 1 mV 65.83 ps; 30 mV 51.50 ps; reset 17.01 ps; energy 170.80 fJ; wrong 0; SOA violations 0 / 69; max 0.8378 V; simultaneous high points 0 |
| w56t3c1 / tt_nom_27 | delay (fine) | 1 mV 47.82 ps; 30 mV 38.73 ps; reset 13.02 ps; energy 186.49 fJ; wrong 0; SOA violations 0 / 69; max 0.9341 V; simultaneous high points 0 |
| w56t3c1 / tt_nom_27 | kickback (fine) | Cin 19.311 fF; CLKC 15.759 fF; kickback 0.000 uV |
| w56t3c1 / tt_nom_27 | noise | noise 185.09 uV (95% CI 163.99–209.37); offset 0.0293 mV; weak decisions 0 |
| x56t3c1 / ff_high_125 | delay (fine) | 1 mV 40.26 ps; 30 mV 30.78 ps; reset 14.85 ps; energy 356.36 fJ; wrong 0; SOA violations 3 / 69; max 1.0049 V; simultaneous high points 0 |
| x56t3c1 / ff_high_m40 | delay (fine) | 1 mV 36.22 ps; 30 mV 29.78 ps; reset 13.11 ps; energy 217.17 fJ; wrong 0; SOA violations 28 / 69; max 1.0160 V; simultaneous high points 0 |
| x56t3c1 / ss_low_125 | delay (fine) | 1 mV 65.26 ps; 30 mV 51.38 ps; reset 23.55 ps; energy 171.94 fJ; wrong 0; SOA violations 0 / 69; max 0.8333 V; simultaneous high points 0 |
| x56t3c1 / tt_nom_27 | delay (fine) | 1 mV 47.61 ps; 30 mV 38.75 ps; reset 17.31 ps; energy 186.34 fJ; wrong 0; SOA violations 0 / 69; max 0.9215 V; simultaneous high points 0 |
| x56t3c1 / tt_nom_27 | kickback (fine) | Cin 19.311 fF; CLKC 14.924 fF; kickback 0.000 uV |
| x56t3c1 / tt_nom_27 | noise | noise 184.95 uV (95% CI 164.10–208.97); offset 0.0169 mV; weak decisions 0 |
| x56t3c1 / ff_high_m40 / maxstep 0.25p | delay (fine) | 1 mV 36.22 ps; 30 mV 29.78 ps; reset 13.11 ps; energy 217.18 fJ; wrong 0; SOA violations 28 / 69; max 1.0160 V; simultaneous high points 0 |

Variant notation: `b0` uses 48 um / 30 nm input devices; `b1` uses 48 um / 60 nm. Prefix `d` instead of `b` removes the four-MOS local clock buffer and drives the core directly from CLKC. The default tail width is 4 um; `t3`, `t2` and `t1` use 3 um, 2 um and 1 um. Prefix `g` uses clock-precharged output sensing nodes (a failed experiment with invalid fast-corner outputs). Prefix `u` removes the output buffers, directly loads the core with 10 fF per output and uses 2 um M8/M9. Prefix `v` additionally enlarges M8/M9 to 4 um and reduces input-drain precharge PMOS to 2 um; this fails slow-corner reset. Prefix `r` instead keeps 2 um M8/M9, uses 6 um input-drain precharge PMOS controlled by a two-inverter delayed clock, and adds two 4 um output-reset NMOS controlled by the inverted clock. Its tail remains driven directly by CLKC. Prefix `q` further changes the first clock inverter NMOS to 1 um and the second inverter NMOS to 8 um. Miyahara `w0` and `w56` split input precharge into 4 um delayed-clock and 2 um direct-clock PMOS in parallel, use a 4 um first clock NMOS, and have 48 or 56 um input devices. `x56` instead uses 3 um first-clock and 2 um output-reset NMOS, and adds 4.46051 fF nominal MOM capacitors to CKB and CKR. StrongARM prefixes `s4` and `s12` set the regenerative NMOS pair to 4 um or 12 um; the corresponding PMOS widths are 4 um and 8 um. StrongARM `svtn`, `svtnp` and `hvtn` use, respectively, SVT NMOS, SVT NMOS/PMOS, and HVT NMOS in the regenerative pair, with 4 um regenerative devices and a 3 um tail. Their `c14` suffix is 14.06 fF per input drain and `c0` adds no capacitor. StrongARM `s56` uses 56 um input NMOS, a 12 um / 8 um regenerative pair and direct clocking; `k56` adds a two-inverter delay on the input-drain precharge PMOS gates and enlarges the directly clocked output-node precharge PMOS to 4 um. StrongARM `l16` and `l24` use 16 or 24 um output precharge PMOS driven by the same delayed clock as input precharge, with 56 um inputs. StrongARM `p56` uses 56 um inputs, series 4/6 um input-drain precharge, parallel 2/4 um output precharge, direct/delayed clock controls, and 4.46051 fF nominal MOM capacitors on CKB and CKD. Suffixes `c1`, `c2`, `c4`, `c6` add a PDK MOM device from each input drain to ground, with nominal callback values 14.06, 27.42, 54.12 and 80.83 fF per side. The modeled device geometry, rather than an ideal capacitance, is simulated.

| Frozen netlist variant | SHA-256 |
|---|---|
| b0 | `095f0467ddfeb45edf5d90c79ab08c6f802a1733dee81754523d54932a4053ee` |
| b0c2 | `c62e70ad63c5f99a7ed226fee335e022fae1b91e4c6fbf6e6d7189b8ae0e5e4c` |
| d0c2 | `501d0920a0a55778d70d3c1cdd2e03f6f47b5a691b9009f9eacd6c2f1442abed` |
| d0t2c2 | `261896256c200f9dcc903054b910cbce618b2c94df527174cd250df5ffb62c10` |
| d0t3c2 | `5eb7705536f2b0a1d2cad02d019f6f791bac08e5b537cba9aaa726a77c108355` |
| g0t3c2 | `6ae329a3a2e9a2c47a924781b4ca998b54616ffee430687e5611c0bec7928cfc` |
| u0c2 | `7c8d919b0fb2a209b76d67ffda6d5df1ffb7dc7bee6686e7f9806f8697536664` |
| u0t3c1 | `d8398c2a93f1486b9b4495546735549365172b3141273fabbad2f6dba2fd5114` |
| u0t3c2 | `4252673c5a5c83c8abec45e43e5b93b92d70bc8ea1dd2e511bb19f747df947c1` |
| v0t3c1 | `961e3333d0ff61b34c7fe5b17d6f274567ac46ad7c09e7837ca8c990aba313bb` |
| v0t3c2 | `a76b1a162893b75a8e624f6020e6e6481c012a0d44aada2bbfa135db384ce96c` |
| r0t3c1 | `96ac36380266059b7b02a3b3ccf7e5844e2d6c74ca10229d60cb7ee5cf313511` |
| r0t3c2 | `e66124eeee9f5b6a3de50a1190e6249a00626b22ceb61ff28c9df8ce84975d9f` |
| q0t3c1 | `b735733d50d4d759f106599436883c750c565b28525987dbb9e04fd81821489c` |
| w0t3c1 | `e4e7d893a746fc619ca2554634a7e90d6e58a4ec4a536f7f766e19199a790475` |
| w56t3c1 | `8613c91e134bea0e85e7ee334326dd819d38fdebf91bfa55adf6c3832179d74e` |
| x56t3c1 | `3b1537b6a7ef273ef9a9a2f7d3f0cf9fae3e404060245e592ea99e9ef7333b7a` |

A lower energy number is not a qualified comparison unless the same noise, timing, reset, input-load, kickback and SOA requirements are met. The table is exploratory evidence only; see the candidate README and repository results for the separately frozen formal run status.
