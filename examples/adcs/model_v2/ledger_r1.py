"""WP22 round 1: regenerate the two v2 datasets from the r1 model and ledger the runs.

The r1 model (``cubesat_r1.sysml``) lives beside ``cubesat.sysml``. This script declares the two
datasets' experiments again with ``model_path`` set to the r1 model, under new ids
(``v2-primary-r1``, ``v2-baseline-r1``), and runs them into the same output paths: the outputs
are expected to be byte-identical to the committed ones (R-7), so the entries carry the same output
hashes as ``v2-primary@2`` and ``v2-baseline@2``. Nothing is superseded: the old entries stay
current and keep citing the old model until the recorded gate (R-14).

    PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_r1.py [--dry]
"""

from __future__ import annotations

import dataclasses
import sys

from experiments import definitions as df
from experiments import ledger as lg
from experiments import runner

R1_MODEL = "examples/adcs/model_v2/cubesat_r1.sysml"
NOTE = (
    "WP22 round 1: the r1 model (requirements over the metrics' own quantities); outputs unchanged"
)


def declared():
    out = []
    for base in ("v2-primary", "v2-baseline"):
        exp = df.EXPERIMENTS[base]
        out.append(
            dataclasses.replace(
                exp,
                id=f"{base}-r1",
                model_path=R1_MODEL,
                inputs={**dict(exp.inputs), "note": NOTE, "compares_with": f"{base}@2"},
            )
        )
    return out


def main(dry: bool = False) -> int:
    entries = lg.read(lg.LEDGER_PATH)
    for exp in declared():
        prev = lg.latest(entries, exp.id.removesuffix("-r1"))
        print(exp.id, "compares with", prev["id"], prev["output_sha256"][:12])
        if dry:
            continue
        (entry,) = runner.run(
            exp,
            df.resolve_oracle(exp.oracle),
            df.resolve_sampler(exp.sampler),
            lg.REPO_ROOT,
            lg.LEDGER_PATH,
        )
        same = entry["output_sha256"] == prev["output_sha256"]
        print(exp.id, entry["output_sha256"][:12], "identical to", prev["id"], same)
        if not same:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main("--dry" in sys.argv))
