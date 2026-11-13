# The pinned container (environment of record)

The Dockerfile at the repository root builds the environment in which the paper's committed
numbers and figures are produced. The platform of record is **linux/arm64** (ratified by the
supervisor: native on the author's machine; the spike is in
`work-packages/spikes/spike-container-platform/report.md`). Nothing is published to a registry.

What is pinned: the base image by the digest of the multi-arch index of `python:3.12-slim` (Debian
trixie, Python 3.12.16), Node v24.22.2 by version, sha256 and release signature (arm64 tarball),
uv 0.9.18 (`UV_VERSION`), and every Python package by `uv.lock` through `uv sync --locked`. The
image sets `HTS_ENVIRONMENT_OF_RECORD=1`, so the tests assert the exact comparisons there.
`BASE_IMAGE`, `PLATFORM`, `NODE_ARCH`/`NODE_SHA256` and `OF_RECORD` are build arguments, so a
comparable image can be swapped in (robustness image `hts-alt`: Ubuntu 24.04, same lock; results in `RECORD.md`).

## Build

    sh paper/container/build.sh              # image hts-paper (commit first: HEAD goes in as a git bundle)
    sh paper/container/build.sh hts-alt      # robustness image

`build.sh` passes `git bundle` of HEAD as the named build context `history` (the context itself
excludes `.git`); the tests that read the git history then run inside the image. Without the bundle
(`docker build .`) the image still builds and those tests skip with a reason.

## Run (always without network)

    docker run --rm --network none hts-paper                                  # toolchain + derivation chain
    docker run --rm --network none hts-paper uv run python -m derivation.proofmap
    docker run --rm --network none hts-paper uv run pytest -q -n 4            # full suite

The full paper (execute both notebooks, then build the site; the MyST template and web libraries were
cached when the image was built). A named container lets you copy the regenerated files out:

    docker run --name hts-exec --network none hts-paper sh -c \
        "uv run python paper/paper_common.py && uv run python paper/execute_notebooks.py \
         && sh paper/container/build-paper.sh"
    docker cp hts-exec:/app/paper/paper.ipynb paper/paper.ipynb     # likewise supporting_material.ipynb,
    docker cp hts-exec:/app/paper/environment_reference.npz paper/    # paper/figures; then docker rm hts-exec

Outside this container, tied rows of gap G-10 may differ on other platforms; the values exact only
in the environment of record are listed in `paper/environment_values.toml`.

## The container is a gate check, not a unit step

Units run on the host and re-record only the reference arrays their change affects, marking each such file
"host-recorded, re-pin at the gate" in its commit message. The container run (this image and the alternative image
`hts-alt`) is dispatched by the driver at gates only: accepted packages, releases and corrections to published
material. At a gate every host-recorded reference is re-pinned from the container before the gate is called green,
and the ledger entries of record are the container's (`HTS_ENVIRONMENT_OF_RECORD=1` selects the exact branches of
the tests, which hold only there). A unit does not wait for the container.

## The five-entry ledger re-run in the image

The data gate's five ledger entries (`v2-primary`, `v2-baseline`, `v2-check-predictions`, `v2-check-designs`,
`scope-sensitivity-shared-subspace-v2`) are re-run in `hts-paper` by `examples/adcs/model_v2/ledger_gate.py --image <id>`, where
`<id>` is the image id (`docker images -q hts-paper`) that goes into each entry's note. Build the image first, from a committed
head, so that the model, the script and the ledger inside are the commit's. Use a named container so the outputs can be copied
out, with the environment variables the host run uses:

    docker create --name hts-gate-regression --network none -e REQUIRE_OPENSYSML=1 -e PYTHONPATH=examples/adcs \
        -e EXPERIMENTS_WORKERS=1 hts-paper sleep infinity
    docker start hts-gate-regression
    docker exec hts-gate-regression uv run python examples/adcs/model_v2/ledger_gate.py --image <id> --wp30 regen --dry
    docker exec hts-gate-regression uv run python examples/adcs/model_v2/ledger_gate.py --image <id> --wp30 regen

One worker: at 3,000 designs per regime the Docker VM's memory (7.7 GB on this Mac) does not hold three spawned oracle
workers, and the run takes about an hour (RECORD.md, the WP30 data gate). `--dry` prints the plan (each entry's new id, the entry it supersedes and that entry's output hash) and runs nothing. The run takes
the five entries in the script's order, one `runner` run each, appends five entries to `examples/adcs/experiments/ledger/ledger.jsonl`
and rewrites each entry's output file; every `git_dirty` must read False (the script excludes the unit's five outputs and the ledger from
the clean-tree check), so the tree inside must be clean before the run: remove anything copied in that git counts as untracked
(the `.claude/` lock directory). `--wp30 values` is the same re-run for the step that moves no output (the supervisor's cost limits): it
also exits 1 and names the entries when an output hash differs from the hash of the entry it supersedes, in which case the entries are not
kept. The earlier gates' notes are the other modes (`--wp26`; neither flag is the close-out's). Then copy the five outputs and the ledger out and
remove the container, by name:

    docker cp hts-gate-regression:/app/examples/adcs/experiments/ledger/ledger.jsonl examples/adcs/experiments/ledger/ledger.jsonl
    docker cp hts-gate-regression:/app/examples/adcs/data/v2/. examples/adcs/data/v2/
    docker cp hts-gate-regression:/app/examples/adcs/data/scope-sensitivity/. examples/adcs/data/scope-sensitivity/
    docker exec hts-gate-regression uv run python -m experiments verify    # 0 drifts
    docker rm -f hts-gate-regression

`RECORD.md` lists the entries, the image id and the wall time of each run.

## What is committed from the container

The committed exact values are the container's (the supervisor's decision recorded in
`work-packages/WP10-decisions.md`): the output cells of both notebooks, `paper/figures/`,
`paper/environment_reference.npz`, `tests/data/soft_fit_default_reference.npz` (with the field `recorded_on`, read by
`tests/test_soft_fit.py`) and `tests/data/v2_first_designs_of_record.csv` (the first 20 v2 designs, compared byte for byte
in the container only). To regenerate them, rebuild the image at the head that carries the code, run the commands under
"Run" for the notebooks, figures and reference arrays, and re-run in the image the test's own case list for the soft-fit
recording and its runner call for the 20 designs, with `docker create`, `docker cp` and `docker start` on `hts-` names.
`RECORD.md` lists what changed against the earlier (Mac) values and the tolerance of each.
