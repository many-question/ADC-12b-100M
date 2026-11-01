# Current validation: wip

Specification: adc_sarlogic 0.7.0. Circuit hash: `237b05f50a71cbad`.
Issue #130's maintainer decision is acknowledged: LOG-08 is still <= 2.75 ns;
2.90 ns is not an approved target. No ports, specifications, testbenches or
numerical settings were changed. Results are self-reported, not independently
verified, and the candidate is not eligible for selection.

## Standard TT function test

The current circuit captures 60 conversions with zero bit and
DAC-level errors, using APS and `errpreset=conservative`. The record is fresh.
**All applicable bounded TT observations pass**, including LOG-08
**2.747012 ns <= 2.75 ns** and LOG-16 **14.46% <= 20%**.

| TT observation | Result |
|---|---:|
| LOG-02 decision to UP/DN | 31.550 ps |
| LOG-03 decision to CLKC falling | 30.721 ps |
| LOG-04 fast wait, net of extra wait | 45.217 ps |
| LOG-05 slow wait, net of extra wait | 92.936 ps |
| LOG-07 first CLKC | 107.257 ps |
| LOG-08 maximum conversion time | 2.747012 ns |
| LOG-10 D setup before RDY | 133.366 ps |
| LOG-13 DVDD power, reported only | 1059.47 uW |
| LOG-14 CONV input capacitance | 2.534 fF |
| LOG-15 larger comparator input capacitance | 6.727 fF |
| LOG-16 worst extra-wait error | 14.46% |

The earlier circuit `df50102541da9321` measured 2.860505 ns for LOG-08.
The current result is 113.493 ps faster without relaxing the 2.75 ns limit.
The changed receivers, output/storage drive and request-tree matching reduce
loop overhead. The slow-wait load is retuned to preserve the fast-corner
70 ps floor. A rejected fully buffered reset path clipped the small extra
DAC waits; the delivered clock retains direct comparator return-to-zero
feedback and separately qualifies the conversion window and timeout.

## Coverage still in progress

The standard all-45-corner slow-comparator test is running with its original
100 conversions per corner and 70 ps comparator condition. The standard
all-45-corner timeout test is also running with its original 40 conversions
per corner. These pending runs are not claimed to pass.

The current four-conversion quick-set diagnostic covers seven corners and
28 conversions with no bit, DAC-level or clock-count errors. Its minimum
slow wait is approximately 70.38 ps, first clock 82.18 ps and D setup
103.37 ps. It is diagnostic only, not formal full-corner coverage for
LOG-06/07/10. The earlier all-45-corner four-conversion diagnostic belongs
to intermediate circuit `49ab94f9521d0865`, before the final timeout and
ready/extra-wait correction, and does not qualify the current circuit.

The previously recorded timeout results and TIMEOUT_CORNERS.png belong to
`df50102541da9321`. They are superseded until replaced by the current
simulations; they are deliberately not rehashed to claim another circuit.

## Reproduction and remaining qualification

```text
python -m adcflow sim tb_sarlogic_func --view adc_sarlogic=xtor:many-question --corners typ
python -m adcflow sim tb_sarlogic_func_slow --view adc_sarlogic=xtor:many-question --corners all
python -m adcflow sim tb_sarlogic_timeout --view adc_sarlogic=xtor:many-question --corners all
```

The candidate stays `wip`: formal remaining function-corner coverage,
1000-conversion random, mixed top-level regression, SOA and independent
verification remain pending. The all-corner slow and timeout tests must also
finish and be judged before their coverage can be claimed. RNL reports zero
errors, warnings and hints. The local unit suite reports 457 passed, 2 skipped
and 1 deselected with `pytest -q -m "not slow"`.
