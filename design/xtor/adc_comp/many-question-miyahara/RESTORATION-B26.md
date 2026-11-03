# Original B26 restoration under adc_comp 0.11.0

The current canonical source is the original physical B26: 43 MOS devices and nine MOM capacitors. No dimensions, parasitics, connections or numerical settings were changed to restore it. It remains **WIP, unqualified and unselected** pending fresh measurements.

The exact source was recovered independently from historical simulation commit `3dd17927ddcb842b4e28289270fa76436dcb4ab1` and published commit `9036f74f024088185398717989ed589784d1d151`, path `design/xtor/adc_comp/many-question-miyahara/BUFFER-V26.txt`; both Git objects are byte-identical to the restored `adc_comp.scs`.

- Full-file SHA-256: `c418be8ea46331a424b823cfc4991ec3b3a27124ff3ed6d26fbf383c5f3fee02`.
- Electrical SHA-256 (adcflow logical lines, no trailing newline): `13c455d69c414b141aa94d910b1adc256d7929e67997eb366a71d77660a59797`.
- Complete RNL checked with core 0.5.2: zero errors, warnings and hints. The canonical schematic is regenerated from this exact source.
- Previous B20 canonical source and all historical formal records are preserved at published commit `2579cdf3c91b81599ca5f9f74a1744495ddfc1ea` and in a verified 367-member archive. Archive SHA-256: `8c2b5cb4233470f4e2932b1bb33d71d894119d87fdd7b582643f2d934959c794`; every member passed CRC and SHA-256 readback. Historical records are not relabeled as B26 results.

## Why this source is being retested

[The original B26 report](BUFFER-V26.md) records FS/low/125 noise of 270.61635250554104 uV rms, profile interval [261.07, 280.60], under the then-current 240 uV limit. That old failure is preserved. Its point estimate is below the current 280 uV limit, but it does not establish current qualification or statistical margin. B26 had no complete TT or FF noise evidence and no full-corner qualification.

Historical TT baseline/tighter 30 mV delay is 48.97788988704756/48.99406817867042 ps against 50 ps. Input capacitance is 19.328731218738323 fF against 20 fF. These narrow margins are explicit first-round checks. Historical convergence failures of B25 and B27 are not attributed to B26.

## Current qualification plan

Main `ac9f7a3bd2c788345464e292a74271d7febe2f8c` is incorporated. Issues #131 and #136 are acknowledged for this candidate: CMP-13 280 uV, CMP-08 45 ps, unchanged TT CMP-01 200 uV and CMP-15, plus official per-device CMP-17 SOA including startup and the sliding-window short-overvoltage rule.

First run fresh official full 17 x 512 physical noise at TT, FF/low/125 and FS/low/125; TT delay/loading; representative official SOA and supporting 43/38/69 ps short-reset windows. Keep exact conservative numerical settings, physical stochastic sources and selective saves. If these gates pass, continue full 45-corner noise, delay, kickback and SOA, TT 50-sample mismatch, then mixed-top reference regression. A measured failure stops qualification expansion for this source and is retained with its raw evidence; no limit adjustment is requested by this restoration.

New run and archive receipts will be appended after measurement. No fresh result is claimed by this source-freeze checkpoint.
