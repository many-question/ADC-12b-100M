# Reset device and sampling switch repair

The first DC screen found a substantially lower-leakage reset candidate at comparable on-resistance. The short main-input restoration test also found a measurable shift in the input bootstrap gate. Both findings are being checked in transient runs. The frozen [mechanism report](reset-mechanism.md) supplies the comparison circuit and measured bias points.

## Hot SS reset screen

The reset source was held at 0.45 V and the body grounded. Nine drain biases span the observed pre-reset TOP excursion of 0.42465 to 0.47653 V. The high gate cases use 1.179 V and 1.0575 V, corresponding to `VCM + k*DVDD` with `k=0.90` and `0.75` at 0.81 V. Off-state drain current uses all five late hold biases, with TOP from about 0.09 to 0.81 V and the actual near-zero gate levels. All six geometries below were verified by device callbacks and compiled in the hot SS model section. The requested 45 nm channel snapped to 40 nm in the callback, so the two longer cases were requested again at the exact 40 nm length.

| NMOS | Total W / L | Median Ron at k=0.90 (ohm) | Median Ron at k=0.75 (ohm) | Max off drain magnitude (uA) |
|---|---|---:|---:|---:|
| ULVT baseline | 6 um / 30 nm | 73.77 | 95.31 | 0.51153 |
| LVT | 8 um / 30 nm | 58.77 | 76.93 | 0.34669 |
| SVT | 10 um / 30 nm | 63.06 | 95.94 | 0.05500 |
| HVT | 12 um / 30 nm | 72.57 | 126.41 | 0.00995 |
| ULVT | 10 um / 40 nm | 50.49 | 67.59 | 0.19207 |
| LVT | 12 um / 40 nm | 44.97 | 61.35 | 0.09898 |

The HVT point cuts the largest sampled off drain current by about 51 times at the original gate amplitude. Its on-resistance range is 69.25–76.25 ohm, compared with 72.22–75.64 ohm for N6. The absolute normalized cubic coefficient of the local I-V fit drops from 2.469 to 0.187 V^-2, while the secant resistance span increases. Both matter when the dynamic TOP swing and gate trajectory change. The larger gate and weaker drive case are separate tradeoffs. The operating-point export did not return gate capacitance, so actual gate-driver charge is being measured in transient.

The first transient candidate uses HVT 12 um / 30 nm, six fingers, the same high gate amplitude and a 20 ps command rise. It keeps the independent ideal booster and 10 ps fall. A second size check is measuring a 10 um / 40 nm LVT device near the lower gate amplitude, guided by the 12 um result. DC probes emit model Vgb warnings with the body grounded. The project judges gs, gd and ds in its dedicated SOA test, with body pairs reported separately under its existing rule. Passing DC or the short waveform check provides no cold SOA result. [Verification rule](https://github.com/many-question/ADC-12b-100M/blob/75f31c14790108d54fb7c57cbaeb461f2035a51c/docs/verification.md#L356)

## Main input restoration

The first restoration keeps the frozen N6 reset and restores just the 22 original main input MOS per side. The remaining 108 replacements, all capacitors and digital controls keep the same source instances. The 80 ns run completed with all four expected sample times matching B, no numerical warnings and no control sequence mismatch. The positive and negative bootstrap gates shift by up to 1.78 ps. The other measured control edges shift by less than 0.04 fs. The sampled and stage voltages are used for preflight only. The complete 256-point run is in progress.

A separate short control uses frozen B with the actual loaded input-gate voltages replayed at every accepted time. This keeps the earlier fixed resistances and measures the effect of the gate trajectory in that circuit. It leaves VIN free to respond to the circuit and keeps the input driver feedback outside this replay comparison. A matched-Ron comparison and additional group restoration depend on the full-record distortion and control data.

| Verified evidence | Archive SHA256 |
|---|---|
| First DC screen | `8115b6efa1b8eafee34f4684751715f8d0b06ad3951174bc9ca61ac29441e0b8` |
| Exact 40 nm DC cases | `90be65eb39f04578e6680528d6c2d860766fc4e1d47ccf921ee7264cdd8b9021` |
| Main input restoration 80 ns | `76fc5c985f60293857547c0f359540eaca7638e29e942e40e70ac6b88b5c4ba2` |

The candidate is WIP. Cold low and high supply SOA, complete hot SS spectra, numerical crosschecks and verification with real peripheral switches are required before a combined repair can be judged.
