# Canonical promotion: RESET-V19

The private screened source is copied into the canonical `adc_comp.scs` with one header-comment change. Removing blank lines and full-line comments, stripping line-edge whitespace and joining the remaining electrical statements with newlines gives the same SHA-256 for both sources: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. No device, terminal, geometry, parasitic or electrical statement changes during promotion.

| Evidence | SHA-256 / commit |
|---|---|
| Pre-promotion fixed commit | `8c0d2666ccb0e135e5799e3c2390bbd4db3dfe12` |
| Screened TXT file | `2f257518bc1b5e6cea5662f0c1eab52926e52c76054d5931511b18458ddbdfde` |
| New canonical file | `3a3221a95784b04c046f19c37e35431ee9ff13d30d7342871c2598420bf422f4` |
| Old canonical file | `b2620013693aad9e815da425884cb41bbed0bc323099d16af6c8ac915a51474e` |
| Verified old-source/92-record archive | `8eef8c4430fe17b8d59dc3fab677ca34e519ff8b19951c7c26daa35ab13e5ae7` |

All old records and figures were preserved and every archived file read back with CRC and SHA verification before replacing the canonical source. Of the 92 records, 2 matched the immediate old canonical source and 90 already referred to older sources; the private preservation manifest retains those source-hash counts. Their original JSON metadata is untouched. All are stale for the promoted source until the existing official runner performs and records new simulations. Private screens remain supplemental and are not converted into formal records.

Known-key screening and the targeted numerical convergence check are documented in [RESET-V19.md](RESET-V19.md). Full qualification remains incomplete. Normal canonical promotion and formal verification are part of the authorized continuous design workflow.
