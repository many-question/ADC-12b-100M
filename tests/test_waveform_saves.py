"""Bound disk usage without dropping metric signals or SOA terminal saves."""
import re

from adcflow import gen_tb


def test_every_bench_has_an_explicit_bounded_save_policy():
    for tb in gen_tb.all_tbs():
        text = gen_tb.render(tb)
        policies = re.findall(r"^\w+ options .*?\bsave=(\w+)", text, re.M)
        assert len(policies) == 1, tb.path
        assert policies[0] in {"selected", "none"}, tb.path
        saves = re.findall(r"^save (.+)$", text, re.M)
        assert all("*" not in line for line in saves), tb.path
        if policies[0] == "selected":
            assert saves, tb.path
        for line in tb.analyses + tb.extra:
            if line.startswith("save "):
                assert line in text, (tb.path, line)


def test_monitor_only_waveforms_stay_disabled():
    for tb in gen_tb.all_tbs():
        if any("save=none" in line for line in tb.analyses):
            text = gen_tb.render(tb)
            assert "save=none" in text
            assert "save=selected" not in text


def test_reference_noise_keeps_both_required_outputs():
    tb = next(tb for tb in gen_tb.all_tbs() if tb.path == "tb/ref/tb_ref_noise.scs")
    text = gen_tb.render(tb)
    assert "save VREFP VCM\n" in text
    assert "waveopts options save=selected\n" in text
