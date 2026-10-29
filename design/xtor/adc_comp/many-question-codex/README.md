# Dynamic comparator candidate

This WIP candidate uses an NMOS dynamic differential preamplifier followed by a
complementary regenerative stage. The preamplifier and regenerative stage have
separate clocked supply paths. Symmetric two-inverter output buffers drive the
specified 10 fF loads and return both outputs to zero in reset.

For INP greater than INN, DP discharges first. The PMOS sense branch then raises
QP, suppresses QN through cross coupling, and asserts OUTP. A local clock buffer
limits the charge demanded from CLKC; its delay is included in timing results.

All device instance dimensions and parasitics come from successful callback
solutions. The complete RNL drawing includes placement, wiring, differential-pair,
matched-device and stage-group semantics.

Validation is in progress. No full-corner, noise or mismatch pass is claimed.
Issue #40 is acknowledged. Issue #63 tracks the missing public flow for 50 actual
device-mismatch samples; transient-noise repetitions do not satisfy CMP-03.
