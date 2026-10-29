"""Gate of the site workflow (site/events.py): which events can change the site. Fixture payloads, no network."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

import events                                                       # noqa: E402
from sitegen import live                                            # noqa: E402

BLOCKS = ["adc_bootstrap", "adc_comp", "adc_top"]


def pr(title, action="opened"):
    return {"action": action, "pull_request": {"title": title, "number": 5}}


def issue(title, action="opened", **extra):
    return {"action": action, "issue": {"title": title, "number": 9}, **extra}


# ------------------------------------------------------------------ events that always rebuild
@pytest.mark.parametrize("event", ["push", "schedule", "workflow_dispatch", "pull_request"])
def test_main_events_always_rebuild(event):
    assert events.relevant(event, {}, BLOCKS) == (True, "always")


# ------------------------------------------------------------------ pull_request_target
@pytest.mark.parametrize("action", sorted(events.PR_ACTIONS))
def test_block_pr_actions_rebuild(action):
    assert events.relevant("pull_request_target", pr("[adc_comp] first netlist", action), BLOCKS) == (True, "block-pr")


@pytest.mark.parametrize("title", ["docs: tidy", "[adc_comp_x] no", "[unknown] x", "x [adc_comp] late", "", "adc_comp"])
def test_other_prs_do_not_rebuild(title):
    assert events.relevant("pull_request_target", pr(title), BLOCKS) == (False, "not-a-block-pr")


def test_pr_actions_that_cannot_matter_are_skipped():
    assert events.relevant("pull_request_target", pr("[adc_comp] x", "labeled"), BLOCKS)[0] is False


# ------------------------------------------------------------------ issues and comments (notices)
@pytest.mark.parametrize("action", sorted(events.ISSUE_ACTIONS))
def test_notice_actions_rebuild(action):
    assert events.relevant("issues", issue("[adc_bootstrap] spec 0.5", action), BLOCKS) == (True, "block-notice")


def test_other_issues_do_not_rebuild():
    assert events.relevant("issues", issue("question about the flow"), BLOCKS) == (False, "not-a-block-notice")


def test_retitling_a_notice_out_of_or_into_scope_rebuilds():
    out_of = issue("renamed", "edited", changes={"title": {"from": "[adc_comp] notice"}})
    into = issue("[adc_comp] notice", "edited", changes={"title": {"from": "notice"}})
    assert events.relevant("issues", out_of, BLOCKS)[0] and events.relevant("issues", into, BLOCKS)[0]
    assert events.relevant("issues", issue("x", "edited", changes={"title": {"from": "y"}}), BLOCKS)[0] is False


def test_comment_on_a_block_notice_rebuilds_comment_elsewhere_does_not():
    assert events.relevant("issue_comment", issue("[adc_comp] notice", "created"), BLOCKS) == (True, "block-notice-comment")
    assert events.relevant("issue_comment", issue("unrelated", "created"), BLOCKS) == (False, "not-a-block-notice")
    on_pr = issue("[adc_comp] a PR with a block title", "created")
    on_pr["issue"]["pull_request"] = {"url": "x"}
    assert events.relevant("issue_comment", on_pr, BLOCKS) == (False, "comment-on-pr")
    assert events.relevant("issue_comment", issue("[adc_comp] notice", "edited"), BLOCKS)[0] is False


# ------------------------------------------------------------------ workflow_run (ci)
def run_payload(event="pull_request", sha="a" * 40):
    return {"action": "completed", "workflow_run": {"event": event, "head_sha": sha}}


def api(prs):
    def get(path):
        base, _, q = path.partition("?")
        assert base == "/pulls"
        page = int(dict(x.split("=") for x in q.split("&"))["page"])
        return prs[(page - 1) * live.PER_PAGE:page * live.PER_PAGE]
    return get


def api_pr(title, sha):
    return {"title": title, "head": {"sha": sha}}


def test_ci_of_an_open_block_pr_head_rebuilds():
    get = api([api_pr("docs", "b" * 40), api_pr("[adc_comp] x", "a" * 40)])
    assert events.relevant("workflow_run", run_payload(), BLOCKS, get) == (True, "ci-of-block-pr")


def test_ci_of_other_heads_does_not_rebuild():
    get = api([api_pr("docs", "a" * 40), api_pr("[adc_comp] x", "c" * 40)])
    assert events.relevant("workflow_run", run_payload(), BLOCKS, get) == (False, "ci-not-of-a-block-pr")


def test_ci_of_a_push_is_skipped_the_pr_run_reports_the_same_head():
    assert events.relevant("workflow_run", run_payload(event="push"), BLOCKS, api([])) == (False, "ci-not-on-pr")


def test_ci_lookup_failure_rebuilds_rather_than_misses_a_preview():
    def boom(path):
        raise live.LiveError("GitHub API answered 403")
    assert events.relevant("workflow_run", run_payload(), BLOCKS, boom) == (True, "ci-unchecked")
    assert events.relevant("workflow_run", run_payload(), BLOCKS, None) == (True, "ci-unchecked")


def test_ci_lookup_pages_through_all_open_prs():
    prs = [api_pr("docs", "d" * 40)] * live.PER_PAGE + [api_pr("[adc_top] late page", "a" * 40)]
    assert events.relevant("workflow_run", run_payload(), BLOCKS, api(prs)) == (True, "ci-of-block-pr")


def test_unknown_events_rebuild():
    assert events.relevant("something_new", {}, BLOCKS) == (True, "unknown-event")


# ------------------------------------------------------------------ the entry point
def test_block_names_come_from_the_spec_files():
    names = events.block_names(ROOT)
    assert "adc_comp" in names and "adc_top" in names and all("." not in n for n in names)


def test_main_prints_a_fixed_reason_only_and_writes_the_output(tmp_path):
    title = "[adc_comp] ::set-output name=x::y"                      # attacker-controlled text must never reach the log
    ev = tmp_path / "event.json"
    ev.write_text(json.dumps(pr(title)))
    out = tmp_path / "out.txt"
    env = {"GITHUB_EVENT_NAME": "pull_request_target", "GITHUB_EVENT_PATH": str(ev), "GITHUB_OUTPUT": str(out), "PATH": ""}
    p = subprocess.run([sys.executable, str(ROOT / "site" / "events.py")], env=env, capture_output=True, text=True)
    assert p.returncode == 0
    assert "::" not in p.stdout and "set-output" not in p.stdout and title not in p.stdout
    assert out.read_text() == "relevant=true\nreason=block-pr\n"


# ------------------------------------------------------------------ the workflow file
@pytest.fixture(scope="module")
def workflow():
    return yaml.safe_load((ROOT / ".github" / "workflows" / "site.yml").read_text(encoding="utf-8"))


def test_workflow_triggers_the_requested_events(workflow):
    on = workflow[True] if True in workflow else workflow["on"]          # PyYAML reads the key `on` as True
    assert {"push", "pull_request", "pull_request_target", "issues", "issue_comment", "workflow_run", "workflow_dispatch",
            "schedule"} <= set(on)
    assert set(on["pull_request_target"]["types"]) == events.PR_ACTIONS
    assert set(on["issues"]["types"]) == events.ISSUE_ACTIONS and on["issue_comment"]["types"] == ["created"]
    assert on["workflow_run"] == {"workflows": ["ci"], "types": ["completed"]}
    assert on["schedule"][0]["cron"].startswith("17 ")


def test_workflow_permissions_are_least_privilege(workflow):
    jobs = workflow["jobs"]
    assert workflow["permissions"] == {"contents": "read"}
    for name in ("gate", "build"):
        assert not any(v == "write" for v in jobs[name]["permissions"].values()), name
    assert jobs["deploy"]["permissions"] == {"pages": "write", "id-token": "write"}


def test_workflow_never_checks_out_a_pr_outside_the_pull_request_event(workflow):
    text = (ROOT / ".github" / "workflows" / "site.yml").read_text(encoding="utf-8")
    assert text.count("head.sha") == 2                    # the checkout of the pull_request event, and its ADC_SITE_SHA
    for name, job in workflow["jobs"].items():
        for step in job["steps"]:
            ref = str((step.get("with") or {}).get("ref", ""))
            if "head.sha" in ref:
                assert "github.event_name == 'pull_request' &&" in ref, name
    gate_steps = workflow["jobs"]["gate"]["steps"]
    (checkout,) = [s for s in gate_steps if str(s.get("uses", "")).startswith("actions/checkout")]
    assert "pull_request" not in checkout["with"]["ref"] and "default_branch" in checkout["with"]["ref"]
    assert checkout["with"]["persist-credentials"] is False


def test_gate_does_not_depend_on_main_for_pull_request_runs(workflow):
    """A PR may add or change site/events.py; its own build must not wait for (or fail on) main's copy of it."""
    gate = workflow["jobs"]["gate"]
    steps = gate["steps"]
    short = [s for s in steps if s.get("if") == "github.event_name == 'pull_request'"]
    assert len(short) == 1 and "relevant=true" in short[0]["run"] and short[0]["id"] == "pr"
    for s in steps:
        if s is not short[0]:                              # checkout of main and the script: privileged events only
            assert s.get("if") == "github.event_name != 'pull_request'", s
    assert "steps.pr.outputs.relevant" in gate["outputs"]["relevant"]


def test_build_checkout_keeps_no_token_except_for_pull_request(workflow):
    (checkout,) = [s for s in workflow["jobs"]["build"]["steps"] if str(s.get("uses", "")).startswith("actions/checkout")]
    assert checkout["with"]["persist-credentials"] == "${{ github.event_name == 'pull_request' }}"


def test_workflow_puts_no_event_text_into_shell_commands(workflow):
    for name, job in workflow["jobs"].items():
        for step in job["steps"]:
            assert "github.event" not in str(step.get("run", "")), (name, step.get("name"))


def test_workflow_concurrency_coalesces_builds_and_never_cancels_a_deploy(workflow):
    jobs = workflow["jobs"]
    assert jobs["build"]["concurrency"]["cancel-in-progress"] is True
    assert jobs["deploy"]["concurrency"] == {"group": "site-deploy", "cancel-in-progress": False}
    assert jobs["build"]["needs"] == "gate" and "relevant" in jobs["build"]["if"]
    assert jobs["deploy"]["needs"] == "build" and "pull_request'" in jobs["deploy"]["if"]
