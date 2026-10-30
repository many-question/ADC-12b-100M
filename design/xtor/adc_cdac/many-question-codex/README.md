# CDAC candidate

This work-in-progress 28 nm HPC+ candidate now uses the exact N4 dummy
variant that completed the limited same-source checks below. It has
540 MOS per half, 31 subcircuits, physical MOM arrays, split-supply
reference drivers, physical midpoint initialization, NMOS charge sharing,
and pulsed PMOS assistance during sampling entry. The differential test
uses two copies, totaling 1,080 MOS. Candidate status remains `wip`.

The complete RNL matches the frozen physical circuit after collapsing only
zero-volt measurement probes. Every functional device, geometry, port,
control connection, and capacitance is unchanged from that checked variant.
The emitted formal RNL differs from its frozen private RNL only in the
package-reference location. Pinned drawing checks report zero errors,
warnings, or hints; all 31 subcircuits are rendered and representative
TOP, bit, driver, and pulse sheets have been inspected.

## Circuit and parasitic assumptions

The 26 half weights use identical physical MOM units for integer portions
and two units in series for each remaining half unit. Weights 180 and 32
are excluded from sampling. There are 2,278 physical MOM units per half.
Each has a user-specified bottom-plate-to-VSS estimate of 5% of its
1.00229 fF nominal capacitance. This is an ideal pre-layout estimate,
not an extracted value or a parameter already included in the two-terminal
MOM model. Both units in every series tail contribute separately: one at
MID and one at the bottom plate. Each contribution is 0.0501145 fF.
The 36 aggregated Cp elements total 114.160831 fF, including 0.300687 fF
at the six series midpoints. The equivalent half-unit capacitance is not
used to calculate these parasitics.

Input NMOS switches scale with sampled weight, with total width 48.69 um.
Physical transmission gates initialize the six MID nodes to VIN while
sampling. Non-sampled pairs remain reference-driven. DVDD prelogic controls
reference-rail final inverters; the full reference swing reaches the
output gates. Internal ENB controls NMOS charge sharing, while a physical
MOS pulse circuit limits PMOS-to-VIN assistance to sampling entry.

The directly clocked TOP transmission gate has N/P total widths 12/4 um.
One additional NMOS per half has D/S tied to TOP, gate at PHI_SB, bulk at
VSS, W=4 um, L=30 nm, and two fingers. Its purpose is to alter switching
charge and redistribution. The observed final-harmonic improvement is not
uniquely attributable to TOP-opening charge cancellation. Added TOP load,
clock charge, gain changes, and higher harmonics are retained in the audit.

## Limited evidence on this exact physical version

These are independent frozen-source experiments before formal-source
promotion. They are not relabeled as clean official runs on the newly
committed source.

| Check | Result and scope |
|---|---|
| Original weights/calibration | All five required metrics pass: Cs 2.065012 pF, full scale 0.993034 V, calibration margin 0.369061 LSB, calibrated ENOB loss 0.000364 bit, TOP gain 0.893800 |
| Original 70 ns fixed-input sequence | All ten required metrics pass: RL12 35.3 ps, RL5 47.3 ps, time constant 9.16361 ps, conversion-start settling 83.4 ps, droop 0.00443904 LSB, Qref 1.124578 pC |
| Total clock/control port capacitance | DH5/PHI_S/PHI_SB/CONV = 0.830865/6.433830/12.242328/9.849301 fF, all within limits |
| Full 70 ns project stress | 540 MOS / 1,620 gs/gd/ds pairs, all 231,022 saved times: no violations; maximum 0.977333326 V |
| Full 125 ns sine project stress | Both halves, 1,080 MOS / 3,240 pairs, all 343,433 saved times: no violations; maximum 0.990224783 V |

The two stress records include time zero and use a 0.5 ps maximum step.
The sine record leaves only 9.775 mV to the project 1.0 V terminal-pair
limit. Model warnings, including gate-to-bulk and 0.99 V checks, remain
retained separately. These records use ideal bootstrap and do not prove
all-phase, startup, long-hold, PVT, or model-reliability acceptance.

The held dummy D+S charge/voltage ratio is approximately 5.38-5.64 fF
along the tested RL steps after leakage correction. It is a trajectory-
dependent branch load, not a constant or complete held-node capacitance.
PHI_SB is measured at the total port; the dummy's same-window gate branch
accounts for about 2.37629 fF of the 12.24233 fF total. Reference plus
internal DVDD prelogic charge excludes other supply branches and ideal
clock/bootstrap sources, so it is not total power or a ranking result.

The matched 48-point differential h3 improves from -83.9867/-83.9393 to
-86.4998/-86.4153 dBc for the h7/h21 bases using each circuit's own
fundamental. With the frozen baseline fundamental, the new values are
-86.5182/-86.4337 dB. The fundamental decreases 0.2111%; h5 and h7 increase.
Removing only DC and the fixed-frequency fundamental leaves residual RMS
37.3746 -> 31.7322 uV. This noncoherent fit is not official SFDR/SNDR or
THD. The h3 diagnostic margin is only about 1.42 dB.

The [detailed diagnosis](sampling-entry-diagnosis.md) retains the full
sequence of failures, complex phasors, both halves, and measurement
limitations. Raw files, frozen inputs, analysis, and recoverable archives
are hash-verified and retained outside the public repository.

## Formal TT verification and retained failures

The former formal circuit at `2ecc285`, with all its formal results,
remains available through
[the pre-N4 history tag](https://github.com/many-question/ADC-12b-100M/tree/adc-cdac-many-question-pre-n4-20261030).
It failed RL12 settling (50.1 ps), Qref (2.629 pC), tracking SFDR
(69.6121 dBc), SNDR (69.5735 dB), and separately checked sampling/output
stress. Those failures have not been erased or marked as passes.

Promoting the new source makes those old result fingerprints stale.
The current official TT weights and settling tests must be rerun on a
clean committed source before 256-point tracking. The selected next
spectral check is the project's complete coherent 256-point record,
with official preparation, analysis, and figures; no additional 128-point
diagnostic is planned. Main tracking runtime is roughly 122 minutes,
excluding retrieval/analysis and a separate required convergence check.
A failing main result requires an audit before a cross-check run; a
passing main result still requires the specified numerical comparison.

The current project tracking settings are reltol 1e-7, voltage tolerance
1e-8, maxstep 1 ps, and traponly; its cross-check uses 0.5 ps and gear2only.
Official weights/settling use their own current configuration, which is
recorded as actually used rather than equated to the stricter private
stress diagnostics. No clean official TT result for the promoted source
is claimed at this source-only stage.

The candidate acknowledges notices #17 and #37. PVT, actual-bootstrap
integration, supply startup, long-hold behavior, full corner coverage,
and project-lead verification remain outstanding. No ready or selection
status is claimed.
