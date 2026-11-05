"""remote.run_jobs: the batch time limit (the server ends the batch, whole process group, before the
local ssh timeout, and a batch ended that way is a reported failure, never a silent one) and the
compile step that builds the shared Verilog-A library before all jobs start together."""

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


def _batch(script: str) -> str:
    return script.split("<<'EOB'\n", 1)[1].split("\nEOB\n", 1)[0]


def test_every_spectre_run_is_inside_the_limited_batch(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    batch = _batch(script)
    assert "$R/compile_va.sh $R a" in batch                     # the compile step
    assert "cat $R/jobs.list | xargs -P 2" in batch             # every job, the first included
    outside = script.replace(batch, "")
    assert "xargs" not in outside and "compile_va.sh $R a" not in outside


def test_jobs_only_read_the_shared_library(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    run_one = script.split("run_one.sh <<'EOS'\n", 1)[1].split("\nEOS\n", 1)[0]
    compile_va = script.split("compile_va.sh <<'EOS'\n", 1)[1].split("\nEOS\n", 1)[0]
    assert "-ahdlshipdbdir=$R/ahdl_lib" in run_one
    assert "shipdbmode" not in run_one and "-ahdllibdir" not in run_one      # read_only, the default
    assert "-ahdlshipdbmode=create_or_update" in compile_va


def test_the_compile_step_stops_its_spectre_and_cleans_up(monkeypatch):
    compile_va = _run(monkeypatch, 0)["script"].split("compile_va.sh <<'EOS'\n", 1)[1].split("\nEOS\n", 1)[0]
    kill = compile_va.index("kill -9")
    assert compile_va.index('cd "$R"') < kill                  # out of $D before killing what runs in it
    assert "Time for Elaboration" in compile_va and 'rm -rf "$D"' in compile_va
    assert compile_va.rstrip().endswith("exit 0")              # never fails the batch by itself


@pytest.mark.parametrize("jobs,compile_step", [(("a",), False), (("a", "b"), True)])
def test_a_single_job_needs_no_compile_step(monkeypatch, jobs, compile_step):
    assert ("compile_va.sh $R" in _batch(_run(monkeypatch, 0, jobs=jobs)["script"])) == compile_step


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
