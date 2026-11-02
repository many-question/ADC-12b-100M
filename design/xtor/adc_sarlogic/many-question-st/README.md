# adc_sarlogic candidate many-question-st

A 1,426-MOS static CMOS self-timed 14-step SAR controller (`adc_sarlogic`) with token-interlocked bit slices, per-step tapped DAC settling wait, inversion-to-depletion MOS varactor timeout compensation, and glitch-free output register in 28 nm HPC+. All 11 subcircuit RNL 0.3 schematic levels are completely drawn (`0 errors, 0 warnings, 0 hints`).

- Top-level schematic: [schematic-top.svg](schematic-top.svg)
- Central controller schematic: [schematic-ctrl.svg](schematic-ctrl.svg)
- Bit-slice schematic: [schematic-slice.svg](schematic-slice.svg)

## Architecture & Circuit Highlights

1. **Token-Interlocked 14-Step Bit Slices (`adc_sarlogic_slice`, `adc_sarlogic_slice14`)**
   - Each bit slice `k` (`k = 1..13` driving `UP<12:0>` / `DN<12:0>`, plus LSB slice `14` capturing `B<0>`) uses a static SR latch (`UP<k-1>`, `DN<k-1>`) triggered when `GO<k-1>` is high and a comparator decision (`CMPP` or `CMPN`) arrives.
   - Once either `UP` or `DN` sets, `SET = UP + DN` asserts `GO<k>` for the next slice and pulls `REQ_B<k>` low for one step (`REQ_B<k> = !(GO<k-1> && !SET)`), requesting a comparison strictly during step `k`.
   - When `CONV` goes low (`IDLE_B = 0`), all slices reset cleanly in parallel (`UP = 0`, `DN = 0`) with `LOG-10` reset-to-idle propagation well above the `100 ps` minimum across all 45 corners.

2. **Per-Step Tapped DAC Settling Loop (`adc_sarlogic_ctrl`)**
   - Active step request signals `REQ_B<1..14>` are combined across four step groups corresponding to the architectural `timing.t_dac_add` schedule (`specs/arch.yaml`):
     - Group A (`k = 1, 2, 7, 8, 10, 11, 12, 13, 14`): base settling delay (`+0 ps`)
     - Group B (`k = 3`, `64C` MSB): `+10 ps` extra settling tap (`XS3`)
     - Group C (`k = 4, 5, 6`, `32C / 16C / 8C`): `+25 ps` extra settling tap (`XS4`, `XS5`, `XS6`)
     - Group D (`k = 9`, `2C` post-bridge): `+20 ps` extra settling tap (`XS9`)
   - This achieves `LOG-16` (`t_dac_add_err_pct`) of `7.23%` (`<= 20%`) and `LOG-08` (`t_conv_ns`) of `2.736 ns` (`<= 2.75 ns`) at `tt_nom_27`, and `LOG-09` (`t_conv_ns <= 4.1 ns` with slow comparator) across all 45 corners.

3. **Inversion-to-Depletion MOS Varactor Timeout Loop (`LOG-11`, `LOG-12`)**
   - When the comparator is metastable (`OP_B = 1`, `ON_B = 1` while `CLKC = 1`), a 4-stage cascaded delay chain (`to1 -> to1_b -> to2 -> to2_b -> to3 -> to3_b -> to4`) fires a synthetic `FORCE_UP` pulse on `CMPP` to resolve the step and continue the conversion without hanging.
   - To keep `t_timeout` (`LOG-12`) strictly inside the tight `200 .. 350 ps` window across all 45 PVT corners (a `1.75x` total window width), the timeout delay stages use **inversion-start to depletion MOS varactor loads** (`pch_lvt_mac` tied to `VDD` on rising nodes `to1..to3`, and `nch_lvt_mac` tied to `VSS` on falling nodes `to1_b..to3_b`).
   - At `ff_high_m40` (`VDD = 0.99 V`, low $|V_{th}|$), the varactor remains in strong inversion (`C_ox`) throughout the first half-swing, maximizing capacitance and preventing early timeout (`~204 ps >= 200 ps`). At `ss_low_125` (`VDD = 0.81 V`, high $|V_{th}|`), the varactor transitions into depletion early in the swing, reducing effective capacitance to compensate lower transistor drive current (`~344 ps <= 350 ps`), compressing the extreme corner ratio `ss_low_125 / ff_high_m40` to `1.68x`.

4. **Glitch-Free Output Register (`adc_sarlogic_dlat`) & Input Capacitance (`LOG-14`, `LOG-15`)**
   - Upon completion of step 14 (`DONE14 = 1`), `LAT_EN` pulses to transfer all 14 raw bits `Q<13:0>` into `D<13:0>` prior to raising `RDY`, guaranteeing zero mid-conversion transitions on `D<13:0>` (`LOG-10 = 104.0 .. 183.4 ps >= 100 ps` across all 45 corners).
   - Compact input buffers on `CONV` (`LOG-14 = 2.53 fF <= 40 fF`) and `OUTP` / `OUTN` (`LOG-15 = 4.22 fF <= 7 fF`) minimize loading on `adc_clkgen` and `adc_comp`.

## 45-Corner Verification Summary (`366 / 369` Required Corner-Specs Passing across 5 Testbenches)

| Spec | Metric | Target Limit | Corner Scope | Measured (`tt_nom_27` / 45-Corner Worst) | Status | Testbench |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `LOG-01` | `code_errors` | `<= 0` | `all` (45/45) | `0` (`0` across 45,000 conversions) | **PASS** | `tb_sarlogic_rand` |
| `LOG-02` | `t_bitd_ps` | `<= 40 ps` | `typ` (1/1) | `27.9 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-03` | `t_rst_ps` | `<= 45 ps` | `typ` (1/1) | `24.45 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-04` | `t_dac_fast_ps` | `35 .. 60 ps` | `typ` (1/1) | `48.21 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-05` | `t_dac_slow_ps` | `70 .. 100 ps` | `typ` (1/1) | `94.88 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-06` | `t_dac_min_ps` | `>= 70 ps` | `all` (45/45) | `71.51 ps` (worst across 45 corners) | **PASS** | `tb_sarlogic_func` |
| `LOG-07` | `t_start_ps` | `80 .. 160 ps` | `all` (45/45) | `94.9 ps` (`81.76 .. 146.1 ps` across 45 corners) | **PASS** | `tb_sarlogic_func` |
| `LOG-08` | `t_conv_ns` | `<= 2.75 ns` | `typ` (1/1) | `2.736 ns` | **PASS** | `tb_sarlogic_func` |
| `LOG-09` | `t_conv_slow_ns` | `<= 4.1 ns` | `all` (45/45) | `3.086 ns` (`3.712 ns` worst at `ss_low_125`) | **PASS** | `tb_sarlogic_func_slow` |
| `LOG-10` | `t_rdy_ps` | `>= 100 ps` | `all` (45/45) | `128.4 ps` (`104.0 ps` worst across 45 corners) | **PASS** | `tb_sarlogic_func` |
| `LOG-11` | `timeout_errors` | `<= 0` | `all` (45/45) | `0` (`0` across all 45 corners) | **PASS** | `tb_sarlogic_timeout` |
| `LOG-12` | `t_timeout_ps` | `200 .. 350 ps` | `all` (45/45) | `258.7 ps` (`205.4 .. 344.4 ps` across 45 corners) | **PASS** | `tb_sarlogic_timeout` |
| `LOG-13` | `power_uw` | `reported` | `typ` (1/1) | `928.1 uW` | **INFO** | `tb_sarlogic_func` |
| `LOG-14` | `cin_conv_ff` | `<= 40 fF` | `typ` (1/1) | `2.534 fF` | **PASS** | `tb_sarlogic_func` |
| `LOG-15` | `cin_cmp_ff` | `<= 7 fF` | `typ` (1/1) | `4.216 fF` | **PASS** | `tb_sarlogic_func` |
| `LOG-16` | `t_dac_add_err_pct` | `<= 20 %` | `typ` (1/1) | `7.227 %` | **PASS** | `tb_sarlogic_func` |
| `LOG-17` | `soa_violations` | `<= 0` | `all` (42/45) | `0` (`0` at 42/45 corners; `1..2` at `{tt,fs,ss}_high_m40`) | **42/45** | `tb_sarlogic_soa` |

## Acknowledged Notices

Acknowledged `[adc_sarlogic]` notices: [#61](https://github.com/many-question/ADC-12b-100M/issues/61), [#79](https://github.com/many-question/ADC-12b-100M/issues/79), [#102](https://github.com/many-question/ADC-12b-100M/issues/102), [#118](https://github.com/many-question/ADC-12b-100M/issues/118), [#135](https://github.com/many-question/ADC-12b-100M/issues/135).
