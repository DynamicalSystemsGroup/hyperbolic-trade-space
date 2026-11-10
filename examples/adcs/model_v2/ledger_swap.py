r"""WP22d: the model swap in the ledger; re-run the five entries that cite the WP15 model.

At the recorded gate (``work-packages/WP22-decisions.md``) the WP22 model became
``cubesat.sysml``; the WP15 file it replaced stays in history only. Five current entries cited the
WP15 model's hash (``v2-primary@2``, ``v2-baseline@2``, ``v2-check-predictions@2``,
``v2-check-designs@2``, ``scope-sensitivity-shared-subspace-v2``), and two cited the WP22 model
under its round name (``v2-primary-r1@2``, ``v2-baseline-r1@2``, file ``cubesat_r1.sysml``). Each
of the five is re-run through the ledger's own re-run (``definitions.revise``: id ``<id>@<n>``,
superseding the current entry, parents re-pointed at the current parent entries); the primary and
baseline re-runs also supersede the two round entries, which carry the same outputs. Every output
is required byte-identical to the entry it supersedes (the gate's finding), so no data file moves.
Run again after the header comment was corrected (comment only): the same five, ``<id>@<n+1>``.

    REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs \
        uv run python examples/adcs/model_v2/ledger_swap.py [--dry]
"""

from __future__ import annotations

import dataclasses
import sys

from experiments import definitions as df
from experiments import ledger as lg
from experiments import runner

NOTE = (
    "WP22d: the model swap (cubesat.sysml is the WP22 model), then its header comment"
    " corrected (comment only); outputs unchanged"
)
# the round entries the primary and baseline re-runs also supersede (same outputs, renamed file)
ROUND = {"v2-primary": "v2-primary-r1", "v2-baseline": "v2-baseline-r1"}
ORDER = (
    *(df.EXPERIMENTS[k] for k in ("v2-primary", "v2-baseline")),
    *(df.EXPERIMENTS[k] for k in ("v2-check-predictions", "v2-check-designs")),
    df.SHARED_V2,
)


def declared(exp, entries):
    """``exp`` as the swap's re-run of its current entry (and of its round entry, if any)."""
    run = df.revise(exp, entries)
    gone = lg.superseded_by(entries)
    rnd = lg.latest(entries, ROUND[exp.id]) if exp.id in ROUND else None
    extra = [rnd["id"]] if rnd and rnd["id"] not in gone else []
    return dataclasses.replace(
        run,
        supersedes=(*run.supersedes, *extra),
        inputs={**dict(run.inputs), "note": NOTE},
    )


def main(dry: bool = False) -> int:
    for exp in ORDER:
        entries = lg.read(lg.LEDGER_PATH)
        prev = lg.latest(entries, exp.id)
        run = declared(exp, entries)
        print(run.id, "supersedes", list(run.supersedes), "output", prev["output_sha256"][:12])
        if dry:
            continue
        (entry,) = runner.run(
            run,
            df.resolve_oracle(run.oracle),
            df.resolve_sampler(run.sampler),
            lg.REPO_ROOT,
            lg.LEDGER_PATH,
        )
        same = entry["output_sha256"] == prev["output_sha256"]
        print(run.id, entry["model_sha256"][:12], entry["output_sha256"][:12], "identical", same)
        if not same:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main("--dry" in sys.argv))
