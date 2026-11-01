# adc_sarlogic candidate many-question

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
   - Upon completion of step 14 (`DONE14 = 1`), `LAT_EN` pulses to transfer all 14 raw bits `Q<13:0>` into `D<13:0>` prior to raising `RDY`, guaranteeing zero mid-conversion transitions on `D<13:0>`.
   - Compact input buffers on `CONV` (`LOG-14 = 2.53 fF <= 40 fF`) and `OP_B` / `ON_B` (`LOG-15 = 4.22 fF <= 7 fF`) minimize loading on `adc_clkgen` and `adc_comp`.

## Acknowledged Notices

Acknowledged `[adc_sarlogic]` notices: [#61](https://github.com/many-question/ADC-12b-100M/issues/61), [#79](https://github.com/many-question/ADC-12b-100M/issues/79), [#102](https://github.com/many-question/ADC-12b-100M/issues/102), [#118](https://github.com/many-question/ADC-12b-100M/issues/118).
