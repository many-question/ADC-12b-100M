# BUFFER-V15: restore buffer-node edge margin

B14's first SF/high/-40 and FS/high/-40 screens pass all 72 actual polarities, resets and output-validity checks, but FS fails six terminal-stress pairs. The actual BN maximum is 1.000091633924 V at 23.997853 ps after a rising midpoint, with CLKC=0.99 V and CKB=0.129335 V. BP similarly reaches 1.000089066299 V. SF peaks at 0.99991 V. B14 stops before TT and noise; no noise improvement has yet been demonstrated for its stronger interstage PMOS drive.

This source changes only CBP/CBN, the physical buffer-node MOMs, from 16 to 20 fingers, nominally 4.46 to 5.66049 fF. It tests additional edge-charge storage at the two observed overvoltage nodes. All 43 MOS devices, including B14's M14/M15 P6 drivers, and the other seven MOMs are electrically unchanged. This repairs an observed edge-margin problem; it does not assume that added capacitance fixes the B13 noise mechanism. Added buffer delay and reset charge must be measured.

The new capacitor callback succeeds without warnings; its SHA-256 is `613c7aa6a617bd67d2699ba18a547794f801dbaee33aeab31e6b964b5ba9cc5d`. Electrical SHA-256: `5006ef01a47d58de546a7925aa88a7ea9d7730b43632efcaf676d28974223d94`. The [source](BUFFER-V15.txt) contains 43 MOS and 9 MOMs, with complete RNL checked on a byte-identical mirror. Canonical B13, its four formal hot noise failures and the B14 stress failure remain preserved.

First repeat SF/high/-40 and FS/high/-40. If they pass, TT and FS/low/125 deterministic screens precede the matched TT/worst-corner noise diagnosis. Broader known-corner coverage, actual-worst convergence, canonical promotion and genuine original formal gates remain to establish.

![Physical comparator with larger buffer-node MOMs](buffer-v15.png)
