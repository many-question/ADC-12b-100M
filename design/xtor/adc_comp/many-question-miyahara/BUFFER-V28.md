# B28: larger buffer MOMs

Private, unqualified physical trial. Only CBP/CBN change 48 to 56 fingers (14.0604 to 16.4603 fF), using exact verified CDP/CDN geometry. All 43 MOS and seven other MOMs are unchanged. Provider and original callback hash match. CDP/CDN drawing labels are corrected from nr48 to actual nr56. B27 tighter convergence failed; the slower-buffer hypothesis does not establish its root cause.

Electrical SHA-256 `6c009cb444cb9b82dfb7d5a48e66c927e1d0d8b6becdfc569f5c89677bd29988`; callback `f553a09aa0a859e87a377f0522eb6653774ef645a8e8fd75d37e131fce9a7560`. [Complete RNL](BUFFER-V28.txt) checks/renders without errors or warnings; drawing inspected locally. [Predecessor source](https://github.com/many-question/ADC-12b-100M/blob/52145b84a2bb73ed7a177c01cb32ba0eac006139/design/xtor/adc_comp/many-question-miyahara/BUFFER-V27.txt) and failures retained. Fresh baseline/tighter timing, reset, validity, private 1.0 V stress, loading and full physical noise are pending. Canonical/formal failure unchanged.

## Recovered baseline evidence, 2026-11-01

The original five-corner run is now closed after input/remote hash checks and verified retrieval; no resimulation was performed. All 180 actual decisions and reset cycles were audited. The raw archive passes CRC and member SHA-256 verification: `86a3823c35ddfabb29c02fca7cc0857fcaab3984daa3d1d3358f94ccbcfb1784`.

| Corner | 1 mV delay (ps) | 30 mV delay (ps) | Reset (ps) | Validity violations | Peak terminal voltage (V) |
|---|---:|---:|---:|---:|---:|
| fs_high_m40 | 51.10846579495296 | not scored | 21.823335220604005 | 0 | 0.999115128250357 |
| fs_low_125 | 62.76913225335976 | not scored | 27.35533335207982 | 0 | 0.8130993431403791 |
| sf_high_m40 | 56.240320202038845 | not scored | 22.400175873720997 | 0 | 0.9991822713834294 |
| ss_low_125 | 77.35796293080188 | not scored | 33.849248058474764 | 0 | 0.8161839497852804 |
| tt_nom_27 | 57.100164542991756 | 48.203099614489815 | 25.037594715671435 | 0 | 0.9079938420652097 |

B28 passes this limited baseline deterministic screen. Tighter repeats and physical noise are not established; no promotion or full qualification is claimed. The original testbench was spec 0.8.0; these retained measurements are not relabeled as fresh formal spec 0.9.0 results.

Dedicated TT input/clock capacitance was already measured at 19.328731218738323/12.110022963648854 fF; retained archive SHA-256 `f8deb8ac647e2f2a2be32f2092be72b8eac595529a3746438a5e24a78a56a6a9`.
