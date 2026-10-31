# Miyahara comparator: BUFFER-V20

**Proposed-settings noise failure:** the full private TT test passes at 191.43800312001045 uV rms (95% profile interval 183.58–199.69 uV), but FS/low/125 fails at 343.4944014285115 uV (332.03–355.53 uV) against 240 uV. Each test retains all 8704 finite samples. B20 qualification expansion has stopped while physical design continues. [NUMERICS-94.md](NUMERICS-94.md) preserves the failed noise test and the passing private critical-corner timing, reset, validity, terminal-stress and kickback checks. These are proposed-settings prechecks, not formal acceptance.

**Numerical-settings transition:** older original-run records below require actual revalidation after [issue #94](NUMERICS-94.md) merges. The old sub-microvolt kickback result is not an established physical conclusion. New private kickback evidence distinguishes the specified net change after evaluation and reset from instantaneous differential and common-mode disturbances; only the net metric is judged against its 40 uV limit. Future actual-CDAC validation must inspect decision-phase input disturbance.

The canonical `adc_comp.scs` now contains the electrically identical source screened as [BUFFER-V20](BUFFER-V20.md). All ten known key corners and targeted convergence at sf_high_m40 pass timing, reset, physical output validity and full-trace MOS stress. This is screening evidence; the candidate remains WIP, unqualified and unselected.

The source contains 43 MOS devices and 9 physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact validated geometry reuse. Physical rail loads carry persistent current; [ENERGY-COMPARISON.md](ENERGY-COMPARISON.md) reports measured complete-circuit AVDD costs. No power limit or topology-efficiency conclusion is implied.

The old canonical netlist and all 96 official records are preserved at commit `5a9405c5ff48d3493c7098a7987ff7c56f7df001` and in a SHA-verified archive. At preservation, 6 records matched the immediate old canonical source and 90 already referred to older sources. At promotion, all 96 records were stale for the new source. Current original-run coverage is reported below. They will be replaced only by actual new-source runs through the existing official runner; no private measurements or old metadata are relabeled. [Promotion proof](PROMOTION-BUFFER-V20.md) records source equivalence and preserved hashes. [Historical baseline](BASELINE-BEFORE-BUFFER-V20.md) retains the previous narrative and experiment links.

The original-run gate status below supersedes the initial post-promotion plan. Remaining-corner SOA, all required formal corners, Monte Carlo and mixed-top qualification remain to establish. No old capacitance, noise, mismatch or qualification result is inherited.

![Current complete transistor schematic](schematic.png)

Issues #40, #63, #69, #75, #77, #78 and #84 remain acknowledged. Every older experiment and failed screen is retained separately.

## Current original-run status

Original tt_nom_27 noise PASS: 191.159437 uV rms against 200 uV (95% interval 183.31–199.41). This is preserved old-settings evidence. Issue #94 supersedes the previous expansion plan: new-settings private prechecks come first; required formal reruns will use the merged official flow. No further old-settings full-corner qualification is being launched.

2 of 96 records match the current electrical source; 94 retain older source hashes. [Original-run evidence](FORMAL-BUFFER-V20.md) preserves actual metadata, counts and archives. Source matching does not imply passing.

Independent [BUFFER-V21](BUFFER-V21.md), with only RP/RN MOMs enlarged from 8 to 16 fingers, fails SS/low/125 reset at 35.42069219051348 ps against 35 ps. All five corners pass actual polarity, output validity and unrounded terminal stress, but this reset failure stops noise expansion. The measured reset path is preserved for physical repair; no noise improvement is claimed.

PR #95 has merged as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`, raising adc_comp to 0.8.0. Necessary canonical-source evidence will be refreshed with the merged official flow and exact pinned dependency; known failed variants are not expanded to full-corner qualification.

Official 0.8.0 run `20261031-125734-f562-tb_comp_noise` refreshes fs_low_125 noise 343.494401429 uV (FAIL CMP-13). [Exact committed evidence](FORMAL-SPEC08.md) preserves the actual source and original results. Current dependency coverage is 1/96; this does not establish qualification.

Independent [BUFFER-V22](BUFFER-V22.md) retains B21 storage and tests only MCKP 4 to 5 um for earlier reset assertion. All other devices remain unchanged. Actual merged-flow timing, reset, stress and validity precede further noise work.

B22 passes five merged-baseline deterministic corners and four tighter repeats, including all 180/144 actual decisions and resets and every unrounded MOS terminal pair. [B22 evidence](BUFFER-V22.md) preserves the complete tighter stress table and matched B21 reset-path comparison. Full noise remains the next gate; no promotion or qualification is claimed.
