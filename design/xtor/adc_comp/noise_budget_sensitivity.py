"""Reproduce the noise-only system-model allocation study without editing specs.

Run from the repository root with adcflow installed. Output is written to the
ignored build directory; the checked-in JSON is the reviewed study snapshot.
"""
from pathlib import Path
import contextlib
import hashlib
import io
import json
import numpy as np
from adcflow import REPO_ROOT, model
from adcflow.arch import Arch


def main():
    arch = Arch.load()
    rows = []
    for sigma in (80, 160, 180, 200, 230, 260, 300):
        runs = []
        for seed in (11, 12, 13):
            ni = model.NonIdeal(temp_c=125, sigma_cmp_top=sigma * 1e-6, seed=seed)
            with contextlib.redirect_stdout(io.StringIO()):
                result, _, fin = model.sine_test(arch, ni, n_fft=4096, fin_target=49.9e6)
                met = model.spectrum_metrics(result.codes, arch.fs, arch.n_codes)
            runs.append({"seed": seed, "enob": float(met["enob"]),
                         "sndr_dbc": float(met["sndr_dbc"]),
                         "incomplete": int(result.incomplete.sum())})
        enob = [r["enob"] for r in runs]
        rows.append({"sigma_cmp_top_uV": sigma, "fin_Hz": float(fin), "n_fft": 4096,
                     "temp_c": 125, "enob_min": min(enob), "enob_mean": float(np.mean(enob)),
                     "enob_max": max(enob), "runs": runs})
    data = {
        "description": "System-model noise-only sensitivity; other budgets and timing unchanged. "
                       "Not transistor-level top verification.",
        "rows": rows,
        "provenance": {
            "model_sha256": hashlib.sha256((REPO_ROOT / "tools/adcflow/model.py").read_bytes()).hexdigest(),
            "architecture_sha256": hashlib.sha256((REPO_ROOT / "specs/arch.yaml").read_bytes()).hexdigest(),
        },
    }
    output = REPO_ROOT / "build/experiments/noise-budget-sensitivity-reproduced.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(output.relative_to(REPO_ROOT))


if __name__ == "__main__":
    main()
