# Supplemental characterization

These are private exploration runs using frozen netlist copies and the standard excitation and 10 fF loads. They are not official acceptance records. Every completed variant, including failures, is retained here. Each noise pilot uses 17 levels, 64 decisions per level, seed 1 and a 50 GHz bandwidth. Fine transient checks use 0.5 ps maximum step, traponly, reltol = 1e-6 and vabstol = 1e-8. Noise pilots retain the standard numerical settings.

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

Variant notation: `b0` uses 48 um / 30 nm input devices; `b1` uses 48 um / 60 nm. Prefix `d` instead of `b` removes the four-MOS local clock buffer and drives the core directly from CLKC. The default tail width is 4 um; `t3`, `t2` and `t1` use 3 um, 2 um and 1 um. Prefix `g` uses clock-precharged output sensing nodes (a failed experiment with invalid fast-corner outputs). Prefix `u` removes the output buffers, directly loads the core with 10 fF per output and uses 2 um M8/M9. StrongARM prefixes `s4` and `s12` set the regenerative NMOS pair to 4 um or 12 um; the corresponding PMOS widths are 4 um and 8 um. Suffixes `c1`, `c2`, `c4`, `c6` add a PDK MOM device from each input drain to ground, with nominal callback values 14.06, 27.42, 54.12 and 80.83 fF per side. The modeled device geometry, rather than an ideal capacitance, is simulated.

| Frozen netlist variant | SHA-256 |
|---|---|
| b0 | `095f0467ddfeb45edf5d90c79ab08c6f802a1733dee81754523d54932a4053ee` |
| b0c2 | `c62e70ad63c5f99a7ed226fee335e022fae1b91e4c6fbf6e6d7189b8ae0e5e4c` |
| d0c2 | `501d0920a0a55778d70d3c1cdd2e03f6f47b5a691b9009f9eacd6c2f1442abed` |
| d0t2c2 | `261896256c200f9dcc903054b910cbce618b2c94df527174cd250df5ffb62c10` |
| d0t3c2 | `5eb7705536f2b0a1d2cad02d019f6f791bac08e5b537cba9aaa726a77c108355` |
| g0t3c2 | `6ae329a3a2e9a2c47a924781b4ca998b54616ffee430687e5611c0bec7928cfc` |

A lower energy number is not a qualified comparison unless the same noise, timing, reset, input-load, kickback and SOA requirements are met. The table is exploratory evidence only; all-corner checks and candidate results from the formal 50-sample mismatch flow remain outstanding.
