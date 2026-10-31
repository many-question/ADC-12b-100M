"""What a result depends on (adcflow.deps): reachability, the arch values a run reads, judging and rehash.

The end-to-end cases run the flow in a temporary git repository (a copy of design/, tb/, specs/ and
tools/adcflow, so the copied package's REPO_ROOT is the copy) in a subprocess."""

import ast
import copy
import json
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

from adcflow import REPO_ROOT, arch, deps
from adcflow.netlist import content_hash
from adcflow.runner import needed_va, view_files
from adcflow.specs import find_test


# ------------------------------------------------------------------ reachability (in-memory trees)
class Mem:
    def __init__(self, files: dict[str, str]):
        self.files = {k: v.encode() for k, v in files.items()}

    def read(self, rel):
        return self.files.get(rel)


def _sub(name, body="", ports="A B"):
    return f"subckt {name} ({ports})\n{body}ends {name}\n"


TB = "simulator lang=spectre\nXDUT (a 0) blk\nV0 (a 0) vsource dc=1\ntran1 tran stop=1n\n"


def test_reach_follows_masters_across_files_and_skips_the_rest():
    t = Mem({"tb/t.scs": TB,
             "design/blk.scs": "simulator lang=spectre\n" + _sub("blk", "X1 (A B) leaf\nM1 (A B B B) nch_mac\n"),
             "design/leaf.scs": _sub("leaf", "U1 (A B) leaf_va\n"),
             "design/other.scs": _sub("other", "R1 (A B) resistor r=1\n"),
             "design/va/leaf_va.va": "module leaf_va(a, b);\nendmodule\n",
             "design/va/other_va.va": "module other_va(a, b);\nendmodule\n"})
    r = deps.reach(t, "tb/t.scs", ["design/blk.scs", "design/leaf.scs", "design/other.scs"],
                   ["design/va/leaf_va.va", "design/va/other_va.va"])
    assert r.files == ["tb/t.scs", "design/blk.scs", "design/leaf.scs", "design/va/leaf_va.va"]
    assert {"blk", "leaf", "leaf_va", "nch_mac", "vsource"} <= r.masters and "other" not in r.masters
    assert not r.problems
    assert set(r.deck) == set(t.files)


def test_reach_records_every_definition_of_a_name_and_files_with_top_level_statements():
    t = Mem({"tb/t.scs": TB,
             "design/a.scs": _sub("blk"),
             "design/b.scs": _sub("blk"),                                   # defined twice: both count
             "design/c.scs": "simulator lang=spectre\nparameters x=1\n" + _sub("unused"),
             "design/d.scs": "model blkmod relay\n" + _sub("unused2")})
    r = deps.reach(t, "tb/t.scs", ["design/a.scs", "design/b.scs", "design/c.scs", "design/d.scs"], [])
    assert r.files == ["tb/t.scs", "design/c.scs", "design/d.scs", "design/a.scs", "design/b.scs"]
    assert "relay" in r.masters                                             # a top-level model is reached


def test_reach_records_the_whole_deck_when_it_cannot_follow():
    files = {"tb/t.scs": TB, "design/blk.scs": _sub("blk") + 'include "elsewhere.scs"\n',
             "design/other.scs": _sub("other")}
    r = deps.reach(Mem(files), "tb/t.scs", ["design/blk.scs", "design/other.scs"], [])
    assert r.problems and r.files == ["tb/t.scs", "design/blk.scs", "design/other.scs"]
    files["design/blk.scs"] = "subckt blk (A B)\n"                          # not closed
    assert deps.reach(Mem(files), "tb/t.scs", ["design/blk.scs", "design/other.scs"], []).problems


def test_reach_resolves_verilog_a_includes_as_staged():
    va = ('`include "disciplines.vams"\n`include "adc_arch.vams"\n'
          "// `include \"commented_out.vams\"\nmodule tb_x_va(a);\nendmodule\n")
    t = Mem({"tb/t.scs": "U1 (a) tb_x_va\n",
             "tb/common/veriloga/tb_x_va.va": va,
             "design/behav/veriloga/adc_arch.vams": '`include "adc_arch_func.vams"\n',
             "design/behav/veriloga/adc_arch_func.vams": "// functions\n"})
    r = deps.reach(t, "tb/t.scs", [], ["tb/common/veriloga/tb_x_va.va"])
    # the stage copies adc_arch*.vams next to the testbench Verilog-A; the simulator's headers are not files
    assert r.files == ["tb/t.scs", "tb/common/veriloga/tb_x_va.va", "design/behav/veriloga/adc_arch.vams",
                       "design/behav/veriloga/adc_arch_func.vams"]
    assert not r.problems
    t.files["tb/common/veriloga/tb_x_va.va"] = b'`include "missing.vams"\nmodule tb_x_va(a);\nendmodule\n'
    assert deps.reach(t, "tb/t.scs", [], ["tb/common/veriloga/tb_x_va.va"]).problems


def test_stage_copies_are_where_staged_source_finds_them(tmp_path):
    from adcflow.runner import Job, stage
    from adcflow.corners import by_name

    stage(tmp_path, [Job("j", by_name("tt_nom_27"), {}, {}, tb_text="")], {"j": ""})
    staged = tmp_path / "stage" / "tb" / "common" / "veriloga" / "adc_arch.vams"
    src = deps.staged_source("tb/common/veriloga/adc_arch.vams", deps.DISK)
    assert src == "design/behav/veriloga/adc_arch.vams"
    assert staged.read_bytes() == (REPO_ROOT / src).read_bytes()


def test_real_decks_record_only_what_the_testbench_reaches():
    _, t = find_test("tb_clkgen_timing")
    assert deps.run_reach(t, {}).files == [
        "tb/clkgen/tb_clkgen_timing.scs", "tb/common/veriloga/tb_imeter_va.va", "design/behav/adc_clkgen.scs",
        "design/behav/veriloga/adc_clkgen_va.va", "specs/soa.yaml"]
    _, t = find_test("tb_ref_dc")
    assert deps.run_reach(t, {}).files == ["tb/ref/tb_ref_dc.scs", "design/behav/adc_ref.scs",
                                           "design/behav/veriloga/adc_ref_va.va"]
    _, t = find_test("tb_top_sine")
    files = deps.run_reach(t, {}).files
    assert {"design/top/adc_top.scs", "design/behav/veriloga/adc_arch.vams",
            "design/behav/veriloga/adc_arch_func.vams"} <= set(files)
    assert len([f for f in files if f.startswith("design/behav/adc_")]) == 6


def test_views_of_inverts_the_result_directory(tmp_path, monkeypatch):
    from adcflow import candidates

    assert deps.views_of("adc_ref", "behav") == {}
    assert deps.views_of("adc_top", "behav") == {}
    with pytest.raises(Exception):
        deps.views_of("adc_clkgen", "xtor-nobody")
    monkeypatch.setattr(candidates, "ROOT", tmp_path)
    for b in ("adc_clkgen", "adc_ref"):
        (tmp_path / "design" / "xtor" / b / "alice").mkdir(parents=True)
        (tmp_path / "design" / "xtor" / b / "alice" / f"{b}.scs").write_text("")
    assert deps.views_of("adc_clkgen", "xtor-alice") == {"adc_clkgen": "xtor:alice"}
    assert deps.views_of("adc_top", "xtor-clkgen@alice+ref@alice") == {"adc_clkgen": "xtor:alice", "adc_ref": "xtor:alice"}


# ------------------------------------------------------------------ arch values
def test_track_logs_the_keys_read():
    with arch.track() as keys:
        a = arch.Arch.load()
        _ = a.lsb, a.raw["cdac"].get("cal_n_sigma", 4), a.raw["cdac"].get("no_such_key", 0)
    assert keys == {"reference.vref", "cdac.cu", "cdac.cap_weights", "cdac.cap_sampled",
                    "cdac.cal_n_sigma", "cdac.no_such_key"}
    with arch.track() as keys:
        copy.deepcopy(a.raw["cdac"])
        list(a.raw["timing"])
    assert arch.minimal(keys | {"cdac.cu"}) == ["cdac", "timing"]
    with arch.track() as keys:
        a.c_s                                              # cached: read once per Arch, as loaded per use
    assert arch.minimal(keys) == ["cdac.cu"]
    assert arch.minimal({"*", "cdac.cu"}) == ["*"]


def test_values_sha_hashes_the_values_read_only():
    data = arch.load_data()
    keys = ["timing.fs", "cdac.cap_weights"]
    h = arch.values_sha(data, keys)
    d2 = copy.deepcopy(data)
    d2["version"] = "9.9.9"
    d2["timing"]["t_dac_add"] = [1e-12] * 13
    assert arch.values_sha(d2, keys) == h                  # values it did not read
    assert arch.values_sha(yaml.safe_load(yaml.safe_dump(data)), keys) == h   # formatting and comments
    d2["cdac"]["cap_weights"][0] += 1
    assert arch.values_sha(d2, keys) != h
    assert arch.values_sha(data, ["cdac.nope"]) != arch.values_sha({**data, "cdac": {**data["cdac"], "nope": 0}},
                                                                   ["cdac.nope"])
    assert arch.values_sha(d2, ["*"]) != arch.values_sha(data, ["*"])


@pytest.mark.needs_toolbox
def test_build_jobs_records_the_keys_prepare_reads():
    pytest.importorskip("adctoolbox")
    from adcflow.corners import by_name
    from adcflow.runner import build_jobs

    b, t = find_test("tb_ref_replay")
    [j] = build_jobs(b, "tb_ref_replay", t, [by_name("tt_nom_27")], {}, {})
    assert {"timing.t_dac_add", "timing.fs", "reference.vin_cm"} <= j.arch_keys    # load waveform from the model
    b, t = find_test("tb_bootstrap_track")
    [j] = build_jobs(b, "tb_bootstrap_track", t, [by_name("tt_nom_27")], {}, {})
    assert j.arch_keys == set()


def test_may_read_arch_follows_the_measure_function():
    assert not deps.may_read_arch("adcflow.measure.ref:dc")
    assert not deps.may_read_arch("adcflow.measure.ref:startup")
    assert not deps.may_read_arch("adcflow.measure.clkgen:timing")
    assert not deps.may_read_arch("adcflow.measure.bootstrap:track")
    assert deps.may_read_arch("adcflow.measure.ref:replay")               # replay_pattern -> Arch.load
    assert deps.may_read_arch("adcflow.measure.cdac:weights")
    assert deps.may_read_arch("adcflow.measure.top:sine")
    assert deps.may_read_arch("adcflow.measure.nosuchmodule:f")
    assert deps.module_reads_arch("adcflow.model") and not deps.module_reads_arch("adcflow.psf")


# ------------------------------------------------------------------ judge and rehash, end to end
@pytest.fixture
def repo(tmp_path):
    """A git repository with the design, testbenches, specs and the flow of this checkout."""
    root = tmp_path / "repo"
    for d in ("design", "tb", "specs"):
        shutil.copytree(REPO_ROOT / d, root / d, ignore=shutil.ignore_patterns("*.png"))
    shutil.copytree(REPO_ROOT / "tools" / "adcflow", root / "tools" / "adcflow",
                    ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    commit(root, "base")
    return root


def git(root, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root,
                          capture_output=True, text=True, check=True).stdout.strip()


def commit(root, msg):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", msg)
    return git(root, "rev-parse", "--short", "HEAD")


def edit(root, rel, old, new):
    p = root / rel
    text = p.read_text(encoding="utf-8")
    assert old in text, (rel, old)
    p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def legacy_result(root, block, test, corner="tt_nom_27"):
    """A result recorded the old way (every deck file, the testbench and arch.yaml hashed) at HEAD,
    with the params of the behavioral result of this checkout."""
    _, t = find_test(test, block)
    vf = view_files({})
    tb = REPO_ROOT / t["netlist"]
    paths = vf + needed_va(vf, tb.read_text(encoding="utf-8"))
    paths += ([REPO_ROOT / "specs" / "soa.yaml"] if t.get("soa") else []) + [tb, REPO_ROOT / "specs" / "arch.yaml"]
    rels = [p.relative_to(REPO_ROOT).as_posix() for p in paths]
    params = json.loads((REPO_ROOT / "results" / block / test / "behav" / f"{corner}.json").read_text(encoding="utf-8"))["params"]
    doc = {"block": block, "test": test, "view": "behav", "corner": corner, "params": params,
           "globals": {}, "metrics": {}, "specs": {}, "figures": [],
           "meta": {"git": git(root, "rev-parse", "--short", "HEAD"), "git_clean": True,
                    "files": {r: content_hash(root / r) for r in rels}}}
    out = root / "results" / block / test / "behav" / f"{corner}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    return out


def flow(root, code: str):
    """Run `code` with the copied flow (its REPO_ROOT is the copy); it prints one JSON value last."""
    pre = ("import json\nfrom pathlib import Path\nimport adcflow\n"
           "assert adcflow.REPO_ROOT.resolve() == Path.cwd().resolve().parent, adcflow.REPO_ROOT\n"
           "from adcflow import deps, checks\n"
           "def doc(p):\n    d = json.loads(Path(p).read_text(encoding='utf-8'))\n    d['_path'] = Path(p).resolve()\n"
           "    return d\n"
           "def rehash(p):\n    r = deps.rehash_doc(doc(p))\n    return {'status': r.status, 'why': r.why, 'meta': r.meta}\n")
    env = {**os.environ, "PYTHONPATH": str(root / "tools")}
    p = subprocess.run([sys.executable, "-c", pre + textwrap.dedent(code)], cwd=root / "tools", env=env,
                       capture_output=True, text=True, timeout=600)
    assert p.returncode == 0, p.stderr[-3000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def test_rehash_moves_a_whole_deck_record_past_unrelated_changes(repo):
    res = legacy_result(repo, "adc_clkgen", "tb_clkgen_timing")
    # what PR #48 did to every candidate's records: other blocks' models and arch.yaml changed
    edit(repo, "design/behav/adc_ref.scs", "parameters cdec=6p", "parameters cdec=7p")
    edit(repo, "design/behav/veriloga/adc_cdac_sw_va.va", "module", "// changed\nmodule")
    edit(repo, "specs/arch.yaml", "version: ", "version: 9")
    out = flow(repo, f"""
        p = {str(res)!r}
        before = checks.judge(doc(p))['stale']
        r = deps.rehash('adc_clkgen')
        after = checks.judge(doc(p))
        print(json.dumps({{'before': before, 'status': [x.status for x in r], 'after': after['stale'],
                          'meta': doc(p)['meta']}}))""")
    assert set(out["before"]) == {"design/behav/adc_ref.scs", "design/behav/veriloga/adc_cdac_sw_va.va", "specs/arch.yaml"}
    assert out["status"] == ["rehashed"] and out["after"] == []
    m = out["meta"]
    assert list(m["files"]) == ["tb/clkgen/tb_clkgen_timing.scs", "tb/common/veriloga/tb_imeter_va.va",
                                "design/behav/adc_clkgen.scs", "design/behav/veriloga/adc_clkgen_va.va", "specs/soa.yaml"]
    assert m["arch"]["keys"] == [] and m["views"] == {} and m["rehashed"]["files_before"] == 18
    # a reduced record is stale when another file starts to define one of its masters ...
    edit(repo, "design/behav/adc_ref.scs", "\nsubckt adc_ref", "\nsubckt tb_imeter_va (P N)\nends tb_imeter_va\nsubckt adc_ref")
    assert flow(repo, f"print(json.dumps(checks.judge(doc({str(res)!r}))['stale']))") == ["design/behav/adc_ref.scs"]
    # ... or one of its files changes
    git(repo, "checkout", "--", "design/behav/adc_ref.scs")
    edit(repo, "design/behav/adc_clkgen.scs", "td_s=40p", "td_s=41p")
    assert flow(repo, f"print(json.dumps(checks.judge(doc({str(res)!r}))['stale']))") == ["design/behav/adc_clkgen.scs"]


def test_rehash_keeps_a_result_stale_when_its_circuit_changed(repo):
    res = legacy_result(repo, "adc_clkgen", "tb_clkgen_timing")
    edit(repo, "design/behav/adc_clkgen.scs", "td_s=40p", "td_s=41p")
    r = flow(repo, f"print(json.dumps(rehash({str(res)!r})))")
    assert r["status"] == "stale" and r["why"] == ["design/behav/adc_clkgen.scs: changed"]


def test_rehash_checks_what_changed_files_defined_for_the_simulation(repo):
    # simulated while an unreached file also defined a reached master; the definition is gone now
    edit(repo, "design/behav/adc_ref.scs", "\nsubckt adc_ref", "\nsubckt tb_imeter_va (P N)\nends tb_imeter_va\nsubckt adc_ref")
    commit(repo, "duplicate definition")
    res = legacy_result(repo, "adc_clkgen", "tb_clkgen_timing")
    git(repo, "revert", "--no-edit", "HEAD")
    r = flow(repo, f"print(json.dumps(rehash({str(res)!r})))")
    assert r["status"] == "stale" and r["why"] == ["design/behav/adc_ref.scs: changed and defines tb_imeter_va"]
    # without the commit the old content is unknown: stale as well
    d = json.loads(res.read_text(encoding="utf-8"))
    d["meta"]["git"] = "0000000"
    res.write_text(json.dumps(d), encoding="utf-8")
    r = flow(repo, f"print(json.dumps(rehash({str(res)!r})))")
    assert r["status"] == "stale" and all("is not available" in w for w in r["why"])


def test_rehash_needs_the_commit_for_files_the_record_did_not_hash(repo):
    res = legacy_result(repo, "adc_sarlogic", "tb_sarlogic_func")     # reaches adc_arch*.vams, never hashed before
    d = json.loads(res.read_text(encoding="utf-8"))
    d["meta"]["git_clean"] = False
    res.write_text(json.dumps(d), encoding="utf-8")
    r = flow(repo, f"print(json.dumps(rehash({str(res)!r})))")
    assert r["status"] == "stale"
    assert "what it included for the simulation is not available" in r["why"][0]


@pytest.mark.needs_toolbox
def test_rehash_checks_the_arch_values_prepare_and_the_measure_read(repo):
    pytest.importorskip("adctoolbox")
    res_replay = legacy_result(repo, "adc_ref", "tb_ref_replay")
    res_dc = legacy_result(repo, "adc_ref", "tb_ref_dc")
    edit(repo, "specs/arch.yaml", "t_dac_add: [0, 0, 10.0e-12", "t_dac_add: [0, 0, 11.0e-12")
    r = flow(repo, f"print(json.dumps([rehash({str(res_replay)!r}), rehash({str(res_dc)!r})]))")
    assert r[0]["status"] == "stale"
    assert "specs/arch.yaml: timing.t_dac_add changed (read by prepare)" in r[0]["why"]
    assert r[1]["status"] == "rehashed" and r[1]["meta"]["arch"]["keys"] == []
    # a value only the replay measure may read (the static check counts the whole file for it)
    git(repo, "checkout", "--", "specs/arch.yaml")
    edit(repo, "specs/arch.yaml", "enob_min: 10.5", "enob_min: 10.6")
    r = flow(repo, f"print(json.dumps(rehash({str(res_replay)!r})))")
    assert r["status"] == "stale" and r["why"] == [
        "specs/arch.yaml: targets.enob_min changed (read by the measure (may read all of it))"]
    git(repo, "checkout", "--", "specs/arch.yaml")
    r = flow(repo, f"print(json.dumps(rehash({str(res_replay)!r})))")
    assert r["status"] == "rehashed" and r["meta"]["arch"]["keys"] == ["*"]


def test_judge_checks_the_recorded_arch_values(repo):
    res = legacy_result(repo, "adc_ref", "tb_ref_dc")
    d = json.loads(res.read_text(encoding="utf-8"))
    d["meta"].update(flow(repo, "from adcflow.specs import find_test\n"
                                "print(json.dumps(deps.record_meta(find_test('tb_ref_dc')[1], {}, {'reference.vref'})))"))
    res.write_text(json.dumps(d), encoding="utf-8")
    judge = f"print(json.dumps(checks.judge(doc({str(res)!r}))['stale']))"
    assert flow(repo, judge) == []
    edit(repo, "specs/arch.yaml", "version: ", "version: 9")
    assert flow(repo, judge) == []
    edit(repo, "specs/arch.yaml", "vref: 0.90", "vref: 0.91")
    assert flow(repo, judge) == ["specs/arch.yaml"]


# ------------------------------------------------------------------ guard: arch.yaml read per use, never at import
# meta.arch relies on prepare and measure code reading arch.yaml through Arch.load() per use, inside
# arch.track(): a read at import time happens once, outside any job, and later jobs would record
# too few keys (and stay fresh when they should be stale).
IMPORT_TIME_OK = {
    "adcflow.gen_tb",   # generation time only (`adcflow gen`): its testbenches are hashed as files
    "adcflow.arch",     # defines ARCH_YAML (a path, not a read) and the loader itself
}


def module_level_arch_reads(tree) -> list[str]:
    """What module-level code of a module (outside function bodies; class bodies run at import and
    count) does that reads arch.yaml: a call of Arch.load() / load_data(), or a name of the file."""
    hits = []

    def walk(node):
        for n in ast.iter_child_nodes(node):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                for d in getattr(n, "decorator_list", []) + list(n.args.defaults) + list(n.args.kw_defaults or []):
                    if d is not None:
                        walk_expr(d)
                continue
            check(n)
            walk(n)

    def walk_expr(node):
        for n in ast.walk(node):
            check(n)

    def check(n):
        if isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            base = f.value if isinstance(f, ast.Attribute) else None
            if name == "load_data" or (name == "load" and isinstance(base, (ast.Name, ast.Attribute))
                                       and (getattr(base, "id", None) == "Arch" or getattr(base, "attr", None) == "Arch")):
                hits.append(f"line {n.lineno}: {ast.unparse(n)}")
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and "arch.yaml" in n.value:
            hits.append(f"line {n.lineno}: names arch.yaml")
        elif isinstance(n, ast.Name) and n.id == "ARCH_YAML":
            hits.append(f"line {n.lineno}: ARCH_YAML")

    walk(tree)
    return hits


def imports_analysis(tree) -> bool:
    for n in ast.walk(tree):
        if isinstance(n, ast.Import) and any(a.name.split(".")[0] == "analysis" for a in n.names):
            return True
        if isinstance(n, ast.ImportFrom) and not n.level and (n.module or "").split(".")[0] == "analysis":
            return True
    return False


def reached_modules(mod: str) -> set[str]:
    seen, todo = set(), [mod]
    while todo:
        m = todo.pop()
        if m in seen or deps._ast(m) is None:
            continue
        seen.add(m)
        todo += deps._imports(m, deps._ast(m))
    return seen


def test_module_level_arch_reads_are_caught():
    assert module_level_arch_reads(ast.parse("from adcflow.arch import Arch\nA = Arch.load()\n"))
    assert module_level_arch_reads(ast.parse("from adcflow import arch\nFS = arch.Arch.load().fs\n"))
    assert module_level_arch_reads(ast.parse("from adcflow import arch\nD = arch.load_data()\n"))
    assert module_level_arch_reads(ast.parse("import yaml\nD = yaml.safe_load(open('specs/arch.yaml'))\n"))
    assert module_level_arch_reads(ast.parse("class C:\n    a = Arch.load()\n"))
    assert module_level_arch_reads(ast.parse("def f(a=Arch.load()):\n    pass\n"))
    assert not module_level_arch_reads(ast.parse("from adcflow.arch import Arch\ndef f():\n    return Arch.load().fs\n"))
    assert imports_analysis(ast.parse("def f():\n    from analysis.x import y\n"))
    assert not imports_analysis(ast.parse("from .analysis import y\n"))


def test_prepare_and_measure_code_reads_arch_per_use():
    from adcflow.specs import blocks

    refs = {t[k] for b in blocks().values() for t in b.tests.values() for k in ("prepare", "measure") if t.get(k)}
    assert refs, "no prepare / measure in the block specs"
    mods = set().union(*(reached_modules(r.split(":")[0]) for r in refs))
    assert "adcflow.measure.ref" in mods and "adcflow.model" in mods
    bad = {}
    for m in sorted(mods - IMPORT_TIME_OK):
        t = deps._ast(m)
        hits = module_level_arch_reads(t) + (["imports analysis/"] if imports_analysis(t) else [])
        if hits:
            bad[m] = hits
    assert not bad, f"arch.yaml read at import time (outside arch.track): {bad}"


# ------------------------------------------------------------------ the site build has no matplotlib
_NO_MPL = """
import json, sys
sys.modules["matplotlib"] = None          # the site build installs the core package only
from adcflow import candidates, checks
stale = {str(d["_path"]): checks.judge(d)["stale"] for d in checks.load_results()}
rows = [[r["block"], r["candidate"], r["eligible"], r["missing"]] for r in candidates.leaderboard()]
print(json.dumps({"stale": stale, "rows": rows}))
"""


def test_freshness_and_leaderboard_need_no_matplotlib():
    """Staleness, verification and the leaderboard must not import the figure code (matplotlib):
    the site build has only the core package, and an import error on that path once made every
    result look stale on the site. The answer must equal the one computed with matplotlib."""
    from adcflow import candidates, checks

    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "tools")}
    out = subprocess.run([sys.executable, "-c", _NO_MPL], capture_output=True, text=True, env=env,
                         cwd=REPO_ROOT, encoding="utf-8")
    assert out.returncode == 0, out.stderr[-2000:]
    got = json.loads(out.stdout.strip().splitlines()[-1])
    want_stale = {str(d["_path"]): checks.judge(d)["stale"] for d in checks.load_results()}
    want_rows = [[r["block"], r["candidate"], r["eligible"], r["missing"]] for r in candidates.leaderboard()]
    assert got["stale"] == want_stale and got["rows"] == want_rows


def test_judge_raises_unexpected_errors_and_marks_unresolved_ones_stale(monkeypatch):
    """Only a test / view / file that no longer resolves makes a result stale; anything else (a
    missing package, a bug) is raised instead of being shown as "stale"."""
    from adcflow import checks

    doc = next(d for d in checks.load_results() if "arch" in (d.get("meta") or {}))

    def unresolved(_):
        raise ValueError("adc_comp: no candidate 'gone'")

    def broken(_):
        raise ModuleNotFoundError("No module named 'matplotlib'")

    monkeypatch.setattr(deps, "unrecorded", unresolved)
    assert "(dependencies: adc_comp: no candidate 'gone')" in checks.judge(doc)["stale"]
    monkeypatch.setattr(deps, "unrecorded", broken)
    with pytest.raises(ModuleNotFoundError):
        checks.judge(doc)
