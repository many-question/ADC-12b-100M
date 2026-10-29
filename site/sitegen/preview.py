"""Draft previews of open `[<block>]` pull requests: their metrics and netlist, read as DATA from the PR head.

A preview is the content of an unreviewed draft on a public site, so it is built under hard rules:

* nothing from a PR is ever executed: files are read with `git cat-file` (no filters, no textconv) from the object
  database after `git fetch origin +refs/pull/<N>/head` (the same for fork PRs), parsed as JSON / YAML / text by the
  generator's own code, which comes from main;
* only a head with a successful CI run "contracts, drawings, results" is previewed (else metadata only, with the reason);
* everything taken from the PR (results, specs, the netlists the viewer will fetch, figure captions, commit titles) goes through
  the process-name guard and the hygiene rules of `adcflow check hygiene` first; one hit and NO content of that PR is rendered;
* previews never touch the main-branch data: they are separate objects, labelled as unreviewed drafts, and are not in any
  verdict, status or count of main;
* figures: PNG only, at most FIGURE_MAX_BYTES each, copied under preview/pr<N>/.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from . import guard, manifest as mf
from .data import ROOT, BlockData, _spec_rows
from .live import PR, Live

FIGURE_MAX_BYTES = 200_000              # as adcflow check results (checks.FIGURE_MAX_BYTES)
MAX_TEXT_BYTES = 2 * 1024 * 1024        # the viewer's per-file limit
MAX_PREVIEWS_PER_BLOCK = 3
MAX_COMMITS = 8
TEXT_SUFFIXES = {".json", ".yaml", ".yml", ".scs", ".rnl", ".va", ".vams"}
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
REGULAR = {"100644", "100755"}          # no symlinks, no submodules


class PreviewError(Exception):
    """Why a PR cannot be previewed; the text is shown on the page, so it never quotes PR content."""


@dataclass
class Preview:
    pr: PR
    block: str
    head_repo: str
    ok: bool = False
    reason: str = ""
    site: object | None = None                          # Site clone: links at the PR head, figures under preview/pr<N>/
    bd: BlockData | None = None
    viewer_files: list[dict] = field(default_factory=list)
    xtor_change: tuple[str, str, str] | None = None     # short sha, date, title of the last commit touching design/xtor/<block>
    commits: list[tuple[str, str]] = field(default_factory=list)   # (short sha, title) of the PR's own commits
    counts: tuple[int, int, int] = (0, 0, 0)            # pass, fail, total specs of the most advanced view
    notes: list[str] = field(default_factory=list)      # log lines (skipped figures, ...)
    unmigrated: bool = False                            # a draft that still has the legacy view (design/xtor/<block>/<block>.scs): not a candidate yet


# ------------------------------------------------------------------ git (read only)
def _git(repo: Path, *args: str, timeout: int = 120) -> bytes:
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, timeout=timeout)
    if p.returncode != 0:
        raise PreviewError("git: " + (p.stderr.decode("utf-8", "replace").strip().splitlines() or ["failed"])[-1][:160])
    return p.stdout


def fetch_pr_head(repo: Path, number: int, sha: str) -> None:
    """Fetch refs/pull/<N>/head (fork PRs included) and check that it is the head the API told us about."""
    try:
        _git(repo, "fetch", "--quiet", "origin", f"+refs/pull/{number}/head:refs/remotes/pr/{number}")
    except (PreviewError, subprocess.TimeoutExpired) as e:
        raise PreviewError("无法获取该 PR 的提交") from e
    got = _git(repo, "rev-parse", "--verify", f"refs/remotes/pr/{number}").decode().strip()
    if got != sha:
        raise PreviewError("该 PR 在获取期间又有了新的提交，下一次重建会显示")


class Tree:
    """The regular files of a commit: path -> size, read with `git cat-file blob` (no filters)."""

    def __init__(self, repo: Path, sha: str):
        self.repo, self.sha = repo, sha
        self.files: dict[str, int] = {}
        for rec in _git(repo, "ls-tree", "-r", "-z", "--long", sha).split(b"\0"):
            if not rec:
                continue
            meta, _, path = rec.partition(b"\t")
            mode, kind, _obj, size = meta.decode().split(None, 3)
            try:
                rel = path.decode("utf-8")
            except UnicodeDecodeError:
                continue
            if kind == "blob" and mode in REGULAR and safe_rel(rel):
                self.files[rel] = int(size.strip())

    def read(self, rel: str, limit: int | None = None) -> bytes:
        if rel not in self.files:
            raise PreviewError(f"{rel} 不在该 PR 的提交里")
        if limit is not None and self.files[rel] > limit:
            raise PreviewError(f"{rel} 太大")
        return _git(self.repo, "cat-file", "blob", f"{self.sha}:{rel}")

    def under(self, prefix: str) -> list[str]:
        return sorted(p for p in self.files if p.startswith(prefix))


def safe_rel(rel: str) -> bool:
    p = PurePosixPath(rel)
    return bool(rel) and not p.is_absolute() and ".." not in p.parts and "\\" not in rel and "\0" not in rel and rel == p.as_posix()


# ------------------------------------------------------------------ the checks every PR text goes through
def hygiene_hits(text: str) -> list[str]:
    """The rules of `adcflow check hygiene` (checks.FORBIDDEN, and the exact strings of the local site config when
    there is one) applied to a text; returns the names of the rules that hit, never the text."""
    from adcflow.checks import FORBIDDEN, _site_literals
    return sorted({what for pat, what in FORBIDDEN + _site_literals()
                   if re.search(pat, text, flags=re.MULTILINE | re.IGNORECASE)})


def screen(label: str, text: str) -> None:
    """Raise PreviewError when `text` (from `label`) would not pass main's checks."""
    if guard.contains(text):
        raise PreviewError(f"{label}: 含有不得公开的工艺名称")
    hits = hygiene_hits(text)
    if hits:
        raise PreviewError(f"{label}: 未通过卫生检查（{'、'.join(hits)}）")


# ------------------------------------------------------------------ pieces shared by the legacy preview and the candidate rows
def commit_titles(repo: Path, sha: str, base: str) -> list[tuple[str, str]]:
    """(short sha, title) of the PR's own commits (`sha --not base`), titles screened."""
    out = []
    for line in _git(repo, "log", f"-{MAX_COMMITS}", "--format=%h%x1f%s", sha, "--not", base).decode("utf-8", "replace").splitlines():
        short, _, title = line.partition("\x1f")
        screen(f"提交 {short} 的标题", title)
        out.append((short, title))
    return out


def last_commit(repo: Path, sha: str, path: str) -> tuple[str, str, str] | None:
    """(short sha, date, title) of the last commit that touched `path` at `sha`; the title is screened."""
    line = _git(repo, "log", "-1", "--format=%h%x1f%cs%x1f%s", sha, "--", path).decode("utf-8", "replace").strip()
    if not line:
        return None
    short, date, title = (line.split("\x1f") + ["", ""])[:3]
    screen("网表最近一次提交的标题", title)
    return short, date, title


def copy_figures(tree: "Tree", docs: list[dict], out: Path, number: int, notes: list[str]) -> None:
    """Copy the small PNGs the results list to out/preview/pr<N>/<repo path>; others are dropped from the doc (figures() skips an
    empty name) and noted. A doc's `_path` is ROOT / <repo path>."""
    for d in docs:
        for f in (d.get("figures") or []):
            name = str(f.get("file", "")) if isinstance(f, dict) else ""
            rel = (PurePosixPath(d["_path"].relative_to(ROOT).as_posix()).parent / name).as_posix() if name else ""
            ok = bool(name) and "/" not in name and name.lower().endswith(".png") and rel in tree.files
            data = tree.read(rel, FIGURE_MAX_BYTES) if ok and tree.files[rel] <= FIGURE_MAX_BYTES else b""
            if not data.startswith(PNG_MAGIC):
                f["file"] = ""
                notes.append(f"{rel or name}: figure skipped (missing, not a small PNG)")
                continue
            dst = out / "preview" / f"pr{number}" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)


def write_manifests(out: Path, pr: PR, head_repo: str, entries: list[dict], rels: list[str]) -> dict[str, str]:
    """Viewer manifests at the PR head, one per entry netlist; returns {entry path: manifest name} (manifests/<name>.json)."""
    if mf.check_limits(entries):
        raise PreviewError("清单超出查看器的限制")
    raw, names = _raw_base(head_repo, pr.sha), {}
    for rel in rels:
        name = f"pr{pr.number}-{pr.sha[:7]}-{mf.name_of(rel)}"
        doc = mf.manifest(rel, entries, raw, head_repo, pr.sha)
        (out / "manifests").mkdir(parents=True, exist_ok=True)
        (out / "manifests" / f"{name}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        names[rel] = name
    return names


# ------------------------------------------------------------------ building one preview
def judge_at(block, doc: dict, root: Path) -> dict:
    """What `adcflow.checks.judge` gives for a result, against the PR's own block (specs) and the PR's input files under `root`."""
    from adcflow.netlist import content_hash
    verdict, na = block.verdicts(doc["test"], doc["corner"], doc.get("meta", {}).get("mc"), doc["metrics"])
    stale = []
    for rel, h in (doc.get("meta", {}).get("files") or {}).items():
        p = root / rel
        try:
            if not safe_rel(rel) or not p.is_file() or content_hash(p) != h:
                stale.append(rel)
        except Exception:                                  # an unparsable input counts as changed
            stale.append(rel)
    return {"specs": verdict, "na": na, "stale": stale, "error": doc["metrics"].get("error")}


def _raw_base(head_repo: str, sha: str) -> str:
    return f"https://raw.githubusercontent.com/{head_repo}/{sha}/"


def build_preview(site, pr: PR, block: str, head_repo: str, out: Path, repo: Path = ROOT,
                  fetch=fetch_pr_head, base: str = "HEAD") -> Preview:
    """One PR's preview (never raises: a PR that cannot be previewed is a Preview with a reason)."""
    pv = Preview(pr, block, head_repo)
    if pr.contracts != "success":
        pv.reason = {"running": "CI「contracts, drawings, results」还在运行", "fail": "CI「contracts, drawings, results」未通过",
                     }.get(pr.contracts, "CI「contracts, drawings, results」没有结果")
        return pv
    try:
        fetch(repo, pr.number, pr.sha)
        _build(pv, site, out, repo, base)
        pv.ok = True
    except PreviewError as e:
        pv.reason = str(e) if not guard.contains(str(e)) else "内容未通过检查"     # a path from the PR must not reach the page
        shutil.rmtree(out / "preview" / f"pr{pr.number}", ignore_errors=True)
        pv.bd = pv.site = None
        pv.viewer_files, pv.commits, pv.xtor_change, pv.counts = [], [], None, (0, 0, 0)
    except Exception as e:                                  # whatever a PR holds, the build goes on
        pv.reason = f"无法读取该 PR 的内容（{type(e).__name__}）"
        shutil.rmtree(out / "preview" / f"pr{pr.number}", ignore_errors=True)
        pv.bd = pv.site = None
        pv.viewer_files, pv.commits, pv.xtor_change, pv.counts = [], [], None, (0, 0, 0)
    return pv


def _build(pv: Preview, site, out: Path, repo: Path, base: str) -> None:
    from adcflow import specs as adc_specs
    pr, block = pv.pr, pv.block
    tree = Tree(repo, pr.sha)

    # --- everything the preview shows or the viewer will fetch, screened first
    commits = commit_titles(repo, pr.sha, base)
    screen("PR 标题", pr.title)
    screen("PR 作者名", pr.author)
    spec_rel = f"specs/blocks/{block}.yaml"
    if spec_rel not in tree.files:
        raise PreviewError("该 PR 里没有这个模块的规格")
    published = [p for p in tree.files if p.split("/")[0] in mf.PUBLISH and PurePosixPath(p).suffix in mf.PUBLISH[p.split("/")[0]]]
    results = [p for p in tree.under(f"results/{block}/") if p.endswith(".json")]
    texts: dict[str, bytes] = {}
    for rel in [spec_rel, *results, *published]:
        texts[rel] = tree.read(rel, MAX_TEXT_BYTES)
        try:
            screen(rel, texts[rel].decode("utf-8"))
        except UnicodeDecodeError:
            raise PreviewError(f"{rel}: 不是 UTF-8 文本") from None

    # --- the PR's own specs and results, judged against the PR's own inputs
    with tempfile.TemporaryDirectory(prefix="adcpr") as tmp:
        root = Path(tmp)
        (root / "specs" / "blocks").mkdir(parents=True)
        (root / spec_rel).write_bytes(texts[spec_rel])
        try:
            pr_block = adc_specs._load_block(root / spec_rel)
        except Exception as e:
            raise PreviewError(f"规格无法解析（{type(e).__name__}）") from None
        if pr_block.name != block:
            raise PreviewError("规格里的模块名与文件名不一致")
        docs = []
        for rel in results:
            try:
                d = json.loads(texts[rel])
            except ValueError:
                pv.notes.append(f"{rel}: not JSON, skipped")
                continue
            if not (isinstance(d, dict) and d.get("block") == block and isinstance(d.get("metrics"), dict)
                    and all(isinstance(d.get(k), str) for k in ("test", "view", "corner"))):
                pv.notes.append(f"{rel}: not a result of {block}, skipped")
                continue
            d["_path"] = ROOT / rel                              # only for relative paths (evidence links, figures)
            for f in (d.get("meta", {}).get("files") or {}):
                if safe_rel(f) and f in tree.files and not (root / f).exists():
                    (root / f).parent.mkdir(parents=True, exist_ok=True)
                    (root / f).write_bytes(tree.read(f, MAX_TEXT_BYTES))
            d["_judged"] = judge_at(pr_block, d, root)
            docs.append(d)
    views = sorted({d["view"] for d in docs})
    rows = {v: _spec_rows(pr_block, v, docs) for v in views}

    # --- the preview's own Site: links at the PR head (and its repository), figures under preview/pr<N>/
    s2 = copy.copy(site)
    s2.build = dataclasses.replace(site.build, repo=pv.head_repo, sha=pr.sha, short=pr.sha[:7])
    s2.fig_prefix = f"preview/pr{pr.number}/"
    s2.prov_scope = "该 PR 的提交"
    xtor = [p for p in tree.under(f"design/xtor/{block}/") if p.endswith(".scs")]
    pv.bd = BlockData(pr_block, docs, rows, [], xtor)
    pv.site = s2

    copy_figures(tree, docs, out, pr.number, pv.notes)

    # --- the netlist viewer: raw files at the head, through a manifest at that sha
    entries = []
    for rel in published:
        data = texts[rel]
        entries.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    raw = _raw_base(pv.head_repo, pr.sha)
    names = write_manifests(out, pr, pv.head_repo, entries, xtor)
    for rel in xtor:
        label = "晶体管级 xtor" + ("" if len(xtor) == 1 else f" · {PurePosixPath(rel).name}")
        pv.viewer_files.append({"label": label, "kind": "xtor", "path": rel, "level": block, "url": raw + rel, "mf": names[rel]})
    if xtor:
        pv.xtor_change = last_commit(repo, pr.sha, f"design/xtor/{block}")
    pv.commits = commits
    pv.unmigrated = bool(pv.viewer_files) or any(d["view"] == "xtor" for d in docs)

    # --- counts of the most advanced view, for the home table (draft: never added to main's numbers)
    view = next((v for v in ("xtor", "behav") if v in rows), None)
    if view:
        rr = [r for s, r in zip(pr_block.specs, rows[view]) if not s.reported]     # a reported-only spec has no verdict
        pv.counts = (sum(r.status == "pass" for r in rr), sum(r.status == "fail" for r in rr), len(rr))


# ------------------------------------------------------------------ all open PRs
def build_previews(site, live: Live, out: Path, repo: Path = ROOT, fetch=fetch_pr_head) -> dict[str, list[Preview]]:
    """Previews of the open PRs of each block (the newest MAX_PREVIEWS_PER_BLOCK; the rest are metadata only)."""
    out_map: dict[str, list[Preview]] = {}
    if not live.ok:
        return out_map
    for block, prs in live.prs.items():
        for i, pr in enumerate(prs):
            if i >= MAX_PREVIEWS_PER_BLOCK:
                out_map.setdefault(block, []).append(Preview(pr, block, pr.head_repo or site.build.repo,
                                                             reason=f"只预览每个模块最新的 {MAX_PREVIEWS_PER_BLOCK} 个 PR"))
                continue
            pv = build_preview(site, pr, block, pr.head_repo or site.build.repo, out, repo, fetch)
            out_map.setdefault(block, []).append(pv)
    return out_map
