"""The release gates of scripts/release_checks.py: the changelog entry, the action pins, the bill
(verification cases VC-6 to VC-8 in 4f81a4ea:work-packages/WP47-rounds/checks.md), and the tag
state, the merge commit and the PyPI hashes (specification 1.2 and 1.3, with the site-only
merge), and the version kind (the versioning rule of GOVERNANCE.md, "Versions")."""

import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "release_checks", ROOT / "scripts" / "release_checks.py"
)
rc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = rc  # dataclasses resolve the module by name
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


# ------------------------------------------------------------------ the bump

PLACES = {p for p, _ in rc.VERSION_PLACES}
# A version assignment in a tracked file: `version = "X"`, `__version__ = "X"`, `version: X`,
# `"version": "X"`, `package.version = "X"`, or the contract document's `Current value: `X``.
ASSIGNMENT = (
    r"""^\s*["']?[\w.-]*version[\w.-]*["']?\s*[:=]\s*["']?{v}["']?\s*,?$|Current value: `{v}`"""
)


def _tree(tmp_path):
    """A copy of the files the bump writes, from the tree."""
    for name in PLACES | {"CHANGELOG.md"}:
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / name, tmp_path / name)
    return tmp_path


def _texts(root):
    return {name: (root / name).read_text(encoding="utf-8") for name in PLACES | {"CHANGELOG.md"}}


def test_bump_writes_every_place_and_releases_the_changelog(tmp_path, capsys):
    """After the bump the consumers agree: pyproject, `__version__`, the manifest (R-2), the
    document's quoted values (R-8), the citation file (the site metadata), and the changelog has
    the released entry with the former unreleased body under it."""
    root = _tree(tmp_path)
    current = rc._release_version(root)
    unreleased = rc.changelog_section(_texts(root)["CHANGELOG.md"], "Unreleased")
    args = ["bump", "9.0.0", "--date", "2026-11-20", "--changelog", "final", "--no-lock"]
    assert rc.main(["--root", str(root), *args]) == 0
    out = capsys.readouterr().out
    for name in PLACES | {"CHANGELOG.md"}:
        assert f"changed: {name}" in out
    assert "bump: 9.0.0 written in 6 files; nothing committed" in out
    assert set(rc.version_values(root).values()) == {"9.0.0"}
    texts = _texts(root)
    for name in PLACES:
        assert current not in texts[name], name
    pyproject = tomllib.loads(texts["pyproject.toml"])["project"]["version"]
    manifest = tomllib.loads(texts["work-packages/interface-contract.toml"])["package"]["version"]
    init = re.search(r'^__version__ = "([^"]+)"$', texts["src/tradespace/__init__.py"], re.M)
    citation = yaml.safe_load(texts["CITATION.cff"])
    document = texts["work-packages/interface-contract.md"]
    quoted = re.search(r'^package\.version = "([^"]+)"$', document, re.M)
    assert pyproject == init.group(1) == manifest == quoted.group(1) == str(citation["version"])
    assert str(citation["date-released"]) == "2026-11-20"
    log = texts["CHANGELOG.md"]
    assert rc.changelog_section(log, "Unreleased") == ""
    assert rc.changelog_section(log, "9.0.0") == unreleased
    assert "## [9.0.0] - 2026-11-20" in log and rc.changelog_problems(root, "9.0.0", True) == []


def test_bump_stub_adds_a_dry_run_entry_and_keeps_the_unreleased_one(tmp_path):
    root = _tree(tmp_path)
    before = _texts(root)
    changed, problems = rc.bump(root, "0.1.1", None, "stub", lock=False)
    assert problems == [] and sorted(changed) == sorted(PLACES | {"CHANGELOG.md"})
    log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert rc.changelog_section(log, "0.1.1") == rc.STUB_LINE
    assert rc.changelog_section(log, "Unreleased") == rc.changelog_section(
        before["CHANGELOG.md"], "Unreleased"
    )
    assert rc.changelog_problems(root, "0.1.1", True) == []
    # without --date the citation file's release day is untouched
    assert (
        yaml.safe_load(before["CITATION.cff"])["date-released"]
        == yaml.safe_load((root / "CITATION.cff").read_text(encoding="utf-8"))["date-released"]
    )
    # `none` leaves the changelog alone
    root2 = _tree(tmp_path / "two")
    changed, problems = rc.bump(root2, "0.1.1", None, "none", lock=False)
    assert problems == [] and "CHANGELOG.md" not in changed
    assert (root2 / "CHANGELOG.md").read_text(encoding="utf-8") == before["CHANGELOG.md"]


def test_bump_refuses_and_writes_nothing(tmp_path):
    root = _tree(tmp_path)
    before = _texts(root)
    current = rc._release_version(root)
    cases = {
        "0.0.1": "is not above the current",
        current: "is not above the current",
        "0.2": "is not major.minor.patch",
        "1.0.0.0": "is not major.minor.patch",
    }
    for version, reason in cases.items():
        changed, problems = rc.bump(root, version, None, "final", lock=False)
        assert changed == [] and len(problems) == 1 and reason in problems[0], version
    _, problems = rc.bump(root, "9.0.0", "20-11-2026", "final", lock=False)
    assert problems == ["--date '20-11-2026' is not YYYY-MM-DD"]
    _, problems = rc.bump(root, "9.0.0", None, "later", lock=False)
    assert problems == ["--changelog must be one of final, stub, none"]
    # an inconsistent tree is named, not papered over
    init = root / "src" / "tradespace" / "__init__.py"
    init.write_text(init.read_text(encoding="utf-8").replace(current, "0.0.9"), encoding="utf-8")
    _, problems = rc.bump(root, "9.0.0", None, "final", lock=False)
    assert len(problems) == 1 and problems[0].startswith("src/tradespace/__init__.py does not hold")
    init.write_text(before["src/tradespace/__init__.py"], encoding="utf-8")
    # nothing to release
    log = root / "CHANGELOG.md"
    text = log.read_text(encoding="utf-8")
    body = rc.changelog_section(text, "Unreleased")
    log.write_text(text.replace(body, "", 1), encoding="utf-8")
    _, problems = rc.bump(root, "9.0.0", None, "final", lock=False)
    assert problems == ["CHANGELOG.md `## [Unreleased]` is empty; nothing to release"]
    log.write_text(text, encoding="utf-8")
    assert _texts(root) == before


@needs_git
def test_the_version_places_are_every_assignment_in_the_tree():
    """The list is complete: every tracked file that assigns the current version is a place
    (uv.lock follows by `uv lock`; the changelog's history and prose mentions are not
    assignments)."""
    current = rc._release_version(ROOT)
    pattern = re.compile(ASSIGNMENT.format(v=re.escape(current)), re.M)
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split("\n")
    found = set()
    for name in tracked:
        path = ROOT / name
        if not name or name == "uv.lock" or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if pattern.search(text):
            found.add(name)
    assert found == PLACES
    assert None not in rc.version_values(ROOT).values()


# ------------------------------------------------------------------ the gates


def test_the_gates_mirror_the_workflows():
    checks = rc.gates(release=True, since="origin/dev")
    names = [g.name for g in checks]
    assert names == [
        "attribution",
        "uv lock --check",
        "ruff check",
        "ruff format --check",
        "pytest (the rule modules)",
        "vocabulary",
        "api surface record",
        "repository settings",
        "branches",
        "version",
        "tag",
        "changelog --final",
        "version-kind",
        "pins",
        "paper mode (served)",
    ]
    assert [g.name for g in rc.gates(False, "origin/dev")] == names[:9]
    assert [g.name for g in checks if g.release] == names[9:]
    assert [g.name for g in checks if g.needs_gh] == ["repository settings", "branches"]
    for module in rc.RULE_MODULES:
        assert (ROOT / module.split("::")[0]).is_file(), module
    tests = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")
    for step in ("uv lock --check", "uv run ruff check .", "uv run ruff format --check ."):
        assert step in tests
    assert f"grep -ciE '{rc.ATTRIBUTION.pattern}'" in tests
    release = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    for step in (
        "check_release_version.py",
        "release_checks.py tag",
        "release_checks.py changelog",
        "release_checks.py version-kind",
        "release_checks.py pins",
        "paper_mode.py check --stage served",
    ):
        assert step in release


def test_run_gates_prints_a_table_and_a_failing_check_fails_the_verdict():
    green = rc.Gate("green", rc.command(sys.executable, "-c", "print('fine')"))
    red = rc.Gate("red", rc.command(sys.executable, "-c", "print('why'); raise SystemExit(3)"))
    gh = rc.Gate("needs gh", rc.command(sys.executable, "-c", "pass"), needs_gh=True)
    out = io.StringIO()
    assert rc.run_gates(ROOT, [green, gh], out=out, gh=False) == 0
    lines = out.getvalue().splitlines()
    assert lines[0].startswith("gates at ") and lines[0].endswith(": 2 checks")
    assert lines[1:] == [
        "  ok    green: fine",
        "  skip  needs gh: gh is not authenticated",
        "verdict: pass (1 checks; 1 skipped (needs gh))",
    ]
    out = io.StringIO()
    assert rc.run_gates(ROOT, [green, red, gh], out=out, gh=True) == 1
    text = out.getvalue()
    assert "  FAIL  red (exit 3)\n        why\n" in text and "  ok    needs gh\n" in text
    assert text.strip().endswith("verdict: refused (1 of 3: red)")
    # a release check alone refusing says what the head is and what to do
    tag = rc.Gate("tag", rc.command(sys.executable, "-c", "raise SystemExit(1)"), release=True)
    out = io.StringIO()
    assert rc.run_gates(ROOT, [green, tag], out=out, gh=True) == 1
    assert "release gates refuse this head" in out.getvalue() and "bump" in out.getvalue()


@needs_git
def test_attribution_lines_read_the_commits_since_the_base(repo):
    _git(repo, "branch", "base")
    _commit(repo, "a.txt", "a\n")
    assert rc.attribution_lines(repo, "base") == []
    trailer = "Co-" + "Authored-By: someone <x@y>"
    (repo / "b.txt").write_text("b\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", f"a change\n\n{trailer}")
    hits = rc.attribution_lines(repo, "base")
    assert len(hits) == 1 and hits[0].startswith(
        "1 attribution line(s) in the commits of base..HEAD"
    )
    # an absent base: the whole log, as the workflow reads it
    assert rc.attribution_lines(repo, "no-such-ref")[0].endswith(f"HEAD: ['{trailer}']")


# ------------------------------------------------------------------ the remote's branches


def test_branches_names_the_stray_and_notices_the_dry_run(monkeypatch, capsys):
    heads = ["main", "dev", "paper", "qc/release", "dependabot/uv/x", "wp-a", "old-b"]
    monkeypatch.setattr(rc, "remote_heads", lambda root, remote: heads)
    monkeypatch.setattr(rc, "open_pull_request_heads", lambda root: {"wp-a"})
    notices, problems = rc.branch_problems(ROOT)
    assert notices == [
        "branches: 7 on origin; long-lived main, dev, paper",
        "branches: qc/release is a dry-run branch; delete it after its run",
    ]
    assert problems == [
        "origin/old-b is neither long-lived, an open pull request's head, qc/ nor dependabot/; "
        "delete it (GOVERNANCE.md, Branches)"
    ]
    assert rc.main(["branches"]) == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines() == notices and "refused: origin/old-b" in captured.err
    monkeypatch.setattr(rc, "open_pull_request_heads", lambda root: {"wp-a", "old-b"})
    assert rc.main(["branches"]) == 0

    def no_gh(root):
        raise RuntimeError("gh pr list failed")

    monkeypatch.setattr(rc, "open_pull_request_heads", no_gh)
    assert rc.main(["branches"]) == 2
