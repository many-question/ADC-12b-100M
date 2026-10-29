# Supplemental characterization

These are private exploration runs using frozen netlist copies and the standard excitation and 10 fF loads. They are not official acceptance records. Every completed variant, including failures, is retained here. Each noise pilot uses 17 levels, 64 decisions per level, seed 1 and a 50 GHz bandwidth. Fine transient checks use 0.5 ps maximum step, traponly, reltol = 1e-6 and vabstol = 1e-8. Noise pilots retain the standard numerical settings.

| Variant / corner | Test | Result |
|---|---|---|
| b0 / tt_nom_27 | delay (fine) | 1 mV 41.89 ps; 30 mV 35.33 ps; reset 33.66 ps; energy 138.19 fJ; wrong 0; SOA violations 0 / 81; max 0.9764 V; simultaneous high points 0 |
| b0 / tt_nom_27 | noise | noise 237.44 uV (95% CI 213.43–264.76); offset -0.0058 mV; weak decisions 0 |
| b0c2 / tt_nom_27 | delay (fine) | 1 mV 53.71 ps; 30 mV 46.15 ps; reset 39.25 ps; energy 185.76 fJ; wrong 0; SOA violations 0 / 81; max 0.9676 V; simultaneous high points 0 |
| b0c2 / tt_nom_27 | noise | noise 215.17 uV (95% CI 192.35–241.22); offset -0.0075 mV; weak decisions 0 |

Variant notation: `b0` uses 48 um / 30 nm input devices; `b1` uses 48 um / 60 nm. The default tail width is 4 um; `t2` and `t1` use 2 um and 1 um. Suffixes `c1`, `c2`, `c4`, `c6` add a PDK MOM device from each input drain to ground, with nominal callback values 14.06, 27.42, 54.12 and 80.83 fF per side. The modeled device geometry, rather than an ideal capacitance, is simulated.

| Frozen netlist variant | SHA-256 |
|---|---|
| b0 | `095f0467ddfeb45edf5d90c79ab08c6f802a1733dee81754523d54932a4053ee` |
| b0c2 | `c62e70ad63c5f99a7ed226fee335e022fae1b91e4c6fbf6e6d7189b8ae0e5e4c` |

A lower energy number is not a qualified comparison unless the same noise, timing, reset, input-load, kickback and SOA requirements are met. The table is exploratory evidence only; all-corner checks and the formal 50-sample mismatch flow remain outstanding.
