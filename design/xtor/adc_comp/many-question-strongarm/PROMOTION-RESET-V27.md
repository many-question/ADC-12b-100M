# Canonical promotion: RESET-V27

This source-preserving promotion uses old-settings screening evidence. [Issue #94 transition](NUMERICS-94.md) now governs subsequent checks; promotion does not establish new-settings qualification.

The private screened source is copied into the canonical `adc_comp.scs` with one header-comment change. Removing blank lines and full-line comments, stripping line-edge whitespace and joining the remaining electrical statements with newlines gives the same SHA-256 for both sources: `7b20b19a2434da94d732f9785a3a8f1a2138d17ed4f4854dbdc5ab1a6cff18df`. No device, terminal, geometry, parasitic or electrical statement changes during promotion.

| Evidence | SHA-256 / commit |
|---|---|
| Pre-promotion fixed commit | `05d4d445c50471c0627d9b41f41b238bb8cfc1d9` |
| Screened TXT file | `0e39095961f9f50612bc6235b8292f1bb1d3030c11f73a4c442875dd6a7e9d60` |
| New canonical file | `c6fb6c893ad2a856e04b2d32dd24c6f8829bd9becdff043b729580d73ca71ac0` |
| Old canonical file | `3a3221a95784b04c046f19c37e35431ee9ff13d30d7342871c2598420bf422f4` |
| Verified old-source/92-record archive | `05c020cce44a497b63eecb9513c048f2f7173e335780166271f9ab06429cbfed` |

All old records and figures were preserved and every archived file read back with CRC and SHA verification before replacing the canonical source. Of the 92 records, 2 matched the immediate old canonical source and 90 already referred to older sources; the private preservation manifest retains those source-hash counts. Their original JSON metadata is untouched. All are stale for the promoted source until the existing official runner performs and records new simulations. Private screens remain supplemental and are not converted into formal records.

Known-key screening and the targeted numerical convergence check are documented in [RESET-V27.md](RESET-V27.md). Full qualification remains incomplete. Normal canonical promotion and formal verification are part of the authorized continuous design workflow.
