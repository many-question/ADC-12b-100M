# Canonical promotion: BUFFER-V20

The private screened source is copied into the canonical `adc_comp.scs` with one header-comment change. Removing blank lines and full-line comments, stripping line-edge whitespace and joining the remaining electrical statements with newlines gives the same SHA-256 for both sources: `53b627cde3353cbe6176adc85391ea2ccb4b51dd81d63849c0ad6c56a5aa895f`. No device, terminal, geometry, parasitic or electrical statement changes during promotion.

| Evidence | SHA-256 / commit |
|---|---|
| Pre-promotion fixed commit | `5a9405c5ff48d3493c7098a7987ff7c56f7df001` |
| Screened TXT file | `24fd9165c0a45b9120f2e929fbd2221e0b5a2dd8dee88cad246689748247825d` |
| New canonical file | `f9bb6817b8062cf37d5b37695f0085f04458c2b119551605d954114d014ddab6` |
| Old canonical file | `0fa3574c587cd03eebc005988a9c1d67962fcc51ec0b76e4a7c7e5486598e6d3` |
| Verified old-source/96-record archive | `8c83962a1e8dfbe935cdaa4b7aabd7d38e45927f9d9d0a645c839e157911b0e8` |

All old records and figures were preserved and every archived file read back with CRC and SHA verification before replacing the canonical source. Of the 96 records, 6 matched the immediate old canonical source and 90 already referred to older sources; the private preservation manifest retains those source-hash counts. Their original JSON metadata is untouched. All are stale for the promoted source until the existing official runner performs and records new simulations. Private screens remain supplemental and are not converted into formal records.

Known-key screening and the targeted numerical convergence check are documented in [BUFFER-V20.md](BUFFER-V20.md). Full qualification remains incomplete. Normal canonical promotion and formal verification are part of the authorized continuous design workflow.
