# L16-SPLIT: isolated reset-routing trial

This new source changes only MRDP/MRDN gates from CKR to CLKC in frozen historical l16t3c1. MRQP/MRQN remain on CKR; all device parameters, 48-finger DP/DN MOMs and physical output buffers are unchanged. It tests whether earlier front-node release provides more useful differential before regeneration, without assuming an independent integration interval through the coupled latch devices.

[Complete source and updated RNL](RESTORE-L16-SPLIT.txt). Electrical SHA-256 `8917ea8349c37517df1f871d7413ff1d232aefee4532e39e49e8a8e9ac85f3b2`; parent `56e3dddc5148fa35041f391de76c820e9e15927221bfc58dc79bea4bc7744577`. An exact electrical-line comparison finds only the two stated gate substitutions. All 19 MOS and two MOM instances are placed; RNL checks return zero diagnostics and the drawing was rendered and visually inspected. The two physical clock inverters and CKR connections are explicitly drawn. A caption-only correction after initial dispatch is separately recorded; it does not change the electrical hash or immutable simulation inputs.

The parent fails full FS noise at 274.20498833482293 uV rms against 240 uV. It has 2.28596 ps TT delay margin, 5.94745 ps worst-reset margin and 8.74336 fF CLKC margin, but only 6.06 mV baseline terminal-stress margin. The 1.1 V limit remains unchanged and is evaluated without rounding all terminal-pair results.

First screen: TT, FS/low/125, SF/high/-40 delay/validity/stress and dedicated TT loading. Exact selected probes include front/latch precharge, input-pair, latch-N and tail drain-terminal currents plus supply current for a per-cycle contention audit. Compare complete precharge, matched-clock-phase DP/DN differential, QP/QN peaks, all 36 actual decisions and reset intervals, CMP-15, energy and CLKC capacitance. Current polarity and successful probe retention must be checked before interpreting current values.

If every first-screen gate passes, complete SS/low/125 and FF/high/-40 before full physical FS 17 x 512 noise. A failure stops expansion for this source. Only FS success permits TT noise. This trial is private screening, not a canonical promotion or a formal result; all outcomes and raw evidence remain retained.

The first screen is dispatched; no completed result or noise improvement is claimed yet.
