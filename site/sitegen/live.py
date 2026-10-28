"""Live per-block activity from GitHub: open pull requests and notices (issues) titled "[<block>]".

Fetched at build time with the GitHub REST API (in Actions with the job's read-only GITHUB_TOKEN). Only metadata is
kept: number, title, link, draft flag, author login, created / updated time, head commit, CI state, comment count.
Bodies and comments are never requested into the result and never rendered.

The build must not depend on the API: any failure gives a `Live` with `ok=False`, which the pages show as a
"could not be fetched" note. A title that would trip the process-name guard is left out (and logged).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

from . import guard

API = "https://api.github.com"
PER_PAGE, MAX_PAGES = 100, 10
CI_FAIL = {"failure", "timed_out", "action_required", "startup_failure"}   # cancelled is a superseded run, not a failure


class LiveError(Exception):
    """The API could not be used; the message is safe to show (no tokens)."""


@dataclass
class PR:
    number: int
    title: str
    url: str
    draft: bool
    author: str
    created: str
    updated: str
    sha: str
    ci: str            # pass | fail | running | none | unknown


@dataclass
class Issue:
    number: int
    title: str
    url: str
    comments: int
    author: str
    created: str
    updated: str


@dataclass
class Live:
    ok: bool
    fetched_at: str                       # "YYYY-MM-DD HH:MM" UTC
    error: str = ""
    prs: dict[str, list[PR]] = field(default_factory=dict)
    issues: dict[str, list[Issue]] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)   # items left out by the name guard, for the build log

    def block_prs(self, block: str) -> list[PR]:
        return self.prs.get(block, [])

    def block_issues(self, block: str) -> list[Issue]:
        return self.issues.get(block, [])


def stamp(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")


def unavailable(error: str, now: datetime | None = None) -> Live:
    return Live(ok=False, fetched_at=stamp(now), error=error)


# ------------------------------------------------------------------ transport
def github_get(repo: str, token: str | None = None, timeout: float = 20.0) -> Callable[[str], object]:
    """`get(path)` -> parsed JSON of one API request. Raises LiveError (never including the token)."""
    def get(path: str) -> object:
        req = urllib.request.Request(API + f"/repos/{repo}" + path, headers={
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "adc-12b-100m-site", **({"Authorization": f"Bearer {token}"} if token else {})})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise LiveError(f"GitHub API answered {e.code}" + (" (rate limit?)" if e.code in (403, 429) else "")) from None
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise LiveError(f"GitHub API not reachable ({type(e).__name__})") from None
        except ValueError:
            raise LiveError("GitHub API answered something that is not JSON") from None
    return get


def token_from_env() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or None


# ------------------------------------------------------------------ reduction
def ci_state(check_runs: list[dict], status: dict | None) -> str:
    """One CI state for a commit from its check runs and its combined commit status:
    fail (any failed) > running (any unfinished) > pass > none (no checks at all)."""
    fail = running = ok = False
    for r in check_runs:
        if r.get("status") != "completed":
            running = True
        elif r.get("conclusion") in CI_FAIL:
            fail = True
        elif r.get("conclusion") in ("success", "neutral", "skipped"):
            ok = True
    if status and status.get("total_count", 0) > 0:
        s = status.get("state")
        if s in ("failure", "error"):
            fail = True
        elif s == "pending":
            running = True
        elif s == "success":
            ok = True
    return "fail" if fail else "running" if running else "pass" if ok else "none"


def block_of(title: str, blocks: list[str]) -> str | None:
    """The block a title is for: it starts with "[<block>]"."""
    t = title.lstrip()
    return next((b for b in blocks if t.startswith(f"[{b}]")), None)


def _pages(get: Callable[[str], object], path: str) -> list[dict]:
    out: list[dict] = []
    sep = "&" if "?" in path else "?"
    for page in range(1, MAX_PAGES + 1):
        chunk = get(f"{path}{sep}per_page={PER_PAGE}&page={page}")
        if not isinstance(chunk, list):
            raise LiveError("GitHub API answered an unexpected shape")
        out += chunk
        if len(chunk) < PER_PAGE:
            break
    return out


def _login(item: dict) -> str:
    return str((item.get("user") or {}).get("login") or "")


def collect(blocks: list[str], get: Callable[[str], object], now: datetime | None = None) -> Live:
    """Open `[<block>]` PRs and issues of the repository behind `get`; a failure gives an unavailable Live."""
    try:
        return _collect(blocks, get, now)
    except LiveError as e:
        return unavailable(str(e), now)
    except Exception as e:                           # a malformed answer must not fail the build either
        return unavailable(f"unexpected answer from the GitHub API ({type(e).__name__})", now)


def _collect(blocks: list[str], get: Callable[[str], object], now: datetime | None) -> Live:
    live = Live(ok=True, fetched_at=stamp(now))

    def allowed(*texts: str) -> bool:
        return not any(guard.contains(t) for t in texts)

    for p in _pages(get, "/pulls?state=open"):
        title = str(p.get("title") or "")
        block = block_of(title, blocks)
        if not block:
            continue
        if not allowed(title, _login(p)):
            live.skipped.append(f"PR #{p.get('number')}")
            continue
        sha = str((p.get("head") or {}).get("sha") or "")
        try:
            runs = get(f"/commits/{sha}/check-runs?per_page={PER_PAGE}")
            status = get(f"/commits/{sha}/status")
            ci = ci_state((runs or {}).get("check_runs", []), status if isinstance(status, dict) else None)
        except LiveError:
            ci = "unknown"
        live.prs.setdefault(block, []).append(PR(
            int(p["number"]), title, str(p.get("html_url") or ""), bool(p.get("draft")), _login(p),
            str(p.get("created_at") or ""), str(p.get("updated_at") or ""), sha, ci))
    for i in _pages(get, "/issues?state=open"):
        if "pull_request" in i:                      # the issues endpoint lists PRs too
            continue
        title = str(i.get("title") or "")
        block = block_of(title, blocks)
        if not block:
            continue
        if not allowed(title, _login(i)):
            live.skipped.append(f"issue #{i.get('number')}")
            continue
        live.issues.setdefault(block, []).append(Issue(
            int(i["number"]), title, str(i.get("html_url") or ""), int(i.get("comments") or 0), _login(i),
            str(i.get("created_at") or ""), str(i.get("updated_at") or "")))
    for lst in live.prs.values():
        lst.sort(key=lambda x: x.updated, reverse=True)
    for lst in live.issues.values():
        lst.sort(key=lambda x: x.updated, reverse=True)
    return live


def fetch(repo: str, blocks: list[str], now: datetime | None = None) -> Live:
    """Live data of `repo` through the real API (token from the environment when there is one)."""
    if not repo:
        return unavailable("repository unknown", now)
    return collect(blocks, github_get(repo, token_from_env()), now)
