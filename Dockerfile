# Environment of record for the paper (WP10, Amendment 1, D-13 / R-31; platform ratified by the
# supervisor 2026-11-09: linux/arm64, the architecture the author's machine runs natively).
#
# Base: python:3.12-slim (Debian trixie), pinned by the DIGEST of its multi-arch index
# (resolved 2026-11-09 with `docker buildx imagetools inspect python:3.12-slim`; tag at
# resolution: 3.12-slim = 3.12.16-slim-trixie; the arm64 manifest in it is
# sha256:c61cffc3bacb94ed026ff8b45d5114b7693dd0420baca0a1ace0e3d0ce9035fd, the amd64 one
# sha256:05a994d2344eb364cc186910f4fc8786a38215f39f00d0acc25bff33a08f4177). The tag is kept for
# readers only; the digest is what is pulled. Platform of record: linux/arm64. The same index
# builds linux/amd64 (PLATFORM=linux/amd64 NODE_ARCH=x64 and the x64 NODE_SHA256 below).
#
# Build:  sh paper/container/build.sh            (image hts-paper; also the history bundle, below)
#         sh paper/container/build.sh hts-alt    (robustness image: a different Debian release)
# Run:    docker run --rm hts-paper                                    (toolchain + derivation)
#         docker run --rm --network none hts-paper uv run pytest -q    (full test suite)
# Robustness: BASE_IMAGE is a build argument. The second image (hts-alt) uses the python:3.12-slim
# of Debian bookworm, pinned by digest, with the same uv.lock; it does NOT set
# HTS_ENVIRONMENT_OF_RECORD, so the exact comparisons are not asserted there (build ARG
# OF_RECORD=0).
# Node (needed by mystmd) is pinned below by version, sha256 and the release signature; the
# Python packages by uv.lock; the toolkit by examples/adcs/experiments/toolkit-pin.toml; the
# MyST site template and web libraries are fetched ONCE at build time (warm-up build) so that the
# whole paper builds with `--network none` at run time. Debian packages (git, curl, gnupg, ...) are
# installed from the base image's apt snapshot-of-the-day and their versions are recorded in
# paper/container/RECORD.md rather than pinned.
# History: tests read the git history (generating commits of the frozen data, the ledger). The
# build context excludes .git (see .dockerignore); instead `build.sh` writes a `git bundle` of HEAD
# outside the context and passes it as the named context `history`, and the image rebuilds a
# repository from it (no .git directory is copied from the host). Without it the image still
# builds and those tests skip with a reason.
# See paper/container/README.md for the full-paper commands and paper/container/RECORD.md for
# the recorded runs. Nothing is published to a registry.
ARG PLATFORM=linux/arm64
ARG BASE_IMAGE=python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
# Empty by default; `--build-context history=<dir holding history.bundle>` replaces it.
FROM scratch AS history
FROM --platform=${PLATFORM} ${BASE_IMAGE}

# EXTRA_APT is empty for the python image; the robustness image on a bare distribution names the
# Python it needs there (see paper/container/build.sh).
ARG EXTRA_APT=""
# System tools: git (toolkit stdlib fetch, tests), gnupg (Node signature), procps (`ps`, which the
# MyST static-site build uses to stop its local server).
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git gnupg procps xz-utils ${EXTRA_APT} \
    && rm -rf /var/lib/apt/lists/*

# Node.js (MyST needs >= 22): an exact LTS release, tarball for the build architecture from nodejs.org.
#  1. the tarball's sha256 below is checked with `sha256sum -c` before extraction;
#  2. SHASUMS256.txt of the release is checked against its clearsigned .asc with GnuPG, with the
#     signing key taken from nodejs/release-keys at a pinned commit (key file sha256 pinned too)
#     and the signature required to be VALIDSIG from that exact fingerprint; and the tarball's
#     line in SHASUMS256.txt must equal the literal sha256 below.
ARG NODE_VERSION=24.22.2
ARG NODE_ARCH=arm64
# arm64 (default); x64: 48cc0e21e048790e54c0cf5749c2725005313d652651c40b7a21feb9697aaf75
ARG NODE_SHA256=eb187837a2230d4047161ac0be008584e16b46f726e9c9490ee35dc6b17d9ba8
ARG NODE_SIGNING_FPR=5BE8A3F6C8A5C01D106C0AD820B1A390B168D356
ARG NODE_RELEASERS_COMMIT=481637f813e912c4aa3622d7964ab426c97b8e8d
ARG NODE_SIGNER_ASC_SHA256=5115095e2f8010c75da052ecb1cfb3af630e084f0f8daa93a863557b01b0f90a
RUN set -eux; \
    cd /tmp; \
    f="node-v${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz"; \
    curl -fsSLO "https://nodejs.org/dist/v${NODE_VERSION}/${f}"; \
    curl -fsSLO "https://nodejs.org/dist/v${NODE_VERSION}/SHASUMS256.txt"; \
    curl -fsSLO "https://nodejs.org/dist/v${NODE_VERSION}/SHASUMS256.txt.asc"; \
    curl -fsSL -o key.asc "https://raw.githubusercontent.com/nodejs/release-keys/${NODE_RELEASERS_COMMIT}/keys/${NODE_SIGNING_FPR}.asc"; \
    echo "${NODE_SIGNER_ASC_SHA256}  key.asc" | sha256sum -c -; \
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --batch --import key.asc; \
    gpg --batch --status-fd 1 --verify SHASUMS256.txt.asc | grep -q "^\[GNUPG:\] VALIDSIG ${NODE_SIGNING_FPR} "; \
    gpg --batch --decrypt SHASUMS256.txt.asc > SHASUMS256.signed.txt; \
    grep -qx "${NODE_SHA256}  ${f}" SHASUMS256.signed.txt; \
    echo "${NODE_SHA256}  ${f}" | sha256sum -c -; \
    tar -xJf "${f}" -C /usr/local --strip-components=1 --no-same-owner; \
    rm -rf /tmp/* "${GNUPGHOME}"; \
    node --version; npm --version

# uv version: the one the record was made with. CI installs astral-sh/setup-uv@v7 without a
# version (latest); the locked environment, not uv, determines the installed packages.
ARG UV_VERSION=0.9.18
RUN pip install --no-cache-dir --break-system-packages "uv==${UV_VERSION}"

ARG OF_RECORD=1
ENV HTS_ENVIRONMENT_OF_RECORD=${OF_RECORD}
# UV_NO_SYNC: the environment was synced (locked) at build time; `uv run` at run time, with no
# network, must not try to re-resolve the build backend if a file's timestamp changes.
ENV UV_NO_SYNC=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    NODE_OPTIONS=--dns-result-order=ipv4first \
    SYSML_TOOLKIT_CACHE=/opt/sysml-toolkit-cache

WORKDIR /app
COPY . /app
# The history of the tracked files, rebuilt from the bundle (HEAD only; the working tree stays as
# copied, so `git diff` in the image shows any difference from HEAD).
COPY --from=history / /history/
RUN if [ -f /history/history.bundle ]; then \
        git init -q . && git fetch -q /history/history.bundle HEAD \
        && git -c user.name=hts -c user.email=hts@invalid reset -q FETCH_HEAD \
        && git log -1 --format='history: %H' ; \
    else echo "no history bundle: history-dependent tests will skip"; fi \
    && rm -rf /history
RUN uv sync --locked

# The pinned model-checking toolkit (examples/adcs/experiments/toolkit-pin.toml: sha256-verified
# release archive, stdlib by commit) goes into the image so the suite needs no network at run time.
# GitHub release downloads answer 504 intermittently, so the fetch is retried (each attempt is
# digest-verified; a bad archive is never accepted).
RUN for i in $(seq 1 30); do \
        PYTHONPATH=examples/adcs uv run python -m experiments.toolkit fetch && exit 0; \
        echo "toolkit fetch failed (attempt $i); retrying"; sleep 30; \
    done; exit 1

# NODE_OPTIONS above: MyST's static build starts a local server that Node binds on ::1 while MyST
# fetches 127.0.0.1; ipv4first makes `localhost` resolve to 127.0.0.1 for both.
#
# The OpenSysML service binary (sysml-grpc, release v0.12.1) the case-model tests start: the
# opensysml package downloads it on first use, verifying it against the release digests shipped in
# the package (release-digests.json); done here so no run needs the network. Cached under
# ~/.opensysml/bin.
RUN uv run python -c "from opensysml.binary import ensure_binary; print(ensure_binary())"

# Warm-up build of the paper (network at BUILD time only): MyST downloads the site template into
# paper/_build/templates and caches web libraries / DOI lookups under paper/_build; the later
# `myst build --html` at run time reuses them with no network. See paper/container/RECORD.md.
# The default site favicon is fetched from https://mystmd.org/favicon.ico on every build and is
# absent offline, so the warm-up copy is kept beside the cache (paper/container/build-paper.sh puts
# it back). The hashes of what was downloaded are printed into the build log (RECORD.md).
RUN cd paper && uv run myst build --html \
    && mkdir -p _build/cache && cp _build/html/favicon.ico _build/cache/favicon.ico \
    && (cd "$(find _build/templates/site -mindepth 1 -maxdepth 2 -name template.zip -exec dirname {} \; | head -1)" \
        && pwd && sha256sum template.zip package-lock.json \
        && grep -m1 '"version"' package.json) \
    && sha256sum _build/cache/favicon.ico

CMD ["sh", "-c", "uv --version && uv run python --version && node --version && uv pip list 2>/dev/null | grep -iE '^(numpy|scipy|sympy|scikit-learn|opensysml|z3-solver) ' ; uv run python derivation/run.py"]
