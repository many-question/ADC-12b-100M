# adc_bootstrap development evidence

**Status: xtor-wip.** Circuit content hash `e07b810975de733d`. This is a stage design with four representative DC corners checked; it is not full-corner or top-level signoff.

The circuit uses 19 thin-oxide MOS and five MOM capacitors. A lower-leakage discharge stack reduces input-dependent loading. CMD shares the middle device's switching transient, while CDN limits the resulting excursion on the lower node. A longer precharge device reduces high-temperature boost variation. The local two-stage clock buffer, reset-gate limiter and startup-gate bleeder remain present. The complete drawing is embedded as RNL in `adc_bootstrap.scs`.

The chosen capacitor dimensions were callback-normalized before use: CMD has 10 fingers and CDN has 20, each with 5 µm finger length, 50 nm finger width/spacing and layers 1–6. Their normalized nominal capacitances are approximately 24.73 fF and 52.65 fF.

## Representative DC evidence

These rows come from private staged simulations of this exact circuit hash, with the original 290 ns stimulus, 50-ohm source and reference switch/load. They use the project measurement functions and unchanged specification 0.5.0 limits. Requested settings are reltol=1e-7, vabstol=1e-8, maxstep=1 ps, traponly, errpreset=conservative. The logs report **effective transient reltol=1e-8**. Full transient waveforms cover startup and switching; the SOA checker evaluates all 60 terminal pairs of the 19 DUT MOS plus the reference switch.

| Corner | min boost (V) | variation (mV) | off (ps) | on (ps) | AVDD (µA) | PHI_B / PHI_BB (fF) | SOA violations / pairs | max abs. V (V) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tt_nom_27` | 0.863731 | 13.191 | 39.744 | 155.483 | 47.238 | 11.409 / 6.727 | 0/60 | 0.99632 |
| `ss_low_125` | 0.776025 | 13.090 | 57.158 | 218.369 | 56.801 | 11.111 / 6.492 | 0/60 | 0.96703 |
| `ff_high_m40` | 0.940162 | 18.340 | 29.573 | 120.241 | 47.566 | 12.366 / 7.007 | 0/60 | 0.99857 |
| `ff_high_125` | 0.898378 | 34.546 | 34.494 | 141.738 | 179.768 | 12.717 / 7.261 | 0/60 | 0.99478 |

All applicable DC limits pass in these four rows. Current and input-capacitance limits apply only at TT. The source run is `20261029-014151-2fc97e-bootstrap-stack-compensation-r2-v050`, cases suffixed `capshare_pre100`. Original samples, waves, numerical logs and normalized callback evidence are retained privately; the unique remote run was retrieved and removed.

The current generated default DC testbench does not yet specify these numerical settings. Shared-flow integration is tracked in [#49](https://github.com/many-question/ADC-12b-100M/issues/49). These exploratory rows must not be presented as results from that default flow. The preceding hash's half-step comparison does not establish convergence of this new circuit.

## Tracking and remaining validation

Current-hash FF-hot and SS tracking are in progress. Earlier candidates' tracking results are not assigned to this circuit. Required work includes this hash's numerical cross-checks, all 45 DC and tracking corners, and mixed top-level acceptance on the coordinated flow. No formal transistor signoff JSON is supplied by this stage note.

The spectrum drawing audit in [#47](https://github.com/many-question/ADC-12b-100M/issues/47) found symmetric-Hann drawing skirts on otherwise coherent captures. Official measurements use periodic Hann. Same-capture rectangular/periodic-Hann comparisons preserve the predecessor's strong third-harmonic failure; changing a drawing window does not remove that distortion. No shared estimator or limit is changed here.
