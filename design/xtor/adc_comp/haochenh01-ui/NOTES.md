# candidate haochenh01-ui (adc_comp) — notes

Status: **wip**. The netlist and RNL are complete (rnl check 0/0/0), but the
candidate has **not been simulated yet**; sizes below are initial choices to be
validated and tuned with the module testbenches.

## Topology

StrongARM dynamic latched comparator:

- input pair `MINP`/`MINN` (nch_ulvt, 52 µm / 30 nm, 52 fingers),
- tail switch `MTAIL` on `CLKC`,
- delayed precharge: a two-stage inverter buffer (`MCKN`/`MCKP`,
  `MCK2N`/`MCK2P`) makes `CKR` from `CLKC`; PMOS `MRDP`/`MRDN` reset
  `DP`/`DN` and PMOS `MRQP`/`MRQN` precharge `QP`/`QN`,
- regenerative latch `MLNP`/`MLNN` + `MLPP`/`MLPN`,
- return-to-zero output inverters `MOPN`/`MOPP`, `MONN`/`MONP`,
- integration caps `CDP`/`CDN` (cfmom_2t, 48 × 1 µm × 50 nm) on the
  decision nodes.

`INP > INN` asserts `OUTP`. Delayed precharge keeps `DP`/`DN` undisturbed
during the evaluate window (kickback), and the caps lower the input-referred
noise.

## Initial sizing rationale (to verify by simulation)

| spec | concern | choice |
|---|---|---|
| CMP-12 (Cin ≤ 20 fF) | input pair width drives Cin | 52 µm (≈ 17–18 fF est.) |
| CMP-01/13 (noise) | pair gm + caps | 52 µm pair, CDP/CDN 48 fingers |
| CMP-04/05/06 (delay) | tail + latch strength | tail 3.3 µm, latch n 10 µm / p 7.2 µm |
| CMP-08 (reset ≤ 45 ps) | precharge PMOS | MRDP/MRDN 3.6 µm, MRQP/MRQN 13.6 µm |
| CMP-14 (CLKC ≤ 16 fF) | clock buffer input | MCKN 2.2 µm / MCKP 4.4 µm |

All thin-oxide devices are expected to stay within the 1.1 V SOA rule
(0.9 V supply; internal nodes bounded by the rail and the input CM ≈ 0.49 V);
CMP-17 must be confirmed per-device on `tb_comp_soa`.

## Simulation plan (run in the contributor's environment)

```text
python -m adcflow sim tb_comp_delay --view adc_comp=xtor:haochenh01-ui --corners all
python -m adcflow sim tb_comp_noise --view adc_comp=xtor:haochenh01-ui --corners all
python -m adcflow sim tb_comp_offset_mc --view adc_comp=xtor:haochenh01-ui
python -m adcflow sim tb_comp_kickback --view adc_comp=xtor:haochenh01-ui --corners all
python -m adcflow sim tb_comp_soa --view adc_comp=xtor:haochenh01-ui --corners all
python -m adcflow check all
```

Tuning knobs, in expected order of effect: input pair width and CDP/CDN size
(noise vs Cin), tail and latch widths (delay/reset), clock-buffer sizes
(CLKC cap and precharge timing).

## Acknowledgments

- #131: spec 0.10.0 (CMP-13 280 µV, CMP-08 45 ps) — limits only, no rerun of
  existing results needed.
- #136: spec 0.11.0 (new `tb_comp_soa` CMP-17 and short-overvoltage rule) —
  requires running `tb_comp_soa` at all corners.
