# L16-SPLIT: isolated reset-routing trial

This new source changes only MRDP/MRDN gates from CKR to CLKC in frozen historical l16t3c1. MRQP/MRQN remain on CKR; all device parameters, 48-finger DP/DN MOMs and physical output buffers are unchanged. It tests whether earlier front-node release provides more useful differential before regeneration, without assuming an independent integration interval through the coupled latch devices.

[Complete source and updated RNL](RESTORE-L16-SPLIT.txt). Electrical SHA-256 `8917ea8349c37517df1f871d7413ff1d232aefee4532e39e49e8a8e9ac85f3b2`; parent `56e3dddc5148fa35041f391de76c820e9e15927221bfc58dc79bea4bc7744577`. An exact electrical-line comparison finds only the two stated gate substitutions. All 19 MOS and two MOM instances are placed; RNL checks return zero diagnostics and the drawing was rendered and visually inspected. The two physical clock inverters and CKR connections are explicitly drawn. A caption-only correction after initial dispatch is separately recorded; it does not change the electrical hash or immutable simulation inputs.

The parent fails full FS noise at 274.20498833482293 uV rms against 240 uV. It has 2.28596 ps TT delay margin, 5.94745 ps worst-reset margin and 8.74336 fF CLKC margin, but only 6.06 mV baseline terminal-stress margin. The 1.1 V limit remains unchanged and is evaluated without rounding all terminal-pair results.

First screen: TT, FS/low/125, SF/high/-40 delay/validity/stress and dedicated TT loading. Exact selected probes include front/latch precharge, input-pair, latch-N and tail drain-terminal currents plus supply current for a per-cycle contention audit. Compare complete precharge, matched-clock-phase DP/DN differential, QP/QN peaks, all 36 actual decisions and reset intervals, CMP-15, energy and CLKC capacitance. Current polarity and successful probe retention must be checked before interpreting current values.

If every first-screen gate passes, complete SS/low/125 and FF/high/-40 before full physical FS 17 x 512 noise. A failure stops expansion for this source. Only FS success permits TT noise. This trial is private screening, not a canonical promotion or a formal result; all outcomes and raw evidence remain retained.

## Measured results

| Test / corner | Results |
|---|---|
| delay / tt_nom_27 | d1=60.72272159160923 ps; d30=46.89882954687035 ps; reset=19.76958032583804 ps; CMP-15=0; unrounded peak=0.9929695395312397 V; energy=196.51170294 fJ; PASS limited gates |
| delay / fs_low_125 | d1=59.88852129000803 ps; d30=46.977244454556725 ps; reset=22.358371071792696 ps; CMP-15=0; unrounded peak=0.8686558225883158 V; energy=198.25158210840002 fJ; PASS limited gates |
| delay / sf_high_m40 | d1=68.5733652985119 ps; d30=50.99744850664624 ps; reset=17.317396936956083 ps; CMP-15=0; unrounded peak=1.097304064036897 V; energy=221.3337690828 fJ; PASS limited gates |
| kickback / tt_nom_27 | Cin=19.311701639827493 fF; CLKC=13.97108851628813 fF; net kickback=4.1512699961582245e-05 uV; PASS |
| delay / ss_low_125 | d1=78.66814829804758 ps; d30=60.44167454551667 ps; reset=25.91374286583142 ps; CMP-15=0; unrounded peak=0.8853753588115706 V; energy=178.0780482792 fJ; PASS limited gates |
| delay / ff_high_m40 | d1=46.29729270055616 ps; d30=35.71171234289827 ps; reset=15.468715879564217 ps; CMP-15=0; unrounded peak=1.090889275399344 V; energy=228.13611076079997 fJ; PASS limited gates |
| delay / sf_high_m40 tighter | d1=69.19803015192613 ps; d30=51.01852098352188 ps; reset=16.65525895322749 ps; CMP-15=0; unrounded peak=1.097264316244123 V; energy=222.69583749599997 fJ; PASS limited gates |
| noise / fs_low_125 | 276.50080267196466 uV rms; 95% profile CI [266.82071470160474, 286.6305794677563]; 17 x 512 finite samples; FAIL 240 uV |

A required gate fails. Stop expansion for this source; no TT-noise/full-corner/mismatch result is claimed.

Non-TT d30 and energy are report-only. The targeted SF check requests reltol=1e-6 and vabstol=1e-8; its log reports effective reltol=1e-7 and voltage abstol=1e-8, with no explicit maxstep/method override; all device-pair limits are applied to unrounded saved waveform maxima. No previous 30-run archive is reverified in this phase.

## Retained waveform and current audit

All five baseline corners and the targeted tighter SF run retain 216 actual decisions including 10 uV and 216 output-reset intervals; every completed cycle passes. Internal precharge is sampled 10 ps before each actual CLKC half-supply rise; it is a diagnostic of these retained cycles, not a new formal specification.

| Corner | Minimum precharge / VDD | Mean core 1 mV event: parent / trial (ps) | D differential at CLK+10 ps: parent / trial (mV) | At CLK+25 ps (mV) |
|---|---:|---|---|---|
| tt_nom_27 | 0.999030793 | 33.717794 / 32.694548 | 0.111899 / 0.142536 | 0.179741 / 0.151115 |
| fs_low_125 | 0.997635110 | 34.534587 / 33.393904 | 0.095232 / 0.122156 | 0.095401 / 0.074621 |
| sf_high_m40 | 0.999376513 | 35.661098 / 34.557862 | 0.128939 / 0.163150 | 0.374530 / 0.345054 |
| ss_low_125 | 0.998087749 | 46.090025 / 45.197346 | 0.040346 / 0.054977 | 0.230222 / 0.228424 |
| ff_high_m40 | 0.999426249 | 24.561907 / 23.318721 | 0.232599 / 0.273220 | 0.171792 / 0.245822 |
| sf_high_m40 tighter | 0.999364900 | 35.661098 / 34.732168 | 0.128939 / 0.162298 | 0.374530 / 0.351650 |

The +/-100 uV first-screen traces show earlier differential development and core response, but a nearly unchanged early front differential peak. At some later matched phases the differential is smaller, then reverses sign through regenerative feedback. These markers are not a small-signal gain or evidence of a noise reduction. Q overshoot increases at SF, which motivated the tighter numerical check.

Exact terminal-current probes were retained and are finite. The mean integral of min(positive precharge drain inflow, positive tail drain current), from CLKC50 to CKR50, is about 2.086/2.227/1.999 fC at TT/FS/SF. Separate signed drain-charge records also cover the first 25 ps and full evaluation for every cycle. These terminal currents include displacement; overlap is a diagnostic proxy, not an isolated conductive short-circuit current. Parent branch-current traces were not retained, so no current-reduction ratio is claimed. Whole-cycle measured energy and complete precharge are reported independently.

## New evidence and runtime

| Run | Wrapper / Spectre elapsed per job (s) | Upload / dispatch / fetch / parse / cleanup / guards (s) | Runner elapsed (s) |
|---|---|---|---:|
| 20261101-061948-soa12-l16split-first | 16.0/11.4, 16.0/11.4, 27.0/22.3 | 21.500 / 64.094 / 45.047 / 3.812 / 21.062 / 122.770 | 278.285 |
| 20261101-061958-soa12-l16split-loading | 32.0/27.9 | 21.453 / 53.640 / 43.156 / 0.188 / 21.032 / 122.286 | 261.755 |
| 20261101-062509-soa12-l16split-remaining | 15.0/11.1, 25.0/21.2, 26.0/21.9 | 21.437 / 73.109 / 47.485 / 15.750 / 21.078 / 122.542 | 301.401 |
| 20261101-062942-soa12-l16split-noise-fs | 357.0/354.0 | 21.562 / 379.656 / 43.078 / 5.843 / 21.016 / 121.461 | 592.616 |

20261101-061948-soa12-l16split-first archive SHA-256 `b97b7891c1c9e9cec25bdea72aecedce800c680f6457cadd91eb909144fcdd0a`.

20261101-061958-soa12-l16split-loading archive SHA-256 `599708f33e5d94d547094594d95423dabbdf627df979bb82d859e16aca9e384e`.

20261101-062509-soa12-l16split-remaining archive SHA-256 `b8be907c317d8a53668f07314def9643dd8c30badb0d5f60176158da9b56ae55`.

20261101-062942-soa12-l16split-noise-fs archive SHA-256 `3af5ef1ad00a22008e85985597ab08e782622d82b24c91c3c271d3b84ced62e5`.

Dispatch source raw SHA-256 `f381341a1ec199d37bcd78c59c4504ca2028362d8cc7a68b8193f005e0e333a4`; published source after caption-only correction `383fef0870fd40016de47fa116ab1437732eb07bc872a05c47dc827943dd764a`; electrical SHA is identical. Each completed archive passed CRC/member SHA verification and exact owned remote-path absence checks. Archive/report generation was not separately timed. Overlapping batch times must not be added as campaign wall time. Noise intervals are conditional on the binomial probit model and do not establish independent-sample or seed robustness.
