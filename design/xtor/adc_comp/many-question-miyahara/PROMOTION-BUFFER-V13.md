# Canonical promotion: BUFFER-V13

> Superseded raw was released. Historical audits do not imply availability; see [retained runs](EVIDENCE-RETENTION.md).

The private screened source is copied into the canonical `adc_comp.scs` with one header-comment change. Removing blank lines and full-line comments, stripping line-edge whitespace and joining the remaining electrical statements with newlines gives the same SHA-256 for both sources: `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`. No device, terminal, geometry, parasitic or electrical statement changes during promotion.

| Evidence | SHA-256 / commit |
|---|---|
| Pre-promotion fixed commit | `740fe564b380bc8e3b6526d8ac109503325935ad` |
| Screened TXT file | `59ae774790bf9c37a2e526dc863948530c3b6ecc604689c99067de2445621a88` |
| New canonical file | `0fa3574c587cd03eebc005988a9c1d67962fcc51ec0b76e4a7c7e5486598e6d3` |
| Old canonical file | `3d95f18933ab4993aed7406f6f4ceb2e9edf900995dfb7d104d0f388f6d71b31` |
| Verified old-source/92-record archive | `798ee34c692563385ac1f9ebedb4c055fa514e0437996a0dfcadf869d05f38a9` |

All old records and figures were preserved and every archived file read back with CRC and SHA verification before replacing the canonical source. Of the 92 records, 2 matched the immediate old canonical source and 90 already referred to older sources; the private preservation manifest retains those source-hash counts. Their original JSON metadata is untouched. All are stale for the promoted source until the existing official runner performs and records new simulations. Private screens remain supplemental and are not converted into formal records.

Known-key screening and the targeted numerical convergence check are documented in [BUFFER-V13.md](BUFFER-V13.md). Full qualification remains incomplete. Normal canonical promotion and formal verification are part of the authorized continuous design workflow.
