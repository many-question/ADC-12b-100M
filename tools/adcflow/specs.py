"""Block specifications (specs/blocks/*.yaml): ports, limits and acceptance tests."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

from . import REPO_ROOT, numerics
from .corners import corner_names

BLOCK_DIR = REPO_ROOT / "specs" / "blocks"

PORT_DIRS = {"in", "out", "inout", "supply", "ground"}
PORT_TYPES = {"analog", "digital", "clock", "supply"}
SIDES = {"left", "right", "top", "bottom"}
STATUSES = {"behavioral", "xtor-review", "signoff"}    # docs/proposals/open-candidates.md §4 (no xtor-wip)
# a test's `montecarlo:` (one Spectre montecarlo analysis, runner.mc_settings); `models` names the
# statistical model sections of the site configuration (pdk.mc_sections)
MC_KEYS = {"runs", "seed", "variations", "models"}
MC_VARIATIONS = {"mismatch", "process", "all"}


@dataclass
class Port:
    name: str
    dir: str
    type: str
    side: str
    desc: str = ""
    bus: str | None = None


@dataclass
class Spec:
    id: str
    name: str
    metric: str
    unit: str
    corners: str
    test: str
    min: float | None = None
    max: float | None = None
    mc: int | None = None

    def check(self, value: float | None) -> bool:
        if value is None:
            return False
        if self.min is not None and value < self.min:
            return False
        if self.max is not None and value > self.max:
            return False
        return True

    def limit_text(self) -> str:
        if self.min is not None and self.max is not None:
            return f"{self.min} .. {self.max}"
        if self.min is not None:
            return f">= {self.min}"
        return f"<= {self.max}"

    def applies(self, corner, mc=None) -> bool:
        """Whether this spec judges a run at `corner` (a corner name or a Corner); `mc` is the
        Monte Carlo setting of the run (meta.mc: the run's montecarlo settings; empty for a
        nominal run).

        The one applicability rule of the flow (runner, check, report, figures, site): the corner
        is in the spec's corner set, expanded as `corner_set` does, and a Monte Carlo spec
        (`mc:`) judges Monte Carlo runs only; the other specs judge both."""
        if self.mc and not mc:
            return False
        return getattr(corner, "name", corner) in corner_names(self.corners)

    def samples(self, metrics: dict) -> dict | None:
        """Sample coverage of a Monte Carlo spec on the metrics of a run: {ok, failed, need}
        from the metrics `mc_ok` (valid samples) and `mc_failed` (failed or missing samples)
        that every Monte Carlo measure reports; None for a spec without `mc:`."""
        if not self.mc:
            return None
        ok, bad = metrics.get("mc_ok"), metrics.get("mc_failed")
        return {"ok": ok if isinstance(ok, int) else 0, "failed": bad if isinstance(bad, int) else None,
                "need": self.mc}

    def judge(self, metrics: dict) -> bool:
        """Pass of an applicable spec: the value within the limits and, for a Monte Carlo spec,
        at least `mc` valid samples and no failed or missing one (a failed sample is never
        dropped to pass: it fails the spec)."""
        ok = self.check(metrics.get(self.metric))
        n = self.samples(metrics)
        return ok and (n is None or (n["ok"] >= n["need"] and n["failed"] == 0))


@dataclass
class Block:
    name: str
    raw: dict
    ports: list[Port]
    specs: list[Spec]
    tests: dict = field(default_factory=dict)
    path: Path | None = None

    @property
    def status(self) -> str:
        return self.raw.get("status", "behavioral")

    @property
    def selected(self) -> str | None:
        """The selected candidate (`selected: <name>`), None for `selected: none` or no field
        (docs/proposals/open-candidates.md §4; every block except adc_top has the field)."""
        sel = self.raw.get("selected")
        return None if sel in (None, "none") else str(sel)

    @property
    def views(self) -> dict:
        return self.raw.get("views", {})

    @property
    def port_names(self) -> list[str]:
        return [p.name for p in self.ports]

    def view_path(self, view: str) -> Path:
        return REPO_ROOT / self.views[view]

    def verdicts(self, test: str, corner, mc, metrics: dict) -> tuple[dict, dict]:
        """The specs of `test` on the metrics of one run at `corner`.

        Returns (judged, na): judged = {id: {metric, value, limit, pass}} of the specs that apply
        (Spec.applies); na = {id: {metric, value, limit, corners}} of the specs that do not apply
        at this corner but whose metric was measured. Their raw values are kept and shown as N/A,
        never judged: they count for no worst value, failure or coverage. A Monte Carlo spec is
        left out of a nominal run altogether; on a Monte Carlo run its verdict also needs every
        sample (Spec.judge) and gives the sample coverage as `samples`."""
        judged, na = {}, {}
        for s in self.specs:
            if s.test != test:
                continue
            v = metrics.get(s.metric)
            if s.applies(corner, mc):
                judged[s.id] = {"metric": s.metric, "value": v, "limit": s.limit_text(), "pass": s.judge(metrics)}
                if s.mc:
                    judged[s.id]["samples"] = s.samples(metrics)
            elif v is not None and not (s.mc and not mc):
                na[s.id] = {"metric": s.metric, "value": v, "limit": s.limit_text(), "corners": s.corners}
        return judged, na


class SpecError(ValueError):
    pass


def _load_block(path: Path) -> Block:
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    errs = []
    for key in ("block", "title", "version", "status", "ports", "specs"):
        if key not in raw:
            errs.append(f"missing key {key!r}")
    if errs:
        raise SpecError(f"{path.name}: " + "; ".join(errs))
    owner, sel = raw.get("owner"), raw.get("selected")
    if raw.get("block") == "adc_top":                     # the lead's block: owner:, no candidates
        if not isinstance(owner, str) or not re.match(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$", owner):
            errs.append(f"adc_top needs owner: <GitHub login> (got {owner!r})")
        if sel is not None:
            errs.append("adc_top has no candidates: it keeps owner:, not selected:")
    else:
        if owner is not None:
            errs.append("owner: is retired for blocks: anyone may submit a candidate; the spec names the "
                        "selected one with `selected: <candidate>` or `selected: none` "
                        "(docs/proposals/open-candidates.md §4)")
        if not isinstance(sel, str) or not re.match(r"^(none|[a-z0-9-]{2,24})$", sel):
            errs.append(f"selected: must be `none` or a candidate name (got {sel!r})")
        elif sel == "none" and raw.get("status") != "behavioral":
            errs.append(f"status {raw.get('status')!r} needs a selected candidate (selected: none -> behavioral)")
    if raw["status"] not in STATUSES:
        errs.append(f"status {raw['status']!r} not in {sorted(STATUSES)}")
    ports = []
    seen = set()
    for p in raw["ports"]:
        port = Port(**{k: p[k] for k in ("name", "dir", "type", "side") if k in p},
                    desc=p.get("desc", ""), bus=p.get("bus"))
        if port.name in seen:
            errs.append(f"duplicate port {port.name}")
        seen.add(port.name)
        if port.dir not in PORT_DIRS:
            errs.append(f"port {port.name}: dir {port.dir!r}")
        if port.type not in PORT_TYPES:
            errs.append(f"port {port.name}: type {port.type!r}")
        if port.side not in SIDES:
            errs.append(f"port {port.name}: side {port.side!r}")
        ports.append(port)
    specs = []
    ids = set()
    tests = raw.get("tests", {}) or {}
    for s in raw["specs"]:
        try:
            spec = Spec(**s)
        except TypeError as e:
            errs.append(f"spec {s.get('id')}: {e}")
            continue
        if spec.id in ids:
            errs.append(f"duplicate spec id {spec.id}")
        ids.add(spec.id)
        if spec.min is None and spec.max is None:
            errs.append(f"spec {spec.id}: needs min or max")
        try:
            corner_names(str(spec.corners))
        except KeyError as e:
            errs.append(f"spec {spec.id}: corners {spec.corners!r}: {e}")
        if spec.test not in tests:
            errs.append(f"spec {spec.id}: test {spec.test!r} not defined in tests:")
        elif spec.mc and int((tests[spec.test].get("montecarlo") or {}).get("runs") or 0) < spec.mc:
            errs.append(f"spec {spec.id}: mc: {spec.mc} needs a test with `montecarlo:` of at least {spec.mc} runs")
        specs.append(spec)
    for tid, t in tests.items():
        if "netlist" not in t or "measure" not in t:
            errs.append(f"test {tid}: needs netlist and measure")
        if "numerics" in t:
            errs += numerics.validate(t["numerics"], f"test {tid}: numerics")
        if "crosscheck" in t:
            errs += numerics.validate(t["crosscheck"], f"test {tid}: crosscheck", ("samples",))
        if "montecarlo" in t:
            errs += _mc_problems(t["montecarlo"], f"test {tid}: montecarlo")
    if errs:
        raise SpecError(f"{path.name}: " + "; ".join(errs))
    return Block(name=raw["block"], raw=raw, ports=ports, specs=specs, tests=tests, path=path)


def _mc_problems(mc, where: str) -> list[str]:
    if not isinstance(mc, dict) or set(mc) != MC_KEYS:
        return [f"{where}: needs exactly {sorted(MC_KEYS)}"]
    out = []
    if not isinstance(mc["runs"], int) or mc["runs"] < 2:
        out.append(f"{where}: runs must be an integer >= 2")
    if not isinstance(mc["seed"], int) or mc["seed"] < 0:
        out.append(f"{where}: seed must be a non-negative integer (a fixed seed: reproducible samples)")
    if mc["variations"] not in MC_VARIATIONS:
        out.append(f"{where}: variations must be one of {sorted(MC_VARIATIONS)}")
    if not isinstance(mc["models"], str) or not re.match(r"^[a-z0-9_]+$", mc["models"]):
        out.append(f"{where}: models must name a pdk.mc_sections entry of the site configuration")
    return out


@lru_cache
def blocks() -> dict[str, Block]:
    out = {}
    for path in sorted(BLOCK_DIR.glob("*.yaml")):
        b = _load_block(path)
        if b.name != path.stem:
            raise SpecError(f"{path.name}: block name {b.name!r} must match the file name")
        out[b.name] = b
    return out


def find_test(test_id: str, block: str | None = None) -> tuple[Block, dict]:
    for b in blocks().values():
        if block and b.name != block:
            continue
        if test_id in b.tests:
            return b, b.tests[test_id]
    raise KeyError(f"test {test_id!r} not found in specs/blocks")
