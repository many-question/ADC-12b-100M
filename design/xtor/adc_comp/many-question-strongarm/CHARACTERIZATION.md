# Supplemental characterization

These are private exploration runs using frozen netlist copies and the standard excitation and 10 fF loads. They are not official acceptance records. Every completed variant, including failures, is retained here. Each noise pilot uses 17 levels, 64 decisions per level, seed 1 and a 50 GHz bandwidth. Fine transient checks use 0.5 ps maximum step, traponly, reltol = 1e-6 and vabstol = 1e-8. Noise pilots retain the standard numerical settings.

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

Variant notation: `b0` uses 48 um / 30 nm input devices; `b1` uses 48 um / 60 nm. Prefix `d` instead of `b` removes the four-MOS local clock buffer and drives the core directly from CLKC. The default tail width is 4 um; `t3`, `t2` and `t1` use 3 um, 2 um and 1 um. Prefix `g` uses clock-precharged output sensing nodes (a failed experiment with invalid fast-corner outputs). Prefix `u` removes the output buffers, directly loads the core with 10 fF per output and uses 2 um M8/M9. StrongARM prefixes `s4` and `s12` set the regenerative NMOS pair to 4 um or 12 um; the corresponding PMOS widths are 4 um and 8 um. Suffixes `c1`, `c2`, `c4`, `c6` add a PDK MOM device from each input drain to ground, with nominal callback values 14.06, 27.42, 54.12 and 80.83 fF per side. The modeled device geometry, rather than an ideal capacitance, is simulated.

| Frozen netlist variant | SHA-256 |
|---|---|
| b0 | `56f176b60569c4e57a56b844e00cdef84e607e26878972df4fd8f6795fb4878a` |
| d0c2 | `0cc4d00d2e78e338930f65e94b82b46ba66be3c16649f0741d1132d34acb6bb1` |
| d0t2c2 | `b4c296fc5193f428c3337d0e90ed377b4c3983b96f7484755fd8092e63c6232b` |

A lower energy number is not a qualified comparison unless the same noise, timing, reset, input-load, kickback and SOA requirements are met. The table is exploratory evidence only; all-corner checks and candidate results from the formal 50-sample mismatch flow remain outstanding.
