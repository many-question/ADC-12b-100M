"""Candidate leaderboard of the site (site/sitegen/cands.py): ranking, merged candidates, candidates of open PR heads.

Fixture trees and fixture git repositories, no network. The verdicts are main's specs (adcflow.specs of this checkout)."""

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

from adcflow import candidates as C                                  # noqa: E402
from adcflow.netlist import content_hash                              # noqa: E402
from adcflow.specs import blocks                                      # noqa: E402
from sitegen import cands, preview                                    # noqa: E402
from sitegen.data import BlockData, Build                             # noqa: E402
from sitegen.live import PR, Issue, Live                              # noqa: E402

BLOCK = "adc_comp"
NAME = "alice-latch"
TEST = "tb_comp_delay"
NETLIST = f"design/xtor/{BLOCK}/{NAME}/{BLOCK}.scs"
YAML = f"design/xtor/{BLOCK}/{NAME}/candidate.yaml"
RESULT = f"results/{BLOCK}/{TEST}/xtor-{NAME}/tt_nom_27.json"
SCS = ("simulator lang=spectre\nsubckt adc_comp (INP INN CLKC OUTP OUTN AVDD VSS)\nR1 (INP OUTP) resistor r=1k\n"
       "ends adc_comp\n")
CAND_YAML = (f"name: {NAME}\ndescription: A dynamic latch, one stage.\nstatus: wip\nacknowledged: []\n"
             "authors:\n  - {github: alice, name: \"Alice's agent\"}\n")


def row(passed=1, failed=0, incomplete=0, results=1, **kw):
    r = {"block": BLOCK, "candidate": "x", "status": "wip", "specs_passed": passed, "specs_failed": failed,
         "specs_incomplete": incomplete, "specs_total": 3, "coverage": [passed, 3], "results": results, "verified": 0,
         "self_reported": results, "mismatch": 0, "flags": {"stale": 0, "unverified": results, "mismatch": 0, "soa": 0, "error": 0}, "worst_margin": {"margin": 0.3, "spec": "CMP-01"},
         "power_uW": 100.0, "area": {"mos": 10, "wl_um2": 5.0, "caps": 0, "cap_F": 0.0, "devices": 10}, "top_enob_margin": 0.5,
         "author_text": "@a", "description": "", "problems": [], "selected": False}
    r.update(kw)
    return r


def cand(name, source="main", **kw):
    r = row(**kw)
    r["candidate"] = name
    sel = r.pop("selected", False)
    r["selected"] = sel
    return cands.Cand(BLOCK, name, r, source, f"cand-{name}")


def names(cs):
    return [c.name for c in cands.rank(cs)]


# ------------------------------------------------------------------ ranking (§4)
def test_fully_passing_candidates_rank_before_the_others():
    good = cand("good")
    failing = cand("a-failing", failed=1, passed=2)          # more specs passed, but one fails
    stale = cand("b-stale", flags={"stale": 1, "unverified": 1, "mismatch": 0, "soa": 0, "error": 0})
    assert names([failing, stale, good]) == ["good", "a-failing", "b-stale"]


def test_ineligible_candidates_rank_by_passed_specs_then_coverage():
    a = cand("a", passed=1, failed=1, coverage=[5, 9])
    b = cand("b", passed=2, failed=1, coverage=[2, 9])
    c = cand("c", passed=2, failed=1, coverage=[4, 9])
    assert names([a, b, c]) == ["c", "b", "a"]


def test_top_enob_margin_decides_first_with_a_tolerance_of_005_bit():
    hi, lo, close = cand("hi", top_enob_margin=0.80), cand("lo", top_enob_margin=0.30), cand("close", top_enob_margin=0.78)
    assert names([lo, hi]) == ["hi", "lo"]
    # 0.80 vs 0.78 is inside the tolerance: power decides
    close.row["power_uW"], hi.row["power_uW"] = 50.0, 100.0
    assert names([hi, close]) == ["close", "hi"]


def test_power_then_area_then_robustness_each_with_its_tolerance():
    lowp, highp = cand("lowp", power_uW=100.0), cand("highp", power_uW=140.0)
    assert names([highp, lowp]) == ["lowp", "highp"]
    same_p = cand("same-p", power_uW=103.0)                  # within 5 % of 100: area decides
    small = cand("small", power_uW=100.0, area={"mos": 5, "wl_um2": 2.0, "caps": 0, "cap_F": 0.0, "devices": 5})
    assert names([same_p, small]) == ["small", "same-p"]
    robust = cand("robust", worst_margin={"margin": 0.40, "spec": "CMP-02"})
    fragile = cand("fragile", worst_margin={"margin": 0.10, "spec": "CMP-03"})
    assert names([fragile, robust]) == ["robust", "fragile"]
    near = cand("near", worst_margin={"margin": 0.28, "spec": "CMP-04"})        # 0.28 vs 0.30: inside 5 % of the limit
    assert names([near, cand("zz")])[0] == "near"            # tied: name order


def test_missing_values_are_worse_than_any_value():
    none_enob = cand("none-enob", top_enob_margin=None)
    some = cand("some", top_enob_margin=-0.5)
    assert names([none_enob, some]) == ["some", "none-enob"]
    assert names([cand("a-none", power_uW=None, top_enob_margin=None), cand("b-p", power_uW=500.0, top_enob_margin=None)]) == ["b-p", "a-none"]


def test_the_selected_candidate_stays_first_inside_every_tolerance():
    sel = cand("zz-selected", selected=True)
    other = cand("aa-other")
    assert names([other, sel]) == ["zz-selected", "aa-other"]
    assert names([other, cand("zz-selected", selected=True, top_enob_margin=0.9)])[0] == "zz-selected"
    assert cands.rank([cand("p", source="pr", selected=True)])[0].selected is False      # only a merged candidate is selected


def test_count_leaves_withdrawn_out():
    cs = [cand("a"), cand("b", status="withdrawn"), cand("c", source="pr")]
    assert cands.count(cs) == 2


# ------------------------------------------------------------------ fixtures: a site stub and a block's data
def site_stub():
    return SimpleNamespace(build=Build(repo="o/r", sha="m" * 40, short="mmmmmmm", date="", ref=""), fig_prefix="", repo="o/r",
                           prov_scope="本次构建")


def main_data():
    b = blocks()[BLOCK]
    return {BLOCK: BlockData(b, [], {}, [], [])}


def live_with(*issues):
    return Live(ok=True, fetched_at="2026-10-29 06:17", issues={BLOCK: list(issues)} if issues else {})


def result_doc(files_hash, value=50.0, figure="tt_nom_27.delay.png", caption="delay"):
    return {"block": BLOCK, "test": TEST, "view": f"xtor-{NAME}", "corner": "tt_nom_27",
            "metrics": {"tdelay_1mV_ps": value, "tdelay_30mV_ps": 30.0, "tau_reg_ps": 5.0, "treset_ps": 20.0, "energy_fJ": 100.0},
            "globals": {"vdd": 0.9}, "meta": {"git": "abc1234", "files": {NETLIST: files_hash}},
            "figures": [{"file": figure, "caption": caption}]}


def png():
    import struct
    import zlib

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = b"".join(b"\0" + b"\x80" * 3 * 40 for _ in range(40))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 40, 40, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def write_candidate(root: Path, netlist=SCS, yaml_text=CAND_YAML, hash_of=None, caption="delay", value=50.0):
    for rel, data in {NETLIST: netlist, YAML: yaml_text}.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(data, encoding="utf-8")
    h = hash_of or content_hash(root / NETLIST)
    (root / RESULT).parent.mkdir(parents=True, exist_ok=True)
    (root / RESULT).write_text(json.dumps(result_doc(h, value=value, caption=caption)), encoding="utf-8")
    (root / RESULT).with_name("tt_nom_27.delay.png").write_bytes(png())


# ------------------------------------------------------------------ merged candidates (main's tree)
def test_merged_candidate_row_comes_from_adcflow_candidates(tmp_path):
    write_candidate(tmp_path)
    with cands.tree_root(tmp_path):
        got = cands.merged(site_stub(), main_data(), live_with())
    (c,) = got[BLOCK]
    assert (c.name, c.source, c.reviewed, c.selected) == (NAME, "main", True, False)
    assert c.row["author_text"] == "Alice's agent (@alice)" and c.row["status"] == "wip"
    assert c.row["flags"]["stale"] == 0 and c.row["self_reported"] == 1            # no verification record: self-reported
    assert c.row["specs_passed"] >= 1 and c.row["power_uW"] is not None and c.row["area"]["devices"] == 1
    assert c.view == f"xtor-{NAME}" and c.anchor == f"cand-{NAME}"


def test_withdrawn_candidates_are_not_listed(tmp_path):
    write_candidate(tmp_path, yaml_text=CAND_YAML.replace("status: wip", "status: withdrawn"))
    with cands.tree_root(tmp_path):
        assert cands.merged(site_stub(), main_data(), live_with()) == {}


def test_unacknowledged_notices_are_flagged_for_active_candidates(tmp_path):
    write_candidate(tmp_path, yaml_text=CAND_YAML.replace("acknowledged: []", "acknowledged: [41]"))
    notices = [Issue(n, f"[{BLOCK}] spec change", f"u/{n}", 0, "lead", "", "") for n in (41, 42)]
    with cands.tree_root(tmp_path):
        (c,) = cands.merged(site_stub(), main_data(), live_with(*notices))[BLOCK]
    assert c.unacked == [42]
    with cands.tree_root(tmp_path):                         # the API is unavailable: no flag, not a guess
        (c2,) = cands.merged(site_stub(), main_data(), Live(ok=False, fetched_at="x", error="down"))[BLOCK]
    assert c2.unacked == []


def test_a_stale_input_is_flagged(tmp_path):
    write_candidate(tmp_path, hash_of="0" * 16)
    with cands.tree_root(tmp_path):
        (c,) = cands.merged(site_stub(), main_data(), live_with())[BLOCK]
    assert c.row["flags"]["stale"] == 1 and not cands.eligible(c.row)


def test_tree_root_restores_the_roots(tmp_path):
    from adcflow import checks
    before = (C.ROOT, checks.REPO_ROOT)
    with cands.tree_root(tmp_path):
        assert C.ROOT == checks.REPO_ROOT == tmp_path
    assert (C.ROOT, checks.REPO_ROOT) == before


# ------------------------------------------------------------------ candidates of an open PR head
def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


def make_pr_repo(tmp_path, *, extra=None, **kw):
    """A repository whose main has no candidate and whose PR head adds the candidate; returns (repo, head sha)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    (repo / "README.md").write_text("main\n")
    git(repo, "add", "."), git(repo, "commit", "-qm", "main")
    git(repo, "checkout", "-qb", "pr")
    write_candidate(repo, **kw)
    for rel, data in (extra or {}).items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(data)
    git(repo, "add", "."), git(repo, "commit", "-qm", f"[{BLOCK}] candidate {NAME} first netlist")
    head = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-q", "main")
    return repo, head


def pr_obj(head, contracts="success", number=7, title=f"[{BLOCK}] candidate {NAME} first netlist"):
    return PR(number, title, f"https://github.com/o/r/pull/{number}", True, "alice", "2026-10-27T10:00:00Z",
              "2026-10-28T15:57:00Z", head, "pass", contracts, "")


def run_pr(tmp_path, pr=None, fork="", **kw):
    repo, head = make_pr_repo(tmp_path, **kw)
    out = tmp_path / "out"
    out.mkdir()
    return cands.pr_candidates(site_stub(), main_data(), live_with(), pr or pr_obj(head), BLOCK, fork or "o/r", out, repo, "HEAD"), out, head


def test_pr_head_candidate_is_scored_with_the_same_function_and_marked_unreviewed(tmp_path):
    got, out, head = run_pr(tmp_path)
    (c,) = got
    assert (c.name, c.source, c.reviewed, c.selected) == (NAME, "pr", False, False)
    assert c.row["author_text"] == "Alice's agent (@alice)" and c.row["flags"]["stale"] == 0
    assert c.row["power_uW"] is not None and c.row["specs_passed"] >= 1
    assert c.anchor == f"cand-{NAME}-pr7" and c.pr.number == 7
    # links and evidence at the PR head, figures and the manifest published under the PR's own names
    assert (c.site.build.sha, c.site.build.repo, c.site.fig_prefix) == (head, "o/r", "preview/pr7/")
    assert (out / "preview/pr7" / RESULT).with_name("tt_nom_27.delay.png").is_file()
    (vf,) = c.viewer_files
    assert vf["url"] == f"https://raw.githubusercontent.com/o/r/{head}/{NETLIST}" and (out / "manifests" / f"{vf['mf']}.json").is_file()
    assert c.commits and c.xtor_change and c.xtor_change[2].startswith(f"[{BLOCK}] candidate")
    rows = c.bd.rows[c.view]
    assert [r.evidence for r in rows if r.test == TEST and r.evidence][0] == RESULT


def test_fork_pr_links_into_the_fork(tmp_path):
    got, out, _ = run_pr(tmp_path, fork="mallory/fork")
    assert got[0].head_repo == "mallory/fork" and got[0].site.build.repo == "mallory/fork"
    assert got[0].viewer_files[0]["url"].startswith("https://raw.githubusercontent.com/mallory/fork/")


def test_a_pr_cannot_change_the_verdict_by_changing_specs(tmp_path):
    spec_rel = f"specs/blocks/{BLOCK}.yaml"
    loosened = (ROOT / spec_rel).read_text(encoding="utf-8").replace("max: 80", "max: 8000")
    assert loosened != (ROOT / spec_rel).read_text(encoding="utf-8")
    # 500 ps fails CMP-04 (<= 80 ps) under main's specs; it would pass under the PR's loosened copy
    got, _, _ = run_pr(tmp_path, extra={spec_rel: loosened}, value=500.0)
    r = got[0].row
    assert r["specs_total"] == len(blocks()[BLOCK].specs)
    assert r["specs_failed"] >= 1
    assert any(x.status == "fail" for x in got[0].bd.rows[got[0].view])


def test_stale_inputs_of_a_pr_candidate_are_flagged(tmp_path):
    got, _, _ = run_pr(tmp_path, hash_of="0" * 16)
    assert got[0].row["flags"]["stale"] == 1


def test_pr_without_a_candidate_is_a_legacy_draft_not_a_candidate(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    (repo / "README.md").write_text("main\n")
    git(repo, "add", "."), git(repo, "commit", "-qm", "main")
    git(repo, "checkout", "-qb", "pr")
    legacy = repo / "design" / "xtor" / BLOCK / f"{BLOCK}.scs"
    legacy.parent.mkdir(parents=True)
    legacy.write_text(SCS)
    git(repo, "add", "."), git(repo, "commit", "-qm", "legacy draft")
    head = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-q", "main")
    out = tmp_path / "out"
    out.mkdir()
    assert cands.pr_candidates(site_stub(), main_data(), live_with(), pr_obj(head), BLOCK, "o/r", out, repo, "HEAD") is None


@pytest.mark.parametrize("label,kw", [
    ("hygiene in the netlist", {"netlist": SCS + "// see /ho" + "me/alice/models\n"}),
    ("vendor name in a result caption", {"caption": "ts" + "mc corner"}),
    ("vendor name in the display name", {"yaml_text": CAND_YAML.replace("Alice's agent", "ts" + "mc agent")}),
])
def test_content_that_fails_main_checks_gives_no_candidate(tmp_path, label, kw):
    repo, head = make_pr_repo(tmp_path, **kw)
    out = tmp_path / "out"
    out.mkdir()
    with pytest.raises(preview.PreviewError):
        cands.pr_candidates(site_stub(), main_data(), live_with(), pr_obj(head), BLOCK, "o/r", out, repo, "HEAD")
    assert not (out / "preview").exists() and not (out / "manifests").exists()          # nothing published before the checks


# ------------------------------------------------------------------ all PRs of a block
def collect_with(tmp_path, pr_state, **kw):
    repo, head = make_pr_repo(tmp_path, **kw)
    out = tmp_path / "out"
    out.mkdir()
    fetched = []
    pr = pr_obj(head, contracts=pr_state)
    live = Live(ok=True, fetched_at="x", prs={BLOCK: [pr]})
    with cands.tree_root(tmp_path / "empty"):          # main has no candidate
        (tmp_path / "empty").mkdir(exist_ok=True)
        got = cands.collect(site_stub(), main_data(), live, out, repo, lambda r, n, s: fetched.append(n), "HEAD")
    return got, fetched


def test_collect_puts_a_passed_candidate_pr_in_the_leaderboard(tmp_path):
    got, fetched = collect_with(tmp_path, "success")
    assert fetched == [7]
    assert [c.name for c in got.cands[BLOCK]] == [NAME] and BLOCK not in got.previews


@pytest.mark.parametrize("state", ["running", "fail", "none", "unknown"])
def test_collect_reads_nothing_of_a_pr_whose_ci_has_not_passed(tmp_path, state):
    got, fetched = collect_with(tmp_path, state)
    assert fetched == [] and BLOCK not in got.cands
    (pv,) = got.previews[BLOCK]
    assert not pv.ok and "CI" in pv.reason


def test_collect_shows_metadata_only_when_a_check_fails(tmp_path):
    got, _ = collect_with(tmp_path, "success", netlist=SCS + "// see /ho" + "me/alice/models\n")
    assert BLOCK not in got.cands
    (pv,) = got.previews[BLOCK]
    assert not pv.ok and "卫生检查" in pv.reason


def test_collect_without_the_api_keeps_the_merged_candidates(tmp_path):
    write_candidate(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    with cands.tree_root(tmp_path):
        got = cands.collect(site_stub(), main_data(), Live(ok=False, fetched_at="x", error="down"), out)
    assert [c.name for c in got.cands[BLOCK]] == [NAME] and got.previews == {}
