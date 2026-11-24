# l16 restoration under comparator 0.11.0

The current candidate is restored to the frozen l16t3c1 electrical baseline. Status remains WIP. Source freeze precedes all new simulations. Notices #131 (CMP-13 280 uV and CMP-08 45 ps) and #136 (official per-device CMP-17 SOA) are acknowledged; CMP-01 remains 200 uV and CMP-15 is unchanged.

## Source identity and historical evidence

- `L16-FROZEN.txt` preserves the original l16 simulation source, normalized UTF-8/LF SHA256 `4c1417fb771024fc1c4568a2d0a1329d7031567df7edeccf5b4a9c34afaef44f`.
- Canonical `adc_comp.scs` adds complete RNL records only. Its electrical SHA256 is `56e3dddc5148fa35041f391de76c820e9e15927221bfc58dc79bea4bc7744577`, matching the frozen source and the historical l16 evidence in [RESTORATION-SECONDARY](RESTORATION-SECONDARY.md).
- Historical full FS noise is 274.20498833482293 uV, with model-conditional 95% interval 264.5703918658524–284.28656376278826 uV. The interval crosses the new 280 uV limit. Historical TT 144.572627 uV is an old-numerics 17 x 64 pilot, not formal TT qualification.
- The canonical source replaced here is RESET-V27 at `cf7a3524aa3872b3fd6145826ff3430979f3b918` (file SHA256 `152e8704a66d79e392d651cde7a6b3329eeb10bc9b8d15154b9fa15553d885a3`). Its historical results and reports retain their actual source identities. They are not relabeled fresh for l16.
- Independent p56 is fixed at `5089a93549d84f5bf26207670343df6a6ceb544a`, source SHA256 `b428bab815754af4e064aacad9b64347f3fdade4777279869b3106f8b7625f81`, historical electrical SHA256 (logical lines with trailing LF) `0e9fac7cfb8de71896777a2bcd685cde9291ac0752fb97f21d028fb32ca83988`; current adcflow normalization without trailing LF gives `150dd81755a64d66f582a84fd734462f5ad2c8b31ce4399b6507481d30372119`. Its FS screen will use an isolated stage with current official noise TB and complete deck, numerical settings and sample audit. It will not write l16 result paths.

## Required sequence

1. Formal l16 TT physical noise: official 17 levels x 512 decisions, APS, conservative, noise seed 1, 50 GHz bandwidth, all physical noise sources enabled.
2. Independent p56 FS physical noise under the same current numerical regime.
3. A promising baseline must pass short reset support tests (TT about 43 ps, fast 38 ps, slow 69 ps) and official device SOA. The old 200 ps low phase is insufficient evidence.
4. Expand full corners, mismatch, kickback and mixed-top only after the first round supports proceeding. New SOA must cover every required corner before eligibility; lead verification remains required.

At the source-freeze checkpoint new simulations were pending. The first formal result is recorded below. No old result is rehashed or declared fresh. A6 and PR #123 remain historical alternatives with no new sizing work.

## Formal l16 TT noise: pass

Source commit `19ae157ffc901a3b576981164c5de99e070f7581` was clean when measured. Canonical full source SHA256 is `8104b210e324bc4d870d4a582d6ba16e7bccb69581502c5b10194ced497d46f4`; electrical identity is unchanged.

The official current test returns **175.29518977435197 uV rms**, 95% profile interval **167.73–183.26 uV**, offset -0.003520208546265018 mV. CMP-01, CMP-13 and CMP-02 pass at TT. All 8,704 decision rows are finite, exactly 512 at each of 17 levels. Actual log settings: APS, conservative, gear2only, reltol 1e-4, voltage abstol 1e-6 V, 50 GHz physical noise and seed 1; no numerical overrides. The 1,825,119 accepted steps average 1.90766 ps. Simulator return code is 0; simulator time 388 s, official wrapper 474.7 s.

The original formal JSON and noise figure are in the candidate's official result path. The fetched stage and outputs match remote SHA256; archive CRC and each member SHA256 are verified. Archive `20261103-021407-4984-tb_comp_noise` SHA256 `cc41241f39650a891f8abc5fccbbcd53cf96c36dac668175f1f10682123ec648`. Remote absence is confirmed after verified retention.

Validation at this checkpoint: `adcflow check all` passes (96 existing stale/failing historical warnings); 507 non-slow tests pass, 1 deselected. Required CI contracts/drawings/results and slow budget jobs pass. Short-reset and official SOA are the next gates; one TT pass does not establish readiness or all-corner qualification.

## p56 FS screen: fail; expansion stopped

The independent source at `5089a93549d84f5bf26207670343df6a6ceb544a` returns **297.73131716270746 uV rms** at FS/low/125, with 95% profile interval **287.58–308.36 uV**, above 280 uV. Offset is +0.008206734022012252 mV. All 8,704 rows are finite with 512 decisions at each level. The actual official TB and complete deck were frozen in the independent stage; APS/conservative gear2only, reltol 1e-4, voltage abstol 1e-6 V, seed 1, 50 GHz, all physical noise enabled. Solver return code 0, 460 s. No p56 result is written into l16 result paths. No further p56 corners are launched.

Archive `20261103-021638-p56-fs-noise` SHA256 `80ed1577fec828d4f211a229c42683a6c3267f9e31e74963b0495d8d842c7615`: remote file hashes, CRC and all member hashes verified; remote absence confirmed.

## l16 short reset support: pass

The private support TB retains the official differential amplitude sequence, 10 fF outputs, 10 ps clock edges, 200 ps high phase (50% crossings), physical source and conservative numerics. It changes the period to 200 ps plus the required low window; each 10 ps input transition ends 10 ps before the next clock rising ramp. Metrics below are supporting evidence, not substituted official records.

| Corner | Low window (ps) | Correct decisions / completed resets | Max reset (ps) | Mean delay 1mV / 30mV (ps) | CMP-15 violations |
|---|---:|---:|---:|---:|---:|
| TT/nom/27 | 43 | 36 / 36 | 22.2498503461 | 60.8316055492 / 46.9327366502 | 0 |
| FF/high/-40 | 38 | 36 / 36 | 17.2700689332 | 47.0264240095 / 36.3448641786 | 0 |
| SS/low/125 | 69 | 36 / 36 | 29.1216801215 | 78.4467481117 / 60.2089009705 | 0 |

Every polarity, including 10 uV, is correct. Every reset completes before the next evaluation; the last cycle is checked to the simulation end, 5 ps before its hypothetical next 50% rising crossing. Worst residual at that boundary is 0.0102883%, 0.00407049%, 0.0563123% VDD respectively. Worst loser peaks are 15.4799%, 17.1376%, 14.6631% VDD. The complete per-cycle audit, actual deck and waveforms are retained. Archive `20261103-022331-l16-short-reset` SHA256 `fec076e6ad964d4e198dee6d196d5b97ab7c283ebce88908ec5c25a56ff72c0f`: remote hashes, CRC/member hashes and remote absence confirmed.

## Initial official device SOA: five corners pass

Official `tb_comp_soa` at source checkpoint `09f2c3c2` checks 19 MOS devices / 57 terminal pairs per corner, including startup, full differential range and the 40 ps low phase. TT, FF/high/-40, SS/low/125, FS/low/125 and SF/high/-40 all return zero CMP-17 violations. Peak absolute terminal voltages are respectively 0.99288, 1.09130, 0.88563, 0.88879 and 1.09578 V; all have zero accumulated time above 1.1 V. Device scope is verified, not external scope. Formal JSON, SOA figures and stimulus figures are committed. Remote reduction uses the official code.

The initial gates support proceeding with l16. Next: representative worst-corner SOA numerical cross-check, remaining official corners, full noise coverage, mismatch and kickback. All-corner eligibility and mixed-top acceptance remain unproven; status remains WIP.

## SF SOA numerical cross-check and TT mismatch: pass

The official `--crosscheck` at SF/high/-40 reports zero violations in both baseline and tighter runs across all 57 terminal pairs. Maximum pair-peak difference is 1.08 mV at MRQP gd. Requested tighter settings are reltol 1e-7, voltage abstol 1e-8 V, maxstep 1 ps, traponly; the actual log reports reltol 1e-8, voltage abstol 1e-8 V, maxstep 1 ps, traponly, conservative. Both actual settings and the comparison are retained in the formal result. The initial five-corner SOA archive is `6069b065bba6b7cc7804fcf2de3bef4895e06eeb1df9427073abebba1e063bb1`, with all hashes verified and remote absence confirmed.

Official TT mismatch, seed 6303 and local device mismatch models: **50/50 valid samples, 0 failed**, offset sigma **1.8944132218595715 mV** (limit 5 mV), mean -0.58740234376534 mV. No missing or invalid sample is discarded. This passes CMP-03. Cross-check and mismatch source checkpoint is `fe227b0b`, electrically identical to the frozen l16 source. Archive audits for these two new runs are in progress at this checkpoint.

## Formal critical noise and all-corner SOA

Official FS/low/125 noise is **274.20498833482293 uV**, 95% profile interval **264.57–284.29 uV**; SS/low/125 is **240.27886128164582 uV**, interval **231.37–249.60 uV**. Each has all 17 x 512 decisions. Both satisfy CMP-13 by its specified point-estimate rule. The FS value reproduces the historical frozen-source result exactly; its interval still crosses 280 uV, so the limited noise margin remains explicit. These are now genuine current formal records, not rehashed historical records.

Official SOA now covers **45/45 required corners**: every corner has device scope, 19 MOS, 57 terminal pairs, zero violations and zero accumulated time above 1.1 V. The new worst peak is 1.09961 V at SS/high/-40. This corner receives a separate numerical cross-check before final acceptance. The original SF cross-check remains retained. Full coverage is candidate evidence, not lead verification.

Official TT kickback/loading also passes: net differential kickback 0.0001097096001285297 uV, input capacitance 19.311701639827493 fF and CLKC capacitance 7.256641126623195 fF. These are the official metrics; the net end-of-cycle kickback is not the maximum instantaneous switching disturbance. Remaining all-corner noise, delay and kickback are next. Archive receipts for the newly completed batches are pending at this checkpoint.

## New worst-corner cross-check and completed archive receipts

SS/high/-40 also passes the official numerical cross-check: 57 terminal pairs, zero violations in both runs, maximum pair-peak change 1.62 mV at MRQP gd. The tighter run's overall peak is 1.09890 V and accumulated time above 1.1 V remains zero. The effective tighter settings are conservative, traponly, maxstep 1 ps, reltol 1e-8 and voltage abstol 1e-8 V, as retained in the formal JSON.

The following formerly pending archive audits are complete. Every archive has verified remote file SHA256, ZIP CRC and member SHA256, and confirmed remote absence after retention.

| Run | Archive SHA256 |
|---|---|
| SF SOA cross-check, 023203-b4e3 | `24b2be81553511d4c8d7b107d965d2a43e68cf05a2b4152d24543d5a9f700cc3` |
| TT mismatch, 023250-5bfc | `56662ff7c63580d9c364c47f3b8057d634204c481cf684269adc2ca02f9e5c4c` |
| FS/SS formal noise, 023203-ab18 | `3e14eab9fd39641d49454961a6304c9970a9730f396b27b568979e22f0d7793b` |
| Remaining 40 SOA corners, 023737-0f15 | `681d7819d868f3fb4cfef9ebc7c389466cf79ee69f11cbc6e24fa8f16a2313e4` |
| TT kickback/loading, 024452-e2b1 | `8b86dfb816267102a818de30eca68a3f30fd6db8f111e9c2a42352cc4b9c5e8b` |
| SS SOA cross-check, 025153-4ebc | `459c885f2499ac530c27d8cc0797bba542ea012b469c07518bcd957b31ca1e84` |

All run IDs above have date prefix 20261103. The earlier archive receipts in this report remain retained. The ongoing 42-corner noise and full delay/kickback runs use unchanged l16 electrical content, frozen at `d0474920`; they do not imply a pass before measurement completes.

## Formal delay: 45/45 corners pass

All required delay, regeneration, reset, decision and output-validity specifications pass at all 45 corners. A separate audit of every fetched waveform confirms **1,620 correct decisions and 1,620 completed resets**, including the 10 uV decisions; no missing cycle is dropped. Maximum output residue at the next evaluation boundary is 0.402298% VDD.

- Worst 1 mV delay: 101.05730969653212 ps at SS/low/-40 (limit 120 ps).
- Worst reset: 29.29568722477588 ps at SS/low/27 (limit 45 ps).
- Worst regeneration constant: 6.243990715687595 ps at SS/low/-40 (limit 15 ps).
- Worst losing-output peak: 22.77930509765373% VDD at SF/low/-40; all CMP-15 counts are zero.
- TT 1 mV / 30 mV delay: 61.56277345045652 / 47.71403968897317 ps (limits 80 / 50 ps). TT mixed-amplitude AVDD energy: 203.492731932 fJ, reported only.

All results use the unchanged frozen l16 electrical source; current official JSON and figures replace stale historical records without rehashing them. The per-cycle audit is retained with run `20261103-025502-a01b-tb_comp_delay`; archive SHA256 `809e71c76842c1061eb35fb48e24168082307d34891bd4a196aef1947d48896b` has remote hashes, CRC/member hashes and remote absence verified. Remaining all-corner noise and kickback are still running. No mixed-top or lead-verification claim is made.

## Blocking FF noise: completed-job checkpoint

The ongoing 42-corner batch `20261103-025105-8754-tb_comp_noise`, frozen at `d0474920`, exposes a failure at **FF/low/125: 284.57485867742884 uV > 280 uV**, 95% interval **274.72–294.90 uV**. Every one of the 17 levels has 512 finite decisions (8,704 total). Decisions SHA256 is `66d2d231381e1cbb006c4d89a1c10830d2252d7762d8eae1e48cd85b580b203c`. Source, staged deck, testbench and downloaded raw hashes match remote files. The official noise measurement is applied without changing defaults: conservative, gear2only, reltol 1e-4 and voltage abstol 1e-6 V. A confidence interval crossing the limit does not turn the failed point estimate into a pass.

This is a private read-only check of completed jobs; the official runner writes formal records after the entire batch completes. Eleven of the 42 jobs have been audited at this checkpoint. The current batch continues to retain full coverage and failures; source, seeds and numerical settings remain unchanged. TT mixed-top expansion is deferred, and l16 remains WIP and unqualified.

## Formal kickback: 45/45 corners pass

All 45 current official kickback records pass CMP-11. Worst net end-of-cycle differential change is 0.0002549126998895035 uV at SS/high/-40; this metric does not bound the instantaneous switching disturbance. TT input/clock capacitances remain 19.311701639827493 / 7.256641126623195 fF, passing CMP-12/14 (TT requirements). Across all corners the reported capacitance ranges are 17.13844089190766–20.677410206499047 fF at the input and 6.449975150518292–7.89160981293955 fF at CLKC. All newly measured records have clean source metadata at bb016f17 and unchanged l16 electrical identity.

Archive 20261103-030948-2dfc-tb_comp_kickback SHA256 `1e6f787297c1fe95101a03ede90faf8ff394d17d1bb55801f5da414f6a450567` has verified remote file hashes, ZIP CRC/member hashes, retained local copy and confirmed remote absence. Full-corner noise remains in progress with the FF/low/125 failure above; mixed-top remains deferred.

## Final formal noise coverage: 44/45 pass, one blocker

The official 42-corner batch has completed and written its formal records at clean checkpoint `2321d8a2`. Together with the earlier TT and FS/SS runs, all **45 corners / 391,680 decisions** are present: 17 levels x 512 finite decisions at every corner. All three staged source files match canonical SHA256 `8104b210e324bc4d870d4a582d6ba16e7bccb69581502c5b10194ced497d46f4`. Every completed-job probe exactly matches its eventual formal metric and decisions hash. All simulations return zero and all formal dependency records are fresh.

**CMP-13 fails only at FF/low/125: 284.57485867742884 uV**, 4.57485867742884 uV (1.63388%) above 280 uV. Its interval remains 274.72–294.90 uV. TT CMP-01 passes at 175.29518977435197 uV; CMP-02 passes everywhere. This supersedes the provisional completed-job checkpoint above.

| Process | Worst corner | Noise (uV) | 95% interval (uV) | CMP-13 |
|---|---|---:|---:|---|
| TT | low/125 | 264.301338 | 254.89–274.15 | pass |
| FF | low/125 | 284.574859 | 274.72–294.90 | **fail** |
| SS | low/125 | 240.278861 | 231.37–249.60 | pass |
| FS | low/125 | 274.204988 | 264.57–284.29 | pass |
| SF | low/125 | 250.596356 | 241.48–260.13 | pass |

Across all five unit tests, all 181 formal records are fresh with zero execution/measurement errors. Delay, SOA, kickback and mismatch pass their applicable requirements; FF noise is the sole specification failure. No seed selection, numerical override or source change was used to remove it. Mixed-top expansion and lead verification are not started for this failed baseline. The candidate remains WIP, unqualified and unselected; the complete distribution is retained for the next design decision.

The final 42-corner noise archive `20261103-025105-8754-tb_comp_noise` SHA256 is `ef9e64b3e9002aa5c9fdd58d26d54395a46af1393a2630895d1cdc9e972e9e8e`. It includes the full 45-corner sample audit and completed-job comparison. Remote file hashes, ZIP CRC/member hashes, retained-copy hashes and remote absence are verified. All 13 restoration-run archives are retained locally. No comparator simulation remains active at this checkpoint.

Final local `check all` passes with the known CMP-13 failure and three unrelated SAR-logic SOA failures reported as warnings. RNL and candidate-content checks pass; the unchanged-source non-slow suite remains 507 passed / 1 deselected. These tooling checks do not override the failed circuit requirement.
