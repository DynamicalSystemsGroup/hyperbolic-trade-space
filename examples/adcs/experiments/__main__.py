"""Command line: ``run <id>``, ``verify``, ``adopt``, ``compare``.

From the repository root::

    PYTHONPATH=examples/adcs uv run python -m experiments verify

(under pytest the ``examples/adcs`` path comes from ``pythonpath`` in ``pyproject.toml``).
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from . import definitions as df
from . import ledger as lg
from . import runner


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="experiments", description=__doc__.splitlines()[0])
    p.add_argument("--root", type=Path, default=lg.REPO_ROOT)
    p.add_argument("--ledger", type=Path, default=lg.LEDGER_PATH)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run a declared experiment by id")
    r.add_argument("id")
    sub.add_parser("verify", help="recompute every ledger hash; exit 1 on drift")
    sub.add_parser("adopt", help="register the frozen datasets (no regeneration)")
    c = sub.add_parser("compare", help="v1-v2 comparison report (experiments.compare)")
    c.add_argument("rest", nargs=argparse.REMAINDER)
    a = p.parse_args(argv)

    if a.cmd == "verify":
        drifts = lg.verify(a.ledger, a.root)
        for d in drifts:
            print(d)
        print(f"{len(lg.read(a.ledger))} entries; {len(drifts)} drifts")
        return 1 if drifts else 0
    if a.cmd == "adopt":
        added = runner.adopt(df.FROZEN, a.root, a.ledger)
        print(f"adopted {len(added)} entries: {[e['id'] for e in added]}")
        return 0
    if a.cmd == "run":
        exp = df.EXPERIMENTS.get(a.id)
        if exp is None:
            print(f"unknown experiment {a.id!r}; known: {sorted(df.EXPERIMENTS)}")
            return 2
        entries = runner.run(
            exp,
            df.resolve_oracle(exp.oracle),
            df.resolve_sampler(exp.sampler),
            a.root,
            a.ledger,
        )
        print(f"ran {[e['id'] for e in entries]}")
        return 0
    try:
        mod = importlib.import_module("experiments.compare")
    except ModuleNotFoundError:
        print("experiments.compare is not present yet (part 15.4 writes it)")
        return 2
    return int(mod.main(a.rest) or 0)


if __name__ == "__main__":
    sys.exit(main())
