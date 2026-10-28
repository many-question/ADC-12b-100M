"""System model sanity: the ideal SAR is an exact quantizer; impairments behave."""

import numpy as np
import pytest

from adcflow import model as m
from adcflow.arch import Arch


def test_ideal_conversion_is_exact():
    a = Arch.load()
    rng = np.random.default_rng(3)
    vin = rng.uniform(-0.99, 0.99, 5000) * a.fs_peak
    r = m.convert(vin, a, m.ideal())
    level = (r.codes - a.code_offset) * a.lsb
    assert np.max(np.abs(level - vin)) <= 0.5 * a.lsb + 1e-12
    assert not r.incomplete.any()


def test_redundancy_absorbs_msb_errors():
    a = Arch.load()
    vin = np.linspace(-0.9, 0.9, 2001)
    # slow DAC settling in the first steps only: the redundancy must hide it
    ni = m.ideal(tau_dac=15e-12, t_dac=75e-12, t_dac_fast=30e-12, n_fast=6)   # 13.5 % residual
    r = m.convert(vin, a, ni)
    level = (r.codes - a.code_offset) * a.lsb
    # quantization (0.5 LSB) + the budgeted 0.25 LSB residual of the 75 ps (5 tau) slow-step wait;
    # without redundancy the 13.5 % residual of the fast steps would cost tens of LSB
    assert np.max(np.abs(level - vin)) <= 0.75 * a.lsb


@pytest.mark.slow
@pytest.mark.needs_toolbox
def test_budget_enob_at_hot():
    a = Arch.load()
    # comparator at its TT limit (the default), calibrated weights as in the acceptance tests
    met, _, _, _ = m.sine_test_cal(a, m.NonIdeal(temp_c=125), n_fft=4096, fin_target=49.7e6)
    assert met["enob"] > float(a.raw["targets"]["enob_design"])


@pytest.mark.needs_toolbox
def test_calibration_removes_mismatch_and_finds_gaps():
    from adcflow import calib

    a = Arch.load()
    ni = m.ideal(sigma_cu=4 * a.sigma_cu, seed=7)
    met, met_nom, _, _ = m.sine_test_cal(a, ni, n_fft=4096, fin_target=49.7e6)
    assert met["enob"] > 11.9 > met_nom["enob"]          # quantization limit after calibration
    margin = calib.cal_margin(a.w, a.w, a.sigma_w_lsb(), 4)
    assert margin.min() > 0 and margin[0] == pytest.approx(310.5 - 4 * a.sigma_cu * np.sqrt(a.w.sum()))
    w = a.w.copy()
    w[-2] += 0.6                                           # weight 2 too large by 0.6 LSB: a gap
    assert calib.cal_margin(w, a.w, a.sigma_w_lsb(), 4).min() < 0


def test_refnet_single_rc_matches_pole():
    # a plain resistive driver into a cap is one real pole: exp(-t / RC) / C
    p, r = m.RefNet(r_o=3.0, f_u=None, c1=100e-12).modes()
    assert p.size == 1
    assert p[0].real == pytest.approx(-1 / (3.0 * 100e-12), rel=1e-9)
    assert r[0].real == pytest.approx(1 / 100e-12, rel=1e-9)
    # the behavioral adc_ref (rout + s L into cdec + esr) is a damped pair near 63 MHz
    p, _ = m.RefNet.decap_2n().modes()
    assert p.size == 2 and np.all(p.real < 0)
    assert abs(p[0]) / (2 * np.pi) == pytest.approx(1 / (2 * np.pi * np.sqrt(1 / (2 * np.pi * 50e6) * 2e-9)), rel=0.02)


def test_coupling_charge_is_signed_square_law():
    # summed over a conversion, the top-plate coupling returns cu*lsb*gain_top*L^2/4 to VREFP
    a = Arch.load()
    vin = np.array([-0.9, -0.4, 0.0, 0.4, 0.9]) * a.fs_peak
    r = m.convert(vin, a, m.ideal(ref_signal_coupling=True))
    q_sig = r.info["q_sw"].sum(1) - a.w.sum() * a.cu / 2 * a.vref
    level = r.codes - a.code_offset
    expect = -a.cu * a.lsb * r.info["gain_top"] * level**2 / 4
    assert np.allclose(q_sig, expect, rtol=1e-3, atol=1e-17)


def test_follower_matches_linear_for_small_droop_and_noise_level():
    a = Arch.load()
    f = m.Follower(i_bias=4e-3, ic=1.0, c_node=50e-12, gamma=0.0)
    lin = m.NonIdeal(ref_follower=None, ref_net=m.RefNet(r_o=1 / f.g_s(), f_u=None, c1=50e-12),
                     ref_periodic=False)
    vin = np.linspace(-0.8, 0.8, 64) * a.fs_peak
    dv_f = m.convert(vin, a, m.NonIdeal(ref_follower=f)).info["dvref"]
    dv_l = m.convert(vin, a, lin).info["dvref"]
    assert np.max(np.abs(dv_f - dv_l)) < 0.1 * np.max(np.abs(dv_l))      # < 10 mV droops: nearly linear
    # node noise of the follower: gamma kT / C
    f = m.Follower(i_bias=2e-3, c_node=2e-12, gamma=2.0)
    ni = m.NonIdeal(ref_follower=f, ref_start_charge=False, ref_signal_coupling=False)
    sd = m.convert(np.zeros(4000), a, ni).info["dvref"][:, 0].std()
    assert sd == pytest.approx(np.sqrt(2.0 * 1.380649e-23 * 300.15 / 2e-12), rel=0.1)


def test_reference_charge_is_drawn_at_the_dac_drive():
    # the SAR logic drives the DAC t_bit after the decision and clocks the comparator t_dac later
    # (LOG-02 / 04): the VREFP charge of a step comes t_bit after its decision, not at it (issue #35)
    a = Arch.load()
    ni = m.ideal(t_bit=35e-12)
    r = m.convert(np.array([0.3, -0.7]) * a.fs_peak, a, ni)
    t_dec, t_sw = r.info["t_dec"], r.info["t_sw"]
    t_cmp = t_sw - t_dec[:, :-1] - ni.t_bit
    assert np.all(t_cmp >= ni.t_cmp0 - 1e-15)                     # comparator delay, then t_bit
    gap = t_dec[:, 1:] - t_sw                                       # DAC drive -> next decision
    assert np.allclose(gap[:, :ni.n_fast], ni.t_dac_fast) and np.allclose(gap[:, ni.n_fast:], ni.t_dac)
