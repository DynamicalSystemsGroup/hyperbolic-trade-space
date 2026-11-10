r"""WP16 Amendment 2, unit B: re-run the v2 entries once the crossing times are event-detected.

The oracle's settling and slew times are located by event detection (``cubesat_oracle``,
``crossing_times``) instead of being read off the accepted steps, so the five current entries
that hash ``cubesat_oracle.py`` are re-run through the ledger's own re-run
(``definitions.revise``: id ``<id>@<n>``, superseding the current entry, parents re-pointed at the
new parent entries), in the ledger's order: ``v2-primary``, ``v2-baseline``,
``v2-check-predictions`` (re-proposed from the new primary data), ``v2-check-designs``,
``scope-sensitivity-shared-subspace-v2``. The outputs change in the time columns and in what
depends on them; nothing is required identical.

Run inside the container of record, a clean checkout at the commit the image carries, with the
image recorded in each entry (``inputs.container``; the platform is recorded by the ledger)::

    docker run --name hts-wp16-gen --network none -e HTS_IMAGE=hts-wp16 \
        -e HTS_IMAGE_ID="$(docker image inspect hts-wp16 --format '{{.Id}}')" \
        -e REQUIRE_OPENSYSML=1 -e EXPERIMENTS_WORKERS=3 -e PYTHONPATH=examples/adcs \
        hts-wp16 uv run python examples/adcs/experiments/rerun_events.py

``--dry`` prints the ids it would write.
"""

from __future__ import annotations

import dataclasses
import os
import sys

from experiments import definitions as df
from experiments import ledger as lg
from experiments import runner

NOTE = (
    "WP16 Amendment 2: settling and slew times by event detection on the dense output "
    "(cubesat_oracle.crossing_times); every other quantity unchanged in kind"
)
ORDER = (
    *(df.EXPERIMENTS[k] for k in ("v2-primary", "v2-baseline")),
    *(df.EXPERIMENTS[k] for k in ("v2-check-predictions", "v2-check-designs")),
    df.SHARED_V2,
)


def container() -> dict:
    """The image the run is made in, from the environment (``HTS_IMAGE``, ``HTS_IMAGE_ID``)."""
    return {"image": os.environ.get("HTS_IMAGE"), "image_id": os.environ.get("HTS_IMAGE_ID")}


def declared(exp, entries):
    """``exp`` as the re-run of its current entry, with the note and the container."""
    run = df.revise(exp, entries)
    return dataclasses.replace(
        run, inputs={**dict(run.inputs), "note": NOTE, "container": container()}
    )


def main(dry: bool = False) -> int:
    if not dry and not all(container().values()):
        print("HTS_IMAGE and HTS_IMAGE_ID must name the image of the run")
        return 2
    for exp in ORDER:
        entries = lg.read(lg.LEDGER_PATH)
        prev = lg.latest(entries, exp.id)
        run = declared(exp, entries)
        print(run.id, "supersedes", list(run.supersedes), "was", prev["output_sha256"][:12])
        if dry:
            continue
        (entry,) = runner.run(
            run,
            df.resolve_oracle(run.oracle),
            df.resolve_sampler(run.sampler),
            lg.REPO_ROOT,
            lg.LEDGER_PATH,
        )
        print(run.id, entry["output_sha256"][:12], "dirty", entry["git_dirty"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main("--dry" in sys.argv))
