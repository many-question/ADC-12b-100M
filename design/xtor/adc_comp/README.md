# Comparator transistor-level experiments

Status: **work in progress, not signed off**. The first candidate was the
conventional single-stage StrongARM latch: an NMOS input pair and clocked tail,
cross-coupled NMOS/PMOS regeneration, four PMOS precharge switches, and two
return-to-zero output inverters. The embedded RNL records show every device,
wire and body connection and identify the differential pair, matched devices,
regenerative group and reset group.

Current checkpoint `my01` implements the self-timed core (M1-M15) of
Miyahara et al., "A Low-Noise Self-Calibrating Dynamic Comparator for
High-Speed ADCs," A-SSCC 2008, Fig. 2(b), DOI 10.1109/ASSCC.2008.4708780.
The paper's offset-compensation devices and charge pump are omitted. P/N
drive both the second-stage PMOS input devices and its NMOS reset devices;
there is no second-stage clock or explicit shared tail. Positive input
difference lowers P first and raises OUTP, preserving the required polarity.

## Reproducible checkpoints

Each checkpoint commit contains its exact netlist plus the three TT result
JSON files and their evidence figures. Restore a checkpoint commit to compare
its results; the results must not be copied onto another netlist version.

| Experiment | Input / tail total W | Latch N / P total W | Noise | Delay at 1 mV / 30 mV | Reset | Energy | Cin | Kickback |
|---|---|---|---|---|---|---|---|---|
| sa01 | 8 / 12 um | 3 / 3 um | 584.7 uV | 22.24 / 15.13 ps | 20.09 ps | 54.97 fJ | 2.63 fF | 0.64 uV |
| sa02 | 40 / 1 um | 6 / 6 um | 227.0 uV | 93.00 / 74.42 ps | 20.89 ps | 103.69 fJ | 14.27 fF | 1.44 uV |
| sa03_c8 | 40 / 8 um | 3 / 3 um | 298.0 uV | 44.15 / 34.27 ps | 21.46 ps | 186.18 fJ | 13.70 fF | 0.20 uV |
| sa03_c0 | 40 / 8 um | 3 / 3 um | 360.1 uV | 27.49 / 20.45 ps | 19.69 ps | 100.41 fJ | not rerun | not rerun |
| sa04_c4 | 40 / 2 um | 1 / 1 um | 283.7 uV | 81.00 / 61.31 ps | 16.25 ps | 133.92 fJ | 14.22 fF | 0.06 uV |

All MOS lengths are 30 nm. Each logical device uses parallel single-finger
instances, represented by the netlist multiplier, with unit width at most
1 um. This is an exploratory pre-layout model, without solved layout-effect
parameters. The full local device-callback runtime has not yet been validated.

The sa01 delay, reset, decision-error, energy, input-capacitance and kickback
metrics pass at TT. Its input noise fails the 80 uV requirement by a large
margin. The fixed noise test spans only +/-300 uV, so a fitted noise above that
window is an approximate diagnostic, not a precise wide-range characterization.

The sa02 input-pair enlargement and smaller tail reduce noise, but noise still
fails. Both TT delay limits now fail (80 ps at 1 mV, 50 ps at 30 mV), and input
capacitance is close to the 15 fF limit. This is a tradeoff checkpoint, not an
accepted candidate. The next experiment adds matched PDK MOM loading to P/N
while restoring stronger tail current.

The sa03_c8 checkpoint adds eight identical PDK MOM units from each input-pair
drain to VSS. One unit uses `nr=24 lr=1u w=50n s=50n stm=1 spm=3`; each branch
uses `multi=8`. This restores timing margin relative to sa02, but noise still
fails and energy exceeds 150 fJ. Since both transistor sizing and loading
changed from sa02, their difference does not isolate the effect of capacitance.

The sa03_c0 local comparison keeps sa03_c8 transistor sizes and removes the
two MOM loads. The measured noise fit decreases from 360.1 to 298.0 uV when
loading is added, while energy rises from 100.4 to 186.2 fJ. These are one-seed,
64-decision-per-level fits and should not be interpreted as precise noise
estimates. The sa04_c4 version reduces the tail and regeneration devices and
uses four MOM units per side. It meets the energy limit but still fails noise
and both TT delay limits. No successful single-stage candidate has been found
in this limited search; this is not a proof that the topology cannot meet the
specification. The unloaded sa03_c0 netlist and measurement data are preserved
locally as a comparison experiment.

Commands used for the existing acceptance tests:

```sh
python -m adcflow sim tb_comp_delay --view adc_comp=xtor --corners typ --mode aps
python -m adcflow sim tb_comp_noise --view adc_comp=xtor --corners typ --mode aps
python -m adcflow sim tb_comp_kickback --view adc_comp=xtor --corners typ --mode aps
```

Exploration initially uses `--no-record --keep`; after local data retrieval,
measurement is rerun with the unchanged adcflow functions and checked against
the saved metrics. Recording verifies the staged netlists against the restored
source. Temporary simulation jobs are removed only after local logs and
outputs have been verified. Raw outputs are kept locally outside version control.

No all-corner, mismatch or top-level acceptance is claimed. Next: exploit the
speed margin through input-stage sizing and matched capacitive loading before
considering a two-stage topology.

## Two-stage comparison

| Experiment | Noise | Delay at 1 mV / 30 mV | Reset | Energy | Cin | Kickback |
|---|---|---|---|---|---|---|
| dt01 | 251.9 uV | 56.25 / 44.27 ps | 14.70 ps | 115.32 fJ | 14.25 fF | 0.037 uV |
| my01 | 262.1 uV | 59.34 / 48.31 ps | 31.06 ps | 115.16 fJ | 14.25 fF | 0.007 uV |

The two-stage clocked comparison meets the TT timing, energy, input-capacitance
and kickback limits, but still fails noise. Its exact source and results are
preserved before moving to the self-timed topology.

The my01 self-timed core also passes the measured TT limits except noise.
The difference between its noise fit and dt01 is small relative to the
limited number of noise decisions; neither is close to 80 uV. Its total MOS
widths are 40 um (input), 1.5 um (tail), 3 um (second-stage PMOS input),
3/2 um (PMOS/NMOS regeneration), and 2 um (reset), all at 30 nm length.
