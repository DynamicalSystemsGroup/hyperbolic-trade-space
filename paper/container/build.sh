#!/bin/sh
# Build the container image (WP10 / P10).
#   sh paper/container/build.sh [hts-paper|hts-alt]
# hts-paper : the environment of record (Dockerfile defaults, linux/arm64).
# hts-alt   : robustness image, Ubuntu 24.04 (CI's distribution; glibc 2.39, Python 3.12 from apt) by digest,
#             HTS_ENVIRONMENT_OF_RECORD unset. (Debian bookworm's python:3.12-slim was tried first: the
#             locked z3-solver has no wheel for its glibc 2.36 on arm64 and `uv sync --locked` fails.)
# A `git bundle` of HEAD is written to a temporary directory and handed to the build as the named
# context `history` (the build context itself excludes .git).
set -eu
NAME="${1:-hts-paper}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
H="$(mktemp -d)"
trap 'rm -rf "$H"' EXIT
git -C "$ROOT" bundle create "$H/history.bundle" HEAD >/dev/null 2>&1
case "$NAME" in
hts-paper) set -- ;;
hts-alt) set -- --build-arg OF_RECORD=0 --build-arg BASE_IMAGE=ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852 --build-arg "EXTRA_APT=python3 python3-venv python3-pip python-is-python3" ;;
*) echo "unknown image $NAME" >&2; exit 2 ;;
esac
docker build --build-context history="$H" "$@" -t "$NAME" "$ROOT"
