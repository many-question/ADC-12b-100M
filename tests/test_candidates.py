"""Transistor-level candidates (docs/proposals/open-candidates.md): candidate.yaml, views and
result paths, port contracts, scoring and migration of a legacy view. Every test works in a
temporary repository root (candidates.ROOT, checks.REPO_ROOT)."""

import json

import pytest
import yaml

from adcflow import candidates as cand
from adcflow import checks, runner
from adcflow.netlist import content_hash
from adcflow.specs import blocks

BLOCK = "adc_comp"
SLASH = "/"                       # site-like strings are assembled so this file stays clean


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(cand, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    for b in blocks().values():             # main's selections name candidates this tree does not have
        if b.raw.get("selected") not in (None, "none"):
            monkeypatch.setitem(b.raw, "selected", "none")
            monkeypatch.setitem(b.raw, "status", "behavioral")
    return tmp_path


def _netlist(ports=None, body="MN1 (OUTP INP VSS VSS) nch_ulvt_mac w=2u l=30n m=2\n"
                             "MP1 (OUTP CLKC AVDD AVDD) pch_ulvt_mac w=1u l=40n\n"
                             "C0 (OUTP VSS) capacitor c=5f\n"):
    ports = ports or blocks()[BLOCK].port_names
    return f"simulator lang=spectre\nsubckt {BLOCK} ({' '.join(ports)})\n{body}ends {BLOCK}\n"


def _meta(name="alice", **over):
    m = {"name": name, "description": "Strong-arm latch.", "status": "wip", "acknowledged": [36],
         "authors": [{"github": "alice", "name": "agent-3"}]}
    m.update(over)
    return m


def _make(root, name="alice", meta=None, netlist=None, block=BLOCK):
    d = root / "design" / "xtor" / block / name
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{block}.scs").write_text(netlist if netlist is not None else _netlist())
    (d / "candidate.yaml").write_text(yaml.safe_dump(meta if meta is not None else _meta(name)))
    return d


def _result(root, test, view, corner="tt_nom_27", block=BLOCK, verified=False, **metrics):
    d = root / "results" / block / test / view
    d.mkdir(parents=True, exist_ok=True)
    meta = {"files": {}, "mc": None}
    if verified:
        meta["verified_by"] = "many-question"
    doc = {"block": block, "test": test, "view": view, "corner": corner, "metrics": metrics,
           "globals": {"vdd": 0.9, "vdd18": 1.8}, "meta": meta}
    (d / f"{corner}.json").write_text(json.dumps(doc))
    return d / f"{corner}.json"


# ------------------------------------------------------------------ candidate.yaml
def test_valid_candidate_and_author_text(root):
    _make(root)
    (c,) = cand.candidates(BLOCK)
    assert c.problems == [] and c.status == "wip"
    assert c.author_text() == "agent-3 (@alice)"
    c2 = cand.Candidate(BLOCK, "x", {"authors": [{"github": "bob"}]})
    assert c2.author_text() == "@bob"


def test_one_login_may_author_several_candidates(root):
    _make(root, "alice")
    _make(root, "alice-strongarm", _meta("alice-strongarm", authors=[{"github": "alice", "name": "agent-7"}]))
    assert [(c.name, c.problems) for c in cand.candidates(BLOCK)] == [("alice", []), ("alice-strongarm", [])]


@pytest.mark.parametrize("over, msg", [
    ({"name": "bob"}, "must be the directory name"),
    ({"status": "done"}, "status"),
    ({"description": ""}, "description"),
    ({"acknowledged": ["#36"]}, "issue numbers"),
    ({"authors": []}, "at least one"),
    ({"authors": [{"github": "not a login"}]}, "not a GitHub login"),
    ({"authors": [{"github": "alice", "email": "x"}]}, "authors[0] must be"),
    ({"authors": [{"github": "alice", "name": "x" * 65}]}, "at most 64"),
    ({"authors": [{"github": "alice", "name": SLASH.join(["", "home", "agent"])}]}, "absolute home path"),
    ({"owner": "alice"}, "unknown keys"),
])
def test_invalid_candidate_yaml(root, over, msg):
    _make(root, meta=_meta(**over))
    (c,) = cand.candidates(BLOCK)
    assert any(msg in p for p in c.problems), c.problems


def test_invalid_name_and_missing_netlist(root):
    d = _make(root, "Bad_Name", _meta("Bad_Name"))
    assert any("[a-z0-9-]" in p for p in cand.load(BLOCK, "Bad_Name").problems)
    (d / f"{BLOCK}.scs").unlink()
    assert any("netlist adc_comp.scs missing" in p for p in cand.load(BLOCK, "Bad_Name").problems)


# ------------------------------------------------------------------ views and result paths
def test_view_keys_resolve_to_candidates_and_result_dirs(root, monkeypatch):
    _make(root)
    path, d = cand.resolve(BLOCK, "xtor:alice")
    assert path == root / "design" / "xtor" / BLOCK / "alice" / f"{BLOCK}.scs" and d == "xtor-alice"
    assert cand.resolve(BLOCK, "behav")[1] == "behav"
    with pytest.raises(cand.ViewError, match="no candidate 'bob'"):
        cand.resolve(BLOCK, "xtor:bob")
    # plain xtor: the selected candidate; with selected: none an error (no legacy views on main) ...
    with pytest.raises(cand.ViewError, match="no candidate is selected"):
        cand.resolve(BLOCK, "xtor")
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "alice")
    assert cand.resolve(BLOCK, "xtor") == (path, "xtor-alice")
    # ... and a legacy single view (views.xtor) is still read while nothing is selected
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "none")
    monkeypatch.setitem(blocks()[BLOCK].raw["views"], "xtor", "design/xtor/adc_comp/adc_comp.scs")
    assert cand.resolve(BLOCK, "xtor") == (blocks()[BLOCK].view_path("xtor"), "xtor")


def test_runner_uses_candidates(root, monkeypatch):
    _make(root)
    b = blocks()
    for n in b:                                           # legacy single views, as before migration
        if n != "adc_top":
            monkeypatch.setitem(b[n].raw["views"], "xtor", f"design/xtor/{n}/{n}.scs")
    assert runner._viewsig(b[BLOCK], {BLOCK: "xtor:alice"}) == "xtor-alice"
    assert runner._viewsig(b[BLOCK], {}) == "behav"
    assert runner._viewsig(b["adc_top"], {BLOCK: "xtor:alice"}) == "xtor-comp@alice"
    assert runner._viewsig(b["adc_top"], {BLOCK: "xtor:alice", "adc_ref": "xtor"}) == "xtor-comp@alice+ref"
    assert runner._viewsig(b["adc_top"], {}) == "behav"
    legacy = {n: "xtor" for n in b if n != "adc_top"}
    assert runner._viewsig(b["adc_top"], legacy) == "xtor"
    files = runner.view_files({BLOCK: "xtor:alice"})
    assert root / "design" / "xtor" / BLOCK / "alice" / f"{BLOCK}.scs" in files


def test_selected_field(monkeypatch, tmp_path):
    """Every block except adc_top has selected: (open-candidates row 4); owner: is retired for them.
    A selected candidate exists, and only a selected block leaves `behavioral`."""
    import re

    from adcflow.specs import SpecError, _load_block

    for name, b in blocks().items():
        if name == "adc_top":
            assert b.raw["owner"] == "many-question" and "selected" not in b.raw
        else:
            assert "owner" not in b.raw and "xtor" not in b.views    # no legacy single views
            if b.raw["selected"] == "none":
                assert b.status == "behavioral"
            else:
                assert cand.netlist_path(name, b.raw["selected"]).exists() and b.status != "behavioral"
    b = blocks()[BLOCK]
    assert b.selected is None
    monkeypatch.setitem(b.raw, "selected", "alice")
    assert b.selected == "alice"
    text = b.path.read_text(encoding="utf-8")
    p = tmp_path / f"{BLOCK}.yaml"

    def load(t):
        p.write_text(t, encoding="utf-8")
        return _load_block(p)

    sel = re.compile(r"^selected: .*$", re.M)
    assert load(sel.sub("selected: alice", text)).selected == "alice"
    for bad, msg in ((sel.sub("selected: Not_A_Name", text), "selected: must be"),
                     (sel.sub("", text), "selected: must be"),                         # required
                     (sel.sub("selected: none\nowner: alice", text), "owner: is retired"),
                     (text.replace("status: behavioral", "status: xtor-review"), "needs a selected candidate"),
                     (text.replace("status: behavioral", "status: xtor-wip"), "status 'xtor-wip'")):
        with pytest.raises(SpecError, match=msg):
            load(bad)
    top = blocks()["adc_top"].path.read_text(encoding="utf-8")
    p = tmp_path / "adc_top.yaml"
    for bad, msg in ((top.replace("owner: many-question", "owner: not a login"), "adc_top needs owner"),
                     (top.replace("owner: many-question", "owner: many-question\nselected: none"), "keeps owner")):
        p.write_text(bad, encoding="utf-8")
        with pytest.raises(SpecError, match=msg):
            _load_block(p)


# ------------------------------------------------------------------ checks
def test_port_check_walks_every_candidate(root, monkeypatch):
    from adcflow import REPO_ROOT
    monkeypatch.setattr(checks, "REPO_ROOT", REPO_ROOT)        # the real views; candidates under root
    _make(root, "alice")
    assert checks.check_ports().errors == []
    _make(root, "bob", _meta("bob", authors=[{"github": "bob"}]), _netlist(ports=["INP", "INN", "CLKC"]))
    _make(root, "carol", _meta("carol", status="maybe"))
    errs = checks.check_ports().errors
    assert any("bob/adc_comp.scs: ports of adc_comp differ" in e for e in errs)
    assert any("carol/candidate.yaml: status" in e for e in errs)
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "dave")
    assert any("selected candidate 'dave' does not exist" in e for e in checks.check_ports().errors)


def test_rnl_check_walks_candidate_directories(root, monkeypatch):
    monkeypatch.setattr(checks, "REPO_ROOT", root)
    _make(root)
    assert root / "design" / "xtor" / BLOCK / "alice" / f"{BLOCK}.scs" in checks._netlists()


# ------------------------------------------------------------------ scoring
def test_score(root):
    _make(root)
    good = {"tdelay_1mV_ps": 60.0, "tdelay_30mV_ps": 30.0, "tau_reg_ps": 10.0, "treset_ps": 20.0,
            "wrong_decisions": 0, "energy_fJ": 100.0, "validity_violations": 0, "loser_peak_pct": 1.0}
    _result(root, "tb_comp_delay", "xtor-alice", **good)
    _result(root, "tb_comp_delay", "xtor-alice", "ss_low_125", verified=True, **dict(good, tdelay_1mV_ps=130.0))
    _result(root, "tb_top_sine", "xtor-comp@alice", block="adc_top", enob=10.9)
    (row,) = cand.leaderboard(BLOCK)
    specs = [s for s in blocks()[BLOCK].specs]
    n_rep = sum(s.reported for s in specs)                  # CMP-10, CMP-16: reported only, no verdict
    assert row["specs_total"] == len(specs) - n_rep and row["reported_total"] == n_rep
    assert row["specs_failed"] == 1 and row["specs_failing"] == ["CMP-05"]   # CMP-05 at ss_low_125: 130 > 120
    assert row["specs_passed"] == 2                         # CMP-04, CMP-06 (typ only, recorded)
    assert row["specs_reported"] == 1 and "CMP-10" not in row["specs_missing"]      # energy_fJ recorded at TT
    assert "CMP-16" in row["specs_missing"]                 # reported at all corners: 2 of 45 recorded
    assert row["specs_incomplete"] == len(row["specs_missing"]) == len(specs) - 4
    assert row["worst_margin"]["spec"] == "CMP-05" and row["worst_margin"]["margin"] == pytest.approx(-10 / 120)
    n_all = sum(s.test == "tb_comp_delay" and s.corners == "all" for s in specs)    # CMP-05/07/08/09/15/16
    assert row["coverage"][0] == 3 + n_all * 2              # typ specs 1 corner each, all-corner specs 2 of 45
    # meta.verified_by in a result is not trusted: only a verification record verifies (tests/test_verify.py)
    assert row["results"] == 2 and row["self_reported"] == 2 and row["flags"]["unverified"] == 2
    assert row["verified"] == 0 and row["mismatch"] == 0 and row["flags"]["mismatch"] == 0
    assert row["power_uW"] == pytest.approx(100e-15 * 14 * 100e6 * 1e6)
    assert row["area"] == {"devices": 4, "mos": 3, "wl_um2": pytest.approx(2 * 0.06 + 0.04), "caps": 1,
                           "cap_F": pytest.approx(5e-15)}
    assert row["top_enob_margin"] == pytest.approx(10.9 - 10.75)  # TOP-02 is the tightest ENOB limit
    assert "self-reported" in cand.table([row])
    # not eligible: a failing and incomplete specs, self-reported results, no complete mixed top-level regression
    assert not row["eligible"] and [m["what"] for m in row["missing"]] == ["failing", "incomplete", "unverified", "top"]
    assert row["top_regression"]["status"] == "fail" and row["top_regression"]["results"] == 1     # only enob recorded
    text = cand.table([row])
    assert "adc_comp -- not eligible" in text and "missing: fails CMP-05;" in text and "eligible, ranked" not in text
    _result(root, "tb_top_sine", "xtor-comp@alice", "ss_low_125", block="adc_top", enob=10.6)
    assert cand.top_enob_margin(BLOCK, "alice") == pytest.approx(10.6 - 10.5)  # TOP-01 there, not TT-only TOP-02


TOP_GOOD = {"enob": 10.9, "sfdr_dBc": 85.0, "fs_peak_V": 0.99, "missing_rdy": 0, "t_conv_max_ns": 2.9, "spike_count": 0}


def _top(root, test, job, view="xtor-comp@alice", **metrics):
    """A top-level result of the mixed regression (results/adc_top/<test>/<view>/<job>.json)."""
    d = root / "results" / "adc_top" / test / view
    d.mkdir(parents=True, exist_ok=True)
    doc = {"block": "adc_top", "test": test, "view": view, "corner": job.split("__")[0], "metrics": {**TOP_GOOD, **metrics},
           "globals": {"vdd": 0.9, "vdd18": 1.8}, "meta": {"files": {}, "mc": None}}
    (d / f"{job}.json").write_text(json.dumps(doc))
    return d / f"{job}.json"


def _full_top(root, **kw):
    from adcflow.corners import corner_names

    quick = sorted(corner_names("quick"))
    out = [_top(root, "tb_top_sine", c, **kw) for c in quick]
    out += [_top(root, "tb_top_duty", f"{c}__duty{d}", **kw) for c in quick for d in ("0.45", "0.55")]
    return out + [_top(root, "tb_top_sine_lf", "tt_nom_27", **kw)]


def test_mixed_top_level_regression(root):
    """tb_top_sine and tb_top_duty at the quick corners, tb_top_sine_lf at TT, with only this candidate swapped in."""
    r = cand.top_regression(BLOCK, "alice")
    assert r["status"] == "none" and r["results"] == 0 and len(r["missing"]) == 7 + 7 + 1    # corners, not jobs
    _top(root, "tb_top_sine", "tt_nom_27")
    r = cand.top_regression(BLOCK, "alice")
    assert r["status"] == "incomplete" and len(r["missing"]) == 6 + 7 + 1
    assert "tb_top_sine ss_low_125" in r["missing"] and "tb_top_sine_lf tt_nom_27" in r["missing"]
    assert not any(m.startswith("tb_top_sine tt_nom_27") for m in r["missing"])
    paths = _full_top(root)
    assert cand.top_regression(BLOCK, "alice")["status"] == "pass" and cand.top_regression(BLOCK, "alice")["results"] == 22
    assert cand.top_regression(BLOCK, "bob")["status"] == "none"                 # another candidate's runs are its own
    _top(root, "tb_top_sine", "ss_low_125", enob=10.2)                             # TOP-01 >= 10.5 fails there
    r = cand.top_regression(BLOCK, "alice")
    assert r["status"] == "fail" and r["failing"] == ["TOP-01"]
    _top(root, "tb_top_sine", "ss_low_125")
    doc = json.loads(paths[-1].read_text())
    doc["meta"]["files"] = {"specs/arch.yaml": "0" * 16}                          # an input changed since the run
    paths[-1].write_text(json.dumps(doc))
    assert cand.top_regression(BLOCK, "alice")["status"] == "stale"
    _top(root, "tb_top_sine_lf", "tt_nom_27", error="spectre rc=1")
    assert cand.top_regression(BLOCK, "alice")["status"] == "fail"


def test_eligibility_of_a_scored_candidate(root, monkeypatch):
    """Every spec passes at every required corner (the reported CMP-10 recorded), verified, top-level regression passed."""
    from adcflow import verify
    from adcflow.corners import corner_names

    _make(root)
    good = {"tdelay_1mV_ps": 60.0, "tdelay_30mV_ps": 30.0, "tau_reg_ps": 10.0, "treset_ps": 20.0, "wrong_decisions": 0,
            "energy_fJ": 100.0, "validity_violations": 0, "loser_peak_pct": 1.0, "noise_uV": 150.0, "offset_abs_mV": 0.5, "kickback_uV": 10.0, "cin_fF": 10.0,
            "cin_clkc_fF": 10.0, "offset_sigma_mV": 2.0, "mc_ok": 50, "mc_failed": 0}
    mc = {"runs": 50, "seed": 6303, "firstrun": 1, "variations": "mismatch", "models": "local_tt"}
    for test in ("tb_comp_delay", "tb_comp_noise", "tb_comp_kickback"):
        for c in sorted(corner_names("all")):
            _result(root, test, "xtor-alice", c, **good)
    p = _result(root, "tb_comp_offset_mc", "xtor-alice", **good)
    doc = json.loads(p.read_text())
    doc["meta"]["mc"] = mc
    p.write_text(json.dumps(doc))
    _full_top(root)
    monkeypatch.setattr(verify, "state", lambda d: {"state": "verified", "why": ""})     # verification: tests/test_verify.py
    (row,) = cand.leaderboard(BLOCK)
    assert row["eligible"] and row["missing"] == [] and row["specs_passed"] == row["specs_total"]
    assert row["specs_reported"] == row["reported_total"] == sum(s.reported for s in blocks()[BLOCK].specs)
    assert "adc_comp -- eligible" in cand.table([row])
    # the reported metric missing at TT: incomplete, not eligible (power is the ranking key)
    p = root / "results" / BLOCK / "tb_comp_delay" / "xtor-alice" / "tt_nom_27.json"
    doc = json.loads(p.read_text())
    del doc["metrics"]["energy_fJ"]
    p.write_text(json.dumps(doc))
    (row,) = cand.leaderboard(BLOCK)
    assert not row["eligible"] and row["specs_missing"] == ["CMP-10"] and row["power_uW"] is None
    # a value far above the old 200 fJ limit has no verdict: eligible again
    doc["metrics"]["energy_fJ"] = 5000.0
    p.write_text(json.dumps(doc))
    (row,) = cand.leaderboard(BLOCK)
    assert row["eligible"] and row["specs_failed"] == 0


def test_withdrawn_candidates_leave_the_leaderboard(root):
    _make(root, "alice", _meta(status="withdrawn"))
    assert cand.leaderboard(BLOCK) == []
    assert [r["candidate"] for r in cand.leaderboard(BLOCK, withdrawn=True)] == ["alice"]


# ------------------------------------------------------------------ migration
def _legacy(root):
    src = root / "design" / "xtor" / BLOCK
    src.mkdir(parents=True)
    (src / f"{BLOCK}.scs").write_text(_netlist())
    (src / "README.md").write_text("notes\n")
    rel = f"design/xtor/{BLOCK}/{BLOCK}.scs"
    h = content_hash(src / f"{BLOCK}.scs")
    for path, view, block in ((_result(root, "tb_comp_delay", "xtor", tdelay_1mV_ps=60.0), "xtor", BLOCK),
                              (_result(root, "tb_top_sine", "xtor-comp+ref", block="adc_top", enob=10.9),
                               "xtor-comp+ref", "adc_top")):
        doc = json.loads(path.read_text())
        doc["meta"]["files"] = {rel: h, "specs/arch.yaml": "abc"}
        path.write_text(json.dumps(doc))
        (path.parent / "tt_nom_27.delay.png").write_bytes(b"png")
    return h


def test_migrate_moves_view_and_results_keeping_hashes(root):
    h = _legacy(root)
    plan = cand.migrate(BLOCK, "many-question", [{"github": "many-question"}], "First transistor view.", dry=True)
    assert any("xtor -> " in p or "xtor/ -> " in p for p in plan)
    assert (root / "design" / "xtor" / BLOCK / f"{BLOCK}.scs").exists()            # dry run moves nothing
    cand.migrate(BLOCK, "many-question", [{"github": "many-question"}], "First transistor view.")
    new = root / "design" / "xtor" / BLOCK / "many-question"
    assert sorted(p.name for p in new.iterdir()) == ["README.md", f"{BLOCK}.scs", "candidate.yaml"]
    assert cand.load(BLOCK, "many-question").problems == []
    assert not (root / "results" / BLOCK / "tb_comp_delay" / "xtor").exists()
    doc = json.loads((root / "results" / BLOCK / "tb_comp_delay" / "xtor-many-question" / "tt_nom_27.json").read_text())
    key = f"design/xtor/{BLOCK}/many-question/{BLOCK}.scs"
    assert doc["view"] == "xtor-many-question" and doc["meta"]["files"] == {key: h, "specs/arch.yaml": "abc"}
    assert content_hash(new / f"{BLOCK}.scs") == h                     # same content: not stale
    assert doc["meta"]["migrated"]["candidate"] == "many-question"
    assert (root / "results" / BLOCK / "tb_comp_delay" / "xtor-many-question" / "tt_nom_27.delay.png").exists()
    top = root / "results" / "adc_top" / "tb_top_sine" / "xtor-comp@many-question+ref" / "tt_nom_27.json"
    assert json.loads(top.read_text())["view"] == "xtor-comp@many-question+ref"
    assert checks.judge({**doc, "metrics": doc["metrics"]})["stale"] == ["specs/arch.yaml"]   # only the fake hash


def test_migrate_refuses(root):
    with pytest.raises(FileNotFoundError, match="no legacy view"):
        cand.migrate(BLOCK, "x1", [{"github": "a"}], "d")
    _legacy(root)
    with pytest.raises(ValueError, match="candidate name"):
        cand.migrate(BLOCK, "Bad", [{"github": "a"}], "d")
    with pytest.raises(ValueError, match="not a GitHub login"):
        cand.migrate(BLOCK, "x1", [{"github": "a b"}], "d")
    with pytest.raises(ValueError, match="can have candidates"):
        cand.migrate("adc_top", "x1", [{"github": "a"}], "d")
    _make(root, "x1")
    with pytest.raises(FileExistsError):
        cand.migrate(BLOCK, "x1", [{"github": "a"}], "d")
