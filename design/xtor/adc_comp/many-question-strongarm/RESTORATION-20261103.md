# l16 restoration under comparator 0.11.0

The current candidate is restored to the frozen l16t3c1 electrical baseline. Status remains WIP. Source freeze precedes all new simulations. Notices #131 (CMP-13 280 uV and CMP-08 45 ps) and #136 (official per-device CMP-17 SOA) are acknowledged; CMP-01 remains 200 uV and CMP-15 is unchanged.

## Source identity and historical evidence

- `L16-FROZEN.txt` preserves the original l16 simulation source, normalized UTF-8/LF SHA256 `4c1417fb771024fc1c4568a2d0a1329d7031567df7edeccf5b4a9c34afaef44f`.
- Canonical `adc_comp.scs` adds complete RNL records only. Its electrical SHA256 is `56e3dddc5148fa35041f391de76c820e9e15927221bfc58dc79bea4bc7744577`, matching the frozen source and the historical l16 evidence in [RESTORATION-SECONDARY](RESTORATION-SECONDARY.md).
- Historical full FS noise is 274.20498833482293 uV, with model-conditional 95% interval 264.5703918658524–284.28656376278826 uV. The interval crosses the new 280 uV limit. Historical TT 144.572627 uV is an old-numerics 17 x 64 pilot, not formal TT qualification.
- The canonical source replaced here is RESET-V27 at `cf7a3524aa3872b3fd6145826ff3430979f3b918` (file SHA256 `152e8704a66d79e392d651cde7a6b3329eeb10bc9b8d15154b9fa15553d885a3`). Its historical results and reports retain their actual source identities. They are not relabeled fresh for l16.
- Independent p56 is fixed at `5089a93549d84f5bf26207670343df6a6ceb544a`, source SHA256 `b428bab815754af4e064aacad9b64347f3fdade4777279869b3106f8b7625f81`, electrical SHA256 `0e9fac7cfb8de71896777a2bcd685cde9291ac0752fb97f21d028fb32ca83988`. Its FS screen will use an isolated stage with current official noise TB and complete deck, numerical settings and sample audit. It will not write l16 result paths.

## Required sequence

1. Formal l16 TT physical noise: official 17 levels x 512 decisions, APS, conservative, noise seed 1, 50 GHz bandwidth, all physical noise sources enabled.
2. Independent p56 FS physical noise under the same current numerical regime.
3. A promising baseline must pass short reset support tests (TT about 43 ps, fast 38 ps, slow 69 ps) and official device SOA. The old 200 ps low phase is insufficient evidence.
4. Expand full corners, mismatch, kickback and mixed-top only after the first round supports proceeding. New SOA must cover every required corner before eligibility; lead verification remains required.

New simulations are pending at this source-freeze checkpoint. No old result is rehashed or declared fresh. A6 and PR #123 remain historical alternatives with no new sizing work.
