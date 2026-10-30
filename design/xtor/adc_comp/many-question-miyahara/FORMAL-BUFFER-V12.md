# Official new-source validation: BUFFER-V12

The canonical electrical SHA-256 is `e64f215d6bd941a8c48d56a5cf4582d6459c4a31981ff85973a2e4915d96bc65`. These results come from actual new simulations through the existing official runner and recorder. Private screening remains supplemental.

## TT capacitance and kickback

Actual clean source commit: `7e6d4dede3c74ef0554fe425fe16148f8a8230df`. Run: `20261031-055648-7ca5-tb_comp_kickback`. The canonical view, official testbench, numerical settings, measurements and recording are unchanged. The private wrapper adds resource accounting, evidence verification and owned-run cleanup only.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Differential kickback | 0.002025736 uV | 40 uV | pass |
| Input capacitance per input | 19.328731219 fF | 20 fF | pass |
| CLKC capacitance | 9.609324821 fF | 16 fF | pass |

The genuine [TT kickback JSON](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-miyahara/tt_nom_27.json) records `git_clean=true`, mode `aps`, and source electrical hash prefix `e64f215d6bd941a8`. Numerics remain reltol 0.001, traponly, configured maxstep 66 ps; largest accepted step is 50.5 ps. This official capacitance test is separate from the mixed-delay clock-charge diagnostic.

One job used +aps, no explicit +mt and effective single-thread execution. All fetched raw/deck hashes match, and the owned remote run is removed with absence confirmed. Verified archive SHA-256: `b4d31c289c9e1eb95a19722428d716a6d192cef31592654599c0053fe05ade90`. The archive contains a byte-exact snapshot of the genuine JSON and figures.

## TT transient noise: failed gate

Actual clean source commit: `701c79c85148d11a29018eb8442ada2699330acd`. Official run: `20261031-060215-b7b5-tb_comp_noise`. The original 17 levels, 512 decisions per level, 50 GHz upper noise frequency, seed 1, sampler, numerical settings and measurement are unchanged.

| Metric | Measured | Limit | Result |
|---|---:|---:|---|
| Input-referred noise | 201.879919 uV rms | 200 uV at TT | fail |
| Noise 95% profile-likelihood interval | 193.82 to 210.34 uV | — | reported |
| Absolute systematic offset | 0.005300 mV | 2 mV | pass |

The genuine [TT noise JSON](../../../../results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/tt_nom_27.json) retains the strict failure. The confidence interval crossing 200 uV does not change the specified point-estimate verdict. All 8,704 samples are present, exactly 512 per level; minimum sampled output-difference magnitude is 0.873724 V and the largest standardized Gaussian-fit residual is 2.13. The curve has the expected monotonic transition. The original test saves the analog trace only at the end, so this run does not establish full reset or noise-transient SOA coverage.

The old canonical TT noise was 193.758465 uV with interval 185.84 to 202.07 uV. The intervals overlap; the observed 8.121454 uV difference cannot by itself be assigned to a particular repair device or interpreted as a precise degradation. B12 still lacks required TT noise margin, and its expensive qualification expansion stops. A physically justified circuit revision will be evaluated; the seed and sample count will not be changed to seek a pass.

The run uses +aps, no explicit +mt and effective single-thread execution. All fetched raw/deck hashes match, and the exact owned remote directory is removed with absence confirmed. Verified archive SHA-256: `36caa4fcf4b1536c382aac53071c131b41d68222914bdacbe1f9d118a94b8aa6`, including actual recorded JSON/figure and the independent sample-count/curve audit.

Two official cases are fresh for B12; 90 old-source records remain stale. Remaining-corner stress, full official coverage, mismatch and mixed-top qualification remain open. No old-source performance is inherited.
