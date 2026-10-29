"""Numerical settings of transient runs: explicit per test, recorded per result, cross-checked.

A test can fix its transient settings in its block spec (issue #28)::

    tests:
      tb_bootstrap_track:
        numerics: {reltol: 1.0e-7, vabstol: 1.0e-8, maxstep: 1p, method: traponly}
        crosscheck: {maxstep: 0.5p, method: gear2only, samples: samples.txt}

* ``numerics``: written into the generated testbench (gen_tb.py), so the testbench file, which
  every result hashes, carries them. Simulator options (reltol, vabstol, iabstol) go on its
  ``options`` line, the others (maxstep, method, errpreset, lteratio) on its ``tran`` line.
* ``crosscheck``: ``python -m adcflow sim <test> --crosscheck`` runs every job a second time
  with these settings replacing the testbench's and records the differences of the spec
  metrics and of the raw samples (``samples``, a tb_sampler_va file) in the result's
  ``meta.crosscheck`` (docs/verification.md §2).

Every result records the settings the simulator actually used (``meta.numerics``), read from
its log, and the largest time step taken where a waveform of the whole run is saved.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

OPTION_KEYS = ("reltol", "vabstol", "iabstol")
TRAN_KEYS = ("maxstep", "method", "errpreset", "lteratio")
METHODS = ("traponly", "trap", "gear2only", "gear2", "euler")
CROSSCHECK_KEYS = OPTION_KEYS + TRAN_KEYS + ("samples",)


def validate(settings, where: str, extra: tuple[str, ...] = ()) -> list[str]:
    """Errors of a `numerics:` / `crosscheck:` mapping of a block spec."""
    if not isinstance(settings, dict):
        return [f"{where}: must be a mapping"]
    errs = [f"{where}: unknown key {k!r}" for k in settings if k not in OPTION_KEYS + TRAN_KEYS + extra]
    if "method" in settings and settings["method"] not in METHODS:
        errs.append(f"{where}: method {settings['method']!r} not in {list(METHODS)}")
    return errs


def _fmt(v) -> str:
    return f"{v:g}" if isinstance(v, float) else str(v)


def set_params(line: str, kv: dict) -> str:
    """`line` with each `key=value` replaced, or appended when the line has none."""
    for k, v in kv.items():
        new = f"{k}={_fmt(v)}"
        line, n = re.subn(rf"(?<=\s){re.escape(k)}=\S+", new, line)
        if not n:
            line = f"{line} {new}"
    return line


def apply(tb_text: str, settings: dict) -> str:
    """The testbench text with `settings` on its first `tran` and `options` statements.

    Simulator options need an `options` statement and the others a `tran` statement in the
    testbench; a testbench without one raises ValueError."""
    opts = {k: v for k, v in settings.items() if k in OPTION_KEYS}
    tran = {k: v for k, v in settings.items() if k in TRAN_KEYS}
    lines = tb_text.split("\n")
    for want, kv in (("options", opts), ("tran", tran)):
        if not kv:
            continue
        i = next((i for i, ln in enumerate(lines) if re.match(rf"^\w+\s+{want}\b", ln)), None)
        if i is None:
            raise ValueError(f"the testbench has no {want} statement for {sorted(kv)}")
        lines[i] = set_params(lines[i], kv)
    return "\n".join(lines)


# ------------------------------------------------------------------ what the simulator used
_SI = {"f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}
_UNITS = ("s", "V", "A", "Ohm", "F", "C", "S", "Hz")


def _value(text: str):
    """'52.1 ns' -> 5.21e-08, '10e-06' -> 1e-05, 'traponly' -> 'traponly'."""
    m = re.match(r"^([-+]?[0-9.]+(?:[eE][-+]?\d+)?)\s*(\S*)$", text.strip())
    if not m:
        return text.strip()
    x, unit = float(m.group(1)), m.group(2)
    if unit and unit not in _UNITS and unit[0] in _SI and unit[1:] in _UNITS:
        x *= _SI[unit[0]]
    return x


def _block(text: str, title: str, need: str = "") -> dict[str, object]:
    """`key = value` lines of the first indented block after `title` (up to the first blank line)
    that has the key `need` (with need empty: the first block)."""
    for m in re.finditer(rf"{re.escape(title)}\n((?:[ \t]+\S.*\n)+)", text):
        out = {}
        for line in m.group(1).splitlines():
            k, sep, v = line.partition(" = ")
            if sep:
                out[k.strip()] = _value(v)
        if not need or need in out:
            return out
    return {}


def _tran_block(text: str) -> dict[str, object]:
    """The `Important parameter values` of the first transient: a montecarlo analysis around it
    prints its own block first; the transient's has `stop`."""
    return _block(text, "Important parameter values:", "stop")


def from_log(text: str) -> dict:
    """Effective settings of the first transient analysis in a Spectre log: reltol, maxstep,
    method, errpreset, lteratio, abstol(V) (`Important parameter values`), vabstol (global
    options) and the number of accepted time steps with the mean step. {} without a tran."""
    tran = _tran_block(text)
    if not tran:
        return {}
    opts = _block(text, "Global user options:")
    out: dict = {"source": "spectre.log"}
    for key, name, scale in (("reltol", "reltol", 1), ("maxstep", "maxstep_ps", 1e12), ("method", "method", 1),
                             ("errpreset", "errpreset", 1), ("lteratio", "lteratio", 1),
                             ("abstol(V)", "abstol_V", 1)):
        v = tran.get(key)
        if v is not None:
            out[name] = float(f"{v * scale:.6g}") if isinstance(v, float) else v
    if isinstance(opts.get("vabstol"), float):
        out["vabstol"] = opts["vabstol"]
    m = re.search(r"Number of accepted tran steps\s*=\s*(\d+)", text)
    if m:
        out["steps_accepted"] = int(m.group(1))
        span = float(tran.get("stop", 0.0)) - float(tran.get("start", 0.0))
        if span > 0:
            out["step_mean_ps"] = float(f"{span / int(m.group(1)) * 1e12:.6g}")
    return out


_TIME = re.compile(r'^"time" (\S+)$', re.M)


def steps_from_waveform(tran_file: Path | None, stop: float | None) -> float | None:
    """Largest time step (s) between the saved points of a PSF-ASCII transient file when they
    cover the whole run (start at t = 0, reach the stop time), else None: with `outputstart`
    or without saved signals the steps taken are not in the outputs."""
    if tran_file is None or not Path(tran_file).exists():
        return None
    t = np.array([float(x) for x in _TIME.findall(Path(tran_file).read_text(encoding="utf-8", errors="replace"))])
    if len(t) < 3 or t[0] > 1e-15 or (stop and t[-1] < stop * (1 - 1e-9)):
        return None
    return float(np.diff(t).max())


def effective(job_dir: Path) -> dict:
    """meta.numerics of a job: the settings from its log and the largest step of its saved
    waveform (`step_max_ps`, null when no waveform of the whole run is saved)."""
    from . import psf

    log = Path(job_dir) / "spectre.log"
    if not log.exists():
        return {}
    text = log.read_text(errors="replace")
    out = from_log(text)
    if not out:
        return out
    stop = _tran_block(text).get("stop")
    raw = Path(job_dir) / "deck.raw"
    f = (psf.find(raw, "*.tran.tran") or psf.find(raw, "*.tran")) if raw.exists() else None
    dt = steps_from_waveform(f, stop if isinstance(stop, float) else None)
    out["step_max_ps"] = None if dt is None else float(f"{dt * 1e12:.6g}")
    return out


# ------------------------------------------------------------------ cross-check
def compare(ref: dict, alt: dict, metrics: list[str], ref_samples: Path | None, alt_samples: Path | None) -> dict:
    """Differences of a cross-check run (alt) from the run with the test's settings (ref):
    per metric ref, alt, alt - ref; for the raw samples (tb_sampler_va files: index, time,
    value) the count, whether the sample times agree, and the rms / largest difference; for a
    per-device SOA check the largest change of a pair's peak |V| and both violation counts."""
    out: dict = {"metrics": {}}
    for k in metrics:
        a, b = ref.get(k), alt.get(k)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            out["metrics"][k] = {"ref": a, "xcheck": b, "diff": b - a}
        else:
            out["metrics"][k] = {"ref": a, "xcheck": b, "diff": None}
    ta, tb = ref.get("soa_table"), alt.get("soa_table")
    if ta and tb:                                        # per-device SOA: time resolution of the peaks
        peak = {(r["device"], r["pair"]): r["max_V"] for r in tb}
        d = [(r["device"], r["pair"], peak[(r["device"], r["pair"])] - r["max_V"]) for r in ta
             if (r["device"], r["pair"]) in peak]
        w = max(d, key=lambda x: abs(x[2]))
        out["soa"] = {"pairs": len(d), "max_V_diff_max_mV": round(abs(w[2]) * 1e3, 4), "at": f"{w[0]} {w[1]}",
                      "violations": [ref.get("soa_violations"), alt.get("soa_violations")]}
    if ref_samples is None:
        return out
    if not (Path(ref_samples).exists() and Path(alt_samples).exists()):
        out["samples"] = {"error": f"{Path(ref_samples).name} missing"}
        return out
    from .measure.common import read_samples

    sa, sb = read_samples(ref_samples), read_samples(alt_samples)
    n = min(len(sa), len(sb))
    d = sb[:n, 2] - sa[:n, 2]
    out["samples"] = {"file": Path(ref_samples).name, "n": int(n), "n_ref": int(len(sa)), "n_xcheck": int(len(sb)),
                      "time_diff_max_ps": float(np.abs(sb[:n, 1] - sa[:n, 1]).max() * 1e12) if n else None,
                      "diff_rms_uV": float(np.sqrt(np.mean(d ** 2)) * 1e6) if n else None,
                      "diff_max_uV": float(np.abs(d).max() * 1e6) if n else None}
    return out
