# CDAC candidate

This candidate is work in progress. It uses the specified 26 half weights,
with weights 180 and 32 excluded from sampling. Identical MOM units form the
integer portions of each half weight. Two units in series form each remaining
half unit. All array capacitors and switches are PDK devices.

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
midpoint stability. Artificial midpoint capacitance sweeps are sensitivity
studies only; the capacitance values have not been extracted from layout.

Two equal series units have one-quarter capacitance sensitivity to each unit.
Independent unit errors therefore give half-unit relative mismatch equal to
the unit relative mismatch divided by sqrt(2), before midpoint parasitics and
correlation. This calculation does not validate the process mismatch model or
replace the official weight and calibration tests.

The candidate is based on the current module specification and acknowledges
notifications #17 and #37. Initial official TT weights and settling measurements
are the next milestone. Tracking, convergence comparisons, representative PVT,
complete corner coverage, long-hold behavior, device stress, and joint bootstrap
validation remain outstanding. No selection or signoff is claimed.
