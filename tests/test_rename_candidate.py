"""Renaming a candidate that is not merged yet (adcflow rename-candidate, CONTRIBUTING §4): the
directory and results move, the results stay fresh, and a merged or verified candidate is refused.
Every test works in a temporary repository root (candidates.ROOT, checks.REPO_ROOT) that is a git
repository with a branch `base`."""

import json
import shutil
import subprocess

import pytest
import yaml

from adcflow import REPO_ROOT, checks, deps
from adcflow import candidates as cand
from adcflow.cli import main
from adcflow.netlist import content_hash
from adcflow.specs import blocks

BLOCK = "adc_comp"
TEST = "tb_comp_delay"


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(cand, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    for b in blocks().values():             # main's selections name candidates this tree does not have
        if b.raw.get("selected") not in (None, "none"):
            monkeypatch.setitem(b.raw, "selected", "none")
            monkeypatch.setitem(b.raw, "status", "behavioral")
    _git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "README.md").write_text("repo\n")
    (tmp_path / "design" / "rnl").mkdir(parents=True)                # the PDK devices a candidate may use
    shutil.copyfile(REPO_ROOT / "design" / "rnl" / "adc28.rnl", tmp_path / "design" / "rnl" / "adc28.rnl")
    _commit(tmp_path, "start")
    _git(tmp_path, "branch", "base")
    return tmp_path


def _git(root, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                          capture_output=True, text=True, check=True).stdout.strip()


def _commit(root, msg):
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", msg)


def _netlist():
    ports = " ".join(blocks()[BLOCK].port_names)
    return (f"simulator lang=spectre\nsubckt {BLOCK} ({ports})\n"
            "MN1 (OUTP INP VSS VSS) nch_ulvt_mac w=2u l=30n m=2\nends adc_comp\n")


def _make(root, name="alice", login="alice"):
    d = root / "design" / "xtor" / BLOCK / name
    d.mkdir(parents=True)
    (d / f"{BLOCK}.scs").write_text(_netlist())
    (d / "candidate.yaml").write_text(
        f"name: {name}\n# kept as written\ndescription: Strong-arm latch.\nstatus: wip\nacknowledged: [36]\n"
        f"authors:\n  - {{github: {login}, name: agent-3}}\n")
    (d / "README.md").write_text(f"Results in results/{BLOCK}/{TEST}/xtor-{name}/.\n")
    return d


def _record(root, name="alice", test=TEST, block=BLOCK, view=None, views=None, corner="tt_nom_27"):
    """A result as runner.run_test records it: meta.files / arch / views of deps.record_meta, the
    files it names outside the candidate copied into the temporary root (checks.judge reads them there)."""
    views = views or {BLOCK: f"xtor:{name}"}
    _, t = next((b, b.tests[test]) for b in blocks().values() if test in b.tests)
    meta = deps.record_meta(t, views, set())
    for f in meta["files"]:
        if not f.startswith("design/xtor/") and not (root / f).exists():
            (root / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO_ROOT / f, root / f)
    view = view or f"xtor-{name}"
    d = root / "results" / block / test / view
    d.mkdir(parents=True, exist_ok=True)
    doc = {"block": block, "test": test, "view": view, "corner": corner, "metrics": {"tdelay_1mV_ps": 60.0},
           "meta": {"git": "abc1234", "git_clean": True, **meta}}
    (d / f"{corner}.json").write_text(json.dumps(doc))
    (d / f"{corner}.delay.png").write_bytes(b"png")
    return d / f"{corner}.json"


def _load(path):
    doc = json.loads(path.read_text())
    doc["_path"] = path
    return doc


# ------------------------------------------------------------------ the move
def test_rename_moves_the_candidate_and_its_results_and_they_stay_fresh(root):
    _make(root)
    old = _record(root)
    assert checks.judge(_load(old))["stale"] == []
    h = content_hash(root / "design" / "xtor" / BLOCK / "alice" / f"{BLOCK}.scs")

    plan = cand.rename(BLOCK, "alice", "alice-st", "base", dry=True)
    assert plan[0] == f"move design/xtor/{BLOCK}/alice/ -> design/xtor/{BLOCK}/alice-st/"
    assert f"move results/{BLOCK}/{TEST}/xtor-alice/ -> results/{BLOCK}/{TEST}/xtor-alice-st/" in plan
    assert any("rewrite 1 result JSONs" in p for p in plan)
    assert any(p.startswith("note:") and "README.md" in p for p in plan)       # free text is not rewritten
    assert old.exists() and not (root / "design" / "xtor" / BLOCK / "alice-st").exists()   # dry run moves nothing

    cand.rename(BLOCK, "alice", "alice-st", "base")
    new_dir = root / "design" / "xtor" / BLOCK / "alice-st"
    assert sorted(p.name for p in new_dir.iterdir()) == ["README.md", f"{BLOCK}.scs", "candidate.yaml"]
    assert not (root / "design" / "xtor" / BLOCK / "alice").exists() and not old.parent.exists()
    text = (new_dir / "candidate.yaml").read_text()
    assert text.startswith("name: alice-st\n# kept as written\n")            # only name: changes
    assert cand.load(BLOCK, "alice-st").problems == []

    new = root / "results" / BLOCK / TEST / "xtor-alice-st" / "tt_nom_27.json"
    assert (new.parent / "tt_nom_27.delay.png").exists()
    doc = _load(new)
    key = f"design/xtor/{BLOCK}/alice-st/{BLOCK}.scs"
    assert doc["view"] == "xtor-alice-st" and doc["meta"]["views"] == {BLOCK: "xtor:alice-st"}
    assert doc["meta"]["files"][key] == h and not any("/alice/" in k for k in doc["meta"]["files"])
    assert {k: doc["meta"]["renamed"][k] for k in ("from", "to")} == {"from": "alice", "to": "alice-st"}
    assert doc["meta"]["git"] == "abc1234" and doc["metrics"] == {"tdelay_1mV_ps": 60.0}
    assert checks.judge(doc)["stale"] == []
    assert cand.tree_problems(BLOCK, "alice-st", cand.disk_files(BLOCK, "alice-st")) == []
    assert cand.disk_problems() == []

    # a hand edit of the netlist after the rename still shows
    (new_dir / f"{BLOCK}.scs").write_text(_netlist().replace("m=2", "m=3"))
    assert checks.judge(_load(new))["stale"] == [key]


def test_without_rename_a_moved_directory_makes_every_result_stale(root):
    _make(root)
    old = _record(root)
    (root / "design" / "xtor" / BLOCK / "alice").rename(root / "design" / "xtor" / BLOCK / "alice-st")
    stale = checks.judge(_load(old))["stale"]
    assert f"design/xtor/{BLOCK}/alice/{BLOCK}.scs" in stale and any("no candidate 'alice'" in s for s in stale)


def test_rename_follows_top_level_results(root):
    _make(root)
    sig = "xtor-comp@alice+ref"
    d = root / "results" / "adc_top" / "tb_top_sine" / sig
    d.mkdir(parents=True)
    doc = {"block": "adc_top", "test": "tb_top_sine", "view": sig, "corner": "tt_nom_27", "metrics": {},
           "meta": {"files": {f"design/xtor/{BLOCK}/alice/{BLOCK}.scs": "h", "specs/arch.yaml": "a"},
                    "views": {BLOCK: "xtor:alice", "adc_ref": "xtor", "adc_cdac": "behav"}}}
    (d / "tt_nom_27.json").write_text(json.dumps(doc))
    other = root / "results" / "adc_top" / "tb_top_sine" / "xtor-comp@alicex"
    other.mkdir()
    assert any("xtor-comp@alice-st+ref" in p for p in cand.rename(BLOCK, "alice", "alice-st", "base", dry=True))
    cand.rename(BLOCK, "alice", "alice-st", "base")
    new = json.loads((root / "results" / "adc_top" / "tb_top_sine" / "xtor-comp@alice-st+ref" / "tt_nom_27.json").read_text())
    assert new["view"] == "xtor-comp@alice-st+ref"
    assert new["meta"]["views"] == {BLOCK: "xtor:alice-st", "adc_ref": "xtor", "adc_cdac": "behav"}
    assert new["meta"]["files"] == {f"design/xtor/{BLOCK}/alice-st/{BLOCK}.scs": "h", "specs/arch.yaml": "a"}
    assert other.exists()                                               # another candidate's run is left alone


def test_cli_dry_run_and_refusal(root, capsys):
    _make(root)
    _record(root)
    assert main(["rename-candidate", BLOCK, "alice", "alice-st", "--base", "base", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert f"would move design/xtor/{BLOCK}/alice/ -> design/xtor/{BLOCK}/alice-st/" in out and "note:" in out
    assert (root / "design" / "xtor" / BLOCK / "alice").exists()
    assert main(["rename-candidate", BLOCK, "alice", "bob", "--base", "base"]) == 1
    assert "starts with an author's login" in capsys.readouterr().err


# ------------------------------------------------------------------ refusals
@pytest.mark.parametrize("new, msg", [
    ("Alice-St", "must match"),
    ("a", "must match"),
    ("bob-st", "starts with an author's login"),
    ("alicex", "starts with an author's login"),
    ("alice-old", "already the name"),
])
def test_refuses_a_bad_new_name(root, new, msg):
    _make(root, "alice-old")
    with pytest.raises(ValueError, match=msg):
        cand.rename(BLOCK, "alice-old", new, "base")
    assert (root / "design" / "xtor" / BLOCK / "alice-old").exists()


def test_refuses_an_existing_destination(root):
    _make(root)
    _make(root, "alice-st")
    with pytest.raises(FileExistsError, match="alice-st exists"):
        cand.rename(BLOCK, "alice", "alice-st", "base")
    shutil.rmtree(root / "design" / "xtor" / BLOCK / "alice-st")
    (root / "results" / BLOCK / TEST / "xtor-alice").mkdir(parents=True)
    (root / "results" / BLOCK / TEST / "xtor-alice-st").mkdir(parents=True)
    with pytest.raises(FileExistsError, match="xtor-alice-st exists"):
        cand.rename(BLOCK, "alice", "alice-st", "base")
    assert (root / "design" / "xtor" / BLOCK / "alice").exists()


def test_refuses_a_missing_candidate_or_block(root):
    with pytest.raises(FileNotFoundError, match="no candidate 'alice'"):
        cand.rename(BLOCK, "alice", "alice-st", "base")
    with pytest.raises(ValueError, match="can have candidates"):
        cand.rename("adc_top", "alice", "alice-st", "base")


def test_refuses_a_candidate_on_the_base_branch(root):
    _make(root)
    _commit(root, "candidate")
    _git(root, "branch", "-f", "base", "HEAD")
    with pytest.raises(ValueError, match="merged candidate is never renamed"):
        cand.rename(BLOCK, "alice", "alice-st", "base")


def test_refuses_a_candidate_on_the_merge_base(root):
    _make(root)
    _commit(root, "candidate")
    _git(root, "switch", "-q", "-c", "later")                  # base moves on and drops the directory
    shutil.rmtree(root / "design" / "xtor" / BLOCK / "alice")
    _commit(root, "drop")
    _git(root, "branch", "-f", "base", "later")
    _git(root, "switch", "-q", "main")
    with pytest.raises(ValueError, match="merged candidate is never renamed"):
        cand.rename(BLOCK, "alice", "alice-st", "base")


def test_refuses_an_unknown_base(root):
    _make(root)
    with pytest.raises(ValueError, match="not a commit here"):
        cand.rename(BLOCK, "alice", "alice-st", "nope")


def test_refuses_a_verified_or_selected_candidate(root, monkeypatch):
    _make(root)
    v = root / "verification" / BLOCK / "alice"
    v.mkdir(parents=True)
    with pytest.raises(ValueError, match=f"verification/{BLOCK}/alice/ exists"):
        cand.rename(BLOCK, "alice", "alice-st", "base")
    shutil.rmtree(v)
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "alice")
    with pytest.raises(ValueError, match="selected candidate"):
        cand.rename(BLOCK, "alice", "alice-st", "base")


# ------------------------------------------------------------------ the PR after a rename
def test_the_renamed_candidate_passes_the_pull_request_rules(root):
    _make(root)
    _record(root)
    cand.rename(BLOCK, "alice", "alice-st", "base")
    files = cand.disk_files(BLOCK, "alice-st")
    errs = cand.pr_problems(sorted(files), "alice", lambda p: None, lambda b, n: cand.disk_files(b, n))
    assert errs == []
    meta = yaml.safe_load((root / "design" / "xtor" / BLOCK / "alice-st" / "candidate.yaml").read_text())
    assert meta["name"] == "alice-st"
