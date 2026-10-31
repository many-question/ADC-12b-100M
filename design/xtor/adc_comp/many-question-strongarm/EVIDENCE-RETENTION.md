# Evidence retention — 2026-10-31

The user requested removal of superseded waveform data after a disk-space incident. Historical raw/archive verification statements in earlier reports describe the original audit, not present availability. Sources, small failure reports, figures and numerical conclusions remain preserved. **Superseded raw archives were released and cannot be re-audited.** The following runs retain verified archived evidence, including failures and partial traces from errored runs. Archival does not turn a failed run into a completed gate. The original twelve retained archives were fully rechecked by CRC, SHA-256 and byte length during cleanup; subsequent archives use the same verification protocol.

- `20261031-125724-e0ac-tb_comp_noise` — archive SHA-256 `19b0deda49f6e53d8eafe8bf1253318697550b4cf1a6f1d88b9b04ecd8c14277`.
- `20261031-131451-strongarm-reset-v28-spec08-noise-baseline-screen` — archive SHA-256 `54ff6269212616fd41dc09b383f106a78132651e58a2dbbb69c8717e6c296b92`.
- `20261031-133339-strongarm-reset-v28-spec08-noiseoff-input_pair-screen` — archive SHA-256 `035d439a1c6bc6c9cb3a1bb1996b02cb3f914247ef7e95b8f0803a61f20f0f82`.
- `20261031-133342-strongarm-reset-v28-spec08-noiseoff-q_shunts-screen` — archive SHA-256 `a56de68b166db74a927671dd5ef6261a42d99c9bbfc9c59994ccf430ff15d8ec`.
- `20261031-142506-strongarm-reset-v31-spec08-delay-baseline-screen` — archive SHA-256 `16675cf85040eef16b2f1408798ec477e25d271b376798f0cc202b1f35485e36`.
- `20261031-142603-strongarm-reset-v31-spec08-kickback-baseline-screen` — archive SHA-256 `de2075791bc9a9be8109c4cb4db32f66c4f9c90fc6a3779ea0e10a1d04b9bd0e`.
- `20261031-150826-strongarm-reset-v32-spec08-delay-baseline-screen` — archive SHA-256 `23ee62d872be40a886206f848c96f2c53e80a9a728ff60bdfabd9b33daafef6c`.
- `20261031-150826-strongarm-reset-v32-spec08-kickback-baseline-screen` — archive SHA-256 `119356f766a5c8d477f1f64477319260ee36483383bd69ca869c7bebccae5d56`.
- `20261031-151652-strongarm-reset-v32-spec08-delay-tighter-screen` — archive SHA-256 `4bff292951732887e803079a71fd3dfb81ef1ce1fc3a8bb64c98865579695f34`.
- `20261031-151715-strongarm-reset-v32-spec08-noise-baseline-screen` — archive SHA-256 `62d74c2b9aef0cd0b6cc1808caeab81d0cfb551390bb10bdd1917177aee24988`.
- `20261031-153022-strongarm-reset-v32-spec08-delay-baseline-screen` — archive SHA-256 `36976bd7ac9f7e3cb626bb470b288578e35202692865f81dd7f4ce0cef264e31`.
- `20261031-153036-strongarm-reset-v32-spec08-noise-tighter-screen` — archive SHA-256 `68b379d689a8eb810ffcb1341375a60afc3bbae44ea761e9f9130cb58a89fe1c`.
- `20261031-153652-strongarm-reset-v32-spec08-noise-baseline-screen` — archive SHA-256 `b6aca8e051c7a481eb59604c06c987bc6518d64c090e0ac73ddfcfbe9dad91e0`.
- `20261031-155740-strongarm-reset-v32-spec08-noiseoff-input_pair-screen` — archive SHA-256 `05b5044e82b47ab655a53877a0441ec24641b7606076d1f808a2254426de94f4`.
- `20261031-155750-strongarm-reset-v32-spec08-noiseoff-q_shunts-screen` — archive SHA-256 `af2285073d6bc33d99eebcdd7d0e1ad760405a80d89c2f7f4acd19ae60baf5aa`.
- `20261031-161219-strongarm-reset-v32-spec08-noiseoff-regenerative_stage-screen` — archive SHA-256 `9bbd31d6641b33c9dbe7062887ec2b454ef3a8a6b2d829c1aa31c01acbb5c77f`.
- `20261031-162854-strongarm-reset-v33-spec08-delay-baseline-screen` — archive SHA-256 `f6841cb22529eb80b7aa356500442964175076e59ef893b3416d3586ad6608f3`.
- `20261031-162854-strongarm-reset-v33-spec08-kickback-baseline-screen` — archive SHA-256 `5eeb930f26b032d56e04e497a6991757048d537366b8b6776b6d12bb178a1124`.

Artificial noise-suppression trials remain ineligible for qualification. Retention does not establish compliance. Both canonical candidates retain genuine failed official 0.8 noise results. The full qualification remains incomplete.

Future owned runs explicitly select DUT/SOA and measurement signals. Continuous noise/MC traces remain disabled where the existing protocol uses monitor files. Wildcard/global waveform expansion is rejected. Stimuli, numerical tolerances, measurements and acceptance limits are preserved; shared qualification save-policy changes are coordinated separately in PR #111. Original runs are not relabeled as if they used the new wrapper.
