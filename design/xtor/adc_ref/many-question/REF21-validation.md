# Main28/gate16 formal validation

Status: **wip**. Base main: `fac0194179a4ae593438b022a0713d6e5b59663f`;
adc_ref specification 0.8.0. Notice #60 remains acknowledged. The open notice
and PR #31 comments/reviews were checked before source promotion; no new
reference interface, limit or bench condition was found.

## Source and preserved baseline

The promoted source exactly matches the frozen diagnostic proposal:
electrical hash `2b1163f0eb481376`, file SHA-256
`bc0d215942f18c1900825ab6398fb87017e8db365cd68005f957e8429c95443f`.
The electrical changes are MDRV multiplier 16 to 28, MSINK 4 to 7,
MCMH/MCML 8 to 14, and CGATE 8 to 16, with matching RNL annotations.
Ports, topology, other instance parameters and model names are unchanged.

The preceding source and all 136 records are preserved at
[604a61a](https://github.com/many-question/ADC-12b-100M/commit/604a61a144e54e7d6cfae2eaa162f202318c8ece),
tag `archive/adc-ref-ref21-baseline-604a61a`. That source has 91 fresh passes,
four fresh replay failures and 41 stale replay records. The changed circuit
invalidates all of them; old records are not rehashed into new acceptance.
Fresh results will replace individual current files while history and local
raw evidence retain their original provenance.

## Validation stages

At source promotion: **0 fresh / 136 stale**. New formal results are pending.
All simulations use the current official flow, APS and one job at a time,
with a clean committed source frozen through staging, simulation and fetch.
Uploaded inputs and fetched raw files are SHA-256 checked. Only owned remote
run directories are removed after retrieval and audit.

1. Four official replay pilots: TT nominal/27 C, SS low/125 C,
   FF high/125 C and FF low/-40 C; compare with the converged diagnostic.
2. If all four pass, complete 45 DC corners and TT noise, followed by
   45 startup corners with critical-corner cross-checks and all 45 replay corners.
3. Any clear new failure stops expansion for analysis. Full coverage is required
   before readiness; updated mixed-top verification remains a separate stage.

Private strict-step diagnostics retain their actual settings and are not
relabeled as official bench conditions. Public testbenches and tools are unchanged.

## Power cost before formal reruns

The following values are private DC measurements at the official 200 uA load;
they are preliminary characterization until replaced by committed-source runs.
The circuit draws from AVDD18; AVDD is unused. The reference specification has
no power limit, but lower power is preferred.

| Corner | AVDD18 (V) | AVDD (V) | Total supply power (mW) | Baseline (mW) | Increase |
|---|---:|---:|---:|---:|---:|
| tt_nom_27 | 1.80 | 0.90 | 47.04061 | 28.10870 | 67.35% |
| ss_low_125 | 1.62 | 0.81 | 29.70012 | 17.72542 | 67.56% |
| ff_high_m40 | 1.98 | 0.99 | 79.81969 | 47.76554 | 67.11% |

The full DC sweep will report supply-specific currents and extrema across all
45 corners. Lower-power optimization is deferred until this revision has a
complete, comparable validation baseline.
