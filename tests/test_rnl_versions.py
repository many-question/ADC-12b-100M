"""The two RNL versions in the repository during the move from RNL 0.3 to 0.4.

Each file is checked with the pinned rnl command of the version it declares (checks.RNL_PINNED); the
project's packages exist once per version, generated from the same sources (gen.RNL_SETS) or, for the
hand-written adc28.rnl, kept in step by hand."""

import re

from adcflow import REPO_ROOT, checks, gen

RNL = REPO_ROOT / "design" / "rnl"


def _devices(path):
    return re.findall(r'@DEVICE\(name="\*", model="([^"]+)", terminals=(\[[^\]]*\])(?:, type="(\w+)")?\)',
                      path.read_text(encoding="utf-8"))


def test_check_summaries_of_both_cores():
    assert checks._rnl_counts("0 errors, 0 warnings, 0 hints") == (0, 0, 0)                     # core 0.5
    assert checks._rnl_counts("1 error, 2 violations, 0 warnings, 46 hints") == (3, 0, 46)      # core 0.6
    assert checks._rnl_counts("rnl: something else") is None


def test_every_declared_version_has_a_pinned_command():
    files = sorted(RNL.rglob("*.rnl")) + checks._netlists()
    langs = {checks.rnl_language(f) for f in files}
    assert langs <= set(checks.RNL_PINNED), langs
    assert checks.rnl_language(RNL / "adc28.rnl") == "0.3"
    assert checks.rnl_language(RNL / "0.4" / "adc28.rnl") == "0.4"


def test_packages_of_both_versions_declare_the_same_devices():
    old, new = _devices(RNL / "adc28.rnl"), _devices(RNL / "0.4" / "adc28.rnl")
    assert [(m, t) for m, t, _ in old] == [(m, t) for m, t, _ in new]
    for model, _, typ in new:                     # RNL 0.4 says the polarity the model cards cannot
        if model.startswith(("nch", "pch")):
            assert typ == f"{model[0]}mos", model
        else:
            assert typ == "", model


def test_generated_packages_of_both_versions_come_from_the_same_symbols():
    def body(text):
        text = text[text.index("@RNL {"):]
        return re.sub(r", recursive=true\)|\(recursive=true\)", ")", text)

    for fn in (gen.gen_rnl_blocks, gen.gen_rnl_va):
        old, new = fn(gen.RNL_SETS["0.3"]), fn(gen.RNL_SETS["0.4"])
        assert body(old) == body(new)
        assert '@VERSION("0.4")' in new and '@USE-PACKAGE(name="rnl-std-all", version="0.4")' in new
        assert all("recursive=true" in ln for ln in new.splitlines() if "@SELECT-" in ln)
        assert "recursive" not in old
