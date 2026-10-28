"""A spec judges only the corners of its corner set (issue #29).

tb_clkgen_timing mixes `corners: all` specs (CLK-01 .. CLK-08) with CLK-10 (`corners: typ`):
a result at ff_high_125 is judged on CLK-01 .. CLK-08, while its AVDD current stays in the
result as a raw value that CLK-10 does not judge (N/A).
"""

import pytest

from adcflow import REPO_ROOT, checks, results, runner
from adcflow.corners import by_name, corner_names
from adcflow.specs import blocks

BLOCK = "adc_clkgen"
TEST = "tb_clkgen_timing"
GOOD = {"td_s_ps": 46.0, "skew_sb_ps": 40.0, "nov_bc_ps": 20.0, "td_conv_ps": 110.0, "nov_cb_ps": 20.0,
        "tf_s_ps": 10.0, "skew_ssb_ps": 2.0, "duty_errors": 0, "iavg_uA": 70.0, "soa_violations": 0}


def _doc(corner: str, test: str = TEST, view: str = "xtor", mc=None, job: str | None = None, **metrics) -> dict:
    job = job or corner
    return {"block": BLOCK, "test": test, "view": view, "corner": corner, "metrics": {**GOOD, **metrics},
            "meta": {"mc": mc, "files": {}},
            "_path": REPO_ROOT / "results" / BLOCK / test / view / f"{job}.json"}


def _spec(sid: str):
    return next(s for s in blocks()[BLOCK].specs if s.id == sid)


def _summary(sid: str, docs: list[dict]) -> results.SpecSummary:
    return results.summarize(_spec(sid), [(d, checks.judge(d)) for d in docs])


def _warnings(monkeypatch, docs: list[dict]) -> list[str]:
    monkeypatch.setattr(checks, "load_results", lambda: docs)
    rep = checks.check_results()
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
    cmp03 = next(s for s in blocks()["adc_comp"].specs if s.id == "CMP-03")
    assert cmp03.mc and cmp03.corners == "typ"
    assert not cmp03.applies("tt_nom_27") and cmp03.applies("tt_nom_27", "local_tt")
    assert not cmp03.applies("ff_high_125", "local_tt")
    assert _spec("CLK-10").applies("tt_nom_27", "global_local")
    judged, na = blocks()["adc_comp"].verdicts("tb_comp_noise", "tt_nom_27", None, {"offset_sigma_mV": 3.0})
    assert "CMP-03" not in judged and "CMP-03" not in na       # nominal run: left out, as before


def test_tt_passes_while_another_corner_exceeds_the_tt_limit(monkeypatch):
    tt, ff = _doc("tt_nom_27", iavg_uA=79.34202385), _doc("ff_high_125", iavg_uA=569.2671382)
    j = checks.judge(ff)
    assert "CLK-10" not in j["specs"] and j["na"]["CLK-10"]["value"] == pytest.approx(569.2671382)
    assert all(j["specs"][f"CLK-0{i}"]["pass"] for i in range(1, 9))
    r = _summary("CLK-10", [tt, ff])
    assert r.status == "pass" and r.worst == pytest.approx(79.34202385)
    assert (r.covered, r.need) == (1, 1)
    assert r.na == [("ff_high_125", pytest.approx(569.2671382))]
    assert not any("CLK-10" in w for w in _warnings(monkeypatch, [tt, ff]))


def test_tt_really_fails(monkeypatch):
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
    monkeypatch.setitem(blocks()[BLOCK].raw, "status", "signoff")
    monkeypatch.setattr(checks, "load_results", lambda: [_doc(c.name) for c in [by_name("ff_high_125")]])
    errs = [e for e in checks.check_results().errors if "CLK-10" in e]
    assert errs == ["adc_clkgen CLK-10: no xtor result for corner tt_nom_27 (tb_clkgen_timing)"]


def test_signoff_needs_every_applicable_corner_and_ignores_the_others(monkeypatch):
    docs = [_doc(c) for c in sorted(corner_names("all"))]
    docs = [d if d["corner"] != "ff_high_125" else _doc("ff_high_125", iavg_uA=569.0) for d in docs]
    monkeypatch.setitem(blocks()[BLOCK].raw, "status", "signoff")
    monkeypatch.setattr(checks, "load_results", lambda: docs)
    assert [e for e in checks.check_results().errors if "CLK-09" not in e] == []     # CLK-09: jitter test
    docs.remove(next(d for d in docs if d["corner"] == "ss_low_m40"))
    errs = [e for e in checks.check_results().errors if "ss_low_m40" in e]
    n_all = sum(s.test == TEST and s.corners == "all" for s in blocks()[BLOCK].specs)
    assert len(errs) == n_all and all("CLK-10" not in e for e in errs)


def test_an_all_corner_metric_failing_at_one_corner(monkeypatch):
    docs = [_doc("tt_nom_27"), _doc("ss_low_125", td_s_ps=95.0), _doc("ff_high_125", iavg_uA=569.0)]
    r = _summary("CLK-01", docs)
    assert r.status == "fail" and r.worst == pytest.approx(95.0) and (r.covered, r.need) == (3, 45)
    assert r.na == []
    assert _summary("CLK-10", docs).status == "pass"
    w = _warnings(monkeypatch, docs)
    assert len(w) == 1 and "CLK-01" in w[0] and "ss_low_125" in w[0]


def test_non_applicable_raw_data_stay_in_the_result(capsys):
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


def test_one_test_mixing_all_and_typ_specs():
    b = blocks()[BLOCK]
    judged, na = b.verdicts(TEST, "ff_high_125", None, {**GOOD, "iavg_uA": 569.0})
    all_ids = sorted(s.id for s in b.specs if s.test == TEST and s.corners == "all")
    assert sorted(judged) == all_ids and all(v["pass"] for v in judged.values())
    assert list(na) == ["CLK-10"]
    judged, na = b.verdicts(TEST, "tt_nom_27", None, {**GOOD, "iavg_uA": 569.0})
    assert sorted(judged) == sorted(all_ids + ["CLK-10"]) and na == {}
    assert not judged["CLK-10"]["pass"]


def test_errors_and_stale_results_are_never_filtered(monkeypatch, capsys):
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


def test_report_counts_unique_applicable_corners(monkeypatch, capsys):
    docs = [_doc("tt_nom_27", iavg_uA=79.3), _doc("tt_nom_27", job="tt_nom_27__v2", iavg_uA=79.4),
            _doc("ff_high_125", iavg_uA=569.3)]
    assert _summary("CLK-10", docs).covered == 1
    monkeypatch.setattr(results, "load_results", lambda: docs)
    results.report(BLOCK)
    line = next(ln for ln in capsys.readouterr().out.splitlines() if ln.strip().startswith("CLK-10"))
    assert "79.4" in line and "PASS" in line and "1/1" in line
    assert "n/a at 1 corner(s) outside typ, worst 569.3: not judged" in line
