"""The release gates of scripts/release_checks.py: the changelog entry, the action pins, the bill
(verification cases VC-6 to VC-8 in work-packages/WP47-rounds/checks.md), and the tag state, the
merge commit and the PyPI hashes (specification 1.2 and 1.3, with the site-only merge)."""

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "release_checks", ROOT / "scripts" / "release_checks.py"
)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


def test_a_final_release_needs_its_own_changelog_entry(tmp_path):
    (tmp_path / "CHANGELOG.md").write_text("## [Unreleased]\n- a\n", encoding="utf-8")
    assert rc.main(["--root", str(tmp_path), "changelog", "--version", "0.1.0", "--final"]) == 1
    assert rc.main(["--root", str(tmp_path), "changelog", "--version", "0.1.0rc1"]) == 0
    (tmp_path / "CHANGELOG.md").write_text("## [0.1.0] - 2026-11-20\n- a\n", encoding="utf-8")
    notes = tmp_path / "n.md"
    args = [
        "--root",
        str(tmp_path),
        "changelog",
        "--version",
        "0.1.0",
        "--final",
        "--notes",
        str(notes),
    ]
    assert rc.main(args) == 0 and notes.read_text(encoding="utf-8") == "- a\n"


def test_an_empty_changelog_entry_is_refused(tmp_path):
    (tmp_path / "CHANGELOG.md").write_text("## [0.1.0]\n\n## [0.0.1]\n- x\n", encoding="utf-8")
    assert rc.main(["--root", str(tmp_path), "changelog", "--version", "0.1.0", "--final"]) == 1


def test_every_action_in_this_repository_is_pinned_to_a_commit():
    assert rc.pin_problems(ROOT) == []


def test_an_action_pinned_to_a_tag_is_refused(tmp_path):
    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "a.yml").write_text(
        "steps:\n  - uses: actions/checkout@v5\n  - uses: ./x\n", encoding="utf-8"
    )
    assert rc.pin_problems(tmp_path) == ["a.yml: `actions/checkout@v5` is not pinned to a commit"]


def _lock(tmp_path):
    (tmp_path / "uv.lock").write_text(
        '[[package]]\nname = "a"\nversion = "1.0"\n[[package]]\nname = "me"\nversion = "0.1"\n',
        encoding="utf-8",
    )


def _bom(tmp_path, components, root=None):
    doc = {"bomFormat": "CycloneDX", "components": components, "metadata": {"component": root}}
    (tmp_path / "s.json").write_text(json.dumps(doc), encoding="utf-8")
    return ["--root", str(tmp_path), "sbom", "--sbom", str(tmp_path / "s.json")]


def test_a_bill_naming_every_locked_package_passes(tmp_path):
    _lock(tmp_path)
    args = _bom(tmp_path, [{"name": "a", "version": "1.0"}], {"name": "me", "version": "0.1"})
    assert rc.main(args) == 0


def test_a_bill_missing_a_locked_package_or_version_is_refused(tmp_path):
    _lock(tmp_path)
    assert rc.main(_bom(tmp_path, [{"name": "a", "version": "1.0"}])) == 1
    args = _bom(tmp_path, [{"name": "a", "version": "2.0"}], {"name": "me", "version": "0.1"})
    assert rc.main(args) == 1


def test_the_release_workflow_runs_every_gate():
    text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    for gate in (
        "check_release_version.py",
        "release_checks.py changelog",
        "release_checks.py pins",
        "release_checks.py sbom",
        "release_checks.py tag",
        "release_checks.py merge",
        "release_checks.py pypi",
        "paper_mode.py check --stage served",
        "uv lock --check",
    ):
        assert gate in text
    assert re.search(r"cyclonedx1\.5", text)


needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git is not on PATH")


def _git(repo, *args):
    out = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def _commit(repo, path, text):
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_text(text, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", f"edit {path}")
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _commit(r, "pyproject.toml", 'version = "0.1.0"\n')
    return r


def _state(repo, sha):
    return rc.tag_state(repo, "v0.1.0", sha)[0]


@needs_git
def test_tag_state_new_ours_taken(repo):
    first = _git(repo, "rev-parse", "HEAD")
    assert _state(repo, first) == "new"
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0", first)
    assert _state(repo, first) == "ours"
    # A later commit that leaves the package files alone: the merge redeploys the site only.
    docs = _commit(repo, "docs/index.md", "a docs fix\n")
    assert _state(repo, docs) == "site-only"
    # A change to a package file with the version unchanged: taken, and the check exits 1.
    for path in ("src/pkg/__init__.py", "uv.lock", "pyproject.toml"):
        sha = _commit(repo, path, f"changed {path}\n")
        state, reason = rc.tag_state(repo, "v0.1.0", sha)
        assert state == "taken" and path in reason and "new version" in reason
    assert rc.main(["--root", str(repo), "tag", "--tag", "v0.1.0", "--sha", sha]) == 1
    # A tag on a commit that is not an ancestor is taken too.
    _git(repo, "checkout", "-q", "--orphan", "other")
    stray = _commit(repo, "x.txt", "x\n")
    assert _state(repo, stray) == "taken"


@needs_git
def test_merge_commit_needs_two_parents_from_dev(repo):
    _git(repo, "branch", "dev")
    _git(repo, "checkout", "-q", "dev")
    _commit(repo, "a.txt", "on dev\n")
    _git(repo, "checkout", "-q", "main")
    single = _commit(repo, "b.txt", "a direct commit on main\n")
    problems = rc.merge_problems(repo, single, "dev")
    assert problems and "1 parent" in problems[0]
    _git(repo, "merge", "--no-ff", "-q", "-m", "release", "dev")
    merge = _git(repo, "rev-parse", "HEAD")
    assert rc.merge_problems(repo, merge, "dev") == []
    assert rc.main(["--root", str(repo), "merge", "--sha", merge, "--from", "dev"]) == 0
    # A merge of a branch that is not dev.
    _git(repo, "checkout", "-q", "-b", "feature", single)
    _commit(repo, "c.txt", "elsewhere\n")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-q", "-m", "not from dev", "feature")
    other = _git(repo, "rev-parse", "HEAD")
    assert "is not on dev" in rc.merge_problems(repo, other, "dev")[0]


def test_pypi_hashes_must_equal_the_dist(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    files = {"p-0.1.0-py3-none-any.whl": b"wheel", "p-0.1.0.tar.gz": b"sdist"}
    for name, data in files.items():
        (dist / name).write_bytes(data)
    digests = {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}

    def record(d):
        return {"urls": [{"filename": n, "digests": {"sha256": h}} for n, h in d.items()]}

    assert rc.pypi_problems("0.1.0", dist, fetch=lambda v: record(digests), attempts=1) == []
    wrong = dict(digests, **{"p-0.1.0.tar.gz": "0" * 64})
    problems = rc.pypi_problems("0.1.0", dist, fetch=lambda v: record(wrong), attempts=1)
    assert len(problems) == 1 and problems[0].startswith("p-0.1.0.tar.gz: PyPI holds sha256")
    missing = {"p-0.1.0-py3-none-any.whl": digests["p-0.1.0-py3-none-any.whl"]}
    problems = rc.pypi_problems("0.1.0", dist, fetch=lambda v: record(missing), attempts=1)
    assert problems == ["p-0.1.0.tar.gz is built and not on PyPI"]
    calls = []

    def absent(v):
        calls.append(v)
        return None

    problems = rc.pypi_problems("0.1.0", dist, fetch=absent, attempts=2, wait=0)
    assert problems == ["PyPI has no version 0.1.0"] and calls == ["0.1.0", "0.1.0"]
