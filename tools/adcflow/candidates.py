"""Competing transistor-level candidates of a block (docs/proposals/open-candidates.md §1, §3, §4).

A candidate is a directory ``design/xtor/<block>/<name>/`` with the netlist ``<block>.scs``
(subcircuit name and ports as in the block spec) and ``candidate.yaml``::

    name: alice-strongarm                 # the directory name: unique key within the block
    description: StrongARM latch with a preamp-less input pair.
    status: wip                           # wip | ready | withdrawn
    acknowledged: [41]                    # spec-change notices ([<block>] issues) confirmed
    authors:
      - {github: alice, name: "Alice's agent 3"}   # name: optional, self-declared, not verified

Views of a block in a run (``--view <block>=...``):

* ``behav``: the behavioral view;
* ``xtor:<name>``: the candidate ``<name>``; results go to ``results/<block>/<test>/xtor-<name>/``;
* ``xtor``: the block's ``selected:`` candidate (block spec), or, until a block is migrated,
  the legacy single view ``views.xtor`` (``design/xtor/<block>/<block>.scs``, results in ``xtor/``).

Top-level runs are signed ``xtor-<blk>@<name>[+<blk>@<name>...]`` (``blk`` without ``adc_``).

``score`` gives the leaderboard row of a candidate from its results; ``migrate`` moves a legacy
view and its ``xtor`` results into a named candidate.
"""

from __future__ import annotations

import datetime as _dt
import functools
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import REPO_ROOT

ROOT = REPO_ROOT                       # repository root (tests point it at a temporary copy)
NAME_RE = re.compile(r"^[a-z0-9-]{2,24}$")
LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
STATUSES = ("wip", "ready", "withdrawn")
NONE = "none"                          # `selected: none`: no candidate selected yet


class ViewError(ValueError):
    """A --view value that does not name an existing view of the block."""


def block_dir(block: str) -> Path:
    return ROOT / "design" / "xtor" / block


def candidate_dir(block: str, name: str) -> Path:
    return block_dir(block) / name


def netlist_path(block: str, name: str) -> Path:
    return candidate_dir(block, name) / f"{block}.scs"


@dataclass
class Candidate:
    block: str
    name: str
    meta: dict = field(default_factory=dict)          # candidate.yaml
    problems: list[str] = field(default_factory=list)

    @property
    def dir(self) -> Path:
        return candidate_dir(self.block, self.name)

    @property
    def netlist(self) -> Path:
        return netlist_path(self.block, self.name)

    @property
    def status(self) -> str:
        return str(self.meta.get("status", ""))

    @property
    def authors(self) -> list[dict]:
        return [a for a in self.meta.get("authors") or [] if isinstance(a, dict)]

    def author_text(self) -> str:
        """`name (@login)`, or `@login` without a display name; the login is the identity."""
        return ", ".join(f"{a['name']} (@{a['github']})" if a.get("name") else f"@{a.get('github')}"
                         for a in self.authors)


def _text_problems(text: str) -> list[str]:
    """Forbidden names and site-specific / model-card patterns in a free text (checks.hygiene rules)."""
    from .checks import FORBIDDEN, _site_literals, find_names

    out = [what for _, what in find_names(text)]
    out += [what for pat, what in FORBIDDEN + _site_literals()
            if re.search(pat, text, flags=re.MULTILINE | re.IGNORECASE)]
    return out


def validate(block: str, name: str, meta, has_netlist: bool) -> list[str]:
    """Problems of a candidate: its name, candidate.yaml and netlist (empty when valid)."""
    errs = []
    where = f"design/xtor/{block}/{name}"
    if not NAME_RE.match(name):
        errs.append(f"{where}: candidate name must match [a-z0-9-]{{2,24}}")
    if not isinstance(meta, dict):
        return errs + [f"{where}/candidate.yaml: missing or not a mapping"]
    if meta.get("name") != name:
        errs.append(f"{where}/candidate.yaml: name {meta.get('name')!r} must be the directory name {name!r}")
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errs.append(f"{where}/candidate.yaml: description (one or two sentences) is required")
    if meta.get("status") not in STATUSES:
        errs.append(f"{where}/candidate.yaml: status {meta.get('status')!r} not in {list(STATUSES)}")
    ack = meta.get("acknowledged", [])
    if not isinstance(ack, list) or not all(isinstance(a, int) and not isinstance(a, bool) and a > 0 for a in ack):
        errs.append(f"{where}/candidate.yaml: acknowledged must be a list of issue numbers")
    authors = meta.get("authors")
    if not isinstance(authors, list) or not authors:
        errs.append(f"{where}/candidate.yaml: authors must list at least one {{github: <login>}}")
        authors = []
    for i, a in enumerate(authors):
        if not isinstance(a, dict) or set(a) - {"github", "name"}:
            errs.append(f"{where}/candidate.yaml: authors[{i}] must be {{github: <login>, name: <display name>}}")
            continue
        if not isinstance(a.get("github"), str) or not LOGIN_RE.match(a["github"]):
            errs.append(f"{where}/candidate.yaml: authors[{i}].github {a.get('github')!r} is not a GitHub login")
        dn = a.get("name")
        if dn is not None:
            if not isinstance(dn, str) or not dn.strip() or len(dn) > 64 or "\n" in dn:
                errs.append(f"{where}/candidate.yaml: authors[{i}].name must be one line of at most 64 characters")
            else:
                errs += [f"{where}/candidate.yaml: authors[{i}].name: {w} must not be used" for w in _text_problems(dn)]
    unknown = set(meta) - {"name", "description", "status", "acknowledged", "authors"}
    if unknown:
        errs.append(f"{where}/candidate.yaml: unknown keys {sorted(unknown)}")
    if not has_netlist:
        errs.append(f"{where}: netlist {block}.scs missing")
    return errs


def load(block: str, name: str) -> Candidate:
    d = candidate_dir(block, name)
    f = d / "candidate.yaml"
    try:
        meta = yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else None
    except yaml.YAMLError as e:
        meta = None
        problems = [f"design/xtor/{block}/{name}/candidate.yaml: {e}"]
    else:
        problems = []
    c = Candidate(block, name, meta if isinstance(meta, dict) else {})
    c.problems = problems + validate(block, name, meta, netlist_path(block, name).exists())
    return c


def candidates(block: str | None = None) -> list[Candidate]:
    """Every candidate directory of a block (or of all blocks), withdrawn ones included."""
    from .specs import blocks

    out = []
    for b in blocks():
        if block and b != block:
            continue
        d = block_dir(b)
        if d.is_dir():
            out += [load(b, p.name) for p in sorted(d.iterdir()) if p.is_dir()]
    return out


# ------------------------------------------------------------------ views and result paths
def resolve(block: str, view: str) -> tuple[Path, str]:
    """(netlist file, result-directory view name) of `view` of a block."""
    from .specs import blocks

    b = blocks()[block]
    if view == "behav" or (view in b.views and view != "xtor"):
        return b.view_path(view), view
    if view.startswith("xtor:"):
        name = view[5:]
        if not NAME_RE.match(name) or not netlist_path(block, name).exists():
            raise ViewError(f"{block}: no candidate {name!r} (design/xtor/{block}/{name}/{block}.scs)")
        return netlist_path(block, name), f"xtor-{name}"
    if view == "xtor":
        sel = b.selected
        if sel:
            return resolve(block, f"xtor:{sel}")
        if "xtor" in b.views:                                  # legacy single view, until migrated
            return b.view_path("xtor"), "xtor"
        raise ViewError(f"{block}: no candidate is selected (selected: none); use --view {block}=xtor:<name>")
    raise ViewError(f"{block}: unknown view {view!r} (behav, xtor or xtor:<candidate>)")


def view_dir(block: str, view: str) -> str:
    """Result-directory name of a block view: behav, xtor (legacy) or xtor-<candidate>."""
    return resolve(block, view)[1]


def top_signature(views: dict[str, str], n_blocks: int) -> str:
    """View signature of an adc_top run: behav, xtor (every block on its legacy view) or
    xtor-<blk>[@<candidate>]+... for the blocks that are not behavioral."""
    terms, legacy = [], True
    for b in sorted(k for k, v in views.items() if v != "behav"):
        d = view_dir(b, views[b])
        short = b.replace("adc_", "")
        if d.startswith("xtor-"):
            legacy = False
            terms.append(f"{short}@{d[5:]}")
        else:
            terms.append(short)
    if not terms:
        return "behav"
    if legacy and len(terms) == n_blocks:
        return "xtor"
    return "xtor-" + "+".join(terms)


# ------------------------------------------------------------------ scoring (§3)
SUPPLY = {"vdd": "vdd", "vdd18": "vdd18"}
# power in uW at the typical corner: (test, metric, how). how: a global supply (current in uA x V),
# "uW" (already a power) or "comparisons" (energy per comparison in fJ x decisions x fs)
POWER = {
    "adc_bootstrap": [("tb_bootstrap_dc", "iavg_uA", "vdd")],
    "adc_clkgen": [("tb_clkgen_timing", "iavg_uA", "vdd")],
    "adc_ref": [("tb_ref_dc", "i18_uA", "vdd18"), ("tb_ref_dc", "i09_uA", "vdd")],
    "adc_sarlogic": [("tb_sarlogic_func", "power_uW", "uW")],
    "adc_comp": [("tb_comp_delay", "energy_fJ", "comparisons")],
}
TYP = "tt_nom_27"


def _margin(spec, value) -> float | None:
    """(limit - value) / |limit| towards the violated side; negative = fails; |limit| 0 -> 1."""
    if not isinstance(value, (int, float)):
        return None
    out = []
    if spec.max is not None:
        out.append((spec.max - value) / (abs(spec.max) or 1.0))
    if spec.min is not None:
        out.append((value - spec.min) / (abs(spec.min) or 1.0))
    return min(out)


def _value(v):
    """Numbers of a netlist parameter value with an SI suffix ('1.2u' -> 1.2e-6), else None."""
    m = re.match(r"^([-+]?[0-9.]+(?:[eE][-+]?\d+)?)([a-zA-Z]*)$", v)
    if not m:
        return None
    x = float(m.group(1))
    sfx = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3, "k": 1e3, "M": 1e6, "G": 1e9}
    return x * sfx[m.group(2)[0]] if m.group(2) and m.group(2)[0] in sfx else x


def area_proxy(netlist: Path) -> dict:
    """Area proxy of a candidate netlist, below the block subcircuit and with multipliers m:
    device count, MOS count and sum of W*L (um^2, w and l as written on the instance) and the
    capacitors (count, total F where c= is given). Not a layout area: a common yardstick (§3)."""
    from .netlist import parse
    from .soa import classify

    nl = parse(netlist)
    block = netlist.stem
    out = {"devices": 0, "mos": 0, "wl_um2": 0.0, "caps": 0, "cap_F": 0.0}

    def walk(name: str, mult: float, depth: int) -> None:
        sc = nl.subckts.get(name)
        if sc is None or depth > 32:
            return
        for i in sc.instances:
            kv = dict(re.findall(r"(\w+)\s*=\s*(\S+)", i.params))
            m = (_value(kv.get("m", "1")) or 1.0) * mult
            if i.master in nl.subckts:
                walk(i.master, m, depth + 1)
                continue
            kind = classify(i.master)
            if kind in ("mos", "thick", "unknown"):
                out["devices"] += m
                out["mos"] += m
                w, ln = _value(kv.get("w", "")), _value(kv.get("l", ""))
                if w and ln:
                    out["wl_um2"] += w * ln * 1e12 * m
            elif kind == "moscap" or re.search(r"cap|mom|mim", i.master, re.I):
                out["devices"] += m
                out["caps"] += m
                c = _value(kv.get("c", ""))
                out["cap_F"] += (c or 0.0) * m
            else:
                out["devices"] += m

    walk(block, 1.0, 0)
    out["devices"] = int(out["devices"])
    out["mos"] = int(out["mos"])
    out["caps"] = int(out["caps"])
    out["wl_um2"] = round(out["wl_um2"], 4)
    return out


def _results(block: str, view: str) -> list[dict]:
    out = []
    for f in sorted((ROOT / "results" / block).glob(f"*/{view}/*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        d["_path"] = f
        out.append(d)
    return out


def mc_coverage(b, docs: list[tuple[dict, dict]]) -> list[dict]:
    """Sample coverage of the block's Monte Carlo specs over judged results: per spec {spec, ok,
    need, failed} from the verdicts' `samples` (Spec.samples); with several results the fewest valid
    and the most failed samples count. No result: ok 0, failed None."""
    out = []
    for s in b.specs:
        if not s.mc:
            continue
        got = [j["specs"][s.id]["samples"] for d, j in docs
               if d["test"] == s.test and j["specs"].get(s.id, {}).get("samples")]
        fails = [g["failed"] for g in got]
        out.append({"spec": s.id, "need": s.mc, "ok": min((g["ok"] for g in got), default=0),
                    "failed": None if not got or None in fails else max(fails)})
    return out


def mc_text(mc: list[dict]) -> str:
    """'CMP-03 50/50', 'CMP-03 48/50 2 failed', 'CMP-03 0/50' (no result); '-' without Monte Carlo specs."""
    return ", ".join(f"{m['spec']} {m['ok']}/{m['need']}" + (f" {m['failed']} failed" if m["failed"] else "")
                     for m in mc) or "-"


def score(c: Candidate) -> dict:
    """The leaderboard row of a candidate (§3, #75): spec pass count, corner coverage, Monte Carlo
    sample coverage, flags, the block's power at TT, area proxy, the mixed top-level regression and
    whether the candidate is eligible for selection (`eligible`, and `missing`: what keeps it out).
    The worst margin and the top-level ENOB margin are information: margin beyond a limit earns
    nothing, they are not ranking criteria (`compare`).

    A reported-only spec (`reported: true`, the power figures) has no verdict: it counts neither as
    passed nor as failed (`specs_total` counts the specs with a limit), but its value must be
    recorded at every corner it names, else it is incomplete (`specs_reported` / `reported_total`).

    Each result is verified, self-reported or a mismatch (verify.state: only a matching, fresh
    verification record of the lead in verification/ verifies it; nothing in the result's own meta
    counts). flags.unverified counts the self-reported results at corners that a spec of their test
    requires, flags.mismatch every mismatch."""
    from . import verify
    from .checks import judge
    from .corners import corner_names
    from .specs import blocks

    b = blocks()[c.block]
    view = f"xtor-{c.name}"
    docs = [(d, judge(d)) for d in _results(c.block, view)]
    states = [verify.state(d)["state"] for d, _ in docs]
    required = {t: set(verify.required_corners(b, t)) for t in {d["test"] for d, _ in docs}}
    passed = failed = incomplete = reported = 0
    failing, missing = [], []
    need = got = 0
    worst = None
    for s in b.specs:
        req = corner_names(s.corners)
        vals = [(d["corner"], j["specs"][s.id]) for d, j in docs
                if d["test"] == s.test and s.id in j["specs"]]
        have = {c_ for c_, _ in vals} & req
        need += len(req)
        got += len(have)
        if s.reported:                                      # no verdict: recorded at its corners, or incomplete
            if have == req and all(isinstance(v["value"], (int, float)) for _, v in vals):
                reported += 1
            else:
                incomplete += 1
                missing.append(s.id)
            continue
        if any(v["pass"] is False for _, v in vals):
            failed += 1
            failing.append(s.id)
        elif have == req:
            passed += 1
        else:
            incomplete += 1
            missing.append(s.id)
        for _, v in vals:
            mg = _margin(s, v["value"])
            if mg is not None and (worst is None or mg < worst[0]):
                worst = (mg, s.id)
    flags = {"stale": sum(bool(j["stale"]) for _, j in docs),
             "unverified": sum(s == "self-reported" and d["corner"] in required[d["test"]]
                               for (d, _), s in zip(docs, states)),
             "mismatch": states.count("mismatch"),
             "soa": sum(1 for d, _ in docs if (d["metrics"].get("soa_violations") or 0) > 0),
             "error": sum(bool(j["error"]) for _, j in docs)}
    n_rep = sum(s.reported for s in b.specs)
    row = {"block": c.block, "candidate": c.name, "status": c.status, "authors": c.authors,
           "author_text": c.author_text(), "description": c.meta.get("description", ""),
           "problems": list(c.problems), "selected": b.selected == c.name,
           "specs_passed": passed, "specs_failed": failed, "specs_incomplete": incomplete,
           "specs_total": len(b.specs) - n_rep, "specs_reported": reported, "reported_total": n_rep,
           "specs_failing": failing, "specs_missing": missing,
           "coverage": [got, need], "mc": mc_coverage(b, docs), "results": len(docs), "verified": states.count("verified"),
           "self_reported": states.count("self-reported"), "mismatch": states.count("mismatch"), "flags": flags,
           "worst_margin": None if worst is None else {"margin": worst[0], "spec": worst[1]},
           "power_uW": power_uW(c.block, docs),
           "area": area_proxy(c.netlist) if c.netlist.exists() else None,
           "top_enob_margin": top_enob_margin(c.block, c.name),
           "top_regression": top_regression(c.block, c.name)}
    row["missing"] = eligibility(row)
    row["eligible"] = not row["missing"]
    return row


def power_uW(block: str, docs: list[tuple[dict, dict]]) -> float | None:
    """Power at the typical corner from the supply-current (or power, energy) metrics of the
    block's testbenches (POWER); None when the block has none or they are not recorded."""
    rule = POWER.get(block)
    if not rule:
        return None
    total = 0.0
    for test, metric, how in rule:
        d = next((d for d, _ in docs if d["test"] == test and d["corner"] == TYP and metric in d["metrics"]), None)
        if d is None:
            return None
        v = float(d["metrics"][metric])
        if how == "uW":
            total += v
        elif how == "comparisons":
            from .arch import Arch
            a = Arch.load()
            total += v * 1e-15 * a.n_dec * a.fs * 1e6
        else:
            total += v * float(d["globals"][SUPPLY[how]])
    return round(total, 3)


def top_enob_margin(block: str, name: str) -> float | None:
    """Worst ENOB margin of the top-level sine tests with only this candidate swapped in
    (results/adc_top/<test>/xtor-<blk>@<name>/), against the ENOB limits that apply at each
    result's corner; None without results. Information only (#75): not a ranking criterion."""
    from .specs import blocks

    top = blocks().get("adc_top")
    if top is None:
        return None
    view = f"xtor-{block.replace('adc_', '')}@{name}"
    out = None
    for s in top.specs:
        if s.metric != "enob" or s.min is None:
            continue
        for f in (ROOT / "results" / "adc_top" / s.test / view).glob("*.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            if not s.applies(d.get("corner"), d.get("meta", {}).get("mc")):
                continue                                # e.g. TOP-02 judges the typical corner only
            v = d["metrics"].get("enob")
            if isinstance(v, (int, float)) and (out is None or v - s.min < out):
                out = v - s.min
    return None if out is None else round(out, 4)


# the mixed top-level regression of a candidate (CONTRIBUTING §10): every adc_top test at the corners its
# specs require within this set, i.e. tb_top_sine and tb_top_duty at quick, tb_top_sine_lf at typ
TOP_CORNERS = "quick"


def top_regression(block: str, name: str) -> dict:
    """The mixed top-level regression with this candidate: the adc_top runs with only it swapped in
    (results/adc_top/<test>/xtor-<blk>@<name>/, the lead's runs, the other blocks behavioral).

    Every adc_top test needs a result at each corner its specs require within TOP_CORNERS. It
    passes when all of them are there and every result is fresh, without error and passes every
    spec that applies at its corner. Returns {status: pass | fail | stale | incomplete | none,
    results, missing: ["<test> <corner>"], failing: [spec ids], stale, error}."""
    from .checks import judge
    from .corners import corner_names
    from .specs import blocks

    out = {"status": "none", "results": 0, "missing": [], "failing": [], "stale": 0, "error": 0}
    top = blocks().get("adc_top")
    if top is None:
        return out
    view = f"xtor-{block.replace('adc_', '')}@{name}"
    need: dict[str, set[str]] = {}
    for s in top.specs:
        need.setdefault(s.test, set()).update(corner_names(s.corners) & corner_names(TOP_CORNERS))
    failing: set[str] = set()
    for t in sorted(need):
        got = set()
        for f in sorted((ROOT / "results" / "adc_top" / t / view).glob("*.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            d["_path"] = f
            j = judge(d)
            out["results"] += 1
            got.add(d.get("corner"))
            out["stale"] += bool(j["stale"])
            out["error"] += bool(j["error"])
            failing |= {sid for sid, v in j["specs"].items() if v["pass"] is False}
        out["missing"] += [f"{t} {c}" for c in sorted(need[t] - got)]
    out["failing"] = sorted(failing)
    if not out["results"]:
        out["status"] = "none"
    elif failing or out["error"]:
        out["status"] = "fail"
    elif out["stale"]:
        out["status"] = "stale"
    elif out["missing"]:
        out["status"] = "incomplete"
    else:
        out["status"] = "pass"
    return out


# ------------------------------------------------------------------ eligibility and ranking (§4, #75)
TOL_POWER = 0.05                       # power within 5 % is a tie, decided by area
TOL_AREA = 0.05                        # area (sum of W*L, then capacitance) within 5 %: the selected one stays first


def eligibility(row: dict) -> list[dict]:
    """What keeps a candidate out of the eligible tier: [{what, text}], empty when it is eligible.

    Eligible (CONTRIBUTING §10): every spec passes at every corner it requires (and every
    reported-only metric is recorded there), every result is fresh and without error, every result
    at a required corner is verified by the lead (verification/) and none contradicts it, no SOA
    violation, and the mixed top-level regression with the candidate passes (top_regression).
    `what` is one of problems, results, failing, incomplete, stale, error, soa, mismatch,
    unverified, top."""
    f, out = row["flags"], []

    def add(what: str, text: str) -> None:
        out.append({"what": what, "text": text})

    if row["problems"]:
        add("problems", f"{len(row['problems'])} problem(s) in candidate.yaml or the netlist")
    if not row["results"]:
        add("results", "no results")
    if row["specs_failing"]:
        add("failing", "fails " + ", ".join(row["specs_failing"]))
    if row["specs_missing"]:
        add("incomplete", "no result at every required corner: " + ", ".join(row["specs_missing"]))
    if f["stale"]:
        add("stale", f"{f['stale']} stale result(s)")
    if f["error"]:
        add("error", f"{f['error']} result(s) with an error")
    if f["soa"]:
        add("soa", f"SOA violations in {f['soa']} result(s)")
    if f["mismatch"]:
        add("mismatch", f"the lead's rerun contradicts {f['mismatch']} result(s)")
    if f["unverified"]:
        add("unverified", f"{f['unverified']} self-reported result(s) at required corners (not verified)")
    top = row["top_regression"]
    if top["status"] != "pass":
        shown = ", ".join(top["missing"][:3]) + (" ..." if len(top["missing"]) > 3 else "")
        add("top", {"none": "no mixed top-level regression",
                    "fail": "mixed top-level regression fails" + (f" ({', '.join(top['failing'])})" if top["failing"] else ""),
                    "stale": f"mixed top-level regression stale ({top['stale']} result(s))",
                    "incomplete": f"mixed top-level regression incomplete ({len(top['missing'])} missing: {shown})",
                    }[top["status"]])
    return out


def _lower(a, b, tol: float) -> int:
    """-1 when a is lower (better), 1 when b is, 0 within the relative tolerance; a missing value is worse than any."""
    if a is None and b is None:
        return 0
    if a is None:
        return 1
    if b is None:
        return -1
    if abs(a - b) <= tol * max(abs(a), abs(b)):
        return 0
    return -1 if a < b else 1


def compare(a: dict, b: dict) -> int:
    """Leaderboard order of two rows of one block (§4, #75): -1 when a ranks first, 1 when b, 0 tied.

    The eligible tier comes first. Inside it the block's own reported power at TT (power_uW) decides,
    lowest first; within TOL_POWER it is a tie, decided by the area proxy (sum of W*L, then total
    capacitance, each within TOL_AREA); tied inside every tolerance, the selected candidate stays
    first. Not-eligible candidates follow, by more specs passed, then more (spec, corner) coverage,
    then the same power and area order. Margins beyond a limit (worst margin, top-level ENOB margin)
    earn nothing: they are shown, never ranked."""
    if a["eligible"] != b["eligible"]:
        return -1 if a["eligible"] else 1
    if not a["eligible"]:
        for x, y in ((b["specs_passed"], a["specs_passed"]), (b["coverage"][0], a["coverage"][0])):
            if x != y:
                return -1 if x < y else 1
    area = lambda r, k: (r["area"] or {}).get(k) or None           # noqa: E731  (0 -> unknown)
    for c in (_lower(a["power_uW"], b["power_uW"], TOL_POWER),
              _lower(area(a, "wl_um2"), area(b, "wl_um2"), TOL_AREA),
              _lower(area(a, "cap_F"), area(b, "cap_F"), TOL_AREA)):
        if c:
            return c
    if bool(a["selected"]) != bool(b["selected"]):                 # tied inside every tolerance: the selected one stays
        return -1 if a["selected"] else 1
    return 0


def rank(rows: list[dict]) -> list[dict]:
    """Rows of one block in leaderboard order (compare), ties by candidate name."""
    def key(a: dict, b: dict) -> int:
        return compare(a, b) or (a["candidate"] > b["candidate"]) - (a["candidate"] < b["candidate"])

    return sorted(rows, key=functools.cmp_to_key(key))


def leaderboard(block: str | None = None, withdrawn: bool = False) -> list[dict]:
    """Leaderboard rows by block, each block ranked (rank): the eligible tier first."""
    rows = [score(c) for c in candidates(block) if withdrawn or c.status != "withdrawn"]
    return [r for b in sorted({r["block"] for r in rows}) for r in rank([r for r in rows if r["block"] == b])]


def table(rows: list[dict]) -> str:
    """The leaderboard as text for the terminal: per block the eligible tier, ranked, then the
    candidates that are not eligible with what keeps them out."""
    def f(v, fmt="{:.4g}"):
        return "-" if v is None else fmt.format(v)

    head = (f"  {'#':>2s} {'candidate':24s} {'status':9s} {'power uW':>9s} {'MOS':>5s} {'W*L um2':>9s} {'pass':>8s} "
            f"{'corners':>9s} {'MC samples':>22s} {'worst margin':>18s} {'top ENOB':>8s}  flags / authors")
    L = []
    for blk in dict.fromkeys(r["block"] for r in rows):
        mine = [r for r in rows if r["block"] == blk]
        for tier, sel in (("eligible, ranked by power at TT (lowest first; within 5 % by area)", True),
                          ("not eligible", False)):
            part = [r for r in mine if bool(r.get("eligible")) == sel]
            if not part:
                continue
            L += [f"{blk} -- {tier}", head]
            for i, r in enumerate(part, 1):
                wm = r["worst_margin"]
                flags = [k if k != "unverified" else "self-reported" for k, v in r["flags"].items() if v]
                if r["problems"]:
                    flags.append(f"{len(r['problems'])} problem(s)")
                a = r["area"] or {}
                rep = f"+{r['specs_reported']}r" if r.get("reported_total") else ""
                L.append(f"  {str(i) if sel else '-':>2s} {r['candidate'] + (' *' if r['selected'] else ''):24s} "
                         f"{r['status']:9s} {f(r['power_uW']):>9s} {a.get('mos', '-'):>5} {f(a.get('wl_um2')):>9s} "
                         f"{str(r['specs_passed']) + '/' + str(r['specs_total']) + rep:>8s} "
                         f"{r['coverage'][0]:>4d}/{r['coverage'][1]:<4d} {mc_text(r.get('mc') or []):>22s} "
                         f"{(f(wm['margin'], '{:+.3f}') + ' ' + wm['spec']) if wm else '-':>18s} "
                         f"{f(r['top_enob_margin'], '{:+.3f}'):>8s}  {', '.join(flags) or 'ok'} / {r['author_text']}")
                if not sel:
                    L.append("       missing: " + "; ".join(m["text"] for m in r.get("missing") or []))
    L.append("(* = selected. Eligible = every spec passes at every required corner, results fresh and verified, no SOA "
             "violation, mixed top-level regression passed; ranked by the block's power at TT, ties within 5 % by the "
             "area proxy (sum of W*L, then capacitance, 5 %), then the selected one stays first. Worst margin and top "
             "ENOB margin are shown, not ranked. pass = specs with a limit passing at every required corner (+Nr = "
             "reported-only metrics recorded, no verdict); corners = (spec, corner) results / required; MC samples = "
             "valid / required Monte Carlo samples of a spec with mc:, any failed one fails it; self-reported = results "
             "at required corners without a matching, fresh verification record of the lead (verification/, adcflow "
             "verify); mismatch = the lead's rerun disagrees)")
    return "\n".join(L)


# ------------------------------------------------------------------ migration (§1)
def migrate(block: str, name: str, authors: list[dict], description: str, dry: bool = False) -> list[str]:
    """Move the legacy view design/xtor/<block>/* and its `xtor` results into candidate `name`.

    Files are moved, not changed: the result JSONs get view xtor-<name>, their meta.files keys follow
    the moved netlists (content hashes unchanged, so nothing goes stale) and meta.migrated records the
    move. Top-level results whose signature names the block's legacy view are renamed to <blk>@<name>.
    The block spec (views.xtor -> selected:) is left to the caller. Returns the moves done (or planned)."""
    from . import runner
    from .specs import blocks

    if block not in blocks() or block == "adc_top":
        raise ValueError(f"{block}: not a block that can have candidates")
    if not NAME_RE.match(name):
        raise ValueError(f"candidate name {name!r} must match [a-z0-9-]{{2,24}}")
    src = block_dir(block)
    files = sorted(p for p in src.iterdir() if p.is_file()) if src.is_dir() else []
    if not any(p.name == f"{block}.scs" for p in files):
        raise FileNotFoundError(f"design/xtor/{block}/{block}.scs: no legacy view to migrate")
    dst = candidate_dir(block, name)
    if dst.exists():
        raise FileExistsError(f"design/xtor/{block}/{name} exists")
    meta = {"name": name, "description": description, "status": "wip", "acknowledged": [], "authors": authors}
    probs = validate(block, name, meta, True)
    if probs:
        raise ValueError("; ".join(probs))
    rel = lambda p: p.relative_to(ROOT).as_posix()  # noqa: E731
    keymap = {rel(p): rel(dst / p.name) for p in files}
    moves = [(p, dst / p.name) for p in files]
    short = block.replace("adc_", "")
    stamp = {"date": _dt.datetime.now().isoformat(timespec="seconds"),
             "git": runner._git("rev-parse", "--short", "HEAD"), "from": "xtor", "candidate": name}
    result_moves = []                                   # (old dir, new dir, new view)
    for d in sorted((ROOT / "results" / block).glob("*/xtor")):
        result_moves.append((d, d.with_name(f"xtor-{name}"), f"xtor-{name}"))
    for d in sorted((ROOT / "results" / "adc_top").glob("*/xtor*")):
        sig = d.name
        if sig == "xtor":
            continue                                    # every block legacy: renamed when all are migrated
        terms = sig[5:].split("+") if sig.startswith("xtor-") else []
        if short in terms:
            new = "xtor-" + "+".join(f"{short}@{name}" if t == short else t for t in terms)
            result_moves.append((d, d.with_name(new), new))
    log = [f"{rel(a)} -> {rel(b)}" for a, b in moves] + [f"{rel(a)}/ -> {rel(b)}/" for a, b, _ in result_moves]
    if dry:
        return log + [f"write {rel(dst / 'candidate.yaml')}"]
    dst.mkdir(parents=True)
    for a, b in moves:
        shutil.move(str(a), str(b))
    (dst / "candidate.yaml").write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8")
    for old, new, view in result_moves:
        if new.exists():
            raise FileExistsError(f"{rel(new)} exists")
        shutil.move(str(old), str(new))
        for f in sorted(new.glob("*.json")):
            doc = json.loads(f.read_text(encoding="utf-8"))
            doc["view"] = view
            m = doc.setdefault("meta", {})
            m["files"] = {keymap.get(k, k): v for k, v in (m.get("files") or {}).items()}
            if "views" in m:                       # recorded with its dependencies (deps.py)
                m["views"] = {k: f"xtor:{name}" if k == block and v == "xtor" else v for k, v in m["views"].items()}
            m["migrated"] = dict(stamp)
            f.write_text(json.dumps(doc, indent=1, default=float) + "\n", encoding="utf-8", newline="\n")
    return log + [f"wrote {rel(dst / 'candidate.yaml')}"]


# ------------------------------------------------------------------ CI rules (§2): check candidates
PRIMITIVES = {"resistor", "capacitor", "inductor"}         # Spectre primitives a candidate may use
DIR_FILES = {".md", ".png", ".svg", ".txt"}                # besides <block>.scs and candidate.yaml
RESULT_FILES = {".json", ".png"}
MAX_DIR_BYTES = 2_000_000                                  # a candidate directory
MAX_JSON_BYTES = 1_000_000                                 # one result JSON


def pdk_devices() -> set[str]:
    """Device models a candidate may instantiate: those of the RNL package (design/rnl/adc28.rnl)
    and the MOS lists of specs/soa.yaml."""
    from .soa import config

    text = (ROOT / "design" / "rnl" / "adc28.rnl").read_text(encoding="utf-8")
    out = set(re.findall(r'@DEVICE\(name="\*", model="([^"]+)"', text))
    c = config()
    for names in c["thin_oxide"].values():
        out |= set(names)
    return out | set(c["thick_oxide"])


def owner_of_path(path: str) -> tuple[str, str] | None:
    """(block, candidate) of a repository path that belongs to a candidate: its directory
    design/xtor/<block>/<name>/... or its results results/<block>/<test>/xtor-<name>/...;
    None for any other path (legacy views, adc_top runs, specs, tools ...)."""
    p = path.split("/")
    if len(p) >= 5 and p[0] == "design" and p[1] == "xtor":
        return p[2], p[3]
    if len(p) >= 5 and p[0] == "results" and p[3].startswith("xtor-") and "@" not in p[3] and p[1] != "adc_top":
        return p[1], p[3][5:]
    return None


def netlist_problems(block: str, name: str, text: str) -> list[str]:
    """A candidate netlist holds only subcircuits built from PDK devices, Spectre primitives and its
    own subcircuits: no include / ahdl_include (models come from the run deck), no instances at its
    top level, no Verilog-A or other blocks."""
    from .netlist import parse

    where = f"design/xtor/{block}/{name}/{block}.scs"
    nl = parse(where, text=text)
    errs = [f"{where}: {e}" for e in nl.errors]
    errs += [f'{where}: {kind} "{f}" is not allowed: a candidate is self-contained, the run deck '
             "provides the models" for kind, f in nl.includes]
    if nl.top_instances:
        errs.append(f"{where}: {len(nl.top_instances)} instance(s) outside a subcircuit ({nl.top_instances[0].name})")
    if block not in nl.subckts:
        errs.append(f"{where}: does not define subckt {block}")
    allowed = pdk_devices() | PRIMITIVES | set(nl.subckts)
    for sc in nl.subckts.values():
        for i in sc.instances:
            if i.master not in allowed:
                errs.append(f"{where}:{i.line}: {sc.name}.{i.name} uses {i.master}: only PDK devices, "
                            f"{'/'.join(sorted(PRIMITIVES))} and subcircuits of the candidate are allowed")
    return errs


def tree_problems(block: str, name: str, files: dict[str, bytes]) -> list[str]:
    """Rules for the files of one candidate (repo-relative path -> content): its directory holds
    <block>.scs, candidate.yaml and notes / figures, within the size limits; its results are
    result JSONs of this candidate (without meta.verified_by: verification is the lead's record in
    verification/) and PNGs. Includes the naming and candidate.yaml rules."""
    from .checks import FIGURE_MAX_BYTES

    if block not in _blocks() or block == "adc_top":
        return [f"design/xtor/{block}/{name}: {block} is not a block that can have candidates"]
    errs = []
    d = f"design/xtor/{block}/{name}/"
    own = {p: b for p, b in files.items() if p.startswith(d)}
    total = sum(len(b) for b in own.values())
    if total > MAX_DIR_BYTES:
        errs.append(f"{d}: {total / 1e6:.1f} MB (limit {MAX_DIR_BYTES / 1e6:.0f} MB)")
    meta = None
    if d + "candidate.yaml" in own:
        try:
            meta = yaml.safe_load(own[d + "candidate.yaml"].decode("utf-8"))
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            errs.append(f"{d}candidate.yaml: {e}")
    if own:
        errs += validate(block, name, meta, d + f"{block}.scs" in own)
    for p, b in sorted(files.items()):
        ext = Path(p).suffix.lower()
        if p.startswith(d):
            rel = p[len(d):]
            if "/" in rel:
                errs.append(f"{p}: a candidate directory has no subdirectories")
            elif rel == f"{block}.scs":
                try:
                    errs += netlist_problems(block, name, b.decode("utf-8"))
                except UnicodeDecodeError:
                    errs.append(f"{p}: not UTF-8 text")
            elif rel != "candidate.yaml" and ext not in DIR_FILES:
                errs.append(f"{p}: only {block}.scs, candidate.yaml and {', '.join(sorted(DIR_FILES))} files")
            if ext == ".png" and len(b) > FIGURE_MAX_BYTES:
                errs.append(f"{p}: {len(b) // 1000} kB (limit {FIGURE_MAX_BYTES // 1000} kB)")
            continue
        if ext not in RESULT_FILES:
            errs.append(f"{p}: results of a candidate are .json and .png files")
        elif ext == ".png" and len(b) > FIGURE_MAX_BYTES:
            errs.append(f"{p}: {len(b) // 1000} kB (limit {FIGURE_MAX_BYTES // 1000} kB)")
        elif ext == ".json":
            if len(b) > MAX_JSON_BYTES:
                errs.append(f"{p}: {len(b) / 1e6:.1f} MB (limit {MAX_JSON_BYTES / 1e6:.0f} MB)")
                continue
            try:
                doc = json.loads(b.decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as e:
                errs.append(f"{p}: not a result JSON ({e})")
                continue
            parts = p.split("/")
            want = {"block": parts[1], "test": parts[2], "view": parts[3]}
            got = {k: (doc.get(k) if isinstance(doc, dict) else None) for k in want}
            if got != want:
                errs.append(f"{p}: block / test / view {got} do not match its path {want}")
            meta = doc.get("meta") if isinstance(doc, dict) else None
            if isinstance(meta, dict) and "verified_by" in meta:
                errs.append(f"{p}: meta.verified_by is not allowed in a candidate's result: the lead's "
                            "verification is a record in verification/ (adcflow verify), never in the result")
    return errs


def _blocks() -> dict:
    from .specs import blocks
    return blocks()


def disk_files(block: str, name: str) -> dict[str, bytes]:
    """Every file of a candidate on disk: its directory and its result directories."""
    out = {}
    roots = [candidate_dir(block, name)] + sorted((ROOT / "results" / block).glob(f"*/xtor-{name}"))
    for r in roots:
        for f in (sorted(r.rglob("*")) if r.is_dir() else []):
            if f.is_file():
                out[f.relative_to(ROOT).as_posix()] = f.read_bytes()
    return out


def disk_problems() -> list[str]:
    """tree_problems of every candidate in the repository, including result directories
    xtor-<name> whose candidate directory does not exist."""
    names = {(c.block, c.name) for c in candidates()}
    for d in (ROOT / "results").glob("*/*/xtor-*"):
        o = owner_of_path(d.relative_to(ROOT).as_posix() + "/x")
        if o:
            names.add(o)
    errs = []
    for b, n in sorted(names):
        if not candidate_dir(b, n).is_dir():
            errs.append(f"results/{b}/*/xtor-{n}/: no candidate design/xtor/{b}/{n}/")
        errs += tree_problems(b, n, disk_files(b, n))
    return errs


def _authors(text: str | None) -> list[dict] | None:
    """authors of a candidate.yaml text; None without a file."""
    if text is None:
        return None
    try:
        meta = yaml.safe_load(text)
    except yaml.YAMLError:
        return []
    a = meta.get("authors") if isinstance(meta, dict) else None
    return [x for x in a if isinstance(x, dict)] if isinstance(a, list) else []


def pr_problems(changed: list[str], author: str, base_text, head_files) -> list[str]:
    """The pull-request rules of §2 for the paths a PR changes (added, modified or deleted).

    A PR that changes no candidate path is a lead PR: no candidate rule applies (the lead reviews
    it). There is no exemption by login, the lead's account is also used by contributors: any PR
    that touches a candidate follows these rules. A candidate PR changes exactly one candidate and
    nothing outside its directory and its result directories (verification/, the lead's records of
    reruns, least of all). Its author is in the base authors of an existing candidate (whose authors
    it may not change, and which it may not delete), or, for a new candidate, in the new
    candidate.yaml, and the new name starts with the author's login.

    base_text(path) -> str | None: a file at the merge base; head_files(block, name) -> {path: bytes}:
    every file of the candidate in the PR head (for the content rules of tree_problems)."""
    owners = {p: owner_of_path(p) for p in changed}
    touched = sorted({o for o in owners.values() if o})
    if not touched:
        return []
    errs = []
    if len(touched) > 1:
        errs.append(f"the PR changes {len(touched)} candidates ({', '.join(f'{b}/{n}' for b, n in touched)}): "
                    "a candidate PR changes exactly one")
    for p, o in sorted(owners.items()):
        if o is None and p.startswith("verification/"):
            errs.append(f"{p}: verification records are written by the lead (adcflow verify) in a PR that "
                        "touches no candidate, never in a candidate PR")
        elif o is None:
            errs.append(f"{p}: a candidate PR may only change design/xtor/<block>/<name>/ and "
                        "results/<block>/<test>/xtor-<name>/ of its candidate")
    login = author.lower()
    for block, name in touched:
        y = f"design/xtor/{block}/{name}/candidate.yaml"
        base_authors = _authors(base_text(y))
        files = head_files(block, name)
        head_authors = _authors(files[y].decode("utf-8")) if y in files else None
        if base_authors is None:                                   # a new candidate
            if head_authors is None:
                errs.append(f"{y}: a new candidate needs candidate.yaml")
            elif login not in {str(a.get("github", "")).lower() for a in head_authors}:
                errs.append(f"{y}: the PR author @{author} must be in authors[].github of a new candidate")
            if not (name == login or name.startswith(login + "-")):
                errs.append(f"design/xtor/{block}/{name}: a new candidate's name starts with the PR author's "
                            f"login ({login} or {login}-<variant>)")
        else:
            if login not in {str(a.get("github", "")).lower() for a in base_authors}:
                errs.append(f"{block}/{name}: @{author} is not an author of this candidate (base candidate.yaml)")
            if head_authors is None:
                errs.append(f"{y}: a candidate PR may not delete a candidate (set status: withdrawn)")
            elif head_authors != base_authors:
                errs.append(f"{y}: authors may not change in a candidate PR; the lead changes them in a "
                            "PR that touches no candidate")
        errs += tree_problems(block, name, files)
    return errs
