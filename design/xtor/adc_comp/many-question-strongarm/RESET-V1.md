# RESET-V1: one controlled reset-network experiment

This is an independent **private diagnostic**, not the candidate selected by the official view. The canonical `adc_comp.scs`, its schematic and all 92 official records remain frozen. The baseline circuit is the one simulated from clean source `424d10a78ce75a1ef45d121575a9eac07a1ebd93`; its electrical SHA-256 is `150dd81755a64d66f582a84fd734462f5ad2c8b31ce4399b6507481d30372119`. This experiment does not replace the standard-step v0.7.0 evidence or establish qualification.

[Frozen experiment source with complete RNL](RESET-V1.txt) · [schematic](reset-v1.png).

## Evidence motivating the change

The original private 0.5 ps / traponly waveforms were re-read before defining the variant. Their job-local electrical circuit matches the canonical baseline. Their historical enclosing worktree was dirty, so these old runs are not relabeled as clean-source runs. Original waveforms, source metadata and archive hashes are retained privately. The old energy window differs from v0.7.0 and is not used as the matched energy control.

| Corner | Observed stage and terminals | Actual sampled peak | Worst reset |
|---|---|---:|---:|
| ff_high_m40 | Evaluation, CLKC rise +91.995 ps; DPX=1.067415 V, DP=0.013654 V | MRDP \|Vds\|=1.053761 V | 21.185679 ps |
| ff_high_125 | Reset, CLKC fall +17.749 ps; QP=1.020829 V, CLKC=0 | MRQP \|Vgd\|=1.020829 V | 24.030597 ps |
| ss_low_125 | DPX charge redistribution precedes the late DP/Q refill | MRQP \|Vgd\|=0.836633 V | 38.439852 ps |

The cold DPX excursion persists into evaluation. At hot fast conditions, the highest stress instead occurs during Q refill. The delayed series precharge and associated charge redistribution are a hypothesis for the reset bottleneck; temporal association alone does not prove causality.

## Frozen change and falsifiable prediction

- Replace each two-device input-drain precharge branch with one 2.4 um / 30 nm PMOS, three 0.8 um fingers, connected directly from AVDD to DP or DN. DPX/DNX and MPDP/MPDN disappear. The chosen width approximates the nominal series conductance of the previous 4 um and 6 um devices; it is a single fixed choice, not a sweep.
- Generate `PR = CLKC OR CKD` with a transistor NOR and inverter; drive MRDP/MRDN from PR. Generate `TE = CLKC AND CKD` with a transistor NAND and inverter; drive the existing 3 um tail from TE. This intends to separate input precharge and tail conduction; actual analog transition separation must be measured.
- Merge each Q-node's 2 um direct and 4 um delayed precharge devices into one 6 um PMOS controlled by CLKC. The stronger early path is intended to constrain the refill overshoot and shorten reset.
- Keep the input pair, latch, RTZ output inverters, four MOM devices, ports and external 10 fF loads unchanged. The existing two-inverter CKD generator is retained, although its changed load affects its delay.

The 12 added logic MOS have 1 um / 30 nm front devices (one finger) and N2/P4 um output inverters. All new or resized geometries passed device callbacks with no warnings; ordered inputs, outputs, package provenance and SHA verification are retained privately. Total: **31 MOS and four MOM**, versus 23 MOS and four MOM in the baseline. Complete RNL was checked using a byte-identical `.scs` validation copy and visually inspected.

The prediction is lower MRDP ds and MRQP gd stress and shorter SS reset while preserving zero CMP-15 violations. Any remaining or newly introduced terminal overvoltage is a failure of the stress-repair hypothesis. Record added delay, AVDD energy and CLKC charge even if functional validity passes. Added controls may change regeneration timing, kickback, input-referred noise and offset; baseline noise/MC evidence does not transfer to this variant.

## Bounded comparison protocol

Only `tt_nom_27`, `ff_high_m40`, `ff_high_125` and `ss_low_125`: matched baseline and this one variant, eight serial jobs with at most one Spectre process. Use the current official delay stimulus and validity implementation, with private numeric overrides maxstep=0.5 ps, method=traponly, reltol=1e-6 and vabstol=1e-8. AVDD energy uses the current 100 ps..14.5 ns meter, 36 complete mixed-amplitude cycles.

Save every MOS terminal for all gs/gd/ds checks: 69 baseline pairs and 93 variant pairs, including every new logic device. Preserve failed checks and stop on simulation input/solver errors. Saving VCK's branch current adds no circuit element: integrate current delivered by the ideal clock source and apply the existing rising-edge charge window to report effective CLKC capacitance over the 36 mixed-input cycles. This is a private clock-load comparison, not a replacement for official CMP-14 kickback-bench evidence.

If the variant improves the targeted behavior, repeat only its worst stress corner at 0.25 ps. Do not launch another variant, sizing sweep, 45-corner campaign, noise or MC in this experiment. This candidate stays draft/WIP; Miyahara remains frozen.

## Results

Pending the frozen-source four-corner comparison. No new simulation result is claimed by this source-freeze commit.
