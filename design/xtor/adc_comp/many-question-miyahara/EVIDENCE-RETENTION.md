# Evidence retention — 2026-10-31

The user requested removal of superseded waveform data after a disk-space incident. Historical raw/archive verification statements in earlier reports describe the original audit, not present availability. Sources, small failure reports, figures and numerical conclusions remain preserved. **Superseded raw archives were released and cannot be re-audited.** The following completed runs retain full archived evidence. The original twelve retained archives were fully rechecked by CRC, SHA-256 and byte length during cleanup; subsequent archives use the same verification protocol.

- `20261031-125734-f562-tb_comp_noise` — archive SHA-256 `eff1264f038ec86dbf56e337b531c2e22f627d5fc795ef21219e5a087f015d6d`.
- `20261031-131817-miyahara-buffer-v22-spec08-delay-baseline-screen` — archive SHA-256 `5f94e2debe4a8f549c57e17719cfd46eeb8936fbbb6f0c957640cb56059d4c6d`.
- `20261031-132625-miyahara-buffer-v22-spec08-delay-tighter-screen` — archive SHA-256 `a964a42812482b2f92e4d57f789d3e10c0c987b7d8b93ffa6cfdfb9c8980f1da`.
- `20261031-134338-miyahara-buffer-v22-spec08-noise-baseline-screen` — archive SHA-256 `26e302577d4bb1e1ba873aa319be231f6edc2458770a06bc2ab6fc7215845240`.
- `20261031-140219-miyahara-buffer-v22-spec08-noiseoff-input_pair-screen` — archive SHA-256 `2c8ee924b8d0ba57d92c7f1108d479d61e1f20d2673977d8571f0a454cd00db3`.
- `20261031-140219-miyahara-buffer-v22-spec08-noiseoff-regenerative_stage-screen` — archive SHA-256 `eba42669875cc48d8208cb70cefb6007a9292c316890846c52c2c9f8119b3b7a`.
- `20261031-142358-miyahara-buffer-v22-spec08-noiseoff-front_drivers-screen` — archive SHA-256 `9cd53a4ff662ba387361ea76f5c9997425dca79b08cc6cf5b37162891ca1bdfc`.
- `20261031-142358-miyahara-buffer-v22-spec08-noiseoff-latch_devices-screen` — archive SHA-256 `9ba91d5735c997491486182ed1f11e7e9af79052f97652dd5e3080a5c90448ca`.
- `20261031-151621-miyahara-buffer-v23-spec08-delay-baseline-screen` — archive SHA-256 `fa9c7f2c759ee3be53dd4ce7daf89cfcc4179781830004362fa4a6b6984b21aa`.
- `20261031-151635-miyahara-buffer-v23-spec08-kickback-baseline-screen` — archive SHA-256 `340e1463aa7f293ec8c20a0cf4816d56a674e52f96eb51384ec328a9c7e087e6`.
- `20261031-152741-miyahara-buffer-v24-spec08-delay-baseline-screen` — archive SHA-256 `2cd8f43a2829e19f19c91bc9cf7ab356afb08692e9dfe466c652dbd901e08c3e`.
- `20261031-152755-miyahara-buffer-v24-spec08-kickback-baseline-screen` — archive SHA-256 `755525d32f379a3891466cd6bfe5c08e5f3412ff9992c3258d5643dd1ba5ca7b`.
- `20261031-153955-miyahara-buffer-v25-spec08-delay-baseline-screen` — archive SHA-256 `be67008f1cb9c7d2bf5aee8d1cfa72fe3b964ca1c6dbd36e460d9fbdf26a8ad0`.
- `20261031-154013-miyahara-buffer-v25-spec08-kickback-baseline-screen` — archive SHA-256 `4d8c53ec7d1ef654934df795ba0a471deaae6bb0aa46a33f1cb6ceecd88a695d`.

Artificial noise-suppression trials remain ineligible for qualification. Retention does not establish compliance. Both canonical candidates retain genuine failed official 0.8 noise results. The full qualification remains incomplete.

Future owned runs explicitly select DUT/SOA and measurement signals. Continuous noise/MC traces remain disabled where the existing protocol uses monitor files. Wildcard/global waveform expansion is rejected. Stimuli, numerical tolerances, measurements and acceptance limits are preserved; shared qualification save-policy changes are coordinated separately in PR #111. Original runs are not relabeled as if they used the new wrapper.
