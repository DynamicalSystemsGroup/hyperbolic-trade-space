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


def test_node_is_pinned_with_a_verified_checksum_and_signature():
    node = re.search(r"ARG NODE_VERSION=(\d+)\.\d+\.\d+", DOCKERFILE)
    assert node and int(node.group(1)) >= 22, "Node must be an exact release, major >= 22"
    sha = re.search(r"ARG NODE_SHA256=([0-9a-f]{64})\b", DOCKERFILE)
    assert sha, "Node tarball sha256 must be a literal ARG"
    assert "sha256sum -c" in DOCKERFILE
    assert "nodejs.org/dist/v${NODE_VERSION}/" in DOCKERFILE
    assert "linux-x64" in DOCKERFILE
    # the checksum is verified before the tarball is extracted
    assert DOCKERFILE.rindex("sha256sum -c") < DOCKERFILE.index("tar -xJf")
    # the release signature: pinned signer and key file, VALIDSIG required
    assert re.search(r"ARG NODE_SIGNING_FPR=[0-9A-F]{40}\b", DOCKERFILE)
    assert re.search(r"ARG NODE_SIGNER_ASC_SHA256=[0-9a-f]{64}\b", DOCKERFILE)
    assert "VALIDSIG ${NODE_SIGNING_FPR}" in DOCKERFILE


def test_no_floating_tags_or_unpinned_downloads():
    assert not re.search(r":latest\b", DOCKERFILE)
    assert "@latest" not in DOCKERFILE
    assert re.search(r"ARG NODE_RELEASERS_COMMIT=[0-9a-f]{40}\b", DOCKERFILE)


def test_image_is_provisioned_for_an_offline_run():
    # toolkit fetched at build time; MyST warmed up at build time; ipv4first for the local server
    assert "experiments.toolkit fetch" in DOCKERFILE
    assert re.search(r"RUN cd paper && uv run myst build --html", DOCKERFILE)
    assert "NODE_OPTIONS=--dns-result-order=ipv4first" in DOCKERFILE
    assert "SYSML_TOOLKIT_CACHE=" in DOCKERFILE
    assert "paper/_build" in (ROOT / ".dockerignore").read_text().split()


def test_offline_build_script_exists():
    script = (ROOT / "paper" / "container" / "build-paper.sh").read_text()
    assert "npm_config_registry" in script and "myst build --html" in script


def test_record_has_the_recorded_result_lines():
    text = RECORD.read_text()
    assert "RECORD:" in text
    for needle in (
        "image id",
        "uv version",
        "python version",
        "lock hash",
        "node version",
        "ALL LEMMAS PASS",
        "sha256:",
        "--network none",
        "derivation.proofmap",
        "execute_notebooks.py",
        "myst build --html",
        "uv run pytest -q",
        "passed",
        "Colima",
    ):
        assert needle in text, needle
    # the claim that these steps were not run must be gone
    assert "were not run" not in text
    digest = re.search(r"@sha256:([0-9a-f]{64})", DOCKERFILE).group(1)
    assert digest in text, "RECORD.md names a different base digest than the Dockerfile"
    node_sha = re.search(r"ARG NODE_SHA256=([0-9a-f]{64})", DOCKERFILE).group(1)
    assert node_sha in text, "RECORD.md names a different Node checksum than the Dockerfile"
    node_v = re.search(r"ARG NODE_VERSION=(\S+)", DOCKERFILE).group(1)
    assert node_v in text
    assert "RECORD: full test suite" in text
    assert "RECORD: offline paper build" in text
    digest = re.search(r"@sha256:([0-9a-f]{64})", DOCKERFILE).group(1)
    assert digest in text, "RECORD.md names a different base digest than the Dockerfile"


@pytest.mark.skipif(shutil.which("docker") is None, reason="docker CLI not installed")
def test_docker_cli_reports_a_version():
    """Docker-gated: only confirms the CLI answers; it never builds an image."""
    import subprocess

    out = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0 and "Docker" in out.stdout
