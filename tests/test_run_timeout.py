"""The batch time limit of remote.run_jobs: the server ends the batch (whole process group) before the
local ssh timeout, and a batch ended that way is a reported failure, never a silent one."""

import subprocess

import pytest

from adcflow import remote
from adcflow.specs import find_test

CFG = {"spectre": "spectre", "env_setup": ["source env"], "host": "h", "remote_root": "/r"}


def _run(monkeypatch, rc: int, timeout: float = 4 * 3600, jobs=("a", "b", "c")):
    sent = {}

    def fake_ssh(script, timeout=None, stdin_bytes=None, check=True):
        sent.update(script=script, timeout=timeout, check=check)
        return subprocess.CompletedProcess(["ssh"], rc, b"", b"err")

    monkeypatch.setattr(remote, "cfg", lambda: CFG)
    monkeypatch.setattr(remote, "ssh_script", fake_ssh)
    remote.run_jobs("/r/run1", list(jobs), ["+aps"], 2, timeout=timeout)
    return sent


def test_the_server_limit_ends_the_batch_before_the_ssh_timeout(monkeypatch):
    s = _run(monkeypatch, 0)
    limit = remote.server_limit(4 * 3600)
    assert limit + remote.KILL_AFTER_S < s["timeout"] == 4 * 3600
    assert f"timeout -k {remote.KILL_AFTER_S} {limit} bash $R/batch.sh $R" in s["script"]


def test_every_spectre_job_runs_inside_the_limited_batch(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    batch = script.split("<<'EOB'\n", 1)[1].split("\nEOB\n", 1)[0]
    assert "$R/run_one.sh $R a" in batch                       # the warm-up job
    assert "xargs -P 2" in batch and "run_one.sh" in batch     # the rest
    outside = script.replace(batch, "")
    assert "xargs" not in outside and "run_one.sh $R a" not in outside


@pytest.mark.parametrize("rc", [124, 137])
def test_a_batch_ended_by_the_limit_raises_run_timeout(monkeypatch, rc):
    with pytest.raises(remote.RunTimeout, match="timeout:"):
        _run(monkeypatch, rc)


def test_other_failures_stay_plain_errors(monkeypatch):
    with pytest.raises(RuntimeError) as e:
        _run(monkeypatch, 1)
    assert not isinstance(e.value, remote.RunTimeout)


def test_server_limit_stays_positive_for_short_timeouts():
    assert remote.server_limit(14400) == 14400 - remote.SERVER_MARGIN_S
    assert 0 < remote.server_limit(120) < 120


@pytest.mark.parametrize("test_id,at_least_h", [("tb_sarlogic_rand", 12), ("tb_sarlogic_func_slow", 6),
                                                 ("tb_top_sine", 24), ("tb_top_sine_lf", 24), ("tb_top_duty", 24)])
def test_slow_tests_have_a_batch_timeout(test_id, at_least_h):
    _, t = find_test(test_id)
    assert t["timeout"] >= at_least_h * 3600
