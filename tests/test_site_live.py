"""Data layer of the live per-block panel (site/sitegen/live.py, livepanel.py): fixtures only, no network."""

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))

from sitegen import live, livepanel                                # noqa: E402

BLOCKS = ["adc_bootstrap", "adc_clkgen", "adc_comp", "adc_top"]
NOW = datetime(2026, 10, 29, 6, 17, 40, tzinfo=timezone.utc)


def pull(n, title, sha="a" * 40, draft=False, login="alice", updated="2026-10-28T15:57:00Z"):
    return {"number": n, "title": title, "html_url": f"https://github.com/o/r/pull/{n}", "draft": draft,
            "user": {"login": login}, "created_at": "2026-10-27T10:00:00Z", "updated_at": updated,
            "head": {"sha": sha}, "body": "SECRET BODY"}


def issue(n, title, comments=0, login="bob", is_pr=False):
    d = {"number": n, "title": title, "html_url": f"https://github.com/o/r/issues/{n}", "comments": comments,
         "user": {"login": login}, "created_at": "2026-10-27T10:00:00Z", "updated_at": "2026-10-28T15:02:00Z",
         "body": "SECRET BODY"}
    if is_pr:
        d["pull_request"] = {"url": "x"}
    return d


class Api:
    """get(path) over canned answers, in the shape of the GitHub API; records the paths asked for."""

    def __init__(self, pulls=(), issues=(), runs=None, statuses=None, fail=None, pr_ci_fail=False):
        self.pulls, self.issues = list(pulls), list(issues)
        self.runs, self.statuses = runs or {}, statuses or {}
        self.fail, self.pr_ci_fail, self.asked = fail, pr_ci_fail, []

    def __call__(self, path):
        self.asked.append(path)
        if self.fail:
            raise self.fail
        base, _, query = path.partition("?")
        page = int(dict(q.split("=") for q in query.split("&")).get("page", "1")) if "page=" in query else 1
        window = lambda items: items[(page - 1) * live.PER_PAGE:page * live.PER_PAGE]    # noqa: E731
        if base == "/pulls":
            return window(self.pulls)
        if base == "/issues":
            return window(self.issues)
        if self.pr_ci_fail:
            raise live.LiveError("GitHub API answered 500")
        sha = base.split("/")[2]
        if base.endswith("/check-runs"):
            return {"check_runs": self.runs.get(sha, [])}
        return self.statuses.get(sha, {"state": "pending", "total_count": 0})


# ------------------------------------------------------------------ parsing and filtering
def test_parses_prs_and_issues_and_keeps_metadata_only():
    api = Api(pulls=[pull(25, "[adc_bootstrap] protect gate drive", draft=True)],
              issues=[issue(38, "[adc_bootstrap] spec 0.5.0", comments=2), issue(40, "[adc_bootstrap] pr as issue", is_pr=True)],
              runs={"a" * 40: [{"status": "completed", "conclusion": "success"}]})
    got = live.collect(BLOCKS, api, NOW)
    assert got.ok and got.fetched_at == "2026-10-29 06:17"
    (p,) = got.block_prs("adc_bootstrap")
    assert (p.number, p.draft, p.author, p.ci, p.sha) == (25, True, "alice", "pass", "a" * 40)
    assert p.url.endswith("/pull/25")
    (i,) = got.block_issues("adc_bootstrap")              # the PR listed by the issues endpoint is not a notice
    assert (i.number, i.comments, i.author) == (38, 2, "bob")
    assert "SECRET BODY" not in repr(got)                  # bodies are never kept


def test_titles_are_filtered_per_block():
    api = Api(pulls=[pull(1, "[adc_comp] a"), pull(2, "[adc_clkgen] b"), pull(3, "no prefix"), pull(4, "[adc_comp_extra] c"),
                     pull(5, "  [adc_top] padded"), pull(6, "x [adc_comp] not at the start")],
              issues=[issue(7, "[adc_clkgen] notice"), issue(8, "unrelated")])
    got = live.collect(BLOCKS, api, NOW)
    assert {b: [p.number for p in v] for b, v in got.prs.items()} == {"adc_comp": [1], "adc_clkgen": [2], "adc_top": [5]}
    assert {b: [i.number for i in v] for b, v in got.issues.items()} == {"adc_clkgen": [7]}
    assert got.block_prs("adc_bootstrap") == [] and got.block_issues("adc_comp") == []


def test_newest_first_and_pagination():
    many = [pull(n, "[adc_comp] x", updated=f"2026-10-28T{n % 24:02d}:00:00Z") for n in range(1, live.PER_PAGE + 3)]
    got = live.collect(BLOCKS, Api(pulls=many), NOW)
    prs = got.block_prs("adc_comp")
    assert len(prs) == live.PER_PAGE + 2                   # the second page was read
    assert [p.updated for p in prs] == sorted((p.updated for p in prs), reverse=True)


# ------------------------------------------------------------------ CI state
@pytest.mark.parametrize("runs,status,want", [
    ([], None, "none"),
    ([{"status": "completed", "conclusion": "success"}], None, "pass"),
    ([{"status": "completed", "conclusion": "success"}, {"status": "completed", "conclusion": "skipped"}], None, "pass"),
    ([{"status": "completed", "conclusion": "success"}, {"status": "in_progress", "conclusion": None}], None, "running"),
    ([{"status": "queued", "conclusion": None}], None, "running"),
    ([{"status": "completed", "conclusion": "failure"}, {"status": "in_progress", "conclusion": None}], None, "fail"),
    ([{"status": "completed", "conclusion": "timed_out"}], None, "fail"),
    ([{"status": "completed", "conclusion": "cancelled"}], None, "none"),      # a superseded run is not a failure
    ([], {"state": "failure", "total_count": 2}, "fail"),
    ([], {"state": "pending", "total_count": 1}, "running"),
    ([], {"state": "pending", "total_count": 0}, "none"),                      # no statuses at all
    ([{"status": "completed", "conclusion": "success"}], {"state": "success", "total_count": 1}, "pass"),
])
def test_ci_state_reduction(runs, status, want):
    assert live.ci_state(runs, status) == want


def test_ci_of_a_pr_comes_from_its_head_commit():
    sha = "b" * 40
    api = Api(pulls=[pull(9, "[adc_comp] x", sha=sha)], runs={sha: [{"status": "completed", "conclusion": "failure"}]})
    assert live.collect(BLOCKS, api, NOW).block_prs("adc_comp")[0].ci == "fail"
    assert any(f"/commits/{sha}/check-runs" in p for p in api.asked)


def test_ci_lookup_failure_keeps_the_pr_with_unknown_ci():
    got = live.collect(BLOCKS, Api(pulls=[pull(9, "[adc_comp] x")], pr_ci_fail=True), NOW)
    assert got.ok and got.block_prs("adc_comp")[0].ci == "unknown"


# ------------------------------------------------------------------ API failure -> placeholder
@pytest.mark.parametrize("exc", [live.LiveError("GitHub API answered 403 (rate limit?)"), ValueError("x"), KeyError("number")])
def test_api_failure_gives_a_placeholder_not_an_exception(exc):
    got = live.collect(BLOCKS, Api(fail=exc), NOW)
    assert not got.ok and got.fetched_at == "2026-10-29 06:17" and got.error
    html = livepanel.block_panel(got, "adc_comp", "o/r")
    assert "无法获取实时数据" in html and "2026-10-29 06:17" in html
    assert "未获取" in livepanel.overview_cells(got, "adc_comp", "o/r")[0]


def test_http_errors_never_carry_the_token(monkeypatch):
    import urllib.error

    def boom(req, timeout=None):
        raise urllib.error.HTTPError(req.full_url, 403, "rate limited", {}, None)

    monkeypatch.setattr(live.urllib.request, "urlopen", boom)
    got = live.collect(BLOCKS, live.github_get("o/r", token="SECRET-TOKEN"), NOW)
    assert not got.ok and "403" in got.error and "SECRET-TOKEN" not in got.error


def test_no_repository_is_unavailable_without_a_request():
    got = live.fetch("", BLOCKS, NOW)
    assert not got.ok


# ------------------------------------------------------------------ name guard
def test_titles_that_trip_the_name_guard_are_left_out_not_fatal():
    bad = "[adc_comp] uses the " + "TS" + "MC" + " cells"            # the name is never written in one piece in the repo
    api = Api(pulls=[pull(1, bad), pull(2, "[adc_comp] fine")], issues=[issue(3, "[adc_comp] " + "ts" + "mc" + "28 notice")])
    got = live.collect(BLOCKS, api, NOW)
    assert got.ok
    assert [p.number for p in got.block_prs("adc_comp")] == [2]
    assert got.block_issues("adc_comp") == []
    assert got.skipped == ["PR #1", "issue #3"]


# ------------------------------------------------------------------ rendering
def test_titles_are_escaped():
    api = Api(pulls=[pull(1, '[adc_comp] <script>alert("x")</script>', login='a"b')], issues=[issue(2, "[adc_comp] <b>x</b> & y")])
    html = livepanel.block_panel(live.collect(BLOCKS, api, NOW), "adc_comp", "o/r")
    assert "<script>" not in html and "<b>x</b>" not in html
    assert "&lt;script&gt;" in html and "&lt;b&gt;x&lt;/b&gt; &amp; y" in html


def test_panel_shows_badges_stamp_and_search_links():
    api = Api(pulls=[pull(25, "[adc_comp] x", draft=True)], runs={"a" * 40: [{"status": "completed", "conclusion": "success"}]},
              issues=[issue(38, "[adc_comp] notice", comments=3)])
    html = livepanel.block_panel(live.collect(BLOCKS, api, NOW), "adc_comp", "o/r")
    assert "草稿" in html and "CI 通过" in html and "数据更新于 2026-10-29 06:17 UTC" in html
    assert "2026-10-28 15:57" in html                      # last update, UTC
    assert "is%3Apr+is%3Aopen+in%3Atitle+%22%5Badc_comp%5D%22" in html


def test_empty_block_says_so():
    html = livepanel.block_panel(live.collect(BLOCKS, Api(), NOW), "adc_comp", "o/r")
    assert "没有标题以" in html


def test_overview_cells_pick_the_newest_pr_and_count_notices():
    api = Api(pulls=[pull(1, "[adc_comp] old", updated="2026-10-20T00:00:00Z"), pull(2, "[adc_comp] new", updated="2026-10-28T00:00:00Z")],
              issues=[issue(3, "[adc_comp] n1"), issue(4, "[adc_comp] n2")])
    pr, upd, notes = livepanel.overview_cells(live.collect(BLOCKS, api, NOW), "adc_comp", "o/r")
    assert "#2" in pr and "#1" not in pr and "+1" in pr
    assert upd == "2026-10-28 00:00" and ">2<" in notes
