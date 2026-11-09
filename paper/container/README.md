# The pinned container (environment of record)

The Dockerfile at the repository root builds the environment in which the paper's committed
numbers and figures are produced. Nothing is published to a registry (supervisor, WP10 decisions:
documented here and in Appendix F; publishing later is optional and is on the release punch list).

What is pinned: the base image by the digest of its linux/amd64 manifest (tag
`python:3.12-slim`, Debian trixie, Python 3.12.16), uv 0.9.18 (the `UV_VERSION` build argument),
and every Python package by `uv.lock` through `uv sync --locked`. Platform of record: linux/amd64,
as in CI (ubuntu-24.04). Note: CI installs uv unpinned (`astral-sh/setup-uv@v7`); the lock file,
not uv, fixes the installed packages.

## Build

    docker build --platform linux/amd64 -t hts-paper .

## Run

Default command (prints the toolchain versions, then runs the derivation chain L1 to L14 and its
assumption audit):

    docker run --rm --platform linux/amd64 hts-paper

Any other command is passed through, prefixed by `uv run` for Python tools:

    docker run --rm --platform linux/amd64 hts-paper uv run pytest -q tests/test_derivation.py
    docker run --rm --platform linux/amd64 hts-paper uv run pytest -q     # the full test suite

The full paper (run the notebook cells and build the article; the commands of Appendix F are the
authority for the row-by-row reproduction):

    docker run --rm --platform linux/amd64 -v "$PWD/_out:/app/_out" hts-paper \
        sh -c "uv run myst build --html paper/ && cp -r paper/_build /app/_out/"

(adjust to the paper's build command once `myst.yml` is final; the pinned environment is the
same.) To keep outputs, mount a host directory as above.

On Apple silicon, Colima runs linux/amd64 by emulation: slower than native, but workable (see
`RECORD.md`). Outside this container, tied rows of gap G-10 may differ on other platforms.
