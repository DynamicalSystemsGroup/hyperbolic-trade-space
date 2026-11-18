"""The software's release workflow (specification 1.2 and 1.3, with the site-only merge of his
answer of 2026-11-16): triggers, job graph, conditions, permissions, concurrency, the failure path.

Offline: reads the workflow files only.
"""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"
TEXT = (WORKFLOWS / "release.yml").read_text(encoding="utf-8")
WF = yaml.safe_load(TEXT)
JOBS = WF["jobs"]
RELEASE = "github.event_name == 'push' && github.ref == 'refs/heads/main'"
NOT_SITE_ONLY = "needs.check.outputs.tag_state != 'site-only'"
PUBLISH_ACTION = "pypa/gh-action-pypi-publish@"


def _on(wf):
    return wf.get("on", wf.get(True))


def _conditions(wf) -> list[str]:
    """Every `if:` of a workflow, at job and step level."""
    out = []
    for job in wf.get("jobs", {}).values():
        if "if" in job:
            out.append(str(job["if"]))
        out += [str(s["if"]) for s in job.get("steps", []) if "if" in s]
    return out


def _steps(job) -> str:
    """The steps' actions, inputs and commands as one text."""
    parts = []
    for s in job.get("steps", []):
        parts += [str(s.get("uses", "")), str(s.get("run", ""))]
        parts += [f"{k}: {v}".lower() for k, v in (s.get("with") or {}).items()]
    return "\n".join(parts)


def test_release_triggers_are_pull_request_push_to_main_and_qc_and_dispatch():
    on = _on(WF)
    assert set(on) == {"pull_request", "push", "workflow_dispatch"}
    assert on["pull_request"] == {"branches": ["main"]}
    # qc/paper/** belongs to paper.yml; the release's dry run takes every other qc/** branch.
    assert on["push"] == {"branches": ["main", "qc/**", "!qc/paper/**"]}
    inputs = on["workflow_dispatch"]["inputs"]
    assert inputs["target"]["options"] == ["dry-run", "testpypi"]
    assert inputs["target"]["default"] == "dry-run"
    assert inputs["tag"]["default"] == ""
    assert "tags" not in on["push"]


def test_no_workflow_triggers_on_a_v_tag():
    for path in sorted(WORKFLOWS.glob("*.yml")):
        on = _on(yaml.safe_load(path.read_text(encoding="utf-8"))) or {}
        if isinstance(on, (str, list)):
            assert "create" not in on, path.name
            continue
        push = on.get("push") or {}
        if "tags" in push:
            assert path.name == "paper.yml" and push["tags"] == ["paper-*"], path.name
        assert "tags-ignore" not in push and "create" not in on, path.name


def test_no_job_waits_on_a_tag_event():
    for name in ("release.yml", "site.yml", "pages-deploy.yml"):
        wf = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
        guarded = [*_conditions(wf), yaml.safe_dump(_on(wf))]
        for text in guarded:
            assert "ref_type" not in text and "refs/tags/" not in text, (name, text)
        assert "github.ref_type" not in (WORKFLOWS / name).read_text(encoding="utf-8"), name


def test_release_job_graph():
    def listed(job):
        n = job.get("needs", [])
        return sorted([n] if isinstance(n, str) else n)

    needs = {job_id: listed(job) for job_id, job in JOBS.items()}
    expected = {
        # controls first (the settings against .github/governance.toml); every job needs it,
        # directly or through check.
        "controls": [],
        "check": ["controls"],
        "test": ["check"],
        "build": ["check"],
        "site": ["check"],
        "tag": ["build", "check", "controls", "site", "test"],
        "publish-pypi": ["check", "tag"],
        "publish-testpypi": ["build", "test"],
        # The site-only merge skips publish-pypi; the deploy then needs the suite and the
        # admissibility outputs directly.
        "deploy-site": ["check", "publish-pypi", "site", "test"],
        "publish-release": ["check", "deploy-site"],
        "on-failure": sorted(
            [
                "controls",
                "check",
                "test",
                "build",
                "site",
                "tag",
                "publish-pypi",
                "publish-testpypi",
                "deploy-site",
                "publish-release",
            ]
        ),
    }
    assert needs == expected
    assert JOBS["check"]["name"] == "admissibility"
    outputs = JOBS["check"]["outputs"]
    assert set(outputs) == {"version", "tag", "tag_state"}
    steps = _steps(JOBS["check"])
    for command in (
        "scripts/check_release_version.py",
        "release_checks.py tag --tag",
        "release_checks.py changelog",
        "release_checks.py version-kind",
        "uv lock --check",
        "release_checks.py pins",
        "scripts/paper_mode.py check --stage served",
        "release_checks.py merge --sha",
        "gh run list",
    ):
        assert command in steps, command
    assert "fetch-depth: 0" in steps


def test_release_steps_run_only_on_a_push_to_main():
    for job_id in ("tag", "publish-pypi", "deploy-site", "publish-release"):
        assert RELEASE in JOBS[job_id]["if"], job_id
    # The tag, PyPI and the release's publication are skipped on a site-only merge.
    for job_id in ("tag", "publish-pypi"):
        assert NOT_SITE_ONLY in JOBS[job_id]["if"], job_id
    steps = JOBS["publish-release"]["steps"]
    publish = next(s for s in steps if "--draft=false" in s.get("run", ""))
    assert publish["if"] == NOT_SITE_ONLY
    # The deploy runs on a site-only merge with publish-pypi skipped, never after a failure.
    deploy = JOBS["deploy-site"]["if"]
    assert "needs.check.outputs.tag_state == 'site-only'" in deploy
    assert "needs.publish-pypi.result == 'skipped'" in deploy
    assert "needs.publish-pypi.result == 'success'" in deploy
    assert "!cancelled()" in deploy and "always()" not in deploy
    for need in ("check", "test", "site"):
        assert f"needs.{need}.result == 'success'" in deploy, need
    # The changelog check is skipped on a site-only merge; the merge check runs on a release only.
    check = {s.get("name", ""): s for s in JOBS["check"]["steps"]}
    changelog = next(s for n, s in check.items() if "changelog" in n)
    assert changelog["if"] == "steps.tag.outputs.tag_state != 'site-only'"
    merge = next(s for s in check.values() if "release_checks.py merge" in s.get("run", ""))
    assert merge["if"] == RELEASE
    # The dry-run path: the suite on main, qc/** and a testpypi dispatch; build and site everywhere
    # but on a pull request.
    assert "startsWith(github.ref, 'refs/heads/qc/')" in JOBS["test"]["if"]
    assert "inputs.target == 'testpypi'" in JOBS["test"]["if"]
    for job_id in ("build", "site"):
        assert JOBS[job_id]["if"] == "${{ github.event_name != 'pull_request' }}", job_id


def test_pypi_jobs_are_jobs_of_release_yml():
    for job_id, env, extra in (
        ("publish-pypi", "pypi", "skip-existing: true"),
        ("publish-testpypi", "testpypi", "repository-url: https://test.pypi.org/legacy/"),
    ):
        job = JOBS[job_id]
        assert "uses" not in job, job_id
        assert job["environment"]["name"] == env
        assert job["permissions"]["id-token"] == "write"
        steps = _steps(job)
        assert PUBLISH_ACTION in steps and extra in steps, job_id
    assert JOBS["publish-pypi"]["environment"]["url"] == "https://pypi.org/p/tradespace"
    steps = JOBS["publish-pypi"]["steps"]
    publish = next(i for i, s in enumerate(steps) if PUBLISH_ACTION in s.get("uses", ""))
    hashes = next(i for i, s in enumerate(steps) if "release_checks.py pypi" in s.get("run", ""))
    assert publish < hashes


def test_site_jobs_are_called_workflows():
    assert JOBS["site"]["uses"] == "./.github/workflows/site.yml"
    assert JOBS["deploy-site"]["uses"] == "./.github/workflows/pages-deploy.yml"
    assert JOBS["deploy-site"]["permissions"] == {"pages": "write", "id-token": "write"}
    assert JOBS["test"]["uses"] == "./.github/workflows/test.yml"
    assert JOBS["test"]["with"] == {"windows": False, "controls": False}
    for job_id in ("site", "deploy-site", "test"):
        assert "environment" not in JOBS[job_id], job_id
    for name in ("site.yml", "pages-deploy.yml", "test.yml"):
        assert (WORKFLOWS / name).is_file(), name


def test_on_failure_cleans_up_and_opens_an_issue():
    job = JOBS["on-failure"]
    assert job["if"] == (
        "${{ always() && (failure() || cancelled()) && github.event_name == 'push' "
        "&& github.ref == 'refs/heads/main' }}"
    )
    assert job["permissions"] == {"contents": "write", "issues": "write", "actions": "read"}
    steps = _steps(job)
    assert "gh run view" in steps and "GITHUB_STEP_SUMMARY" in steps
    assert re.search(r"scripts/release_cleanup\.py --tag \"v\$VERSION\"", steps)
    assert "--run-id" in steps and "--report cleanup.md" in steps
    assert "gh label create release-failure" in steps
    assert "gh issue create" in steps and "gh issue comment" in steps
    assert "--label release-failure" in steps
    # The issue is closed by the next successful run of the version.
    closing = _steps(JOBS["publish-release"])
    assert "gh issue close" in closing and "release-failure" in closing
    assert JOBS["publish-release"]["permissions"] == {"contents": "write", "issues": "write"}


def test_top_level_permissions_read_only():
    assert WF["permissions"] == {"contents": "read"}
    for job_id, job in JOBS.items():
        perms = job.get("permissions", {})
        if job_id not in ("tag", "publish-release", "on-failure"):
            assert perms.get("contents") in (None, "read"), job_id
    assert JOBS["tag"]["permissions"] == {"contents": "write"}


def test_concurrency_never_cancels_a_release():
    c = WF["concurrency"]
    assert c["cancel-in-progress"] == "${{ github.event_name == 'pull_request' }}"
    assert "format('release-pr-{0}', github.event.pull_request.number)" in c["group"]
    assert "format('release-{0}', github.ref)" in c["group"]


def test_pages_yml_is_gone():
    assert not (WORKFLOWS / "pages.yml").exists()
    assert "pages.yml" not in TEXT
