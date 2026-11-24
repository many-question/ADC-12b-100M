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
     - Group C (`k = 4, 5, 6`, `32C / 16C / 8C`): `+30 ps` extra settling tap (`XS4`, `XS5`, `XS6`)
     - Group D (`k = 9`, `2C` post-bridge): `+25 ps` extra settling tap (`XS9`)
   - This achieves `LOG-16` (`t_dac_add_err_pct`) of `9.44%` (`<= 20%`), `LOG-06` (`t_dac_slow_ps`) of `72.84 .. 130.8 ps` (`70 .. 160 ps` across 45 corners), `LOG-08` (`t_conv_ns`) of `2.723 ns` (`<= 2.75 ns`) at `tt_nom_27`, and `LOG-09` (`t_conv_ns <= 4.1 ns` with slow comparator, `2.689 .. 3.658 ns`) across all 45 corners.

3. **Inversion-to-Depletion MOS Varactor Timeout Loop (`LOG-11`, `LOG-12`)**
   - When the comparator is metastable (`OP_B = 1`, `ON_B = 1` while `CLKC = 1`), a 4-stage cascaded delay chain (`to1 -> to1_b -> to2 -> to2_b -> to3 -> to3_b -> to4`) fires a synthetic `FORCE_UP` pulse on `CMPP` to resolve the step and continue the conversion without hanging.
   - To keep `t_timeout` (`LOG-12`) strictly inside the tight `200 .. 350 ps` window across all 45 PVT corners (a `1.75x` total window width), the timeout delay stages use **complementary HVT MOS gate/varactor loads** (`pch_hvt_mac` tied to `VDD` on rising nodes `to1..to3`, and `nch_hvt_mac` tied to `VSS` on falling nodes `to1_b..to2_b`) with parallel `to_rst` reset gates (`XTO1A`, `XTO2A`, `XTO3A`).
   - This achieves `LOG-11 = 0` across all 45 corners and `LOG-12` (`t_timeout_ps`) of `255.0 ps` at `tt_nom_27` (`204.0 .. 340.4 ps` across all 45 corners).

4. **Glitch-Free Output Register (`adc_sarlogic_dlat`), Input Capacitance (`LOG-14`, `LOG-15`) & Device SOA (`LOG-17`)**
   - Upon completion of step 14 (`DONE14 = 1`), `LAT_EN` pulses to transfer all 14 raw bits `Q<13:0>` into `D<13:0>` prior to raising `RDY`, guaranteeing zero mid-conversion transitions on `D<13:0>` (`LOG-10 = 104.0 .. 183.5 ps >= 100 ps` across all 45 corners).
   - Compact input buffers on `CONV` (`LOG-14 = 2.53 fF <= 40 fF`) and `OUTP` / `OUTN` (`LOG-15 = 4.22 fF <= 7 fF`) minimize loading on `adc_clkgen` and `adc_comp`.
   - Balanced request-combiner sizing (`XGA`, `XGB`, `XG1..XG5`), fast completion-chain reset (`XDONE`, `XD4`), and `VSS`-tied `XTO1A:A` eliminate internal stack-node bootstrap spikes during reset, achieving **`LOG-17 = 0` (`0` SOA violations across all 45 corners)**.

## 45-Corner Verification Summary (`369 / 369` Required Corner-Specs Passing across 5 Testbenches)

| Spec | Metric | Target Limit | Corner Scope | Measured (`tt_nom_27` / 45-Corner Range) | Status | Testbench |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `LOG-01` | `func_errors` | `<= 0` | `all` (45/45) | `0` (`0` across 45,000 conversions) | **PASS** | `tb_sarlogic_rand` |
| `LOG-02` | `t_bit_ps` | `<= 40 ps` | `typ` (1/1) | `27.55 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-03` | `t_rst_ps` | `<= 45 ps` | `typ` (1/1) | `24.31 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-04` | `t_dac_fast_ps` | `35 .. 60 ps` | `typ` (1/1) | `47.43 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-05` | `t_dac_slow_ps` | `70 .. 100 ps` | `typ` (1/1) | `95.44 ps` | **PASS** | `tb_sarlogic_func` |
| `LOG-06` | `t_dac_slow_ps` | `70 .. 160 ps` | `all` (45/45) | `95.44 ps` (`72.84 .. 130.8 ps` across 45 corners) | **PASS** | `tb_sarlogic_func` |
| `LOG-07` | `t_start_ps` | `80 .. 160 ps` | `all` (45/45) | `106.6 ps` (`81.65 .. 145.1 ps` across 45 corners) | **PASS** | `tb_sarlogic_func` |
| `LOG-08` | `t_conv_ns` | `<= 2.75 ns` | `typ` (1/1) | `2.723 ns` | **PASS** | `tb_sarlogic_func` |
| `LOG-09` | `t_conv_ns` | `<= 4.1 ns` | `all` (45/45) | `3.074 ns` (`2.689 .. 3.658 ns` across 45 corners) | **PASS** | `tb_sarlogic_func_slow` |
| `LOG-10` | `t_setup_ps` | `>= 100 ps` | `all` (45/45) | `134.0 ps` (`104.0 .. 183.5 ps` across 45 corners) | **PASS** | `tb_sarlogic_func` |
| `LOG-11` | `timeout_errors` | `<= 0` | `all` (45/45) | `0` (`0` across all 45 corners) | **PASS** | `tb_sarlogic_timeout` |
| `LOG-12` | `t_timeout_ps` | `200 .. 350 ps` | `all` (45/45) | `255.0 ps` (`204.0 .. 340.4 ps` across 45 corners) | **PASS** | `tb_sarlogic_timeout` |
| `LOG-13` | `power_uW` | `reported` | `typ` (1/1) | `1055 uW` | **INFO** | `tb_sarlogic_func` |
| `LOG-14` | `cin_conv_fF` | `<= 40 fF` | `typ` (1/1) | `2.534 fF` | **PASS** | `tb_sarlogic_func` |
| `LOG-15` | `cin_cmp_fF` | `<= 7 fF` | `typ` (1/1) | `4.215 fF` | **PASS** | `tb_sarlogic_func` |
| `LOG-16` | `t_dac_add_err_pct` | `<= 20 %` | `typ` (1/1) | `9.442 %` | **PASS** | `tb_sarlogic_func` |
| `LOG-17` | `soa_violations` | `<= 0` | `all` (45/45) | `0` (`0` across all 45 corners) | **PASS** | `tb_sarlogic_soa` |

## Acknowledged Notices

Acknowledged `[adc_sarlogic]` notices: [#61](https://github.com/many-question/ADC-12b-100M/issues/61), [#79](https://github.com/many-question/ADC-12b-100M/issues/79), [#102](https://github.com/many-question/ADC-12b-100M/issues/102), [#118](https://github.com/many-question/ADC-12b-100M/issues/118), [#135](https://github.com/many-question/ADC-12b-100M/issues/135).
