r"""WP23's data gate in the ledger: re-run the five entries that cite the model.

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

The five entries are one unit run in one tree, so each entry's ``git_dirty`` excludes the unit's
five outputs and the ledger (``runner.run`` excludes only the entry's own output: run that way, the
second entry onward would be marked dirty by the first's regenerated file; R-12 asks for none
dirty).

The WP23 close-out (``WP23-closeout-scope-of-work.md``, D-15) re-ran the same five entries (``@6``,
``scope-sensitivity-shared-subspace-v2@5``) on the model without the eclipse reserve and with the
supervisor's four thresholds, on the host under the supervisor's rule of 2026-11-10 ("The container
is a gate check, not a unit step", ``PM-BRIEF.md``): ``--host`` writes the close-out's note, which
names the platform (the entry's ``platform`` field records it too). At the close-out gate the
driver's container regression re-runs the same five entries in ``hts-paper`` (``@7``,
``scope-sensitivity-shared-subspace-v2@6``) and re-pins the exact outputs: ``--image`` writes the
gate's note naming the image. The data gate's note (the ``@5`` entries) stays as ``DATA_GATE_NOTE``.

WP26 (``WP26-decisions.md``, OD1 (b) as amended 2026-11-10, 15:05) re-runs the same five entries
in the container of record after the close-out gate's (``@8``,
``scope-sensitivity-shared-subspace-v2@7``), on edits to ``cubesat.sysml`` that leave every output
byte-identical (docs and comments read in a SysML v2 view editor, and WP23's O-1: the pointing
limit's primary share printed as 95.0 %): ``--image <id> --wp26`` writes its note; each output's
hash must equal the hash of the entry it supersedes, or the edits revert and the entries are not
kept. A host run (``--host --wp26``, in a throwaway tree) is the neutrality evidence before it.

WP30 (``WP30-decisions.md``, OD1 (a), OD2 (a), OD5 (b)) re-runs the same five entries twice. First
the regeneration (``--wp30 regen``, ``@9``, ``scope-sensitivity-shared-subspace-v2@8``): the
momentum headroom, the cost model and the two newly traded quantities add columns (``fleet_size``,
``momentum_headroom``, ``available_power_w`` (before, an auxiliary column),
``battery_peak_power_ratio``, ``unit_cost_usd``, ``fleet_cost_usd``), and each regime has 2,000
designs (the first 1,000 are the earlier sample), so the outputs move and nothing is required of
their hashes; the model already carries the supervisor's two cost limits (350,000 and 6,000,000
USD) and the restated launch budget, so this is the gate's regeneration. A later edit of a cost
limit or the launch budget is a verdict only (OD2 (a)) and moves no output: ``--wp30 values``
re-runs the five entries on the model with his values, against the new model hash, and requires
each output hash to equal the hash of the entry it supersedes (the WP26 rule, enforced: the script
exits 1 and names the entries when one differs, and the commit that edited the model is reverted).
Run on the host in a throwaway tree it is the neutrality evidence; run in ``hts-paper``
(``--image``) after a container regeneration it is the gate's closing proof.

    REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs \
        uv run python examples/adcs/model_v2/ledger_gate.py \
        (--image <image id> | --host) [--wp26 | --wp30 {regen,values}] [--dry]
"""

from __future__ import annotations

import argparse
import dataclasses
import platform
import sys

from experiments import definitions as df
from experiments import ledger as lg
from experiments import runner

DATA_GATE_NOTE = (  # the data gate's run (the @5 entries, 2026-11-10)
    "WP23 data gate: the WP23 model adopted as cubesat.sysml (the slew time out, every traded"
    " metric marked MoE or MoP and tied to a requirement, launch cost the MoE on the total mass);"
    " the settling time by event detection; regenerated in the container of record hts-paper"
    " (image {image})"
)
NOTE = (
    "WP23 close-out gate: the host run's entries (the eclipse reserve out of the model, eight"
    " traded metrics, the supervisor's four thresholds literal in budgets) re-run in the container"
    " of record hts-paper (image {image}) by the driver's container regression, which re-pins the"
    " exact outputs"
)
HOST_NOTE = (
    "WP23 close-out: the eclipse reserve out of the model (its requirement restated the"
    " depth-of-discharge requirement; eight traded metrics), the supervisor's four thresholds"
    " literal in budgets; regenerated on the host ({where}) under the rule that the container"
    " is a gate check; the container of record re-pins the exact outputs at the gate"
)
WP26_NOTE = (
    "WP26: edits to cubesat.sysml that leave every output byte-identical (docs and comments read"
    " in a SysML v2 view editor; WP23's O-1, the pointing limit's primary share 95.0 %);"
    " regenerated {where}; each output's hash equal to the hash of the entry it supersedes"
)
WP30_NOTE = (
    "WP30: the momentum headroom and the cost model (fleet size, unit cost, fleet cost) added to"
    " cubesat.sysml, thirteen traded metrics (the available power and the battery peak power ratio"
    " traded, so every requirement reads a traded metric), the two cost limits at the supervisor's"
    " values (350,000 and 6,000,000 USD; a verdict only, not a flag), 2,000 designs per regime;"
    " regenerated {where}; the container of record re-pins the exact outputs"
)
WP30_VALUES_NOTE = (
    "WP30: the supervisor's two cost limits and the restated launch budget set in cubesat.sysml"
    " (verdicts only, no output moves); regenerated {where}; each output's hash equal to the hash"
    " of the entry it supersedes"
)
ORDER = (
    *(df.EXPERIMENTS[k] for k in ("v2-primary", "v2-baseline")),
    *(df.EXPERIMENTS[k] for k in ("v2-check-predictions", "v2-check-designs")),
    df.SHARED_V2,
)


def declared(exp, entries, image: str | None, wp26: bool = False, wp30: str | None = None):
    """``exp`` as the gate's re-run of its current entry, the note naming the image (the gate) or
    the host's platform (the close-out, WP26's re-run with ``wp26``, or WP30's with ``wp30`` set to
    ``"regen"`` or ``"values"``; ``image`` None)."""
    run = df.revise(exp, entries)
    host = f"{platform.system()} {platform.machine()}"
    where = (
        f"in the container of record hts-paper (image {image})"
        if image
        else f"on the host ({host})"
    )
    if wp30 is not None:
        notes = {"regen": WP30_NOTE, "values": WP30_VALUES_NOTE}
        if wp30 not in notes:
            raise ValueError(f"wp30 is 'regen' or 'values', not {wp30!r}")
        note = notes[wp30].format(where=where)
    elif wp26:
        note = WP26_NOTE.format(where=where)
    elif image:
        note = NOTE.format(image=image)
    else:
        note = HOST_NOTE.format(where=host)
    return dataclasses.replace(run, inputs={**dict(run.inputs), "note": note})


def moved(prev: dict, entry: dict) -> bool:
    """Whether the new entry's output hash differs from the hash of the entry it supersedes."""
    return prev["output_sha256"] != entry["output_sha256"]


def run_one(run):
    """``runner.run`` for one declaration, the clean-tree rule over the unit's five outputs."""
    (cell,) = run.expand()
    if cell.id in {e["id"] for e in lg.read(lg.LEDGER_PATH)}:
        raise lg.LedgerError(f"entry {cell.id} exists; the ledger is append-only")
    own = [lg.LEDGER_PATH, *(lg.REPO_ROOT / e.output for e in ORDER)]
    return runner._run_cell(
        cell,
        df.resolve_oracle(run.oracle),
        df.resolve_sampler(run.sampler),
        lg.REPO_ROOT,
        lg.LEDGER_PATH,
        own,
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    where = ap.add_mutually_exclusive_group(required=True)
    where.add_argument("--image", help="the hts-paper image id the run is made in")
    where.add_argument("--host", action="store_true", help="the close-out's run on the host")
    kind = ap.add_mutually_exclusive_group()
    kind.add_argument("--wp26", action="store_true", help="WP26's re-run note")
    kind.add_argument(
        "--wp30",
        choices=("regen", "values"),
        help="WP30's regeneration note, or the values' note with hash equality required",
    )
    ap.add_argument("--dry", action="store_true", help="print the plan, run nothing")
    a = ap.parse_args(argv)
    differ = []
    for exp in ORDER:
        entries = lg.read(lg.LEDGER_PATH)
        prev = lg.latest(entries, exp.id)
        run = declared(exp, entries, a.image, a.wp26, a.wp30)
        print(run.id, "supersedes", list(run.supersedes), "output was", prev["output_sha256"][:12])
        if a.dry:
            continue
        entry = run_one(run)
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
        if a.wp30 == "values" and moved(prev, entry):
            differ.append(run.id)
    if differ:
        print("output hash differs from the superseded entry's:", *differ)
        print("the values are not neutral: revert the model edit and do not keep these entries")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
