# Current validation: wip

Specification: adc_sarlogic 0.7.0. Circuit hash: `df50102541da9321`.
All recorded results below use this circuit, APS and the unchanged project
`errpreset=conservative` testbench settings. Results are self-reported;
independent verification and selection have not been performed.

## Timeout qualification

The standard timeout test was run at all 45 corners, with its specified
40 conversions per corner. It captures **1800 conversions
with zero bit/DAC-level recovery errors**. LOG-11 and LOG-12 pass at every
required corner. All records match the current circuit and are not stale.

The corner-average timeout range is **205.277 to
340.024 ps**, within 200-350 ps. The minimum is
`ff_high_m40`; the maximum is `ss_low_125`.

The timeout uses 12 resettable taps and an EHVT NMOS-only gate load at each
tap (`timer_load=4400n`). The original reset NAND gates and output inverters
are retained. The voltage-dependent load reduces PVT delay spread without an
extra reference, calibration phase, port or ideal delay element. DAC waits
continue to use their separate paired MOS loads.

| Previously failing corner | Baseline timeout (ps) | Current timeout (ps) | 200-350 ps |
|---|---:|---:|---|
| ff_high_m40 | 199.955 | 205.277 | pass |
| ss_low_m40 | 354.763 | 312.287 | pass |
| ss_low_125 | 365.375 | 340.024 | pass |

The baseline values are the earlier four-conversion diagnostics of circuit
`e3eebc31d22e3add`; current values are the full 40-conversion formal runs.
The current four-conversion sweep also covers all 45 corners, captures 180
conversions without recovery errors and measures approximately 205-340 ps.

![Formal timeout across all PVT corners](TIMEOUT_CORNERS.png)

## Ordinary TT conversion

The standard function test captures 60 conversions with
zero bit or DAC-level errors. Among the applicable bounded TT observations,
only the existing LOG-08 conversion-time limit is unmet.

| TT observation | Measured | Requirement | TT verdict |
|---|---:|---:|---|
| LOG-02 decision to UP/DN | 35.428210 ps | <= 40 | pass |
| LOG-03 decision to CLKC falling | 36.177000 ps | <= 45 | pass |
| LOG-04 fast wait, net of extra wait | 53.094494 ps | 35-60 | pass |
| LOG-05 slow wait, net of extra wait | 93.436694 ps | 70-100 | pass |
| LOG-07 first CLKC | 113.273954 ps | 80-160 | pass at TT |
| LOG-08 maximum conversion time | 2.860505 ns | <= 2.75 | FAIL |
| LOG-10 D setup before RDY | 140.426259 ps | >= 100 | pass at TT |
| LOG-13 DVDD power | 940.131396 uW | reported only | info |
| LOG-14 CONV input capacitance | 2.534006 fF | <= 40 | pass |
| LOG-15 larger comparator input capacitance | 5.032981 fF | <= 7 | pass |
| LOG-16 worst extra-wait error | 13.459551 % | <= 20 | pass |

These are TT observations. Requirements that name all corners still need
their formal coverage in the corresponding function tests. This run does not
satisfy LOG-01's separate 1000-conversion random test.

## Reproduction and remaining qualification

```text
python -m adcflow sim tb_sarlogic_timeout --view adc_sarlogic=xtor:many-question --corners all
python -m adcflow sim tb_sarlogic_func --view adc_sarlogic=xtor:many-question --corners typ
```

The full-corner timeout execution used the same 45 named corners in a
different order to run the fastest corner first during simulator warm-up;
no parameters, sample counts, numerical settings or limits were changed.

The aggregate waveform archive transfer failed after all 45 simulator jobs
completed. The same completed jobs were recovered in six transfer batches.
Their preserved decks, testbenches and dependency hashes were checked against
the original staged inputs before the unchanged project measurement,
figure and recording functions were used. The result metadata records this
as `fetch_recovery`; no simulation data or acceptance conditions were changed.

The candidate remains `wip`: LOG-08 still needs
110.505 ps less maximum TT conversion time. The required
1000-conversion random, slow-comparator and remaining full-corner function
tests, mixed top-level regression and independent verification are pending.
No specifications, testbenches or acceptance limits were changed.

Local checks pass with the known LOG-08 results warning. RNL has zero
errors, warnings and hints. The unit suite reports 457 passed, 2 skipped
and 1 deselected with `pytest -q -m "not slow"`.
