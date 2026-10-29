# Supplemental characterization

These are private exploration runs using frozen netlist copies and the standard excitation and 10 fF loads. They are not official acceptance records. Every completed variant, including failures, is retained here. Each noise pilot uses 17 levels, 64 decisions per level, seed 1 and a 50 GHz bandwidth. Fine transient checks use 0.5 ps maximum step, traponly, reltol = 1e-6 and vabstol = 1e-8. Noise pilots retain the standard numerical settings.

| Variant / corner | Test | Result |
|---|---|---|
| b0 / tt_nom_27 | delay (fine) | 1 mV 44.93 ps; 30 mV 34.52 ps; reset 22.99 ps; energy 124.59 fJ; wrong 0; SOA violations 0 / 57; max 0.9553 V; simultaneous high points 0 |
| b0 / tt_nom_27 | noise | noise 255.79 uV (95% CI 230.99–284.01); offset -0.0184 mV; weak decisions 0 |

Variant notation: `b0` uses 48 um / 30 nm input devices; `b1` uses 48 um / 60 nm. The default tail width is 4 um; `t2` and `t1` use 2 um and 1 um. Suffixes `c1`, `c2`, `c4`, `c6` add a PDK MOM device from each input drain to ground, with nominal callback values 14.06, 27.42, 54.12 and 80.83 fF per side. The modeled device geometry, rather than an ideal capacitance, is simulated.

| Frozen netlist variant | SHA-256 |
|---|---|
| b0 | `56f176b60569c4e57a56b844e00cdef84e607e26878972df4fd8f6795fb4878a` |

A lower energy number is not a qualified comparison unless the same noise, timing, reset, input-load, kickback and SOA requirements are met. The table is exploratory evidence only; all-corner checks and the formal 50-sample mismatch flow remain outstanding.
