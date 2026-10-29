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
on the frozen circuit. Tracking with its numerical cross-check is in progress.
An exploratory run with the official settling stimulus and ideal bootstrap,
adding only zero-volt current probes, found a 1.06433 V peak absolute Vgd on
one sampling switch. This exceeds 1.0 V and remains unresolved. That diagnostic
covers the sampling switches, not complete device stress or a joint bootstrap
implementation.
Convergence comparisons, representative PVT,
complete corner coverage, long-hold behavior, device stress, and joint bootstrap
validation remain outstanding. No selection or signoff is claimed.
