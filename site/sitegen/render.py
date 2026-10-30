"""HTML of the pages. Plain f-strings: the site is small and the pages are mostly tables."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from urllib.parse import quote, quote_plus

from .data import (CONTRIBUTING_RAW, FALLBACK_REPO, PROCESS, REPORTED_TITLE, ROOT, STATUS_ORDER, BlockData, Build, SpecRow,
                   arch, docs, evidence_path, figures, fmt, has_doc, judged_rows, last_change, limit_label, owner_login,
                   verdict_counts)
from . import cands as candmod, livepanel
from .live import Live, unavailable
from .manifest import name_of
from .md import esc, slug

VIEWER = "https://rich-netlist.github.io/rnl/viewer/"
STATUS_LABEL = {"behavioral": "行为级", "xtor-review": "晶体管级 · 待评审", "signoff": "签核"}
STATUS_HINT = {"behavioral": "只有行为级视图（Verilog-A）", "xtor-review": "全部用例已跑，等待复核",
               "signoff": "全角通过并已复核"}
NAV = [("index", "概览", "index.html"), ("progress", "进展", "progress.html"), ("verification", "验证", "verification.html"),
       ("blocks", "模块", "blocks/index.html"), ("docs", "文档", "docs/index.html")]
COLLAB = ("collab", "参与协作", "docs/contributing.html")


class Site:
    """Page context: repository identity, link roots and the netlist location."""

    def __init__(self, build: Build, netlist_base: str, base_url: str, manifests: bool = False):
        self.build, self.netlist_base, self.base_url, self.manifests = build, netlist_base, base_url, manifests
        self.live: Live = unavailable("本次构建没有获取")      # per-block PRs and notices (build.py sets the real data)
        self.combos: list = []                                 # verification combinations of the top level (combos.py)
        self.cands: dict[str, list] = {}                       # block -> ranked candidates (merged + open PRs), see cands.py
        self.previews: dict = {}                               # block -> [preview.Preview] of its open PRs (draft content, never main's)
        self.prov_scope = "本次构建"                            # what recorded inputs are compared with ("该 PR 的提交" in a preview)
        self.fig_prefix = ""                                   # where figures of the results shown live in the site ("preview/pr<N>/" for a PR)
        self.doc_ids: dict[str, set[str]] = {}      # doc slug -> heading ids, to link only anchors that exist

    def gh(self, rel: str, is_dir: bool = False) -> str:
        ref = self.build.sha or "main"
        return f"https://github.com/{self.build.repo}/{'tree' if is_dir else 'blob'}/{ref}/{rel}"

    def netlist_url(self, rel: str) -> str | None:
        """Absolute URL when it is known at build time (raw base, or --base-url of the deployed site)."""
        if self.netlist_base.startswith("http"):
            return self.netlist_base + rel
        if self.base_url:
            return self.base_url + self.netlist_base + rel
        return None

    @property
    def repo(self) -> str:
        return self.build.repo or FALLBACK_REPO

    def manifest_url(self, rel: str) -> str | None:
        """Absolute URL of the manifest whose entry is `rel`, when the site's own address is known at build time."""
        return f"{self.base_url}manifests/{name_of(rel)}.json" if self.manifests and self.base_url else None

    def full_viewer_href(self, rel: str, level: str | None = None, mf_name: str | None = None, url: str | None = None) -> str:
        """The standalone viewer on the design through a manifest; without manifests, on the single netlist.

        `mf_name` / `url` are for a netlist that is not main's (a PR preview): its manifest name and its own address.
        When the address is not known at build time, app.js sets the real link from the page location."""
        lv = f"&level={quote(level)}" if level else ""
        if mf_name:
            m = f"{self.base_url}manifests/{mf_name}.json" if self.manifests and self.base_url else None
        else:
            m = self.manifest_url(rel)
        if m:
            return f"{VIEWER}?manifest={quote(m, safe='')}{lv}"
        if self.manifests:
            return VIEWER
        u = url or self.netlist_url(rel)
        return f"{VIEWER}?url={quote(u, safe='')}{lv}" if u else VIEWER

    def prs_url(self, block: str) -> str:
        """Open pull requests of a block: their titles start with [<block>]."""
        return f"https://github.com/{self.repo}/pulls?q=" + quote_plus(f'is:pr is:open in:title "[{block}]"')

    def evidence(self, rel: str, label: str = "JSON ↗", doc: dict | None = None) -> str:
        """Link to a result file on GitHub at the built commit, with the result's provenance under it when `doc` is given."""
        link = (f'<a class="ev" href="{esc(self.gh(rel))}" target="_blank" rel="noopener" '
                f'title="证据：{esc(rel)}（构建提交 {esc(self.build.short)}）">{label}</a>')
        return link + (self.provenance(doc) if doc else "")

    def provenance(self, doc: dict) -> str:
        """One short muted line: the commit the result was simulated on, whether its inputs match this build's files,
        and (when the result records it) whether the working tree was clean at simulation time.

        The result file is committed after the simulation, so the commit it names is older than the build's by design."""
        meta = doc.get("meta") or {}
        sha = str(meta.get("git") or "").strip()
        parts = []
        if sha:
            parts.append(f'仿真于 <a href="https://github.com/{self.repo}/commit/{esc(sha)}" target="_blank" rel="noopener">{esc(sha[:7])}</a>'
                         if re.fullmatch(r"[0-9a-f]{7,40}", sha) else f"仿真于 {esc(sha)}")
        stale = (doc.get("_judged") or {}).get("stale")
        if stale is not None:
            if stale:
                shown = "，".join(stale[:2]) + (f" 等 {len(stale)} 个" if len(stale) > 2 else "")
                parts.append(f'<span class="warn-t" title="自仿真后已变化的输入：{esc("，".join(stale))}">已过期：{esc(shown)}</span>')
            else:
                parts.append(f"输入与{self.prov_scope}一致")
        if meta.get("git_clean") is False:
            dirty = "，".join(str(p) for p in meta.get("git_dirty_paths") or [])
            title = f' title="未提交的路径：{esc(dirty)}"' if dirty else ""
            parts.append(f'<span class="warn-t"{title}>仿真时工作区有未提交改动</span>')
        return f'<small class="prov muted">{" · ".join(parts)}</small>' if parts else ""


# ------------------------------------------------------------------ frame
def page(site: Site, *, title: str, body: str, active: str, root: str, desc: str = "", wide: bool = False) -> str:
    items = NAV + ([COLLAB] if has_doc("contributing") else [])
    def nav_link(key: str, label: str, href: str) -> str:
        cls = " ".join(c for c in (key == "collab" and "nav-collab", key == active and "on") if c)
        attrs = (f' class="{cls}"' if cls else "") + (" aria-current=page" if key == active else "")
        return f'<a href="{root}{href}"{attrs}>{label}</a>'
    nav = "".join(nav_link(*i) for i in items)
    b = site.build
    ver = f'<a href="{site.gh("", True)}commit/{b.sha}">{esc(b.short)}</a>' if b.sha and b.repo else esc(b.short)
    gh = f'<a class="gh" href="https://github.com/{b.repo}" rel="noopener" title="GitHub">GitHub ↗</a>' if b.repo else ""
    top_href = site.full_viewer_href("design/top/adc_top.scs", "adc_top")
    nl_base = site.netlist_base if site.netlist_base.startswith("http") else root + site.netlist_base   # relative to this page
    mf_href = site.base_url + "manifests/" if site.base_url else root + "manifests/"
    mf_base = f'<meta name="manifest-base" content="{esc(mf_href)}">' if site.manifests else ""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{esc(desc or f'ADC-12b-100M：{PROCESS} 异步 SAR ADC 设计进展、验证结果与原理图')}">
<meta name="netlist-base" content="{esc(nl_base)}">
{mf_base}
<title>{esc(title)} · ADC-12b-100M</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23127a8c'/%3E%3Cpath d='M5 21h5v-6h5v-5h5v-4h7' fill='none' stroke='white' stroke-width='3' stroke-linejoin='round'/%3E%3C/svg%3E">
<script>document.documentElement.classList.add('js');try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="{root}assets/style.css">
<script src="{root}assets/app.js" defer></script>
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
<header class="top"><div class="bar">
  <a class="brand" href="{root}index.html"><span class="logo" aria-hidden="true"></span><b>ADC-12b-100M</b></a>
  <nav aria-label="主导航">{nav}</nav>
  <div class="tools">
    <a class="btn small primary hide-sm" data-top-viewer href="{esc(top_href)}" target="_blank" rel="noopener">顶层原理图 ↗</a>
    <button class="icon" id="theme" type="button" aria-label="切换明暗主题" title="切换明暗主题"></button>
  </div>
</div></header>
<main id="main" class="{'wide' if wide else ''}">
{body}
</main>
<footer><div>
  <span>由仓库自动生成 · 版本 {ver} · {esc(b.date)}{' · ' + esc(b.ref) if b.ref else ''}</span>
  <span>网表与规格以仓库为准 {gh}</span>
</div></footer>
</body>
</html>
"""


def chip(kind: str, text: str, title: str = "") -> str:
    t = f' title="{esc(title)}"' if title else ""
    return f'<span class="chip {kind}"{t}>{esc(text)}</span>'


def status_chip(status: str) -> str:
    return chip(f"st st-{status}", STATUS_LABEL[status], STATUS_HINT[status])


def stepper(status: str) -> str:
    i = STATUS_ORDER.index(status)
    dots = "".join(f'<li class="{"done" if k < i else "now" if k == i else ""}" title="{esc(STATUS_LABEL[s])}"></li>'
                   for k, s in enumerate(STATUS_ORDER))
    return f'<ol class="stepper" aria-label="状态 {esc(STATUS_LABEL[status])}">{dots}</ol>'


def verdict_chip(r: SpecRow | None) -> str:
    if r is None:
        return chip("none", "无结果")
    if r.status == "fail":
        return chip("fail", "不通过")
    if r.status == "mc":
        return chip("none", f"待 MC {r.mc}")
    if r.status == "none":
        return chip("none", "无结果")
    out = chip("none", "仅报告", REPORTED_TITLE) if r.status == "reported" else chip("pass", "通过")
    if r.stale:
        out += " " + chip("stale", "过期", "自仿真后这些文件已更改：" + "，".join(r.stale))
    return out


def coverage(r: SpecRow) -> str:
    if r.status in ("none", "mc"):
        return f'<span class="cov" title="0 / {r.need} 个工艺角"><i style="width:0"></i></span><span class="muted">0/{r.need}</span>'
    pct = max(3, round(100 * r.n / r.need))
    return (f'<span class="cov" title="{r.n} / {r.need} 个工艺角（{esc(r.corner_set)}）"><i style="width:{pct}%"></i></span>'
            f'<span class="muted">{r.n}/{r.need}</span>')


def spec_table(site: Site, rows: list[SpecRow], with_test: bool = True) -> str:
    body = []
    for r in rows:
        worst = f"{fmt(r.worst)} <span class='muted'>{esc(r.unit)}</span>" if r.worst is not None else "–"
        test = f'<td><code>{esc(r.test)}</code></td>' if with_test else ""
        ev = site.evidence(r.evidence, doc=r.evidence_doc) if r.evidence else "<span class='muted'>–</span>"
        body.append(f"<tr class='{r.status}'><td><b>{esc(r.id)}</b></td><td>{esc(r.name)}</td>"
                    f"<td class=num>{esc(r.limit)} <span class='muted'>{esc(r.unit)}</span></td>"
                    f"<td class=num>{worst}</td><td>{verdict_chip(r)}</td><td class=cov-cell>{coverage(r)}</td>"
                    f"<td class=ev-cell>{ev}</td>{test}</tr>")
    head = "<th>ID<th>指标<th>限值<th>最差值<th>判定<th>工艺角<th title='最差值所在结果文件'>证据" + ("<th>用例" if with_test else "")
    return f'<div class="table-wrap"><table class="specs"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def figure_strip(site: Site, doc: dict, root: str) -> str:
    """Thumbnails of a result's figures (PNGs next to its JSON, copied under results/ of the site): click to enlarge."""
    items = []
    for f in figures(doc):
        cap = f.caption or Path(f.rel).name
        href = f"{root}{site.fig_prefix}{f.rel}"
        items.append(f'<figure><a href="{esc(href)}" data-zoom data-caption="{esc(cap)}" title="点击放大">'
                     f'<img src="{esc(href)}" alt="{esc(cap)}" loading="lazy"></a><figcaption>{esc(cap)}</figcaption></figure>')
    # collapsed until asked for; the images are lazy, so closed figures cost nothing
    return (f'<details class="figdet"><summary>图（{len(items)}）</summary><div class="figs">{"".join(items)}</div></details>' if items else "")


def corner_detail(site: Site, bd: BlockData, view: str, root: str = "") -> str:
    """Per test, per corner: every metric of a spec, colored by its verdict (a reported-only one uncolored), the evidence file
    and the result's figures."""
    out = []
    for tid, t in bd.b.tests.items():
        specs = [s for s in bd.b.specs if s.test == tid]
        results = sorted((d for d in bd.docs if d["test"] == tid and d["view"] == view), key=lambda d: d["corner"])
        if not results:
            continue
        head = "".join(f"<th title='{esc(s.name)}'>{esc(s.id)}<br><small>{esc(s.metric)}</small></th>" for s in specs)
        rows = []
        nfig = 0
        for d in results:
            j = d["_judged"]
            cells = []
            for s in specs:
                v = j["specs"].get(s.id)
                na = (j.get("na") or {}).get(s.id)
                if v is None and na is not None:          # measured, but the spec does not apply at this corner
                    cells.append(f"<td class='num muted' title='n/a: {esc(s.id)} applies to {esc(s.corners)} only, "
                                 f"not judged here'>{fmt(na['value'])} <small>n/a</small></td>")
                elif v is None:
                    cells.append("<td class='num muted'>–</td>")
                elif v["pass"] is None:                   # a reported-only spec: the value, no verdict
                    cells.append(f"<td class='num' title='{esc(REPORTED_TITLE)}'>{fmt(v['value'])}</td>")
                else:
                    cells.append(f"<td class='num {'ok' if v['pass'] else 'bad'}'>{fmt(v['value'])}</td>")
            st = chip("stale", "过期", "，".join(j["stale"])) if j["stale"] else ""
            err = chip("fail", "错误", str(j["error"])) if j["error"] else ""
            m = d.get("meta", {})
            rows.append(f"<tr><th scope=row><code>{esc(d['corner'])}</code> {st}{err}</th>{''.join(cells)}"
                        f"<td class='muted'>{esc((m.get('date') or '')[:10])}<br><small>{esc(m.get('git') or '')}</small></td>"
                        f"<td class=ev-cell>{site.evidence(evidence_path(d), doc=d)}</td></tr>")
            fs = figure_strip(site, d, root)
            if fs:
                nfig += 1
                rows.append(f"<tr class='figrow'><td colspan='{len(specs) + 3}'><code>{esc(d['corner'])}</code>{fs}</td></tr>")
        out.append(f"<details class='corners'><summary><code>{esc(tid)}</code> · {len(results)} 个结果文件"
                   f"{f' · {nfig} 个带图' if nfig else ''}</summary>"
                   f"<div class='table-wrap'><table class='detail'><thead><tr><th>工艺角{head}<th>日期 / git<th>证据</tr></thead>"
                   f"<tbody>{''.join(rows)}</tbody></table></div></details>")
    return "".join(out)


def verification_section(site: Site, bd: BlockData, level: int = 2, link: bool = True, root: str = "") -> str:
    b = bd.b
    h = f"h{level}"
    name = f'<a href="blocks/{b.name}.html">{esc(b.name)}</a>' if link else esc(b.name)
    parts = [f'<section class="vblock" id="{b.name}"><{h}>{name} {status_chip(b.status)}</{h}>']
    if link:
        parts.append(f"<p class='muted'>{esc(b.raw['title'])}</p>")
    if not bd.rows:
        parts.append("<p class='empty'>尚无记录的仿真结果。</p></section>")
        return "".join(parts)
    for view in sorted(bd.rows, key=lambda v: (v != "xtor", v)):
        label = view_label(view)
        parts.append(f"<h{level + 1}>{label}</h{level + 1}>{spec_table(site, bd.rows[view])}{corner_detail(site, bd, view, root)}")
    if "xtor" not in bd.rows and "xtor" in b.views:
        parts.append("<p class='empty'>晶体管级（xtor）视图：尚无结果。</p>")
    parts.append("</section>")
    return "".join(parts)


def view_label(view: str) -> str:
    return {"behav": "行为级 behav", "xtor": "晶体管级 xtor"}.get(view) or (f"候选 {view[5:]}" if view.startswith("xtor-") else view)


# ------------------------------------------------------------------ schematic viewer
def viewer(site: Site, files: list[dict], vid: str, height: int = 460, note: str = "") -> str:
    if not files:
        return "<p class='empty'>该模块还没有可画的网表。</p>"
    data = [{"label": f["label"], "path": f["path"], "level": f.get("level"), "kind": f["kind"], "mf": f.get("mf") or name_of(f["path"]),
             "url": f.get("url"), "src": site.gh(f["path"]),
             "full": site.full_viewer_href(f["path"], f.get("level"), f.get("mf"), f.get("url"))} for f in files]
    tabs = "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}">'
                   f'{esc(f["label"])}</button>' for i, f in enumerate(data))
    first = data[0]
    return f"""<section class="viewer" id="{vid}" data-files='{esc(json.dumps(data, ensure_ascii=False))}' style="--vh:{height}px">
<div class="viewer-bar">
  <div class="tabs" role="tablist" aria-label="网表">{tabs}</div>
  <div class="vtools">
    <label class="lvl" hidden>层次 <select aria-label="层次"></select></label>
    <button type="button" class="btn small ghost" data-act="grow" aria-pressed="false">放大</button>
    <a class="btn small" data-act="full" href="{esc(first['full'])}" target="_blank" rel="noopener">完整查看器 ↗</a>
  </div>
</div>
<div class="viewer-frame">
  <iframe title="RNL 原理图" loading="lazy" allow="fullscreen" referrerpolicy="no-referrer"></iframe>
  <div class="viewer-status" role="status" aria-live="polite">正在加载原理图查看器…</div>
</div>
<div class="viewer-foot"><span class="muted">{esc(note) or '拖动平移、滚轮缩放、双击子电路进入下一层（Backspace 返回）。'}</span>
  <a data-act="src" href="{esc(first['src'])}" target="_blank" rel="noopener">查看网表源码 ↗</a></div>
<noscript><p class="empty">原理图需要 JavaScript；也可以在 <a href="{esc(first['full'])}">RNL 查看器</a> 中打开。</p></noscript>
</section>"""


# ------------------------------------------------------------------ blocks
def contributing_href(site: Site, root: str) -> str | None:
    """The rendered CONTRIBUTING.md, at its "提交一个候选" section when that heading exists."""
    if not has_doc("contributing"):
        return None
    anchor = next((i for i in sorted(site.doc_ids.get("contributing", ())) if "提交一个候选" in i), "")
    return f"{root}docs/contributing.html" + (f"#{anchor}" if anchor else "")


def selection_label(b) -> str:
    """"选定候选" once the block spec has `selected:` (open candidates), "负责人" while it still has `owner:` (and for adc_top)."""
    return "选定候选" if "selected" in b.raw and b.name != "adc_top" else "负责人"


def selection_html(site: Site, b, root: str, links: bool = True) -> str:
    """Who the block belongs to: the selected candidate as `name (@login)` (adc_top and a spec that still has `owner:`: the
    owner); an unselected block invites a candidate. `links=False` is for text inside another link (the cards)."""
    block = b.name
    prs = f'<a href="{esc(site.prs_url(block))}" target="_blank" rel="noopener" title="标题以 [{esc(block)}] 开头的进行中 PR">进行中的 PR ↗</a>'
    href = contributing_href(site, root)
    if block == "adc_top" or "selected" not in b.raw:            # the project lead's block, or a spec that still has `owner:`
        owner = owner_login(b.raw.get("owner"))
        if owner:
            who = f'<a href="https://github.com/{esc(owner)}" target="_blank" rel="noopener">@{esc(owner)}</a>' if links else f"@{esc(owner)}"
        else:
            who = '<span class="unselected">未选定</span>'
    elif b.selected:
        c = next((c for c in site.cands.get(block, []) if c.name == b.selected and c.source == "main"), None)
        text = esc(b.selected) + (f" · {esc(c.row['author_text'])}" if c and c.row["author_text"] else "")
        who = f'<a href="{root}blocks/{block}.html#cand-{esc(b.selected)}">{text}</a>' if links else text
    else:
        invite = f' <a href="{esc(href)}">提交候选</a>' if links and href else ""
        who = f'<span class="unselected">未选定</span>{invite}'
    return who + (f' · {prs}' if links else "")


def card_selection(site: Site, b) -> str:
    """Compact "候选 N · 选定 X" for the cards (text only: the card is a link)."""
    if b.name == "adc_top" or "selected" not in b.raw:
        return selection_html(site, b, "", links=False)
    sel = f" · 选定 {esc(b.selected)}" if b.selected else ""
    return f"候选 {candmod.count(site.cands.get(b.name, []))}{sel}"


def cand_cell(site: Site, b) -> str:
    """Home table: "N" candidates (not withdrawn: merged, and open PRs whose head passed CI) and the selected one."""
    if b.name == "adc_top":
        return selection_html(site, b, "", links=False)
    n = candmod.count(site.cands.get(b.name, []))
    sel = ""
    if "selected" in b.raw:
        sel = f"<br><small>{'选定 ' + esc(b.selected) if b.selected else '<span class=muted>未选定</span>'}</small>"
    return f'<a href="blocks/{b.name}.html#candidates">候选：{n}</a>{sel}'


def port_table(b) -> str:
    rows, seen = [], set()
    for i, p in enumerate(b.ports, 1):
        if p.bus:
            if p.bus in seen:
                continue
            seen.add(p.bus)
            mem = [q for q in b.ports if q.bus == p.bus]
            name = f"{mem[0].name} … {mem[-1].name}"
            desc = next((q.desc for q in mem if q.desc), "")
            idx = f"{i}–{i + len(mem) - 1}"
        else:
            name, desc, idx = p.name, p.desc, str(i)
        rows.append(f"<tr><td class=num>{idx}</td><td><code>{esc(name)}</code></td><td>{esc(p.dir)}</td>"
                    f"<td>{esc(p.type)}</td><td>{esc(desc)}</td></tr>")
    return ('<div class="table-wrap"><table><thead><tr><th>#<th>端口<th>方向<th>类型<th>说明</tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def block_page(site: Site, bd: BlockData, all_names: list[str]) -> str:
    b = bd.b
    chips = "".join(f'<a class="pill{" on" if n == b.name else ""}" href="{n}.html">{esc(n)}</a>' for n in all_names)
    raw = b.raw
    summary = " ".join(str(raw.get("summary", "")).split())
    views = []
    for v, p in b.views.items():
        exists = (ROOT / p).is_file() or (v == "xtor" and bd.xtor_files)
        paths = bd.xtor_files if v == "xtor" and bd.xtor_files else [p]
        link = " ".join(f'<a href="{esc(site.gh(q))}" rel="noopener"><code>{esc(q)}</code></a>' for q in paths) if exists \
            else f'<code class="muted">{esc(p)}</code>'
        views.append(f"<li>{chip('pass' if exists else 'none', '有' if exists else '未建')} <b>{esc(v)}</b> {link}</li>")
    op = raw.get("operating") or {}
    op_html = ("<ul class='plain'>" + "".join(f"<li><code>{esc(k)}</code> {esc(' '.join(str(v).split()))}</li>"
                                              for k, v in op.items()) + "</ul>") if op else ""
    tests = []
    for tid, t in b.tests.items():
        covered = ", ".join(s.id for s in b.specs if s.test == tid)
        desc = " ".join(str(t.get("desc", "")).split())
        tests.append(f"<article class='test'><h3><code>{esc(tid)}</code></h3><p>{esc(desc)}</p>"
                     f"<p class='muted'>覆盖指标：{esc(covered) or '–'} · 测试台 <a href='{esc(site.gh(t['netlist']))}' rel=noopener>"
                     f"<code>{esc(t['netlist'])}</code></a> · 度量 <code>{esc(t['measure'])}</code></p></article>")
    docs_links = [(f"docs/{d}.html" + (f"#{slug(b.name)}" if slug(b.name) in site.doc_ids.get(d, ()) else ""), t)
                  for d, t in (("specs", "规格与用例（generated）"), ("handoff", "晶体管级设计分工包"), ("architecture", "架构设计"),
                               ("verification", "验证计划"), ("workflow", "工作流程"))
                  if d not in ("handoff",) or slug(b.name) in site.doc_ids.get(d, ())]
    dl = "".join(f"<li><a href='../{h}'>{t}</a></li>" for h, t in docs_links)
    cfg_link = f"<a href='{esc(site.gh(b.path.relative_to(ROOT).as_posix()))}' rel=noopener><code>specs/blocks/{b.name}.yaml</code></a>"
    note = ("上面是该模块的网表：行为级视图（Verilog-A 符号）与验收测试台；"
            + ("晶体管级视图已就绪时在最前面。" if bd.xtor_files else "晶体管级网表放入 design/xtor/ 后会自动出现在这里。"))
    vsec = ""
    main_views = [v for v in bd.rows if not v.startswith("xtor-")]       # the candidates' results are in the 候选 tab
    if main_views:
        for view in sorted(main_views, key=lambda v: (v != "xtor", v)):
            vsec += f"<h3>{view_label(view)}</h3>{spec_table(site, bd.rows[view], with_test=True)}{corner_detail(site, bd, view, '../')}"
    else:
        vsec = "<p class='empty'>尚无记录的仿真结果。</p>"
    body = f"""<div class="pills" aria-label="切换模块">{chips}</div>
<div class="page-head">
  <p class="eyebrow">模块 · 规格 v{esc(raw['version'])}</p>
  <h1><code class="h1code">{esc(b.name)}</code></h1>
  <p class="lead">{esc(raw['title'])}</p>
  <div class="meta">{status_chip(b.status)} {stepper(b.status)}
    <span><span class="muted">{selection_label(b)}</span> {selection_html(site, b, '../')}</span>
    <span><span class="muted">最近更新</span> {esc(last_change(bd) or '–')}</span>
    <span>{cfg_link}</span></div>
</div>
{{TABS}}"""
    main_html = f"""{livepanel.block_panel(site.live, b.name, site.repo)}
<section><h2 id="summary">功能概述</h2><p>{esc(summary)}</p>{op_html}</section>
<section><h2 id="schematic">原理图</h2>
{viewer(site, bd.files, 'v-' + b.name, 480, note)}
<ul class="plain views">{''.join(views)}</ul></section>
<section><h2 id="verification">验证结果</h2>{vsec}</section>
<section><h2 id="specs">规格与端口</h2><h3>端口（子电路端口顺序）</h3>{port_table(b)}
<h3>指标限值</h3>{_spec_limit_table(b)}</section>
<section><h2 id="tests">验收用例</h2><div class="tests">{''.join(tests)}</div></section>
<section><h2 id="docs">相关文档</h2><ul class="plain docs-links">{dl}</ul></section>"""
    body = body.replace("{TABS}", block_tabs(site, b.name, main_html))
    return page(site, title=b.name, body=body, active="blocks", root="../", desc=raw["title"])


DRAFT = "未评审的草稿，不是签核证据"


def block_tabs(site: Site, block: str, main_html: str) -> str:
    """The block's content in tabs: 主分支 (default), 候选 (the leaderboard: merged candidates and open PRs whose head passed CI), and one
    tab per draft PR that is not a candidate (a legacy draft, or a PR shown as metadata only).

    The tab is in the URL hash (#candidates, #pr<N>; none for main). Without JavaScript every panel is visible, stacked, each with
    its heading. Candidate and draft panels are separate from main: labelled, never counted for main."""
    pvs = site.previews.get(block, [])
    cs = site.cands.get(block, [])
    with_cands = block != "adc_top"                                     # the project lead's block takes no candidates
    if not with_cands and not pvs:
        return main_html
    tabs = ['<button type="button" role="tab" id="tab-main" aria-controls="content-main" aria-selected="true" tabindex="0">主分支</button>']
    panels = [f'<div role="tabpanel" id="content-main" aria-labelledby="tab-main"><h2 class="panel-title">主分支</h2>{main_html}</div>']
    if with_cands:
        tabs.append(f'<button type="button" role="tab" id="tab-candidates" aria-controls="candidates" aria-selected="false" tabindex="-1">'
                    f'候选 <span class="chip none">{candmod.count(cs)}</span></button>')
        panels.append(candidates_panel(site, block, cs, pvs))
    for pv in pvs:
        kind, label = livepanel.CI.get(pv.pr.ci, livepanel.CI["unknown"])
        tabs.append(f'<button type="button" role="tab" id="tab-pr{pv.pr.number}" aria-controls="pr{pv.pr.number}" aria-selected="false" tabindex="-1" '
                    f'title="{DRAFT}">草稿 PR #{pv.pr.number} <span class="chip {kind}">{esc(label)}</span></button>')
        panels.append(preview_section(site, pv))
    return (f'<div class="btabs" data-tabs><div class="tabbar" role="tablist" aria-label="内容来源：主分支、候选或草稿 PR">{"".join(tabs)}</div>'
            f'{"".join(panels)}</div>')


def _pct(m: float) -> str:
    return f"{m * 100:+.1f}%"


def cand_flags(site: Site, c) -> str:
    """The flags of a candidate row: results stale, verified / self-reported / mismatch (the lead's records in verification/),
    SOA, errors, problems, unacknowledged notices."""
    r, f = c.row, c.row["flags"]
    out = []
    extra = r["self_reported"] - f["unverified"]                  # self-reported results at corners no spec requires
    note = f"；另有 {extra} 个结果在规格不要求的工艺角，未复核" if extra else ""
    if not r["results"]:
        out.append(chip("none", "无结果"))
    elif f["unverified"] == 0 and not f["mismatch"] and r["verified"]:
        out.append(chip("pass", "已复核", f"规格要求的工艺角上的 {r['verified']} 个结果都有项目负责人的复核记录（verification/）："
                                       f"同一网表哈希上复跑，判定相同，指标在容差内，记录未过期{note}"))
    elif f["unverified"]:
        out.append(chip("none", "自报", f"规格要求的工艺角上有 {f['unverified']} 个结果没有有效的复核记录（自报，未经项目负责人复跑）；"
                                      f"已复核 {r['verified']} / {r['results']}{note}"))
    if f["mismatch"]:
        out.append(chip("fail", f"复核不符 {f['mismatch']}", "项目负责人在同一网表哈希上的复跑与自报值不符：判定不同或指标超出容差"))
    out += [chip(kind, label, title) for kind, label, title in candmod.mc_chips(r)]
    if f["stale"]:
        out.append(chip("stale", f"过期 {f['stale']}", "输入文件自仿真后已变化，需要重跑"))
    if f["soa"]:
        out.append(chip("fail", f"SOA {f['soa']}", "有结果报告了 SOA 违例"))
    if f["error"]:
        out.append(chip("fail", f"错误 {f['error']}", "仿真或度量出错的结果"))
    if r["problems"]:
        out.append(chip("fail", f"{len(r['problems'])} 个问题", "candidate.yaml 或网表不符合规则"))
    if c.unacked:
        links = "，".join(f'<a href="https://github.com/{esc(site.repo)}/issues/{n}" target="_blank" rel="noopener">#{n}</a>' for n in c.unacked)
        out.append(f'<span class="chip stale" title="规格变更通知，candidate.yaml 的 acknowledged 里还没有">未确认通知 {links}</span>')
    return " ".join(out)


def cand_row(site: Site, c, i: int | None) -> str:
    """One leaderboard row; i is the rank in the eligible tier, None for a candidate that is not eligible (then the row
    says what it misses)."""
    r = c.row
    wm = r["worst_margin"]
    a = r["area"] or {}
    area = "–"
    if a:
        area = f"MOS {a['mos']} · ΣWL {fmt(a['wl_um2'])} µm²" + (f" · {a['caps']} 电容 {fmt(a['cap_F'] * 1e15)} fF" if a.get("caps") else "")
    badges = ""
    if c.selected:
        badges += " " + chip("pass", "★ 选定", "项目负责人选定的候选")
    if c.source == "pr":
        badges += " " + chip("stale", "未评审", DRAFT)
    badges += " " + chip({"ready": "st-xtor-review", "wip": "st-wip"}.get(r["status"], "none"), r["status"] or "无 candidate.yaml")
    pct = max(3, round(100 * r["coverage"][0] / r["coverage"][1])) if r["coverage"][1] else 0
    cov = (f'<span class="cov" title="{r["coverage"][0]} / {r["coverage"][1]}（规格, 工艺角）"><i style="width:{pct}%"></i></span>'
           f'<span class="muted">{r["coverage"][0]}/{r["coverage"][1]}</span>')
    where = (f'<a href="{esc(c.pr.url)}" target="_blank" rel="noopener">PR #{c.pr.number} ↗</a>' if c.pr else
             f'<a href="{esc(site.gh(f"design/xtor/{c.block}/{c.name}", True))}" target="_blank" rel="noopener">目录 ↗</a>')
    spec = (f"<b class=ok-t>{r['specs_passed']}</b> / {r['specs_total']}"
            + (f' · <b class="bad-t">{r["specs_failed"]} 不过</b>' if r["specs_failed"] else "")
            + (f' · <span class="muted">{r["specs_incomplete"]} 不完整</span>' if r["specs_incomplete"] else "")
            + (f' · <span class="muted" title="{esc(REPORTED_TITLE)}">{r.get("specs_reported", 0)}/{r["reported_total"]} 仅报告</span>'
               if r.get("reported_total") else ""))
    who = esc(r["author_text"]) or "–"
    enob = f"{r['top_enob_margin']:+.3f} bit" if r["top_enob_margin"] is not None else "–"
    miss = ("" if i is not None else
            "<td><ul class='plain'>" + "".join(f"<li>{esc(m)}</li>" for m in candmod.missing_items(r)) + "</ul></td>")
    return (f'<tr class="{"selected" if c.selected else ""}"><td class=num>{i if i is not None else "–"}</td>'
            f'<td><a href="#{esc(c.anchor)}"><code>{esc(c.name)}</code></a>{badges}<br><small class="muted">{who}</small></td>'
            f'<td class=num>{fmt(r["power_uW"]) + " µW" if r["power_uW"] is not None else "–"}</td>'
            f'<td class=num>{area}</td>{miss}'
            f'<td>{spec}</td><td class=cov-cell>{cov}</td><td>{cand_flags(site, c)}</td>'
            f'<td class=num>{(_pct(wm["margin"]) + " <small class=muted>" + esc(wm["spec"]) + "</small>") if wm else "–"}</td>'
            f'<td class=num>{enob}</td>'
            f'<td>{where}</td></tr>')


def cand_table(site: Site, cs: list, eligible: bool) -> str:
    head = ('<th>#<th>候选<th title="本模块自己报告的 TT 功耗（各测试台的电源电流 × 电压，或能量 × 判决次数 × 采样率）">TT 功耗'
            '<th title="器件数、ΣW·L、电容：由网表算出，不依赖版图">面积代理'
            + ("" if eligible else "<th>未满足")
            + '<th>规格 通过 / 总数<th>工艺角覆盖<th>标记<th title="各规格 (限值−值)/限值 的最小值及规格号；只作参考，不参与排序">最小裕量（参考）'
            '<th title="项目负责人把该候选换进顶层后的结果；只作参考，不参与排序">顶层 ENOB 裕量（参考）<th>来源')
    rows = "".join(cand_row(site, c, i if eligible else None) for i, c in enumerate(cs, 1))
    return f'<div class="table-wrap"><table class="cands"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def cand_detail(site: Site, c) -> str:
    """One candidate's section under the table: its description, netlist in the viewer, and its metrics (judged with main's specs)."""
    s2 = c.site or site
    r = c.row
    head = f'<code>{esc(c.name)}</code> {esc(r["author_text"])}' + (" " + chip("stale", "未评审", DRAFT) if c.source == "pr" else "")
    body = [f'<p class="muted">{esc(r["description"])}</p>'] if r["description"] else []
    if c.pr:
        sha = (f'<a href="https://github.com/{esc(c.head_repo)}/commit/{esc(c.pr.sha)}" target="_blank" rel="noopener"><code>{esc(c.pr.sha[:7])}</code></a>')
        body.append(f'<p class="muted"><b>{DRAFT}</b>。{livepanel.pr_link(c.pr)} · {livepanel.pr_badges(c.pr)} · 提交 {sha}，PR 最近更新 '
                    f'{esc(livepanel.when(c.pr.updated))} UTC。内容读自该 PR 的提交，经过与主分支相同的检查；判定用主分支的规格；'
                    f'不计入主分支的状态、判定和统计。</p>')
    if c.viewer_files:
        body.append("<h4>网表</h4>" + viewer(s2, c.viewer_files, f"v-{c.anchor}", 420, "该候选的晶体管级网表。"))
        if c.xtor_change:
            sha, date, title = c.xtor_change
            body.append(f'<p class="muted">网表最近一次改动：<a href="https://github.com/{esc(s2.repo)}/commit/{esc(sha)}" target="_blank" rel="noopener">'
                        f'<code>{esc(sha)}</code></a> {esc(date)} {esc(title)}</p>')
        if c.commits:
            lis = "".join(f'<li><a href="https://github.com/{esc(c.head_repo)}/commit/{esc(h)}" target="_blank" rel="noopener"><code>{esc(h)}</code></a> {esc(t)}</li>'
                          for h, t in c.commits)
            body.append(f"<details class='corners'><summary>PR 的最近 {len(c.commits)} 个提交</summary><ul class='plain'>{lis}</ul></details>")
    else:
        body.append("<p class='empty'>这个候选里没有可画的网表。</p>")
    rows = c.bd.rows.get(c.view) if c.bd else None
    if rows:
        body.append(f"<h4>指标</h4>{spec_table(s2, rows, with_test=True)}{corner_detail(s2, c.bd, c.view, '../')}"
                    "<p class='muted legend'>判定按主分支的规格；“过期”表示结果记录的输入已不是当前的文件。</p>")
    else:
        body.append("<h4>指标</h4><p class='empty'>这个候选还没有提交仿真结果。</p>")
    return f'<details class="cand" id="{esc(c.anchor)}"><summary>{head}</summary>{"".join(body)}</details>'


def candidates_panel(site: Site, block: str, cs: list, pvs: list) -> str:
    """The 候选 tab: the leaderboard in two tiers (adcflow.candidates.compare, #75), then each candidate's netlist and metrics."""
    href = contributing_href(site, "../")
    invite = f'<a href="{esc(href)}">提交候选（协作流程 §4）</a>' if href else "提交候选"
    intro = (f'<p>任何人都可以为这个模块提交候选，没有人数和候选数上限；{invite}。排行榜分两层（协作流程 §10）：'
             f'<b>可选定</b>的候选——规格要求的全部指标在全部工艺角通过、结果未过期且已复核、通过 SOA 检查、换进顶层的混合回归通过——'
             f'按本模块自己报告的 TT 功耗从低到高排序，相差 5 % 以内算相同，由面积代理（先 ΣW·L 再总电容，各 5 %）决定，仍相同时已选定的保持在前；'
             f'<b>未满足资格</b>的候选另列一表，写明缺什么。项目不设功耗上限，功耗指标只报告、不判定。超出限值的裕量不加分：'
             f'最小裕量和顶层 ENOB 裕量只作参考，不参与排序。'
             f'提交的结果是<b>自报</b>的；项目负责人用 <code>adcflow verify</code> 在同一网表哈希上复跑，复核记录（<code>verification/</code>）匹配、未过期时才标“已复核”，只有已复核的结果才能用于选定。</p>')
    head = f'<h2 class="panel-title">候选</h2>'
    panel = f'role="tabpanel" id="candidates" aria-labelledby="tab-candidates"'
    if not cs:
        body = (f"<p class='empty'>这个模块现在没有候选。{invite}。</p>")
    else:
        elig = [c for c in cs if candmod.eligible(c.row)]
        rest = [c for c in cs if not candmod.eligible(c.row)]
        body = (f'<h3 id="cands-eligible">可选定（{len(elig)}）</h3>'
                + (cand_table(site, elig, True) if elig else "<p class='empty'>还没有满足全部资格的候选。</p>")
                + (f'<h3 id="cands-other">未满足资格（{len(rest)}）</h3>' + cand_table(site, rest, False) if rest else "")
                + '<p class="muted legend">★ = 已选定；“未评审”的是开放 PR 里的候选（CI 已通过，内容读自 PR 的提交并过了与主分支相同的检查），不计入主分支的状态，'
                '也没有复核记录，所以不会可选定；“—” = 没有这项数据；“仅报告” = 没有限值、不判定的功耗指标。</p>'
                + "".join(cand_detail(site, c) for c in cs))
    n_draft = len(pvs)
    extra = (f'<p class="muted legend">另有 {n_draft} 个草稿 PR 还不是候选（旧的单一视图、CI 未通过或内容未通过检查），见各自的“草稿 PR”标签。</p>' if n_draft else "")
    return f'<section {panel}>{head}{intro}{body}{extra}</section>'


def preview_section(site: Site, pv) -> str:
    pr = pv.pr
    panel = f'class="preview" role="tabpanel" id="pr{pr.number}" aria-labelledby="tab-pr{pr.number}"'
    head = (f'<a href="https://github.com/{esc(pv.head_repo)}/commit/{esc(pr.sha)}" target="_blank" rel="noopener"><code>{esc(pr.sha[:7])}</code></a>')
    top = (f'<h2>草稿预览 PR #{pr.number} @ <code>{esc(pr.sha[:7])}</code> '
           f'<span class="chip stale draft-label">{DRAFT}</span>'
           + ('<span class="chip none draft-label" title="还在用旧的单一视图 design/xtor/&lt;block&gt;/&lt;block&gt;.scs，没有候选目录">未迁移为候选</span>' if pv.unmigrated else "")
           + '</h2>'
           f'<p class="muted">{livepanel.pr_link(pr)} · {livepanel.pr_badges(pr)} · @{esc(pr.author)} · 提交 {head}，PR 最近更新 {esc(livepanel.when(pr.updated))} UTC。'
           f'内容读自该 PR 的提交，经过与主分支相同的检查；不计入主分支的状态、判定和统计。</p>')
    if not pv.ok:
        return f'<section {panel}>{top}<p class="empty">只显示元数据：{esc(pv.reason)}。</p></section>'
    s2 = pv.site
    if pv.viewer_files:
        notes = []
        if pv.xtor_change:
            sha, date, title = pv.xtor_change
            notes.append(f'网表最近一次改动：<a href="https://github.com/{esc(pv.head_repo)}/commit/{esc(sha)}" target="_blank" rel="noopener">'
                         f'<code>{esc(sha)}</code></a> {esc(date)} {esc(title)}')
        net = viewer(s2, pv.viewer_files, f"v-pr{pr.number}", 420, "该 PR 的晶体管级网表（未评审）。")
        commits = ""
        if pv.commits:
            lis = "".join(f'<li><a href="https://github.com/{esc(pv.head_repo)}/commit/{esc(c)}" target="_blank" rel="noopener"><code>{esc(c)}</code></a> {esc(t)}</li>'
                          for c, t in pv.commits)
            commits = f"<details class='corners'><summary>PR 的最近 {len(pv.commits)} 个提交</summary><ul class='plain'>{lis}</ul></details>"
        net += (f"<p class='muted'>{' · '.join(notes)}</p>" if notes else "") + commits
    else:
        net = f"<p class='empty'>这个 PR 里还没有 <code>design/xtor/{esc(pv.block)}/</code> 网表。</p>"
    if pv.bd.rows:
        met = ""
        for view in sorted(pv.bd.rows, key=lambda v: (v != "xtor", v)):
            label = {"behav": "行为级 behav", "xtor": "晶体管级 xtor"}.get(view, view)
            met += f"<h4>{label}</h4>{spec_table(s2, pv.bd.rows[view], with_test=True)}{corner_detail(s2, pv.bd, view, '../')}"
        met += "<p class='muted legend'>判定按该 PR 自己的规格（<code>specs/blocks/%s.yaml</code> 在该提交里的版本）和它自己的输入文件重新计算；“过期”表示结果记录的输入已不是该提交里的文件。</p>" % esc(pv.block)
    else:
        met = "<p class='empty'>这个 PR 里还没有记录的仿真结果。</p>"
    return f'<section {panel}>{top}<h3>网表</h3>{net}<h3>指标</h3>{met}</section>'


def _spec_limit_table(b) -> str:
    rows = "".join(f"<tr><td><b>{esc(s.id)}</b></td><td>{esc(s.name)}</td>"
                   f"<td class=num>{esc(limit_label(s))} <span class=muted>{esc(s.unit)}</span></td>"
                   f"<td>{esc(s.corners)}{f' · MC {s.mc}' if s.mc else ''}</td><td><code>{esc(s.test)}</code></td></tr>"
                   for s in b.specs)
    return ('<div class="table-wrap"><table class="specs"><thead><tr><th>ID<th>指标<th>限值<th>工艺角<th>用例</tr></thead><tbody>'
            + rows + "</tbody></table></div>")


def blocks_index(site: Site, data: dict[str, BlockData]) -> str:
    cards = []
    for bd in data.values():
        cards.append(block_card(site, bd, "../"))
    body = f"""<div class="page-head"><p class="eyebrow">模块</p><h1>模块一览</h1>
<p class="lead">6 个待做晶体管级设计的模块与顶层。每个页面包含端口、规格、验收用例、验证结果和可交互的原理图。</p></div>
<div class="cards">{''.join(cards)}</div>"""
    return page(site, title="模块", body=body, active="blocks", root="../")


def block_card(site: Site, bd: BlockData, root: str) -> str:
    b = bd.b
    rows = judged_rows(bd)
    ok = sum(1 for r in rows if r and r.status == "pass")
    bad = sum(1 for r in rows if r and r.status == "fail")
    n = len(rows)
    views = " ".join(chip("pass" if (ROOT / p).is_file() or (v == "xtor" and bd.xtor_files) else "none", v) for v, p in b.views.items())
    prog = f"{ok}/{n} 通过" + (f" · {bad} 不通过" if bad else "")
    return f"""<a class="card block" href="{root}blocks/{b.name}.html">
<div class="card-top"><code>{esc(b.name)}</code>{status_chip(b.status)}</div>
<p>{esc(b.raw['title'])}</p>
<div class="card-foot">{stepper(b.status)}<span class="muted">v{esc(b.raw['version'])} · {card_selection(site, b)}</span></div>
<div class="card-foot">{views}<span class="{'bad-t' if bad else 'muted'}">{prog}</span></div></a>"""


# ------------------------------------------------------------------ overview
def stat(label: str, value: str, sub: str = "") -> str:
    return f'<div class="stat"><div class="k">{esc(label)}</div><div class="v">{value}</div><div class="s">{sub}</div></div>'


def cdac_table(a) -> str:
    red = a.redundancy()
    wmax = float(a.w.max())
    rows = []
    for k, (w, s) in enumerate(zip(a.w, a.sampled), 1):
        bar = f'<span class="bar-cell"><i style="width:{max(2, 100 * math.sqrt(w / wmax)):.0f}%"></i></span>'
        r = f"{red[k - 1]:g}" if k - 1 < len(red) else "–"
        rows.append(f"<tr><td class=num>{k}</td><td class=num>{w:g}</td><td>{bar}</td><td>{'采样' if s else '<span class=muted>中性</span>'}</td><td class=num>{r}</td></tr>")
    return ('<div class="table-wrap"><table class="compact"><thead><tr><th>决策<th>电容权重<th>相对大小（√）<th>跟踪期间<th>冗余容限 (LSB)</tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def collaboration(site: Site, root: str) -> str:
    """The entry for a person to hand to their agent: the rendered CONTRIBUTING.md and its raw address, with a copy button."""
    raw = CONTRIBUTING_RAW.format(repo=site.repo)
    return f"""<section class="collab" id="collab"><h2>参与协作</h2>
<p>想为某个模块提交一个晶体管级候选、或者让自己的 AI 助手（agent）来帮忙？把下面这个地址交给它：无需事先申请，任何人随时可以提交；
协作流程（§4 提交候选）里写明了候选的命名、<code>candidate.yaml</code>、PR 规则，以及候选怎样被评比和选定。</p>
<div class="copyline"><code id="contrib-raw">{esc(raw)}</code><button type="button" class="btn small" data-copy="{esc(raw)}">复制</button></div>
<div class="cta"><a class="btn primary" href="{esc(contributing_href(site, root))}">提交候选（协作流程 §4）→</a>
<a class="btn" href="{esc(raw)}" target="_blank" rel="noopener">原始 Markdown ↗</a></div>
</section>"""


def design_library(site: Site) -> str:
    """Where the design itself is: the RNL library and the netlists on GitHub, and the whole design in the viewer."""
    top = site.full_viewer_href("design/top/adc_top.scs", "adc_top")
    return f"""<section class="design" id="design"><h2>设计库</h2>
<p>设计数据全部是文本：<b>Spectre 网表</b>写电路，<b>RNL</b> 写在网表注释里，说明原理图怎么画（符号、位置、连线）。
<code>design/rnl/</code> 是项目的 RNL 库：<code>adc28.rnl</code> 引入标准符号，另有由规格生成的模块符号和 Verilog-A 符号文件。
下面的查看器链接用清单（manifest）把这些文件作为一个整体打开，整个设计的原理图可以逐层展开。</p>
<div class="cta">
<a class="btn primary" data-top-viewer href="{esc(top)}" target="_blank" rel="noopener">在查看器中打开完整设计（顶层 adc_top）↗</a>
<a class="btn" href="{esc(site.gh('design/rnl', True))}" target="_blank" rel="noopener">RNL 库 <code>design/rnl/</code> ↗</a>
<a class="btn" href="{esc(site.gh('design', True))}" target="_blank" rel="noopener">网表 <code>design/</code> ↗</a>
<a class="btn" href="{esc(site.gh('tb', True))}" target="_blank" rel="noopener">测试台 <code>tb/</code> ↗</a></div>
</section>"""


def draft_cell(site: Site, b) -> str:
    """Home table, "草稿预览（未评审）": the newest open PR's draft result (a PR candidate's, or a legacy draft's), marked as a draft."""
    pr_cands = [c for c in site.cands.get(b.name, []) if c.source == "pr"]
    pvs = site.previews.get(b.name) or []
    best_cand = max(pr_cands, key=lambda c: c.pr.updated, default=None)
    legacy = pvs[0] if pvs else None
    if best_cand and (legacy is None or best_cand.pr.updated >= legacy.pr.updated):
        r = best_cand.row
        fail = f" · {r['specs_failed']} 不通过" if r["specs_failed"] else ""
        return (f'<a href="blocks/{b.name}.html#{best_cand.anchor}"><code>{esc(best_cand.name)}</code> {r["specs_passed"]}/{r["specs_total"]} 通过{fail}</a> '
                f'{chip("stale", "草稿", DRAFT)}')
    if legacy and legacy.ok and legacy.counts[2]:
        p, f, n = legacy.counts
        return (f'<a href="blocks/{b.name}.html#pr{legacy.pr.number}">{p}/{n} 通过{f" · {f} 不通过" if f else ""}</a> '
                f'{chip("stale", "草稿", DRAFT)} {chip("none", "未迁移", "未迁移为候选")}')
    if legacy:
        return f'<a href="blocks/{b.name}.html#pr{legacy.pr.number}" class="muted">仅元数据</a>'
    return '<span class="muted">–</span>'


def combo_blocks_cell(site: Site, c) -> str:
    """The transistor-level blocks of a combination with their candidate, display name and state; the rest is behavioral."""
    if not c.xtor:
        return "<b>全部行为级</b>"
    if c.legacy:
        return "<b>全部晶体管级</b> <small class=muted>（旧的单一 xtor 视图）</small>"
    lines = []
    for b in c.xtor:
        text = f"<code>{esc(b.block.replace('adc_', ''))}</code> " + (f"<code>{esc(b.candidate)}</code>" if b.candidate else "")
        who = f" <small class=muted>{esc(b.author_text)}</small>" if b.author_text else ""
        chips = ""
        if b.selected:
            chips += " " + chip("pass", "★ 选定", "块规格的 selected: 是这个候选")
        if not b.merged:
            chips += " " + chip("stale", f"未合并{f' · PR #{b.pr}' if b.pr else ''}", "只在开放的 PR 里，未评审")
        elif b.verification == "verified":
            chips += " " + chip("pass", "已复核", f"{b.verified} / {b.results} 个结果经项目负责人复跑核对")
        elif b.verification == "self-reported":
            chips += " " + chip("none", "自报", f"{b.results} 个结果都没有项目负责人的复核记录")
        elif b.verification == "mixed":
            chips += " " + chip("stale", f"部分复核 {b.verified}/{b.results}", "有的结果已复核，有的是自报")
        lines.append(f"<div>{text}{who}{chips}</div>")
    n_other = len(site_blocks_without_top()) - len(c.xtor)
    return "".join(lines) + (f"<small class=muted>其余 {n_other} 个模块行为级</small>" if n_other > 0 else "")


def site_blocks_without_top() -> list[str]:
    from adcflow.specs import blocks as spec_blocks
    return [b for b in spec_blocks() if b != "adc_top"]


def combo_row(site: Site, c) -> str:
    cov = "".join(f'<div><code>{esc(t.test)}</code> <b>{t.corners}/{t.required}</b>'
                  + (f' <small class=muted>（{t.results} 个结果）</small>' if t.results != t.corners else "") + "</div>" for t in c.tests)
    spec_title = (f"共 {c.specs_total} 项有限值的规格；这里只数在已覆盖的角上适用并有结果的" + (f"；不通过：{', '.join(c.failing)}" if c.failing else ""))
    specs = (f'<span title="{esc(spec_title)}"><b class="{"bad-t" if c.failing else "ok-t"}">{c.specs_pass}</b> / {c.specs_applicable}</span>'
             + (f'<br><small class="bad-t">{esc(", ".join(c.failing))}</small>' if c.failing else ""))
    metrics = []
    for m in c.metrics:
        bad = m.margin is not None and m.margin < 0
        marg = f" <small class=\"{'bad-t' if bad else 'muted'}\">（{m.margin:+.3g}）</small>" if m.margin is not None else ""
        metrics.append(f'<div title="{esc(m.name)}；限值 {esc(m.limit)}"><b>{esc(m.spec)}</b> {fmt(m.value)} {esc(m.unit)}{marg} '
                       f'<small class=muted>@ {esc(m.corner)}</small></div>')
    power = ("<br>".join(f"{esc(k.upper())} {fmt(v)}" for k, v in c.power.items()) + f" mW <small class=muted>@ {esc(c.power_corner)}</small>") if c.power else "–"
    state = (chip("pass", "新鲜") if not c.stale else chip("stale", f"过期 {c.stale}/{c.results}", "这些结果的输入文件自仿真后已变化"))
    if c.errors:
        state += " " + chip("fail", f"错误 {c.errors}")
    kind = (chip("none", "全行为级") if not c.xtor else chip("st-xtor-wip", f"混合 · {c.n_xtor} 个晶体管级") if not c.legacy
            else chip("st-xtor-review", "全部晶体管级"))
    subset = ("" if c.full else " " + chip("stale", "回归子集", "只覆盖部分工艺角（quick = 7 个角），不是 45 角签核"))
    links = " ".join(f'<a href="{esc(site.gh(p, True))}" target="_blank" rel="noopener" title="{esc(p)}">{esc(t.replace("tb_top_", ""))} ↗</a>' for t, p in c.dirs.items())
    return (f'<tr><td data-label="组合"><code>{esc(c.signature)}</code><br>{kind}{subset}</td>'
            f'<td data-label="晶体管级模块">{combo_blocks_cell(site, c)}</td>'
            f'<td data-label="工艺角覆盖（每个顶层测试）" class="nw">{cov}</td><td data-label="顶层规格 通过 / 适用" class=num>{specs}</td>'
            f'<td data-label="关键指标（最差值 @ 工艺角）" class="nw">{"".join(metrics) or "–"}</td><td data-label="功耗" class="nw">{power}</td>'
            f'<td data-label="状态">{state}</td><td data-label="结果">{links}</td></tr>')


def combos_section(site: Site) -> str:
    """Home page: the verification combinations of the top level, from results/adc_top/<test>/<view signature>/."""
    from adcflow.corners import corner_set
    cs = site.combos
    quick, allc = len(corner_set("quick")), len(corner_set("all"))
    head = ('<thead><tr><th>组合<th>晶体管级模块<th>工艺角覆盖<th title="顶层规格：在已覆盖的角上适用并有结果的规格里通过的">规格<th>关键指标<th>功耗<th>状态<th>结果</tr></thead>')
    body = "".join(combo_row(site, c) for c in cs) if cs else '<tr><td colspan=8 class=muted>还没有顶层结果。</td></tr>'
    return f"""<section id="combos"><h2>验证组合</h2>
<p class="muted legend">顶层（<code>adc_top</code>）的仿真按<b>哪些模块是晶体管级</b>分组：全行为级是基线；换进某个候选的混合运行记录在
<code>results/adc_top/&lt;测试&gt;/&lt;视图签名&gt;/</code>，每个签名一行（<code>xtor-clkgen@候选</code> = 只有 clkgen 换成该候选，其余行为级）。
上面“关键数字”里的通过率只统计行为级基线，<b>不包含</b>晶体管级候选和混合运行。
标“回归子集”的行只跑了部分工艺角：<code>quick</code> = {quick} 个角的回归子集，不是 {allc} 个角的签核；覆盖列是已有结果的角 / 规格要求的角。
判定和新鲜度与验证页是同一套（<code>adcflow</code> 的 <code>judge</code>）；“已复核”指该候选的结果经项目负责人复跑核对，否则是自报。</p>
<div class="table-wrap"><table class="combos">{head}<tbody>{body}</tbody></table></div></section>"""


def live_overview(site: Site, data: dict[str, BlockData]) -> str:
    """One table across the blocks: owner, status on main, newest open PR (draft / CI), its last update, open notices."""
    live = site.live
    rows = []
    for bd in data.values():
        b = bd.b
        pr, upd, notes = livepanel.overview_cells(live, b.name, site.repo)
        draft = draft_cell(site, b)
        rows.append(f"""<tr><td><a href="blocks/{b.name}.html"><code>{esc(b.name)}</code></a></td>
<td>{cand_cell(site, b)}</td><td>{status_chip(b.status)}</td>
<td>{pr}</td><td class=muted>{upd}</td><td>{draft}</td><td class=num>{notes}</td></tr>""")
    note = (livepanel.unavailable_note(live) if not live.ok else "")
    return f"""<section id="live"><h2>实时进展 {livepanel.stamp_html(live)}</h2>
<p class="muted legend">状态是主分支上的（来自 <code>specs/blocks/*.yaml</code>）；晶体管级工作在各模块的 PR 里，下表显示每个模块最近更新的进行中 PR
（草稿 / 待评审、CI 状态）和未关闭的通知数。只显示标题和状态，不显示正文；站点每小时重建一次。</p>{note}
<div class="table-wrap"><table class="live"><thead><tr><th>模块<th>候选<th>主分支状态<th>最新进行中 PR<th>最近更新 (UTC)<th title="取自该 PR 的提交，未评审，不计入主分支">草稿预览（未评审）<th>通知</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div></section>"""


def extra_waits(add) -> str:
    """timing.t_dac_add (extra DAC wait after decision 1, 2, ...) as text, e.g. " · 附加 DAC 等待 +10/+30 ps（判决 3/4）"."""
    steps = [(k + 1, float(v)) for k, v in enumerate(add or []) if float(v) > 0]
    if not steps:
        return ""
    waits = "/".join(f"+{v * 1e12:g}" for _, v in steps)
    return f" · 附加 DAC 等待 {waits} ps（判决 {'/'.join(str(k) for k, _ in steps)} 之后）"


def overview(site: Site, data: dict[str, BlockData]) -> str:
    a = arch()
    raw = a.raw
    s = a.summary()
    cnt = verdict_counts(data)
    enob, enob_doc = None, None
    for d in data["adc_top"].docs if "adc_top" in data else []:
        if d["test"] == "tb_top_sine" and d["corner"] == "tt_nom_27":
            enob, enob_doc = d["metrics"].get("enob"), d
    # PyYAML reads 100.0e6 as a string; list values (timing.t_dac_add, per DAC step) are not scalars
    t = {k: float(v) for k, v in raw["timing"].items() if not isinstance(v, (list, tuple))}
    tg = raw["targets"]
    stats = "".join([
        stat("采样率", f"{t['fs'] / 1e6:g}<small> MS/s</small>", "单一 CLK，高电平采样，低电平保持 + 转换"),
        stat("分辨率", f"{s['bits_equiv']:.2f}<small> bit</small>", f"{raw['conversion']['n_decisions']} 次异步判决 · {s['levels']} 个码"),
        stat("满量程", f"{s['FS_peak_diff_V']:.3f}<small> Vp</small>", f"差分峰值，VREF = {raw['reference']['vref']:g} V"),
        stat("ENOB 目标", f"&gt; {tg['enob_min']:g}<small> bit</small>", f"@ 50 MHz, −1 dBFS, 45 个角 · TT 设计目标 {tg['enob_design']:g}"),
        stat("行为级 ENOB", (f"{enob:.2f}<small> bit</small>" if enob else "–"),
             "顶层行为级仿真，TT/0.9 V/27 °C" + (f" · {site.evidence(evidence_path(enob_doc), '证据 ↗', doc=enob_doc)}" if enob_doc else "")),
        stat("LSB", f"{s['LSB_uV']:.1f}<small> µV</small>", f"C_S = {s['C_S_per_side_pF']:.3f} pF / 侧 · kT/C {s['kTC_noise_27C_uV']:.0f} µV"),
        stat("转换时间", f"≤ {t['t_conv_max'] * 1e9:g}<small> ns</small>",
             f"最坏角，每次比较 ≤ {t['t_cycle_max'] * 1e12:g} ps" + extra_waits(raw["timing"].get("t_dac_add"))),
        stat("工艺 / 电源", "28<small> nm</small>", f"{PROCESS} · {raw['process']['vdd_core']:g} V / {raw['process']['vdd_io']:g} V"),
    ])
    pct = round(100 * cnt["pass_"] / max(cnt["total"], 1))
    health = f"""<div class="health"><div class="meter" role="img" aria-label="{cnt['pass_']} 项通过，共 {cnt['total']} 项">
<i class="pass" style="width:{100 * cnt['pass_'] / max(cnt['total'], 1):.1f}%"></i><i class="fail" style="width:{100 * cnt['fail'] / max(cnt['total'], 1):.1f}%"></i></div>
<p><b>行为级基线</b>（模块级行为模型 + 全行为级顶层，不含晶体管级候选和混合运行）：<b>{cnt['pass_']}</b> / {cnt['total']} 项有限值的规格通过（{pct}%），<b class="{'bad-t' if cnt['fail'] else ''}">{cnt['fail']}</b> 项不通过，
<b>{cnt['none']}</b> 项尚无结果；只在 TT 一个角验证过：{cnt['pass_'] - cnt['full']} 项，全部要求的角：{cnt['full']} 项{f'，过期：{cnt["stale"]}' if cnt['stale'] else ''}。
<a href="verification.html">详细结果 →</a> · <a href="#combos">晶体管级 / 混合顶层的验证组合 ↓</a></p></div>"""
    arch_rows = [
        ("架构", f"底板采样 · 分裂电容冗余 CDAC（{len(a.w)} 个权重）· {raw['conversion']['n_decisions']} 次异步判决"),
        ("原始码", "权重 " + " ".join(f"{int(w)}" for w in a.out_weights) + f"；重构 <code>code = Σ W·D</code>，共 {s['levels']} 个码"),
        ("输入", f"单端 0 … {raw['reference']['vref']:g} V，共模 {raw['reference']['vin_cm']:g} V，每端 {tg['source_impedance']:g} Ω 源阻抗，无输入驱动"),
        ("参考", f"VREF_IN {raw['reference']['vref']:g} V → 片内驱动 <code>adc_ref</code> → VREFP；全片内去耦"),
        ("功耗", "项目不设上限，逐电源报告（越低越好）"),
        ("输出", "并行原始码 D13…D0 + RDY"),
    ]
    arch_html = "".join(f"<tr><th scope=row>{k}</th><td>{v}</td></tr>" for k, v in arch_rows)
    cards = "".join(block_card(site, bd, "") for bd in data.values())
    top_href = site.full_viewer_href("design/top/adc_top.scs", "adc_top")
    enob_figs = figure_strip(site, enob_doc, "") if enob_doc else ""
    collab_sec = collaboration(site, "") if has_doc("contributing") else ""
    body = f"""<section class="hero">
<p class="eyebrow">{PROCESS} · 异步 SAR</p>
<h1>ADC-12b-100M</h1>
<p class="lead">100 MS/s、12 bit 级异步 SAR ADC。整个设计只有 <b>Spectre 网表 + RNL 原理图</b>、Verilog-A 行为级模型和 Python 流程，没有图形化原理图编辑器。
这个网站由仓库自动生成，随每个 PR 更新。</p>
<div class="cta">
<a class="btn primary big" data-top-viewer href="{esc(top_href)}" target="_blank" rel="noopener">打开顶层原理图 adc_top ↗</a>
<a class="btn big" href="verification.html">验证结果</a><a class="btn big" href="progress.html">模块进展</a></div>
</section>
<section><h2 id="numbers">关键数字</h2><div class="stats">{stats}</div>{enob_figs}{health}</section>
{live_overview(site, data)}
{combos_section(site)}
<section><h2 id="top">顶层原理图</h2>
{viewer(site, [f for f in data['adc_top'].files if f['kind'] in ('struct', 'behav')] or data['adc_top'].files, 'v-top', 520,
        '顶层结构网表 adc_top.scs（同一个文件适用于任意视图组合）。双击模块进入下一层；也可以到各模块页面看它的行为级 / 晶体管级网表。')}
</section>
{design_library(site)}
<section><h2 id="arch">架构摘要</h2><div class="split">
<div><div class="table-wrap"><table class="kv"><tbody>{arch_html}</tbody></table></div>
<p><a href="docs/architecture.html">完整架构文档 →</a> · <a href="docs/reference.html">参考电压研究 →</a></p></div>
<div><h3>CDAC 权重与冗余</h3>{cdac_table(a)}</div></div></section>
<section><h2 id="blocks">模块</h2><div class="cards">{cards}</div></section>
{collab_sec}"""
    return page(site, title="概览", body=body, active="index", root="", wide=True)


# ------------------------------------------------------------------ progress
def progress(site: Site, data: dict[str, BlockData]) -> str:
    rows = []
    for bd in data.values():
        b = bd.b
        rr = judged_rows(bd)
        ok = sum(1 for r in rr if r and r.status == "pass")
        bad = sum(1 for r in rr if r and r.status == "fail")
        ntb = len({t["netlist"] for t in b.tests.values()})
        v = {k: ((ROOT / p).is_file() or (k == "xtor" and bool(bd.xtor_files))) for k, p in b.views.items()}
        vc = " ".join(chip("pass" if ok_ else "none", k) for k, ok_ in v.items())
        rows.append(f"""<tr><td><a href="blocks/{b.name}.html"><code>{esc(b.name)}</code></a><br><small class=muted>{esc(b.raw['title'])}</small></td>
<td>{status_chip(b.status)}<br>{stepper(b.status)}</td><td>v{esc(b.raw['version'])}</td><td>{selection_html(site, b, '')}</td>
<td>{vc}</td><td class=num>{ntb}</td>
<td class=num><b>{ok}</b>/{len(rr)}{f' <span class=bad-t>· {bad} 不通过</span>' if bad else ''}</td>
<td class=muted>{esc(last_change(bd) or '–')}</td></tr>""")
    legend = " → ".join(f"{status_chip(s)}" for s in STATUS_ORDER)
    tags = ""
    for t in reversed(site.build.tags):
        href = f"https://github.com/{site.build.repo}/tree/{t.name}" if site.build.repo else ""
        name = f"<a href='{esc(href)}' rel=noopener><code>{esc(t.name)}</code></a>" if href else f"<code>{esc(t.name)}</code>"
        tags += f"<li><span class='when'>{esc(t.date)}</span><div>{name} <span class='muted'>{esc(t.sha)}</span><br>{esc(t.subject)}</div></li>"
    if not tags:
        tags = "<li class='muted'>没有标签（本次构建没有拉取 git 标签）。</li>"
    body = f"""<div class="page-head"><p class="eyebrow">进展</p><h1>模块进展</h1>
<p class="lead">状态、负责人和版本来自 <code>specs/blocks/*.yaml</code>；视图是否存在由仓库里的网表文件决定。</p></div>
<section><h2 id="blocks">各模块</h2><p class="muted legend">状态流程：{legend}</p>
<div class="table-wrap"><table class="progress"><thead><tr><th>模块<th>状态<th>规格版本<th>选定候选 / 负责人<th>视图<th>测试台<th>规格通过<th>最近更新</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="muted">“规格通过”按每条规格的最高级视图（xtor 优先于 behav）统计，不含仅报告的功耗指标（没有限值，不判定）；覆盖的工艺角数见验证页。
晶体管级设计的分工与要点见 <a href="docs/handoff.html">分工包</a>。</p></section>
<section><h2 id="tags">冻结点（git 标签）</h2><ul class="timeline">{tags}</ul></section>"""
    return page(site, title="进展", body=body, active="progress", root="")


def verification(site: Site, data: dict[str, BlockData]) -> str:
    cnt = verdict_counts(data)
    tiles = "".join([
        stat("规格总数", str(cnt["total"]), "行为级基线，不含候选"), stat("通过", f"<span class=ok-t>{cnt['pass_']}</span>"),
        stat("不通过", f"<span class='{'bad-t' if cnt['fail'] else ''}'>{cnt['fail']}</span>"),
        stat("无结果", str(cnt["none"])), stat("过期", f"<span class='{'warn-t' if cnt['stale'] else ''}'>{cnt['stale']}</span>", "自仿真后文件已变"),
    ])
    nav = " ".join(f'<a class="pill" href="#{n}">{esc(n)}</a>' for n in data)
    secs = "".join(verification_section(site, bd, 2) for bd in data.values())
    body = f"""<div class="page-head"><p class="eyebrow">验证</p><h1>验证结果</h1>
<p class="lead">记录在 <code>results/&lt;block&gt;/&lt;test&gt;/&lt;view&gt;/&lt;corner&gt;.json</code> 的仿真结果，用当前规格限值重新判定
（与 <code>python -m adcflow report</code> 同一套逻辑）。结果里的文件哈希与当前网表不一致时标为<b>过期</b>。</p></div>
<div class="stats small">{tiles}</div>
<div class="pills" aria-label="跳到模块">{nav}</div>
<p class="muted legend">“工艺角”一列：已记录 / 规格要求的角数（<code>typ</code> = 1，<code>all</code> = 45）。
行为级基线只在 TT/0.9 V/27 °C 一个角验证，所以覆盖都是 1/45；晶体管级视图要补满。验证约定见 <a href="docs/verification.html">验证计划</a>。</p>
{secs}"""
    return page(site, title="验证", body=body, active="verification", root="", wide=True)


# ------------------------------------------------------------------ docs
def docs_index(site: Site) -> str:
    cards = "".join(f'<a class="card doc" href="{"../index.html" if s == "readme" else s + ".html"}"><div class="card-top"><b>{esc(t)}</b></div>'
                    f'<p>{esc(d)}</p><p class="muted"><code>{esc(f)}</code></p></a>' for f, s, t, d in docs() if s != "readme")
    body = f"""<div class="page-head"><p class="eyebrow">文档</p><h1>文档</h1>
<p class="lead">仓库 <code>docs/</code> 与 <code>CONTRIBUTING.md</code> 的渲染版，内容以仓库为准。</p></div><div class="cards">{cards}</div>"""
    return page(site, title="文档", body=body, active="docs", root="../")


def doc_page(site: Site, slug_: str, title: str, src: str, html_body: str, heads: list[tuple[int, str, str]]) -> str:
    toc = "".join(f'<a class="l{lv}" href="#{i}">{esc(t)}</a>' for lv, i, t in heads if lv in (2, 3))
    body = f"""<div class="doc-layout"><aside class="toc" aria-label="目录"><details open><summary>目录</summary>{toc}</details></aside>
<article class="prose"><p class="eyebrow">文档 · <a href="{esc(site.gh(src))}" rel="noopener"><code>{esc(src)}</code></a></p>
<h1>{esc(title)}</h1>{html_body}</article></div>"""
    return page(site, title=next((t for f, s_, t, _ in docs() if s_ == slug_), title), body=body,
                active="collab" if slug_ == "contributing" else "docs", root="../", wide=True)
