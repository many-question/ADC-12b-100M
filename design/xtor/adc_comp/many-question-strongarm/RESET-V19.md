# RESET-V19: reduce clock-gate load

V18 passes SF/high/-40, FS/high/-40 and TT timing, reset, output validity and all 69 MOS terminal pairs. The two Q MOMs reduce the previously failing reset peak to 0.99878 V. TT 1/30 mV delay is 61.343944/47.475090 ps. Its matched short fine-step diagnosis records 0/256 wrong polarities at +/-800 uV (OUTP counts 0/128 and 128/128). This remains a short diagnostic with a different low noise frequency, not an official noise estimate.

V18's TT mixed-sequence CLK charge gives 16.037833 fF, slightly above the 16 fF gate. The mixed sequence is not the official capacitance test, but it provides insufficient confidence to expand a marginal clock load. This source changes only MCKP from 3.0 um to 2.7 um at 30 nm, retaining three fingers, N4 clock pull-down, both N0.5 Q shunts and all five MOMs. The new callback succeeds without warnings; all terminal parasitics come from its result, SHA-256 `4c95992b12488f02b405cc506443cde9dc0bb5750de45d19aff81a133bffa2e5`. No other electrical statement changes.

The smaller PMOS should reduce external clock-gate charge but may delay shunt turn-on and restore reset overshoot. SF/high/-40 and FS/high/-40 therefore come first, followed by TT and the matched noise diagnosis only if those pass. Electrical SHA-256: `c14d49b929c6c404d4166762d41bc8773e097a141c4ba0365d5462fbd007e008`. The [source](RESET-V19.txt) contains 23 MOS and 5 MOMs, with complete RNL checked on a byte-identical mirror. Canonical V14 and all older evidence remain preserved. Formal capacitance, noise and qualification do not transfer.

![Physical comparator with smaller clock PMOS](reset-v19.png)
