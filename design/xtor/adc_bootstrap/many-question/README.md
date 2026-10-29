# adc_bootstrap candidate many-question: development evidence

**Candidate status: wip.** Circuit content hash `f9330137569bdf81`. All 45 standard DC primary corners and all 45 standard tracking corners pass their applicable electrical limits. Eight DC and three tracking numerical comparisons also pass those limits. Two DC alternates have saved-step / first-event differences, described below as limitations of the convergence evidence. Mixed top-level validation remains outstanding.

The circuit uses **20 thin-oxide MOS and eight MOM capacitors**, with the complete drawing embedded as RNL in `adc_bootstrap.scs`. MAUX connects CBN to VIN through the limited startup control before MTRK fully turns on. This reduces the SS-low-cold MTRK drain/source peak from 1.039716 V in the preceding public circuit to 0.996974 V here. CMD distributes the switching transient across the discharge stack; the long precharge device retains the reduction in high-temperature leakage.

Three small clock-coupled capacitors control switching feedthrough. CFF connects PHI_BBF to PHI_BB, CBI connects PHI_BBI to PHI_B, and CCONT connects PCP to PHI_BB. CBI suppresses the first buffer stage's negative excursion. CCONT counters the PCP positive excursion; reducing it from a tested 2.90 fF to 1.46 fF avoids a later MXFER gate/source violation. MCSTART remains 0.5 µm: larger tested sizes introduced cold-corner violations or exceeded the TT current limit.

All changed dimensions were callback-normalized before simulation. CFF uses 6 fingers of length 1 µm on layers 1–6, approximately 2.90249 fF. CBI and CCONT use the same finger geometry on layers 1–3, approximately 1.46055 fF each. CBG and CMD use 12 fingers of length 5 µm on layers 1–6, approximately 30.3137 fF each; CDN uses 20 fingers of length 5 µm, approximately 52.653 fF. Finger width and spacing are 50 nm throughout. Callback payloads and device models remain private.

## Complete standard DC sweep

Fresh standard-flow DC runs use specification 0.6.0 and the approved numerical configuration from [#49](https://github.com/many-question/ADC-12b-100M/issues/49), integrated through [#53](https://github.com/many-question/ADC-12b-100M/pull/53). The explicit view is `adc_bootstrap=xtor:many-question`. All 45 unique primary corners pass every applicable limit. Each original official JSON and its three measurement figures are committed under `results/adc_bootstrap/tb_bootstrap_dc/xtor-many-question/`.

| DC metric | Worst primary result | Corner | Limit |
|---|---:|---|---:|
| Minimum boost | 0.734025962 V | `ff_low_125` | >= 0.72 V |
| Boost variation | 35.581543 mV | `ff_high_125` | <= 40 mV |
| Turn-off | 59.524581 ps | `ss_low_125` | <= 60 ps |
| Turn-on | 229.944229 ps | `ss_low_m40` | <= 300 ps |
| TT average current | 48.567152 µA | `tt_nom_27` | <= 50 µA |
| TT PHI_B input capacitance | 11.244909 fF | `tt_nom_27` | <= 16 fF |
| TT PHI_BB input capacitance | 7.525217 fF | `tt_nom_27` | <= 16 fF |
| Largest absolute terminal voltage | 0.998681198 V | `fs_high_125` | <= 1 V |

Current and input-capacitance limits apply at TT nominal / 27 °C. Two instances plus the allocated 8 fF wiring give estimated PHI_B / PHI_BB driver loads of 30.489817 / 23.050434 fF, below the 40 fF allocation for each phase.

The unchanged 290 ns stimulus, 50-ohm source, reference switch/load and project measurements cover the complete five-process, three-supply and three-temperature matrix. The generic SOA plan covers 20 DUT MOS and the reference switch: 63 terminal pairs per run, checked through startup and switching. Independent remeasurement reproduces every recorded primary metric; all 2,835 primary pair/corner peaks pass. All input hashes, staged decks, raw captures, actual numerical settings and figures were checked. The 45 primary logs report effective reltol=1e-8, vabstol=1e-8 and conservative; requested reltol is 1e-7. Primary configured and largest saved steps are 1 ps (apart from floating-point representation).

Original records retain `git=710ce5d`, `git_clean=true`, mode APS, the circuit hash and their numerical cross-check metadata. The four sources are `20261029-121318-36ca-tb_bootstrap_dc`, `20261029-124822-d354-tb_bootstrap_dc`, `20261029-121328-e518-tb_bootstrap_dc`, `20261029-124832-b23b-tb_bootstrap_dc`. All data was retrieved and the unique remote directories' removal verified. The input tree and Git remained frozen through recording; the submitted records and figures are byte-for-byte copies of the official outputs. Raw data and the detailed audit remain private.

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

The initial private audit failure on the saved-step check and subsequent raw-data review are retained privately, and the official JSON preserves the configured and observed step values and the sample-time differences. Every one of the 63 device/terminal pairs was independently checked over the entire saved transient in both runs, including startup, with zero violations. The largest change of a corresponding exact peak is 0.013469 mV. Across all sixteen runs the largest terminal voltage is 0.998681198 V, and the worst turn-off is 59.587332 ps. At these two intervals, terminal-voltage endpoint changes are below 1e-14 V; endpoint agreement does not establish the waveform inside the unsaved interval. CLK and PHI_S were not saved by the original testbench, so the first-event mechanism is not fully established. These observations do not establish strict 0.5 ps coverage throughout those two alternates or waive any official criterion.

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

## Remaining acceptance

The planned mixed `tb_top_sine` validation uses seven quick corners with only this candidate replacing the behavioral bootstrap, retaining 1024 calibration and 1024 independent judged conversions, the official coherent frequency, noise switches and seed. It has been prepared locally but not simulated. By coordination decision, new mixed runs wait for [#48](https://github.com/many-question/ADC-12b-100M/pull/48) to merge, followed by an input-dependency and result-validity audit against the new baseline. Affected module tests will be rerun as required, retaining the original evidence and provenance. The system baseline issue [#35](https://github.com/many-question/ADC-12b-100M/issues/35) will also be checked before launch. Candidate selection and transistor signoff are not claimed.

The existing SS-low-hot behavioral control from clean `75e7a0f` / main `11fe593` has been checked against the current mixed preflight: 17 common electrical inputs, architecture, prepared parameters/globals and electrical testbench content agree. Its original capture hashes are preserved and remeasurement reproduces ENOB 10.324003109 bit, failing TOP-01. The normalized deck differs only in the bootstrap view and required includes. This reuses an existing single-seed control with its original provenance; it is not a new baseline run or an isolated bootstrap-noise measurement. Comparability must be rechecked if shared models change.

The official `migrate-candidate` command moved this design and its 45 tracking records into candidate `many-question`. Result changes were limited to view/path labels, corresponding `meta.files` keys and explicit `meta.migrated`; metrics, verdicts, original Git provenance, simulation-input hashes and spectrum pixels were preserved. The RNL package reference was adjusted for the extra directory level without changing the circuit hash. Historical captures retain their original provenance and any staleness.

Repository validation: `adcflow check all` reports no errors or warnings, generated files are current, the complete RNL was rendered and visually inspected, and tests pass: **266 passed, 1 deselected**. The separate flow baselines are not transistor-level acceptance evidence.
