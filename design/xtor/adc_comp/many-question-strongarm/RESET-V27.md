# RESET-V27: larger Q storage with N8 coupling devices

V26 passes its three initial deterministic corners, but its matched short noise diagnosis retains the same wrong cycle 54 as V20. Descriptive Q SNR changes from 1.896073 to 1.917068 at +30 ps and from 3.346148 to 3.261936 at +40 ps. At -20 ps, Q differential standard deviations remain 0.361281/0.373230 mV across the two input levels; the wrong cycle already has -0.812609 mV Q differential. These phase observations do not establish a noise source or completed decision. [RESET-V26.md](RESET-V26.md) preserves the full result.

This experiment changes only CQP/CQN from 20 to 44 fingers, nominally 5.66049 to 12.86040 fF. All 23 MOS devices and the other three MOMs remain electrically identical to V26, including its N8 coupling devices, 0.5 um/30 nm Q reset shunts and 3 um tail. Finger length, width, spacing and metal range are unchanged. The zero-warning capacitor callback SHA-256 is `7c980b3d9fa9ea317087d837feea5cab285a7ff84a9de34c7d0fe95f6b90b851`.

The added storage tests whether early Q variation and release disturbance decrease enough to improve signal-to-noise after transfer. It may also attenuate the signal and slow regeneration and reset. V26 has 2.823328 ps of TT 30 mV delay margin; an earlier smaller capacitance step on V19 is not a guarantee for this source. TT and SS/low/125 timing and reset are therefore checked together with both high-voltage cold stress corners before any short noise run. No noise improvement is assumed.

Electrical SHA-256: `7b20b19a2434da94d732f9785a3a8f1a2138d17ed4f4854dbdc5ab1a6cff18df`. The [source](RESET-V27.txt) contains 23 MOS and 5 MOMs with complete RNL checked on a byte-identical mirror. Remaining known corners, actual-worst numerical convergence, source-preserving canonical promotion and original formal tests remain open. Canonical V19 and every genuine original record are unchanged.

![Physical comparator with larger Q capacitors](reset-v27.png)
