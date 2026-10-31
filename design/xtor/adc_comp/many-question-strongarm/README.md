# Strongarm comparator: RESET-V27

Canonical **V27 fails the merged adc_comp 0.8.0 official TT noise test at 210.1008609253812 uV rms against 200 uV**. The original 17 x 512 decisions are retained, with a model-conditional 95% profile interval of 201.81 to 218.79 uV. [FORMAL-SPEC08](FORMAL-SPEC08.md) links the genuine committed result and figure. Current dependency coverage is 1 fresh / 92 records; freshness does not imply passing. This candidate remains WIP, unqualified and unselected.

Independent [V28](RESET-V28.md) reduces CKB storage from 16 to 8 fingers. Critical-corner deterministic checks and tighter repeats pass, but full physical TT noise still fails at 206.44956249285457 uV rms (198.24 to 215.06 uV). Its tighter TT 30 mV delay is 49.84967366576565 ps, leaving 0.15032633423435 ps. A confidence interval crossing the limit does not establish a pass; V28 qualification expansion is stopped.

Independent [V29](RESET-V29.md) doubles four output MOS devices from 4 to 8 um. Its four-corner baseline retains all 144 actual decisions and resets, passes output validity and all 69 unrounded terminal pairs per corner, but **fails TT 30 mV delay at 50.5384103494184 ps**. Matched waveform diagnostics show a later Q-node transition outweighing the shorter Q-to-output interval. V29 qualification expansion is stopped, with no noise run or promotion. Further physical design tests output pull-up/pull-down balance before reconsidering input-tail current.

[Artificial V28 noise-source diagnostics](NOISE-SOURCE-DIAGNOSTICS-V28.md) give fitted widths of 143.69178503038893 uV with input-pair noise suppressed and 187.75199804064 uV with Q-shunt noise suppressed. These are explicitly ineligible for qualification and cannot be variance-subtracted into unique additive contributions. Complete-circuit V28 noise remains the failed result above. Every physical trial restores all noise sources.

The canonical source contains 23 MOS devices and five physical MOM capacitors. Geometry and terminal parasitics come from successful callbacks or exact verified reuse. Physical shunts and rail loads carry reset current; whole-cycle AVDD energy includes that current and is report-only.

![Current complete transistor schematic](schematic.png)

[NUMERICS-94](NUMERICS-94.md) preserves the numerical migration and private checks. PR #95 is merged at c6152d236e525793ecc4809b9a6c9dfb9fd0ad77, with comp 0.8.0 and exact ADCToolbox commit cd72061ff3b7a977163dac540da126ae22f5e38d. The runtime passes the #96 self-check at 79.999999999274 dB. New evidence uses APS and actual conservative settings, with no explicit maxstep or method. No old or private result is relabeled as formal.

V27's separate tighter TT capacitance measurements are 19.331118542884703 fF per input and 15.782118507199666 fF for CLKC. The specified net differential change after evaluation plus reset is 3.749160010224628e-05 uV, within numerical drift. Instantaneous differential disturbance reaches 354.6187879230329 uV during evaluation and common-mode excursion reaches 7.405456990178305 mV. Those instantaneous values are distinct from the net metric and are not compared to its 40 uV limit. Actual-CDAC validation must check decision-phase differential and common-mode disturbance.

[V27 promotion proof](PROMOTION-RESET-V27.md), [historical baseline](BASELINE-BEFORE-RESET-V27.md) and prior experiment reports preserve older sources, every failure and verified archives. Historical figures use byte-verified fixed published links where duplicate local PNGs were removed. Canonical V27 remains unchanged.

Issues #40/#63/#69/#75/#77/#78/#84/#100 remain acknowledged. The branch includes main f1ac9a5's site-only fix; comparator tools, testbenches and specifications are unchanged by this candidate. Remaining corners, full formal coverage, 50-sample mismatch, operating range, mixed-top regression and lead review remain open.

Independent [V30](RESET-V30.md) retains V29 P8 output pull-ups and restores exact V28 N4 pull-downs. TT 30 mV delay improves to 47.35514490849851 ps, but SS/low/125 reset fails at 36.646221657802904 ps. All 144 actual decisions/resets, output validity and unrounded terminal pairs pass; the reset-time failure stops qualification expansion. Noise and capacitance remain untested. Further physical work tests Q precharge strength and explicitly checks the added clock load before any tail-current reduction.

Independent [V31](RESET-V31.md) changes only Q precharge MRQP/MRQN from 3 to 3.6 um to address V30 reset. Full deterministic gates and the dedicated clock-capacitance check precede further noise work.
