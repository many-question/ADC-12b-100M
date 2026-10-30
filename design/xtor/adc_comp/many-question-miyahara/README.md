# Miyahara comparator: BUFFER-V13

The canonical `adc_comp.scs` now contains the electrically identical source screened as [BUFFER-V13](BUFFER-V13.md). All ten known key corners and targeted convergence at sf_high_m40 pass timing, reset, physical output validity and full-trace MOS stress. This is screening evidence; the candidate remains WIP, unqualified and unselected.

The source contains 43 MOS devices and 9 physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact validated geometry reuse. Physical rail loads carry persistent current; [ENERGY-COMPARISON.md](ENERGY-COMPARISON.md) reports measured complete-circuit AVDD costs. No power limit or topology-efficiency conclusion is implied.

The old canonical netlist and all 92 official records are preserved at commit `740fe564b380bc8e3b6526d8ac109503325935ad` and in a SHA-verified archive. At preservation, 2 records matched the immediate old canonical source and 90 already referred to older sources. All 92 are stale for the new source. They will be replaced only by actual new-source runs through the existing official runner; no private measurements or old metadata are relabeled. [Promotion proof](PROMOTION-BUFFER-V13.md) records source equivalence and preserved hashes. [Historical baseline](BASELINE-BEFORE-BUFFER-V13.md) retains the previous narrative and experiment links.

Next formal gates are TT input/clock capacitance and kickback, followed by TT noise. Remaining-corner SOA, all required formal corners, Monte Carlo and mixed-top qualification remain to establish. No old capacitance, noise, mismatch or qualification result is inherited.

![Current complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 remain acknowledged. Every older experiment and failed screen is retained separately.
