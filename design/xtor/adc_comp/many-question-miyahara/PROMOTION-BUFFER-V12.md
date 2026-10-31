# Canonical promotion: BUFFER-V12

> Evidence retention (2026-10-31): Superseded raw was released. Historical verification does not imply current availability; [retained evidence](EVIDENCE-RETENTION.md) determines which runs can be re-audited.

The private screened source is copied into the canonical `adc_comp.scs` with one header-comment change. Removing blank lines and full-line comments, stripping line-edge whitespace and joining the remaining electrical statements with newlines gives the same SHA-256 for both sources: `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. No device, terminal, geometry, parasitic or electrical statement changes during promotion.

| Evidence | SHA-256 / commit |
|---|---|
| Pre-promotion fixed commit | `efe4fe080ceaa9ba37f8bdfbf4a6b3eccae311ed` |
| Screened TXT file | `9b46556ec87e060059b73bb61bc9898dcb8c49fbabd7f5b983666d5646213c88` |
| New canonical file | `3d95f18933ab4993aed7406f6f4ceb2e9edf900995dfb7d104d0f388f6d71b31` |
| Old canonical file | `40cf3172acd0929ccd148080e36ca698bd3fdcc852413da339b6c2d7efc50a2e` |
| Verified old-source/92-record archive | `71c012c5551df665ac8d5ee8ef8ad957578b6a7cd6684f47e354de4e061934e5` |

All old records and figures were preserved and every archived file read back with CRC and SHA verification before replacing the canonical source. Their original JSON metadata is untouched. They are stale for the promoted source until the existing official runner performs and records new simulations. Private screens remain supplemental and are not converted into formal records.

Known-key screening and the targeted numerical convergence check are documented in [BUFFER-V12.md](BUFFER-V12.md). Full qualification remains incomplete. Normal canonical promotion and formal verification are part of the authorized continuous design workflow.
