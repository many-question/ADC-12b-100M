"""Candidate leaderboard data (docs/proposals/open-candidates.md): merged candidates and the candidates of open PRs.

* Merged candidates: `adcflow.candidates.leaderboard()` on main's tree, the verdicts of main's specs.
* Open PR candidates: the same function (`candidates.score`) on the PR head's candidate files, read as DATA with the rules of
  `sitegen/preview.py`: only heads with a successful "contracts, drawings, results" run, everything taken from the PR goes
  through the process-name guard and the hygiene rules first (one hit: no content, only the PR's metadata), nothing from the
  PR is ever run (`git cat-file` after `git fetch origin +refs/pull/<N>/head`), the verdict is main's specs (a PR cannot
  change them), PNG figures up to 200 kB. They carry the "未评审" label and never reach main's status or counts.

The ranking is the public order of §4: top-level ENOB margin (±0.05 bit), power (±5 %), area proxy (±5 %), the smallest
robustness margin (±5 % of the limit); inside a tolerance the next criterion decides, and then the selected candidate stays first.
Candidates that are not fully passing (a failed, incomplete, stale, SOA or error result) come after the eligible ones.
"""

from __future__ import annotations

import functools
import hashlib
import json
import re
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from . import manifest as mf, preview as pv
from .data import ROOT, BlockData, _spec_rows
from .live import PR, Live

TOL_ENOB, TOL_POWER, TOL_AREA, TOL_MARGIN = 0.05, 0.05, 0.05, 0.05     # §4 (bit, relative, relative, of the limit)
CAND_TEXT = {".scs", ".yaml", ".yml", ".json"}
NAME_RE = re.compile(r"^[a-z0-9-]{2,24}$")                              # candidates.NAME_RE


@dataclass
class Cand:
    block: str
    name: str
    row: dict                                 # adcflow.candidates.score(): the leaderboard row
    source: str                               # "main" (merged) | "pr" (an open PR, unreviewed)
    anchor: str
    pr: PR | None = None
    head_repo: str = ""
    site: object | None = None                # Site for links and evidence (the PR head and its repository for a PR)
    bd: BlockData | None = None               # this candidate's results, judged with main's specs
    view: str = ""                            # result view directory: xtor-<name>
    viewer_files: list[dict] = field(default_factory=list)
    xtor_change: tuple[str, str, str] | None = None
    commits: list[tuple[str, str]] = field(default_factory=list)
    unacked: list[int] = field(default_factory=list)     # open [<block>] notices its candidate.yaml has not acknowledged
    notes: list[str] = field(default_factory=list)

    @property
    def selected(self) -> bool:
        return bool(self.row.get("selected")) and self.source == "main"

    @property
    def reviewed(self) -> bool:
        return self.source == "main"


@dataclass
class Collected:
    cands: dict[str, list[Cand]] = field(default_factory=dict)         # block -> ranked candidates
    previews: dict[str, list[pv.Preview]] = field(default_factory=dict)  # block -> PRs that are not (or not yet) candidates
    logs: list[str] = field(default_factory=list)


# ------------------------------------------------------------------ ranking (§4)
def eligible(row: dict) -> bool:
    """No failed, incomplete, stale, SOA-violating or erroring result (reviewing is separate: unverified is shown, not excluded)."""
    f = row["flags"]
    return (row["results"] > 0 and row["specs_failed"] == 0 and row["specs_incomplete"] == 0
            and not (f["stale"] or f["soa"] or f["error"]))


def _better(a, b, *, higher: bool, tol: float, relative: bool) -> int:
    """-1 when a is better, 1 when b is better, 0 within the tolerance; a missing value is worse than any value."""
    if a is None and b is None:
        return 0
    if a is None:
        return 1
    if b is None:
        return -1
    scale = max(abs(a), abs(b)) if relative else 1.0
    if abs(a - b) <= tol * scale:
        return 0
    return -1 if (a > b) == higher else 1


def compare(a: Cand, b: Cand) -> int:
    ra, rb = a.row, b.row
    ea, eb = eligible(ra), eligible(rb)
    if ea != eb:
        return -1 if ea else 1
    if not ea:                                                    # neither is fully passing: more passed specs, more coverage
        for x, y in ((rb["specs_passed"], ra["specs_passed"]), (rb["coverage"][0], ra["coverage"][0])):
            if x != y:
                return -1 if x < y else 1
    wm = lambda r: (r["worst_margin"] or {}).get("margin")        # noqa: E731
    area = lambda r, k: (r["area"] or {}).get(k) or None           # noqa: E731  (0 -> unknown)
    for c in (_better(ra["top_enob_margin"], rb["top_enob_margin"], higher=True, tol=TOL_ENOB, relative=False),
              _better(ra["power_uW"], rb["power_uW"], higher=False, tol=TOL_POWER, relative=True),
              _better(area(ra, "wl_um2"), area(rb, "wl_um2"), higher=False, tol=TOL_AREA, relative=True),
              _better(area(ra, "cap_F"), area(rb, "cap_F"), higher=False, tol=TOL_AREA, relative=True),
              _better(wm(ra), wm(rb), higher=True, tol=TOL_MARGIN, relative=False)):
        if c:
            return c
    if a.selected != b.selected:                                  # tied inside every tolerance: the selected one stays
        return -1 if a.selected else 1
    return -1 if (a.name, a.source) < (b.name, b.source) else 1


def rank(cands: list[Cand]) -> list[Cand]:
    return sorted(cands, key=functools.cmp_to_key(compare))


def mc_chips(row: dict) -> list[tuple[str, str, str]]:
    """(chip kind, label, title) of the Monte Carlo sample coverage of a leaderboard row (candidates.mc_coverage):
    pass with every sample valid, fail with a failed sample or too few, none without a Monte Carlo result."""
    out = []
    for m in row.get("mc") or []:
        label = f"{m['spec']} MC {m['ok']}/{m['need']}"
        if m["failed"] is None and m["ok"] == 0:
            out.append(("none", label, f"{m['spec']}：还没有 Monte Carlo 结果（需要 {m['need']} 个有效样本）"))
        elif m["failed"] == 0 and m["ok"] >= m["need"]:
            out.append(("pass", label, f"{m['spec']}：{m['ok']} 个 Monte Carlo 样本全部有效，0 个失败"))
        else:
            out.append(("fail", label + (f" · {m['failed']} 失败" if m["failed"] else ""),
                        f"{m['spec']}：{m['ok']} / {m['need']} 个有效样本，{m['failed']} 个失败或缺失；任一样本失败，该指标即不通过"))
    return out


def count(cands: list[Cand]) -> int:
    """Candidates of a block for "候选：N": not withdrawn (merged ones, and open PRs whose head passed CI)."""
    return sum(c.row["status"] != "withdrawn" for c in cands)


# ------------------------------------------------------------------ merged candidates (main's tree)
def unacknowledged(live: Live, block: str, meta: dict, status: str) -> list[int]:
    """Open [<block>] notices an active (wip / ready) candidate has not acknowledged in candidate.yaml."""
    if status not in ("wip", "ready") or not live.ok:
        return []
    ack = {a for a in (meta.get("acknowledged") or []) if isinstance(a, int)}
    return sorted(i.number for i in live.block_issues(block) if i.number not in ack)


def viewer_entry(block: str, name: str, **extra) -> dict:
    return {"label": f"晶体管级 xtor · {name}", "kind": "xtor", "path": f"design/xtor/{block}/{name}/{block}.scs",
            "level": block, **extra}


def merged(site, data: dict[str, BlockData], live: Live) -> dict[str, list[Cand]]:
    from adcflow import candidates as C

    out: dict[str, list[Cand]] = {}
    for row in C.leaderboard():                                     # withdrawn ones are left out
        block, name = row["block"], row["candidate"]
        bd = data.get(block)
        if bd is None:
            continue
        view = f"xtor-{name}"
        docs = [d for d in bd.docs if d["view"] == view]
        rows = bd.rows.get(view)
        c = Cand(block, name, row, "main", f"cand-{name}", site=site, view=view,
                 bd=BlockData(bd.b, docs, {view: rows} if rows else {}, [], []))
        if (ROOT / viewer_entry(block, name)["path"]).is_file():
            c.viewer_files = [viewer_entry(block, name)]
        c.unacked = unacknowledged(live, block, C.load(block, name).meta, row["status"])
        out.setdefault(block, []).append(c)
    return out


# ------------------------------------------------------------------ open PRs (the PR head, read as data)
@contextmanager
def tree_root(root: Path):
    """Point adcflow's candidate readers and result judging at `root` (a temporary tree of the PR's files)."""
    from adcflow import candidates as C, checks
    saved = (C.ROOT, checks.REPO_ROOT)
    C.ROOT = checks.REPO_ROOT = root
    try:
        yield
    finally:
        C.ROOT, checks.REPO_ROOT = saved


def touched_candidates(repo: Path, sha: str, base: str, block: str) -> list[str]:
    """Names of the candidates of `block` that the PR changes (paths against the merge base); only well-formed names count."""
    from adcflow import candidates as C
    mb = pv._git(repo, "merge-base", base, sha).decode().strip()                # noqa: SLF001
    paths = pv._git(repo, "diff", "--name-only", "-z", mb, sha).split(b"\0")       # noqa: SLF001
    names = set()
    for p in paths:
        try:
            o = C.owner_of_path(p.decode("utf-8"))
        except UnicodeDecodeError:
            continue
        if o and o[0] == block and NAME_RE.match(o[1]):
            names.add(o[1])
    return sorted(names)


def pr_candidates(site, data: dict[str, BlockData], live: Live, pr: PR, block: str, head_repo: str, out: Path,
                  repo: Path, base: str) -> list[Cand] | None:
    """The candidates a PR (whose head was fetched and passed CI) adds or changes; None when it changes none (a legacy draft).
    Raises PreviewError when anything of it fails main's checks: the caller then shows the PR's metadata only."""
    from adcflow import candidates as C
    from adcflow.checks import judge

    names = touched_candidates(repo, pr.sha, base, block)
    if not names:
        return None
    tree = pv.Tree(repo, pr.sha)
    commits = pv.commit_titles(repo, pr.sha, base)
    pv.screen("PR 标题", pr.title)
    pv.screen("PR 作者名", pr.author)

    # everything the page shows or the viewer can fetch, screened before any of it is used
    published = [p for p in tree.files if p.split("/")[0] in mf.PUBLISH and PurePosixPath(p).suffix in mf.PUBLISH[p.split("/")[0]]]
    own: dict[str, list[str]] = {}
    for n in names:
        d = f"design/xtor/{block}/{n}/"
        own[n] = [p for p in tree.files if (p.startswith(d) and PurePosixPath(p).suffix in CAND_TEXT)
                  or (p.startswith(f"results/{block}/") and f"/xtor-{n}/" in p and p.endswith(".json"))]
    texts: dict[str, bytes] = {}
    for rel in sorted(set(published).union(*own.values())):
        texts[rel] = tree.read(rel, pv.MAX_TEXT_BYTES)
        try:
            pv.screen(rel, texts[rel].decode("utf-8"))
        except UnicodeDecodeError:
            raise pv.PreviewError(f"{rel}: 不是 UTF-8 文本") from None

    main_block = data[block].b
    entries = [{"path": p, "sha256": hashlib.sha256(texts[p]).hexdigest(), "size": len(texts[p])} for p in published]
    netlists = [f"design/xtor/{block}/{n}/{block}.scs" for n in names if f"design/xtor/{block}/{n}/{block}.scs" in texts]
    manifests = pv.write_manifests(out, pr, head_repo, entries, netlists)
    raw = pv._raw_base(head_repo, pr.sha)                                     # noqa: SLF001
    s2 = _head_site(site, pr, head_repo)
    cands = []
    with tempfile.TemporaryDirectory(prefix="adccand") as td:
        root = Path(td)
        for n in names:
            for rel in own[n]:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_bytes(texts[rel])
        for n in names:                                                       # inputs of the results: the candidate's own files from the PR, the shared ones from main
            for rel in own[n]:
                if not rel.endswith(".json"):
                    continue
                try:
                    doc = json.loads(texts[rel])
                except ValueError:
                    continue
                for f in ((doc.get("meta") or {}).get("files") or {}) if isinstance(doc, dict) else ():
                    if pv.safe_rel(f) and not (root / f).exists() and (ROOT / f).is_file():
                        (root / f).parent.mkdir(parents=True, exist_ok=True)
                        (root / f).write_bytes((ROOT / f).read_bytes())
        with tree_root(root):
            for n in names:
                view = f"xtor-{n}"
                c = C.load(block, n)
                row = C.score(c)
                row["selected"] = False                                        # only a merged candidate is selected
                docs = C._results(block, view)                                 # noqa: SLF001
                for d in docs:
                    d["_path"] = ROOT / d["_path"].relative_to(root).as_posix()    # repo path, for evidence links and figures
                    d["_judged"] = judge(d)
                rows = _spec_rows(main_block, view, docs)
                cand = Cand(block, n, row, "pr", f"cand-{n}-pr{pr.number}", pr, head_repo, s2,
                            BlockData(main_block, docs, {view: rows} if docs else {}, [], []), view)
                cand.unacked = unacknowledged(live, block, c.meta, row["status"])
                cands.append(cand)
    for cand in cands:
        pv.copy_figures(tree, cand.bd.docs, out, pr.number, cand.notes)
        rel = f"design/xtor/{block}/{cand.name}/{block}.scs"
        if rel in manifests:
            cand.viewer_files = [viewer_entry(block, cand.name, url=raw + rel, mf=manifests[rel])]
            cand.xtor_change = pv.last_commit(repo, pr.sha, f"design/xtor/{block}/{cand.name}")
        cand.commits = commits
    return cands


def _head_site(site, pr: PR, head_repo: str):
    import copy
    import dataclasses
    s2 = copy.copy(site)
    s2.build = dataclasses.replace(site.build, repo=head_repo, sha=pr.sha, short=pr.sha[:7])
    s2.fig_prefix = f"preview/pr{pr.number}/"
    s2.prov_scope = "该 PR 的提交"
    return s2


# ------------------------------------------------------------------ all blocks
def collect(site, data: dict[str, BlockData], live: Live, out: Path, repo: Path = ROOT, fetch=pv.fetch_pr_head,
            base: str = "HEAD") -> Collected:
    """Merged candidates and the open PRs of every block: ranked candidates, and the PRs that are not candidates (legacy drafts,
    metadata-only rows) for the draft tabs."""
    got = Collected(cands=merged(site, data, live))
    if live.ok:
        for block, prs in live.prs.items():
            for i, pr in enumerate(prs):
                head_repo = pr.head_repo or site.build.repo
                if i >= pv.MAX_PREVIEWS_PER_BLOCK:
                    got.previews.setdefault(block, []).append(pv.Preview(
                        pr, block, head_repo, reason=f"只预览每个模块最新的 {pv.MAX_PREVIEWS_PER_BLOCK} 个 PR"))
                    continue
                if pr.contracts != "success":                              # the legacy path reports the CI reason, metadata only
                    got.previews.setdefault(block, []).append(pv.build_preview(site, pr, block, head_repo, out, repo, fetch, base))
                    continue
                try:
                    fetch(repo, pr.number, pr.sha)
                    found = pr_candidates(site, data, live, pr, block, head_repo, out, repo, base)
                except pv.PreviewError as e:
                    reason = str(e) if not pv.guard.contains(str(e)) else "内容未通过检查"
                    got.previews.setdefault(block, []).append(pv.Preview(pr, block, head_repo, reason=reason))
                    got.logs.append(f"PR #{pr.number} [{block}] metadata only ({reason})")
                    continue
                except Exception as e:                                     # whatever a PR holds, the build goes on
                    reason = f"无法读取该 PR 的内容（{type(e).__name__}）"
                    got.previews.setdefault(block, []).append(pv.Preview(pr, block, head_repo, reason=reason))
                    got.logs.append(f"PR #{pr.number} [{block}] metadata only ({reason})")
                    continue
                if found is None:                                          # not a candidate PR: the legacy draft preview
                    got.previews.setdefault(block, []).append(
                        pv.build_preview(site, pr, block, head_repo, out, repo, lambda *a: None, base))
                else:
                    got.cands.setdefault(block, []).extend(found)
                    got.logs.append(f"PR #{pr.number} [{block}] candidates: {', '.join(c.name for c in found)}")
    for block in got.cands:
        got.cands[block] = rank(got.cands[block])
    return got
