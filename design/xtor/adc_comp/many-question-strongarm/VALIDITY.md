# Output validity and complete 45-corner failure baseline

Spec v0.7.0, after merged [PR #82](https://github.com/many-question/ADC-12b-100M/pull/82), [notice #84](https://github.com/many-question/ADC-12b-100M/issues/84) and [energy notice #78](https://github.com/many-question/ADC-12b-100M/issues/78). All 45 corners were simulated from clean source `424d10a78ce75a1ef45d121575a9eac07a1ebd93` with the frozen electrical SHA-256 `150dd81755a64d66f582a84fd734462f5ad2c8b31ce4399b6507481d30372119`. These are self-reported measurements; the candidate remains WIP and unselected.

**CMP-15 passes at all 45 corners, with 0/1620 violating evaluation cycles.** 0 cycles have both outputs reaching 50% VDD. There are 0 undecided cycles and 0 wrong decisions under the CMP-09 input mask. The worst CMP-16 losing-output peak is **21.236684% VDD** at `sf_low_m40`, cycle 18, vd = -10 uV, OUTP, 90.992 ps after the rising clock 50% crossing.

Each evaluation interval runs from CLKC rising 50% to the next falling 50% crossing. The first output reaching 50% wins. The losing peak includes every saved point and linearly interpolated interval boundaries; both outputs deciding or a losing peak >=30% VDD is a violation. These saved-waveform results do not prove an unsampled continuous-time bound. CMP-16 is reported-only. Undecided cycles are handled separately by CMP-09 for |vd| >=100 uV and by the SAR timeout below that.

Cycle numbers are one-based. Cycles 1–18 use +100 mV, -100 mV, +30 mV, -30 mV, +10 mV, -10 mV, +3 mV, -3 mV, +1 mV, -1 mV, +300 uV, -300 uV, +100 uV, -100 uV, +30 uV, -30 uV, +10 uV, -10 uV. Cycles 19–36 repeat that sequence. Each linked JSON contains every violating cycle, polarity, losing peak, both-decided flag and all 36 losing peaks.

| Corner / official JSON | CMP-15 cycles | CMP-16 (% VDD) | Worst cycle | Largest saved step (ps) | Reset (ps) | AVDD energy (fJ/cycle) |
|---|---:|---:|---:|---:|---:|---:|
| [ff_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_high_125.json) | 0 | 18.037777 | 18 | 29.5162 | 25.216709 | 349.332865 |
| [ff_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_high_27.json) | 0 | 15.919073 | 18 | 33.6259 | 23.282592 | 247.542209 |
| [ff_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_high_m40.json) | 0 | 15.297615 | 35 | 33.4574 | 22.042182 | 215.671281 |
| [ff_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_low_125.json) | 0 | 18.337067 | 36 | 25.3803 | 29.535739 | 220.196815 |
| [ff_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_low_27.json) | 0 | 18.853588 | 35 | 29.1088 | 27.667616 | 159.773189 |
| [ff_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_low_m40.json) | 0 | 16.894255 | 36 | 26.4467 | 25.995456 | 140.711121 |
| [ff_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_nom_125.json) | 0 | 18.535504 | 18 | 25.6738 | 27.177424 | 279.188571 |
| [ff_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_nom_27.json) | 0 | 17.383289 | 35 | 30.8129 | 24.879994 | 199.946362 |
| [ff_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ff_nom_m40.json) | 0 | 16.307954 | 36 | 30.0723 | 23.804225 | 175.441221 |
| [fs_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_high_125.json) | 0 | 12.163907 | 18 | 25.9793 | 28.673678 | 291.009149 |
| [fs_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_high_27.json) | 0 | 12.037785 | 36 | 32.3046 | 25.855004 | 231.728046 |
| [fs_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_high_m40.json) | 0 | 10.394314 | 18 | 30.6372 | 24.817770 | 209.103502 |
| [fs_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_low_125.json) | 0 | 13.449422 | 36 | 24.2861 | 34.353139 | 191.456057 |
| [fs_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_low_27.json) | 0 | 13.130734 | 35 | 26.0413 | 33.544989 | 153.098511 |
| [fs_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_low_m40.json) | 0 | 12.067086 | 17 | 28.3865 | 32.082819 | 139.355611 |
| [fs_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_nom_125.json) | 0 | 13.483527 | 18 | 26.3170 | 31.355425 | 238.049014 |
| [fs_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_nom_27.json) | 0 | 12.093599 | 36 | 26.7621 | 28.904170 | 189.450579 |
| [fs_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/fs_nom_m40.json) | 0 | 10.524743 | 18 | 28.3500 | 27.485823 | 171.853312 |
| [sf_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_high_125.json) | 0 | 16.934351 | 18 | 24.7647 | 27.920304 | 297.093678 |
| [sf_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_high_27.json) | 0 | 15.205881 | 17 | 24.8641 | 26.110455 | 233.783372 |
| [sf_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_high_m40.json) | 0 | 13.923596 | 35 | 25.4431 | 24.994927 | 211.342090 |
| [sf_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_low_125.json) | 0 | 18.894829 | 18 | 23.0322 | 33.421369 | 191.522400 |
| [sf_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_low_27.json) | 0 | 17.998963 | 17 | 24.7992 | 32.425088 | 153.459548 |
| [sf_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_low_m40.json) | 0 | 21.236684 | 18 | 23.8744 | 30.420822 | 139.660188 |
| [sf_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_nom_125.json) | 0 | 17.655709 | 36 | 23.9401 | 30.899651 | 239.937866 |
| [sf_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_nom_27.json) | 0 | 14.627383 | 18 | 25.2997 | 27.622629 | 190.514295 |
| [sf_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/sf_nom_m40.json) | 0 | 18.162708 | 18 | 24.4319 | 26.777736 | 173.583697 |
| [ss_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_high_125.json) | 0 | 11.093113 | 15 | 24.2772 | 32.129090 | 259.081715 |
| [ss_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_high_27.json) | 0 | 10.080677 | 18 | 26.5483 | 29.268041 | 223.774791 |
| [ss_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_high_m40.json) | 0 | 8.547658 | 36 | 24.1219 | 27.952364 | 208.549021 |
| [ss_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_low_125.json) | 0 | 13.124335 | 17 | 23.3697 | 39.888795 | 172.612626 |
| [ss_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_low_27.json) | 0 | 11.465262 | 18 | 22.4059 | 38.854023 | 149.895952 |
| [ss_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_low_m40.json) | 0 | 14.169949 | 18 | 23.0099 | 37.071163 | 139.438848 |
| [ss_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_nom_125.json) | 0 | 11.457537 | 18 | 25.8137 | 35.644217 | 212.937399 |
| [ss_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_nom_27.json) | 0 | 11.353699 | 17 | 24.9608 | 32.627434 | 185.089076 |
| [ss_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/ss_nom_m40.json) | 0 | 11.850370 | 17 | 23.4459 | 32.122921 | 172.303724 |
| [tt_high_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_high_125.json) | 0 | 14.889193 | 36 | 25.0559 | 28.727077 | 283.872718 |
| [tt_high_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_high_27.json) | 0 | 13.563227 | 35 | 26.1301 | 26.583517 | 230.809393 |
| [tt_high_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_high_m40.json) | 0 | 11.261900 | 36 | 27.9678 | 24.003667 | 209.664823 |
| [tt_low_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_low_125.json) | 0 | 16.218149 | 35 | 21.7157 | 34.642987 | 186.080090 |
| [tt_low_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_low_27.json) | 0 | 13.903558 | 36 | 25.5878 | 32.570738 | 152.162811 |
| [tt_low_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_low_m40.json) | 0 | 15.796882 | 18 | 23.9616 | 31.720734 | 139.189268 |
| [tt_nom_125](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_nom_125.json) | 0 | 15.478914 | 18 | 24.7073 | 31.435132 | 231.562122 |
| [tt_nom_27](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_nom_27.json) | 0 | 13.818931 | 36 | 25.7623 | 28.900132 | 188.590270 |
| [tt_nom_m40](../../../../results/adc_comp/tb_comp_delay/xtor-many-question-strongarm/tt_nom_m40.json) | 0 | 14.230133 | 36 | 27.5337 | 27.594574 | 172.097718 |

## Violating cycles by corner

| Corner | CMP-15 violating cycles | Both outputs reach 50% cycles |
|---|---|---|
| All 45 | None | None |

## Reset, energy and known device stress

CMP-08 fails in 4/45 corners: `ss_low_125` (39.888795 ps); `ss_low_27` (38.854023 ps); `ss_low_m40` (37.071163 ps); `ss_nom_125` (35.644217 ps). The worst reset is 39.888795 ps at `ss_low_125`; the limit is 35 ps.

TT CMP-10 is **188.590270 fJ/cycle**. Across 45 corners, energy ranges from 139.189268 fJ at `tt_low_m40` to 349.332865 fJ at `ff_high_125`. The AVDD meter integrates 100 ps–14.5 ns, exactly 36 complete cycles of the mixed-amplitude sequence; charge x VDD / 36 gives the reported value. There is no acceptance limit. External CLKC source energy is excluded. These are new simulations, not rescaled old results.

The earlier fine SOA failures below belong to the identical frozen circuit. They remain failures; the refreshed standard-step output-validity run is not a new fine SOA test. A shared corner does not by itself establish causation.

| Earlier fine SOA corner | Maximum absolute device voltage | Reported worst device/pair | Current CMP-15 count | Current CMP-16 (% VDD) | Current reset (ps) |
|---|---:|---|---:|---:|---:|
| ff_high_m40 | 1.05376 V | MRDP / ds | 0 | 15.297615 | 22.042182 |
| ff_high_125 | 1.02083 V | MRQP / gd | 0 | 18.037777 | 25.216709 |

The 0.25 ps cold-corner repeat preserved the voltage violation. [VERIFICATION.md](VERIFICATION.md) and [CHARACTERIZATION.md](CHARACTERIZATION.md) retain the fine settings and other prior results. No all-corner noise or full-corner SOA qualification is claimed.

## Priority structural direction

Rework the series input-drain precharge network to remove floating DPX/DNX intermediate nodes and give them a defined, bounded reset path, with controlled tail/precharge overlap. The known MRDP drain-source overshoot and slow-corner reset failures make this the first structural experiment. This is a repair hypothesis; preserve the observed CMP-15 pass while improving reset and terminal stress. Any added clamp or driver must be evaluated for reset, validity, device stress, noise, delay and total AVDD/clock energy.

This refresh changes no devices, sizing or connectivity. The direction above is a proposal for a later electrical revision, not a completed repair.
