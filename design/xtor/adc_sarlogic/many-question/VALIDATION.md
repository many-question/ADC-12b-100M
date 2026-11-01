# LOG-08 optimization and revalidation in progress

Current circuit hash: `49ab94f9521d0865`. Specification: adc_sarlogic 0.7.0.
Issue #130's maintainer decision is acknowledged: LOG-08 remains <= 2.75 ns;
2.90 ns is not an approved target. The candidate remains `wip`.

The current revision rebalances the comparator receivers, result/output
cells and request tree. The clock latch retains direct comparator reset,
with conversion-window and timeout qualification factored separately.
This avoids the clipping of small extra DAC waits observed in a rejected
fully buffered reset experiment. Output drive uses device multiplicities
rather than extending individual device geometry outside its valid range.

Fast waits are shortened; slow waits are retuned to preserve the all-corner
70 ps floor. The start delay preserves the 80 ps floor at the fast corner.
The nominal extra DAC/reference waits and all external ports are unchanged.
The ready delay must still provide >= 100 ps output setup.

The current revision's standard TT function test and short full-corner
functional/timing diagnostic are being rerun. The prescribed 100-conversion,
70 ps comparator full-corner test will follow on a stable circuit.

The previously recorded results and TIMEOUT_CORNERS.png belong to circuit
`df50102541da9321`, not this revision. That circuit passed LOG-11/12 at all
45 corners but failed LOG-08 (2.860505 ns). Those observations are superseded
for current-circuit qualification; stale records are deliberately not
rehashed to claim they describe a different circuit.

The required formal remaining corner tests, 1000-conversion random,
current-circuit timeout coverage, mixed top-level regression and independent
verification remain pending. No specifications or testbenches were changed.
