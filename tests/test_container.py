"""Static checks on the pinned container (WP10, D-13 / R-31); no Docker needed to run them."""

import re
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCKERFILE = (ROOT / "Dockerfile").read_text(encoding="utf-8")
RECORD = ROOT / "paper" / "container" / "RECORD.md"


def _instructions():
    return [ln for ln in DOCKERFILE.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def test_from_is_pinned_by_digest():
    # The base is a build argument (BASE_IMAGE, so a comparable image can be swapped in); its
    # default is pinned by digest, and every FROM that names a registry image goes through it.
    base = [ln for ln in _instructions() if ln.startswith("ARG BASE_IMAGE=")]
    assert base, "no ARG BASE_IMAGE"
    assert re.search(r"@sha256:[0-9a-f]{64}$", base[0]), f"base not pinned by digest: {base[0]}"
    froms = [ln for ln in _instructions() if ln.startswith("FROM ") and "scratch" not in ln]
    assert froms and all("${BASE_IMAGE}" in ln for ln in froms)


def test_platform_of_record_is_linux_arm64():
    froms = [ln for ln in _instructions() if ln.startswith("FROM ") and "scratch" not in ln]
    assert all("--platform=" in ln for ln in froms)
    assert "ARG PLATFORM=linux/arm64" in DOCKERFILE
    assert "ARG NODE_ARCH=arm64" in DOCKERFILE


def test_environment_of_record_variable_is_set_in_the_image():
    assert "ARG OF_RECORD=1" in DOCKERFILE
    assert "ENV HTS_ENVIRONMENT_OF_RECORD=${OF_RECORD}" in DOCKERFILE


def test_locked_install_and_pinned_uv():
    assert "uv sync --locked" in DOCKERFILE
    assert re.search(r"ARG UV_VERSION=\d+\.\d+\.\d+", DOCKERFILE)


def test_default_command_runs_the_derivation():
    cmd = [ln for ln in _instructions() if ln.startswith("CMD")]
    assert cmd and "derivation/run.py" in cmd[-1]


def test_dockerignore_excludes_build_products():
    path = ROOT / ".dockerignore"
    assert path.exists()
    entries = set(path.read_text(encoding="utf-8").split())
    assert {".venv", ".git", "_site", "_stage", "build"} <= entries


def test_record_has_the_recorded_result_lines():
    text = RECORD.read_text(encoding="utf-8")
    assert "RECORD:" in text
    for needle in (
        "image id",
        "uv version",
        "python version",
        "lock hash",
        "ALL LEMMAS PASS",
        "103 passed",
        "sha256:",
    ):
        assert needle in text, needle
    digest = re.search(r"@sha256:([0-9a-f]{64})", DOCKERFILE).group(1)
    assert digest in text, "RECORD.md names a different base digest than the Dockerfile"


@pytest.mark.skipif(shutil.which("docker") is None, reason="docker CLI not installed")
def test_docker_cli_reports_a_version():
    """Docker-gated: only confirms the CLI answers; it never builds an image."""
    import subprocess

    out = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0 and "Docker" in out.stdout
