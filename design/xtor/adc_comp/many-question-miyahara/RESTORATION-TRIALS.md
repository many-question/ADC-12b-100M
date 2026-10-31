# Isolated physical restoration trials

Each frozen revision changes one symmetric device pair from the original V2/B2 source, preserving physical output isolation and full device noise. These private screens do not promote a canonical circuit or replace formal results. The [mechanism report](RESTORATION-MECHANISM.md) motivated the changes but does not predict success.

## B2-C52

[Complete frozen source](RESTORE-B2-C52.txt), raw SHA-256 `b06b77a5c33a3e65dbccd2b3467de7f204359b04fe15190380f8df3d001f5264`; electrical SHA-256 `5a3bed89a0ee024014a2604d65b80cbc12d350cd09e17afe5253044de5561f29`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only CDP/CDN MOM finger count changes from 48 to 52; callback nominal capacitance 15.26030 fF per node. Length, width, spacing, metal stack and multiplicity remain the parent values.

Callback receipt SHA-256 `b7ce79bbb6ee753c7660876650ee783af37a20aaca6a17cd8b39e0e949704c7f`. Provider tsmc-n28-hpcplus-ull-mmwave-1.8-2p2a-20190531, adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`. Ordered request: `[['Nfinger', '52'], ['Lfinger', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

TT screening has been dispatched; no completed archived result or qualification is claimed yet.

## B2-P5

[Complete frozen source](RESTORE-B2-P5.txt), raw SHA-256 `82c32d30eb380f185bcd4d4cc67be1cf81697ebc76c05f62ff389bd15f9ba01c`; electrical SHA-256 `0242a27c4d8b3ccccaf712ab242fee68e77d872f3424c4b87a064934b5d38282`. Parent restore-b2: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`.

Only M14/M15 changes from W=4 um / nf=4 to W=5 um / nf=5, L=30 nm; all terminal geometry/parasitic parameters come from the successful callback. M12/M13 and DP/DN capacitance remain the parent values.

Callback receipt SHA-256 `e0a6e29486c6fe53f2f3dd8c92c47f81bfa5cdf3c6b89023cf699835120771ba`. Provider tsmc-n28-hpcplus-ull-mmwave-1.8-2p2a-20190531, adapter 0.1.0, payload SHA-256 `c46e4713691443dbd588238d581c1863b255767fe1f79fc58722e81c0244b81f`. Ordered request: `[['l', '30n'], ['fingers', '5'], ['Wfg', '1u']]`. Actual values were asserted before source generation; RNL checks return zero errors/warnings/hints.

TT screening has been dispatched; no completed archived result or qualification is claimed yet.


All listed completed archives passed CRC/member SHA checks and exact remote-path absence checks. Batch timers include other variants in a shared run; overlapping durations are not campaign wall time. Archive/report time was not instrumented. Noise CIs are conditional on the binomial probit model and do not establish independent samples or seed robustness. Non-TT 30 mV delay and energy are report-only.

The initial PMOS request used w before fingers and returned 15 um total width; it was rejected before any netlist/simulation. A corrected l/fingers/Wfg request produced and verified 5 um. Two local checker setup attempts (text-format recognition, then missing copied RNL packages) were corrected using an exact .scs copy and complete project RNL package set; no circuit change was used to hide diagnostics.
