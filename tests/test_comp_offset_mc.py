"""CMP-03: comparator offset under device mismatch (issue #63, tb_comp_offset_mc).

One Spectre montecarlo analysis appends the search of every sample to offset.txt
(tb_offset_search_va); measure.comp reads the samples in iteration order, counts failed and
missing ones and takes the sample standard deviation (n - 1) of the valid offsets. A Monte Carlo
spec passes only with every sample valid (Spec.judge), on Monte Carlo runs only (Spec.applies).
"""

import json
import sys
from pathlib import Path

import numpy as np
import pytest

from adcflow import candidates as cand
from adcflow import checks, corners, figures, runner, site
from adcflow.corners import by_name, corner_set
from adcflow.measure import comp
from adcflow.specs import _mc_problems, blocks

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "site"))
from sitegen import cands as site_cands                               # noqa: E402

TEST = "tb_comp_offset_mc"
MC = {"runs": 50, "seed": 6303, "firstrun": 1, "variations": "mismatch", "models": "local_tt"}


def _sample(offset_v: float | None, status: int | None = 0, cycles: int = 17) -> str:
    """One sample block as tb_offset_search_va writes it (status None: no R line, the transient aborted)."""
    lines = ["B 13 2.500000000e-02 5.000000000e-05 4.900000000e-01"]
    lines += [f"D {k} {1e-3 * k:.9e} {k % 2}" for k in range(1, cycles + 1)]
    if status is not None:
        o = offset_v or 0.0
        lines.append(f"R {status} {o:.9e} {o - 3e-6:.9e} {o + 3e-6:.9e} {cycles}")
    return "\n".join(lines) + "\n"


def _cmp03():
    return next(s for s in blocks()["adc_comp"].specs if s.id == "CMP-03")


# ------------------------------------------------------------------ reading and aggregation
def test_samples_in_iteration_order_with_failed_and_missing(tmp_path):
    f = tmp_path / "offset.txt"
    f.write_text(_sample(1.5e-3) + _sample(-0.5e-3) + _sample(None, 1, 1) + _sample(2e-4, 3)
                 + _sample(None, None, 9) + _sample(None, 2, 4))
    s = comp.read_offset_samples(f, runs=8)
    assert [x["run"] for x in s] == list(range(1, 9))
    assert [x["status"] for x in s] == ["ok", "ok", "out of range", "re-check failed", comp.MC_ABORTED,
                                       "no valid decision", comp.MC_MISSING, comp.MC_MISSING]
    assert s[0]["offset"] == pytest.approx(1.5e-3) and s[3]["offset"] is None      # a failed search has no offset
    assert len(s[4]["search"]) == 9 and s[6]["search"] == []
    m = comp.offset_stats(s)
    assert (m["mc_runs"], m["mc_ok"], m["mc_failed"]) == (8, 2, 6)
    assert m["mc_fail_reasons"] == {"out of range": 1, "re-check failed": 1, comp.MC_ABORTED: 1,
                                    "no valid decision": 1, comp.MC_MISSING: 2}
    assert m["offsets_mV"] == [1.5, -0.5, None, None, None, None, None, None]
    assert m["sample_status"][6:] == [comp.MC_MISSING] * 2


def test_firstrun_numbers_the_samples(tmp_path):
    f = tmp_path / "offset.txt"
    f.write_text(_sample(1e-3) + _sample(2e-3))
    assert [x["run"] for x in comp.read_offset_samples(f, runs=3, firstrun=11)] == [11, 12, 13]


def test_sigma_is_the_sample_standard_deviation():
    offs = [1e-3, 2e-3, 3e-3, 4e-3]
    m = comp.offset_stats([{"run": i + 1, "status": "ok", "offset": o, "search": []} for i, o in enumerate(offs)])
    assert m["offset_sigma_mV"] == pytest.approx(np.std([1, 2, 3, 4], ddof=1))       # 1.291, n - 1
    assert m["offset_sigma_mV"] != pytest.approx(np.std([1, 2, 3, 4]))                 # not the n form (1.118)
    assert m["offset_mean_mV"] == pytest.approx(2.5) and m["offset_max_abs_mV"] == pytest.approx(4.0)
    assert "mc_fail_reasons" not in m


def test_sigma_ignores_failed_samples_but_counts_them():
    s = [{"run": 1, "status": "ok", "offset": 1e-3, "search": []},
         {"run": 2, "status": "ok", "offset": 3e-3, "search": []},
         {"run": 3, "status": "out of range", "offset": None, "search": []}]
    m = comp.offset_stats(s)
    assert m["offset_sigma_mV"] == pytest.approx(np.std([1, 3], ddof=1))
    assert m["mc_failed"] == 1


def test_fewer_than_two_valid_samples_give_no_sigma():
    m = comp.offset_stats([{"run": 1, "status": "ok", "offset": 1e-3, "search": []},
                           {"run": 2, "status": comp.MC_MISSING, "offset": None, "search": []}])
    assert "offset_sigma_mV" not in m and m["mc_ok"] == 1


def test_no_file_means_every_sample_missing(tmp_path):
    s = comp.read_offset_samples(tmp_path / "offset.txt", runs=50)
    assert len(s) == 50 and {x["status"] for x in s} == {comp.MC_MISSING}
    assert comp.offset_stats(s)["mc_failed"] == 50


@pytest.mark.parametrize("text, msg", [
    (_sample(1e-3) * 3, "3 samples for 2"),
    ("D 1 2.5e-02 1\n" + _sample(1e-3), "before the first sample"),
])
def test_foreign_or_broken_files_are_errors(tmp_path, text, msg):
    f = tmp_path / "offset.txt"
    f.write_text(text)
    with pytest.raises(ValueError, match=msg):
        comp.read_offset_samples(f, runs=2)


def test_measure_end_to_end_with_figure(tmp_path):
    rng = np.random.default_rng(1)
    offs = rng.normal(0, 2e-3, 50)
    (tmp_path / "offset.txt").write_text("".join(_sample(o) for o in offs[:49]) + _sample(None, 1, 1))
    sink = figures.FigureSink(tmp_path / "figs", "tt_nom_27", header="t")
    ctx = {"corner": by_name("tt_nom_27"), "params": {}, "globals": {"vdd": 0.9}, "test": TEST,
           "block": "adc_comp", "view": "behav", "figs": sink, "mc": MC}
    m = comp.offset_mc(tmp_path, ctx)
    assert (m["mc_ok"], m["mc_failed"]) == (49, 1)
    assert m["offset_sigma_mV"] == pytest.approx(np.std(offs[:49] * 1e3, ddof=1), rel=1e-5)
    assert [e["file"] for e in sink.entries] == ["tt_nom_27.offset_mc.png"]
    assert ctx["provenance"]["offset_search"]["bits"] == comp.MC_BITS
    judged, _ = blocks()["adc_comp"].verdicts(TEST, "tt_nom_27", MC, m)
    assert judged["CMP-03"]["pass"] is False                                  # one failed sample: CMP-03 fails
    assert judged["CMP-03"]["samples"] == {"ok": 49, "failed": 1, "need": 50}


def test_search_resolution_and_range():
    assert 2 * comp.MC_RANGE / 2 ** comp.MC_BITS == pytest.approx(6.1e-6, rel=0.01)    # about 10 uV or better
    assert comp.MC_RANGE >= 5 * _cmp03().max * 1e-3                                       # +/-5 sigma at the limit


# ------------------------------------------------------------------ verdicts and applicability
@pytest.mark.parametrize("metrics, ok", [
    ({"offset_sigma_mV": 3.0, "mc_ok": 50, "mc_failed": 0}, True),
    ({"offset_sigma_mV": 3.0, "mc_ok": 49, "mc_failed": 1}, False),       # a failed or missing sample
    ({"offset_sigma_mV": 3.0, "mc_ok": 10, "mc_failed": 0}, False),       # --mc-runs 10: too few samples
    ({"offset_sigma_mV": 5.5, "mc_ok": 50, "mc_failed": 0}, False),       # over the limit
    ({"offset_sigma_mV": 3.0}, False),                                    # no sample counts: not judged a pass
    ({"mc_ok": 50, "mc_failed": 0}, False),                               # no sigma
    ({"offset_sigma_mV": 3.0, "mc_ok": 60, "mc_failed": 0}, True),        # more samples than required
])
def test_monte_carlo_spec_needs_every_sample(metrics, ok):
    judged, na = blocks()["adc_comp"].verdicts(TEST, "tt_nom_27", MC, metrics)
    assert judged["CMP-03"]["pass"] is ok and na == {}
    assert judged["CMP-03"]["samples"]["need"] == 50


def test_cmp03_is_judged_by_the_monte_carlo_test_only():
    s = _cmp03()
    assert s.test == TEST and s.mc == 50 and s.corners == "typ"
    assert blocks()["adc_comp"].tests[TEST]["montecarlo"] == {"runs": 50, "seed": 6303, "variations": "mismatch",
                                                              "models": "local_tt"}
    assert s.applies("tt_nom_27", MC) and not s.applies("tt_nom_27", None) and not s.applies("ff_high_125", MC)
    b = blocks()["adc_comp"]
    judged, na = b.verdicts(TEST, "tt_nom_27", None, {"offset_sigma_mV": 1.0, "mc_ok": 50, "mc_failed": 0})
    assert judged == {} and na == {}                                     # a nominal run of it: left out
    judged, na = b.verdicts("tb_comp_noise", "tt_nom_27", MC, {"noise_uV": 150.0, "offset_abs_mV": 0.1})
    assert set(judged) == {"CMP-01", "CMP-13", "CMP-02"}                  # tb_comp_noise keeps CMP-01/02/13


def test_judge_and_report_on_recorded_mc_result(tmp_path, monkeypatch, capsys):
    from adcflow import results
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    doc = {"block": "adc_comp", "test": TEST, "view": "behav", "corner": "tt_nom_27",
           "metrics": {"offset_sigma_mV": 2.0, "mc_ok": 48, "mc_failed": 2}, "meta": {"mc": MC, "files": {}},
           "_path": tmp_path / "x.json"}
    j = checks.judge(doc)
    assert j["specs"]["CMP-03"]["pass"] is False
    r = results.summarize(_cmp03(), [(doc, j)])
    assert r.status == "fail" and r.covered == 1 and r.samples == [{"ok": 48, "failed": 2, "need": 50}]
    nominal = {**doc, "meta": {"mc": None, "files": {}}}
    assert results.summarize(_cmp03(), [(nominal, checks.judge(nominal))]).status == "none"


@pytest.mark.parametrize("mc, msg", [
    ({"runs": 50, "seed": 1, "variations": "mismatch"}, "needs exactly"),
    ({"runs": 1, "seed": 1, "variations": "mismatch", "models": "local_tt"}, "runs"),
    ({"runs": 50, "seed": -1, "variations": "mismatch", "models": "local_tt"}, "seed"),
    ({"runs": 50, "seed": 1, "variations": "local", "models": "local_tt"}, "variations"),
    ({"runs": 50, "seed": 1, "variations": "mismatch", "models": "/x/y"}, "models"),
])
def test_montecarlo_settings_are_validated(mc, msg):
    assert any(msg in e for e in _mc_problems(mc, "t"))
    assert _mc_problems({"runs": 50, "seed": 1, "variations": "mismatch", "models": "local_tt"}, "t") == []


def test_spec_with_mc_needs_enough_runs(tmp_path):
    from adcflow.specs import SpecError, _load_block
    raw = (blocks()["adc_comp"].path.read_text(encoding="utf-8")
           .replace("montecarlo: {runs: 50,", "montecarlo: {runs: 20,"))
    p = tmp_path / "adc_comp.yaml"
    p.write_text(raw, encoding="utf-8")
    with pytest.raises(SpecError, match="mc: 50 needs a test with `montecarlo:` of at least 50 runs"):
        _load_block(p)


# ------------------------------------------------------------------ runner, models, testbench
def test_mc_settings_from_the_spec_and_overrides():
    b, t = blocks()["adc_comp"], blocks()["adc_comp"].tests[TEST]
    typ = corner_set("typ")
    assert runner.mc_settings(b, TEST, t, typ) == MC
    assert runner.mc_settings(b, TEST, t, typ, {"runs": 5, "seed": None})["runs"] == 5
    assert runner.mc_settings(b, TEST, t, typ, None, {"mc_seed": "7"})["seed"] == 7
    with pytest.raises(ValueError, match="Monte Carlo test for the corners of CMP-03"):
        runner.mc_settings(b, TEST, t, corner_set("ss_low_m40"))
    assert runner.mc_settings(b, "tb_comp_noise", b.tests["tb_comp_noise"], typ) is None
    with pytest.raises(ValueError, match="not a Monte Carlo test"):
        runner.mc_settings(b, "tb_comp_noise", b.tests["tb_comp_noise"], typ, {"runs": 5})


def test_dry_run_passes_samples_and_seed_to_the_testbench(monkeypatch):
    staged, models = {}, []
    monkeypatch.setattr(runner, "stage", lambda run_dir, jobs, decks: staged.update(jobs=jobs, decks=decks))
    make_deck = runner.make_deck
    monkeypatch.setattr(runner, "make_deck", lambda j, r, v, pdk, mc, extra: models.append(mc) or make_deck(j, r, v, pdk, mc, extra))
    runner.run_test(TEST, dry=True, mc={"runs": 7, "seed": 11}, mode="aps")
    assert models == [None]                                              # behavioral: no statistical model sections
    (job,) = staged["jobs"]
    tb, deck = job.tb_text, staged["decks"][job.name]
    assert job.params["mc_runs"] == 7 and job.params["mc_seed"] == 11
    assert "mc_runs=7 mc_seed=11" in tb
    assert "mc1 montecarlo numruns=mc_runs seed=mc_seed firstrun=1 donominal=no variations=mismatch" in tb
    assert " comp_behav=1" in deck and "include" not in deck.split("ahdl_include")[0]   # behavioral: no PDK


def test_comp_behav_follows_the_comparator_view():
    b, t = blocks()["adc_comp"], blocks()["adc_comp"].tests[TEST]
    (j,) = runner.build_jobs(b, TEST, t, corner_set("typ"), {}, {})
    assert j.globals_["comp_behav"] == 1
    (j,) = runner.build_jobs(b, TEST, t, corner_set("typ"), {"adc_ref": "xtor:x"}, {}, needs_pdk=True)
    assert j.globals_["comp_behav"] == 1                                 # another block's view does not matter
    (j,) = runner.build_jobs(b, TEST, t, corner_set("typ"), {"adc_comp": "xtor:x"}, {}, needs_pdk=True)
    assert j.globals_["comp_behav"] == 0


def test_statistical_sections_come_from_the_corner_file(monkeypatch):
    cfg = {"_path": "site.local.yaml", "pdk": {"model_dir": "M", "core_file": "c.lib", "hv_file": "h.lib"}}
    monkeypatch.setattr(site, "site", lambda: cfg)
    secs = corners._cfg()["pdk"]["mc_sections"]["local_tt"]
    lines = corners.model_includes(by_name("tt_nom_27"), mc="local_tt").splitlines()
    assert lines == [f'include "M/c.lib" section={secs["mos"]}', f'include "M/c.lib" section={secs["res"]}',
                     f'include "M/c.lib" section={secs["mom"]}', f'include "M/h.lib" section={secs["mos"]}']
    with pytest.raises(KeyError, match="pdk.mc_sections.local_ff needs mos, res and mom"):
        corners.model_includes(by_name("tt_nom_27"), mc="local_ff")


def test_generated_testbench():
    tb = (blocks()["adc_comp"].path.parents[2] / "tb" / "comp" / f"{TEST}.scs").read_text(encoding="utf-8")
    assert "mc_runs=50 mc_seed=6303" in tb and "nbits=13" in tb and "vrange=0.025" in tb
    assert "variations=mismatch" in tb and "donominal=no" in tb
    assert "ISRCH (INPS INN CLKC OUTP OUTN 0) tb_offset_search_va" in tb
    assert "XVOS (INP INPS) tb_mm_vos" in tb and "V0 (P N) vsource dc=comp_behav*vos_beh*mm_beh" in tb
    assert "noisefmax" not in tb                                         # transient noise off


# ------------------------------------------------------------------ figures and leaderboard
def test_figure_spec_rows_judge_the_monte_carlo_spec():
    ctx = {"block": "adc_comp", "test": TEST, "corner": by_name("tt_nom_27"), "mc": MC}
    rows = figures.spec_rows(ctx, {"offset_sigma_mV": 2.0, "mc_ok": 49, "mc_failed": 1}, ["offset_sigma_mV"])
    assert rows == [("CMP-03  offset_sigma_mV", "2 mV", "<= 5", False)]
    assert figures.limits(ctx, "offset_sigma_mV") == (None, 5)
    assert figures.limits({**ctx, "mc": None}, "offset_sigma_mV") == (None, None)


def _mc_doc(root, ok, failed, name="alice"):
    d = root / "results" / "adc_comp" / TEST / f"xtor-{name}"
    d.mkdir(parents=True, exist_ok=True)
    doc = {"block": "adc_comp", "test": TEST, "view": f"xtor-{name}", "corner": "tt_nom_27",
           "metrics": {"offset_sigma_mV": 2.0, "mc_ok": ok, "mc_failed": failed},
           "globals": {"vdd": 0.9}, "meta": {"files": {}, "mc": MC}}
    (d / "tt_nom_27.json").write_text(json.dumps(doc))


@pytest.mark.parametrize("ok, failed, text, kind", [
    (50, 0, "CMP-03 50/50", "pass"),
    (48, 2, "CMP-03 48/50 2 failed", "fail"),
    (None, None, "CMP-03 0/50", "none"),
])
def test_leaderboard_shows_sample_coverage(tmp_path, monkeypatch, ok, failed, text, kind):
    monkeypatch.setattr(cand, "ROOT", tmp_path)
    monkeypatch.setattr(checks, "REPO_ROOT", tmp_path)
    d = tmp_path / "design" / "xtor" / "adc_comp" / "alice"
    d.mkdir(parents=True)
    (d / "candidate.yaml").write_text("name: alice\ndescription: x\nstatus: wip\nauthors: [{github: alice}]\n")
    if ok is not None:
        _mc_doc(tmp_path, ok, failed)
    (row,) = cand.leaderboard("adc_comp")
    assert row["mc"] == [{"spec": "CMP-03", "need": 50, "ok": ok or 0, "failed": failed}]
    assert cand.mc_text(row["mc"]) == text and text in cand.table([row])
    assert [c[0] for c in site_cands.mc_chips(row)] == [kind]

