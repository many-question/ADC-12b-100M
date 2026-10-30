"""Verification combinations of the top level: which blocks are transistor level in a mixed adc_top run, and what those runs show.

Rows come from the result directories `results/adc_top/<test>/<view signature>/` (the signature is the one of
`adcflow.candidates.top_signature`: `behav`, `xtor` (every block on its legacy view) or `xtor-<blk>[@<candidate>]+...`), never from
a list. Judging is `adcflow.checks.judge` (already applied by the site's data layer: `doc["_judged"]`), the verification state of
the transistor-level blocks is the candidates' own (`adcflow.verify.state` through the leaderboard row); nothing is judged here.
No matplotlib is imported (the site build installs the core package only).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

TOP = "adc_top"
KEY_SPECS = ["TOP-01", "TOP-03", "TOP-06", "TOP-08", "TOP-09", "TOP-10"]       # worst ENOB, SFDR, conversion time, low-frequency ENOB, duty ENOB, spikes
POWER_KEY = re.compile(r"^p_([a-z0-9]+)_mW$")


@dataclass
class BlockState:
    block: str
    candidate: str | None                  # None: the block's legacy single xtor view
    author_text: str = ""                  # `name (@login)`, from candidate.yaml (empty when the candidate is not merged)
    selected: bool = False                 # the block spec's `selected:`
    merged: bool = True                    # False: only in an open PR
    pr: int | None = None
    verification: str = "unknown"          # verified | self-reported | mixed | unknown
    verified: int = 0
    results: int = 0


@dataclass
class TestCov:
    test: str
    corners: int                           # distinct corners with a result
    required: int                          # corners the test's specs require
    results: int                           # result files (a test may run several cases per corner)
    need: list[str] = field(default_factory=list)
    got: list[str] = field(default_factory=list)


@dataclass
class Metric:
    spec: str
    name: str
    unit: str
    value: float
    corner: str
    limit: str
    margin: float | None                   # towards the violated side: limit - value for a max, value - limit for a min; negative fails


@dataclass
class Combo:
    signature: str
    xtor: list[BlockState]                 # the transistor-level blocks; the others are behavioral
    legacy: bool = False                   # signature `xtor`: every block on its legacy single view
    tests: list[TestCov] = field(default_factory=list)
    specs_pass: int = 0
    specs_applicable: int = 0              # specs (with a limit) judged at the covered corners
    specs_total: int = 0                   # specs of adc_top with a limit
    failing: list[str] = field(default_factory=list)
    metrics: list[Metric] = field(default_factory=list)
    power: dict[str, float] = field(default_factory=dict)      # supply -> mW at `power_corner`
    power_corner: str = ""
    results: int = 0
    stale: int = 0                         # result files whose inputs changed since the simulation
    errors: int = 0
    dirs: dict[str, str] = field(default_factory=dict)         # test -> repo path of its result directory

    @property
    def n_xtor(self) -> int:
        return len(self.xtor)

    @property
    def full(self) -> bool:
        """Every test covers every corner its specs require (a sign-off run); else a regression subset."""
        return bool(self.tests) and all(t.corners >= t.required for t in self.tests)


def parse_signature(sig: str, blocks: list[str]) -> tuple[list[tuple[str, str | None]], bool] | None:
    """The transistor-level blocks of a signature as [(block, candidate or None)], and whether it is the legacy `xtor` (every block);
    None for `behav`, for a signature that does not parse or names an unknown block. The inverse of candidates.top_signature."""
    if sig == "behav":
        return [], False
    if sig == "xtor":
        return [(b, None) for b in blocks], True
    if not sig.startswith("xtor-"):
        return None
    out = []
    for term in sig[5:].split("+"):
        blk, _, name = term.partition("@")
        block = f"adc_{blk}"
        if not blk or block not in blocks or (name and not re.fullmatch(r"[a-z0-9-]{2,24}", name)):
            return None
        out.append((block, name or None))
    return out, False


def _worst(spec, values: list[tuple[float, str]]) -> tuple[float, str]:
    """The value of a spec that is closest to (or past) its limit, with its corner."""
    if spec.min is not None and spec.max is None:
        return min(values)
    if spec.max is not None and spec.min is None:
        return max(values)
    mid = (spec.min + spec.max) / 2
    return max(values, key=lambda v: abs(v[0] - mid))


def _margin(spec, v: float) -> float | None:
    out = []
    if spec.max is not None:
        out.append(spec.max - v)
    if spec.min is not None:
        out.append(v - spec.min)
    return min(out) if out else None


def block_state(block: str, name: str | None, selected_of, cands: dict[str, list]) -> BlockState:
    """What the site knows of a transistor-level block of a combination: its candidate (merged, or in an open PR), whether the block
    spec selected it, and how its own results are verified (the leaderboard row: adcflow.verify.state)."""
    st = BlockState(block, name, selected=bool(name) and selected_of(block) == name)
    if name is None:
        return st
    found = next((c for c in cands.get(block, []) if c.name == name and c.source == "main"), None)
    if found is None:
        pr = next((c for c in cands.get(block, []) if c.name == name and c.source == "pr"), None)
        st.merged = False
        if pr is not None:
            st.pr, st.author_text = pr.pr.number, pr.row["author_text"]
        return st
    r = found.row
    st.author_text, st.results, st.verified = r["author_text"], r["results"], r["verified"]
    if not r["results"]:
        st.verification = "unknown"
    elif r["verified"] == r["results"]:
        st.verification = "verified"
    elif r["verified"] == 0:
        st.verification = "self-reported"
    else:
        st.verification = "mixed"
    return st


def build(docs: list[dict], top, blocks: list[str], selected_of, cands: dict[str, list] | None = None) -> list[Combo]:
    """One Combo per view signature found under results/adc_top/<test>/<signature>/.

    `docs`: the judged result docs (`_judged` from checks.judge, `_path` the file), `top`: the adc_top Block (its specs), `blocks`:
    the names of the blocks that can have a transistor-level view, `selected_of(block)`: the block's selected candidate, `cands`:
    the site's candidates by block (for the display name and verification of each transistor-level block)."""
    from adcflow.corners import corner_names

    cands = cands or {}
    need: dict[str, set[str]] = {}
    for s in top.specs:
        if not s.mc:
            need.setdefault(s.test, set()).update(corner_names(s.corners))
    limited = [s for s in top.specs if not s.reported]
    by_sig: dict[str, list[dict]] = {}
    for d in docs:
        if d.get("block") == TOP:
            by_sig.setdefault(Path(d["_path"]).parent.name, []).append(d)
    out = []
    for sig, group in by_sig.items():
        parsed = parse_signature(sig, blocks)
        if parsed is None:
            continue
        terms, legacy = parsed
        c = Combo(sig, [block_state(b, n, selected_of, cands) for b, n in terms], legacy, specs_total=len(limited))
        per_spec: dict[str, list[tuple[float, str, bool]]] = {}
        verdicts: dict[str, list[bool]] = {}
        for d in group:
            j = d["_judged"]
            c.results += 1
            c.stale += bool(j["stale"])
            c.errors += bool(j["error"])
            for sid, v in j["specs"].items():
                if v.get("pass") is None:                          # reported only: no verdict
                    continue
                verdicts.setdefault(sid, []).append(bool(v["pass"]))
                if isinstance(v.get("value"), (int, float)):
                    per_spec.setdefault(sid, []).append((float(v["value"]), d["corner"], bool(v["pass"])))
        c.specs_applicable = len(verdicts)
        c.specs_pass = sum(all(v) for v in verdicts.values())
        c.failing = sorted(sid for sid, v in verdicts.items() if not all(v))
        for t in sorted(need):
            ds = [d for d in group if d["test"] == t]
            if not ds:
                continue
            got = {d["corner"] for d in ds}
            c.tests.append(TestCov(t, len(got & need[t]) if need[t] else len(got), len(need[t]), len(ds), sorted(need[t]), sorted(got)))
            c.dirs[t] = f"results/{TOP}/{t}/{sig}"
        specs_by_id = {s.id: s for s in top.specs}
        for sid in KEY_SPECS:
            s, vals = specs_by_id.get(sid), per_spec.get(sid)
            if s is None or not vals:
                continue
            v, corner = _worst(s, [(x, k) for x, k, _ in vals])
            c.metrics.append(Metric(sid, s.name, s.unit, v, corner, s.limit_text(), _margin(s, v)))
        _power(c, group)
        out.append(c)
    out.sort(key=lambda c: (c.n_xtor, c.signature != "behav", c.signature))
    return out


def _power(c: Combo, group: list[dict]) -> None:
    """Supply power the results record (metrics p_<supply>_mW): at the typical corner when there is a result for it, else the largest."""
    best = None
    for d in group:
        m = {k: v for k, v in d["metrics"].items() if POWER_KEY.match(k) and isinstance(v, (int, float))}
        if not m:
            continue
        total = sum(m.values())
        key = (d["corner"] == "tt_nom_27", total)
        if best is None or key > best[0]:
            best = (key, d["corner"], m)
    if best:
        c.power_corner = best[1]
        c.power = {POWER_KEY.match(k).group(1): v for k, v in sorted(best[2].items())}
