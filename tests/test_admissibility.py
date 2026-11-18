"""The machine rows of the issue and pull request admissibility conditions, one case per row
(verification cases VC-1 to VC-5 in 4f81a4ea:work-packages/WP47-rounds/checks.md)."""

import importlib.util
import json
import re
from pathlib import Path

import pytest
import yaml

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


# The paper's route (WP79 G3, R-1): a pull request into paper is merged by a paper approver, the
# logins on the paper/ line of CODEOWNERS, who is not its author. The * line does not count.
PAPER_OWNERS = "*   @alice @bob @carol\n/paper/   @alice @dana\n"


def test_paper_pull_request_by_one_approver_merged_by_the_other_passes(tmp_path):
    ev = pr_event("", action="closed", merged=True, base="paper", author="alice", merger="dana")
    assert run(tmp_path, "merge", ev, PAPER_OWNERS)[0] == 0
    ev = pr_event("", action="closed", merged=True, base="paper", author="dana", merger="Alice")
    assert run(tmp_path, "merge", ev, PAPER_OWNERS)[0] == 0


def test_paper_pull_request_merged_by_its_author_fails(tmp_path):
    ev = pr_event("", action="closed", merged=True, base="paper", author="alice", merger="alice")
    code, report = run(tmp_path, "merge", ev, PAPER_OWNERS)
    assert code == 1 and "own author" in report and "paper approver" in report


def test_paper_pull_request_merged_by_a_code_owner_who_is_not_an_approver_fails(tmp_path):
    ev = pr_event("", action="closed", merged=True, base="paper", author="alice", merger="bob")
    code, report = run(tmp_path, "merge", ev, PAPER_OWNERS)
    assert code == 1 and "@bob, who is not a paper approver" in report


def test_paper_pull_request_without_a_paper_line_fails_and_says_so(tmp_path, capsys):
    ev = pr_event("", action="closed", merged=True, base="paper", author="alice", merger="bob")
    code, report = run(tmp_path, "merge", ev, "*   @alice @bob\n")
    assert code == 1 and "no `paper/` line" in report
    assert "::notice::" not in capsys.readouterr().out  # no one-person notice on the paper's row


def test_the_paper_line_does_not_make_a_code_owner_and_the_star_line_no_approver(tmp_path):
    for line in ("/paper/   @alice @dana\n", "paper/ @alice @dana\n"):
        p = tmp_path / "CODEOWNERS"
        p.write_text("*   @alice @bob @carol\n" + line, encoding="utf-8")
        assert adm.code_owners(p) == {"alice", "bob", "carol"}
        assert adm.paper_approvers(p) == {"alice", "dana"}
    # a stranger on the code owners' line still cannot merge into dev
    ev = pr_event("", action="closed", merged=True, base="dev", author="alice", merger="dana")
    assert run(tmp_path, "merge", ev, PAPER_OWNERS)[0] == 1


def test_this_repository_codeowners_names_the_code_owners_and_the_paper_approvers():
    path = ROOT / ".github" / "CODEOWNERS"
    assert adm.code_owners(path) == {"mzargham", "danlessa", "rororowyourboat"}
    assert adm.paper_approvers(path) == {"mzargham", "jshorish"}  # his word, 2026-11-17 13:05
    # the governed files' lines name the three code owners (his word, 2026-11-17, WP82)
    governed = adm.governed_owners(path)
    assert set(governed) == set(adm.GOVERNED_PATTERNS) and len(governed) == 9
    assert all(owners == adm.code_owners(path) for owners in governed.values()), governed


def test_the_merge_workflow_fires_on_pull_requests_into_dev_and_paper():
    wf = yaml.safe_load(
        (ROOT / ".github" / "workflows" / "merge-by-code-owner.yml").read_text(encoding="utf-8")
    )
    on = wf.get("on", wf.get(True))
    assert on["pull_request_target"] == {"types": ["closed"], "branches": ["dev", "paper"]}


# The template: one file, the software's sections and a Paper section (the pr-fields check reads
# the Paper section on a pull request into paper only).
GOOD_PAPER_PR = GOOD_PR.replace("## Issue\n\ncloses #12\n", "## Issue\n\nsmall fix\n") + (
    "\n## Paper\n\nMethods, one sentence; residuals 0 rose; `myst build --html` exit 0.\n"
)


def test_pull_request_into_paper_with_the_paper_section_passes_the_fields_check(tmp_path):
    assert run(tmp_path, "pr-fields", pr_event(GOOD_PAPER_PR, base="paper"))[0] == 0


def test_pull_request_into_paper_without_the_paper_section_fails_and_names_it(tmp_path):
    code, report = run(tmp_path, "pr-fields", pr_event(GOOD_PR, base="paper"))
    assert code == 1 and "`Paper`" in report
    empty = GOOD_PR + "\n## Paper\n\n<!-- the section or figure -->\n"
    assert run(tmp_path, "pr-fields", pr_event(empty, base="paper"))[0] == 1


def test_pull_request_into_dev_leaves_the_paper_section_empty(tmp_path):
    empty = GOOD_PR + "\n## Paper\n\n<!-- a change to the paper only -->\n"
    assert run(tmp_path, "pr-fields", pr_event(empty, base="dev"))[0] == 0


def test_the_templates_carry_the_fields_the_checks_read():
    text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "scope-of-work.yml").read_text(encoding="utf-8")
    assert all(f"label: {f}" in text for f in adm.ISSUE_FIELDS)
    assert "labels: [draft]" in text
    pr = (ROOT / ".github" / "pull_request_template.md").read_text(encoding="utf-8")
    assert all(f"## {f}\n" in pr for f in adm.PR_FIELDS + adm.PAPER_FIELDS)
    assert "Target `dev`" in pr and "`paper`" in pr


# The dependency route (the dependency row of PR_ADMISSIBILITY.md): a pull request opened by
# dependabot[bot] against dev with the `dependencies` label passes the linked-issue and the fields
# checks with a notice quoting the row; any one of the three conditions missing, it is read as a
# pull request like any other.
BOT_BODY = "Bumps [actions/checkout](https://github.com/actions/checkout) from 5.0.0 to 5.1.0.\n"


def bot_event(labels=("dependencies",), base="dev", author="dependabot[bot]", **kw):
    return pr_event(BOT_BODY, labels=labels, base=base, author=author, **kw)


@pytest.mark.parametrize("check", ["linked-issue", "pr-fields"])
def test_a_dependency_update_passes_with_the_row_quoted(tmp_path, capsys, check):
    assert run(tmp_path, check, bot_event())[0] == 0
    out = capsys.readouterr().out
    assert out.startswith("::notice::a dependency update; the row says: A dependency update")
    assert "stands in for the first three rows" in out and "::error::" not in out


@pytest.mark.parametrize("check", ["linked-issue", "pr-fields"])
@pytest.mark.parametrize(
    "event",
    [
        bot_event(labels=()),  # no label
        bot_event(base="main"),  # a pull request into main is judged as a release
        bot_event(author="alice"),  # a person with the label is not the bot
        bot_event(author="alice", labels=()),
    ],
    ids=["no-label", "into-main", "a-person", "a-person-unlabelled"],
)
def test_a_pull_request_missing_one_of_the_three_conditions_is_read_as_any_other(
    tmp_path, capsys, check, event
):
    assert run(tmp_path, check, event)[0] == 1
    assert "::notice::" not in capsys.readouterr().out


def test_a_dependency_update_is_merged_by_a_code_owner_without_a_notice(tmp_path, capsys):
    ev = bot_event(action="closed", merged=True, merger="alice")
    assert run(tmp_path, "merge", ev, "*   @alice @bob\n")[0] == 0
    assert "::notice::" not in capsys.readouterr().out
    ev = bot_event(action="closed", merged=True, merger="eve")
    assert run(tmp_path, "merge", ev, "*   @alice @bob\n")[0] == 1


def test_dependabot_targets_dev_with_the_label_the_row_reads():
    config = yaml.safe_load((ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8"))
    updates = config["updates"]
    assert {u["package-ecosystem"] for u in updates} == {"github-actions", "uv"}
    for update in updates:
        assert update["target-branch"] == adm.DEV_BRANCH, update
        assert update["labels"] == [adm.DEPENDENCIES], update
        assert update["schedule"] == {"interval": "weekly"}, update
        # minor and patch bumps arrive as one pull request per ecosystem; a major comes on its own
        (group,) = update["groups"].values()
        assert group == {"patterns": ["*"], "update-types": ["minor", "patch"]}, update


def test_the_fields_workflow_fires_when_the_label_arrives_after_the_open():
    wf = yaml.safe_load(
        (ROOT / ".github" / "workflows" / "pr-fields.yml").read_text(encoding="utf-8")
    )
    on = wf.get("on", wf.get(True))
    assert on["pull_request_target"] == {"types": ["opened", "edited", "synchronize", "labeled"]}
