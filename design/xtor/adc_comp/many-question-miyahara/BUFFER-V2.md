# BUFFER-V2: recover threshold-stage speed

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

BUFFER-V1 has a large output-validity margin in its six screened corners but misses the TT 30 mV delay by 2.984 ps. This experiment changes only the first buffer NMOS from 0.5 um/nf1 to 1 um/nf1, using the existing successful callback geometry. It increases pull-down drive and lowers the first-stage switching region. The P6 first-stage device, second inverter, core and reset circuitry remain electrically identical to V1.

The first diagnostic compares TT and SF low/-40 C against their existing V1 traces at the same 0.5 ps settings. It tests whether the speed recovery preserves physical losing-output suppression before spending work on a separate reset/feedthrough redesign. V1's high-voltage failures remain known concerns; no high-voltage qualification is inherited or claimed.

Independent source: [BUFFER-V2.txt](BUFFER-V2.txt), 31 MOS and four MOM. Electrical SHA-256: `2fcb783897758f6e3191cf85edcb8dc3a3fc8b4b357e80f8a59de2cfefa1b666`. Full RNL passes core 0.5.2 on a byte-identical `.scs` mirror with 0 errors, 0 warnings and 0 hints. This source-freeze commit claims no performance result.

![Faster first-stage pull-down](https://raw.githubusercontent.com/many-question/ADC-12b-100M/fe173f9df274e8fa4fdddfbdb14f20208dc441fb/design/xtor/adc_comp/many-question-miyahara/buffer-v2.png)

## Completed targeted speed/validity check

Actual frozen source: `c4c736318f2d05a1fd3eb59f8d4e739a77ba5ebd` (full commit retained in each private record). TT 30 mV delay falls from 52.984285 to 48.296388 ps. Both targeted traces decide all 36 cycles with correct first-event polarity and CMP-15 = 0. The threshold-stage speed change is retained for the next reset/feedthrough revision.

| Corner | 1 mV ps | 30 mV ps | Reset ps | AVDD fJ | Losing peak % VDD | Max terminal V | Violating pairs / 93 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tt_nom_27 | 58.878904 | 48.296388 | 22.647479 | 205.667996 | 0.122957 | 0.921550 | 0 |
| sf_low_m40 | 72.605439 | 58.773821 | 25.850392 | 147.619438 | 0.162395 | 0.847300 | 0 |

This is a two-corner diagnostic, not a high-voltage clearance. The next step must repair V1's observed high-voltage clock/reset excursions and recheck the complete circuit. No all-corner, noise or MC expansion has been launched. Both jobs used +aps, no ++aps or explicit +mt, with solver multithreading disabled; actual peak was one job because the first job warmed the shared AHDL library. Concurrent work was explicitly reserved under the session ceiling of six. Raw/source/deck hashes were verified before remote cleanup.

## Remaining four key corners completed

After the first two corners passed, the remaining four key corners were measured without rerunning the completed cases. Actual clean source commit: `ece253cfbba122b68907dd7ee2399a0f11e100b9`; the electrical source and source-file hashes match the first two-corner run. These fresh measurements confirm that all six tested corners pass decisions, external output validity, delay and reset, while high-voltage terminal stress still fails. The B1 voltage results are not inherited.

| Corner | 1 mV ps | 30 mV ps | Reset ps | AVDD fJ | Losing peak % VDD | Max terminal V | Violating pairs / 93 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ff_high_m40 | 44.721462 | 36.937768 | 17.323400 | 242.006861 | 0.116221 | 1.017210 | 50 |
| ff_high_125 | 51.603197 | 40.621728 | 18.226117 | 424.670505 | 0.761046 | 1.008230 | 10 |
| ss_low_125 | 80.476533 | 64.988479 | 29.678585 | 189.486615 | 0.172515 | 0.833300 | 0 |
| sf_high_27 | 56.309755 | 46.596302 | 20.899112 | 260.574573 | 0.165078 | 1.018890 | 44 |

The SF low/-40 raw losing node still reaches 0.421485 V (52.035% VDD) before the physical buffer suppresses it. Thus raw common-mode behavior remains important when modifying thresholds or adding feedback. Six-corner external CMP-15 is 0/216 cycles; the largest external losing peak is 0.761047% VDD. No broad corner/noise/MC expansion is performed on this failing source. All 93 terminal pairs per trace were checked, hashes verified, and exact-owned remote cleanup completed. The follow-on batch peaked at three jobs, +aps with effective single-thread solving.
