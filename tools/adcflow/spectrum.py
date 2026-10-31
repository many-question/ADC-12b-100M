"""Sine-test spectrum metrics: ENOB, SNDR, SFDR, SNR, THD from ADCToolbox ``compute_spectrum``.

The toolbox is pinned to a commit, not a version: cd72061 reports 0.9.1, and PyPI's 0.9.1 still
has the SFDR error of a spur touching the signal bins (issue #36, Arcadia-1/ADCToolbox#100).
docs/sfdr-estimator.md has the history, the cases and the limit that remains (SNDR).
"""

from __future__ import annotations

import numpy as np

ADCTOOLBOX = "0.9.1"            # its version string, the same as PyPI's 0.9.1 without the fix
ADCTOOLBOX_COMMIT = "cd72061"   # the upstream commit the metrics come from (pyproject.toml pins it)
ESTIMATOR = f"adctoolbox {ADCTOOLBOX} @ {ADCTOOLBOX_COMMIT} compute_spectrum"
PROVENANCE = {"estimator": ESTIMATOR, "adctoolbox": ADCTOOLBOX, "adctoolbox_commit": ADCTOOLBOX_COMMIT}


def hann(n: int) -> np.ndarray:
    """Periodic Hann window of n points, as compute_spectrum uses it (scipy hann(n, sym=False)).

    A coherent sine at bin k then occupies exactly bins k-1 .. k+1; the symmetric window
    (numpy.hanning) adds a skirt around it that is not in the record (#47)."""
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / n)


def analyze(codes: np.ndarray, fs: float, full_scale: float | None) -> dict:
    """compute_spectrum metrics (adctoolbox key names)."""
    from adctoolbox.spectrum import compute_spectrum

    r = compute_spectrum(np.asarray(codes, dtype=float), fs=fs, max_scale_range=full_scale)
    return {k: float(v) for k, v in r["metrics"].items() if np.isscalar(v)}
