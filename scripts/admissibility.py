"""The machine rows of the issue and pull request admissibility conditions.

Each check reads a GitHub event payload (the file named by ``--event``, which ``GITHUB_EVENT_PATH``
names) and ``.github/CODEOWNERS``, prints what it finds, writes a Markdown report for a comment
when it fails, and exits 1 on a failure. It never runs a field of the payload
as a command and calls no network service; the workflows do the commenting and the labelling.

    issue          an issue labelled ``draft`` carries every field of the scope-of-work template
    label-gate     the ``draft`` label was removed by a code owner, else it must be restored
    linked-issue   a pull request names the issue it resolves or has the ``small-fix`` label
    pr-fields      a pull request's description fields are present and non-empty (into ``paper``,
                   the ``Paper`` section too)
    merge          a pull request merged into ``dev`` was merged by a code owner, not its author;
                   one merged into ``paper``, by a paper approver (the ``paper/`` line), not its
                   author

    uv run --no-project python scripts/admissibility.py issue --event e.json --report r.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT = "draft"
SMALL_FIX = "small-fix"
ISSUE_FIELDS = (
    "Scope",
    "Non-goals",
    "Blast radius",
    "Definition of good",
    "Definition of good enough",
    "Open decisions",
)
PR_FIELDS = ("What changed", "What backs it", "Tests", "Defaults", "Tools used")
PAPER_FIELDS = ("Paper",)  # required as well on a pull request into ``paper``
PAPER_BRANCH = "paper"
PAPER_PATTERNS = ("paper/", "/paper/")  # the CODEOWNERS line of the repository's paper directory
CLOSING = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:[\w.-]+/[\w.-]+)?#\d+", re.I
)
KIND_MARK = re.compile(r"\b(conformance|fitness)\b", re.I)
EMPTY = {"", "_no response_", "no response"}


def owners_of(path: Path, patterns: tuple[str, ...]) -> set[str]:
    """Logins on the lines of a CODEOWNERS file whose pattern is one of ``patterns``.

    Users only (a team is not expanded); a comment is dropped; another line's logins are not read.

    >>> import tempfile, pathlib
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "CODEOWNERS"
    >>> _ = p.write_text("# c\\n*   @Ada @org/team\\n/paper/ @bob @Ada\\n", encoding="utf-8")
    >>> sorted(owners_of(p, ("*",))), sorted(owners_of(p, ("paper/", "/paper/")))
    (['ada'], ['ada', 'bob'])
    """
    owners: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("#")[0].split()
        if parts and parts[0] in patterns:
            owners |= {o[1:].lower() for o in parts[1:] if o.startswith("@") and "/" not in o}
    return owners


def code_owners(path: Path) -> set[str]:
    """The code owners: the logins on the ``*`` line (a ``paper/`` line adds none).

    >>> import tempfile, pathlib
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "CODEOWNERS"
    >>> _ = p.write_text("*   @Ada @org/team\\n/paper/ @bob\\n", encoding="utf-8")
    >>> sorted(code_owners(p))
    ['ada']
    """
    return owners_of(path, ("*",))


def paper_approvers(path: Path) -> set[str]:
    """The paper's approvers: the logins on the ``paper/`` line (``/paper/`` anchors it at root).

    >>> import tempfile, pathlib
    >>> p = pathlib.Path(tempfile.mkdtemp()) / "CODEOWNERS"
    >>> _ = p.write_text("*   @Ada @carol\\n/paper/ @bob @Ada\\n", encoding="utf-8")
    >>> sorted(paper_approvers(p))
    ['ada', 'bob']
    """
    return owners_of(path, PAPER_PATTERNS)


def sections(body: str, marker: str) -> dict[str, str]:
    """Split a body at lines that start with ``marker``; HTML comments are dropped.

    >>> sections("## A\\ntext\\n## B\\n<!-- x -->\\n", "## ")
    {'A': 'text', 'B': ''}
    """
    body = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    out: dict[str, str] = {}
    name = None
    for line in body.splitlines():
        if line.startswith(marker):
            name = line[len(marker) :].strip()
            out[name] = ""
        elif name is not None:
            out[name] += line + "\n"
    return {k: v.strip() for k, v in out.items()}


def issue_problems(event: dict) -> list[str]:
    issue = event["issue"]
    labels = {label["name"] for label in issue.get("labels", [])}
    if DRAFT not in labels:
        return []
    found = sections(issue.get("body") or "", "### ")
    problems = []
    for field in ISSUE_FIELDS:
        if found.get(field, "").strip().lower() in EMPTY:
            problems.append(f"the field `{field}` is missing or empty")
    items = [
        ln.strip()
        for ln in found.get("Definition of good enough", "").splitlines()
        if re.match(r"\s*(?:[-*+]|\d+[.)])\s+\S", ln)
    ]
    if found.get("Definition of good enough", "").strip().lower() not in EMPTY:
        if not items:
            problems.append("`Definition of good enough` is not a list of items")
        for item in items:
            if not KIND_MARK.search(item):
                problems.append(
                    f"the good-enough item `{item[:60]}` is marked neither conformance nor fitness"
                )
    return problems


def label_gate_problems(event: dict, owners: set[str]) -> list[str]:
    if event.get("action") != "unlabeled" or event.get("label", {}).get("name") != DRAFT:
        return []
    actor = event["sender"]["login"].lower()
    if actor in owners:
        return []
    return [f"`{DRAFT}` was removed by @{event['sender']['login']}, who is not a code owner"]


def linked_issue_problems(event: dict) -> list[str]:
    pr = event["pull_request"]
    labels = {label["name"] for label in pr.get("labels", [])}
    if SMALL_FIX in labels or CLOSING.search(pr.get("body") or ""):
        return []
    return [
        f"the description names no issue it resolves (`closes #n`) and has no `{SMALL_FIX}` label"
    ]


def pr_field_problems(event: dict) -> list[str]:
    """The template's sections, and the ``Paper`` section on a pull request into ``paper``."""
    pr = event["pull_request"]
    found = sections(pr.get("body") or "", "## ")
    fields = PR_FIELDS + (PAPER_FIELDS if pr["base"]["ref"] == PAPER_BRANCH else ())
    return [
        f"the section `{f}` is missing or empty"
        for f in fields
        if found.get(f, "").strip().lower() in EMPTY
    ]


def merge_row(root: Path = ROOT) -> str:
    """The pull request admissibility row about the merge, quoted in the notice."""
    text = (root / ".github" / "PR_ADMISSIBILITY.md").read_text(encoding="utf-8")
    row = next(ln for ln in text.splitlines() if ln.startswith("| It is merged by a code owner"))
    cells = [c.strip() for c in row.strip().strip("|").split(" | ")]
    return f"{cells[0]} ({cells[1]}): {cells[2]}"


def merge_problems(
    event: dict, owners: set[str], root: Path = ROOT, approvers: set[str] = frozenset()
) -> tuple[list[str], list[str]]:
    """Return (problems, notices) for a closed pull request.

    Into ``dev``: merged by a code owner who is not the author (a notice while the code owners
    are one person). Into ``paper``: merged by a paper approver who is not the author; the
    approvers are two, so there is no notice. Any other base is not checked.
    """
    pr = event["pull_request"]
    if event.get("action") != "closed" or not pr.get("merged"):
        return [], []
    author = pr["user"]["login"].lower()
    merger = ((pr.get("merged_by") or {}).get("login") or "").lower()
    if pr["base"]["ref"] == PAPER_BRANCH:
        if not approvers:
            return ["no `paper/` line of CODEOWNERS names the paper's approvers"], []
        if merger not in approvers:
            return [f"merged by @{merger or 'unknown'}, who is not a paper approver"], []
        if merger == author:
            return ["merged by its own author; another paper approver merges it"], []
        return [], []
    if pr["base"]["ref"] != "dev":
        return [], []
    if not (owners - {author}):
        return [], [f"merged without a second code owner; the row says: {merge_row(root)}"]
    if merger not in owners:
        return [f"merged by @{merger or 'unknown'}, who is not a code owner"], []
    if merger == author:
        return ["merged by its own author, though another code owner exists"], []
    return [], []


def _report(problems: list[str], title: str, path: str | None) -> None:
    if not problems:
        return
    text = f"{title}\n\n" + "\n".join(f"- {p}" for p in problems) + "\n"
    if path:
        Path(path).write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "check", choices=["issue", "label-gate", "linked-issue", "pr-fields", "merge"]
    )
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--codeowners", type=Path, default=ROOT / ".github" / "CODEOWNERS")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--report", help="write the Markdown comment here on a failure")
    args = parser.parse_args(argv)
    event = json.loads(args.event.read_text(encoding="utf-8"))
    owners = code_owners(args.codeowners)
    notices: list[str] = []
    titles = {
        "issue": "This draft is not yet admissible; the `draft` label stays until these are fixed:",
        "label-gate": "Only a code owner turns a draft into an issue, so the label is restored:",
        "linked-issue": "This pull request does not name its issue:",
        "pr-fields": "This pull request's description is incomplete:",
        "merge": "This merge does not meet the pull request admissibility conditions:",
    }
    if args.check == "issue":
        problems = issue_problems(event)
    elif args.check == "label-gate":
        problems = label_gate_problems(event, owners)
    elif args.check == "linked-issue":
        problems = linked_issue_problems(event)
    elif args.check == "pr-fields":
        problems = pr_field_problems(event)
    else:
        problems, notices = merge_problems(
            event, owners, args.root, paper_approvers(args.codeowners)
        )
    for notice in notices:
        print(f"::notice::{notice}")
    for p in problems:
        print(f"::error::{p}")
    _report(problems, titles[args.check], args.report)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
