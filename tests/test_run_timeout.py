"""remote.run_jobs and the runner: each job has its own time limit (the test's `timeout:`), a job that
runs past it fails alone and is named as a timeout while the others are measured, the batch has a
derived backstop that leaves nothing running on the server, and a capped compile step builds the
shared Verilog-A library before all jobs start together."""

import shutil
import subprocess

import pytest

from adcflow import remote, runner
from adcflow.specs import find_test

CFG = {"spectre": "spectre", "env_setup": ["source env"], "host": "h", "remote_root": "/r"}


def _run(monkeypatch, rc: int, job_timeout: float = 3600, jobs=("a", "b", "c"), stdout: bytes = b""):
    sent = {}

    def fake_ssh(script, timeout=None, stdin_bytes=None, check=True):
        sent.update(script=script, timeout=timeout, check=check)
        return subprocess.CompletedProcess(["ssh"], rc, stdout, b"err")

    monkeypatch.setattr(remote, "cfg", lambda: CFG)
    monkeypatch.setattr(remote, "ssh_script", fake_ssh)
    remote.run_jobs("/r/run1", list(jobs), ["+aps"], 2, job_timeout)
    return sent


def _heredoc(script: str, name: str, end: str = "EOS") -> str:
    return script.split(f"{name} <<'{end}'\n", 1)[1].split(f"\n{end}\n", 1)[0]


def test_each_job_has_its_own_limit(monkeypatch):
    run_one = _heredoc(_run(monkeypatch, 0, job_timeout=43200)["script"], "$R/run_one.sh")
    assert f'timeout -k {remote.KILL_AFTER_S} 43200 csh -c "' in run_one
    assert run_one.index("rc=$?") < run_one.index("> rc.txt")          # a timed-out job still writes its rc


def test_the_batch_backstop_is_derived_from_the_job_limit(monkeypatch):
    s = _run(monkeypatch, 0, job_timeout=3600)                          # 3 jobs, 2 at a time: 2 waves
    limit = remote.batch_limit(3, 2, 3600, True)
    assert limit == remote.COMPILE_CAP_S + 2 * (3600 + remote.KILL_AFTER_S) + remote.SERVER_MARGIN_S
    assert f"timeout -k {remote.KILL_AFTER_S} {limit} bash $R/batch.sh $R" in s["script"]
    assert s["timeout"] > limit + remote.KILL_AFTER_S                   # the ssh waits for the server


def test_backstop_scales_with_corners_and_jobs():
    # all 45 corners of tb_sarlogic_rand at the default 6 parallel jobs: 8 waves of its job limit
    assert remote.batch_limit(45, 6, 43200, True) >= 8 * 43200
    assert remote.batch_limit(1, 6, 3600, False) == 3600 + remote.KILL_AFTER_S + remote.SERVER_MARGIN_S


def test_the_backstop_leaves_nothing_running(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    after = script.split("bash $R/batch.sh $R\n", 1)[1]
    assert "[ $rc -eq 124 ] || [ $rc -eq 137 ]" in after and "kill -9" in after and '"$R"/*' in after
    assert after.rstrip().endswith("exit $rc")


@pytest.mark.parametrize("rc", [124, 137])
def test_a_batch_ended_by_the_backstop_raises_run_timeout(monkeypatch, rc):
    with pytest.raises(remote.RunTimeout, match="backstop"):
        _run(monkeypatch, rc)


def test_other_failures_stay_plain_errors(monkeypatch):
    with pytest.raises(RuntimeError) as e:
        _run(monkeypatch, 1)
    assert not isinstance(e.value, remote.RunTimeout)


def test_every_spectre_run_is_inside_the_batch(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    batch = _heredoc(script, "$R/batch.sh", "EOB")
    assert "$R/compile_va.sh $R a" in batch                           # the compile step
    assert "cat $R/jobs.list | xargs -P 2" in batch                    # every job, the first included
    outside = script.replace(batch, "")
    assert "xargs" not in outside and "compile_va.sh $R a" not in outside


def test_jobs_only_read_the_shared_library(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    run_one, compile_va = _heredoc(script, "$R/run_one.sh"), _heredoc(script, "$R/compile_va.sh")
    assert "-ahdlshipdbdir=$R/ahdl_lib" in run_one
    assert "shipdbmode" not in run_one and "-ahdllibdir" not in run_one   # read_only, the default
    assert "-ahdlshipdbmode=create_or_update" in compile_va


def test_the_compile_step_is_capped_stops_its_spectre_and_cleans_up(monkeypatch):
    compile_va = _heredoc(_run(monkeypatch, 0)["script"], "$R/compile_va.sh")
    assert f"-ge {remote.COMPILE_CAP_S} ]" in compile_va and "compile step stopped at its cap" in compile_va
    kill = compile_va.index("kill -9")
    assert compile_va.index('cd "$R"') < kill                          # out of $D before killing what runs in it
    assert "Time for Elaboration" in compile_va and 'rm -rf "$D"' in compile_va
    assert compile_va.rstrip().endswith("exit 0")                      # never fails the batch by itself


def test_server_notes_reach_the_run_output(monkeypatch, capsys):
    _run(monkeypatch, 0, stdout=b"noise\nadcflow: compile step stopped at its cap of 900 s\n")
    out = capsys.readouterr().out
    assert "[adcflow] compile step stopped at its cap of 900 s" in out and "noise" not in out


@pytest.mark.parametrize("jobs,compile_step", [(("a",), False), (("a", "b"), True)])
def test_a_single_job_needs_no_compile_step(monkeypatch, jobs, compile_step):
    batch = _heredoc(_run(monkeypatch, 0, jobs=jobs)["script"], "$R/batch.sh", "EOB")
    assert ("compile_va.sh $R" in batch) == compile_step


def test_a_timed_out_job_is_named_as_such():
    for rc in remote.TIMEOUT_RCS:
        assert runner.job_error(rc, [], 3600).startswith("timeout: the job ran past its `timeout:` of 3600 s")
    assert runner.job_error("1", ["ERROR (SPECTRE-1): x"], 3600) == "ERROR (SPECTRE-1): x"
    assert runner.job_error("1", [], 3600) == "spectre rc=1"


def test_runner_fails_only_the_timed_out_job(monkeypatch, tmp_path):
    """Three corners, the second ended by its time limit: it alone is an error, the others are measured."""
    calls = {}

    def fake_fetch(rroot, patterns, run_dir, max_mb):
        calls["run_dir"] = run_dir
        for i, staged in enumerate(sorted((run_dir / "stage" / "jobs").iterdir())):
            jd = run_dir / "jobs" / staged.name                        # what the real fetch brings back
            jd.mkdir(parents=True, exist_ok=True)
            (jd / "rc.txt").write_text("124 3660\n" if i == 1 else "0 10\n")
            (jd / "spectre.log").write_text("ok\n")
        return []

    monkeypatch.setattr(runner, "require_toolbox", lambda: None, raising=False)
    monkeypatch.setattr("adcflow.spectrum.require_toolbox", lambda: None)
    monkeypatch.setattr(remote, "cfg", lambda: {**CFG, "modes": {"aps": ["+aps"]}, "fetch": [], "fetch_max_mb": 50})
    monkeypatch.setattr(remote, "remote_root", lambda: "/r")
    monkeypatch.setattr(remote, "upload_tree", lambda *a: None)
    monkeypatch.setattr(remote, "run_jobs", lambda *a, **k: calls.setdefault("run_jobs", a))
    monkeypatch.setattr(remote, "fetch", fake_fetch)
    monkeypatch.setattr(remote, "remove", lambda *a: None)
    monkeypatch.setattr(runner, "measure", lambda test, jd, ctx: {"ok": 1})
    try:
        rows = runner.run_test("tb_sarlogic_func", None, "tt_nom_27,ff_high_125,ss_low_m40", {}, {}, "aps", 3,
                               False, False, timeout=3600)
    finally:
        if "run_dir" in calls:
            shutil.rmtree(calls["run_dir"], ignore_errors=True)
    assert calls["run_jobs"][4] == 3600                                 # the job limit reaches run_jobs
    bad = [r for r in rows if "error" in r["metrics"]]
    assert len(rows) == 3 and len(bad) == 1
    assert bad[0]["metrics"]["error"].startswith("timeout:") and bad[0]["rc"] == "124"
    assert all(r["metrics"] == {"ok": 1} for r in rows if r is not bad[0])


@pytest.mark.parametrize("test_id,at_least_h", [("tb_sarlogic_rand", 9), ("tb_top_sine", 20),
                                                 ("tb_top_sine_lf", 20), ("tb_top_duty", 20)])
def test_slow_tests_have_a_job_timeout(test_id, at_least_h):
    _, t = find_test(test_id)
    assert t["timeout"] >= at_least_h * 3600
