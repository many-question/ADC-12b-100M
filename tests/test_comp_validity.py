"""CMP-15 output validity of tb_comp_delay (#77): in every evaluate interval, CLKC rise .. CLKC fall, exactly one of
OUTP / OUTN crosses 50 % VDD and the other stays below 30 % VDD; CMP-16 reports the worst losing-output peak.

CMP-09 (the polarity of the first output to rise, |vd| >= 100 uV) is unchanged and judged separately: a cycle without
any decision is CMP-09's (or, below 100 uV, the metastable case of the SAR timeout, LOG-11), never CMP-15's. The
waveforms are synthetic, on a 0.5 ps grid like a saved transient; comp.delay reads them through a stubbed `tran`."""

import json

import numpy as np
import pytest

from adcflow import REPO_ROOT, checks, verify
from adcflow.measure import comp
from adcflow.measure.comp import DELAY_LEVELS, N_DELAY, T0, TCYC
from adcflow.specs import blocks

VDD = 0.9
DT = 0.5e-12
VDS = DELAY_LEVELS * 2
T = np.arange(int(round((T0 + N_DELAY * TCYC) / DT)) + 1) * DT
CTX = {"globals": {"vdd": VDD}, "block": "adc_comp", "test": "tb_comp_delay"}


def _i(t: float) -> int:
    return int(round(t / DT))


def _clock():
    ph = (T - T0) % TCYC
    v = np.clip(ph / 10e-12, 0, 1) - np.clip((ph - 200e-12) / 10e-12, 0, 1)
    return np.where(T < T0, 0.0, v) * VDD


def _ramp(v, t_from: float, level: float, t_to: float, width: float = 10e-12) -> None:
    """v rises to `level` x VDD over `width` from t_from, holds, and falls back to 0 over `width` from t_to."""
    a, b = _i(t_from), _i(t_to)
    n = _i(width)
    v[a:a + n] = np.maximum(v[a:a + n], np.linspace(0, level * VDD, n))
    v[a + n:b] = np.maximum(v[a + n:b], level * VDD)
    v[b:b + n] = np.maximum(v[b:b + n], np.linspace(level * VDD, 0, n))


def ideal(delay: float = 40e-12):
    """A comparator that decides every cycle correctly `delay` after the CLKC rise and resets at the CLKC fall."""
    op, on = np.zeros_like(T), np.zeros_like(T)
    for k, vd in enumerate(VDS):
        tr = T0 + k * TCYC
        _ramp(op if vd > 0 else on, tr + delay, 1.0, tr + 200e-12)
    return op, on


def run(monkeypatch, tmp_path, op, on):
    w = {"time": T, "CLKC": _clock(), "OUTP": op, "OUTN": on}
    monkeypatch.setattr(comp, "tran", lambda job_dir: w)
    return comp.delay(tmp_path, CTX)


def cycle_start(k: int) -> float:
    """Start of the CLKC rise of cycle k (0-based); its 50 % crossing is 5 ps later."""
    return T0 + k * TCYC


def loser(k: int, op, on):
    return on if VDS[k] > 0 else op


def test_an_ideal_comparator_passes(monkeypatch, tmp_path):
    m = run(monkeypatch, tmp_path, *ideal())
    assert m["validity_violations"] == 0 and m["wrong_decisions"] == 0
    assert m["loser_peak_pct"] == pytest.approx(0.0, abs=1e-9)
    v = m["validity"]
    assert v["cycles"] == v["decided"] == N_DELAY and v["violations"] == [] and v["undecided"] == []
    assert v["dt_max_ps"] == pytest.approx(0.5) and len(v["loser_peaks_pct"]) == N_DELAY


def test_a_correct_first_rise_followed_by_the_other_output_is_a_violation(monkeypatch, tmp_path):
    """The case of #77: the right output rises first (CMP-09 is satisfied), the other rises 10 ps later."""
    op, on = ideal()
    k = VDS.index(100e-6)                                   # +100 uV: OUTP wins, OUTN rises too
    _ramp(on, cycle_start(k) + 50e-12, 1.0, cycle_start(k) + 200e-12)
    m = run(monkeypatch, tmp_path, op, on)
    assert m["wrong_decisions"] == 0                        # CMP-09 only looks at the first rise
    assert m["validity_violations"] == 1
    (bad,) = m["validity"]["violations"]
    assert bad == {"cycle": k + 1, "vd_uV": 100.0, "winner": "OUTP", "loser_peak_pct": pytest.approx(100.0),
                   "both_decided": True}
    assert m["loser_peak_pct"] == pytest.approx(100.0)
    assert m["validity"]["worst"]["cycle"] == k + 1 and m["validity"]["worst"]["output"] == "OUTN"


@pytest.mark.parametrize("level, bad", [(0.29, 0), (0.31, 1)])
def test_the_losing_peak_limit_is_30_percent_of_vdd(monkeypatch, tmp_path, level, bad):
    op, on = ideal()
    k = VDS.index(-10e-6)                                   # -10 uV: OUTN wins, OUTP bumps
    _ramp(op, cycle_start(k) + 30e-12, level, cycle_start(k) + 90e-12)
    m = run(monkeypatch, tmp_path, op, on)
    assert m["validity_violations"] == bad and m["wrong_decisions"] == 0
    assert m["loser_peak_pct"] == pytest.approx(level * 100)
    # the plateau starts 39.5 ps after the CLKC rise starts, 34.5 ps after its 50 % crossing
    assert m["validity"]["worst"] == {"cycle": k + 1, "vd_uV": -10.0, "output": "OUTP",
                                      "t_ps": pytest.approx(34.5, abs=0.01)}
    assert (m["validity"]["violations"] != []) == bool(bad)


def test_a_one_sample_glitch_counts(monkeypatch, tmp_path):
    """The peak is taken over every saved point: a glitch only one sample wide (0.5 ps) is not missed."""
    op, on = ideal()
    k = VDS.index(3e-3)
    loser(k, op, on)[_i(cycle_start(k) + 123.5e-12)] = 0.31 * VDD
    m = run(monkeypatch, tmp_path, op, on)
    assert m["validity_violations"] == 1 and m["loser_peak_pct"] == pytest.approx(31.0)
    assert m["validity"]["worst"]["t_ps"] == pytest.approx(123.5 - 5.0, abs=0.01)   # from the CLKC 50 % crossing


def test_only_the_evaluate_interval_counts(monkeypatch, tmp_path):
    """A bump on the losing output after the CLKC fall (reset, CMP-08) or before the CLKC rise is not judged here."""
    op, on = ideal()
    k = VDS.index(30e-3)
    lose = loser(k, op, on)
    lose[_i(cycle_start(k) + 215e-12)] = 0.6 * VDD           # after the CLKC fall (50 % at ~205 ps)
    lose[_i(cycle_start(k) - 50e-12)] = 0.6 * VDD            # before the CLKC rise
    m = run(monkeypatch, tmp_path, op, on)
    assert m["validity_violations"] == 0 and m["loser_peak_pct"] == pytest.approx(0.0, abs=1e-9)


def test_no_decision_below_100_uV_is_not_a_violation(monkeypatch, tmp_path):
    op, on = ideal()
    k = VDS.index(10e-6)                                     # metastable: neither output rises (SAR timeout, LOG-11)
    sl = slice(_i(cycle_start(k)), _i(cycle_start(k) + TCYC))
    op[sl], on[sl] = 0.2 * VDD, 0.2 * VDD                    # both hover below 50 %: no crossing, not judged
    m = run(monkeypatch, tmp_path, op, on)
    assert m["validity_violations"] == 0 and m["wrong_decisions"] == 0
    assert m["validity"]["undecided"] == [{"cycle": k + 1, "vd_uV": 10.0}] and m["validity"]["decided"] == N_DELAY - 1
    assert m["validity"]["loser_peaks_pct"][k] is None
    assert m["loser_peak_pct"] == pytest.approx(0.0, abs=1e-9)  # an undecided cycle has no loser


def test_a_missing_decision_at_100_uV_or_more_is_cmp09_not_cmp15(monkeypatch, tmp_path):
    op, on = ideal()
    k = VDS.index(-1e-3)
    op[_i(cycle_start(k)):_i(cycle_start(k) + TCYC)] = 0.0
    on[_i(cycle_start(k)):_i(cycle_start(k) + TCYC)] = 0.0
    m = run(monkeypatch, tmp_path, op, on)
    assert m["wrong_decisions"] == 1 and m["validity_violations"] == 0
    assert m["validity"]["undecided"] == [{"cycle": k + 1, "vd_uV": -1000.0}]


def test_a_wrong_first_polarity_is_cmp09_and_a_correct_late_one_is_cmp15(monkeypatch, tmp_path):
    """Both outputs rise, the wrong one first: CMP-09 counts the polarity, CMP-15 the second rise."""
    op, on = ideal(delay=60e-12)
    k = VDS.index(100e-3)
    _ramp(on, cycle_start(k) + 30e-12, 1.0, cycle_start(k) + 200e-12)
    m = run(monkeypatch, tmp_path, op, on)
    assert m["wrong_decisions"] == 1 and m["validity_violations"] == 1
    assert m["validity"]["violations"][0]["winner"] == "OUTN"


def test_an_output_still_high_at_the_clkc_rise_decides_there(monkeypatch, tmp_path):
    """An output that did not reset is high from the interval start: the other output's decision makes it a violation."""
    op, on = ideal()
    k = VDS.index(-30e-3)                                    # the previous cycle (+30 mV) left OUTP high
    op[_i(cycle_start(k) - 10e-12):_i(cycle_start(k) + 60e-12)] = VDD
    m = run(monkeypatch, tmp_path, op, on)
    assert m["validity_violations"] == 1
    assert m["validity"]["violations"][0] == {"cycle": k + 1, "vd_uV": -30000.0, "winner": "OUTP",
                                              "loser_peak_pct": pytest.approx(100.0), "both_decided": True}


def test_the_largest_saved_time_step_is_recorded():
    """`_peak` takes every saved point of a non-uniform grid, and the saved spacing around the interval ends."""
    t = np.array([0.0, 1.0, 1.5, 4.0, 4.2, 9.0, 10.0]) * 1e-12
    v = np.array([0.0, 0.1, 0.35, 0.1, 0.0, 0.0, 0.0])
    pk, t_pk, dt = comp._peak(t, v, 1.2e-12, 4.1e-12)
    assert (pk, t_pk) == (0.35, 1.5e-12) and dt == pytest.approx(2.5e-12)
    pk, t_pk, dt = comp._peak(t, v, 1.75e-12, 4.1e-12)      # the peak point is outside: the value at the start
    assert pk == pytest.approx(0.35 - 0.25 / 2.5 * 0.25) and t_pk == 1.75e-12


# ------------------------------------------------------------------ the spec
def test_cmp15_and_cmp16_on_tb_comp_delay():
    b = blocks()["adc_comp"]
    s15, s16, s09 = (next(s for s in b.specs if s.id == i) for i in ("CMP-15", "CMP-16", "CMP-09"))
    assert (s15.metric, s15.max, s15.corners, s15.test) == ("validity_violations", 0, "all", "tb_comp_delay")
    assert (s16.metric, s16.reported, s16.max, s16.corners, s16.test) == ("loser_peak_pct", True, None, "all",
                                                                         "tb_comp_delay")
    assert (s09.metric, s09.max, s09.corners) == ("wrong_decisions", 0, "all")      # unchanged
    assert b.raw["version"] == "0.7.0"
    judged, _ = b.verdicts("tb_comp_delay", "ss_low_125", None, {"validity_violations": 1, "loser_peak_pct": 55.0})
    assert judged["CMP-15"]["pass"] is False and judged["CMP-16"]["pass"] is None
    judged, _ = b.verdicts("tb_comp_delay", "ss_low_125", None, {"validity_violations": 0, "loser_peak_pct": 12.0})
    assert judged["CMP-15"]["pass"] is True


def test_the_behavioral_comparator_passes():
    """Main's recorded behavioral tb_comp_delay: no violation, every cycle decided, a fresh result."""
    path = REPO_ROOT / "results" / "adc_comp" / "tb_comp_delay" / "behav" / "tt_nom_27.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["_path"] = path
    j = checks.judge(doc)
    assert j["stale"] == [] and j["specs"]["CMP-15"]["pass"] is True and j["specs"]["CMP-09"]["pass"] is True
    m = doc["metrics"]
    assert m["validity_violations"] == 0 and m["loser_peak_pct"] < 30
    assert m["validity"]["decided"] == N_DELAY and m["validity"]["dt_max_ps"] > 0


def test_verify_compares_the_count_and_the_peak_not_the_details():
    """The location of the worst peak and the saved time step are details: a rerun may differ there."""
    a = {"validity_violations": 0, "loser_peak_pct": 12.0, "validity": {"dt_max_ps": 0.5, "worst": {"cycle": 3}}}
    b = {"validity_violations": 0, "loser_peak_pct": 12.1, "validity": {"dt_max_ps": 4.0, "worst": {"cycle": 21}}}
    _, problems, skipped = verify.compare_metrics(a, b)
    assert problems == [] and "validity" in skipped
    _, problems, _ = verify.compare_metrics(a, dict(b, validity_violations=1))
    assert any("validity_violations" in p for p in problems)
