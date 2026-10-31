# BUFFER-V24: repair scaled-stage reset and loading

[B23](BUFFER-V23.md) fails SS/FS low-hot reset at 46.1394172594504/35.69263848338459 ps and TT 30 mV delay at 50.14965558025553 ps. All 180 actual decisions/resets and full-device stress pass, but those timing failures stop noise expansion. At its worst SS cycle, CKB reaches 90% at 12.077896200270299 ps while RP/RN reach 30% at 33.5402498709134 ps; B22 measured 11.691430471496775 and 19.753870866716156 ps respectively. This points to the regenerative-node discharge path for the next experiment.

B24 changes only MRQP/MRQN N4 to N8 at 30 nm/1 um finger width and CRP/CRN from 16 to 8 physical MOM fingers. The other 41 MOS devices and seven MOMs are exactly B23, including its doubled ten-device second stage, input pair, tail, clock driver and external output buffers. Stronger reset assists target the observed RP/RN discharge delay; smaller MOM loading targets both evaluation and reset delay. Added CKB gate loading, reset release, stress and all-source noise must be remeasured. This combined physical experiment does not isolate a unique capacitance, transconductance or noise contribution.

Both complete geometries come from fresh zero-warning callbacks with matching provider/release, SHA-verified retrieval and exact remote-directory absence. No ideal clamp, behavioral latch, disabled noise source, or changed stimulus is introduced.

| Callback | SHA-256 |
|---|---|
| cr8 | `d1cd467c1d3b6acba416f8d0e58f6f7b2973b5576df3a03d6ac9438a521d9a15` |
| n8 | `e705ebc2985cc3b6bbbe232cb188f1b0c155751d55a7a5aeaeec5df014a19f6a` |

Electrical SHA-256: `763f0e16fbbc42e1d237fa6e316ddfbab162a21b59b7396fd92dd1bf1281e7cc`. The [complete RNL source](BUFFER-V24.txt) is checked/rendered on a byte-identical mirror with zero errors/warnings; its full drawing remains in local source evidence. B23 source is pinned at [published commit 01524e4](https://github.com/many-question/ADC-12b-100M/blob/01524e4bc95e7a6eb73f09ae6d4f2fb1a99d3e88/design/xtor/adc_comp/many-question-miyahara/BUFFER-V23.txt) and in its retained raw archive. Canonical B20 and all formal results are unchanged.

First repeat TT, SS/low/125, SF/high/-40, FS/high/-40 and FS/low/125 timing/reset/validity/SOA plus dedicated TT input/clock capacitance. Only a useful pass permits full physical noise at the known FS/low/125 problem corner. Every private run uses explicit selected DUT/SOA/metric saves or the preserved monitor-only noise protocol, under the six-job session limit. No pass or promotion is assumed.
