"""Sine-test spectrum metrics: ENOB, SNDR, SFDR, SNR, THD from ADCToolbox ``compute_spectrum``.

The toolbox is pinned to a commit, not a version: cd72061 reports 0.9.1, and PyPI's 0.9.1 still
has the SFDR error of a spur touching the signal bins (issue #36, Arcadia-1/ADCToolbox#100).
docs/sfdr-estimator.md has the history, the cases and the limit that remains (SNDR).
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import metadata

import numpy as np

ADCTOOLBOX = "0.9.1"            # its version string, the same as PyPI's 0.9.1 without the fix
ADCTOOLBOX_COMMIT = "cd72061"   # the upstream commit the metrics come from (pyproject.toml pins it)
ESTIMATOR = f"adctoolbox {ADCTOOLBOX} @ {ADCTOOLBOX_COMMIT} compute_spectrum"
PROVENANCE = {"estimator": ESTIMATOR, "adctoolbox": ADCTOOLBOX, "adctoolbox_commit": ADCTOOLBOX_COMMIT}


@lru_cache
def toolbox_problem() -> str | None:
    """Why the installed adctoolbox is not the pinned commit, None when it is or none is installed
    (its import then fails by itself). Only the install record tells: the version string is the same
    without the fix, and PROVENANCE names the pin whatever is installed."""
    try:
        dist = metadata.distribution("adctoolbox")
    except metadata.PackageNotFoundError:
        return None
    commit = json.loads(dist.read_text("direct_url.json") or "{}").get("vcs_info", {}).get("commit_id", "")
    if commit.startswith(ADCTOOLBOX_COMMIT):
        return None
    return (f"adctoolbox {dist.version} ({commit[:7] or 'not installed from git'}) is not the pinned commit "
            f"{ADCTOOLBOX_COMMIT}, its SFDR can be wrong: run pip install -e \".[analysis]\"")


def require_toolbox() -> None:
    """Stop before metrics that would carry PROVENANCE without coming from the pinned toolbox."""
    problem = toolbox_problem()
    if problem:
        raise RuntimeError(problem)


def hann(n: int) -> np.ndarray:
    """Periodic Hann window of n points, as compute_spectrum uses it (scipy hann(n, sym=False)).

    A coherent sine at bin k then occupies exactly bins k-1 .. k+1; the symmetric window
    (numpy.hanning) adds a skirt around it that is not in the record (#47)."""
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / n)


def analyze(codes: np.ndarray, fs: float, full_scale: float | None) -> dict:
    """compute_spectrum metrics (adctoolbox key names)."""
    from adctoolbox.spectrum import compute_spectrum

    require_toolbox()
    r = compute_spectrum(np.asarray(codes, dtype=float), fs=fs, max_scale_range=full_scale)
    return {k: float(v) for k, v in r["metrics"].items() if np.isscalar(v)}
