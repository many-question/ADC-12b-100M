# StrongARM comparator: RESET-V19

The canonical `adc_comp.scs` now contains the electrically identical source screened as [RESET-V19](RESET-V19.md). All ten known key corners and targeted convergence at sf_high_m40 pass timing, reset, physical output validity and full-trace MOS stress. This is screening evidence; the candidate remains WIP, unqualified and unselected.

The source contains 23 MOS devices and 5 physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact validated geometry reuse. Physical rail loads carry persistent current; [ENERGY-COMPARISON.md](ENERGY-COMPARISON.md) reports measured complete-circuit AVDD costs. No power limit or topology-efficiency conclusion is implied.

The old canonical netlist and all 92 official records are preserved at commit `8c0d2666ccb0e135e5799e3c2390bbd4db3dfe12` and in a SHA-verified archive. At preservation, 2 records matched the immediate old canonical source and 90 already referred to older sources. At promotion all 92 were stale for the new source. Two genuine new-source TT cases now match V19 (capacitance/kickback and noise); 90 remain stale. They will be replaced only by actual new-source runs through the existing official runner; no private measurements or old metadata are relabeled. [Promotion proof](PROMOTION-RESET-V19.md) records source equivalence and preserved hashes. [Historical baseline](BASELINE-BEFORE-RESET-V19.md) retains the previous narrative and experiment links.

[Original TT capacitance/kickback validation](FORMAL-RESET-V19.md) passes: input 19.330641 fF, CLKC 15.807766 fF and kickback 0.930826 uV. The original complete TT noise test gives 218.770059 uV rms (95% interval 210.31–227.64), a fail against 200 uV. V19 qualification expansion stops at this failure; physical diagnosis and a subsequent circuit revision remain active. Remaining-corner SOA, all required formal corners, Monte Carlo and mixed-top qualification remain to establish. No old capacitance, noise, mismatch or qualification result is inherited.

![Current complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 remain acknowledged. Every older experiment and failed screen is retained separately.

Independent [RESET-V20](RESET-V20.md) changes only the two Q-node MOMs from 4.46 to 5.66049 fF to test release-stage signal-to-noise margin after the genuine V19 TT noise failure. Its first SF/FS high/-40 and TT private screens pass all 108 actual polarities, resets, timing, output validity and terminal stress. TT 1/30 mV delay is 62.091895/47.862333 ps and reset 23.672701 ps. A matched short phase diagnosis follows; no noise benefit is established. Canonical V19 and all formal records remain unchanged.
