#!/usr/bin/env python3
"""Gate of the `site` workflow: can the event that started this run change the website?

Run in the `gate` job (main's code, stdlib only) on the event payload GitHub wrote to $GITHUB_EVENT_PATH. The workflow
rebuilds and deploys the site on pull request, notice (issue) and CI events as well as on pushes and the hourly schedule;
most of those events cannot change anything the site shows, and a skipped build also cannot cancel a deploy that is running.

What the site shows from GitHub: the open PRs and open issues whose title starts with "[<block>]" and the CI state of the PR
heads (sitegen/live.py, sitegen/preview.py). So an event is relevant when it concerns such a PR or issue:

  push / schedule / workflow_dispatch   always
  pull_request                          always (builds the preview artifact of the PR itself, as before)
  pull_request_target                   the PR title starts with "[<block>]"
  issues                                the issue title (or, for an edit, the title before it) starts with "[<block>]"
  issue_comment                         a comment on such an issue (comments on PRs show nothing)
  workflow_run (ci completed)           CI of a pull request whose head is an open "[<block>]" PR

Nothing from the payload is ever printed or put into a shell command: titles are attacker-controlled text (a printed
"::..." line is a workflow command). The output is a fixed reason code.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from sitegen import live                                        # noqa: E402  (stdlib only)

ALWAYS = {"push", "schedule", "workflow_dispatch", "pull_request"}
PR_ACTIONS = {"opened", "synchronize", "reopened", "ready_for_review", "converted_to_draft", "closed"}
ISSUE_ACTIONS = {"opened", "edited", "closed", "reopened"}


def block_names(root: Path) -> list[str]:
    return sorted(p.stem for p in (root / "specs" / "blocks").glob("*.yaml"))


def _title(obj) -> str:
    return str(obj.get("title") or "") if isinstance(obj, dict) else ""


def relevant(event: str, payload: dict, blocks: list[str], get: Callable[[str], object] | None = None) -> tuple[bool, str]:
    """(rebuild?, reason code). `get(path)` is the GitHub API (needed only for workflow_run); a failure rebuilds."""
    if event in ALWAYS:
        return True, "always"
    action = payload.get("action")
    if event == "pull_request_target":
        if action not in PR_ACTIONS:
            return False, "pr-action"
        return (True, "block-pr") if live.block_of(_title(payload.get("pull_request")), blocks) else (False, "not-a-block-pr")
    if event == "issues":
        if action not in ISSUE_ACTIONS:
            return False, "issue-action"
        before = ((payload.get("changes") or {}).get("title") or {}).get("from", "")
        if live.block_of(_title(payload.get("issue")), blocks) or (action == "edited" and live.block_of(str(before), blocks)):
            return True, "block-notice"
        return False, "not-a-block-notice"
    if event == "issue_comment":
        issue = payload.get("issue") or {}
        if action != "created":
            return False, "comment-action"
        if "pull_request" in issue:
            return False, "comment-on-pr"
        return (True, "block-notice-comment") if live.block_of(_title(issue), blocks) else (False, "not-a-block-notice")
    if event == "workflow_run":
        run = payload.get("workflow_run") or {}
        if run.get("event") != "pull_request":
            return False, "ci-not-on-pr"              # a push to a branch: the PR's own CI run reports the same head
        sha = str(run.get("head_sha") or "")
        try:
            for pr in live._pages(get, "/pulls?state=open"):              # noqa: SLF001 (the paging helper)
                if (pr.get("head") or {}).get("sha") == sha and live.block_of(_title(pr), blocks):
                    return True, "ci-of-block-pr"
        except Exception:                                # cannot tell: rebuild rather than miss a preview
            return True, "ci-unchecked"
        return False, "ci-not-of-a-block-pr"
    return True, "unknown-event"


def main() -> int:
    import json
    event = os.environ.get("GITHUB_EVENT_NAME", "")
    payload: dict = {}
    path = os.environ.get("GITHUB_EVENT_PATH")
    if path and Path(path).is_file():
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except ValueError:
            payload = {}
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    get = live.github_get(repo, live.token_from_env()) if repo else None
    ok, reason = relevant(event, payload, block_names(HERE.parent), get)
    print(f"gate: event={event} relevant={str(ok).lower()} reason={reason}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"relevant={str(ok).lower()}\nreason={reason}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
