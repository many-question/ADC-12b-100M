"""SFDR estimator cases of issue #36 (docs/sfdr-estimator.md).

Coherent records of N = 1024 samples: a unit sine plus one deliberate spur whose true SFDR
(power of the fundamental over the power of the spur) is known. ``python tests/sfdr_cases.py
<dir>`` writes each record as <dir>/<case>.txt for tests/matlab/sfdr_plotspec.m.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

N = 1024
_n = np.arange(N)


def _tone(k: int, a: float, phase: float = 0.3) -> np.ndarray:
    return a * np.sin(2 * np.pi * k * _n / N + phase)


def _dbc(a: float) -> float:
    """SFDR of a unit sine over a sine spur of amplitude a."""
    return float(20 * np.log10(1 / a))


def cases() -> dict[str, tuple[np.ndarray, float, str]]:
    """name -> (record, true SFDR in dBc, what it tests)."""
    s301, s509 = _tone(301, 1.0, 0.0), _tone(509, 1.0, 0.0)
    q = np.round((_tone(509, 0.89, 0.7) + 1) * 2047.5) / 2047.5 - 1
    return {
        "issue36": (np.sin(2 * np.pi * 509 * _n / N) + 1e-4 * np.sin(2 * np.pi * 507 * _n / N), _dbc(1e-4),
                    "#36 repro: fundamental 509, -80 dBc at 507, next to the signal bins 508..510"),
        "lower_edge": (s301 + _tone(299, 1e-4), _dbc(1e-4), "-80 dBc next to the lower edge (299; signal 300..302)"),
        "upper_edge": (s301 + _tone(303, 1e-4), _dbc(1e-4), "-80 dBc next to the upper edge (303)"),
        "upper_edge_509": (s509 + _tone(511, 1e-4), _dbc(1e-4), "fundamental 509, -80 dBc at 511 (upper edge, below Nyquist)"),
        "nonoverlap": (s301 + _tone(305, 1e-4), _dbc(1e-4), "-80 dBc 4 bins away (305): no overlap with the signal bins"),
        "near2": (s301 + _tone(303, 1e-3), _dbc(1e-3), "real -60 dBc tone 2 bins from the fundamental (303)"),
        "near3": (s301 + _tone(298, 1e-3), _dbc(1e-3), "real -60 dBc tone 3 bins from the fundamental (298)"),
        "dc_offset": (s301 + 0.01 + _tone(150, 10 ** -4.5), 90.0, "DC offset 0.01 (not a spur) and -90 dBc at 150"),
        "bin1": (s301 + _tone(1, 1e-4), _dbc(1e-4), "-80 dBc at bin 1, the lowest non-DC bin"),
        "nyquist": (s301 + 1e-4 / np.sqrt(2) * np.cos(np.pi * _n), _dbc(1e-4),
                    "-80 dBc (power) cosine at Nyquist, bin 512"),
        "bin511": (s301 + _tone(511, 1e-4), _dbc(1e-4), "-80 dBc at bin 511, the last bin below Nyquist"),
        "clean": (s301, float("inf"), "clean double-precision sine"),
        "quantized": (q, float("nan"), "12-bit quantized -1 dBFS sine at 509 (no injected spur; no exact value)"),
    }


# MATLAB ADCToolbox plotspec (v1.32, R2025a; plotspec(x, 100e6, 2, 5, 'disp', false)) on the same records
MATLAB_PLOTSPEC = {"issue36": 80.0, "lower_edge": 80.0, "upper_edge": 80.0, "upper_edge_509": 80.0,
                   "nonoverlap": 80.0, "near2": 60.0, "near3": 60.0, "dc_offset": 90.0, "bin1": 80.0,
                   "nyquist": 80.0, "bin511": 80.0, "clean": 6.020599913, "quantized": 88.0827902}


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, (x, _, _) in cases().items():
        np.savetxt(out / f"{name}.txt", x, fmt="%.17g")
