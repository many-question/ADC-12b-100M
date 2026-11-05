# Reset device and sampling switch repair

The DC screen found reset devices with lower leakage at comparable on-resistance. Two fast-rise variants reached their final gate voltage before TOP recovered in the cold SOA test. A slower rise with a wider, low-voltage reset is now under test. The frozen mechanism study supplies the comparison circuit and measured bias points. [Mechanism evidence](reset-mechanism.md)

## Hot SS reset screen

The reset source was held at 0.45 V and the body grounded. Nine drain biases span the observed pre-reset TOP excursion of 0.42465 to 0.47653 V. The high gate cases use 1.179 V and 1.0575 V, corresponding to `VCM + k*DVDD` with `k=0.90` and `0.75` at 0.81 V. Off-state drain current uses all five late hold biases, with TOP from about 0.09 to 0.81 V and the actual near-zero gate levels. Each geometry was verified by device callbacks and compiled in the hot SS model section. The requested 45 nm channel snapped to 40 nm in the callback, so the longer cases use exact 40 nm requests.

| NMOS | Total W / L | Median Ron at k=0.90 (ohm) | Median Ron at k=0.75 (ohm) | Max off drain magnitude (uA) |
|---|---|---:|---:|---:|
| ULVT baseline | 6 um / 30 nm | 73.77 | 95.31 | 0.51153 |
| LVT | 8 um / 30 nm | 58.77 | 76.93 | 0.34669 |
| SVT | 10 um / 30 nm | 63.06 | 95.94 | 0.05500 |
| HVT | 12 um / 30 nm | 72.57 | 126.41 | 0.00995 |
| ULVT | 10 um / 40 nm | 50.49 | 67.59 | 0.19207 |
| LVT | 12 um / 40 nm | 44.97 | 61.35 | 0.09898 |
| LVT | 10 um / 40 nm | 53.96 | 73.62 | 0.08248 |
| LVT | 14 um / 40 nm | 38.54 | 52.59 | 0.11547 |

The HVT point cuts the largest sampled off drain current by about 51 times at the original gate amplitude. Its on-resistance range is 69.25–76.25 ohm, compared with 72.22–75.64 ohm for N6. The absolute normalized cubic coefficient of the local I-V fit drops from 2.469 to 0.187 V^-2, while the secant resistance span increases. Both matter when the dynamic TOP swing and gate trajectory change. The larger gate and weaker drive case are separate tradeoffs. The operating-point export did not return gate capacitance, so actual gate-driver charge is being measured in transient.

Inverting the fitted I-V relation reveals the effect of the quadratic term on voltage H3. At a fixed 25.926 mV linear TOP fundamental, the quasistatic differential H3 estimates are 35.7 uV for N6, 62.1 uV for HVT12 at k=0.90 and 64.3 uV for LVT10 at k=0.75. The HVT short record shows about twice the pre-reset common-mode offset of B across its four sample phases. The inverse fit omits charge, source feedback and time-varying gate voltage. The wider LVT14 targets less TOP excursion at comparable current forcing, with a larger gate as the cost.

## Cold SOA and gate charge

HVT12 at k=0.90 and LVT10 at k=0.75 both passed the 80 ns hot functional preflight. Both use 20 ps rise and 10 ps fall commands through the independent ideal driver. The cold test restores the full physical periphery and judges all 1,782 gs/gd/ds pairs over 70 ns. The largest excursions in this table are reset Vgd. All four runs completed with zero numerical warnings.

| Reset and supply at cold SS | Violations | Peak Vgd (V) | Max above 1.1 V in 10 ns (ps) |
|---|---:|---:|---:|
| HVT12, 0.81 V | 1 | 1.35776 | 130.540 |
| HVT12, 0.99 V | 1 | 1.51941 | 188.379 |
| LVT10, 0.81 V | 0 | 1.23673 | 63.628 |
| LVT10, 0.99 V | 1 | 1.37121 | 115.568 |

At the high-supply worst point, TOP is near -0.179 V while the HVT and LVT gates have reached about 1.341 V and 1.192 V respectively. The project allows a peak of 1.29 V with at most 100 ps above 1.1 V in any 10 ns. The failure points rule out these two settings for full-spectrum qualification. LVT14 uses k=0.75 and a 300 ps rise to let TOP recover before the gate reaches full amplitude. Its 80 ns preflight passes with the 10 ps fall, and both cold endpoint runs have started.

Measured turn-on charge in the hot short records is 3.48–3.82 fC for N6, 5.57–5.96 fC for HVT12, 5.36–5.76 fC for LVT10, and 7.46–8.07 fC for LVT14. Assuming a fully charged boost capacitor and only gate charge as the load, the largest Q divided by allowable droop is 47.2, 73.6, 28.5 and 39.9 fF respectively. The lower LVT amplitude gives more droop headroom despite a larger gate. Actual booster parasitics, settling and internal SOA still need validation. DC probes emit model Vgb warnings with the body grounded. The project's acceptance checks gs, gd and ds, with body pairs treated separately under the existing rule. [Verification rule](https://github.com/many-question/ADC-12b-100M/blob/75f31c14790108d54fb7c57cbaeb461f2035a51c/docs/verification.md#L356)

Across the four short sine phases and both sides, the maximum absolute drain-terminal integral over the last 50 ps is 0.02573 fC for N6, 0.000502 fC for HVT12, 0.00415 fC for LVT10 and 0.00641 fC for LVT14. The integrals measure total signed terminal flow, including displacement. Their reduction agrees with the off-state DC trend. LVT14 also gives a slightly smaller pre-reset common-mode offset than N6 at these phases.

## Main input restoration

The first restoration keeps the frozen N6 reset and restores just the 22 original main input MOS per side. The remaining 108 replacements, all capacitors and digital controls keep the same source instances. The 80 ns run completed with all four expected sample times matching B, no numerical warnings and no control sequence mismatch. The positive and negative bootstrap gates shift by up to 1.78 ps. The other measured control edges shift by less than 0.04 fs. The sampled and stage voltages are used for preflight only. The complete 256-point run is in progress.

A separate short control uses frozen B with the actual loaded input-gate voltages replayed at every accepted time. Actual replay error is below 0.95 pV. The largest final differential change from gate replay alone is 4.23 uV across four phases. Real restoration minus the replay case differs by up to 0.503 mV in the raw final samples. The comparison fixes the absolute gate trajectory and lets VIN respond to the circuit. The full record separates linear gain, phase and nonlinear residual.

The restored main-input device sizes were also tested at five source voltages with `VG=VIN+0.81 V`, grounded bulk and symmetric +/-1 mV VDS. The largest bit's differential Ron is 33.02–35.61 ohm over VIN=0.05–0.85 V and 34.32 ohm at nominal VIN. The calibrated fixed-Ron replay uses each size's own nominal slope. This preserves on-resistance at the center point and omits signal-dependent conductance, device charge and leakage. The first targeted additional restoration is sharing, motivated by its measured loading-dependent phase shift in the earlier isolation.

| Verified evidence | Archive SHA256 |
|---|---|
| First DC screen | `8115b6efa1b8eafee34f4684751715f8d0b06ad3951174bc9ca61ac29441e0b8` |
| Exact 40 nm DC cases | `90be65eb39f04578e6680528d6c2d860766fc4e1d47ccf921ee7264cdd8b9021` |
| Main input restoration 80 ns | `76fc5c985f60293857547c0f359540eaca7638e29e942e40e70ac6b88b5c4ba2` |
| Loaded input gate replay 80 ns | `f6d2db0bbcc8497e04ec32a65d299b0401af2e70db9ff185fe77ccf7bea69748` |
| Main-input on-resistance DC | `81f0cd301f962b30c56d21473a015250cb019e55f525e3a6f3a823a8f5503297` |
| HVT12 cold low / high | `178f60103d4a69a27028a0e470652ff452068a19998b9a00308ab5d76b812a10` / `8d1d2405a1f940da681f7f17db6b7aed4726b6693072b54cc963f70c0b4b174a` |
| LVT10 cold low / high | `d69b33628f83755a1ffc2ff9c850ff757d46158442646eca7fcd739666c62ba4` / `99b65882d17916f08fc5884eb7f172bf73bcf50ab72e03e9fd09df1186244124` |

The candidate is WIP. Cold low and high supply SOA, complete hot SS spectra, numerical crosschecks and verification with real peripheral switches are required before a combined repair can be judged.
