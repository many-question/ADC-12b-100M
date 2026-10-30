"""Verification combinations of the top level (site/sitegen/combos.py): rows built from result directories.

Fixture result trees under tmp_path; judging is adcflow.checks.judge against main's specs; no matplotlib is imported."""

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

from adcflow import candidates as C, checks                       # noqa: E402
from adcflow.netlist import content_hash                          # noqa: E402
from adcflow.specs import blocks                                  # noqa: E402
from sitegen import cands, combos                                 # noqa: E402

TOP = blocks()["adc_top"]
BLOCKS = [b for b in blocks() if b != "adc_top"]
INPUT = "specs/arch.yaml"                                          # an input file every result of the fixture records


def doc(test, sig, corner, *, enob=10.9, sfdr=80.0, t_conv=3.0, spikes=0, rdy=0, power=None, file_hash=None):
    metrics = {"enob": enob, "sfdr_dBc": sfdr, "fs_peak_V": 0.99, "missing_rdy": rdy, "t_conv_max_ns": t_conv, "spike_count": spikes}
    metrics.update(power or {})
    return {"block": "adc_top", "test": test, "view": sig, "corner": corner, "metrics": metrics, "globals": {},
            "meta": {"git": "abc1234", "files": {INPUT: file_hash or content_hash(ROOT / INPUT)}}}


def write(root: Path, d, case=""):
    p = root / "results" / "adc_top" / d["test"] / d["view"] / f"{d['corner']}{case}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d), encoding="utf-8")


def fill(root: Path, sig: str, *, corners=("tt_nom_27", "ff_high_125"), **kw):
    """tb_top_sine at each corner and tb_top_duty (two duty cases per corner), tb_top_sine_lf at the typical corner."""
    for c in corners:
        write(root, doc("tb_top_sine", sig, c, **kw))
        for duty in ("0.45", "0.55"):
            write(root, doc("tb_top_duty", sig, c, **kw), case=f"__duty{duty}")
    write(root, doc("tb_top_sine_lf", sig, "tt_nom_27", **kw))


def judged(root: Path) -> list[dict]:
    """Load and judge the fixture results the way the site's data layer does, with the repository roots pointed at the fixture."""
    (root / INPUT).parent.mkdir(parents=True, exist_ok=True)
    (root / INPUT).write_bytes((ROOT / INPUT).read_bytes())          # the input the results record, as in a checkout
    with cands.tree_root(root):
        docs = checks.load_results()
        for d in docs:
            d["_judged"] = checks.judge(d)
    return docs


def build(root: Path, cs=None, selected=lambda b: None):
    return combos.build(judged(root), TOP, BLOCKS, selected, cs or {})


def row_stub(block, name, *, verified=1, results=1, selected=False, author="Alice (@alice)", source="main", pr=None):
    r = {"block": block, "candidate": name, "author_text": author, "verified": verified, "results": results, "selected": selected}
    return SimpleNamespace(name=name, source=source, row=r, pr=SimpleNamespace(number=pr) if pr else None)


# ------------------------------------------------------------------ rows come from the directory names
def test_one_row_per_signature_found_in_results_ordered_by_number_of_xtor_blocks(tmp_path):
    for sig in ("xtor-bootstrap@alice+clkgen@alice", "xtor-ref@bob", "behav", "xtor-clkgen@alice"):
        fill(tmp_path, sig, corners=("tt_nom_27",))
    got = build(tmp_path)
    assert [c.signature for c in got] == ["behav", "xtor-clkgen@alice", "xtor-ref@bob", "xtor-bootstrap@alice+clkgen@alice"]
    assert [c.n_xtor for c in got] == [0, 1, 1, 2]
    two = got[-1]
    assert [(b.block, b.candidate) for b in two.xtor] == [("adc_bootstrap", "alice"), ("adc_clkgen", "alice")]


def test_nothing_is_hard_coded_a_new_signature_is_a_new_row(tmp_path):
    fill(tmp_path, "behav", corners=("tt_nom_27",))
    assert [c.signature for c in build(tmp_path)] == ["behav"]
    fill(tmp_path, "xtor-sarlogic@carol", corners=("tt_nom_27",))
    assert [c.signature for c in build(tmp_path)] == ["behav", "xtor-sarlogic@carol"]


def test_directories_that_are_not_view_signatures_are_ignored(tmp_path):
    fill(tmp_path, "behav", corners=("tt_nom_27",))
    for odd in ("xtor-nosuchblock@x", "xtor-clkgen@A", "xtor-", "scratch", "xtor-clkgen@a+"):
        fill(tmp_path, odd, corners=("tt_nom_27",))
    assert [c.signature for c in build(tmp_path)] == ["behav"]


def test_legacy_xtor_signature_means_every_block(tmp_path):
    fill(tmp_path, "xtor", corners=("tt_nom_27",))
    (row,) = build(tmp_path)
    assert row.legacy and [b.block for b in row.xtor] == BLOCKS and all(b.candidate is None for b in row.xtor)


def test_parse_signature_is_the_inverse_of_candidates_top_signature(monkeypatch):
    monkeypatch.setattr(C, "view_dir", lambda block, view: "xtor-" + view[5:] if view.startswith("xtor:") else view)
    views = {"adc_clkgen": "xtor:alice", "adc_bootstrap": "xtor:alice", "adc_ref": "behav"}
    sig = C.top_signature(views, len(BLOCKS))
    assert sig == "xtor-bootstrap@alice+clkgen@alice"
    assert combos.parse_signature(sig, BLOCKS) == ([("adc_bootstrap", "alice"), ("adc_clkgen", "alice")], False)
    assert combos.parse_signature(C.top_signature({}, len(BLOCKS)), BLOCKS) == ([], False)          # behav
    assert combos.parse_signature("xtor", BLOCKS)[1] is True


# ------------------------------------------------------------------ what a row shows
def test_corner_coverage_per_top_test_and_results_count(tmp_path):
    fill(tmp_path, "xtor-clkgen@alice")
    (row,) = build(tmp_path)
    cov = {t.test: t for t in row.tests}
    assert (cov["tb_top_sine"].corners, cov["tb_top_sine"].required, cov["tb_top_sine"].results) == (2, 45, 2)
    assert (cov["tb_top_duty"].corners, cov["tb_top_duty"].required, cov["tb_top_duty"].results) == (2, 7, 4)     # two duty cases per corner
    assert (cov["tb_top_sine_lf"].corners, cov["tb_top_sine_lf"].required) == (1, 1)
    assert row.dirs["tb_top_sine"] == "results/adc_top/tb_top_sine/xtor-clkgen@alice"
    assert not row.full                                              # a regression subset: 2 of 45 corners


def test_only_the_covered_tests_are_listed_and_a_complete_test_set_is_full(tmp_path):
    write(tmp_path, doc("tb_top_sine_lf", "xtor-ref@bob", "tt_nom_27"))
    (row,) = build(tmp_path)
    assert [t.test for t in row.tests] == ["tb_top_sine_lf"] and row.full


def test_specs_are_counted_where_they_apply_and_failures_are_named(tmp_path):
    write(tmp_path, doc("tb_top_sine", "behav", "tt_nom_27"))
    write(tmp_path, doc("tb_top_sine", "xtor-ref@bob", "tt_nom_27", enob=9.0))     # TOP-01 (>= 10.5) and TOP-02 fail
    ok, bad = build(tmp_path)
    assert ok.signature == "behav" and ok.failing == [] and ok.specs_pass == ok.specs_applicable > 0
    assert bad.failing and "TOP-01" in bad.failing and bad.specs_pass < bad.specs_applicable
    assert bad.specs_total == len([s for s in TOP.specs if not s.reported])


def test_key_metrics_show_the_worst_value_with_its_corner_and_margin(tmp_path):
    write(tmp_path, doc("tb_top_sine", "xtor-ref@bob", "tt_nom_27", enob=10.9, sfdr=85.0, t_conv=3.0))
    write(tmp_path, doc("tb_top_sine", "xtor-ref@bob", "ff_high_125", enob=10.62, sfdr=79.0, t_conv=4.1, spikes=0))
    (row,) = build(tmp_path)
    m = {x.spec: x for x in row.metrics}
    assert (m["TOP-01"].value, m["TOP-01"].corner) == (10.62, "ff_high_125") and m["TOP-01"].margin == pytest.approx(0.12)     # min of >= 10.5
    assert (m["TOP-03"].value, m["TOP-03"].corner) == (79.0, "ff_high_125")                     # worst SFDR is the lowest
    assert (m["TOP-06"].value, m["TOP-06"].corner) == (4.1, "ff_high_125") and m["TOP-06"].margin == pytest.approx(0.3)   # worst time is the highest
    assert "TOP-10" in m and "TOP-08" not in m                       # TOP-08 / TOP-09 only when their tests have results


def test_a_failing_metric_has_a_negative_margin(tmp_path):
    write(tmp_path, doc("tb_top_sine", "behav", "tt_nom_27", enob=10.2))
    (row,) = build(tmp_path)
    assert {x.spec: x for x in row.metrics}["TOP-01"].margin == pytest.approx(-0.3)


def test_power_per_supply_prefers_the_typical_corner(tmp_path):
    p = lambda a, d, h: {"p_avdd_mW": a, "p_dvdd_mW": d, "p_avdd18_mW": h, "power_mW": a + d + h}      # noqa: E731
    write(tmp_path, doc("tb_top_sine", "behav", "ff_high_125", power=p(9.0, 9.0, 9.0)))
    write(tmp_path, doc("tb_top_sine", "behav", "tt_nom_27", power=p(0.3, 0.2, 14.0)))
    (row,) = build(tmp_path)
    assert row.power_corner == "tt_nom_27" and row.power == {"avdd": 0.3, "dvdd": 0.2, "avdd18": 14.0}
    write(tmp_path, doc("tb_top_sine", "xtor-ref@bob", "tt_nom_27"))                            # no power recorded
    assert build(tmp_path)[1].power == {}


def test_stale_results_are_counted_with_the_same_judge(tmp_path):
    fill(tmp_path, "behav", corners=("tt_nom_27",))
    write(tmp_path, doc("tb_top_sine", "xtor-ref@bob", "tt_nom_27", file_hash="0" * 16))
    fresh, stale = build(tmp_path)
    assert (fresh.stale, stale.stale, stale.results) == (0, 1, 1)


# ------------------------------------------------------------------ the transistor-level blocks
def test_block_state_selected_verified_self_reported_and_unmerged(tmp_path):
    fill(tmp_path, "xtor-bootstrap@alice+clkgen@alice+ref@bob+comp@dan", corners=("tt_nom_27",))
    cs = {"adc_bootstrap": [row_stub("adc_bootstrap", "alice", verified=3, results=3, selected=True)],
          "adc_clkgen": [row_stub("adc_clkgen", "alice", verified=0, results=4)],
          "adc_ref": [row_stub("adc_ref", "bob", verified=1, results=4)],
          "adc_comp": [row_stub("adc_comp", "dan", source="pr", pr=61, author="Dan (@dan)")]}
    (row,) = build(tmp_path, cs, selected=lambda b: "alice" if b == "adc_bootstrap" else None)
    st = {b.block: b for b in row.xtor}
    assert (st["adc_bootstrap"].verification, st["adc_bootstrap"].selected) == ("verified", True)
    assert (st["adc_clkgen"].verification, st["adc_clkgen"].selected) == ("self-reported", False)
    assert st["adc_ref"].verification == "mixed" and (st["adc_ref"].verified, st["adc_ref"].results) == (1, 4)
    assert (st["adc_comp"].merged, st["adc_comp"].pr, st["adc_comp"].author_text) == (False, 61, "Dan (@dan)")
    assert st["adc_bootstrap"].author_text == "Alice (@alice)"


def test_a_candidate_the_site_does_not_know_is_unknown_not_verified(tmp_path):
    fill(tmp_path, "xtor-clkgen@alice", corners=("tt_nom_27",))
    (row,) = build(tmp_path, {})
    assert row.xtor[0].verification == "unknown" and row.xtor[0].author_text == ""


# ------------------------------------------------------------------ no matplotlib, and the real results
_NO_MPL = """
import json, sys
sys.modules["matplotlib"] = None          # the site build installs the core package only
sys.path.insert(0, "site")
from adcflow import checks
from adcflow.specs import blocks
from sitegen import combos
docs = checks.load_results()
for d in docs:
    d["_judged"] = checks.judge(d)
rows = combos.build(docs, blocks()["adc_top"], [b for b in blocks() if b != "adc_top"], lambda b: blocks()[b].selected)
print(json.dumps([[c.signature, c.results, c.stale, c.specs_pass, c.specs_applicable] for c in rows]))
"""


def test_combinations_need_no_matplotlib_and_match_the_in_process_answer():
    import os
    env = {**os.environ, "PYTHONPATH": str(ROOT / "tools")}
    out = subprocess.run([sys.executable, "-c", _NO_MPL], capture_output=True, text=True, env=env, cwd=ROOT, encoding="utf-8")
    assert out.returncode == 0, out.stderr[-2000:]
    got = json.loads(out.stdout.strip().splitlines()[-1])
    docs = checks.load_results()
    for d in docs:
        d["_judged"] = checks.judge(d)
    want = combos.build(docs, TOP, BLOCKS, lambda b: blocks()[b].selected)
    assert got == [[c.signature, c.results, c.stale, c.specs_pass, c.specs_applicable] for c in want]
    assert got and got[0][0] == "behav"                              # the repository's own results: all-behavioral first
