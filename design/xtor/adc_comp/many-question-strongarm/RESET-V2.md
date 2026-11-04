# RESET-V2: direct-clock reset experiment

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

This independent experiment removes RESET-V1's NAND/NOR controls, their internal floating nodes and the now-unused two-inverter clock branch. The tail and all four single precharge devices use CLKC. Input precharge remains 2.4 um / 30 nm, nf3; Q precharge remains 6 um / 30 nm, nf6. The other device geometries and the two input-drain capacitors are unchanged. These geometries reuse successful, warning-free callbacks from RESET-V1; no parasitic values were hand scaled.

The hypothesis is that direct tail activation avoids V1's added evaluation delay and Q-node rising-edge overshoot, while single precharge removes DPX/DNX and AX entirely. Stronger Q reset may retain the slow-corner reset improvement. Direct clock coupling and clock-input charge remain risks to measure.

The standalone Spectre source is [RESET-V2.txt](RESET-V2.txt), with full RNL. Its electrical SHA-256 is `608dfd3e547ee65738662bf62ef9c9cb548b0b7ea1000b21c22087ee0c958db8`. It has 15 MOS and two MOM capacitors. A byte-identical `.scs` validation mirror passes RNL core 0.5.2 with 0 errors, 0 warnings and 0 hints; the extension workaround does not change the source.

![Direct-clock experiment](https://raw.githubusercontent.com/many-question/ADC-12b-100M/e45f2ad7bea3b45f5822eae18549b326c19fc727/design/xtor/adc_comp/many-question-strongarm/reset-v2.png)

The planned first screen uses TT nominal 27 C, FF high -40 C, FF high 125 C and SS low 125 C, the current v0.7.0 delay stimulus and measurement, 0.5 ps maximum step, traponly, reltol 1e-6 and vabstol 1e-8. Every MOS |Vgs|, |Vgd| and |Vds| is checked over the full trace. Physical output validity, delay, reset, AVDD energy and supplemental clock charge are measured. Existing matched baseline traces are reused as references, not rerun or relabeled. No new validation is claimed in this source-freeze commit.

Canonical `adc_comp.scs` and its official results remain the previous baseline. A failed screen stops this version's expansion while evidence-based iteration continues.

## Completed four-corner screen

Actual source commit: `8d67a75c40bb99dd5066e64ae8e8db687c7daa1f`. All four jobs completed successfully. This version fails high-voltage stress and will not be expanded.

| Corner | 1 mV delay ps | 30 mV delay ps | Reset ps | AVDD fJ | Losing peak % VDD | Maximum terminal V | Failed pairs / 45 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 57.254343 | 44.241961 | 18.616292 | 151.398834 | 17.106816 | 0.956410 | 0 |
| ff_high_m40 | 43.299197 | 33.742890 | 14.385204 | 171.721568 | 18.618108 | 1.048560 | 8 |
| ff_high_125 | 42.833602 | 32.635112 | 16.317241 | 274.766018 | 19.717295 | 1.038750 | 8 |
| ss_low_125 | 74.637375 | 57.102136 | 25.168412 | 140.186650 | 15.961280 | 0.862230 | 0 |

CMP-15 is 0/144 cycles and first-event polarity is correct in all four traces. Compared with the matched 0.5 ps canonical baseline, SS low/hot reset improves from 38.439852 to 25.168412 ps; TT AVDD energy falls from 190.686419 to 151.398834 fJ. These are current-meter private comparisons, not refreshed official records. Supplemental mixed-cycle clock Ceff is 15.204425 fF at TT, not an official CMP-14 measurement.

The maximum QP voltage is 1.048563379 V in FF high/cold at 110 ps, the end of the first clock rise. At that sample CLKC is 0.99 V, TAIL is 0.353397 V and OUTP is 0.001577 V. QN also reaches 1.048223 V. In FF high/hot QP reaches 1.038747022 V. Removing the floating control nodes and tail delay resolves V1's specific mechanisms, but direct-clock Q-precharge coupling remains. Cold QP undershoot is only -0.003858 V; the dominant remaining issue is the high excursion.

Every device's three terminal pairs was measured over the entire trace. The execution used +aps, no ++aps or explicit +mt; all logs disabled solver multithreading. Actual peak simultaneous jobs was 3. Retrieved files were SHA-256 checked before the exact owned remote directory was removed and its absence confirmed. Baseline official files remain byte-identical. Shared-tool validation: 439 non-slow tests passed, 1 deselected.
