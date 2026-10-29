"""The lead's verification of candidate results (docs/verification.md §7): tolerances, the rerun
and its record in verification/, and how the leaderboard counts verified / self-reported / mismatch.
Every test works in a temporary repository root (candidates.ROOT, checks.REPO_ROOT); the rerun is
a stand-in for runner.run_test."""

import json
import shutil

import pytest
import yaml

from adcflow import REPO_ROOT
from adcflow import candidates as cand
from adcflow import checks, verify
from adcflow.cli import main
from adcflow.netlist import content_hash
from adcflow.specs import blocks

B, NAME, TEST = "adc_comp", "alice", "tb_comp_delay"
NL = f"design/xtor/{B}/{NAME}/{B}.scs"
GOOD = {"tdelay_1mV_ps": 60.0, "tdelay_30mV_ps": 30.0, "tau_reg_ps": 10.0, "treset_ps": 20.0,
        "wrong_decisions": 0, "energy_fJ": 100.0}
GLOBALS = {"vdd": 0.9, "vdd18": 1.8, "tempc": 27.0, "noise_en": 0, "devnoise": 1}


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(cand, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    shutil.copytree(REPO_ROOT / "design" / "rnl", tmp_path / "design" / "rnl")      # the PDK device list
    d = tmp_path / "design" / "xtor" / B / NAME
    d.mkdir(parents=True)
    ports = " ".join(blocks()[B].port_names)
    (d / f"{B}.scs").write_text(f"simulator lang=spectre\nsubckt {B} ({ports})\n"
                                "MN1 (OUTP INP VSS VSS) nch_ulvt_mac w=2u l=30n\nends {B}\n".replace("{B}", B))
    (d / "candidate.yaml").write_text(yaml.safe_dump({"name": NAME, "description": "A latch.", "status": "ready",
                                                      "acknowledged": [], "authors": [{"github": NAME}]}))
    return tmp_path


def nl_hash(root):
    return content_hash(root / NL)


def result(root, corner="tt_nom_27", metrics=None, files=None, test=TEST, **meta):
    d = root / "results" / B / test / f"xtor-{NAME}"
    d.mkdir(parents=True, exist_ok=True)
    m = {"date": "2026-10-01T00:00:00", "git": "abc1234", "mode": "aps", "mc": None,
         "files": files if files is not None else {NL: nl_hash(root)}, **meta}
    doc = {"block": B, "test": test, "view": f"xtor-{NAME}", "corner": corner, "params": {},
           "globals": GLOBALS, "metrics": dict(GOOD if metrics is None else metrics), "meta": m}
    p = d / f"{corner}.json"
    p.write_text(json.dumps(doc))
    doc["_path"] = p
    return doc


MC = {"runs": 50, "seed": 7, "firstrun": 1, "variations": "mismatch", "models": "tt_mm"}


def fake_run(root, metrics=None, calls=None, **row):
    """A runner.run_test stand-in: one job per corner with the given metrics and the netlist hash of now."""
    def run(test_id, block, corners, views, params, mode, parallel, keep, do_record, mc=None):
        if calls is not None:
            calls.append((test_id, block, corners, views, mode, do_record) + ((mc,) if mc else ()))
        out = []
        for c in corners.split(","):
            meta = {"date": "2026-10-30T00:00:00", "git": "def5678", "git_clean": True, "mode": mode, "pdk": True,
                    "mc": dict(MC, **mc) if mc else None, "rc": "0", "sim_s": "12", "numerics": {"reltol": 1e-7},
                    "files": {NL: nl_hash(root)}, "views": dict(views)}
            r = {"job": c, "corner": c, "rc": "0", "metrics": dict(GOOD if metrics is None else metrics), "out": None,
                 "params": {}, "globals": dict(GLOBALS), "meta": meta}
            r.update(row)
            out.append(r)
        return out
    return run


# ------------------------------------------------------------------ tolerances
@pytest.mark.parametrize("metric, tol", [
    ("enob", (0.0, 0.05)), ("enob_nom", (0.0, 0.05)), ("sfdr_dBc", (0.0, 0.5)), ("sndr_dB", (0.0, 0.5)),
    ("t_off_ps", (0.02, 1.0)), ("t_conv_max_ns", (0.02, 0.001)), ("jitter_fs", (0.10, 0.0)),
    ("noise_uV", (0.08, 0.0)), ("vgs_min_V", (0.01, 0.001)), ("vgs_var_mV", (0.02, 0.5)),
    ("iavg_uA", (0.02, 0.1)), ("cin_phb_fF", (0.02, 0.1)), ("energy_fJ", (0.02, 0.5)), ("top_gain", (0.02, 0.0)),
])
def test_tolerance_by_metric_name(metric, tol):
    assert verify.tolerance(metric) == tol


def test_compare_metrics():
    a = {"sfdr_dBc": 90.0, "t_off_ps": 18.0, "soa_violations": 0, "soa_scope": "device", "soa_table": [{"max_V": 1}],
         "soa_points": 100, "cal_independent": True}
    m, probs, skipped = verify.compare_metrics(a, dict(a, sfdr_dBc=90.45, t_off_ps=18.9, soa_points=120,
                                                       soa_table=[{"max_V": 2}]))
    assert probs == [] and sorted(skipped) == ["soa_points", "soa_table"]
    assert m["sfdr_dBc"]["ok"] and m["sfdr_dBc"]["tol"] == 0.5 and m["t_off_ps"]["tol"] == 1.0
    for change, what in (({"sfdr_dBc": 89.4}, "sfdr_dBc: 90 self-reported, 89.4 rerun"),
                         ({"t_off_ps": 19.5}, "t_off_ps"),
                         ({"soa_violations": 1}, "soa_violations: 0 self-reported, 1 rerun (must be equal)"),
                         ({"soa_scope": "external"}, "soa_scope"),
                         ({"cal_independent": 1}, "cal_independent")):
        _, probs, _ = verify.compare_metrics(a, dict(a, **change))
        assert len(probs) == 1 and probs[0].startswith(what), probs
    _, probs, _ = verify.compare_metrics(a, {**a, "error": "spectre rc=1"})
    assert probs == ["error: not self-reported"]
    _, probs, _ = verify.compare_metrics({**a, "extra_ps": 1.0}, a)
    assert probs == ["extra_ps: not in the rerun"]
    # lists of scalars: element by element with the metric's tolerance, same length
    off = {"offsets_mV": [1.0, -2.0, None], "sample_status": ["ok", "ok", "failed"]}
    m, probs, _ = verify.compare_metrics(off, {"offsets_mV": [1.3, -2.4, None], "sample_status": ["ok", "ok", "failed"]})
    assert probs == [] and m["offsets_mV"]["n"] == 3 and m["offsets_mV"]["worst_diff_per_tol"] == pytest.approx(0.8)
    _, probs, _ = verify.compare_metrics(off, {**off, "offsets_mV": [1.0, -3.0, None]})
    assert probs == ["offsets_mV: 1 of 3 values differ (first [1]: -2.0 self-reported, -3.0 rerun)"]
    _, probs, _ = verify.compare_metrics(off, {**off, "offsets_mV": [1.0, -2.0, 0.5]})
    assert probs[0].startswith("offsets_mV: 1 of 3 values differ (first [2]: None")
    _, probs, _ = verify.compare_metrics(off, {**off, "sample_status": ["ok", "ok"]})
    assert probs == ["sample_status: 3 values self-reported, 2 rerun"]


def test_compare_verdicts_params_globals_and_inputs(root):
    doc = result(root)
    rec = {**doc, "metrics": dict(GOOD, tdelay_1mV_ps=60.5), "meta": {"files": {NL: nl_hash(root)}}}
    c = verify.compare(doc, rec)
    assert c["ok"] and c["verdicts"]["CMP-04"] == {"self": True, "rerun": True, "ok": True}
    # a verdict that differs comes first, even inside the metric tolerance (here: 79.5 vs 80.5 ps, limit 80)
    c = verify.compare({**doc, "metrics": dict(GOOD, tdelay_1mV_ps=79.5)}, {**rec, "metrics": dict(GOOD, tdelay_1mV_ps=80.5)})
    assert not c["ok"] and c["problems"][0] == "CMP-04: pass self-reported, fail rerun"
    assert c["metrics"]["tdelay_1mV_ps"]["ok"]
    c = verify.compare(doc, {**rec, "params": {"npts": 4096}})
    assert not c["ok"] and c["problems"][0].startswith("params differ")
    c = verify.compare(doc, {**rec, "globals": dict(GLOBALS, cdac_behav=1)})
    assert c["ok"] and c["notes"] == ["global cdac_behav recorded by the rerun only"]
    c = verify.compare(doc, {**rec, "globals": dict(GLOBALS, vdd=0.81)})
    assert not c["ok"] and "global vdd: 0.9 self-reported, 0.81 rerun" in c["problems"]
    c = verify.compare(doc, {**rec, "meta": {"files": {NL: nl_hash(root), "tb/comp/tb_comp_delay.scs": "1234"}}})
    assert c["problems"] == ["input tb/comp/tb_comp_delay.scs: not recorded self-reported, 1234 rerun"]
    c = verify.compare(doc, {**rec, "meta": {"files": {}}})
    assert c["problems"] == [f"the rerun does not record the candidate netlist {NL}"]


# ------------------------------------------------------------------ refusals (nothing simulated)
def test_refusals(root, capsys):
    calls = []
    run = fake_run(root, calls=calls)
    assert verify.verify(TEST, B, NAME, "tt_nom_27,ss_low_125", run=run) == 1
    assert "tb_comp_delay at ss_low_125: no self-reported result" in capsys.readouterr().out
    result(root, "ss_low_125", files={NL: "0000"})
    result(root, "ff_high_125", files={})
    result(root, "tt_nom_125", metrics={"error": "spectre rc=1"})
    result(root, "tt_nom_m40", files={NL: nl_hash(root), "tb/x.scs": "dead"})
    result(root, "tt_low_27", mc=dict(MC))
    _, ref = verify.plan(TEST, B, NAME, "ss_low_125,ff_high_125,tt_nom_125,tt_nom_m40,tt_low_27")
    text = "\n".join(ref)
    assert "recorded on netlist 0000" in text and "the netlist differs" in text
    assert f"does not record the candidate netlist {NL}" in text
    assert "an error result" in text and "stale (tb/x.scs)" in text and "different Monte Carlo settings" in text
    assert verify.verify(TEST, B, NAME, "ss_low_125", run=run) == 1 and calls == []
    assert not (root / "verification").exists()
    # the default corners are those the test's specs require: CMP-05 and others are `all`
    _, ref = verify.plan(TEST, B, NAME)
    assert sum("no self-reported result" in r for r in ref) == 45 - 5
    assert verify.plan("tb_top_sine", "adc_top", NAME)[1] == ["adc_top has no candidates"]
    assert "no candidate 'bob'" in verify.plan(TEST, B, "bob")[1][0]


# ------------------------------------------------------------------ the rerun and its record
def test_verify_writes_a_matching_record_and_the_leaderboard_counts_it(root, capsys):
    doc = result(root)
    (row,) = cand.leaderboard(B)
    assert (row["verified"], row["self_reported"], row["flags"]["unverified"]) == (0, 1, 1)
    calls = []
    assert verify.verify(TEST, B, NAME, "tt_nom_27", run=fake_run(root, dict(GOOD, tau_reg_ps=10.1), calls)) == 0
    assert calls == [(TEST, B, "tt_nom_27", {B: f"xtor:{NAME}"}, "aps", False)]
    p = root / "verification" / B / NAME / TEST / "tt_nom_27.json"
    rec = json.loads(p.read_text())
    assert rec["status"] == "match" and rec["candidate"] == NAME and rec["job"] == "tt_nom_27"
    assert rec["verifies"] == {"result": f"results/{B}/{TEST}/xtor-{NAME}/tt_nom_27.json", "netlist": NL,
                               "netlist_hash": nl_hash(root), "date": "2026-10-01T00:00:00", "git": "abc1234",
                               "mode": "aps"}
    assert rec["metrics"]["tau_reg_ps"] == 10.1 and rec["specs"]["CMP-07"]["pass"]
    assert rec["meta"]["git"] == "def5678" and rec["meta"]["files"] == {NL: nl_hash(root)}
    assert rec["comparison"]["metrics"]["tau_reg_ps"]["diff"] == pytest.approx(0.1)
    assert "match     verification/" in capsys.readouterr().out
    assert verify.state(doc) == {"state": "verified", "why": ""}
    (row,) = cand.leaderboard(B)
    assert (row["verified"], row["self_reported"], row["mismatch"]) == (1, 0, 0)
    assert row["flags"]["unverified"] == 0 and row["flags"]["mismatch"] == 0
    assert checks.check_candidates().errors == []


def test_a_mismatch_is_written_as_failed(root, capsys):
    doc = result(root)
    assert verify.verify(TEST, B, NAME, "tt_nom_27", run=fake_run(root, dict(GOOD, tau_reg_ps=16.0))) == 1
    out = capsys.readouterr().out
    assert "MISMATCH  verification/" in out and "CMP-07: pass self-reported, fail rerun" in out
    rec = json.loads((root / "verification" / B / NAME / TEST / "tt_nom_27.json").read_text())
    assert rec["status"] == "mismatch" and not rec["comparison"]["ok"]
    assert verify.state(doc)["state"] == "mismatch"
    (row,) = cand.leaderboard(B)
    assert (row["verified"], row["mismatch"], row["flags"]["mismatch"]) == (0, 1, 1)
    assert "mismatch" in cand.table([row])
    # a rerun without the job is a mismatch too, never silently nothing
    assert verify.verify(TEST, B, NAME, "tt_nom_27", run=lambda *a, **k: []) == 1
    rec = json.loads((root / "verification" / B / NAME / TEST / "tt_nom_27.json").read_text())
    assert rec["status"] == "mismatch" and "error: not self-reported" in rec["comparison"]["problems"]


def test_what_does_not_verify(root):
    doc = result(root, verified_by="many-question")             # the result's own meta never counts
    assert verify.state(doc) == {"state": "self-reported", "why": "no verification record"}
    assert verify.verify(TEST, B, NAME, "tt_nom_27", run=fake_run(root)) == 0
    assert verify.state(doc)["state"] == "verified"
    # the author changes the self-reported numbers after the verification: compared again, a mismatch
    changed = result(root, metrics=dict(GOOD, energy_fJ=150.0), verified_by="many-question")
    assert verify.state(changed)["state"] == "mismatch" and "energy_fJ" in verify.state(changed)["why"]
    # a stale record (an input it recorded changed) no longer verifies
    p = root / "verification" / B / NAME / TEST / "tt_nom_27.json"
    rec = json.loads(p.read_text())
    rec["meta"]["files"]["tb/x.scs"] = "dead"
    p.write_text(json.dumps(rec))
    assert verify.state(doc)["state"] == "self-reported" and "stale (tb/x.scs)" in verify.state(doc)["why"]
    # a new netlist: the record is of another netlist
    rec["meta"]["files"].pop("tb/x.scs")
    p.write_text(json.dumps(rec))
    assert verify.state(doc)["state"] == "verified"
    (root / NL).write_text((root / NL).read_text().replace("w=2u", "w=3u"))
    assert verify.state(doc) == {"state": "self-reported", "why": "the verification record is of another netlist"}


def test_record_problems_in_check_candidates(root):
    result(root)
    assert verify.verify(TEST, B, NAME, "tt_nom_27", run=fake_run(root)) == 0
    p = root / "verification" / B / NAME / TEST / "tt_nom_27.json"
    rec = json.loads(p.read_text())
    (p.parent / "ss_low_125.json").write_text(json.dumps(rec))                  # copied: path and content disagree
    (p.parent / "notes.txt").write_text("x")
    orphan = dict(rec, corner="ff_high_125", job="ff_high_125",
                  verifies=dict(rec["verifies"], result=f"results/{B}/{TEST}/xtor-{NAME}/ff_high_125.json"))
    (p.parent / "ff_high_125.json").write_text(json.dumps(orphan))
    r = checks.check_candidates()
    text = "\n".join(r.errors)
    assert "ss_low_125.json: {" in text and "do not match its path" in text and "verifies.result must be" in text
    assert "notes.txt: verification/ holds only" in text
    assert r.warnings == [f"verification/{B}/{NAME}/{TEST}/ff_high_125.json: the result it verifies "
                          f"(results/{B}/{TEST}/xtor-{NAME}/ff_high_125.json) does not exist"]


def test_cli_dry_run(root, capsys):
    result(root)
    assert main(["verify", TEST, "--block", B, "--candidate", NAME, "--corners", "typ", "--dry-run"]) == 0
    assert f"1 result(s) on netlist {nl_hash(root)}: tt_nom_27" in capsys.readouterr().out
    assert main(["verify", TEST, "--candidate", NAME, "--corners", "quick", "--dry-run"]) == 1
    assert not (root / "verification").exists()


def test_monte_carlo_results_rerun_with_their_samples_and_seed(root):
    """CMP-03 (tb_comp_offset_mc): verified like the others; the rerun gets the recorded runs and seed,
    the per-sample offsets compare one by one, and the Monte Carlo verdict needs every sample."""
    mt = "tb_comp_offset_mc"
    offs = [round(0.1 * i - 2.5, 3) for i in range(50)]
    good = {"mc_runs": 50, "mc_ok": 50, "mc_failed": 0, "offset_sigma_mV": 1.5, "offset_mean_mV": 0.0,
            "offset_max_abs_mV": 2.5, "offsets_mV": offs, "sample_status": ["ok"] * 50}
    doc = result(root, metrics=good, test=mt, mc=dict(MC))
    assert verify.required_corners(blocks()[B], mt) == ["tt_nom_27"]
    calls = []
    assert verify.verify(mt, B, NAME, run=fake_run(root, good, calls)) == 0
    assert calls == [(mt, B, "tt_nom_27", {B: f"xtor:{NAME}"}, "aps", False, {"runs": 50, "seed": 7})]
    rec = json.loads((root / "verification" / B / NAME / mt / "tt_nom_27.json").read_text())
    assert rec["status"] == "match" and rec["specs"]["CMP-03"]["samples"] == {"ok": 50, "failed": 0, "need": 50}
    assert rec["comparison"]["metrics"]["offsets_mV"]["n"] == 50 and verify.state(doc)["state"] == "verified"
    # one sample's offset moved: a mismatch, whatever sigma does
    moved = dict(good, offsets_mV=offs[:10] + [offs[10] + 1.0] + offs[11:])
    assert verify.verify(mt, B, NAME, run=fake_run(root, moved)) == 1
    assert verify.state(doc)["state"] == "mismatch" and "offsets_mV: 1 of 50 values differ" in verify.state(doc)["why"]
    # a failed sample in the rerun fails CMP-03 there: the verdicts differ
    failed = dict(good, mc_ok=49, mc_failed=1, sample_status=["ok"] * 49 + ["failed"], offsets_mV=offs[:49] + [None])
    assert verify.verify(mt, B, NAME, run=fake_run(root, failed)) == 1
    assert verify.state(doc)["why"].startswith("CMP-03: pass self-reported, fail rerun")
    # other Monte Carlo settings in the rerun: a mismatch
    c = verify.compare(doc, {**doc, "meta": {**doc["meta"], "mc": dict(MC, seed=8)}})
    assert any(p.startswith("Monte Carlo settings differ") for p in c["problems"])
