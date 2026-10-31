# Miyahara comparator: BUFFER-V20

> Evidence retention (2026-10-31): Historical raw/archive statements below refer to the original audit. Superseded waveforms were released under the user's retention policy. [EVIDENCE-RETENTION](EVIDENCE-RETENTION.md) lists the completed runs still available for raw re-audit.

Canonical **B20 fails the merged adc_comp 0.8.0 official FS/low/125 noise test at 343.4944014285115 uV rms against 240 uV**. The original 17 x 512 decisions are retained, with a model-conditional 95% profile interval of 332.03 to 355.53 uV. [FORMAL-SPEC08](FORMAL-SPEC08.md) links the genuine committed result and figure. Current dependency coverage is 1 fresh / 96 records; freshness does not imply passing. This candidate remains WIP, unqualified and unselected.

The independent [B22 experiment](BUFFER-V22.md) passes five merged-baseline deterministic corners and four tighter repeats: all 180/144 actual decisions and resets, output validity and all 129 unrounded MOS terminal pairs. Its stronger CKB pull-up repairs B21's SS reset failure to 34.071442458944574 ps at baseline and 33.30087103116152 ps tighter. However, its complete FS/low/125 noise test **also fails at 342.51175741522553 uV rms** (331.11 to 354.49 uV). B22 qualification expansion stops; B22 TT noise remains untested and B22 is not promoted. Further circuit design continues, preserving every failure.

The canonical source contains 43 MOS devices and nine physical MOM capacitors. All dimensions and terminal parasitics come from successful callbacks or exact verified geometry reuse. Physical rail loads carry persistent current. [ENERGY-COMPARISON](ENERGY-COMPARISON.md) and the later private reports retain whole-cycle AVDD measurements; energy is report-only.

![Current complete transistor schematic](schematic.png)

[NUMERICS-94](NUMERICS-94.md) retains the numerical migration and every private gate. PR #95 is merged at c6152d236e525793ecc4809b9a6c9dfb9fd0ad77, with comp 0.8.0 and exact ADCToolbox commit cd72061ff3b7a977163dac540da126ae22f5e38d. The runtime passes the #96 self-check at 79.999999999274 dB. New evidence uses APS and actual conservative settings, without explicit maxstep or method. No old or private result is relabeled as formal.

Earlier private B20 TT noise is 191.43800312001045 uV rms; it is not a new formal TT result. Its separate tighter TT capacitance measurements are 19.328731218738323 fF per input and 11.288471705097978 fF for CLKC. The specified net differential change after evaluation plus reset is 8.49919999830473e-05 uV, within numerical drift. Instantaneous differential disturbance reaches 25.237840952966987 uV during evaluation and common-mode excursion reaches 7.4257336460090695 mV. These instantaneous values are distinct from the net metric and are not compared to its 40 uV limit. Actual-CDAC validation must check decision-phase differential and common-mode disturbance.

[B21](BUFFER-V21.md) retains its SS reset failure at 35.42069219051348 ps. [B20 promotion proof](PROMOTION-BUFFER-V20.md), [historical baseline](BASELINE-BEFORE-BUFFER-V20.md) and [old-setting original runs](FORMAL-BUFFER-V20.md) preserve earlier sources, records and verified archives. Historical figures use byte-verified fixed published links where duplicate local PNGs were removed. No failure or stale record is discarded.

Issues #40/#63/#69/#75/#77/#78/#84/#100 remain acknowledged. The branch includes main f1ac9a5's site-only fix; comparator tools, testbenches and specifications are unchanged by this candidate. Remaining corners, full formal coverage, 50-sample mismatch, operating range, mixed-top regression and lead review remain open.

[Artificial B22 source diagnostics](NOISE-SOURCE-DIAGNOSTICS-B22.md) retain input-pair and regenerative-stage trials plus the completed subgroup split. Front-driver noise suppression gives 314.50354475961876 uV rms; latch/DP-device suppression gives 281.27833319310434 uV rms, each with all 17 x 512 decisions and unchanged physical source. These artificial widths cannot be variance-subtracted into independent contributions and are ineligible for qualification; full physical B22 noise remains the failed 342.51175741522553 uV rms result.

Independent [B23](BUFFER-V23.md) uniformly strengthens the ten-device second stage while retaining the B22 input/tail/reset/output devices. Added loading and physical all-source noise require new validation; no pass or promotion is assumed.
