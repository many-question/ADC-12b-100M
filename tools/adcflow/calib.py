"""Digital weight calibration shared by the acceptance tests, the CDAC metrics and the budget.

The ADC outputs raw bits; the backend decodes ``code = bits @ W`` with weights W
estimated per chip. Procedure (arch v0.3, docs/verification.md section 2):

1. calibration record: a coherent sine of the same chip; the bit weights are
   fitted to it (``adctoolbox.calibrate_weight_sine``, the wcalsin method) and
   scaled to the nominal sum (the fitted LSB scale is arbitrary);
2. judged record: other conversions of the same chip (independent noise, other
   phase), decoded with those weights. ENOB / SNDR / SFDR are taken there, so
   the fit cannot absorb the noise of the record it is judged on.

The weights can only correct the transfer if it has no gaps: every weight error
must stay inside the redundancy (:func:`cal_margin`).
"""

from __future__ import annotations

import contextlib
import io

import numpy as np


def weights(bits: np.ndarray, freq: float, nominal: np.ndarray) -> np.ndarray:
    """Calibrated output weights from a sine record (``freq`` = fin / fs), scaled to the nominal sum."""
    from adctoolbox import calibrate_weight_sine

    nominal = np.asarray(nominal, dtype=float)
    with contextlib.redirect_stdout(io.StringIO()):
        cal = calibrate_weight_sine(np.asarray(bits, dtype=float), freq=freq, nominal_weights=nominal)
    w = np.asarray(cal["weight"], dtype=float)
    return w * (nominal.sum() / w.sum())


def cal_margin(w_lsb: np.ndarray, w_nom: np.ndarray, sigma_lsb: np.ndarray, n_sigma: float) -> np.ndarray:
    """Redundancy left per decision (LSB) after the weight errors, worst case.

    ``w_lsb`` are the actual cap weights (decision order, LSB), ``w_nom`` the
    nominal ones and ``sigma_lsb`` the random (mismatch) sigma of each weight.
    Decision k has redundancy delta_k = sum_{i>k} w_i + 1 - w_k; the errors of
    its own weight and of all later weights can eat it: the worst case is
    |e_k| + sum_{i>k} |e_i| (systematic) + n_sigma * sqrt(sigma_k^2 + sum_{i>k} sigma_i^2).
    The last half step (output weight 1) absorbs up to 0.5 LSB, so
    margin_k = delta_k + 0.5 - worst case; a negative margin is a gap in the
    transfer that calibrated weights cannot close.
    """
    w_nom = np.asarray(w_nom, dtype=float)
    e = np.abs(np.asarray(w_lsb, dtype=float) - w_nom)
    s2 = np.asarray(sigma_lsb, dtype=float) ** 2
    tail = np.concatenate([np.cumsum(w_nom[::-1])[::-1][1:], [0.0]])
    delta = tail + 1.0 - w_nom
    e_tail = np.cumsum(e[::-1])[::-1]                  # |e_k| + sum_{i>k} |e_i|
    s_tail = np.sqrt(np.cumsum(s2[::-1])[::-1])
    return delta + 0.5 - (e_tail + n_sigma * s_tail)
