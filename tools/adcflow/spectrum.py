"""Sine-test spectrum metrics: ENOB, SNDR, SFDR, SNR, THD from ADCToolbox ``compute_spectrum``.

The toolbox is pinned to the release 0.9.2 from PyPI, the first release with the fix for the SFDR
of a spur touching the signal bins (issue #36, Arcadia-1/ADCToolbox#100). Results recorded before
#96 name the upstream commit cd72061 instead; 0.9.2 gives the same metrics on them.
docs/sfdr-estimator.md has the history, the cases and the limit that remains (SNDR).
"""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import metadata

import numpy as np

ADCTOOLBOX = "0.9.2"            # the release the metrics come from (pyproject.toml pins it)
ESTIMATOR = f"adctoolbox {ADCTOOLBOX} compute_spectrum"
PROVENANCE = {"estimator": ESTIMATOR, "adctoolbox": ADCTOOLBOX}


@lru_cache
def toolbox_problem() -> str | None:
    """Why the installed adctoolbox is not the pinned release, None when it is or none is installed
    (its import then fails by itself). A git or local checkout is refused even at the same version
    string: it can carry changes after the release, and PROVENANCE names the release whatever is installed."""
    try:
        dist = metadata.distribution("adctoolbox")
    except metadata.PackageNotFoundError:
        return None
    source = json.loads(dist.read_text("direct_url.json") or "{}")   # empty for an install from PyPI
    if dist.version == ADCTOOLBOX and not source:
        return None
    commit = source.get("vcs_info", {}).get("commit_id", "")
    origin = f"git {commit[:7]}" if commit else "a local checkout" if source else "an index"
    return (f"adctoolbox {dist.version} (from {origin}) is not the pinned release {ADCTOOLBOX} from PyPI, "
            f"its SFDR can be wrong: run pip install -e \".[analysis]\"")


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
