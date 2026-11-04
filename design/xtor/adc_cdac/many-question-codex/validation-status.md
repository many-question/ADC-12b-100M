# V29 validation status, 2026-11-04

The unchanged V29 source (dependency `9b00f07143da7cc5`) is WIP with three
blocking observations. Full-corner expansion and mixed-top validation remain
incomplete. Original official failures are preserved.

| Observation | Primary | Independent check | Conclusion |
|---|---|---|---|
| ss_low_m40 SOA | 3 violations; peak 1.25686 V; worst window 127.281 ps | 3 violations; 1.25631 V; 126.906 ps | Sustained overvoltage exceeds 100 ps; numerical difference 0.375 ps is much smaller than the violation. |
| ss_low_m40 track | SPECTRE-16928 at 60.1007 ns; 2/256 samples | Observation-only replay fails at the same time | Reproducible solver failure; no valid spectrum. |
| ss_low_125 track | SFDR 63.13694 dBc, SNDR 63.06129 dB; 256/256 samples | 63.15043 dBc, 63.07558 dB; 256/256 samples | Converged failure against 85/80 dB limits. |

SOA crosscheck uses effective reltol 1e-8, vabstol 10 nV, traponly and
maxstep 1 ps. Tracking uses effective reltol 1e-7 and vabstol 10 nV;
its crosscheck changes gear2only to traponly with maxstep 1 ps. Hot-track
sample differences are 5.765 uV rms and 10.841 uV maximum. Both complete
hot-track jobs were recovered after controller interruption; staged decks,
testbenches and dependencies matched before official measurement and recording.
The attempted cancellation was not executed before the jobs finished.

## Localization and interface distinctions

The three SOA rows are the same TOP-PHI_SB stress: MTP Vgd and MTD Vgs/Vgd.
Primary continuous intervals above 1.1 V are 124.228, 127.281 and 124.338 ps
near 10.1, 30.1 and 50.1 ns. At the largest peak, VIN=0.946488 V,
TOP=1.256859 V, CONV=0, PHI_S=0.81 V and PHI_SB=0. It occurs during
sampling restoration. It is not caused by summing separate periods.

The cold-track replay changes only waveform saving. Its 62 selected voltages
contain 41588 accepted points, ending at 60.100662546 ns. The last 0.396 fs
contains 2209 steps smaller than 0.01 fs; preceding cycles have none.
SAMP_ON is rising and APGATE falling. At failure TOPP=0.698 V and
TOPN=0.232 V while PHI_SB=0, so the simultaneous top-reset stress is below
1.1 V. This does not establish a shared root cause with the SOA failure.
The log shows a solver abort; earlier device warnings do not identify its cause.

The SOA bench drives the input extremes directly with 100 ps edges and
exercises DAC decisions. Track uses a continuous sine through 50 ohm per
side with neutral DAC decisions. Both use ideal phase/bootstrap generators
and an ideal reference. These are existing test requirements, not grounds
for relaxing limits or changing the public stimulus. Candidate behavior,
source-impedance interaction and the numerical solver still need separation.

## Settling convergence

At ss_low_125, primary RL12/RL5/start are 39.7/57.9/97.9 ps. Private
traponly, 1 ps, effective reltol 1e-7 and 10 nV gives 39.6/58.3/98.4 ps.
A further refinement (logged maxstep 0.5 ps, effective reltol 1e-8, 1 nV)
gives exactly the same timing readings on the 0.1 ps measurement grid.
Its saved wave has one 1 ps interval at 5.01 ns; other intervals respect
0.5 ps. The stricter result passes, but the primary start reading is
optimistic by 0.5 ps; its narrow margin is explicitly retained as a caveat.

## Bounded next-step proposal, not yet executed

1. One cold-track integration-method diagnostic: retain original stimulus,
   circuit, stop time and tolerances; use the existing traponly/1 ps
   crosscheck settings. Capture the same switching nodes. Bound observation
   to progress past 80 ns or a 10-minute solver budget, then stop and retain
   partial data as diagnostic only. Compare shared sample times and the
   failure neighborhood; calculate no truncated acceptance spectrum.
2. One hot-track observation diagnostic with unchanged primary settings:
   inspect the first judged cycles, selected input-switch/reset currents,
   Vgs/Vds and residual tracking error. Bound it to 100 ns of progress or
   10 minutes. Check its sample prefix against the already complete record.
   This distinguishes incomplete tracking, charge injection and reset timing
   before selecting a circuit change.
3. Only if those measurements identify a limiting path, propose one isolated
   internal change supported by measured charge/current or settling time.
   Preserve all ports and external phases, validate changed PDK parameters,
   and rerun cold SOA plus hot track before broader tests. Do not perform a
   blind size sweep. If attribution remains unclear, report that uncertainty
   before further experiments. No public settings or limits change is proposed.

Source/deck/log/sample and reduced SOA-table archives have per-file remote
hash checks. No incomplete samples are used for an acceptance result.
