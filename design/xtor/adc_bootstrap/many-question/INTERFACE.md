# Bootstrap / CDAC interface constraints

Candidate `many-question`, circuit hash `f9330137569bdf81`. These constraints describe the existing reference-load evidence; they do not establish a maximum admissible VG load or replace validation with the actual CDAC.

## Reference load per CDAC side

| Item | Standard bootstrap testbench |
|---|---|
| Input switch | `nch_ulvt_mac`, total W = 96 µm, L = 30 nm, 48 fingers |
| Ron | 12.5 Ω design target at Vgs = 0.9 V; not a measured BST result |
| Sampling capacitance | 2.057 pF between bottom plate and reset top plate |
| VG wiring | 10 fF to ground, in addition to the MOS gate load |
| Source resistance | 50 Ω |
| Top-plate reset | Ideal PHI_S-controlled relay, 20 Ω on resistance |
| Sampling order | Ideal PHI_S fall precedes PHI_B fall by nominally 40 ps; the project interface permits 20–80 ps |

DC uses one side; differential tracking uses two independent copies. The reference MOS presents voltage-dependent gate charge and coupling. Its gate capacitance was not extracted as a scalar measurement, and the 10 fF wiring allocation is not the total VG capacitance or spare capacitance.

## Measured margins under that load

The complete 45-primary / eight-alternate DC evidence covers startup and switching over 290 ns, with 20 DUT MOS plus the reference switch and 63 terminal pairs per run.

| Quantity | Worst observed value | Remaining margin |
|---|---:|---:|
| Turn-off, primary | 59.524581 ps, SS-low-hot | 0.475419 ps to 60 ps |
| Turn-off, including alternates | 59.587332 ps, SS-low-hot | 0.412668 ps to 60 ps |
| Turn-on, primary | 229.944229 ps, SS-low-cold | 70.055771 ps to 300 ps |
| Minimum VG − VIN, primary | 0.734025962 V, FF-low-hot | 14.025962 mV above 0.72 V |
| Largest DUT/reference terminal voltage | 0.998681198 V, MPRE gate/drain, FS-high-hot | 1.318802 mV to 1.0 V |

Across all 53 jobs, the reference switch itself reaches at most |Vgs| = 0.971931033 V, |Vgd| = 0.972103642 V and |Vds| = 0.883784451 V. The internal MPRE terminal voltage is more limiting. All values above are evaluated at saved transient points. The two alternate saved-step/first-event limitations and full review are disclosed in the [README](README.md); they remain limitations, without a numerical waiver.

The input clock load at TT is 11.244909 fF on PHI_B and 7.525217 fF on PHI_BB per bootstrap. Two instances plus 8 fF wiring give 30.489817 / 23.050434 fF, within the respective 40 fF driver allocations.

## Information needed from the transistor CDAC

- Total VG gate charge versus VG, VIN, bottom-plate voltage and PVT, including peak charging/discharging current and the estimated VG wiring load.
- Total input-switch W/L/finger count, distribution across the capacitor bank, and Ron versus VIN and PVT. The reference sizing is a comparison point, not proof that a different implementation meets the Ron budget.
- Top-plate and bottom-plate switching sequence, PHI_S-to-PHI_B ordering, and terminal-voltage envelopes through startup, track-to-hold and conversion.

The turn-off and internal voltage margins require direct validation with the actual load and switching sequence; they cannot be converted into an extra capacitance allowance by linear extrapolation. A bootstrap-only mixed-top run uses behavioral CDAC switches that read VG to control conductance without modeling physical input-gate charge. That run checks system behavior under the behavioral load; the reference-load module tests and later transistor-CDAC interface checks provide different evidence.
