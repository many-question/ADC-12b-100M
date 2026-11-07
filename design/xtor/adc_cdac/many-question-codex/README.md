# CDAC candidate

## Formal candidate and qualification

The [formal source](adc_cdac.scs) uses a 14 um / 40 nm LVT reset driven by the independent Fig. 11(c) v3 booster, LVT / 40 nm main input switches and SVT / 40 nm reference output pairs on bits 12 and 11, and the original sharing sizes. It retains the XCAP and XSW partition. Both complete hot spectra meet the 84 dBc DAC-09 limit in spec 0.11.0. The official slow-corner RL12 and conversion-start failures keep the candidate WIP. [Qualification matrix and evidence](qualification.md) · [Physical repair experiments](reset-repair.md)

Cold Gear2 still stops at 60.0983 ns on the formal bench. The voltage-only replay reproduces the failure. The paired local stack, driver and bottom-plate replays leave the full-circuit convergence mechanism unresolved. [Cold replay boundaries and archives](qualification.md#reduced-replay)

The complete cold numerical crosscheck finds a consistent H5 deficit. A private combined predriver change passes both SS timing screens. The best screened physical variant reaches 81.01 dBc SFDR and 79.75 dB SNDR in the complete cold record, below the 84 dBc and 80 dB limits. [Numerical crosscheck and timing screen](qualification.md#full-length-cold-numerical-crosscheck)

## V29 and preceding experiments

The records below describe the historical baseline and earlier circuit variants. The [V29 source and official records](https://github.com/many-question/ADC-12b-100M/tree/7fb3ce84ae0f7e8ea161cd7ec514895f8276ec20) are retained at their original commit.

## Completed reset mechanism isolation

All other signal switches are now idealized in an explicit A/B experiment.
The completed fixed-input controls show a nearly constant immediate reset
offset and later input-dependent hold error; static bias checks confirm late
off-state flow. Full256 A/B gives SFDR 112.863/85.802dBc; B's traponly/1ps
crosscheck gives 85.554dBc, retaining a 0.247dB method difference. Dynamic H3 is
already 32.842uV before reset turnoff and grows to 40.593uV at sampling, versus
A's 1.308/1.800uV. On-state bias checks corroborate nonlinear clamping; late
off-state flow adds a different-phase component during hold. All ten records
are reviewed and archived. The canonical circuit remains WIP. See the
[replacement boundary, measured timing and evidence](reset-mechanism.md).

## Completed first boosted-reset cohort

The first independent finite-driver / real-NMOS cohort is complete: all three
full256 hot spectra miss the targets, and dedicated cold SOA exposes supply/size
limits. See the [results, mechanism and source patches](boosted-reset-experiment.md).
The V29 attribution results below belong to that historical source.


V29 status (2026-11-05): resumed after the project resolved issue #125.
DAC-12 is now 1.35 pC (#132); the new all-corner DAC-18 SOA test and
transient-overvoltage rule (#137) apply. Candidate remains WIP.

V29 blockers (see [validation status and completed diagnostics](validation-status.md)): official track aborts at 60.1007 ns with
SPECTRE-16928 (minstep approach count), only 2/256 samples; no valid spectrum.
Dedicated SOA completes but fails 3 terminal pairs: MTP Vgd and MTD Vgs/Vgd,
all the TOP-PHI_SB stress. SOA crosscheck confirms 126.906 ps above 1.1 V
per 10 ns window (limit 100 ps), versus primary 127.281 ps. Track replay
reproduces the same cold-corner solver failure. Complete ss_low_125 track
also fails: SFDR/SNDR 63.137/63.061 dB, confirmed within 0.015 dB by
crosscheck. Batch expansion has stopped; official failures are preserved.
Bounded cold traponly/1 ps reaches 80.050 ns without the old step-collapse
cluster. Hot observation reaches 100.064 ns with all requested currents;
reset tracking impedance and off-state currents warrant further isolation.
These partial diagnostics do not close the blockers or prove a repair.
An ideal late-track reset shunt halves tracking error and reduces the
matched 16-sample non-fundamental residual by 29.72%; hold drift worsens.
This supports a reset-path contribution, not a full-spectrum pass.
Private physical reset2x now passes all five pre-tracking gates, including
cold SOA primary/cross (0 violations, 53.34/53.27 ps). Hot-SS droop worsens
to .0606 LSB but passes. Full hot primary fails at 67.033/66.609 dB despite
a 3.90/3.55 dB improvement. Full cross differs by only .0083/.0052 dB.
Four independent ideal-switch replacements from original V29 now have complete
256-point hot-SS spectra. Reset improves SFDR by 13.725 dB to 76.862 dBc;
input improves .658 dB, reference .031 dB, and sharing worsens .302 dB.
Reset H3 falls from 545.39 to 112.80 uV. This identifies the reset cell as
the strongest group intervention, including its removed intrinsic charges.
All reset subcase primaries are complete. P-only idealization has the largest
response: 82.740/80.526 dB and H3 57.16 uV, versus N-only 70.413/70.213,
N/P ideal with real dummy 77.269/76.762, and dummy removal 63.084/63.013.
N/P effects are strongly nonadditive; these interventions do not isolate an
independent physical contribution. P-only primary logs two LTE relaxations.
Full-reset cross agrees within .082/.068 dB SFDR/SNDR. P-only cross retains
82.366/80.318 dB, changes -.374/-.208 dB, preserving its large response.
The SNDR change is material to the .318 dB cross margin, whose numerical
convergence is not established. Both complete cross records are archived.
The completed attribution stage did not qualify a physical repair; even P-only
misses the SFDR target. The newly authorized boosted-reset experiment is separate.
See the validation status for the complete matrix and attribution limits.
The canonical source and its official failures remain unchanged.


V29 was migrated into the accepted XCAP/XSW
functional partition. XCAP holds the 36 array MOM and 36 associated 5% Cp;
the 26 AP delay loads and one SAMP_ON control load, with their own 5% Cp,
remain inside the corresponding XSW control functions. There are still
32 array connections and 37 unchanged external ports. No sizing, model,
parameter or electrical connection has changed from historical V29.
Independent flattening compares all 722 leaves (596 MOS, 63 MOM, 63 Cp),
273 bijective nets and ordered terminals including bulk. Dependency hash:
`9b00f07143da7cc5`. Historical V29 source SHA-256:
`29d867d5bf07d79b3514cb49af0ad7c572ae1e929df88f33990a723bccfa0626`.
N4 remains preserved at f578badee155449a905ff6d63c22088e48a623f7.

First gate passed: TT weights 5/5, settle 10/10, track 2/2 and
ff_high_125 dedicated SOA. TT SFDR is 88.3724 dBc and SNDR 86.6184 dB;
Cs is 2.065123 pF and calibration margin 0.369435 LSB. Convergence checks,
remaining required corners and real-reference mixed-top validation are pending.
FF high125 SOA crosscheck passes with 0/0 violations over 1788 pairs;
peak 1.21415 -> 1.21343 V and worst 10 ns overvoltage window
21.638 -> 21.690 ps. Largest pair-peak change is 3.93 mV on a
0.63638 -> 0.64031 V pair, well below 1.1 V. N4's reported FF midpoint
PMOS violation is not evidence about V29, which uses a different gate signal.
No historical result is rehashed or treated as fresh evidence for this source.

SS low125 primary passes its five applicable metrics. Engineering convergence
(traponly, maxstep 1 ps, effective reltol 1e-7, vabstol 10 nV) changes RL12
39.7 -> 39.6 ps, RL5 57.9 -> 58.3 ps and start 97.9 -> 98.4 ps.
All remain within limits, but the 0.5 ps start difference is 24% of the
primary margin. A further 0.5 ps / 1e-8 / 1 nV refinement leaves all
timing readings unchanged; the stricter result passes with narrow margin.
This is a private numerical diagnostic, not a specification-defined crosscheck.

See [schematic review](schematic-review.md) and [source](adc_cdac.scs).

Evidence-retention update (2026-10-31): superseded large raw waveforms and
duplicate caches/archives have been released under the user's retention policy.
Historical formal N4 SS, V16 SS/FF and follow-up V29 SS/FF retain compressed originals;
V17/V18 retain selected decision signals, result reports and source hashes.
Historical archive statements describe capture-time storage. Released raw data
cannot be re-audited; selected V17/V18 signals do not support a full-DUT audit.

Historical N4 baseline (superseded by V29 above): all 17 required TT metrics
passed under the preceding protocol; its first slow-corner screen failed RL12
and conversion-start settling. Historical reports are preserved without relabeling.

Numerical-settings transition: [PR #95](https://github.com/many-question/ADC-12b-100M/pull/95)
merged as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`. The candidate branch
includes that official flow. ADCToolbox is installed from the exact pinned
upstream commit `cd72061ff3b7a977163dac540da126ae22f5e38d` in an isolated environment.
The first PR95 official rerun recorded N4 SS settling: RL12/start still fail
at 47.4/116.8 ps, using conservative, effective reltol 1e-4, gear2only
and no explicit maxstep. The old TT results are stale and do not establish
current acceptance; no eligibility or lead verification is inherited. PR112 now
also makes the stored SS settle testbench dependency stale.

Before the merge, same-source private comparisons retained the same V6 FF
failures (387 pairs in full settling, 355 in the original first 12 ns).
V11/V12 circuit exploration used those verified proposed settings. Their
private evidence remains separate from the new official baseline. See the
[same-source comparison](numerics94-same-source.png) and evidence ledger.

## Circuit and fixed assumptions

The current single-sided CDAC has 596 MOS, 63 aggregated MOM instances
and 63 explicit Cp elements. The differential test instantiates two copies.
It uses physical
midpoint initialization, split-supply reference drivers, NMOS sharing,
pulsed PMOS sampling assistance and an N4 TOP dummy. Complete RNL is
included in [adc_cdac.scs](adc_cdac.scs).

Every physical MOM unit has the user-specified 5% bottom-plate-to-VSS
estimate, including both series-tail units and MID. One 1.00229 fF unit
contributes 0.0501145 fF; 36 array Cp elements total 114.160831 fF,
including 0.300687 fF at six MID nodes. This is a pre-layout estimate,
not an extracted value or a parameter already present in the MOM model.
Weights 180 and 32 are excluded from sampling. No assumption changes in
the private output-driver studies.

## N4 evidence: historical TT and failing SS

| Check | Result |
|---|---|
| Historical TT weights/calibration (stale) | Previously 5/5 pass; Cs 2.065012 pF, full scale 0.993034 V, calibration margin 0.369061 LSB, calibrated ENOB loss 0.000364369 bit |
| Historical TT settling/charge/load (stale) | Previously 10/10 pass; RL12/start 35.3/83.4 ps, tau 9.120184 ps, Qref 1.124389535 pC |
| Historical TT tracking (stale) | Previously SFDR 86.417966859 dBc and SNDR 84.523548567 dB pass; old prescribed comparison differs by 0.000307850/0.000215801 dB |
| Historical N4 official ss_low_125 | RL5, tau and droop pass; RL12 47.4 ps >40 ps and start 116.8 ps >100 ps fail |

The preceding 12 official result/figure files are preserved in history;
the SS result and its two figures were refreshed by an actual rerun.
The old 9/17 requirement and 23/369 corner coverage counts describe the
preceding protocol, not current acceptance. Other current tests/corners,
project-lead verification and mixed top-level regression remain incomplete. Status stays
`wip`; ideal bootstrap/clock stimuli do not establish full integration or
reliability acceptance.

The separate same-source private TT stress checks cover 540 MOS for 70 ns
and 1,080 MOS for 125 ns of sine input. Maxima are 0.977333326 and
0.990224783 V, respectively, with no project gs/gd/ds violation. Model
warnings remain retained. These are limited records, not full PVT/startup
or long-hold qualification, and do not transfer to a changed circuit.

## Historical design studies and retained evidence

These studies precede the current V29 qualification and use their stated
historical limits. Their passes do not transfer to a changed source or to
the current protocol. The [diagnosis ledger](sampling-entry-diagnosis.md)
retains source identifiers, measurements and rejected variants. The
[complete pre-compaction report](https://github.com/many-question/ADC-12b-100M/blob/4f5d363c76a132d6a37dce4e6e0b3d19a3d83ba8/design/xtor/adc_cdac/many-question-codex/README.md)
preserves the full chronology and figure links. This documentation
compaction removes no circuit, formal result, diagnostic image or raw archive.

| Historical study | Retained outcome and limitation |
|---|---|
| N4 output-width +25% | SS RL12/start 42.2/113.0 ps fail; tau 17.111 ps adds a failure; no TT expansion |
| Lower-threshold outputs | SS 42.7/100.6 ps fail; reference charge +50.02%; off currents rise |
| Coordinated outputs and predrive | Intermediate cases still fail RL12 or old TT Qref limit; first passing SS upper-PMOS case has TT Qref 1.281323 pC > old 1.2 pC |
| Faster enable | TT Qref 1.203201 pC still fails old budget; internal-PMOS peak 1.014916 V exceeds old private 1.0 V screen |
| V6 AP keeper | SS and TT gates pass, TT Qref 1.187183 pC; complete FF settle fails 387 terminal pairs, differential sine fails 550; no full FFT expansion |
| V7–V13 control trials | Matched early-FF failing pairs progress through 472/299/279/272/269/205/175; local improvements remain failures. Missing-save attempts are unverified and retained separately |
| V14/V15 | V14 removes observed control-chain failures but leaves 157 early-FF pairs; V15 fails SS RL12 44.8 ps and two voltage pairs |
| V16 | SS RL12/start 39.7/96.5 ps, 123 early-FF failing pairs; narrow timing margin requires convergence checks |
| V17/V18 | 95/127 early-FF pairs; V17 fails SS RL12 41.0 ps, V18 raises SS reference charge to 3.056424 pC. Selected signals do not support a repeated full-DUT audit |
| V19/V20 | Better settling introduces BN undershoot and approximately 1.10 V FF peaks; rejected |
| V21/V22 | SS passes; 124/132 early-FF pairs include new NEN failures; not promoted |
| V23–V27 | NEN strengthening fails SS start; assist/sharing/transmission-gate trials pass SS but worsen early-FF failures to 141/165/183; not promoted |
| V28/V29 | NOFF dummy compensation reduces V16's 123 early-FF pairs to 69/51 without new pairs; V29 retains SS 39.7/97.9 ps and is the current follow-up baseline |

The historical FF counts above are private 1.0 V screens, generally the
matched first 12 ns unless a complete record is identified. Later rules
do not rewrite those results. Current dedicated SOA failures and limits
are in [validation-status.md](validation-status.md).

The [original history snapshot](https://github.com/many-question/ADC-12b-100M/tree/6a4bf94977db967dbd27ef47669d5d3d25735477/design/xtor/adc_cdac/many-question-codex),
[N4 TT tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-n4-tt-20261030),
[pre-N4 tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-pre-n4-20261030)
and [V9 snapshot](https://github.com/many-question/ADC-12b-100M/tree/20d4d8896dc8d9b94206b7c928e8e5e255b5c511/design/xtor/adc_cdac/many-question-codex)
retain prior reports, clean simulation commits and figures moved during
earlier size-limit compaction. Private waveform retention remains limited
to the evidence stated near the top of this document; released data are
not represented as re-auditable.

## Historical protocol migration

PR95 established the current numerical flow; PR112 added explicit-save
policy and the then-global 1.1 V limit. At that time CDAC had no formal SOA
metric. This is superseded by current DAC-18 and its transient-overvoltage
rule, described in the current status above.

After PR112, six V16/V29 SS primary/convergence and TT comparisons, a
reference-branch audit and V32/V33 TT studies completed. V16/V29 TT Qref
1.271878/1.269059 pC failed the old 1.2 pC budget; nine other TT metrics
passed. A branch audit found 77.084398 fC in reference-fed assist/phase
control. V32/V33 confirmed supply-load transfer with all capacitors and
5% parasitics retained. Those studies stopped pending the budget decision.
The current 1.35 pC limit and actual reruns are reported above; no historical
measurement was rehashed into a new-source pass.
