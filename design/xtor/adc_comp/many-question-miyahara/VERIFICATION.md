# Official test evidence — spec v0.7.0

The complete 45-corner delay/energy/validity refresh is recorded from clean source `a2e3509597563d607d2a873ed9cc5e9d667ccfff`. All 92 candidate records pass the current dependency freshness check; the other 47 records and their 139 JSON/PNG files are byte-identical to their pre-refresh versions. No circuit changed. All simulations used APS with one Spectre process at a time. The candidate remains WIP, self-reported and unselected.

| Test | Recorded corners | Source commit(s) |
|---|---:|---|
| tb_comp_delay | 45/45 | `a2e3509` |
| tb_comp_kickback | 45/45 | `c41a097` |
| tb_comp_noise | 1/45 | `fcf5c09` |
| tb_comp_offset_mc | 1/1 | `128b899` |

Frozen electrical SHA-256: `e8a0e3d3dc1366cd20f72c291397b352c8b9a6eeb87df618e41c49199372597a`. The JSONs retain actual source, reached-file hashes, effective numerics and measurement provenance. [REFRESH.md](REFRESH.md) describes execution and archival; [VALIDITY.md](VALIDITY.md) lists all 45 corners and all violating cycles.

| TT metric | Value |
|---|---:|
| Noise rms | 193.758465 uV |
| Noise 95% profile-likelihood interval | [185.84, 202.07] uV |
| Systematic offset magnitude | 0.000199071 mV |
| Mismatch sigma (sample standard deviation) | 1.947055 mV |
| Valid / failed mismatch samples | 50 / 0 |
| Delay at 1 / 30 mV | 47.512933 / 38.754848 ps |
| Reset | 17.786952 ps |
| CMP-15 violating cycles | 24 / 36 |
| CMP-16 losing-output peak | 48.521649% VDD |
| CMP-10 AVDD energy, exact 36 mixed cycles | 187.647444 fJ/cycle |
| Input / CLKC capacitance | 19.310269 / 14.924420 fF |
| Differential kickback | 0.000485769 uV |
| Separate external clock-driver charge-energy estimate | 12.088780 fJ |

CMP-10 integrates AVDD charge over 100 ps–14.5 ns and multiplies by VDD / 36. The stimulus is the unchanged mixed sequence from +/-100 mV down to +/-10 uV, repeated twice, with 400 ps periods, VCM 0.49 V and 10 fF per output. It is reported-only and excludes the external CLKC source. The separate clock estimate is C_CLKC x VDD^2, not a measured system energy.

The unchanged TT noise result uses 17 levels x 512 decisions, seed 1 and 50 GHz bandwidth; its confidence interval is conditional on the probit model. Mismatch retains all 50 local TT samples, seed 6303, with no samples discarded. Neither falling-edge-sampled test independently validates first-event receiver noise or mismatch.

Across the refreshed delay sweep: 45/45 corners and 1084/1620 cycles fail CMP-15; 0/45 corners fail CMP-08; CMP-09 records 0 wrong decisions. The worst 1 mV delay is 76.793410 ps at `ss_low_m40`. The worst reset is 24.721438 ps at `ss_low_125`. All 45 simulator return codes are zero; known specification failures did not stop the baseline.

## Historical supplemental evidence

The old v0.5.0 official TT energy was 186.363293 fJ, measured as average AVDD power over 0–14.5 ns multiplied by 400 ps; the 100 ps reset lead-in was included. It is preserved in Git history and is not a fresh current-definition value. The following fine-step diagnostics retain their original stimulus, integration window, source and numerical settings. They are not the fresh v0.7.0 mixed-sequence energy or output-validity measurements. The unchanged circuit still has the stated SOA failures.

## Separate 1 mV energy diagnostic

This is supplemental evidence, not official acceptance JSON. Both candidates use VCM = 0.49 V, alternating +/-1 mV, 400 ps clocks, 10 fF per output, TT at 0.9 V / 27 C, and noise off. The DC operating point starts with CLKC low; the initial 0–100 ps remains in reset. The actual AVDD current-meter integral runs from 100 ps to 14.5 ns: exactly 36 complete decision/reset cycles. The first evaluation is included and no warmup decisions are discarded. Energy is measured directly from this preserved diagnostic run, not inferred from the mixed-sequence result. Fine settings are maxstep = 0.5 ps, traponly, reltol = 1e-6 and vabstol = 1e-8. The existing mixed-sequence control below uses the same frozen diagnostic source and fine numerical settings. Comparison with the official number also changes numerical settings; it must not be attributed solely to the stimulus or integration window.

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

Known fine-step device-voltage failures exceed 1.0 V. The official score can show soa=0 because private SOA findings are absent from its metric records; that is not a SOA pass. Transient-noise coverage remains 1/45 corners; full common-mode/differential range, full-corner SOA and mixed-top qualification are not established. No qualified-energy winner is claimed.

The only new simulation command for this refresh was:

```text
python -m adcflow sim tb_comp_delay --view adc_comp=xtor:many-question-miyahara --corners all --mode aps --jobs 1 --keep
```
