# StrongARM comparator: RESET-V27

**Numerical-settings transition:** new-settings private checks are recorded in [issue #94 evidence](NUMERICS-94.md). Four critical corners and tighter TT/SF/SS timing, reset, output validity and MOS stress pass, as do TT capacitance and the specified net per-cycle kickback at two precisions. The full TT noise precheck fails: **210.1008609253812 uV rms against 200 uV**, with 95% interval 201.81 to 218.79 uV and all 8704 samples retained. Qualification expansion of V27 stops; circuit diagnosis and design continue. The historical screening below uses the preceding settings. No formal or new-settings qualification is claimed.

The canonical `adc_comp.scs` now contains the electrically identical source screened as [RESET-V27](RESET-V27.md). All ten known key corners and targeted convergence at sf_high_m40, tt_nom_27 pass timing, reset, physical output validity and full-trace MOS stress. This is screening evidence; the candidate remains WIP, unqualified and unselected.

The source contains 23 MOS devices and 5 physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact validated geometry reuse. Physical rail loads carry persistent current; [ENERGY-COMPARISON.md](ENERGY-COMPARISON.md) reports measured complete-circuit AVDD costs. No power limit or topology-efficiency conclusion is implied.

The old canonical netlist and all 92 official records are preserved at commit `05d4d445c50471c0627d9b41f41b238bb8cfc1d9` and in a SHA-verified archive. At preservation, 2 records matched the immediate old canonical source and 90 already referred to older sources. All 92 are stale for the new source. They will be replaced only by actual new-source runs through the existing official runner; no private measurements or old metadata are relabeled. [Promotion proof](PROMOTION-RESET-V27.md) records source equivalence and preserved hashes. [Historical baseline](BASELINE-BEFORE-RESET-V27.md) retains the previous narrative and experiment links.

The conservative workflow merged in PR #95 as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`, with adc_comp 0.8.0. The next step is to refresh necessary key evidence through the merged official runner and pinned dependency, while continuing physical repair of the known noise failure. Remaining-corner SOA, all required formal corners, Monte Carlo and mixed-top qualification remain to establish. No old capacitance, noise, mismatch or qualification result is inherited.

![Current complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 remain acknowledged. Every older experiment and failed screen is retained separately.

Independent [RESET-V28](RESET-V28.md) changes only the CKB MOM from 16 to 8 fingers. All MOS and other MOMs are unchanged. Four proposed-settings critical corners and tighter TT/SF/SS repeats pass every actual polarity, reset, output-validity and unrounded terminal-stress check. Tighter TT 30 mV delay is 49.84967366576565 ps, leaving only 0.15032633423435 ps. These are private screens; a noise benefit remains unproven and V28 is not promoted.

Official 0.8.0 run `20261031-125724-e0ac-tb_comp_noise` refreshes tt_nom_27 noise 210.100860925 uV (FAIL CMP-01). [Exact committed evidence](FORMAL-SPEC08.md) preserves the actual source and original results. Current dependency coverage is 1/92; this does not establish qualification.
