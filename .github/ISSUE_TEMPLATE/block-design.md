---
name: Block design task
about: Interface, spec or testbench question for a block (candidates are submitted by PR, see CONTRIBUTING.md)
title: "[adc_...] question or proposal"
labels: block
---

## Block

- Spec: `specs/blocks/adc_....yaml` (version: )
- Behavioral reference: `design/behav/adc_....scs`
- Candidate(s) concerned: `design/xtor/adc_.../<name>/` (if any)
- Target date:

## Acceptance

All specs of the block pass at their corner sets with the transistor view:

```
python -m adcflow sim <test> --view adc_...=xtor:<name> --corners all
python -m adcflow report --block adc_...
```

Then the full ADC with this block in transistor level and the rest behavioral:

```
python -m adcflow sim tb_top_sine --view adc_...=xtor --corners quick
```

## Notes / open questions

<!-- Open an issue here before changing ports, specs, testbenches or other blocks.
     The project lead (@many-question) decides; a candidate PR never edits them. -->
