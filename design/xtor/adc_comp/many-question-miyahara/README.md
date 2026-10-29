# Miyahara comparator

WIP candidate in 28 nm HPC+. No signoff claim.

Core connectivity follows [Fig. 2(b)](https://www.ssc.p.isct.ac.jp/private/publications/2008/ASSCC/miyahara.pdf). Miyahara self-triggered two-stage comparator core with reset Xi nodes and RTZ buffers.

The common comparison includes 10 fF on each output, the local clock buffer, and all output-adapter devices. Additional equal first-stage drain capacitances are an exploration variable; formal versions use permitted PDK capacitors.

Input-pair total width is 48 um, L = 30 nm, with 48 fingers. Initial baseline has no additional drain capacitors. The external input polarity and reset behavior are verified by simulation.

Issues #40 and #63 are acknowledged. CMP-03 remains pending the formal 50-sample mismatch flow.
