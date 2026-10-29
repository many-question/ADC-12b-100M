# Sampling-entry diagnosis

These are private exploratory simulations of the circuit frozen at `2ecc285`,
reported on 2026-10-30. They do not replace the official test results or validate
an actual bootstrap circuit. All cases retain the user-specified 5% ground
capacitance on each physical MOM unit, including both units of every series tail.

The six cases use TT, VIN = 0.65 V, the first 34 ns of the official settling
stimulus, maximum step 0.5 ps, reltol 1e-7, and voltage tolerance 1e-8. Inputs
and retrieved simulator outputs were hash-verified. The sampling check covers
22 devices and 66 gs/gd/ds pairs, or 44 devices and 132 pairs in the doubled-width
case. The output check covers 52 devices and 156 pairs in every case. Internal
logic and top-switch stress are outside this six-case comparison.

| Case | Sampling peak absolute voltage (V) | Failing sampling pairs | Output peak absolute voltage (V) | Failing output pairs |
|---|---:|---:|---:|---:|
| Frozen baseline, finer step | 1.06736 | 7 | 1.15921 | 22 |
| Recorded VG imposed by an ideal PWL source | 1.06400 | 7 | 1.15921 | 22 |
| Same recorded VG, TOP clamped to VCM | 1.01509 | 5 | 0.98110 | 0 |
| CONV falls 40 ps earlier; PHI_S/PHI_B unchanged | 1.06713 | 7 | 1.15866 | 22 |
| Behavioral VG turn-on transition 120 ps, instead of 60 ps | 0.95397 | 0 | 1.14560 | 22 |
| Two copies of every sampling MOS | 0.94779 | 0 | 1.18106 | 24 |

The limit is 1.0 V, including brief excursions. Counts above apply to this
34 ns interval; the earlier 70 ns output check found 26 failing pairs. The PWL
trace was recorded in that earlier run. It reproduces its VG waveform, not the
slightly different waveform produced by the finer-step baseline.

![Sampling-entry comparisons](sampling-entry-core-six.png)

The replay/clamp pair supports a contribution from TOP motion to H-side
bottom-plate overshoot. The clamp disables normal conversion and changes the
initial charge state, so it is an isolation experiment, not a repair or a
quantitative prediction of a stronger physical top switch. Residual sampling
stress with the clamp shows that local bottom-plate charging also matters.
Advancing CONV alone has little effect in this case.

Slowing VG or doubling the sampling devices removes the observed sampling
violations over this interval, but neither removes output-device violations.
Doubling sampling width from 48.69 to 97.38 um increases the measured VG rise
charge from 38.47–40.24 fC to 76.95–80.48 fC and peak rise current from about
1.05 to 2.13 mA. This uses the ideal behavioral gate source and excludes wire
capacitance. A width-only change is therefore not selected.

The physical follow-ups below test stronger top-plate clamping and H/L charge
sharing during sampling. Any implementation must check sampling, output, top-switch, added,
and internal devices, as well as settling, reference charge, tracking distortion,
and joint bootstrap behavior. The candidate remains `wip`.

## Physical follow-ups

Two further hypotheses retain the original clock stimuli and the same 5%
parasitics. The first duplicates both top-plate TG devices. The second adds two
copies of each sampled pair's validated input-NMOS geometry between its H and L
bottom plates, gated directly by PHI_S; non-sampled pairs remain unchanged.
These are exploratory variants, not changes to the committed circuit.

| Variant and interval | MOS / gs-gd-ds pairs checked | Failing pairs | Maximum absolute voltage (V) |
|---|---:|---:|---:|
| Top TG doubled, 34 ns | 628 / 1,884 | 29 | 1.13112 |
| Pair charge sharing, 34 ns | 648 / 1,944 | 0 | 0.97255 |
| Pair charge sharing, full 70 ns | 648 / 1,944 | 11 | 1.07948 |

The 34 ns result does **not** establish a repair. Over 70 ns, the pair-sharing
variant has ten failing output pairs and one failing sampling pair. The exact
output maximum is j5L NMOS Vds = 1.079480 V at 40.127138 ns. Before that sampling
entry, both j5 bottom plates are at 0.899935 V, so local sharing cannot lower
their voltage. At the peak, TOP = 0.462507 V and VG = 1.028191 V. After the full
13-step pattern, j0L sampling Vgd reaches -1.003500 V at 60.086107 ns, with
VG = 0.002114 V and its bottom plate at 1.005614 V. A short excursion is still
a failure.

The full interval saves all MOS terminal nodes and checks 173,039 time points.
The added sharing devices and top TG stay within the project gs/gd/ds limit in
this run. Other model voltage warnings are retained; this table does not claim
that every model warning or a supply-ramp startup check has passed.

Using the official settling measurement on the private 70 ns variant gives
RL12 = 50.4 ps and reference charge = 2.671275 pC, both failing their limits.
PHI_S capacitance is 31.1848 fF, PHI_SB is 16.1850 fF, and CONV is 9.8492 fF.
Zero-volt output-source probes partition reference charge into 1.116475 pC
through the output PMOS source/bulk branches and 1.554800 pC through the other
logic. These figures motivate further driver work; no new official acceptance
result or candidate selection is implied.

## Driver and supply-domain comparisons

Further private experiments use the full original 70 ns TT settling sequence,
the same physical-unit 5% estimate, and a 0.5 ps maximum step. All MOS terminal
nodes are saved. These are unselected circuit variants; the committed netlist
and official results still describe `2ecc285`.

The shared-node variant connects each sampled bottom plate through one
PHI_S-controlled NMOS to a common internal node. It improves the pair-sharing
result but still fails. After the full decision pattern, j0L output Vgd reaches
1.009743 V: its bottom plate is 0.984858 V while GN has undershot to -0.024885 V.
The sampling-switch maximum is 1.000276 V, also a failure. The shared node has
no extracted wire capacitance in these experiments.

The simpler driver uses skewed NAND2/NOR2 gates and removes the turn-off
feedback. The split-supply driver moves command and enable prelogic to the
specified DVDD port, followed by standard-threshold inverters that restore
GP/GN to the reference rails. Its H and L command paths are also shortened.
Both driver families use 75% of the original output width, with geometry
validated before simulation. Boolean functions alone do not establish
non-overlap.

| Variant | Sharing arrangement | MOS / failing gs-gd-ds pairs | Maximum (V) | RL12 (ps) | Qref (pC) |
|---|---|---:|---:|---:|---:|
| Original feedback driver | Shared node | 648 / 4 | 1.00974 | 50.2 | 2.639093 |
| Simple driver, low threshold | H/L pair | 440 / 18 | 1.08464 | 36.8 | 2.272340 |
| Simple driver, standard threshold | H/L pair | 440 / 36 | 1.09772 | 48.2 | 1.505366 |
| DVDD prelogic, low-threshold outputs | Shared node | 492 / 2 | 1.00150 | 30.5 | 1.236260 |
| DVDD prelogic, standard-threshold outputs | Shared node | 492 / 9 | 1.02125 | 34.1 | 1.071765 |

Limits are 1.0 V, 40 ps, and 1.2 pC respectively. The last row satisfies the
two listed performance limits in this experiment but fails device stress.
The two failures in the preceding row are Vgd and Vds of the same j0H output
NMOS near 30.086 ns; the small excess is not rounded into a pass. Its sampling
maximum is 0.99889 V, leaving little margin. No row is a complete repair.

The supply split also changes where energy is drawn. Over the official
54.8–64.8 ns charge window, zero-volt probes give:

| Output threshold | Reference output branches (pC) | Other reference branches (pC) | DVDD prelogic (pC) | Signed sum (pC) |
|---|---:|---:|---:|---:|
| Low | 1.034075 | 0.202185 | 0.902989 | 2.139249 |
| Standard | 0.875401 | 0.196364 | 0.902991 | 1.974755 |

The DVDD column measures internal prelogic only; these sums exclude direct
DVDD current into the top-switch bulk and ideal external clock and bootstrap
sources. The integrated minimum of the positive
P-output-source and N-output-source currents is 0.153061 pC and 0.014734 pC,
respectively. This proxy includes leakage and displacement current and does
not prove channel-current non-overlap or safety at other supply values.

## Limited TT passes with smaller output devices

Two subsequent variants retain the split supply and shared sampling node. One
reduces low-threshold output width to about 50% of the original, with j0 output
N/P widths of 0.12/0.24 um. The other retains standard-threshold 75% outputs,
reduces both j0 and j1 to those widths, and adds a physical transmission gate
from each of the six series midpoints to VIN. These minimum-size midpoint
switches use PHI_S/PHI_SB and open with the top-plate switch. Their junction
and gate parasitics are part of the simulated circuit.

| Variant, original 70 ns TT sequence at VIN=0.65 V | MOS / gs-gd-ds pairs | Failing pairs | Maximum (V) | RL12 (ps) | Qref (pC) |
|---|---:|---:|---:|---:|---:|
| Low-threshold 50% outputs, smaller j0 | 492 / 1,476 | 0 | 0.98671 | 34.9 | 1.116935 |
| Standard-threshold 75% outputs, smaller j0/j1, physical MID switches | 504 / 1,512 | 0 | 0.99707 | 34.1 | 1.068123 |

These are **limited experimental passes**, not a validation of the committed
candidate. In the second row, the sampling maximum is 0.99351 V and the output
maximum is 0.99707 V, leaving little voltage margin. RL5 is 46.2 ps, conversion
start is 80.0 ps, tau is 9.989 ps, and droop is 0.002369 LSB. PHI_S/PHI_SB/CONV
capacitance is 27.814/16.610/9.849 fF. Internal DVDD prelogic draws another
0.902993 pC in the reference-charge window, for a signed two-rail sum of
1.971116 pC, excluding direct DVDD top-switch bulk current and ideal external
clock and bootstrap sources.

The second variant also passes the five weight and calibration limits with the
original weight stimulus: C_S = 2.065030 pF, top gain = 0.888807, full scale =
0.992823 V, minimum calibration margin = 0.369004 LSB, and calibrated ENOB loss
= 0.001320 bit. The actual midpoint-switch parasitics reduce the j0 weight to
0.9038 LSB; this 9.61% maximum nominal weight error is retained in the evidence,
and the measured array remains calibratable under the specified model.

At seven late-tracking observations, all six midpoints agree with VIN within
the transient voltage tolerance. Over the 4 ns quiet-hold windows in the first
two conversions, their largest voltage drift is 17.53 uV. This establishes
physical initialization for this stimulus, not long-term behavior across the
full input range or supply-ramp startup. The simulator still reports a roughly
11.4 uV Gmin influence on an internal logic node; no global Gmin-independence
claim is made.

Complete tracking acceptance, actual-bootstrap integration, startup, and PVT
remain unverified for these variants. Original failures and all model warnings remain
in the retained evidence. In particular, a pass against the project's
gs/gd/ds criterion is not a claim that every model-specific voltage warning
has passed. The formal netlist and official results have not been replaced.

## Short tracking probe of the midpoint-switch variant

The standard-threshold smaller-j0/j1 variant with physical midpoint switches
was also run for 32 samples at 48.828125 MHz, using the original 50 ohm sources,
ideal VG generators, 1 ps maximum step, traponly, reltol 1e-7, and voltage
tolerance 1e-8. A least-squares fit at the known fundamental and odd harmonics
3, 5, and 7 gives:

| Diagnostic | Frozen circuit, first 32 samples | Midpoint-switch variant, 32 samples |
|---|---:|---:|
| Third harmonic relative to fundamental (dBc) | -69.6431 | -75.1339 |
| Fifth harmonic relative to fundamental (dBc) | -90.6398 | -87.6231 |
| Seventh harmonic relative to fundamental (dBc) | -103.2819 | -90.9593 |
| Residual RMS after fitting (uV) | 0.46 | 7.76 |

The frozen-circuit reference reuses its completed strict run; that simulation
was not repeated. The third harmonic improves by about 5.5 dB, but the new
variant still needs substantial linearity improvement. This short regression
is not an FFT, SFDR/SNDR result, or numerical convergence comparison. The
noncoherent 32-sample fit has condition number 9.84, and its higher residual
also limits interpretation of individual fitted harmonics.

Additional voltage observations at PHI_S falling and immediately before VG
turn-off show large, opposing VIN and TOP harmonic terms. The top-plate switch
is already opening during the PHI_S crossing, so the observed VIN harmonic
cannot be assigned directly to final sampled error. A static-gain charge
reconstruction is only approximate: finite tracking lag, nonlinear parasitics,
and switch injection remain mixed. The separate sine-input stress result below
finds additional failures; the remaining physical sampling changes require
new evidence.

A matched 32-sample comparison removes only the 12 MID-switch MOS devices
while retaining all 5% capacitances and the rest of the circuit. It gives
h3 = -75.1170 dBc and a 7.748 uV fit residual, versus -75.1339 dBc and 7.757 uV
with the switches. This small change does not support the MID switches as
the dominant source of the observed third harmonic. The comparison removes
their parasitics and initialization together, so it does not isolate either
effect individually. Its missing physical initialization path excludes it
from adoption.

## Sine-input stress of the midpoint-switch variant

The same unselected variant was checked over 125 ns with the original sine
sources and ideal VG generators. Both CDAC halves save every MOS terminal
from time zero: 1,008 devices, 3,024 gs/gd/ds pairs, and 282,412 accepted time
points with a 0.5 ps maximum step. The stimulus uses 48.828125 MHz, -1 dBFS,
50 ohm per side, traponly, reltol 1e-7, and voltage tolerance 1e-8.

| Device group, both halves | MOS | Failing pairs | Maximum absolute terminal difference (V) |
|---|---:|---:|---:|
| Sampling NMOS | 44 | 10 | 1.00487 |
| Output N/P | 104 | 60 | 1.14792 |
| Shared-node NMOS | 44 | 0 | 0.99899 |
| Top-plate TG | 4 | 0 | 0.89808 |
| MID TG | 24 | 0 | 0.94974 |
| Other logic | 788 | 0 | 0.96837 |
| Total | 1,008 | **70** | **1.14792** |

![Sine-input stress by device group and the worst sampling-entry overshoot](sine-entry-stress.png)

The exact maximum occurs at 10.111177551 ns on the P-side j12H output NMOS:
D = 1.147915514 V, G = 4.719 uV, and S = B = 0 V. At that instant CONV is
low, PHI_S is high, TOP is 0.414483 V, VIN is 0.481908 V, and VG is 0.558330 V.
The high bottom plate overshoots while TOP returns from its prior held level
to VCM. Thus the earlier fixed-VIN pass does not cover sampling entry after
the larger sine-driven top-plate excursions.

Rechecking all terminal pairs only over 40-125 ns still finds 70 failing
pairs, with a 1.132552531 V maximum on N-side j12H at 40.109095358 ns.
The failure therefore persists beyond the initial four cycles. This interval
comparison does not establish periodic steady state or supply-ramp startup.

A second failure occurs when entering conversion: on the N side, the
nonsampled j9H output NMOS reaches Vds = 1.106712376 V at 5.161260550 ns;
j6H reaches 1.103907729 V. These halves remain connected to their reference
rails, but their finite drive strength permits bottom-plate overshoot as TOP
moves. This is distinct from the sampled-half entry event in the figure.

The sampling-switch maximum is positive Vgd = 1.004872340 V on P-side j10L
at 70.148704136 ns: G = 1.626193151 V, D = 0.621320811 V, and VIN = 0.740160753 V.
The loaded VIN nodes also have brief negative excursions, down to -40.64 mV,
despite the nominal in-range sine sources. These excursions remain part of
the retained evidence.

The run completed successfully and all retrieved raw files were hash-verified.
A private postprocessing error on a pair of grounded terminals was fixed and
the saved waveforms reanalyzed; the simulation was not repeated. The checks
cover the project's gs/gd/ds limit for this stimulus, including its initial
condition and subsequent cycles. They do not establish a supply-ramp startup,
PVT, real-bootstrap, or model-warning pass. The candidate remains WIP and the
frozen official results remain unchanged.

## PMOS sampling assistance and stronger nonsampled outputs

A further physical variant replaces the 22 shared-node NMOS per side with
PHI_SB-controlled PMOS switches from each sampled bottom plate to VIN. Their
widths match the main sampling NMOS widths. It also triples only the j9/j6
output N/P finger counts to strengthen the nonsampled reference connections.
All changed geometries were validated before simulation; the six MID TGs,
clock phases, and 5% estimate remain. These two changes address the distinct
sampling-entry and conversion-entry events above; this comparison does not
isolate their individual effects.

The same 125 ns sine-input check covers 1,008 MOS, 3,024 terminal pairs, and
281,891 accepted points at a 0.5 ps maximum step:

| Group | Failing pairs | Maximum absolute terminal difference (V) |
|---|---:|---:|
| Main sampling NMOS | 0 | 0.98061 |
| New PMOS assistance | 0 | 0.99369 |
| j9/j6 output devices | 0 | 0.98673 |
| All output devices | **36** | **1.11951** |
| Top-plate TG | 0 | 0.88415 |
| MID TG | 0 | 0.93844 |

All remaining failures are on sampled L-side output PMOS devices. The worst
is N-side j12L at 50.099391365 ns: D = -0.219514683 V, G = 0.899838051 V,
and S = B = 0.9 V, giving Vds = -1.119514683 V. At that instant TOP is
0.539874370 V, VIN is 0.322397778 V, VG is 0.238380961 V, PHI_S is high,
and CONV is low. The low bottom plate undershoots while TOP returns toward
VCM. With PMOS assistance and no NMOS sharing path, this negative excursion
remains uncontrolled even though the main sampling-device failures are removed.
This variant is therefore still unsuccessful. Loaded VIN also peaks at
0.934345 V in this run; its input kickback has not been accepted.

Its matched 32-sample tracking probe gives h3 = -77.2407 dBc, h5 = -86.6147 dBc,
h7 = -95.5741 dBc, and a 2.658 uV regression residual. The approximately 2.1 dB
third-harmonic improvement over the MID-switch/shared-node variant remains
insufficient to resolve linearity. The same short-fit limitations apply; this
is not an SFDR/SNDR or convergence pass, and the output stress failure remains.

## Combined physical paths: limited sine-stress pass

Restoring the original 22 NMOS shared-node devices per side while retaining
PMOS-to-VIN assistance and stronger j9/j6 outputs gives 526 MOS per CDAC.
The six physical MID TGs and every 5% unit parasitic remain. The main VG-driven
sampling NMOS width remains 48.69 um per side. This is still an unselected
experimental circuit.

![Positive and negative entry waveforms for NMOS sharing, PMOS assistance, and both paths](sampling-assist-comparison.png)

The matched 125 ns TT sine run checks all 1,052 MOS in both CDAC halves and
3,156 gs/gd/ds pairs. All pairs pass the 1.0 V project limit over 281,800
accepted points, including time zero, with a 0.5 ps maximum step. The deck
hash, device count, complete 0-125 ns coverage, and retrieved raw-file hashes
were checked.

| Device group | Maximum absolute terminal difference (V) | Failing pairs |
|---|---:|---:|
| Main sampling NMOS | 0.97401 | 0 |
| Output devices | 0.98568 | 0 |
| PMOS VIN assistance | 0.95862 | 0 |
| NMOS shared-node path | 0.98568 | 0 |
| Top-plate TG | 0.88250 | 0 |
| MID TG | 0.94166 | 0 |
| Complete circuit | **0.98568** | **0 of 3,156** |

The exact largest difference is 0.985680847 V on N-side j12L output PMOS Vds
at 50.094865824 ns: D = -0.085680847 V, G = 0.899667934 V, and S = B = 0.9 V.
The NMOS sharing device at the same bottom plate has the same magnitude of
Vgd. This leaves only 14.32 mV nominal margin at the worst event.

This pass is limited to the stated TT sine stimulus. Loaded VIN still spans
approximately -34.56 mV to 0.92227 V. Input kickback, other sampling phases,
supply-ramp startup, PVT, real-bootstrap operation, and model-specific warning
limits are not validated by this result. Tracking linearity is checked
separately before any formal adoption.

The original 70 ns TT control sequence also has zero project SOA violations
over 526 MOS / 1,578 pairs, with a 0.97887 V maximum and 164,327 accepted points
at a 0.5 ps maximum step. It gives RL12 = 35.3 ps, RL5 = 47.3 ps, tau = 9.120 ps,
conversion-start settling = 81.5 ps, droop = 0.002368 LSB, and reference charge
= 1.107164 pC, all meeting their respective limits. However, **PHI_SB
capacitance is 45.126 fF and fails the 40 fF limit**. Control, PHI_S, and CONV
capacitances are 0.831, 27.799, and 9.849 fF. The added paths therefore solve
the observed TT stress cases while introducing a clock-load failure.

Reference charge partitions into 0.898882 pC through output PMOS source/bulk
branches and 0.208282 pC through the remaining reference branches, including
the auxiliary and MID switch bulk currents. Internal DVDD prelogic draws
0.902994 pC, giving a reference-plus-prelogic signed sum of 2.010157 pC.
This sum excludes direct DVDD top-switch bulk current and ideal external
clock/bootstrap sources; it is not total circuit power. The candidate remains
WIP, with the committed netlist and official results unchanged.
