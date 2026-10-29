# Baseline and dependency audit

On 2026-10-29 this candidate was rebased from main `17205ec` to `3f1f7ce`, including #48, #57 and #62. The public tag `history/adc_clkgen/numerics53-before-arch48` preserves the completed stage at `441d48c`. The 60-MOS netlist is byte-identical; its electrical content hash remains `878752080031c251`.

## Module results

The #48 changes initially made all 46 legacy records stale because each listed the whole deck. Every record reported the same four changed inputs: the behavioral reference wrapper, CDAC switch model, SAR logic model and `specs/arch.yaml`. The clock netlist, both clock testbenches, measurement code, ports, loads, limits and numerical settings are unchanged. The arch changes are its version and `timing.t_dac_add`.

After #62 was merged, the official commands were run with both block and candidate filters:

```text
python -m adcflow rehash --block adc_clkgen --view xtor-many-question --dry-run -v
python -m adcflow rehash --block adc_clkgen --view xtor-many-question
```

Both passes accepted all 46 records, leaving zero stale records. No simulation was run, and no result hash was edited manually. The official check establishes that current reached definitions match the simulated definitions, changed files do not define a reached name then or now, and required arch values are unchanged.

| Test | Records | Previously recorded files | Current dependency files |
|---|---:|---:|---|
| `tb_clkgen_timing` | 45 | 17 | Clock testbench, `tb_imeter_va.va`, candidate netlist, `specs/soa.yaml` |
| `tb_clkgen_jitter` | 1 | 16 | Clock testbench, `tb_sampler_va.va`, candidate netlist |

Both tests have an empty recorded arch-key set. `meta.views` explicitly selects `adc_clkgen=xtor:many-question`; `meta.rehashed` records this operation at clean commit `aae19ba`. The rehash preserved every other metadata field and every non-metadata field in all 46 records. All 91 evidence PNGs are byte-identical. Original simulation sources remain `cef765f` (five timing corners), `5c87359` (forty timing corners) and `add690e` (TT jitter), with their original dates and clean-state flags; all commits remain available through preserved history.

The regenerated job parameters match the recorded parameters. The new runner additionally declares `cdac_behav=1`; this global is used by the changed top-level noise setup and is unused by these clock testbenches and their reached circuit. It has not been inserted into old simulation records.

## Integration boundary

#48 changes the behavioral reference to 8 mA / 6 pF, introduces extra DAC waits, changes reference-charge timing and noise accounting, and adds the top-level TOP-10 spike counter. Those changes affect a mixed-top circuit. The old seven-corner clock mixed-top run and matched behavioral SS control retain their real failures (10.348264814 and 10.324003109 bit respectively).

Issue #35 is closed after the project baseline fix. This candidate has no new-baseline mixed-top acceptance result. Its status is `ready`: module validation is complete, with 46 fresh records covering all 11 specifications and 407 required spec/corner combinations, so it is available for comparison under CONTRIBUTING. Results remain self-reported. Project-led reproduction and new-baseline mixed-top validation are pending for selection/signoff; the block remains `selected: none`. Any new mixed-top run needs a separately reviewed input plan and a coordinator-assigned slot. Historical failures remain preserved.

## Receiver interfaces

All clock controls use the 0.9 V domain. External CLK is 100 MHz with 45–55% duty. On CLK falling, PHI_S falls first (sampling instant), PHI_B falls 20–80 ps later, and CONV rises at least 10 ps after PHI_B. On return to tracking, CONV falls at least 10 ps before PHI_B rises.

| Driven net | Receiver limit | Allocated driver load |
|---|---|---:|
| PHI_S, PHI_SB | Each CDAC input ≤40 fF (DAC-15/16); two instances | 100 fF each, including 20 fF wire |
| CONV | Two CDAC inputs ≤80 fF each (DAC-17), SAR input ≤40 fF (LOG-14) | 250 fF, including 50 fF wire |
| PHI_B, PHI_BB | Each bootstrap input ≤16 fF (BST-09/10); two instances | 40 fF each, including 8 fF wire |
| UP/DN | Each CDAC DH/RL input ≤6 fF (DAC-13); two instances | SAR output 15 fF per net |
| CLKC | Comparator input ≤16 fF (CMP-14) | SAR output 20 fF, including 4 fF wire |
| Comparator OUTP/OUTN | SAR input ≤7 fF each (LOG-15) | 10 fF each, including 3 fF wire |
| CDAC TOP | Comparator input ≤20 fF per input (CMP-12) | 20 fF per side |

CLKC comes from the SAR logic. Low resets both comparator outputs to zero; its rising edge evaluates. Top-level comparator INP is TOPN and INN is TOPP because bottom-plate sampling inverts. CDAC reference drivers must break before make, as specified in the updated handoff. Internal sampling buffers add delay and jitter beyond the clock generator's CLK-09 measurement.

The five clock-output loads total 530 fF. The historical TT total current is 79.67181473 µA, only 0.32818527 µA below the 80 µA limit, so increasing the receiver load is not covered by this evidence. Input capacitance measured as rising-edge charge divided by voltage applies to the phase and comparator-clock limits; DAC-13 and CMP-12 use their specified AC measurements.
