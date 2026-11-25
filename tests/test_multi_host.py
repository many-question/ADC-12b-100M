"""Several simulation hosts (remote.hosts): the site config lists them, a launch probes them and takes
the one with the most room within its thread budget (remote.choose) or spreads the jobs over several,
the run's manifest names its host(s) and every later call goes back there; a run of before several
hosts belongs to the default host. A host whose Spectre is a sandbox wrapper gets --read-only
directories, a hard-linked copy of the Verilog-A library and its local copy of the PDK models."""

import shutil
import subprocess
import textwrap

import pytest

from adcflow import checks, remote, runner, site
from adcflow.cli import main

TEST, CORNERS = "tb_sarlogic_func", "tt_nom_27,ff_high_125,ss_low_m40"
BASE = {"modes": {"aps": ["+aps"], "cx": ["+preset=cx", "+mt"]}, "fetch": ["*.txt"], "fetch_max_mb": 50}
LEGACY = {**BASE, "host": "old", "remote_root": "/ssd/{user}/runs", "env_setup": ["source env"], "spectre": "spectre"}
MULTI = {**BASE, "spectre_args": ["+mt=2"], "threads": 32, "hosts": [
    {"name": "a", "ssh": "alias-a", "remote_root": "/ssd/{user}/runs", "env_setup": ["source env"], "cpus": "0-62:2"},
    {"name": "b", "ssh": "alias-b", "remote_root": "/scratch/{user}/runs", "spectre": "spectre-sandbox",
     "model_cache": "/scratch/{user}/pdk", "venv": "/scratch/{user}/py"},
    {"name": "c", "ssh": "alias-c", "remote_root": "/scratch/{user}/runs", "spectre": "spectre-sandbox"}]}


@pytest.fixture
def multi(monkeypatch):
    monkeypatch.setattr(remote, "cfg", lambda: MULTI)
    monkeypatch.delenv("ADCFLOW_HOST", raising=False)
    monkeypatch.setitem(remote._USERS, "alias-a", "u")
    monkeypatch.setitem(remote._USERS, "alias-b", "u")
    monkeypatch.setitem(remote._USERS, "alias-c", "u")


def caps(**hosts):
    """probe results: name -> (load, our running Spectre, free GB[, runs of our pending batches]) or an
    error text."""
    def probe(hs):
        out = {}
        for h in hs:
            v = hosts[h.name]
            out[h.name] = {"error": v} if isinstance(v, str) else remote.capacity(
                h, {"user": "u", "load": v[0], "nproc": 64.0, "ours": v[1], "disk_mb": v[2] * 1024.0,
                    "pending": v[3] if len(v) > 3 else 0.0})
        return out
    return probe


# ------------------------------------------------------------------ the site config
def test_the_single_host_form_still_works(monkeypatch):
    monkeypatch.setattr(remote, "cfg", lambda: LEGACY)
    (h,) = remote.hosts()
    assert (h.name, h.ssh, h.env_setup, h.sandbox, h.threads, h.cpus, h.model_cache) == \
        ("old", "old", ("source env",), False, None, None, None)
    assert remote.get_host() is not None and remote.get_host(None).name == "old"
    assert remote.choose(3, 6) == [(h, 6)]                              # one host, no budget: no probe


def test_each_host_has_its_own_settings_and_shares_the_rest(multi):
    a, b, c = remote.hosts()
    assert remote.get_host() == a and remote.get_host("b") == b and remote.get_host("alias-c") == c
    assert not a.sandbox and b.sandbox and c.sandbox and b.env_setup == ()
    assert a.threads == b.threads == 32 and a.job_threads == 2           # +mt=2 of the shared spectre_args
    assert a.cpus == "0-62:2" and b.cpus is None and remote.python(b) == "/scratch/u/py/bin/python3"
    assert remote.python(c) == "python3"
    with pytest.raises(RuntimeError, match="no simulation host 'x'"):
        remote.get_host("x")


@pytest.mark.parametrize("bad,match", [({"remote_root": None}, "remote_root is required"),
                                       ({"spectre": "spectre"}, "env_setup is required"),
                                       ({"ssh": None, "name": None}, "ssh")])
def test_a_host_needs_its_settings(monkeypatch, bad, match):
    h = {**MULTI["hosts"][1], **bad}
    monkeypatch.setattr(remote, "cfg", lambda: {**BASE, "hosts": [h]})
    with pytest.raises(RuntimeError, match=match):
        remote.hosts()


def test_nothing_under_home(multi, monkeypatch):
    monkeypatch.setattr(remote, "cfg", lambda: {**BASE, "hosts": [{**MULTI["hosts"][1], "remote_root": "/home/{user}/r"}]})
    with pytest.raises(RuntimeError, match="/home"):
        remote.remote_root()


def test_a_mode_thread_count_gives_way_to_the_hosts(multi):
    a = remote.get_host("a")
    assert remote.spectre_args(["+preset=cx", "+mt"], a) == ["+preset=cx", "+mt=2"]
    assert remote.spectre_args(["+aps"], a) == ["+aps", "+mt=2"]


# ------------------------------------------------------------------ choosing
def test_the_roomiest_host_is_chosen(multi, monkeypatch, capsys):
    monkeypatch.setattr(remote, "probe", caps(a=(60.0, 1, 900), b=(0.1, 0, 300), c=(3.0, 0, 300)))
    ((h, par),) = remote.choose(10, 8)
    assert h.name == "b" and par == 8                    # a is busy (others' load), b and c idle, b the less loaded
    out = capsys.readouterr().out
    assert "a: load 60.0 of 64 threads, our runs 1, room for 2 run(s) (budget 15)" in out


def test_the_thread_budget_limits_the_parallel_runs(multi, monkeypatch, capsys):
    monkeypatch.setattr(remote, "probe", caps(a="down", b=(20.0, 10, 300), c=(30.0, 12, 300)))
    ((h, par),) = remote.choose(30, 20)
    assert h.name == "b" and par == 6                    # 32 threads - 10 runs x 2 = 12 threads: 6 runs
    assert "6 parallel run(s), not 20" in capsys.readouterr().out


def test_launched_batches_count_before_their_spectre_runs(multi, monkeypatch, capsys):
    # b: one Spectre runs (the compile step of a batch of 16 at a time), c: nothing launched
    monkeypatch.setattr(remote, "probe", caps(a="down", b=(2.0, 1, 300, 16), c=(4.0, 0, 300)))
    ((h, par),) = remote.choose(24, 16)
    assert h.name == "c" and par == 16                   # b's budget is taken by its batch: 16 runs x 2 threads
    assert "b: load 2.0 of 64 threads, our runs 16 (1 running now), room for 0 run(s) (budget 0)" in \
        capsys.readouterr().out
    c = remote.capacity(remote.get_host("b"), {"user": "u", "load": 10.0, "nproc": 64.0, "ours": 5.0,
                                               "disk_mb": 1e6, "pending": 2.0})
    assert c["runs"] == 5 and c["budget_jobs"] == 11     # other sessions' Spectre count when they are more


class Server:
    """Hosts whose probe answers from their batches: (parallel, jobs left); a batch has one Spectre
    running (its compile step) until it ends, the rest of its runs not started yet."""

    def __init__(self, names):
        self.batches = {n: [] for n in names}

    def probe(self, hs):
        out = {}
        for h in hs:
            bs = self.batches[h.name]
            out[h.name] = remote.capacity(h, {"user": "u", "load": 2.0 * len(bs), "nproc": 64.0, "ours": len(bs),
                                              "disk_mb": 300 * 1024.0,
                                              "pending": sum(min(p, n) for p, n in bs)})
        return out

    def submit(self, n_jobs, parallel, **k):
        got = remote.choose(n_jobs, parallel, **k)
        for h, par in got:
            self.batches[h.name].append((par, n_jobs))
        return [(h.name, par) for h, par in got]

    def runs(self, name):
        return sum(min(p, n) for p, n in self.batches[name])


def test_back_to_back_launches_stay_within_the_budget(multi, monkeypatch, capsys):
    srv = Server(["a", "b", "c"])
    monkeypatch.setattr(remote, "probe", srv.probe)
    slept = []

    def sleep(s):                                        # while it waits, the first batch ends
        slept.append(s)
        srv.batches["b"].pop(0)
    monkeypatch.setattr(remote, "_sleep", sleep)
    assert srv.submit(24, 16, only=["b", "c"]) == [("b", 16)]
    assert srv.submit(24, 16, only=["b", "c"]) == [("c", 16)]   # not b again: its batch has not started Spectre
    assert srv.submit(8, 4, only=["b", "c"]) == [("b", 4)]      # both full: it waits for room, does not exceed
    assert slept == [remote.ROOM_POLL_S] and "waiting for room" in capsys.readouterr().out
    assert srv.submit(10, 16, only=["b"]) == [("b", 12)]        # 16 - 4 runs: what the budget leaves
    assert srv.runs("b") <= 16 and srv.runs("c") <= 16
    srv.batches["b"].clear()
    srv.batches["c"] = [(16, 2)]                                # a batch with 2 jobs left takes 2 runs
    assert srv.submit(40, 30, only=["b", "c"], split=True) == [("b", 16), ("c", 14)]


def test_it_gives_up_when_no_room_comes(multi, monkeypatch):
    monkeypatch.setattr(remote, "probe", caps(a="down", b=(4.0, 2, 300, 16), c="down"))
    clock = iter(range(0, 10 ** 6, 5000))
    monkeypatch.setattr(remote, "_clock", lambda: next(clock))
    monkeypatch.setattr(remote, "_sleep", lambda s: None)
    with pytest.raises(remote.RemoteError, match="stayed at its thread budget"):
        remote.choose(3, 4)


def test_hosts_without_answer_or_space_are_not_chosen(multi, monkeypatch):
    monkeypatch.setattr(remote, "probe", caps(a="ssh: timeout", b=(0.0, 0, 5), c=(1.0, 0, 300)))
    assert remote.choose(2, 2)[0][0].name == "c"
    monkeypatch.setattr(remote, "probe", caps(a="ssh: timeout", b=(0.0, 0, 5), c="down"))
    with pytest.raises(remote.RemoteError, match="no simulation host can take the batch"):
        remote.choose(2, 2)


def test_only_the_named_hosts_are_probed(multi, monkeypatch):
    seen = []
    monkeypatch.setattr(remote, "probe", lambda hs: seen.extend(h.name for h in hs) or caps(c=(0, 0, 300))(hs))
    assert remote.choose(2, 2, only=["c"])[0][0].name == "c" and seen == ["c"]
    monkeypatch.setenv("ADCFLOW_HOST", "c")
    seen.clear()
    assert remote.choose(2, 2)[0][0].name == "c" and seen == ["c"]


def test_split_spreads_the_slots_over_the_roomiest_hosts(multi, monkeypatch):
    monkeypatch.setattr(remote, "probe", caps(a=(50.0, 0, 900), b=(0.0, 10, 300), c=(0.0, 0, 300)))
    got = [(h.name, n) for h, n in remote.choose(45, 30, split=True)]
    assert got == [("c", 16), ("a", 7), ("b", 6)]          # room: c 16, a (64-50)/2 = 7, b (32-20)/2 = 6
    assert [(h.name, n) for h, n in remote.choose(45, 10, split=True)] == [("c", 10)]


def test_spread_keeps_the_order_in_proportion_to_the_slots():
    jobs = [f"j{i}" for i in range(10)]
    assert remote.spread(jobs, [16, 6, 7]) == [jobs[:6], jobs[6:8], jobs[8:]]
    assert sum(remote.spread(jobs, [1, 1, 1]), []) == jobs
    assert remote.spread(["x", "y"], [9, 1]) == [["x"], ["y"]]           # every host with slots gets a job


def test_the_probe_is_one_short_script():
    s = remote._probe_script(remote.Host("b", "alias-b", "/scratch/{user}/runs"))
    assert 'pgrep -u "$u" -x spectre' in s and "/proc/loadavg" in s and 'd="/scratch/${u}/runs"' in s
    assert 'echo "pending $(pending "/scratch/${u}/runs")"' in s
    p = remote.parse_probe("user u\nload 1.5\nnproc 64\nours 3\ndisk_mb 1000\n")
    assert p == {"user": "u", "load": 1.5, "nproc": 64.0, "ours": 3.0, "disk_mb": 1000.0, "pending": 0.0}
    assert remote.parse_probe("user u\nload 1\nnproc 4\nours 0\npending 7\ndisk_mb 9\n")["pending"] == 7.0
    with pytest.raises(remote.RemoteError, match="nproc"):
        remote.parse_probe("user u\nload 1\n")


def _bash():
    b = shutil.which("bash")
    if not b or subprocess.run([b, "-c", "[ -r /proc/$$/cmdline ]"]).returncode:
        pytest.skip("no bash with /proc")
    return b


def test_pending_counts_launched_and_reserved_batches(tmp_path):
    """PENDING_FN on a tree like a host's remote_root: launched batches whose launch.sh lives (also one
    level down, the runs of another design area), a reservation of a batch being uploaded; not a batch
    that ended, one whose launch.sh is gone (its pid now another process's) or an old reservation."""
    script = remote.PENDING_FN + textwrap.dedent("""
        T=$(pwd)/root
        batch() {   # dir parallel jobs ended: a launched batch with a live launch.sh
          mkdir -p $1/jobs; printf 'cat $R/jobs.list | xargs -P %s -I{} run\n' $2 > $1/batch.sh
          for i in $(seq $3); do echo j$i >> $1/jobs.list; mkdir -p $1/jobs/j$i; done
          for i in $(seq $4); do echo 0 > $1/jobs/j$i/rc.txt; done
          printf 'sleep 30; true\n' > $1/launch.sh
          bash $1/launch.sh & echo $! > $1/adcflow.pid
        }
        batch $T/r1 4 6 1                      # 5 jobs left, 4 at a time: 4
        batch $T/area/r2 8 3 0                 # one level down, 3 jobs: 3
        batch $T/r3 4 6 0; echo "0 1 2" > $T/r3/adcflow.done    # ended: 0
        mkdir -p $T/r4; cp $T/r1/batch.sh $T/r1/jobs.list $T/r4/; cp $T/r1/adcflow.pid $T/r4/   # not its launch.sh: 0
        mkdir -p $T/r5; echo "6 2" > $T/r5/adcflow.reserved       # being uploaded, 2 jobs: 2
        mkdir -p $T/r6; echo "6 10" > $T/r6/adcflow.reserved; touch -d '2 hours ago' $T/r6/adcflow.reserved   # 0
        mkdir -p $T/r7/jobs                    # never launched: 0
        sleep 0.5
        echo "pending $(pending "$T")"
        echo "none $(pending "$T/nothing")"
        kill $(jobs -p) 2>/dev/null
    """)
    p = subprocess.run([_bash(), "-s"], input=script.encode(), cwd=tmp_path, capture_output=True, timeout=60)
    out = p.stdout.decode()
    assert "pending 9\n" in out and "none 0\n" in out, (out, p.stderr.decode())


def test_the_upload_reserves_the_room_and_the_runner_uploads_first(monkeypatch, tmp_path):
    (tmp_path / "jobs" / "j1").mkdir(parents=True)
    (tmp_path / "jobs" / "j2").mkdir()
    sent = []
    monkeypatch.setattr(remote, "ssh_pipe", lambda cmd, data=None, timeout=None, host=None: sent.append(cmd))
    remote.upload_tree(tmp_path, "/scratch/u/runs/r1", jobs=["j2"], reserve=6)
    remote.upload_tree(tmp_path, "/scratch/u/runs/r2", reserve=4)
    remote.upload_tree(tmp_path, "/scratch/u/runs/r3")
    assert sent[0].startswith("mkdir -p /scratch/u/runs/r1 && echo '6 1' > /scratch/u/runs/r1/adcflow.reserved && tar")
    assert "echo '4 2' > /scratch/u/runs/r2/adcflow.reserved" in sent[1] and "reserved" not in sent[2]


# ------------------------------------------------------------------ the scripts of a host
def _launch(monkeypatch, host, models=None, jobs=("a", "b"), soa_jobs=None):
    sent = {}

    def fake(script, timeout=None, stdin_bytes=None, check=True, host=None):
        sent.update(script=script, host=host)
        return subprocess.CompletedProcess(["ssh"], 0, b"", b"")

    monkeypatch.setattr(remote, "ssh_script", fake)
    remote.launch("/r/run1", list(jobs), ["+aps"], 2, 3600, soa_jobs=soa_jobs, host=host, models=models)
    return sent


def _heredoc(script: str, name: str, end: str = "EOS") -> str:
    return script.split(f"{name} <<'{end}'\n", 1)[1].split(f"\n{end}\n", 1)[0]


def test_a_sandboxed_job_reads_the_run_and_the_models_read_only(multi, monkeypatch):
    sent = _launch(monkeypatch, "b", models="/scratch/u/pdk/abc", soa_jobs=["a"])
    assert sent["host"].name == "b"
    s = sent["script"]
    run_one = _heredoc(s, "$R/run_one.sh")
    assert "csh" not in run_one and "M=/scratch/u/pdk/abc" in run_one
    assert '*) RO+=(--read-only "$d");;' in run_one and "jobs|compile|ahdl_lib) ;;" in run_one
    assert '[ -n "$M" ] && RO+=(--read-only "$M")' in run_one
    assert 'cp -al "$R/ahdl_lib" "$D/ahdl_lib"' in run_one              # its own hard-linked library
    assert ('timeout -k 60 3600 spectre-sandbox "${RO[@]}" -- -64 deck.scs' in run_one
            and '-ahdlshipdbdir="$D/ahdl_lib" +aps +mt=2 +lqtimeout 900' in run_one)
    assert run_one.index("rc=$?") < run_one.index("> rc.txt")
    compile_va = _heredoc(s, "$R/compile_va.sh")
    assert "-ahdlshipdbmode=create_or_update" in compile_va and '-ahdlshipdbdir="$D/ahdl_lib"' in compile_va
    assert compile_va.index("kill -9") < compile_va.index('mv "$D/ahdl_lib" "$R/ahdl_lib"') < compile_va.index('rm -rf "$D"')
    assert "/scratch/u/py/bin/python3 soa_core.py" in _heredoc(s, "$R/launch.sh", "EOL")
    st = remote.parse_status("exists 1\nlimit timeout -k 60 3600 \n")    # status reads its job limit
    assert st["job_timeout"] == 3600.0


def test_a_csh_host_is_pinned_and_keeps_its_environment(multi, monkeypatch):
    s = _launch(monkeypatch, "a")["script"]
    run_one = _heredoc(s, "$R/run_one.sh")
    assert 'timeout -k 60 3600 taskset -c 0-62:2 csh -c "source env >& /dev/null; cd $D; spectre -64' in run_one
    assert "--read-only" not in run_one and "+aps +mt=2 +lqtimeout" in run_one
    assert 'taskset -c 0-62:2 csh -c "' in _heredoc(s, "$R/compile_va.sh")


def test_the_models_are_copied_on_the_host_whole_or_not_at_all(multi, monkeypatch):
    monkeypatch.setattr(site, "get", lambda sec, key: "/nfs/pdk/m")
    sent = {}

    def fake(script, timeout=None, stdin_bytes=None, check=True, host=None):
        sent.update(script=script, host=host)
        return subprocess.CompletedProcess(["ssh"], 0, b"", b"")

    monkeypatch.setattr(remote, "ssh_script", fake)
    d = remote.ensure_models("b")
    assert d.startswith("/scratch/u/pdk/") and sent["host"].name == "b"
    s = sent["script"]
    assert 'cp -a "$S" "$M.tmp"' in s and f'mv "$M.tmp" "$M"' in s and "flock 9" in s
    assert s.index('[ "$a" = "$b" ]') < s.index(f'touch "$M.tmp/{remote.MODELS_DONE}"')
    assert remote.ensure_models("a") == "/nfs/pdk/m"       # no model_cache: the models as they are
    assert remote.model_dir("c") == "/nfs/pdk/m"


def test_clean_remote_goes_to_every_host(multi, monkeypatch, capsys):
    seen = []

    def fake(script, timeout=None, stdin_bytes=None, check=True, host=None):
        seen.append(host.name)
        if host.name == "b":
            raise remote.RemoteError("ssh: down")
        return subprocess.CompletedProcess(["ssh"], 0, b"", b"")

    monkeypatch.setattr(remote, "ssh_script", fake)
    assert remote.clean_remote(12) == 1 and seen == ["a", "b", "c"]
    assert "b: not cleaned" in capsys.readouterr().out
    seen.clear()
    assert remote.clean_remote(12, only=["c"]) == 0 and seen == ["c"]


# ------------------------------------------------------------------ the runner
class Hosts:
    """remote's run-directory calls over several hosts (rroot -> host, state)."""

    def __init__(self):
        self.dirs, self.calls = {}, []

    def upload_tree(self, local_dir, rroot, host=None, jobs=None, reserve=None):
        self.calls.append(("upload", host, rroot, sorted(jobs)))
        self.dirs[rroot] = {"host": host, "jobs": list(jobs), "done": None, "fetched": False}

    def launch(self, rroot, jobs, mode_args, parallel, job_timeout=3600, compile_first=True, soa_jobs=None,
               host=None, models=None):
        self.calls.append(("launch", host, rroot, parallel, models))
        return 100

    def status(self, rroot, host=None):
        self.calls.append(("status", host, rroot))
        d = self.dirs.get(rroot)
        if d is None or d["host"] != host:
            return remote.parse_status("exists 0\n")
        lines = ["exists 1", f"live {0 if d['done'] else 1}", f"ended {len(d['jobs']) if d['done'] else 0} 5",
                 "start 1"] + [f"job {j}" for j in d["jobs"]] + ([f"done {d['done']}"] if d["done"] else [])
        return remote.parse_status("\n".join(lines))

    def fetch(self, rroot, patterns, local_dir, max_mb, host=None):
        self.calls.append(("fetch", host, rroot))
        for j in self.dirs[rroot]["jobs"]:
            (local_dir / "jobs" / j).mkdir(parents=True, exist_ok=True)
            (local_dir / "jobs" / j / "rc.txt").write_text("0 10\n")
            (local_dir / "jobs" / j / "spectre.log").write_text("ok\n")
        return []

    def mark_fetched(self, rroot, host=None):
        self.dirs[rroot]["fetched"] = True

    def remove(self, rroot, host=None):
        self.calls.append(("remove", host, rroot))
        del self.dirs[rroot]


@pytest.fixture
def farm(multi, monkeypatch, tmp_path):
    f = Hosts()
    for name in ("upload_tree", "launch", "status", "fetch", "mark_fetched", "remove"):
        monkeypatch.setattr(remote, name, getattr(f, name))
    monkeypatch.setattr(remote, "probe", caps(a=(60.0, 0, 900), b=(0.0, 13, 300), c=(0.0, 0, 300)))
    monkeypatch.setattr(runner, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(runner, "POLL_S", (0.0, 0.0))
    monkeypatch.setattr("adcflow.spectrum.require_toolbox", lambda: None)
    monkeypatch.setattr(runner, "result_dir", lambda block, test_id, viewsig: tmp_path / "results")
    monkeypatch.setattr(runner, "measure", lambda test, jd, ctx: {"t_ps": 1.0})
    monkeypatch.setattr(runner, "record", lambda *a, **k: tmp_path / "results" / "x.json")
    return f


def _end(f, batch_rc="0"):
    for d in f.dirs.values():
        d["done"] = f"{batch_rc} 10 20"


def test_a_run_goes_back_to_its_host(farm):
    runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 4, detach=True)
    (rroot,) = farm.dirs
    run_id = rroot.rsplit("/", 1)[1]
    assert rroot == f"/scratch/u/runs/{run_id}"                       # c: the roomiest (b has 13 runs)
    man = runner.load_manifest(run_id)
    assert man["host"] == "c" and [(p["host"], p["parallel"], p["models"]) for p in man["parts"]] == [("c", 3, None)]
    assert runner.collect(run_id)["state"] == "running"
    assert all(c[1] == "c" for c in farm.calls)
    _end(farm)
    assert runner.collect(run_id)["state"] == runner.COLLECTED
    assert farm.calls[-1] == ("remove", "c", rroot) and runner.load_manifest(run_id)["removed"]


def test_a_split_run_has_one_part_per_host_and_is_collected_from_all(farm, monkeypatch):
    monkeypatch.setattr(remote, "probe", caps(a=(60.0, 0, 900), b=(0.0, 14, 300), c=(0.0, 15, 300)))
    runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 4, detach=True, split=True)
    run_id = next(iter(farm.dirs)).rsplit("/", 1)[1]
    man = runner.load_manifest(run_id)
    parts = [(p["host"], len(p["jobs"])) for p in man["parts"]]
    assert parts == [("b", 2), ("a", 1)]          # room for 2 (b: budget left), 2 (a: others' load), 1 (c)
    assert sorted(j for p in man["parts"] for j in p["jobs"]) == sorted(man["jobs"])
    ups = [c for c in farm.calls if c[0] == "upload"]
    assert [(c[1], len(c[3])) for c in ups] == parts                  # each host gets only its jobs
    staged = runner.RUNS / run_id / "stage" / "jobs"
    for p in man["parts"]:                                             # a job's deck includes from its host's dir
        for j in p["jobs"]:
            assert f'include "{p["rroot"]}/jobs/{j}/tb.scs"' in (staged / j / "deck.scs").read_text()
    farm.dirs[man["parts"][0]["rroot"]]["done"] = "0 10 20"            # one part ended, the other runs
    assert runner.collect(run_id)["state"] == "running"
    _end(farm)
    assert runner.collect(run_id)["state"] == runner.COLLECTED
    assert {c[1] for c in farm.calls if c[0] in ("fetch", "remove")} == {"a", "b"} and not farm.dirs


def test_a_failed_part_fails_the_run(farm, monkeypatch):
    monkeypatch.setattr(remote, "probe", caps(a=(60.0, 0, 900), b=(0.0, 14, 300), c=(0.0, 15, 300)))
    runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 4, detach=True, split=True)
    run_id = next(iter(farm.dirs)).rsplit("/", 1)[1]
    _end(farm)
    farm.dirs[runner.load_manifest(run_id)["parts"][1]["rroot"]]["done"] = "1 10 30"
    with pytest.raises(RuntimeError, match=r"rc 1"):
        runner.collect(run_id)


def test_a_run_of_before_several_hosts_belongs_to_the_default_host(farm):
    runner.run_test(TEST, None, CORNERS, {}, {}, "aps", 4, detach=True, hosts=["a"])
    (rroot,) = farm.dirs
    run_id = rroot.rsplit("/", 1)[1]
    man = runner.load_manifest(run_id)
    for k in ("parts", "host"):                                        # as an old launcher wrote it
        man.pop(k)
    man["rroot"] = rroot
    runner.save_manifest(man)
    farm.dirs[rroot]["host"] = None                                    # the default host: called without a name
    _end(farm)
    assert runner.collect(run_id)["state"] == runner.COLLECTED
    assert [c[1] for c in farm.calls if c[0] in ("status", "fetch", "remove")][-3:] == [None, None, None]


def test_a_sandbox_host_with_a_model_cache_gets_its_models(farm, monkeypatch):
    monkeypatch.setattr(site, "get", lambda sec, key: {"model_dir": "/nfs/pdk", "core_file": "core.scs",
                                                         "hv_file": "hv.scs"}[key])
    copied = []
    monkeypatch.setattr(remote, "ensure_models", lambda host=None: copied.append(host))
    run_id = runner.submit(runner.run_args("tb_bootstrap_dc", None, "tt_nom_27", {}, {}, "aps", 2), hosts=["b"])
    (part,) = runner.load_manifest(run_id)["parts"]
    assert copied == ["b"] and part["models"].startswith("/scratch/u/pdk/")
    launch = next(c for c in farm.calls if c[0] == "launch")
    assert launch[1] == "b" and launch[4] == part["models"]
    deck = (runner.RUNS / run_id / "stage" / "jobs" / "tt_nom_27" / "deck.scs").read_text()
    assert f'include "{part["models"]}/core.scs"' in deck and "/nfs/pdk" not in deck
    run_id = runner.submit(runner.run_args("tb_bootstrap_dc", None, "tt_nom_27", {}, {}, "aps", 2), hosts=["c"])
    deck = (runner.RUNS / run_id / "stage" / "jobs" / "tt_nom_27" / "deck.scs").read_text()
    assert 'include "/nfs/pdk/core.scs"' in deck and copied == ["b"]   # c: the models as they are


def test_cli_hosts_shows_and_prepares(multi, monkeypatch, capsys):
    monkeypatch.setattr(remote, "probe", caps(a=(1.0, 0, 900), b=(0.0, 0, 300), c="down"))
    done = []
    monkeypatch.setattr(remote, "ensure_models", lambda h: done.append(("models", h.name)))
    monkeypatch.setattr(remote, "ensure_python", lambda h: done.append(("python", h.name)))
    assert main(["hosts", "--prepare"]) == 1                            # c did not answer
    out = capsys.readouterr().out
    assert "a: load 1.0" in out and "[csh env; 32 thread budget, 2 per run; pinned]" in out and "c: no answer" in out
    assert done == [("models", "a"), ("python", "a"), ("models", "b"), ("python", "b")]


def test_the_hygiene_check_knows_every_hosts_strings(monkeypatch):
    monkeypatch.setattr(site, "site", lambda: {"_path": "x", "sim": {"hosts": [
        {"name": "srv-one", "ssh": "srv-one-alias", "remote_root": "/scratch/{user}/runs",
         "model_cache": "/scratch2/{user}/pdk", "spectre": "/opt/tool/bin/sim"}]}})
    lits = [p for p, _ in checks._site_literals()]
    for v in ("srv-one", "srv-one-alias", "/scratch", "/scratch2", "/opt/tool/bin/sim"):
        assert any(__import__("re").fullmatch(p, v) for p in lits), v
