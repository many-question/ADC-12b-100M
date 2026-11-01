# adc_sarlogic: static CMOS completion chain

This candidate targets the unchanged port contract and version 0.7.0 of
`adc_sarlogic`. It is a work in progress; transistor simulations, rather than
the delay-load parameter names, determine whether it meets the timing limits.

The architecture is 14 successive decisions and 13 CDAC updates. Decision
`k` writes raw bit `D(14-k)` and, for `k <= 13`, selects `UP(13-k)` or
`DN(13-k)`. These are the project's redundant decisions, with output weights
1960, 1120, 636, 360, 204, 114, 64, 36, 20, 12, 6, 4, 2, 1. The output is
the parallel raw word; no binary recoding is performed in this block.

## Decision and restart

Each stage contains two result NOR latches and one ACTIVE NOR latch. An enabled stage stores the
positive or negative comparator result. Their OR is the stage's completion
state and disables further writes to that stage. The complementary latch
nodes drive its UP/DN outputs through conversion-qualified NOR gates.
Delayed completion prepares the next stage after the local DAC wait.
Completion is monotonic during a conversion, so subsequent comparator
activity cannot retract it. A local ACTIVE latch is set only when that stage
is requested and CLKC is high. It holds permission through comparator reset
until this stage's result has been stored. Permission is also qualified by
CONV, so interruption inhibits further writes while preserving the raw bank
for capture. Once ACTIVE is set, this stage withdraws its clock request;
its DONE bit prevents the request from reappearing when ACTIVE is cleared.

The balanced request tree sets a separate clock holding latch. Comparator
validity, timeout or CONV low resets that latch. The comparator receivers'
first inverter outputs reset CLKC, while their later stages drive the bit
latches. ACTIVE retains the enabled stage long enough to store its result
after comparator reset. Because the old request was withdrawn at evaluation
start, return-to-zero cannot reassert the clock for the previous stage.
Only the next stage's request can restart it, after stored completion and
the DAC wait, and with both comparator outputs low.

The comparator pins each see one small input receiver. Its later stages drive
the distributed decision latches. CONV similarly has one input buffer before
the internal reset, enable and capture distribution.

## Waits and timeout

The local wait is an inverter pair with PDK MOS gate loads. Separate load
parameters set the first-six and last-seven DAC waits. Additional loads on
decisions 3, 4, 5, 6 and 9 implement the project's nominal extra waits of
10, 30, 30, 30 and 25 ps. These increments must be measured with LOG-16;
they are not ideal time-delay sources.

A shared 16-tap timeout chain starts on CLKC rising. Each tap is explicitly
reset while CLKC is low. This prevents a delayed pulse from a completed
comparison from forcing the next comparison. A timeout sets the currently
enabled stage's positive rail, producing the required forced decision of 1.

## Output capture and interruption

The raw bank and the parallel output bank are separate. Static transmission
gate latches track the raw bank at decision 14. RDY is stored separately and
set after a delayed completion event. Its delay must leave at least 100 ps
between the last D transition and RDY rising. The next CONV rising edge
resets the completion and RDY latches.

CONV falling immediately disables the clock and opens a short capture window.
The raw bank is cleared only after a longer internal delay. The output latch
must close before that clear reaches the raw bank, preserving the decisions
made so far and leaving undecided bits at zero. A retained completion event
also produces RDY for this interrupted conversion. Output data and RDY then
hold through the sampling interval.

## Reference and verification

The reference [L3_logic_V2](https://github.com/rich-netlist/rnl-gallery/blob/main/examples/risca/L3_logic_V2.scs)
suggests a sequence of local logic segments and a comparator return-to-zero
handshake. This candidate implements its own transistor cells and the
project's single 14-decision sequence. It does not use the reference's
standard cells, split MSB/LSB sequence, selectable LSB stage, trim interface
or serial output.

Every primitive, storage cell and hierarchy has explicit RNL placement,
orientation and labelled wire endpoints. Signal stubs with the same net
label are electrically connected by the Spectre netlist. The PDK MOS bodies
are shown and tied to their supply rails. No PDK models or ideal behavioral
devices are included in the candidate.

Acceptance uses the unchanged project tests `tb_sarlogic_func`,
`tb_sarlogic_rand`, `tb_sarlogic_func_slow` and `tb_sarlogic_timeout`, with
`--view adc_sarlogic=xtor:many-question --mode aps`. Official results belong
under this candidate's result view. Short diagnostic runs do not establish
LOG-01's 1000-conversion requirement or all-corner coverage.

Current measurements and remaining failures are recorded in
[VALIDATION.md](VALIDATION.md). The candidate is not ready for selection.
