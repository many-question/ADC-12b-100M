# BUFFER-V9: earlier clocked reset and input-drain recharge

B8 passes six-key-corner terminal stress and physical output validity but SS low/hot reset is 41.146991 ps. At 20 ps after the falling clock, CKB is only 0.663 V, the raw winner remains at 0.475 V, and DP is only 0.159 V, leaving the second-stage supply conducting. This experiment changes the clock PMOS P2 to P3 and direct input precharge P1.6 to P2.4. The intent is to start raw reset earlier and shut off its competing PMOS supply earlier. All physical rail-offset loads and buffer capacitances remain; no ideal gate or changed threshold is introduced. Both complete geometries reuse successful zero-warning callbacks.

The [independent source](BUFFER-V9.txt) has electrical SHA-256 `8c1e96b76b749f0d72b0be3c3f3ba4d1e1dd6cc4c3813b74074600af39df3c2f`. Full RNL on its byte-identical Spectre mirror passes core 0.5.2 with 0 errors, 0 warnings and 0 hints; the schematic was inspected.

![Physical reset and output repair](buffer-v9.png)

Six key corners now include both limiting SF cases and SS low/hot, together with TT and FF high/cold/hot. Every MOS terminal pair, all physical decisions, output validity, delay/reset and AVDD energy are checked over the entire trace. The next necessary simulations also save AVDD and device branch currents so reset/evaluation energy and persistent load current can be measured. See [energy comparison](ENERGY-COMPARISON.md); no prior qualification or topology-only efficiency advantage is claimed.
