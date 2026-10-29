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

After rehash, all **45 old replay records were byte-identical and stale**:
their generated load depends on the changed `timing.t_dac_add`. The pilot below
replaces four of them with actual new simulations; 41 remain stale. Old replay
metrics cannot be rehashed into REF-21 acceptance.

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

## Four-pilot result: failed

Four new APS simulations completed from clean commit
`607d9a52f95888fc4a24b481c3a0280c4b69bc19`, with at most two jobs in parallel.
All four return codes are zero, but **all four fail REF-21** and the SS low/hot
corner also fails REF-13. All four pass REF-12 and REF-14.

| Corner | REF-12 loss (bit), <= 0.1 | REF-13 tail (uV), <= 200 | REF-14 start p-p (uV), <= 100 | REF-21 ratio, <= 1 | Worst decision |
|---|---:|---:|---:|---:|---:|
| tt_nom_27 | 0.031287772 | 153.466465 | 37.829798 | **1.220239888 FAIL** | 4 |
| ss_low_125 | 0.015125222 | **247.534969 FAIL** | 54.220195 | **1.797049059 FAIL** | 10 |
| ff_high_125 | -0.021391916 | 151.106846 | 53.106662 | **1.302602236 FAIL** | 3 |
| ff_low_m40 | -0.015732304 | 71.349927 | 17.223801 | **1.050423077 FAIL** | 3 |

The actual 59 uploaded input files match the staged SHA-256 values. All 20
fetched raw/log/return-code files match their remote SHA-256 values, with no
skipped files. Each corner has 15,840 finite, contiguous samples. The largest
trigger-time error is 5.25 fs. Independent calculations from raw samples
reproduce REF-13, REF-14, the complete REF-21 vector and its worst decision.
All four evidence figures were inspected. All original raw evidence is retained.

The actual numerical settings are the same as the previous formal replay:
APS, `reltol=0.001`, `traponly`, `errpreset=moderate`, `lteratio=3.5`,
voltage absolute tolerance 1 uV. Accepted step counts are 565,614–568,807,
with mean steps 18.60–18.71 ps. The logged maximum-step setting is 211.6 ns;
the sampled-event timing is separately verified above. The bench saves only
the endpoint waveform, so an actual largest transient step cannot be recovered
from it. These runs are not an additional numerical convergence cross-check.
There are no reported device-limit violations; this is not an independent SOA
signoff. The existing environment/model-option and removed unused-instance
warnings are retained in the original logs.

## Failure localization and remaining work

| Corner | Decisions exceeding REF-21 | Worst absolute deviation / tolerance |
|---|---|---|
| tt_nom_27 | 3, 4, 6, 7 | 25.162911 / 20.621282 mV at decision 4 |
| ss_low_125 | 3 through 11 | 0.712643 / 0.396563 mV at decision 10 |
| ff_high_125 | 3 through 7 | 48.557017 / 37.276933 mV at decision 3 |
| ff_low_m40 | 3 | 39.156551 / 37.276933 mV at decision 3 |

At the worst SS tail event, decisions 12, 13 and 14 are respectively
0.9006725023374, 0.9008796560713 and 0.9009200373068 V. Decision 12 is therefore
247.534969 uV below the final decision. The failures include both early
recovery and late residual error; passing REF-12 does not remove them.

The new formal pattern changes pulse amplitudes as well as times (maximum
amplitude difference from the archived pattern: 6.0298089 mA). Both follow their
respective model preparation. Their comparison is not a controlled timing-only
experiment. These output samples establish the acceptance failures, but do not
alone isolate which bias or compensation change would fix the circuit.

Current coverage is **91 fresh/passing unaffected records + 4 fresh/failing
replay records + 41 stale replay records**. The pilot results and audit were
reported to the coordinator before expansion. All simulation slots are
released. The remaining 41 runs are on hold following the failures and the
coordinator's resource schedule; no circuit, limit, timing or numerical setting
has been changed to remove a failure. A design follow-up and scheduling decision
precede further simulations.

REF-21 requires the worst envelope ratio at decisions 1–11 to be at most 1,
using the final decision as the reference and the specified residual-code
margin. The last three decisions remain covered by REF-13. Acceptance is
incomplete until all 45 fresh replay records satisfy every applicable limit.
The historical mixed-top SS-hot TOP-01 failure remains documented in the
[README](README.md); updated top evidence is separate coordinator work.
