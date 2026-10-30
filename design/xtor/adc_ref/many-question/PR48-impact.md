# PR #48 impact and retest plan

**Historical review.** This document records the unmerged `88b7624` snapshot
and its then-current base. PRs #48, #57 and #62 have since merged. For the actual
merged-input audit, current freshness and reruns, see [REF21-retest.md](REF21-retest.md).
The statements below about pending changes and an empty stale list apply only
to the historical base named below.

This is a read-only review of [PR #48 at 88b7624](https://github.com/many-question/ADC-12b-100M/pull/48),
full head `88b7624e1e1bf4c66aeb024d7fcc5c03087ca588`, while it is unmerged.
Current main is `17205ec66d7265da5bf1e4a603ea514f34e99c09`.
The candidate remains **wip**. Its existing 136 records are fresh and pass all
applicable limits on that main (14/14 specifications, 586/586 spec/corner pairs).
No pending code is applied and no new simulation is run for this review.

## Recorded input hashes

All 136 module records contain each of these three changed inputs. Comparing
their recorded hashes with the pending blobs gives:

| Input | Recorded on current main | Pending PR #48 |
|---|---|---|
| `design/behav/veriloga/adc_cdac_sw_va.va` | `e465880479187179` | `25fa7719fc730a3a` |
| `design/behav/veriloga/adc_sarlogic_va.va` | `42f06909a81347ef` | `5cd9dbd22bf395eb` |
| `specs/arch.yaml` | `bffadef750bb5205` | `04b74bfe28a6229a` |

Thus this version would make **all 136 records hash-stale if merged**, even
though the source of this candidate and the four direct reference testbench
netlists are electrically unchanged. The runner records all block views and
their Verilog-A dependencies, including blocks not instantiated by a standalone
reference bench. The actual current-main stale list is **empty**.

| Test | Records | Direct bench hash (same on both revisions) | Physical or measurement impact |
|---|---:|---|---|
| `tb_ref_dc` | 45 | `6c0b4787bdd7e2bb` | Same standalone DUT, load and corrected supply sweep; changed recorded shared dependencies. |
| `tb_ref_noise` | 1 | `edce75b69c56ee11` | Same transistor reference, load and noise analyses; the behavioral reference's bias change does not set this candidate's bias. |
| `tb_ref_startup` | 45 | `d0842a4224af4dfb` | Same supply/reference ramps, capacitive loads and ready-time criteria; changed recorded shared dependencies. |
| `tb_ref_replay` | 45 | `2ea234d4ebabeece` | Same bench text, but its generated load/trigger PWL, model feedback and envelope measurement change. A fresh replay is required. |

The recorded `meta.files` does not directly cover `model.py`, `measure/ref.py`
or the block-spec YAML. Therefore a bench-text comparison or a hash check alone
does not establish semantic equivalence. No recorded hash, metric, original git
ID, `git_clean`, figure or migration provenance is rewritten in this review.

## Replay timing and REF-21

`replay_pattern` calls the system model with an ideal reference; `replay_prepare`
turns its `t_sw`, switch charges and `t_dec` into `iload.pwl` and `trig.pwl`.
The pending model draws charge at comparator decision completion + 35 ps logic
delay + 10 ps driver delay. Architecture waits after decisions 3, 4, 5, 6 and 9
are respectively **10, 30, 30, 30 and 25 ps**.

At TT, charge onset to the next comparator clock is
`max(t_bit + t_dac + extra, t_loop) - t_bit - t_drv`. For steps 1..13 it is:

| Step | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Interval (ps) | 30 | 30 | 40 | 60 | 60 | 60 | 65 | 65 | 90 | 65 | 65 | 65 | 65 |

The no-extra fast step has **30 ps** from charge onset, while UP/DN to the next
clock is 40 ps. The former model gave 85 ps from charge onset on fast steps.
The updated timing regression uses `rtol=0, atol=1e-16`; the earlier ineffective
NumPy default tolerance is fixed. The reviewed PR diagnosis still describes
approximately 40 ps of follower recovery; the coordinator has requested that
its timing reference points be clarified.

Pending REF-21 requires `env_ratio <= 1` at all 45 corners. It takes the maximum,
over conversions and decisions **1..11**, of
`abs(VREFP(k) - VREFP(14)) / (delta_k * LSB * VREF / FS)`.
Decisions 12..14 remain under REF-13. The measurement also adds an 11-element
`env_ratio_per_decision` and the limiting `env_ratio_decision`.

The old diagnostic `env_ratio` used all 14 decisions with a redundancy floor of
0.25 LSB, and the old waveform used the old timing. Its recorded maximum
1.45532317 is preserved as a historical diagnostic; it is **not a REF-21 verdict
under the pending stimulus**. Remeasuring old raw data alone cannot validate
the new load/trigger sequence.

The replay still uses TT decision spacing at every PVT corner. Hot-fast x0.88,
cold-fast x0.8 and slow x1.6 are model studies, not corner-scaled Spectre replay
coverage. A timing-scaled replay would need a shared-flow follow-up; this
candidate does not silently add timing overrides.

## Behavioral reference and mixed top

The behavioral reference changes from 4 mA / 3 pF to 8 mA / 6 pF, and the
analytical follower node includes the additional CDAC capacitance. The block
spec explicitly leaves transistor topology, bias current and decoupling to the
designer. These model values are **not hard requirements on this candidate**.
The ideal-reference replay preparation also does not instantiate that follower.

Mixed-top behavior changes through the SAR extra waits, CDAC break-before-make
switching and source-noise accounting. With behavioral CDAC, source resistance
noise is disabled to avoid counting its sampled kT/C share twice; transient
noise follows `noise_en`. A new behavioral control therefore has a different
baseline, while a reference-mixed run uses this candidate in place of the
behavioral reference. Neither is comparable to the old run as a one-variable
reference-bias experiment.

The old seven-corner mixed-top records, including SS-hot TOP-01 failure, remain
linked in [README.md](README.md). No new top result is placed in this candidate
PR; the coordinator maintains top-level evidence separately.

## Retest sequence after integration

1. **Pin the actual merged main and read the module notice.** Recheck the final
   spec, prepared parameters, numerical settings and source dependency hashes;
   this plan names a pending snapshot, not a future merge guarantee. Keep the
   current source hash `380f10b05b0af622` initially and preserve all old evidence.
2. **Prepare and audit replay on the merged flow.** Regenerate both PWL files;
   verify the charge/clock intervals and architecture waits, coherent stimulus,
   32 warmups plus 1024 judged conversions, 15,840 contiguous decision/start
   samples, unchanged load assumptions and actual numerical settings. Record
   the PWL/source identities rather than reuse the old files.
3. **Run replay pilots, then the full 45-corner acceptance.** Start with TT,
   `ss_low_125`, `ff_high_125` and `ff_low_m40`, then complete the remaining
   corners on the same source. Check REF-12/13/14/21 together, inspect the
   per-decision envelope and limiting decision, and investigate any failure
   before changing the circuit. Use APS and at most two concurrent jobs.
   Boundary failures or numerical ambiguity require convergence checks using
   the shared flow, with both outcomes retained.
4. **Refresh other records according to the merged dependency audit.** The
   prospective 45 DC + 45 startup + one TT noise mismatches are currently
   attributable to shared dependencies, not changed standalone stimulus.
   Compare prepared decks after integration before deciding the execution
   scope. If no supported evidence-reuse mechanism is provided by the lead,
   rerun those 91 cases to obtain clean evidence for the merged inputs; never
   manually replace hashes to mark old results fresh. Retain required startup
   convergence evidence and its actual baseline/twin settings in any refreshed
   acceptance set. A later circuit change invalidates the affected unit evidence
   independently of this shared-flow review.
5. **Coordinate mixed-top reruns after module acceptance.** The coordinator
   arranges the new matched behavioral control and representative mixed-top
   corners, preserving old comparisons and the SS-hot failure. Use identical
   merged inputs, capture/calibration settings and noise settings for that new
   comparison. Keep candidate status wip until the remaining evidence and
   project-lead review support a later status change.

These are deferred actions. This review does not start a retest, alter the
candidate's devices or parameters, apply a pending specification, or claim
that the new acceptance has passed.
