# BUFFER-V13: genuine new-source formal gates

The canonical source is electrically identical to the ten-key-corner and tight-convergence source. The existing official runner, original testbench, numerical settings, measurement and recorder are unchanged. Private screens are not adopted as official records.

## TT capacitance and kickback: pass

Run `20261031-070641-13bb-tb_comp_kickback` starts from clean source commit `d4c88fe23e96627826be3e39d56de1ba71ed01ab`. Electrical SHA-256 is `ce5b3787a38ea80eb6775686bbe1df538e8864a2deb3d5f784d67e119b6146e0`.

| Metric | Measured | Limit |
|---|---:|---:|
| Input capacitance | 19.328731218738 fF | 20 fF |
| CLKC capacitance | 9.604337628086 fF | 16 fF |
| Differential kickback | 0.001649260400 uV | 40 uV |

The [official TT result](../../../../results/adc_comp/tb_comp_kickback/xtor-many-question-miyahara/tt_nom_27.json) retains its actual clean-source metadata. The complete original run and result figures are SHA-verified in a private archive, and the exact owned remote directory is confirmed absent. Execution uses +aps without explicit +mt; logs confirm effective single-thread operation.

At the completion of this first gate one of 92 records matched B13; 91 remained stale. The prescribed original TT noise test follows below. No B12 noise, remaining-corner, Monte Carlo or mixed-top result transfers.

## TT noise: prescribed point estimate passes

Run `20261031-071236-dad5-tb_comp_noise` uses actual clean source `78ab776553b77383cb642956e43ed6ac203a3749` and the unchanged original 17 x 512 decisions, 50 GHz bandwidth and seed 1. The official estimate is **198.728193916 uV rms**, against 200 uV at TT and 240 uV for the all-corner requirement. The 95% profile-likelihood interval is 190.74–207.11 uV. Absolute systematic offset is 0.004044969093 mV. The prescribed point estimate passes; the 1.271806 uV margin is small and the interval crosses 200 uV. No robustness margin or statistically isolated repair benefit is claimed, and no seed/sample-count retry is used. B12's interval overlaps this one.

All 8704 samples are present and finite, with exactly 512 at every level and none outside the expected sequence. Minimum absolute sampled OUTP-minus-OUTN is 0.873724294294 V. Maximum absolute standardized binomial fit residual is 1.922026; the S-curve has no gross anomaly. The fit interval is conditional on the Gaussian-CDF model. Original outputstart=tstop prevents inferring full reset or MOS-stress coverage from this official noise waveform; the separate deterministic and diagnostic evidence retains its own scope.

| Input (uV) | OUTP count / 512 | Probability |
|---:|---:|---:|
| -800 | 0 / 512 | 0.00000000 |
| -700 | 0 / 512 | 0.00000000 |
| -600 | 2 / 512 | 0.00390625 |
| -500 | 3 / 512 | 0.00585938 |
| -400 | 17 / 512 | 0.03320312 |
| -300 | 24 / 512 | 0.04687500 |
| -200 | 77 / 512 | 0.15039062 |
| -100 | 136 / 512 | 0.26562500 |
| 0 | 269 / 512 | 0.52539062 |
| 100 | 341 / 512 | 0.66601562 |
| 200 | 443 / 512 | 0.86523438 |
| 300 | 476 / 512 | 0.92968750 |
| 400 | 499 / 512 | 0.97460938 |
| 500 | 508 / 512 | 0.99218750 |
| 600 | 511 / 512 | 0.99804688 |
| 700 | 512 / 512 | 1.00000000 |
| 800 | 512 / 512 | 1.00000000 |

[Official TT result](../../../../results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/tt_nom_27.json) and its plot retain the original runner metadata. Raw/deck hashes are verified and the exact owned remote run is absent. Two genuine TT cases now match B13 and 90 older-source records remain stale. Next are required official noise cases at SS/low/125, FF/high/125, SF/high/125 and FS/low/125, whose private deterministic stress gates already pass. Remaining-corner stress, all required formal coverage, mismatch and mixed-top qualification remain open.

![Original official noise curve and residual](../../../../results/adc_comp/tb_comp_noise/xtor-many-question-miyahara/tt_nom_27.noise.png)
