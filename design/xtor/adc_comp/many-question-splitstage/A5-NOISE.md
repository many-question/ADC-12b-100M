# A5 full FS physical-noise gate: FAIL

After the initial TT/SF delay and TT loading screen and the six subsequent gates passed, one full FS low-voltage/125 C noise test was run on unchanged A5. Input-referred noise is **341.8605253429254 uV rms**, exceeding the CMP-13 limit of 240 uV. The 95% profile-likelihood interval is **330.4249508199212–353.8682080578653 uV**. The failure is not marginal relative to sampling uncertainty. TT noise was not dispatched; no additional corner, seed, mismatch or electrical revision followed this result.

| Item | Result |
|---|---:|
| Noise, differential input-referred rms | 341.8605253429254 uV |
| 95% profile-likelihood interval | 330.4249508199212–353.8682080578653 uV |
| CMP-13 limit | 240 uV — **FAIL** |
| Systematic offset | -0.00145687399222376 mV |
| CMP-02 absolute-offset limit | 2 mV — pass |
| Input levels | 17, from -800 to +800 uV in 100 uV steps |
| Samples per level | 512 at every level |
| Total finite samples | 8,704 |
| Simulator return code | 0 |

The OUTP counts, in increasing input order, are `[6, 9, 25, 46, 70, 102, 147, 189, 231, 302, 359, 413, 446, 483, 503, 504, 510]`. The official binomial maximum-likelihood probit fit was independently checked from these counts. No samples were removed or selectively refitted. This is a transient-noise systematic-offset measurement, not a device-mismatch Monte Carlo result.

The source SHA-256 remains `2de4dd1c4da47a28a4449dbac1ee532f70012475528bd4d55f5a5b71108f14bb`; the electrical SHA-256 is `632931d6f052a6b87efdc8e67fc59d797ed644a41cc5eec6a9166ebe0f15bc93`. The official testbench, stimuli and numerical statements are unchanged; only the explicit output-retention policy is added. The deck selects the transistor comparator (`comp_behav=0`) with device transient noise enabled (`noise_en=1`, `devnoise=1`) and the official seed 1. No extra ideal noise source or assumed stage-noise allocation is used.

Effective settings are conservative, gear2only, reltol=1e-4 and voltage abstol=1e-6. The solver accepts 2,452,397 steps; Spectre elapsed time is 838 s, wrapper time 842 s. Only the official decision sampler is retained, rather than a full continuous noise waveform. The deterministic full-terminal SOA results are documented separately in [A5-GATES.md](A5-GATES.md); this sampler-only noise run is not a new full-waveform SOA or output-validity test.

Archive SHA-256 `2e6a63e386592519f7a8e8fc1d6d63a43b0663708a219632c42379cea7093285`, 235,046 bytes, 67 members: CRC and every member SHA-256 verified, exact owned remote directory absence confirmed. Decision-file SHA-256 is `1d2ba69edc1551fbc088c2c05468e975ac833f6461cec98659e870457ff2a1f4`. The official FS noise record and probability-fit figure are retained under the candidate results.

A5 remains `wip` and is not qualified. Its passing deterministic gates do not imply acceptable physical noise. This total noise result alone does not identify front-pair, reset, hold, clock or latch contributions, and differences of squared noise values between different circuits are not component-noise measurements. Further architecture review must distinguish measured operating trajectories from simplified noise assumptions.
