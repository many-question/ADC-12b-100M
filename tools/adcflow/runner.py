"""Build run decks for a block test, run them on the server, measure, record.

Deck layout (all paths absolute on the server):

    simulator lang=spectre
    parameters vdd=... vdd18=... tempc=... noise_en=... beh_speed=... vref_in=...
    adcflow_opts options temp=<T> tnom=27
    include <PDK sections>                 (when a transistor view or the test needs it)
    ahdl_include <Verilog-A of the behavioral views and the testbench>
    include <one view of every block>      (behav unless --view block=xtor)
    include design/top/adc_top.scs
    include jobs/<job>/tb.scs              (the testbench with its parameters substituted)
    save <device terminal nodes>           (tests with `soa:` in their spec, see soa.py)

Global parameters are declared by the deck only; testbenches and views use
them (`vdd`, `vdd18`, `tempc`, `noise_en`, `beh_speed`, `vref_in`).
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import importlib
import json
import shutil
import subprocess
import time
import traceback
import uuid
from dataclasses import dataclass, field, replace
from pathlib import Path

import yaml

from . import REPO_ROOT
from . import numerics, remote, soa
from .corners import Corner, corner_set, model_includes, vref_in
from .figures import FigureSink
from .netlist import content_hash, parse, substitute_parameters
from .specs import Block, blocks, find_test

STAGE_DIRS = ("design", "tb")
STAGE_EXT = {".scs", ".va", ".vams"}
VA_YAML = REPO_ROOT / "specs" / "va_modules.yaml"
GLOBAL_PARAMS = ("vdd", "vdd18", "tempc", "noise_en", "devnoise", "beh_speed", "vref_in")


@dataclass
class Job:
    name: str
    corner: Corner
    params: dict
    globals_: dict
    tb_text: str = ""
    files: list[str] = field(default_factory=list)   # repo-relative files used (for hashes)
    extra: dict[str, str] = field(default_factory=dict)  # job-local input files written by `prepare`


def _va_modules() -> dict:
    with open(VA_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)["modules"]


def _sha(path: Path) -> str:
    return content_hash(path)


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception:
        return ""


def dirty_paths(porcelain: str) -> list[str]:
    """Paths that ``git status --porcelain`` lists (modified, staged or untracked) outside results/.

    results/ does not count: a suite run rewrites results while it runs. Ignored files
    (site.local.yaml) are not listed by git at all. A rename counts by its new path.
    """
    out = []
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].split(" -> ")[-1].strip('"')
        if path == "results" or path.startswith("results/"):
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
        p = b.view_path(v)
        if not p.exists():
            raise FileNotFoundError(f"{b.name}: view {v!r} file {p.relative_to(REPO_ROOT)} does not exist")
        out.append(p)
    out.append(REPO_ROOT / "design" / "top" / "adc_top.scs")
    return out


def _needed_va(netlists: list[Path], tb_text: str) -> list[Path]:
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
    if block.name == "adc_top":
        x = sorted(b for b, v in views.items() if v != "behav")
        if not x:
            return "behav"
        if len(x) == len(blocks()) - 1:
            return "xtor"
        return "xtor-" + "+".join(s.replace("adc_", "") for s in x)
    return views.get(block.name, "behav")


def build_jobs(block: Block, test_id: str, test: dict, corners: list[Corner], views: dict,
               cli_params: dict, needs_pdk: bool = False) -> list[Job]:
    tb_path = REPO_ROOT / test["netlist"]
    tb_text = tb_path.read_text(encoding="utf-8")
    variants = test.get("variants") or [{}]
    jobs = []
    for c in corners:
        for var in variants:
            params = {**(test.get("params") or {}), **var, **cli_params}
            if test.get("prepare"):
                mod, fn = test["prepare"].split(":")
                params = getattr(importlib.import_module(mod), fn)(dict(params))
            extra = params.pop("_files", {})
            g = {"vdd": c.vdd, "vdd18": c.vdd18, "tempc": c.temp,
                 "noise_en": 1 if test.get("tran_noise") else 0, "devnoise": 1 if needs_pdk else 0,
                 "beh_speed": 1.0, "vref_in": vref_in()}
            for k in list(params):
                if k in GLOBAL_PARAMS:
                    g[k] = params.pop(k)
            text, done = substitute_parameters(tb_text, {k: v for k, v in params.items()})
            missing = set(params) - done
            if missing:
                raise ValueError(f"{test['netlist']}: parameters not declared in the testbench: {sorted(missing)}")
            vname = "_".join(f"{k}{v}" for k, v in var.items())
            name = c.name + (f"__{vname}" if vname else "")
            jobs.append(Job(name=name, corner=c, params=params, globals_=g, tb_text=text, extra=extra))
    return jobs


def make_deck(job: Job, rroot: str, views: dict, needs_pdk: bool, mc: str | None,
              extra: list[str] | None = None) -> tuple[str, list[Path]]:
    """The run deck of a job; `extra` lines (the saves of the SOA check) come after the testbench."""
    vfiles = view_files(views)
    va = _needed_va(vfiles, job.tb_text)
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
    # testbench Verilog-A includes the architecture constants
    for vams in (REPO_ROOT / "design" / "behav" / "veriloga").glob("adc_arch*.vams"):
        shutil.copyfile(vams, st / "tb" / "common" / "veriloga" / vams.name)
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
    out.write_text(json.dumps(doc, indent=1, default=float) + "\n", encoding="utf-8", newline="\n")
    return out


def run_test(test_id: str, block_name: str | None = None, corners: str = "typ",
             views: dict | None = None, params: dict | None = None, mode: str = "ax",
             parallel: int = 6, keep: bool = False, do_record: bool = True, dry: bool = False,
             mc: str | None = None, timeout: float | None = None, crosscheck: bool = False) -> list[dict]:
    """Run a test at the corners of `corners`; with `crosscheck` every job runs a second time
    with the test's `crosscheck:` settings (numerics.py) and only the first is recorded, with the
    differences in its meta.crosscheck."""
    views = views or {}
    block, test = find_test(test_id, block_name)
    cl = corner_set(corners)
    needs_pdk = bool(test.get("needs_pdk")) or any(v != "behav" for v in views.values())
    jobs = build_jobs(block, test_id, test, cl, views, params or {}, needs_pdk)
    xc = dict(test.get("crosscheck") or {})
    if crosscheck and not xc:
        raise ValueError(f"{test_id}: no `crosscheck:` settings in its spec")
    twins = {}                                 # job -> its convergence cross-check twin
    if crosscheck:
        settings = {k: v for k, v in xc.items() if k != "samples"}
        for j in list(jobs):
            twins[j.name] = replace(j, name=j.name + XCHECK, tb_text=numerics.apply(j.tb_text, settings))
            jobs.append(twins[j.name])
    run_id = _dt.datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{uuid.uuid4().hex[:4]}-{test_id}"
    run_dir = REPO_ROOT / "build" / "runs" / run_id
    rroot = "<R>" if dry else f"{remote.remote_root()}/{run_id}"
    decks, used, soa_plans = {}, {}, {}
    for j in jobs:
        save = []
        if test.get("soa"):                    # per-device SOA check: save the device terminal nodes
            soa_plans[j.name] = soa.plan(block.name, test, j.tb_text, view_files(views), views)
            save = soa.deck_lines(soa_plans[j.name], j.tb_text)
        decks[j.name], files = make_deck(j, rroot, views, needs_pdk, mc, save)
        used[j.name] = files + ([soa.SOA_YAML] if test.get("soa") else [])
    stage(run_dir, jobs, decks)
    print(f"[adcflow] {test_id} ({block.name}): {len(jobs)} job(s), views={views or 'behav'}, "
          f"pdk={'yes' if needs_pdk else 'no'}, staged in {run_dir.relative_to(REPO_ROOT)}")
    if dry:
        return []
    mode_args = remote.cfg()["modes"][mode]
    t0 = time.time()
    try:
        remote.upload_tree(run_dir / "stage", rroot)
        remote.run_jobs(rroot, [j.name for j in jobs], mode_args, parallel,
                        timeout=timeout or float(test.get("timeout", 4 * 3600)))
        skipped = remote.fetch(rroot, remote.cfg()["fetch"] + ["rc.txt"], run_dir,
                               float(remote.cfg()["fetch_max_mb"]))
        if skipped:
            print("[adcflow] skipped large files:", *skipped, sep="\n  ")
    finally:
        if not keep:
            remote.remove(rroot)
    wall = time.time() - t0
    meta_base = {
        "date": _dt.datetime.now().isoformat(timespec="seconds"),
        "git": _git("rev-parse", "--short", "HEAD"),
        **git_state(),
        "mode": mode, "pdk": needs_pdk, "mc": mc, "wall_s": round(wall, 1),
    }
    summary = []
    viewsig = _viewsig(block, views)
    done = {}
    for j in jobs:
        jd = run_dir / "jobs" / j.name
        rc = (jd / "rc.txt").read_text().split() if (jd / "rc.txt").exists() else ["?", "?"]
        errs = _spectre_errors(jd / "spectre.log")
        # what the simulation depends on: views, Verilog-A, testbench, architecture.
        # The block spec is not hashed: limits are re-judged at check time and the
        # test parameters are recorded with the result.
        files = [p for p in used[j.name]] + [REPO_ROOT / test["netlist"], REPO_ROOT / "specs" / "arch.yaml"]
        meta = {**meta_base, "rc": rc[0], "sim_s": rc[1] if len(rc) > 1 else None,
                "numerics": numerics.effective(jd),
                "files": {p.relative_to(REPO_ROOT).as_posix(): _sha(p) for p in files}}
        # evidence figures go next to the result JSON (or into the run directory without --record
        # and for a cross-check twin, which is never recorded)
        twin = j.name.endswith(XCHECK)
        figs = FigureSink(result_dir(block, test_id, viewsig) if do_record and not twin else run_dir / "figs",
                          j.name, header=f"{test_id} | {viewsig} | {j.name}")
        figs.clear()
        ctx = {"corner": j.corner, "params": j.params, "globals": j.globals_, "test": test_id,
               "block": block.name, "view": viewsig, "figs": figs, "soa": soa_plans.get(j.name)}
        try:
            metrics = measure(test, jd, ctx) if rc[0] == "0" else {}
            if rc[0] != "0":
                metrics = {"error": "; ".join(errs) or f"spectre rc={rc[0]}"}
            if "error" in metrics:                 # never record server paths
                metrics["error"] = str(metrics["error"]).replace(rroot, "<run>")
        except Exception as e:  # keep going, record the failure
            traceback.print_exc()
            metrics = {"error": f"measure failed: {e}"}
        done[j.name] = (j, metrics, meta, figs.entries)
    for name, (j, metrics, meta, entries) in done.items():
        if name.endswith(XCHECK):
            continue
        if name in twins:
            meta["crosscheck"] = _crosscheck(block, test_id, xc, run_dir / "jobs", metrics, done[name + XCHECK])
        out = record(block, test_id, viewsig, j, metrics, meta, entries) if do_record else None
        summary.append({"job": name, "corner": j.corner.name, "rc": meta["rc"], "metrics": metrics, "out": out})
        if name in twins:
            t, tm, tmeta, _ = done[name + XCHECK]
            summary.append({"job": t.name, "corner": t.corner.name, "rc": tmeta["rc"], "metrics": tm, "out": None})
    _print_summary(block, test_id, summary, mc)
    for name in twins:
        _print_crosscheck(name, done[name][2]["crosscheck"])
    return summary


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
    print(f"  crosscheck {name} ({', '.join(f'{k}={v}' for k, v in xc['settings'].items())}): " + "  ".join(parts))


def _print_summary(block: Block, test_id: str, summary: list[dict], mc: str | None = None) -> None:
    def fmt(v) -> str:
        return "-" if v is None else (f"{v:.4g}" if isinstance(v, (int, float)) else str(v))

    for row in summary:
        m = row["metrics"]
        if "error" in m:
            print(f"  {row['job']:28s} ERROR {m['error'][:200]}")
            continue
        judged, na = block.verdicts(test_id, row["corner"], mc, m)
        parts = [f"{sid}={fmt(v['value'])}{'' if v['pass'] else '(FAIL ' + v['limit'] + ')'}"
                 for sid, v in judged.items()]
        parts += [f"{sid}={fmt(v['value'])}(n/a: {v['corners']} only)" for sid, v in na.items()]
        print(f"  {row['job']:28s} " + "  ".join(parts))


def run_test_cli(a) -> int:
    views = dict(v.split("=", 1) for v in a.view)
    params = {}
    for p in a.param:
        k, v = p.split("=", 1)
        params[k] = v
    summary = run_test(a.test, a.block, a.corners, views, params, a.mode, a.jobs, a.keep,
                       not a.no_record, a.dry_run, crosscheck=a.crosscheck)
    bad = [r for r in summary if "error" in r["metrics"]]
    return 1 if bad else 0
