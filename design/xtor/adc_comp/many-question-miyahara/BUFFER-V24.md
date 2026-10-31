# BUFFER-V24: repair scaled-stage reset and loading

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

**B24 repairs reset but still fails TT 30 mV delay:** `50.00497745635165` ps is strictly above 50 ps. The approximately 5 fs excess is retained as a failure, with no rounding waiver. SS/FS low-hot reset improves to `32.17894196165223`/`26.15800892442384` ps, below 35 ps. B24 has no noise result and is not promoted.

[B23](BUFFER-V23.md) fails SS/FS low-hot reset at 46.1394172594504/35.69263848338459 ps and TT 30 mV delay at 50.14965558025553 ps. All 180 actual decisions/resets and full-device stress pass, but those timing failures stop noise expansion. At its worst SS cycle, CKB reaches 90% at 12.077896200270299 ps while RP/RN reach 30% at 33.5402498709134 ps; B22 measured 11.691430471496775 and 19.753870866716156 ps respectively. This points to the regenerative-node discharge path for the next experiment.

B24 changes only MRQP/MRQN N4 to N8 at 30 nm/1 um finger width and CRP/CRN from 16 to 8 physical MOM fingers. The other 41 MOS devices and seven MOMs are exactly B23, including its doubled ten-device second stage, input pair, tail, clock driver and external output buffers. Stronger reset assists target the observed RP/RN discharge delay; smaller MOM loading targets both evaluation and reset delay. Added CKB gate loading, reset release, stress and all-source noise must be remeasured. This combined physical experiment does not isolate a unique capacitance, transconductance or noise contribution.

Both complete geometries come from fresh zero-warning callbacks with matching provider/release, SHA-verified retrieval and exact remote-directory absence. No ideal clamp, behavioral latch, disabled noise source, or changed stimulus is introduced.

| Callback | SHA-256 |
|---|---|
| cr8 | `d1cd467c1d3b6acba416f8d0e58f6f7b2973b5576df3a03d6ac9438a521d9a15` |
| n8 | `e705ebc2985cc3b6bbbe232cb188f1b0c155751d55a7a5aeaeec5df014a19f6a` |

Electrical SHA-256: `763f0e16fbbc42e1d237fa6e316ddfbab162a21b59b7396fd92dd1bf1281e7cc`. The [complete RNL source](https://github.com/many-question/ADC-12b-100M/blob/18501e5d7c1ce1548c01083a5173458c9d898e65/design/xtor/adc_comp/many-question-miyahara/BUFFER-V24.txt) is checked/rendered on a byte-identical mirror with zero errors/warnings; its full drawing remains in local source evidence. B23 source is pinned at [published commit 01524e4](https://github.com/many-question/ADC-12b-100M/blob/01524e4bc95e7a6eb73f09ae6d4f2fb1a99d3e88/design/xtor/adc_comp/many-question-miyahara/BUFFER-V23.txt) and in its retained raw archive. Canonical B20 and all formal results are unchanged.

First repeat TT, SS/low/125, SF/high/-40, FS/high/-40 and FS/low/125 timing/reset/validity/SOA plus dedicated TT input/clock capacitance. Only a useful pass permits full physical noise at the known FS/low/125 problem corner. Every private run uses explicit selected DUT/SOA/metric saves or the preserved monitor-only noise protocol, under the six-job session limit. No pass or promotion is assumed.

## Completed five-corner screen

Frozen source `892fe664af7c0764ed93b689b28da4514b64dd63` retains all 180 actual decisions and resets, including 10 uV polarities. Every full evaluation output-validity check and all 129 MOS terminal pairs per corner pass. The smallest unrounded stress margin is only `47.6004190316` uV, at the first-buffer node in FS/high/-40 (`0.9999523995809684` V); tighter-numerics clearance is untested. Timing failure stops full noise and qualification expansion.

The same-numerics/non-output-testbench comparison with B23 shows SS CKB 90% becoming later, 12.077896200270299 to 14.05786243640283 ps, while both RP/RN below 30% improve from 33.5402498709134 to 17.561926427432788 ps. Both BP/BN above 90% improve from 39.53923185833273 to 26.184684074884604 ps and external reset from 46.1394172594504 to 32.17894196165223 ps. All cycles remain in the comparison. The combined size/load change repairs the observed reset path without isolating the two contributions.

At TT/30 mV, RP/RN 50%, BP/BN 50% and output 50% mean crossings occur at 36.62484060586704, 45.248204187974075 and 50.00497745635165 ps. The next physical experiment targets first-buffer pull-down speed and adds buffer-node edge storage to address the narrow measured voltage margin. Its output threshold, losing-output validity, reset, all-device stress and noise must be remeasured.

Dedicated TT Cin/CLK Cin are 19.328731218738323/12.105033730917267 fF. Net per-cycle kickback is 8.291090015065394e-05 uV; the distinct instantaneous differential maximum is 30.67320509575933 uV in reset, and common-mode maximum is 7.418207759610773 mV in evaluation. Actual-CDAC decision-phase validation remains open. TT full-cycle AVDD meter energy is 699.9399864 fJ; all supply probes are present and KCL closes. [NUMERICS-94](NUMERICS-94.md) retains all measurements and numerical/output settings.

- `20261031-152741-miyahara-buffer-v24-spec08-delay-baseline-screen`: archive SHA-256 `2cd8f43a2829e19f19c91bc9cf7ab356afb08692e9dfe466c652dbd901e08c3e`.
- `20261031-152755-miyahara-buffer-v24-spec08-kickback-baseline-screen`: archive SHA-256 `755525d32f379a3891466cd6bfe5c08e5f3412ff9992c3258d5643dd1ba5ca7b`.

Every archive member passed CRC/SHA readback, and both exact remote run directories are absent. Canonical B20 and genuine formal results are unchanged.
