"""Specs are loadable and consistent; the CI checks catch what they should."""

import importlib
import re

import numpy as np
import pytest

from adcflow import REPO_ROOT, checks
from adcflow.corners import all_corners, corner_set
from adcflow.netlist import logical_lines, parse, substitute_parameters
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
    # the reference DC and noise tests load VREFP with the spec's average CDAC load
    iload = blocks()["adc_ref"].raw["operating"]["load_vrefp_dc"]
    for tb in ("tb/ref/tb_ref_dc.scs", "tb/ref/tb_ref_noise.scs"):
        m = re.search(r"^parameters iload=([\d.]+)u\b", (REPO_ROOT / tb).read_text(encoding="utf-8"), re.M)
        assert m and float(m[1]) * 1e-6 == pytest.approx(iload), tb


def _limit_fF(block: str, metric: str) -> float:
    return next(s.max for s in blocks()[block].specs if s.metric == metric) * 1e-15


# input-capacitance limit of every block input that a specified load drives
CIN_METRIC = {("adc_cdac", "PHI_S"): "cin_phs_fF", ("adc_cdac", "PHI_SB"): "cin_phsb_fF",
              ("adc_cdac", "CONV"): "cin_conv_fF", ("adc_bootstrap", "PHI_B"): "cin_phb_fF",
              ("adc_bootstrap", "PHI_BB"): "cin_phbb_fF", ("adc_sarlogic", "CONV"): "cin_conv_fF",
              ("adc_sarlogic", "OUTP"): "cin_cmp_fF", ("adc_sarlogic", "OUTN"): "cin_cmp_fF",
              ("adc_comp", "CLKC"): "cin_clkc_fF"}


def _cin_metric(block: str, port: str) -> str:
    return "cin_ctrl_fF" if block == "adc_cdac" and port[:2] in ("DH", "RL") else CIN_METRIC[(block, port)]


def _receivers(net: str) -> list[tuple[str, str]]:
    """(block, port) of every block input on a net of the structural top level."""
    top = parse(REPO_ROOT / "design" / "top" / "adc_top.scs").subckts["adc_top"]
    out = []
    for inst in top.instances:
        b = blocks()[inst.master]
        out += [(b.name, p.name) for p, n in zip(b.ports, inst.nodes) if n == net and p.dir == "in"]
    return out


def test_specified_loads_cover_the_receivers():
    """Every specified output load is at least the input-capacitance limits of all inputs on that net
    (counted in the top-level netlist) plus about 20 % of the load for the wire (PR #23 audit C-E)."""
    loads = dict(blocks()["adc_clkgen"].raw["operating"]["loads"])
    op = {b: blocks()[b].raw["operating"] for b in ("adc_comp", "adc_sarlogic")}
    loads.update({"OUTP": op["adc_comp"]["load_per_output"], "OUTN": op["adc_comp"]["load_per_output"],
                  "CLKC": op["adc_sarlogic"]["load_clkc"], "DN5": op["adc_sarlogic"]["load_updn"]})
    for net, load in loads.items():
        rx = _receivers(net)
        assert rx, net
        cin = sum(_limit_fF(b, _cin_metric(b, p)) for b, p in rx)
        wire = load - cin
        assert 0.19 * load <= wire <= 0.31 * load + 1e-18, (net, rx, load, cin)


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


def test_owner_field_is_validated_on_load(tmp_path):
    """check owners is retired (open-candidates row 2); the spec loader still rejects a bad owner:
    and adc_top keeps owner: many-question."""
    from adcflow.specs import SpecError, _load_block

    assert blocks()["adc_top"].raw["owner"] == "many-question"
    text = blocks()["adc_comp"].path.read_text(encoding="utf-8")
    bad = re.sub(r"^owner: .*$", "owner: not a login", text, count=1, flags=re.M)
    p = tmp_path / "adc_comp.yaml"
    p.write_text(bad, encoding="utf-8")
    with pytest.raises(SpecError, match="owner"):
        _load_block(p)


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


def test_startup_bench_follows_the_power_up_sequence():
    """tb_ref_startup applies adc_ref.yaml operating.power_up (issue #34): both supplies ramp together
    in supply_ramp, VREF_IN stays at 0 V for vref_dwell after them and then ramps in vref_ramp, and the
    run outlasts ready."""
    from adcflow.measure.ref import startup_times

    pu = blocks()["adc_ref"].raw["operating"]["power_up"]
    ts = startup_times()
    text = (REPO_ROOT / "tb" / "ref" / "tb_ref_startup.scs").read_text(encoding="utf-8")
    waves = {m[1]: [float(x) for x in m[2].split()[::2]]
             for m in re.finditer(r"^(\w+) \(\w+ 0\) vsource type=pwl wave=\[(.*?) \w+\]$", text, re.M)}
    assert waves["VH"] == waves["VA"] == pytest.approx([0, ts["sup0"], ts["sup0"] + pu["supply_ramp"]])
    assert waves["VREF"] == pytest.approx([0, ts["ref0"], ts["ref0"] + pu["vref_ramp"]])
    assert pu["vref_dwell"] >= 5e-6 and ts["ref0"] == pytest.approx(ts["sup1"] + pu["vref_dwell"])
    assert ts["ready"] == pytest.approx(ts["ref1"] + pu["ready"]) and ts["stop"] > ts["ready"]
    stop = float(re.search(r"^parameters tstop=(\S+)$", text, re.M)[1])
    assert stop == pytest.approx(ts["stop"])


def test_ref04_line_sweep_stays_inside_the_supply_envelope():
    """#46: tb_ref_dc sweeps AVDD18 over the specified envelope (corners.yaml) at every corner,
    not +/-10 % around the corner's own supply (up to 2.178 V at the high corners)."""
    from adcflow.corners import supply_envelope

    lo, hi = supply_envelope("vdd18")
    assert (lo, hi) == (min(c.vdd18 for c in all_corners()), max(c.vdd18 for c in all_corners()))
    assert (lo, hi) == pytest.approx((1.62, 1.98))
    text = (REPO_ROOT / "tb" / "ref" / "tb_ref_dc.scs").read_text(encoding="utf-8")
    line = next(ln for _, ln in logical_lines(text) if ln.startswith("dcline "))
    kv = dict(re.findall(r"(\w+)=(\S+)", line))
    assert "vdd18" not in line                                     # independent of the corner's supply
    start, stop, step = (float(kv[k]) for k in ("start", "stop", "step"))
    pts = np.arange(start, stop + step / 2, step)
    assert pts[0] == pytest.approx(lo) and pts[-1] == pytest.approx(hi) and len(pts) == 5
    assert all(lo - 1e-12 <= v <= hi + 1e-12 for v in pts)
