"""Per-device SOA check (adcflow.soa): plans from netlists, verdicts from waveforms."""

import re

import numpy as np
import pytest

from adcflow import REPO_ROOT, psf, soa
from adcflow.corners import by_name
from adcflow.runner import Job, make_deck, view_files
from adcflow.specs import blocks, find_test


@pytest.fixture(autouse=True)
def _no_selection(monkeypatch):
    """The transistor-level cases here swap in their own netlist as the legacy plain `xtor` view,
    which only applies while a block has no selected candidate: clear main's selections."""
    for b in blocks().values():
        if b.raw.get("selected") not in (None, "none"):
            monkeypatch.setitem(b.raw, "selected", "none")


DUT = """simulator lang=spectre
subckt inv (A Y VDD VSS)
MP (Y A VDD VDD) pch_ulvt_mac w=1u l=30n
MN (Y A VSS VSS) nch_ulvt_mac w=1u l=30n
ends inv
subckt dut (IN OUT VDD VSS)
M1 (n1 IN VSS VSS) nch_ulvt_mac w=1u l=30n
X1 (n1 OUT VDD VSS) inv
MT (OUT n1 VSS VSS) nch_18_mac w=1u l=150n
C1 (n1 VSS) capacitor c=1f
ends dut
"""
TB = """simulator lang=spectre
XDUT (IN OUT VDD 0) dut
MEXT (OUT IN 0 0) nch_ulvt_mac w=1u l=30n
tran1 tran stop=3n
save OUT
"""
SOA = {"soa": {"dut": ["XDUT"], "external": ["MEXT"]}}
T = np.array([0.0, 1e-9, 1.01e-9, 1.02e-9, 2e-9, 3e-9])


def _plan(tmp_path, dut=DUT, tb=TB, test=SOA):
    f = tmp_path / "dut.scs"
    f.write_text(dut)
    return soa.plan("dut", test, tb, [f], {})


def _clean() -> dict:
    """Every node at a safe constant level."""
    c = lambda v: np.full_like(T, v)  # noqa: E731
    return {"time": T, "IN": c(0.5), "OUT": c(0.4), "VDD": c(0.9), "XDUT.n1": c(0.45)}


def _one(device: str, nodes: dict[str, str], where: str = "dut") -> soa.Plan:
    return soa.Plan(scope="device", limit_V=1.0, duts=["XDUT"],
                    devices=[soa.Device(device, "nch_ulvt_mac", "mos", where, nodes)])


def _rows(m: dict, bad: bool = True) -> list[tuple[str, str]]:
    return [(r["device"], r["pair"]) for r in m["soa_table"] if r["pass"] != bad]


# ------------------------------------------------------------------ plan
def test_every_pdk_mos_model_is_classified():
    """Each MOS / MOS-capacitor model of the RNL package is listed in specs/soa.yaml, thin or thick."""
    text = (REPO_ROOT / "design" / "rnl" / "adc28.rnl").read_text(encoding="utf-8")
    models = re.findall(r'@DEVICE\(name="\*", model="([^"]+)"', text)
    mos = [m for m in models if soa.classify(m) is not None]
    assert len(mos) >= 20
    assert all(soa.classify(m) in ("mos", "moscap", "thick") for m in mos)
    assert soa.classify("nch_18_mac") == "thick" and soa.classify("pch_ulvt_mac") == "mos"
    assert soa.classify("nch_svt_foo") == "unknown" and soa.classify("cfmom_2t") is None


def test_plan_flattens_the_dut(tmp_path):
    p = _plan(tmp_path)
    assert p.scope == "device" and p.problem is None
    nodes = {d.name: d.nodes for d in p.devices}
    assert list(nodes) == ["XDUT.M1", "XDUT.X1.MP", "XDUT.X1.MN", "MEXT"]
    assert nodes["XDUT.M1"] == {"d": "XDUT.n1", "g": "IN", "s": "0", "b": "0"}
    assert nodes["XDUT.X1.MP"] == {"d": "OUT", "g": "XDUT.n1", "s": "VDD", "b": "VDD"}
    assert [d.where for d in p.devices] == ["dut", "dut", "dut", "external"]
    assert p.skipped == ["XDUT.MT (nch_18_mac)"]
    assert p.signals() == ["IN", "OUT", "VDD", "XDUT.n1"]
    lines = soa.deck_lines(p, TB)                  # OUT is saved by the testbench already
    assert lines[-1].split() == ["save", "IN", "VDD", "XDUT.n1"]


def test_plan_unknown_mos_model_is_unverified(tmp_path):
    p = _plan(tmp_path, dut=DUT.replace("M1 (n1 IN VSS VSS) nch_ulvt_mac", "M1 (n1 IN VSS VSS) nch_xyz_mac"))
    assert "XDUT.M1 (nch_xyz_mac)" in p.problem
    with pytest.raises(soa.Unverified, match="cannot be resolved"):
        soa.check(p, _clean())


def test_plan_unparsed_device_line_is_unverified(tmp_path):
    """A MOS written without parentheses is not read by the netlist reader: never skipped silently."""
    p = _plan(tmp_path, dut=DUT.replace("M1 (n1 IN VSS VSS) nch_ulvt_mac", "M1 n1 IN VSS VSS nch_ulvt_mac"))
    assert "not read as an instance" in p.problem and "M1 n1 IN" in p.problem


def test_plan_bad_config_fails_before_simulating(tmp_path):
    with pytest.raises(ValueError, match="XNONE"):
        _plan(tmp_path, test={"soa": {"dut": ["XNONE"]}})
    with pytest.raises(ValueError, match="external device"):
        _plan(tmp_path, test={"soa": {"dut": ["XDUT"], "external": ["XDUT"]}})


def test_bootstrap_behavioral_view_is_external_only():
    """tb_bootstrap_dc with the behavioral view: only the reference switch, already saved."""
    b, t = find_test("tb_bootstrap_dc")
    text = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8")
    p = soa.plan(b.name, t, text, view_files({}), {})
    assert p.scope == "external" and p.problem is None
    assert [(d.name, d.where, d.nodes) for d in p.devices] == \
        [("MSWP", "external", {"d": "BP", "g": "VG", "s": "VIN", "b": "0"})]
    assert soa.deck_lines(p, text) == []


def _xtor(tmp_path, monkeypatch, body: str):
    f = tmp_path / "adc_bootstrap.scs"
    f.write_text("simulator lang=spectre\nsubckt adc_bootstrap (VIN PHI_B PHI_BB VG AVDD VSS)\n" + body
                 + "ends adc_bootstrap\n")
    monkeypatch.setitem(blocks()["adc_bootstrap"].raw["views"], "xtor", str(f))
    b, t = find_test("tb_bootstrap_dc")
    text = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8")
    views = {"adc_bootstrap": "xtor"}
    return soa.plan(b.name, t, text, view_files(views), views), text, views


def test_bootstrap_transistor_view_saves_internal_nodes(tmp_path, monkeypatch):
    p, text, views = _xtor(tmp_path, monkeypatch,
                           "MS (VG boot VIN VSS) nch_ulvt_mac w=1u l=30n\n"
                           "MP (boot PHI_BB AVDD AVDD) pch_ulvt_mac w=1u l=30n\n")
    assert p.scope == "device" and p.problem is None
    assert [d.name for d in p.devices] == ["XDUT.MS", "XDUT.MP", "MSWP"]
    assert p.devices[0].nodes == {"d": "VG", "g": "XDUT.boot", "s": "VIN", "b": "0"}
    # VG VIN BP: saved by the testbench; PHI_BBX is the DUT side of the PHI_BB input-capacitance meter
    assert soa.deck_lines(p, text)[-1] == "save AVDD PHI_BBX XDUT.boot"


def test_deck_carries_the_soa_saves_after_the_testbench():
    _, t = find_test("tb_bootstrap_dc")
    job = Job("tt_nom_27", by_name("tt_nom_27"), {}, {"vdd": 0.9},
              tb_text=(REPO_ROOT / t["netlist"]).read_text(encoding="utf-8"))
    deck, _ = make_deck(job, "<R>", {}, False, None, ["// soa", "save XDUT.boot"])
    assert deck.rstrip().endswith("save XDUT.boot")
    assert deck.index("tb.scs") < deck.index("save XDUT.boot")


def test_bootstrap_transistor_view_without_devices_is_unverified(tmp_path, monkeypatch):
    p, _, _ = _xtor(tmp_path, monkeypatch, "R0 (VIN VG) resistor r=1k\n")
    assert p.scope == "device" and "no thin-oxide device found under XDUT" in p.problem
    with pytest.raises(soa.Unverified):
        soa.check(p, {"time": T})


# ------------------------------------------------------------------ verdicts
def test_clean_case(tmp_path):
    m = soa.check(_plan(tmp_path), _clean())
    assert m["soa_violations"] == 0 and m["soa_scope"] == "device"
    assert m["soa_devices"] == 4 and m["soa_devices_dut"] == 3 and m["soa_pairs"] == 12
    assert m["soa_skipped"] == ["XDUT.MT (nch_18_mac)"]
    assert m["soa_max_V"] == pytest.approx(0.5)            # |Vgs| of M1 and MEXT, |Vds| of MP
    assert all(r["max_V"] <= 1.0 and r["pass"] for r in m["soa_table"])


def test_negative_vgs_violation():
    """g = 0, s = 1.15 V: Vgs = -1.15 V. A check of VG - VS > 1 V alone would pass it."""
    p = _one("XDUT.M1", {"d": "D", "g": "G", "s": "S", "b": "0"})
    w = {"time": T, "D": np.full_like(T, 0.5), "G": np.zeros_like(T), "S": np.array([0, 0, 1.15, 1.15, 0, 0])}
    m = soa.check(p, w)
    assert m["soa_violations"] == 1 and _rows(m) == [("XDUT.M1", "gs")]
    gs = m["soa_table"][0]
    assert gs["signed_V"] == pytest.approx(-1.15) and gs["max_V"] == pytest.approx(1.15)
    assert gs["t_ns"] == pytest.approx(1.01)
    assert m["soa_worst"]["device"] == "XDUT.M1" and m["soa_worst"]["pair"] == "gs"


def test_vds_violation():
    p = _one("XDUT.M2", {"d": "D", "g": "G", "s": "0", "b": "0"})
    w = {"time": T, "D": np.array([0, 0, 0.6, 1.15, 0.6, 0]), "G": np.full_like(T, 0.5)}
    m = soa.check(p, w)
    assert m["soa_violations"] == 1 and _rows(m) == [("XDUT.M2", "ds")]
    assert m["soa_max_V"] == pytest.approx(1.15)
    assert m["soa_table"][2]["t_ns"] == pytest.approx(1.02)


def test_internal_device_violation(tmp_path):
    """A spike on the internal node XDUT.n1 only: the ports stay clean, devices inside fail."""
    w = _clean()
    w["XDUT.n1"] = np.array([0.45, 0.45, 1.2, 0.45, 0.45, 0.45])
    m = soa.check(_plan(tmp_path), w)
    assert sorted(_rows(m)) == [("XDUT.M1", "ds"), ("XDUT.X1.MN", "gs")]
    assert m["soa_violations"] == 2
    assert all(r["where"] == "dut" for r in m["soa_table"] if not r["pass"])
    assert m["soa_worst"]["t_ns"] == pytest.approx(1.01)


def test_violation_is_counted_per_pair_not_per_event():
    p = _one("XDUT.M1", {"d": "D", "g": "G", "s": "0", "b": "0"})
    w = {"time": T, "D": np.array([0, 0.9, 0, 0.9, 0, 0]), "G": np.array([0, 1.1, 0, 1.1, 0, 0])}
    m = soa.check(p, w)
    assert m["soa_violations"] == 1 and _rows(m) == [("XDUT.M1", "gs")]


def test_missing_data_is_an_error_not_zero(tmp_path):
    p = _plan(tmp_path)
    w = _clean()
    del w["XDUT.n1"]
    with pytest.raises(soa.Unverified, match="XDUT.n1"):
        soa.check(p, w)
    with pytest.raises(soa.Unverified, match="no SOA plan"):
        soa.check(None, _clean())
    late = _clean()
    late["time"] = T + 1e-9
    with pytest.raises(soa.Unverified, match="whole transient"):
        soa.check(p, late)
    m = {"vgs_min_V": 0.85}
    soa.measure({"soa": p}, w, m)
    assert m["error"].startswith("SOA unverified") and "soa_violations" not in m


def test_parsed_psf_sample(tmp_path):
    """Hierarchical and escaped node names as Spectre writes them in PSF-ASCII."""
    dut = DUT.replace("n1", "n\\<1\\>")
    p = _plan(tmp_path, dut=dut)
    assert "XDUT.n\\<1\\>" in p.signals()
    vals = {"IN": [0.5, 0.5, 0.5], "OUT": [0.4, 0.4, 0.4], "VDD": [0.9, 0.9, 0.9],
            "XDUT.n\\<1\\>": [0.45, -0.3, 0.45]}
    lines = ["HEADER", '"PSFversion" "1.00"', "TYPE", "SWEEP", '"time" "sweep"', "TRACE"]
    lines += [f'"{k}" "V"' for k in vals] + ["VALUE"]
    for i, t in enumerate([0.0, 1e-9, 2e-9]):
        lines.append(f'"time" {t:.15e}')
        lines += [f'"{k}" {v[i]:.15e}' for k, v in vals.items()]
    f = tmp_path / "tran.tran"
    f.write_text("\n".join(lines + ["END", ""]))
    m = soa.check(p, psf.read(f))
    bad = {(r["device"], r["pair"]): r["signed_V"] for r in m["soa_table"] if not r["pass"]}
    assert bad == {("XDUT.X1.MP", "gs"): pytest.approx(-1.2)}


# ------------------------------------------------------------------ adc_clkgen (CLK-11, issue #27)
def test_clkgen_behavioral_view_has_nothing_to_check():
    """Behavioral DUT and no thin-oxide device at the testbench top level: an explicit external
    scope with no pairs and a note, not an error and not a silent device check."""
    b, t = find_test("tb_clkgen_timing")
    assert t["soa"] == {"dut": ["XDUT"]}
    text = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8")
    p = soa.plan(b.name, t, text, view_files({}), {})
    assert p.scope == "external" and p.problem is None and p.devices == []
    assert p.note.startswith("nothing to check: XDUT uses behavioral views")
    assert soa.deck_lines(p, text) == []
    m = {"td_s_ps": 46.0}
    soa.measure({"soa": p}, {"time": T, "CLK": np.zeros_like(T)}, m)
    assert "error" not in m
    assert m["soa_scope"] == "external" and m["soa_devices"] == 0 and m["soa_pairs"] == 0
    assert m["soa_violations"] == 0 and m["soa_table"] == [] and m["soa_note"] == p.note
    assert "soa_max_V" not in m
    with pytest.raises(soa.Unverified, match="whole transient"):     # still needs the whole run
        soa.check(p, {"time": T + 1e-9})


def test_clkgen_transistor_view_is_a_device_check(tmp_path, monkeypatch):
    f = tmp_path / "adc_clkgen.scs"
    f.write_text("simulator lang=spectre\n"
                 "subckt adc_clkgen (CLK PHI_S PHI_SB PHI_B PHI_BB CONV AVDD VSS)\n"
                 "MP (clkb CLK AVDD AVDD) pch_ulvt_mac w=1u l=30n\n"
                 "MN (clkb CLK VSS VSS) nch_ulvt_mac w=1u l=30n\n"
                 "MS (PHI_S clkb VSS VSS) nch_ulvt_mac w=1u l=30n\n"
                 "ends adc_clkgen\n")
    monkeypatch.setitem(blocks()["adc_clkgen"].raw["views"], "xtor", str(f))
    b, t = find_test("tb_clkgen_timing")
    text = (REPO_ROOT / t["netlist"]).read_text(encoding="utf-8")
    views = {"adc_clkgen": "xtor"}
    p = soa.plan(b.name, t, text, view_files(views), views)
    assert p.scope == "device" and p.problem is None and p.note is None
    assert [d.name for d in p.devices] == ["XDUT.MP", "XDUT.MN", "XDUT.MS"]
    assert p.devices[2].nodes == {"d": "PHI_S", "g": "XDUT.clkb", "s": "0", "b": "0"}
    assert soa.deck_lines(p, text)[-1] == "save AVDD XDUT.clkb"     # CLK, PHI_S: saved by the testbench
    empty = tmp_path / "empty.scs"
    empty.write_text("simulator lang=spectre\nsubckt adc_clkgen (CLK PHI_S PHI_SB PHI_B PHI_BB CONV AVDD VSS)\n"
                     "R0 (CLK PHI_S) resistor r=1k\nends adc_clkgen\n")
    monkeypatch.setitem(blocks()["adc_clkgen"].raw["views"], "xtor", str(empty))
    p = soa.plan(b.name, t, text, view_files(views), views)
    assert "no thin-oxide device found under XDUT" in p.problem      # never "nothing to check"


def test_unlisted_mos_at_the_testbench_top_level_is_unverified(tmp_path):
    tb = TB.replace("MEXT (OUT IN 0 0) nch_ulvt_mac", "MEXT (OUT IN 0 0) nch_xyz_mac")
    p = _plan(tmp_path, tb=tb, test={"soa": {"dut": ["XDUT"]}})
    assert "MEXT (nch_xyz_mac)" in p.problem


def test_time_above_the_limit_is_a_diagnostic_only():
    """A 1.2 V triangle peak 2 ps wide is above 1.0 V for 1/3 ps. The verdict is the peak alone."""
    t = np.array([0.0, 1e-12, 2e-12, 3e-12, 4e-12])
    assert soa.time_over(t, np.array([0.0, 0.0, 1.2, 0.0, 0.0]), 1.0) * 1e12 == pytest.approx(1 / 3)
    assert soa.time_over(t, np.array([0.0, -1.1, -1.1, 0.0, 0.0]), 1.0) * 1e12 == pytest.approx(1 + 2 / 11)
    assert soa.time_over(t, np.array([0.0, 0.5, 1.0, 0.5, 0.0]), 1.0) == 0
    p = _one("XDUT.M1", {"d": "D", "g": "G", "s": "0", "b": "0"})
    w = {"time": t, "D": np.array([0.0, 0.0, 1.2, 0.0, 0.0]), "G": np.array([0.0, 0.0, 0.99, 0.99, 0.0])}
    m = soa.check(p, w)
    rows = {r["pair"]: r for r in m["soa_table"]}
    assert rows["ds"]["t_over_ps"] == pytest.approx(1 / 3, abs=1e-3) and not rows["ds"]["pass"]
    assert rows["gs"]["t_over_ps"] == 0 and rows["gs"]["pass"]
    assert m["soa_violations"] == 1 and m["soa_worst"]["t_over_ps"] == pytest.approx(1 / 3, abs=1e-3)
