# REF-21 retest record

Candidate `many-question` remains **wip**, with unchanged electrical content
hash `380f10b05b0af622`. This stage uses main
`3f1f7ce4d36cd2053dd0663856a52d58844c727a` and adc_ref spec 0.8.0.
The source file SHA-256 is
`1ca5f3143f4845e043416e8262d622e0556d4c060df175e21b448ed7991c6913`.
Notice [#60](https://github.com/many-question/ADC-12b-100M/issues/60) is read and
acknowledged. Original history is retained under
`archive/adc-ref-pre-ref21-42f458d` (commit `42f458d4aa93e7fa42430dddb863c8524f865e8c`)
and `archive/adc-ref-v8-legacy-e46427c`.

## Merged inputs

PR #48 merged as `9ee7cee10d8e83b8b374b3a4757ae663ebcbe3b4`, from final head
`ec55165b178ef63101d2df56b26a503c7765f0f0`. Comparing that head with the previously
reviewed `88b7624` finds no further changes to the replay model, reference
measurement, architecture, reference specification or direct reference benches.
The incremental TOP-10 spike-count limit belongs to the separate top regression.
PR #57 clears selection; all runs explicitly select `adc_ref=xtor:many-question`.
PR #62 supplies the official dependency tracking and rehash command, including
its final import-time architecture-read guard.

The behavioral reference's 8 mA / 6 pF remains a model starting point. No new
transistor bias, capacitance requirement or timing override is inferred from it.

## Official rehash of unaffected evidence

After the official dry-run and an independent dependency audit:

```text
python -m adcflow rehash --block adc_ref --view xtor-many-question --dry-run -v
python -m adcflow rehash --block adc_ref --view xtor-many-question
```

The command rehashed **91 records**: 45 DC, 45 startup and one TT noise. Each
test reaches only the unchanged candidate netlist and its unchanged direct
bench, and its measurement reads no architecture values. All 91 are fresh and
pass their applicable limits on the stated base. The audit independently matched
the current reached-file hashes to the original recorded inputs and checked the
electrical netlist at each original simulation commit.

Only official `meta.files`, `meta.arch`, `meta.views` and `meta.rehashed` fields
changed. Metrics, original simulation git/date/clean state, numerics, startup
cross-checks and migration provenance are preserved. All 136 figure files and
the candidate source are byte-identical. This step ran no simulations.

All **45 old replay records remain byte-identical and stale**: their generated
load depends on the changed `timing.t_dac_add`. They cannot be rehashed into
acceptance. Old replay metrics do not establish REF-21 compliance.

## Actual stimulus audit

The official preparation and staging code generated the four pilot decks.
They use N=1024 after 32 warmup conversions, 100 MS/s, k=509
(49.70703125 MHz), normal charge scale 1 and no extra DC load. ADCToolbox remains
0.6.4. All four corners use the same formal TT timing; only supplies and
temperature vary. Hot-fast/cold-fast timing scaling remains separate model
coverage, not an unstated override in this replay.

Each staged load has 14,784 charge pulses; the trigger has 15,840 events
(start plus 14 decision clocks for each of 1,056 conversions). The PWL audit
matches every pulse time and trigger center to the model, checks 2 ps edges
and 20 ps integrated pulse width, and checks integrated charge with maximum
relative formatting error below `4.70e-7`.

| File | SHA-256, identical at all four pilot corners |
|---|---|
| `iload.pwl` | `571634ca2aa0903e391f25a84952d78d5f664f24ecab952e1fa310d1fff02a9a` |
| `trig.pwl` | `b384177796d276dd61fb43f6778d976923268b18ed9d8523a90c886bc54c8953` |
| `tb.scs` | `842ccf4f7a0ef42f161148547a83ef22a485be3dd041e341b74079bed08f70c0` |

Both PWL hashes differ from the old formal run. Charge-onset to the next
comparator clock for steps 1–13 is **30, 30, 40, 60, 60, 60, 65, 65, 90, 65,
65, 65, 65 ps**. The first interval is measured from DAC charge onset; the
40 ps interval cited from UP/DN uses a different origin.

## Rerun coverage

No new replay simulation has completed at this stage. First run
`tt_nom_27`, `ss_low_125`, `ff_high_125`, `ff_low_m40` with APS and at most two
concurrent jobs. Freeze the committed inputs for each batch. Audit fetched raw
data, original return codes/logs, sample continuity, numerics and REF-12/13/14/21,
then report the pilots before expanding to the remaining 41 corners. A failing
pilot requires diagnosis before expansion; no limit is waived.

REF-21 requires the worst envelope ratio at decisions 1–11 to be at most 1,
using the final decision as the reference and the specified residual-code
margin. The last three decisions remain covered by REF-13. Acceptance is
incomplete until all 45 fresh replay records satisfy every applicable limit.
The historical mixed-top SS-hot TOP-01 failure remains documented in the
[README](README.md); updated top evidence is separate coordinator work.
