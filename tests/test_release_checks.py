"""The release gates of scripts/release_checks.py: the changelog entry, the action pins, the bill
(verification cases VC-6 to VC-8 in 4f81a4ea:work-packages/WP47-rounds/checks.md), and the tag
state, the merge commit and the PyPI hashes (specification 1.2 and 1.3, with the site-only
merge), and the version kind (the versioning rule of GOVERNANCE.md, "Versions")."""

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
        "release_checks.py version-kind",
        "paper_mode.py check --stage served",
        "uv lock --check",
        "check_repo_settings.py",
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


# ------------------------------------------------------------------ the versioning rule


def test_version_keys_order_releases_and_pre_releases():
    order = ["0.1.0", "0.1.1", "0.2.0a1", "0.2.0rc1", "0.2.0", "1.0.0"]
    assert sorted(order, key=rc.parse_version) == order
    assert rc.parse_version("v0.1.0") == rc.parse_version("0.1.0")
    assert rc.parse_version("paper-2") is None and rc.parse_version("0.1") is None
    tags = ["v0.1.0", "v0.1.1", "v0.2.0", "paper-1", "v0.3.0rc1"]
    assert rc.previous_release(tags, "0.1.2") == "v0.1.1"
    assert rc.previous_release(tags, "0.3.0") == "v0.3.0rc1"
    assert rc.previous_release(tags, "0.1.0") is None
    assert rc.bump_kind("v0.1.0", "0.1.1") == "patch"
    assert rc.bump_kind("v0.1.4", "0.2.0") == "minor"
    assert rc.bump_kind("v0.2.0", "1.0.0") == "major"


DECLARATION = (
    '[[governed_files]]\npath = "GOVERNANCE.md"\n'
    '[[governed_files]]\npath = ".github/workflows/*.yml"\n'
)
RECORD = {"pkg": {"f": {"kind": "function", "signature": "(a)"}}}


def _version(repo, version, changelog="## [Unreleased]\n- a\n"):
    (repo / "pyproject.toml").write_text(f'[project]\nversion = "{version}"\n', encoding="utf-8")
    (repo / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "--allow-empty", "-m", f"version {version}")


@pytest.fixture
def released(tmp_path):
    """A repository at v0.1.0 with the record, the declaration and a governed file committed."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    (r / "tests" / "data").mkdir(parents=True)
    (r / "tests" / "data" / "api_surface.json").write_text(json.dumps(RECORD), encoding="utf-8")
    (r / ".github" / "workflows").mkdir(parents=True)
    (r / ".github" / "governance.toml").write_text(DECLARATION, encoding="utf-8")
    (r / ".github" / "workflows" / "a.yml").write_text("on: push\n", encoding="utf-8")
    (r / "GOVERNANCE.md").write_text("# Governance\n", encoding="utf-8")
    _version(r, "0.1.0", "## [0.1.0]\n### Added\n- the package\n")
    _git(r, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    return r


def _kind(repo, capsys):
    code = rc.main(["--root", str(repo), "version-kind", "--package", "pkg"])
    out = capsys.readouterr()
    return code, out.out, [line for line in out.err.splitlines() if line.startswith("refused")]


@needs_git
def test_version_kind_first_release_and_redeploy_pass_with_a_notice(repo, capsys):
    (repo / "pyproject.toml").write_text('[project]\nversion = "0.1.0"\n', encoding="utf-8")
    code, out, refused = _kind(repo, capsys)
    assert (code, refused) == (0, []) and "first release" in out
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    code, out, refused = _kind(repo, capsys)
    assert (code, refused) == (0, []) and "already a tag" in out


@needs_git
def test_a_patch_release_that_changes_nothing_it_may_not_passes(released, capsys):
    (released / "docs.md").write_text("a fix\n", encoding="utf-8")
    _version(released, "0.1.1", "## [0.1.1]\n### Fixed\n- a typo\n## [0.1.0]\n### Added\n- x\n")
    code, out, refused = _kind(released, capsys)
    assert (code, refused) == (0, []) and "0.1.1 after v0.1.0 is a patch release" in out


@needs_git
def test_a_patch_release_is_refused_for_each_kind_of_change(released, capsys):
    changed = {"pkg": {"f": {"kind": "function", "signature": "(a, b)"}}}
    (released / "tests" / "data" / "api_surface.json").write_text(
        json.dumps(changed), encoding="utf-8"
    )
    (released / "GOVERNANCE.md").write_text("# Governance\nchanged\n", encoding="utf-8")
    workflow = released / ".github" / "workflows" / "a.yml"
    workflow.write_text("on: pull_request\n", encoding="utf-8")
    _version(
        released,
        "0.1.1",
        "## [0.1.1]\n### Added\n- a thing\n### Removed\n- another\n## [0.1.0]\n- x\n",
    )
    code, out, refused = _kind(released, capsys)
    assert code == 1 and "patch release" in out
    assert refused == [
        "refused: the public surface changed since v0.1.0 "
        "(changed: pkg.f: function (a) -> function (a, b)); a patch release keeps it",
        "refused: GOVERNANCE.md changed since v0.1.0; a patch release changes no governed file",
        "refused: .github/workflows/a.yml changed since v0.1.0; "
        "a patch release changes no governed file",
        "refused: CHANGELOG.md `## [0.1.1]` has a `### Added` section; "
        "a patch release adds and removes nothing",
        "refused: CHANGELOG.md `## [0.1.1]` has a `### Removed` section; "
        "a patch release adds and removes nothing",
    ]
    # The same changes under a minor bump pass with the kind printed; a major bump likewise.
    _version(released, "0.2.0", "## [0.2.0]\n### Added\n- a thing\n")
    code, out, refused = _kind(released, capsys)
    assert (code, refused) == (0, []) and "0.2.0 after v0.1.0 is a minor release" in out
    _version(released, "1.0.0", "## [1.0.0]\n### Removed\n- a thing\n")
    code, out, refused = _kind(released, capsys)
    assert (code, refused) == (0, []) and "1.0.0 after v0.1.0 is a major release" in out


@needs_git
def test_a_patch_release_without_an_entry_yet_reads_no_sections(released, capsys):
    _version(released, "0.1.1")
    code, out, refused = _kind(released, capsys)
    assert (code, refused) == (0, []) and "no `## [0.1.1]` entry yet" in out


@needs_git
def test_a_previous_tag_without_a_record_is_read_from_its_source(repo, capsys):
    """The releases before the rule carry no record: the surface is computed from the tag's src."""
    _commit(repo, "src/pkg/__init__.py", "__all__ = ['f']\n\n\ndef f(a):\n    return a\n")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    # The record at HEAD says what the package is now; the fallback reads v0.1.0's src.
    same = rc.surface_from_source(repo / "src", "pkg")
    assert same == {"pkg": {"f": {"kind": "function", "signature": "(a)"}}}
    (repo / "tests" / "data").mkdir(parents=True)
    (repo / "tests" / "data" / "api_surface.json").write_text(json.dumps(same), encoding="utf-8")
    _version(repo, "0.1.1", "## [0.1.1]\n### Fixed\n- a\n")
    code, _, refused = _kind(repo, capsys)
    assert (code, refused) == (0, [])
    widened = {"pkg": {"f": {"kind": "function", "signature": "(a, b=None)"}}}
    (repo / "tests" / "data" / "api_surface.json").write_text(json.dumps(widened), encoding="utf-8")
    _version(repo, "0.1.1", "## [0.1.1]\n### Fixed\n- a\n")
    code, _, refused = _kind(repo, capsys)
    assert code == 1 and refused == [
        "refused: the public surface changed since v0.1.0 "
        "(changed: pkg.f: function (a) -> function (a, b=None)); a patch release keeps it"
    ]


@needs_git
def test_a_patch_release_without_a_record_in_the_tree_is_refused(repo, capsys):
    _commit(repo, "x.txt", "x\n")
    _git(repo, "tag", "-a", "v0.1.0", "-m", "v0.1.0")
    _version(repo, "0.1.1", "## [0.1.1]\n- a\n")
    code, _, refused = _kind(repo, capsys)
    assert code == 1 and refused[0].startswith("refused: tests/data/api_surface.json is missing")
