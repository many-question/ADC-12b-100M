## What

<!-- Title: `[<block>] candidate <name> <summary>`, e.g. `[adc_comp] candidate alice-strongarm first netlist`.
     One candidate per PR; it may only touch design/xtor/<block>/<name>/ and results/<block>/*/xtor-<name>/. -->

<!-- One paragraph: which block / tool / spec, what changed and why. -->

## Block status

- Block: `adc_...`   candidate: `<name>`   `candidate.yaml` status before -> after: new / `wip` / `ready` / `withdrawn`
- Specs changed? <!-- not in a candidate PR: port / spec / testbench changes go through an issue and are decided by the project lead (@many-question) -->

## Evidence

<!-- Paste the summary of `python -m adcflow report --block adc_...` and the
     commands you ran, e.g.
       python -m adcflow sim tb_comp_delay --view adc_comp=xtor:<name> --corners all
     Results are recorded under results/ and must be committed with the netlist
     they were simulated with (stale results are flagged by CI and on the leaderboard). -->

## Checklist

- [ ] `python -m adcflow check all` passes locally (hygiene, ports, rnl, generated files, results)
- [ ] `python -m pytest -q -m "not slow"` passes
- [ ] Netlist has a complete RNL drawing and RNL semantics (structures / groups)
- [ ] No server names, server paths, shell-setup paths, PDK paths or model data anywhere (files and commit messages)
- [ ] Port list unchanged (specs, testbenches and other candidates untouched); netlist has no `include`
- [ ] Checked open `[<block>]` issues (spec-change notices acknowledged); results re-run after any spec change
- [ ] Title is `[<block>] candidate <name> …`; `candidate.yaml` lists my GitHub login in `authors`, `acknowledged` has the spec-change notices I read
