# V2 FS noise: retained-waveform diagnosis

The complete physical noise failure is retained in [RESTORATION-11](RESTORATION-11.md). This analysis reuses its exact noise-off deterministic source at TT and FS/low/125. It does not identify additive device-noise contributions. Measurements below average the four +100/-100 uV cycles (both repetitions), referenced to each actual CLKC half-supply rise, using linear interpolation on the original saved grids. D denotes the DP/DN pair; core difference denotes QN-QP. Threshold events are descriptive waveform markers, not measured loop-gain unity or transistor turn-on times.

| Marker | TT | FS/low/125 |
|---|---:|---:|
| D common mode crosses 0.8 VDD (ps) | 15.130772 | 14.096146 |
| D common mode crosses 0.6 VDD (ps) | 24.956801 | 23.141327 |
| Core differential reaches 1 mV (ps) | 33.482846 | 32.630726 |
| Core differential reaches 5 mV (ps) | 45.397085 | 42.848699 |
| D differential at core 1 mV (mV) | 0.040920 | 0.070869 |
| Max saved D differential before core 1 mV (mV) | 0.316247 | 0.201010 |
| D common mode at core 1 mV (V) | 0.409891 | 0.348751 |
| Winning output reaches 0.5 VDD (ps) | 63.287664 | 63.613075 |

Both corners use the same typical MOM passive model; FS is fast NMOS / slow PMOS in the project corner mapping, with supply reduced from 0.90 to 0.81 V and temperature raised from 27 to 125 C. Merely scaling temperature in an otherwise fixed kT-type variance gives sqrt(398.15/300.15) = 1.152, whereas the measured noise-width ratio is 1.7212. This comparison only shows why temperature scaling alone is an inadequate explanation; gm, bias, transfer functions and device noise spectra are not held fixed in these simulations. No transient gm or device-noise spectrum was saved, so their individual effects remain unmeasured.

V2 shares the DP/DN dynamic discharge with the regenerative N stack. FS crosses 0.6 VDD 1.815 ps earlier, and the maximum saved front differential before the 1 mV core marker falls from 0.316 to 0.201 mV. The core reaches 5 mV earlier, yet the final 100 uV output delay is nearly unchanged. Faster final regeneration therefore does not demonstrate improved input-referred noise. Front-stage signal development and noise transfer into regeneration are plausible contributors, but these deterministic markers cannot separate input-pair, tail, latch or reset-device noise.

The first discriminating physical trial should alter only the existing symmetric DP/DN-to-ground MOM loading (48-finger baseline, one modest callback-valid increase), preserving the 56 um input devices, tail and output isolation. The objective is to extend signal development before regeneration; increased reset load and slower TT decisions are explicit costs. The present TT 30 mV margin is 5.8305 ps and SS reset margin is 8.8685 ps. A separate alternative is one modest tail-current reduction, only if the waveform markers show the desired change without losing delay. Do not change both simultaneously or enlarge the input pair as the first action: measured Cin is already 19.3131 fF against 20 fF. Any improvement must be checked by full physical FS transient noise after timing/reset/CMP-15/stress/Cin gates. The separate V2-C56 source now implements the capacitor trial; current results are in RESTORATION-TRIALS.md. The tail alternative remains untested, and no pass is predicted.

Provenance: TT archive `372533cafa9ea446ad9dc9db15f8e308c7b32b0d535668274452441d97cbf315`; four-corner archive `48a1b0264fded9768059d1f566911ebdc229193a73291c2522cfdd5c07e4cd9c`. Every per-cycle event and original PSF SHA is retained in the private waveform audit. Existing noise-off source-suppression results from other variants are not borrowed or variance-subtracted here.
