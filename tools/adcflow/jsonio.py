"""The text of a recorded result: ``json.dumps(doc, indent=1, default=float)``, with one line per pair for the SOA table.

Results are read by people in diffs and are limited to 1 MB each (candidates.MAX_JSON_BYTES). The
per-device SOA table (``metrics.soa_table``, soa.py) is by far their largest part, and ``indent=1`` would
put every number of it on a line of its own. Wherever a dict has a ``soa_table`` key, the lines of a packed
table (``devices`` and ``rows``, soa.pack_table) are therefore written one per line, each without spaces.
So is the list of dicts of a result recorded before the packed form when it has more than OLD_LINES_ABOVE
rows (the 4278-pair results of adc_sarlogic are laid out so); a shorter one is laid out as json.dumps does.
The rest of the document is exactly what json.dumps writes, so rewriting a result (rehash, rename,
remeasure ...) changes nothing else in it.
"""

from __future__ import annotations

import json

TABLE = "soa_table"
LINES = ("devices", "rows")                 # the lists of a packed table that go one item per line
OLD_LINES_ABOVE = 1000                      # rows of an old-form table above which it goes one row per line


def _compact(o) -> str:
    return json.dumps(o, separators=(",", ":"), default=float)


def _lines(items: list, ind: int) -> str:
    return "[\n" + ",\n".join(" " * (ind + 2) + _compact(x) for x in items) + "\n" + " " * ind + "]"


def _table(t, ind: int) -> str:
    """The soa_table value `t` of a key written at indent `ind`."""
    if isinstance(t, (list, tuple)):
        return _lines(t, ind)
    pad = " " * (ind + 2)
    items = [f"{pad}{json.dumps(k)}: " + (_lines(v, ind + 2) if k in LINES and isinstance(v, (list, tuple)) and v
                                         else _compact(v)) for k, v in t.items()]
    return "{\n" + ",\n".join(items) + "\n" + " " * ind + "}"


def _enc(o, ind: int, key=None) -> str:
    if key == TABLE and o and (isinstance(o, dict) or (isinstance(o, (list, tuple)) and len(o) > OLD_LINES_ABOVE)):
        return _table(o, ind)
    if isinstance(o, dict) and o:
        pad = " " * (ind + 1)
        return ("{\n" + ",\n".join(f"{pad}{json.dumps(k if isinstance(k, str) else str(k))}: {_enc(v, ind + 1, k)}"
                                   for k, v in o.items()) + "\n" + " " * ind + "}")
    if isinstance(o, (list, tuple)) and o:
        pad = " " * (ind + 1)
        return "[\n" + ",\n".join(pad + _enc(v, ind + 1) for v in o) + "\n" + " " * ind + "]"
    return json.dumps(o, default=float)    # a scalar or an empty container


def dumps(doc) -> str:
    """The text a result (or any record that carries a soa_table) is written as, without the final newline."""
    return _enc(doc, 0)
