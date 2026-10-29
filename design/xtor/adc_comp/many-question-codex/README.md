# Dynamic comparator candidate

The current 30-transistor WIP candidate uses an NMOS dynamic differential
preamplifier followed by a complementary regenerative stage. The preamplifier
and regenerative stage have separate clocked supply paths. Each output uses a
clock-enabled NAND followed by an inverter, driving the specified 10 fF load.
The NAND resets the external output promptly while the internal latch resets.

For INP greater than INN, DP discharges first. The PMOS sense branch then raises
QP, suppresses QN through cross coupling, and asserts OUTP. A local clock buffer
limits the charge demanded from CLKC; its delay is included in timing results.

All device instance dimensions and parasitics come from successful callback
solutions. The complete RNL drawing includes placement, wiring, differential-pair,
matched-device and stage-group semantics.

Validation is in progress. No full-corner, noise or mismatch pass is claimed.

| Circuit revision | Evidence and limitation |
|---|---|
| `205f419` (26 MOS, smaller input pair) | Official TT timing and input-charge checks pass. Noise pilot: 325.1 uV, 95% CI 295.4–359.2 uV. Supplemental ff/high/125 SOA fails: 6 of 78 pairs, maximum 1.01193 V. |
| `3cc79ff` (26 MOS, larger input pair) | TT noise pilot improves to 249.5 uV, CI 224.8–277.6 uV, but reset is 46.85 ps and fails. |
| `ea81846` / `227305a` (30 MOS, NAND/INV outputs) | Official TT delay is 51.50 ps at 1 mV and 44.50 ps at 30 mV; reset 23.28 ps; energy 178.8 fJ; errors 0. Input capacitance 18.83 fF, CLKC 5.063 fF. The noise pilot worsens to 754.4 uV, CI 665.0–869.0 uV; further input-stage work is required. |

Each noise pilot used 17 levels, 64 decisions per level, fixed seed 1 and a
50 GHz noise bandwidth. These pilots are characterization, not the official
17-by-512 acceptance test. Raw data and exact decks are retained outside git.
Numbers from different revisions must not be combined into a passing result.

Issue #40 is acknowledged. Under the decision in #63, CMP-03 will use 50 TT
local-mismatch samples, transient noise off, a fixed seed, a +/-25 mV offset
search with about 10 uV resolution, and sample standard deviation (n-1).
Any failed sample must fail CMP-03. The independent public flow is pending;
transient-noise repetitions do not satisfy this requirement.
