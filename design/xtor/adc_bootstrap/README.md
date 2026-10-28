# adc_bootstrap development evidence

**Status: xtor-wip.** Circuit content hash `f9330137569bdf81`. Six representative DC corners pass all applicable limits under the explicit private settings below. This stage still needs expanded PVT coverage, same-hash numerical cross-checks, tracking and mixed top-level acceptance.

The circuit uses **20 thin-oxide MOS and eight MOM capacitors**, with the complete drawing embedded as RNL in `adc_bootstrap.scs`. MAUX connects CBN to VIN through the limited startup control before MTRK fully turns on. This reduces the SS-low-cold MTRK drain/source peak from 1.039716 V in the preceding public circuit to 0.996974 V here. CMD distributes the switching transient across the discharge stack; the long precharge device retains the reduction in high-temperature leakage.

Three small clock-coupled capacitors control switching feedthrough. CFF connects PHI_BBF to PHI_BB, CBI connects PHI_BBI to PHI_B, and CCONT connects PCP to PHI_BB. CBI suppresses the first buffer stage's negative excursion. CCONT counters the PCP positive excursion; reducing it from a tested 2.90 fF to 1.46 fF avoids a later MXFER gate/source violation. MCSTART remains 0.5 µm: larger tested sizes introduced cold-corner violations or exceeded the TT current limit.

All changed dimensions were callback-normalized before simulation. CFF uses 6 fingers of length 1 µm on layers 1–6, approximately 2.90249 fF. CBI and CCONT use the same finger geometry on layers 1–3, approximately 1.46055 fF each. CBG and CMD use 12 fingers of length 5 µm on layers 1–6, approximately 30.3137 fF each; CDN uses 20 fingers of length 5 µm, approximately 52.653 fF. Finger width and spacing are 50 nm throughout. Callback payloads and device models remain private.

## Completed representative DC evidence

These are private staged simulations of this exact circuit hash, using the original 290 ns stimulus, 50-ohm source and reference switch/load, project measurement functions and unchanged specification 0.5.0 limits. Requested settings are reltol=1e-7, vabstol=1e-8, maxstep=1 ps, traponly, errpreset=conservative. Logs report **effective transient reltol=1e-8**. The generic SOA checker evaluates all 63 terminal pairs of 20 DUT MOS plus the reference switch, over the whole transient including startup and switching.

| Corner | min boost (V) | variation (mV) | off (ps) | on (ps) | AVDD (µA) | PHI_B / PHI_BB (fF) | SOA violations / pairs | max abs. V (V) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tt_nom_27` | 0.862540 | 13.794 | 41.379 | 156.666 | 48.567 | 11.245 / 7.525 | 0/63 | 0.97800 |
| `ss_low_125` | 0.775052 | 13.534 | 59.525 | 220.430 | 58.316 | 11.033 / 7.614 | 0/63 | 0.95167 |
| `ss_low_m40` | 0.785622 | 10.031 | 55.423 | 229.944 | 37.071 | 9.491 / 7.220 | 0/63 | 0.99697 |
| `ss_high_m40` | 0.961469 | 10.166 | 40.345 | 155.561 | 47.488 | 11.075 / 7.351 | 0/63 | 0.99825 |
| `fs_high_m40` | 0.950412 | 14.209 | 33.804 | 140.168 | 49.022 | 11.993 / 7.435 | 0/63 | 0.99725 |
| `fs_high_125` | 0.921178 | 27.062 | 39.348 | 169.720 | 129.514 | 12.486 / 7.736 | 0/63 | 0.99868 |

All applicable DC limits pass in these six rows. Current and clock-input-capacitance limits apply only at TT. The SS-low-hot turn-off margin is approximately 0.475 ps and still needs the new hash's finer-step check. Exact worst stresses are 0.998247131 V at SS-high-cold, 0.996974147 V at SS-low-cold, 0.997253479 V at FS-high-cold and 0.998681198 V at FS-high-hot.

Source: `20261029-044015-9a5503-bootstrap-control-trim-v050`, cases suffixed `pcp_m13_cbi_m13`. The entire run was retrieved and its unique remote directory removed. Every one of the 63 peak values and peak times at each of these six corners matches the independent full-pair preview exactly. Raw waveforms, samples and logs remain private. Selected-pair previews are never substituted for the complete SOA result.

The current default generated DC testbench does not yet specify these numerical settings. [#49](https://github.com/many-question/ADC-12b-100M/issues/49) tracks their integration into the shared flow. These rows are not formal default-flow acceptance records. Ten additional corners and four same-hash 0.5 ps/gear checks are running separately; they are not included in the completed table.

## Tracking and remaining validation

No tracking result is claimed for this new hash yet. The preceding public circuit `e07b810975de733d` had passing FF-hot and SS-low-hot tracking captures, but those captures do not validate this circuit. Required work remains: this hash's convergence comparisons, all 45 DC and tracking corners, representative tracking cross-checks with recorded numerical provenance, and mixed top-level acceptance on the coordinated flow. No formal transistor signoff JSON is supplied by this stage note.

The branch is synchronized with main `ad5134e` ([#50](https://github.com/many-question/ADC-12b-100M/pull/50)). Its periodic-Hann drawing correction was applied to five retained historical tracking records using official `remeasure --redraw`; all metrics, verdicts, capture hashes and original provenance were verified unchanged. Those historical results retain their circuit hashes and any staleness. #50 does not resolve the separate DC numerical-configuration issue #49.

Repository validation for this stage: `adcflow check all` reports no errors or warnings, generated files are current, the complete RNL was rendered and visually inspected, and tests pass: **188 passed, 1 deselected**.
