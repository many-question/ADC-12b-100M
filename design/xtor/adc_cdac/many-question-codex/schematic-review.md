# V29 functional hierarchy — pending simulation

2026-11-03. XCAP contains the CDAC weighting/sampling MOM capacitors and their
5% bottom/MID parasitics. XSW contains all bottom/MID switches, reference
and logic drivers, and their control delay loads. The 26 AP loads and one
SAMP_ON load are control capacitors, so remain with their associated control
circuit. This grouping preserves 32 physical array interfaces, not 59.
All 37 external pins keep their order.

![Wrapper](schematic-array.png)

[Array](schematic-capacitors.png) · [Switches](schematic-switches.png) ·
[Bit 12](schematic-switch12.png) · [Source](adc_cdac.scs)

Independent parsing and flattening against frozen historical V29 matches
722 leaf devices, 273 nets, every parameter/model and ordered terminal
including bulk. 596 MOS + 63 MOM + 63 Cp, including all control loads.
[Mapping](schematic-audit.txt). N4/f578bad remains historical; the old N4
mapping/checker does not prove V29 equivalence. A new V29 checker and frozen
sources are retained with the migration evidence.

RNL check: zero errors/warnings. Source dependency: 9b00f07143da7cc5.
The source is pending new measurements. Prior results are retained with their
original provenance; no rehash. New SOA follows specs/soa_rule.yaml:
peak <=1.1 V, or peak <=1.29 V AND time above 1.1 V <=100 ps in every
10 ns sliding window over the entire transient including startup.

First gate: TT weights/settle/track plus FF high-temperature SOA. Subsequent
full-corner checks and real-reference mixed-top depend on that gate passing.
