"""SFDR estimator (issue #36): adcflow.spectrum against the true values and MATLAB plotspec."""

import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))

from sfdr_cases import MATLAB_PLOTSPEC, cases  # noqa: E402

from adcflow import REPO_ROOT, model, runner, spectrum  # noqa: E402
from adcflow.corners import by_name  # noqa: E402
from adcflow.measure.common import spectrum as measure_spectrum  # noqa: E402
from adcflow.specs import find_test  # noqa: E402

CASES = cases()
FS = 100e6


@pytest.mark.parametrize("name", sorted(CASES))
def test_sfdr_matches_the_injected_spur(name):
    x, true, _ = CASES[name]
    got = spectrum.analyze(x, FS, 1.0)["sfdr_dbc"]
    if np.isinf(true):
        assert got > 250                                   # numerical floor of a clean sine
    elif not np.isnan(true):
        assert got == pytest.approx(true, abs=0.01)


@pytest.mark.parametrize("name", sorted(set(CASES) - {"clean"}))
def test_sfdr_matches_matlab_plotspec(name):
    """Same definition as MATLAB ADCToolbox plotspec (values recorded with tests/matlab/sfdr_plotspec.m).
    `clean` is left out: plotspec's automatic sideBin is 0 on a noise-free spectrum (6.02 dB)."""
    assert spectrum.analyze(CASES[name][0], FS, 1.0)["sfdr_dbc"] == pytest.approx(MATLAB_PLOTSPEC[name], abs=1e-3)


def test_issue36_repro():
    """The pinned adctoolbox still sums the spur window into the signal bins (7.78 dBc); ours: 80."""
    x = CASES["issue36"][0]
    r = spectrum.analyze(x, FS, 2.0)
    assert r["sfdr_dbc_adctoolbox"] == pytest.approx(7.7807885108, abs=1e-6)
    assert r["sfdr_dbc"] == pytest.approx(80.0, abs=1e-6) and r["spur_bin"] == 507
    assert r["sndr_dbc"] == pytest.approx(80.7919572179, abs=1e-6)          # unchanged, from adctoolbox


def test_near_tone_dc_and_nyquist():
    near = spectrum.analyze(CASES["near2"][0], FS, 1.0)
    assert near["spur_bin"] == 303 and near["sfdr_dbc"] == pytest.approx(60.0, abs=0.01)   # found, not hidden
    assert spectrum.analyze(CASES["dc_offset"][0], FS, 1.0)["spur_bin"] == 150             # DC is not a spur
    assert spectrum.analyze(CASES["bin1"][0], FS, 1.0)["spur_bin"] == 1
    nyq = spectrum.analyze(CASES["nyquist"][0], FS, 1.0)
    assert nyq["spur_bin"] == 512 and nyq["sfdr_dbc_adctoolbox"] > 84                    # 0.6.4 misses it


def test_the_pinned_toolbox_is_the_one_the_fix_is_for():
    import adctoolbox

    pin = re.search(r'"adctoolbox==([\d.]+)"', (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pin and pin.group(1) == spectrum.ADCTOOLBOX == adctoolbox.__version__


def test_every_sfdr_path_uses_the_estimator():
    x = CASES["issue36"][0]
    ctx: dict = {}
    m = measure_spectrum(x, FS, None, ctx)
    assert m["sfdr_dBc"] == pytest.approx(80.0, abs=1e-6)
    assert ctx["provenance"]["spectrum"]["estimator"] == spectrum.ESTIMATOR
    assert model.spectrum_metrics(x, FS)["sfdr_dbc"] == pytest.approx(80.0, abs=1e-6)


def _run_dir(tmp_path, samples: np.ndarray) -> Path:
    run = tmp_path / "run"
    (run / "jobs" / "tt_nom_27").mkdir(parents=True, exist_ok=True)
    (run / "stage" / "jobs" / "tt_nom_27").mkdir(parents=True, exist_ok=True)
    rows = [f"{i} {45e-9 + i * 10e-9:.9e} {v:.15e}" for i, v in enumerate(samples)]
    (run / "jobs" / "tt_nom_27" / "samples.txt").write_text("\n".join(rows) + "\n")
    (run / "stage" / "jobs" / "tt_nom_27" / "tb.scs").write_text("simulator lang=spectre\n")
    return run


def test_remeasure_replaces_only_the_estimator(tmp_path, monkeypatch):
    """A recorded tracking result with the #36 SFDR is measured again from its run data:
    SFDR changes, everything else must reproduce, the simulation meta is kept."""
    monkeypatch.setattr(runner, "result_dir", lambda b, t, v: tmp_path / "results")
    block, _ = find_test("tb_bootstrap_track")
    x = 0.45 + 0.4 * CASES["issue36"][0]
    run = _run_dir(tmp_path, x)
    job = runner.Job("tt_nom_27", by_name("tt_nom_27"), {"npts": 256 * 4, "tper": 10e-9}, {"vdd": 0.9})
    old = spectrum.analyze(x - x.mean(), 1e8, None)
    metrics = {"sfdr_dBc": old["sfdr_dbc_adctoolbox"], "sndr_dB": old["sndr_dbc"], "thd_dBc": old["thd_dbc"]}
    meta = {"date": "then", "git": "abc1234", "files": {"x": "0"}}
    (tmp_path / "results").mkdir()
    path = tmp_path / "results" / "tt_nom_27.json"
    path.write_text(json.dumps(runner.result_doc(block, "tb_bootstrap_track", "behav", job, metrics, meta)))
    out = runner.remeasure("tb_bootstrap_track", run)
    assert list(out[0]["changed"]) == ["sfdr_dBc"]
    doc = json.loads(path.read_text())
    assert doc["metrics"]["sfdr_dBc"] == pytest.approx(80.0, abs=1e-6)
    assert doc["meta"]["git"] == "abc1234" and doc["meta"]["remeasured"]["run"] == "run"
    assert doc["meta"]["remeasured"]["changed"]["sfdr_dBc"][0] == pytest.approx(7.78, abs=0.01)
    assert doc["meta"]["provenance"]["spectrum"]["estimator"] == spectrum.ESTIMATOR
    assert doc["specs"]["BST-05"]["value"] == pytest.approx(80.0, abs=1e-6) and doc["figures"]   # re-judged
    # other data than the recorded simulation: refused, nothing written
    _run_dir(tmp_path, x * 1.001 + 1e-3 * np.sin(np.arange(len(x))))
    before = path.read_text()
    with pytest.raises(ValueError, match="not the same simulation data"):
        runner.remeasure("tb_bootstrap_track", run)
    assert path.read_text() == before
