"""Remote Spectre execution on the simulation server over ssh.

Everything is staged into one run directory under ``remote_root`` (a local SSD
of the compute server, never /home), executed, the useful outputs are pulled
back, and the directory is deleted. Model files are only referenced by their
server path; nothing from the PDK is downloaded.

The batch runs on the server by itself (launch): an ssh call starts it detached from the ssh
session and returns, and the batch writes its rc and the done marker MARK_DONE into the run
directory when it ends. The local side only asks short questions (status) and fetches once it is
done; a lost connection changes nothing on the server. A run directory is deleted (remove) only
once its files were fetched (MARK_FETCHED) and nothing runs in it.
"""

from __future__ import annotations

import io
import os
import shlex
import subprocess
import tarfile
import time
from functools import lru_cache
from pathlib import Path

import yaml

from . import REPO_ROOT

SIM_YAML = REPO_ROOT / "specs" / "sim.yaml"
DEFAULT_JOBS = 6                                 # parallel Spectre runs without `sim.jobs` in the site config
JOB_TIMEOUT_S = 4 * 3600                         # a job's time limit without `timeout:` in its test spec
KILL_AFTER_S = 60                                # SIGKILL this long after the SIGTERM of a time limit
COMPILE_CAP_S = 900                              # the compile step stops its Spectre after this at the latest
SERVER_MARGIN_S = 300                            # slack of the batch backstops (server side, then ssh)
TIMEOUT_RCS = ("124", "137")                     # rc of a job that coreutils `timeout` ended (TERM, or KILL too)
SOA_TIMEOUT_S = 3600                             # the SOA step after the batch (soa_core.py over its jobs)
MARK_DONE = "adcflow.done"                       # "<rc> <start> <end>" (s since the epoch) of a batch that ended
MARK_FETCHED = "adcflow.fetched"                 # the run's files were fetched (remove requires it)
PID_FILE = "adcflow.pid"                         # the pid of the detached launch.sh
BATCH_LOG = "batch.log"                          # what launch.sh and the batch print (the compile-step notes)

# `live <dir>`: the number of processes of this account whose cwd is <dir> or below it, plus one while
# the run's detached launch.sh lives (from the moment it is started, before it reaches $R itself)
LIVE_FN = r"""live() {
  local n=0 p pid
  for p in $(pgrep -u "$(id -un)"); do
    case "$(readlink /proc/$p/cwd 2>/dev/null)" in "$1"|"$1"/*) n=$((n+1));; esac
  done
  pid=$(cat "$1/adcflow.pid" 2>/dev/null)
  if [ -n "$pid" ] && tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null | grep -qF "$1/launch.sh"; then n=$((n+1)); fi
  echo $n
}"""


class RunTimeout(RuntimeError):
    """A batch ran past its backstop limit; its Spectre processes were killed on the server."""


class RemoteError(RuntimeError):
    """ssh or scp failed: the connection, or a command on the server."""


class RemoteBusy(RuntimeError):
    """A run directory was not deleted: it is not fetched yet, or something still runs in it."""


@lru_cache
def cfg() -> dict:
    """specs/sim.yaml (site independent) merged with the `sim` section of the site config."""
    from .site import site

    with open(SIM_YAML, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    c.update(site().get("sim") or {})
    if os.environ.get("ADCFLOW_HOST"):
        c["host"] = os.environ["ADCFLOW_HOST"]
    for key in ("host", "remote_root", "env_setup"):
        if not c.get(key):
            raise RuntimeError(f"site config {site()['_path']}: sim.{key} is required")
    return c


def default_jobs() -> int:
    """Default of --jobs: `sim.jobs` of the site config, else DEFAULT_JOBS."""
    from .site import SiteConfigError, site

    try:
        return int((site().get("sim") or {}).get("jobs") or DEFAULT_JOBS)
    except SiteConfigError:
        return DEFAULT_JOBS


def _tool(name: str) -> str:
    """ssh / scp executable: site config `sim.<name>`, else Windows OpenSSH on
    Windows (a Git-Bash msys ssh found first on PATH can hang on binary pipes)."""
    if cfg().get(name):
        return str(cfg()[name])
    if os.name == "nt":
        win = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "OpenSSH" / f"{name}.exe"
        if win.exists():
            return str(win)
    return name


def _ssh_base() -> list[str]:
    return [_tool("ssh"), "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
            "-o", "ServerAliveInterval=30", cfg()["host"]]


def ssh_script(script: str, timeout: float | None = None, stdin_bytes: bytes | None = None,
               check: bool = True) -> subprocess.CompletedProcess:
    """Run a bash script on the server (the remote login shell may be csh)."""
    if stdin_bytes is not None:
        raise ValueError("use ssh_pipe for binary stdin")
    p = subprocess.run(_ssh_base() + ["bash", "-s"], input=script.encode(), capture_output=True,
                       timeout=timeout)
    if check and p.returncode != 0:
        raise RemoteError(f"remote script failed ({p.returncode}): {p.stderr.decode(errors='replace')[-2000:]}")
    return p


def ssh_pipe(remote_cmd: str, data: bytes | None = None, timeout: float | None = None) -> bytes:
    """Run one command through bash (the login shell may be csh) with binary stdin/stdout."""
    wrapped = "bash -c " + shlex.quote(remote_cmd)
    cmd = _ssh_base() + [wrapped]
    if data is not None:
        p = subprocess.run(cmd, input=data, capture_output=True, timeout=timeout)
    else:   # stdin must be closed: Windows OpenSSH otherwise may never exit
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
    if p.returncode != 0:
        raise RemoteError(f"ssh {remote_cmd!r} failed: {p.stderr.decode(errors='replace')[-2000:]}")
    return p.stdout


@lru_cache
def remote_user() -> str:
    return ssh_pipe("whoami", timeout=60).decode().strip()


def remote_root() -> str:
    root = cfg()["remote_root"].format(user=remote_user())
    if root.startswith("/home"):
        raise RuntimeError("remote_root must not be under /home (use the local SSD)")
    return root


def upload_tree(local_dir: Path, remote_dir: str) -> None:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for p in sorted(local_dir.rglob("*")):
            if p.is_file():
                info = tf.gettarinfo(str(p), arcname=p.relative_to(local_dir).as_posix())
                info.mtime = int(time.time()) - 600   # avoid "time stamp in the future" noise
                with open(p, "rb") as f:
                    tf.addfile(info, f)
    ssh_pipe(f"mkdir -p {shlex.quote(remote_dir)} && tar xzf - -C {shlex.quote(remote_dir)} 2>/dev/null",
             data=buf.getvalue(), timeout=600)


def fetch(remote_dir: str, patterns: list[str], local_dir: Path, max_mb: float) -> list[str]:
    """Pull files matching patterns (relative to remote_dir/jobs/*/) back. Returns skipped files."""
    pats = " ".join(shlex.quote(p) for p in patterns)
    script = f"""
cd {shlex.quote(remote_dir)} || exit 0
: > fetch.list; : > skipped.list
for j in jobs/*/; do
  for p in {pats}; do
    for f in $j$p; do
      [ -f "$f" ] || continue
      sz=$(stat -c %s "$f")
      if [ "$sz" -le {int(max_mb * 1e6)} ]; then echo "$f" >> fetch.list; else echo "$f $sz" >> skipped.list; fi
    done
  done
done
sort -u fetch.list -o fetch.list
tar czf fetch.tgz -T fetch.list skipped.list 2>/dev/null
"""
    ssh_script(script, timeout=600)
    # one archive, copied with scp: piping multi-MB binary output through
    # Windows OpenSSH stdout can hang, and scp of several files at once is flaky
    local_tgz = local_dir / "fetch.tgz"
    local_dir.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([_tool("scp"), "-q", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
                        f"{cfg()['host']}:{remote_dir}/fetch.tgz", str(local_tgz)],
                       stdin=subprocess.DEVNULL, capture_output=True, timeout=1800)
    if p.returncode != 0:
        raise RemoteError(f"scp of results failed: {p.stderr.decode(errors='replace')[-1000:]}")
    blob = local_tgz.read_bytes()
    local_tgz.unlink()
    skipped: list[str] = []
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        for m in tf.getmembers():
            if not m.isfile() or ".." in m.name or m.name.startswith("/"):
                continue
            data = tf.extractfile(m).read()
            if m.name == "skipped.list":
                skipped = [ln for ln in data.decode().splitlines() if ln.strip()]
                continue
            dest = local_dir / m.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    return skipped


def _soa_step(parallel: int) -> str:
    """The SOA check of the jobs in soa_jobs.list (soa_core.py), run in the run directory; a job that
    has its soa_rows.json already is not reduced again (soa_core thins the transient it reads)."""
    return (f"xargs -P {max(int(parallel), 1)} -I J sh -c '[ -f jobs/J/soa_rows.json ] || "
            "python3 soa_core.py jobs/J > jobs/J/soa_reduce.log 2>&1' < soa_jobs.list")


def soa_reduce(remote_dir: str, jobs: list[str], parallel: int) -> None:
    """The per-device SOA check of these jobs on the server (soa_core.py). A job that fails has no
    soa_rows.json and keeps its full waveforms, which are too large to fetch: its result reports the
    missing transient as an error. Each job's log is soa_reduce.log, fetched with the job. A launched
    batch runs this step itself (launch); this is for a run adopted from a launcher that did not."""
    joblist = "\n".join(jobs)
    script = f"""
cd {shlex.quote(remote_dir)} || exit 1
cat > soa_jobs.list <<'EOF'
{joblist}
EOF
{_soa_step(parallel)}
"""
    ssh_script(script, timeout=SOA_TIMEOUT_S, check=False)


def launch(remote_dir: str, jobs: list[str], mode_args: list[str], parallel: int,
           job_timeout: float = JOB_TIMEOUT_S, compile_first: bool = True,
           soa_jobs: list[str] | None = None) -> int:
    """Start Spectre on every jobs/<job>/deck.scs, `parallel` at a time, detached from the ssh session
    (setsid nohup), and return the batch's backstop (s). The ssh call returns at once.

    The compiled Verilog-A is shared through Spectre's library sharing (-ahdlshipdbdir): with more
    than one job, a compile step first runs the first job's deck in a copy of its directory, with
    the shared library $R/ahdl_lib in create_or_update mode, and stops that Spectre once it reaches
    the analyses (every module of the deck is compiled and copied into the library by then; about
    a minute), or after COMPILE_CAP_S at the latest. All jobs then start together and only read
    the library: a module it lacks is compiled in the job's own directory, so no two Spectre runs
    write the same library.

    `job_timeout` (s) limits each job: coreutils `timeout` ends its csh and Spectre (their own
    process group) and the job's rc.txt gets 124 or 137 (TIMEOUT_RCS); the other jobs go on. The
    batch has a backstop derived from it (batch_limit); after a batch ended by it, everything still
    running in the run directory is killed. A batch that ended normally then runs the SOA check of
    `soa_jobs` (soa_core.py, at most SOA_TIMEOUT_S). Last, $R/launch.sh writes MARK_DONE: the batch's
    rc (124 or 137: the backstop), and its start and end on the server clock."""
    c = cfg()
    spectre = c.get("spectre", "spectre")
    setup = "; ".join(f"{cmd} >& /dev/null" for cmd in c["env_setup"])
    args = " ".join(shlex.quote(a) for a in mode_args)
    rd = shlex.quote(remote_dir)
    joblist = "\n".join(jobs)
    run = f"{spectre} -64 deck.scs +escchars +log spectre.log -format psfascii -raw deck.raw -ahdlshipdbdir=$R/ahdl_lib"
    tail = f"{args} +lqtimeout 900 -maxw 5 -maxn 5 >& spectre.stdout.log"
    script = f"""
set -u
R={rd}
cat > $R/jobs.list <<'EOF'
{joblist}
EOF
mkdir -p $R/ahdl_lib
cat > $R/run_one.sh <<'EOS'
#!/bin/bash
R="$1"; J="$2"; D="$R/jobs/$J"
cd "$D" || exit 1
start=$(date +%s)
timeout -k {KILL_AFTER_S} {int(job_timeout)} csh -c "{setup}; cd $D; {run} {tail}"
rc=$?
echo "$rc $(( $(date +%s) - start ))" > rc.txt
EOS
cat > $R/compile_va.sh <<'EOS'
#!/bin/bash
# the shared Verilog-A library from the deck of job $2, run in a copy of its directory and stopped
# at the analyses, or after {COMPILE_CAP_S} s; a failure here only leaves the jobs to compile for themselves
R="$1"; J="$2"; D="$R/compile"
cp -r "$R/jobs/$J" "$D" && cd "$D" || exit 0
start=$(date +%s)
csh -c "{setup}; cd $D; {run} -ahdlshipdbmode=create_or_update {tail}" &
pid=$!
while kill -0 $pid 2>/dev/null; do
  grep -q -e "Time for Elaboration" -e "DC simulation time" -e "Transient Analysis" spectre.log 2>/dev/null && break
  if [ $(( $(date +%s) - start )) -ge {COMPILE_CAP_S} ]; then
    echo "adcflow: compile step stopped at its cap of {COMPILE_CAP_S} s before the analyses; the jobs compile what the shared library lacks"
    break
  fi
  sleep 2
done
cd "$R"
for p in $(pgrep -u "$(id -un)"); do
  case "$(readlink /proc/$p/cwd 2>/dev/null)" in "$D"|"$D"/*) kill -9 $p 2>/dev/null;; esac
done
wait $pid
echo "adcflow: compile step $(( $(date +%s) - start )) s"
rm -rf "$D"
exit 0
EOS
chmod +x $R/run_one.sh $R/compile_va.sh
cat > $R/batch.sh <<'EOB'
R="$1"
"""
    compile_step = compile_first and len(jobs) > 1
    if compile_step:
        script += f"$R/compile_va.sh $R {shlex.quote(jobs[0])}\n"
    script += f"cat $R/jobs.list | xargs -P {int(parallel)} -I{{}} $R/run_one.sh $R {{}}\n"
    limit = batch_limit(len(jobs), parallel, job_timeout, compile_step)
    soa = ""
    if soa_jobs:
        script += "EOB\ncat > $R/soa_jobs.list <<'EOF'\n" + "\n".join(soa_jobs) + "\nEOF\n"
        soa = f"""elif [ $rc -eq 0 ]; then                       # the SOA check where the waveforms are (soa_core.py)
  (cd "$R" && timeout -k {KILL_AFTER_S} {SOA_TIMEOUT_S} {_soa_step(parallel)})
"""
    else:
        script += "EOB\n"
    script += f"""cat > $R/launch.sh <<'EOL'
#!/bin/bash
# the batch on its own (adcflow remote.launch): its backstop, the done marker when it ends
R="$1"
echo $$ > $R/{PID_FILE}
start=$(date +%s)
timeout -k {KILL_AFTER_S} {limit} bash $R/batch.sh $R
rc=$?
if [ $rc -eq 124 ] || [ $rc -eq 137 ]; then     # the backstop: nothing may keep running in $R
  for p in $(pgrep -u "$(id -un)"); do
    case "$(readlink /proc/$p/cwd 2>/dev/null)" in "$R"|"$R"/*) kill -9 $p 2>/dev/null;; esac
  done
{soa}fi
echo "$rc $start $(date +%s)" > $R/{MARK_DONE}.tmp
mv $R/{MARK_DONE}.tmp $R/{MARK_DONE}
EOL
rm -f $R/{MARK_DONE} $R/{MARK_FETCHED}
setsid nohup bash $R/launch.sh $R > $R/{BATCH_LOG} 2>&1 < /dev/null &
for i in $(seq 100); do [ -s $R/{PID_FILE} ] && exit 0; sleep 0.1; done
echo "launch.sh did not start" >&2
exit 1
"""
    ssh_script(script, timeout=300)
    return limit


def batch_limit(n_jobs: int, parallel: int, job_timeout: float, compile_step: bool) -> int:
    """The server-side backstop of a batch (s): the compile cap, then every wave of `parallel` jobs at
    its full job limit and KILL grace, plus SERVER_MARGIN_S. Normal batches end long before it."""
    waves = -(-max(n_jobs, 1) // max(int(parallel), 1))
    return (COMPILE_CAP_S if compile_step else 0) + waves * (int(job_timeout) + KILL_AFTER_S) + SERVER_MARGIN_S


def status(remote_dir: str) -> dict:
    """The state of a run directory on the server, from one short ssh call (it changes nothing there).

    exists; done: (rc, start, end) of MARK_DONE, None before the batch ends; fetched: MARK_FETCHED is
    there; jobs: the names in its jobs.list; ended: how many of them have an rc.txt; start / last:
    the server time of jobs.list (the batch's start) and of the latest rc.txt; live: processes of
    this account running in it (LIVE_FN); job_timeout / parallel: the job limit of its run_one.sh
    and the xargs -P of its batch.sh (None if absent); notes: the `adcflow:` lines of its batch log.
    A directory where nothing lives while jobs are left without rc.txt is looked at once more after
    a few seconds (the gap between two jobs of an xargs that a launcher of before launch runs)."""
    script = f"""
{LIVE_FN}
R={shlex.quote(remote_dir)}
[ -d "$R" ] || {{ echo "exists 0"; exit 0; }}
look() {{
  n=0; last=0; total=0
  if [ -f "$R/jobs.list" ]; then
    while read -r j; do
      [ -n "$j" ] || continue
      total=$((total+1))
      if [ -f "$R/jobs/$j/rc.txt" ]; then n=$((n+1)); t=$(stat -c %Y "$R/jobs/$j/rc.txt"); [ $t -gt $last ] && last=$t; fi
    done < "$R/jobs.list"
  fi
  l=$(live "$R")
}}
look
if [ ! -f "$R/{MARK_DONE}" ] && [ "$l" -eq 0 ] && [ $n -lt $total ]; then sleep 5; look; fi
echo "exists 1"
echo "live $l"
echo "ended $n $last"
[ -f "$R/{MARK_DONE}" ] && echo "done $(cat "$R/{MARK_DONE}")"
[ -f "$R/{MARK_FETCHED}" ] && echo "fetched 1"
[ -f "$R/jobs.list" ] && echo "start $(stat -c %Y "$R/jobs.list")" && sed 's/^/job /' "$R/jobs.list"
grep -o 'timeout -k [0-9]* [0-9]* csh' "$R/run_one.sh" 2>/dev/null | head -1 | sed 's/^/limit /'
grep -o 'xargs -P [0-9]*' "$R/batch.sh" 2>/dev/null | head -1 | sed 's/^/parallel /'
grep '^adcflow: ' "$R/{BATCH_LOG}" 2>/dev/null | sed 's/^/note /'
exit 0
"""
    p = ssh_script(script, timeout=120)
    return parse_status(p.stdout.decode(errors="replace"))


def parse_status(text: str) -> dict:
    st = {"exists": False, "done": None, "fetched": False, "jobs": [], "ended": 0, "start": None, "last": None,
          "live": 0, "job_timeout": None, "parallel": None, "notes": []}
    for line in text.splitlines():
        key, _, rest = line.partition(" ")
        w = rest.split()
        if key == "exists":
            st["exists"] = rest.strip() == "1"
        elif key == "live":
            st["live"] = int(w[0])
        elif key == "ended":
            st["ended"], st["last"] = int(w[0]), (int(w[1]) or None)
        elif key == "done" and w:
            st["done"] = (w[0], *(int(x) for x in w[1:3]))
        elif key == "fetched":
            st["fetched"] = True
        elif key == "start":
            st["start"] = int(w[0])
        elif key == "job" and w:
            st["jobs"].append(rest.strip())
        elif key == "limit":                        # "timeout -k 60 <s> csh"
            st["job_timeout"] = float(w[3])
        elif key == "parallel":                     # "xargs -P <n>"
            st["parallel"] = int(w[2])
        elif key == "note":
            st["notes"].append(rest[len("adcflow: "):])
    return st


def mark_fetched(remote_dir: str) -> None:
    """Record on the server that the run's files are fetched (MARK_FETCHED): remove needs it."""
    ssh_script(f"[ -d {shlex.quote(remote_dir)} ] && touch {shlex.quote(remote_dir)}/{MARK_FETCHED}", timeout=120)


def remove(remote_dir: str) -> None:
    """Delete a run directory on the server: only one inside remote_root, fetched (MARK_FETCHED)
    and with nothing running in it (LIVE_FN); else RemoteBusy and the directory stays."""
    root = remote_root()
    if not remote_dir.startswith(root + "/"):
        raise RuntimeError(f"refusing to delete {remote_dir} outside {root}")
    script = f"""
{LIVE_FN}
R={shlex.quote(remote_dir)}
[ -d "$R" ] || exit 0
[ -f "$R/{MARK_FETCHED}" ] || {{ echo "not fetched"; exit 3; }}
n=$(live "$R")
[ "$n" -eq 0 ] || {{ echo "$n process(es) still run in it"; exit 3; }}
rm -rf "$R"
"""
    p = ssh_script(script, timeout=600, check=False)
    if p.returncode == 3:
        raise RemoteBusy(f"{remote_dir} stays on the server: {p.stdout.decode(errors='replace').strip()}")
    if p.returncode:
        raise RemoteError(f"remote delete failed ({p.returncode}): {p.stderr.decode(errors='replace')[-1000:]}")


def clean_remote(older_than_h: float = 0.0, unfetched: bool = False) -> int:
    """Delete this project's run directories on the server older than `older_than_h` (by the
    directory's time). Kept: a directory where something runs (LIVE_FN), and one whose batch ended
    but whose files were never fetched (a done marker, or an rc.txt for every job, and no
    MARK_FETCHED): `adcflow collect` (or `sim/verify --adopt`) still needs it; `unfetched` deletes those too."""
    root = remote_root()
    mins = int(older_than_h * 60)
    script = f"""
{LIVE_FN}
[ -d {shlex.quote(root)} ] || exit 0
cd {shlex.quote(root)}
for d in $(find . -mindepth 1 -maxdepth 1 -type d -mmin +{mins}); do
  R="$PWD/${{d#./}}"
  if [ "$(live "$R")" -gt 0 ]; then echo "kept (running): $d"; continue; fi
  if [ {1 if unfetched else 0} -eq 0 ] && [ ! -f "$R/{MARK_FETCHED}" ]; then
    ended=0
    if [ -f "$R/{MARK_DONE}" ]; then ended=1
    elif [ -s "$R/jobs.list" ]; then
      ended=1
      while read -r j; do [ -z "$j" ] || [ -f "$R/jobs/$j/rc.txt" ] || ended=0; done < "$R/jobs.list"
    fi
    if [ $ended -eq 1 ]; then echo "kept (ended, not fetched; collect it, or --unfetched): $d"; continue; fi
  fi
  echo "$d"
  rm -rf "$R"
done
du -sh {shlex.quote(root)} 2>/dev/null
"""
    p = ssh_script(script, timeout=1800)
    print(p.stdout.decode())
    return 0
