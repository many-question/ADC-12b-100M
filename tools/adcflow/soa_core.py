"""The arithmetic of the per-device SOA check (soa.py), with numpy as its only dependency.

The runner also copies this file to the server: for a test with `soa: {remote: true}` the waveforms
of every device node are too large to fetch, so `python3 soa_core.py <job dir>` runs there after the
simulation. It reads the job's soa_plan.json and PSF-ASCII transient, writes soa_rows.json (the same
rows as a local check) and rewrites the transient with only the signals the testbench saves itself
and the nodes of the worst pair, so that the figures still have their waveforms.
"""

from __future__ import annotations

import json
import sys
from array import array
from pathlib import Path

import numpy as np

GROUND = "0"
PAIRS = {"mos": (("gs", "g", "s"), ("gd", "g", "d"), ("ds", "d", "s")), "moscap": (("pn", "p", "n"),)}
PLATEAU_V = 1e-4            # a maximum "occurs" at the first point within this of it (start of a plateau)
TIME_TOL = 1e-9             # relative: a window of exactly max_over_s passes


def key(node: str) -> str:
    """Waveform name of a node as written in a netlist (PSF names carry no escapes)."""
    return node.replace("\\<", "<").replace("\\>", ">").replace("\\\\", "\\")


def passes(vmax: float, window: float, limit: float, rule: dict) -> bool:
    """The rule for one pair: its largest |V| and its time above `limit` in its worst window (s)."""
    return bool(vmax <= limit or (vmax <= rule["peak_V"] and window <= rule["max_over_s"] * (1 + TIME_TOL)))


def over_spans(t: np.ndarray, x: np.ndarray, limit: float) -> np.ndarray:
    """Intervals [[start, end], ...] (s, in time order) during which |x| > limit, x linear between
    the saved points (both polarities). An interval per step of the waveform, at most two per step."""
    out = []
    for y in (x - limit, -x - limit):                    # above +limit, below -limit
        a, b = y[:-1], y[1:]
        k = np.flatnonzero((a > 0) | (b > 0))
        t0, t1, ya, yb = t[k], t[k + 1], a[k], b[k]
        with np.errstate(divide="ignore", invalid="ignore"):
            tc = t0 + (t1 - t0) * ya / (ya - yb)         # the crossing, for a step that has one
        out.append(np.column_stack((np.where(ya > 0, t0, tc), np.where(yb > 0, t1, tc))))
    spans = np.concatenate(out)
    return spans[np.argsort(spans[:, 0], kind="stable")]


def worst_window(spans: np.ndarray, window: float) -> float:
    """The largest time (s) that `spans` (over_spans) put into any window of this length. A transient
    shorter than the window has one window, itself. The sum is piecewise linear in the window's
    position, so its largest value comes with the window starting or ending on a span's edge."""
    if not len(spans):
        return 0.0
    starts, ends = spans[:, 0], spans[:, 1]
    cum = np.concatenate(([0.0], np.cumsum(ends - starts)))

    def before(t: np.ndarray) -> np.ndarray:             # time above the limit up to t (spans do not overlap in time)
        i = np.searchsorted(starts, t, side="right")
        j = np.maximum(i - 1, 0)
        return np.where(i > 0, cum[j] + np.minimum(t, ends[j]) - starts[j], 0.0)

    from_start = before(starts + window) - before(starts)
    to_end = before(ends) - before(ends - window)
    return float(max(from_start.max(), to_end.max()))


def pair_rows(devices: list[dict], t: np.ndarray, w: dict, limit: float, rule: dict) -> list[dict]:
    """One row per device and terminal pair. devices: {name, master, kind, where, nodes}."""
    zero = np.zeros_like(t)
    dt = np.diff(t)
    rows = []
    for d in devices:
        for pair, a, b in PAIRS[d["kind"]]:
            na, nb = d["nodes"][a], d["nodes"][b]
            x = (zero if na == GROUND else w[key(na)]) - (zero if nb == GROUND else w[key(nb)])
            mag = np.abs(x)
            vmax = float(mag.max())
            k = int(np.argmax(mag >= vmax - PLATEAU_V))      # first point of the maximum (start of a plateau)
            step = max(dt[k - 1] if k > 0 else 0.0, dt[k] if k < len(dt) else 0.0)
            over = window = 0.0
            if vmax > limit:
                spans = over_spans(t, x, limit)
                over, window = float((spans[:, 1] - spans[:, 0]).sum()), worst_window(spans, rule["window_s"])
            rows.append({"device": d["name"], "master": d["master"], "where": d["where"], "pair": pair,
                         "max_V": round(vmax, 5), "signed_V": round(float(x[k]), 5),
                         "t_ns": round(float(t[k]) * 1e9, 4), "dt_ps": round(float(step) * 1e12, 3),
                         "t_over_ps": round(over * 1e12, 3), "t_window_ps": round(window * 1e12, 3),
                         "pass": passes(vmax, window, limit, rule)})
    return rows


# ------------------------------------------------------------------ on the server
def _unesc(name: str) -> str:
    return name.replace("\\<", "<").replace("\\>", ">").replace("\\\\", "\\")


def _name(line: str) -> str:
    return _unesc(line[1:line.index('"', 1)])


def reduce_job(job_dir: Path | str) -> dict:
    """soa_rows.json and the thin transient of one job from its soa_plan.json (module docstring)."""
    job = Path(job_dir)
    plan = json.loads((job / "soa_plan.json").read_text(encoding="utf-8"))
    path = next(iter(sorted((job / "deck.raw").glob("*.tran.tran"))), None)
    if path is None:
        raise FileNotFoundError("no transient results")
    want = {key(n) for d in plan["devices"] for n in d["nodes"].values() if n != GROUND} | {key(k) for k in plan["keep"]}
    head, traces, data, sec, sweep = [], [], {}, None, None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s in ("HEADER", "TYPE", "SWEEP", "TRACE", "VALUE", "END"):
                sec = s
                if sec not in ("VALUE", "END"):
                    head.append(line)
                continue
            if sec == "VALUE":
                if s:
                    i = s.index('"', 1)
                    name = s[1:i]
                    if name == sweep or name in want or (("\\" in name) and _unesc(name) in want):
                        data.setdefault(_unesc(name), array("d")).append(float(s[i + 1:]))
            elif sec == "TRACE" and s:
                traces.append(line)
            else:
                if sec == "SWEEP" and s and sweep is None:
                    sweep = _name(s)
                head.append(line)
    w = {k: np.frombuffer(v, dtype=float) for k, v in data.items()}
    t = w[sweep]
    missing = sorted(n for n in want if n not in w or len(w[n]) != len(t))
    doc = {"size_bytes": path.stat().st_size, "points": int(len(t)), "t_start": float(t[0]), "missing": missing, "rows": []}
    if not missing and len(t) >= 2:
        doc["rows"] = pair_rows(plan["devices"], t, w, plan["limit_V"], plan["rule"])
        doc["dt_max_ps"] = round(float(np.diff(t).max()) * 1e12, 3)
    keep = {key(k) for k in plan["keep"]}
    if doc["rows"]:
        worst = max(doc["rows"], key=lambda r: r["max_V"])
        d = next(x for x in plan["devices"] if x["name"] == worst["device"])
        keep |= {key(n) for n in d["nodes"].values() if n != GROUND}
    out = [n for n in w if n in keep]
    (job / "soa_rows.json").write_text(json.dumps(doc), encoding="utf-8")
    if not missing:                                      # else keep the file for a look on the server
        tmp = path.with_suffix(".thin")
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(head)
            f.write("TRACE\n")
            f.writelines(line for line in traces if _name(line.strip()) in keep)
            f.write("VALUE\n")
            for k in range(len(t)):
                f.write(f'"{sweep}" {t[k]:.15e}\n')
                f.writelines(f'"{n}" {w[n][k]:.15e}\n' for n in out)
            f.write("END\n")
        tmp.replace(path)
    return doc


if __name__ == "__main__":
    reduce_job(sys.argv[1])
