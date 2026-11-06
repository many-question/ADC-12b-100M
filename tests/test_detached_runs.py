"""A run's batch runs on the server by itself (runner.submit, remote.launch). The local side waits by
asking the server now and then (runner.wait) or comes back later (`adcflow collect`); once the batch
ended it fetches, measures and records, and deletes the server directory last. A lost connection
never aborts or deletes anything, and a run of a launcher of before the manifest is adopted from its
own arguments (runner.adopt). The server is a stand-in (FakeServer); the scripts that remote sends
are checked as text."""

import subprocess

import pytest

from adcflow import remote, runner, verify
from adcflow.cli import main
from adcflow.specs import find_test

TEST, CORNERS = "tb_sarlogic_func", "tt_nom_27,ff_high_125"
JOBS = ["ff_high_125", "tt_nom_27"]
CFG = {"spectre": "spectre", "env_setup": ["source env"], "host": "h", "remote_root": "/r",
       "modes": {"aps": ["+aps"]}, "fetch": ["*.txt"], "fetch_max_mb": 50}


class FakeServer:
    """remote's functions over run directories kept in memory (rroot -> its state)."""

    def __init__(self):
        self.dirs: dict[str, dict] = {}
        self.calls: list[tuple] = []           # (what, rroot) in order; the runner's record adds ("record", job)
        self.down = 0                          # this many next calls fail as over a lost connection
        self.on_status = None                  # called at each status (a batch can end while one waits)

    def _net(self, what, rroot):
        self.calls.append((what, rroot))
        if self.down:
            self.down -= 1
            raise remote.RemoteError("ssh: connect to host h port 22: Connection timed out")

    def what(self) -> list[str]:
        return [c[0] for c in self.calls]

    def upload_tree(self, local_dir, rroot):
        self._net("upload", rroot)
        self.dirs[rroot] = {"jobs": sorted(p.name for p in (local_dir / "jobs").iterdir()), "rc": {}, "done": None,
                            "live": 0, "fetched": False, "limit": None, "notes": []}

    def launch(self, rroot, jobs, mode_args, parallel, job_timeout=3600, compile_first=True, soa_jobs=None):
        self._net("launch", rroot)
        d = self.dirs[rroot]
        assert d["jobs"] == sorted(jobs)
        d.update(jobs=list(jobs), live=1, limit=job_timeout)
        return remote.batch_limit(len(jobs), parallel, job_timeout, len(jobs) > 1)

    def end(self, rroot, rcs=None, marker=True, batch_rc="0"):
        """The batch ends: an rc.txt for every job (rcs: job -> "<rc> <s>"), nothing runs, the done marker."""
        d = self.dirs[rroot]
        d.update(rc={j: (rcs or {}).get(j, "0 10") for j in d["jobs"]}, live=0,
                 done=f"{batch_rc} 1000 1100" if marker else None)

    def status(self, rroot):
        if self.on_status:
            self.on_status(self)
        self._net("status", rroot)
        d = self.dirs.get(rroot)
        if d is None:
            return remote.parse_status("exists 0\n")
        lines = ["exists 1", f"live {d['live']}", f"ended {len(d['rc'])} {1100 if d['rc'] else 0}", "start 1000"]
        lines += [f"done {d['done']}"] if d["done"] else []
        lines += ["fetched 1"] if d["fetched"] else []
        lines += [f"job {j}" for j in d["jobs"]]
        lines += [f"limit timeout -k 60 {int(d['limit'])} csh"] if d["limit"] else []
        lines += ["parallel xargs -P 2"] + [f"note adcflow: {n}" for n in d["notes"]]
        return remote.parse_status("\n".join(lines) + "\n")

    def fetch(self, rroot, patterns, local_dir, max_mb):
        self._net("fetch", rroot)
        for j, rc in self.dirs[rroot]["rc"].items():
            jd = local_dir / "jobs" / j
            jd.mkdir(parents=True, exist_ok=True)
            (jd / "rc.txt").write_text(rc + "\n")
            (jd / "spectre.log").write_text("ok\n")
        return []

    def mark_fetched(self, rroot):
        self._net("mark_fetched", rroot)
        self.dirs[rroot]["fetched"] = True

    def remove(self, rroot):
        self._net("remove", rroot)
        d = self.dirs[rroot]
        if not d["fetched"] or d["live"]:                  # the guard of remote.remove's script
            raise remote.RemoteBusy(f"{rroot} stays on the server")
        del self.dirs[rroot]

    def soa_reduce(self, rroot, jobs, parallel):
        self._net("soa_reduce", rroot)


@pytest.fixture
def srv(monkeypatch, tmp_path):
    s = FakeServer()
    for name in ("upload_tree", "launch", "status", "fetch", "mark_fetched", "remove", "soa_reduce"):
        monkeypatch.setattr(remote, name, getattr(s, name))
    monkeypatch.setattr(remote, "cfg", lambda: CFG)
    monkeypatch.setattr(remote, "remote_root", lambda: "/r")
    monkeypatch.setattr(runner, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(runner, "POLL_S", (0.0, 0.0))
    monkeypatch.setattr("adcflow.spectrum.require_toolbox", lambda: None)
    monkeypatch.setattr(runner, "result_dir", lambda block, test_id, viewsig: tmp_path / "results")
    monkeypatch.setattr(runner, "measure", lambda test, jd, ctx: {"t_ps": 10.0 + len(ctx["corner"].name)})

    def record(block, test_id, viewsig, job, metrics, meta, figures=None):
        s.calls.append(("record", job.name))
        return tmp_path / "results" / f"{job.name}.json"

    monkeypatch.setattr(runner, "record", record)
    return s


def detach(**kw) -> list:
    return runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 2, detach=True, **kw)


def the_run(srv) -> tuple[str, str]:
    (rroot,) = srv.dirs
    return rroot, rroot.rsplit("/", 1)[1]


# ------------------------------------------------------------------ submit
def test_detach_returns_once_the_batch_runs_and_writes_the_manifest(srv):
    assert detach() == []
    rroot, run_id = the_run(srv)
    assert srv.what() == ["upload", "launch"]                          # nothing waits for the batch
    man = runner.load_manifest(run_id)
    assert man["state"] == "submitted" and not man["adopted"] and man["rroot"] == rroot == f"/r/{run_id}"
    assert sorted(man["jobs"]) == JOBS and man["args"] == runner.run_args(TEST, None, CORNERS, {}, {}, "aps", 2)
    assert man["job_timeout"] == float(find_test(TEST)[1].get("timeout", remote.JOB_TIMEOUT_S))
    assert man["git"] and "git_clean" in man["git_state"] and man["upload_s"] >= 0
    assert (runner.RUNS / run_id / "stage" / "jobs" / "tt_nom_27" / "deck.scs").is_file()


def test_a_failed_start_says_how_to_look_at_it(srv, capsys):
    srv.down = 1
    with pytest.raises(remote.RemoteError):
        detach()
    assert "`python -m adcflow collect " in capsys.readouterr().out
    (p,) = runner.RUNS.glob("*/manifest.json")
    assert runner.load_manifest(p.parent.name)["state"] == "submitted"


# ------------------------------------------------------------------ collect
def test_collect_leaves_a_running_batch_alone(srv, capsys):
    detach()
    rroot, run_id = the_run(srv)
    res = runner.collect(run_id)
    assert res["state"] == "running" and res["ended"] == 0 and res["code"] == 0
    assert srv.what() == ["upload", "launch", "status"]                # nothing fetched, nothing deleted
    assert runner.load_manifest(run_id)["state"] == "submitted"
    assert f"{run_id}: running, 0 of 2 job(s) ended" in capsys.readouterr().out


def test_collect_measures_records_then_deletes_and_is_idempotent(srv, capsys):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot)
    srv.dirs[rroot]["notes"] = ["compile step 38 s"]
    res = runner.collect(run_id)
    assert res["state"] == "collected" and res["code"] == 0
    assert srv.what()[2:] == ["status", "fetch", "mark_fetched", "record", "record", "remove"]
    assert sorted(r["job"] for r in res["summary"]) == JOBS
    man = runner.load_manifest(run_id)
    assert man["state"] == "collected" and man["removed"] and rroot not in srv.dirs
    meta = res["summary"][0]["meta"]
    assert meta["git"] == man["git"] and meta["wall_s"] == round(100 + man["upload_s"], 1)  # the batch on the server
    assert "[adcflow] compile step 38 s" in capsys.readouterr().out
    n = len(srv.calls)
    assert runner.collect(run_id)["state"] == "collected" and len(srv.calls) == n   # nothing twice
    assert runner.pending() == []


def test_the_default_waits_and_rides_out_a_lost_connection(srv, capsys):
    """sim without --detach: the batch ends while the launcher waits; two looks in between fail (ssh rc 255)."""
    looks = []

    def tick(s):
        looks.append(1)
        if len(looks) == 2:
            s.down = 2
        if len(looks) == 5:
            s.end(next(iter(s.dirs)))

    srv.on_status = tick
    rows = runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 2)
    assert sorted(r["job"] for r in rows) == JOBS and all("error" not in r["metrics"] for r in rows)
    assert capsys.readouterr().out.count("no answer from the server") == 2
    w = srv.what()
    assert w.count("status") == 5 and "remove" not in w[:w.index("fetch")] and w[-1] == "remove"


def test_a_failed_fetch_changes_nothing_and_collect_tries_again(srv, monkeypatch):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot)

    def lost(*a):
        raise remote.RemoteError("scp of results failed: lost connection")

    monkeypatch.setattr(remote, "fetch", lost)
    with pytest.raises(remote.RemoteError):
        runner.collect(run_id)
    assert runner.load_manifest(run_id)["state"] == "submitted" and rroot in srv.dirs
    assert "remove" not in srv.what() and "record" not in srv.what()
    monkeypatch.setattr(remote, "fetch", srv.fetch)
    assert runner.collect(run_id)["state"] == "collected" and rroot not in srv.dirs


def test_a_directory_that_cannot_be_deleted_yet_is_tried_again(srv, monkeypatch, capsys):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot)
    monkeypatch.setattr(remote, "remove", lambda r: (_ for _ in ()).throw(remote.RemoteBusy(f"{r}: 1 process")))
    assert runner.collect(run_id)["state"] == "collected" and rroot in srv.dirs
    assert "not deleted on the server" in capsys.readouterr().out
    assert runner.pending() == [run_id] and not runner.load_manifest(run_id).get("removed")
    monkeypatch.setattr(remote, "remove", srv.remove)
    n = srv.what().count("record")
    assert runner.collect(run_id)["state"] == "collected" and rroot not in srv.dirs
    assert srv.what().count("record") == n and runner.pending() == []


def test_keep_leaves_the_directory(srv):
    detach(keep=True)
    rroot, run_id = the_run(srv)
    srv.end(rroot)
    assert runner.collect(run_id)["state"] == "collected" and rroot in srv.dirs and "remove" not in srv.what()
    assert runner.pending() == []


@pytest.mark.parametrize("rc", remote.TIMEOUT_RCS)
def test_a_batch_ended_by_its_backstop_records_nothing(srv, rc):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot, batch_rc=rc)
    with pytest.raises(remote.RunTimeout, match="backstop"):
        runner.collect(run_id)
    w = srv.what()
    assert "record" not in w and w.index("fetch") < w.index("mark_fetched") < w.index("remove")
    assert runner.load_manifest(run_id)["state"] == "failed" and rroot not in srv.dirs


def test_a_batch_that_failed_otherwise_is_a_plain_error(srv):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot, batch_rc="123")
    with pytest.raises(RuntimeError, match="rc 123") as e:
        runner.collect(run_id)
    assert not isinstance(e.value, remote.RunTimeout) and "record" not in srv.what()


def test_a_timed_out_job_fails_alone_with_the_runs_job_limit(srv):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot, rcs={"tt_nom_27": "124 14460"})
    rows = {r["job"]: r for r in runner.collect(run_id)["summary"]}
    limit = runner.load_manifest(run_id)["job_timeout"]
    assert rows["tt_nom_27"]["metrics"]["error"].startswith(f"timeout: the job ran past its `timeout:` of {limit:.0f} s")
    assert "error" not in rows["ff_high_125"]["metrics"]


def test_a_stopped_batch_is_not_recorded_until_discarded(srv):
    detach()
    rroot, run_id = the_run(srv)
    d = srv.dirs[rroot]
    d.update(live=0, rc={"tt_nom_27": "0 10"})                          # one job ended, nothing runs, no marker
    res = runner.collect(run_id)
    assert res["state"] == "dead" and res["code"] == 1 and "fetch" not in srv.what()
    assert runner.collect(run_id, discard=True)["state"] == "discarded"
    assert "record" not in srv.what() and rroot not in srv.dirs
    assert (runner.RUNS / run_id / "jobs" / "tt_nom_27" / "rc.txt").is_file()   # fetched for a look
    assert runner.load_manifest(run_id)["state"] == "discarded" and runner.pending() == []


def test_discard_leaves_a_running_batch_alone(srv):
    detach()
    rroot, run_id = the_run(srv)
    assert runner.collect(run_id, discard=True)["state"] == "running" and rroot in srv.dirs
    assert runner.load_manifest(run_id)["state"] == "submitted"


def test_a_run_gone_from_the_server(srv):
    detach()
    rroot, run_id = the_run(srv)
    del srv.dirs[rroot]
    assert runner.collect(run_id)["state"] == "missing"
    assert runner.collect(run_id, discard=True)["state"] == "discarded" and runner.pending() == []


def test_collect_refuses_a_run_this_tree_no_longer_builds(srv):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot)
    st = runner.RUNS / run_id / "stage"
    deck = st / "jobs" / "tt_nom_27" / "deck.scs"
    deck.write_bytes(deck.read_bytes() + b"// another deck\n")
    with pytest.raises(runner.RunRefused, match="jobs/tt_nom_27/deck.scs"):
        runner.collect(run_id)
    tb = find_test(TEST)[1]["netlist"]                                  # a file the circuit depends on
    (st / tb).write_bytes((st / tb).read_bytes() + b"parameters changed_since=1\n")
    with pytest.raises(runner.RunRefused, match=tb):
        runner.collect(run_id)
    assert "fetch" not in srv.what() and runner.load_manifest(run_id)["state"] == "submitted"


def test_one_collect_at_a_time(srv):
    detach()
    _, run_id = the_run(srv)
    with runner._lock(runner.RUNS / run_id):
        with pytest.raises(runner.RunBusy):
            runner.collect(run_id)


def test_a_verify_run_is_compared_by_whoever_collects_it(srv, monkeypatch):
    got = {}

    def finish(*a):
        got["finish"] = a
        return 1

    monkeypatch.setattr(verify, "load_docs", lambda paths: [{"_path": p} for p in paths])
    monkeypatch.setattr(verify, "finish", finish)
    a = runner.run_args(TEST, None, CORNERS, {}, {}, "aps", 2, do_record=False)
    run_id = runner.submit(a, {"candidate": "alice", "docs": ["results/b/t/xtor-alice/tt_nom_27.json"]})
    srv.end(f"/r/{run_id}")
    res = runner.collect(run_id)
    test_id, block, name, docs, summary, took = got["finish"]
    assert (test_id, block, name) == (TEST, "adc_sarlogic", "alice")
    assert docs == [{"_path": "results/b/t/xtor-alice/tt_nom_27.json"}] and len(summary) == 2
    assert res["code"] == 1 and runner.load_manifest(run_id)["code"] == 1 and "record" not in srv.what()
    assert took == round(100 + runner.load_manifest(run_id)["upload_s"], 1)


# ------------------------------------------------------------------ adopt
def old_launcher_run(srv, **kw) -> tuple[str, str]:
    """A run as a launcher of before the manifest leaves it: staged, running on the server, no manifest."""
    detach(**kw)
    rroot, run_id = the_run(srv)
    runner.manifest_path(run_id).unlink()
    srv.dirs[rroot]["limit"] = 86400                                    # the job limit of its own run_one.sh
    return rroot, run_id


def test_adopt_takes_over_a_run_of_an_old_launcher(srv):
    rroot, run_id = old_launcher_run(srv)
    n = len(srv.calls)
    assert runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 2, detach=True, adopt_id=run_id) == []
    assert srv.what()[n:] == ["status"]                                 # nothing uploaded or started again
    man = runner.load_manifest(run_id)
    assert man["adopted"] and man["job_timeout"] == 86400 and man["rroot"] == rroot and man["state"] == "submitted"
    # no done marker: it ended once every job has its rc.txt and nothing runs in it
    srv.dirs[rroot].update(rc={"tt_nom_27": "0 10"}, live=1)
    assert runner.collect(run_id)["state"] == "running"
    srv.end(rroot, rcs={"tt_nom_27": "124 86460"}, marker=False)
    res = runner.collect(run_id)
    assert res["state"] == "collected" and rroot not in srv.dirs and res["code"] == 1
    rows = {r["job"]: r for r in res["summary"]}
    assert rows["tt_nom_27"]["metrics"]["error"].startswith("timeout: the job ran past its `timeout:` of 86400 s")
    assert rows["ff_high_125"]["meta"]["wall_s"] == 100.0                # from its jobs.list to its last rc.txt


def test_adopt_refuses_other_arguments(srv):
    rroot, run_id = old_launcher_run(srv)
    with pytest.raises(runner.RunRefused, match="jobs: staged"):
        runner.run_test(TEST, None, "tt_nom_27", {}, {}, "aps", 2, detach=True, adopt_id=run_id)
    with pytest.raises(runner.RunRefused, match="jobs/tt_nom_27/tb.scs"):
        runner.run_test(TEST, None, CORNERS, {}, {"nconv": "7"}, "aps", 2, detach=True, adopt_id=run_id)
    assert not runner.manifest_path(run_id).exists()


def test_adopt_dry_run_checks_the_rebuild_only(srv, capsys):
    rroot, run_id = old_launcher_run(srv)
    n = len(srv.calls)
    assert runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 2, dry=True, adopt_id=run_id) == []
    assert len(srv.calls) == n and not runner.manifest_path(run_id).exists()
    assert "rebuilt as staged, 2 job(s)" in capsys.readouterr().out


def test_adopt_refuses_a_run_with_a_manifest_or_gone(srv):
    detach()
    rroot, run_id = the_run(srv)
    with pytest.raises(runner.RunRefused, match="manifest already"):
        detach(adopt_id=run_id)
    runner.manifest_path(run_id).unlink()
    del srv.dirs[rroot]
    with pytest.raises(runner.RunRefused, match="not on the server"):
        detach(adopt_id=run_id)


# ------------------------------------------------------------------ the command line
def test_cli_detach_then_collect_all(srv, monkeypatch, capsys):
    monkeypatch.setattr(remote, "default_jobs", lambda: 2)
    assert main(["sim", TEST, "--corners", CORNERS, "--detach"]) == 0
    assert main(["sim", TEST, "--corners", "tt_nom_27", "--detach", "--no-record"]) == 0
    assert srv.what() == ["upload", "launch"] * 2
    first = next(r for r, d in srv.dirs.items() if len(d["jobs"]) == 2)
    srv.end(first)
    assert main(["collect", "--all"]) == 0
    out = capsys.readouterr().out
    assert "running, 0 of 1 job(s) ended" in out and srv.what().count("record") == 2
    assert runner.pending() == [r.rsplit("/", 1)[1] for r in srv.dirs]
    with pytest.raises(SystemExit):
        main(["collect"])


def test_cli_collect_reports_a_failure(srv):
    detach()
    rroot, run_id = the_run(srv)
    srv.end(rroot, rcs={"tt_nom_27": "1 3"})
    assert main(["collect", run_id]) == 1
    assert main(["collect", "no-such-run"]) == 1


# ------------------------------------------------------------------ the scripts on the server
def _script(monkeypatch, fn, *args, rc=0, out=b""):
    sent = {}

    def fake(script, timeout=None, stdin_bytes=None, check=True):
        sent.update(script=script, timeout=timeout)
        if check and rc:
            raise remote.RemoteError(f"remote script failed ({rc})")
        return subprocess.CompletedProcess(["ssh"], rc, out, b"")

    monkeypatch.setattr(remote, "ssh_script", fake)
    monkeypatch.setattr(remote, "remote_root", lambda: "/r")
    return sent, fn(*args)


def test_status_is_one_short_look(monkeypatch):
    out = (b"exists 1\nlive 0\nended 2 1700\ndone 0 1000 1700\nfetched 1\nstart 999\njob a\njob b__duty0.55\n"
           b"limit timeout -k 60 86400 csh\nparallel xargs -P 3\nnote adcflow: compile step 38 s\n")
    sent, st = _script(monkeypatch, remote.status, "/r/run1", out=out)
    assert st == {"exists": True, "done": ("0", 1000, 1700), "fetched": True, "jobs": ["a", "b__duty0.55"],
                  "ended": 2, "start": 999, "last": 1700, "live": 0, "job_timeout": 86400.0, "parallel": 3,
                  "notes": ["compile step 38 s"]}
    s = sent["script"]
    assert remote.LIVE_FN in s and sent["timeout"] <= 120
    assert "sleep 5; look" in s                                         # a gap between two jobs is not a stop
    assert remote.parse_status("exists 0\n")["exists"] is False


def test_live_counts_processes_in_the_directory_and_the_launcher():
    f = remote.LIVE_FN
    assert '"$1"|"$1"/*) n=$((n+1))' in f and 'grep -qF "$1/launch.sh"' in f and remote.PID_FILE in f


def test_remove_needs_the_fetch_and_nothing_running(monkeypatch):
    sent, _ = _script(monkeypatch, remote.remove, "/r/run1")
    s = sent["script"]
    assert f'[ -f "$R/{remote.MARK_FETCHED}" ] || {{ echo "not fetched"; exit 3; }}' in s
    assert remote.LIVE_FN in s and s.index('n=$(live "$R")') < s.index('rm -rf "$R"')
    with pytest.raises(remote.RemoteBusy, match="not fetched"):
        _script(monkeypatch, remote.remove, "/r/run1", rc=3, out=b"not fetched")
    with pytest.raises(RuntimeError, match="outside"):
        remote.remove("/elsewhere/run1")


def test_clean_remote_keeps_running_and_uncollected_runs(monkeypatch):
    s = _script(monkeypatch, remote.clean_remote, 12)[0]["script"]
    assert 'if [ "$(live "$R")" -gt 0 ]; then echo "kept (running)' in s
    assert "kept (ended, not fetched" in s and f'[ -f "$R/{remote.MARK_DONE}" ]' in s and "[ 0 -eq 0 ]" in s
    assert "-mmin +720" in s
    assert "[ 1 -eq 0 ]" in _script(monkeypatch, remote.clean_remote, 12, True)[0]["script"]
