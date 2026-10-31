# B2 FS noise: retained-waveform diagnosis

The complete physical noise failure is retained in [RESTORATION-11](RESTORATION-11.md). This analysis reuses its exact noise-off deterministic source at TT and FS/low/125. It does not identify additive device-noise contributions. Measurements below average the four +100/-100 uV cycles (both repetitions), referenced to each actual CLKC half-supply rise, using linear interpolation on the original saved grids. D denotes the DP/DN pair; core difference denotes RP-RN. Threshold events are descriptive waveform markers, not measured loop-gain unity or transistor turn-on times.

| Marker | TT | FS/low/125 |
|---|---:|---:|
| D common mode crosses 0.8 VDD (ps) | 16.344521 | 15.061770 |
| D common mode crosses 0.6 VDD (ps) | 25.409639 | 22.807157 |
| Core differential reaches 1 mV (ps) | 34.646518 | 41.360939 |
| Core differential reaches 5 mV (ps) | 42.454480 | 50.321999 |
| D differential at core 1 mV (mV) | 0.542460 | 0.020730 |
| Max saved D differential before core 1 mV (mV) | 0.536524 | 0.338202 |
| D common mode at core 1 mV (V) | 0.378500 | 0.223456 |
| Winning output reaches 0.5 VDD (ps) | 66.610510 | 80.354367 |

Both corners use the same typical MOM passive model; FS is fast NMOS / slow PMOS in the project corner mapping, with supply reduced from 0.90 to 0.81 V and temperature raised from 27 to 125 C. Merely scaling temperature in an otherwise fixed kT-type variance gives sqrt(398.15/300.15) = 1.152, whereas the measured noise-width ratio is 2.5146. This comparison only shows why temperature scaling alone is an inadequate explanation; gm, bias, transfer functions and device noise spectra are not held fixed in these simulations. No transient gm or device-noise spectrum was saved, so their individual effects remain unmeasured.

B2 adds PMOS-mediated XP/XN and RP/RN stages after the same dynamic input principle. FS crosses 0.6 VDD 2.602 ps earlier, while the core 1 mV marker is 6.714 ps later. At that marker, the front differential has fallen from 0.54246 to 0.02073 mV; its earlier peak also falls from 0.5365 to 0.3382 mV. CKB half-supply timing changes only 5.532 to 5.336 ps; CKR changes 8.392 to 9.106 ps. These observations support investigating the relation between front-stage discharge and later-stage response, rather than assuming the whole delay increase comes from clock buffering. The sampled values are on evolving nonlinear trajectories and are not a small-signal gain or proof of where noise originates.

Two isolated physical trials are justified: (1) a modest symmetric DP/DN-to-ground MOM increase from the existing 48-finger devices to keep the input-stage signal available longer; (2) separately, a callback-valid change to the M14/M15 PMOS versus M12/M13 NMOS transfer-stage ratio, targeting earlier XP/XN response under FS. Preserve physical RP/RN-to-output isolation and check its loser peaks at every trial. Strengthening PMOS can also add drain-node gate capacitance and noise; reducing NMOS can alter reset and contention, so no improvement is assumed. TT delay margin is only 1.6881 ps and SS reset margin 4.7953 ps. A tail reduction is a lower-priority alternative given those timing margins. All trials require deterministic/loading gates before full physical FS noise; the first small steps are now implemented separately as B2-C52 and B2-P5, with current results in RESTORATION-TRIALS.md.

The first complete tests distinguish these directions. C52 gives 463.741786 uV rms versus B2's 469.460077 uV, with strongly overlapping profile intervals and a nearly unchanged early differential peak; no further capacitor step follows. P5 gives 395.813841 uV rms, a 15.7% reduction, while its FS core 1 mV marker moves from 41.360939 to 38.833182 ps and the front differential at that marker rises from 0.020730 to 0.048833 mV. This joint evidence motivates one bounded P6 step on the same PMOS pair, retaining original capacitance and N geometry. P5 still fails 240 uV; neither its waveform markers nor the single-seed profile interval establish general noise attribution or seed robustness. The separate P6 gates and outcome are recorded in [RESTORATION-TRIALS](RESTORATION-TRIALS.md).

Provenance: TT archive `372533cafa9ea446ad9dc9db15f8e308c7b32b0d535668274452441d97cbf315`; four-corner archive `48a1b0264fded9768059d1f566911ebdc229193a73291c2522cfdd5c07e4cd9c`. Every per-cycle event and original PSF SHA is retained in the private waveform audit. Existing noise-off source-suppression results from other variants are not borrowed or variance-subtracted here.
