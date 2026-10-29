"""Explicit transient settings of the tracking tests and their convergence cross-check (issue #28)."""

import numpy as np
import pytest

from adcflow import REPO_ROOT, numerics, runner
from adcflow.specs import blocks, find_test

TRACKING = ("tb_bootstrap_track", "tb_cdac_track")

LOG = """Global user options:
               temp = 27
               save = none
            vabstol = 1e-08
             reltol = 1e-07

Scoped user options:

Opening the PSFASCII file deck.raw/tran1.tran.tran ...
Important parameter values:
    start = 0 s
    outputstart = 2.605 us
    stop = 2.605 us
    step = 2.605 ns
    maxstep = 1 ps
    reltol = 100e-09
    abstol(V) = 10 nV
    abstol(I) = 1 pA
    temp = 27 C
    errpreset = moderate
    method = traponly
    lteratio = 3.5
    rabsshort = 1 mOhm


......9......8......7......6......5......4......3......2......1......0
Number of accepted tran steps =             2700000
"""


def _analyses(test_id: str) -> tuple[str, str]:
    _, t = find_test(test_id)
    lines = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8").splitlines()
    return next(ln for ln in lines if " tran " in ln), next(ln for ln in lines if " options " in ln)


@pytest.mark.parametrize("test_id", TRACKING)
def test_tracking_testbenches_carry_the_spec_settings(test_id):
    _, t = find_test(test_id)
    assert t["numerics"] == {"reltol": 1e-7, "vabstol": 1e-8, "maxstep": "1p", "method": "traponly"}
    assert t["crosscheck"] == {"maxstep": "0.5p", "method": "gear2only", "samples": "samples.txt"}
    tran, opts = _analyses(test_id)
    assert tran == "tran1 tran stop=tstop outputstart=tstop maxstep=1p method=traponly"
    assert opts == "tbopts options save=none reltol=1e-07 vabstol=1e-08"


def test_crosscheck_replaces_only_step_and_method():
    _, t = find_test("tb_bootstrap_track")
    text = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8")
    alt = numerics.apply(text, {"maxstep": "0.5p", "method": "gear2only"})
    diff = [(a, b) for a, b in zip(text.splitlines(), alt.splitlines()) if a != b]
    assert diff == [("tran1 tran stop=tstop outputstart=tstop maxstep=1p method=traponly",
                     "tran1 tran stop=tstop outputstart=tstop maxstep=0.5p method=gear2only")]


def test_bootstrap_dc_generates_numerics_and_preserves_full_waveform_crosscheck():
    _, test = find_test("tb_bootstrap_dc")
    assert test["numerics"] == {"reltol": 1e-7, "vabstol": 1e-8, "maxstep": "1p",
                                "method": "traponly", "errpreset": "conservative"}
    assert test["crosscheck"] == {"maxstep": "0.5p", "method": "gear2only", "samples": "vgs.txt"}
    text = (REPO_ROOT / test["netlist"]).read_text(encoding="utf-8")
    tran, opts = _analyses("tb_bootstrap_dc")
    assert tran == "tran1 tran stop=tstop maxstep=1p method=traponly errpreset=conservative"
    assert opts == "tbopts options reltol=1e-07 vabstol=1e-08"
    assert "save VG VIN PHI_B PHI_BB BP QPB QPBB" in text.splitlines()
    alt = numerics.apply(text, {k: v for k, v in test["crosscheck"].items() if k != "samples"})
    diff = [(a, b) for a, b in zip(text.splitlines(), alt.splitlines()) if a != b]
    assert diff == [(tran, "tran1 tran stop=tstop maxstep=0.5p method=gear2only errpreset=conservative")]


def test_conservative_log_uses_effective_transient_reltol():
    # The unchanged global request is 1e-7; the transient reports 1e-8.
    text = LOG.replace("reltol = 100e-09", "reltol = 10e-09").replace("errpreset = moderate", "errpreset = conservative")
    nu = numerics.from_log(text)
    assert nu["reltol"] == pytest.approx(1e-8)
    assert nu["vabstol"] == pytest.approx(1e-8)
    assert nu["errpreset"] == "conservative"


def test_clkgen_timing_generates_numerics_and_preserves_step_only_crosscheck():
    _, test = find_test("tb_clkgen_timing")
    assert test["numerics"] == {"reltol": 1e-7, "vabstol": 1e-8, "maxstep": "1p",
                                "method": "traponly", "errpreset": "conservative"}
    assert test["crosscheck"] == {"maxstep": "0.5p"}
    text = (REPO_ROOT / test["netlist"]).read_text(encoding="utf-8")
    tran, opts = _analyses("tb_clkgen_timing")
    assert tran == "tran1 tran stop=tstop maxstep=1p method=traponly errpreset=conservative"
    assert opts == "tbopts options reltol=1e-07 vabstol=1e-08"
    assert "parameters tstop=161n" in text.splitlines()
    assert "save CLK PHI_S PHI_SB PHI_B PHI_BB CONV" in text.splitlines()
    alt = numerics.apply(text, test["crosscheck"])
    diff = [(a, b) for a, b in zip(text.splitlines(), alt.splitlines()) if a != b]
    assert diff == [(tran, "tran1 tran stop=tstop maxstep=0.5p method=traponly errpreset=conservative")]


def test_apply_sets_and_appends():
    text = "simulator lang=spectre\ntran1 tran stop=1n maxstep=2p\nsave X\n"
    out = numerics.apply(text, {"maxstep": "1p", "method": "traponly"})
    assert out.splitlines()[1] == "tran1 tran stop=1n maxstep=1p method=traponly"
    with pytest.raises(ValueError, match="no options statement"):
        numerics.apply(text, {"reltol": 1e-7})
    assert numerics.set_params("o options save=none reltol=1e-5", {"reltol": 1e-7}) == "o options save=none reltol=1e-07"


def test_spec_settings_are_validated():
    assert numerics.validate({"maxstep": "1p", "method": "traponly"}, "x") == []
    assert numerics.validate({"maxstep": "1p", "metod": "trap"}, "x") == ["x: unknown key 'metod'"]
    assert "method 'gear3'" in numerics.validate({"method": "gear3"}, "x")[0]
    assert numerics.validate({"samples": "s.txt"}, "x", ("samples",)) == []


def test_effective_settings_from_the_log():
    nu = numerics.from_log(LOG)
    assert nu["reltol"] == pytest.approx(1e-7) and nu["vabstol"] == pytest.approx(1e-8)
    assert nu["maxstep_ps"] == pytest.approx(1.0) and nu["method"] == "traponly"
    assert nu["errpreset"] == "moderate" and nu["abstol_V"] == pytest.approx(1e-8)
    assert nu["steps_accepted"] == 2700000 and nu["step_mean_ps"] == pytest.approx(2605e-9 / 2.7e6 * 1e12)
    assert numerics.from_log("no transient here") == {}


def test_largest_step_only_from_a_waveform_of_the_whole_run(tmp_path):
    def psf(times):
        f = tmp_path / "tran1.tran.tran"
        f.write_text("HEADER\nVALUE\n" + "".join(f'"time" {t:.15e}\n"X" 0\n' for t in times) + "END\n")
        return f

    assert numerics.steps_from_waveform(psf([0, 1e-12, 3e-12, 3.5e-12, 4e-12]), 4e-12) == pytest.approx(2e-12)
    assert numerics.steps_from_waveform(psf([1e-12, 2e-12, 3e-12, 4e-12]), 4e-12) is None    # outputstart
    assert numerics.steps_from_waveform(psf([0, 4e-12]), 4e-12) is None
    assert numerics.steps_from_waveform(None, 1.0) is None


def test_compare_metrics_and_raw_samples(tmp_path):
    t = np.arange(4) * 10e-9
    a, b = tmp_path / "a.txt", tmp_path / "b.txt"
    a.write_text("".join(f"{i} {ti:.9e} {v:.9e}\n" for i, (ti, v) in enumerate(zip(t, [0.1, 0.2, 0.3, 0.4]))))
    b.write_text("".join(f"{i} {ti:.9e} {v:.9e}\n" for i, (ti, v) in enumerate(zip(t, [0.1, 0.2 + 3e-6, 0.3, 0.4]))))
    c = numerics.compare({"sfdr_dBc": 93.5, "sndr_dB": 92.9}, {"sfdr_dBc": 93.6, "sndr_dB": 92.9},
                         ["sfdr_dBc", "sndr_dB"], a, b)
    assert c["metrics"]["sfdr_dBc"]["diff"] == pytest.approx(0.1)
    s = c["samples"]
    assert s["n"] == 4 and s["time_diff_max_ps"] == pytest.approx(0.0)
    assert s["diff_max_uV"] == pytest.approx(3.0, rel=1e-3) and s["diff_rms_uV"] == pytest.approx(1.5, rel=1e-3)


def test_crosscheck_needs_settings_in_the_spec():
    assert "crosscheck" not in blocks()["adc_comp"].tests["tb_comp_delay"]
    with pytest.raises(ValueError, match="no `crosscheck:`"):
        runner.run_test("tb_comp_delay", crosscheck=True, dry=True)


def test_compare_soa_peaks():
    row = lambda dev, pair, v: {"device": dev, "pair": pair, "max_V": v}  # noqa: E731
    ref = {"soa_violations": 1, "soa_table": [row("XDUT.MA", "ds", 1.0638), row("XDUT.MB", "gs", 0.9)]}
    alt = {"soa_violations": 1, "soa_table": [row("XDUT.MA", "ds", 1.0641), row("XDUT.MB", "gs", 0.9)]}
    c = numerics.compare(ref, alt, ["soa_violations"], None, None)
    assert c["soa"] == {"pairs": 2, "max_V_diff_max_mV": pytest.approx(0.3), "at": "XDUT.MA ds", "violations": [1, 1]}
    assert c["metrics"]["soa_violations"]["diff"] == 0
