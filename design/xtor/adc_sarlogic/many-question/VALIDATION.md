# Current validation: repaired candidate, wip (specification 0.8.0)

Current circuit hash: 700f1fc44e737b6f. Baseline hash 237b05f50a71cbad
has been superseded. Issues #130, #133 and #135 remain acknowledged.
All results are contributor self-tests, **not independent verification**.
Candidate status remains wip; there is no full-eligibility or signoff claim.

## Electrical changes

The DAC-output NOR PMOS inputs are ordered with global CVB on top and local
data below. Only the first timeout tap changes from a NAND with identical
CLK inputs to a matched-drive inverter, removing its floating NMOS node.
The CVB reset driver is reduced by 25% (drive 4 to 3); comparator-clock and
per-bit output drive remain unchanged. No ports, specified waits, shared
specifications, testbenches, numerical presets or SOA algorithm are changed.
Two MOS devices are removed.

## Same-circuit private prechecks

These unrecorded standard-stimulus tests selected the repair; they are not
substituted for formal results on the actual candidate path.

| Precheck | Coverage | Outcome |
|---|---|---|
| LOG-17 SOA | SS high -40 C, 1770 devices / 5310 pairs, full 51.12 ns | zero violations; worst 10 ns window 71.479 ps |
| LOG-17 SOA | FS high -40 C, 1770 devices / 5310 pairs, full 51.12 ns | zero violations; worst 10 ns window 54.809 ps |
| TT ordinary function | 60 complete conversions | zero bit/DAC errors; all applicable bounds pass |
| TT LOG-08 | full 60-conversion run | 2.743338 ns <=2.75 ns |
| TT LOG-16 | full 60-conversion run | 15.300468% <=20% |

[SOA_REPAIR.md](SOA_REPAIR.md) contains the unsuccessful weak-drive A/B
trials and explains why weakening drivers alone was insufficient.

## Fresh formal regression required

The two formerly failing corners have now completed **fresh formal**
`tb_sarlogic_soa` runs on the committed candidate path and hash:

| Corner | Devices / pairs | Violations | Worst sliding 10 ns over-limit time |
|---|---:|---:|---:|
| `ss_high_m40` | 1770 / 5310 | **0** | **71.479 ps** |
| `fs_high_m40` | 1770 / 5310 | **0** | **54.809 ps** |

Both are standard APS/errpreset=conservative results with five captures,
all measured pairs retained and no stale dependencies. This is **2/45 fresh
SOA corners**, not all-corner acceptance. Tight numerical crosschecks remain
running. The fresh formal TT function run has also completed: **60 full
conversions, zero bit/DAC errors**, and every applicable bound passes.
LOG-08 is **2.743338 ns**; LOG-16 is **15.300468%**. The other 44 saved-waveform
function corners and all 45 random corners still need fresh results.

A guarded queue runs the unchanged standard tests against only the new hash:

- Formal SOA at the two previously failing corners and a fresh TT function
  run, followed by the remaining SOA corners and specified tight crosschecks.
- Ordinary function: all 45 corners, 60 conversions per corner.
- Slow comparator: all 45 corners, 100 conversions per corner.
- Timeout: all 45 corners, 40 conversions per corner.
- Random: all 45 corners, **1000 conversions per corner**; old TT random
  evidence is not reusable after the electrical change.
- Mixed reference runs: high-frequency sine at quick (7 corners), low-
  frequency sine at TT, duty 45% and 55% at quick (14 variant jobs).

The new formal queue is running; the private
prechecks above must not be read as all-corner formal acceptance. Existing
baseline result files remain historical/stale until replaced by freshly
simulated records. **No old data is rehashed to the new circuit.** Source
hashes, staged dependencies, standard parameters, complete conversion/word
counts and verdicts are checked before accepting each new module record.
A failed stage stops progression to later qualification stages.

Mixed results are kept as private contributor references, not published to

esults/adc_top/ in this candidate PR. Official mixed regression and
independent erification/ records belong to the project lead and remain
outstanding even if every contributor self-test passes.

## Baseline history and local checks

Baseline commit 6748108 documents the former full-corner function, slow
and timeout passes, TT-only random coverage, and 43/45 SOA passes. Its two
SOA failures persisted under traponly/maxstep 1 ps/reltol 1e-7/vabstol 1e-8.
That is evidence for the former circuit, not for the repair.

The existing SOA_CORNERS.png, TIMEOUT_CORNERS.png and strict-peak diagnostic
plots are **baseline historical plots**, not current-hash evidence. New
all-corner summaries will replace them only after fresh runs finish.

The repaired complete-RNL netlist checks with zero errors, warnings and
hints. The unchanged tool unit suite has 485 passed, 3 skipped and 1
deselected. Code checks do not establish electrical qualification.
