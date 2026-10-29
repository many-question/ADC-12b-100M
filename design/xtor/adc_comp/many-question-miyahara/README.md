# Miyahara comparator

WIP candidate in 28 nm HPC+. No signoff claim.

Core connectivity follows [Fig. 2(b)](https://www.ssc.p.isct.ac.jp/private/publications/2008/ASSCC/miyahara.pdf). Miyahara self-triggered two-stage comparator core with reset Xi nodes and RTZ buffers.

The common comparison includes 10 fF on each output, the local clock buffer, and all output-adapter devices. Additional equal first-stage drain capacitances are an exploration variable; formal versions use permitted PDK capacitors.

Input-pair total width is 48 um, L = 30 nm, with 48 fingers. The current intermediate revision has a 3 um tail, direct CLKC drive and 27.42 fF nominal PDK MOM capacitors from DP and DN to ground. The original buffered baseline is preserved in git history. The external input polarity and reset behavior are verified by simulation.

Issues #40, #63 and #69 are acknowledged. Spec v0.5.0 supplies tb_comp_offset_mc: 50 TT local-mismatch samples, seed 6303, with every sample required to succeed. Formal candidate mismatch evidence remains to be collected.

The current intermediate circuit is not qualified: its supplemental ff/high/125 check exceeds the 1.0 V thin-oxide limit, and ss/low/125 reset is 47.34 ps. See [all exploratory results](CHARACTERIZATION.md), including failures.
