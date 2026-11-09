#!/bin/sh
# Build the container image (WP10 / P10).
#   sh paper/container/build.sh [hts-paper|hts-alt]
# hts-paper : the environment of record (Dockerfile defaults, linux/arm64).
# hts-alt   : robustness image, Debian bookworm python:3.12-slim by digest, HTS_ENVIRONMENT_OF_RECORD unset.
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
hts-alt) set -- --build-arg OF_RECORD=0 --build-arg BASE_IMAGE=python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df ;;
*) echo "unknown image $NAME" >&2; exit 2 ;;
esac
docker build --build-context history="$H" "$@" -t "$NAME" "$ROOT"
