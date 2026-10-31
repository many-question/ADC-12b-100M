# V34: stronger N latch pair

Private, unqualified physical trial. Only MLNP/MLNN change N4 to N16 (16 one-um fingers, L30nm; twice V32 N8), with complete zero-warning callback geometry/parasitics. Other 21 MOS and five MOMs are unchanged. V33 full FS noise failed at 483.2613219887676 uV; stronger latch drive is a new hypothesis, not a measured noise benefit.

Electrical SHA-256 `56babc884fca6a518621de8d4eec451b64c60dd45bf1af2ff393f3cc374e215b`; callback `f7dd3061987c03157e7411ed97c5554d5d6981d377691e3da1413bee8298ef85`. [Complete RNL](RESET-V34.txt) checks/renders without errors or warnings; drawing inspected locally. [Predecessor source](https://github.com/many-question/ADC-12b-100M/blob/d2dd7184b0f435b46b351b948eb1ca4bdbeeb99b/design/xtor/adc_comp/many-question-strongarm/RESET-V33.txt) and failures retained. Fresh baseline/tighter timing, reset, validity, private 1.0 V stress, loading and full physical noise are pending. Canonical/formal failure unchanged.

## Recovered baseline evidence, 2026-11-01

The original five-corner run is now closed after input/remote hash checks and verified retrieval; no resimulation was performed. All 180 actual decisions and reset cycles were audited. The raw archive passes CRC and member SHA-256 verification: `bd2afe8e272e1c07b5700d9054cd38c77ce85972c34ab9ed805d067d83f694b7`.

| Corner | 1 mV delay (ps) | 30 mV delay (ps) | Reset (ps) | Validity violations | Peak terminal voltage (V) |
|---|---:|---:|---:|---:|---:|
| fs_high_m40 | 57.520240033087596 | not scored | 22.867795966456057 | 0 | 0.9954512866312383 |
| fs_low_125 | 65.02306638209024 | not scored | 31.982287552495347 | 0 | 0.8111404933256227 |
| sf_high_m40 | 74.01809042939068 | not scored | 21.423611762791698 | 0 | 1.00172024722332 |
| ss_low_125 | 87.43509914047833 | not scored | 36.27916208222824 | 0 | 0.8175893429966951 |
| tt_nom_27 | 65.62900492477611 | 48.49053809494014 | 26.1897203065617 | 0 | 0.9069582264865301 |

V34 still fails the 35 ps reset limit. Its 1.00172024722332 V peak was an old 1.0 V diagnostic failure, but passes the current 1.1 V project rule. Qualification expansion remains stopped for the reset failure. The original testbench was spec 0.8.0; these retained measurements are not relabeled as fresh formal spec 0.9.0 results.

Dedicated TT input/clock capacitance was already measured at 19.331118542884703/15.497177546543838 fF; retained archive SHA-256 `c2b282b3b42742b1090dd5a5a85e4d2e4bcfdbf2c363724d3532a03991bc151b`.
