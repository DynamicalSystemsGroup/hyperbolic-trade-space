"""The paper's release control model (WP65 specification, sections 2, 3.1 and 5): the mode file and
its validation, the tag shapes, the key manifest, the link pinning, the pin tooling, the paper's
workflow and the cut that keeps the paper's tests out of the software's gate.

The tests marked ``paper`` read the paper itself (its notebooks, its build, its theme) and run in
the paper's workflow; the rest are the model's form and run in the software's gate.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "paper"))

import build_keys  # noqa: E402
import paper_mode  # noqa: E402
import paper_pin  # noqa: E402
import pin_links  # noqa: E402

WORKFLOW_FILE = ROOT / ".github" / "workflows" / "paper.yml"
ABSTRACT = dict(schema=1, mode="abstract", pin="", venue="", round=0, date="", doi="", sha256="")
WORKING = {
    **ABSTRACT,
    "mode": "working",
    "pin": "paper-working-20261120",
    "date": "2026-11-20",
    "doi": "10.5281/zenodo.123",
    "sha256": "0" * 64,
}
SUBMITTED = {**WORKING, "mode": "submitted", "pin": "paper-submitted-ieee-tse", "venue": "ieee-tse"}
REVISION = {
    **SUBMITTED,
    "mode": "revision",
    "pin": "paper-revision-ieee-tse-r2",
    "round": 2,
}


def _write_mode(path: Path, fields: dict, raw: str | None = None) -> Path:
    if raw is None:
        raw = "\n".join(
            f"{k} = {v}" if isinstance(v, int) else f"{k} = {json.dumps(v)}"
            for k, v in fields.items()
        )
    path.write_text(raw + "\n", encoding="utf-8")
    return path


# --- the mode file (3.1) -------------------------------------------------------------------------


def test_mode_file_is_valid_for_serving(capsys):
    assert paper_mode.main(["check", "--stage", "served"]) == 0, capsys.readouterr().out
    assert capsys.readouterr().out.startswith("paper_mode: ok ")
    fields = paper_mode.load()
    assert (ROOT / "paper" / "mode.toml").read_text(encoding="utf-8") == paper_mode.render(fields)


@pytest.mark.parametrize("good", [ABSTRACT, WORKING, SUBMITTED, REVISION], ids=lambda f: f["mode"])
def test_every_mode_has_a_valid_served_form(tmp_path, good, capsys):
    path = _write_mode(tmp_path / "mode.toml", good)
    assert paper_mode.main(["check", "--stage", "served", "--file", str(path)]) == 0
    assert paper_mode.main(["check", "--stage", "tag", "--file", str(path)]) == 0
    capsys.readouterr()


BROKEN = [
    # (name, fields, stage, extra argv, the field named)
    ("schema", {**ABSTRACT, "schema": 2}, "tag", [], "schema"),
    ("unknown-key", {**ABSTRACT, "colour": "red"}, "tag", [], "colour"),
    ("missing-key", {k: v for k, v in ABSTRACT.items() if k != "doi"}, "tag", [], "doi"),
    ("type", {**ABSTRACT, "round": "0"}, "tag", [], "round"),
    ("mode", {**ABSTRACT, "mode": "forthcoming"}, "tag", [], "mode"),
    ("abstract-pin", {**ABSTRACT, "pin": "paper-working-20261120"}, "tag", [], "pin"),
    ("abstract-round", {**ABSTRACT, "round": 1}, "tag", [], "round"),
    ("abstract-doi", {**ABSTRACT, "doi": "10.5281/zenodo.1"}, "tag", [], "doi"),
    ("pin-shape", {**WORKING, "pin": "paper-submitted-ieee"}, "tag", [], "pin"),
    ("pin-v", {**WORKING, "pin": "v0.1.0"}, "tag", [], "pin"),
    ("venue-of-tag", {**SUBMITTED, "venue": "acm"}, "tag", [], "venue"),
    ("venue-in-working", {**WORKING, "venue": "ieee"}, "tag", [], "venue"),
    ("round-of-tag", {**REVISION, "round": 3}, "tag", [], "round"),
    ("round-in-submitted", {**SUBMITTED, "round": 1}, "tag", [], "round"),
    ("date-iso", {**SUBMITTED, "date": "20261120"}, "tag", [], "date"),
    ("date-real", {**SUBMITTED, "date": "2026-02-30"}, "tag", [], "date"),
    ("date-of-working-tag", {**WORKING, "date": "2026-11-21"}, "tag", [], "date"),
    ("tag-names-pin", WORKING, "tag", ["--tag", "paper-working-20261121"], "pin"),
    ("tag-in-abstract", ABSTRACT, "tag", ["--tag", "paper-working-20261120"], "pin"),
    ("doi-form", {**WORKING, "doi": "10.1234/x"}, "tag", [], "doi"),
    ("sha256-form", {**WORKING, "sha256": "ABC"}, "tag", [], "sha256"),
    ("doi-served", {**WORKING, "doi": ""}, "served", [], "doi"),
    ("sha256-served", {**REVISION, "sha256": ""}, "served", [], "sha256"),
]


@pytest.mark.parametrize(
    "fields, stage, extra, field", [b[1:] for b in BROKEN], ids=[b[0] for b in BROKEN]
)
def test_each_broken_mode_field_is_named(tmp_path, capsys, fields, stage, extra, field):
    path = _write_mode(tmp_path / "mode.toml", fields)
    code = paper_mode.main(["check", "--stage", stage, "--file", str(path), *extra])
    out = capsys.readouterr().out
    assert code == 1, out
    assert f"paper_mode: {field}: " in out, out


def test_the_tag_stage_admits_an_empty_doi_and_checksum(tmp_path, capsys):
    path = _write_mode(tmp_path / "mode.toml", {**WORKING, "doi": "", "sha256": ""})
    assert paper_mode.main(["check", "--stage", "tag", "--file", str(path)]) == 0
    assert paper_mode.main(["check", "--stage", "served", "--file", str(path)]) == 1
    capsys.readouterr()


def test_mode_usage_errors_exit_two(tmp_path, capsys):
    assert paper_mode.main(["check", "--file", str(tmp_path / "absent.toml")]) == 2
    with pytest.raises(SystemExit) as exc:
        paper_mode.main(["check", "--stage", "draft"])
    assert exc.value.code == 2
    capsys.readouterr()


def test_show_prints_the_fields_and_the_banner(tmp_path, capsys):
    path = _write_mode(tmp_path / "mode.toml", REVISION)
    assert paper_mode.main(["show", "--json", "--file", str(path)]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["banner"] == (
        "Revision 2 for ieee-tse · paper-revision-ieee-tse-r2 · 2026-11-20 · DOI 10.5281/zenodo.123"
    )
    assert paper_mode.banner(SUBMITTED).startswith("Submitted to ieee-tse · ")
    assert paper_mode.banner(ABSTRACT) == ""


# --- the tag shapes (2.3) ------------------------------------------------------------------------

TAGS = {
    "paper-working-20261120": ("working", {"date": "20261120"}),
    "paper-working-20261120-2": ("working", {"date": "20261120", "n": "2"}),
    "paper-working-20261120-12": ("working", {"date": "20261120", "n": "12"}),
    "paper-submitted-ieee-tse": ("submitted", {"venue": "ieee-tse"}),
    "paper-revision-ieee-tse-r2": ("revision", {"venue": "ieee-tse", "round": "2"}),
    "paper-revision-ieee-tse-r10": ("revision", {"venue": "ieee-tse", "round": "10"}),
}
NOT_TAGS = [
    "v0.1.0",
    "paper-working-2026112",
    "paper-working-20261120-1",
    "paper-working-20261120-02",
    "paper-submitted-IEEE",
    "paper-submitted-ieee-",
    "paper-revision-ieee-r0",
    "paper-revision-ieee",
    "paper-abstract",
    "paper-",
]


def test_tag_shapes_parse(capsys):
    for tag, want in TAGS.items():
        assert paper_mode.parse_tag(tag) == want, tag
        assert paper_mode.main(["parse", tag]) == 0
        assert capsys.readouterr().out.split()[0] == want[0]
    for tag in NOT_TAGS:
        assert paper_mode.parse_tag(tag) is None, tag
        assert paper_mode.main(["parse", tag]) == 2, tag
    capsys.readouterr()


def test_no_paper_tag_matches_v_star():
    """The paper's tags and the software's `v` tags never share a name (C13)."""
    for shape in paper_mode.TAG_SHAPES.values():
        assert shape.pattern.startswith("^paper-"), shape.pattern
    for tag in TAGS:
        assert not fnmatch.fnmatch(tag, "v*") and fnmatch.fnmatch(tag, "paper-*")
    assert not fnmatch.fnmatch("v0.1.0", "paper-*")


# --- the key manifest (2.6, 4) -------------------------------------------------------------------

MANIFEST = ROOT / "paper" / "paper-keys.json"


def test_key_manifest_is_canonical():
    text = MANIFEST.read_text(encoding="utf-8")
    assert build_keys.manifest_problems(text) == []
    doc = json.loads(text)
    assert doc["schema"] == 1 and list(doc) == ["schema", "keys"]
    keys = doc["keys"]
    assert keys and list(keys) == sorted(keys)
    assert set(keys.values()) <= {"paper/", "paper/supporting-material/"}
    assert all(re.fullmatch(r"[A-Za-z0-9_-]+", k) for k in keys)
    assert MANIFEST.read_bytes() == build_keys.render(keys).encode("utf-8")
    assert MANIFEST.read_bytes().endswith(b"}\n") and not MANIFEST.read_bytes().endswith(b"\n\n")


@pytest.mark.parametrize(
    "text, problem",
    [
        ('{"schema": 2, "keys": {"a": "paper/"}}', "schema"),
        ('{"schema": 1, "keys": {}}', "non-empty"),
        ('{"schema": 1, "keys": {"a b": "paper/"}}', "is not"),
        ('{"schema": 1, "keys": {"a": "docs/"}}', "route"),
        ('{"schema": 1, "keys": {"b": "paper/", "a": "paper/"}}', "sorted"),
        ('{"schema": 1, "keys": {"a": "paper/"}}', "canonical"),
        ('{"keys": {"a": "paper/"}, "schema": 1}', "canonical"),
        ('{"schema": 1, "keys": {"a": "paper/"}, "x": 0}', "exactly"),
    ],
)
def test_a_broken_manifest_is_named(text, problem):
    assert any(problem in p for p in build_keys.manifest_problems(text))


def _notebook(path: Path, sources: list[str]) -> None:
    cells = [{"cell_type": "markdown", "metadata": {}, "source": [s]} for s in sources]
    nb = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    path.write_text(json.dumps(nb), encoding="utf-8")


def test_build_keys_writes_checks_and_names_the_difference(tmp_path, capsys):
    _notebook(tmp_path / "paper.ipynb", [":::{prf:theorem}\n:label: thm-a\n:::", "(sec-b)=\n# B"])
    _notebook(tmp_path / "supporting_material.ipynb", ["(appendix-c)=\n# C"])
    argv = ["--paper-dir", str(tmp_path)]
    assert build_keys.main(["--check", *argv]) == 1  # no manifest yet
    assert build_keys.main(argv) == 0
    written = json.loads((tmp_path / "paper-keys.json").read_text(encoding="utf-8"))
    assert written["keys"] == {
        "appendix-c": "paper/supporting-material/",
        "sec-b": "paper/",
        "thm-a": "paper/",
    }
    assert build_keys.main(["--check", *argv]) == 0
    _notebook(tmp_path / "paper.ipynb", ["(sec-b)=\n# B", "(appendix-c-moved)=\n# M"])
    _notebook(tmp_path / "supporting_material.ipynb", ["(sec-x)=\n# X"])
    capsys.readouterr()
    assert build_keys.main(["--check", *argv]) == 1
    out = capsys.readouterr().out
    assert "added: appendix-c-moved" in out and "removed: thm-a" in out
    _notebook(tmp_path / "supporting_material.ipynb", ["(sec-b)=\n# B again"])
    assert build_keys.main(["--check", *argv]) == 2  # a key defined in two pages


def test_build_keys_xref_names_each_miss(tmp_path, capsys):
    xref = tmp_path / "myst.xref.json"
    refs = [
        {"identifier": "thm-a", "url": "/hyperbolic-trade-space/paper/"},
        {"identifier": "appendix-c", "url": "/hyperbolic-trade-space/paper/supporting-material"},
        {"identifier": "sec-b", "url": "/hyperbolic-trade-space/paper/supporting-material"},
    ]
    xref.write_text(json.dumps({"references": refs}), encoding="utf-8")
    keys = {"thm-a": "paper/", "appendix-c": "paper/supporting-material/", "sec-b": "paper/"}
    misses = build_keys.xref_misses(keys, xref, "/hyperbolic-trade-space/paper")
    assert misses == ["sec-b: on paper/ by the manifest, '/supporting-material' in the built paper"]
    assert build_keys.xref_misses({"gone": "paper/"}, xref)[0].startswith("gone: ")


@pytest.mark.paper
def test_key_manifest_equals_the_notebooks_labels(capsys):
    assert build_keys.main(["--check"]) == 0, capsys.readouterr().out


@pytest.mark.paper
@pytest.mark.slow
@pytest.mark.skipif(
    not os.environ.get("PAPER_BUILD") or shutil.which("node") is None,
    reason="set PAPER_BUILD=1 with Node 22 or newer on PATH (the first build needs the network)",
)
def test_key_manifest_equals_the_built_paper_labels(tmp_path):
    """Each key of the manifest is an identifier on the page its route names in the built paper
    (moved from tests/test_site.py; built here, in a copy, so no earlier build is relied on)."""
    work = tmp_path / "paper"
    (tmp_path / "docs").mkdir()
    shutil.copy(ROOT / "docs" / "references.bib", tmp_path / "docs" / "references.bib")
    shutil.copytree(ROOT / "paper", work, ignore=shutil.ignore_patterns("_build", "__pycache__"))
    out = subprocess.run(
        [str(ROOT / ".venv" / "bin" / "myst"), "build", "--html"],
        capture_output=True,
        text=True,
        cwd=work,
        check=False,
    )
    assert out.returncode == 0, out.stdout[-2000:] + out.stderr[-2000:]
    xref = work / "_build" / "html" / "myst.xref.json"
    keys = json.loads(MANIFEST.read_text(encoding="utf-8"))["keys"]
    assert build_keys.xref_misses(keys, xref, os.environ.get("BASE_URL", "")) == []


@pytest.mark.paper
def test_paper_theme_is_pinned_to_a_commit():
    """A clean checkout must build the paper on the theme it was reviewed on (WP8b D-8): the
    article theme is a commit-pinned archive, not the name that follows the main branch (moved
    from tests/test_site.py)."""
    myst = yaml.safe_load((ROOT / "paper" / "myst.yml").read_text(encoding="utf-8"))
    template = myst["site"]["template"]
    assert re.fullmatch(
        r"https://github\.com/myst-templates/article-theme/archive/[0-9a-f]{40}\.zip", template
    ), template


# --- the paper's workflow (2.2) ------------------------------------------------------------------


@pytest.fixture(scope="module")
def workflow() -> dict:
    return yaml.safe_load(WORKFLOW_FILE.read_text(encoding="utf-8"))


def _runs(job: dict) -> str:
    return "\n".join(step.get("run", "") for step in job["steps"])


def _uses(job: dict) -> list[str]:
    return [step["uses"].split("@")[0] for step in job["steps"] if "uses" in step]


def test_paper_workflow_triggers_and_tag_filter(workflow):
    triggers = workflow.get("on", workflow.get(True))
    assert set(triggers) == {"push", "workflow_dispatch"}
    assert triggers["push"] == {"branches": ["paper", "qc/paper/**"], "tags": ["paper-*"]}
    assert not triggers["workflow_dispatch"]  # no inputs
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"] == {
        "group": "paper-${{ github.ref }}",
        "cancel-in-progress": "${{ github.ref_type == 'branch' }}",
    }
    assert workflow["env"] == {
        "HTS_PAPER_TESTS": "1",
        "PAPER_EXECUTE": "1",
        "PAPER_BUILD": "1",
        "REQUIRE_OPENSYSML": "1",
        "BASE_URL": "/hyperbolic-trade-space/paper",
    }
    build = workflow["jobs"]["build"]
    runs = _runs(build)
    for needle in (
        'git merge-base --is-ancestor "$GITHUB_SHA" origin/paper',
        'paper_mode.py check --stage tag --tag "$GITHUB_REF_NAME"',
        "uv lock --check",
        "uv sync --locked",
        "scripts/build_generated.py",
        "uv run pytest -q -n auto --dist loadgroup -m paper",
        "uv run myst build --html",
        "paper/build_keys.py --check --xref paper/_build/html/myst.xref.json",
        'paper/pin_links.py --ref "$GITHUB_REF_NAME" paper/_build/html',
        "co-authored-by",
    ):
        assert needle in runs, needle
    assert "actions/setup-node" in _uses(build)
    node = next(s for s in build["steps"] if s.get("uses", "").startswith("actions/setup-node"))
    assert node["with"]["node-version"] == "22"
    test_yml = yaml.safe_load((ROOT / ".github" / "workflows" / "test.yml").read_text("utf-8"))

    def attribution(job):
        return next(s["run"] for s in job["steps"] if "co-authored-by" in s.get("run", ""))

    assert attribution(build) == attribution(test_yml["jobs"]["test"]), "test.yml's, verbatim"


def test_paper_workflow_release_job_publishes_two_assets_from_a_draft(workflow):
    build = workflow["jobs"]["build"]
    upload = next(s for s in build["steps"] if "upload-artifact" in s.get("uses", ""))
    assert upload["with"]["name"] == "paper-release"
    assert upload["with"]["path"].split() == ["paper-html.tar.gz", "paper-keys.json"]
    assert "tar -czf paper-html.tar.gz -C paper/_build/html ." in _runs(build)
    release = workflow["jobs"]["release"]
    assert release["needs"] == "build" and release["if"] == "github.ref_type == 'tag'"
    assert release["permissions"] == {"contents": "write"}
    assert release["environment"] == "paper-release"
    runs = _runs(release)
    create = runs.index(
        'gh release create "$TAG" paper-html.tar.gz paper-keys.json --draft --verify-tag'
    )
    assert "--latest=false" in runs[create : create + 200]
    view = runs.index('gh release view "$TAG" --json assets')
    publish = runs.index('gh release edit "$TAG" --draft=false')
    assert create < view < publish
    assert "paper_mode.py show --json" in runs and "uv.lock" in runs and "CHANGES.md" in runs
    assert "git describe --tags --match 'v*' --abbrev=12" in runs


def test_paper_workflow_never_deploys(workflow):
    text = WORKFLOW_FILE.read_text(encoding="utf-8")
    for forbidden in ("deploy-pages", "upload-pages-artifact", "pages: write", "git push"):
        assert forbidden not in text, forbidden
    for name, job in workflow["jobs"].items():
        perms = job.get("permissions", {})
        assert "pages" not in perms and "id-token" not in perms, name
        assert "uses" not in job, name  # no called workflow
    assert workflow["jobs"]["build"]["permissions"] == {"contents": "read"}


def test_paper_workflow_failure_runs_the_cleanup(workflow):
    job = workflow["jobs"]["on-failure"]
    assert job["needs"] == ["build", "release"]
    assert job["if"] == ("always() && (failure() || cancelled()) && github.ref_type == 'tag'")
    assert job["permissions"] == {"contents": "write", "issues": "write", "actions": "read"}
    runs = _runs(job)
    for needle in (
        'gh run view "$GITHUB_RUN_ID" --json jobs',
        'scripts/release_cleanup.py --tag "$TAG"',
        '--run-id "$GITHUB_RUN_ID" --report cleanup.md',
        'title="Paper release $TAG failed"',
        'gh issue create --title "$title" --label release-failure',
        "gh label create release-failure",
        "$GITHUB_STEP_SUMMARY",
    ):
        assert needle in runs, needle


# --- the link pinning (2.7) ----------------------------------------------------------------------


def test_pin_links_rewrites_blob_main_to_the_tag(tmp_path, capsys):
    repo = pin_links.REPO
    (tmp_path / "sub").mkdir()
    (tmp_path / "index.html").write_text(
        f'<a href="{repo}/blob/main/src/a.py">a</a> <a href="{repo}/tree/main/docs/">d</a>',
        encoding="utf-8",
    )
    (tmp_path / "sub" / "page.json").write_text(
        json.dumps({"url": f"{repo}/blob/main/README.md"}), encoding="utf-8"
    )
    other = f"{repo}/blob/main/x.txt"
    (tmp_path / "notes.txt").write_text(other, encoding="utf-8")
    (tmp_path / "plain.html").write_text("<p>no links</p>", encoding="utf-8")
    tag = "paper-working-20261120"
    assert pin_links.main(["--ref", tag, str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "index.html: 2" in out and "sub/page.json: 1" in out and "plain.html" not in out
    html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert f"{repo}/blob/{tag}/src/a.py" in html and f"{repo}/tree/{tag}/docs/" in html
    assert "/main/" not in html
    assert f"/blob/{tag}/README.md" in (tmp_path / "sub" / "page.json").read_text(encoding="utf-8")
    assert (tmp_path / "notes.txt").read_text(encoding="utf-8") == other  # neither html nor json
    assert pin_links.main(["--ref", tag, str(tmp_path)]) == 1  # nothing left to replace
    assert pin_links.main(["--ref", tag, str(tmp_path / "absent")]) == 2


# --- the pin tooling (2.4) -----------------------------------------------------------------------


def test_paper_pin_prepare_and_record_write_the_mode_file(tmp_path, capsys):
    path = tmp_path / "mode.toml"
    path.write_text(paper_mode.render(ABSTRACT), encoding="utf-8")
    tag = "paper-revision-ieee-tse-r2"
    argv = ["--file", str(path)]

    before = path.read_bytes()
    prepare = ["prepare", "--tag", tag, "--date", "2026-12-01", *argv]
    assert paper_pin.main([*prepare, "--dry-run"]) == 0
    assert path.read_bytes() == before and 'pin = "paper-revision-ieee-tse-r2"' in (
        capsys.readouterr().out
    )
    assert paper_pin.main(prepare) == 0
    fields = paper_mode.load(path)
    assert fields == {
        **ABSTRACT,
        "mode": "revision",
        "pin": tag,
        "venue": "ieee-tse",
        "round": 2,
        "date": "2026-12-01",
    }
    assert paper_mode.main(["check", "--stage", "tag", "--tag", tag, *argv]) == 0
    assert paper_mode.main(["check", "--stage", "served", *argv]) == 1

    asset = b"the built paper"
    calls = []

    def fake_gh(args):
        calls.append(args)
        out = Path(args[args.index("--dir") + 1])
        (out / "paper-html.tar.gz").write_bytes(asset)
        return 0

    doi = "10.5281/zenodo.4242"
    record = ["record", "--tag", tag, "--doi", doi, "--repo", "o/r", *argv]
    assert paper_pin.main(record, gh=fake_gh) == 0
    assert calls[0][:3] == ["release", "download", tag] and calls[0][-2:] == ["--repo", "o/r"]
    fields = paper_mode.load(path)
    assert fields["doi"] == doi and fields["sha256"] == hashlib.sha256(asset).hexdigest()
    assert paper_mode.main(["check", "--stage", "served", "--tag", tag, *argv]) == 0
    capsys.readouterr()

    # the failures: another tag, a download that fails, a malformed DOI, a working date that
    # differs from the tag's, a tag of no shape
    other = ["record", "--tag", "paper-submitted-x", "--doi", doi, *argv]
    assert paper_pin.main(other, gh=fake_gh) == 1
    assert paper_pin.main(record, gh=lambda args: 1) == 1
    assert paper_pin.main([*record[:4], "10.1/x", *record[5:]], gh=fake_gh) == 1
    working = ["prepare", "--tag", "paper-working-20261120", "--date", "2026-11-21", *argv]
    assert paper_pin.main(working) == 1
    assert paper_mode.load(path)["pin"] == tag  # nothing written by a failed check
    assert paper_pin.main(["prepare", "--tag", "v0.1.0", *argv]) == 2
    capsys.readouterr()


# --- the cut (5.1) -------------------------------------------------------------------------------

PLANTED_TESTS = """
import pytest

def test_software():
    pass

@pytest.mark.paper
def test_paper():
    pass
"""
PLANTED_MODULE = """
import pytest

pytestmark = pytest.mark.paper

def test_in_a_paper_module():
    pass
"""


def test_paper_tests_are_deselected_without_the_switch(pytester, monkeypatch):
    pytester.makeconftest((ROOT / "tests" / "conftest.py").read_text(encoding="utf-8"))
    pytester.makepyfile(test_mixed=PLANTED_TESTS, test_paper_module=PLANTED_MODULE)
    monkeypatch.delenv("HTS_PAPER_TESTS", raising=False)
    result = pytester.runpytest("-p", "no:cacheprovider", "-p", "no:randomly")
    result.assert_outcomes(passed=1, deselected=2)
    result = pytester.runpytest("-p", "no:cacheprovider", "-m", "paper")
    result.assert_outcomes(deselected=3)
    monkeypatch.setenv("HTS_PAPER_TESTS", "1")
    result = pytester.runpytest("-p", "no:cacheprovider")
    result.assert_outcomes(passed=3)
    result = pytester.runpytest("-p", "no:cacheprovider", "-m", "paper")
    result.assert_outcomes(passed=2, deselected=1)
    monkeypatch.setenv("HTS_PAPER_TESTS", "0")
    pytester.runpytest("-p", "no:cacheprovider").assert_outcomes(passed=1, deselected=2)
