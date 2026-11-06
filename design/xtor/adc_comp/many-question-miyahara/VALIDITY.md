# Output validity and complete 45-corner failure baseline

Spec v0.7.0, after merged [PR #82](https://github.com/many-question/ADC-12b-100M/pull/82), [notice #84](https://github.com/many-question/ADC-12b-100M/issues/84) and [energy notice #78](https://github.com/many-question/ADC-12b-100M/issues/78). All 45 corners were simulated from clean source `a2e3509597563d607d2a873ed9cc5e9d667ccfff` with the frozen electrical SHA-256 `e8a0e3d3dc1366cd20f72c291397b352c8b9a6eeb87df618e41c49199372597a`. These are self-reported measurements; the candidate remains WIP and unselected.

**CMP-15 fails in 45/45 corners, with 1084/1620 violating evaluation cycles.** 108 cycles have both outputs reaching 50% VDD. There are 0 undecided cycles and 0 wrong decisions under the CMP-09 input mask. The worst CMP-16 losing-output peak is **52.820335% VDD** at `sf_high_27`, cycle 36, vd = -10 uV, OUTP, 55.309 ps after the rising clock 50% crossing.

Each evaluation interval runs from CLKC rising 50% to the next falling 50% crossing. The first output reaching 50% wins. The losing peak includes every saved point and linearly interpolated interval boundaries; both outputs deciding or a losing peak >=30% VDD is a violation. These saved-waveform results do not prove an unsampled continuous-time bound. CMP-16 is reported-only. Undecided cycles are handled separately by CMP-09 for |vd| >=100 uV and by the SAR timeout below that.

Cycle numbers are one-based. Cycles 1–18 use +100 mV, -100 mV, +30 mV, -30 mV, +10 mV, -10 mV, +3 mV, -3 mV, +1 mV, -1 mV, +300 uV, -300 uV, +100 uV, -100 uV, +30 uV, -30 uV, +10 uV, -10 uV. Cycles 19–36 repeat that sequence. Each linked JSON contains every violating cycle, polarity, losing peak, both-decided flag and all 36 losing peaks.

| Corner / official JSON | CMP-15 cycles | CMP-16 (% VDD) | Worst cycle | Largest saved step (ps) | Reset (ps) | AVDD energy (fJ/cycle) |
|---|---:|---:|---:|---:|---:|---:|
| [ff_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_high_125.json) | 24 | 48.494778 | 36 | 29.8754 | 15.482509 | 358.086160 |
| [ff_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_high_27.json) | 24 | 48.988570 | 18 | 36.5812 | 13.821406 | 251.880601 |
| [ff_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_high_m40.json) | 24 | 48.958777 | 17 | 39.0946 | 13.555150 | 218.672140 |
| [ff_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_low_125.json) | 28 | 47.900509 | 35 | 29.5884 | 17.673611 | 223.503118 |
| [ff_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_low_27.json) | 24 | 48.318766 | 36 | 29.4476 | 16.836396 | 158.329814 |
| [ff_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_low_m40.json) | 24 | 48.271569 | 17 | 35.7159 | 15.949350 | 138.289898 |
| [ff_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_nom_125.json) | 24 | 48.200853 | 17 | 33.9369 | 16.053452 | 284.675884 |
| [ff_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_nom_27.json) | 24 | 48.666587 | 17 | 34.5974 | 14.995948 | 200.818083 |
| [ff_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ff_nom_m40.json) | 24 | 48.646370 | 35 | 32.2320 | 14.236163 | 174.700173 |
| [fs_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_high_125.json) | 24 | 43.945984 | 18 | 28.2637 | 17.480398 | 295.327501 |
| [fs_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_high_27.json) | 24 | 44.655450 | 18 | 34.5653 | 15.903643 | 234.055938 |
| [fs_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_high_m40.json) | 24 | 44.655149 | 17 | 34.2609 | 15.244155 | 210.952606 |
| [fs_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_low_125.json) | 24 | 43.099223 | 36 | 27.1151 | 20.948464 | 192.878391 |
| [fs_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_low_27.json) | 24 | 43.612088 | 36 | 31.7643 | 19.546407 | 152.371872 |
| [fs_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_low_m40.json) | 24 | 43.637299 | 36 | 31.3174 | 19.555423 | 137.774093 |
| [fs_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_nom_125.json) | 24 | 43.516539 | 18 | 32.5294 | 18.209048 | 240.253716 |
| [fs_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_nom_27.json) | 24 | 44.149195 | 36 | 33.5773 | 17.480239 | 189.902193 |
| [fs_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/fs_nom_m40.json) | 24 | 44.172085 | 18 | 35.7892 | 17.208580 | 171.390143 |
| [sf_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_high_125.json) | 24 | 52.665401 | 18 | 30.0458 | 17.594734 | 304.905054 |
| [sf_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_high_27.json) | 24 | 52.820335 | 36 | 31.1047 | 16.273700 | 235.793271 |
| [sf_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_high_m40.json) | 24 | 52.377519 | 18 | 29.9020 | 15.252599 | 211.621091 |
| [sf_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_low_125.json) | 24 | 52.762634 | 17 | 27.1181 | 20.734264 | 192.577503 |
| [sf_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_low_27.json) | 24 | 52.772627 | 36 | 26.6705 | 20.143379 | 150.451284 |
| [sf_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_low_m40.json) | 24 | 52.361650 | 36 | 26.3753 | 19.668289 | 135.737924 |
| [sf_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_nom_125.json) | 24 | 52.663879 | 36 | 27.7602 | 19.013718 | 243.878496 |
| [sf_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_nom_27.json) | 24 | 52.804386 | 18 | 29.3979 | 17.732389 | 189.420224 |
| [sf_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/sf_nom_m40.json) | 24 | 52.408538 | 17 | 26.9984 | 17.071274 | 170.259522 |
| [ss_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_high_125.json) | 24 | 48.297002 | 18 | 28.9615 | 19.924985 | 262.400383 |
| [ss_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_high_27.json) | 24 | 48.450021 | 17 | 26.3995 | 18.619164 | 225.249923 |
| [ss_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_high_m40.json) | 24 | 48.203145 | 35 | 27.8971 | 17.654717 | 207.963860 |
| [ss_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_low_125.json) | 24 | 47.910238 | 35 | 28.1563 | 24.721438 | 173.006503 |
| [ss_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_low_27.json) | 24 | 47.975621 | 17 | 26.9066 | 23.669374 | 148.141341 |
| [ss_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_low_m40.json) | 24 | 47.640412 | 35 | 27.5938 | 23.446708 | 137.036701 |
| [ss_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_nom_125.json) | 24 | 48.088164 | 35 | 27.3427 | 21.499338 | 214.504888 |
| [ss_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_nom_27.json) | 24 | 48.223779 | 18 | 27.6404 | 20.568100 | 183.769079 |
| [ss_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/ss_nom_m40.json) | 24 | 47.965516 | 18 | 26.4836 | 19.797281 | 169.747139 |
| [tt_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_high_125.json) | 24 | 48.445214 | 36 | 31.1892 | 17.780943 | 288.829841 |
| [tt_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_high_27.json) | 24 | 48.803105 | 18 | 32.5716 | 16.407379 | 231.877723 |
| [tt_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_high_m40.json) | 24 | 48.567868 | 17 | 32.0802 | 15.481270 | 210.287936 |
| [tt_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_low_125.json) | 24 | 47.953768 | 35 | 29.6206 | 21.202516 | 186.968460 |
| [tt_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_low_27.json) | 24 | 48.196732 | 35 | 28.2039 | 20.280703 | 150.136060 |
| [tt_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_low_m40.json) | 24 | 47.990669 | 36 | 31.2243 | 19.423651 | 136.472597 |
| [tt_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_nom_125.json) | 24 | 48.216741 | 17 | 30.7596 | 19.146930 | 233.902230 |
| [tt_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_nom_27.json) | 24 | 48.521649 | 35 | 27.8333 | 17.786952 | 187.647444 |
| [tt_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-miyahara/tt_nom_m40.json) | 24 | 48.335162 | 17 | 31.1141 | 17.052639 | 170.259835 |

## Violating cycles by corner

| Corner | CMP-15 violating cycles | Both outputs reach 50% cycles |
|---|---|---|
| ff_high_125 | 7–18, 25–36 | None |
| ff_high_27 | 7–18, 25–36 | None |
| ff_high_m40 | 7–18, 25–36 | None |
| ff_low_125 | 5–18, 23–36 | None |
| ff_low_27 | 7–18, 25–36 | None |
| ff_low_m40 | 7–18, 25–36 | None |
| ff_nom_125 | 7–18, 25–36 | None |
| ff_nom_27 | 7–18, 25–36 | None |
| ff_nom_m40 | 7–18, 25–36 | None |
| fs_high_125 | 7–18, 25–36 | None |
| fs_high_27 | 7–18, 25–36 | None |
| fs_high_m40 | 7–18, 25–36 | None |
| fs_low_125 | 7–18, 25–36 | None |
| fs_low_27 | 7–18, 25–36 | None |
| fs_low_m40 | 7–18, 25–36 | None |
| fs_nom_125 | 7–18, 25–36 | None |
| fs_nom_27 | 7–18, 25–36 | None |
| fs_nom_m40 | 7–18, 25–36 | None |
| sf_high_125 | 7–18, 25–36 | 13–18, 31–36 |
| sf_high_27 | 7–18, 25–36 | 13–18, 31–36 |
| sf_high_m40 | 7–18, 25–36 | 13–18, 31–36 |
| sf_low_125 | 7–18, 25–36 | 13–18, 31–36 |
| sf_low_27 | 7–18, 25–36 | 13–18, 31–36 |
| sf_low_m40 | 7–18, 25–36 | 13–18, 31–36 |
| sf_nom_125 | 7–18, 25–36 | 13–18, 31–36 |
| sf_nom_27 | 7–18, 25–36 | 13–18, 31–36 |
| sf_nom_m40 | 7–18, 25–36 | 13–18, 31–36 |
| ss_high_125 | 7–18, 25–36 | None |
| ss_high_27 | 7–18, 25–36 | None |
| ss_high_m40 | 7–18, 25–36 | None |
| ss_low_125 | 7–18, 25–36 | None |
| ss_low_27 | 7–18, 25–36 | None |
| ss_low_m40 | 7–18, 25–36 | None |
| ss_nom_125 | 7–18, 25–36 | None |
| ss_nom_27 | 7–18, 25–36 | None |
| ss_nom_m40 | 7–18, 25–36 | None |
| tt_high_125 | 7–18, 25–36 | None |
| tt_high_27 | 7–18, 25–36 | None |
| tt_high_m40 | 7–18, 25–36 | None |
| tt_low_125 | 7–18, 25–36 | None |
| tt_low_27 | 7–18, 25–36 | None |
| tt_low_m40 | 7–18, 25–36 | None |
| tt_nom_125 | 7–18, 25–36 | None |
| tt_nom_27 | 7–18, 25–36 | None |
| tt_nom_m40 | 7–18, 25–36 | None |

## Reset, energy and known device stress

CMP-08 fails in 0/45 corners: none. The worst reset is 24.721438 ps at `ss_low_125`; the limit is 35 ps.

TT CMP-10 is **187.647444 fJ/cycle**. Across 45 corners, energy ranges from 135.737924 fJ at `sf_low_m40` to 358.086160 fJ at `ff_high_125`. The AVDD meter integrates 100 ps–14.5 ns, exactly 36 complete cycles of the mixed-amplitude sequence; charge x VDD / 36 gives the reported value. There is no acceptance limit. External CLKC source energy is excluded. These are new simulations, not rescaled old results.

The earlier fine SOA failures below belong to the identical frozen circuit. They remain failures; the refreshed standard-step output-validity run is not a new fine SOA test. A shared corner does not by itself establish causation.

| Earlier fine SOA corner | Maximum absolute device voltage | Reported worst device/pair | Current CMP-15 count | Current CMP-16 (% VDD) | Current reset (ps) |
|---|---:|---|---:|---:|---:|
| ff_high_m40 | 1.01599 V | MRQP / gd | 24 | 48.958777 | 13.555150 |
| ff_high_125 | 1.00488 V | MRQP / gd | 24 | 48.494778 | 15.482509 |

The 0.25 ps cold-corner repeat preserved the voltage violation. [VERIFICATION.md](VERIFICATION.md) and [CHARACTERIZATION.md](CHARACTERIZATION.md) retain the fine settings and other prior results. No all-corner noise or full-corner SOA qualification is claimed.

## Priority structural direction

Rework the native-output/reset interface while preserving the drain-triggered 15-MOS core. Evaluate a rail-restoring output stage with mutual exclusion and controlled reset isolation, so the physical losing output remains below 30% VDD and clock/reset feedthrough into the output reset devices is reduced. The observed loser excursions and MRQP gate-drain stress motivate this direction; they do not prove a shared cause. An ideal first-event latch alone cannot repair a physical losing-output excursion. Added delay, AVDD energy, clock load and noise must be measured before accepting a revision.

This refresh changes no devices, sizing or connectivity. The direction above is a proposal for a later electrical revision, not a completed repair.
