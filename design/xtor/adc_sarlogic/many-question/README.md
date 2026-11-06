# adc_sarlogic: static CMOS completion chain

This candidate targets the unchanged port contract and version 0.8.0 of
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

The balanced request tree sets a separate clock holding latch. The
conversion window and timeout are combined separately, while the comparator
receivers' first inverter outputs retain a direct four-input NAND reset
path. This avoids clipping the small extra DAC waits with a slow reset
qualification buffer. Receiver, storage/output and request-tree drive
strengths are matched using approved device geometries and multiplicities.
Later receiver stages drive the bit latches. ACTIVE retains the enabled stage long enough to store its result
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

A shared 12-tap timeout chain starts on CLKC rising. Its first tap uses an
inverter because the former NAND's two inputs were both CLKC; all subsequent
taps retain their explicit CLKC reset. Each tap clears while CLKC is low.
This prevents a delayed pulse from a completed
comparison from forcing the next comparison. A timeout sets the currently
enabled stage's positive rail, producing the required forced decision of 1.

The timeout taps use a separate EHVT NMOS gate-load cell, with its drain,
source and body tied to VSS. The falling wait node sees the load's
bias-dependent capacitance. This reduces slow/fast delay spread compared with
the paired ULVT MOS loads used for DAC waits. The tap count and `timer_load`
are jointly set from PVT measurements. The first tap's inverter has the
equivalent pull-up/pull-down drive without the floating NMOS series node;
later reset NAND gates and the output inverters retain their devices.
No extra timing pin, reference
voltage, calibration interval or ideal delay element is introduced.

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
`tb_sarlogic_rand`, `tb_sarlogic_func_slow`, `tb_sarlogic_timeout` and
`tb_sarlogic_soa`, with
`--view adc_sarlogic=xtor:many-question --mode aps`. Official results belong
under this candidate's result view. Short diagnostic runs do not establish
LOG-01's 1000-conversion requirement or all-corner coverage.

Current measurements and remaining failures are recorded in
[VALIDATION.md](VALIDATION.md). The candidate is not ready for selection.

## Timing-budget decision

Issue #130's maintainer decision is acknowledged: LOG-08 remains <= 2.75 ns,
and 2.90 ns is not an approved target. The SOA repair changes the circuit
hash, so the baseline's all-corner timing data cannot qualify this revision.
All applicable tests are being rerun without changing the specified waits,
test lengths or numerical settings. See VALIDATION.md for current coverage.

## SOA repair

Simple 25% driver reductions alone still failed both high-supply cold corners.
The current revision puts CVB on the upper DAC-output NOR PMOS, uses the
equivalent first-tap inverter and reduces only CVB reset drive from 4 to 3.
Comparator-clock and per-bit output drive remain unchanged. The correction
removes two MOS devices and addresses floating internal series nodes rather
than relaxing the SOA rule. [SOA_REPAIR.md](SOA_REPAIR.md) distinguishes the
A/B experiments from formal candidate acceptance.
