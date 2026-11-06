"""adcflow: design, verification and sign-off tooling for the ADC-12b-100M project."""

import os
from pathlib import Path

# One BLAS thread unless the caller chose otherwise; set before anything imports numpy or scipy.
# OpenBLAS reserves a buffer per thread at import (about 620 MB for each of numpy's and scipy's copies
# on a 20-thread PC), and a `sim` / `verify` process holds that for hours while it waits on the server;
# its own numerics are small.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

REPO_ROOT = Path(__file__).resolve().parents[2]

__all__ = ["REPO_ROOT"]
