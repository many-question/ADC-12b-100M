# Strongarm comparator

WIP candidate in 28 nm HPC+. No signoff claim.

Core connectivity follows [Fig. 1(b)](https://www.seas.ucla.edu/brweb/papers/Journals/BR_Magzine4.pdf). Single-stage StrongARM comparator with four precharge devices and inverting RTZ outputs.

The common comparison includes 10 fF on each output, the local clock buffer, and all output-adapter devices. Additional equal first-stage drain capacitances are an exploration variable; formal versions use permitted PDK capacitors.

Input-pair total width is 48 um, L = 30 nm, with 48 fingers. Initial baseline has no additional drain capacitors. The external input polarity and reset behavior are verified by simulation.

Issues #40, #63 and #69 are acknowledged. Spec v0.5.0 supplies tb_comp_offset_mc: 50 TT local-mismatch samples, seed 6303, with every sample required to succeed. Formal candidate mismatch evidence remains to be collected.

The current baseline fails the TT noise target. See [all exploratory results](CHARACTERIZATION.md), including the drain-capacitance and tail-current trials. No lower-power winner is claimed while the compared circuits fail requirements.
