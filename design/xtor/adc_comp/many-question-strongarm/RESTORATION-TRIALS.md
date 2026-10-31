# Isolated physical restoration trials

Each frozen revision changes one symmetric device pair from the original V2/B2 source, preserving physical output isolation and full device noise. These private screens do not promote a canonical circuit or replace formal results. The [mechanism report](RESTORATION-MECHANISM.md) motivated the changes but does not predict success.

## V2-C56

[Complete frozen source](RESTORE-V2-C56.txt), raw SHA-256 `6b6c7aecf59235f1fd3e6eb19f17b8b1096f50a2af69a3bb53c163368bd68391`; electrical SHA-256 `daa991386afa21c7a615c6bdee674c8b298e40303a2fb734c8be02ccbec2e9dc`. Parent restore-v2: `608dfd3e547ee65738662bf62ef9c9cb548b0b7ea1000b21c22087ee0c958db8`.

Only CDP/CDN MOM finger count changes from 48 to 56; callback nominal capacitance 16.46030 fF per node. Length, width, spacing, metal stack and multiplicity remain the parent values.

Callback receipt SHA-256 `c6778b1e6296559ad3dd87ad5289a2b4aea41d1cd6c60be66fc78a4241944f5c`. Provider tsmc-n28-hpcplus-ull-mmwave-1.8-2p2a-20190531, adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`. Ordered request: `[['Nfinger', '56'], ['Lfinger', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

TT screening has been dispatched; no completed archived result or qualification is claimed yet.


All listed completed archives passed CRC/member SHA checks and exact remote-path absence checks. Batch timers include other variants in a shared run; overlapping durations are not campaign wall time. Archive/report time was not instrumented. Noise CIs are conditional on the binomial probit model and do not establish independent samples or seed robustness. Non-TT 30 mV delay and energy are report-only.

The initial PMOS request used w before fingers and returned 15 um total width; it was rejected before any netlist/simulation. A corrected l/fingers/Wfg request produced and verified 5 um. Two local checker setup attempts (text-format recognition, then missing copied RNL packages) were corrected using an exact .scs copy and complete project RNL package set; no circuit change was used to hide diagnostics.
