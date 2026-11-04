# V29 validation status, 2026-11-05

Canonical V29 (`9b00f07143da7cc5`) remains WIP. Its three official blockers
below are preserved. The private reset2x experiment has passed its five
pre-tracking gates but fails full hot primary tracking; crosscheck is running. This does not
promote the private source or establish full-corner/mixed-top qualification.

## Canonical failures

| Test | Primary | Independent check |
|---|---|---|
| ss_low_m40 SOA | 3 violations; 1.25686 V; worst 10 ns window 127.281 ps | 3; 1.25631 V; 126.906 ps, over the 100 ps limit |
| ss_low_m40 track | SPECTRE-16928 at 60.1007 ns; 2/256 samples | Observation-only replay fails at the same instant; no spectrum |
| ss_low_125 track | SFDR 63.13694 dBc / SNDR 63.06129 dB | 63.15043 / 63.07558; both below 85/80 limits |

Both hot records contain 256 samples; their difference is 5.765 uV rms,
10.841 uV maximum. They finished before attempted cancellation and were
recovered after controller interruption, with staged TB/deck/dependency
identity checked before official measurement. No rerun or partial FFT was
substituted. Tracking uses effective reltol 1e-7 / vabstol 10 nV; crosscheck
uses traponly / maxstep 1 ps. SOA cross uses effective 1e-8 / 10 nV.

The three SOA rows are TOP-PHI_SB: MTP Vgd and MTD Vgs/Vgd. Continuous
over-1.1-V intervals are 124.228/127.281/124.338 ps near 10.1/30.1/50.1 ns.
At the largest peak, VIN=.946488, TOP=1.256859, PHI_S=.81 V, PHI_SB=CONV=0:
sampling restoration, not a sum of separate intervals. Cold-track replay
has 41588 points; its last .396 fs contains 2209 steps below .01 fs while
SAMP_ON rises and APGATE falls. TOPP/N=.698/.232 V with PHI_SB=0, so this
does not identify the same physical cause as SOA or a particular model.
SOA directly drives extremes with 100 ps edges and DAC decisions; track
uses a continuous sine through 50 ohm with neutral decisions. Both have
ideal external phases/bootstrap/reference; those prescribed stimuli remain.

Canonical hot-SS RL12/RL5/start settling is 39.7/57.9/97.9 ps; private
traponly/1 ps/effective 1e-7/10 nV gives 39.6/58.3/98.4 ps. Further
.5 ps/1e-8/1 nV refinement agrees on the .1 ps measurement grid, though
one saved interval is 1 ps at 5.01 ns. The narrow margin remains explicit;
primary startup is optimistic by .5 ps. This is an engineering refinement,
not a specification-defined settling crosscheck.

## Completed diagnostics

Bounded diagnostics retain the original 2.605 us requested stop/tolerances
and use intentional progress interruption (rc=2); no acceptance FFT.
First cold attempt stopped at 30.086858 ns because its watchdog misread a
partial timestamp; evidence is retained and only that instrumentation
failure was repeated after parser testing. Retry `20261104-103853-f4d4`
reaches 80.050462 ns / four samples with traponly/1 ps. Near the former
failure, minimum step is 61.675 fs with no collapse; whole trace has two
isolated sub-.01-fs steps elsewhere. Two shared samples differ 9.772 uV rms,
9.968 uV maximum. This shows method/step sensitivity, not a full cold pass.

Hot observation `20261104-103000-62d8` reaches 100.064429 ns; all 64 voltage
and 22 native-current probes are present. Six samples match the full run
within 3e-13 V; native source currents agree with (SRC-VIN)/50. Full-record
H3 is 545.39 uV peak (98.27% residual power), versus TT 30.05 uV.
In track phase 1..4.8 ns over 40..99.9 ns, rms TOP-VCM is 39.45..39.66 mV,
VIN-BH12 2.95..2.97 mV and SRC-VIN 18.47..18.54 mV. Dynamic reset V/I is
105..131 ohm versus input 33..36 ohm; both include displacement/recovery.
VGS error is under 2.6 uV. First held-sample reset currents are -.749/+.577
uA, selected input currents about 20 uA; differential TOP drifts 22.83 uV
in its final 50 ps versus full-record residual 446.18 uV. Partial harmonic
fits vary with order and are rejected as unique H3 attribution.

Private ideal-shunt run `20261104-171150-9367` reaches 200.055719 ns and
16 samples, interrupted after 393 s. A symmetric 1/120-ohm TOP-VCM branch
is active only in late track, withdrawn 34 ps before PHI_S begins falling.
All 89 probes, envelope/current support and native G*a*V checks pass;
pre-40-ns quiet difference is under 2.4e-5 uV and sample times are identical.
P/N track reset error falls 37.58/37.71 -> 18.58/18.60 mV rms. Removing DC
and the known fundamental from 16 matched samples gives 114.122 -> 80.205
uV residual rms (-29.72%, above predeclared 25% and 10 uV thresholds;
primary/cross floor .525 uV). This supports reset-conduction causality,
not a full SFDR pass or a PDK repair. Final-50-ps held drift worsens to
28.48 uV: changed state alters edge/hold currents despite the branch being off.
Three bounded archives each have 62 remote-hash-matched files; the ideal
intervention has 63. ZIP contents and hashes were verified.

## Private physical reset2x gates

Only MTN 12u/nf6 -> 24u/nf12, MTP and MTD 4u/nf2 -> 8u/nf4 change;
L=30 nm, finger width=2 um, models, ordered terminals/bulks and ports stay
fixed. No ideal branch. Source SHA-256
`82ff356fa4287d74686f0697073d0dc705ded881bfa412fcb65861c80db3d013`,
dependency `f1331c7d13f6b64f`. PDK callback validates six old/new parameter
sets without warnings; complete geometry/parasitic outputs are retained.
Existing MAC w/l/nf invocation style is preserved, without adding explicit
parasitic overrides as another experimental variable. Source/patch/callback
provenance is copied into each isolated stage; official source is untouched.

| Gate | Primary | Strict check |
|---|---|---|
| TT phase Cin PHI_S/PHI_SB/CONV | 28.0319/29.0593/14.7740 fF (limits 40/40/80) | n/a |
| TT Qref; RL12/start | 1.271747 pC; 30.2/70.1 ps | n/a |
| Cold SOA, 596 MOS / 1788 pairs | 0 violations; 1.18702 V; 53.337 ps/window | 0; 1.18689 V; 53.265 ps/window |
| Hot SS RL12/RL5/start | 39.7/56.8/97.9 ps | 39.6/57.3/98.4 ps |
| Hot SS droop | .060590 LSB | .060639 LSB (limit .1) |

All five required runs exit 0 and pass applicable limits. Strict settling
uses traponly/1 ps/effective 1e-7/10 nV; SOA cross uses 1e-8/10 nV.
Actual staged source SHA, logged numerics and rc match records; raw settling
remeasures exactly and all SOA pair-table rows match. Droop worsens from
canonical .00493 LSB; startup/RL12 margins stay narrow. Gate success is
not evidence that the hot-track 22 dB shortfall closes.

Runs: TT `20261104-174009-02be`; cold SOA `20261104-174009-220b`, cross
`20261104-174457-1a04`; hot SS `20261104-174457-c9be`, strict
`20261104-174457-5186`. All reach 70 ns. No owned CDAC process remained
at 2026-11-05 00:08:07 +08:00 before dispatch. Hot tracking uses
all 256 samples and the same private source for primary/cross, with original
precision and stop. Dense current waveforms cover the first 100 ns; later
waveform output is reduced without disabling the independent event sampler.
Any hard failure stops further expansion; no automatic size/topology sweep.
All five gate directories have remote/local SHA equality and verified ZIP
archives (65 files per settling run, 68 per SOA run).

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
Cross `20261105-000917-2235` is still running; full numerical agreement is
not yet established. Expansion is stopped; no further size/topology is launched.
Canonical failures, remaining corners and real-reference mixed-top remain open.
