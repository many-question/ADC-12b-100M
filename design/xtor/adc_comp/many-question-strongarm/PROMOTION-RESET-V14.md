# Canonical promotion: RESET-V14

The private screened source is copied into the canonical `adc_comp.scs` with one header-comment change. Removing blank lines and full-line comments, stripping line-edge whitespace and joining the remaining electrical statements with newlines gives the same SHA-256 for both sources: `dd44da2a98a529e3f4dced4b72a1728101738d03a1bdc63d4042371206fa6455`. No device, terminal, geometry, parasitic or electrical statement changes during promotion.

| Evidence | SHA-256 / commit |
|---|---|
| Pre-promotion fixed commit | `4f7e762fdc2686dd909045bf5e8a6e1834fee599` |
| Screened TXT file | `f2df295b61f6cdd5ada28b2d92fff6b6ca6bca6d0f2f7a2c3b7140b04601451c` |
| New canonical file | `b2620013693aad9e815da425884cb41bbed0bc323099d16af6c8ac915a51474e` |
| Old canonical file | `b428bab815754af4e064aacad9b64347f3fdade4777279869b3106f8b7625f81` |
| Verified old-source/92-record archive | `c9fe9f194db712a18bf26597ac859299ab7974e4b81ade20b8bc36f83d9800b2` |

All old records and figures were preserved and every archived file read back with CRC and SHA verification before replacing the canonical source. Their original JSON metadata is untouched. They are stale for the promoted source until the existing official runner performs and records new simulations. Private screens remain supplemental and are not converted into formal records.

Known-key screening and the targeted numerical convergence check are documented in [RESET-V14.md](RESET-V14.md). Full qualification remains incomplete. Normal canonical promotion and formal verification are part of the authorized continuous design workflow.
