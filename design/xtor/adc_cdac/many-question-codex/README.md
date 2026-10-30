# CDAC candidate

This candidate is work in progress. It uses the specified 26 half weights,
with weights 180 and 32 excluded from sampling. Identical MOM units form the
integer portions of each half weight. Two units in series form each remaining
half unit. The functional array capacitors and switches are PDK devices.

Every physical MOM unit also has an ideal bottom-plate-to-VSS capacitance of
5% of its nominal unit capacitance. This is a user-specified pre-layout estimate,
not a PDK parameter or an extracted layout value. The two-terminal MOM model
does not already include this ground capacitance. Parallel banks aggregate
their unit contributions at their common bottom plate. In each TOP--MID--B
series tail, the first unit adds its parasitic at MID and the second at B.
Each is 0.0501145 fF, based on the 1.00229 fF physical unit; the half-unit
equivalent is not used to calculate this parasitic. There are 2,278 physical
units and 114.160831 fF of added ground capacitance in total. Six series
midpoints account for 0.300687 fF; the bottom-plate nodes account for the rest.

The input NMOS switches scale with sampled weight, subject to minimum device
size; their total width is 48.69 um. This is a starting point for characterization,
not an assertion of compatibility with a particular bootstrap candidate.
The top-plate transmission gate receives PHI_S and PHI_SB directly. The input
load, sampling distortion, gate charge, and terminal-voltage limits must all
be measured with the actual circuit.

Command buffers and tristate drivers use the reference supply so that the
output PMOS gate reaches VREFP even when DVDD is lower. A driver computes
GP = NAND(EN, HI, NOT(GN)) and GN = NOR(ENB, HI, NOT(GP)). The feedback delays
turn-on until the opposite gate turns off. Actual overlap charge and settling
remain measurements, rather than consequences assumed from Boolean logic.

The two-terminal MOM model does not represent midpoint-to-substrate parasitics
or an explicit physical DC path. Spectre reports automatic Gmin insertion at
the floating series midpoints. The small-structure study uses no prescribed
node initial conditions or added leakage device. Its repeated pulses, alternate
initial source levels, and Gmin checks do not establish long-term physical
midpoint stability. Earlier artificial midpoint capacitance sweeps were
sensitivity studies. The current 5% values above are an explicit pre-layout
assumption and have not been extracted from layout.

Two equal series units have one-quarter capacitance sensitivity to each unit.
Independent unit errors therefore give half-unit relative mismatch equal to
the unit relative mismatch divided by sqrt(2), before midpoint parasitics and
correlation. This calculation does not validate the process mismatch model or
replace the official weight and calibration tests.

The candidate is based on the current module specification and acknowledges
notifications #17 and #37. The initial official TT run before the 5% estimate
passed the five weight/calibration metrics but failed RL12 settling
(49.3 ps against 40 ps) and reference charge (2.562 pC against 1.2 pC).
That evidence remains in commit history and does not validate the current
parasitic model. With the 5% estimate, official TT weights/calibration pass:
C_S = 2.061 pF, full scale = 0.9931 V, calibration margin = 0.4409 LSB,
calibrated ENOB loss = -0.01008 bit, and top gain = 0.8886. Settling still
fails RL12 (50.1 ps) and reference charge (2.629 pC); the other eight settling,
droop, and input-capacitance metrics pass. These are preliminary TT results
on the frozen circuit. The strict TT tracking baseline also fails:
SFDR = 69.6121 dBc (limit 85 dBc), SNDR = 69.5735 dB (limit 80 dB).
It completed with the specified 1 ps maximum step, traponly, reltol 1e-7,
and voltage tolerance 1e-8. The numerical cross-check was deliberately deferred
after auditing this failure, so the recorded cross-check status is incomplete
(scheduling return code 125; no simulator was launched for it). It has not
passed a convergence comparison. Short causal diagnostics take priority.
An exploratory run with the official settling stimulus and ideal bootstrap,
adding only zero-volt current probes, found a 1.06433 V peak absolute Vgd on
one sampling switch. This exceeds 1.0 V and remains unresolved. That diagnostic
covers the sampling switches, not complete device stress or a joint bootstrap
implementation. Additional checks of the 52 output devices found a worst
absolute Vds of 1.15899 V on an H-side output NMOS during sampling entry.
That check uses recorded bottom-plate and gate voltages and the exact ideal
reference rails. On the frozen `2ecc285` circuit, the exact maximum is at
20.127200335 ns on j12H: D = 1.1589942 V, G = 0.0004423 V, S = B = 0 V.
This is positive H-bottom-plate overshoot with ideal VG generation and the
5% parasitic estimate. The 22 sampling and 52 output devices checked so far
do not cover all 626 MOS instances. Bottom-plate overshoot is another unresolved
stress failure; improving the sampling switches alone is not sufficient.
The [sampling-entry and driver diagnosis](sampling-entry-diagnosis.md)
confirms both failures with a finer step and compares isolated timing, VG,
top-plate, and sampling-width changes. Later unselected variants pass the
full 70 ns TT stress check at VIN=0.65 V together with the listed settling
and charge limits; one also passes the five weight/calibration limits with
physical midpoint-initialization switches. These limited experiments do not
validate the frozen circuit or establish complete acceptance.
A 32-sample diagnostic on that variant estimates the third harmonic at
-75.13 dBc, improved from the frozen circuit but still requiring further work;
it is not an official SFDR/SNDR or convergence result.
A subsequent 125 ns sine-input check of all 1,008 MOS in both halves finds
70 failing terminal pairs, with 1.14792 V output stress and 1.00487 V sampling
stress. The fixed-input experimental passes do not extend to this stimulus.
A later variant combines NMOS sharing with PMOS-to-VIN assistance and stronger
nonsampled outputs. It has zero project stress violations over both the
125 ns sine stimulus (maximum 0.98568 V) and the original 70 ns control sequence
(0.97887 V). RL12 = 35.3 ps and Qref = 1.1072 pC also meet their limits, but
PHI_SB capacitance = 45.13 fF fails the 40 fF limit. Its matched 32-sample
diagnostic gives h3 = -72.56 dBc, worse than PMOS assistance alone. Reducing
only the top-plate N/P switches from 32 to 16 um each lowers PHI_SB capacitance
to 37.04 fF while retaining RL12 = 35.3 ps, Qref = 1.1039 pC, and zero stress
violations in the 70 ns control sequence. Its matched 32-sample diagnostic
gives h3 = -75.11 dBc, an improvement of about 2.55 dB that still leaves
linearity unresolved. It has no sine-stress or official tracking acceptance
yet. Driving the NMOS sharing gates from internal ENB instead of PHI_S also
passes the 70 ns checks, but its matched h3 = -75.71 dBc gives only another
0.61 dB improvement. Moving PMOS assistance to EN gives h3 = -76.13 dBc but
increases Qref to 1.1855 pC, leaving little charge margin. These short-record
results do not justify adopting that higher-charge variant. Returning PMOS assistance to PHI_SB and reducing only
the top N/P switches from 16 to 8 um each gives h3 = -79.90 dBc in the matched
32-sample diagnostic, approximately 4.18 dB better than the ENB-sharing 16 um
case. Its own 70 ns fixed-input check gives RL12 = 35.2 ps,
Qref = 1.12394 pC, PHI_SB capacitance = 32.99 fF, and zero violations across
1,578 terminal pairs (maximum 0.97734 V). Sine-input stress and official
linearity acceptance remain unverified for this geometry. Further reducing
only the top N/P switches to 4 um worsens the matched third harmonic to
-61.99 dBc; that geometry is not pursued. These experiments have not
replaced the candidate. A subsequent physical pulse circuit limits PMOS
assistance to sampling entry while retaining the 8 um top switches. Its
70 ns fixed-input check covers all 539 MOS, with zero stress violations
(maximum 0.97736 V), RL12 = 35.2 ps, and Qref = 1.12350 pC. Internal DVDD
logic charge increases by about 0.183 pC, while matched h3 worsens to
-75.08 dBc. Lower fifth and seventh harmonics do not offset this third-
harmonic deterioration. The pulse with 8/8 um top switches remains unselected;
its fixed-input pass does not establish sine-input or PVT acceptance.
Changing only the pulse circuit's top N/P widths to 12/4 um gives matched
h3 = -81.62 dBc. This geometry has no own fixed-input or sine-stress pass.
A read-only fit-basis audit also finds that some 32-point harmonic estimates
change substantially when higher odd harmonics are included. These short
comparisons need longer phase coverage before a near-limit design choice;
no alternative fit is used to claim a pass. The continuous-assistance 12/4 um
48-point audit gives h3 = -78.66 to -78.74 dBc across the tested bases,
with much lower condition numbers. Its first-32 fit predicts the remaining
16 points with 46.55 uV RMS error, exposing the short-window limitation.
All 17 contiguous 32-point windows, with the same basis, span 6.53 dB in
estimated h3 without any circuit change.
This source has little apparent linearity margin. The next diagnostic
freezes the existing pulse-assisted 12/4 um circuit and extends its record
to 128 points. All remain LS diagnostics rather than official spectra.
Convergence comparisons, representative PVT,
complete corner coverage, long-hold behavior, device stress, and joint bootstrap
validation remain outstanding. No selection or signoff is claimed.
