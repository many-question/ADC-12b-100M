# A6 full FS physical-noise gate: FAIL

A6's one authorized FS/low/125 physical-noise job completed naturally with **325.0388413768936 uV rms**, exceeding CMP-13's **240 uV** limit. Its model-conditional 95% profile interval is **314.05764906285185–336.55596519873524 uV**. The statistical audit flags a Gaussian/binomial fit limitation, detailed below; the official estimate and FAIL are preserved without removing samples, changing the model used for qualification, or retrying.

Work is paused under [issue 124](https://github.com/many-question/ADC-12b-100M/issues/124). No TT noise, other noise corners, mismatch, new diagnostics or electrical variants follow this result. A6 remains `wip` and unqualified. [The historical noise-delay audit](HISTORICAL-NOISE-DELAY-AUDIT.md) presents the alternatives and auxiliary constraints for top-level decisions.

| Measurement | Result |
|---|---:|
| Full physical differential input-referred noise | 325.0388413768936 uV rms — FAIL |
| Model-conditional 95% profile CI | 314.05764906285185–336.55596519873524 uV |
| Signed systematic offset | -0.003407580757166038 mV |
| CMP-02 absolute offset, 2 mV limit | PASS |
| Samples | 8704 finite; 512 at each of 17 levels |
| Simulator return code / error count | 0 / 0 |
| Accepted transient steps | 2451799 |
| Spectre elapsed / CPU | 852 / 838 s |
| Wrapper elapsed | 855 s |

Increasing input levels are -800 through +800 uV in 100 uV steps. Exact positive-output counts are `[2, 7, 18, 43, 65, 106, 149, 183, 236, 307, 358, 413, 452, 490, 507, 507, 512]`, each out of 512. Sample indices are contiguous 1–8704, timestamps are monotonic and match the expected 400 ps sequence, and minimum sampled absolute differential output is 0.8060762998482 V. The sampler contains differential output only; it does not independently establish per-output CMP-15 or continuous SOA coverage. Those deterministic results retain their separate [A6 screen scope](A6-SCREEN.md). Systematic offset here is not mismatch Monte Carlo.

## Statistical audit and comparison limits

Independent Powell optimization in microvolt coordinates and an independent profile-likelihood interval reproduce the official fit within 0.000003 uV. This verifies numerical optimization, not the physical statistical assumptions.

Binomial deviance is **42.50490064179345** on 15 degrees of freedom, with approximate asymptotic **p = 0.00018786192986467625**; Pearson statistic is 36.13409820607994, and maximum absolute standardized residual is 2.8326127934419976. The S-curve residual pattern warrants a model-fit warning. Sparse extreme bins and any sample dependence also limit the asymptotic p value. The quoted CI assumes the Gaussian-CDF/binomial model and cannot be described as a validated unconditional physical-noise uncertainty bound.

Descriptive pooled correlations within each input level are lag1 **0.04269873956225544**, lag2 0.010281185775788813, lag4 0.0010598083305921495, lag8 0.007962253400849379 and lag16 -0.019268652839432028. These do not prove IID sampling. First/second within-level halves give 330.0944902938652 / 319.89325440025067 uV, with overlapping conditional intervals [314.50145557375726, 346.7827176834279] / [304.7242517540172, 336.11268336908563] uV. All official 512 samples per level are retained; the halves are descriptive and do not replace the official result.

A5 measured 341.8605253429254 uV on the matched full protocol, versus A6's 325.0388413768936 uV. This is a lower single-seed point estimate, **not a statistically established improvement**: the conditional intervals overlap, A6 has the model-fit warning above, and adaptive integration changes stochastic trajectories despite the same seed. It does not isolate second-pair noise or justify subtracting squared widths as a component-noise measurement. Both sources fail 240 uV.

## Exact source, protocol and evidence closure

Source commit at dispatch is `0e360b771b3e90912a711341289adf5d2cfb61c1`. Source SHA-256 is `8d300f399e0ff5b9f2273ba23c166ce6de63aa8218da1dd434ad4b2225d00621`; electrical SHA-256 is `fb35051d0ec3e345c550baddafc8e3ab43d9de7187453188e365cddca1544274`. Only MSIP/MSIN W4/nf4 to W6/nf6 differs electrically from A5, using the complete callback geometry documented in A6-SCREEN. No electrical edits occurred during this run.

The official and staged testbenches are byte-identical to the A5 parent; normalized decks, global parameters and 47 shared staged dependencies match. The main reference is `88654d672044eee754472d1c2c8a0dee2e76d81e`, comparator specification 0.9.0. Transistor view, physical device noise and seed 1 are enabled; no source masks or added ideal noise sources are present. Exactly one invocation ran, with APS and single-job concurrency; no explicit multithreading override was used.

Actual settings from the log: conservative, gear2only, reltol 1e-4, voltage/current abstol 1e-6 V / 1e-12 A, relref alllocal, lteratio 10, noisefmax 50 GHz, implicit noisefmin 287.216 kHz, stop/outputstart 3.4817 us, useprevic=no and skipdc=no. The default 34.817 ns maxstep is a ceiling; mean accepted step is about 1.42006 ps. The sampler-only explicit-save policy is identical to the matched parent. All seven simulator warnings and five notices remain in the original log; no errors occurred.

Run `20261101-113354-soa29-a6-noise-fs` retained and verified 57 staged/retrieved files against their remote SHA-256 values. The exact owned remote directory was then removed and its absence confirmed. Archive **`b84a8cc0c6286f39a1f23c8aaeab1be54808937907f7cf4d443fb65879d4d5ac`**, **234956 bytes / 67 members**, passed CRC and every-member SHA-256 readback. Original source, deck, TB, logs and every decision remain archived. Decision-file SHA-256 is `f9bf91bcb21789982bd468fbe24eb3d93d7de6fc6b740f9d1832a296797344bf`.

The original recorder refreshed only the FS noise result and its plot. Its displayed CI rounds to [314.06, 336.56] uV; the unrounded values above are retained from the original decisions. The previous A5 result was backed up before recording, and A5-NOISE.md remains unchanged. No old TT, other-corner noise or mismatch record qualifies A6.
