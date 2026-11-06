"""`import adcflow` sets one OpenBLAS thread before numpy or scipy load, unless the caller set a number:
a `sim` / `verify` process waits hours on the server and should not hold a BLAS buffer per CPU thread."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def _threads_seen(preset: str | None) -> str:
    env = {k: v for k, v in os.environ.items() if k != "OPENBLAS_NUM_THREADS"}
    env["PYTHONPATH"] = str(TOOLS)
    if preset is not None:
        env["OPENBLAS_NUM_THREADS"] = preset
    code = "import os, adcflow, numpy; print(os.environ['OPENBLAS_NUM_THREADS'])"
    return subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True,
                          check=True).stdout.strip()


@pytest.mark.parametrize("preset,seen", [(None, "1"), ("4", "4")])
def test_one_blas_thread_unless_the_caller_chose(preset, seen):
    assert _threads_seen(preset) == seen
