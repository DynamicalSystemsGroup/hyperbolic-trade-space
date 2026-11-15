"""The machine rows of the issue and pull request admissibility conditions, one case per row
(verification cases VC-1 to VC-5 in work-packages/WP47-rounds/checks.md)."""

import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "admissibility", ROOT / "scripts" / "admissibility.py"
)
adm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adm)

GOOD_ISSUE = """### Scope

Add the page.

### Non-goals

No redesign.

### Blast radius

docs/page.md

### Definition of good

Readers find it.

### Definition of good enough

- The link test passes (conformance)
- The page reads as intended in a browser (fitness)

### Open decisions

none
"""
GOOD_PR = """## Issue

closes #12

## What changed

A page.

## What backs it

A test.

## Tests

uv run pytest

## Defaults

none

## Tools used

an editor
"""


def run(tmp_path, check, event, owners="*   @owner\n"):
    (tmp_path / "e.json").write_text(json.dumps(event), encoding="utf-8")
    (tmp_path / "CODEOWNERS").write_text(owners, encoding="utf-8")
    report = tmp_path / "r.md"
    code = adm.main(
        [
            check,
            "--event",
            str(tmp_path / "e.json"),
            "--codeowners",
            str(tmp_path / "CODEOWNERS"),
            "--report",
            str(report),
        ]
    )
    return code, report.read_text(encoding="utf-8") if report.exists() else ""


def issue_event(body, labels=("draft",)):
    return {"issue": {"body": body, "labels": [{"name": n} for n in labels]}}


def pr_event(
    body, labels=(), action="opened", merged=False, base="dev", author="alice", merger=None
):
    return {
        "action": action,
        "pull_request": {
            "body": body,
            "labels": [{"name": n} for n in labels],
            "merged": merged,
            "base": {"ref": base},
            "user": {"login": author},
            "merged_by": {"login": merger} if merger else None,
        },
    }


def test_issue_with_every_field_passes(tmp_path):
    assert run(tmp_path, "issue", issue_event(GOOD_ISSUE))[0] == 0


@pytest.mark.parametrize("field", list(adm.ISSUE_FIELDS))
def test_issue_missing_or_empty_field_fails_and_names_it(tmp_path, field):
    body = GOOD_ISSUE.replace(f"### {field}", "### Other")
    code, report = run(tmp_path, "issue", issue_event(body))
    assert code == 1 and field in report
    empty = re.sub(
        rf"(### {field}\n\n).*?(\n\n###|\Z)", r"\1_No response_\2", GOOD_ISSUE, flags=re.S
    )
    assert empty != GOOD_ISSUE and run(tmp_path, "issue", issue_event(empty))[0] == 1


def test_good_enough_item_without_a_mark_fails(tmp_path):
    body = GOOD_ISSUE.replace("(fitness)", "")
    code, report = run(tmp_path, "issue", issue_event(body))
    assert code == 1 and "neither conformance nor fitness" in report


def test_issue_without_the_draft_label_is_not_checked(tmp_path):
    assert run(tmp_path, "issue", issue_event("anything", labels=("bug",)))[0] == 0


def label_event(actor, label="draft"):
    return {"action": "unlabeled", "label": {"name": label}, "sender": {"login": actor}}


def test_draft_label_removed_by_a_code_owner_stays_removed(tmp_path):
    assert run(tmp_path, "label-gate", label_event("Owner"))[0] == 0


def test_draft_label_removed_by_anyone_else_is_reverted(tmp_path):
    code, report = run(tmp_path, "label-gate", label_event("mallory"))
    assert code == 1 and "not a code owner" in report


def test_another_label_removed_is_ignored(tmp_path):
    assert run(tmp_path, "label-gate", label_event("mallory", "bug"))[0] == 0


@pytest.mark.parametrize("text", ["closes #3", "Fixes #3", "resolved org/repo#9"])
def test_pull_request_naming_an_issue_passes(tmp_path, text):
    assert run(tmp_path, "linked-issue", pr_event(text))[0] == 0


def test_pull_request_with_neither_issue_nor_label_fails(tmp_path):
    assert run(tmp_path, "linked-issue", pr_event("see #3"))[0] == 1


def test_small_fix_label_stands_in_for_an_issue(tmp_path):
    assert run(tmp_path, "linked-issue", pr_event("typo", labels=("small-fix",)))[0] == 0


def test_pull_request_with_every_field_passes(tmp_path):
    assert run(tmp_path, "pr-fields", pr_event(GOOD_PR))[0] == 0


@pytest.mark.parametrize("field", list(adm.PR_FIELDS))
def test_pull_request_with_an_empty_field_fails_and_names_it(tmp_path, field):
    body = GOOD_PR.replace(f"## {field}\n", f"## {field}\n<!-- say it -->\n## Z\n")
    code, report = run(tmp_path, "pr-fields", pr_event(body))
    assert code == 1 and field in report


def test_merge_by_another_code_owner_passes(tmp_path):
    ev = pr_event("", action="closed", merged=True, merger="bob")
    assert run(tmp_path, "merge", ev, "*   @alice @bob\n")[0] == 0


def test_merge_by_the_author_when_another_code_owner_exists_fails(tmp_path):
    ev = pr_event("", action="closed", merged=True, merger="alice")
    code, report = run(tmp_path, "merge", ev, "*   @alice @bob\n")
    assert code == 1 and "own author" in report


def test_merge_by_a_stranger_fails(tmp_path):
    ev = pr_event("", action="closed", merged=True, merger="eve")
    assert run(tmp_path, "merge", ev, "*   @alice @bob\n")[0] == 1


def test_merge_by_the_only_code_owner_passes_with_the_row_quoted(tmp_path, capsys):
    ev = pr_event("", action="closed", merged=True, merger="alice")
    assert run(tmp_path, "merge", ev, "*   @alice\n")[0] == 0
    out = capsys.readouterr().out
    assert out.startswith("::notice::") and "cannot hold" in out


def test_merge_into_another_branch_or_unmerged_is_ignored(tmp_path):
    ev = pr_event("", action="closed", merged=True, merger="eve", base="main")
    assert run(tmp_path, "merge", ev, "*   @alice @bob\n")[0] == 0
    ev = pr_event("", action="closed", merged=False)
    assert run(tmp_path, "merge", ev, "*   @alice @bob\n")[0] == 0


def test_this_repository_codeowners_names_at_least_one_user():
    assert adm.code_owners(ROOT / ".github" / "CODEOWNERS")


def test_the_templates_carry_the_fields_the_checks_read():
    text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "scope-of-work.yml").read_text(encoding="utf-8")
    assert all(f"label: {f}" in text for f in adm.ISSUE_FIELDS)
    assert "labels: [draft]" in text
    pr = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
    assert all(f"## {f}\n" in pr for f in adm.PR_FIELDS)
