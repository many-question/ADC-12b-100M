# Split-stage comparator A1

**Initial screen failed; expansion stopped.** TT 30 mV delay is 59.9852 ps against 50 ps, and only 8/36 TT and 4/36 FS decisions complete. See [the retained A1 screen](A1-SCREEN.md) for the three recorded tests, physical timing, signal decay and limitations. Status remains `wip`.

This work-in-progress candidate separates a dynamic integrating input stage from a second StrongARM latch. The first-stage DP/DN nodes connect only to the second input pair's gates. Two physical tail switches, physical precharge devices and transistor clock generation are present in each appropriate stage. Physical output inverters preserve the return-to-zero interface.

The first circuit contains 40 MOS devices and 10 MOM capacitors. All MOS geometries and MOM instance parameters were generated with successful device callbacks. The external input pair is W56/L0.03 with 56 fingers; front and latch tails each use two W3/L0.03 units. Front precharge uses P16. Each front drain has five 52-finger, 1 µm MOM units (76.3015 fF nominal total before device parasitics). The second pair is W4, with N12/P8 regenerative devices and N2/P4 output inverters. Dimensions are in µm; all MOS lengths are 0.03.

CLKC drives two physical inverters to CKF. CKF passes through four further inverters to CKD. A physical NAND2 and inverter produce CKL = CLKC AND CKD. The direct CLKC path lets CKL fall without waiting for the delay chain. No ideal source, delay, or assumed 20 ps phase spacing is part of the candidate. Actual rise/fall crossings and reset overlap must be measured with the full load.

## Prior risks and bounded first validation

- At a separate fixed FS diagnostic point, the unchanged W56 input geometry gave gm 21.68 mS and gds 4.23 mS at 1.75 mA per branch. This does not support the original 25.36–38.04 mS planning assumption. It is not a bound on all possible transient operating points.
- The old source released its front resets approximately 10–12 ps after CLKC 50%. The added physical clock path may consume much of the TT 50 ps budget. Neither timing nor noise feasibility is established.
- The 0.3–0.8 pJ energy range is planning context only. CMP-10 is reported without an acceptance limit. The official CMP-14 limit is 16 fF; 15 fF is only an optional margin target.
- Only TT and FS official 36-cycle noise-off delay tests and TT loading are authorized initially. Noise, mismatch, remaining corners and common-mode endpoints are untested. Any TT 30 mV delay failure or absence of a useful gain interval stops expansion.
- Simplified 4kTγ/∫gm and weighted variants, and any RSS allocation, are assumptions rather than hard bounds or proof that reset/front/latch noise are independent.

## History

Earlier candidates and all their evidence remain unchanged: [StrongARM at cf7a3524](https://github.com/many-question/ADC-12b-100M/tree/cf7a3524aa3872b3fd6145826ff3430979f3b918/design/xtor/adc_comp/many-question-strongarm) and [Miyahara at 2579cdf3](https://github.com/many-question/ADC-12b-100M/tree/2579cdf3c91b81599ca5f9f74a1744495ddfc1ea/design/xtor/adc_comp/many-question-miyahara). This independent candidate does not reuse their result claims.

Open comparator notices #69, #78, #84, #100 and #116 were read. The circuit and tests target specification 0.9.0 with conservative transient numerics and APS. The source includes complete RNL placement, orientation, explicit pin wires and exact net labels, matched-device semantics and functional groups.
