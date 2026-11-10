r"""WP23's data gate in the ledger: re-run the five entries that cite the model, in the container.

At the recorded gate (``work-packages/WP23-decisions.md``) the WP23 model became ``cubesat.sysml``;
the WP22 version it replaced stays in history only (d3018ba). Five current entries cited the WP22
model's hash (``v2-primary@4``, ``v2-baseline@4``, ``v2-check-predictions@4``,
``v2-check-designs@4``, ``scope-sensitivity-shared-subspace-v2@3``). Each is re-run through the
ledger's own re-run (``definitions.revise``: id ``<id>@<n>``, superseding the current entry,
parents re-pointed at the current parent entries) inside the container of record ``hts-paper``,
whose image id goes into the entry's note with the gate. Unlike WP22d's swap (``ledger_swap.py``,
in history), the outputs move: the slew-time columns leave (WP23 G5) and the settling time is read
by event detection (WP16 Amendment 2 D-7), so the script prints each output hash, old and new,
and requires nothing of them; the comparison of old and new is the gate's report (WP23 D-9).

    REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs \
        uv run python examples/adcs/model_v2/ledger_gate.py --image <image id> [--dry]
"""

from __future__ import annotations

import argparse
import dataclasses
import sys

from experiments import definitions as df
from experiments import ledger as lg
from experiments import runner

NOTE = (
    "WP23 data gate: the WP23 model adopted as cubesat.sysml (the slew time out, every traded"
    " metric marked MoE or MoP and tied to a requirement, launch cost the MoE on the total mass);"
    " the settling time by event detection; regenerated in the container of record hts-paper"
    " (image {image})"
)
ORDER = (
    *(df.EXPERIMENTS[k] for k in ("v2-primary", "v2-baseline")),
    *(df.EXPERIMENTS[k] for k in ("v2-check-predictions", "v2-check-designs")),
    df.SHARED_V2,
)


def declared(exp, entries, image: str):
    """``exp`` as the gate's re-run of its current entry, the note naming the image."""
    run = df.revise(exp, entries)
    return dataclasses.replace(run, inputs={**dict(run.inputs), "note": NOTE.format(image=image)})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--image", required=True, help="the hts-paper image id the run is made in")
    ap.add_argument("--dry", action="store_true", help="print the plan, run nothing")
    a = ap.parse_args(argv)
    for exp in ORDER:
        entries = lg.read(lg.LEDGER_PATH)
        prev = lg.latest(entries, exp.id)
        run = declared(exp, entries, a.image)
        print(run.id, "supersedes", list(run.supersedes), "output was", prev["output_sha256"][:12])
        if a.dry:
            continue
        (entry,) = runner.run(
            run,
            df.resolve_oracle(run.oracle),
            df.resolve_sampler(run.sampler),
            lg.REPO_ROOT,
            lg.LEDGER_PATH,
        )
        print(
            run.id,
            "model",
            entry["model_sha256"][:12],
            "output",
            entry["output_sha256"][:12],
            "dirty",
            entry["git_dirty"],
            "rows",
            entry["output_rows"],
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
