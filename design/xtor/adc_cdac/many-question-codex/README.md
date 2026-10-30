# CDAC candidate

This WIP 28 nm HPC+ candidate retains the formal N4 source and its complete
TT evidence. All 17 required TT metrics pass; the first slow-corner screen
fails RL12 and conversion-start settling. Successor experiments remain
independent until they earn their own validation; no old result is relabeled.

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

## Formal evidence on N4

| Check | Result |
|---|---|
| TT weights/calibration | 5/5 pass; Cs 2.065012 pF, full scale 0.993034 V, calibration margin 0.369061 LSB, calibrated ENOB loss 0.000364369 bit |
| TT settling/charge/load | 10/10 pass; RL12/start 35.3/83.4 ps, tau 9.120184 ps, Qref 1.124389535 pC |
| TT tracking | SFDR 86.417966859 dBc and SNDR 84.523548567 dB pass; prescribed numerical comparison differs by 0.000307850/0.000215801 dB |
| Official ss_low_125 | Full scale, RL5, tau and droop pass; RL12 47.4 ps >40 ps and start 117.7 ps >100 ps fail |

All 12 official result/figure files remain unchanged. Required coverage is
9/17 requirements complete across their corner sets, 23/369 specification-
corner results, with five self-reported records. Other corners, project-lead
verification and mixed top-level regression remain incomplete. Status stays
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
is stopped. Its [matched waveform comparison](matched-output-family-screen.png)
and the ledger retain the independent source and evidence. The next case
returns to nominal-threshold outputs and coordinates output/enable sizing.

The complete earlier report and every historical diagnostic figure remain
in the [immutable history snapshot](https://github.com/many-question/ADC-12b-100M/tree/6a4bf94977db967dbd27ef47669d5d3d25735477/design/xtor/adc_cdac/many-question-codex),
also retained by tag `adc-cdac-many-question-history-20261031`.
The [N4 TT evidence tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-n4-tt-20261030)
and [pre-N4 history tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-pre-n4-20261030)
preserve the actual clean simulation commits and prior failures. Raw data,
frozen inputs, scripts, geometry validation and recovery/hash manifests are
retained privately. This compaction changes no circuit or official evidence.
