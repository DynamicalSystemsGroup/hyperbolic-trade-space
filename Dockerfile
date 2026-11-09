# Environment of record for the paper (WP10, Amendment 1, D-13 / R-31).
#
# Base: python:3.12-slim (Debian trixie), pinned by the DIGEST of its linux/amd64 manifest
# (resolved 2026-11-08 with `docker buildx imagetools inspect python:3.12-slim`; tag at
# resolution: 3.12-slim = 3.12.16-slim-trixie; the multi-arch index digest was
# sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b). The tag is kept
# for readers only; the digest is what is pulled. Platform of record: linux/amd64 (matches CI).
#
# Build:  docker build --platform linux/amd64 -t hts-paper .
# Run:    docker run --rm --platform linux/amd64 hts-paper            (toolchain + derivation)
#         docker run --rm --platform linux/amd64 hts-paper uv run pytest -q    (full test suite)
# See paper/container/README.md for the full-paper commands and paper/container/RECORD.md for
# the recorded local run. Nothing is published to a registry.
ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} python:3.12-slim@sha256:05a994d2344eb364cc186910f4fc8786a38215f39f00d0acc25bff33a08f4177

# uv version: the one the record was made with. CI installs astral-sh/setup-uv@v7 without a
# version (latest); the locked environment, not uv, determines the installed packages.
ARG UV_VERSION=0.9.18
RUN pip install --no-cache-dir "uv==${UV_VERSION}"

ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

WORKDIR /app
COPY . /app
RUN uv sync --locked

CMD ["sh", "-c", "uv --version && uv run python --version && uv pip list 2>/dev/null | grep -iE '^(numpy|scipy|sympy|scikit-learn|opensysml|z3-solver) ' ; uv run python derivation/run.py"]
