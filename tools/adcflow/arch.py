"""Architecture parameters (specs/arch.yaml) and the quantities derived from them.

`Arch.load()` gives a read-tracked view of the file: inside ``with track() as keys`` every key
read is added to `keys` as a dotted path (``timing.t_dac_add``; ``*`` = the whole file). The
runner records the keys a run read, and a hash of their values (`values_sha`), as the arch
values its result depends on (deps.py).
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import numpy as np
import yaml

from . import REPO_ROOT

ARCH_YAML = REPO_ROOT / "specs" / "arch.yaml"

K_BOLTZMANN = 1.380649e-23

WHOLE = "*"                    # key path of the whole file
_LOGS: list[set[str]] = []     # the key sets of the active track() blocks


@contextmanager
def track():
    """Collect the key paths of arch.yaml read inside the block (nested blocks all collect)."""
    keys: set[str] = set()
    _LOGS.append(keys)
    try:
        yield keys
    finally:
        _LOGS.remove(keys)


def _log(path: str) -> None:
    for keys in _LOGS:
        keys.add(path)


class _Tracked(Mapping):
    """Read-only view of a mapping of arch.yaml that logs what is read: every leaf value and every
    missing key (``.get`` with a default reads one too) by its path; listing the keys or copying
    logs the whole mapping. Nested mappings are views as well."""

    __slots__ = ("_data", "_path", "_kids")

    def __init__(self, data: dict, path: str = ""):
        self._data, self._path, self._kids = data, path, {}

    def __getitem__(self, k):
        p = f"{self._path}.{k}" if self._path else str(k)
        if k not in self._data:
            _log(p)
            raise KeyError(k)
        v = self._data[k]
        if isinstance(v, dict):
            if k not in self._kids:
                self._kids[k] = _Tracked(v, p)
            return self._kids[k]
        _log(p)
        return v

    def __iter__(self):
        _log(self._path or WHOLE)
        return iter(self._data)

    def __len__(self) -> int:
        _log(self._path or WHOLE)
        return len(self._data)

    def __deepcopy__(self, memo) -> dict:
        _log(self._path or WHOLE)
        return copy.deepcopy(self._data, memo)

    def __repr__(self) -> str:
        return f"_Tracked({self._path or WHOLE})"


def minimal(keys) -> list[str]:
    """Sorted key paths without those under another one of the set (``*`` covers all)."""
    keys = set(keys)
    if WHOLE in keys:
        return [WHOLE]
    return sorted(k for k in keys if not any(k.startswith(o + ".") for o in keys if o != k))


_ABSENT = {"absent": True}


def value_at(data: dict, key: str):
    """The value of a key path in the plain data of arch.yaml (a marker when it is absent)."""
    if key == WHOLE:
        return {"value": data}
    cur = data
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return _ABSENT
        cur = cur[part]
    return {"value": cur}


def values_sha(data: dict, keys) -> str:
    """Hash of the values of `keys` in the plain data of arch.yaml (formatting and comments do not count)."""
    vals = {k: value_at(data, k) for k in minimal(keys)}
    return hashlib.sha256(json.dumps(vals, sort_keys=True, default=repr).encode()).hexdigest()[:16]


def load_data(path: Path | str = ARCH_YAML) -> dict:
    """The plain (untracked) data of arch.yaml."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


@dataclass(frozen=True)
class Arch:
    raw: dict

    @classmethod
    def load(cls, path: Path | str = ARCH_YAML) -> "Arch":
        return cls(_Tracked(load_data(path)))

    # --- basic parameters -------------------------------------------------
    @property
    def fs(self) -> float:
        return float(self.raw["timing"]["fs"])

    @property
    def vref(self) -> float:
        return float(self.raw["reference"]["vref"])

    @property
    def cu(self) -> float:
        return float(self.raw["cdac"]["cu"])

    @cached_property
    def w(self) -> np.ndarray:
        """CDAC weights in decision order (cap index 12 .. 0)."""
        return np.asarray(self.raw["cdac"]["cap_weights"], dtype=float)

    @cached_property
    def sampled(self) -> np.ndarray:
        return np.asarray(self.raw["cdac"]["cap_sampled"], dtype=bool)

    @cached_property
    def out_weights(self) -> np.ndarray:
        return np.asarray(self.raw["conversion"]["out_weights"], dtype=float)

    @property
    def n_dec(self) -> int:
        return int(self.raw["conversion"]["n_decisions"])

    # --- derived ----------------------------------------------------------
    @cached_property
    def t_dac_add(self) -> np.ndarray:
        """Extra DAC wait (s, TT) after the DAC step of decision 1 .. n_dec - 1 (timing.t_dac_add)."""
        add = np.zeros(self.n_dec - 1)
        v = np.asarray(self.raw["timing"].get("t_dac_add", []), dtype=float)
        add[:v.size] = v
        return add

    @property
    def sigma_cu(self) -> float:
        """Relative random mismatch of one unit cap cu (Pelgrom scaling from the 1 fF value)."""
        return float(self.raw["cdac"].get("mismatch_sigma_1f", 0.0)) * float(np.sqrt(1e-15 / self.cu))

    def sigma_w_lsb(self) -> np.ndarray:
        """Random mismatch sigma (LSB) of each weight's step, decision order: sigma_cu * sqrt(w)."""
        return self.sigma_cu * np.sqrt(self.w)

    @property
    def c_dac(self) -> float:
        """Total switched DAC capacitance per side."""
        return float(self.w.sum() * self.cu)

    @property
    def c_s(self) -> float:
        """Sampling capacitance per side (caps whose bottom plate tracks VIN)."""
        return float(self.w[self.sampled].sum() * self.cu)

    @property
    def c_p(self) -> float:
        return float(self.raw["cdac"]["cp_top_ratio"]) * self.c_dac

    @property
    def c_tot(self) -> float:
        return self.c_dac + self.c_p

    @property
    def lsb(self) -> float:
        """Input-referred differential LSB = weight-1 step of the code."""
        return self.vref * self.cu / self.c_s

    @property
    def n_codes(self) -> int:
        return int(self.out_weights.sum()) + 1

    @property
    def fs_peak(self) -> float:
        """Differential full-scale peak (V): +/- (sum(w) + 1/2) LSB."""
        return (self.w.sum() + 0.5) * self.lsb

    @property
    def code_offset(self) -> float:
        """code - code_offset = signed DAC level in LSB."""
        return float(self.w.sum() + 0.5)

    @property
    def gain_top(self) -> float:
        """Input-to-top-plate attenuation C_S / C_tot."""
        return self.c_s / self.c_tot

    def redundancy(self) -> np.ndarray:
        """Decision-error tolerance (LSB, input referred) of decisions 1..13."""
        w = self.w
        tail = np.concatenate([np.cumsum(w[::-1])[::-1][1:], [0.0]])
        return tail + 1.0 - w

    def ktc_noise(self, temp_c: float = 27.0) -> float:
        """Input-referred differential sampled kT/C noise (V rms).

        Bottom-plate sampling: the top node freezes kT*C_tot of charge noise;
        referred to the input through C_S per side, doubled for the two sides.
        """
        kt = K_BOLTZMANN * (temp_c + 273.15)
        return float(np.sqrt(2.0 * kt * self.c_tot / self.c_s**2))

    def summary(self) -> dict:
        return {
            "C_S_per_side_pF": self.c_s * 1e12,
            "C_DAC_per_side_pF": self.c_dac * 1e12,
            "C_tot_per_side_pF": self.c_tot * 1e12,
            "LSB_uV": self.lsb * 1e6,
            "FS_peak_diff_V": self.fs_peak,
            "levels": self.n_codes,
            "bits_equiv": float(np.log2(self.n_codes)),
            "top_gain": self.gain_top,
            "redundancy_LSB": self.redundancy().tolist(),
            "kTC_noise_27C_uV": self.ktc_noise(27) * 1e6,
            "kTC_noise_125C_uV": self.ktc_noise(125) * 1e6,
        }


def decode(bits: np.ndarray, arch: Arch | None = None, weights=None) -> np.ndarray:
    """Raw bits (N x 14, MSB first) -> unsigned code using output weights."""
    if weights is None:
        weights = (arch or Arch.load()).out_weights
    bits = np.asarray(bits, dtype=float)
    return bits @ np.asarray(weights, dtype=float)


def code_to_volts(code: np.ndarray, arch: Arch) -> np.ndarray:
    """Unsigned code -> differential input voltage estimate."""
    return (np.asarray(code, dtype=float) - arch.code_offset) * arch.lsb
