# Current dependency audit and deferred refresh

Audited on 2026-10-30 (Asia/Shanghai), against main `33337c605ff670e04eee814c2178ed26eca7346d` and comparator spec v0.6.0. [PR #76](https://github.com/many-question/ADC-12b-100M/pull/76) is merged; [notice #78](https://github.com/many-question/ADC-12b-100M/issues/78) applies. This update synchronizes documentation and checks only. It launches no simulation and changes no circuit, result JSON or evidence figure. Status stays WIP and unselected.

## Official current status

The current `adcflow.checks.judge` evaluates every original record, including reached-file hashes, unrecorded dependencies and architecture dependencies. `adcflow check results` and the current candidate score independently expose the stale set.

| Recorded test | Records | Fresh | Stale | Actual changed dependency |
|---|---:|---:|---:|---|
| tb_comp_delay | 45 | 0 | 45 | tb/comp/tb_comp_delay.scs |
| tb_comp_kickback | 45 | 45 | 0 | None |
| tb_comp_noise | 1 | 1 | 0 | None |
| tb_comp_offset_mc | 1 | 1 | 0 | None |

The delay testbench content hash changed from `c9bbdac040c91a1f` to `ca754d0b9373b04c`. No additional reached file or architecture value is reported stale. The whole delay record is stale, including its delay, regeneration, reset and decision fields; unchanged stimulus does not make those fields fresh evidence. The other 47 records remain fresh, self-reported evidence, with noise still covering only TT and mismatch retaining its original 50 samples. No record is independently verified.

All 229 candidate result JSON/PNG files are byte-identical to pre-sync head `6cc0a59d639bc7a3a0cea1ec2146dd1a6a2474b9`. The netlist including RNL comments is byte-identical too. Original clean source commits, result metadata and private raw archives are retained. Main was merged, preserving simulated commits instead of rewriting them. No rehash or remeasurement was used.

The candidate score reports `stale=45`, `error=0`, `mismatch=0` and `eligible=false`. Its displayed power still derives from an old stale energy record, so it is not a current v0.6.0 power comparison. The score's `soa=0` means these official JSONs do not contain the private SOA failures; it does not mean SOA passed. Known device-voltage failures remain, as do the four recorded reset failures. Full noise coverage and mixed-top qualification are also absent.

## Energy definition

Current CMP-10 is the average AVDD energy over the unchanged 36-decision mixed sequence, +/-100 mV through +/-10 uV, repeated twice. Its meter integrates from 100 ps to 14.5 ns, exactly 36 complete 400 ps cycles; energy is AVDD charge x VDD / 36. The metric is reported-only with no acceptance limit. The external CLKC source remains outside the AVDD meter.

The preserved v0.5.0 number instead integrates 0–14.5 ns and normalizes average power to 400 ps, including the 100 ps lead-in (36.25 periods). It remains historical and stale. The existing private +/-1 mV probe uses a different stimulus and fine numerical settings, so it is also not the new official mixed-sequence CMP-10. No new-definition energy value is claimed here. The new extractor rejects the old meter window; rescaling or rehashing the old result is not an official refresh.

## One combined refresh, deferred

The [#77 lead decision](https://github.com/many-question/ADC-12b-100M/issues/77#issuecomment-6514624643) adds all-corner output validity over each of the 36 CLKC evaluation intervals: exactly one output crosses 50% VDD, and the losing output stays below 30% VDD. Violation count must be zero and worst losing-output peak is reported. A no-crossing interval is handled separately by CMP-09 for |vd| >=100 uV and the stated small-input timeout case. Noise and mismatch retain falling-edge sampling. The implementing flow change is not in audited main; no passing result under that new rule is claimed.

For a fresh record of this unchanged frozen candidate, #78 requires exactly **45 tb_comp_delay jobs**. The two candidates together require 90 jobs, with at most one Spectre process across the comparison. The 45 kickback, one noise and one mismatch records per candidate do not need rerunning for the currently merged change. Wait for the #77 measurement/spec implementation and notice, then recheck actual dependencies and perform the one combined delay refresh if the frozen failing baseline is still needed. Do not run the same full sweep once for #78 and again for #77. If a later circuit repair or another dependency changes, recalculate the affected scope instead of assuming the other 47 records remain reusable.

Historical timing for this candidate's 45-job serial batch is **772.6 s (12.88 min)** for upload, remote execution and fetch, with **653 s** summed simulator time. `meta.wall_s` repeats the single batch wall time in every JSON and must not be summed 45 times. Allow roughly **15–20 minutes per candidate, 30–40 minutes for both**, including measurement/figures and verified archival under similar conditions; queue, license waits and retries can extend this. This is a planning estimate, not a queued run.

After any later authorized refresh, retain the old evidence, run the official merged test with `--corners all --mode aps --jobs 1 --keep`, retrieve and verify raw artifacts, and publish fresh source/dependency provenance and all failures. The current known failures are retained while this plan is deferred; neither candidate is eligible for selection.
