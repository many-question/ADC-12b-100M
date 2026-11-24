"""RNL viewer manifests (format 1): the design as the viewer's library, one manifest per netlist.

The hosted viewer opens `?manifest=<address>`: it fetches every listed file from `base` (or the
file's own `url`), checks its SHA-256 and size, keeps the files in the library with their
directories, and opens `entry`. The relative `@USE-PACKAGE(path=...)` includes and the project's
package files (`design/rnl/adc28.rnl` and the generated block and Verilog-A symbol files) are then
all in the viewer's pool, so a netlist draws with its symbols the same way wherever it is opened.

Format and limits: apps/web/README.md of https://github.com/rich-netlist/rnl ("External manifests").

Versions: the hosted viewer at VIEWER reads RNL 0.4 only; RNL 0.3 files open in the frozen VIEWERS["0.3"]
(same query and postMessage protocol, same origin). Each netlist opens in the viewer of its own
`@VERSION`, and a manifest lists only the files its entry's viewer can read: those of the entry's
version and files without RNL (Verilog-A). In a hierarchy that mixes versions (a 0.4 candidate under
the 0.3 top) the entry decides, and the parts in the other version are not in its manifest.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from .data import ROOT

ID = "adc-12b-100m"
POOL = ["design/rnl/adc28.rnl", "design/rnl/adc28_blocks.rnl", "design/rnl/adc28_va.rnl",      # RNL 0.3
        "design/rnl/0.4/adc28.rnl", "design/rnl/0.4/adc28_blocks.rnl", "design/rnl/0.4/adc28_va.rnl"]   # RNL 0.4
MAX_FILES, MAX_FILE_BYTES, MAX_BYTES = 300, 2 * 1024 * 1024, 20 * 1024 * 1024     # the viewer's limits
PUBLISH = {"design": {".scs", ".rnl", ".va", ".vams"}, "tb": {".scs", ".va", ".vams"}}
VIEWER = "https://rich-netlist.github.io/rnl/viewer/"                      # the current viewer: RNL 0.4
VIEWERS = {"0.3": "https://rich-netlist.github.io/rnl/viewer-0.3/"}       # frozen viewers of older versions
_VERSION = re.compile(rb'@VERSION\(\s*"([0-9]+\.[0-9]+)"\s*\)')


def rnl_version(data: bytes) -> str | None:
    """The RNL version a file declares (its header's @VERSION), None for a file without one (Verilog-A)."""
    m = _VERSION.search(data)
    return m.group(1).decode() if m else None


def viewer_for(version: str | None) -> str:
    """The hosted viewer that reads RNL `version`; the current one for 0.4, a newer or an undeclared version
    (an undeclared one is the current language, as for `adcflow check rnl`: checks.RNL_CURRENT)."""
    return VIEWERS.get(version or "", VIEWER)


def readable(files: list[dict], version: str | None) -> list[dict]:
    """The files a manifest of an entry in RNL `version` lists: that version's, and those without RNL."""
    return [f for f in files if f.get("version") in (None, version)]


def netlist_files() -> list[str]:
    """Repository-relative paths of the published design files, sorted."""
    return sorted(f.relative_to(ROOT).as_posix() for top, suffixes in PUBLISH.items()
                  for f in (ROOT / top).rglob("*") if f.is_file() and f.suffix in suffixes)


def name_of(rel: str) -> str:
    """File name of the manifest whose entry is the netlist `rel`: design/top/adc_top.scs -> design-top-adc_top."""
    return rel.rsplit(".", 1)[0].replace("/", "-")


def _blob(commit: str, rel: str) -> bytes | None:
    """The bytes git has for `rel` at `commit`: what raw.githubusercontent.com serves, whatever the checkout's line ends."""
    if not commit:
        return None
    p = subprocess.run(["git", "show", f"{commit}:{rel}"], cwd=ROOT, capture_output=True)
    return p.stdout if p.returncode == 0 else None


def file_entries(commit: str, from_git: bool) -> list[dict]:
    """path, sha256 and size of every published file; `from_git` hashes the committed bytes (files served from raw)."""
    out = []
    for rel in netlist_files():
        data = (_blob(commit, rel) if from_git else None)
        if data is None:
            data = (ROOT / rel).read_bytes()
        out.append(entry(rel, data))
    return out


def entry(rel: str, data: bytes) -> dict:
    """A file of a manifest; `version` (rnl_version) only chooses the files and is not written (manifest)."""
    return {"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "version": rnl_version(data)}


def check_limits(files: list[dict]) -> list[str]:
    problems = []
    if len(files) > MAX_FILES:
        problems.append(f"manifest: {len(files)} files, the viewer takes at most {MAX_FILES}")
    for f in files:
        if f["size"] > MAX_FILE_BYTES:
            problems.append(f"manifest: {f['path']} has {f['size']} bytes, the viewer takes at most {MAX_FILE_BYTES} per file")
    if sum(f["size"] for f in files) > MAX_BYTES:
        problems.append(f"manifest: the files hold more than {MAX_BYTES} bytes in all")
    return problems


def manifest(entry: str, files: list[dict], base: str, repo: str, commit: str, level: str | None = None) -> dict:
    """The manifest of `entry`: only the files of its RNL version (readable), with its pool among them."""
    version = next((f.get("version") for f in files if f["path"] == entry), None)
    files = readable(files, version)
    have = {f["path"] for f in files}
    owner = repo.split("/")[0] if repo else ""
    doc: dict = {
        "format": 1,
        "id": ID,
        "title": {"en": f"ADC-12b-100M · {Path(entry).stem}", "zh": f"ADC-12b-100M · {Path(entry).stem}"},
        "description": "12-bit-class 100 MS/s asynchronous SAR ADC: Spectre netlists with RNL schematics",
    }
    if owner:
        doc["author"] = [{"name": owner, "url": f"https://github.com/{owner}"}]
    if repo and commit:
        doc["source"] = {"repo": repo, "commit": commit, "url": f"https://github.com/{repo}/tree/{commit}/design"}
    doc.update({"base": base, "entry": entry, "files": [{k: f[k] for k in ("path", "sha256", "size")} for f in files],
                "pool": [p for p in POOL if p in have]})
    if level:
        doc["level"] = level
    return doc


def write_all(out: Path, entries: list[tuple[str, str | None]], files: list[dict], base: str, repo: str, commit: str) -> list[str]:
    """Write manifests/<name>.json for every (entry, level); returns problems."""
    problems = check_limits(files)
    have = {f["path"] for f in files}
    for rel, level in entries:
        if rel not in have:
            problems.append(f"manifest: entry {rel} is not a published file")
            continue
        dst = out / "manifests" / f"{name_of(rel)}.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(manifest(rel, files, base, repo, commit, level), indent=1, ensure_ascii=False) + "\n",
                       encoding="utf-8", newline="\n")
    return problems
