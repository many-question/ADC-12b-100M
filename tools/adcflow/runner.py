"""Build run decks for a block test, run them on the server, measure, record.

Deck layout (all paths absolute on the server):

    simulator lang=spectre
    parameters vdd=... vdd18=... tempc=... noise_en=... beh_speed=... vref_in=... cdac_behav=...
    adcflow_opts options temp=<T> tnom=27
    include <PDK sections>                 (when a transistor view or the test needs it)
    ahdl_include <Verilog-A of the behavioral views and the testbench>
    include <one view of every block>      (behav unless --view block=xtor or block=xtor:<candidate>)
    include design/top/adc_top.scs
    include jobs/<job>/tb.scs              (the testbench with its parameters substituted)
    save <device terminal nodes>           (tests with `soa:` in their spec, see soa.py)

Global parameters are declared by the deck only; testbenches and views use
them (`vdd`, `vdd18`, `tempc`, `noise_en`, `beh_speed`, `vref_in`, `cdac_behav`, `comp_behav`).

A test with `montecarlo:` in its spec (tb_comp_offset_mc) is one Spectre montecarlo analysis in its
testbench: the runner passes the number of samples and the seed as the testbench parameters
`mc_runs` and `mc_seed`, includes the statistical model sections of specs/corners.yaml
(pdk.mc_sections, corners.model_includes), records the settings as meta.mc and always measures the job, so that a
failed sample is recorded as failed (Spec.judge) and not lost with the run.

A result records only what its circuit depends on (deps.py): the files the testbench reaches
through the deck, and the arch.yaml values that its jobs' `prepare` and its measure read.

A run is submitted, then collected (docs/workflow.md §3). submit stages it in build/runs/<run_id>/,
uploads it, starts its batch on the server detached from ssh (remote.launch) and writes
build/runs/<run_id>/manifest.json: its arguments (run_args), its server directory and jobs, the job
limit, and the commit and tree the decks were built from. collect, in this process (wait) or in
another one later (`adcflow collect`), rebuilds the jobs, decks and SOA plans from the arguments
(prepare), checks them against the staged files (staged_differences), fetches the jobs once the
batch ended, measures and records them (or writes the verification records, verify.finish), and
deletes the server directory last. A run of a launcher of before the manifest is taken over with
`adopt` from its own arguments.
"""

from __future__ import annotations

import contextlib
import datetime as _dt
import importlib
import json
import os
import re
import shutil
import subprocess
import time
import traceback
import uuid
from dataclasses import dataclass, field, replace
from pathlib import Path

import yaml

from . import REPO_ROOT
from . import arch as archmod
from . import candidates, deps, jsonio, numerics, remote, soa
from .corners import Corner, by_name, corner_set, model_includes, vref_in
from .netlist import content_hash, parse, substitute_parameters
from .specs import Block, blocks, find_test

STAGE_DIRS, STAGE_EXT = deps.STAGE_DIRS, deps.STAGE_EXT
VA_YAML = REPO_ROOT / "specs" / "va_modules.yaml"
GLOBAL_PARAMS = ("vdd", "vdd18", "tempc", "noise_en", "devnoise", "beh_speed", "vref_in", "cdac_behav",
                 "comp_behav")


@dataclass
class Job:
    name: str
    corner: Corner
    params: dict
    globals_: dict
    tb_text: str = ""
    files: list[str] = field(default_factory=list)   # repo-relative files used (for hashes)
    extra: dict[str, str] = field(default_factory=dict)  # job-local input files written by `prepare`
    arch_keys: set[str] = field(default_factory=set)     # arch.yaml keys its `prepare` read


def _va_modules() -> dict:
    with open(VA_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)["modules"]


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception:
        return ""


def dirty_paths(porcelain: str) -> list[str]:
    """Paths that ``git status --porcelain`` lists (modified, staged or untracked) outside results/
    and verification/.

    Those do not count: they are outputs that a suite run (or a verify run, verify.py) rewrites
    while others run. Ignored files (site.local.yaml) are not listed by git at all. A rename counts
    by its new path.
    """
    out = []
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].split(" -> ")[-1].strip('"')
        if path.split("/")[0] in ("results", "verification"):
            continue
        out.append(path)
    return out


def git_state() -> dict:
    """``{"git_clean": True}``, or False plus ``git_dirty_paths`` (at most 20) for a result's meta."""
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True,
                           text=True, timeout=30)
        paths = dirty_paths(r.stdout) if r.returncode == 0 else ["(git status failed)"]
    except Exception:
        paths = ["(git status failed)"]
    return {"git_clean": True} if not paths else {"git_clean": False, "git_dirty_paths": paths[:20]}


def view_files(views: dict[str, str]) -> list[Path]:
    out = []
    for b in blocks().values():
        if b.name == "adc_top":
            continue
        v = views.get(b.name, "behav")
        p = candidates.resolve(b.name, v)[0]        # behav, xtor (selected or legacy) or xtor:<candidate>
        if not p.exists():
            raise FileNotFoundError(f"{b.name}: view {v!r} file {p} does not exist")
        out.append(p)
    out.append(REPO_ROOT / "design" / "top" / "adc_top.scs")
    return out


def needed_va(netlists: list[Path], tb_text: str) -> list[Path]:
    """Verilog-A files of the modules that the netlists and the testbench instantiate (the deck's ahdl_include)."""
    mods = _va_modules()
    masters: set[str] = set()
    for p in netlists:
        nl = parse(p)
        for sc in nl.subckts.values():
            masters |= {i.master for i in sc.instances}
        masters |= {i.master for i in nl.top_instances}
    nl = parse("tb.scs", text=tb_text)
    masters |= {i.master for i in nl.top_instances}
    for sc in nl.subckts.values():
        masters |= {i.master for i in sc.instances}
    return [REPO_ROOT / mods[m]["file"] for m in sorted(masters) if m in mods]


def _viewsig(block: Block, views: dict[str, str]) -> str:
    """Result-directory name of a run: behav, xtor (legacy view) or xtor-<candidate>; for adc_top
    xtor-<blk>[@<candidate>]+... over the blocks that are not behavioral (candidates.top_signature)."""
    if block.name == "adc_top":
        return candidates.top_signature(views, len(blocks()) - 1)
    return candidates.view_dir(block.name, views.get(block.name, "behav"))


def build_jobs(block: Block, test_id: str, test: dict, corners: list[Corner], views: dict,
               cli_params: dict, needs_pdk: bool = False) -> list[Job]:
    tb_path = REPO_ROOT / test["netlist"]
    tb_text = tb_path.read_text(encoding="utf-8")
    variants = test.get("variants") or [{}]
    jobs = []
    for c in corners:
        for var in variants:
            params = {**(test.get("params") or {}), **var, **cli_params}
            with archmod.track() as arch_keys:              # what the generated parameters and files read
                if test.get("prepare"):
                    mod, fn = test["prepare"].split(":")
                    params = getattr(importlib.import_module(mod), fn)(dict(params))
            extra = params.pop("_files", {})
            g = {"vdd": c.vdd, "vdd18": c.vdd18, "tempc": c.temp,
                 "noise_en": 1 if test.get("tran_noise") else 0, "devnoise": 1 if needs_pdk else 0,
                 "beh_speed": 1.0, "vref_in": vref_in(),
                 # 1 while adc_cdac is behavioral: its kT/C source counts the sampled noise of the
                 # whole sampling network, so the testbench source resistors must be noiseless
                 "cdac_behav": 0 if views.get("adc_cdac", "behav") != "behav" else 1,
                 # 1 while adc_comp is behavioral: tb_comp_offset_mc then gives every Monte Carlo
                 # sample a stand-in offset (the behavioral comparator has no device statistics)
                 "comp_behav": 0 if views.get("adc_comp", "behav") != "behav" else 1}
            for k in list(params):
                if k in GLOBAL_PARAMS:
                    g[k] = params.pop(k)
            text, done = substitute_parameters(tb_text, {k: v for k, v in params.items()})
            missing = set(params) - done
            if missing:
                raise ValueError(f"{test['netlist']}: parameters not declared in the testbench: {sorted(missing)}")
            vname = "_".join(f"{k}{v}" for k, v in var.items())
            name = c.name + (f"__{vname}" if vname else "")
            jobs.append(Job(name=name, corner=c, params=params, globals_=g, tb_text=text, extra=extra,
                            arch_keys=set(arch_keys)))
    return jobs


def mc_settings(block: Block, test_id: str, test: dict, corners: list[Corner], over: dict | None = None,
                params: dict | None = None) -> dict | None:
    """The Monte Carlo settings of a run (meta.mc): the test's `montecarlo:` {runs, seed, variations,
    models} with `over` (sim --mc-runs / --mc-seed) and `--param mc_runs=` / `mc_seed=` applied, plus
    firstrun 1; None for a test without `montecarlo:`. A Monte Carlo test runs only at corners
    where one of its Monte Carlo specs applies (its statistical models belong to that corner)."""
    mc = test.get("montecarlo")
    if not mc:
        if over:
            raise ValueError(f"{test_id}: not a Monte Carlo test (no `montecarlo:` in its spec)")
        return None
    out = {**mc, **{k: v for k, v in (over or {}).items() if v is not None}}
    for key, name in (("runs", "mc_runs"), ("seed", "mc_seed")):
        if name in (params or {}):
            out[key] = (params or {})[name]
    out = {"runs": int(out["runs"]), "seed": int(out["seed"]), "firstrun": 1,
           "variations": out["variations"], "models": out["models"]}
    if out["runs"] < 1:
        raise ValueError(f"{test_id}: mc runs must be >= 1")
    specs = [s for s in block.specs if s.test == test_id and s.mc]
    bad = [c.name for c in corners if not any(s.applies(c, out) for s in specs)]
    if bad:
        raise ValueError(f"{test_id} is a Monte Carlo test for the corners of {', '.join(s.id for s in specs)} "
                         f"({', '.join(sorted({s.corners for s in specs}))}); not {', '.join(bad)}")
    return out


def make_deck(job: Job, rroot: str, views: dict, needs_pdk: bool, mc: str | None,
              extra: list[str] | None = None) -> tuple[str, list[Path]]:
    """The run deck of a job; `extra` lines (the saves of the SOA check) come after the testbench;
    `mc` names the statistical model sections of a Monte Carlo run (pdk.mc_sections)."""
    vfiles = view_files(views)
    va = needed_va(vfiles, job.tb_text)
    L = [f"// adcflow deck: job={job.name} views={views or 'all behav'}",
         "simulator lang=spectre",
         "global 0",
         "parameters " + " ".join(f"{k}={v}" for k, v in job.globals_.items()),
         f"adcflow_opts options temp={job.corner.temp:g} tnom=27"]
    if needs_pdk:
        L.append(model_includes(job.corner, mc=mc))
    for p in va:
        L.append(f'ahdl_include "{rroot}/{p.relative_to(REPO_ROOT).as_posix()}"')
    for p in vfiles:
        L.append(f'include "{rroot}/{p.relative_to(REPO_ROOT).as_posix()}"')
    L.append(f'include "{rroot}/jobs/{job.name}/tb.scs"')
    L += extra or []
    used = vfiles + va
    return "\n".join(L) + "\n", used


def stage(run_dir: Path, jobs: list[Job], decks: dict[str, str]) -> None:
    st = run_dir / "stage"
    if st.exists():
        shutil.rmtree(st)
    for d in STAGE_DIRS:
        for p in (REPO_ROOT / d).rglob("*"):
            if p.is_file() and p.suffix in STAGE_EXT:
                dest = st / p.relative_to(REPO_ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, dest)
    for pattern, dest in deps.STAGE_COPIES:      # testbench Verilog-A includes the architecture constants
        for src in REPO_ROOT.glob(pattern):
            shutil.copyfile(src, st / dest / src.name)
    for j in jobs:
        jd = st / "jobs" / j.name
        jd.mkdir(parents=True, exist_ok=True)
        (jd / "tb.scs").write_text(j.tb_text, encoding="utf-8", newline="\n")
        (jd / "deck.scs").write_text(decks[j.name], encoding="utf-8", newline="\n")
        for fname, text in j.extra.items():
            (jd / fname).write_text(text, encoding="utf-8", newline="\n")


def _spectre_errors(log: Path) -> list[str]:
    if not log.exists():
        return ["no spectre.log"]
    lines = log.read_text(errors="replace").splitlines()
    errs = [ln.strip() for i, ln in enumerate(lines) if "ERROR" in ln]
    return errs[:10]


def job_error(rc: str, errs: list[str], job_timeout: float) -> str:
    """The recorded error of a job whose Spectre did not end with rc 0."""
    if rc in remote.TIMEOUT_RCS:
        return (f"timeout: the job ran past its `timeout:` of {job_timeout:.0f} s and was killed "
                "(docs/workflow.md §4)")
    return "; ".join(errs) or f"spectre rc={rc}"


def measure(test: dict, job_dir: Path, ctx: dict) -> dict:
    mod_name, fn_name = test["measure"].split(":")
    fn = getattr(importlib.import_module(mod_name), fn_name)
    return fn(job_dir, ctx)


def result_dir(block: Block, test_id: str, viewsig: str) -> Path:
    return REPO_ROOT / "results" / block.name / test_id / viewsig


def result_doc(block: Block, test_id: str, viewsig: str, job: Job, metrics: dict, meta: dict,
               figures: list[dict] | None = None) -> dict:
    """The result JSON of a job: every metric, the verdicts of the specs that apply at its corner
    and, as `specs_na`, the specs of the test that do not apply there (raw value, no verdict)."""
    verdict, na = block.verdicts(test_id, job.corner, meta.get("mc"), metrics)
    doc = {"block": block.name, "test": test_id, "view": viewsig, "corner": job.corner.name,
           "params": job.params, "globals": job.globals_, "metrics": metrics, "specs": verdict}
    if na:
        doc["specs_na"] = na
    return {**doc, "figures": figures or [], "meta": meta}


def record(block: Block, test_id: str, viewsig: str, job: Job, metrics: dict, meta: dict,
           figures: list[dict] | None = None) -> Path:
    out = result_dir(block, test_id, viewsig) / f"{job.name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = result_doc(block, test_id, viewsig, job, metrics, meta, figures)
    out.write_text(jsonio.dumps(doc) + "\n", encoding="utf-8", newline="\n")
    return out


RUNS = REPO_ROOT / "build" / "runs"
MANIFEST = "manifest.json"
POLL_S = (15.0, 300.0)                     # wait: the first and the longest pause between two looks at the server
SUBMITTED, COLLECTED, FAILED, DISCARDED = "submitted", "collected", "failed", "discarded"


class RunRefused(RuntimeError):
    """A run is not collected or adopted: its state cannot be rebuilt as it was staged."""


class RunBusy(RuntimeError):
    """Another process collects this run now."""


@dataclass
class Run:
    """A run as its measurement needs it (prepare): rebuilt from its arguments `args` (run_args), it has
    the jobs, decks and SOA plans that were staged."""
    run_id: str
    rroot: str                                 # its run directory on the server
    args: dict
    block: Block
    test: dict
    jobs: list[Job]
    twins: dict[str, Job]                      # job -> its convergence cross-check twin
    xc: dict
    mcset: dict | None
    needs_pdk: bool
    decks: dict[str, str]
    soa_plans: dict
    remote_plans: dict[str, dict]              # job -> soa_plan.json of a job whose SOA check runs on the server

    @property
    def run_dir(self) -> Path:
        return RUNS / self.run_id


def run_args(test_id: str, block_name: str | None = None, corners: str = "typ", views: dict | None = None,
             params: dict | None = None, mode: str = "ax", parallel: int = 6, keep: bool = False,
             do_record: bool = True, mc: dict | None = None, timeout: float | None = None,
             crosscheck: bool = False) -> dict:
    """The arguments of a run (run_test's), as its manifest keeps them."""
    return {"test": test_id, "block": block_name, "corners": corners, "views": dict(views or {}),
            "params": dict(params or {}), "mode": mode, "parallel": parallel, "keep": keep,
            "do_record": do_record, "mc": mc, "timeout": timeout, "crosscheck": crosscheck}


def prepare(a: dict, run_id: str, rroot: str) -> Run:
    """The jobs, decks and SOA plans of a run with arguments `a` (run_args) in the server directory
    `rroot`: what submit stages, and what collect rebuilds the same way to measure it."""
    views = a["views"]
    block, test = find_test(a["test"], a["block"])
    cl = corner_set(a["corners"])
    needs_pdk = bool(test.get("needs_pdk")) or any(v != "behav" for v in views.values())
    mcset = mc_settings(block, a["test"], test, cl, a["mc"], a["params"])
    params = dict(a["params"])
    if mcset:
        params.update(mc_runs=mcset["runs"], mc_seed=mcset["seed"])
        if not needs_pdk:                      # no model sections: the testbench's own statistics only
            mcset["models"] = None
    jobs = build_jobs(block, a["test"], test, cl, views, params, needs_pdk)
    xc = dict(test.get("crosscheck") or {})
    if a["crosscheck"] and not xc:
        raise ValueError(f"{a['test']}: no `crosscheck:` settings in its spec")
    twins = {}
    if a["crosscheck"]:
        settings = {k: v for k, v in xc.items() if k != "samples"}
        for j in list(jobs):
            twins[j.name] = replace(j, name=j.name + XCHECK, tb_text=numerics.apply(j.tb_text, settings))
            jobs.append(twins[j.name])
    decks, soa_plans = {}, {}
    for j in jobs:
        save = []
        if test.get("soa"):                    # per-device SOA check: save the device terminal nodes
            soa_plans[j.name] = soa.plan(block.name, test, j.tb_text, view_files(views), views)
            save = soa.deck_lines(soa_plans[j.name], j.tb_text)
        decks[j.name], _ = make_deck(j, rroot, views, needs_pdk, mcset and mcset["models"], save)
    remote_plans = {}                          # the SOA check runs where the waveforms are (soa_core.py)
    if isinstance(test.get("soa"), dict) and test["soa"].get("remote"):
        for j in jobs:
            plan = soa.remote_plan(soa_plans[j.name], j.tb_text)
            if plan:
                remote_plans[j.name] = plan
    return Run(run_id, rroot, a, block, test, jobs, twins, xc, mcset, needs_pdk, decks, soa_plans, remote_plans)


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def stage_run(run: Run) -> None:
    stage(run.run_dir, run.jobs, run.decks)
    for name, plan in run.remote_plans.items():
        (run.run_dir / "stage" / "jobs" / name / "soa_plan.json").write_text(json.dumps(plan), encoding="utf-8")
    if run.remote_plans:
        shutil.copy2(Path(soa.__file__).with_name("soa_core.py"), run.run_dir / "stage" / "soa_core.py")
    mcset = run.mcset
    print(f"[adcflow] {run.args['test']} ({run.block.name}): {len(run.jobs)} job(s), views={run.args['views'] or 'behav'}, "
          f"pdk={'yes' if run.needs_pdk else 'no'}"
          + (f", Monte Carlo {mcset['runs']} samples (seed {mcset['seed']}, {mcset['variations']}"
             f"{', models ' + mcset['models'] if run.needs_pdk else ', testbench stand-in'})" if mcset else "")
          + f", staged in {_rel(run.run_dir)}")


def staged_differences(run: Run) -> list[str]:
    """What of a rebuilt run (prepare) differs from what was staged and simulated: the job
    directories (testbench, deck, the files of `prepare`, the SOA plan) and every file the circuit
    depends on (deps.run_reach) that is staged, as staged and as it is now. Empty: collect measures
    and records the simulated circuit."""
    st = run.run_dir / "stage"
    staged = sorted(p.name for p in (st / "jobs").iterdir() if p.is_dir()) if (st / "jobs").is_dir() else []
    if staged != sorted(j.name for j in run.jobs):
        return [f"jobs: staged {staged}, rebuilt {sorted(j.name for j in run.jobs)}"]
    out = []
    for j in run.jobs:
        jd = st / "jobs" / j.name
        want = {"tb.scs": j.tb_text, "deck.scs": run.decks[j.name], **j.extra}
        if j.name in run.remote_plans:
            want["soa_plan.json"] = json.dumps(run.remote_plans[j.name])
        have = {p.name for p in jd.iterdir() if p.is_file()}
        out += [f"jobs/{j.name}/{f}" for f in sorted(have ^ set(want))]
        out += [f"jobs/{j.name}/{f}" for f, text in want.items()
                if f in have and (jd / f).read_bytes() != text.encode("utf-8")]
    for f in deps.run_reach(run.test, run.args["views"]).files:
        if f.split("/")[0] not in STAGE_DIRS:      # specs/soa.yaml: through the SOA plans above
            continue
        p = st / f
        if not p.is_file() or content_hash(f, p.read_bytes()) != deps.file_hash(deps.DISK, f):
            out.append(f)
    return out


# ------------------------------------------------------------------ the manifest of a run
def manifest_path(run_id: str) -> Path:
    return RUNS / run_id / MANIFEST


def load_manifest(run_id: str) -> dict:
    p = manifest_path(run_id)
    if not p.is_file():
        raise FileNotFoundError(f"{run_id}: no {_rel(p)}; a run that a launcher of before the manifest started "
                                "is taken over with its own sim / verify command and --adopt <run_id>")
    return json.loads(p.read_text(encoding="utf-8"))


def save_manifest(man: dict) -> None:
    p = manifest_path(man["run_id"])
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(p)


def _new_manifest(run: Run, verify: dict | None, job_timeout: float, adopted: bool = False) -> dict:
    """What collect needs besides the staged run: its arguments, its server directory and jobs, the
    job limit, and the commit and tree the decks were built from (meta.git, meta.git_clean)."""
    return {"run_id": run.run_id, "state": SUBMITTED, "adopted": adopted,
            "submitted": _dt.datetime.now().isoformat(timespec="seconds"),
            "git": _git("rev-parse", "--short", "HEAD"), "git_state": git_state(), "args": run.args,
            "verify": verify, "rroot": run.rroot, "jobs": [j.name for j in run.jobs], "job_timeout": job_timeout}


@contextlib.contextmanager
def _lock(run_dir: Path):
    """One collect of a run at a time: an OS lock on <run>/collect.lock, which ends with its process."""
    f = open(run_dir / "collect.lock", "a+b")
    try:
        f.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise RunBusy(f"{run_dir.name}: another process collects it now") from None
        yield
    finally:
        f.close()


# ------------------------------------------------------------------ submit, wait, collect
def submit(a: dict, verify: dict | None = None, dry: bool = False) -> str | None:
    """Stage a run (run_args `a`), upload it and start its batch on the server (remote.launch), and
    write its manifest; returns its run id (None for a dry run, which only stages). `verify`: what
    collect needs to write the verification records (verify.verify)."""
    if not dry:                                # before hours of simulation, not at the measure afterwards
        from .spectrum import require_toolbox
        require_toolbox()
    run_id = _dt.datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{uuid.uuid4().hex[:4]}-{a['test']}"
    run = prepare(a, run_id, "<R>" if dry else f"{remote.remote_root()}/{run_id}")
    stage_run(run)
    if dry:
        return None
    mode_args = remote.cfg()["modes"][a["mode"]]
    job_timeout = a["timeout"] or float(run.test.get("timeout", remote.JOB_TIMEOUT_S))
    man = _new_manifest(run, verify, job_timeout)
    save_manifest(man)
    t0 = time.time()
    try:
        remote.upload_tree(run.run_dir / "stage", run.rroot)
        limit = remote.launch(run.rroot, man["jobs"], mode_args, a["parallel"], job_timeout,
                              soa_jobs=list(run.remote_plans))
    except BaseException:
        print(f"[adcflow] {run_id}: starting it on the server failed; `python -m adcflow collect {run_id}` "
              "tells whether it runs, `--discard` drops it")
        raise
    man.update(upload_s=round(time.time() - t0, 1), backstop_s=limit)
    save_manifest(man)
    print(f"[adcflow] {run_id}: runs on the server (each job at most {job_timeout:.0f} s, the batch {limit} s)")
    return run_id


def _staged_root(run_dir: Path, run_id: str) -> str:
    """The server run directory that the staged decks of a run include from."""
    for deck in sorted((run_dir / "stage" / "jobs").glob("*/deck.scs")):
        m = re.search(r'^include "(.+)/jobs/[^/"]+/tb\.scs"$', deck.read_text(encoding="utf-8"), re.M)
        if m and m.group(1).endswith("/" + run_id):
            return m.group(1)
    raise RunRefused(f"{run_id}: no staged deck in {_rel(run_dir / 'stage' / 'jobs')} includes its testbench "
                     f"from a server directory .../{run_id}")


def adopt(a: dict, run_id: str, verify: dict | None = None, dry: bool = False) -> str | None:
    """Take over a run that a launcher of before the manifest started (it held one ssh session for the
    whole batch) and that has no manifest: rebuild it from the same arguments `a` (run_args) in this
    tree, check it against what it staged (staged_differences) and against its directory on the server
    (the same jobs), and write its manifest, with the job limit of its own run_one.sh. It has no done
    marker: collect takes it as ended once every job has its rc.txt and nothing runs in its
    directory. Stop its old launcher first (the whole process tree), or both collect it.
    With `dry` only the rebuild is checked (nothing on the server)."""
    run_dir = RUNS / run_id
    if manifest_path(run_id).exists():
        raise RunRefused(f"{run_id} has a manifest already: python -m adcflow collect {run_id}")
    if not dry:
        from .spectrum import require_toolbox
        require_toolbox()
    run = prepare(a, run_id, _staged_root(run_dir, run_id))
    diff = staged_differences(run)
    if diff:
        raise RunRefused(f"{run_id}: not the run of these arguments in this tree; differs from what it staged: "
                         + ", ".join(diff[:10]) + (f" (+{len(diff) - 10})" if len(diff) > 10 else ""))
    print(f"[adcflow] {run_id}: rebuilt as staged, {len(run.jobs)} job(s)")
    if dry:
        return None
    st = remote.status(run.rroot)
    if not st["exists"]:
        raise RunRefused(f"{run_id}: its run directory is not on the server (collected already, or deleted)")
    names = [j.name for j in run.jobs]
    if st["jobs"] != names:
        raise RunRefused(f"{run_id}: the server's jobs.list has {st['jobs']}, the rebuilt run {names}")
    job_timeout = st["job_timeout"] or a["timeout"] or float(run.test.get("timeout", remote.JOB_TIMEOUT_S))
    man = _new_manifest(run, verify, job_timeout, adopted=True)
    save_manifest(man)
    print(f"[adcflow] {run_id}: adopted ({st['ended']} of {len(names)} job(s) ended, {st['live']} process(es) "
          f"running in it, each job at most {job_timeout:.0f} s)")
    return run_id


def _batch_state(st: dict, n_jobs: int) -> str:
    """running | ended | dead of a run directory (remote.status): ended once its done marker is
    there, or (a run adopted from a launcher that writes none) once every job has its rc.txt and
    nothing runs in it; dead when nothing runs in it and jobs are left without rc.txt."""
    if st["done"]:
        return "ended"
    if st["live"]:
        return "running"
    return "ended" if st["ended"] >= n_jobs else "dead"


def _wall(man: dict, st: dict) -> float | None:
    """meta.wall_s: the batch on the server (start to end, done marker) plus the upload; for an
    adopted run, from its jobs.list to its latest rc.txt."""
    if st["done"] and len(st["done"]) == 3:
        return round(st["done"][2] - st["done"][1] + man.get("upload_s", 0.0), 1)
    if st["start"] and st["last"]:
        return round(float(st["last"] - st["start"]), 1)
    return None


def _remove(man: dict) -> None:
    """Delete the run directory on the server (remote.remove: only fetched, with nothing running in it)."""
    if man["args"]["keep"]:
        return
    try:
        remote.remove(man["rroot"])
        man["removed"] = True
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        print(f"[adcflow] {man['run_id']}: not deleted on the server ({str(e)[-300:]}); "
              f"a later `python -m adcflow collect {man['run_id']}` tries again")
    save_manifest(man)


def collect(run_id: str, discard: bool = False, quiet: bool = False) -> dict:
    """Collect a run once its batch ended on the server: fetch its files, measure and record its
    results (or write the verification records, verify.finish), then delete its run directory
    there. Idempotent: a run that is still running is only reported; a collected one again is.

    Returns {"state", "code", ...}: running (with `ended` and `jobs`), dead (nothing runs and jobs
    never ended: nothing is recorded; `discard` drops it), missing (no run directory on the server),
    collected (`summary`: the rows as run_test returns them; `code` 1 for an error result or a
    mismatch), discarded. A batch ended by its backstop raises remote.RunTimeout and one that failed
    otherwise RuntimeError, after its files are fetched (for a look) and nothing is recorded.

    The rebuilt run must be as staged (staged_differences), else RunRefused and the run stays as it
    is. Fetch and record come before the deletion, which never touches a directory where something
    runs; a failed ssh raises remote.RemoteError and the run stays as it is, to be collected again."""
    run_dir = RUNS / run_id
    load_manifest(run_id)
    with _lock(run_dir):
        man = load_manifest(run_id)
        a = man["args"]
        if man["state"] != SUBMITTED:
            if not man.get("removed") and not a["keep"]:
                _remove(man)
            if not quiet:
                print(f"[adcflow] {run_id}: {man['state']} ({man.get('collected', '')})")
            return {"state": man["state"], "code": man.get("code", 0), "summary": None}
        st = remote.status(man["rroot"])
        n = len(man["jobs"])
        if not st["exists"]:
            print(f"[adcflow] {run_id}: its run directory is not on the server; nothing to collect"
                  + ("" if discard else f" (`python -m adcflow collect --discard {run_id}` forgets it)"))
            if discard:
                man.update(state=DISCARDED, collected=_now(), removed=True)
                save_manifest(man)
                return {"state": DISCARDED, "code": 0}
            return {"state": "missing", "code": 1}
        state = _batch_state(st, n)
        if state == "running":
            if not quiet or discard:
                print(f"[adcflow] {run_id}: running, {st['ended']} of {n} job(s) ended"
                      + (": not discarded" if discard else ""))
            return {"state": "running", "code": 0, "ended": st["ended"], "jobs": n}
        if state == "dead" and not discard:
            print(f"[adcflow] {run_id}: nothing runs in it and {n - st['ended']} of {n} job(s) never ended "
                  f"(the batch was stopped); nothing recorded. `python -m adcflow collect --discard {run_id}` drops it")
            return {"state": "dead", "code": 1}
        for note in st["notes"]:
            print(f"[adcflow] {note}")
        run = None
        if not discard:
            run = prepare(a, run_id, man["rroot"])
            diff = staged_differences(run)
            if diff:
                raise RunRefused(f"{run_id}: this tree no longer builds the run that was simulated; changed since "
                                 f"it was staged: {', '.join(diff[:10])}. Restore them and collect it again")
            if run.remote_plans and not st["done"]:      # a launcher of before launch.sh: its SOA step
                remote.soa_reduce(man["rroot"], list(run.remote_plans), a["parallel"])
        skipped = remote.fetch(man["rroot"], remote.cfg()["fetch"] + ["rc.txt"], run_dir,
                               float(remote.cfg()["fetch_max_mb"]))
        if skipped:
            print("[adcflow] skipped large files:", *skipped, sep="\n  ")
        remote.mark_fetched(man["rroot"])
        rc = st["done"][0] if st["done"] else "0"
        if discard or rc != "0":
            man.update(state=DISCARDED if discard else FAILED, collected=_now(), batch_rc=rc)
            save_manifest(man)
            _remove(man)
            if discard:
                print(f"[adcflow] {run_id}: discarded, nothing recorded (its files are in {_rel(run_dir)})")
                return {"state": DISCARDED, "code": 0}
            if rc in remote.TIMEOUT_RCS:
                raise remote.RunTimeout(f"the batch ran past its backstop on the server (jobs limited to "
                                        f"{man['job_timeout']:.0f} s each) and was killed there, nothing recorded")
            raise RuntimeError(f"the batch failed on the server (rc {rc}), nothing recorded")
        summary = _measure(run, man, st)
        code = 1 if any("error" in r["metrics"] for r in summary) else 0
        if man.get("verify"):
            from . import verify as vf
            v = man["verify"]
            code = vf.finish(a["test"], run.block.name, v["candidate"], vf.load_docs(v["docs"]), summary,
                             _wall(man, st))
        man.update(state=COLLECTED, collected=_now(), code=code)
        save_manifest(man)
        _remove(man)
        return {"state": COLLECTED, "code": code, "summary": summary}


def _now() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def wait(run_id: str) -> dict:
    """Wait until the batch of a run ends on the server, then collect it (collect's result).

    The server is asked every POLL_S (growing from the first to the second value), each time with one
    short ssh call. One that fails is reported and asked again later: a lost connection, a sleeping
    PC or an ssh timeout neither stops the batch nor deletes anything. Ctrl-C stops the waiting only."""
    pause, seen = POLL_S[0], None
    try:
        while True:
            try:
                res = collect(run_id, quiet=True)
            except RunBusy:                        # another process collects it: look again later
                res = {"state": "running", "ended": seen, "jobs": None}
            except (remote.RemoteError, subprocess.TimeoutExpired) as e:
                print(f"[adcflow] {run_id}: no answer from the server ({str(e).strip()[-300:]}); "
                      f"asking again in {pause:.0f} s", flush=True)
                res = None
            if res and res["state"] != "running":
                return res
            if res and res["ended"] != seen:
                seen = res["ended"]
                print(f"[adcflow] {run_id}: {seen} of {res['jobs']} job(s) ended", flush=True)
            time.sleep(pause)
            pause = min(pause * 1.5, POLL_S[1])
    except KeyboardInterrupt:
        print(f"\n[adcflow] stopped waiting; {run_id} goes on on the server: python -m adcflow collect {run_id}")
        raise


def pending() -> list[str]:
    """Runs with a manifest that collect has more to do for: not collected yet, or not yet deleted on the server."""
    out = []
    for p in sorted(RUNS.glob(f"*/{MANIFEST}")):
        m = json.loads(p.read_text(encoding="utf-8"))
        if m["state"] == SUBMITTED or not (m.get("removed") or m["args"]["keep"]):
            out.append(m["run_id"])
    return out


def _measure(run: Run, man: dict, st: dict) -> list[dict]:
    """Measure the fetched jobs of a run and record their results (run_args do_record); the rows of run_test."""
    from .figures import FigureSink          # matplotlib: only where figures are drawn, not for deps / checks
    from .spectrum import require_toolbox
    require_toolbox()
    a, block, test, mcset = run.args, run.block, run.test, run.mcset
    test_id, run_dir, rroot, do_record = a["test"], run.run_dir, run.rroot, a["do_record"]
    jobs, twins, xc, soa_plans = run.jobs, run.twins, run.xc, run.soa_plans
    meta_base = {
        "date": _now(),
        "git": man["git"],                     # the commit and tree the decks were built from
        **man["git_state"],
        "mode": a["mode"], "pdk": run.needs_pdk, "mc": mcset, "wall_s": _wall(man, st),
    }
    summary = []
    viewsig = _viewsig(block, a["views"])
    done = {}
    for j in jobs:
        jd = run_dir / "jobs" / j.name
        rc = (jd / "rc.txt").read_text().split() if (jd / "rc.txt").exists() else ["?", "?"]
        errs = _spectre_errors(jd / "spectre.log")
        meta = {**meta_base, "rc": rc[0], "sim_s": rc[1] if len(rc) > 1 else None,
                "numerics": numerics.effective(jd)}
        # evidence figures go next to the result JSON (or into the run directory without --record
        # and for a cross-check twin, which is never recorded)
        twin = j.name.endswith(XCHECK)
        figs = FigureSink(result_dir(block, test_id, viewsig) if do_record and not twin else run_dir / "figs",
                          j.name, header=f"{test_id} | {viewsig} | {j.name}")
        figs.clear()
        ctx = {"corner": j.corner, "params": j.params, "globals": j.globals_, "test": test_id,
               "block": block.name, "view": viewsig, "figs": figs, "soa": soa_plans.get(j.name),
               "mc": mcset}
        try:
            with archmod.track() as measure_keys:
                # a Monte Carlo job is always measured: the samples before an abort are kept and
                # the others count as failed (the run's error is recorded as well)
                metrics = measure(test, jd, ctx) if rc[0] == "0" or mcset else {}
            if rc[0] != "0":
                metrics["error"] = job_error(rc[0], errs, man["job_timeout"])
            if "error" in metrics:                 # never record server (or local) paths
                metrics["error"] = str(metrics["error"]).replace(rroot, "<run>").replace(str(run_dir), "<run>")
        except Exception as e:  # keep going, record the failure
            traceback.print_exc()
            metrics = {"error": f"measure failed: {e}"}
        # what the simulated circuit depends on (deps.py): the files the testbench reaches and the
        # arch values read by `prepare` and the measure. The block spec is not hashed: limits are
        # re-judged at check time and the test parameters are recorded with the result.
        meta.update(deps.record_meta(test, a["views"], j.arch_keys | measure_keys))
        if ctx.get("provenance"):                  # estimators the measure used (e.g. adcflow.spectrum)
            meta["provenance"] = ctx["provenance"]
        done[j.name] = (j, metrics, meta, figs.entries)
    for name, (j, metrics, meta, entries) in done.items():
        if name.endswith(XCHECK):
            continue
        if name in twins:
            meta["crosscheck"] = _crosscheck(block, test_id, xc, run_dir / "jobs", metrics, done[name + XCHECK])
        out = record(block, test_id, viewsig, j, metrics, meta, entries) if do_record else None
        summary.append({"job": name, "corner": j.corner.name, "rc": meta["rc"], "metrics": metrics, "out": out,
                        "params": j.params, "globals": j.globals_, "meta": meta})
        if name in twins:
            t, tm, tmeta, _ = done[name + XCHECK]
            summary.append({"job": t.name, "corner": t.corner.name, "rc": tmeta["rc"], "metrics": tm, "out": None,
                            "params": t.params, "globals": t.globals_, "meta": tmeta})
    _print_summary(block, test_id, summary, mcset)
    for name in twins:
        _print_crosscheck(name, done[name][2]["crosscheck"])
    return summary


def run_test(test_id: str, block_name: str | None = None, corners: str = "typ",
             views: dict | None = None, params: dict | None = None, mode: str = "ax",
             parallel: int = 6, keep: bool = False, do_record: bool = True, dry: bool = False,
             mc: dict | None = None, timeout: float | None = None, crosscheck: bool = False,
             detach: bool = False, adopt_id: str | None = None) -> list[dict]:
    """Run a test at the corners of `corners`; with `crosscheck` every job runs a second time
    with the test's `crosscheck:` settings (numerics.py) and only the first is recorded, with the
    differences in its meta.crosscheck. A test with `montecarlo:` runs its samples (mc_settings;
    `mc` overrides its runs and seed). Each job runs at most `timeout` s (default: the test's
    `timeout:`, else remote.JOB_TIMEOUT_S); a job ended by it fails, the others are measured as
    usual. Returns one row per job: job, corner, rc, metrics, out (the
    recorded file, None without recording), params, globals and meta (as a result records them).

    The batch runs on the server by itself (submit); this waits for it and collects it (wait,
    collect). With `detach` it returns [] once the batch is started (`adcflow collect` later);
    `adopt_id` takes over a run that a launcher of before the manifest started (adopt)."""
    a = run_args(test_id, block_name, corners, views, params, mode, parallel, keep, do_record, mc, timeout, crosscheck)
    run_id = adopt(a, adopt_id, dry=dry) if adopt_id else submit(a, dry=dry)
    if run_id is None:
        return []
    if detach:
        print(f"[adcflow] {run_id}: `python -m adcflow collect {run_id}` records it once it ended")
        return []
    res = wait(run_id)
    if res["state"] != COLLECTED:
        raise RuntimeError(f"{run_id}: {res['state']}, nothing recorded")
    return res["summary"] or []


XCHECK = "__xcheck"


def _crosscheck(block: Block, test_id: str, xc: dict, jobs_dir: Path, metrics: dict, twin: tuple) -> dict:
    """meta.crosscheck of a job: the twin's settings (as asked and as used) and the differences
    of the spec metrics and raw samples from the job (numerics.compare)."""
    t, tm, tmeta, _ = twin
    names = list(dict.fromkeys(s.metric for s in block.specs if s.test == test_id))
    f = xc.get("samples")
    out = {"settings": {k: v for k, v in xc.items() if k != "samples"}, "numerics": tmeta.get("numerics"),
           "rc": tmeta["rc"], "sim_s": tmeta["sim_s"]}
    if "error" in tm or "error" in metrics:
        return {**out, "error": tm.get("error") or metrics.get("error")}
    ref = jobs_dir / t.name.removesuffix(XCHECK)
    return {**out, **numerics.compare(metrics, tm, names, ref / f if f else None, jobs_dir / t.name / f if f else None)}


def _print_crosscheck(name: str, xc: dict) -> None:
    if "error" in xc:
        print(f"  crosscheck {name}: ERROR {str(xc['error'])[:200]}")
        return
    parts = [f"d{k}={v['diff']:+.4g}" for k, v in xc["metrics"].items() if v["diff"] is not None]
    s = xc.get("samples") or {}
    if "diff_rms_uV" in s:
        parts.append(f"samples {s['n']}: rms {s['diff_rms_uV']:.4g} uV, max {s['diff_max_uV']:.4g} uV, "
                     f"time diff max {s['time_diff_max_ps']:.3g} ps")
    if "soa" in xc:
        parts.append(f"SOA peaks of {xc['soa']['pairs']} pairs: max change {xc['soa']['max_V_diff_max_mV']:.3g} mV "
                     f"({xc['soa']['at']}), violations {xc['soa']['violations']}")
    print(f"  crosscheck {name} ({', '.join(f'{k}={v}' for k, v in xc['settings'].items())}): " + "  ".join(parts))


def _print_summary(block: Block, test_id: str, summary: list[dict], mc: dict | None = None) -> None:
    def fmt(v) -> str:
        return "-" if v is None else (f"{v:.4g}" if isinstance(v, (int, float)) else str(v))

    for row in summary:
        m = row["metrics"]
        if "error" in m:
            print(f"  {row['job']:28s} ERROR {m['error'][:200]}")
            continue
        judged, na = block.verdicts(test_id, row["corner"], mc, m)
        parts = [f"{sid}={fmt(v['value'])}"
                 + ("(reported)" if v["pass"] is None else "" if v["pass"] else f"(FAIL {v['limit']})")
                 + (f"[{v['samples']['ok']}/{v['samples']['need']} samples, {v['samples']['failed']} failed]"
                    if v.get("samples") else "")
                 for sid, v in judged.items()]
        parts += [f"{sid}={fmt(v['value'])}(n/a: {v['corners']} only)" for sid, v in na.items()]
        print(f"  {row['job']:28s} " + "  ".join(parts))


def _same(a, b) -> bool:
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-9 * max(abs(a), abs(b))
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def _by_rows(metrics: dict) -> dict:
    return {**metrics, "soa_table": soa.table_rows(metrics)} if "soa_table" in metrics else metrics


def remeasure(test_id: str, run_dir: Path, block_name: str | None = None, views: dict | None = None,
              allow: tuple[str, ...] = ("sfdr",), dry: bool = False, redraw: bool = False) -> list[dict]:
    """Measure the fetched jobs of an earlier run again with the current measure code and
    re-record their results, without simulating (issue #36: a fixed SFDR estimator).

    It only replaces a measurement of the same simulation: each job must have a recorded result,
    and every metric whose name contains none of `allow` must come out exactly as recorded, else
    nothing of that job is written. The simulation meta (date, git, files, rc ...) is kept;
    meta.remeasured gives the date, commit and run of the new measurement and old -> new of
    every metric that changed; meta.provenance names the estimators used now. When the arch
    values the result read (meta.arch) are those of now, the keys the new measurement reads are
    added to them.

    With `redraw` only the figures may change (issue #47: the spectrum plot window): every metric
    must come out as recorded, and meta.redrawn gives the date, commit and run of the redraw."""
    from .figures import FigureSink          # matplotlib: only where figures are drawn
    from .spectrum import require_toolbox
    if not dry:
        require_toolbox()
    views = views or {}
    if redraw:
        allow = ()
    block, test = find_test(test_id, block_name)
    viewsig = _viewsig(block, views)
    rdir = result_dir(block, test_id, viewsig)
    run_dir = Path(run_dir)
    out = []
    for jd in sorted(p for p in (run_dir / "jobs").iterdir() if p.is_dir() and not p.name.endswith(XCHECK)):
        path = rdir / f"{jd.name}.json"
        if not path.exists():
            raise FileNotFoundError(f"{jd.name}: no recorded result {path.relative_to(REPO_ROOT)}")
        old = json.loads(path.read_text(encoding="utf-8"))
        job = Job(jd.name, by_name(old["corner"]), old["params"], old["globals"])
        tmp = run_dir / "remeasure_figs"
        figs = FigureSink(tmp, jd.name, header=f"{test_id} | {viewsig} | {jd.name}")
        figs.clear()
        tb_text = (run_dir / "stage" / "jobs" / jd.name / "tb.scs").read_text(encoding="utf-8")
        ctx = {"corner": job.corner, "params": job.params, "globals": job.globals_, "test": test_id,
               "block": block.name, "view": viewsig, "figs": figs, "mc": old["meta"].get("mc"),
               "soa": soa.plan(block.name, test, tb_text, view_files(views), views) if test.get("soa") else None}
        with archmod.track() as measure_keys:
            metrics = measure(test, jd, ctx)
        was = _by_rows(old["metrics"])                # a soa_table recorded in either form compares by its pairs
        now = _by_rows(metrics)
        changed = {k: [was.get(k), v] for k, v in now.items() if not _same(was.get(k), v)}
        changed.update({k: [v, None] for k, v in was.items() if k not in now})
        bad = sorted(k for k in changed if not any(a in k for a in allow))
        if bad:
            raise ValueError(f"{jd.name}: {bad} differ from the recorded result: not the same simulation data "
                             f"(or the measure changed beyond {allow}): {[changed[k] for k in bad][:3]}")
        meta = dict(old["meta"])
        stamp = {"date": _dt.datetime.now().isoformat(timespec="seconds"),
                 "git": _git("rev-parse", "--short", "HEAD"), **git_state(), "run": run_dir.name}
        if redraw:
            meta["redrawn"] = stamp                  # figures only; metrics checked unchanged above
        else:
            meta["remeasured"] = {**stamp, "changed": changed}
        if "arch" in meta and not deps.arch_changed(meta["arch"]):
            # the values it read are those of now: add what the new measurement read
            keys = archmod.minimal(set(meta["arch"]["keys"]) | measure_keys)
            meta["arch"] = {"keys": keys, "sha": archmod.values_sha(archmod.load_data(), keys)}
        if ctx.get("provenance"):
            meta["provenance"] = ctx["provenance"]
        out.append({"job": jd.name, "changed": changed})
        print(f"  {jd.name:28s} " + ("  ".join(f"{k}: {a:.4g} -> {b:.4g}" for k, (a, b) in changed.items()
                                               if isinstance(a, float) and isinstance(b, float)) or "unchanged"))
        if dry:
            continue
        FigureSink(rdir, jd.name).clear()
        for e in figs.entries:
            shutil.copyfile(tmp / e["file"], rdir / e["file"])
        doc = result_doc(block, test_id, viewsig, job, old["metrics"] if redraw else metrics, meta, figs.entries)
        path.write_text(jsonio.dumps(doc) + "\n", encoding="utf-8", newline="\n")
    return out


def run_test_cli(a) -> int:
    views = dict(v.split("=", 1) for v in a.view)
    params = {}
    for p in a.param:
        k, v = p.split("=", 1)
        params[k] = v
    mc = {"runs": a.mc_runs, "seed": a.mc_seed} if a.mc_runs is not None or a.mc_seed is not None else None
    args = run_args(a.test, a.block, a.corners, views, params, a.mode, a.jobs, a.keep, not a.no_record, mc,
                    crosscheck=a.crosscheck)
    run_id = adopt(args, a.adopt, dry=a.dry_run) if a.adopt else submit(args, dry=a.dry_run)
    if run_id is None:
        return 0
    if a.detach:
        print(f"[adcflow] {run_id}: `python -m adcflow collect {run_id}` records it once it ended")
        return 0
    res = wait(run_id)
    return res["code"] if res["state"] == COLLECTED else 1


def collect_cli(a) -> int:
    """`adcflow collect`: each run once (or, with --wait, once it ended); 1 when one failed, was
    refused, or has an error result or a mismatch. A run still running is reported, not an error."""
    ids = list(dict.fromkeys([*a.run_id, *(pending() if a.all else [])]))
    if not ids:
        print("[adcflow] collect: no run waits to be collected")
        return 0
    rc = 0
    for run_id in ids:
        try:
            res = wait(run_id) if a.wait else collect(run_id, discard=a.discard)
        except (FileNotFoundError, RunRefused, RunBusy, remote.RunTimeout, remote.RemoteError,
                subprocess.TimeoutExpired, RuntimeError) as e:
            print(f"[adcflow] {run_id}: {e}")
            rc = 1
            continue
        if res["state"] != "running" and (res.get("code") or res["state"] in (FAILED, "dead", "missing")):
            rc = 1
    return rc
