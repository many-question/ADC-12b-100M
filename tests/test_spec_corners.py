"""A spec judges only the corners of its corner set (issue #29).

tb_clkgen_timing mixes `corners: all` specs (CLK-01 .. CLK-08) with CLK-10 (`corners: typ`):
a result at ff_high_125 is judged on CLK-01 .. CLK-08, while its AVDD current stays in the
result as a raw value that CLK-10 does not judge (N/A). CLK-10 is reported only since adc_clkgen
0.6.0 (#75: no limit, no verdict); the tests of the corner rule with a limit give it back the TT
limit it had until 0.5.1 (`clk10_limit`), the last tests check the reported-only spec itself.

The synthetic records live under a temporary repository root and the verdict checks stub the
evidence-figure check (tests/test_figures.py tests it): real results/ and their figures, which
differ between branches, cannot change these verdicts (#41).
"""

import subprocess

import pytest
import yaml

from adcflow import checks, results, runner
from adcflow.corners import by_name, corner_names
from adcflow.specs import blocks

BLOCK = "adc_clkgen"
TEST = "tb_clkgen_timing"
GOOD = {"td_s_ps": 46.0, "skew_sb_ps": 40.0, "nov_bc_ps": 20.0, "td_conv_ps": 110.0, "nov_cb_ps": 20.0,
        "tf_s_ps": 10.0, "skew_ssb_ps": 2.0, "duty_errors": 0, "iavg_uA": 70.0, "soa_violations": 0}


@pytest.fixture(autouse=True)
def _isolated_root(tmp_path, monkeypatch):
    """The checks see a temporary repository root, never the real results/ directory."""
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    return tmp_path


@pytest.fixture
def clk10_limit(monkeypatch):
    """CLK-10 as it was until adc_clkgen 0.5.1: a TT limit of 80 uA (the corner rule with a limit)."""
    s = _spec("CLK-10")
    monkeypatch.setattr(s, "reported", False)
    monkeypatch.setattr(s, "max", 80)
    return s


def _doc(corner: str, test: str = TEST, view: str = "xtor", mc=None, job: str | None = None, **metrics) -> dict:
    job = job or corner
    return {"block": BLOCK, "test": test, "view": view, "corner": corner, "metrics": {**GOOD, **metrics},
            "meta": {"mc": mc, "files": {}},
            "_path": checks.REPO_ROOT / "results" / BLOCK / test / view / f"{job}.json"}


def _spec(sid: str):
    return next(s for s in blocks()[BLOCK].specs if s.id == sid)


def _summary(sid: str, docs: list[dict]) -> results.SpecSummary:
    return results.summarize(_spec(sid), [(d, checks.judge(d)) for d in docs])


def _check(monkeypatch, docs: list[dict], figures: bool = False) -> checks.Report:
    """check_results on `docs` only; the evidence-figure check, which a verdict test is not
    about, is stubbed unless `figures`."""
    monkeypatch.setattr(checks, "load_results", lambda: docs)
    if not figures:
        monkeypatch.setattr(checks, "_check_figures", lambda *a, **k: None)
    return checks.check_results()


def _warnings(monkeypatch, docs: list[dict]) -> list[str]:
    rep = _check(monkeypatch, docs)
    assert rep.errors == []
    return rep.warnings


def test_corner_sets_expand_as_corner_set():
    clk10, clk01 = _spec("CLK-10"), _spec("CLK-01")
    assert clk10.corners == "typ" and corner_names("typ") == {"tt_nom_27"}
    assert clk10.applies("tt_nom_27") and clk10.applies(by_name("tt_nom_27"))
    assert not clk10.applies("ff_high_125")
    assert all(clk01.applies(c) for c in corner_names("all")) and len(corner_names("all")) == 45


def test_monte_carlo_rule_is_kept():
    """A Monte Carlo spec judges Monte Carlo runs only (and only in its corner set); others judge both."""
    mc = {"runs": 50, "seed": 6303, "firstrun": 1, "variations": "mismatch", "models": "local_tt"}   # meta.mc
    cmp03 = next(s for s in blocks()["adc_comp"].specs if s.id == "CMP-03")
    assert cmp03.mc and cmp03.corners == "typ" and cmp03.test == "tb_comp_offset_mc"
    assert not cmp03.applies("tt_nom_27") and cmp03.applies("tt_nom_27", mc)
    assert not cmp03.applies("ff_high_125", mc)
    assert _spec("CLK-10").applies("tt_nom_27", mc)
    judged, na = blocks()["adc_comp"].verdicts("tb_comp_offset_mc", "tt_nom_27", None, {"offset_sigma_mV": 3.0})
    assert "CMP-03" not in judged and "CMP-03" not in na       # nominal run: left out, as before
    # (sample coverage and failed samples: tests/test_comp_offset_mc.py)


def test_tt_passes_while_another_corner_exceeds_the_tt_limit(monkeypatch, clk10_limit):
    tt, ff = _doc("tt_nom_27", iavg_uA=79.34202385), _doc("ff_high_125", iavg_uA=569.2671382)
    j = checks.judge(ff)
    assert "CLK-10" not in j["specs"] and j["na"]["CLK-10"]["value"] == pytest.approx(569.2671382)
    assert all(j["specs"][f"CLK-0{i}"]["pass"] for i in range(1, 9))
    r = _summary("CLK-10", [tt, ff])
    assert r.status == "pass" and r.worst == pytest.approx(79.34202385)
    assert (r.covered, r.need) == (1, 1)
    assert r.na == [("ff_high_125", pytest.approx(569.2671382))]
    assert not any("CLK-10" in w for w in _warnings(monkeypatch, [tt, ff]))


def test_tt_really_fails(monkeypatch, clk10_limit):
    tt, ff = _doc("tt_nom_27", iavg_uA=85.0), _doc("ff_high_125", iavg_uA=569.0)
    r = _summary("CLK-10", [tt, ff])
    assert r.status == "fail" and r.worst == pytest.approx(85.0) and (r.covered, r.need) == (1, 1)
    w = [x for x in _warnings(monkeypatch, [tt, ff]) if "CLK-10" in x]
    assert len(w) == 1 and "tt_nom_27.json" in w[0]


def test_tt_missing_is_incomplete_not_a_pass(monkeypatch):
    ff = _doc("ff_high_125", iavg_uA=569.0)
    r = _summary("CLK-10", [ff])
    assert r.status == "none" and r.worst is None and (r.covered, r.need) == (0, 1)
    assert len(r.na) == 1
    # a block in sign-off needs the applicable corner, and only that one
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "none")      # these docs are the legacy plain xtor view
    monkeypatch.setitem(blocks()[BLOCK].raw, "status", "signoff")
    errs = [e for e in _check(monkeypatch, [_doc(by_name("ff_high_125").name)]).errors if "CLK-10" in e]
    assert errs == ["adc_clkgen CLK-10: no xtor result for corner tt_nom_27 (tb_clkgen_timing)"]


def test_signoff_needs_every_applicable_corner_and_ignores_the_others(monkeypatch):
    docs = [_doc(c) for c in sorted(corner_names("all"))]
    docs = [d if d["corner"] != "ff_high_125" else _doc("ff_high_125", iavg_uA=569.0) for d in docs]
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "none")      # these docs are the legacy plain xtor view
    monkeypatch.setitem(blocks()[BLOCK].raw, "status", "signoff")
    assert [e for e in _check(monkeypatch, docs).errors if "CLK-09" not in e] == []     # CLK-09: jitter test
    docs.remove(next(d for d in docs if d["corner"] == "ss_low_m40"))
    errs = [e for e in _check(monkeypatch, docs).errors if "ss_low_m40" in e]
    n_all = sum(s.test == TEST and s.corners == "all" for s in blocks()[BLOCK].specs)
    assert len(errs) == n_all and all("CLK-10" not in e for e in errs)


def test_an_all_corner_metric_failing_at_one_corner(monkeypatch, clk10_limit):
    docs = [_doc("tt_nom_27"), _doc("ss_low_125", td_s_ps=95.0), _doc("ff_high_125", iavg_uA=569.0)]
    r = _summary("CLK-01", docs)
    assert r.status == "fail" and r.worst == pytest.approx(95.0) and (r.covered, r.need) == (3, 45)
    assert r.na == []
    assert _summary("CLK-10", docs).status == "pass"
    w = _warnings(monkeypatch, docs)
    assert len(w) == 1 and "CLK-01" in w[0] and "ss_low_125" in w[0]


def test_non_applicable_raw_data_stay_in_the_result(capsys, clk10_limit):
    b = blocks()[BLOCK]
    job = runner.Job("ff_high_125", by_name("ff_high_125"), {}, {})
    m = {**GOOD, "iavg_uA": 569.2671382}
    doc = runner.result_doc(b, TEST, "xtor", job, m, {"mc": None})
    assert doc["metrics"]["iavg_uA"] == pytest.approx(569.2671382)
    assert "CLK-10" not in doc["specs"]
    assert doc["specs_na"] == {"CLK-10": {"metric": "iavg_uA", "value": 569.2671382, "limit": "<= 80",
                                          "corners": "typ"}}
    runner._print_summary(b, TEST, [{"job": "ff_high_125", "corner": "ff_high_125", "metrics": m}])
    out = capsys.readouterr().out
    assert "CLK-10=569.3(n/a: typ only)" in out and "FAIL" not in out
    tt = runner.result_doc(b, TEST, "xtor", runner.Job("tt_nom_27", by_name("tt_nom_27"), {}, {}), m, {})
    assert tt["specs"]["CLK-10"]["pass"] is False and "specs_na" not in tt


def test_one_test_mixing_all_and_typ_specs(clk10_limit):
    b = blocks()[BLOCK]
    judged, na = b.verdicts(TEST, "ff_high_125", None, {**GOOD, "iavg_uA": 569.0})
    all_ids = sorted(s.id for s in b.specs if s.test == TEST and s.corners == "all")
    assert sorted(judged) == all_ids and all(v["pass"] for v in judged.values())
    assert list(na) == ["CLK-10"]
    judged, na = b.verdicts(TEST, "tt_nom_27", None, {**GOOD, "iavg_uA": 569.0})
    assert sorted(judged) == sorted(all_ids + ["CLK-10"]) and na == {}
    assert not judged["CLK-10"]["pass"]


def test_errors_and_stale_results_are_never_filtered(monkeypatch, capsys, clk10_limit):
    """An error or a stale input at a corner where some spec does not apply is still reported."""
    err = _doc("ff_high_125")
    err["metrics"] = {"iavg_uA": 569.0, "error": "spectre rc=1"}
    stale = _doc("ss_low_m40")
    stale["meta"]["files"] = {"specs/arch.yaml": "0000000000000000"}
    docs = [_doc("tt_nom_27"), err, stale]
    w = _warnings(monkeypatch, docs)
    assert any("ff_high_125.json: simulation/measurement error" in x for x in w)
    assert any("ss_low_m40.json: stale" in x for x in w)
    assert _summary("CLK-01", docs).status == "fail"            # the error corner has no metrics
    assert _summary("CLK-10", docs).status == "pass"
    monkeypatch.setattr(results, "load_results", lambda: docs)
    results.report(BLOCK)
    out = capsys.readouterr().out
    assert "error  tb_clkgen_timing/ff_high_125: spectre rc=1" in out
    assert "stale  tb_clkgen_timing/ss_low_m40: specs/arch.yaml" in out


def _stale_review_docs() -> list[dict]:
    """Every result the selected candidate of an xtor-review block needs, one of them stale."""
    b = blocks()[BLOCK]
    view = f"xtor-{b.selected}"
    docs = [_doc(c, test=t, view=view) for t in {s.test for s in b.specs}
            for c in sorted(corner_names("all"))]
    stale = next(d for d in docs if d["corner"] == "ff_high_125" and d["test"] == TEST)
    stale["meta"]["files"] = {"specs/arch.yaml": "0000000000000000"}
    return docs


def _review_check(monkeypatch, docs, changed: bool) -> checks.Report:
    monkeypatch.setattr(checks, "load_results", lambda: docs)
    monkeypatch.setattr(checks, "_check_figures", lambda *a, **k: None)
    monkeypatch.setattr(checks, "_selection_changed", lambda b, base: changed and b.name == BLOCK)
    return checks.check_results(strict=True, base="base")


def _stale_errors(rep: checks.Report) -> list[str]:
    return [e for e in rep.errors if e.startswith(BLOCK) and "result is stale" in e]


def test_strict_stale_review_results_only_warn(monkeypatch):
    rep = _review_check(monkeypatch, _stale_review_docs(), changed=False)
    assert _stale_errors(rep) == []
    assert f"{BLOCK}: selected candidate {blocks()[BLOCK].selected} has 1 stale results, not eligible" in rep.warnings


def test_strict_stale_review_results_fail_a_pr_that_changes_the_selection(monkeypatch):
    rep = _review_check(monkeypatch, _stale_review_docs(), changed=True)
    assert _stale_errors(rep)
    assert not any("not eligible" in w for w in rep.warnings)


def test_strict_stale_signoff_results_still_fail(monkeypatch):
    monkeypatch.setitem(blocks()[BLOCK].raw, "status", "signoff")
    assert _stale_errors(_review_check(monkeypatch, _stale_review_docs(), changed=False))


def test_strict_missing_and_failing_review_results_stay_errors(monkeypatch):
    docs = _stale_review_docs()
    docs.remove(next(d for d in docs if d["corner"] == "ss_low_m40" and d["test"] == TEST))
    bad = next(d for d in docs if d["corner"] == "tt_nom_27" and d["test"] == TEST)
    bad["metrics"]["td_s_ps"] = 1e4
    errs = _review_check(monkeypatch, docs, changed=False).errors
    assert any("no xtor-" in e and "ss_low_m40" in e for e in errs)
    assert any("tt_nom_27: fails" in e for e in errs)


@pytest.fixture
def base_repo(_isolated_root):
    """A git repository whose HEAD holds adc_clkgen with the given fields."""
    b = blocks()[BLOCK]
    (_isolated_root / "specs" / "blocks").mkdir(parents=True)

    def commit(**over):
        raw = {"block": BLOCK, "selected": b.selected, "status": b.status, **over}
        (_isolated_root / "specs" / "blocks" / b.path.name).write_text(yaml.safe_dump(raw), encoding="utf-8")
        for args in (["init", "-q"], ["add", "-A"],
                     ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "x", "--allow-empty"]):
            subprocess.run(["git", *args], cwd=_isolated_root, check=True)

    return b, commit


def test_selection_changed_compares_selected_and_status(base_repo):
    b, commit = base_repo
    assert checks._selection_changed(b, None) is False
    commit()
    assert checks._selection_changed(b, "HEAD") is False
    commit(status="behavioral")
    assert checks._selection_changed(b, "HEAD") is True
    commit(selected="none")
    assert checks._selection_changed(b, "HEAD") is True
    assert checks._selection_changed(b, "no-such-ref") is True


def test_report_counts_unique_applicable_corners(monkeypatch, capsys, clk10_limit):
    docs = [_doc("tt_nom_27", iavg_uA=79.3), _doc("tt_nom_27", job="tt_nom_27__v2", iavg_uA=79.4),
            _doc("ff_high_125", iavg_uA=569.3)]
    assert _summary("CLK-10", docs).covered == 1
    monkeypatch.setattr(results, "load_results", lambda: docs)
    results.report(BLOCK)
    line = next(ln for ln in capsys.readouterr().out.splitlines() if ln.strip().startswith("CLK-10"))
    assert "79.4" in line and "PASS" in line and "1/1" in line
    assert "n/a at 1 corner(s) outside typ, worst 569.3: not judged" in line


def _figures_next_to(docs: list[dict]) -> list:
    """Evidence figures that a design branch has next to its results (#26): one unlisted
    <corner>.timing.png per record, in the records' own directory."""
    out = []
    for d in docs:
        png = d["_path"].with_name(d["_path"].stem + ".timing.png")
        png.parent.mkdir(parents=True, exist_ok=True)
        png.write_bytes(b"\x89PNG\r\n")
        out.append(png)
    return out


def test_verdicts_do_not_depend_on_figures_next_to_the_results(monkeypatch, _isolated_root):
    """#41: with figures next to the results the verdict warnings are the same."""
    docs = [_doc("tt_nom_27"), _doc("ss_low_125", td_s_ps=95.0), _doc("ff_high_125", iavg_uA=569.0)]
    assert all(_isolated_root in d["_path"].parents for d in docs)            # never the real results/
    _figures_next_to(docs)
    w = _warnings(monkeypatch, docs)
    assert len(w) == 1 and "CLK-01" in w[0] and "ss_low_125" in w[0]


def test_unlisted_figures_are_still_reported_by_the_production_check(monkeypatch):
    """The isolation is only in the verdict tests: check_results itself still reports every
    PNG of a result that its `figures` do not list."""
    docs = [_doc("tt_nom_27"), _doc("ss_low_125"), _doc("ff_high_125")]
    pngs = _figures_next_to(docs)
    rep = _check(monkeypatch, docs, figures=True)
    assert sorted(w for w in rep.warnings if "is not listed in figures" in w) == \
        sorted(f"results/{BLOCK}/{TEST}/xtor/{p.stem.split('.')[0]}.json: {p.name} is not listed in figures"
               for p in pngs)


# ------------------------------------------------------------------ CLK-10 reported only (#75)
def test_reported_only_spec_has_no_verdict_at_its_corners():
    """CLK-10 (adc_clkgen 0.6.0): judged nowhere, a value at TT (pass None, limit "reported"), N/A elsewhere."""
    b, s = blocks()[BLOCK], _spec("CLK-10")
    assert s.reported and s.max is None and s.min is None and s.limit_text() == "reported"
    assert s.judge({"iavg_uA": 1e6}) is None and s.judge({}) is None
    judged, na = b.verdicts(TEST, "tt_nom_27", None, {**GOOD, "iavg_uA": 569.0})
    assert judged["CLK-10"] == {"metric": "iavg_uA", "value": 569.0, "limit": "reported", "pass": None}
    assert all(v["pass"] for k, v in judged.items() if k != "CLK-10")
    judged, na = b.verdicts(TEST, "ff_high_125", None, {**GOOD, "iavg_uA": 569.0})
    assert "CLK-10" not in judged and na["CLK-10"]["limit"] == "reported"


def test_reported_only_spec_is_reported_never_failed(monkeypatch, capsys):
    tt, ff = _doc("tt_nom_27", iavg_uA=569.0), _doc("ff_high_125", iavg_uA=900.0)
    r = _summary("CLK-10", [tt, ff])
    assert r.status == "reported" and r.worst == pytest.approx(569.0) and (r.covered, r.need) == (1, 1)
    assert not any("CLK-10" in w for w in _warnings(monkeypatch, [tt, ff]))
    monkeypatch.setattr(results, "load_results", lambda: [tt, ff])
    results.report(BLOCK)
    line = next(ln for ln in capsys.readouterr().out.splitlines() if ln.strip().startswith("CLK-10"))
    assert "reported" in line and "569" in line and "INFO" in line and "1/1" in line
    assert "PASS" not in line and "FAIL" not in line
    runner._print_summary(blocks()[BLOCK], TEST, [{"job": "tt_nom_27", "corner": "tt_nom_27", "metrics": tt["metrics"]}])
    out = capsys.readouterr().out
    assert "CLK-10=569(reported)" in out and "FAIL" not in out


def test_signoff_needs_the_reported_value_but_no_verdict(monkeypatch):
    monkeypatch.setitem(blocks()[BLOCK].raw, "selected", "none")      # these docs are the legacy plain xtor view
    monkeypatch.setitem(blocks()[BLOCK].raw, "status", "signoff")
    docs = [_doc(c, iavg_uA=900.0 if c == "tt_nom_27" else 70.0) for c in sorted(corner_names("all"))]
    assert [e for e in _check(monkeypatch, docs).errors if "CLK-09" not in e] == []     # any value, no limit
    tt = next(d for d in docs if d["corner"] == "tt_nom_27")
    del tt["metrics"]["iavg_uA"]
    errs = [e for e in _check(monkeypatch, docs).errors if "CLK-10" in e]
    assert errs == ["adc_clkgen CLK-10 tt_nom_27: reported metric iavg_uA not measured"]


def test_reported_only_spec_takes_no_limit(tmp_path):
    import yaml

    from adcflow.specs import SpecError, _load_block

    raw = yaml.safe_load(blocks()[BLOCK].path.read_text(encoding="utf-8"))
    path = tmp_path / f"{BLOCK}.yaml"
    for bad, msg in (({"max": 80}, "has no min, max or mc"), ({"reported": "yes"}, "reported must be true or false"),
                     ({"reported": False}, "needs min or max")):
        path.write_text(yaml.safe_dump(dict(raw, specs=[dict(s, **bad) if s["id"] == "CLK-10" else s
                                                        for s in raw["specs"]])), encoding="utf-8")
        with pytest.raises(SpecError, match=msg):
            _load_block(path)
