"""SFDR (issue #36): the pinned ADCToolbox against the true values and MATLAB plotspec."""

import json
import re
import sys
from importlib import metadata
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


@pytest.mark.parametrize("name", sorted(set(CASES) - {"clean", "quantized"}))
def test_sfdr_matches_matlab_plotspec(name):
    """Same value as MATLAB ADCToolbox plotspec on a tone (values recorded with tests/matlab/sfdr_plotspec.m).
    `clean`: plotspec's automatic sideBin is 0 on a noise-free spectrum (6.02 dB). `quantized`: below."""
    assert spectrum.analyze(CASES[name][0], FS, 1.0)["sfdr_dbc"] == pytest.approx(MATLAB_PLOTSPEC[name], abs=1e-3)


def test_sfdr_on_a_noise_floor_is_the_summed_spur_window():
    """No injected tone: the spur is the window around the largest bin over the ENBW, plotspec its single bin."""
    assert spectrum.analyze(CASES["quantized"][0], FS, 1.0)["sfdr_dbc"] == pytest.approx(88.418, abs=1e-3)
    assert MATLAB_PLOTSPEC["quantized"] == pytest.approx(88.083, abs=1e-3)


def test_sndr_limit_that_remains():
    """A spur that touches the signal bins partly counts as signal: SNDR about 0.8 dB high. Nyquist is seen now."""
    assert spectrum.analyze(CASES["issue36"][0], FS, 2.0)["sndr_dbc"] == pytest.approx(80.792, abs=1e-3)
    assert spectrum.analyze(CASES["nonoverlap"][0], FS, 1.0)["sndr_dbc"] == pytest.approx(80.0, abs=1e-3)
    assert spectrum.analyze(CASES["nyquist"][0], FS, 1.0)["sndr_dbc"] == pytest.approx(80.0, abs=1e-3)


def test_the_pinned_toolbox_is_the_commit_with_the_fix():
    import adctoolbox

    pin = re.search(r"ADCToolbox@([0-9a-f]+)#subdirectory=python", (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pin and pin.group(1).startswith(spectrum.ADCTOOLBOX_COMMIT)
    assert adctoolbox.__version__ == spectrum.ADCTOOLBOX
    assert spectrum.ADCTOOLBOX_COMMIT in spectrum.PROVENANCE["estimator"]
    installed = json.loads(metadata.distribution("adctoolbox").read_text("direct_url.json") or "{}")
    assert installed.get("vcs_info", {}).get("commit_id", "").startswith(spectrum.ADCTOOLBOX_COMMIT)


class _Install:
    """An adctoolbox install as importlib.metadata shows it."""
    version = "0.9.1"

    def __init__(self, direct_url):
        self.direct_url = direct_url

    def read_text(self, name):
        return self.direct_url if name == "direct_url.json" else None


@pytest.fixture
def install(monkeypatch):
    def use(direct_url):
        monkeypatch.setattr(spectrum.metadata, "distribution", lambda name: _Install(direct_url))
        spectrum.toolbox_problem.cache_clear()
    yield use
    spectrum.toolbox_problem.cache_clear()


WRONG_INSTALLS = {
    "pypi": None,                                                       # the same version string, no fix
    "another commit": json.dumps({"vcs_info": {"vcs": "git", "commit_id": "0123456789abcdef"}}),
    "local checkout": json.dumps({"dir_info": {"editable": True}}),
}


@pytest.mark.parametrize("name", WRONG_INSTALLS)
def test_metrics_and_runs_refuse_any_other_install(install, name):
    install(WRONG_INSTALLS[name])
    assert spectrum.ADCTOOLBOX_COMMIT in spectrum.toolbox_problem()
    with pytest.raises(RuntimeError, match="pip install"):
        spectrum.analyze(CASES["issue36"][0], FS, 2.0)
    with pytest.raises(RuntimeError, match="pip install"):       # before anything is simulated
        runner.run_test("tb_top_sine")
    with pytest.raises(RuntimeError, match="pip install"):
        runner.remeasure("tb_top_sine", REPO_ROOT)
    assert runner.run_test("tb_top_sine", dry=True) is not None  # a dry run measures nothing


def test_the_pinned_install_passes_and_no_install_is_left_to_the_import(install, monkeypatch):
    install(json.dumps({"vcs_info": {"commit_id": spectrum.ADCTOOLBOX_COMMIT + "1ff3b7a977"}}))
    assert spectrum.toolbox_problem() is None
    spectrum.require_toolbox()

    def missing(name):
        raise metadata.PackageNotFoundError(name)
    monkeypatch.setattr(spectrum.metadata, "distribution", missing)
    spectrum.toolbox_problem.cache_clear()
    assert spectrum.toolbox_problem() is None


def test_the_local_sfdr_is_retired():
    assert not hasattr(spectrum, "sfdr_dbc")
    assert "sfdr_dbc_adctoolbox" not in spectrum.analyze(CASES["issue36"][0], FS, 2.0)


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
    metrics = {"sfdr_dBc": 7.78, "sndr_dB": old["sndr_dbc"], "thd_dBc": old["thd_dbc"]}   # the #36 value
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


def test_redraw_refuses_any_metric_change(tmp_path, monkeypatch):
    """#47: --redraw rewrites the figures of a result from its run data; every metric must come
    out as recorded (they are written back unchanged) and meta.redrawn says so."""
    monkeypatch.setattr(runner, "result_dir", lambda b, t, v: tmp_path / "results")
    block, _ = find_test("tb_bootstrap_track")
    x = 0.45 + 0.4 * CASES["near3"][0][:256]
    run = _run_dir(tmp_path, x)
    job = runner.Job("tt_nom_27", by_name("tt_nom_27"), {"npts": 256, "tper": 10e-9}, {"vdd": 0.9})
    new = spectrum.analyze(x - x.mean(), 1e8, None)
    metrics = {"sfdr_dBc": new["sfdr_dbc"], "sndr_dB": new["sndr_dbc"], "thd_dBc": new["thd_dbc"]}
    (tmp_path / "results").mkdir()
    path = tmp_path / "results" / "tt_nom_27.json"
    path.write_text(json.dumps(runner.result_doc(block, "tb_bootstrap_track", "behav", job, metrics,
                                                 {"date": "then", "git": "abc1234", "files": {}})))
    runner.remeasure("tb_bootstrap_track", run, redraw=True)
    doc = json.loads(path.read_text())
    assert doc["metrics"] == metrics and doc["meta"]["redrawn"]["run"] == "run"
    assert "remeasured" not in doc["meta"] and doc["figures"]
    old = dict(metrics, sfdr_dBc=metrics["sfdr_dBc"] - 1.0)                 # a different estimator: refused
    path.write_text(json.dumps(runner.result_doc(block, "tb_bootstrap_track", "behav", job, old, {})))
    with pytest.raises(ValueError, match="sfdr_dBc"):
        runner.remeasure("tb_bootstrap_track", run, redraw=True)
