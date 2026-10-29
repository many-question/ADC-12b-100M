# Official test evidence

The recorded source was clean before each official test. All jobs used APS with one Spectre job at a time. The source remained electrically frozen across the tests. These are self-reported results; the candidate remains WIP and is not selected.

| Test | Corner coverage | Source commit |
|---|---:|---|
| tb_comp_delay | 45/45 | `cd9863b` |
| tb_comp_kickback | 45/45 | `c41a097` |
| tb_comp_offset_mc | 1/1 | `128b899` |
| tb_comp_noise | 1/45 | `fcf5c09` |

Runner content hash of adc_comp.scs: `e8a0e3d3dc1366cd`. The result JSON files preserve the full reached-file hashes, settings and estimator provenance.

| TT metric | Value |
|---|---:|
| Noise rms | 193.758 uV |
| Noise 95% profile-likelihood interval | [185.84, 202.07] uV |
| Systematic offset magnitude | 0.000199071 mV |
| Mismatch sigma (sample standard deviation) | 1.947 mV |
| Valid / failed mismatch samples | 50 / 0 |
| Delay at 1 / 30 mV | 47.513 / 38.755 ps |
| Reset | 17.787 ps |
| Official AVDD window-average energy normalized to 400 ps | 186.363 fJ |
| Input / CLKC capacitance | 19.310 / 14.924 fF |
| Differential kickback | 0.000485769 uV |
| Estimated external clock-driver charge energy | 12.089 fJ |
| AVDD plus that clock-driver estimate | 198.452 fJ |

The official energy_fJ is average AVDD power over the complete 14.5 ns mixed-amplitude delay test, multiplied by 400 ps. The window includes the initial 100 ps and spans 36.25 clock periods, so this is neither a dedicated 1 mV measurement nor exactly total energy divided by 36 decisions. See [issue #75](https://github.com/many-question/ADC-12b-100M/issues/75). These records use spec v0.5.0. The lead has decided to change the official meter to exactly 36 cycles and make energy reported-only; implementation is pending at the time of this evidence. The old records are preserved and will not be reinterpreted as the new definition. The clock-driver estimate is C_CLKC * VDD^2, reported separately from measured AVDD energy; it does not replace a system energy measurement. The noise test uses the standard 17 levels x 512 decisions, seed 1 and 50 GHz bandwidth. Mismatch uses all 50 local TT samples with seed 6303; no samples are discarded. The reported noise interval is conditional on the probit model. The largest probability residual in the tabulated fit is +0.0356 at 0 uV; the official residual plot is retained.

| Formal test | Failed specifications in recorded jobs |
|---|---|
| delay | None in recorded jobs |
| kickback | None in recorded jobs |
| offset_mc | None in recorded jobs |
| noise | None in recorded jobs |

| All-corner functional extreme | Value | Corner |
|---|---:|---|
| tdelay_1mV_ps | 76.793 | ss_low_m40 |
| treset_ps | 24.721 | ss_low_125 |
| tau_reg_ps | 7.395 | ss_low_m40 |
| wrong_decisions | 0.000 | ff_high_125 |
| kickback_uV | 0.049 | sf_nom_m40 |
| cin_fF | 20.677 | ff_low_m40 |
| cin_clkc_fF | 16.203 | ff_high_125 |

CMP-12 and CMP-14 impose their capacitance limits at TT only. Non-TT capacitance extrema above are reported for visibility and are not treated as additional formal failures.

## Saved-waveform interface audit

Read-back of the 45 official delay waveforms finds 36 rising and 36 falling clock edges per corner, 1620 reset responses in total, and 0 invalid/wrong late decisions among 1260 samples with |vd| >= 100 uV. The late sample is 150 ps after the rising 50% clock crossing; a valid output has one side above 80% VDD and the other below 20%. Reset plateaus at 100–170 ps after the falling 50% clock crossing stay below 10% VDD. These checks supplement the official metric extraction.

There are 454 saved points with both outputs above 50% VDD in 9 SF corners: `sf_high_125`, `sf_high_27`, `sf_high_m40`, `sf_low_125`, `sf_low_27`, `sf_low_m40`, `sf_nom_125`, `sf_nom_27`, `sf_nom_m40`. This overlap is an additional interface concern even though the official first-crossing decision metric, supplemental late-decision check and reset metrics pass; the official delay test does not separately judge one-hot output behavior. [Issue #77](https://github.com/many-question/ADC-12b-100M/issues/77) tracks this gap. [INTERFACE.md](INTERFACE.md) preserves the source, derived figure, crossing brackets and receiver-scope limits.

The frozen source repeat at `sf_low_m40` with maxstep 0.25 ps, traponly, reltol 1e-6 and vabstol 1e-8 finds 12 overlap intervals. The largest min(OUTP,OUTN) is 0.424097 V (0.523576 VDD); the longest linearly interpolated overlap is 26.091 ps. This supplemental result uses the same circuit and standard mixed-amplitude excitation.

## Separate 1 mV energy diagnostic

This is supplemental evidence, not official acceptance JSON. Both candidates use VCM = 0.49 V, alternating +/-1 mV, 400 ps clocks, 10 fF per output, TT at 0.9 V / 27 C, and noise off. The DC operating point starts with CLKC low; the initial 0–100 ps remains in reset. The actual AVDD current-meter integral runs from 100 ps to 14.5 ns: exactly 36 complete decision/reset cycles. The first evaluation is included and no warmup decisions are discarded. Energy is measured directly from this new run, not inferred from the mixed-sequence result. Fine settings are maxstep = 0.5 ps, traponly, reltol = 1e-6 and vabstol = 1e-8. The existing mixed-sequence control below uses the same frozen diagnostic source and fine numerical settings. Comparison with the official number also changes numerical settings; it must not be attributed solely to the stimulus or integration window.

| Fine diagnostic | Integration window | AVDD energy normalized to one cycle |
|---|---|---:|
| Mixed-amplitude sequence | 0–14.5 ns, 36.25 periods | 186.339 fJ |
| Fixed +/-1 mV | 100 ps–14.5 ns, 36 complete cycles | 187.192 fJ |

| Frozen diagnostic source SHA-256 | AVDD energy / cycle | Wrong decisions |
|---|---:|---:|
| `3b1537b6a7ef273ef9a9a2f7d3f0cf9fae3e404060245e592ea99e9ef7333b7a` | 187.192 fJ | 0 / 36 |

The diagnostic audit verifies both PWL levels, the saved testbench hash and the 14.4 ns meter window. Every one of the 36 decisions is checked at 100 ps after the clock 50% crossing, including the cycles omitted by the mixed-sequence small-input error mask. Measured fixed-1mV AVDD energy plus the separately estimated clock-driver charge energy is 199.280 fJ; this sum is not an official acceptance metric.

## Supplemental device-voltage failures

These fine checks cover |Vgs|, |Vgd| and |Vds| for all 23 MOS devices (69 terminal pairs). The failing corner repeats use the same frozen circuit and mixed-amplitude excitation.

| Corner | Maximum step | Violating pairs / 69 | Maximum absolute voltage | Reported worst device / pair |
|---|---:|---:|---:|---|
| ff_high_125 | 0.5ps | 3 / 69 | 1.00488 V | MRQP / gd |
| ff_high_m40 | 0.5ps | 28 / 69 | 1.01599 V | MRQP / gd |
| ff_high_m40 | 0.25ps | 28 / 69 | 1.01599 V | MRQP / gd |

## Remaining limits

Fine supplemental checks in [CHARACTERIZATION.md](CHARACTERIZATION.md) fail the 1.0 V device-voltage requirement. The 0.25 ps maximum-step repeat preserves the cold-corner violation. Passing a formal metric or the repository checks does not remove this failure. Transient-noise corner coverage is 1/45; all-corner noise, wider input common-mode/differential coverage and full-corner SOA are not established. No qualified-energy winner is claimed.

Commands (each result set was archived, hash-verified and committed before the next test):

```text
python -m adcflow sim tb_comp_delay --view adc_comp=xtor:many-question-miyahara --corners all --mode aps --jobs 1 --keep
python -m adcflow sim tb_comp_kickback --view adc_comp=xtor:many-question-miyahara --corners all --mode aps --jobs 1 --keep
python -m adcflow sim tb_comp_offset_mc --view adc_comp=xtor:many-question-miyahara --corners typ --mode aps --jobs 1 --keep
python -m adcflow sim tb_comp_noise --view adc_comp=xtor:many-question-miyahara --corners typ --mode aps --jobs 1 --keep
```
