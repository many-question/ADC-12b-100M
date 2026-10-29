"""Command line entry: ``python -m adcflow <command>``."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="adcflow")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("budget", help="print the architecture noise / timing budget tables")
    sub.add_parser("arch", help="print derived architecture numbers")

    c = sub.add_parser("corners", help="list the PVT corners of a set")
    c.add_argument("set", nargs="?", default="all")

    g = sub.add_parser("gen", help="regenerate files derived from specs/")
    g.add_argument("what", choices=["rnl", "va-params", "top", "tb", "docs", "all"], nargs="?", default="all")
    g.add_argument("--check", action="store_true", help="fail if a generated file is out of date")

    k = sub.add_parser("check", help="CI checks")
    k.add_argument("what", choices=["ports", "rnl", "results", "hygiene", "candidates", "all"], nargs="?", default="all")
    k.add_argument("--strict", action="store_true", help="results: require sign-off evidence for signoff blocks")
    k.add_argument("--base", help="candidates: git ref of the pull request base")
    k.add_argument("--author", help="candidates: GitHub login of the pull request author")

    s = sub.add_parser("sim", help="run a block test on the simulation server")
    s.add_argument("test", help="test id, e.g. tb_comp_delay")
    s.add_argument("--block", help="block that owns the test (default: searched)")
    s.add_argument("--corners", default="typ", help="corner set or comma list")
    s.add_argument("--view", action="append", default=[],
                   help="block=view override: behav (default), xtor (the selected candidate) or xtor:<candidate>, "
                        "e.g. adc_comp=xtor:alice")
    s.add_argument("--param", action="append", default=[], help="tb parameter override name=value")
    s.add_argument("--mode", default="aps",
                   help="spectre mode: spectre aps cx ax mx (default aps; ax/mx lose accuracy with the Verilog-A views)")
    s.add_argument("--jobs", type=int, default=6)
    s.add_argument("--keep", action="store_true", help="keep the remote run directory")
    s.add_argument("--no-record", action="store_true", help="do not write results/")
    s.add_argument("--dry-run", action="store_true", help="only build the run deck locally")
    s.add_argument("--mc-runs", type=int,
                   help="Monte Carlo test (`montecarlo:` in its spec, e.g. tb_comp_offset_mc): number of samples "
                        "instead of the spec's (fewer than a spec's mc: fail it; for a quick check)")
    s.add_argument("--mc-seed", type=int, help="Monte Carlo test: seed instead of the spec's")
    s.add_argument("--crosscheck", action="store_true",
                   help="also run every job with the test's `crosscheck:` numerical settings and record "
                        "the differences in meta.crosscheck (docs/verification.md section 2)")

    cd = sub.add_parser("candidates", help="leaderboard of the transistor-level candidates (scores from results)")
    cd.add_argument("--block")
    cd.add_argument("--json", action="store_true", help="structured data (as the site uses it)")
    cd.add_argument("--withdrawn", action="store_true", help="also list withdrawn candidates")

    mg = sub.add_parser("migrate-candidate", help="move the legacy view design/xtor/<block>/ and its xtor results "
                                                  "into a named candidate")
    mg.add_argument("block")
    mg.add_argument("name")
    mg.add_argument("--author", action="append", default=[], required=True,
                    help="login or login=display name (repeat for co-authors)")
    mg.add_argument("--description", required=True)
    mg.add_argument("--dry-run", action="store_true")

    rm = sub.add_parser("remeasure", help="measure the fetched jobs of an earlier run again (no simulation) "
                                          "and re-record their results")
    rm.add_argument("test")
    rm.add_argument("--run", required=True, help="the run directory (build/runs/<run id>) with the fetched jobs")
    rm.add_argument("--block")
    rm.add_argument("--view", action="append", default=[], help="block=view, as for sim")
    rm.add_argument("--allow", action="append", default=[],
                    help="metric-name part that may change (default: sfdr); any other change aborts")
    rm.add_argument("--dry-run", action="store_true", help="only print old -> new")
    rm.add_argument("--redraw", action="store_true",
                    help="figures only: every metric must come out as recorded (meta.redrawn)")

    rh = sub.add_parser("rehash", help="record, without simulating, only what each result's circuit depends on "
                                       "(the files its testbench reaches, the arch.yaml values it read); "
                                       "a result whose dependencies changed stays stale")
    rh.add_argument("--block")
    rh.add_argument("--test")
    rh.add_argument("--view", help="result directory, e.g. behav or xtor-alice")
    rh.add_argument("--dry-run", action="store_true", help="only report what would be rehashed")
    rh.add_argument("-v", "--verbose", action="store_true", help="list every result, not only the stale ones")

    r = sub.add_parser("report", help="summarise recorded results against specs")
    r.add_argument("--block")

    cl = sub.add_parser("clean-remote", help="delete this project's run directories on the server")
    cl.add_argument("--older-than-h", type=float, default=0.0)

    a = p.parse_args(argv)

    if a.cmd == "budget":
        from .budget import main as budget_main
        budget_main()
    elif a.cmd == "arch":
        from .arch import Arch
        for key, val in Arch.load().summary().items():
            print(f"{key}: {val}")
    elif a.cmd == "corners":
        from .corners import corner_set
        for cn in corner_set(a.set):
            print(cn.name)
    elif a.cmd == "gen":
        from .gen import generate
        return generate(a.what, check=a.check)
    elif a.cmd == "check":
        from .checks import run_checks
        return run_checks(a.what, strict=a.strict, base=a.base, author=a.author)
    elif a.cmd == "sim":
        from .runner import run_test_cli
        return run_test_cli(a)
    elif a.cmd == "candidates":
        import json

        from .candidates import leaderboard, table
        rows = leaderboard(a.block, a.withdrawn)
        print(json.dumps(rows, indent=1, default=float) if a.json else table(rows))
    elif a.cmd == "migrate-candidate":
        from .candidates import migrate
        authors = [dict(zip(("github", "name"), x.split("=", 1))) for x in a.author]
        for line in migrate(a.block, a.name, authors, a.description, a.dry_run):
            print(("would move " if a.dry_run else "") + line)
        if not a.dry_run:
            print(f"next: in specs/blocks/{a.block}.yaml replace views.xtor by `selected: none` or `selected: {a.name}`")
    elif a.cmd == "remeasure":
        from pathlib import Path

        from .runner import remeasure
        remeasure(a.test, Path(a.run), a.block, dict(v.split("=", 1) for v in a.view),
                  tuple(a.allow) or ("sfdr",), a.dry_run, a.redraw)
    elif a.cmd == "rehash":
        from .deps import rehash
        rehash(a.block, a.test, a.view, a.dry_run, a.verbose)
    elif a.cmd == "report":
        from .results import report
        return report(a.block)
    elif a.cmd == "clean-remote":
        from .remote import clean_remote
        return clean_remote(a.older_than_h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
