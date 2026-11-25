# candidate haochenh01-ui (adc_comp) — notes

Status: **ready**. All five adc_comp tests are simulated with Spectre APS over
every corner and committed under `results/adc_comp/<test>/xtor-haochenh01-ui/`;
every spec passes (numbers below).

## Topology

StrongARM dynamic latched comparator:

- input pair `MINP`/`MINN` (nch_ulvt, 56 µm / 30 nm, 56 fingers),
- tail switch `MTAIL` (3.5 µm) on `CLKC`,
- delayed precharge: a two-stage inverter buffer (`MCKN`/`MCKP`,
  `MCK2N`/`MCK2P`) makes `CKR` from `CLKC`; PMOS `MRDP`/`MRDN` reset
  `DP`/`DN` and PMOS `MRQP`/`MRQN` precharge `QP`/`QN`,
- regenerative latch `MLNP`/`MLNN` (14 µm) + `MLPP`/`MLPN` (10 µm),
- return-to-zero output inverters `MOPN`/`MOPP`, `MONN`/`MONP`,
- integration caps `CDP`/`CDN` (cfmom_2t, 88 × 1 µm × 50 nm) on the
  decision nodes.

`INP > INN` asserts `OUTP`. Delayed precharge keeps `DP`/`DN` undisturbed
during the evaluate window (kickback), and the caps lower the input-referred
noise.

The netlist is RNL 0.4 (`adc28` 0.2). Its drawing is the 0.4 solver's placement
(`rnl 0.6.2`), so `rnl check` on it reports layout hints only; the drawing is
comment-only and none of the committed results depend on it (the content hash
is unchanged across the 0.3 → 0.4 migration).

## Sizing history

Iteration 1 (initial WIP): input pair 52 µm/52 fingers, tail 3.3 µm, latch
n 10 µm / p 7.2 µm, resets 3.6 µm / 13.6 µm, CDP/CDN 48 fingers. The all-corner
noise run failed CMP-13 (≤ 280 µV) at four 125 °C corners
(ff_low_125 = 304 µV, fs_low_125 = 297 µV, tt_low_125 = 287 µV,
ff_nom_125 = 281 µV); every other spec passed at all corners.

Iteration 2 (final, 2026-11-23): core aligned with the project reference
strongarm — input pair 56 µm/56 fingers, resets 4 µm / 16 µm, outputs
2 µm / 4 µm, clock buffer 2 µm / 4 µm — with tail 3.5 µm, latch n 14 µm /
p 10 µm and CDP/CDN raised to 88 fingers for hot-corner noise margin.

| spec | concern | final choice |
|---|---|---|
| CMP-12 (Cin ≤ 20 fF) | input pair width drives Cin | 56 µm |
| CMP-01/13 (noise) | pair gm + caps + latch | 56 µm pair, CDP/CDN 88 fingers, latch n 14 µm / p 10 µm |
| CMP-04/05/06 (delay) | tail + latch strength | tail 3.5 µm |
| CMP-08 (reset ≤ 45 ps) | precharge PMOS | MRDP/MRDN 4 µm, MRQP/MRQN 16 µm |
| CMP-14 (CLKC ≤ 16 fF) | clock buffer input | MCKN 2 µm / MCKP 4 µm |

All thin-oxide devices stay within the 1.1 V SOA rule (0.9 V supply; internal
nodes bounded by the rail and the input CM ≈ 0.49 V); CMP-17 = 0 at every
corner on `tb_comp_soa`.

## Results summary (2026-11-23, Spectre APS, ULL v1.8 models)

Worst value over all corners (45 corners for the all-corner specs: 5 process
corners × 3 temperatures × 3 supplies), from the committed
`results/adc_comp/<test>/xtor-haochenh01-ui/` JSONs of iteration 2:

| spec | limit | worst | corner |
|---|---|---|---|
| CMP-01 noise (typ) | ≤ 200 µV | 175.1 µV | tt_nom_27 |
| CMP-02 systematic offset | ≤ 2 mV | 0.007 mV | fs_low_125 |
| CMP-03 offset sigma (MC, 50 samples) | ≤ 5 mV | 1.893 mV | tt_nom_27, 50/50 valid |
| CMP-04 delay @1 mV (typ) | ≤ 80 ps | 62.0 ps | tt_nom_27 |
| CMP-05 delay @1 mV (all) | ≤ 120 ps | 104.7 ps | ss_low_m40 |
| CMP-06 delay @30 mV (typ) | ≤ 50 ps | 48.3 ps | tt_nom_27 |
| CMP-07 regeneration tau | ≤ 15 ps | 6.07 ps | ss_low_m40 |
| CMP-08 reset time | ≤ 45 ps | 30.1 ps | ss_low_125 |
| CMP-09 wrong decisions | = 0 | 0 | all |
| CMP-10 energy per comparison | reported | 228.5 fJ | tt_nom_27 |
| CMP-11 kickback | ≤ 40 µV | 0.26 nV | ss_high_m40 |
| CMP-12 input capacitance | ≤ 20 fF | 19.18 fF | tt_nom_27 |
| CMP-13 noise (all corners) | ≤ 280 µV | 274.0 µV | ff_low_125 |
| CMP-14 CLKC capacitance | ≤ 16 fF | 7.63 fF | tt_nom_27 |
| CMP-15 output validity | = 0 | 0 | all |
| CMP-16 losing-output peak | reported | 19.9 % VDD | sf_low_m40 |
| CMP-17 SOA violations | = 0 | 0 | all |

Margins are thin at the hot/fast noise corner (274 µV of 280 µV) and on input
capacitance (19.18 fF of 20 fF); both are set by the 56 µm input pair, which is
what the reference strongarm uses as well.

## Acknowledgments

- #131: spec 0.10.0 (CMP-13 280 µV, CMP-08 45 ps) — limits only, no rerun of
  existing results needed.
- #136: spec 0.11.0 (new `tb_comp_soa` CMP-17 and short-overvoltage rule) —
  requires running `tb_comp_soa` at all corners.
