# B27: weaker D-gated latch clamps

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

Private, unqualified physical trial. Only M8/M9 change from N4 to N2 at 30 nm, using the exact verified B26 M12/M13 model, two 1 um fingers and all terminal parasitics. The other 41 MOS devices and nine MOMs are unchanged. Earlier R-node release is a hypothesis; delay, reset, output validity, unrounded SOA, port loading and full physical noise need new checks.

Electrical SHA-256 `12af77935658afe02d22cf915b436c702ebafcc0635e2fef176e62417aa52bac`. The [complete RNL source](https://github.com/many-question/ADC-12b-100M/blob/52145b84a2bb73ed7a177c01cb32ba0eac006139/design/xtor/adc_comp/many-question-miyahara/BUFFER-V27.txt) passes check/render with zero errors or warnings; its full drawing is inspected and retained locally. A stale footer is corrected to reset N8 / buffer N2.6. B26 is preserved at [published 9036f74](https://github.com/many-question/ADC-12b-100M/blob/9036f74f024088185398717989ed589784d1d151/design/xtor/adc_comp/many-question-miyahara/BUFFER-V26.txt) and in verified archives. Canonical B20 and its formal failure remain unchanged.

Completed baseline at `aa34324bf3fe55d9a89e647873669894578eae4d`: five corners pass all 180 actual decisions/reset intervals, output validity, 129 unrounded MOS pairs per corner and AVDD KCL. TT 1 mV/30 mV delay is 56.47951364995501/47.57069780086384 ps; SS reset 33.00179441176625 ps; worst stress 0.999342381737211 V. Dedicated TT input/clock capacitance is 19.328731218738323/12.110042590340404 fF. Exact runs, numerics, kickback phase context and archive hashes are in NUMERICS-94.

Matched TT 30 mV paths move R 50% crossing from 36.67952058125359 to 35.38451681143498 ps and output 50% crossing from 48.97788988704756 to 47.57069780086384 ps. Every cycle is retained in the archive; actual tested stimulus/numerics match B26. This confirms earlier latch timing, not a noise improvement. Tighter corners must pass before full physical noise.

**The tighter FS/high/-40 job fails with SPECTRE-16929 at 137.149 ps.** Only this first job ran; four planned corners are unstarted, so there is no completed tighter gate or B27 noise result. All 1249 accepted samples and the failure log are verified and retained; final rejected iterates are not captured. NUMERICS-94 records the exact settings and archive. This resembles B25's error class, but does not establish the same cause. Qualification expansion stops.
