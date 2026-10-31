# BUFFER-V21: larger regeneration-node storage

B20 passes the full proposed-settings TT noise precheck at 191.43800312001045 uV rms but fails FS/low/125 at 343.4944014285115 uV against 240 uV (95% profile interval 332.03 to 355.53 uV). All 8704 finite samples per corner remain preserved. [NUMERICS-94.md](NUMERICS-94.md) records the failure and verified archive. B20 qualification expansion has stopped.

This experiment changes only CRP/CRN from 8 to 16 MOM fingers, 2.06055 to 4.46051 fF. Every one of the 43 MOS devices and the other seven MOMs is electrically identical to B20. Finger length, width, spacing and metal range remain unchanged. The zero-warning callback SHA-256 is `84249f3512afcb0edf2f7347f87ad24398cca5bb59af70eca1e7bd579b236135`.

Earlier phase diagnoses found correct DP/DN signs before residual errors appeared at RP/RN. Added local storage tests whether the early regenerative-node signal/noise trajectory improves. It also slows voltage development, adds reset charge and changes coupling; a noise benefit is not assumed and a simple kT/C estimate cannot establish input-referred noise. B20 has limited TT timing and SS hot reset margin, so those checks accompany SF/FS high-voltage cold whole-trace terminal stress and output validity. FS/low/125 is included because it is the failed noise corner.

The private screen uses conservative APS with no explicit maxstep, checking the actual Spectre log. It preserves the physical stimuli and original measurements and does not alter shared testbenches, tools, thresholds or formal results. Proposed-settings screens do not constitute official acceptance. Electrical SHA-256: `6f23c8669d6380bef466bdf2537d515f1e1802ce113310be3ffabaf43689f319`. The [source](BUFFER-V21.txt) contains complete RNL checked on a byte-identical mirror. Canonical B20 and every earlier failure remain preserved; B21 is not promoted or qualified.

![Comparator with larger RP/RN MOMs](buffer-v21.png)
