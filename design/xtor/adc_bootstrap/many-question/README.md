# adc_bootstrap candidate many-question: ready module evidence

**Candidate status: ready; results are self-reported.** Circuit content hash `f9330137569bdf81`. All 45 standard DC and 45 standard tracking records are fresh on main `33337c6`: **9/9 limited specifications pass, BST-07 is reported, and coverage is 318/318**. Eight DC and three tracking numerical comparisons retain their passing applicable criteria and disclosed limitations. The project lead's [#67 disposition](https://github.com/many-question/ADC-12b-100M/issues/67#issuecomment-6500083531) explicitly excludes body pairs from current acceptance and removes that readiness block. Ready means complete for comparison under CONTRIBUTING; lead verification, selection and formal mixed-top regression remain separate. The optional SS-low-hot top pilot and real-CDAC interface limitations are retained below.

The circuit uses **20 thin-oxide MOS and eight MOM capacitors**, with the complete drawing embedded as RNL in `adc_bootstrap.scs`. MAUX connects CBN to VIN through the limited startup control before MTRK fully turns on. This reduces the SS-low-cold MTRK drain/source peak from 1.039716 V in the preceding public circuit to 0.996974 V here. CMD distributes the switching transient across the discharge stack; the long precharge device retains the reduction in high-temperature leakage.

Three small clock-coupled capacitors control switching feedthrough. CFF connects PHI_BBF to PHI_BB, CBI connects PHI_BBI to PHI_B, and CCONT connects PCP to PHI_BB. CBI suppresses the first buffer stage's negative excursion. CCONT counters the PCP positive excursion; reducing it from a tested 2.90 fF to 1.46 fF avoids a later MXFER gate/source violation. MCSTART remains 0.5 µm: larger tested sizes introduced cold-corner violations or exceeded the then-current TT current criterion. Specification 0.8.0 now reports that current without an acceptance limit.

All changed dimensions were callback-normalized before simulation. CFF uses 6 fingers of length 1 µm on layers 1–6, approximately 2.90249 fF. CBI and CCONT use the same finger geometry on layers 1–3, approximately 1.46055 fF each. CBG and CMD use 12 fingers of length 5 µm on layers 1–6, approximately 30.3137 fF each; CDN uses 20 fingers of length 5 µm, approximately 52.653 fF. Finger width and spacing are 50 nm throughout. Callback payloads and device models remain private.

## Rerun for the numerics change

All 90 records were rerun on main `c6152d2` (spec 0.9.0, #95, notice #97) with the netlist unchanged: every `tran` at `errpreset=conservative`, ADCToolbox `cd72061`, `aps`. All 45 + 45 corners still pass. The numbers and numerical settings in the sections below are the earlier records, kept as history.

| Spec | Limit | Worst corner | Worst value |
|---|---:|---|---:|
| BST-03 turn-off | <= 60 ps | `ss_low_125` | 59.602 ps |
| BST-05 SFDR | >= 82 dBc | `ss_low_125` | 85.00 dBc |
| BST-06 SNDR | >= 78 dB | `ss_low_m40` | 84.65 dB |
| BST-01 minimum boost | >= 0.72 V | `ff_low_125` | 0.73404 V |
| BST-02 boost variation | <= 40 mV | `ff_high_125` | 35.585 mV |
| BST-04 turn-on | <= 300 ps | `ss_low_m40` | 231.27 ps |

Cross-checks (`traponly`, 1 ps; DC also reltol 1e-7, vabstol 10 nV): tracking at the three corners differs by at most 0.31 dB SFDR and 0.27 dB SNDR, DC at the eight corners by at most 0.26 ps turn-off and 2.42 ps turn-on. BST-03's 0.40 ps margin is the smallest one.

## Complete standard DC sweep

Fresh standard-flow DC runs use specification 0.6.0 and the approved numerical configuration from [#49](https://github.com/many-question/ADC-12b-100M/issues/49), integrated through [#53](https://github.com/many-question/ADC-12b-100M/pull/53). The explicit view is `adc_bootstrap=xtor:many-question`. All 45 unique primary corners pass every applicable limit. Each original official JSON and its three measurement figures are committed under `results/adc_bootstrap/tb_bootstrap_dc/xtor-many-question/`.

| DC metric | Worst primary result | Corner | Limit |
|---|---:|---|---:|
| Minimum boost | 0.734025962 V | `ff_low_125` | >= 0.72 V |
| Boost variation | 35.581543 mV | `ff_high_125` | <= 40 mV |
| Turn-off | 59.524581 ps | `ss_low_125` | <= 60 ps |
| Turn-on | 229.944229 ps | `ss_low_m40` | <= 300 ps |
| TT average current (BST-07) | 48.567152 µA | `tt_nom_27` | Reported only |
| TT PHI_B input capacitance | 11.244909 fF | `tt_nom_27` | <= 16 fF |
| TT PHI_BB input capacitance | 7.525217 fF | `tt_nom_27` | <= 16 fF |
| Largest checked absolute gs/gd/ds voltage | 0.998681198 V | `fs_high_125` | <= 1 V |

Current is reported at TT nominal / 27 °C; the input-capacitance limits apply there. Per [#81](https://github.com/many-question/ADC-12b-100M/issues/81), BST-07 has no acceptance upper bound; 50 µA remains an architecture budget only. The reported single-instance TT power is 43.710437 µW. Two instances plus the allocated 8 fF wiring give estimated PHI_B / PHI_BB driver loads of 30.489817 / 23.050434 fF, below the 40 fF allocation for each phase.

The unchanged 290 ns stimulus, 50-ohm source, reference switch/load and project measurements cover the complete five-process, three-supply and three-temperature matrix. The generic SOA plan covers 20 DUT MOS and the reference switch: 63 gs/gd/ds pairs per run, checked through startup and switching. Independent remeasurement reproduces every recorded primary metric; all 2,835 primary pair/corner peaks pass. Body-related pairs are outside that current plan and are reviewed separately below. All input hashes, staged decks, raw captures, actual numerical settings and figures were checked. The 45 primary logs report effective reltol=1e-8, vabstol=1e-8 and conservative; requested reltol is 1e-7. Primary configured and largest saved steps are 1 ps (apart from floating-point representation).

Original records retain `git=710ce5d`, `git_clean=true`, mode APS, the circuit hash and their numerical cross-check metadata. The four sources are `20261029-121318-36ca-tb_bootstrap_dc`, `20261029-124822-d354-tb_bootstrap_dc`, `20261029-121328-e518-tb_bootstrap_dc`, `20261029-124832-b23b-tb_bootstrap_dc`. All data was retrieved and the unique remote directories' removal verified. Inputs and Git remained frozen through recording. At the initial submission, all 45 JSONs and 135 figures were byte-identical to the official outputs; that stage remains at `archive/adc-bootstrap-dc45-b195f7d`. The current JSONs contain the audited official dependency migration described below. Raw data and the detailed audit remain private.

## Representative DC numerical checks

Eight fresh primary/alternate pairs cover the limiting boost, variation, turn-off, turn-on, SOA and TT current/input-capacitance conditions. Every applicable electrical limit passes in both settings. The unchanged standard test requests 1 ps / traponly / conservative for the primary, and 0.5 ps / gear2only / conservative for its alternate. All sixteen logs report effective reltol=1e-8 and voltage tolerance=1e-8.

| Corner | Primary / alternate turn-off (ps) | Primary / alternate turn-on (ps) | Largest exact pair-peak change (mV) | Alternate largest saved interval (ps) |
|---|---:|---:|---:|---:|
| `ff_high_125` | 35.807431 / 35.801677 | 143.502690 / 143.668911 | 0.010821 | 0.5 |
| `ff_low_125` | 40.947852 / 40.874826 | 167.614319 / 167.417421 | 0.008134 | 0.5 |
| `fs_high_125` | 39.348446 / 39.338951 | 169.719570 / 169.943262 | 0.013469 | 1.0 |
| `fs_high_m40` | 33.803711 / 33.794245 | 140.167761 / 140.164514 | 0.003968 | 0.5 |
| `ss_high_m40` | 40.344911 / 40.333461 | 155.561047 / 155.285377 | 0.013060 | 0.5 |
| `ss_low_125` | 59.524581 / 59.587332 | 220.429607 / 220.210388 | 0.007555 | 0.5 |
| `ss_low_m40` | 55.423499 / 55.348278 | 229.944229 / 230.134495 | 0.006282 | 0.5 |
| `tt_nom_27` | 41.379384 / 41.306873 | 156.666047 / 157.058746 | 0.003073 | 1.0 |

**Observed step/first-event differences limit the convergence evidence.** In the FS-high-hot and TT-nominal alternate runs, the log requests maxstep=0.5 ps but the saved waveform contains one 1 ps interval at 5.010–5.011 ns. The first PHI_B fall and first startup sample occur 1 ps later than in the primary; the other 28 sample timestamps agree. The seven samples actually used by the original DC boost measurement (indices 4, 8, 12, 16, 20, 24, 28) have identical timestamps in all eight pairs. The remaining six pairs have identical timestamps for all 29 samples and a largest saved interval of 0.5 ps.

The initial private audit failure on the saved-step check and subsequent raw-data review are retained privately, and the official JSON preserves the configured and observed step values and the sample-time differences. Every one of the 63 gs/gd/ds pairs was independently checked over the entire saved transient in both runs, including startup, with zero violations under those criteria. The largest change of a corresponding exact peak is 0.013469 mV. Across all sixteen runs the largest checked gs/gd/ds voltage is 0.998681198 V, and the worst turn-off is 59.587332 ps. At these two intervals, terminal-voltage endpoint changes are below 1e-14 V; endpoint agreement does not establish the waveform inside the unsaved interval. CLK and PHI_S were not saved by the original testbench, so the first-event mechanism is not fully established. These observations do not establish strict 0.5 ps coverage throughout those two alternates or waive any official criterion.

No captures were aligned, interpolated or rewritten to remove these differences. The stimulus, load, numerical requests, measurement functions and electrical limits remain those of the approved standard flow.

## Earlier private DC history

The earlier same-hash exploratory sweep covered 45 primary corners and four alternate cases, all passing their applicable limits. Its original captures, measurements and audit remain separate from the fresh standard records above. The earlier circuit and tracking history is preserved by tag `archive/adc-bootstrap-pr25-17dd993`.

## Complete standard tracking sweep

**45/45 standard primary records pass** over the complete five-process, three-supply and three-temperature matrix. The lowest SFDR is 85.077394 dBc at `ss_low_125`; the lowest SNDR is 84.480775 dB at `ss_low_m40`. Limits remain 82 dBc and 78 dB. Every selected JSON record and its official spectrum figure are committed under `results/adc_bootstrap/tb_bootstrap_track/xtor-many-question/`.

The unchanged standard runner has completed three representative primary/alternate comparisons, including the minimum-SFDR and minimum-SNDR corners:

| Corner | Primary SFDR / SNDR (dBc / dB) | 0.5 ps / gear2 SFDR / SNDR (dBc / dB) | Sample difference RMS / maximum (µV) |
|---|---:|---:|---:|
| `ff_high_125` | 100.297047 / 97.061710 | 100.315767 / 97.452442 | 2.426666 / 3.785004 |
| `ss_low_m40` | 87.864199 / 84.480775 | 87.942043 / 84.578936 | 1.471096 / 2.305258 |
| `ss_low_125` | 85.077394 / 84.759671 | 85.030887 / 84.751815 | 1.438738 / 2.212097 |

All three comparisons use 256 samples with identical timestamps. Logs report reltol=1e-7, vabstol=1e-8 and moderate; primary maxstep is 1 ps with traponly, alternate maxstep is 0.5 ps with gear2only. The full waveform is not saved, so the recorded observed maximum step is null; the configured maximum and accepted steps come from the original simulator log.

Sources are `20261029-050406-a36d-tb_bootstrap_track` (two primaries and two alternates), `20261029-055023-1a68-tb_bootstrap_track` (22 primaries), `20261029-062340-8233-tb_bootstrap_track` (21 primaries), and `20261029-095216-1966-tb_bootstrap_track` (SS-low-cold primary repeated with its alternate). The selected SS-low-cold JSON is the entire later cross-checked record; metadata was not transplanted onto the earlier primary. Both primaries were independently remeasured and compared. Their captures and the complete comparison remain private.

All standard records retain `git=1478a35`, `git_clean=true`, actual numerical settings, cross-check differences and current input hashes. Each staged testbench and deck was checked against the standard generator; every primary and alternate was remeasured from its original capture with the unchanged official functions. Completed-capture previews agree with the final records. All run data was retrieved and the unique remote directories' removal verified. Inputs and Git remained frozen throughout recording, under a two-Spectre limit.

## Dependency audit after the system baseline update

At the previous dependency-migration stage, the branch incorporated [#48](https://github.com/many-question/ADC-12b-100M/pull/48), [#57](https://github.com/many-question/ADC-12b-100M/pull/57) and [#62](https://github.com/many-question/ADC-12b-100M/pull/62), with main then at `3f1f7ce`. Bootstrap specification 0.7.0 changed candidate-selection metadata; its ports, operating load, electrical limits and test definitions remained identical to 0.6.0. The later 0.8.0 readiness audit is described below. Bootstrap selection remains `none` in current main.

An independent audit rebuilt all 90 module jobs and compared each prepared testbench with its original staged input. The reachable circuit files, original parameters and existing global values are unchanged. The added `cdac_behav=1` global is unused by either module test. The changed reference, CDAC and SAR model files are unreachable from these module testbenches; the changed architecture version and extra DAC waits are not read by their preparation or measurements.

The merged official `adcflow rehash --block adc_bootstrap --view xtor-many-question` implementation first completed a dry run with **90 eligible, 0 stale**, then performed the migration. A per-record audit verifies that only dependency metadata changed: DC records now list seven reached inputs, tracking records four, and both record an empty set of architecture keys. Every metric, verdict, parameter, global value, original Git/date, numerical cross-check and migration history remains identical. All **180 evidence PNGs** are byte-identical. `meta.rehashed` records this separate operation at `55b81d1`; no simulation was rerun or relabeled. All 90 records pass the current dependency checks.

## Body-terminal observations and project disposition: #67

All 53 retained standard DC logs contain body-source, body-drain and gate-body model operating-range warnings. The project lead [closed #67 with an explicit disposition](https://github.com/many-question/ADC-12b-100M/issues/67#issuecomment-6500083531): body pairs are not acceptance conditions at present, these warnings are expected for this topology, and they do not block ready or require a redesign for this point. BST-08 remains unchanged: absolute gs/gd/ds at most 1.0 V throughout the transient. This is the project's acceptance scope, with no waiver; it is distinct from an independently established process-reliability qualification. The warnings and original evidence are retained.

MDHI is connected `(VG AVDD DU VSS)` and MDUP `(VG VG DU VSS)`, in drain/gate/source/body order. Both bodies are grounded in the standard DC test, so their signed Vbs is `-V(DU)`. Read-only review of all 45 primary and eight alternate saved waveforms gives a largest absolute Vbs for these two devices of **1.770898645 V at FS-high / 27 °C**, at 245.105287658 ns. At that instant Vb=0 V, Vs=1.770898645 V, Vd=1.859837503 V, and the MDHI / MDUP gates are 0.99 / 1.859837503 V. These are simulated circuit voltages, not published process limits. The eight numerical pairs reproduce their Vbs peaks within 0.748 µV; numerical agreement itself is not a reliability rating. Other body-related observations remain outside the current project checks under the linked disposition. Detailed waveforms, source hashes, model-specific thresholds and logs remain private.

The previous body-related readiness hold is removed. The earlier official electrical records, numerical limitations, warning audit and failure history remain intact; none has been relabeled as independent reliability verification.

## Matched SS-low-hot top pilot

A fresh all-behavioral control and a run with only this bootstrap at transistor level completed sequentially under one allocated Spectre slot. Both froze source **`a78a9d1`**, including main `3f1f7ce`, and retain their original clean-source provenance. The sources are `20261029-213718-2f13-tb_top_sine` and `20261029-215631-871f-tb_top_sine`. Raw inputs and outputs were retrieved, remote/local hashes verified, and unique run-directory removal checked before recording ended. Top records remain private to preserve this candidate PR's path scope.

| SS-low-hot metric | Behavioral control | Bootstrap mixed |
|---|---:|---:|
| ENOB (bit) | 10.831940507 | 10.873827358 |
| SNDR (dB) | 66.968281851 | 67.220440695 |
| SFDR (dBc) | 84.967890961 | 81.119893672 |
| TOP-10 spike count | 0 | 0 |
| Maximum sine-fit residual (LSB) | 2.215550678 | 2.211888839 |
| Maximum conversion time (ns) | 2.819435 | 2.845443 |
| Total power (mW) | 13.720489549 | 13.755795001 |

Both pass every applicable top criterion. Independent remeasurement reproduces the records. All 18 shared dependency files match; stimulus, load, measurement and thresholds are unchanged. Each capture has continuous indices 1–2049: indices 1–1024 calibrate the weights, 1025–2048 are judged independently, and 2049 is unused. The footer has 2050 clocks and 2049 RDY events; its final unfinished conversion is outside the judged window, with no missing interior cycles.

The standard test uses 49.70703125 MHz, -1 dBFS, 20 GHz noise bandwidth and seed 1. `noise_en=1` and `cdac_behav=1` in both runs; device noise changes from 0 in the control to 1 in the mixed run. A single-seed difference does not isolate a particular noise contribution. Executed logs report moderate / traponly, reltol=1e-3 and voltage abstol=1e-6, with configured maxstep=410.52 ns. Mean accepted steps are 5.42824 / 5.51790 ps, respectively; internal waveforms were not saved, so the actual maximum saved interval and internal mixed terminal-voltage envelopes are unavailable.

**Optional pilot numerical follow-up remains.** Both logs contain four VA convergence warnings during initial-condition solving and five printed trapezoidal-ringing notices, with suppression. The mixed run additionally reports LTE relaxation on D0 and a VA convergence warning at 2.57764 µs, during calibration conversion 255 (clock 2.575009717 µs to RDY 2.577741 µs). Calibration effects can propagate into fitted weights and the judged record; rc=0 and zero TOP-10 spikes do not prove absence of numerical influence. Mixed body-source, body-drain and gate-body warnings are also present and suppressed, so the printed count is not a total occurrence count or duration. Complete logs and the warning/capture correlation are retained privately. This optional reference pilot is not formal mixed-top signoff or a prerequisite for module ready under CONTRIBUTING §9.2. Further diagnostic runs require coordinated scheduling; none has started.

## Current-specification readiness audit

The branch was rebased onto main **`33337c6`**, which includes specification 0.8.0 and [#81](https://github.com/many-question/ADC-12b-100M/issues/81). The original pre-rebase stage is preserved at `archive/adc-bootstrap-pr25-887209a`. The circuit, all **90 result JSONs and 180 evidence PNGs are byte-identical** to that archive. Original simulation Git/date, metrics, numerical settings and cross-check metadata remain unchanged. Both official `rehash --dry-run` and `rehash` report **0 changes, 90 already valid, 0 stale**.

All 90 jobs were rebuilt for comparison: parameters and original globals agree. Added `cdac_behav=1` and `comp_behav=1` globals are unused by every reached bootstrap input. The shared meter-reader refactor reproduces the original current values from all 53 retained DC meter files. Current judgments give **317/317 limited spec/corner passes plus the one required reported BST-07 value**, for total coverage **318/318**. The 2,835 primary gs/gd/ds pair/corner peaks and eight DC / three tracking comparisons remain intact. The two isolated 1 ps alternate saved intervals are still disclosed; no full 0.5 ps coverage is claimed for those two runs. No simulation was rerun for this readiness update.

## Lead verification, selection and interface follow-up

The [bootstrap/CDAC interface constraints](INTERFACE.md) document the reference load, measured voltage and turn-off margins, and the gate-charge/Ron information needed from the real CDAC. The behavioral CDAC has no physical VG gate-charge model, so mixed-top testing does not replace that interface validation.

Only the SS-low-hot reference pair has run. The other six sine quick corners, duty-cycle regression and LF test are outside this completed module evidence. Lead verification and the required formal mixed-top regression determine eligibility for selection under CONTRIBUTING §10; they do not change the meaning of candidate ready. The pilot slot has been released. Future joint CDAC work must incorporate its actual bottom-plate dynamics, gate charge and phase ordering. Candidate selection and transistor signoff are not claimed.

The older SS-low-hot control from `75e7a0f` / main `11fe593` remains archived with its original 10.324003109-bit TOP-01 failure; it no longer matches the new system baseline. Main also contains an all-behavioral SS-low-hot record from clean `3460c8c`, with ENOB 10.831940507 bit and zero spikes. The current comparison above uses the newly executed local control at `a78a9d1`; it does not relabel or replace either historical record.

The official `migrate-candidate` command moved this design and its 45 tracking records into candidate `many-question`. Result changes were limited to view/path labels, corresponding `meta.files` keys and explicit `meta.migrated`; metrics, verdicts, original Git provenance, simulation-input hashes and spectrum pixels were preserved. The RNL package reference was adjusted for the extra directory level without changing the circuit hash. Historical captures retain their original provenance and any staleness.

Readiness validation on the latest included main passes `adcflow check all` with no errors or warnings and **408 tests, 1 deselected**. Candidate path/author checks constrain this PR to its own candidate and results; CI is tracked on the submitted head. The unchanged complete RNL was previously rendered and visually inspected. The separate flow baselines are not transistor-level acceptance evidence.
