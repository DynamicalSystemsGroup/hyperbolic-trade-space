"""Static checks on the pinned container (WP10, D-13 / R-31); no Docker needed to run them."""

import re
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCKERFILE = (ROOT / "Dockerfile").read_text()
RECORD = ROOT / "paper" / "container" / "RECORD.md"


def _instructions():
    return [ln for ln in DOCKERFILE.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def test_from_is_pinned_by_digest():
    froms = [ln for ln in _instructions() if ln.startswith("FROM ")]
    assert froms, "no FROM line"
    for ln in froms:
        assert re.search(r"@sha256:[0-9a-f]{64}\b", ln), f"FROM not pinned by digest: {ln}"


def test_platform_of_record_is_linux_amd64():
    froms = [ln for ln in _instructions() if ln.startswith("FROM ")]
    assert all("--platform=" in ln for ln in froms)
    assert "ARG PLATFORM=linux/amd64" in DOCKERFILE


def test_locked_install_and_pinned_uv():
    assert "uv sync --locked" in DOCKERFILE
    assert re.search(r"ARG UV_VERSION=\d+\.\d+\.\d+", DOCKERFILE)


def test_default_command_runs_the_derivation():
    cmd = [ln for ln in _instructions() if ln.startswith("CMD")]
    assert cmd and "derivation/run.py" in cmd[-1]


def test_dockerignore_excludes_build_products():
    path = ROOT / ".dockerignore"
    assert path.exists()
    entries = set(path.read_text().split())
    assert {".venv", ".git", "_site", "_stage", "build"} <= entries


def test_record_has_the_recorded_result_lines():
    text = RECORD.read_text()
    assert "RECORD:" in text
    for needle in (
        "image id",
        "uv version",
        "python version",
        "lock hash",
        "ALL LEMMAS PASS",
        "101 passed",
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
