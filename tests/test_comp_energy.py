"""CMP-10 (#75): the average AVDD energy per comparison over the 36-decision mixed-amplitude sequence of tb_comp_delay.

The AVDD meter (tb_imeter_va) of the generated bench integrates exactly the 36 full CLKC cycles from the first rising edge, and
energy_fJ = AVDD charge x VDD / 36. Until adc_comp 0.5.0 the window was 0 .. 14.5 ns: a 100 ps lead-in before the first edge, 36.25
cycles. These tests catch a window with the lead-in or a partial cycle, a wrong cycle count, and an old bench measured as the new
definition."""

import re

import numpy as np
import pytest

from adcflow import REPO_ROOT
from adcflow.gen_tb import tb_comp
from adcflow.measure import comp
from adcflow.measure.comp import DELAY_LEVELS, N_DELAY, T0, TCYC
from adcflow.specs import blocks

BENCH = REPO_ROOT / "tb" / "comp" / "tb_comp_delay.scs"
VDD = 0.9


def _si(v: str) -> float:
    m = re.fullmatch(r"([-+0-9.eE]+)([fpnum]?)", v)
    return float(m.group(1)) * {"": 1, "f": 1e-15, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3}[m.group(2)]


def _bench(text: str) -> dict:
    """The timing of a tb_comp_delay netlist: meter window, clock, decisions, transient stop."""
    params = dict(re.findall(r"(\w+)=(\S+)", " ".join(ln for ln in text.splitlines() if ln.startswith("parameters "))))
    vck = next(ln for ln in text.splitlines() if ln.startswith("VCK "))
    clk = dict(re.findall(r"(\w+)=(\S+)", vck))
    meter = next(ln for ln in text.splitlines() if ln.startswith("IMAVDD "))
    vdp = next(ln for ln in text.splitlines() if ln.startswith("VDP "))
    steps = re.search(r"wave=\[([^]]*)\]", vdp).group(1).split()
    return {"tstart": _si(params["tstart"]), "tstop": _si(params["tstop"]), "delay": _si(clk["delay"]),
            "period": _si(clk["period"]), "rise": _si(clk["rise"]), "meter": meter,
            "tran": re.search(r"^tran1 tran stop=(\S+)", text, re.M).group(1),
            "levels": (len(steps) // 2 + 1) // 2}                                  # (0, v0) and two points per later step


def test_the_generated_meter_window_is_exactly_the_36_cycles_from_the_first_rising_edge():
    b = _bench(BENCH.read_text(encoding="utf-8"))
    assert 'tstart=tstart tstop=tstop label="AVDD" fname="power.txt"' in b["meter"]
    assert b["tran"] == "tstop"
    assert b["levels"] == N_DELAY == 2 * len(DELAY_LEVELS) == 36                  # one decision per cycle, the sequence twice
    assert b["period"] == pytest.approx(TCYC, abs=1e-18)
    assert b["tstart"] == pytest.approx(b["delay"], abs=1e-18) == pytest.approx(T0, abs=1e-18)   # no lead-in
    n = (b["tstop"] - b["tstart"]) / b["period"]
    assert n == pytest.approx(36, abs=1e-9)                                         # whole cycles only, 36 of them
    # the committed bench is the generator's output (adcflow gen --check also checks it)
    (tb,) = [t for t in tb_comp() if t.path.endswith("tb_comp_delay.scs")]
    assert f"parameters tstart={T0:g} tstop={T0 + N_DELAY * TCYC:g}" in tb.params


def _clock(t):
    """The VCK pulse of the bench: rises at T0 + k TCYC (10 ps edges), 190 ps high."""
    ph = (t - T0) % TCYC
    v = np.clip(ph / 10e-12, 0, 1) - np.clip((ph - 200e-12) / 10e-12, 0, 1)
    return np.where(t < T0, 0.0, v) * VDD


def _meter(t, i, t0, t1):
    """What tb_imeter_va writes: (average current over [t0, t1], t1 - t0)."""
    q = np.concatenate([[0.0], np.cumsum(np.diff(t) * (i[1:] + i[:-1]) / 2)])
    return (np.interp(t1, t, q) - np.interp(t0, t, q)) / (t1 - t0), t1 - t0


DT = 0.5e-12


def _grid(t_end):
    return np.arange(int(round(t_end / DT)) + 1) * DT


def _avdd(t, q_cycle=50e-15, q_lead=30e-15, i_static=2e-6):
    """A comparator's AVDD current on _grid: a static part, a 20 ps charge pulse after every rising edge and a lead-in charge
    before the first edge (a supply that charges internal nodes at start-up). Pulses on whole samples, so the trapezoidal
    integral is exact."""
    i = np.full_like(t, i_static)
    n = int(round(20e-12 / DT))
    for k in range(N_DELAY):
        e = int(round((T0 + k * TCYC) / DT))
        i[e:e + n] += q_cycle / 20e-12
    a, z = int(round(20e-12 / DT)), int(round(80e-12 / DT))
    i[a:z] += q_lead / 60e-12
    return i


def test_energy_is_the_charge_over_the_36_cycles_times_vdd_over_36():
    t = _grid(T0 + N_DELAY * TCYC)
    b = _bench(BENCH.read_text(encoding="utf-8"))
    i_avg, win = _meter(t, _avdd(t), b["tstart"], b["tstop"])
    t_rise = comp.psf.crossings(t, _clock(t), VDD / 2, +1)
    e = comp.comparison_energy(i_avg, win, VDD, t_rise)
    want = (50e-15 + 2e-6 * TCYC) * VDD * 1e15                       # per cycle: the pulse and the static current; no lead-in
    assert e == pytest.approx(want, rel=1e-3)
    # the window of adc_comp 0.5.0 (0 .. 14.5 ns, 36.25 cycles) holds the lead-in charge: refused, never reinterpreted
    old = _meter(t, _avdd(t), 0.0, b["tstop"])
    old_formula = old[0] * VDD * TCYC * 1e15                         # adc_comp 0.5.0: window average x VDD x 400 ps
    assert old_formula == pytest.approx((36 * 50e-15 + 2e-6 * 14.5e-9 + 30e-15) / 36.25 * VDD * 1e15, rel=1e-3)
    assert old_formula > want
    with pytest.raises(ValueError, match="not the 36 CLKC cycles"):
        comp.comparison_energy(*old, VDD, t_rise)


@pytest.mark.parametrize("t0, t1, why", [
    (0.0, T0 + 36 * TCYC, "lead-in before the first edge"),
    (T0, T0 + 35.75 * TCYC, "a partial last cycle"),
    (T0, T0 + 35 * TCYC, "35 cycles"),
    (T0, T0 + 37 * TCYC, "37 cycles"),
])
def test_a_wrong_window_is_refused(t0, t1, why):
    """The meter file gives the window length (where it starts is checked on the bench, above)."""
    t = _grid(T0 + 37 * TCYC)
    t_rise = comp.psf.crossings(t, _clock(t), VDD / 2, +1)
    i_avg, win = _meter(t, _avdd(t), t0, t1)
    with pytest.raises(ValueError, match="not the 36 CLKC cycles"):
        comp.comparison_energy(i_avg, win, VDD, t_rise[t_rise < t1])


def test_a_wrong_cycle_count_in_the_clock_is_refused():
    t = _grid(T0 + N_DELAY * TCYC)
    t_rise = comp.psf.crossings(t, _clock(t), VDD / 2, +1)
    assert len(t_rise) == N_DELAY
    with pytest.raises(ValueError, match="35 CLKC rising edges"):
        comp.comparison_energy(1e-6, N_DELAY * TCYC, VDD, t_rise[:-1])               # a clock that stopped one cycle early
    with pytest.raises(ValueError, match="CLKC rising edges"):
        comp.comparison_energy(1e-6, N_DELAY * TCYC, VDD, t_rise + TCYC / 2)         # edges half a cycle late
    with pytest.raises(ValueError):
        comp.comparison_energy(1e-6, None, VDD, t_rise)                              # a meter line without its window


def test_the_measure_reads_the_meter_window(tmp_path, monkeypatch):
    """comp.delay end to end on a synthetic run: power.txt as tb_imeter_va writes it (label, average current, window)."""
    t = _grid(T0 + N_DELAY * TCYC)
    clk = _clock(t)
    vds = DELAY_LEVELS * 2
    op, on = np.zeros_like(t), np.zeros_like(t)
    for k, vd in enumerate(vds):
        on_ = (t >= T0 + k * TCYC + 40e-12) & (t < T0 + k * TCYC + 200e-12)
        (op if vd > 0 else on)[on_] = VDD
    monkeypatch.setattr(comp, "tran", lambda job_dir: {"time": t, "CLKC": clk, "OUTP": op, "OUTN": on})
    b = _bench(BENCH.read_text(encoding="utf-8"))
    i_avg, win = _meter(t, _avdd(t), b["tstart"], b["tstop"])
    (tmp_path / "power.txt").write_text(f"AVDD {i_avg:.9e} {win:.6e}\n")
    m = comp.delay(tmp_path, {"globals": {"vdd": VDD}, "block": "adc_comp", "test": "tb_comp_delay"})
    assert m["energy_fJ"] == pytest.approx((50e-15 + 2e-6 * TCYC) * VDD * 1e15, rel=1e-3)
    assert m["wrong_decisions"] == 0
    (tmp_path / "power.txt").write_text(f"AVDD {i_avg:.9e} {14.5e-9:.6e}\n")       # a run of the 0.5.0 bench
    with pytest.raises(ValueError, match="regenerate tb_comp_delay"):
        comp.delay(tmp_path, {"globals": {"vdd": VDD}, "block": "adc_comp", "test": "tb_comp_delay"})


def test_cmp10_is_named_for_what_it_measures_and_reported_only():
    s = next(s for s in blocks()["adc_comp"].specs if s.id == "CMP-10")
    assert s.metric == "energy_fJ" and s.reported and s.max is None and s.corners == "typ" and s.test == "tb_comp_delay"
    assert "36-decision mixed-amplitude sequence" in s.name and "1 mV" not in s.name
    assert tuple(int(x) for x in blocks()["adc_comp"].raw["version"].split(".")) >= (0, 6, 0)
