"""scripts/release_cleanup.py (specification 1.4): a fake gh and a fake PyPI injected as callables.

Offline: nothing here calls gh or PyPI.
"""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "release_cleanup", ROOT / "scripts" / "release_cleanup.py"
)
rcl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rcl)

REPO = "Owner/name"
SHA = "1a2b3c4d5e6f" + "0" * 28


class FakeGh:
    """A repository with an optional tag and an optional release; records every call."""

    def __init__(self, tag=True, release="draft", fail_on=None):
        self.tag = tag
        self.release = release  # None, "draft" or "published"
        self.fail_on = fail_on  # "release delete" or "api -X"
        self.calls = []

    def __call__(self, args):
        self.calls.append(args)
        key = " ".join(args[:2])
        if self.fail_on and key == self.fail_on:
            return 1, "", "HTTP 500: server error"
        if args[:2] == ["api", "-X"]:
            self.tag = False
            return 0, "", ""
        if args[0] == "api":
            if not self.tag:
                return 1, "", "gh: Not Found (HTTP 404)"
            return 0, json.dumps({"object": {"sha": SHA, "type": "commit"}}), ""
        if args[:2] == ["release", "view"]:
            if self.release is None:
                return 1, "", "release not found"
            doc = {"isDraft": self.release == "draft", "assets": [{}, {}, {}]}
            return 0, json.dumps(doc), ""
        if args[:2] == ["release", "delete"]:
            self.release = None
            return 0, "", ""
        raise AssertionError(f"unexpected gh call {args}")

    def deletions(self):
        return [c for c in self.calls if c[:2] in (["release", "delete"], ["api", "-X"])]


def pypi_with(present):
    def pypi(version):
        pypi.asked.append(version)
        return present

    pypi.asked = []
    return pypi


def run(capsys, args, gh, pypi):
    code = rcl.main(["--repo", REPO, *args], gh=gh, pypi=pypi, env={})
    return code, capsys.readouterr().out


def test_removes_the_draft_then_the_tag_when_pypi_lacks_the_version(capsys):
    gh, pypi = FakeGh(), pypi_with(False)
    code, out = run(capsys, ["--tag", "v0.1.0", "--run-id", "123456"], gh, pypi)
    assert code == 0
    assert gh.deletions() == [
        ["release", "delete", "v0.1.0", "--repo", REPO, "--yes"],
        ["api", "-X", "DELETE", f"repos/{REPO}/git/refs/tags/v0.1.0"],
    ]
    assert pypi.asked == ["0.1.0"]
    assert "found: tag v0.1.0 -> 1a2b3c4; draft release v0.1.0 (3 assets); PyPI 0.1.0 absent" in out
    assert out.index("removed: draft release v0.1.0") < out.index("removed: tag v0.1.0")
    assert "retry: gh run rerun 123456" in out
    assert "merge a new pull request into main; v0.1.0 is free" in out


def test_dry_run_removes_nothing(capsys):
    gh = FakeGh()
    code, out = run(capsys, ["--tag", "v0.1.0", "--dry-run"], gh, pypi_with(False))
    assert code == 0 and gh.deletions() == []
    assert "would remove: draft release v0.1.0" in out and "would remove: tag v0.1.0" in out
    assert "removed:" not in out


def test_keeps_everything_when_pypi_holds_the_version(capsys):
    gh = FakeGh()
    code, out = run(capsys, ["--tag", "v0.1.0", "--run-id", "77"], gh, pypi_with(True))
    assert code == 3 and gh.deletions() == []
    assert "kept: tag v0.1.0 and the draft: PyPI holds 0.1.0" in out
    assert "retry: gh run rerun 77 --failed" in out
    assert "the next release is a new version: PyPI holds 0.1.0" in out


def test_refuses_a_published_release(capsys):
    gh, pypi = FakeGh(release="published"), pypi_with(False)
    code, out = run(capsys, ["--tag", "v0.1.0"], gh, pypi)
    assert code == 3 and gh.deletions() == []
    assert "published" in out


def test_nothing_to_clean_exits_zero(capsys):
    gh, pypi = FakeGh(tag=False, release=None), pypi_with(False)
    code, out = run(capsys, ["--tag", "v0.0.0", "--dry-run"], gh, pypi)
    assert code == 0 and gh.deletions() == []
    assert "nothing to remove" in out
    assert pypi.asked == []


def test_a_paper_tag_never_asks_pypi(capsys):
    def pypi(version):
        raise AssertionError("a paper tag asked PyPI")

    gh = FakeGh()
    code, out = run(capsys, ["--tag", "paper-working-20261120"], gh, pypi)
    assert code == 0 and len(gh.deletions()) == 2
    assert "PyPI" not in out.split("retry:")[0]
    assert "retry: fix on `paper`, push, and push the tag again; the name is free" in out


@pytest.mark.parametrize(
    "tag", ["0.1.0", "v0.1", "vx", "paper-working-2026", "paper-final", "paper-revision-x-r0"]
)
def test_a_bad_tag_is_a_usage_error(capsys, tag):
    gh = FakeGh()
    code = rcl.main(["--repo", REPO, "--tag", tag], gh=gh, pypi=pypi_with(False), env={})
    assert code == 2 and gh.calls == []


def test_a_failed_deletion_exits_one_and_reports_what_was_removed(capsys):
    gh = FakeGh(fail_on="api -X")
    code, out = run(capsys, ["--tag", "v0.1.0"], gh, pypi_with(False))
    assert code == 1
    assert "removed: draft release v0.1.0" in out
    assert "error: could not remove tag v0.1.0" in out
    gh = FakeGh()

    def unreadable(version):
        raise rcl.Unreadable("PyPI answered 503 for 0.1.0")

    code, out = run(capsys, ["--tag", "v0.1.0"], gh, unreadable)
    assert code == 1 and gh.deletions() == [] and "error: PyPI answered 503" in out


def test_json_report_has_its_fields(capsys, tmp_path):
    report = tmp_path / "cleanup.md"
    code, out = run(
        capsys, ["--tag", "v0.1.0", "--json", "--report", str(report)], FakeGh(), pypi_with(False)
    )
    doc = json.loads(out)
    assert {"tag", "repo", "found", "removed", "kept", "retry", "exit"} <= set(doc)
    assert doc["tag"] == "v0.1.0" and doc["repo"] == REPO and doc["exit"] == code == 0
    assert doc["found"] == {
        "tag": SHA,
        "release": {"draft": True, "assets": 3},
        "pypi": False,
    }
    assert doc["removed"] == ["draft release v0.1.0", "tag v0.1.0"]
    text = report.read_text(encoding="utf-8")
    assert text.startswith("### release_cleanup: v0.1.0 in Owner/name")
    assert "- removed: tag v0.1.0" in text
