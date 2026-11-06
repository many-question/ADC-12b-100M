"""remote.launch and the runner: each job has its own time limit (the test's `timeout:`), a job that
runs past it fails alone and is named as a timeout while the others are measured, the batch has a
derived backstop that leaves nothing running on the server, and a capped compile step builds the
shared Verilog-A library before all jobs start together. (How the detached batch is waited for and
collected: test_detached_runs.py.)"""

import subprocess

import pytest

from adcflow import remote, runner
from adcflow.specs import find_test

CFG = {"spectre": "spectre", "env_setup": ["source env"], "host": "h", "remote_root": "/r"}


def _run(monkeypatch, rc: int, job_timeout: float = 3600, jobs=("a", "b", "c"), soa_jobs=None):
    sent = {}

    def fake_ssh(script, timeout=None, stdin_bytes=None, check=True):
        sent.update(script=script, timeout=timeout, check=check)
        if check and rc:
            raise remote.RemoteError(f"remote script failed ({rc}): err")
        return subprocess.CompletedProcess(["ssh"], rc, b"", b"err")

    monkeypatch.setattr(remote, "cfg", lambda: CFG)
    monkeypatch.setattr(remote, "ssh_script", fake_ssh)
    sent["limit"] = remote.launch("/r/run1", list(jobs), ["+aps"], 2, job_timeout, soa_jobs=soa_jobs)
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
    assert s["limit"] == limit
    launch = _heredoc(s["script"], "$R/launch.sh", "EOL")
    assert f"timeout -k {remote.KILL_AFTER_S} {limit} bash $R/batch.sh $R" in launch
    assert s["timeout"] < 3600                                          # the ssh does not wait for the batch


def test_backstop_scales_with_corners_and_jobs():
    # all 45 corners of tb_sarlogic_rand at the default 6 parallel jobs: 8 waves of its job limit
    assert remote.batch_limit(45, 6, 43200, True) >= 8 * 43200
    assert remote.batch_limit(1, 6, 3600, False) == 3600 + remote.KILL_AFTER_S + remote.SERVER_MARGIN_S


def test_the_backstop_leaves_nothing_running(monkeypatch):
    launch = _heredoc(_run(monkeypatch, 0)["script"], "$R/launch.sh", "EOL")
    after = launch.split("bash $R/batch.sh $R\n", 1)[1]
    assert "[ $rc -eq 124 ] || [ $rc -eq 137 ]" in after and "kill -9" in after and '"$R"/*' in after
    # the done marker (rc, start, end) comes last, after the kill
    assert after.index("kill -9") < after.index(f'"$rc $start $(date +%s)" > $R/{remote.MARK_DONE}.tmp')
    assert after.rstrip().endswith(f"mv $R/{remote.MARK_DONE}.tmp $R/{remote.MARK_DONE}")


def test_the_batch_runs_detached_from_the_ssh_session(monkeypatch):
    script = _run(monkeypatch, 0)["script"]
    after = script.split("\nEOL\n", 1)[1]
    assert f"rm -f $R/{remote.MARK_DONE} $R/{remote.MARK_FETCHED}" in after
    assert f"setsid nohup bash $R/launch.sh $R > $R/{remote.BATCH_LOG} 2>&1 < /dev/null &" in after
    assert f"[ -s $R/{remote.PID_FILE} ] && exit 0" in after              # returns once launch.sh runs
    assert f"echo $$ > $R/{remote.PID_FILE}" in _heredoc(script, "$R/launch.sh", "EOL")


def test_the_soa_step_runs_on_the_server_after_a_normal_batch(monkeypatch):
    s = _run(monkeypatch, 0, soa_jobs=["a", "c"])
    assert "cat > $R/soa_jobs.list <<'EOF'\na\nc\nEOF" in s["script"]
    launch = _heredoc(s["script"], "$R/launch.sh", "EOL")
    soa = launch.split("elif [ $rc -eq 0 ]; then", 1)[1].split("\nfi\n", 1)[0]
    assert f"timeout -k {remote.KILL_AFTER_S} {remote.SOA_TIMEOUT_S} xargs -P 2" in soa
    assert "[ -f jobs/J/soa_rows.json ] || python3 soa_core.py jobs/J" in soa
    assert launch.index("kill -9") < launch.index("elif [ $rc -eq 0 ]") < launch.index(remote.MARK_DONE)
    assert "soa_core" not in _run(monkeypatch, 0)["script"]


def test_a_failed_start_is_a_plain_error(monkeypatch):
    with pytest.raises(remote.RemoteError) as e:
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
        for i, staged in enumerate(sorted((run_dir / "stage" / "jobs").iterdir())):
            jd = run_dir / "jobs" / staged.name                        # what the real fetch brings back
            jd.mkdir(parents=True, exist_ok=True)
            (jd / "rc.txt").write_text("124 3660\n" if i == 1 else "0 10\n")
            (jd / "spectre.log").write_text("ok\n")
        return []

    monkeypatch.setattr(runner, "RUNS", tmp_path)
    monkeypatch.setattr("adcflow.spectrum.require_toolbox", lambda: None)
    monkeypatch.setattr(remote, "cfg", lambda: {**CFG, "modes": {"aps": ["+aps"]}, "fetch": [], "fetch_max_mb": 50})
    monkeypatch.setattr(remote, "remote_root", lambda: "/r")
    monkeypatch.setattr(remote, "upload_tree", lambda *a: None)
    monkeypatch.setattr(remote, "launch", lambda *a, **k: calls.setdefault("launch", a) and 0)
    monkeypatch.setattr(remote, "status", lambda rroot: remote.parse_status("exists 1\nlive 0\nended 3 0\ndone 0 1 2"))
    monkeypatch.setattr(remote, "fetch", fake_fetch)
    monkeypatch.setattr(remote, "mark_fetched", lambda *a: None)
    monkeypatch.setattr(remote, "remove", lambda *a: None)
    monkeypatch.setattr(runner, "measure", lambda test, jd, ctx: {"ok": 1})
    rows = runner.run_test("tb_sarlogic_func", None, "tt_nom_27,ff_high_125,ss_low_m40", {}, {}, "aps", 3,
                           False, False, timeout=3600)
    assert calls["launch"][4] == 3600                                   # the job limit reaches the batch
    bad = [r for r in rows if "error" in r["metrics"]]
    assert len(rows) == 3 and len(bad) == 1
    assert bad[0]["metrics"]["error"].startswith("timeout:") and bad[0]["rc"] == "124"
    assert all(r["metrics"] == {"ok": 1} for r in rows if r is not bad[0])


@pytest.mark.parametrize("test_id,at_least_h", [("tb_sarlogic_rand", 9), ("tb_top_sine", 20),
                                                 ("tb_top_sine_lf", 20), ("tb_top_duty", 20)])
def test_slow_tests_have_a_job_timeout(test_id, at_least_h):
    _, t = find_test(test_id)
    assert t["timeout"] >= at_least_h * 3600
