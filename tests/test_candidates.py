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
    # plain xtor: the legacy single view until the block is migrated ...
    assert cand.resolve(BLOCK, "xtor") == (blocks()[BLOCK].view_path("xtor"), "xtor")
    # ... then the selected candidate
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "alice")
    assert cand.resolve(BLOCK, "xtor") == (path, "xtor-alice")
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "none")
    monkeypatch.delitem(blocks()[BLOCK].raw["views"], "xtor")
    with pytest.raises(cand.ViewError, match="no candidate is selected"):
        cand.resolve(BLOCK, "xtor")


def test_runner_uses_candidates(root):
    _make(root)
    b = blocks()
    assert runner._viewsig(b[BLOCK], {BLOCK: "xtor:alice"}) == "xtor-alice"
    assert runner._viewsig(b[BLOCK], {}) == "behav"
    assert runner._viewsig(b["adc_top"], {BLOCK: "xtor:alice"}) == "xtor-comp@alice"
    assert runner._viewsig(b["adc_top"], {BLOCK: "xtor:alice", "adc_ref": "xtor"}) == "xtor-comp@alice+ref"
    assert runner._viewsig(b["adc_top"], {}) == "behav"
    legacy = {n: "xtor" for n in b if n != "adc_top"}
    assert runner._viewsig(b["adc_top"], legacy) == "xtor"
    files = runner.view_files({BLOCK: "xtor:alice"})
    assert root / "design" / "xtor" / BLOCK / "alice" / f"{BLOCK}.scs" in files


def test_selected_field(monkeypatch):
    from adcflow.specs import SpecError, _load_block

    b = blocks()[BLOCK]
    assert b.selected is None
    monkeypatch.setitem(b.raw, "selected", "none")
    assert b.selected is None
    monkeypatch.setitem(b.raw, "selected", "alice")
    assert b.selected == "alice"
    import tempfile
    from pathlib import Path
    text = b.path.read_text(encoding="utf-8").replace("owner:", "selected: Not_A_Name\nowner:", 1)
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / f"{BLOCK}.yaml"
        p.write_text(text, encoding="utf-8")
        with pytest.raises(SpecError, match="selected"):
            _load_block(p)
        p.write_text(text.replace("Not_A_Name", "alice"), encoding="utf-8")
        assert _load_block(p).selected == "alice"             # accepted next to owner:


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
            "wrong_decisions": 0, "energy_fJ": 100.0}
    _result(root, "tb_comp_delay", "xtor-alice", **good)
    _result(root, "tb_comp_delay", "xtor-alice", "ss_low_125", verified=True, **dict(good, tdelay_1mV_ps=130.0))
    _result(root, "tb_top_sine", "xtor-comp@alice", block="adc_top", enob=10.9)
    (row,) = cand.leaderboard(BLOCK)
    specs = [s for s in blocks()[BLOCK].specs]
    assert row["specs_total"] == len(specs)
    assert row["specs_failed"] == 1                         # CMP-05 at ss_low_125: 130 > 120
    assert row["specs_passed"] == 3                         # CMP-04, CMP-06, CMP-10 (typ only, recorded)
    assert row["worst_margin"]["spec"] == "CMP-05" and row["worst_margin"]["margin"] == pytest.approx(-10 / 120)
    assert row["coverage"][0] == 3 + 4 * 2                  # typ specs 1 corner each, all-corner specs 2 of 45
    assert row["results"] == 2 and row["self_reported"] == 1 and row["flags"]["unverified"] == 1
    assert row["power_uW"] == pytest.approx(100e-15 * 14 * 100e6 * 1e6)
    assert row["area"] == {"devices": 4, "mos": 3, "wl_um2": pytest.approx(2 * 0.06 + 0.04), "caps": 1,
                           "cap_F": pytest.approx(5e-15)}
    assert row["top_enob_margin"] == pytest.approx(10.9 - 10.75)  # TOP-02 is the tightest ENOB limit
    assert "self-reported" in cand.table([row])
    _result(root, "tb_top_sine", "xtor-comp@alice", "ss_low_125", block="adc_top", enob=10.6)
    assert cand.top_enob_margin(BLOCK, "alice") == pytest.approx(10.6 - 10.5)  # TOP-01 there, not TT-only TOP-02


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
