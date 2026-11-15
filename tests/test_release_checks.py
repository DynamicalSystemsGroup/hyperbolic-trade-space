"""The release gates that read files (verification cases VC-6 to VC-8 in
work-packages/WP47-rounds/checks.md): the changelog entry, the action pins, the bill."""

import importlib.util
import json
import re
from pathlib import Path

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
        "uv lock --check",
    ):
        assert gate in text
    assert re.search(r"cyclonedx1\.5", text)
