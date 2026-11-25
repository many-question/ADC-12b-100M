# A5 representative corners, numerical sensitivity and CM gates: pass

Six bounded tests on unchanged A5 source pass: official nominal-CM FS/SS/FF noise-off delay tests, one private tighter TT diagnostic, and private FS common-mode endpoints at 0.40/0.56 V. All six retain 36 correct decisions and reset, CMP-09/CMP-15=0, no front differential reversal before the expected output, and all 40-MOS/120-pair full-transient SOA checks below 1.1 V. This is selected coverage, not full qualification.

Source SHA-256: `2de4dd1c4da47a28a4449dbac1ee532f70012475528bd4d55f5a5b71108f14bb`. The source and all geometry remain exactly those of the [initial A5 screen](A5-SCREEN.md).

| Test | d30 (ps) | d1 (ps) | tau (ps) | reset (ps) | loser (% VDD) | exact SOA max (V) |
|---|---:|---:|---:|---:|---:|---:|
| fs_low_125 official | 58.538570278 | 77.400806810 | 6.008275018 | 22.800556454 | 12.908472470 | 0.859454264 |
| ss_low_125 official | 67.944295028 | 87.369279377 | 6.371254845 | 26.051325457 | 15.029969455 | 0.868747584 |
| ff_high_m40 official | 37.439749020 | 46.865988856 | 3.183919398 | 15.852547160 | 17.267556114 | 1.059023823 |
| tt_nom_27 tighter | 49.622718539 | 62.900424490 | 4.661766107 | 19.809128506 | 16.745840216 | 0.970472643 |
| fs_low_125 VCM=0.40 | 57.099859510 | 74.710468073 | 5.652221562 | 22.840758734 | 13.929076143 | 0.859241549 |
| fs_low_125 VCM=0.56 | 60.270595995 | 80.039588212 | 6.152335776 | 22.715036705 | 12.422547894 | 0.859562674 |

The 50 ps d30 and 80 ps d1 limits apply at TT. Other corners use their applicable limits; in particular FS VCM=0.56 V d1=80.039588 ps passes the all-corner 120 ps limit. No acceptance limit was relaxed. Energy remains reporting only.

## Independent tighter TT result

Requested reltol=1e-6 and voltage abstol=1e-8; effective conservative settings from the log are reltol=1e-7, voltage abstol=1e-8, gear2only. Source, stimuli, method and measurements are unchanged. The dedicated list has 23 explicit signals: required outputs, supply current, full SOA node voltages and clocks, without unnecessary device OP saves. It produces 90,677 accepted steps and a 68,313,477-byte transient; no transport-cap recovery or simulation rerun was needed.

Primary TT d30=49.630304508151376 ps remains the official result. Tighter TT is 49.62271853885258 ps, a change of -0.007585969298794737 ps, leaving 0.3772814611474189 ps to the 50 ps limit. d1 changes +0.4495481351 ps, reported tau +0.3702800617 ps, reset -0.3052040883 ps, loser peak +0.0062703780 percentage points, and energy +1.0484538840 fJ. Maximum saved evaluation step falls from 20.9849 to 4.2075 ps. The tighter diagnostic supports this bounded timing check but does not establish wide margin or overwrite primary TT.

## Common-mode scope

Only the two input-source common-mode levels change to 0.40 and 0.56 V. Differential input sequence, clock, source, numerics and other conditions are unchanged; the script checks the input waveforms algebraically. Each endpoint runs the complete 36-cycle noise-off sequence at FS low voltage/125 C. Both are private operating-range diagnostics. The official FS result remains nominal VCM=0.49 V. Delay/CM jobs retain 107 explicit signals; full SOA coverage is retained in every job.

## Coverage and retained evidence

Fresh official A5 delay records now cover TT, SF, FS, SS and FF at the named representative corners, plus TT loading. The private tighter TT and CM results are reported separately. No full corner sweep, mismatch or noise result is claimed here. The candidate remains `wip`; physical noise is the next gated test, FS first and TT only if the FS noise estimate is at most 240 uV.

- Archive `ab233f27bf403ce0d3272ea10bfa6f00b7ef29ffe021677f8cefe404aa7725cf`: 47,923,044 bytes, 103 members; CRC and every member SHA-256 verified; exact owned remote directory absence confirmed.
- Archive `9ba8f615141b882fc57edda92bffb6032e5ad8b37cef5f91fdb658076bfd6bde`: 19,037,670 bytes, 79 members; CRC and every member SHA-256 verified; exact owned remote directory absence confirmed.
