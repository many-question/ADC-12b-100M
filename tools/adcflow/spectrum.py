"""Sine-test spectrum metrics: ENOB, SNDR, SNR, THD from ADCToolbox, SFDR from adcflow (issue #36).

ADCToolbox 0.6.4 ``compute_spectrum`` finds the largest spur outside the signal bins but
then sums the spectrum over the spur bin +/- side_bin (``_harmonics._extract_highest_spur``).
For a spur next to the signal bins that window re-enters them: a -80 dBc tone two bins from
the fundamental reads as SFDR 7.8 dBc. It also searches bins 0 .. N/2 - 1 only, so a spur at
Nyquist is not seen. docs/sfdr-estimator.md has the comparison with the MATLAB ADCToolbox.

``sfdr_dbc`` therefore uses the definition of MATLAB ADCToolbox ``plotspec``: the power of the
fundamental's peak bin over the power of the largest single bin outside the signal bins and
DC, Nyquist included (and halved, as a one-sided boundary bin, so that it is a power). Both
peak bins carry the same window gain, so for coherent records this is the power ratio of the
two tones. The signal bins and the window are those of ``compute_spectrum`` (Hann; side_bin 1
for a coherent record), so SFDR, SNDR and THD describe the same signal.
"""

from __future__ import annotations

import numpy as np

ADCTOOLBOX = "0.6.4"            # the version the other metrics come from (pyproject.toml pins it)
ESTIMATOR = "adcflow.spectrum v1"
PROVENANCE = {"estimator": ESTIMATOR, "adctoolbox": ADCTOOLBOX,
              "sfdr": "plotspec definition: peak bin of the fundamental / largest other single bin "
                      "(DC and signal bins excluded, Nyquist included)",
              "enob_sndr_snr_thd": f"adctoolbox {ADCTOOLBOX} compute_spectrum"}


def hann(n: int) -> np.ndarray:
    """Periodic Hann window of n points, as compute_spectrum uses it (scipy hann(n, sym=False)).

    A coherent sine at bin k then occupies exactly bins k-1 .. k+1; the symmetric window
    (numpy.hanning) adds a skirt around it that is not in the record (#47)."""
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(n) / n)


def sfdr_dbc(data: np.ndarray, fundamental_bin: int, side_bin: int) -> tuple[float, int]:
    """SFDR (dBc) of a record and the bin of its largest spur.

    The record is mean-removed and Hann-windowed (periodic), as in compute_spectrum. Excluded
    from the spur search: the signal bins fundamental_bin +/- side_bin and the DC bins
    0 .. max(side_bin, 1) - 1. A spur adjacent to the signal bins is one bin, never a window
    that reaches into them; a real tone two bins away is found."""
    x = np.asarray(data, dtype=float).ravel()
    n = len(x)
    p = np.abs(np.fft.rfft((x - x.mean()) * hann(n))) ** 2
    if n % 2 == 0:
        p[-1] /= 2                                        # Nyquist: one-sided boundary bin
    sig = p[fundamental_bin]
    q = p.copy()
    q[max(fundamental_bin - side_bin, 0):fundamental_bin + side_bin + 1] = 0
    q[:max(side_bin, 1)] = 0
    k = int(np.argmax(q))
    return (float("inf") if q[k] <= 0 else float(10 * np.log10(sig / q[k]))), k


def analyze(codes: np.ndarray, fs: float, full_scale: float | None) -> dict:
    """compute_spectrum metrics (adctoolbox key names) with the SFDR of `sfdr_dbc`, plus
    'sfdr_dbc_adctoolbox' (the value it would have reported) and 'spur_bin'."""
    from adctoolbox.spectrum import compute_spectrum

    x = np.asarray(codes, dtype=float)
    r = compute_spectrum(x, fs=fs, max_scale_range=full_scale)
    pd = r["plot_data"]
    f = int(pd["fundamental_bin"])
    side = max(f - int(pd["sig_bin_start"]), int(pd["sig_bin_end"]) - f - 1)   # either edge may be clipped
    out = {k: float(v) for k, v in r["metrics"].items() if np.isscalar(v)}
    out["sfdr_dbc_adctoolbox"] = out["sfdr_dbc"]
    out["sfdr_dbc"], out["spur_bin"] = sfdr_dbc(x, f, side)
    return out
