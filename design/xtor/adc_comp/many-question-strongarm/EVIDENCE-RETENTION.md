# Evidence retention — 2026-10-31

The user requested removal of superseded waveform data after a disk-space incident. Historical raw/archive verification statements in earlier reports describe the original audit, not present availability. Sources, small failure reports, figures and numerical conclusions remain preserved. **Superseded raw archives were released and cannot be re-audited.** The following completed runs retain full archived evidence. The original twelve retained archives were fully rechecked by CRC, SHA-256 and byte length during cleanup; subsequent archives use the same verification protocol.

- `20261031-125724-e0ac-tb_comp_noise` — archive SHA-256 `19b0deda49f6e53d8eafe8bf1253318697550b4cf1a6f1d88b9b04ecd8c14277`.
- `20261031-131451-strongarm-reset-v28-spec08-noise-baseline-screen` — archive SHA-256 `54ff6269212616fd41dc09b383f106a78132651e58a2dbbb69c8717e6c296b92`.
- `20261031-133339-strongarm-reset-v28-spec08-noiseoff-input_pair-screen` — archive SHA-256 `035d439a1c6bc6c9cb3a1bb1996b02cb3f914247ef7e95b8f0803a61f20f0f82`.
- `20261031-133342-strongarm-reset-v28-spec08-noiseoff-q_shunts-screen` — archive SHA-256 `a56de68b166db74a927671dd5ef6261a42d99c9bbfc9c59994ccf430ff15d8ec`.
- `20261031-142506-strongarm-reset-v31-spec08-delay-baseline-screen` — archive SHA-256 `16675cf85040eef16b2f1408798ec477e25d271b376798f0cc202b1f35485e36`.
- `20261031-142603-strongarm-reset-v31-spec08-kickback-baseline-screen` — archive SHA-256 `de2075791bc9a9be8109c4cb4db32f66c4f9c90fc6a3779ea0e10a1d04b9bd0e`.

Artificial noise-suppression trials remain ineligible for qualification. Retention does not establish compliance. Both canonical candidates retain genuine failed official 0.8 noise results. The full qualification remains incomplete.

Future owned runs explicitly select DUT/SOA and measurement signals. Continuous noise/MC traces remain disabled where the existing protocol uses monitor files. Wildcard/global waveform expansion is rejected. Stimuli, numerical tolerances, measurements and acceptance limits are preserved; shared qualification save-policy changes are coordinated separately in PR #111. Original runs are not relabeled as if they used the new wrapper.
