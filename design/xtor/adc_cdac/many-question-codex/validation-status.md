# V29 validation status, 2026-11-05

Canonical V29 (`9b00f07143da7cc5`) remains WIP. Its three official blockers
below are preserved. Private reset2x passes five pre-tracking gates but
fails full hot tracking in both primary and crosscheck. No private source
is promoted or full-corner/mixed-top qualification established.

## Canonical failures

| Test | Primary | Independent check |
|---|---|---|
| ss_low_m40 SOA | 3 violations; 1.25686 V; worst 10 ns window 127.281 ps | 3; 1.25631 V; 126.906 ps, over the 100 ps limit |
| ss_low_m40 track | SPECTRE-16928 at 60.1007 ns; 2/256 samples | Observation-only replay fails at the same instant; no spectrum |
| ss_low_125 track | SFDR 63.13694 dBc / SNDR 63.06129 dB | 63.15043 / 63.07558; both below 85/80 limits |

Both hot records have 256 samples, differing 5.765 uV rms / 10.841 uV max.
Recovery verified staged TB/deck/dependency identity. Tracking uses effective
reltol 1e-7 / 10 nV, cross traponly / 1 ps; SOA cross uses 1e-8 / 10 nV.

SOA failures are MTP Vgd and MTD Vgs/Vgd during sampling restoration.
Cold-track replay has 2209 steps below .01 fs in its final .396 fs while
SAMP_ON rises and APGATE falls; this does not establish the SOA cause.

Canonical hot-SS RL12/RL5/start is 39.7/57.9/97.9 ps; private strict checks
give 39.6/58.3/98.4 ps. Startup is optimistic by .5 ps; margin stays narrow.
These are engineering refinements, not specification-defined settling checks.

## Completed diagnostics

Bounded cold traponly/1 ps retry `20261104-103853-f4d4` reaches
80.050462 ns / four samples. Near the old abort, minimum step is 61.675 fs
without collapse; shared sample differences are 9.772 uV rms. The first
attempt's timestamp-parser watchdog failure is retained. These partial
records show method/step sensitivity, not a full cold pass.

Hot observation `20261104-103000-62d8` captures 100 ns / 86 probes; six
samples match baseline within 3e-13 V. H3 is 545.39 uV, 98.27% of residual.
Dynamic reset/input V/I is 105..131 / 33..36 ohm, including displacement.
Partial harmonic fits do not uniquely attribute H3.

Private ideal late-track shunt `20261104-171150-9367` reaches 200.055719 ns
and 16 samples. A symmetric 1/120-ohm TOP-VCM branch withdraws 34 ps
before PHI_S falls. Current-law checks pass; matched tracking error halves.
Removing DC/fundamental from 16 samples reduces residual 114.122 ->
80.205 uV rms (29.72%), while final-50-ps hold drift worsens 22.83 ->
28.48 uV. This supports reset-conduction causality, not a full SFDR pass.
All bounded/shunt archives have remote/local hash equality and verified ZIPs.

## Active priority: switch-group SFDR attribution

The user prioritizes full-spectrum distortion attribution. Further physical
sizing, SOA/corner expansion and qualification are paused. Four independent
private cases start from original V29, not reset2x, and change P/N symmetrically:

| Group | Idealized MOS per CDAC | Explicit exclusions/removals |
|---|---:|---|
| reset_cell | MTN/MTP: 2 | Top MTD dummy also removed |
| input_sampling | MSH/MSL/MEQ1/MEQ2 plus midpoint: 56 | Bits 9/6 have no VIN path |
| sharing | MSHAREH/L: 22 | Only BP-to-EQBUS branches |
| reference_outputs | MNOUT/MPOUT: 52 | All 13 bits, both H/L drivers |

All 126 explicit MOM/Cp elements and 463 control MOS remain. Other dummies
are retained. Removed intrinsic capacitance, leakage, injection and gate
loading are absent; no guessed matching loads are added. Actual controls
are recorded, so group association includes load-mediated timing changes.

Switches are bilateral finite resistances: Roff=1e12 ohm; constant Ron
with a C1 smooth transition over normalized gate 0.45..0.55. Fixed Ron
heuristics are reset N/P 170/430 ohm, bit12 input N/P 35/57 ohm, sharing
100 ohm and reference outputs 30 ohm, with inverse-width scaling. These
are diagnostics, not exact DC calibration. Original gates/polarity remain;
boosted gates use actual VG/(VIN+DVDD), exposing changed generator loading.

Private archives retain sources, inventories, patches and model hashes.
An 80 ns preflight precedes each full 256-point spectrum at official precision.
Zero-load edge loggers cover full duration and add numerical events.
Baseline samples are reused; baseline control comparisons
cover only previously observed first-100-ns representative nodes. All four
80 ns preflights and complete 2.605 us / 256-sample primary records now pass
source/model/numerics, current-law/passivity, sample-count and control checks.
Sample-time differences from baseline are at most 1.01 fs; no samples are missing.

| Independent replacement | SFDR dBc | SNDR dB | Delta SFDR dB | H3 peak uV | H3 phase deg | H5 peak uV | Gain/base |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original V29 | 63.13694 | 63.06129 | 0 | 545.389 | -128.895 | 71.487 | 1 |
| reset_cell | 76.86170 | 76.43856 | +13.72476 | 112.805 | -174.238 | 34.757 | 1.004204 |
| input_sampling | 63.79531 | 63.72661 | +.65837 | 505.850 | -127.251 | 62.925 | 1.000545 |
| sharing | 62.83525 | 62.76790 | -.30169 | 564.760 | -126.599 | 68.975 | 1.000130 |
| reference_outputs | 63.16763 | 63.06830 | +.03070 | 544.090 | -125.285 | 82.255 | 1.001105 |

SFDR/SNDR use the official pinned estimator. Harmonic peaks and phase are
coherent-DFT diagnostics; phase is aligned to each record's fundamental.
Reset is the strongest intervention in this matrix, with H3 amplitude down
79.3%, but the changed phasors are not an additive physical decomposition.
Reference H3 phase changes 3.61 deg despite nearly unchanged SFDR.
Reference primary also logs two SPECTRE-16780 LTE relaxations at 105.165 ns
and 2.21517 us on XDH.GP controls, with SPECTRE-16881 warnings. Its +.031 dB
change is not established as numerically significant. Logged tolerance and
complete-record/model checks do not by themselves establish convergence.
The replacement also idealizes threshold/body behavior and removes intrinsic
charges and gate loading; it does not isolate Ron, leakage or injection.
Even the ideal reset record remains below the 85/80 dB limits.

Full runs (normal rc=0) are reset `20261105-024217-e156` (6385 s), input
`20261105-024954-483a` (5020 s), sharing `20261105-025021-b857` (6071 s),
and reference `20261105-024955-f113` (5265 s), all `tb_cdac_track`.
Each full run retains 179 files with remote/local SHA equality and verified
ZIP contents. Common ideal-model SHA-256 is
`d8926d245e558b264a20ae3b277019a995cb938e73299dd6fb79cc4a2fa33d06`.
Frozen source SHA-256 values, respectively:

```text
35dd81f7c21d156d743ac87daf3a2182290bfcd6e497afb05d7e954523aff9f9
733f67afd8e9da2b4e6a737a68a261a67e8b59d2645966c3e5f2086a4a36b0f6
27725b56bc1329b581f37d7186e4583692666c67a89f15e5036f0fcfd5516663
7740883c5d2980b91c97db4b1044f8d5f870617a7b780518ea01212bdb4602a3
```

Observed control advances reach 4.293 ps (input APGATE), 3.748 ps
(reference GP), 2.577 ps (sharing SAMP_ON), versus .103 ps for reset.
These comparisons cover representative controls in 40..79 ns only.
Reset `20261105-043242-ef38` repeats the complete record with traponly/1 ps
at the same effective 1e-7/10 nV. Four independent subcases start from V29:
only MTN ideal, only MTP ideal, only MTD removed, and MTN/MTP ideal with MTD
retained. The last case tests N/P-device and dummy interaction. All four
80 ns preflights pass; three individual-device full records remain in progress.
The MTN/MTP-ideal, MTD-real case completes 2.605 us / 256 samples, rc=0,
5595 s, with all record/source/model/control checks valid. SFDR/SNDR are
77.26857/76.76205 dB, up 14.13163/13.70076 dB from V29. H3/H5 are
107.455/36.560 uV; H3 aligned phase -173.929 deg, gain/base 1.002504.
The large primary-run improvement thus persists with the dummy retained.
The .407 dB difference from removing MTD is not established as numerically
resolved: this endpoint logs SPECTRE-16780/16881 at 200.092 ns on PHI_SB
and lacks its own completed crosscheck. Individual N/P/dummy effects and
their interactions await the remaining records.
Run `20261105-044111-6ca9-tb_cdac_track` retains 179 remote-hash-matched
files and a verified ZIP. Frozen source SHA-256:
`227e23d0a02f05f1947a10a45ff040e3c19c1faef6cefc2f23f15852aa344aa1`.
The running reset cross logs an LTE relaxation at 200.092 ns on PHI_SB;
its full sample/spectrum comparison remains pending. Baseline primary/cross
and the completed reset, input and sharing primary logs contain no such warnings.
No ideal case is a manufacturable candidate or qualification result.

## Private physical reset2x gates

Only MTN 12u/nf6 -> 24u/nf12, MTP/MTD 4u/nf2 -> 8u/nf4 change;
L=30 nm, models, ordered terminals/bulks and ports stay fixed. Source SHA-256
`82ff356fa4287d74686f0697073d0dc705ded881bfa412fcb65861c80db3d013`,
dependency `f1331c7d13f6b64f`. Six old/new callback sets validate without
warnings; full outputs are retained. Existing MAC w/l/nf calls remain,
without explicit parasitic overrides. Each stage retains source provenance.

| Gate | Primary | Strict check |
|---|---|---|
| TT phase Cin PHI_S/PHI_SB/CONV | 28.0319/29.0593/14.7740 fF (limits 40/40/80) | n/a |
| TT Qref; RL12/start | 1.271747 pC; 30.2/70.1 ps | n/a |
| Cold SOA, 596 MOS / 1788 pairs | 0 violations; 1.18702 V; 53.337 ps/window | 0; 1.18689 V; 53.265 ps/window |
| Hot SS RL12/RL5/start | 39.7/56.8/97.9 ps | 39.6/57.3/98.4 ps |
| Hot SS droop | .060590 LSB | .060639 LSB (limit .1) |

All five runs pass. Source SHA/numerics match; settling remeasures exactly
and every SOA row matches. Strict settling uses traponly/1 ps/1e-7/10 nV,
SOA cross 1e-8/10 nV. Droop worsens from .00493 LSB; margins stay narrow.

Five gate runs reach 70 ns, with remote/local hash equality and verified
ZIPs (65 files per settling, 68 per SOA). Full tracking preserves original
precision/stop and all 256 event samples; dense currents cover first 100 ns.

Full hot primary `20261105-000909-56d3` completes 2.605 us / 256 samples,
rc=0, 4601 s: SFDR **67.03254 dBc**, SNDR **66.60858 dB**, both fail 85/80.
Improvement over canonical is only 3.896/3.547 dB. H3 falls 545.39 ->
349.23 uV peak, but H5 rises 71.49 -> 110.65 uV; residual rms falls
389.02 -> 259.30 uV. H3 still accounts for 90.70% of residual power.
Raw remeasurement is exact; its completed-wave prefix matches the live
100 ns snapshot byte-for-byte. All 66 archived files match remote hashes.
Private source and actual numerics match the frozen provenance.

Matched tracking reset error is 18.63/18.70 mV rms versus 37.58/37.71;
first-sample final-50-ps drift worsens 22.83 -> 56.90 uV (cross 56.90).
Late-hold differential reset terminal charge grows .160 -> .399 fC;
terminal currents include displacement. These observations do not uniquely
allocate full-record harmonics to tracking, injection or hold leakage.
Cross `20261105-000917-2235` completes 2.605 us / 256 samples, rc=0,
10039 s: SFDR 67.02427 dBc / SNDR 66.60338 dB. Primary differences
are .00828/.00520 dB; sample difference 4.249 uV rms / 7.975 uV max.
Both full records verify source/numerics, exact raw remeasurement and
first-100-ns snapshot prefixes. Cross archive: 66 remote-hash-matched files.
Further physical sizing is stopped; ideal attribution continues.
Canonical failures, remaining corners and real-reference mixed-top remain open.
