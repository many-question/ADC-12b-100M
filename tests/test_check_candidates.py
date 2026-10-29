"""`check candidates` (open-candidates row 2, docs/proposals/open-candidates.md §2): PR rules on
fixture diffs (base files -> head files) and the content rules of a candidate."""

import json
import shutil
import subprocess

import pytest
import yaml

from adcflow import REPO_ROOT, checks
from adcflow import candidates as cand
from adcflow.specs import blocks

B = "adc_comp"
PORTS = " ".join(blocks()[B].port_names)
NET = (f"simulator lang=spectre\nsubckt {B} ({PORTS})\n"
       "MN1 (OUTP INP VSS VSS) nch_ulvt_mac w=1u l=30n\nC0 (OUTP VSS) capacitor c=2f\nends {B}\n").replace("{B}", B)


def _yaml(name, *logins, **over):
    m = {"name": name, "description": "A latch.", "status": "wip",
         "authors": [{"github": g} for g in logins]}
    m.update(over)
    return yaml.safe_dump(m)


def _cand(name, *logins, net=NET, **over):
    d = f"design/xtor/{B}/{name}/"
    return {d + f"{B}.scs": net, d + "candidate.yaml": _yaml(name, *logins, **over)}


def _res(name, corner="tt_nom_27", **over):
    doc = {"block": B, "test": "tb_comp_delay", "view": f"xtor-{name}", "corner": corner, "metrics": {}}
    doc.update(over)
    return {f"results/{B}/tb_comp_delay/xtor-{name}/{corner}.json": json.dumps(doc)}


def run(base: dict, head: dict, author: str) -> list[str]:
    """pr_problems for the diff base -> head (path -> text or bytes)."""
    enc = {p: v.encode() if isinstance(v, str) else v for p, v in head.items()}
    benc = {p: v.encode() if isinstance(v, str) else v for p, v in base.items()}
    changed = sorted((set(benc) ^ set(enc)) | {p for p in set(benc) & set(enc) if benc[p] != enc[p]})
    return cand.pr_problems(changed, author, lambda p: base.get(p),
                            lambda b, n: {p: v for p, v in enc.items() if cand.owner_of_path(p) == (b, n)})


def has(errs, text):
    return any(text in e for e in errs)


# ------------------------------------------------------------------ the cases of the plan
def test_valid_new_candidate():
    assert run({}, {**_cand("alice-sa", "alice"), **_res("alice-sa")}, "alice") == []


def test_update_by_an_author():
    base = _cand("alice-sa", "alice", "bob")
    head = {**_cand("alice-sa", "alice", "bob", net=NET.replace("w=1u", "w=2u")), **_res("alice-sa")}
    assert run(base, head, "bob") == []
    assert run(base, head, "Bob") == []                                   # logins are case-insensitive


def test_update_by_a_non_author():
    base = _cand("alice-sa", "alice")
    head = _cand("alice-sa", "alice", net=NET.replace("w=1u", "w=2u"))
    assert has(run(base, head, "carol"), "@carol is not an author of this candidate")


def test_no_exemption_for_the_lead_account():
    base = _cand("alice-sa", "alice")
    head = _cand("alice-sa", "alice", net=NET.replace("w=1u", "w=2u"))
    assert has(run(base, head, "many-question"), "@many-question is not an author")


def test_two_candidates_in_one_pr():
    errs = run({}, {**_cand("alice-sa", "alice"), **_cand("alice-sb", "alice")}, "alice")
    assert has(errs, "changes 2 candidates")


@pytest.mark.parametrize("path", ["specs/blocks/adc_comp.yaml", "tools/adcflow/runner.py", "tb/comp/tb_comp_delay.scs",
                                  ".github/workflows/ci.yml", "docs/specs.md", "results/adc_comp/tb_comp_delay/xtor/x.json",
                                  "results/adc_top/tb_top_sine/xtor-comp@alice-sa/tt_nom_27.json",
                                  "design/xtor/adc_comp/adc_comp.scs"])
def test_candidate_pr_touching_anything_else(path):
    errs = run({}, {**_cand("alice-sa", "alice"), path: "x"}, "alice")
    assert has(errs, f"{path}: a candidate PR may only change")


def test_candidate_pr_touching_verification_records():
    rec = f"verification/{B}/alice-sa/tb_comp_delay/tt_nom_27.json"
    errs = run({}, {**_cand("alice-sa", "alice"), **_res("alice-sa"), rec: "{}"}, "alice")
    assert has(errs, f"{rec}: verification records are written by the lead (adcflow verify)")
    assert run({}, {rec: "{}"}, "many-question") == []                     # a lead PR: the lead reviews it


def test_verified_by_in_a_candidate_result():
    errs = run({}, {**_cand("alice-sa", "alice"), **_res("alice-sa", meta={"verified_by": "many-question"})}, "alice")
    assert has(errs, "meta.verified_by is not allowed in a candidate's result")
    base = {**_cand("alice-sa", "alice"), **_res("alice-sa", meta={})}
    errs = run(base, {**_cand("alice-sa", "alice"), **_res("alice-sa", meta={"verified_by": "x"})}, "alice")
    assert has(errs, "meta.verified_by is not allowed")


def test_include_in_a_netlist():
    net = NET.replace("subckt", 'include "models.scs"\nsubckt', 1)
    assert has(run({}, _cand("alice-sa", "alice", net=net), "alice"), 'include "models.scs" is not allowed')
    net = NET.replace("subckt", 'ahdl_include "x.va"\nsubckt', 1)
    assert has(run({}, _cand("alice-sa", "alice", net=net), "alice"), 'ahdl_include "x.va" is not allowed')


def test_authors_change():
    base = _cand("alice-sa", "alice")
    for head in (_cand("alice-sa", "alice", "bob"),                       # add a co-author
                 _cand("alice-sa", "alice", authors=[{"github": "alice", "name": "agent-2"}])):  # rename
        assert has(run(base, head, "alice"), "authors may not change in a candidate PR")


def test_lead_pr_without_candidate_paths():
    for author in ("many-question", "alice"):
        assert run({"specs/blocks/adc_comp.yaml": "a"}, {"specs/blocks/adc_comp.yaml": "b", "tools/x.py": "y"},
                   author) == []


# ------------------------------------------------------------------ further rules
def test_new_candidate_rules():
    assert has(run({}, _cand("bob-sa", "alice"), "alice"), "name starts with the PR author's login")
    assert has(run({}, _cand("alice-sa", "bob"), "alice"), "@alice must be in authors[].github of a new candidate")
    head = _cand("alice-sa", "alice")
    del head[f"design/xtor/{B}/alice-sa/candidate.yaml"]
    assert has(run({}, head, "alice"), "a new candidate needs candidate.yaml")
    assert run({}, _cand("alice", "alice"), "alice") == []                # the login alone is a name


def test_deleting_a_candidate_is_a_lead_change():
    assert has(run(_cand("alice-sa", "alice"), {}, "alice"), "may not delete a candidate")


def test_content_rules():
    va = NET.replace("nch_ulvt_mac", "adc_comp_va")
    assert has(run({}, _cand("alice-sa", "alice", net=va), "alice"), "uses adc_comp_va: only PDK devices")
    top = NET + "X0 (A B) nch_ulvt_mac\n"
    assert has(run({}, _cand("alice-sa", "alice", net=top), "alice"), "outside a subcircuit")
    head = {**_cand("alice-sa", "alice"), f"design/xtor/{B}/alice-sa/run.sh": "x",
            f"design/xtor/{B}/alice-sa/sub/a.md": "x",
            f"design/xtor/{B}/alice-sa/big.png": b"\x89PNG" + b"0" * 250_000,
            f"results/{B}/tb_comp_delay/xtor-alice-sa/raw.tran": "x"}
    errs = run({}, head, "alice")
    assert has(errs, "run.sh: only adc_comp.scs, candidate.yaml")
    assert has(errs, "no subdirectories") and has(errs, "big.png: 250 kB")
    assert has(errs, "raw.tran: results of a candidate are .json and .png")
    errs = run({}, {**_cand("alice-sa", "alice"), **_res("alice-sa", view="xtor-bob")}, "alice")
    assert has(errs, "do not match its path")
    assert has(run({}, _cand("alice-sa", "alice", status="done"), "alice"), "status")


def test_adc_top_has_no_candidates():
    head = {"design/xtor/adc_top/alice/adc_top.scs": "x"}
    assert has(run({}, head, "alice"), "adc_top is not a block that can have candidates")


# ------------------------------------------------------------------ on disk and through git
def test_disk_rules_cover_every_candidate(tmp_path, monkeypatch):
    monkeypatch.setattr(cand, "ROOT", tmp_path)
    shutil.copytree(REPO_ROOT / "design" / "rnl", tmp_path / "design" / "rnl")
    for p, v in {**_cand("alice-sa", "alice", net=NET.replace("subckt", 'include "m.scs"\nsubckt', 1)),
                 **_res("orphan")}.items():
        (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / p).write_text(v)
    errs = cand.disk_problems()
    assert has(errs, 'include "m.scs" is not allowed')
    assert has(errs, "results/adc_comp/*/xtor-orphan/: no candidate")


def _git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def test_check_candidates_through_git(tmp_path, monkeypatch):
    """The CLI path: merge base, changed files and base candidate.yaml come from git."""
    shutil.copytree(REPO_ROOT / "design" / "rnl", tmp_path / "design" / "rnl")
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@example.org")
    _git(tmp_path, "config", "user.name", "t")

    def write(files):
        for p, v in files.items():
            (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
            (tmp_path / p).write_text(v)
        _git(tmp_path, "add", "-A")
        _git(tmp_path, "commit", "-q", "-m", "x")

    write(_cand("alice-sa", "alice"))
    _git(tmp_path, "checkout", "-q", "-b", "pr")
    write({**_cand("alice-sa", "alice", net=NET.replace("w=1u", "w=3u")), **_res("alice-sa")})
    monkeypatch.setattr(cand, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    assert checks.check_candidates("main", "alice").errors == []
    errs = checks.check_candidates("main", "bob").errors
    assert errs == ["adc_comp/alice-sa: @bob is not an author of this candidate (base candidate.yaml)"]
    assert checks.check_candidates().errors == []                          # no PR: content rules only
