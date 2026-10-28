"""Per-device safe-operating-area (SOA) check of the thin-oxide MOS devices.

A block spec can require |Vgs|, |Vgd|, |Vds| <= limit for every thin-oxide device over
a whole transient, both polarities, edges included. A test enables the check in its
block spec (docs/verification.md §5):

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
every time point the simulator accepted, when it occurs, and pass / fail.

A DUT whose views are all behavioral has no devices: the scope is then ``external`` (the
boundary devices only), which is not transistor-level evidence. Whatever is missing (no
plan, no thin-oxide device under a transistor-level DUT, an unclassified MOS master, a
node without a waveform, waveforms that do not start at t = 0) raises ``Unverified``; a
measure reports that as an error, never as 0 violations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

from . import REPO_ROOT
from .netlist import ENDS_RE, INST_RE, SUBCKT_RE, Subckt, logical_lines, parse

SOA_YAML = REPO_ROOT / "specs" / "soa.yaml"
TERMINALS = {"mos": ("d", "g", "s", "b"), "moscap": ("p", "n")}
PAIRS = {"mos": (("gs", "g", "s"), ("gd", "g", "d"), ("ds", "d", "s")), "moscap": (("pn", "p", "n"),)}
GROUND = "0"
MAX_DEPTH = 32


class Unverified(RuntimeError):
    """The SOA check cannot be made: device data are missing or cannot be read."""


@lru_cache
def config() -> dict:
    with open(SOA_YAML, encoding="utf-8") as f:
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


def _key(node: str) -> str:
    """Waveform name of a node as written in a netlist (PSF names carry no escapes)."""
    return node.replace("\\<", "<").replace("\\>", ">").replace("\\\\", "\\")


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
        p.problem = "no device to check"
    return p


def deck_lines(pl: Plan, tb_text: str) -> list[str]:
    return pl.save_lines(_saved(tb_text))


def check(pl: Plan | None, w: dict[str, np.ndarray]) -> dict:
    """SOA metrics from the transient waveforms `w` (psf.read of the tran results).

    soa_violations is the number of device / terminal pairs whose largest |V| exceeds the
    limit; soa_table lists every pair. Raises Unverified when the check cannot be made."""
    if pl is None:
        raise Unverified("no SOA plan for this run (the deck saved no device nodes)")
    if pl.problem:
        raise Unverified(pl.problem)
    t = w.get("time")
    if t is None or len(t) < 2:
        raise Unverified("no transient waveforms")
    if t[0] > 1e-15:
        raise Unverified(f"the waveforms start at {t[0] * 1e9:g} ns: the check needs the whole transient")
    missing = [s for s in pl.signals() if _key(s) not in w or len(w[_key(s)]) != len(t)]
    if missing:
        raise Unverified(f"{len(missing)} device node(s) without a waveform: {', '.join(missing[:6])}")
    zero = np.zeros_like(t)
    dt = np.diff(t)
    rows = []
    for d in pl.devices:
        for pair, a, b in PAIRS[d.kind]:
            na, nb = d.nodes[a], d.nodes[b]
            x = (zero if na == GROUND else w[_key(na)]) - (zero if nb == GROUND else w[_key(nb)])
            k = int(np.argmax(np.abs(x)))
            step = max(dt[k - 1] if k > 0 else 0.0, dt[k] if k < len(dt) else 0.0)
            rows.append({"device": d.name, "master": d.master, "where": d.where, "pair": pair,
                         "max_V": round(float(abs(x[k])), 5), "signed_V": round(float(x[k]), 5),
                         "t_ns": round(float(t[k]) * 1e9, 4), "dt_ps": round(float(step) * 1e12, 3),
                         "pass": bool(abs(x[k]) <= pl.limit_V)})
    worst = max(rows, key=lambda r: r["max_V"])
    out = {"soa_scope": pl.scope, "soa_limit_V": pl.limit_V,
           "soa_devices": len(pl.devices), "soa_devices_dut": sum(d.where == "dut" for d in pl.devices),
           "soa_pairs": len(rows), "soa_violations": sum(not r["pass"] for r in rows),
           "soa_max_V": worst["max_V"],
           "soa_worst": {k: worst[k] for k in ("device", "pair", "signed_V", "t_ns", "dt_ps")},
           "soa_points": int(len(t)), "soa_dt_max_ps": round(float(dt.max()) * 1e12, 3)}
    if pl.skipped:
        out["soa_skipped"] = list(pl.skipped)
    out["soa_table"] = rows
    return out


def measure(ctx: dict, w: dict[str, np.ndarray], m: dict) -> None:
    """Add the SOA metrics to `m`, or the error that says why they could not be made."""
    try:
        m.update(check(ctx.get("soa"), w))
    except Unverified as e:
        m["error"] = f"SOA unverified: {e}"


# ------------------------------------------------------------------ figure
def figure(fg, ctx: dict, m: dict, w: dict[str, np.ndarray], nbars: int = 18) -> None:
    """Largest |V| per device and terminal pair against the limit, the worst pair over the
    whole run, and the worst peak with the saved time points (the time resolution)."""
    from .figures import C1, C2, C3, LIMIT, MUTED, hline, note, vline

    pl: Plan = ctx["soa"]
    rows = sorted(m["soa_table"], key=lambda r: -r["max_V"])
    lim = pl.limit_V
    fig, axs = fg.new(1, 3, size=(16.0, 4.9), gridspec_kw={"width_ratios": [1.25, 1, 1]})
    ax = axs[0, 0]
    shown = rows[:nbars][::-1]
    y = np.arange(len(shown))
    ax.barh(y, [r["max_V"] for r in shown], color=[C1 if r["pass"] else LIMIT for r in shown], height=0.7)
    ax.set_yticks(y, [f"{r['device']} |V{r['pair']}|" + (" (ext)" if r["where"] == "external" else "")
                      for r in shown], fontsize=7)
    ax.axvline(lim, color=LIMIT, lw=1.1, ls="--")
    ax.text(lim, 0.99, f" limit {lim:g} V", transform=ax.get_xaxis_transform(), ha="left", va="top",
            fontsize=7.5, color=LIMIT)
    ax.set(xlabel="largest |V| over the whole run (V)", xlim=(0, max(lim, rows[0]["max_V"]) * 1.12),
           title=f"Per-device SOA ({len(shown)} of {len(rows)} pairs, worst first)")
    ax.grid(axis="y", visible=False)
    ndut = m.get("soa_devices_dut", 0)
    scope = (f"scope: {ndut} thin-oxide device(s) in {', '.join(pl.duts)}"
             if pl.scope == "device" else "scope: external nodes only\n(behavioral DUT: not transistor-level evidence)")
    nboundary = m["soa_devices"] - ndut
    if nboundary:
        scope += f"\n+ {nboundary} boundary device(s) of the testbench"
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
    hline(ax, lim, f"+{lim:g} V")
    hline(ax, -lim, f"-{lim:g} V")
    ax.plot([wr["t_ns"]], [wr["signed_V"]], "o", color=C2, ms=5)
    top = max(lim * 1.25, wr["max_V"] * 1.1)
    ax.set(xlabel="time (ns)", ylabel="voltage (V)", title=f"Worst pair: {wr['device']} V{wr['pair']}",
           ylim=(-top, top))
    ax.legend(loc="upper right")
    # zoom on its peak with the saved time points
    ax = axs[0, 2]
    tk = wr["t_ns"] * 1e-9
    sel = (t > tk - 150e-12) & (t < tk + 150e-12)
    ax.plot((t[sel] - tk) * 1e12, np.abs(x[sel]), "-", color=C1, lw=1.0)
    ax.plot((t[sel] - tk) * 1e12, np.abs(x[sel]), ".", color=C3, ms=3.5, label="saved time points")
    hline(ax, lim, f"limit {lim:g} V", x=0.7)
    vline(ax, 0.0, None, color=MUTED, ls=":")
    ax.set(xlabel=f"time from the peak at {wr['t_ns']:.3f} ns (ps)", ylabel="|V| (V)",
           title="Worst peak and the time resolution")
    ax.legend(loc="lower right")
    note(ax, f"peak |V{wr['pair']}| = {wr['max_V']:.4f} V\nlocal step {wr['dt_ps']:.2f} ps\n"
         f"{m['soa_points']} time points, largest step {m['soa_dt_max_ps']:.0f} ps", loc="upper left")
    fg.save(fig, "soa", f"Largest |Vgs|, |Vgd|, |Vds| of every checked device against the {lim:g} V limit "
            f"(scope: {pl.scope}), the worst pair over the whole run, and its peak with the saved time points "
            "that set the time resolution.")
