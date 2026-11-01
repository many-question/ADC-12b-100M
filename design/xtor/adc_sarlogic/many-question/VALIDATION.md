# Validation: timeout optimization in progress

The baseline measurements below belong to the previous circuit
`e3eebc31d22e3add`. The current circuit is `df50102541da9321`, with a 12-tap
EHVT NMOS-loaded timeout chain. Its four-conversion diagnostics cover all
45 corners with zero recovery errors and approximately 205–340 ps timeout.
The standard 40-conversion full-corner timeout runs and the standard TT
function run are in progress. The old result JSON is intentionally not
rehashed; it will be replaced by the new simulations.

Specification: adc_sarlogic 0.7.0. Circuit hash: `e3eebc31d22e3add`.
All observations below use this circuit, APS and the project's unchanged
`errpreset=conservative` testbench settings. Results are self-reported;
independent verification and selection have not been performed.

## Recorded TT acceptance runs

The committed JSON and figures are produced by these standard commands,
without overriding conversion counts:

```text
python -m adcflow sim tb_sarlogic_func --view adc_sarlogic=xtor:many-question --corners typ
python -m adcflow sim tb_sarlogic_timeout --view adc_sarlogic=xtor:many-question --corners typ
```

The first run captures 60 conversions with zero bit or DAC-level errors.
The second captures 40 conversions with zero forced-decision recovery errors.
Both results match the current circuit hash and are not stale.

| TT observation | Measured | Requirement | TT verdict |
|---|---:|---:|---|
| LOG-02: decision to UP/DN | 35.43 ps | <= 40 ps | pass |
| LOG-03: decision to CLKC falling | 36.50 ps | <= 45 ps | pass |
| LOG-04: fast DAC wait, net of extra wait | 53.37 ps | 35–60 ps | pass |
| LOG-05/06: slow DAC wait, net of extra wait | 93.69 ps | 70–100 ps at TT | pass |
| LOG-07: first CLKC | 113.54 ps | 80–160 ps | pass |
| LOG-08: maximum conversion time | **2.864236 ns** | **<= 2.75 ns** | **FAIL** |
| LOG-10: D setup before RDY | 140.43 ps | >= 100 ps | pass |
| LOG-11: forced-decision errors | 0 / 40 conversions | 0 | pass |
| LOG-12: timeout | 264.54 ps | 200–350 ps | pass |
| LOG-13: DVDD power at 100 MS/s | 960.68 uW | reported only | info |
| LOG-14: CONV input capacitance | 2.53 fF | <= 40 fF | pass |
| LOG-15: larger comparator input capacitance | 5.03 fF | <= 7 fF | pass |
| LOG-16: worst extra-wait error | 14.98 % | <= 20 % | pass |

These are TT observations. Requirements that name all corners still need
their complete formal corner coverage. The 60-conversion function run does
not satisfy LOG-01's separate 1000-conversion random test.

## Additional diagnostics

* The unmodified function test with `--corners all --param nconv=4 --no-record`
  captures 180 conversions across all 45 corners. Bit errors, DAC-level errors
  and comparison-clock-count errors are all zero. Every completed conversion
  has exactly 14 comparison clocks.
* The timeout test with `--corners quick --param nconv=4 --no-record` captures
  four conversions in each of seven corners, all with zero recovery errors.
  The timeout range is not yet compliant:

  | Corner | Timeout | 200–350 ps |
  |---|---:|---|
  | tt_nom_27 | 264.518 ps | pass |
  | ss_low_m40 | **354.763 ps** | **FAIL** |
  | ss_low_125 | **365.375 ps** | **FAIL** |
  | ff_high_m40 | **199.955 ps** | **FAIL** |
  | ff_high_125 | 235.022 ps | pass |
  | fs_nom_27 | 264.038 ps | pass |
  | sf_nom_27 | 260.392 ps | pass |

* An interruption diagnostic uses `--param nconv=4 --param tconv=700p
  --no-record`. The shortened window permits five captures before the test
  stops. Each contains exactly the first four completed comparator decisions
  followed by ten zeros. Comparing the output against comparator edges before
  CONV falls gives zero errors; RDY is generated for every capture.

These short runs are diagnostic observations, not substitute acceptance
records. Their raw simulator data is not committed.

## Remaining qualification

The candidate remains `wip`. LOG-08 needs 114.236 ps less maximum TT conversion
time; LOG-12 needs more margin across PVT. After tuning, the required
1000-conversion random, slow-comparator and full-corner acceptance runs must
be completed on the final circuit hash, followed by mixed top-level regression
and independent verification. No specification, testbench or acceptance limit
was changed to accommodate this candidate.

Local checks pass, with the results check reporting the known LOG-08 limit
warning. RNL reports zero errors, warnings and hints. The unit suite reports
455 passed, 2 skipped and 1 deselected with `pytest -q -m "not slow"`.
