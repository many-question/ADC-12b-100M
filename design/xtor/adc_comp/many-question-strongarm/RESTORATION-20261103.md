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
