"""``python -m adcflow report``: recorded results against the specs, per block and view."""

from __future__ import annotations

from dataclasses import dataclass, field

from .checks import judge, load_results
from .corners import corner_names
from .specs import Spec, blocks


def _fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


@dataclass
class SpecSummary:
    """One spec over the judged results of one block view."""
    spec: Spec
    vals: list[tuple[str, object, bool, bool]] = field(default_factory=list)  # applicable: corner, value, pass, stale
    na: list[tuple[str, object]] = field(default_factory=list)                 # not applicable: corner, raw value
    samples: list[dict] = field(default_factory=list)                          # Monte Carlo spec: Spec.samples per result

    def _worst(self, nums: list[float]) -> float | None:
        if not nums:
            return None
        return max(nums) if self.spec.max is not None else min(nums)

    @property
    def worst(self) -> float | None:
        return self._worst([v for _, v, _, _ in self.vals if isinstance(v, (int, float))])

    @property
    def na_worst(self) -> float | None:
        return self._worst([v for _, v in self.na if isinstance(v, (int, float))])

    @property
    def status(self) -> str:
        """pass | fail | none (no result at an applicable corner)."""
        if not self.vals:
            return "none"
        return "pass" if all(p for _, _, p, _ in self.vals) else "fail"

    @property
    def stale(self) -> bool:
        return any(st for *_, st in self.vals)

    @property
    def covered(self) -> int:
        """Unique applicable corners with a result (variants of a corner count once)."""
        return len({c for c, *_ in self.vals})

    @property
    def need(self) -> int:
        return len(corner_names(self.spec.corners))


def summarize(spec: Spec, judged: list[tuple[dict, dict]]) -> SpecSummary:
    """Collect the results of the spec's test: those at corners where the spec applies
    (Spec.applies) give the worst value, the verdict and the coverage; the others are kept
    as N/A with their raw values. A Monte Carlo spec ignores nominal runs."""
    out = SpecSummary(spec)
    for d, j in judged:
        if d["test"] != spec.test:
            continue
        if spec.applies(d["corner"], d.get("meta", {}).get("mc")):
            v = j["specs"].get(spec.id, {})
            out.vals.append((d["corner"], v.get("value"), bool(v.get("pass")), bool(j["stale"])))
            if v.get("samples"):
                out.samples.append(v["samples"])
        elif spec.id in j.get("na", {}):
            out.na.append((d["corner"], j["na"][spec.id]["value"]))
    return out


def report(block: str | None = None) -> int:
    docs = load_results()
    idx: dict = {}
    for d in docs:
        idx.setdefault((d["block"], d["view"]), []).append((d, judge(d)))
    for b in blocks().values():
        if block and b.name != block:
            continue
        views = sorted({v for (bn, v) in idx if bn == b.name})
        print(f"\n== {b.name} ({b.status}) -- {b.raw['title']}")
        if not views:
            print("   no recorded results")
            continue
        for view in views:
            rows = idx[(b.name, view)]
            print(f"   view {view}:")
            print(f"   {'spec':8s} {'limit':>16s} {'worst':>10s} {'pass':>6s} {'corners':>9s}  test")
            for s in b.specs:
                r = summarize(s, rows)
                if r.status == "none":
                    flag = f"MC{s.mc}" if s.mc else "-"
                else:
                    flag = ("PASS" if r.status == "pass" else "FAIL") + ("*" if r.stale else "")
                na = (f"  [n/a at {len(r.na)} corner(s) outside {s.corners}, worst {_fmt(r.na_worst)}: not judged]"
                      if r.na else "")
                mc = "".join(f"  [MC samples {n['ok']}/{n['need']} valid, {n['failed']} failed]" for n in r.samples)
                print(f"   {s.id:8s} {s.limit_text():>16s} {_fmt(r.worst):>10s} {flag:>6s} "
                      f"{r.covered:>4d}/{r.need:<4d}  {s.test}{mc}{na}")
            for d, j in rows:                         # never hidden by the corner sets of the specs
                where = f"{d['test']}/{d['_path'].stem}"
                if j["error"]:
                    print(f"   error  {where}: {str(j['error'])[:160]}")
                if j["stale"]:
                    print(f"   stale  {where}: {', '.join(j['stale'][:3])}")
    print("\n(worst, pass and corners count only the results at corners in a spec's corner set; corners = "
          "unique such corners recorded / the set. n/a = raw values at other corners, not judged. "
          "* = stale: a file changed after the simulation. Errors and stale results are listed per view.)")
    return 0
