"""The site builds offline (`site/build.py --no-live`) with the repository's architecture,
including list-valued timing fields such as timing.t_dac_add (#35)."""

import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

# The site's own dependencies (site/requirements.txt) are installed by the site workflow, not by the
# test jobs: skip there instead of failing at collection.
pytest.importorskip("markdown_it")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

from sitegen import render  # noqa: E402


def _build_module():
    spec = importlib.util.spec_from_file_location("site_build", ROOT / "site" / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_site_builds_offline(tmp_path):
    r = subprocess.run([sys.executable, str(ROOT / "site" / "build.py"), "--no-live", "--out", str(tmp_path / "site")],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert "附加 DAC 等待 +10/+30/+30/+30/+25 ps（判决 3/4/5/6/9 之后）" in html
    # the home page labels its pass rate as the behavioral baseline and lists the verification combinations of the top level
    assert "行为级基线" in html and 'id="combos"' in html
    # the "behavioral ENOB" card reads the behavioral result, not whichever mixed run comes last
    card = html[html.index("行为级 ENOB"):html.index(">LSB<")]
    assert "results/adc_top/tb_top_sine/behav/tt_nom_27.json" in card and "xtor-" not in card
    # embedded viewers start inactive behind a "click to operate" button, and the live section no longer claims an hourly rebuild
    assert 'class="viewer-activate"' in html and 'data-act="exit"' in html and "点击以操作原理图" in html
    assert "站点每小时重建一次" not in html and "每小时的定时重建只是兜底" in html
    body = html[html.index('id="combos"'):].split("<tbody>")[1].split("</tbody>")[0]
    assert body.index("<code>behav</code>") < (body.index("<code>xtor-") if "<code>xtor-" in body else 10**9)         # all-behavioral first


def test_overview_accepts_any_list_valued_timing_field(tmp_path, monkeypatch):
    real = render.arch()
    raw = copy.deepcopy(real.raw)
    raw["timing"]["another_list"] = [1.0e-12, 2.0e-12]          # a further per-step list must not break the page
    patched = type(real)(raw)
    monkeypatch.setattr(render, "arch", lambda: patched)
    assert _build_module().build(tmp_path / "site", "pages", "", use_live=False) == []
    assert render.extra_waits([0, 0, 1e-11]) == " · 附加 DAC 等待 +10 ps（判决 3 之后）"
    assert render.extra_waits(None) == ""
