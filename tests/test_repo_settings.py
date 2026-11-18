"""The settings checker (`scripts/check_repo_settings.py`) on recorded responses: the conforming
fixture passes; each kind of drift is named; an unreadable endpoint exits 2; the declaration's
governed files and GOVERNANCE.md's agree; the `controls` job is first in both workflows."""

import copy
import glob
import importlib.util
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "data" / "wp78"
WORKFLOWS = ROOT / ".github" / "workflows"
spec = importlib.util.spec_from_file_location("crs", ROOT / "scripts" / "check_repo_settings.py")
crs = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = crs  # dataclasses resolve the module by name
spec.loader.exec_module(crs)

DECLARATION = crs.load_declaration(crs.DECLARATION)
OWNERS = crs.code_owners(ROOT / ".github" / "CODEOWNERS")
APPROVERS = crs.paper_approvers(ROOT / ".github" / "CODEOWNERS")
# the fixture's fields: 61 at WP78; 64 with the paper approvers (WP79: their row and two logins);
# 69 with the governance-files push ruleset (WP82: target, enforcement, bypass actors, rules,
# paths); 70 with the general settings' delete_branch_on_merge (WP82 Amendment 3)
FIELDS = 70
LOCAL_ONLY = 7  # five rulesets' bypass actors and the two workflow-permission fields


@pytest.fixture
def payloads():
    return copy.deepcopy(crs.load_fixture(FIXTURE))


def compare(payloads, declaration=DECLARATION, owners=OWNERS, approvers=APPROVERS, runner=False):
    return crs.Comparison(
        declaration, crs.dict_fetch(payloads), owners, runner=runner, approvers=approvers
    ).run()


def ruleset(payloads, name):
    rid = next(r["id"] for r in payloads["rulesets"] if r["name"] == name)
    return payloads[f"rulesets/{rid}"]


def environment(payloads, name):
    return next(e for e in payloads["environments"]["environments"] if e["name"] == name)


def test_the_conforming_fixture_passes(tmp_path, capsys):
    report = tmp_path / "report.md"
    code = crs.main(["--fixture", str(FIXTURE), "--report", str(report)])
    assert code == 0
    out = capsys.readouterr().out
    assert out.strip().endswith(f"conforming ({FIELDS} fields)")
    text = report.read_text(encoding="utf-8")
    assert f"**conforming ({FIELDS} fields)**" in text and "differs" not in text
    assert "| `environments.paper-release.reviewers` |" in text
    approvers = '| `paper_approvers` | `"at least one login"` | `["jshorish", "mzargham"]` | ok |'
    assert approvers in text
    assert '| `paper_approvers.jshorish.permission` | `"read or more"` | `"write"` | ok |' in text


def test_a_missing_required_check_is_named(payloads):
    rule = next(
        r
        for r in ruleset(payloads, "main-checks")["rules"]
        if r["type"] == "required_status_checks"
    )
    rule["parameters"]["required_status_checks"] = [
        c for c in rule["parameters"]["required_status_checks"] if c["context"] != "admissibility"
    ]
    result = compare(payloads)
    assert result.exit_code == 1
    (line,) = result.lines()
    assert line.startswith(
        "rulesets.main-checks.rules.required_status_checks.required_status_checks:"
    )
    assert (
        '"admissibility"' in line.split("found")[0]
        and '"admissibility"' not in line.split("found")[1]
    )


def test_an_extra_bypass_actor_is_named(payloads):
    ruleset(payloads, "dev")["bypass_actors"].append(
        {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
    )
    result = compare(payloads)
    assert result.exit_code == 1
    assert result.lines() == [
        'rulesets.dev.bypass_actors: expected [], found ["RepositoryRole:5:always"]'
    ]


def test_a_changed_reviewer_is_named(payloads):
    rule = next(
        r
        for r in environment(payloads, "paper-release")["protection_rules"]
        if r["type"] == "required_reviewers"
    )
    rule["reviewers"][1]["reviewer"]["login"] = "someone"
    result = compare(payloads)
    assert result.exit_code == 1
    (line,) = result.lines()
    assert line.startswith("environments.paper-release.reviewers: expected")
    assert '"someone"' in line and '"jshorish"' in line


def test_a_policy_on_the_wrong_branch_is_named(payloads):
    payloads["environments/pypi/deployment-branch-policies"]["branch_policies"][0]["name"] = "dev"
    result = compare(payloads)
    assert result.exit_code == 1
    assert result.lines() == [
        'environments.pypi.policies: expected ["branch:main"], found ["branch:dev"]'
    ]


def test_a_code_owner_without_write_access_is_named(payloads):
    payloads["collaborators/rororowyourboat/permission"]["permission"] = "read"
    result = compare(payloads)
    assert result.exit_code == 1
    assert result.lines() == [
        'code_owners.rororowyourboat.permission: expected "write or more", found "read"'
    ]
    # maintain is reported as write by the API and is enough; admin is more.
    payloads["collaborators/rororowyourboat/permission"]["permission"] = "admin"
    assert compare(payloads).exit_code == 0


def test_a_paper_approver_without_read_access_is_named(payloads):
    """The paper/ line of CODEOWNERS (WP79): read is enough to approve; none is a difference, and
    the code owners' minimum (write) is not asked of an approver who is not a code owner."""
    assert DECLARATION["paper_approvers"]["minimum_permission"] == "read"
    payloads["collaborators/jshorish/permission"]["permission"] = "none"
    result = compare(payloads)
    assert result.exit_code == 1
    assert result.lines() == [
        'paper_approvers.jshorish.permission: expected "read or more", found "none"'
    ]
    payloads["collaborators/jshorish/permission"]["permission"] = "read"
    assert compare(payloads).exit_code == 0
    # the approvers are read from the paper/ line, not the * line, and jshorish is no code owner
    assert {"mzargham", "jshorish"} == APPROVERS and "jshorish" not in OWNERS
    assert compare(payloads, approvers=set()).lines() == [
        'paper_approvers: expected "at least one login", found []'
    ]
    # a declaration without the section checks no approver
    without = copy.deepcopy(DECLARATION)
    del without["paper_approvers"]
    result = compare(payloads, declaration=without)
    assert result.exit_code == 0 and len(result.rows) == FIELDS - 3
    assert not any(r.path.startswith("paper_approvers") for r in result.rows)


def test_an_extra_or_missing_ruleset_or_environment_is_named(payloads):
    payloads["rulesets"].append({"id": 1, "name": "stray"})
    payloads["environments"]["environments"].pop()
    result = compare(payloads)
    assert result.exit_code == 1
    lines = result.lines()
    assert any(ln.startswith("rulesets: expected") and '"stray"' in ln for ln in lines)
    assert any(ln.startswith("environments: expected") and '"testpypi"' in ln for ln in lines)


def test_an_unreadable_endpoint_exits_2_and_is_named(payloads, tmp_path, capsys):
    del payloads["actions/permissions/workflow"]
    result = compare(payloads)
    assert result.exit_code == 2
    assert result.lines() == ["unreadable: actions/permissions/workflow (no recorded response)"]
    # every other field is still compared, so one unreadable endpoint hides nothing
    assert len(result.rows) == FIELDS - 2 and not result.differences
    # the same through the command line, from a fixture directory missing the file
    for path in FIXTURE.glob("*.json"):
        if path.name != "actions__permissions__workflow.json":
            (tmp_path / path.name).write_bytes(path.read_bytes())
    report = tmp_path / "r.md"
    assert crs.main(["--fixture", str(tmp_path), "--report", str(report)]) == 2
    out = capsys.readouterr().out
    assert "unreadable: actions/permissions/workflow" in out
    assert "1 endpoint(s) unreadable" in report.read_text(encoding="utf-8")


def test_a_drift_and_an_unreadable_endpoint_together_exit_2_and_report_both(payloads):
    del payloads["pages"]
    payloads["actions/permissions/workflow"]["default_workflow_permissions"] = "write"
    result = compare(payloads)
    assert result.exit_code == 2
    assert result.lines() == [
        'actions.default_workflow_permissions: expected "read", found "write"',
        "unreadable: pages (no recorded response)",
    ]


def test_runner_mode_lists_local_only_fields_and_never_reads_them(payloads, tmp_path, capsys):
    """The actions section is checked_on = "local": absent from the fixture it does not fail in
    runner mode; present and differing it is not reported there, and is reported locally."""
    assert DECLARATION["actions"]["checked_on"] == "local"
    others = [DECLARATION["pages"], DECLARATION["code_owners"], DECLARATION["paper_approvers"]]
    others += [DECLARATION["general"]]
    others += DECLARATION["rulesets"] + DECLARATION["environments"]
    assert all(s.get("checked_on", "both") == "both" for s in others)
    del payloads["actions/permissions/workflow"]
    result = compare(payloads, runner=True)
    assert result.exit_code == 0 and not result.unreadable
    assert result.verdict == (
        f"conforming ({FIELDS - LOCAL_ONLY} fields on the runner; {LOCAL_ONLY} local-only)"
    )
    assert [f for f, _ in result.local_only] == [
        "rulesets.main-review.bypass_actors",
        "rulesets.main-checks.bypass_actors",
        "rulesets.dev.bypass_actors",
        "rulesets.paper.bypass_actors",
        "rulesets.governance-files.bypass_actors",
        "actions.default_workflow_permissions",
        "actions.can_approve_pull_request_reviews",
    ]
    assert all(
        "Administration (read)" in r for f, r in result.local_only if f.startswith("actions")
    )
    text = result.markdown("o/r", Path("d.toml"))
    assert "Not checked on the runner (needs a code owner's local run):" in text
    assert "- `actions.default_workflow_permissions`: GET actions/permissions/workflow" in text
    # present and differing: not read in runner mode, reported in a local run
    differing = copy.deepcopy(crs.load_fixture(FIXTURE))
    differing["actions/permissions/workflow"]["default_workflow_permissions"] = "write"
    runner = compare(differing, runner=True)
    assert runner.exit_code == 0 and runner.differences == []
    local = compare(differing)
    assert local.exit_code == 1
    assert local.lines() == ['actions.default_workflow_permissions: expected "read", found "write"']
    # a readable endpoint that is missing still exits 2 in runner mode
    del payloads["pages"]
    result = compare(payloads, runner=True)
    assert result.exit_code == 2
    assert result.verdict == f"1 endpoint(s) unreadable; {LOCAL_ONLY} local-only"
    # the command line
    for path in FIXTURE.glob("*.json"):
        if path.name != "actions__permissions__workflow.json":
            (tmp_path / path.name).write_bytes(path.read_bytes())
    assert crs.main(["--fixture", str(tmp_path), "--runner"]) == 0
    out = capsys.readouterr().out
    assert (
        "local-only: actions.default_workflow_permissions (GET actions/permissions/workflow" in out
    )
    assert out.strip().endswith(
        f"conforming ({FIELDS - LOCAL_ONLY} fields on the runner; {LOCAL_ONLY} local-only)"
    )


def test_bypass_actors_are_local_only_on_the_runner_and_compared_locally(payloads):
    """The API returns bypass actors to administrators only (the first controls run on dev,
    2026-11-17, saw [] for main-review): a field-level override marks them local. The 0.1
    bypass (a user, on pull requests) put back in the fixture is a ruleset not yet changed."""
    for r in DECLARATION["rulesets"]:
        assert r["fields"]["bypass_actors"]["checked_on"] == "local", r["name"]
    ruleset(payloads, "main-review")["bypass_actors"] = [
        {"actor_id": 10465438, "actor_type": "User", "bypass_mode": "pull_request"}
    ]
    runner = compare(payloads, runner=True)
    assert runner.exit_code == 0 and runner.differences == []
    assert not any(r.path.endswith(".bypass_actors") for r in runner.rows)
    listed = dict(runner.local_only)
    assert "administrators only" in listed["rulesets.main-review.bypass_actors"]
    assert "Not checked on the runner" in runner.markdown("o/r", Path("d.toml"))
    assert "- `rulesets.main-review.bypass_actors`: the API returns" in runner.markdown(
        "o/r", Path("d.toml")
    )
    local = compare(payloads)
    assert local.exit_code == 1
    assert local.lines() == [
        'rulesets.main-review.bypass_actors: expected [], found ["User:10465438:pull_request"]'
    ]


def test_a_bad_checked_on_value_is_refused(tmp_path):
    source = crs.DECLARATION.read_text(encoding="utf-8")
    section = source.replace(
        '[actions]\nchecked_on = "local"', '[actions]\nchecked_on = "sometimes"'
    )
    field = source.replace(
        '[rulesets.fields.bypass_actors]\nchecked_on = "local"',
        '[rulesets.fields.bypass_actors]\nchecked_on = "runner"',
        1,
    )
    for text in (section, field):
        assert text != source
        (tmp_path / "g.toml").write_text(text, encoding="utf-8")
        with pytest.raises(ValueError, match="checked_on"):
            crs.load_declaration(tmp_path / "g.toml")


def test_a_governed_path_missing_from_the_push_ruleset_is_named(payloads):
    """The governance-files push ruleset (WP82) restricts pushes touching the governed paths; a path
    dropped from it is a difference, and a push ruleset has no branch-condition rows."""
    rule = ruleset(payloads, "governance-files")["rules"][0]
    assert rule["type"] == "file_path_restriction"
    rule["parameters"]["restricted_file_paths"].remove("GOVERNANCE.md")
    result = compare(payloads)
    assert result.exit_code == 1
    (line,) = result.lines()
    assert line.startswith(
        "rulesets.governance-files.rules.file_path_restriction.restricted_file_paths: expected"
    )
    assert '"GOVERNANCE.md"' in line.split("found")[0]
    assert '"GOVERNANCE.md"' not in line.split("found")[1]
    paths = [r.path for r in result.rows if r.path.startswith("rulesets.governance-files")]
    assert paths == [
        "rulesets.governance-files.target",
        "rulesets.governance-files.enforcement",
        "rulesets.governance-files.bypass_actors",
        "rulesets.governance-files.rules",
        "rulesets.governance-files.rules.file_path_restriction.restricted_file_paths",
    ]
    # the paths compare as a set: the API's order is not the declaration's
    rule["parameters"]["restricted_file_paths"] = sorted(
        rule["parameters"]["restricted_file_paths"] + ["GOVERNANCE.md"], reverse=True
    )
    assert compare(payloads).exit_code == 0


def test_the_governed_files_are_the_push_rulesets_paths_and_each_has_its_codeowners_line():
    """The declaration's governed_files table, the governance-files ruleset's paths and the
    CODEOWNERS lines (scripts/admissibility.py) name the same files; each line's approvers are the
    code owners (his word, 2026-11-17)."""
    governed = DECLARATION["governed_files"]
    push = next(r for r in DECLARATION["rulesets"] if r["name"] == "governance-files")
    assert push["target"] == "push" and "include" not in push
    (rule,) = push["rules"]
    assert sorted(rule["parameters"]["restricted_file_paths"]) == sorted(
        g["path"] for g in governed
    )
    assert crs._actors(push["bypass_actors"]) == ["RepositoryRole:5:always"]
    adm = crs._code_owners_module()
    lines = adm.governed_owners(ROOT / ".github" / "CODEOWNERS")
    assert sorted(lines) == sorted(g["codeowners"] for g in governed)
    assert all(owners == OWNERS for owners in lines.values()), lines
    for g in governed:
        assert "CODEOWNERS line" in g["control"] and "governance-files" in g["control"], g["path"]


def test_codeowners_without_a_login_is_a_difference(payloads):
    result = compare(payloads, owners=set())
    assert result.exit_code == 1
    assert result.lines() == ['code_owners: expected "at least one login", found []']


# ------------------------------------------------------- the declaration and GOVERNANCE.md


def governed_in_governance_md() -> dict[str, str]:
    """``path -> executable|guideline`` from the list under "The secondary rules"."""
    text = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
    section = text.split("## The secondary rules", 1)[1].split("\n## ", 1)[0]
    found = re.findall(r"^- `([^`]+)`[^\n]*?\b(executable|guideline)\b", section, re.M)
    return dict(found)


def test_the_declaration_and_governance_md_name_the_same_secondary_rules():
    declared = {g["path"]: g["check"] for g in DECLARATION["governed_files"]}
    assert set(declared.values()) <= {"executable", "guideline"}
    assert governed_in_governance_md() == declared
    assert {
        ".github/CODEOWNERS",
        ".github/governance.toml",
        ".github/workflows/*.yml",
        "GOVERNANCE.md",
        ".github/RELEASE_ADMISSIBILITY.md",
        ".github/pull_request_template.md",
    } <= set(declared)


def test_every_governed_path_and_every_checker_it_names_exists():
    for g in DECLARATION["governed_files"]:
        assert glob.glob(str(ROOT / g["path"])), g["path"]
        assert g["control"], g["path"]
        for name in re.findall(r"[\w./-]+\.(?:py|yml|md)", g["by"]):
            candidates = (ROOT / name, ROOT / "scripts" / name, WORKFLOWS / name)
            assert any(c.is_file() for c in candidates), (g["path"], name)


def test_the_declaration_names_this_repository_and_codeowners():
    assert DECLARATION["repository"] == "DynamicalSystemsGroup/tradespace"
    assert DECLARATION["code_owners"]["file"] == ".github/CODEOWNERS"
    assert (ROOT / DECLARATION["code_owners"]["file"]).is_file()
    assert DECLARATION["paper_approvers"]["file"] == ".github/CODEOWNERS"
    assert DECLARATION["paper_approvers"]["pattern"] == "paper/"
    assert {r["name"] for r in DECLARATION["rulesets"]} == {
        "main-review",
        "main-checks",
        "dev",
        "paper",
        "governance-files",
    }
    assert {e["name"] for e in DECLARATION["environments"]} == {
        "github-pages",
        "pypi",
        "testpypi",
        "paper-release",
    }


# ------------------------------------------------------------------ the controls job


def _reaches(jobs, job_id, target, seen=()):
    needs = jobs[job_id].get("needs", [])
    needs = [needs] if isinstance(needs, str) else needs
    return target in needs or any(
        _reaches(jobs, n, target, (*seen, job_id)) for n in needs if n not in seen
    )


@pytest.mark.parametrize("name", ["test.yml", "release.yml"])
def test_controls_is_first_and_every_other_job_needs_it(name):
    wf = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
    jobs = wf["jobs"]
    assert next(iter(jobs)) == "controls"
    controls = jobs["controls"]
    assert "needs" not in controls
    assert controls["permissions"] == {"contents": "read", "actions": "read", "pages": "read"}
    run = next(s["run"] for s in controls["steps"] if "check_repo_settings" in s.get("run", ""))
    assert 'scripts/check_repo_settings.py --runner --report "$GITHUB_STEP_SUMMARY"' in run
    for job_id in jobs:
        if job_id != "controls":
            assert _reaches(jobs, job_id, "controls"), (name, job_id)


def test_release_runs_controls_once_and_carries_the_attestation():
    release = yaml.safe_load((WORKFLOWS / "release.yml").read_text(encoding="utf-8"))
    tests = yaml.safe_load((WORKFLOWS / "test.yml").read_text(encoding="utf-8"))
    assert release["jobs"]["test"]["with"] == {"windows": False, "controls": False}
    call_inputs = tests.get("on", tests.get(True))["workflow_call"]["inputs"]
    assert call_inputs["controls"]["default"] is True
    # The release's call passes controls: false; the second clause is the Dependabot gate on a pull
    # request into dev (tests/test_ci_shards.py holds it in full).
    assert tests["jobs"]["controls"]["if"].startswith(
        "${{ (github.workflow == 'Tests' || inputs.controls) && "
    )
    assert "needs.controls.result == 'skipped'" in tests["jobs"]["test"]["if"]
    outputs = release["jobs"]["controls"]["outputs"]
    assert set(outputs) == {"declaration", "result"}
    controls_run = "\n".join(s.get("run", "") for s in release["jobs"]["controls"]["steps"])
    assert 'git rev-parse --short=12 "HEAD:.github/governance.toml"' in controls_run
    assert "Controls: $declaration checked at $GITHUB_SHA: $result" in controls_run
    assert "sed -n 's/^check_repo_settings: //p' controls.txt" in controls_run
    assert "code=${PIPESTATUS[0]}" in controls_run
    tag_run = "\n".join(s.get("run", "") for s in release["jobs"]["tag"]["steps"])
    assert '--controls "$CONTROLS_DECLARATION" --checked-at "$GITHUB_SHA"' in tag_run
    assert '--controls-result "$CONTROLS_RESULT"' in tag_run
    env = release["jobs"]["tag"]["env"]
    assert env["CONTROLS_DECLARATION"] == "${{ needs.controls.outputs.declaration }}"
    assert env["CONTROLS_RESULT"] == "${{ needs.controls.outputs.result }}"


def test_a_merged_branch_kept_is_named(payloads):
    """Settings, General: a merged pull request's branch is deleted (GOVERNANCE.md, "Branches");
    the field is read on the runner (Metadata), so a drift turns the controls job red."""
    assert DECLARATION["general"] == {"delete_branch_on_merge": True}
    payloads["repository"]["delete_branch_on_merge"] = False
    result = compare(payloads)
    assert result.exit_code == 1
    assert result.lines() == ["general.delete_branch_on_merge: expected true, found false"]
    runner = compare(payloads, runner=True)
    assert [r.path for r in runner.differences] == ["general.delete_branch_on_merge"]
    assert crs.fixture_name(crs.REPOSITORY) == "repository.json"
    del payloads["repository"]
    assert compare(payloads).exit_code == 2
