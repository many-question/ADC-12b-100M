"""HTML for the live activity of the blocks (open PRs and notices). Metadata only; every text is escaped.

Kept free of the other site modules (no Markdown, no adcflow) so that the tests can import it alone.
"""

from __future__ import annotations

from html import escape
from urllib.parse import quote_plus

from .live import PR, Live

CI = {"pass": ("pass", "CI 通过"), "fail": ("fail", "CI 失败"), "running": ("run", "CI 运行中"),
      "none": ("none", "无 CI"), "unknown": ("none", "CI 未知")}


def esc(s) -> str:
    return escape(str(s), quote=True)


def chip(kind: str, text: str, title: str = "") -> str:
    t = f' title="{esc(title)}"' if title else ""
    return f'<span class="chip {kind}"{t}>{esc(text)}</span>'


def when(iso: str) -> str:
    """'2026-10-29T06:17:03Z' -> '2026-10-29 06:17' (UTC)."""
    return iso[:16].replace("T", " ") if iso else "–"


def stamp_html(live: Live) -> str:
    return f'<span class="stamp muted">数据更新于 {esc(live.fetched_at)} UTC</span>'


def search_url(repo: str, kind: str, block: str) -> str:
    """GitHub search of the open PRs / issues whose title starts with [<block>]."""
    return f"https://github.com/{repo}/{'pulls' if kind == 'pr' else 'issues'}?q=" + quote_plus(f'is:{kind} is:open in:title "[{block}]"')


def pr_badges(pr: PR) -> str:
    kind, label = CI.get(pr.ci, CI["unknown"])
    return (chip("none" if pr.draft else "st-xtor-review", "草稿" if pr.draft else "待评审",
                 "草稿 PR" if pr.draft else "已就绪，等待评审") + " " + chip(kind, label))


def pr_link(pr: PR) -> str:
    return f'<a href="{esc(pr.url)}" target="_blank" rel="noopener">#{pr.number}</a> {esc(pr.title)}'


def _who(login: str) -> str:
    return f'<a href="https://github.com/{esc(login)}" target="_blank" rel="noopener">@{esc(login)}</a>' if login else "–"


def unavailable_note(live: Live) -> str:
    return (f'<p class="empty">无法获取实时数据（{esc(live.fetched_at)} UTC）：{esc(live.error)}。'
            f'PR 与通知请直接看 GitHub；下一次重建会再试。</p>')


def block_panel(live: Live, block: str, repo: str) -> str:
    """The "进行中" section of a block page: its open PRs and its open notices."""
    head = f'<h2 id="live">进行中 {stamp_html(live)}</h2>'
    if not live.ok:
        return f'<section>{head}{unavailable_note(live)}</section>'
    prs, issues = live.block_prs(block), live.block_issues(block)
    if not prs and not issues:
        return (f'<section>{head}<p class="empty">现在没有标题以 <code>[{esc(block)}]</code> 开头的进行中 PR 或通知。</p></section>')
    body = ""
    if prs:
        rows = "".join(f"<tr><td>{pr_link(p)}</td><td>{pr_badges(p)}</td><td>{_who(p.author)}</td>"
                       f"<td class=muted>{esc(when(p.updated))}</td></tr>" for p in prs)
        body += ('<h3>进行中的 PR</h3><div class="table-wrap"><table class="live"><thead><tr><th>PR<th>状态<th>作者<th>最近更新 (UTC)</tr></thead>'
                 f"<tbody>{rows}</tbody></table></div>")
    if issues:
        rows = "".join(f'<tr><td><a href="{esc(i.url)}" target="_blank" rel="noopener">#{i.number}</a> {esc(i.title)}</td>'
                       f"<td class=num>{i.comments}</td><td class=muted>{esc(when(i.updated))}</td></tr>" for i in issues)
        body += ('<h3>通知（规格变更等）</h3><div class="table-wrap"><table class="live"><thead><tr><th>通知<th>评论<th>最近更新 (UTC)</tr></thead>'
                 f"<tbody>{rows}</tbody></table></div>"
                 '<p class="muted legend">评论数为负责人确认等回复；页面只显示标题和数量，不显示正文。</p>')
    links = (f'<p class="muted legend"><a href="{esc(search_url(repo, "pr", block))}" target="_blank" rel="noopener">在 GitHub 上查看全部 PR ↗</a>'
             f' · <a href="{esc(search_url(repo, "issue", block))}" target="_blank" rel="noopener">全部通知 ↗</a></p>')
    return f"<section>{head}{body}{links}</section>"


def newest_pr(live: Live, block: str) -> PR | None:
    prs = live.block_prs(block)
    return max(prs, key=lambda p: p.updated) if prs else None


def overview_cells(live: Live, block: str, repo: str) -> tuple[str, str, str]:
    """(newest open PR with its draft / CI badges, its last update, open notices) cells of the home table."""
    if not live.ok:
        return '<span class="muted">未获取</span>', "–", "–"
    p = newest_pr(live, block)
    n = len(live.block_issues(block))
    pr_cell = (f"{pr_link(p)}<br>{pr_badges(p)}" if p else '<span class="muted">无</span>')
    if len(live.block_prs(block)) > 1:
        pr_cell += f' <span class="muted">+{len(live.block_prs(block)) - 1}</span>'
    notice = (f'<a href="{esc(search_url(repo, "issue", block))}" target="_blank" rel="noopener">{n}</a>' if n else "0")
    return pr_cell, esc(when(p.updated)) if p else "–", notice
