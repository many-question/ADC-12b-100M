# RESET-V29: stronger physical output drivers

The complete V28 circuit still fails TT noise at 206.44956249285457 uV rms against 200 uV. Its tighter TT 30 mV delay is 49.84967366576565 ps, leaving only 0.15032633423435 ps. [RESET-V28](RESET-V28.md) preserves the failure; [artificial source diagnostics](NOISE-SOURCE-DIAGNOSTICS-V28.md) guide further work without constituting physical performance.

This experiment doubles all four RTZ output MOS devices MOPN/MONN/MOPP/MONP from 4 um/nf4 to 8 um/nf8, keeping 30 nm length and 1 um fingers. The other 19 MOS devices and all five MOMs are unchanged. The 3 um tail current device, 56 um input pair, Q shunts and storage remain fixed. Exact previously solved, zero-warning N8/P8 callback geometries are reused after SHA-256 verification: N8 `e705ebc2985cc3b6bbbe232cb188f1b0c155751d55a7a5aeaeec5df014a19f6a`, P8 `20855415d9559ad00227138e98d1e759f6c67857f07cd4c5123d67502d0fec87`. Their provider and release match, and the original remote callback directories are absent.

The immediate question is whether stronger output drivers create timing headroom while preserving reset, output validity and full terminal stress. Added gate loading also slows the preceding latch and changes noise transfer, so no delay or noise improvement is assumed. A prior 2.4 um tail experiment failed TT 30 mV delay at 55.2584 ps; a lower-current input stage will only be considered after measuring available headroom. Every physical noise source remains enabled in subsequent noise trials; this is a physical sizing experiment, not a source-suppression diagnostic.

Initial private checks use the merged 0.8.0 baseline, with no numerical overrides, at TT, SS/low/125 and both SF/FS high-voltage cold corners. All actual polarities, reset intervals, output validity, complete-transient terminal stress and full-cycle AVDD energy are audited. Capacitance and noise require their own tests. No formal record, shared tool, testbench, specification or threshold changes. Canonical V27 remains unchanged and neither V28 nor V29 is qualified.

Electrical SHA-256: `f09e932d738d714ea723c327eccecc41a3b1da499a4b1efb561cfdd1b14b7ee9`. The [complete source](RESET-V29.txt) contains RNL checked on a byte-identical mirror.

![Stronger RTZ output inverters](reset-v29.png)
