# StrongARM comparator: RESET-V19

The canonical `adc_comp.scs` now contains the electrically identical source screened as [RESET-V19](RESET-V19.md). All ten known key corners and targeted convergence at sf_high_m40 pass timing, reset, physical output validity and full-trace MOS stress. This is screening evidence; the candidate remains WIP, unqualified and unselected.

The source contains 23 MOS devices and 5 physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact validated geometry reuse. Physical rail loads carry persistent current; [ENERGY-COMPARISON.md](ENERGY-COMPARISON.md) reports measured complete-circuit AVDD costs. No power limit or topology-efficiency conclusion is implied.

The old canonical netlist and all 92 official records are preserved at commit `8c0d2666ccb0e135e5799e3c2390bbd4db3dfe12` and in a SHA-verified archive. At preservation, 2 records matched the immediate old canonical source and 90 already referred to older sources. At promotion all 92 were stale for the new source. One genuine new-source TT capacitance/kickback record now matches V19; 91 remain stale. They will be replaced only by actual new-source runs through the existing official runner; no private measurements or old metadata are relabeled. [Promotion proof](PROMOTION-RESET-V19.md) records source equivalence and preserved hashes. [Historical baseline](BASELINE-BEFORE-RESET-V19.md) retains the previous narrative and experiment links.

[Original TT capacitance/kickback validation](FORMAL-RESET-V19.md) passes: input 19.330641 fF, CLKC 15.807766 fF and kickback 0.930826 uV. The next gate is the original complete TT noise test. Remaining-corner SOA, all required formal corners, Monte Carlo and mixed-top qualification remain to establish. No old capacitance, noise, mismatch or qualification result is inherited.

![Current complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 remain acknowledged. Every older experiment and failed screen is retained separately.
