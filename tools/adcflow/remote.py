"""Remote Spectre execution on the simulation servers over ssh.

Everything is staged into one run directory under ``remote_root`` (a local disk
of the compute server, never /home), executed, the useful outputs are pulled
back, and the directory is deleted. Model files are only referenced by their
server path (or by a host's local copy of them, ensure_models); nothing from the
PDK is downloaded.

The site config may list several hosts (hosts), each with its own settings. A launch probes them
at once and takes the one with the most room within its thread budget (choose), or spreads a large
batch over several; the run's record names its host, and every later call goes to that host. A
host whose Spectre is a sandbox wrapper gets its writable job directory and --read-only directories
(launch).

The batch runs on the server by itself (launch): an ssh call starts it detached from the ssh
session and returns, and the batch writes its rc and the done marker MARK_DONE into the run
directory when it ends. The local side only asks short questions (status) and fetches once it is
done; a lost connection changes nothing on the server. A run directory is deleted (remove) only
once its files were fetched (MARK_FETCHED) and nothing runs in it.
"""

from __future__ import annotations

import hashlib
import io
import os
import shlex
import subprocess
import sys
import tarfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
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
MODELS_DONE = ".adcflow_complete"                # the copy of the PDK models in a host's model_cache is whole
MIN_FREE_GB = 20.0                               # a host with less free space under remote_root is not chosen
PROBE_TIMEOUT_S = 90                             # the probe of a host before a launch

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
    if os.environ.get("ADCFLOW_HOST") and not c.get("hosts"):
        c["host"] = os.environ["ADCFLOW_HOST"]          # the single-host form: another ssh alias
    c.setdefault("_path", site().get("_path", "site config"))
    return c


# ------------------------------------------------------------------ the simulation hosts
@dataclass(frozen=True)
class Host:
    """A simulation server as the site config describes it (`sim.hosts`, or the single-host `sim`)."""
    name: str                                    # how runs record it (the ssh alias if not named)
    ssh: str                                     # ssh alias (key-based login)
    remote_root: str                             # run directories, on a local disk; {user} = the remote login
    env_setup: tuple[str, ...] = ()              # csh commands that make `spectre` available (not in a sandbox)
    spectre: str = "spectre"                     # the command
    spectre_args: tuple[str, ...] = ()           # appended to the mode's arguments; a +mt=N replaces the mode's +mt
    sandbox: bool = False                        # spectre is a sandbox wrapper: --read-only dirs, no csh
    threads: int | None = None                   # thread budget: what our Spectre runs may use there at most
    job_threads: int = 1                         # threads one Spectre run counts with
    cpus: str | None = None                      # taskset -c list the runs are pinned to (e.g. one socket)
    model_cache: str | None = None               # local directory the PDK model directory is copied into
    venv: str | None = None                      # local python venv with numpy for the SOA step (else python3)
    min_free_gb: float = MIN_FREE_GB             # a host with less free space under remote_root is not chosen


def _host(d: dict, where: str) -> Host:
    sandbox = bool(d.get("sandbox", str(d.get("spectre", "")).endswith("-sandbox")))
    for key in ("remote_root",) + (() if sandbox else ("env_setup",)):
        if not d.get(key):
            raise RuntimeError(f"{where}: {key} is required")
    ssh = d.get("ssh") or d.get("host")
    if not ssh:
        raise RuntimeError(f"{where}: ssh (the ssh alias) is required")
    args = tuple(str(a) for a in d.get("spectre_args") or ())
    mt = [a for a in args if a.startswith("+mt=")]
    return Host(name=str(d.get("name") or ssh), ssh=str(ssh), remote_root=str(d["remote_root"]),
                env_setup=tuple(d.get("env_setup") or ()), spectre=str(d.get("spectre") or "spectre"),
                spectre_args=args, sandbox=sandbox,
                threads=int(d["threads"]) if d.get("threads") else None,
                job_threads=int(d.get("job_threads") or (mt[-1].split("=")[1] if mt else 1)),
                cpus=str(d["cpus"]) if d.get("cpus") else None,
                model_cache=d.get("model_cache") or None, venv=d.get("venv") or None,
                min_free_gb=float(d.get("min_free_gb", MIN_FREE_GB)))


HOST_KEYS = ("remote_root", "env_setup", "spectre", "spectre_args", "sandbox", "threads", "job_threads", "cpus",
             "model_cache", "venv", "min_free_gb")


def hosts() -> list[Host]:
    """The configured simulation hosts: `sim.hosts` (a list, each with its own settings; keys left out
    come from `sim`), or the single host of `sim` (host, remote_root, env_setup, spectre). The first
    is the default host: a run whose record names no host (one of before several hosts) is there."""
    c = cfg()
    if c.get("hosts"):
        shared = {k: c[k] for k in HOST_KEYS if k in c}
        out = [_host({**shared, **h}, f"{c.get('_path', 'site config')}: sim.hosts[{i}]") for i, h in enumerate(c["hosts"])]
        names = [h.name for h in out]
        if len(set(names)) != len(names):
            raise RuntimeError(f"{c.get('_path', 'site config')}: sim.hosts: names must differ ({names})")
        return out
    return [_host(c, f"{c.get('_path', 'site config')}: sim")]


def get_host(host: "Host | str | None" = None) -> Host:
    """A host by name or ssh alias (None: the default host, the first)."""
    if isinstance(host, Host):
        return host
    hs = hosts()
    if host is None:
        return hs[0]
    for h in hs:
        if host in (h.name, h.ssh):
            return h
    raise RuntimeError(f"no simulation host {host!r} in the site config (hosts: {', '.join(h.name for h in hs)})")


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


def _ssh_base(host=None) -> list[str]:
    return [_tool("ssh"), "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
            "-o", "ServerAliveInterval=30", get_host(host).ssh]


def ssh_script(script: str, timeout: float | None = None, stdin_bytes: bytes | None = None,
               check: bool = True, host=None) -> subprocess.CompletedProcess:
    """Run a bash script on a host (the remote login shell may be csh)."""
    if stdin_bytes is not None:
        raise ValueError("use ssh_pipe for binary stdin")
    p = subprocess.run(_ssh_base(host) + ["bash", "-s"], input=script.encode(), capture_output=True,
                       timeout=timeout)
    if check and p.returncode != 0:
        raise RemoteError(f"remote script failed ({p.returncode}): {p.stderr.decode(errors='replace')[-2000:]}")
    return p


def ssh_pipe(remote_cmd: str, data: bytes | None = None, timeout: float | None = None, host=None) -> bytes:
    """Run one command through bash (the login shell may be csh) with binary stdin/stdout."""
    wrapped = "bash -c " + shlex.quote(remote_cmd)
    cmd = _ssh_base(host) + [wrapped]
    if data is not None:
        p = subprocess.run(cmd, input=data, capture_output=True, timeout=timeout)
    else:   # stdin must be closed: Windows OpenSSH otherwise may never exit
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
    if p.returncode != 0:
        raise RemoteError(f"ssh {remote_cmd!r} failed: {p.stderr.decode(errors='replace')[-2000:]}")
    return p.stdout


_USERS: dict[str, str] = {}                      # ssh alias -> remote login (from a probe, or whoami)


def remote_user(host=None) -> str:
    h = get_host(host)
    if h.ssh not in _USERS:
        _USERS[h.ssh] = ssh_pipe("whoami", timeout=60, host=h).decode().strip()
    return _USERS[h.ssh]


def _local_dir(template: str, user: str, what: str) -> str:
    d = template.format(user=user).rstrip("/")
    if d == "/home" or d.startswith("/home/"):
        raise RuntimeError(f"{what} must not be under /home (use a local disk of the server)")
    return d


def remote_root(host=None) -> str:
    h = get_host(host)
    return _local_dir(h.remote_root, remote_user(h), "remote_root")


def model_dir(host=None) -> str:
    """The PDK model directory the decks of a host include from: pdk.model_dir of the site config, or,
    for a host with `model_cache`, its local copy there (ensure_models makes it)."""
    from .site import get

    h = get_host(host)
    src = str(get("pdk", "model_dir")).rstrip("/")
    if not h.model_cache:
        return src
    tag = hashlib.sha1(src.encode()).hexdigest()[:12]
    return f"{_local_dir(h.model_cache, remote_user(h), 'model_cache')}/{tag}"


def ensure_models(host=None) -> str:
    """Copy the PDK model directory into the host's model_cache once (on the server, from its own mount;
    nothing comes to this PC), complete or not at all; returns the directory the decks include from.
    A host without model_cache includes pdk.model_dir as it is."""
    from .site import get

    h = get_host(host)
    dst = model_dir(h)
    if not h.model_cache:
        return dst
    src = str(get("pdk", "model_dir")).rstrip("/")
    cache = dst.rsplit("/", 1)[0]
    count = r"""find . -type f -printf '%s\n' | awk '{n++; b+=$1} END {print n " files, " b " bytes"}'"""
    script = f"""
set -u
S={shlex.quote(src)}; M={shlex.quote(dst)}; C={shlex.quote(cache)}
[ -f "$M/{MODELS_DONE}" ] && exit 0
mkdir -p "$C" && chmod 700 "$C" || exit 2
exec 9> "$C/.lock"; flock 9
[ -f "$M/{MODELS_DONE}" ] && exit 0
[ -d "$S" ] || {{ echo "pdk.model_dir is not readable on this host" >&2; exit 2; }}
rm -rf "$M.tmp" "$M"
cp -a "$S" "$M.tmp" || {{ rm -rf "$M.tmp"; exit 2; }}
a=$(cd "$S" && {count})
b=$(cd "$M.tmp" && {count})
[ "$a" = "$b" ] || {{ echo "copy incomplete: $a vs $b" >&2; rm -rf "$M.tmp"; exit 2; }}
touch "$M.tmp/{MODELS_DONE}" && mv "$M.tmp" "$M"
echo "copied the PDK model directory into its model_cache ($b)"
"""
    out = ssh_script(script, timeout=1800, host=h).stdout.decode(errors="replace").strip()
    if out:
        print(f"[adcflow] {h.name}: {out}")
    return dst


def python(host=None) -> str:
    """The python of the SOA step on a host: python3, or that of its `venv` (ensure_python makes it)."""
    h = get_host(host)
    return f"{_local_dir(h.venv, remote_user(h), 'venv')}/bin/python3" if h.venv else "python3"


def ensure_python(host=None) -> str:
    """The python of the SOA step on a host (soa_core.py needs numpy): python3, or the python of the
    host's `venv`, made once on its local disk: python3 -m venv, and numpy installed from a wheel
    for its python that pip of this PC downloads from PyPI (a host may not reach PyPI itself)."""
    h = get_host(host)
    py = python(h)
    if not h.venv:
        return py
    v = py.removesuffix("/bin/python3")
    q = shlex.quote(v)
    look = (f'V={q}; "$V/bin/python3" -c "import numpy" 2>/dev/null && echo ready || '
            "python3 -c 'import sys; print(\"python %d.%d\" % sys.version_info[:2])'")
    out = ssh_script(look, timeout=120, host=h).stdout.decode(errors="replace").split()
    if "ready" in out:
        return py
    if len(out) < 2 or out[0] != "python":
        raise RemoteError(f"{h.name}: no python3 for the SOA step ({' '.join(out)[-200:]})")
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p = subprocess.run([sys.executable, "-m", "pip", "download", "numpy", "--only-binary=:all:", "--quiet",
                            "--platform", "manylinux2014_x86_64", "--python-version", out[1],
                            "--implementation", "cp", "-d", tmp], capture_output=True, timeout=900)
        wheels = sorted(Path(tmp).glob("numpy-*.whl"))
        if p.returncode or not wheels:
            raise RemoteError(f"pip download of numpy for python {out[1]} failed: "
                              f"{p.stderr.decode(errors='replace')[-500:]}")
        wd = f"{v}.wheels"
        ssh_pipe(f"mkdir -p {shlex.quote(wd)} && cat > {shlex.quote(wd + '/' + wheels[0].name)}",
                 data=wheels[0].read_bytes(), timeout=900, host=h)
    script = f"""
set -u
V={q}; W={shlex.quote(wd)}
exec 9> "$V.lock"; flock 9
if ! "$V/bin/python3" -c 'import numpy' 2>/dev/null; then
  rm -rf "$V"
  python3 -m venv "$V" && "$V/bin/pip" -q install --no-index --find-links "$W" numpy     || {{ echo "cannot make the venv with numpy" >&2; rm -rf "$W"; exit 2; }}
fi
rm -rf "$W"
"""
    ssh_script(script, timeout=900, host=h)
    print(f"[adcflow] {h.name}: made the python venv of the SOA step")
    return py


# ------------------------------------------------------------------ choosing hosts
PROBE_FIELDS = ("user", "load", "nproc", "ours", "disk_mb")


def _probe_script(h: Host) -> str:
    root = h.remote_root.replace("{user}", "${u}")
    return f"""
u=$(id -un)
echo "user $u"
echo "load $(cut -d' ' -f1 /proc/loadavg)"
echo "nproc $(nproc)"
echo "ours $(pgrep -u "$u" -x spectre | wc -l)"
d="{root}"
while [ ! -d "$d" ] && [ "$d" != / ]; do d=$(dirname "$d"); done
echo "disk_mb $(df -BM --output=avail "$d" | tail -1 | tr -dc 0-9)"
"""


def parse_probe(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        k, _, v = line.partition(" ")
        if k in PROBE_FIELDS and v.strip():
            out[k] = v.strip() if k == "user" else float(v)
    missing = [k for k in PROBE_FIELDS if k not in out]
    if missing:
        raise RemoteError(f"probe: no {', '.join(missing)} in {text[-300:]!r}")
    return out


def capacity(h: Host, p: dict) -> dict:
    """What a probed host can take: `budget_jobs` more Spectre runs within its thread budget (`threads`,
    else all its threads) beside our runs there, and `free_jobs`, as many as also fit beside the load
    of the others (load average minus our runs). A host with less than min_free_gb under remote_root
    takes none (`usable` False)."""
    jt = max(h.job_threads, 1)
    ours = p["ours"] * jt
    others = max(p["load"] - ours, 0.0)
    budget = (h.threads or p["nproc"]) - ours
    idle = p["nproc"] - others - ours
    usable = p["disk_mb"] >= h.min_free_gb * 1024
    return {**p, "budget_jobs": max(int(budget // jt), 0) if usable else 0,
            "free_jobs": max(int(min(budget, idle) // jt), 0) if usable else 0, "usable": usable}


def probe(hs: list[Host]) -> dict[str, dict]:
    """One short ssh call to each host, all at once: its load, threads, our Spectre runs and free space
    (capacity). A host that does not answer maps to {"error": ...}."""
    def one(h: Host) -> dict:
        try:
            out = ssh_script(_probe_script(h), timeout=PROBE_TIMEOUT_S, host=h).stdout.decode(errors="replace")
            p = parse_probe(out)
            _USERS[h.ssh] = p["user"]
            return capacity(h, p)
        except (RemoteError, subprocess.TimeoutExpired, OSError) as e:
            return {"error": str(e).strip()[-200:] or type(e).__name__}

    with ThreadPoolExecutor(max_workers=max(len(hs), 1)) as ex:
        return dict(zip((h.name for h in hs), ex.map(one, hs)))


def describe(h: Host, c: dict) -> str:
    if "error" in c:
        return f"{h.name}: no answer ({c['error']})"
    return (f"{h.name}: load {c['load']:.1f} of {c['nproc']:.0f} threads, our runs {c['ours']:.0f}, "
            f"room for {c['free_jobs']} run(s) (budget {c['budget_jobs']}), "
            f"{c['disk_mb'] / 1024:.0f} GB free" + ("" if c["usable"] else f" (< {h.min_free_gb:g} GB: not used)"))


def choose(n_jobs: int, parallel: int, split: bool = False, only: list[str] | None = None) -> list[tuple[Host, int]]:
    """Where a batch of `n_jobs` runs, `parallel` at a time: [(host, its parallel)].

    The hosts (`only`, else ADCFLOW_HOST, else every configured host) are probed at once (probe) and the
    one with the most room is chosen (free_jobs, then the lower load, then the order of the config).
    Its parallel is `parallel`, at most what its thread budget leaves beside our other runs there
    (at least 1). With `split` the jobs are spread over several hosts: each takes as many of the
    `parallel` slots as it has room for, the roomiest first. A single host without a thread budget is
    taken as it is, without a probe."""
    env = os.environ.get("ADCFLOW_HOST") if cfg().get("hosts") else None
    names = only or ([env] if env else None)
    hs = [get_host(n) for n in names] if names else hosts()
    if len(hs) == 1 and not hs[0].threads:
        return [(hs[0], parallel)]
    caps = probe(hs)
    for h in hs:
        print(f"[adcflow] {describe(h, caps[h.name])}", flush=True)
    ok = [h for h in hs if caps[h.name].get("usable")]
    if not ok:
        raise RemoteError("no simulation host can take the batch: " + "; ".join(describe(h, caps[h.name]) for h in hs))
    order = {h.name: i for i, h in enumerate(hs)}
    ok.sort(key=lambda h: (-caps[h.name]["free_jobs"], caps[h.name]["load"], order[h.name]))
    if split and n_jobs > 1:
        out, left = [], min(parallel, n_jobs)
        for h in ok:
            take = min(caps[h.name]["free_jobs"], left)
            if take > 0:
                out.append((h, take))
                left -= take
        if len(out) > 1:
            return out
    best = ok[0]
    par = max(min(parallel, caps[best.name]["budget_jobs"]), 1)
    if par < parallel:
        print(f"[adcflow] {best.name}: {par} parallel run(s), not {parallel}: its thread budget "
              f"({best.threads or 'all'} threads, {best.job_threads} per run) beside our other runs there")
    return [(best, par)]


def show_hosts(only: list[str] | None = None, prepare: bool = False) -> int:
    """`adcflow hosts`: probe the hosts and print what a launch chooses by; with `prepare` also make
    each host's model copy and SOA venv (ensure_models, ensure_python). 1 if one did not answer."""
    hs = [get_host(n) for n in only] if only else hosts()
    caps = probe(hs)
    rc = 0
    for h in hs:
        kind = "sandbox" if h.sandbox else "csh env"
        extra = f"; {h.threads} thread budget, {h.job_threads} per run" if h.threads else ""
        print(f"{describe(h, caps[h.name])} [{kind}{extra}{'; pinned' if h.cpus else ''}]")
        if "error" in caps[h.name]:
            rc = 1
            continue
        if prepare:
            try:
                ensure_models(h)
                ensure_python(h)
            except (RuntimeError, subprocess.TimeoutExpired) as e:
                print(f"[adcflow] {h.name}: not prepared ({str(e).strip()[-300:]})")
                rc = 1
    return rc


def spread(jobs: list[str], slots: list[int]) -> list[list[str]]:
    """The jobs split in order into one part per host, in proportion to its parallel slots, each part
    at least one job (there are at least as many jobs as hosts with slots)."""
    n, total = len(jobs), sum(slots)
    counts = [n * s // total for s in slots]
    for i in sorted(range(len(slots)), key=lambda i: -(n * slots[i] % total))[:n - sum(counts)]:
        counts[i] += 1
    for i in range(len(counts)):
        if counts[i] == 0:
            j = max(range(len(counts)), key=lambda k: counts[k])
            counts[j] -= 1
            counts[i] = 1
    out, k = [], 0
    for c in counts:
        out.append(jobs[k:k + c])
        k += c
    return out


def upload_tree(local_dir: Path, remote_dir: str, host=None, jobs: list[str] | None = None) -> None:
    """Upload a staged run; with `jobs`, of its job directories only these (the part of a host)."""
    buf = io.BytesIO()
    keep = None if jobs is None else set(jobs)
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for p in sorted(local_dir.rglob("*")):
            rel = p.relative_to(local_dir).parts
            if keep is not None and rel[0] == "jobs" and len(rel) > 1 and rel[1] not in keep:
                continue
            if p.is_file():
                info = tf.gettarinfo(str(p), arcname=p.relative_to(local_dir).as_posix())
                info.mtime = int(time.time()) - 600   # avoid "time stamp in the future" noise
                with open(p, "rb") as f:
                    tf.addfile(info, f)
    ssh_pipe(f"mkdir -p {shlex.quote(remote_dir)} && tar xzf - -C {shlex.quote(remote_dir)} 2>/dev/null",
             data=buf.getvalue(), timeout=600, host=host)


def fetch(remote_dir: str, patterns: list[str], local_dir: Path, max_mb: float, host=None) -> list[str]:
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
    ssh_script(script, timeout=600, host=host)
    # one archive, copied with scp: piping multi-MB binary output through
    # Windows OpenSSH stdout can hang, and scp of several files at once is flaky
    local_tgz = local_dir / "fetch.tgz"
    local_dir.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([_tool("scp"), "-q", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
                        f"{get_host(host).ssh}:{remote_dir}/fetch.tgz", str(local_tgz)],
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


def _soa_step(parallel: int, python: str = "python3") -> str:
    """The SOA check of the jobs in soa_jobs.list (soa_core.py), run in the run directory; a job that
    has its soa_rows.json already is not reduced again (soa_core thins the transient it reads)."""
    return (f"xargs -P {max(int(parallel), 1)} -I J sh -c '[ -f jobs/J/soa_rows.json ] || "
            f"{python} soa_core.py jobs/J > jobs/J/soa_reduce.log 2>&1' < soa_jobs.list")


def soa_reduce(remote_dir: str, jobs: list[str], parallel: int, host=None) -> None:
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
{_soa_step(parallel, python(host))}
"""
    ssh_script(script, timeout=SOA_TIMEOUT_S, check=False, host=host)


def spectre_args(mode_args: list[str], host=None) -> list[str]:
    """The mode's arguments with the host's `spectre_args` after them; a +mt=N of the host replaces
    the mode's own +mt (its thread count is what the host's budget counts with)."""
    h = get_host(host)
    if any(a.startswith("+mt") for a in h.spectre_args):
        mode_args = [a for a in mode_args if not a.startswith("+mt")]
    return [*mode_args, *h.spectre_args]


# the read-only directories of a sandboxed job: every directory of the run directory but the jobs'
# (the staged design/ and tb/ its deck includes), and the PDK model copy ($M, empty without models)
SANDBOX_RO = """RO=()
for d in "$R"/*/; do d="${d%/}"; case "${d##*/}" in jobs|compile|ahdl_lib) ;; *) RO+=(--read-only "$d");; esac; done
[ -n "$M" ] && RO+=(--read-only "$M")"""


def launch(remote_dir: str, jobs: list[str], mode_args: list[str], parallel: int,
           job_timeout: float = JOB_TIMEOUT_S, compile_first: bool = True,
           soa_jobs: list[str] | None = None, host=None, models: str | None = None) -> int:
    """Start Spectre on every jobs/<job>/deck.scs, `parallel` at a time, detached from the ssh session
    (setsid nohup), and return the batch's backstop (s). The ssh call returns at once.

    The compiled Verilog-A is shared through Spectre's library sharing (-ahdlshipdbdir): with more
    than one job, a compile step first runs the first job's deck in a copy of its directory, with
    the shared library $R/ahdl_lib in create_or_update mode, and stops that Spectre once it reaches
    the analyses (every module of the deck is compiled and copied into the library by then; about
    a minute), or after COMPILE_CAP_S at the latest. All jobs then start together and only read
    the library: a module it lacks is compiled in the job's own directory, so no two Spectre runs
    write the same library.

    On a host whose spectre is a sandbox wrapper (Host.sandbox) only the job's own directory is
    writable and every other directory it reads is passed with --read-only: the run directory's
    staged directories and `models` (the host's copy of the PDK models, ensure_models). A read-only
    library is not read by Spectre (it takes it for one being written), so the compile step builds
    the library in its own directory and moves it to $R/ahdl_lib, and each job gets a hard-linked
    copy of it in its directory. Otherwise Spectre runs under csh with the host's env_setup.
    A host's `cpus` pins every Spectre run (taskset -c).

    `job_timeout` (s) limits each job: coreutils `timeout` ends its Spectre (with its csh or its
    sandbox) and the job's rc.txt gets 124 or 137 (TIMEOUT_RCS); the other jobs go on. The batch
    has a backstop derived from it (batch_limit); after a batch ended by it, everything still
    running in the run directory is killed. A batch that ended normally then runs the SOA check of
    `soa_jobs` (soa_core.py, at most SOA_TIMEOUT_S). Last, $R/launch.sh writes MARK_DONE: the batch's
    rc (124 or 137: the backstop), and its start and end on the server clock."""
    h = get_host(host)
    spectre = h.spectre
    args = " ".join(shlex.quote(a) for a in spectre_args(mode_args, h))
    pin = f"taskset -c {shlex.quote(h.cpus)} " if h.cpus else ""
    rd = shlex.quote(remote_dir)
    joblist = "\n".join(jobs)
    common = "-64 deck.scs +escchars +log spectre.log -format psfascii -raw deck.raw"
    opts = f"{args} +lqtimeout 900 -maxw 5 -maxn 5"
    if h.sandbox:
        m = shlex.quote(models or "")
        sb = f'{spectre} "${{RO[@]}}" -- {common}'
        run_one = f"""#!/bin/bash
R="$1"; J="$2"; D="$R/jobs/$J"; M={m}
cd "$D" || exit 1
{SANDBOX_RO}
rm -rf "$D/ahdl_lib"
if [ -d "$R/ahdl_lib" ]; then cp -al "$R/ahdl_lib" "$D/ahdl_lib"; else mkdir "$D/ahdl_lib"; fi
start=$(date +%s)
timeout -k {KILL_AFTER_S} {int(job_timeout)} {pin}{sb} -ahdlshipdbdir="$D/ahdl_lib" {opts} > spectre.stdout.log 2>&1
rc=$?
echo "$rc $(( $(date +%s) - start ))" > rc.txt"""
        compile_head = f"""R="$1"; J="$2"; D="$R/compile"; M={m}
cp -r "$R/jobs/$J" "$D" && cd "$D" || exit 0
{SANDBOX_RO}
mkdir -p "$D/ahdl_lib"
start=$(date +%s)
{pin}{sb} -ahdlshipdbdir="$D/ahdl_lib" -ahdlshipdbmode=create_or_update {opts} > spectre.stdout.log 2>&1 &"""
        compile_lib = """rm -rf "$R/ahdl_lib"
mv "$D/ahdl_lib" "$R/ahdl_lib" || mkdir -p "$R/ahdl_lib"
"""
    else:
        setup = "; ".join(f"{cmd} >& /dev/null" for cmd in h.env_setup)
        run = f"{spectre} {common} -ahdlshipdbdir=$R/ahdl_lib"
        tail = f"{opts} >& spectre.stdout.log"
        run_one = f"""#!/bin/bash
R="$1"; J="$2"; D="$R/jobs/$J"
cd "$D" || exit 1
start=$(date +%s)
timeout -k {KILL_AFTER_S} {int(job_timeout)} {pin}csh -c "{setup}; cd $D; {run} {tail}"
rc=$?
echo "$rc $(( $(date +%s) - start ))" > rc.txt"""
        compile_head = f"""R="$1"; J="$2"; D="$R/compile"
cp -r "$R/jobs/$J" "$D" && cd "$D" || exit 0
start=$(date +%s)
{pin}csh -c "{setup}; cd $D; {run} -ahdlshipdbmode=create_or_update {tail}" &"""
        compile_lib = ""
    script = f"""
set -u
R={rd}
cat > $R/jobs.list <<'EOF'
{joblist}
EOF
mkdir -p $R/ahdl_lib
cat > $R/run_one.sh <<'EOS'
{run_one}
EOS
cat > $R/compile_va.sh <<'EOS'
#!/bin/bash
# the shared Verilog-A library from the deck of job $2, run in a copy of its directory and stopped
# at the analyses, or after {COMPILE_CAP_S} s; a failure here only leaves the jobs to compile for themselves
{compile_head}
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
{compile_lib}echo "adcflow: compile step $(( $(date +%s) - start )) s"
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
  (cd "$R" && timeout -k {KILL_AFTER_S} {SOA_TIMEOUT_S} {_soa_step(parallel, python(h))})
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
    ssh_script(script, timeout=300, host=h)
    return limit


def batch_limit(n_jobs: int, parallel: int, job_timeout: float, compile_step: bool) -> int:
    """The server-side backstop of a batch (s): the compile cap, then every wave of `parallel` jobs at
    its full job limit and KILL grace, plus SERVER_MARGIN_S. Normal batches end long before it."""
    waves = -(-max(n_jobs, 1) // max(int(parallel), 1))
    return (COMPILE_CAP_S if compile_step else 0) + waves * (int(job_timeout) + KILL_AFTER_S) + SERVER_MARGIN_S


def status(remote_dir: str, host=None) -> dict:
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
grep -o 'timeout -k [0-9]* [0-9]* ' "$R/run_one.sh" 2>/dev/null | head -1 | sed 's/^/limit /'
grep -o 'xargs -P [0-9]*' "$R/batch.sh" 2>/dev/null | head -1 | sed 's/^/parallel /'
grep '^adcflow: ' "$R/{BATCH_LOG}" 2>/dev/null | sed 's/^/note /'
exit 0
"""
    p = ssh_script(script, timeout=120, host=host)
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
        elif key == "limit":                        # "timeout -k 60 <s> "
            st["job_timeout"] = float(w[3])
        elif key == "parallel":                     # "xargs -P <n>"
            st["parallel"] = int(w[2])
        elif key == "note":
            st["notes"].append(rest[len("adcflow: "):])
    return st


def mark_fetched(remote_dir: str, host=None) -> None:
    """Record on the server that the run's files are fetched (MARK_FETCHED): remove needs it."""
    ssh_script(f"[ -d {shlex.quote(remote_dir)} ] && touch {shlex.quote(remote_dir)}/{MARK_FETCHED}", timeout=120,
               host=host)


def remove(remote_dir: str, host=None) -> None:
    """Delete a run directory on the server: only one inside remote_root, fetched (MARK_FETCHED)
    and with nothing running in it (LIVE_FN); else RemoteBusy and the directory stays."""
    root = remote_root(host)
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
    p = ssh_script(script, timeout=600, check=False, host=host)
    if p.returncode == 3:
        raise RemoteBusy(f"{remote_dir} stays on the server: {p.stdout.decode(errors='replace').strip()}")
    if p.returncode:
        raise RemoteError(f"remote delete failed ({p.returncode}): {p.stderr.decode(errors='replace')[-1000:]}")


def clean_remote(older_than_h: float = 0.0, unfetched: bool = False, only: list[str] | None = None) -> int:
    """Delete this project's run directories on the server older than `older_than_h` (by the
    directory's time). Kept: a directory where something runs (LIVE_FN), and one whose batch ended
    but whose files were never fetched (a done marker, or an rc.txt for every job, and no
    MARK_FETCHED): `adcflow collect` (or `sim/verify --adopt`) still needs it; `unfetched` deletes those too.
    Every configured host, or those of `only`; 1 if one of them could not be cleaned."""
    rc = 0
    for h in [get_host(n) for n in only] if only else hosts():
        try:
            _clean_host(h, older_than_h, unfetched)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"[adcflow] {h.name}: not cleaned ({str(e).strip()[-300:]})")
            rc = 1
    return rc


def _clean_host(h: Host, older_than_h: float, unfetched: bool) -> None:
    root = remote_root(h)
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
    p = ssh_script(script, timeout=1800, host=h)
    print(f"[adcflow] {h.name}:")
    print(p.stdout.decode())
