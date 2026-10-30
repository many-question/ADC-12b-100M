"""What a simulation result depends on, so that it goes stale only when one of those changes.

A run deck (runner.make_deck) includes the view of every block, the top level, the Verilog-A of
all of them and the testbench. The simulated circuit is only the part the testbench reaches, and
a result records only that part:

* ``meta.files``: content hashes of the testbench; of every deck netlist that defines a master
  name reachable from the testbench's instances (transitively, by name, across all deck files: a
  name defined twice records both), or that has top-level statements besides
  ``simulator lang=spectre``; of the Verilog-A files that define the reached modules and the files
  they `include (as staged by runner.stage: the testbench Verilog-A gets the architecture
  constants copied next to it); and of specs/soa.yaml when the test runs the SOA check. When the
  reader cannot follow something (an include in a netlist, a parse error, an `include it cannot
  find), the whole deck is recorded.
* ``meta.arch``: the keys of specs/arch.yaml that the run read (arch.track) while building its jobs
  (a test's `prepare`: generated parameters and job files) and while measuring, with a hash of
  their values. The deck's generated includes (adc_arch*.vams) are files of the first list.
* ``meta.views``: the views of the run.

checks.judge marks such a result stale when a recorded file changed, when the circuit now reaches
a file the result did not record (for example another file now defines one of its masters, or a
view changed), or when a recorded arch value changed. A result recorded with the whole deck (no
``meta.arch``) keeps the old rule (any recorded file changed); `adcflow rehash` (rehash below)
moves it onto the reduced set without simulating, when that is sound.
"""

from __future__ import annotations

import ast
import datetime as _dt
import fnmatch
import json
import posixpath
import re
import subprocess
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from . import REPO_ROOT
from . import arch as archmod
from .netlist import ENDS_RE, SUBCKT_RE, content_hash, logical_lines, parse

STAGE_DIRS = ("design", "tb")
STAGE_EXT = {".scs", ".va", ".vams"}
# extra copies of the stage (source glob, staged directory): the testbench Verilog-A `include
# the architecture constants
STAGE_COPIES = [("design/behav/veriloga/adc_arch*.vams", "tb/common/veriloga")]
SYSTEM_HEADERS = {"disciplines.vams", "constants.vams"}       # the simulator's own Verilog-A headers
ARCH = "specs/arch.yaml"
# Errors that mean a result's test, view or input files no longer resolve: its dependencies are
# then unknown and the result counts as stale. Anything else (a missing package, a bug) is raised.
UNRESOLVED = (KeyError, ValueError, OSError)
SOA = "specs/soa.yaml"

MODEL_RE = re.compile(r"^\s*model\s+([A-Za-z_]\w*)\s+([A-Za-z_]\w*)")
HARMLESS_TOP_RE = re.compile(r"^\s*simulator\s+lang\s*=\s*spectre\s*$")
VA_MODULE_RE = re.compile(r"\b(?:macro)?module\s+([A-Za-z_]\w*)")
VA_INCLUDE_RE = re.compile(r'`include\s+"([^"]+)"')
VA_COMMENT_RE = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)


# ------------------------------------------------------------------ trees
class Disk:
    """The working tree (candidate netlists under candidates.ROOT, which the site points elsewhere)."""

    def path(self, rel: str) -> Path:
        from . import candidates
        return (candidates.ROOT if rel.startswith("design/xtor/") else REPO_ROOT) / rel

    def read(self, rel: str) -> bytes | None:
        p = self.path(rel)
        return p.read_bytes() if p.is_file() else None


class Git:
    """The tree of a commit (None contents when the commit is not available)."""

    def __init__(self, commit: str | None):
        self.commit = commit or ""
        self.ok = bool(self.commit) and _git("cat-file", "-e", f"{self.commit}^{{commit}}")[0] == 0
        self._cache: dict[str, bytes | None] = {}

    def read(self, rel: str) -> bytes | None:
        if not self.ok:
            return None
        if rel not in self._cache:
            rc, out = _git("show", f"{self.commit}:{rel}")
            self._cache[rel] = out if rc == 0 else None
        return self._cache[rel]


def _git(*args: str) -> tuple[int, bytes]:
    try:
        p = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, timeout=60)
        return p.returncode, p.stdout
    except Exception:
        return 1, b""


DISK = Disk()


def rel(p: Path) -> str:
    """Repository path of a deck file (a candidate netlist is relative to candidates.ROOT)."""
    from . import candidates
    for root in (REPO_ROOT, candidates.ROOT):
        try:
            return Path(p).relative_to(root).as_posix()
        except ValueError:
            continue
    raise ValueError(f"{p} is outside the repository")


def file_hash(tree, r: str) -> str | None:
    data = tree.read(r)
    return None if data is None else content_hash(r, data)


# ------------------------------------------------------------------ what files define and use
@dataclass
class Unit:
    """A netlist as reachability sees it."""
    defs: dict[str, list[str]]          # name defined here (subckt or model) -> masters it uses
    top: list[str] | None               # masters of its top-level statements; None: it has none
    problem: str = ""                   # what the reader cannot follow


@lru_cache(maxsize=512)
def netlist_unit(name: str, data: bytes) -> Unit:
    text = data.decode("utf-8")
    nl = parse(name, text=text)
    defs = {n: [i.master for i in sc.instances] for n, sc in nl.subckts.items()}
    depth, has_top, top_models = 0, False, []
    for _, line in logical_lines(text):
        if SUBCKT_RE.match(line):
            depth += 1
            continue
        if ENDS_RE.match(line):
            depth = max(depth - 1, 0)
            continue
        m = MODEL_RE.match(line)
        if m:
            defs.setdefault(m.group(1), []).append(m.group(2))
            if depth == 0:
                top_models.append(m.group(2))
        if depth == 0 and not HARMLESS_TOP_RE.match(line):
            has_top = True
    problems = list(nl.errors) + [f"{kind} \"{p}\"" for kind, p in nl.includes]
    top = [i.master for i in nl.top_instances] + top_models if has_top else None
    return Unit(defs, top, "; ".join(problems))


@lru_cache(maxsize=512)
def _va_text(data: bytes) -> tuple[frozenset[str], tuple[str, ...]]:
    """(modules, `include names) of a Verilog-A text, comments removed."""
    text = VA_COMMENT_RE.sub(" ", data.decode("utf-8", errors="replace"))
    return frozenset(VA_MODULE_RE.findall(text)), tuple(VA_INCLUDE_RE.findall(text))


def staged_source(staged: str, tree) -> str | None:
    """The repository file that runner.stage puts at stage path `staged` in `tree` (None: nothing)."""
    d, name = posixpath.split(staged)
    for pattern, dest in STAGE_COPIES:
        if d == dest and fnmatch.fnmatchcase(name, posixpath.basename(pattern)):
            src = posixpath.join(posixpath.dirname(pattern), name)
            if tree.read(src) is not None:
                return src                     # the copy overwrites a file of the same name
    if staged.split("/")[0] in STAGE_DIRS and posixpath.splitext(staged)[1] in STAGE_EXT \
            and tree.read(staged) is not None:
        return staged
    return None


def va_closure(r: str, tree) -> tuple[set[str], list[str], list[str]]:
    """(modules, files, problems) of a Verilog-A file and the files it `include`s, transitively.

    Includes resolve against the including file's staged directory (the simulator looks there
    first); the simulator's own headers are not repository files."""
    mods: set[str] = set()
    files: list[str] = []
    problems: list[str] = []
    todo, seen = [(r, r)], set()
    while todo:
        src, staged = todo.pop()
        if staged in seen:
            continue
        seen.add(staged)
        data = tree.read(src)
        if data is None:
            problems.append(f"{src}: missing")
            continue
        if src not in files:
            files.append(src)
        m, incs = _va_text(data)
        mods |= m
        for inc in incs:
            st = posixpath.normpath(posixpath.join(posixpath.dirname(staged), inc))
            s = staged_source(st, tree)
            if s is not None:
                todo.append((s, st))
            elif inc not in SYSTEM_HEADERS:
                problems.append(f"{staged}: `include \"{inc}\" not found")
    return mods, files, problems


def defines(r: str, tree) -> set[str]:
    """Names a deck file defines in `tree`: subckts and models of a netlist, the modules of a
    Verilog-A file and its includes, the modules written in an include file itself."""
    data = tree.read(r)
    if data is None:
        return set()
    if r.endswith(".scs"):
        return set(netlist_unit(r, data).defs)
    if r.endswith(".va"):
        return va_closure(r, tree)[0]
    return set(_va_text(data)[0])


# ------------------------------------------------------------------ reachability
@dataclass
class Reach:
    masters: set[str]                   # every master name the testbench reaches (also primitives, devices)
    files: list[str]                    # what the circuit depends on: the testbench first
    deck: list[str]                     # every file of the deck (netlists, Verilog-A and their includes)
    problems: list[str] = field(default_factory=list)   # why the whole deck is recorded


def reach(tree, tb: str, netlists: list[str], va: list[str]) -> Reach:
    """The masters and files a testbench reaches through the deck files `netlists` and `va`."""
    units: dict[str, Unit] = {}
    problems: list[str] = []
    for r in dict.fromkeys([tb, *netlists]):
        data = tree.read(r)
        if data is None:
            problems.append(f"{r}: missing")
            continue
        units[r] = netlist_unit(r, data)
        if units[r].problem:
            problems.append(f"{r}: {units[r].problem}")
    vinfo: dict[str, tuple[set[str], list[str]]] = {}
    for r in va:
        mods, files, probs = va_closure(r, tree)
        vinfo[r] = (mods, files)
        problems += probs
    definers: dict[str, list[str]] = {}
    for r, u in units.items():
        for n in u.defs:
            definers.setdefault(n, []).append(r)
    for r, (mods, _) in vinfo.items():
        for n in mods:
            definers.setdefault(n, []).append(r)
    keep = [tb] + [r for r, u in units.items() if r != tb and u.top is not None]
    todo = [m for r in keep if r in units for m in (units[r].top or [])]
    masters: set[str] = set()
    while todo:
        m = todo.pop()
        if m in masters:
            continue
        masters.add(m)
        for r in definers.get(m, []):
            if r not in keep:
                keep.append(r)
            if r in units:
                todo += units[r].defs[m]
    files = list(keep)
    for r in keep:
        files += [f for f in vinfo.get(r, ((), []))[1] if f not in files]
    deck = list(dict.fromkeys([*units, *(f for _, fs in vinfo.values() for f in fs)]))
    if problems:
        files = list(dict.fromkeys([tb, *deck]))
    return Reach(masters, files, deck, problems)


def deck_inputs(test: dict, views: dict) -> tuple[str, list[str], list[str]]:
    """(testbench, netlists, Verilog-A) that runner.make_deck includes for a test and views."""
    from .runner import needed_va, view_files
    vfiles = view_files(views)
    tb = test["netlist"]
    va = needed_va(vfiles, (REPO_ROOT / tb).read_text(encoding="utf-8"))
    return tb, [rel(p) for p in vfiles], [rel(p) for p in va]


def run_reach(test: dict, views: dict, tree=DISK) -> Reach:
    """What a run of `test` with `views` depends on in `tree` (soa.yaml when it runs the SOA check)."""
    r = reach(tree, *deck_inputs(test, views))
    if test.get("soa"):
        r.files.append(SOA)
    return r


def record_meta(test: dict, views: dict, arch_keys) -> dict:
    """meta.files, meta.arch and meta.views of a result recorded now (runner.run_test)."""
    r = run_reach(test, views)
    if r.problems:
        print("[adcflow] recording the whole deck:", *r.problems[:5], sep="\n  ")
    keys = archmod.minimal(arch_keys)
    return {"files": {f: file_hash(DISK, f) for f in r.files},
            "arch": {"keys": keys, "sha": archmod.values_sha(archmod.load_data(), keys)},
            "views": dict(views)}


# ------------------------------------------------------------------ views of a result
def views_of(block: str, viewsig: str) -> dict[str, str]:
    """The views of a result directory name (runner._viewsig, inverted)."""
    from . import candidates
    from .specs import blocks

    names = [b for b in blocks() if b != "adc_top"]
    if viewsig == "behav":
        views = {}
    elif block != "adc_top":
        views = {block: "xtor:" + viewsig[5:] if viewsig.startswith("xtor-") else viewsig}
    elif viewsig == "xtor":
        views = {b: "xtor" for b in names}
    elif viewsig.startswith("xtor-"):
        views = {}
        for term in viewsig[5:].split("+"):
            short, _, cand = term.partition("@")
            views["adc_" + short] = f"xtor:{cand}" if cand else "xtor"
    else:
        raise ValueError(f"{block}: unknown view directory {viewsig!r}")
    if block == "adc_top":
        sig = candidates.top_signature(views, len(names))
    else:
        sig = candidates.view_dir(block, views.get(block, "behav"))
    if sig != viewsig:
        raise ValueError(f"{block}: view directory {viewsig!r} does not resolve ({views} gives {sig!r})")
    return views


# ------------------------------------------------------------------ judging (checks.judge)
def unrecorded(doc: dict) -> list[str]:
    """Files that the circuit of a result reaches now and that its meta.files does not list."""
    from .specs import find_test

    meta = doc.get("meta") or {}
    _, test = find_test(doc["test"], doc["block"])
    views = meta["views"] if "views" in meta else views_of(doc["block"], doc["view"])
    rec = meta.get("files") or {}
    return [f for f in run_reach(test, views).files if f not in rec]


def arch_changed(rec: dict) -> bool:
    """True when an arch value recorded in meta.arch differs from specs/arch.yaml now."""
    return archmod.values_sha(archmod.load_data(), rec.get("keys") or []) != rec.get("sha")


# ------------------------------------------------------------------ measure functions and arch.yaml
def _module_path(mod: str) -> Path | None:
    parts = mod.split(".")
    if parts[0] != "adcflow":
        return None
    p = REPO_ROOT / "tools" / Path(*parts)
    if p.with_suffix(".py").is_file():
        return p.with_suffix(".py")
    if (p / "__init__.py").is_file():
        return p / "__init__.py"
    return None


def _resolve_from(mod: str, node: ast.ImportFrom) -> list[str]:
    """adcflow modules an ImportFrom in module `mod` binds (a module or the module of a name)."""
    if node.level:
        base = mod.split(".")
        if _module_path(mod) and _module_path(mod).name != "__init__.py":
            base = base[:-1]
        base = base[:len(base) - (node.level - 1)]
        pkg = ".".join(base + ([node.module] if node.module else []))
    else:
        pkg = node.module or ""
    out = []
    for a in node.names:
        sub = f"{pkg}.{a.name}"
        out.append(sub if _module_path(sub) else pkg)
    return [m for m in out if m.startswith("adcflow")]


def _imports(mod: str, tree: ast.AST) -> list[str]:
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            out += _resolve_from(mod, n)
        elif isinstance(n, ast.Import):
            out += [a.name for a in n.names if a.name.startswith("adcflow")]
    return out


@lru_cache
def _ast(mod: str) -> ast.Module | None:
    p = _module_path(mod)
    return ast.parse(p.read_text(encoding="utf-8")) if p else None


@lru_cache
def module_reads_arch(mod: str) -> bool:
    """Whether code of adcflow module `mod` can read arch.yaml: it is adcflow.arch, names the file,
    or imports (anywhere in it) a module that can."""
    seen, todo = set(), [mod]
    while todo:
        m = todo.pop()
        if m in seen:
            continue
        seen.add(m)
        if m == "adcflow.arch":
            return True
        t = _ast(m)
        if t is None:
            continue
        if any(isinstance(n, ast.Constant) and isinstance(n.value, str) and "arch.yaml" in n.value
               for n in ast.walk(t)):
            return True
        todo += _imports(m, t)
    return False


DYNAMIC = {"importlib", "__import__", "eval", "exec", "globals"}


def may_read_arch(ref: str) -> bool:
    """Static over-approximation: can the function ``module:name`` read arch.yaml?

    Walks the function and every function, class and module-level value of its module that it
    names, transitively; it can when that code names an adcflow module (or something imported from
    one) that can read arch.yaml (module_reads_arch), imports one, names the file, or imports
    dynamically. Other modules count as a whole. It assumes the arguments the function gets (a
    measure: the job directory and ctx) carry no Arch, which runner.run_test guarantees."""
    mod, name = ref.split(":")
    t = _ast(mod)
    if t is None:
        return True
    defs: dict[str, list[ast.AST]] = {}
    bound: dict[str, list[str]] = {}
    always: list[ast.AST] = []
    for st in t.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs.setdefault(st.name, []).append(st)
        elif isinstance(st, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = st.targets if isinstance(st, ast.Assign) else [st.target]
            for tg in targets:
                for n in ast.walk(tg):
                    if isinstance(n, ast.Name):
                        defs.setdefault(n.id, []).append(st)
        elif isinstance(st, ast.ImportFrom):
            for a, m in zip(st.names, _resolve_from(mod, st)):
                bound.setdefault(a.asname or a.name, []).append(m)
        elif isinstance(st, ast.Import):
            for a in st.names:
                if a.name.startswith("adcflow"):
                    bound.setdefault(a.asname or a.name.split(".")[0], []).append(a.name)
        elif not (isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant)):
            always.append(st)                    # other module-level code: always counted
    if name not in defs:
        return True
    todo, seen = list(defs[name]) + always, set()
    while todo:
        node = todo.pop()
        if id(node) in seen:
            continue
        seen.add(id(node))
        for n in ast.walk(node):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                if any(module_reads_arch(m) for m in _imports(mod, n)):
                    return True
            elif isinstance(n, ast.Constant) and isinstance(n.value, str) and "arch.yaml" in n.value:
                return True
            elif isinstance(n, ast.Name):
                if n.id in DYNAMIC:
                    return True
                if any(module_reads_arch(m) for m in bound.get(n.id, [])):
                    return True
                todo += defs.get(n.id, [])
    return False


# ------------------------------------------------------------------ rehash
@dataclass
class Rehash:
    path: Path
    status: str                         # fresh (already on its set) | rehashed | stale
    why: list[str] = field(default_factory=list)
    meta: dict | None = None            # the new meta of a rehashed result


def rehash_doc(doc: dict, path: Path | None = None) -> Rehash:
    """Bring a result onto the files and arch values its circuit depends on, without simulating.

    Its meta.files may list the whole deck (recorded before deps.py) or the reduced set. With the
    files of the simulation's commit (meta.git, only when meta.git_clean) for what the result did
    not hash, it stays fresh only when:

    1. every file the circuit reaches now (run_reach) has the content it had for the simulation;
    2. no file whose content differs (or that exists in only one of the two decks) defines, then or
       now, a name that the circuit reaches now;
    3. the arch values it read are unchanged: the keys its jobs' `prepare` reads (the job is built
       again under arch.track and must give the recorded params) and, when the measure function
       may read arch.yaml at all (may_read_arch), the whole file, against arch.yaml of the run
       (its recorded hash, the commit's file).

    A result already on the reduced set (meta.arch) that checks.judge finds fresh is left alone."""
    from .checks import judge
    from .corners import by_name
    from .runner import build_jobs
    from .specs import find_test

    path = Path(path or doc.get("_path"))
    meta = dict(doc.get("meta") or {})
    rec: dict = dict(meta.get("files") or {})
    legacy = "arch" not in meta
    if not legacy and not judge(doc)["stale"]:
        return Rehash(path, "fresh")
    why: list[str] = []
    block, test = find_test(doc["test"], doc["block"])
    try:
        views = meta["views"] if "views" in meta else views_of(block.name, doc["view"])
        now = run_reach(test, views)
    except Exception as e:                                       # a view that no longer resolves ...
        return Rehash(path, "stale", [f"dependencies: {e}"])
    if now.problems:
        why.append("the reader cannot follow: " + "; ".join(now.problems[:3]))
    then = Git(meta.get("git") if meta.get("git_clean") is True else None)

    # the deck of the simulation as far as needed: recorded hashes, and (whole-deck records) the
    # files the recorded Verilog-A included, from the commit
    then_hash = {r: h for r, h in rec.items() if r != ARCH}
    if legacy:
        for r in [r for r in rec if r.endswith(".va")]:
            if file_hash(then, r) != rec[r]:
                why.append(f"{r}: what it included for the simulation is not available "
                           f"(needs meta.git_clean and the commit {meta.get('git') or '?'})")
                break
            for f in va_closure(r, then)[1][1:]:
                then_hash.setdefault(f, file_hash(then, f))

    def then_defs(r: str) -> set[str] | None:
        """Names `r` defined for the simulation (None: its content then is not available)."""
        if then_hash.get(r) is None:
            return set()                                         # not in the deck then
        if file_hash(then, r) != then_hash[r]:
            return None
        return defines(r, then)

    # 1. the files the circuit reaches now: as they were
    for f in now.files:
        h = file_hash(DISK, f)
        if f not in then_hash:
            why.append(f"{f}: not part of the recorded deck")
        elif then_hash[f] != h:
            why.append(f"{f}: changed")
    # 2. changed files (outside those, already checked) define no reached name, then or now
    for f in sorted(set(then_hash) | set(now.deck)):
        if f == SOA or f in now.files or then_hash.get(f) == file_hash(DISK, f):
            continue
        old = then_defs(f)
        if old is None:
            why.append(f"{f}: changed, and its content at {meta.get('git') or '?'} is not available")
            continue
        hit = (old | defines(f, DISK)) & now.masters
        if hit:
            why.append(f"{f}: changed and defines {', '.join(sorted(hit))}")
    # 3. the arch values it read
    cur = archmod.load_data()
    if legacy:
        keys: set[str] = set()
        try:
            corner = by_name(doc["corner"])
            needs_pdk = bool(test.get("needs_pdk")) or any(v != "behav" for v in views.values())
            with archmod.track() as keys:
                jobs = {j.name: j for j in build_jobs(block, doc["test"], test, [corner], views, {}, needs_pdk)}
            job = jobs.get(path.stem)
            if job is None:
                why.append(f"job {path.stem} is not a job of {doc['test']} at {doc['corner']}")
            elif json.loads(json.dumps(job.params, default=float)) != doc.get("params"):
                why.append(f"job {path.stem} does not rebuild with the recorded params")
        except Exception as e:
            why.append(f"job {path.stem} does not rebuild: {e}")
        reads = {"prepare": set(keys)}
        if may_read_arch(test["measure"]):
            reads["the measure (may read all of it)"] = {archmod.WHOLE}
        keys = set(archmod.minimal(set().union(*reads.values())))
        if keys:
            old = _then_arch(rec, then)
            if old is None:
                why.append(f"{ARCH} of the simulation is not available")
            else:
                for who, ks in reads.items():
                    diff = sorted(p for k in ks for p in _diff(archmod.value_at(old, k), archmod.value_at(cur, k), k))
                    if diff:
                        why.append(f"{ARCH}: {', '.join(diff[:4])} changed (read by {who})")
    else:
        keys = set(meta["arch"].get("keys") or [])
        if arch_changed(meta["arch"]):
            why.append(f"{ARCH}: values the run read changed")
    if why:
        return Rehash(path, "stale", why)
    keys_l = archmod.minimal(keys)
    stamp = {"date": _dt.datetime.now().isoformat(timespec="seconds"),
             "git": _git("rev-parse", "--short", "HEAD")[1].decode().strip(),
             "files_before": len(rec)}
    new = {}
    for k, v in meta.items():                                    # keep the order of meta
        new[k] = {f: file_hash(DISK, f) for f in now.files} if k == "files" else v
    new["arch"] = {"keys": keys_l, "sha": archmod.values_sha(cur, keys_l)}
    new["views"] = dict(views)
    new["rehashed"] = stamp
    return Rehash(path, "rehashed", [], new)


def _diff(a, b, key: str) -> list[str]:
    """Leaf key paths under `key` whose values differ between two value_at results."""
    if a == b:
        return []
    va, vb = a.get("value"), b.get("value")
    if isinstance(va, dict) and isinstance(vb, dict):
        out = []
        for k in sorted(set(va) | set(vb), key=str):
            sub = str(k) if key == archmod.WHOLE else f"{key}.{k}"
            out += _diff({"value": va[k]} if k in va else {}, {"value": vb[k]} if k in vb else {}, sub)
        return out
    return [key]


def _then_arch(rec: dict, then: Git) -> dict | None:
    """The data of arch.yaml that a whole-deck record simulated with (by its recorded hash)."""
    import yaml

    h = rec.get(ARCH)
    if h is None:
        return None
    if h == file_hash(DISK, ARCH):
        return archmod.load_data()
    data = then.read(ARCH)
    if data is None or content_hash(ARCH, data) != h:
        return None
    return yaml.safe_load(data.decode("utf-8"))


def rehash(block: str | None = None, test: str | None = None, view: str | None = None,
           dry: bool = False, verbose: bool = False) -> list[Rehash]:
    """rehash_doc on every recorded result (of a block / test / view directory); writes the rehashed ones."""
    from .checks import load_results

    out = []
    for d in load_results():
        if (block and d["block"] != block) or (test and d["test"] != test) or (view and d["view"] != view):
            continue
        r = rehash_doc(d)
        out.append(r)
        relp = r.path.relative_to(REPO_ROOT).as_posix()
        if r.status == "stale" or verbose:
            print(f"  {r.status:8s} {relp}" + (f": {'; '.join(r.why[:3])}" if r.why else ""))
        if r.status == "rehashed" and not dry:
            doc = {k: v for k, v in d.items() if k != "_path"}
            doc["meta"] = r.meta
            r.path.write_text(json.dumps(doc, indent=1, default=float) + "\n", encoding="utf-8", newline="\n")
    n = {s: sum(r.status == s for r in out) for s in ("rehashed", "fresh", "stale")}
    print(f"[adcflow] rehash: {n['rehashed']} {'would be ' if dry else ''}rehashed, "
          f"{n['fresh']} already on their dependencies, {n['stale']} stale (re-run them)")
    return out
