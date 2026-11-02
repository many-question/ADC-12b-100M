# SOA repair experiments (self-tests, not independent verification)

The baseline circuit `237b05f50a71cbad` fails LOG-17 at `ss_high_m40`
and `fs_high_m40`. The standard and tighter numerical runs agree on the
25 / 24 violating terminal pairs. These are **sliding-window duration**
failures under spec 0.8.0, not peaks above 1.29 V.

## Weaker-drive A/B trials

Every experiment used the unchanged, full 51.12 ns `tb_sarlogic_soa`
stimulus, APS and the project numerical preset. The table reports the worst
time above 1.1 V in **any sliding 10 ns window**; the limit is 100 ps.
Experiments were unrecorded private circuits, not relabeled baseline results.

| Circuit / changed driver | Hash | SS high -40 C (ps) | FS high -40 C (ps) | Violations SS / FS |
|---|---|---:|---:|---:|
| Baseline | `237b05f50a71cbad` | 719.163 | 223.484 | 25 / 24 |
| CVB and CLKC drive multiplied by 0.75 | `f3f6245265d2cbf3` | 512.392 | 223.240 | 25 / 24 |
| UP/DN output drive multiplied by 0.75 | `fe194273c6624f41` | 718.006 | 254.791 | 25 / 24 |
| Both changes | `78e9969610185a71` | 509.982 | 254.459 | 25 / 24 |

**Simply weakening the drivers did not fix either corner.** It reduced the
SS timer-node duration but did not remove the floating nodes, and it did not
consistently improve FS. No failing experiment is claimed as passing.

## Topology-directed correction under evaluation

- In the DAC-output NORs, put global CVB on the upper series PMOS and local
  data on the lower PMOS. Boolean logic is unchanged, but the internal
  floating-node behavior during reset and interruptions differs.
- The first timeout NAND has identical CLK and enable inputs. Replace only
  that first tap with a matched-drive inverter, eliminating its floating
  NMOS-stack node. Keep asynchronous clearing of all later taps.
- Evaluate a 25% weaker **CVB reset driver only**. Keep the comparator-clock
  and per-bit UP/DN drivers unchanged so that the normal conversion loop is
  not deliberately slowed.

The complete-RNL weak-reset preview has circuit hash `700f1fc44e737b6f`;
RNL checking gives zero errors, warnings and hints. Its complete standard
SOA experiments at `ss_high_m40` / `fs_high_m40` pass with **zero violating
pairs**, 1770 devices / 5310 pairs per corner and worst-window times
**71.479 / 54.809 ps**. The full 60-conversion TT experiment also passes:
zero bit/DAC errors, conversion time **2.743338 ns**, extra-wait error
**15.300468%**, and every applicable TT bound satisfied. The identical
electrical circuit has now been promoted with complete RNL. These private
experiments are **not formal candidate acceptance**. Promotion is followed
by fresh tests on the
actual candidate hash, including all 45 random corners (old TT data cannot
be transferred to a different circuit), SOA, normal/slow/timeout tests and
mixed top-level reference tests. Independent lead verification remains a
separate qualification requirement.
