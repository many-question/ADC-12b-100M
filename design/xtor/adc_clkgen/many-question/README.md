# adc_clkgen candidate many-question

A 60-MOS static CMOS phase generator with feedback from the loaded PHI_B and CONV outputs. MOS gate loads shape internal voltage excursions. The electrical circuit and its RNL drawings are unchanged; electrical content hash: `878752080031c251`.

**Status: WIP after specification 0.7.0 / PR #95.** Six official primary records have been refreshed: five timing/SOA corners and TT jitter. Their judged metrics pass, and all four prescribed timing crosschecks pass the metric limits. Forty timing corners remain stale. Per-pair SOA peak differences are material relative to the remaining margins, so numerical-evidence acceptance is unresolved in [#103](https://github.com/many-question/ADC-12b-100M/issues/103). This is not an observed voltage-limit violation.

The block still selects this candidate, but its new-setting eligibility, independent verification and mixed-top qualification are not established by these partial results. The remaining full-corner run awaits the maintainer's decision in #103. [Formal notice #99](https://github.com/many-question/ADC-12b-100M/issues/99) is acknowledged.

## Refreshed official evidence

All new runs used clean source `c6152d236e525793ecc4809b9a6c9dfb9fd0ad77`, the merged official runner and testbenches, and APS. ADCToolbox was installed from exact upstream commit `cd72061ff3b7a977163dac540da126ae22f5e38d`; the [#96](https://github.com/many-question/ADC-12b-100M/issues/96) self-test gives 80.00 dBc. Clock timing/jitter are time-domain measurements.

- Timing/SOA: `tt_nom_27`, `ss_high_125`, `ss_high_m40`, `ss_low_125`, `fs_high_27`.
- Official crosschecks: the four non-TT corners above; both primary and alternate return zero SOA violations across all 60 MOS / 180 terminal pairs over the full 0–161 ns waveform.
- TT jitter: **38.583988 fs**, 200 edges, limit 60 fs.
- TT AVDD current: **79.747346 uA**, reported only under CLK-10.
- Smallest timing margin among these runs: **3.258501 ps** for SS/low/125 C conversion delay.
- Smallest primary voltage margin among these runs: **69.534894 uV**, SS/high/125 C XOFF.MN Vds.

Primary logs report conservative, gear2only, reltol=1e-4, voltage absolute tolerance=1 uV, relref=alllocal and lteratio=10, with no explicit maxstep. Prescribed crosschecks request traponly/maxstep=1 ps/reltol=1e-7/vabstol=1e-8; their actual reltol is 1e-8. [Detailed evidence and matched-event diagnosis](NUMERICS94.md) explain the unresolved convergence issue without replacing the official result values.

All ten official simulator jobs returned rc=0. Their fifty retrieved output files (659,224,746 bytes) matched the original SHA256 hashes before cleanup. Actual peak concurrency was six jobs; commands used +aps without an explicit +mt, and all logs report multithreading disabled for this small design.

## Preserved history

The pre-#95 module results, earlier numerical settings and dependency-only migrations remain available in history. [BASELINE.md](BASELINE.md) documents the 2026-10-29 transition and is historical; its old freshness and selection statements do not apply to this migration. No rehash was used to restore the results invalidated by #95.

The earlier mixed-top SS/low/125 C result **ENOB 10.348264814 < 10.5 bit**, and its matched behavioral control **10.324003109 bit**, remain historical failures from [#35](https://github.com/many-question/ADC-12b-100M/issues/35#issuecomment-6476475531). They are not current mixed-top acceptance evidence. Existing history tags and original simulation provenance are retained.

Acknowledged specification notices: #18, #27, #29, #49, #80 and #99. Candidate and result changes do not modify the project specifications, testbenches, tools or independent verification records.
