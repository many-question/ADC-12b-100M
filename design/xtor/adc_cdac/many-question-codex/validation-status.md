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

## Completed bounded diagnostics

Both retain the original 2.605 us requested stop, source and tolerances;
each was intentionally interrupted at its progress bound (rc=2, SPECTRE-25).
No partial acceptance FFT was calculated. The first cold attempt stopped at
30.086858 ns because the watchdog misread an incomplete timestamp. Its
evidence is preserved; the parser was fixed and tested on truncated lines.
Only that instrumentation failure was repeated.

Cold retry `20261104-103853-f4d4` reached 80.050462 ns, with 105864 points
and four samples, using traponly/1 ps and effective 1e-7/10 nV. Near the
old failure (60.099..60.102 ns), 33 steps have minimum 61.675 fs and no
sub-0.01 fs cluster, versus 2209 such steps in the failed primary replay.
The whole retry has only two isolated sub-0.01 fs steps at other times.
Its two shared samples differ by 9.772 uV rms, 9.968 uV maximum.
This establishes sensitivity to integrator/step settings, not a full cold
pass or the identity of a failing device/model; those two effects are not
separated by this experiment.

Hot observation `20261104-103000-62d8` reached 100.064429 ns and contains
all 64 requested voltages and 22 native currents. Its six sample times
match the original complete run; values agree within 3e-13 V. The native
source-resistor currents agree with (SRC-VIN)/50. Full-record analysis,
not the partial trace, identifies H3 at 545.39 uV peak (98.27% of residual
power), versus 30.05 uV in TT.

On a uniform 1 ps grid at 40..99.9 ns, track phase 1..4.8 ns, per-side rms
TOP-VCM is 39.45..39.66 mV, VIN-BH12 is 2.95..2.97 mV, and SRC-VIN is
18.47..18.54 mV. Reset-terminal delta-V/I is about 105..131 ohm, versus
33..36 ohm for the bit-12 input path; these include displacement current.
VGS stays within 2.6 uV of 0.81 V. Early portions still include recovery;
these are not DC resistance or output-distortion allocations.

At the first judged sample, low-TOP MTN current is -0.749 uA and high-TOP
MTP current +0.577 uA despite reset being off; selected bit-12 input
branches carry about 20 uA. Differential TOP changes 22.83 uV in the final
50 ps before that sample, whose complete-record residual is 446.18 uV.
Thus finite reset impedance, edge injection and hold currents all remain
plausible contributors. Partial-window harmonic fits vary with fit order
and are rejected as a unique attribution of the complete-record H3.

The reset path is the first candidate for a controlled causal experiment,
but widening it also changes off-current and injection. No dimension change
is yet justified as a demonstrated repair. Next isolate its on-state effect
from edge/hold effects in one explicitly scoped diagnostic before selecting
one internal change. Keep external ports/phases and official precision;
validate changed PDK parameters and cold SOA/hot track before expansion.

All three bounded-run directories (including the instrumentation failure)
have 62-file remote hash matches and verified ZIP archives. Source SHA is
unchanged. Server audit at 2026-11-04 16:54:46 +08:00 found no active owned
CDAC processes. Original failures remain authoritative; all three blockers
are still open.
