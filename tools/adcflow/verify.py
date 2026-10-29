"""The project lead's rerun of a candidate's results: ``python -m adcflow verify`` (docs/verification.md §7).

A candidate's results are self-reported: its authors simulate with their own PDK and Spectre and
commit the result JSONs in their own PR. Selection needs results that the lead reran on the same
netlist (CONTRIBUTING §4 step 5, §10). The verification of a result is a record in a place that only
lead PRs change, never inside the candidate's paths (a candidate PR could forge anything there)::

    verification/<block>/<candidate>/<test>/<job>.json      (<job>: the result's file name)

A record is shaped like a result (block, test, view, corner, params, globals, metrics, specs, meta:
git, date, numerics and the dependency records meta.files / meta.arch / meta.views of deps.py), so
checks.judge judges its freshness as it judges a result's. It adds the candidate result it verifies
(`verifies`: path, netlist and netlist hash, the result's date and commit), the comparison with
the self-reported values (`comparison`, TOLERANCES) and `status`: match | mismatch.

`verify` refuses before simulating when a result to verify is missing, stale, an error, a Monte
Carlo run, or recorded on another netlist than the candidate's netlist now. It reruns with
``--view <block>=xtor:<name>`` and writes one record per result, a mismatch included (status
mismatch, exit code 1).

The leaderboard (candidates.score, the site) never trusts a result's own meta: `state` counts a
result as verified only when its record exists, verifies the netlist hash the result records (and
the netlist has now), is fresh under checks.judge, and compares within the tolerances now.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

from . import candidates as cand

TOL_DOC = "docs/verification.md §7"

# metric name pattern -> (relative, absolute) tolerance; the first match decides. A float value
# compares within max(absolute, relative * |self-reported|); integers, booleans and strings exactly.
TOLERANCES: list[tuple[str, float, float]] = [
    (r"^enob", 0.0, 0.05),                       # bit (the ranking tolerance of the top-level ENOB)
    (r"_dBc?$", 0.0, 0.5),                       # dB, dBc
    (r"^jitter_fs$", 0.10, 0.0),                 # transient-noise statistic (200 edges)
    (r"noise.*_uV$", 0.08, 0.0),                 # noise statistics / noise integrals
    (r"_fs$", 0.02, 1.0),
    (r"_ps$", 0.02, 1.0),
    (r"_ns$", 0.02, 0.001),                      # 1 ps
    (r"_us$", 0.02, 0.001),                      # 1 ns
    (r"_V$", 0.01, 0.001),                       # 1 mV
    (r"_mV(_per_V)?$", 0.02, 0.5),
    (r"_uV$", 0.05, 5.0),
    (r"_uA$", 0.02, 0.1),
    (r"_mA$", 0.02, 0.0001),
    (r"_uW$", 0.02, 0.1),
    (r"_mW$", 0.02, 0.0001),
    (r"_fJ$", 0.02, 0.5),
    (r"_fF$", 0.02, 0.1),
    (r"_pF$", 0.02, 0.0001),
    (r"_pC$", 0.02, 0.0001),
    (r"_(lsb|LSB)$", 0.05, 0.05),
    (r"_pct$", 0.02, 0.1),
]
DEFAULT_TOL = (0.02, 0.0)                        # any other number: 2 %
# simulator time-step statistics (they follow the simulator's step control, not the circuit)
NOT_COMPARED = {"soa_points", "soa_dt_max_ps"}


def tolerance(metric: str) -> tuple[float, float]:
    for pat, rel, ab in TOLERANCES:
        if re.search(pat, metric):
            return rel, ab
    return DEFAULT_TOL


def record_path(block: str, name: str, test: str, job: str) -> Path:
    return cand.ROOT / "verification" / block / name / test / f"{job}.json"


def netlist_rel(block: str, name: str) -> str:
    return f"design/xtor/{block}/{name}/{block}.scs"


def _norm(v):
    return json.loads(json.dumps(v, default=float))


def _scalar(v) -> bool:
    return v is None or isinstance(v, (bool, int, float, str))


# ------------------------------------------------------------------ comparison
def compare_metrics(self_m: dict, rerun: dict) -> tuple[dict, list[str], list[str]]:
    """(per metric {self, rerun, diff, tol, ok}, problems, not compared) of two metric sets."""
    out, problems, skipped = {}, [], []
    for k in sorted(set(self_m) | set(rerun)):
        a, b = self_m.get(k), rerun.get(k)
        if k in NOT_COMPARED or not (_scalar(a) and _scalar(b)):
            skipped.append(k)
            continue
        if k not in self_m or k not in rerun:
            out[k] = {"self": a, "rerun": b, "ok": False}
            problems.append(f"{k}: {'not self-reported' if k not in self_m else 'not in the rerun'}")
            continue
        num = isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) \
            and not isinstance(b, bool)
        if num and (isinstance(a, float) or isinstance(b, float)):
            rel, ab = tolerance(k)
            tol = max(ab, rel * abs(a))
            ok = abs(b - a) <= tol * (1 + 1e-12)
            out[k] = {"self": a, "rerun": b, "diff": b - a, "tol": tol, "ok": ok}
            if not ok:
                problems.append(f"{k}: {a:.6g} self-reported, {b:.6g} rerun (|diff| {abs(b - a):.3g} > {tol:.3g})")
        else:
            ok = a == b and (num or type(a) is type(b))       # 1 == True, but a count is no flag
            out[k] = {"self": a, "rerun": b, "ok": ok}
            if not ok:
                problems.append(f"{k}: {a!r} self-reported, {b!r} rerun (must be equal)")
    return out, problems, skipped


def compare(doc: dict, rec: dict) -> dict:
    """A self-reported result (doc) against a rerun (rec, shaped like a result).

    Identical verdicts of every spec of the test (judged now, with the specs of now), each metric
    within its tolerance, the same params, and the same content of every input the rerun recorded
    (the candidate netlist among them). Globals that both record must be equal; a global only one
    of them records (a parameter added to the deck since) is a note."""
    from .specs import blocks

    b = blocks()[doc["block"]]
    metrics, problems, skipped = compare_metrics(doc.get("metrics") or {}, rec.get("metrics") or {})
    mc = (doc.get("meta") or {}).get("mc")
    sv, _ = b.verdicts(doc["test"], doc["corner"], mc, doc.get("metrics") or {})
    rv, _ = b.verdicts(rec["test"], rec["corner"], (rec.get("meta") or {}).get("mc"), rec.get("metrics") or {})
    verdicts = {}
    for sid in sorted(set(sv) | set(rv)):
        a, r = sv.get(sid, {}).get("pass"), rv.get(sid, {}).get("pass")
        verdicts[sid] = {"self": a, "rerun": r, "ok": a == r}
        if a != r:
            problems.insert(0, f"{sid}: {'pass' if a else 'fail'} self-reported, {'pass' if r else 'fail'} rerun")
    notes = []
    if _norm(doc.get("params")) != _norm(rec.get("params")):
        problems.append(f"params differ: {doc.get('params')} self-reported, {rec.get('params')} rerun")
    g1, g2 = _norm(doc.get("globals") or {}), _norm(rec.get("globals") or {})
    for k in sorted(set(g1) | set(g2)):
        if k in g1 and k in g2:
            if g1[k] != g2[k]:
                problems.append(f"global {k}: {g1[k]} self-reported, {g2[k]} rerun")
        else:
            notes.append(f"global {k} recorded by {'the rerun' if k in g2 else 'the result'} only")
    sf = (doc.get("meta") or {}).get("files") or {}
    rf = (rec.get("meta") or {}).get("files") or {}
    for f, h in rf.items():
        if sf.get(f) != h:
            problems.append(f"input {f}: {'not recorded' if f not in sf else sf[f]} self-reported, {h} rerun")
    nl = netlist_rel(doc["block"], doc["view"][5:]) if doc.get("view", "").startswith("xtor-") else None
    if nl and nl not in rf:
        problems.append(f"the rerun does not record the candidate netlist {nl}")
    return {"ok": not problems, "tolerances": TOL_DOC, "problems": problems, "verdicts": verdicts,
            "metrics": metrics, "not_compared": skipped, "notes": notes}


# ------------------------------------------------------------------ the leaderboard's view
def load_record(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def state(doc: dict) -> dict:
    """{"state": verified | self-reported | mismatch, "why": ...} of a candidate result.

    verified: its record (record_path) verifies the netlist hash the result records, which is also
    the hash of the candidate's netlist now; the record is fresh (checks.judge); and the result
    compares with the record within the tolerances, with identical verdicts. mismatch: a record of
    this netlist that is fresh but does not compare. self-reported: anything else (no record, a
    record of another netlist, a stale record). The result's own meta (verified_by ...) never counts."""
    from .checks import judge
    from .netlist import content_hash

    view = doc.get("view", "")
    if doc.get("block") == "adc_top" or not view.startswith("xtor-"):
        return {"state": "self-reported", "why": "not a candidate result"}
    name = view[5:]
    p = record_path(doc["block"], name, doc["test"], Path(doc["_path"]).stem)
    if not p.exists():
        return {"state": "self-reported", "why": "no verification record"}
    rec = load_record(p)
    if not isinstance(rec, dict) or not isinstance(rec.get("verifies"), dict):
        return {"state": "self-reported", "why": "unreadable verification record"}
    nl = netlist_rel(doc["block"], name)
    h_res = ((doc.get("meta") or {}).get("files") or {}).get(nl)
    net = cand.netlist_path(doc["block"], name)
    h_now = content_hash(net) if net.exists() else None
    if rec["verifies"].get("netlist_hash") != h_res or h_res != h_now:
        return {"state": "self-reported", "why": "the verification record is of another netlist"}
    try:
        stale = judge(rec)["stale"]
    except Exception as e:                                  # a record that no longer resolves
        stale = [f"({e})"]
    if stale:
        return {"state": "self-reported", "why": f"the verification is stale ({', '.join(stale[:3])})"}
    try:
        c = compare(doc, rec)
    except Exception as e:
        return {"state": "mismatch", "why": f"cannot compare: {e}"}
    if not c["ok"]:
        return {"state": "mismatch", "why": "; ".join(c["problems"][:3])}
    return {"state": "verified", "why": ""}


def record_problems() -> tuple[list[str], list[str]]:
    """(errors, warnings) of the verification records on disk: each is a JSON whose block,
    candidate, test and job are its path and whose `verifies.result` is the result at the matching
    path; a record whose result no longer exists is a warning."""
    errs, warns = [], []
    root = cand.ROOT / "verification"
    for f in sorted(root.rglob("*")) if root.is_dir() else []:
        if f.is_dir():
            continue
        rel = f.relative_to(cand.ROOT).as_posix()
        parts = rel.split("/")
        if len(parts) != 5 or f.suffix != ".json":
            errs.append(f"{rel}: verification/ holds only <block>/<candidate>/<test>/<job>.json")
            continue
        rec = load_record(f)
        if not isinstance(rec, dict):
            errs.append(f"{rel}: not a JSON object")
            continue
        _, block, name, test, job = parts
        want = {"block": block, "candidate": name, "test": test, "job": job[:-5], "view": f"xtor-{name}"}
        got = {k: rec.get(k) for k in want}
        if got != want:
            errs.append(f"{rel}: {got} do not match its path {want}")
        res = f"results/{block}/{test}/xtor-{name}/{job}"
        if (rec.get("verifies") or {}).get("result") != res:
            errs.append(f"{rel}: verifies.result must be {res}")
        elif not (cand.ROOT / res).is_file():
            warns.append(f"{rel}: the result it verifies ({res}) does not exist")
        if rec.get("status") not in ("match", "mismatch"):
            errs.append(f"{rel}: status must be match or mismatch")
    return errs, warns


# ------------------------------------------------------------------ the rerun
def required_corners(block, test_id: str) -> list[str]:
    """Corners that a nominal spec of the test requires (union of their corner sets)."""
    from .corners import corner_names

    out: set[str] = set()
    for s in block.specs:
        if s.test == test_id and not s.mc:
            out |= corner_names(s.corners)
    return sorted(out)


def plan(test_id: str, block: str | None, name: str, corners: str | None = None) -> tuple[list[dict], list[str]]:
    """(self-reported results to verify, refusals) for a test of a candidate at `corners` (default:
    the corners its specs require). A refusal means nothing is simulated."""
    from .checks import judge
    from .corners import corner_set
    from .netlist import content_hash
    from .specs import find_test

    b, _ = find_test(test_id, block)
    if b.name == "adc_top":
        return [], ["adc_top has no candidates"]
    c = cand.load(b.name, name)
    if not c.netlist.exists():
        return [], [f"no candidate {name!r} (design/xtor/{b.name}/{name}/{b.name}.scs)"]
    want = [x.name for x in corner_set(corners)] if corners else required_corners(b, test_id)
    if not want:
        return [], [f"{test_id}: no nominal spec requires a corner; give --corners"]
    nl, h_now = netlist_rel(b.name, name), content_hash(c.netlist)
    docs = [d for d in cand._results(b.name, f"xtor-{name}") if d["test"] == test_id and d["corner"] in want]
    refusals = [f"{test_id} at {x}: no self-reported result of {name} to verify"
                for x in want if x not in {d["corner"] for d in docs}]
    for d in docs:
        where = Path(d["_path"]).relative_to(cand.ROOT).as_posix()
        meta = d.get("meta") or {}
        h = (meta.get("files") or {}).get(nl)
        if meta.get("mc"):
            refusals.append(f"{where}: a Monte Carlo result (verify runs nominal corners)")
        elif h is None:
            refusals.append(f"{where}: does not record the candidate netlist {nl}")
        elif h != h_now:
            refusals.append(f"{where}: recorded on netlist {h}, {nl} is now {h_now}: the netlist differs "
                            "(the author re-runs it first)")
        elif "error" in (d.get("metrics") or {}):
            refusals.append(f"{where}: an error result, nothing to verify")
        else:
            st = judge(d)["stale"]
            if st:
                refusals.append(f"{where}: stale ({', '.join(st[:3])}); the author re-runs or rehashes it first")
    return sorted(docs, key=lambda d: Path(d["_path"]).stem), refusals


def record_doc(doc: dict, row: dict | None, name: str) -> dict:
    """The verification record of a self-reported result `doc` from a rerun summary row (None:
    the rerun had no such job)."""
    from .specs import blocks

    b = blocks()[doc["block"]]
    nl = netlist_rel(doc["block"], name)
    smeta = doc.get("meta") or {}
    row = row or {"metrics": {"error": f"the rerun has no job {Path(doc['_path']).stem}"}, "params": None,
                  "globals": None, "meta": {}}
    meta = row.get("meta") or {}
    verdict, na = b.verdicts(doc["test"], doc["corner"], meta.get("mc"), row["metrics"])
    rec = {"block": doc["block"], "candidate": name, "test": doc["test"], "view": f"xtor-{name}",
           "corner": doc["corner"], "job": Path(doc["_path"]).stem, "status": None,
           "verifies": {"result": Path(doc["_path"]).relative_to(cand.ROOT).as_posix(), "netlist": nl,
                        "netlist_hash": (smeta.get("files") or {}).get(nl), "date": smeta.get("date"),
                        "git": smeta.get("git"), "mode": smeta.get("mode")},
           "params": row.get("params"), "globals": row.get("globals"), "metrics": row["metrics"], "specs": verdict}
    if na:
        rec["specs_na"] = na
    rec["comparison"] = None
    rec["meta"] = meta
    rec = _norm(rec)
    c = compare(doc, rec)
    rec["status"] = "match" if c["ok"] else "mismatch"
    rec["comparison"] = c
    return rec


def write(rec: dict) -> Path:
    p = record_path(rec["block"], rec["candidate"], rec["test"], rec["job"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1, default=float) + "\n", encoding="utf-8", newline="\n")
    return p


def verify(test_id: str, block: str | None, name: str, corners: str | None = None, mode: str = "aps",
           parallel: int = 6, keep: bool = False, dry: bool = False, run=None) -> int:
    """Rerun a candidate's self-reported results of a test and write their verification records.

    0 when every record matches; 1 when anything was refused (nothing simulated) or a record is a
    mismatch (written with status mismatch). `run` is runner.run_test (tests replace it)."""
    from .specs import find_test

    b, _ = find_test(test_id, block)
    docs, refusals = plan(test_id, b.name, name, corners)
    if refusals:
        print(f"[adcflow] verify {test_id} {b.name}/{name}: refused, nothing simulated")
        for r in refusals:
            print(f"  {r}")
        return 1
    stems = [Path(d["_path"]).stem for d in docs]
    print(f"[adcflow] verify {test_id} {b.name}/{name}: {len(docs)} result(s) on netlist "
          f"{(docs[0]['meta']['files'][netlist_rel(b.name, name)])}: {', '.join(stems)}")
    if dry:
        return 0
    if run is None:
        from .runner import run_test as run
    t0 = _dt.datetime.now()
    summary = run(test_id, b.name, ",".join(sorted({d["corner"] for d in docs})), {b.name: f"xtor:{name}"},
                  {}, mode, parallel, keep, False)
    rows = {r["job"]: r for r in summary}
    bad = 0
    print(f"[adcflow] verify {test_id} {b.name}/{name}: rerun took {(_dt.datetime.now() - t0).total_seconds():.0f} s")
    for d in docs:
        stem = Path(d["_path"]).stem
        rec = record_doc(d, rows.get(stem), name)
        p = write(rec)
        c = rec["comparison"]
        rel = p.relative_to(cand.ROOT).as_posix()
        if rec["status"] == "match":
            worst = max((abs(v["diff"]) / v["tol"] for v in c["metrics"].values() if v.get("tol")), default=0.0)
            print(f"  match     {rel} (largest |diff| / tolerance {worst:.2f})")
        else:
            bad += 1
            print(f"  MISMATCH  {rel}")
            for pr in c["problems"][:8]:
                print(f"            {pr}")
    extra = sorted(set(rows) - set(stems))
    if extra:
        print(f"  (rerun jobs without a self-reported result, not recorded: {', '.join(extra)})")
    print(f"[adcflow] verify: {len(docs) - bad} match, {bad} mismatch")
    return 1 if bad else 0
