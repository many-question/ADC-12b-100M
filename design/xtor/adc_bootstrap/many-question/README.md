# adc_bootstrap candidate many-question: development evidence

**Candidate status: wip.** Circuit content hash `f9330137569bdf81`. All 45 standard tracking corners and three representative alternate runs pass. All 45 private DC primary corners and four alternate runs also pass. Formal DC and mixed top-level validation remain outstanding.

The circuit uses **20 thin-oxide MOS and eight MOM capacitors**, with the complete drawing embedded as RNL in `adc_bootstrap.scs`. MAUX connects CBN to VIN through the limited startup control before MTRK fully turns on. This reduces the SS-low-cold MTRK drain/source peak from 1.039716 V in the preceding public circuit to 0.996974 V here. CMD distributes the switching transient across the discharge stack; the long precharge device retains the reduction in high-temperature leakage.

Three small clock-coupled capacitors control switching feedthrough. CFF connects PHI_BBF to PHI_BB, CBI connects PHI_BBI to PHI_B, and CCONT connects PCP to PHI_BB. CBI suppresses the first buffer stage's negative excursion. CCONT counters the PCP positive excursion; reducing it from a tested 2.90 fF to 1.46 fF avoids a later MXFER gate/source violation. MCSTART remains 0.5 µm: larger tested sizes introduced cold-corner violations or exceeded the TT current limit.

All changed dimensions were callback-normalized before simulation. CFF uses 6 fingers of length 1 µm on layers 1–6, approximately 2.90249 fF. CBI and CCONT use the same finger geometry on layers 1–3, approximately 1.46055 fF each. CBG and CMD use 12 fingers of length 5 µm on layers 1–6, approximately 30.3137 fF each; CDN uses 20 fingers of length 5 µm, approximately 52.653 fF. Finger width and spacing are 50 nm throughout. Callback payloads and device models remain private.

## Complete private DC sweep

The 45 primary corners cover five process, three supply and three temperature conditions. Every applicable limit of specification 0.5.0 passes. The unchanged generic SOA checker covers all 63 terminal pairs of 20 DUT MOS plus the reference switch throughout startup and switching: 2,835 pair/corner peaks, zero violations.

| DC metric | Worst result | Corner | Limit |
|---|---:|---|---:|
| Minimum boost | 0.734025962 V | `ff_low_125` | ≥0.72 V |
| Boost variation | 35.581542847 mV | `ff_high_125` | ≤40 mV |
| Turn-off | 59.524580635 ps | `ss_low_125` | ≤60 ps |
| Turn-on | 229.944229313 ps | `ss_low_m40` | ≤300 ps |
| Largest absolute terminal voltage | 0.998681198 V | `fs_high_125` | ≤1 V |
| TT average current | 48.567152 µA | `tt_nom_27` | ≤50 µA |
| TT PHI_B / PHI_BB input capacitance | 11.244909 / 7.525217 fF | `tt_nom_27` | ≤16 fF each |

Current and input-capacitance limits apply only at TT nominal / 27 °C. Two instances plus the allocated 8 fF wiring give estimated PHI_B / PHI_BB driver loads of 30.489817 / 23.050434 fF, below the 40 fF allocation for each phase.

The original 290 ns stimulus, 50-ohm source, reference switch/load and project measurement functions are unchanged. Private primary settings request reltol=1e-7, vabstol=1e-8, maxstep=1 ps, traponly and conservative. All 45 logs report effective transient reltol=1e-8, and all saved-step maxima were checked against 1 ps. Exact peaks above use the complete saved data. Generic SOA diagnostics may identify the start of the peak plateau rather than the exact maximum's timestamp.

Sources are `20261029-044015-9a5503-bootstrap-control-trim-v050` (six cases suffixed `pcp_m13_cbi_m13`), `20261029-045040-29685d-bootstrap-cbi-extended-v050` (ten `cbi_extended` cases), and `20261029-050355-82a86f-bootstrap-cbi-remaining-v050` (29 `cbi_remaining` cases). All data was retrieved and each unique remote directory's removal verified. Independent full-pair previews at 19 corners match all local peak values and exact peak timestamps. Raw samples, waveforms, logs, models and callback payloads remain private.

Four same-hash 0.5 ps / gear2only comparisons also pass: SS high/cold, SS low/cold, SS low/hot and FS high/cold. Each checks all 63 terminal pairs. The largest absolute change of a corresponding peak is 0.013060 mV; the largest turn-off change is 0.075221 ps. SS-low-hot turn-off changes from 59.524581 to 59.587332 ps, leaving 0.412668 ps of margin. The 29 sample timestamps agree exactly in all four comparisons, and the largest RMS sample difference is 0.0192 µV. These are four representative comparisons, not alternate coverage of all 45 corners.

The explicit configuration approved in [#49](https://github.com/many-question/ADC-12b-100M/issues/49) is now integrated through [#53](https://github.com/many-question/ADC-12b-100M/pull/53). Fresh transistor DC runs under that standard flow remain outstanding; the private sweep is not relabeled as formal evidence. Formal reruns will also cross-check FS-high-hot (maximum SOA), FF-low-hot (minimum boost), FF-high-hot (maximum boost variation) and TT nominal (the applicable current/input-capacitance limits), for eight representative DC comparisons in total.

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

Required work: rerun formal DC with eight representative convergence checks using `--view adc_bootstrap=xtor:many-question`, then run mixed top-level `tb_top_sine` at seven quick corners with only this candidate replacing the behavioral bootstrap. The mixed test retains 1024 calibration and 1024 independent judged conversions, the official coherent frequency and noise settings. It has been prepared locally but not simulated; its pending model changes must be reviewed before launch. Formal transistor signoff is not claimed.

The branch incorporates main `17205ec`, including the numerical configuration and candidate workflow. The official `migrate-candidate` command moved this design and its 45 tracking records into candidate `many-question`. It only changed result view/path labels, corresponding `meta.files` keys and added `meta.migrated`; metrics, verdicts, original Git provenance, simulation-input hashes and spectrum pixels are preserved. The RNL package reference was adjusted for the extra directory level; this comment-only drawing path does not affect the circuit hash. The complete pre-migration circuit and tracking history remains reachable through tag `archive/adc-bootstrap-pr25-17dd993`. Historical captures keep their original circuit hashes and any staleness.

Repository validation: `adcflow check all` reports no errors or warnings, generated files are current, the complete RNL was rendered and visually inspected, and tests pass: **266 passed, 1 deselected**. The separate #49 flow checks and behavioral baselines do not constitute circuit acceptance.
