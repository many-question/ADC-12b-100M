"""Per-device safe-operating-area (SOA) check of the thin-oxide MOS devices.

A block spec can require the SOA rule for every thin-oxide device and terminal pair
(|Vgs|, |Vgd|, |Vds|) over a whole transient, both polarities, edges included. A test
enables the check in its block spec (docs/verification.md §5):

    tests:
      tb_bootstrap_dc:
        soa: {dut: [XDUT], external: [MSWP]}

* ``dut``: testbench instances whose devices are checked (default: every instance of the
  block). The netlists of the run (the selected views) are flattened below them; every
  MOS master is classified with specs/soa.yaml: thin oxide is checked, thick oxide is
  skipped, any other MOS-like master makes the check unverified.
* ``external``: thin-oxide MOS devices of the testbench itself at the boundary of the DUT,
  such as a reference load switch (default: every one at the testbench top level). They
  are checked in every view.

``plan`` runs when the run deck is built: it lists the devices and the nodes on their
terminals, and the deck saves exactly those nodes (``Plan.save_lines``). ``check`` reads
their transient waveforms and returns, per device and terminal pair, the largest |V| over
every time point the simulator accepted, when it occurs, its time above the limit and
pass / fail.

For a test with ``soa: {remote: true}`` the waveforms of every device node are too large to
fetch: the runner makes the same check on the server (soa_core.py) and fetches its rows, the
signals the testbench saves itself and the nodes of the worst pair.

A DUT whose views are all behavioral has no devices: the scope is then ``external`` (the
boundary devices only), which is not transistor-level evidence. A behavioral DUT in a
testbench without thin-oxide devices at its top level (tb_clkgen_timing) has nothing to
check at all: the result says so explicitly (``soa_scope: external``, ``soa_pairs: 0``,
``soa_note``), it is not a device check. Whatever is missing (no plan, no thin-oxide device
under a transistor-level DUT, an unclassified MOS master, a node without a waveform,
waveforms that do not start at t = 0) raises ``Unverified``; a measure reports that as an
error, never as 0 violations.

The rule, a project decision (2026-11-02, #133; specs/soa_rule.yaml): a pair passes if its
largest |V| is at most limit_V (specs/soa.yaml, 1.1 V). It also passes if its largest |V| is
at most peak_V (1.29 V) and its time above limit_V is at most max_over_s (100 ps) in every
window_s (10 ns) window, sliding over the whole transient, start-up included. Anything else
is a violation. It replaces the #27 rule that a short excursion is never waived.

Each pair reports its total time above the limit (``t_over_ps``) and the time in its worst
window (``t_window_ps``), both linear between the saved points. ``violations`` applies the
rule to the recorded table when a result is judged, so specs/soa_rule.yaml makes no result
stale. A result recorded before the rule has no ``t_window_ps``: its total time is an upper
bound of every window, so a pair within the rule by that bound passes.

A result records the table packed (``pack_table``: the device, master and where of each device
once, one short row per pair), which keeps every field of every pair and is 2.5 times smaller than
one dict per pair (a result is limited to 1 MB: about 12 900 pairs instead of 5 100). Results
recorded before that hold the list of dicts. ``table_rows`` reads either form back as dicts:
every consumer goes through it.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

from . import REPO_ROOT, soa_core
from .netlist import ENDS_RE, INST_RE, SUBCKT_RE, Subckt, logical_lines, parse
from .soa_core import GROUND, PAIRS, key as _key, over_spans, worst_window  # noqa: F401

SOA_YAML = REPO_ROOT / "specs" / "soa.yaml"
RULE_YAML = REPO_ROOT / "specs" / "soa_rule.yaml"     # read when judging: not a dependency of any result
ROWS_FILE = "soa_rows.json"                           # a job's check made on the server (soa_core.py)
TERMINALS = {"mos": ("d", "g", "s", "b"), "moscap": ("p", "n")}
MAX_DEPTH = 32


class Unverified(RuntimeError):
    """The SOA check cannot be made: device data are missing or cannot be read."""


@lru_cache
def config() -> dict:
    with open(SOA_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache
def rule() -> dict:
    with open(RULE_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def classify(master: str) -> str | None:
    """'mos' / 'moscap' (thin oxide, checked), 'thick' (skipped), 'unknown' (looks like a MOS
    device but is not listed in specs/soa.yaml) or None (not a MOS device)."""
    c = config()
    for kind, names in c["thin_oxide"].items():
        if master in names:
            return kind
    if master in c["thick_oxide"]:
        return "thick"
    if re.search(c["mos_pattern"], master):
        return "unknown"
    return None


@dataclass
class Device:
    name: str                   # hierarchical instance name (XDUT.X1.M3), or the testbench name (MSWP)
    master: str
    kind: str                   # mos | moscap
    where: str                  # dut | external
    nodes: dict[str, str]       # terminal -> node as the deck saves it ("0" is ground)


@dataclass
class Plan:
    scope: str                  # device (devices under the DUT and external) | external (external only)
    limit_V: float
    duts: list[str] = field(default_factory=list)
    devices: list[Device] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)     # thick-oxide devices, "name (master)"
    problem: str | None = None                           # why the check cannot be made
    note: str | None = None                              # why there is nothing to check (external scope)

    def signals(self) -> list[str]:
        return sorted({n for d in self.devices for n in d.nodes.values() if n != GROUND})

    def save_lines(self, already: set[str] | frozenset = frozenset()) -> list[str]:
        """Deck lines that save the terminal nodes not saved by the testbench already."""
        sigs = [s for s in self.signals() if s not in already]
        if not sigs:
            return []
        out = [f"// adcflow SOA check: terminal nodes of {len(self.devices)} device(s), scope {self.scope}"]
        line = "save"
        for s in sigs:
            if len(line) + len(s) > 92:
                out.append(line + " \\")
                line = "    "
            line += " " + s
        return out + [line]


def _saved(tb_text: str) -> set[str]:
    out: set[str] = set()
    for _, line in logical_lines(tb_text):
        f = line.split()
        if f and f[0] == "save":
            out.update(f[1:])
    return out


def _unparsed(text: str, names: set[str]) -> list[str]:
    """Lines inside the subcircuits `names` that name a MOS model but are not read as an
    instance (e.g. written without parentheses): such a device would escape the check."""
    out, cur = [], None
    for ln, line in logical_lines(text):
        m = SUBCKT_RE.match(line)
        if m:
            cur = m.group(1)
            continue
        if ENDS_RE.match(line):
            cur = None
            continue
        if cur in names and not INST_RE.match(line) and any(classify(w) for w in re.findall(r"[\w!]+", line)):
            out.append(f"{cur} line {ln}: {line.strip()[:40]!r} not read as an instance")
    return out


def plan(block: str, test: dict, tb_text: str, netlists: list[Path], views: dict[str, str]) -> Plan:
    """Devices and nodes of the SOA check of one testbench run.

    netlists: the view files of the run (the subcircuits below a DUT instance); views: the
    view of every block that does not use its behavioral view (as for the runner).
    A wrong `dut` / `external` name in the spec raises ValueError (before simulating)."""
    from .specs import blocks

    cfg = test.get("soa")
    cfg = dict(cfg) if isinstance(cfg, dict) else {}
    tb = parse("tb.scs", text=tb_text)
    top = {i.name: i for i in tb.top_instances}
    subckts: dict[str, Subckt] = {}
    texts: dict[str, str] = {}                           # subcircuit -> text of the file that defines it
    for path in netlists:
        text = Path(path).read_text(encoding="utf-8")
        found = parse(path, text=text).subckts
        subckts.update(found)
        texts.update({name: text for name in found})
    subckts.update(tb.subckts)
    texts.update({name: tb_text for name in tb.subckts})
    visited: set[str] = set()
    duts = list(cfg.get("dut") or [i.name for i in tb.top_instances if i.master == block])
    p = Plan(scope="external", limit_V=float(config()["limit_V"]), duts=duts)
    unknown: list[str] = []
    xtor = False

    def walk(sc: Subckt, prefix: str, netmap: dict[str, str], depth: int) -> None:
        nonlocal xtor
        if depth > MAX_DEPTH:
            unknown.append(f"{prefix}: hierarchy deeper than {MAX_DEPTH}")
            return
        visited.add(sc.name)
        for i in sc.instances:
            name = f"{prefix}.{i.name}"
            nodes = [netmap.get(n, n if n == GROUND else f"{prefix}.{n}") for n in i.nodes]
            kind = classify(i.master)
            if kind in TERMINALS:
                if len(nodes) != len(TERMINALS[kind]):
                    unknown.append(f"{name} ({i.master}): {len(nodes)} terminals")
                    continue
                p.devices.append(Device(name, i.master, kind, "dut", dict(zip(TERMINALS[kind], nodes))))
            elif kind == "thick":
                p.skipped.append(f"{name} ({i.master})")
            elif kind == "unknown":
                unknown.append(f"{name} ({i.master})")
            elif i.master in subckts:
                if i.master in blocks() and views.get(i.master, "behav") != "behav":
                    xtor = True
                sub = subckts[i.master]
                walk(sub, name, dict(zip(sub.ports, nodes)), depth + 1)

    for name in duts:
        inst = top.get(name)
        if inst is None:
            raise ValueError(f"soa: DUT instance {name!r} is not in the testbench")
        if inst.master in blocks() and views.get(inst.master, "behav") != "behav":
            xtor = True
        sc = subckts.get(inst.master)
        if sc is None:
            unknown.append(f"{name}: subcircuit {inst.master} not found in the netlists of the run")
            continue
        walk(sc, name, dict(zip(sc.ports, inst.nodes)), 1)
    for text in {id(texts[n]): texts[n] for n in visited}.values():
        unknown += _unparsed(text, visited)
    p.scope = "device" if xtor or p.devices else "external"
    ext = cfg.get("external")
    if ext is None:
        ext = [i.name for i in tb.top_instances if classify(i.master) in TERMINALS]
        unknown += [f"{i.name} ({i.master})" for i in tb.top_instances if classify(i.master) == "unknown"]
    for name in ext:
        inst = top.get(name)
        kind = classify(inst.master) if inst else None
        if kind not in TERMINALS:
            raise ValueError(f"soa: external device {name!r} is not a thin-oxide device of the testbench")
        p.devices.append(Device(name, inst.master, kind, "external", dict(zip(TERMINALS[kind], inst.nodes))))
    if unknown:
        p.problem = (f"{len(unknown)} instance(s) cannot be resolved (MOS models must be listed in "
                     "specs/soa.yaml): " + "; ".join(unknown[:6]))
    elif xtor and not any(d.where == "dut" for d in p.devices):
        p.problem = f"no thin-oxide device found under {', '.join(duts)} (transistor-level view)"
    elif not p.devices:
        p.note = (f"nothing to check: {', '.join(duts)} uses behavioral views (no devices) and the testbench "
                  "has no thin-oxide device at its top level; not transistor-level evidence")
    return p


def deck_lines(pl: Plan, tb_text: str) -> list[str]:
    return pl.save_lines(_saved(tb_text))


def remote_plan(pl: Plan, tb_text: str) -> dict | None:
    """soa_plan.json of a job for the check on the server (soa_core.reduce_job); None when there is
    nothing to read there (no device, or the check cannot be made anyway)."""
    if pl.problem or not pl.devices:
        return None
    return {"limit_V": pl.limit_V, "rule": rule(), "keep": sorted(_saved(tb_text)),
            "devices": [{"name": d.name, "master": d.master, "kind": d.kind, "where": d.where, "nodes": d.nodes}
                        for d in pl.devices]}


def check(pl: Plan | None, w: dict[str, np.ndarray], remote: dict | None = None) -> dict:
    """SOA metrics from the transient waveforms `w` (psf.read of the tran results), or from the rows
    of the check made on the server (`remote`, soa_rows.json) when `w` is only a thin part of them.

    soa_violations is the number of device / terminal pairs outside the rule (module docstring);
    soa_table lists every pair, packed (pack_table). Raises Unverified when the check cannot be made."""
    if pl is None:
        raise Unverified("no SOA plan for this run (the deck saved no device nodes)")
    if pl.problem:
        raise Unverified(pl.problem)
    t = w.get("time")
    if t is None or len(t) < 2:
        raise Unverified("no transient waveforms")
    t_start = remote["t_start"] if remote else t[0]
    if t_start > 1e-15:
        raise Unverified(f"the waveforms start at {t_start * 1e9:g} ns: the check needs the whole transient")
    missing = (remote["missing"] if remote else
               [s for s in pl.signals() if _key(s) not in w or len(w[_key(s)]) != len(t)])
    if missing:
        raise Unverified(f"{len(missing)} device node(s) without a waveform: {', '.join(missing[:6])}")
    dt = np.diff(t)
    r = rule()
    base = {"soa_scope": pl.scope, "soa_limit_V": pl.limit_V, "soa_peak_V": r["peak_V"],
            "soa_window_ns": round(r["window_s"] * 1e9, 6), "soa_max_over_ps": round(r["max_over_s"] * 1e12, 6),
            "soa_devices": len(pl.devices),
            "soa_devices_dut": sum(d.where == "dut" for d in pl.devices)}
    if not pl.devices:                                   # external scope without devices: said, not hidden
        return {**base, "soa_pairs": 0, "soa_violations": 0, "soa_note": pl.note or "no device in scope",
                "soa_points": int(len(t)), "soa_dt_max_ps": round(float(dt.max()) * 1e12, 3), "soa_table": []}
    if remote:
        rows = remote["rows"]
        if len(rows) != sum(len(PAIRS[d.kind]) for d in pl.devices):
            raise Unverified(f"{len(rows)} rows from the server for a plan of {len(pl.devices)} device(s)")
    else:
        rows = soa_core.pair_rows([{"name": d.name, "master": d.master, "kind": d.kind, "where": d.where, "nodes": d.nodes}
                                   for d in pl.devices], t, w, pl.limit_V, r)
    worst = max(rows, key=lambda r: r["max_V"])
    out = {**base, "soa_pairs": len(rows), "soa_violations": sum(not r["pass"] for r in rows),
           "soa_max_V": worst["max_V"], "soa_window_max_ps": max(r["t_window_ps"] for r in rows),
           "soa_worst": {k: worst[k] for k in ("device", "pair", "signed_V", "t_ns", "dt_ps", "t_over_ps", "t_window_ps")},
           "soa_points": remote["points"] if remote else int(len(t)),
           "soa_dt_max_ps": remote["dt_max_ps"] if remote else round(float(dt.max()) * 1e12, 3)}
    if remote:
        out["soa_waveform_MB"] = round(remote["size_bytes"] / 1e6, 1)     # read on the server, not fetched
    if pl.skipped:
        out["soa_skipped"] = list(pl.skipped)
    out["soa_table"] = pack_table(rows)
    return out


# ------------------------------------------------------------------ the recorded table
TABLE_DEVICE = ("device", "master", "where")             # what a pair has from its device, recorded once per device


def pack_table(rows: list[dict]) -> dict | list:
    """The soa_table that a result records, from the rows of pair_rows (one dict per pair), keeping every
    field of every pair: ``devices`` lists each device's [device, master, where] once, ``columns`` names the
    fields of a row ("device" first, the index into ``devices``) and ``rows`` has one list per pair, in
    the order of the pairs. Empty without rows. All rows must have the same fields."""
    if not rows:
        return []
    fields = [k for k in rows[0] if k not in TABLE_DEVICE]
    index: dict[tuple, int] = {}
    devices, out = [], []
    for r in rows:
        if r.keys() != rows[0].keys():
            raise ValueError("soa_table: the rows do not all have the same fields")
        key = tuple(r[k] for k in TABLE_DEVICE)
        if key not in index:
            index[key] = len(devices)
            devices.append(list(key))
        out.append([index[key]] + [r[k] for k in fields])
    return {"devices": devices, "columns": ["device", *fields], "rows": out}


def table_rows(metrics: dict) -> list[dict]:
    """The pairs of a result's soa_table as dicts (device, master, where, pair, max_V, signed_V, t_ns, dt_ps,
    t_over_ps, t_window_ps, pass), from either recorded form: the list of dicts of the results recorded
    before pack_table, or the packed table. A result without a table, or with an empty one, has none."""
    table = metrics.get("soa_table")
    if not table:
        return []
    if isinstance(table, list):
        return table
    devices, columns = table["devices"], table["columns"]
    if columns[0] != "device":
        raise ValueError(f"soa_table: the first column is {columns[0]!r}, not 'device'")
    return [{**dict(zip(TABLE_DEVICE, devices[row[0]])), **dict(zip(columns[1:], row[1:]))} for row in table["rows"]]


def passes(vmax: float, window: float, limit: float) -> bool:
    """The rule for one pair: its largest |V| and its time above `limit` in its worst window (s)."""
    return soa_core.passes(vmax, window, limit, rule())


def time_over(t: np.ndarray, x: np.ndarray, limit: float) -> float:
    """Total time (s) during which |x| > limit, x linear between the saved points."""
    spans = over_spans(t, x, limit)
    return float((spans[:, 1] - spans[:, 0]).sum())


def violations(metrics: dict) -> int | None:
    """soa_violations by the current rule from a recorded soa_table (when a result is judged);
    None without a table, then the recorded metric stands. A window recorded for another length,
    or none at all, is replaced by the total time above the limit, its upper bound."""
    table = table_rows(metrics)
    limit = metrics.get("soa_limit_V")
    if not table or limit is None:
        return None
    same = metrics.get("soa_window_ns") == round(rule()["window_s"] * 1e9, 6)
    n = 0
    for r in table:
        window = r.get("t_window_ps") if same else None
        over = r.get("t_over_ps") if window is None else window
        n += not passes(r["max_V"], float("inf") if over is None else over * 1e-12, limit)
    return n


def measure(ctx: dict, w: dict[str, np.ndarray], m: dict, job_dir: Path | None = None) -> None:
    """Add the SOA metrics to `m`, or the error that says why they could not be made. A job
    in `job_dir` that was checked on the server has its rows there (ROWS_FILE)."""
    try:
        f = Path(job_dir) / ROWS_FILE if job_dir else None
        m.update(check(ctx.get("soa"), w, json.loads(f.read_text(encoding="utf-8")) if f and f.exists() else None))
    except Unverified as e:
        m["error"] = f"SOA unverified: {e}"


# ------------------------------------------------------------------ figure
def figure(fg, ctx: dict, m: dict, w: dict[str, np.ndarray], nbars: int = 18) -> None:
    """Largest |V| per device and terminal pair against both limits of the rule, the worst pair
    over the whole run, and the worst peak with the saved time points (the time resolution)."""
    from .figures import C1, C2, C3, LIMIT, MUTED, hline, note, vline

    pl: Plan = ctx["soa"]
    rows = sorted(table_rows(m), key=lambda r: -r["max_V"])
    if not rows:                                         # nothing to check: the measure's own figure says so
        return
    lim = pl.limit_V
    peak, over_max = m.get("soa_peak_V", rule()["peak_V"]), m.get("soa_max_over_ps", rule()["max_over_s"] * 1e12)
    window_ns = m.get("soa_window_ns", rule()["window_s"] * 1e9)
    fig, axs = fg.new(1, 3, size=(16.0, 4.9), gridspec_kw={"width_ratios": [1.25, 1, 1]})
    ax = axs[0, 0]
    shown = rows[:nbars][::-1]
    y = np.arange(len(shown))
    ax.barh(y, [r["max_V"] for r in shown], color=[C1 if r["pass"] else LIMIT for r in shown], height=0.7)
    ax.set_yticks(y, [f"{r['device']} |V{r['pair']}|" + (" (ext)" if r["where"] == "external" else "")
                      for r in shown], fontsize=7)
    ax.axvline(lim, color=LIMIT, lw=1.1, ls="--")
    ax.text(lim, 0.99, f" limit {lim:.1f} V", transform=ax.get_xaxis_transform(), ha="left", va="top",
            fontsize=7.5, color=LIMIT)
    ax.axvline(peak, color=LIMIT, lw=1.1, ls=":")
    ax.text(peak, 0.92, f" transient {peak:.2f} V\n <= {over_max:.0f} ps in {window_ns:.0f} ns", ha="left", va="top",
            transform=ax.get_xaxis_transform(), fontsize=7.5, color=LIMIT)
    for yi, r in zip(y, shown):                           # how long above the limit, in the worst window
        if r.get("t_over_ps"):
            ax.text(r["max_V"], yi, f" {r.get('t_window_ps', r['t_over_ps']):.1f} ps in window", va="center",
                    fontsize=6.5, color=LIMIT)
    ax.set(xlabel="largest |V| over the whole run (V)", xlim=(0, max(peak, rows[0]["max_V"]) * 1.2),
           title=f"Per-device SOA ({len(shown)} of {len(rows)} pairs, worst first)")
    ax.grid(axis="y", visible=False)
    ndut = m.get("soa_devices_dut", 0)
    ext = ", ".join(d.name for d in pl.devices if d.where == "external")
    if pl.scope == "device":
        scope = f"scope: {ndut} thin-oxide device(s) in {', '.join(pl.duts)}" + (f"\n+ boundary: {ext}" if ext else "")
    else:
        scope = f"scope: external, boundary device(s) {ext} only\n(behavioral DUT: not transistor-level evidence)"
    note(ax, f"{scope}\nviolations {m['soa_violations']} of {m['soa_pairs']} pairs", loc="lower right")
    # the worst pair over time
    wr = rows[0]
    d = next(x for x in pl.devices if x.name == wr["device"])
    a, b = next((a, b) for p, a, b in PAIRS[d.kind] if p == wr["pair"])
    t = w["time"]
    zero = np.zeros_like(t)
    x = (zero if d.nodes[a] == GROUND else w[_key(d.nodes[a])]) - (zero if d.nodes[b] == GROUND else w[_key(d.nodes[b])])
    ax = axs[0, 1]
    ax.plot(t * 1e9, x, color=C1, lw=0.8, label=f"V{wr['pair']} (signed)")
    hline(ax, lim, f"+{lim:.1f} V")
    hline(ax, -lim, f"-{lim:.1f} V")
    hline(ax, peak, f"+{peak:.2f} V", ls=":")
    hline(ax, -peak, f"-{peak:.2f} V", ls=":")
    ax.plot([wr["t_ns"]], [wr["signed_V"]], "o", color=C2, ms=5)
    top = max(peak * 1.1, wr["max_V"] * 1.1)
    ax.set(xlabel="time (ns)", ylabel="voltage (V)", title=f"Worst pair: {wr['device']} V{wr['pair']}",
           ylim=(-top, top))
    ax.legend(loc="upper right")
    # zoom on the time of its maximum with the saved time points
    ax = axs[0, 2]
    tk = wr["t_ns"] * 1e-9
    sel = (t > tk - 150e-12) & (t < tk + 150e-12)
    ax.plot((t[sel] - tk) * 1e12, np.abs(x[sel]), "-", color=C1, lw=1.0)
    ax.plot((t[sel] - tk) * 1e12, np.abs(x[sel]), ".", color=C3, ms=3.5, label="saved time points")
    hline(ax, lim, f"limit {lim:.1f} V", x=0.7)
    hline(ax, peak, f"transient {peak:.2f} V", x=0.7, ls=":")
    vline(ax, 0.0, None, color=MUTED, ls=":")
    ax.set(xlabel=f"time from the maximum at {wr['t_ns']:.3f} ns (ps)", ylabel="|V| (V)",
           title="Worst maximum and the time resolution", xlim=(-150, 150), ylim=(0, top))
    ax.legend(loc="lower right")
    note(ax, f"max |V{wr['pair']}| = {wr['max_V']:.4f} V\nlocal step {wr['dt_ps']:.2f} ps\n"
         f"time above the limit: {wr.get('t_over_ps', 0.0):.1f} ps in all, "
         f"{wr.get('t_window_ps', 0.0):.1f} ps in the worst {window_ns:.0f} ns window (max {over_max:.0f} ps)\n"
         f"{m['soa_points']} time points, largest step {m['soa_dt_max_ps']:.0f} ps", loc="lower left")
    fg.save(fig, "soa", f"Largest |Vgs|, |Vgd|, |Vds| of every checked device against the {lim:.1f} V limit and the "
            f"{peak:.2f} V transient limit (at most {over_max:.0f} ps above {lim:.1f} V in any {window_ns:.0f} ns window; "
            f"scope: {pl.scope}), the worst pair over the whole run, and the saved time points around the "
            "time of its maximum, which set the time resolution.")
