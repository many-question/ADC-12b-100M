# Split-stage comparator A5

**A5 passes the initial TT/SF delay and TT loading screen.** SF validity is repaired by changing only MOPN/MONN from N2 to complete callback-derived N3 geometry. TT 30 mV delay is 49.630304508151376 ps, leaving only 0.3696954918 ps margin. See [A5 measurements and timing cost](A5-SCREEN.md). All connections, including the A4 NAND reorder, remain unchanged. Fresh records cover TT/SF delay and TT loading; older FS/SS/FF records are stale. Wider corners, common-mode and noise remain unestablished; status is `wip`.

**A4 fixes SOA in the bounded TT/SF screen, but SF still fails CMP-15.** TT 30 mV delay is 48.745866 ps; SF loser peak is 34.472066% VDD with eight violations. See [A4 measurements and reset mechanism](A4-SCREEN.md). Only MNG1 gate CLKC→CKD and MNG2 gate CKD→CLKC change; all device geometries, PMOS connections and outputs remain unchanged. Logic remains CKL=CLKC AND CKD. A3 evidence is frozen at [93caae32](https://github.com/many-question/ADC-12b-100M/tree/93caae32913aef5c8a1754210ff9cf2c398f027a/design/xtor/adc_comp/many-question-splitstage). TT/SF delay records are fresh for A4; remaining A3 records, including loading, are stale. No loading, CM or noise jobs were added.

**A3 fails the subsequent representative-corner gate.** SF high voltage at -40 C has eight CMP-15 violations (loser peak 34.2195% VDD) and MNG1 Vds=1.116376 V against 1.1 V. SS and FF pass the bounded gate; a separate tighter TT diagnostic also passes but retains narrow margins. See [the failure measurements and mechanism](A3-GATES.md). CM endpoints and all noise testing stopped before dispatch. Status remains `wip`.

**A3 passes the initial TT/FS deterministic and TT loading screen, with narrow TT timing/validity margins.** TT30mV=49.5278ps, TT loser peak=27.2491% VDD; see [A3 measurements and remaining gates](A3-SCREEN.md). No noise or qualification claim is made. It removes MD1P/MD1N/MD2P/MD2N, connects MD3P/MD3N gates to CKF, and preserves every other A2 instance. The current clock chain has two inverters, MD3 and MD4. [A2 remains frozen at 7fa8baf4](https://github.com/many-question/ADC-12b-100M/tree/7fa8baf44200b05e2e4da2d501600f1c0aa6c588/design/xtor/adc_comp/many-question-splitstage).

**A2 restores 36/36 deterministic decisions at TT and FS, but TT 30 mV delay is 56.7251 ps and still fails 50 ps.** See [A2 measurements and hold limitations](A2-SCREEN.md). Only two delay jobs were run; no A2 loading or noise result is available. A1 source and results remain frozen at [d948f9af](https://github.com/many-question/ADC-12b-100M/tree/d948f9af607cb669d18d37c2175624e726b4f7e3/design/xtor/adc_comp/many-question-splitstage). A2 adds only a four-MOS NOR2, CKE=NOT(CKB OR CKL), and connects the two front-tail gates to CKE. Front resets stay on CKF; all analog geometries, MOMs, four delay stages and the second latch are unchanged. The old TT loading record belongs to A1 and is stale for A2.

**A1 screen failed; its expansion stopped.** TT 30 mV delay is 59.9852 ps against 50 ps, and only 8/36 TT and 4/36 FS decisions complete. See [the retained A1 screen](A1-SCREEN.md) for the three recorded tests, physical timing, signal decay and limitations. Status remains `wip`.

This work-in-progress candidate separates a dynamic integrating input stage from a second StrongARM latch. The first-stage DP/DN nodes connect only to the second input pair's gates. Two physical tail switches, physical precharge devices and transistor clock generation are present in each appropriate stage. Physical output inverters preserve the return-to-zero interface.

The A3 circuit contains 40 MOS devices and 10 MOM capacitors. All MOS geometries and MOM instance parameters were generated with successful device callbacks. The external input pair is W56/L0.03 with 56 fingers; front and latch tails each use two W3/L0.03 units. Front precharge uses P16. Each front drain has five 52-finger, 1 µm MOM units (76.3015 fF nominal total before device parasitics). The second pair is W4, with N12/P8 regenerative devices and N2/P4 output inverters. Dimensions are in µm; all MOS lengths are 0.03.

CLKC drives two physical inverters to CKF. CKF passes through two further inverters to CKD. A physical NAND2 and inverter produce CKL = CLKC AND CKD. The direct CLKC path lets CKL fall without waiting for the delay chain. No ideal source, delay, or assumed 20 ps phase spacing is part of the candidate. Actual rise/fall crossings and reset overlap must be measured with the full load.

## Prior risks and bounded first validation

- At a separate fixed FS diagnostic point, the unchanged W56 input geometry gave gm 21.68 mS and gds 4.23 mS at 1.75 mA per branch. This does not support the original 25.36–38.04 mS planning assumption. It is not a bound on all possible transient operating points.
- The old source released its front resets approximately 10–12 ps after CLKC 50%. The added physical clock path may consume much of the TT 50 ps budget. Neither timing nor noise feasibility is established.
- The 0.3–0.8 pJ energy range is planning context only. CMP-10 is reported without an acceptance limit. The official CMP-14 limit is 16 fF; 15 fF is only an optional margin target.
- The initial TT/FS and TT loading screen passed on A3. The subsequent SS/FF/SF gate failed at SF; noise, mismatch, remaining corners and common-mode endpoints remain untested. Expansion is stopped.
- Simplified 4kTγ/∫gm and weighted variants, and any RSS allocation, are assumptions rather than hard bounds or proof that reset/front/latch noise are independent.

## History

Earlier candidates and all their evidence remain unchanged: [StrongARM at cf7a3524](https://github.com/many-question/ADC-12b-100M/tree/cf7a3524aa3872b3fd6145826ff3430979f3b918/design/xtor/adc_comp/many-question-strongarm) and [Miyahara at 2579cdf3](https://github.com/many-question/ADC-12b-100M/tree/2579cdf3c91b81599ca5f9f74a1744495ddfc1ea/design/xtor/adc_comp/many-question-miyahara). This independent candidate does not reuse their result claims.

Open comparator notices #69, #78, #84, #100 and #116 were read. The circuit and tests target specification 0.9.0 with conservative transient numerics and APS. The source includes complete RNL placement, orientation, explicit pin wires and exact net labels, matched-device semantics and functional groups.
