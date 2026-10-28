"""Specs are loadable and consistent; the CI checks catch what they should."""

import importlib
import re

import pytest

from adcflow import REPO_ROOT, checks
from adcflow.corners import all_corners, corner_set
from adcflow.netlist import parse, substitute_parameters
from adcflow.specs import blocks


def test_45_corners():
    assert len(all_corners()) == 45
    assert len({c.name for c in all_corners()}) == 45
    assert [c.name for c in corner_set("typ")] == ["tt_nom_27"]


def test_every_test_has_netlist_and_measure():
    for b in blocks().values():
        for tid, t in b.tests.items():
            assert (REPO_ROOT / t["netlist"]).exists(), f"{b.name}:{tid}"
            mod, fn = t["measure"].split(":")
            assert callable(getattr(importlib.import_module(mod), fn)), t["measure"]
            if "prepare" in t:
                mod, fn = t["prepare"].split(":")
                assert callable(getattr(importlib.import_module(mod), fn))


def test_spec_ids_unique_across_blocks():
    ids = [s.id for b in blocks().values() for s in b.specs]
    assert len(ids) == len(set(ids))


def test_testbench_parameters_exist():
    """Every parameter a test overrides is declared in its testbench."""
    for b in blocks().values():
        for tid, t in b.tests.items():
            params = dict(t.get("params") or {})
            params.pop("fin_target", None)
            if "fin_target" in (t.get("params") or {}):
                params["fin"] = 1
            for v in t.get("variants") or []:
                params.update(v)
            text = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8")
            _, done = substitute_parameters(text, {k: v for k, v in params.items()})
            assert set(params) <= done, f"{tid}: {set(params) - done}"


def test_testbench_loads_follow_the_specs():
    """Capacitive loads in the generated testbenches are the `operating:` values of the specs."""
    def caps(path):
        text = (REPO_ROOT / path).read_text(encoding="utf-8")
        return {m[1]: float(m[2]) * 1e-15 for m in re.finditer(r"^CL(\w+) \(\w+ 0\) capacitor c=([\d.]+)f$", text, re.M)}

    loads = blocks()["adc_clkgen"].raw["operating"]["loads"]
    for tb in ("tb/clkgen/tb_clkgen_timing.scs", "tb/clkgen/tb_clkgen_jitter.scs"):
        assert caps(tb) == pytest.approx(loads), tb
    # the CDAC top-plate load is the comparator input capacitance limit
    cmp12 = next(s for s in blocks()["adc_comp"].specs if s.id == "CMP-12")
    assert blocks()["adc_cdac"].raw["operating"]["top_load"] == pytest.approx(cmp12.max * 1e-15)


def test_ports_check_passes():
    assert checks.check_ports().errors == []


def test_ports_check_detects_mismatch(tmp_path, monkeypatch):
    bad = tmp_path / "adc_comp.scs"
    bad.write_text("simulator lang=spectre\nsubckt adc_comp (INP INN CLKC OUTP AVDD VSS)\nends adc_comp\n")
    b = blocks()["adc_comp"]
    monkeypatch.setitem(b.raw["views"], "behav", str(bad))
    errs = checks.check_ports().errors
    assert any("ports of adc_comp differ" in e for e in errs)


# examples are assembled from pieces so this file itself stays clean
SLASH = "/"
LEAKS = [
    "root: " + SLASH + "server_" + "scratch/x",
    "source " + SLASH + "home" + SLASH + "someone/.c" + "shrc.tools",
    "include " + chr(34) + "lib.scs" + chr(34) + " section=tt",
    "dir: " + SLASH + "opt/pdk/models" + SLASH + "spectre",
    "+ toxe = 1.2e-9",
    "model nch bsim4 level=54",
]


@pytest.mark.parametrize("text", LEAKS)
def test_hygiene_patterns(text):
    assert any(re.search(p, text, flags=re.MULTILINE | re.IGNORECASE) for p, _ in checks.FORBIDDEN)


def test_hygiene_clean_repo():
    assert checks.check_hygiene().errors == []


def test_netlist_parser_reads_views():
    nl = parse(REPO_ROOT / "design" / "behav" / "adc_comp.scs")
    assert nl.subckts["adc_comp"].ports == blocks()["adc_comp"].port_names
    assert {i.master for i in nl.subckts["adc_comp"].instances} >= {"adc_comp_va", "capacitor"}


# the forbidden process names are assembled from pieces so this file stays clean
NAME_EXAMPLES = ["TS" + "MC 28 nm", "CRN28" + "HPC+ULL models", "台" + "积电", "ts" + "mc28"]


@pytest.mark.parametrize("text", NAME_EXAMPLES)
def test_process_names_are_caught(text):
    assert checks.find_names(text)


def test_process_names_allow_plain_process():
    assert checks.find_names("28 nm HPC+ (0.9 V / 1.8 V), 工艺角") == []


@pytest.mark.parametrize("old,new,author,ok", [
    ("TBD", "alice", "alice", True),            # claim
    ("TBD", "Alice", "alice", True),            # logins are case-insensitive
    ("alice", "TBD", "alice", True),            # release
    ("TBD", "bob", "alice", False),             # claim for someone else
    ("alice", "bob", "bob", False),             # take over a claimed block
    ("alice", "TBD", "bob", False),             # release someone else's claim
    ("alice", "alice", "bob", True),            # unchanged
    (None, "TBD", "bob", True),                 # new block file, unclaimed
])
def test_owner_change_rules(old, new, author, ok):
    assert checks.owner_change_allowed(old, new, author) is ok


def test_owners_in_repo_are_valid():
    assert checks.check_owners().errors == []


def test_git_state_ignores_results_and_caps_paths():
    from adcflow.runner import dirty_paths

    porcelain = "\n".join([
        " M results/adc_top/tb_top_sine/behav/tt_nom_27.json",
        "?? results/adc_comp/tb_comp_noise/behav/tt_nom_27.noise.png",
        " M specs/arch.yaml",
        "M  tools/adcflow/model.py",
        "?? analysis/new.py",
        "R  docs/old.md -> docs/new.md",
    ])
    assert dirty_paths(porcelain) == ["specs/arch.yaml", "tools/adcflow/model.py", "analysis/new.py", "docs/new.md"]
    assert dirty_paths(" M results/x.json\n") == []
    assert dirty_paths("") == []


def test_git_state_meta(monkeypatch):
    import subprocess
    from adcflow import runner

    class R:
        returncode = 0
        stdout = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: R)
    assert runner.git_state() == {"git_clean": True}
    R.stdout = " M results/a.json\n" + "".join(f"?? f{i}.txt\n" for i in range(25))
    st = runner.git_state()
    assert st["git_clean"] is False and len(st["git_dirty_paths"]) == 20 and st["git_dirty_paths"][0] == "f0.txt"


def test_probit_fit_recovers_sigma_with_interval():
    import numpy as np
    from scipy.stats import norm

    from adcflow.measure.comp import NOISE_LEVELS, probit_fit

    vd = np.asarray(NOISE_LEVELS)
    n = np.full(vd.size, 512)
    rng = np.random.default_rng(5)
    hits = 0
    for _ in range(20):
        k = rng.binomial(n, norm.cdf((vd - 30e-6) / 200e-6))
        f = probit_fit(vd, k, n)
        lo, hi = f["ci95"]
        assert lo < f["sigma"] < hi and abs(f["sigma"] / 200e-6 - 1) < 0.12 and abs(f["mu"] - 30e-6) < 30e-6
        hits += lo <= 200e-6 <= hi
    assert hits >= 16                       # ~95 % coverage
    # exact expected counts: the fit returns the true parameters
    k = np.round(n * norm.cdf((vd + 50e-6) / 150e-6))
    f = probit_fit(vd, k, n)
    assert f["sigma"] == pytest.approx(150e-6, rel=0.01) and f["mu"] == pytest.approx(-50e-6, abs=2e-6)
