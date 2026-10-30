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
"""

from __future__ import annotations

import datetime as _dt
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
from . import arch as archmod
from . import candidates, deps, numerics, remote, soa
from .corners import Corner, by_name, corner_set, model_includes, vref_in
from .figures import FigureSink
from .netlist import parse, substitute_parameters
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
             mc: dict | None = None, timeout: float | None = None, crosscheck: bool = False) -> list[dict]:
    """Run a test at the corners of `corners`; with `crosscheck` every job runs a second time
    with the test's `crosscheck:` settings (numerics.py) and only the first is recorded, with the
    differences in its meta.crosscheck. A test with `montecarlo:` runs its samples (mc_settings;
    `mc` overrides its runs and seed). Returns one row per job: job, corner, rc, metrics, out (the
    recorded file, None without recording), params, globals and meta (as a result records them)."""
    views = views or {}
    block, test = find_test(test_id, block_name)
    cl = corner_set(corners)
    needs_pdk = bool(test.get("needs_pdk")) or any(v != "behav" for v in views.values())
    mcset = mc_settings(block, test_id, test, cl, mc, params)
    params = dict(params or {})
    if mcset:
        params.update(mc_runs=mcset["runs"], mc_seed=mcset["seed"])
        if not needs_pdk:                      # no model sections: the testbench's own statistics only
            mcset["models"] = None
    jobs = build_jobs(block, test_id, test, cl, views, params, needs_pdk)
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
    decks, soa_plans = {}, {}
    for j in jobs:
        save = []
        if test.get("soa"):                    # per-device SOA check: save the device terminal nodes
            soa_plans[j.name] = soa.plan(block.name, test, j.tb_text, view_files(views), views)
            save = soa.deck_lines(soa_plans[j.name], j.tb_text)
        decks[j.name], _ = make_deck(j, rroot, views, needs_pdk, mcset and mcset["models"], save)
    stage(run_dir, jobs, decks)
    print(f"[adcflow] {test_id} ({block.name}): {len(jobs)} job(s), views={views or 'behav'}, "
          f"pdk={'yes' if needs_pdk else 'no'}"
          + (f", Monte Carlo {mcset['runs']} samples (seed {mcset['seed']}, {mcset['variations']}"
             f"{', models ' + mcset['models'] if needs_pdk else ', testbench stand-in'})" if mcset else "")
          + f", staged in {run_dir.relative_to(REPO_ROOT)}")
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
        "mode": mode, "pdk": needs_pdk, "mc": mcset, "wall_s": round(wall, 1),
    }
    summary = []
    viewsig = _viewsig(block, views)
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
                metrics["error"] = "; ".join(errs) or f"spectre rc={rc[0]}"
            if "error" in metrics:                 # never record server (or local) paths
                metrics["error"] = str(metrics["error"]).replace(rroot, "<run>").replace(str(run_dir), "<run>")
        except Exception as e:  # keep going, record the failure
            traceback.print_exc()
            metrics = {"error": f"measure failed: {e}"}
        # what the simulated circuit depends on (deps.py): the files the testbench reaches and the
        # arch values read by `prepare` and the measure. The block spec is not hashed: limits are
        # re-judged at check time and the test parameters are recorded with the result.
        meta.update(deps.record_meta(test, views, j.arch_keys | measure_keys))
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
        changed = {k: [old["metrics"].get(k), v] for k, v in metrics.items() if not _same(old["metrics"].get(k), v)}
        changed.update({k: [v, None] for k, v in old["metrics"].items() if k not in metrics})
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
        path.write_text(json.dumps(doc, indent=1, default=float) + "\n", encoding="utf-8", newline="\n")
    return out


def run_test_cli(a) -> int:
    views = dict(v.split("=", 1) for v in a.view)
    params = {}
    for p in a.param:
        k, v = p.split("=", 1)
        params[k] = v
    mc = {"runs": a.mc_runs, "seed": a.mc_seed} if a.mc_runs is not None or a.mc_seed is not None else None
    summary = run_test(a.test, a.block, a.corners, views, params, a.mode, a.jobs, a.keep,
                       not a.no_record, a.dry_run, mc=mc, crosscheck=a.crosscheck)
    bad = [r for r in summary if "error" in r["metrics"]]
    return 1 if bad else 0
