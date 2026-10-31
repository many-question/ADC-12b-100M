"""CI checks: ``python -m adcflow check [ports|rnl|results|hygiene|candidates|all]``.

ports    every view and every candidate (design/xtor/<block>/<name>/) of every
         block defines its subcircuit with exactly the port list of
         specs/blocks/<block>.yaml; candidate.yaml is valid and a `selected:`
         candidate exists; every instance of a block (top level, testbenches)
         has that many terminals; Verilog-A module headers match
         specs/va_modules.yaml.
rnl      `rnl check` on every netlist and package (candidates included, design/
         is walked recursively): no errors, no warnings; netlists under design/
         and tb/ must be completely drawn (no hints).
results  recorded results (results/**.json) are re-judged with the current
         limits; a result is stale when something its simulated circuit depends
         on changed since the simulation (deps.py: a file the testbench reaches,
         a file it now reaches that was not recorded, an arch.yaml value its
         prepare or measure read; a result recorded with the whole deck: any of
         its files); blocks in status `signoff` need passing, fresh results for every spec
         in its required corner set, and so do `xtor-review` blocks with --strict, except
         that their stale results only warn while the PR leaves `selected:` and `status:`
         alone (--base; a flow change makes them stale until the candidate's own PR).
         Evidence figures (`figures` of a result):
         listed files must exist next to the JSON and stay below 200 kB; with
         --strict every result needs figures. They are not hashed: a figure is
         as stale as the JSON it belongs to.
hygiene  nothing site specific (servers, server paths, shell setup, PDK paths),
         no foundry name or PDK product code, and no model cards or large
         binaries in tracked files.
candidates  every candidate (docs/proposals/open-candidates.md §2): its
         netlist <block>.scs only uses PDK devices, resistor / capacitor /
         inductor and its own subcircuits, with no include / ahdl_include;
         its directory holds the netlist, candidate.yaml (valid) and
         .md/.png/.svg/.txt files, <= 2 MB, PNG <= 200 kB; its results are
         its JSONs (block / test / view as their path, no meta.verified_by)
         and PNGs; the lead's verification records (verification/, adcflow
         verify) are well formed. With --base and --author (pull requests):
         a PR that touches a candidate touches exactly one and nothing else
         (not verification/), and its author is an author of the candidate
         (base candidate.yaml) or, for a new one, in the new candidate.yaml
         with the name starting with the login; authors do not change in a
         candidate PR. A PR that touches no candidate is a lead PR; no login
         is exempt.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml

from . import REPO_ROOT, deps, numerics
from .corners import corner_set
from .netlist import parse
from .specs import blocks

RNL_PINNED = "core-v0.5.2"


class Report:
    def __init__(self, name: str):
        self.name = name
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def print(self) -> None:
        status = "FAIL" if self.errors else "ok"
        print(f"[{status}] {self.name}: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
        for e in self.errors:
            print(f"  error: {e}")
        for w in self.warnings:
            print(f"  warning: {w}")


def _tracked(pattern: str = "") -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO_ROOT, capture_output=True, text=True).stdout
    files = [REPO_ROOT / f for f in out.split("\0") if f]
    return [f for f in files if f.match(pattern)] if pattern else files


def _netlists() -> list[Path]:
    files = sorted(set(p for p in (REPO_ROOT / "design").rglob("*.scs")) | set((REPO_ROOT / "tb").rglob("*.scs")))
    return files


# ------------------------------------------------------------------ ports
def check_ports() -> Report:
    r = Report("ports")
    bl = blocks()
    defined: dict[str, Path] = {}
    def contract(b, path: Path, rel: str) -> None:
        nl = parse(path)
        for e in nl.errors:
            r.err(e)
        sc = nl.subckts.get(b.name)
        if sc is None:
            r.err(f"{rel}: does not define subckt {b.name}")
        elif sc.ports != b.port_names:
            r.err(f"{rel}: ports of {b.name} differ from specs: {sc.ports} != {b.port_names}")

    for b in bl.values():
        for view, rel in b.views.items():
            path = REPO_ROOT / rel
            if not path.exists():
                if view == "xtor" and b.status == "behavioral":
                    continue                      # not started yet
                r.err(f"{b.name}: view {view} file {rel} missing (status {b.status})")
                continue
            contract(b, path, rel)
    # every candidate (design/xtor/<block>/<name>/): candidate.yaml and the same port contract
    from . import candidates as cand
    names: dict[str, set[str]] = {}
    for c in cand.candidates():
        names.setdefault(c.block, set()).add(c.name)
        for e in c.problems:
            r.err(e)
        if c.netlist.exists():
            contract(bl[c.block], c.netlist, c.netlist.relative_to(cand.ROOT).as_posix())
    for b in bl.values():
        if b.selected and b.selected not in names.get(b.name, set()):
            r.err(f"{b.name}: selected candidate {b.selected!r} does not exist (design/xtor/{b.name}/{b.selected}/)")
        elif b.selected and next(c for c in cand.candidates(b.name) if c.name == b.selected).status == "withdrawn":
            r.err(f"{b.name}: selected candidate {b.selected!r} is withdrawn")
    # every instance of a block or VA module has the right number of terminals
    va = yaml.safe_load(open(REPO_ROOT / "specs" / "va_modules.yaml", encoding="utf-8"))["modules"]
    from .gen import cdac_sw_symbol, va_ports
    va_n = {}
    for m, cfg in va.items():
        va_n[m] = len(cdac_sw_symbol()[1]) if cfg.get("symbol") == "generated" else len(va_ports(m))
    for path in _netlists():
        nl = parse(path)
        insts = list(nl.top_instances) + [i for sc in nl.subckts.values() for i in sc.instances]
        for i in insts:
            if i.master in bl and len(i.nodes) != len(bl[i.master].port_names):
                r.err(f"{path.relative_to(REPO_ROOT)}:{i.line}: {i.name} has {len(i.nodes)} terminals, "
                      f"{i.master} has {len(bl[i.master].port_names)}")
            if i.master in va_n and len(i.nodes) != va_n[i.master]:
                r.err(f"{path.relative_to(REPO_ROOT)}:{i.line}: {i.name} has {len(i.nodes)} terminals, "
                      f"{i.master} has {va_n[i.master]}")
    # Verilog-A headers: port count after vector expansion
    for m, cfg in va.items():
        text = (REPO_ROOT / cfg["file"]).read_text(encoding="utf-8")
        hm = re.search(rf"module\s+{m}\s*\(([^)]*)\)", text)
        if not hm:
            r.err(f"{cfg['file']}: module {m} not found")
            continue
        n = 0
        for port in [p.strip() for p in hm.group(1).split(",")]:
            vm = re.search(rf"(?:input|output|inout|electrical)\s*\[(\d+):(\d+)\]\s*[^;]*\b{port}\b", text)
            n += abs(int(vm.group(1)) - int(vm.group(2))) + 1 if vm else 1
        if n != va_n[m]:
            r.err(f"{cfg['file']}: {m} has {n} terminals, specs/va_modules.yaml implies {va_n[m]}")
    return r


# ------------------------------------------------------------------ rnl
def rnl_exe() -> str | None:
    for cand in ("rnl", str(REPO_ROOT / ".rnl-cli" / "rnl")):
        if shutil.which(cand):
            return shutil.which(cand)
    return None


def check_rnl() -> Report:
    r = Report("rnl")
    exe = rnl_exe()
    if exe is None:
        r.err(f"rnl command not found (install {RNL_PINNED}, see docs/workflow.md)")
        return r
    files = sorted((REPO_ROOT / "design" / "rnl").glob("*.rnl")) + _netlists()
    for f in files:
        p = subprocess.run([exe, "check", str(f)], cwd=REPO_ROOT, capture_output=True, text=True)
        out = (p.stdout + p.stderr).strip().splitlines()
        summary = out[-1] if out else ""
        m = re.search(r"(\d+) errors, (\d+) warnings, (\d+) hints", summary)
        rel = f.relative_to(REPO_ROOT).as_posix()
        if not m:
            r.err(f"{rel}: unexpected rnl output: {summary}")
            continue
        e, w, h = map(int, m.groups())
        if e or w:
            r.err(f"{rel}: {summary}")
            for line in out:
                if line.startswith(("error", "warning")):
                    r.err(f"  {line}")
        elif h and f.suffix == ".scs":
            r.err(f"{rel}: {h} hint(s): every netlist must be completely drawn")
            for line in out:
                if line.startswith("hint"):
                    r.err(f"  {line}")
    return r


# ------------------------------------------------------------------ results
def _sha(path: Path) -> str:
    from .netlist import content_hash
    return content_hash(path)


def load_results() -> list[dict]:
    out = []
    for f in sorted((REPO_ROOT / "results").rglob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        doc["_path"] = f
        out.append(doc)
    return out


def judge(doc: dict) -> dict:
    """Re-judge a result with the current limits and corner sets.

    'specs': pass/fail of the specs that apply at the result's corner (Spec.applies); 'na': the
    specs of its test that do not apply there, with their raw values and no verdict; 'stale' and
    'error' are reported for every result, whatever applies. 'stale' lists the recorded files that
    changed and, for a result recorded with what its circuit depends on (meta.arch, deps.py), the
    files it reaches now without having recorded them and specs/arch.yaml when a value it read
    changed."""
    b = blocks().get(doc["block"])
    verdict, na = {}, {}
    meta = doc.get("meta", {})
    if b is not None:
        verdict, na = b.verdicts(doc["test"], doc["corner"], meta.get("mc"), doc["metrics"])
    stale = []
    for rel, h in (meta.get("files") or {}).items():
        p = REPO_ROOT / rel
        if not p.exists() or _sha(p) != h:
            stale.append(rel)
    if "arch" in meta:
        try:
            stale += deps.unrecorded(doc)
        except deps.UNRESOLVED as e:              # a test or view that no longer resolves
            stale.append(f"(dependencies: {e})")
        if deps.arch_changed(meta["arch"]):
            stale.append(deps.ARCH)
    return {"specs": verdict, "na": na, "stale": stale, "error": doc["metrics"].get("error")}


def preset_problem(doc: dict) -> str | None:
    """What is wrong with the transient preset of a result, None when nothing: a test with a
    `tran` must have run at errpreset=conservative, read from its log (meta.numerics). A result
    whose simulation failed has no numbers to doubt; `--mode cx` shows up here because it
    replaces the preset (docs/verification.md §2)."""
    t = getattr(blocks().get(doc["block"]), "tests", {}).get(doc["test"]) or {}
    tb = REPO_ROOT / str(t.get("netlist", ""))
    if doc["metrics"].get("error") or not tb.is_file():
        return None
    if not re.search(r"^\w+\s+tran\b", tb.read_text(encoding="utf-8"), re.M):
        return None
    got = (doc.get("meta", {}).get("numerics") or {}).get("errpreset")
    return None if got == numerics.PRESET else f"ran at errpreset {got}, not {numerics.PRESET}"


FIGURE_MAX_BYTES = 200_000


def _check_figures(r: Report, doc: dict, rel: str, strict: bool, failed: bool) -> None:
    """Evidence figures of a result: `figures: [{file, caption}]`, the PNGs next to the JSON.

    Listed files must exist and be small; PNGs of this result that are not listed are
    reported. Figures never make a result stale: they come from the same simulation as
    the JSON, whose file hashes decide. With `strict` every result needs figures (except
    a failed one, which is already reported)."""
    path = doc["_path"]
    figs = doc.get("figures")
    if not figs:
        if strict and not failed:
            r.err(f"{rel}: no evidence figures (re-run the test: python -m adcflow sim <test>)")
        figs = []
    listed = set()
    for i, f in enumerate(figs):
        name = f.get("file", "") if isinstance(f, dict) else ""
        if not name or not f.get("caption"):
            r.err(f"{rel}: figures[{i}] needs a file and a caption")
            continue
        listed.add(name)
        png = path.parent / name
        if not name.startswith(path.stem + ".") or not name.endswith(".png") or "/" in name:
            r.err(f"{rel}: figure {name!r} must be named <{path.stem}>.<tag>.png next to the result")
        elif not png.exists():
            r.err(f"{rel}: listed figure {name} does not exist")
        elif png.stat().st_size > FIGURE_MAX_BYTES:
            r.err(f"{rel}: figure {name} is {png.stat().st_size // 1000} kB (limit {FIGURE_MAX_BYTES // 1000} kB)")
    for png in sorted(path.parent.glob(f"{path.stem}.*.png")):
        if png.name not in listed and png.name[len(path.stem) + 1:].count(".") == 1:
            r.warn(f"{rel}: {png.name} is not listed in figures")


def _selection_changed(block, base: str | None) -> bool:
    """Whether this PR changes `selected:` or `status:` of a block (compared with the git ref `base`).
    Without a base nothing is known to change; a block that base cannot show counts as changed."""
    if not base:
        return False
    out = subprocess.run(["git", "show", f"{base}:specs/blocks/{block.path.name}"], cwd=REPO_ROOT, capture_output=True, text=True,
                         encoding="utf-8")
    if out.returncode:
        return True
    old = yaml.safe_load(out.stdout) or {}
    return (old.get("selected") or None, old.get("status")) != (block.selected, block.status)


def check_results(strict: bool = False, base: str | None = None) -> Report:
    r = Report("results")
    docs = load_results()
    by = {}
    for d in docs:
        j = judge(d)
        rel = d["_path"].relative_to(REPO_ROOT).as_posix()
        if j["error"]:
            r.warn(f"{rel}: simulation/measurement error: {j['error']}")
        for sid, v in j["specs"].items():
            if v["pass"] is False:                # None: a reported-only spec, no verdict
                r.warn(f"{rel}: {sid} = {v['value']} violates {v['limit']}")
        if j["stale"]:
            r.warn(f"{rel}: stale (changed since simulated: {', '.join(j['stale'][:4])})")
        elif preset_problem(d):                   # a stale result is reported above and judged when rerun
            r.err(f"{rel}: {preset_problem(d)}")
        _check_figures(r, d, rel, strict, bool(j["error"]))
        by.setdefault((d["block"], d["test"], d["view"]), {}).setdefault(d["corner"], []).append((d, j))
    for b in blocks().values():
        need_signoff = b.status == "signoff" or (strict and b.status == "xtor-review")
        if not need_signoff:
            continue
        view = f"xtor-{b.selected}" if b.selected else "xtor"     # the selected candidate, or the legacy view
        stale_errors = b.status == "signoff" or _selection_changed(b, base)
        stale_docs = set()
        for s in b.specs:
            corners = [c.name for c in corner_set(s.corners)]
            got = by.get((b.name, s.test, view), {})
            for c in corners:
                # every result at the corner (all variants) that the spec applies to
                hit = [(d, j) for d, j in got.get(c, []) if s.applies(c, d.get("meta", {}).get("mc"))]
                if not hit:
                    r.err(f"{b.name} {s.id}: no {view} result for corner {c} ({s.test})")
                    continue
                for d, j in hit:
                    if j["stale"]:
                        stale_docs.add(d["_path"])
                        if stale_errors:
                            r.err(f"{b.name} {s.id} {c}: result is stale")
                    v = j["specs"].get(s.id, {})
                    if s.reported:                # no verdict, but the value must be there
                        if v.get("value") is None:
                            r.err(f"{b.name} {s.id} {c}: reported metric {s.metric} not measured")
                    elif not v.get("pass"):
                        r.err(f"{b.name} {s.id} {c}: fails ({v or None})")
        if stale_docs and not stale_errors:
            r.warn(f"{b.name}: selected candidate {b.selected or view} has {len(stale_docs)} stale results, not eligible")
    return r


# ------------------------------------------------------------------ hygiene
# Generic patterns only: site-specific strings (host names, paths) must not even
# appear in this file. The exact strings of the local site configuration are
# added at run time (see _site_literals), so local runs and the commit hook
# catch them too.
FORBIDDEN = [
    (r"/home/[A-Za-z]", "absolute home path"),
    (r"\.cshrc", "shell setup file"),
    (r"/server_[a-z]+", "server scratch path"),
    (r"models/spectre", "PDK model directory"),
    (r"\.scs\"\s+section=", "direct include of a model library"),
    (r"^\s*\+?\s*(toxe|vth0|u0|k1|nfactor)\s*=", "model-card parameter"),
    (r"^\s*model\s+\w+\s+(bsim\w*|psp\w*)\b", "model card"),
]
HYGIENE_SKIP = {"site.example.yaml"}

# Names that must not appear anywhere in tracked files (the process is only ever
# called "28 nm HPC+"). Stored as sha256 of the lowercased word, so this file does
# not contain them either; words are letter runs, letter+digit runs and, for CJK
# text, windows of 2-3 characters.
NAME_HASHES = {
    "17b7a45dc3a95bfd7c0d4c5963b75f2bd2c962eb04b50d50c086c3dc2e260fea": "foundry name",
    "b8b8592c26c3594b3a48e95893d392f5611f8b0dad7432a200688eae3710bf4c": "PDK product code",
    "7ad9114a6ee73402a554f6d7b2d8396457ef3344f2d8cb75ad2a5b10879b67c2": "foundry name",
    "e3f496390767e61726899aca851e7c18e0ef0cdb97dceb6cdcce851550b4921b": "foundry name",
}


def _words(line: str):
    low = line.lower()
    for m in re.finditer(r"[a-z]+", low):
        yield m.group()
    for m in re.finditer(r"[a-z0-9]+", low):
        yield m.group()
    for m in re.finditer(f"[{chr(0x3400)}-{chr(0x9fff)}]+", low):
        run = m.group()
        for n in (2, 3):
            for i in range(len(run) - n + 1):
                yield run[i:i + n]


def find_names(text: str) -> list[tuple[int, str]]:
    """(line, what) for every forbidden process / foundry name in text."""
    hits = set()
    for n, line in enumerate(text.splitlines(), 1):
        for w in _words(line):
            what = NAME_HASHES.get(hashlib.sha256(w.encode()).hexdigest())
            if what:
                hits.add((n, what))
    return sorted(hits)


def _site_literals() -> list[tuple[str, str]]:
    """Exact strings of the local site config (host, paths, PDK files), if present."""
    try:
        from .site import site
        s = site()
    except Exception:
        return []
    vals = []
    sim, pdk = s.get("sim") or {}, s.get("pdk") or {}
    if sim.get("host"):
        vals.append(str(sim["host"]))
    if sim.get("remote_root"):
        vals.append(str(sim["remote_root"]).split("{")[0].rstrip("/"))
    for cmd in sim.get("env_setup") or []:
        vals += [w for w in str(cmd).split() if "/" in w]
    for k in ("model_dir", "core_file", "hv_file"):
        if pdk.get(k):
            vals.append(str(pdk[k]))
    return [(re.escape(v), "site-specific string from the site config") for v in vals if len(v) >= 4]


def check_hygiene() -> Report:
    r = Report("hygiene")
    patterns = FORBIDDEN + _site_literals()
    for f in _tracked():
        rel = f.relative_to(REPO_ROOT).as_posix()
        if rel in HYGIENE_SKIP or not f.exists():
            continue
        if f.stat().st_size > 2_000_000:
            r.err(f"{rel}: {f.stat().st_size / 1e6:.1f} MB tracked file (keep large data out of git)")
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, what in find_names(text):
            r.err(f"{rel}:{n}: {what} must not be committed (write \"28 nm HPC+\")")
        for pat, what in patterns:
            for m in re.finditer(pat, text, flags=re.MULTILINE | re.IGNORECASE):
                if rel == "tools/adcflow/checks.py" and what != "site-specific string from the site config":
                    continue                      # the generic pattern list itself
                line = text.count("\n", 0, m.start()) + 1
                r.err(f"{rel}:{line}: {what} must not be committed")
    return r


# ------------------------------------------------------------------ candidates
def _git_out(*args: str) -> tuple[int, str]:
    p = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True)
    return p.returncode, p.stdout


def check_candidates(base: str | None = None, author: str | None = None) -> Report:
    """Every candidate (directory and results) follows the content rules; with --base and --author
    (CI, pull requests) the PR also follows the candidate-PR rules (candidates.pr_problems)."""
    from . import candidates as cand

    from . import verify

    r = Report("candidates")
    errs = cand.disk_problems()
    rec_errs, rec_warns = verify.record_problems()
    errs += rec_errs
    for w in rec_warns:
        r.warn(w)
    if base and author:
        rc, mb = _git_out("merge-base", base, "HEAD")
        if rc != 0:
            r.err(f"cannot find the merge base of {base} and HEAD")
            return r
        mb = mb.strip()
        _, out = _git_out("diff", "--name-only", "--no-renames", mb, "HEAD")
        changed = [p for p in out.splitlines() if p]

        def base_text(path: str) -> str | None:
            rc, text = _git_out("show", f"{mb}:{path}")
            return text if rc == 0 else None

        errs += cand.pr_problems(changed, author, base_text, cand.disk_files)
    for e in dict.fromkeys(errs):
        r.err(e)
    return r


def run_checks(what: str = "all", strict: bool = False, base: str | None = None,
               author: str | None = None) -> int:
    from .gen import generate

    reports = []
    if what in ("ports", "all"):
        reports.append(check_ports())
    if what in ("rnl", "all"):
        reports.append(check_rnl())
    if what in ("results", "all"):
        reports.append(check_results(strict, base))
    if what in ("hygiene", "all"):
        reports.append(check_hygiene())
    if what in ("candidates", "all"):
        reports.append(check_candidates(base, author))
    for rep in reports:
        rep.print()
    rc = 1 if any(rep.errors for rep in reports) else 0
    if what == "all":
        print("[..] generated files")
        rc |= generate("all", check=True)
    return rc
