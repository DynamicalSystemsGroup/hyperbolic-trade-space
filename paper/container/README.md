# The pinned container (environment of record)

The Dockerfile at the repository root builds the environment in which the paper's committed
numbers and figures are produced. The platform of record is **linux/arm64** (ratified by the
supervisor: native on the author's machine; the spike is in
`docs/superpowers/notes/spike-container-platform/report.md`). Nothing is published to a registry.

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

## What is committed from the container

The committed exact values are the container's (the supervisor's decision recorded in
`work-packages/WP10-decisions.md`): the output cells of both notebooks, `paper/figures/`,
`paper/environment_reference.npz`, `tests/data/soft_fit_default_reference.npz` (with the field `recorded_on`, read by
`tests/test_soft_fit.py`) and `tests/data/v2_first_designs_of_record.csv` (the first 20 v2 designs, compared byte for byte
in the container only). To regenerate them, rebuild the image at the head that carries the code, run the commands under
"Run" for the notebooks, figures and reference arrays, and re-run in the image the test's own case list for the soft-fit
recording and its runner call for the 20 designs, with `docker create`, `docker cp` and `docker start` on `hts-` names.
`RECORD.md` lists what changed against the earlier (Mac) values and the tolerance of each.
