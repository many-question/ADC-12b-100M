# adc_bootstrap development evidence

**Status: xtor-wip.** Circuit content hash `e07b810975de733d`. This is a stage design with all seven quick DC corners checked and two known SOA failures; it is not full-corner or top-level signoff.

The circuit uses 19 thin-oxide MOS and five MOM capacitors. A lower-leakage discharge stack reduces input-dependent loading. CMD shares the middle device's switching transient, while CDN limits the resulting excursion on the lower node. A longer precharge device reduces high-temperature boost variation. The local two-stage clock buffer, reset-gate limiter and startup-gate bleeder remain present. The complete drawing is embedded as RNL in `adc_bootstrap.scs`.

The chosen capacitor dimensions were callback-normalized before use: CMD has 10 fingers and CDN has 20, each with 5 µm finger length, 50 nm finger width/spacing and layers 1–6. Their normalized nominal capacitances are approximately 24.73 fF and 52.65 fF.

## Quick-corner DC evidence

These rows come from private staged simulations of this exact circuit hash, with the original 290 ns stimulus, 50-ohm source and reference switch/load. They use the project measurement functions and unchanged specification 0.5.0 limits. Requested settings are reltol=1e-7, vabstol=1e-8, maxstep=1 ps, traponly, errpreset=conservative. The logs report **effective transient reltol=1e-8**. Full transient waveforms cover startup and switching; the SOA checker evaluates all 60 terminal pairs of the 19 DUT MOS plus the reference switch.

| Corner | min boost (V) | variation (mV) | off (ps) | on (ps) | AVDD (µA) | PHI_B / PHI_BB (fF) | SOA violations / pairs | max abs. V (V) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tt_nom_27` | 0.863731 | 13.191 | 39.744 | 155.483 | 47.238 | 11.409 / 6.727 | 0/60 | 0.99632 |
| `ss_low_125` | 0.776025 | 13.090 | 57.158 | 218.369 | 56.801 | 11.111 / 6.492 | 0/60 | 0.96703 |
| `ff_high_m40` | 0.940162 | 18.340 | 29.573 | 120.241 | 47.566 | 12.366 / 7.007 | 0/60 | 0.99857 |
| `ff_high_125` | 0.898378 | 34.546 | 34.494 | 141.738 | 179.768 | 12.717 / 7.261 | 0/60 | 0.99478 |
| `ss_low_m40` | 0.786784 | 9.063 | 52.704 | 229.456 | 35.865 | 9.647 / 6.093 | 1/60 | 1.03972 |
| `fs_nom_27` | 0.860588 | 14.785 | 37.658 | 164.252 | 51.840 | 11.690 / 6.704 | 0/60 | 0.98014 |
| `sf_nom_27` | 0.866024 | 12.226 | 42.161 | 150.295 | 47.053 | 11.123 / 6.745 | 1/60 | 1.00480 |

Five of the seven quick corners pass all applicable DC limits. **BST-08 fails at SS-low-−40°C: MTRK |Vds| = 1.039716384 V; and at SF-nominal-27°C: MDMID |Vds| = 1.004798487 V.** The first peak occurs on entering track, when CBN falls to −147.906 mV while VIN is 891.811 mV. Current and input-capacitance limits apply only at TT; FS current is retained as a measurement without applying the TT-only limit.

The first four rows come from `20261029-014151-2fc97e-bootstrap-stack-compensation-r2-v050`, cases suffixed `capshare_pre100`; the three added rows come from `20261029-015753-fbdddb-bootstrap-capshare-validation-v050`, cases suffixed `pre100_quick`. Original samples, waveforms, logs and callback evidence remain private. Both runs were retrieved and their unique remote directories removed.

Same-hash TT and FF-cold checks with 0.5 ps/gear retain 0/60 SOA violations. Exact peak changes across all 60 corresponding terminal pairs are at most **0.010621 mV at TT / 0.002845 mV at FF-cold**. FF-cold maximum stress is 0.998573909 V primary / 0.998572801 V cross-check. TT logs maxstep=0.5 ps, but the saved waveform contains one 1 ps interval starting at 5.010 ns and its first sampler timestamp differs by 1 ps; these are preserved in the comparison. All other saved TT intervals are at most 0.5 ps. These passing-corner checks do not establish convergence or acceptance of the two failing corners.

The current generated default DC testbench does not yet specify these numerical settings. Shared-flow integration is tracked in [#49](https://github.com/many-question/ADC-12b-100M/issues/49). These exploratory rows must not be presented as results from that default flow. The preceding hash's half-step comparison does not establish convergence of this new circuit.

## Tracking and remaining validation

The current-hash tracking batch `20261029-015316-1b4ebe-candidate-track` has been fully retrieved and its unique remote directory removed. FF-hot gives **97.479161 dBc SFDR / 95.142933 dB SNDR / −95.584829 dBc THD**; SS-low-hot gives **85.511970 dBc SFDR / 85.355589 dB SNDR / −85.415397 dBc THD**. Both use all 256 samples, 1 ps/traponly and effective reltol=1e-7, and pass the tracking limits. These are private exploratory measurements, not formal acceptance records. Earlier candidates' tracking results are not assigned to this circuit. Required work includes repair of the two SOA failures, tracking numerical cross-checks, all 45 DC and tracking corners, and mixed top-level acceptance on the coordinated flow. No formal transistor signoff JSON is supplied by this stage note.

The spectrum drawing audit in [#47](https://github.com/many-question/ADC-12b-100M/issues/47) found symmetric-Hann drawing skirts on otherwise coherent captures. Official measurements use periodic Hann. Same-capture rectangular/periodic-Hann comparisons preserve the predecessor's strong third-harmonic failure; changing a drawing window does not remove that distortion. No shared estimator or limit is changed here.

After the frozen diagnostic batch was fully retrieved and measured, this branch synchronized with main `ad5134e` ([PR50](https://github.com/many-question/ADC-12b-100M/pull/50)). Bootstrap simulation input hashes are unchanged; among design/testbench simulation inputs, only the reference DC testbench changed. Official `remeasure --redraw` updated five retained historical tracking records across four private runs. Every metric, verdict, capture SHA256 and original provenance field was verified unchanged; only figures and `meta.redrawn` changed. Historical circuit hashes and any existing staleness remain in force. These redraws do not supply current-circuit acceptance. Local checks pass; tests after synchronization: 188 passed, 1 deselected.
