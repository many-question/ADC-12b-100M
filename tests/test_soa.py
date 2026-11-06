"""Per-device SOA check (adcflow.soa): plans from netlists, verdicts from waveforms."""

import json
import re

import numpy as np
import pytest

from adcflow import REPO_ROOT, candidates, jsonio, psf, soa, soa_core
from adcflow.corners import by_name
from adcflow.runner import Job, _by_rows, _same, make_deck, view_files
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
    return [(r["device"], r["pair"]) for r in soa.table_rows(m) if r["pass"] != bad]


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
    assert all(r["max_V"] <= 1.0 and r["pass"] for r in soa.table_rows(m))


def test_negative_vgs_violation():
    """g = 0, s = 1.15 V: Vgs = -1.15 V. A check of VG - VS > 1 V alone would pass it."""
    p = _one("XDUT.M1", {"d": "D", "g": "G", "s": "S", "b": "0"})
    w = {"time": T, "D": np.full_like(T, 0.5), "G": np.zeros_like(T), "S": np.array([0, 0, 1.15, 1.15, 0, 0])}
    m = soa.check(p, w)
    assert m["soa_violations"] == 1 and _rows(m) == [("XDUT.M1", "gs")]
    gs = soa.table_rows(m)[0]
    assert gs["signed_V"] == pytest.approx(-1.15) and gs["max_V"] == pytest.approx(1.15)
    assert gs["t_ns"] == pytest.approx(1.01)
    assert m["soa_worst"]["device"] == "XDUT.M1" and m["soa_worst"]["pair"] == "gs"


def test_vds_violation():
    p = _one("XDUT.M2", {"d": "D", "g": "G", "s": "0", "b": "0"})
    w = {"time": T, "D": np.array([0, 0, 0.6, 1.15, 0.6, 0]), "G": np.full_like(T, 0.5)}
    m = soa.check(p, w)
    assert m["soa_violations"] == 1 and _rows(m) == [("XDUT.M2", "ds")]
    assert m["soa_max_V"] == pytest.approx(1.15)
    assert soa.table_rows(m)[2]["t_ns"] == pytest.approx(1.02)


def test_internal_device_violation(tmp_path):
    """A spike on the internal node XDUT.n1 only: the ports stay clean, devices inside fail."""
    w = _clean()
    w["XDUT.n1"] = np.array([0.45, 0.45, 1.5, 0.45, 0.45, 0.45])       # above the transient limit too
    m = soa.check(_plan(tmp_path), w)
    assert sorted(_rows(m)) == [("XDUT.M1", "ds"), ("XDUT.X1.MN", "gs")]
    assert m["soa_violations"] == 2
    assert all(r["where"] == "dut" for r in soa.table_rows(m) if not r["pass"])
    assert m["soa_worst"]["t_ns"] == pytest.approx(1.01)


def test_violation_is_counted_per_pair_not_per_event():
    p = _one("XDUT.M1", {"d": "D", "g": "G", "s": "0", "b": "0"})
    w = {"time": T, "D": np.array([0, 0.9, 0, 0.9, 0, 0]), "G": np.array([0, 1.4, 0, 1.4, 0, 0])}
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
    bad = {(r["device"], r["pair"]): r["signed_V"] for r in soa.table_rows(m) if not r["pass"]}
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


def test_time_above_the_limit_is_interpolated():
    """A 1.2 V triangle peak 2 ps wide is above 1.0 V for 1/3 ps."""
    t = np.array([0.0, 1e-12, 2e-12, 3e-12, 4e-12])
    assert soa.time_over(t, np.array([0.0, 0.0, 1.2, 0.0, 0.0]), 1.0) * 1e12 == pytest.approx(1 / 3)
    assert soa.time_over(t, np.array([0.0, -1.1, -1.1, 0.0, 0.0]), 1.0) * 1e12 == pytest.approx(1 + 2 / 11)
    assert soa.time_over(t, np.array([0.0, 0.5, 1.0, 0.5, 0.0]), 1.0) == 0
    p = _one("XDUT.M1", {"d": "D", "g": "G", "s": "0", "b": "0"})
    w = {"time": t, "D": np.array([0.0, 0.0, 1.2, 0.0, 0.0]), "G": np.array([0.0, 0.0, 0.99, 0.99, 0.0])}
    m = soa.check(p, w)
    rows = {r["pair"]: r for r in soa.table_rows(m)}
    assert rows["ds"]["t_over_ps"] == pytest.approx(1 / 3, abs=1e-3) and rows["ds"]["pass"]            # 1.2 V for 1/3 ps: within the transient rule
    assert rows["gs"]["t_over_ps"] == 0 and rows["gs"]["pass"]
    assert m["soa_violations"] == 0 and m["soa_worst"]["t_over_ps"] == pytest.approx(1 / 3, abs=1e-3)


# ------------------------------------------------------------------ the rule: 1.1 V, or 1.29 V for 100 ps in any 10 ns
def _gate(t_ps, v, limit=1.1):
    """One pair: Vgs follows (t_ps, v), the check over the waveform; returns its row."""
    t = np.asarray(t_ps, dtype=float) * 1e-12
    pl = soa.Plan(scope="device", limit_V=limit, duts=["XDUT"],
                  devices=[soa.Device("XDUT.M1", "nch_ulvt_mac", "mos", "dut", {"d": "0", "g": "G", "s": "0", "b": "0"})])
    return soa.table_rows(soa.check(pl, {"time": t, "G": np.asarray(v, dtype=float)}))[0]


def _pulse(start_ps, width_ps, v, edge_ps=0.001):
    """Points of one pulse to v, 0 V around it, from a nearly square edge."""
    return ([start_ps - edge_ps, start_ps, start_ps + width_ps, start_ps + width_ps + edge_ps], [0.0, v, v, 0.0])


def _train(pulses, stop_ps=100000.0):
    t, v = [0.0], [0.0]
    for p in pulses:
        a, b = _pulse(*p)
        t += a
        v += b
    return t + [stop_ps], v + [0.0]


def test_rule_comes_from_its_own_file_and_is_no_dependency():
    assert soa.rule() == {"peak_V": 1.29, "window_s": 10e-9, "max_over_s": 100e-12}
    assert soa.config()["limit_V"] == 1.1


@pytest.mark.parametrize("v,width_ps,ok", [
    (1.1, 100000.0, True),      # at the continuous limit, as long as it likes
    (1.0999, 90000.0, True),
    (1.1001, 90000.0, False),   # just above it, far too long
    (1.29, 99.0, True),         # at the transient limit
    (1.2901, 1.0, False),       # above it, however short
])
def test_rule_voltage_boundaries(v, width_ps, ok):
    r = _gate(*_train([(5000.0, width_ps, v)], 200000.0))
    assert r["pass"] is ok


def test_rule_at_100_ps_in_a_window():
    """Square pulses: a window of exactly 100 ps passes, a little more does not (the edges add under 1 fs)."""
    assert _gate(*_train([(5000.0, 100.0 - 0.002, 1.2)]))["pass"] is True
    assert _gate(*_train([(5000.0, 100.0 + 0.1, 1.2)]))["pass"] is False
    r = soa.passes(1.2, 100e-12, 1.1), soa.passes(1.2, 100e-12 * 1.001, 1.1)
    assert r == (True, False)


def test_excursion_within_the_average_duty_fails_one_window():
    """120 ps above 1.1 V within 5 ns, then nothing for 995 ns: 0.012 % on average, 120 ps in one window."""
    r = _gate(*_train([(1000.0, 60.0, 1.2), (5000.0, 60.0, 1.2)], 1000000.0))
    assert r["t_over_ps"] == pytest.approx(120.0, abs=0.01) and r["t_window_ps"] == pytest.approx(120.0, abs=0.01)
    assert r["pass"] is False


def test_the_same_excursions_in_separate_windows_pass():
    """The same two pulses 10.1 ns apart: 120 ps in all, never more than 60 ps in one window."""
    r = _gate(*_train([(1000.0, 60.0, 1.2), (11160.0, 60.0, 1.2)], 1000000.0))
    assert r["t_over_ps"] == pytest.approx(120.0, abs=0.01) and r["t_window_ps"] == pytest.approx(60.0, abs=0.01)
    assert r["pass"] is True


def test_window_slides_and_can_cut_a_pulse():
    """Two 80 ps pulses 9.91 ns apart: 160 ps in all, 90 ps in the worst window, which cuts one of them."""
    r = _gate(*_train([(1000.0, 80.0, 1.2), (10990.0, 80.0, 1.2)]))    # the second starts 9.91 ns after the first ends
    assert r["t_over_ps"] == pytest.approx(160.0, abs=0.01) and r["t_window_ps"] == pytest.approx(10000.0 - 9910.0, abs=0.01)
    assert r["pass"] is True


def test_startup_counts_and_a_run_shorter_than_the_window_is_one_window():
    r = _gate([0.0, 110.0, 110.001, 5000.0], [1.2, 1.2, 0.0, 0.0])
    assert r["t_window_ps"] == pytest.approx(110.0, abs=0.01) and r["pass"] is False


def test_both_polarities_add_up_in_a_window():
    t, v = _train([(1000.0, 60.0, 1.2), (5000.0, 60.0, -1.2)])
    r = _gate(t, v)
    assert r["t_window_ps"] == pytest.approx(120.0, abs=0.01) and r["pass"] is False


def test_worst_pair_reports_its_window_and_the_metrics_carry_the_rule():
    t = np.array([0.0, 1000.0, 1000.001, 1050.0, 1050.001, 5000.0]) * 1e-12
    pl = soa.Plan(scope="device", limit_V=1.1, duts=["XDUT"],
                  devices=[soa.Device("XDUT.M1", "nch_ulvt_mac", "mos", "dut", {"d": "0", "g": "G", "s": "0", "b": "0"})])
    m = soa.check(pl, {"time": t, "G": np.array([0.0, 0.0, 1.2, 1.2, 0.0, 0.0])})
    assert m["soa_violations"] == 0 and m["soa_max_V"] == pytest.approx(1.2)
    assert m["soa_window_max_ps"] == pytest.approx(50.0, abs=0.01) and m["soa_worst"]["t_window_ps"] == pytest.approx(50.0, abs=0.01)
    assert (m["soa_peak_V"], m["soa_window_ns"], m["soa_max_over_ps"]) == (1.29, 10.0, 100.0)


def _row(**kw):
    return {"device": "XDUT.M1", "master": "nch_ulvt_mac", "where": "dut", "pair": "gs", "pass": True, **kw}


def test_violations_applies_the_rule_when_judging():
    new = {"soa_limit_V": 1.1, "soa_window_ns": 10.0, "soa_violations": 1,
           "soa_table": [_row(max_V=1.2, t_over_ps=500.0, t_window_ps=50.0), _row(max_V=1.0, t_over_ps=0.0, t_window_ps=0.0)]}
    assert soa.violations(new) == 0                     # the table decides, not the recorded count
    assert soa.violations({**new, "soa_table": [_row(max_V=1.3, t_over_ps=1.0, t_window_ps=1.0)]}) == 1
    assert soa.violations({**new, "soa_table": [_row(max_V=1.2, t_over_ps=500.0, t_window_ps=150.0)]}) == 1
    assert soa.violations({"soa_violations": 0, "soa_table": []}) is None
    assert soa.violations({"noise_uV": 1.0}) is None


def test_results_recorded_before_the_rule_are_judged_by_their_total_time():
    old = {"soa_limit_V": 1.1, "soa_violations": 1, "soa_table": [_row(max_V=1.2, t_over_ps=40.0)]}
    assert soa.violations(old) == 0                     # 40 ps in all is at most 40 ps in any window
    old["soa_table"] = [_row(max_V=1.2, t_over_ps=400.0)]
    assert soa.violations(old) == 1                     # cannot be shown: stays a violation until it is rerun
    old["soa_table"] = [_row(max_V=1.2)]
    assert soa.violations(old) == 1
    # a window recorded for another length says nothing: the total time again
    assert soa.violations({"soa_limit_V": 1.1, "soa_window_ns": 20.0,
                           "soa_table": [_row(max_V=1.2, t_over_ps=400.0, t_window_ps=50.0)]}) == 1


def _packed(m: dict) -> dict:
    return {**m, "soa_table": soa.pack_table(m["soa_table"])}


def test_violations_is_the_same_for_both_forms_of_the_table():
    """The list of dicts of results recorded before pack_table and the packed table are judged alike,
    also without the windows of a result recorded before the rule."""
    base = {"soa_limit_V": 1.1, "soa_window_ns": 10.0, "soa_violations": 1}
    for rows, want in (([_row(max_V=1.2, t_over_ps=500.0, t_window_ps=50.0), _row(max_V=1.0, t_over_ps=0.0, t_window_ps=0.0)], 0),
                       ([_row(max_V=1.3, t_over_ps=1.0, t_window_ps=1.0)], 1),
                       ([_row(max_V=1.2, t_over_ps=500.0, t_window_ps=150.0)], 1),
                       ([_row(max_V=1.2, t_over_ps=40.0)], 0), ([_row(max_V=1.2, t_over_ps=400.0)], 1),
                       ([_row(max_V=1.2)], 1)):
        m = {**base, "soa_table": rows}
        if "t_window_ps" not in rows[0]:
            m.pop("soa_window_ns")
        assert soa.violations(m) == soa.violations(_packed(m)) == want


def test_block_verdict_uses_the_rule():
    b = blocks()["adc_clkgen"]
    m = {"soa_limit_V": 1.1, "soa_window_ns": 10.0, "soa_violations": 1, "soa_scope": "device", "soa_pairs": 1,
         "soa_table": [_row(max_V=1.2, t_over_ps=50.0, t_window_ps=50.0)]}
    judged, _ = b.verdicts("tb_clkgen_timing", "tt_nom_27", None, m)
    assert judged["CLK-11"]["pass"] is True and judged["CLK-11"]["value"] == 0


@pytest.mark.parametrize("block,test,spec", [("adc_sarlogic", "tb_sarlogic_soa", "LOG-17"),
                                             ("adc_comp", "tb_comp_soa", "CMP-17"),
                                             ("adc_cdac", "tb_cdac_soa", "DAC-18")])
def test_new_soa_tests_stand_alone(block, test, spec):
    """A judged spec at all corners, a test of its own with a crosscheck; no other test of the block has soa:."""
    b = blocks()[block]
    s = next(x for x in b.specs if x.id == spec)
    assert (s.metric, s.max, s.corners, s.test, s.reported) == ("soa_violations", 0, "all", test, False)
    assert b.tests[test]["soa"] == {"dut": ["XDUT"], "remote": True} and b.tests[test]["crosscheck"]["maxstep"] == "1p"
    assert [t for t, d in b.tests.items() if d.get("soa")] == [test]
    text = (REPO_ROOT / b.tests[test]["netlist"]).read_text(encoding="utf-8")
    assert "errpreset=conservative" in text and "maxstep" not in text


# ------------------------------------------------------------------ the check on the server (soa_core.reduce_job)
PSF_T = [0.0, 1e-9, 1.0001e-9, 1.05e-9, 1.0501e-9, 2e-9]
PSF_G = [0.0, 0.0, 1.2, 1.2, 0.0, 0.0]
PSF_D = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]


def _psf_job(tmp_path, plan_keep=("CK",)):
    raw = tmp_path / "deck.raw"
    raw.mkdir()
    vals = "".join(f'"time" {t:.15e}\n"CK" 0.5\n"XDUT.a\\<1\\>" {g:.15e}\n"D" {d:.15e}\n"OTHER" 0.25\n'
                   for t, g, d in zip(PSF_T, PSF_G, PSF_D))
    (raw / "tran1.tran.tran").write_text('HEADER\n"PSFversion" "1.00"\nTYPE\n"V" FLOAT DOUBLE PROP(\n"units" "V"\n)\nSWEEP\n"time" "sweep"\nTRACE\n'
                                         '"CK" "V"\n"XDUT.a\\<1\\>" "V"\n"D" "V"\n"OTHER" "V"\nVALUE\n' + vals + "END\n", encoding="utf-8")
    pl = soa.Plan(scope="device", limit_V=1.1, duts=["XDUT"],
                  devices=[soa.Device("XDUT.M1", "nch_ulvt_mac", "mos", "dut", {"d": "D", "g": "XDUT.a\\<1\\>", "s": "0", "b": "0"})])
    plan = soa.remote_plan(pl, "".join(f"save {k}\n" for k in plan_keep))
    (tmp_path / "soa_plan.json").write_text(json.dumps(plan), encoding="utf-8")
    return pl, raw / "tran1.tran.tran"


def test_server_check_gives_the_rows_of_a_local_check_and_thins_the_waveform(tmp_path):
    pl, f = _psf_job(tmp_path)
    full = psf.read(f)
    local = soa.check(pl, full)
    assert soa_core.reduce_job(tmp_path)["rows"] == soa.table_rows(local)
    thin = psf.read(f)
    assert sorted(thin) == sorted(["time", "CK", "XDUT.a<1>", "D"])          # OTHER is gone, the worst pair's nodes stay
    assert np.allclose(thin["XDUT.a<1>"], PSF_G) and np.allclose(thin["time"], PSF_T)
    m: dict = {}
    soa.measure({"soa": pl}, thin, m, tmp_path)
    assert {k: v for k, v in m.items() if k != "soa_waveform_MB"} == local
    assert m["soa_waveform_MB"] >= 0


def test_server_check_with_a_missing_node_is_unverified_and_keeps_the_waveform(tmp_path):
    pl, f = _psf_job(tmp_path)
    before = f.read_bytes()
    plan = json.loads((tmp_path / "soa_plan.json").read_text(encoding="utf-8"))
    plan["devices"][0]["nodes"]["d"] = "NOPE"
    (tmp_path / "soa_plan.json").write_text(json.dumps(plan), encoding="utf-8")
    doc = soa_core.reduce_job(tmp_path)
    assert doc["missing"] == ["NOPE"] and doc["rows"] == [] and f.read_bytes() == before
    pl.devices[0].nodes["d"] = "NOPE"
    m: dict = {}
    soa.measure({"soa": pl}, psf.read(f), m, tmp_path)
    assert "SOA unverified" in m["error"] and "soa_violations" not in m


def test_a_behavioral_run_has_no_server_check():
    pl = soa.Plan(scope="external", limit_V=1.1, note="nothing to check")
    assert soa.remote_plan(pl, "") is None
    assert soa.remote_plan(soa.Plan(scope="device", limit_V=1.1, problem="unknown"), "") is None


def test_core_runs_with_numpy_alone():
    text = (REPO_ROOT / "tools/adcflow/soa_core.py").read_text(encoding="utf-8")
    assert set(re.findall(r"^(?:from|import) (\S+)", text, re.M)) <= {"__future__", "json", "sys", "array", "pathlib", "numpy"}


# ------------------------------------------------------------------ the recorded table: packed, lossless, small
FIELDS = ["device", "master", "where", "pair", "max_V", "signed_V", "t_ns", "dt_ps", "t_over_ps", "t_window_ps", "pass"]


def _pairs(n: int) -> list[dict]:
    """n pairs like those of pair_rows: three per device, deep device names, a few above the limit."""
    rng = np.random.default_rng(7)
    rows = []
    for i in range(-(-n // 3)):
        name = f"XDUT.XSLICE{i % 12}.XCTRL.XGA{i // 12}.M{'PN'[i % 2]}{i}"
        master = ("nch_ulvt_mac", "pch_ulvt_mac", "nch_lvt_mac")[i % 3]
        for pair in ("gs", "gd", "ds"):
            v = round(float(rng.uniform(0.0, 1.0)), 5) + (0.25 if i % 40 == 0 else 0.0)
            over = round(float(rng.uniform(0.0, 80.0)), 3) if v > 1.1 else 0.0
            rows.append({"device": name, "master": master, "where": "dut" if i % 50 else "external", "pair": pair,
                         "max_V": v, "signed_V": round(float(-v if i % 2 else v), 5),
                         "t_ns": round(float(rng.uniform(0.0, 160.0)), 4), "dt_ps": round(float(rng.uniform(0.1, 400.0)), 3),
                         "t_over_ps": over, "t_window_ps": over, "pass": v <= 1.1 or over <= 100.0})
    return rows[:n]


@pytest.mark.parametrize("n", [5000, 10000])
def test_packed_table_is_lossless_and_fits_in_a_result(n):
    """Every field of every pair comes back, as it was written; the result stays below the size limit
    (a list of dicts takes about 200 bytes a pair, the packed table 77 in a real result, 90 at most here)."""
    rows = _pairs(n)
    doc = {"block": "adc_sarlogic", "metrics": {"soa_violations": 0, "soa_pairs": n, "soa_table": soa.pack_table(rows)}}
    text = jsonio.dumps(doc) + "\n"
    assert len(text.encode()) < min(candidates.MAX_JSON_BYTES, 90 * n + 5000)       # random digits: more than a real table
    old = jsonio.dumps({**doc, "metrics": {**doc["metrics"], "soa_table": rows}})
    assert len(old) > 2 * len(text)
    back = soa.table_rows(json.loads(text)["metrics"])
    assert back == rows and [list(r) for r in back] == [FIELDS] * n
    assert all(type(r["pass"]) is bool and type(r["max_V"]) is float for r in back)
    assert soa.table_rows(json.loads(old)["metrics"]) == rows            # and the old form reads back the same


def test_table_rows_reads_either_form_and_none():
    rows = _pairs(30)
    assert soa.table_rows({"soa_table": rows}) == rows
    assert soa.table_rows({"soa_table": soa.pack_table(rows)}) == rows
    assert soa.table_rows({"soa_table": []}) == soa.table_rows({"soa_table": soa.pack_table([])}) == []
    assert soa.table_rows({}) == soa.table_rows({"soa_table": None}) == []
    with pytest.raises(ValueError, match="not 'device'"):
        soa.table_rows({"soa_table": {"devices": [], "columns": ["pair"], "rows": []}})


def test_pack_table_factors_the_device_and_needs_uniform_rows():
    rows = _pairs(9)
    t = soa.pack_table(rows)
    assert len(t["devices"]) == 3 and t["devices"][0] == [rows[0]["device"], rows[0]["master"], rows[0]["where"]]
    assert t["columns"] == ["device", "pair", "max_V", "signed_V", "t_ns", "dt_ps", "t_over_ps", "t_window_ps", "pass"]
    assert [r[0] for r in t["rows"]] == [0, 0, 0, 1, 1, 1, 2, 2, 2]
    with pytest.raises(ValueError, match="same fields"):
        soa.pack_table([rows[0], {k: v for k, v in rows[1].items() if k != "dt_ps"}])


def test_check_records_the_packed_table(tmp_path):
    m = soa.check(_plan(tmp_path), _clean())
    t = m["soa_table"]
    assert isinstance(t, dict) and sorted(t) == ["columns", "devices", "rows"]
    assert len(t["devices"]) == m["soa_devices"] and len(t["rows"]) == m["soa_pairs"] == 12
    rows = soa.table_rows(m)
    assert [list(r) for r in rows] == [FIELDS] * 12
    assert {(r["device"], r["master"], r["where"]) for r in rows} >= {("XDUT.M1", "nch_ulvt_mac", "dut"),
                                                                       ("MEXT", "nch_ulvt_mac", "external")}
    assert soa.violations(m) == m["soa_violations"] == 0


def test_the_figure_reads_either_form(tmp_path, monkeypatch):
    """soa.figure takes its rows through table_rows: a packed table and the list of dicts give the same bars."""
    plan = _plan(tmp_path)
    w = _clean()
    m = soa.check(plan, w)
    seen = []
    monkeypatch.setattr(soa, "table_rows", lambda mm, f=soa.table_rows: seen.append(f(mm)) or seen[-1])

    class Sink:                                          # stops the figure right after its rows are read
        def new(self, *a, **k):
            raise StopIteration

    for metrics in (m, {**m, "soa_table": soa.table_rows(m)}):
        with pytest.raises(StopIteration):
            soa.figure(Sink(), {"soa": plan}, metrics, w)
    assert seen[0] == seen[1] and len(seen[0]) == 12


def test_remeasure_compares_the_pairs_not_the_form():
    rows = _pairs(30)
    old, new = {"soa_table": rows, "n": 1}, {"soa_table": soa.pack_table(rows), "n": 1}
    assert _same(_by_rows(old)["soa_table"], _by_rows(new)["soa_table"])
    assert not _same(_by_rows(old)["soa_table"], _by_rows({"soa_table": soa.pack_table(rows[:-1])})["soa_table"])
    assert _by_rows({"n": 1}) == {"n": 1}


def test_json_text_is_json_dumps_except_the_table_lines():
    doc = {"a": 1, "b": [], "c": {}, "d": {"e": [1.5, None, True, "ü\n"], "f": {"g": [[1, 2], [3]]}},
           "figures": [{"file": "x.png"}], "soa_table": [], "n": {"soa_table": [{"device": "D", "pair": "gs"}] * 3}}
    assert jsonio.dumps(doc) == json.dumps(doc, indent=1, default=float)
    num = {"x": np.float64(0.5), "y": float("nan")}
    assert jsonio.dumps(num) == json.dumps(num, indent=1, default=float)
    rows = _pairs(30)
    packed = {"m": {"soa_table": soa.pack_table(rows), "z": [1, 2]}}
    text = jsonio.dumps(packed)
    lines = text.split("\n")
    assert lines[:3] == ["{", ' "m": {', '  "soa_table": {']
    assert lines[3] == '    "devices": [' and lines[4].startswith('      ["XDUT.XSLICE0.XCTRL.XGA0.MP0","nch_ulvt_mac","external"]')
    assert sum(ln.startswith('      [0,"gs",') for ln in lines) == 1
    assert sum(ln.startswith("      [") for ln in lines) == 10 + 30                      # one line per device and per pair
    assert json.loads(text) == packed
    # the list of dicts of a large old-form table goes one pair per line, a small one as json.dumps writes it
    big = _pairs(jsonio.OLD_LINES_ABOVE + 3)
    t = jsonio.dumps({"metrics": {"soa_table": big}})
    assert t.count("\n") == len(big) + 5 and json.loads(t)["metrics"]["soa_table"] == big
    small = {"metrics": {"soa_table": big[:jsonio.OLD_LINES_ABOVE]}}
    assert jsonio.dumps(small) == json.dumps(small, indent=1, default=float)


def test_recorded_results_stay_readable_in_either_form():
    """A result of each directory that has a table: its pairs read back with every field, and packing
    them loses nothing and does not change the verdict (existing results are not rewritten)."""
    seen: set = set()
    for f in sorted((REPO_ROOT / "results").glob("*/*/*/*.json")):
        if f.parent in seen:
            continue
        m = json.loads(f.read_text(encoding="utf-8")).get("metrics") or {}
        if not m.get("soa_table"):
            continue
        seen.add(f.parent)
        rows = soa.table_rows(m)
        assert rows and all(set(FIELDS) - {"t_window_ps"} <= set(r) for r in rows), f      # no window before the rule
        packed = {**m, "soa_table": soa.pack_table(rows)}
        assert soa.table_rows(packed) == rows and soa.violations(packed) == soa.violations(m), f
    assert seen
