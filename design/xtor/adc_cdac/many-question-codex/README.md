# CDAC candidate

Evidence-retention update (2026-10-31): superseded large raw waveforms and
duplicate caches/archives have been released under the user's retention policy.
Current formal N4 SS and V16 SS/FF retain one compressed original each;
V17/V18 retain selected decision signals, result reports and source hashes.
Historical archive statements describe capture-time storage. Released raw data
cannot be re-audited; selected V17/V18 signals do not support a full-DUT audit.

This WIP 28 nm HPC+ candidate retains the formal N4 source and its historical
TT reports. All 17 required TT metrics passed under the preceding protocol; the first slow-corner screen
fails RL12 and conversion-start settling. Successor experiments remain
independent until they earn their own validation; no old result is relabeled.

Numerical-settings transition: [PR #95](https://github.com/many-question/ADC-12b-100M/pull/95)
merged as `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`. The candidate branch
includes that official flow. ADCToolbox is installed from the exact pinned
upstream commit `cd72061ff3b7a977163dac540da126ae22f5e38d` in an isolated environment.
The first official rerun refreshes N4 SS settling: RL12/start still fail
at 47.4/116.8 ps, using conservative, effective reltol 1e-4, gear2only
and no explicit maxstep. The old TT results are stale and do not establish
current acceptance; no eligibility or lead verification is inherited.

Before the merge, same-source private comparisons retained the same V6 FF
failures (387 pairs in full settling, 355 in the original first 12 ns).
V11/V12 circuit exploration used those verified proposed settings. Their
private evidence remains separate from the new official baseline. See the
[same-source comparison](numerics94-same-source.png) and evidence ledger.

## Circuit and fixed assumptions

The single-sided CDAC has 540 MOS, 31 subcircuits and 2,278 physical MOM
units. The differential test instantiates two copies. It uses physical
midpoint initialization, split-supply reference drivers, NMOS sharing,
pulsed PMOS sampling assistance and an N4 TOP dummy. Complete RNL is
included in [adc_cdac.scs](adc_cdac.scs).

Every physical MOM unit has the user-specified 5% bottom-plate-to-VSS
estimate, including both series-tail units and MID. One 1.00229 fF unit
contributes 0.0501145 fF; 36 aggregated Cp elements total 114.160831 fF,
including 0.300687 fF at six MID nodes. This is a pre-layout estimate,
not an extracted value or a parameter already present in the MOM model.
Weights 180 and 32 are excluded from sampling. No assumption changes in
the private output-driver studies.

## N4 evidence: historical TT and current failing SS

| Check | Result |
|---|---|
| Historical TT weights/calibration (stale) | Previously 5/5 pass; Cs 2.065012 pF, full scale 0.993034 V, calibration margin 0.369061 LSB, calibrated ENOB loss 0.000364369 bit |
| Historical TT settling/charge/load (stale) | Previously 10/10 pass; RL12/start 35.3/83.4 ps, tau 9.120184 ps, Qref 1.124389535 pC |
| Historical TT tracking (stale) | Previously SFDR 86.417966859 dBc and SNDR 84.523548567 dB pass; old prescribed comparison differs by 0.000307850/0.000215801 dB |
| Current official ss_low_125 | RL5, tau and droop pass; RL12 47.4 ps >40 ps and start 116.8 ps >100 ps fail |

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

## Current design studies and retained history

The [current diagnosis and trial ledger](sampling-entry-diagnosis.md)
separates formal results, unchanged-source diagnostics and rejected variants.
The first private +25% bit-12 output-width trial was rejected: RL12/start
42.2/113.0 ps still fail and equivalent tau rises to 17.111203 ps, a new
failure. Its conditional TT run was not launched. Design iteration continues
through separately frozen experiments, with SS settling/all-device stress
before TT charge/load/settling, then spectra and further corners.

A complete matched SS comparison of lower-threshold reference outputs
also fails RL12/start (42.7/100.6 ps), despite improved tau (11.204798 ps)
and lower TOP overshoot. Full 540-MOS pressure checks pass, but Qref rises
50.0247% and quiet-window off currents increase. The trial's TT expansion
is stopped. Its [matched waveform comparison](https://github.com/many-question/ADC-12b-100M/blob/20d4d8896dc8d9b94206b7c928e8e5e255b5c511/design/xtor/adc_cdac/many-question-codex/matched-output-family-screen.png)
and the ledger retain the independent source and evidence. A subsequent
nominal-threshold case with coordinated output/enable sizing passes start
(90.6 ps), tau (11.117939 ps) and full MOS pressure, but RL12 still fails
at 43.6 ps. Its Qref increase is 6.8171%; TT expansion is stopped. The next
gate-driver family trial improves RL12 to 40.6 ps, still failing; start,
tau and all-MOS pressure pass, while Qref rises to 2.006878206 pC at SS
(n/a). Its TT expansion is also stopped. The subsequent upper-PMOS predrive
case passes all five SS settling requirements and all 540-MOS pressure
checks: RL12 39.2 ps, start 91.3 ps, tau 11.248227 ps. Its independent TT
check passes timing, loads and all-MOS pressure, but Qref is 1.281322764 pC
against the 1.2 pC limit. Its spectrum/corner expansion is stopped. A matched
phase audit identifies increased sampling-entry charge in one bit-12 branch
and slower shared disable. The next case doubles only the enable pull-up
and passes its independent SS gate (RL12/start 39.2/91.9 ps, all-MOS
maximum 0.979957590 V); SS Qref falls to 1.916043704 pC (n/a).
Its conditional TT run reduces Qref to 1.203200599 pC, still failing by
3.200599 fC, and finds a new internal-PMOS stress peak of 1.014916187 V.
That case stops before weights/spectra/corners. Its total-current integral
closes against the official meter: relative to a retained strict N4
diagnostic, sampling-entry charge is lower but start, decisions and sampling
tail add charge. The [TT reference-current audit](enable-pfast-tt-charge.png)
and internal-node voltages guide the next AP-hold/gate-family trial.
That independent V6 source now passes the full SS gate: RL12/start
38.7/92.3 ps, tau 11.291657 ps, and all 546 MOS / 1638 pairs below
1.0 V (maximum 0.978430006 V). Low-branch AP's sampling-entry peak
falls from 0.884407 to 0.853787 V at SS. Same-source TT then passes all
ten settling/charge/load requirements and full MOS pressure: Qref
1.187183082 pC, RL12/start 29.5/65.7 ps, global stress 0.996299050 V.
The previously failing bit-12 MPA1 peak falls to 0.945160621 V; the
global maximum now occurs at bit 11. The [TT waveforms](apkeeper-tt-waveforms.png)
and [charge audit](apkeeper-tt-charge.png) show the mechanism and retained
margin. Independent TT weights/calibration also passes all five checks,
including Cs 2.065012117 pF and calibration margin 0.369043499 LSB.
The same-source ff_high_m40 checks fail device voltage: complete 70 ns
settling passes all five applicable timing requirements but has 387 failing
terminal pairs, with a 1.103478637 V maximum. The 125 ns differential sine
screen has 550 failing pairs among 1092 MOS / 3276 pairs, with a
1.108169154 V maximum. FF full scale passes its one applicable weights
requirement. These failures stop V6's further-corner and full FFT expansion.
The [fast-corner waveforms](fast-stress-mechanisms.png) retain the AP,
control-buffer and bottom-plate failure mechanisms. The completed
[node/event audit](fast-node-events.png) identifies repeated shared-net
excursions and motivates a separate sharing-phase experiment. The formal
source is unchanged.
The independent V7 sharing-phase experiment passes SS timing and all-MOS
pressure, but its early FF screen fails. On a matched 0..12 ns interval,
the worst bottom-plate excursion decreases while the total failing-pair
count rises from 355 to 472. Its [matched comparison](early-sharing-comparison.png)
retains both effects; TT/weights expansion is stopped for V7.
The independent V8 common-edge experiment also passes SS: RL12/start
38.7/94.1 ps and maximum device voltage 0.978616967 V. Its matched early
FF record reduces failing pairs from 472 to 299, representing 212 actual
net pairs, but still reaches 1.075905098 V on a floating AP path.
The [common-edge comparison](common-edge-control.png) shows which shared
excursions improve and which remain. V8 stops before TT/weights; a structural
AP discharge experiment is the next separate source, with no inherited pass.
That V9 experiment passes SS (RL12/start 38.4/95.6 ps; maximum voltage
0.977265105 V), but early FF still has 279 failing pairs. Its
[AP comparison](ap-discharge-effects.png) shows positive retention removed
and a new -30.20 mV AP excursion; command-buffer negative swing worsens.
V9 is not promoted and stops before TT/weights. The next experiment tests
physical AP capacitance against the remaining 4.4 ps SS start margin.
V10's AP capacitance passes SS (RL12/start 38.3/96.4 ps), while early FF
still has 272 failing pairs. AP and HIB negative swings decrease, but
SS start develops 34.4 mV TOP overshoot and SS reference charge increases.
Its sampling-assist successor V11 was then compared with V10 under the
same announced conservative settings. Both pass SS, but V11 still fails
269 early-FF pairs versus V10's 272: its maximum falls to 1.056374 V,
while the phase pass path returns the assist gate to the higher digital
clock level. SS reference charge rises by 89.826 fC. Neither is promoted.
V12 adds a physical reference-powered phase inverter for that pass path.
It removes all 55 sampling-assist and 12 MID-PMOS failing pairs in the
same early window, but still fails 205/3420 pairs: the largest voltage
is now 1.063648 V in the assist control chain. SS still passes; reference
charge and PHI_S load increase. Its [matched waveform comparison](https://github.com/many-question/ADC-12b-100M/blob/adc-cdac-many-question-v16-history-20261031/design/xtor/adc_cdac/many-question-codex/assist-phase-reference-effects.png)
retains both the local improvement and the later control-node failure.
Existing V4 TT saves do not permit assigning its total excess to a phase.
N4's TT evidence does not transfer to any changed case.
The [first passing private SS comparison](https://github.com/many-question/ADC-12b-100M/blob/20d4d8896dc8d9b94206b7c928e8e5e255b5c511/design/xtor/adc_cdac/many-question-codex/balanced-predrive-ss-screen.png)
and complete source/evidence identifiers are in the ledger.

The complete earlier report and every historical diagnostic figure remain
in the [immutable history snapshot](https://github.com/many-question/ADC-12b-100M/tree/6a4bf94977db967dbd27ef47669d5d3d25735477/design/xtor/adc_cdac/many-question-codex),
also retained by tag `adc-cdac-many-question-history-20261031`.
The [N4 TT evidence tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-n4-tt-20261030)
and [pre-N4 history tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-pre-n4-20261030)
preserve the actual clean simulation commits and prior failures. Frozen inputs,
scripts, geometry validation and recovery/hash manifests are retained privately;
large waveform retention is limited to the evidence listed above. This compaction
changes no circuit or official result.
The [V9 history snapshot](https://github.com/many-question/ADC-12b-100M/tree/20d4d8896dc8d9b94206b7c928e8e5e255b5c511/design/xtor/adc_cdac/many-question-codex),
tagged `adc-cdac-many-question-v9-history-20261031`, additionally preserves
every report and figure through V9. Three earlier figures are now linked
there to keep the current candidate within its 2 MB limit; their bytes
were verified against the snapshot before removal from this checkout.

The subsequent matched V12/V13 private tests are generated from the merged
official flow. V13 strengthens only the second-stage high-command and
assist inverters, retaining their connections and all capacitors. SS passes;
early FF falls from 205 to 175 failing pairs, with no added failures and
maximum voltage reduced to 1.021300057 V. D1 undershoot improves, but
NOFF/BN and other paths remain outside the limit. The first FF attempts
lacked voltage saves and are retained as unverified; complete-voltage reruns
provide these conclusions. See [control-node comparison](control-clamp-comparison.png)
and the evidence ledger. V13 stops before expensive downstream expansion.

Formal spec notice [#98](https://github.com/many-question/ADC-12b-100M/issues/98)
is acknowledged. The frequency-tool announcement #96 was checked, including
its two-tone self-test: installed SFDR is 80.00 dB. V14 subsequently removes
the remaining observed control-chain failures and retains passing SS,
but still fails 157 early-FF pairs. Independent V15 reduces BN undershoot
yet fails SS RL12 at 44.8 ps and two SS voltage pairs; it is not expanded.

V16 balances the NAND N devices and reaches SS RL12/start 39.7/96.5 ps,
but still fails 123 early-FF terminal pairs. Its 0.3 ps RL12 margin has not
been confirmed by a convergence comparison. Two independent V16 children
identify further tradeoffs: V17 reduces FF failures to 95, with no new pair,
but fails SS RL12 at 41.0 ps. V18 removes four assist-device failures but
adds eight output-device failures (127 total), while SS reference charge
rises from 1.992429 to 3.056424 pC. Neither proceeds to TT or longer-window
qualification. The [matched decision waveforms](next-controls-tradeoffs.png)
and the ledger retain these failures; selected V17/V18 signals support the
displayed comparisons, not a repeat of their original full-DUT audit.

The next NAND stack-order trials V19/V20 improve SS RL12 to 37.7/39.2 ps
but introduce an internal BN undershoot and approximately 1.10 V FF
MNB0 drain/source peaks. They are rejected despite better settling.
Their new explicit-save runs preserve every required DUT terminal node
while recording only 285/497 SS/FF signals; no blanket current save or
duplicate full-wave cache is used.
