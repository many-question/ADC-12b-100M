"""Draft previews of PR heads (site/sitegen/preview.py) on fixture git repositories: no network, nothing from a PR is run."""

import json
import struct
import subprocess
import sys
import zlib
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))

from sitegen import preview                                         # noqa: E402
from sitegen.data import Build                                      # noqa: E402
from sitegen.live import PR                                         # noqa: E402

BLOCK = "adc_demo"
NETLIST = f"design/xtor/{BLOCK}/{BLOCK}.scs"
SCS = "// demo\nsimulator lang=spectre\nsubckt adc_demo (A B)\nends adc_demo\n"
SPEC = f"""block: {BLOCK}
title: demo
version: 0.1.0
selected: none
status: behavioral
views: {{xtor: {NETLIST}}}
ports:
  - {{name: A, dir: in, type: analog, side: left}}
  - {{name: B, dir: out, type: analog, side: right}}
specs:
  - {{id: DEM-01, name: gain, metric: gain, unit: dB, min: 10, corners: typ, test: tb_demo}}
  - {{id: DEM-02, name: gain, metric: gain, unit: dB, min: 10, corners: all, test: tb_demo}}
tests:
  tb_demo: {{netlist: tb/demo/tb_demo.scs, measure: adcflow.measure.demo:run}}
"""


def png(size=100):
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = b"".join(b"\0" + b"\x80" * 3 * size for _ in range(size))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def run(repo, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


def result_doc(files_hash, extra_caption="gain vs corner", figure="tt_nom_27.a.png"):
    return {"block": BLOCK, "test": "tb_demo", "view": "xtor", "corner": "tt_nom_27", "metrics": {"gain": 20.0},
            "meta": {"git": "abc1234", "files": {NETLIST: files_hash}},
            "figures": [{"file": figure, "caption": extra_caption}]}


def make_pr(tmp_path, *, netlist=SCS, hash_of=None, caption="gain vs corner", figures=None, symlink=False):
    """A repository with a main commit and a PR head commit on top of it; returns (repo, head sha)."""
    from adcflow.netlist import content_hash
    repo = tmp_path / "repo"
    repo.mkdir()
    run(repo, "init", "-q", "-b", "main")
    (repo / "README.md").write_text("main\n")
    run(repo, "add", "."), run(repo, "commit", "-qm", "main")
    run(repo, "checkout", "-qb", "pr")
    for rel, data in {"specs/blocks/%s.yaml" % BLOCK: SPEC, NETLIST: netlist, "design/top/adc_top.scs": SCS}.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(data)
    h = hash_of or content_hash(repo / NETLIST)
    rdir = repo / "results" / BLOCK / "tb_demo" / "xtor"
    rdir.mkdir(parents=True)
    (rdir / "tt_nom_27.json").write_text(json.dumps(result_doc(h, caption)))
    for name, data in (figures if figures is not None else {"tt_nom_27.a.png": png()}).items():
        (rdir / name).write_bytes(data)
    if symlink:
        link = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=repo, input=b"/etc/passwd", capture_output=True, check=True).stdout.decode().strip()
        run(repo, "update-index", "--add", "--cacheinfo", f"120000,{link},design/xtor/{BLOCK}/link.scs")
    run(repo, "add", "."), run(repo, "commit", "-qm", f"[{BLOCK}] first xtor netlist")
    head = run(repo, "rev-parse", "HEAD")
    run(repo, "checkout", "-q", "main")
    return repo, head


def pr_for(head, contracts="success", number=7):
    return PR(number, f"[{BLOCK}] first xtor netlist", f"https://github.com/o/r/pull/{number}", True, "alice",
              "2026-10-27T10:00:00Z", "2026-10-28T15:57:00Z", head, "pass", contracts, "")


SITE = SimpleNamespace(build=Build(repo="o/r", sha="m" * 40, short="mmmmmmm", date="", ref=""), fig_prefix="", repo="o/r")


def make(tmp_path, pr=None, fetch=None, fork="", **kw):
    repo, head = make_pr(tmp_path, **kw)
    out = tmp_path / "out"
    out.mkdir()
    calls = []
    pr = pr or pr_for(head)
    got = preview.build_preview(SITE, pr, BLOCK, fork or "o/r", out, repo, fetch or (lambda r, n, s: calls.append((n, s))), "HEAD")
    return got, out, calls


# ------------------------------------------------------------------ the normal case
def test_preview_of_a_clean_passed_head(tmp_path):
    pv, out, calls = make(tmp_path)
    assert pv.ok, pv.reason
    assert calls and calls[0][0] == 7                       # fetched refs/pull/7/head
    assert pv.counts == (2, 0, 2)                           # both specs pass at the one recorded corner ...
    assert [(r.n, r.need > 1) for r in pv.bd.rows["xtor"]] == [(1, False), (1, True)]   # ... DEM-02 needs every corner
    row = pv.bd.rows["xtor"][0]
    assert row.status == "pass" and row.evidence == f"results/{BLOCK}/tb_demo/xtor/tt_nom_27.json"
    assert pv.bd.rows["xtor"][0].stale == []                # the recorded input hash is the head's own file
    # evidence and the viewer's files point at the PR head, in the PR's repository
    assert (pv.site.build.sha, pv.site.build.repo) == (pv.pr.sha, "o/r") and pv.site.fig_prefix == "preview/pr7/"
    assert SITE.build.sha == "m" * 40                      # main's Site is left as it was
    assert pv.commits and pv.commits[0][1] == f"[{BLOCK}] first xtor netlist"
    assert pv.xtor_change and pv.xtor_change[2] == f"[{BLOCK}] first xtor netlist"
    # figure copied under preview/pr7/, manifest written at that sha
    assert (out / "preview/pr7/results" / BLOCK / "tb_demo/xtor/tt_nom_27.a.png").is_file()
    (mf,) = list((out / "manifests").glob("pr7-*.json"))
    doc = json.loads(mf.read_text())
    assert doc["base"] == f"https://raw.githubusercontent.com/o/r/{pv.pr.sha}/" and doc["entry"] == NETLIST
    assert {f["path"] for f in doc["files"]} == {NETLIST, "design/top/adc_top.scs"}
    (vf,) = pv.viewer_files
    assert vf["url"] == doc["base"] + NETLIST and vf["mf"] == mf.stem


def test_fork_pr_uses_the_fork_for_links_and_fetches_the_pull_ref(tmp_path):
    pv, out, calls = make(tmp_path, fork="mallory/fork")
    assert pv.ok and calls == [(7, pv.pr.sha)]
    assert pv.site.build.repo == "mallory/fork" and pv.site.build.sha == pv.pr.sha
    doc = json.loads(next((out / "manifests").glob("pr7-*.json")).read_text())
    assert doc["base"].startswith("https://raw.githubusercontent.com/mallory/fork/")


# ------------------------------------------------------------------ stale marking
def test_inputs_that_differ_from_the_heads_files_are_stale(tmp_path):
    pv, _, _ = make(tmp_path, hash_of="0" * 16)
    assert pv.ok
    row = pv.bd.rows["xtor"][0]
    assert row.stale == [NETLIST]
    assert pv.bd.docs[0]["_judged"]["stale"] == [NETLIST]


# ------------------------------------------------------------------ only CI-passed heads
@pytest.mark.parametrize("state", ["running", "fail", "none", "unknown", ""])
def test_head_without_a_successful_contracts_run_is_metadata_only(tmp_path, state):
    repo, head = make_pr(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    fetched = []
    pv = preview.build_preview(SITE, pr_for(head, contracts=state), BLOCK, "o/r", out, repo, lambda *a: fetched.append(a), "HEAD")
    assert not pv.ok and "CI" in pv.reason
    assert fetched == []                                     # not even fetched
    assert not (out / "preview").exists() and not (out / "manifests").exists()


# ------------------------------------------------------------------ same checks as main
def test_hygiene_hit_in_a_netlist_gives_metadata_only(tmp_path):
    pv, out, _ = make(tmp_path, netlist=SCS + "// see /ho" + "me/alice/models\n")
    assert not pv.ok and "卫生检查" in pv.reason
    assert pv.bd is None and pv.viewer_files == []
    assert not (out / "preview").exists() and not list((out / "manifests").glob("*")) if (out / "manifests").exists() else True


def test_hygiene_hit_in_a_result_gives_metadata_only(tmp_path):
    pv, _, _ = make(tmp_path, caption="loaded from /ser" + "ver_scratch/run1")
    assert not pv.ok and "卫生检查" in pv.reason


def test_vendor_name_anywhere_gives_metadata_only_and_the_reason_does_not_repeat_it(tmp_path):
    name = "ts" + "mc"
    pv, out, _ = make(tmp_path, caption=f"{name} corner sweep")
    assert not pv.ok and "工艺名称" in pv.reason and name not in pv.reason.lower()
    assert pv.bd is None and not (out / "preview").exists()


def test_vendor_name_in_a_file_path_is_not_echoed_in_the_reason(tmp_path):
    from sitegen import guard
    name = "TS" + "MC"
    repo, head = make_pr(tmp_path, netlist=SCS)
    # a path of the PR that carries the name: add it on a new commit and preview that head
    run(repo, "checkout", "-q", "pr")
    p = repo / "design" / "top" / f"{name}_x.scs"
    p.write_text(SCS)
    run(repo, "add", "."), run(repo, "commit", "-qm", "[adc_demo] more")
    head2 = run(repo, "rev-parse", "HEAD")
    run(repo, "checkout", "-q", "main")
    out = tmp_path / "out"
    out.mkdir()
    pv = preview.build_preview(SITE, pr_for(head2), BLOCK, "o/r", out, repo, lambda *a: None, "HEAD")
    assert pv.ok or not guard.contains(pv.reason)


def test_commit_titles_and_the_pr_title_are_screened(tmp_path):
    repo, head = make_pr(tmp_path)
    pr = pr_for(head)
    pr.title = f"[{BLOCK}] " + "ts" + "mc" + " cells"
    out = tmp_path / "out"
    out.mkdir()
    pv = preview.build_preview(SITE, pr, BLOCK, "o/r", out, repo, lambda *a: None, "HEAD")
    assert not pv.ok


# ------------------------------------------------------------------ fetch problems, figures, odd files
def test_a_head_that_moved_or_cannot_be_fetched_is_metadata_only(tmp_path):
    def boom(repo, n, sha):
        raise preview.PreviewError("无法获取该 PR 的提交")
    pv, _, _ = make(tmp_path, fetch=boom)
    assert not pv.ok and "无法获取" in pv.reason


def test_big_and_non_png_figures_are_skipped_the_preview_stays(tmp_path):
    figs = {"tt_nom_27.a.png": png(300) + b"\0" * preview.FIGURE_MAX_BYTES}       # over the limit
    pv, out, _ = make(tmp_path, figures=figs)
    assert pv.ok and any("figure skipped" in n for n in pv.notes)
    assert not list((out / "preview").rglob("*.png"))


def test_a_figure_that_is_not_a_png_is_skipped(tmp_path):
    pv, out, _ = make(tmp_path, figures={"tt_nom_27.a.png": b"<svg onload=alert(1)>"})
    assert pv.ok and not list((out / "preview").rglob("*.png"))


def test_symlinks_in_the_tree_are_ignored(tmp_path):
    repo, head = make_pr(tmp_path, symlink=True)
    tree = preview.Tree(repo, head)
    assert f"design/xtor/{BLOCK}/link.scs" not in tree.files and NETLIST in tree.files


@pytest.mark.parametrize("rel,ok", [("a/b.scs", True), ("../x", False), ("/etc/passwd", False), ("a/../b", False),
                                    ("a\\b", False), ("a//b", False), ("", False)])
def test_safe_rel(rel, ok):
    assert preview.safe_rel(rel) is ok


def test_main_data_is_untouched_by_a_preview(tmp_path):
    from sitegen import data
    before = repr(sorted(data.collect_blocks()))
    make(tmp_path)
    assert repr(sorted(data.collect_blocks())) == before
