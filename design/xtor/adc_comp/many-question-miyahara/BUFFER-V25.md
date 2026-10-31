# BUFFER-V25: first-buffer timing and edge margin

**B25 has a reproducible tighter-numerics convergence failure at FS/high/-40.** The five baseline corners and dedicated TT loading pass, but the four-corner tighter gate is incomplete. Full physical noise testing is held; B25 is not promoted.

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

[B24](BUFFER-V24.md) repairs SS/FS low-hot reset but strictly fails TT 30 mV delay at 50.00497745635165 ps against 50 ps. The approximately 5 fs excess is not rounded into a pass. Its narrowest unrounded stress margin is 47.6004190316 uV at BP/BN in FS/high/-40; no tighter clearance or noise result exists. TT 30 mV mean RP, BP and external-output 50% crossings are 36.62484060586704, 45.248204187974075 and 50.00497745635165 ps.

B25 changes only MBPN/MBNN, the first-buffer pull-down MOS, from 2 um/nf2 to 2.6 um/nf2 (1.3 um finger width, length 30 nm), and CBP/CBN from 40 to 44 physical MOM fingers. Stronger pull-down targets the measured buffer-to-output evaluation path; added BP/BN storage targets the observed narrow positive edge-stress margin. The other 41 MOS devices and seven MOMs are exactly B24, including its ten-device scaled stage and repaired N8 reset assists/eight-finger RP/RN loads. All stochastic sources remain enabled.

Changing the inverter ratio also shifts its threshold and may affect losing-output rejection. Extra storage affects reset and delay. These coupled changes are a measured physical hypothesis: no pass, isolated noise benefit or promotion is inherited. Full-cycle AVDD energy includes weak loads and reset consumption.

Both accepted geometries use fresh zero-warning callbacks with complete parasitics and the same verified provider/release. Retrieval hashes match and the exact owned remote callback directory is absent. No Virtuoso, PDK model export, ideal clamp or behavioral output storage is used.

The completed baseline screen at clean source `0768f17556b497d222a2b9d07bb9d72a63e5ed4e` passes TT, SS/low/125, SF/high/-40, FS/high/-40 and FS/low/125. All 180 actual decisions and resets, output validity, every one of 129 unrounded terminal pairs per corner and full-cycle AVDD KCL pass. TT 1 mV/30 mV delay is 58.04680362938184/48.65231181041175 ps; SS/low/125 reset is 32.64727688136176 ps. The highest unrounded stress is 0.9995750733643868 V at FS/high/-40, leaving only 424.92663561322087 uV. This requires tighter verification before noise expansion.

Matched B24/B25 physical testbenches and numerical settings locate the TT 30 mV mean RP, BP and external-output 50% crossings at 36.6803612927205, 44.156566834671715 and 48.65231181041175 ps for B25. RP is slightly later than B24, while the buffer/output path is earlier. SS reset increases from 32.17894196165223 to 32.64727688136176 ps. All cycle-level path data are retained; these coupled changes do not isolate a noise contribution.

Dedicated TT Cin/CLKC are 19.328731218738323/12.105047338129033 fF, both passing. Net per-cycle kickback is 8.58761000678554e-05 uV, a numerical residual. Separate instantaneous differential disturbance reaches 30.64311606267001 uV during reset and common-mode excursion reaches 7.418206202436939 mV during evaluation. They are not compared with the net 40 uV limit; actual-CDAC decision-phase validation remains open.

[NUMERICS-94](NUMERICS-94.md) records the complete baseline delay and capacitance/kickback results. Both archives were read back with CRC/SHA verification; only verified expanded duplicates were removed. The retained delay archive includes the matched B24/B25 path audit, and the kickback archive includes full phase/load context. No B25 noise result or promotion exists. Every new simulation selects exact DUT/SOA/metric signals or keeps the original monitor-only noise protocol, with at most six session-wide jobs. Stimuli, numerical acceptance definitions and limits remain unchanged.

## Reproduced tighter convergence failure

The four-corner attempt `20261031-154911-miyahara-buffer-v25-spec08-delay-tighter-screen` and isolated FS repeat `20261031-155649-miyahara-buffer-v25-spec08-delay-tighter-screen` use frozen source `a67115971679dcbf8bfbe3102be700d14931315a`. Both fail FS/high/-40 with SPECTRE-16929 at 137.816 ps: 1000 consecutive timesteps below 1.45e-21 s. Each retains 1260 accepted samples through 137.8159453449029 ps, with identical last saved node values. The failed Newton iterate is not in those accepted samples. The diagnostic identifies current convergence failures including MOPP's bulk terminal; it does not establish the underlying model or circuit cause.

The complete physical source, exact tested TB, numerical overrides and job deck after run-path normalization match between attempts. Only dispatch grouping changes from the four-corner batch to an isolated FS job. The first attempt's TT/SS/SF jobs return zero, but are preserved without claiming a complete tighter gate. No tolerance, maxstep, numerical capacitance, model or acceptance limit is changed. Baseline passage cannot clear this repeated failure.

All 79 and 55 fetched/staged files respectively match remote SHA-256 hashes. Both owned process sets ended, source/canonical/formal guards pass, and both exact remote directories are absent. The failed runs retain `failed_reviewed` status and all partial raw/log evidence. ZIP CRC/SHA readback passed before native removal of expanded duplicates: original archive `0f08fb5f42597c59c0fb31bbdaebb0631a4886ec23fa6b5a90e20d4af08b33db`; isolated repeat `af149bbea21cf9b349b62e0951e778a51306447f094e6f8a7b318f496489a4d9`.


| Callback | SHA-256 |
|---|---|
| cb44 | `7c980b3d9fa9ea317087d837feea5cab285a7ff84a9de34c7d0fe95f6b90b851` |
| n26 | `035f1627060423d06dfea2ec4fc93c3d57a188e2adda8d95b57da1f5012a9d33` |

Electrical SHA-256: `729ab621a0c85d21bc76dc59004ec69ce304a3d678f1c259427ee062c67d6959`. The [complete RNL source](https://github.com/many-question/ADC-12b-100M/blob/855618b7d6ad7aeed2b909dfbd70e4b86975e99a/design/xtor/adc_comp/many-question-miyahara/BUFFER-V25.txt) is checked and rendered on a byte-identical mirror with zero errors and warnings. The full drawing remains in local source evidence. Prior B24 source is pinned at [published commit 18501e5](https://github.com/many-question/ADC-12b-100M/blob/18501e5d7c1ce1548c01083a5173458c9d898e65/design/xtor/adc_comp/many-question-miyahara/BUFFER-V24.txt) and in retained raw evidence. Canonical B20 and formal records are unchanged.
