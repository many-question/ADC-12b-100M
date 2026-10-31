# Miyahara comparator: BUFFER-V20

The canonical `adc_comp.scs` now contains the electrically identical source screened as [BUFFER-V20](BUFFER-V20.md). All ten known key corners and targeted convergence at sf_high_m40 pass timing, reset, physical output validity and full-trace MOS stress. This is screening evidence; the candidate remains WIP, unqualified and unselected.

The source contains 43 MOS devices and 9 physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact validated geometry reuse. Physical rail loads carry persistent current; [ENERGY-COMPARISON.md](ENERGY-COMPARISON.md) reports measured complete-circuit AVDD costs. No power limit or topology-efficiency conclusion is implied.

The old canonical netlist and all 96 official records are preserved at commit `5a9405c5ff48d3493c7098a7987ff7c56f7df001` and in a SHA-verified archive. At preservation, 6 records matched the immediate old canonical source and 90 already referred to older sources. At promotion, all 96 records were stale for the new source. Current original-run coverage is reported below. They will be replaced only by actual new-source runs through the existing official runner; no private measurements or old metadata are relabeled. [Promotion proof](PROMOTION-BUFFER-V20.md) records source equivalence and preserved hashes. [Historical baseline](BASELINE-BEFORE-BUFFER-V20.md) retains the previous narrative and experiment links.

The original-run gate status below supersedes the initial post-promotion plan. Remaining-corner SOA, all required formal corners, Monte Carlo and mixed-top qualification remain to establish. No old capacitance, noise, mismatch or qualification result is inherited.

![Current complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 remain acknowledged. Every older experiment and failed screen is retained separately.

## Current original-run status

Original TT capacitance/kickback PASS: input 19.328731 fF, CLKC 11.287775 fF and kickback 0.004586 uV. The next gate is the original complete TT noise test.

1 of 96 records match the current electrical source; 95 retain older source hashes. [Original-run evidence](FORMAL-BUFFER-V20.md) preserves actual metadata, counts and archives. Source matching does not imply passing.
