# Recorded evidence and current validity

After merging main `33337c6` (spec v0.6.0, [notice #78](https://github.com/many-question/ADC-12b-100M/issues/78)), current official checks mark **45 delay records stale and 47 other records fresh**: kickback 45, TT noise 1 and TT mismatch 1. All original result JSONs, figures and source commits are preserved. The delay/reset/energy values below are historical v0.5.0 evidence, not fresh v0.6.0 results. No new simulation was run. [REFRESH.md](REFRESH.md) gives the dependency audit and deferred combined refresh plan.

The recorded source was clean before each official test. All jobs used APS with one Spectre job at a time. The source remained electrically frozen across the tests. These are self-reported results; the candidate remains WIP and is not selected.

| Test | Corner coverage | Source commit |
|---|---:|---|
| tb_comp_delay | 45/45 | `36cdfb3` |
| tb_comp_kickback | 45/45 | `01fcb5c` |
| tb_comp_offset_mc | 1/1 | `2dc3d80` |
| tb_comp_noise | 1/45 | `5089a93` |

Runner content hash of adc_comp.scs: `150dd81755a64d66`. The result JSON files preserve the full reached-file hashes, settings and estimator provenance.

| Recorded TT metric (delay-derived rows are stale) | Value |
|---|---:|
| Noise rms | 187.108 uV |
| Noise 95% profile-likelihood interval | [179.33, 195.28] uV |
| Systematic offset magnitude | 0.00747647 mV |
| Mismatch sigma (sample standard deviation) | 1.898 mV |
| Valid / failed mismatch samples | 50 / 0 |
| Delay at 1 / 30 mV | 56.937 / 44.921 ps |
| Reset | 28.900 ps |
| Historical v0.5.0 AVDD window-average energy normalized to 400 ps | 187.299 fJ |
| Input / CLKC capacitance | 19.313 / 15.156 fF |
| Differential kickback | 0.386579 uV |
| Estimated external clock-driver charge energy | 12.277 fJ |
| AVDD plus that clock-driver estimate | 199.575 fJ |

The preserved v0.5.0 energy_fJ is average AVDD power over the complete 14.5 ns mixed-amplitude delay test, multiplied by 400 ps. The window includes the initial 100 ps and spans 36.25 clock periods, so this is neither a dedicated 1 mV measurement nor exactly total energy divided by 36 decisions. See [issue #75](https://github.com/many-question/ADC-12b-100M/issues/75). These records use spec v0.5.0. PR #76 is merged as `33337c6`; spec v0.6.0 now measures AVDD charge x VDD / 36 over 100 ps–14.5 ns with the unchanged mixed-amplitude sequence. CMP-10 is reported-only, with no 200 fJ acceptance limit. The 45 old delay records are stale because the reached testbench changed. No v0.6.0 energy measurement is recorded for this candidate. Old values and verdicts remain unchanged in their original JSONs; neither rehashing nor relabeling makes them new-definition evidence. The clock-driver estimate is C_CLKC * VDD^2, reported separately from measured AVDD energy; it does not replace a system energy measurement. The noise test uses the standard 17 levels x 512 decisions, seed 1 and 50 GHz bandwidth. Mismatch uses all 50 local TT samples with seed 6303; no samples are discarded. The reported noise interval is conditional on the probit model. The largest probability residual in the tabulated fit is +0.0862 at 0 uV; the official residual plot is retained.

| Formal test | Failed specifications in recorded jobs |
|---|---|
| delay | CMP-08: ss_low_125, ss_low_27, ss_low_m40, ss_nom_125 |
| kickback | None in recorded jobs |
| offset_mc | None in recorded jobs |
| noise | None in recorded jobs |

| All-corner functional extreme | Value | Corner |
|---|---:|---|
| tdelay_1mV_ps | 96.118 | ss_low_m40 |
| treset_ps | 39.889 | ss_low_125 |
| tau_reg_ps | 5.419 | ss_low_m40 |
| wrong_decisions | 0.000 | ff_high_125 |
| kickback_uV | 0.932 | tt_low_27 |
| cin_fF | 20.678 | ff_low_m40 |
| cin_clkc_fF | 16.757 | ff_high_125 |

CMP-12 and CMP-14 impose their capacitance limits at TT only. Non-TT capacitance extrema above are reported for visibility and are not treated as additional formal failures.

## Saved-waveform interface audit

Read-back of the 45 preserved v0.5.0 delay waveforms finds 36 rising and 36 falling clock edges per corner, 1620 reset responses in total, and 0 invalid/wrong late decisions among 1260 samples with |vd| >= 100 uV. The late sample is 150 ps after the rising 50% clock crossing; a valid output has one side above 80% VDD and the other below 20%. Reset plateaus at 100–170 ps after the falling 50% clock crossing stay below 10% VDD. These checks supplement the official metric extraction.

No simultaneous-high saved points are present in this audit. This statement concerns the saved standard-setting waveforms, not a continuous-time guarantee. [Issue #77](https://github.com/many-question/ADC-12b-100M/issues/77) tracks a shared measurement gap demonstrated by the separate Miyahara candidate; its dual-high result is not attributed to this StrongARM circuit. This audit does not establish real receiver threshold margins, first-event noise/mismatch behavior or closed-loop SAR/CDAC performance.


The [new #77 decision](https://github.com/many-question/ADC-12b-100M/issues/77#issuecomment-6514624643) requires one output crossing 50% VDD and the losing output staying below 30% VDD during each of the 36 evaluation windows. The implementation is not present in this audited main. The existing audit does not report the new losing-output peak metric. Absence of simultaneous-high saved samples does not establish compliance with the new 30% losing-output limit. The combined refresh remains deferred as described in [REFRESH.md](REFRESH.md).

## Separate 1 mV energy diagnostic

This is supplemental evidence, not official acceptance JSON. Both candidates use VCM = 0.49 V, alternating +/-1 mV, 400 ps clocks, 10 fF per output, TT at 0.9 V / 27 C, and noise off. The DC operating point starts with CLKC low; the initial 0–100 ps remains in reset. The actual AVDD current-meter integral runs from 100 ps to 14.5 ns: exactly 36 complete decision/reset cycles. The first evaluation is included and no warmup decisions are discarded. Energy is measured directly from this preserved diagnostic run, not inferred from the mixed-sequence result. Fine settings are maxstep = 0.5 ps, traponly, reltol = 1e-6 and vabstol = 1e-8. The existing mixed-sequence control below uses the same frozen diagnostic source and fine numerical settings. Comparison with the official number also changes numerical settings; it must not be attributed solely to the stimulus or integration window.

| Fine diagnostic | Integration window | AVDD energy normalized to one cycle |
|---|---|---:|
| Mixed-amplitude sequence | 0–14.5 ns, 36.25 periods | 189.380 fJ |
| Fixed +/-1 mV | 100 ps–14.5 ns, 36 complete cycles | 188.069 fJ |

| Frozen diagnostic source SHA-256 | AVDD energy / cycle | Wrong decisions |
|---|---:|---:|
| `1b6c812a2dbdcdaef57b727194822dc179fbd934b519d932a3586225ebc74ff5` | 188.069 fJ | 0 / 36 |

The diagnostic audit verifies both PWL levels, the saved testbench hash and the 14.4 ns meter window. Every one of the 36 decisions is checked at 100 ps after the clock 50% crossing, including the cycles omitted by the mixed-sequence small-input error mask. Measured fixed-1mV AVDD energy plus the separately estimated clock-driver charge energy is 200.346 fJ; this sum is not an official acceptance metric.

## Supplemental device-voltage failures

These fine checks cover |Vgs|, |Vgd| and |Vds| for all 23 MOS devices (69 terminal pairs). The failing corner repeats use the same frozen circuit and mixed-amplitude excitation.

| Corner | Maximum step | Violating pairs / 69 | Maximum absolute voltage | Reported worst device / pair |
|---|---:|---:|---:|---|
| ff_high_125 | 0.5ps | 8 / 69 | 1.02083 V | MRQP / gd |
| ff_high_m40 | 0.5ps | 21 / 69 | 1.05376 V | MRDP / ds |
| ff_high_m40 | 0.25ps | 21 / 69 | 1.05376 V | MRDP / ds |

## Remaining limits

Fine supplemental checks in [CHARACTERIZATION.md](CHARACTERIZATION.md) fail the 1.0 V device-voltage requirement. The 0.25 ps maximum-step repeat preserves the cold-corner violation. Passing a formal metric or the repository checks does not remove this failure. Transient-noise corner coverage is 1/45; all-corner noise, wider input common-mode/differential coverage and full-corner SOA are not established. No qualified-energy winner is claimed.

Historical commands (each result set was archived, hash-verified and committed before the next test; these commands were not rerun during this audit):

```text
python -m adcflow sim tb_comp_delay --view adc_comp=xtor:many-question-strongarm --corners all --mode aps --jobs 1 --keep
python -m adcflow sim tb_comp_kickback --view adc_comp=xtor:many-question-strongarm --corners all --mode aps --jobs 1 --keep
python -m adcflow sim tb_comp_offset_mc --view adc_comp=xtor:many-question-strongarm --corners typ --mode aps --jobs 1 --keep
python -m adcflow sim tb_comp_noise --view adc_comp=xtor:many-question-strongarm --corners typ --mode aps --jobs 1 --keep
```
