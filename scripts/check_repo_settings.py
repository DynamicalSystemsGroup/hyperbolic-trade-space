"""Compare the repository's live settings on GitHub with their declaration.

The declaration is ``.github/governance.toml`` (``GOVERNANCE.md``): the rulesets (branch rulesets
with their conditions; the push ruleset on the governed files, which has none), the environments
and their deployment policies, the Pages build, the code owners' access, the paper approvers'
access and the default workflow permissions. The checker reads each through ``gh api`` (the
user's login locally, the workflow token on a runner), compares field by field, prints each
difference as ``path: expected X, found Y`` and exits 1 on any. An endpoint that cannot be read is
named and exits 2, never skipped.

    uv run python scripts/check_repo_settings.py
    uv run python scripts/check_repo_settings.py --report report.md
    uv run python scripts/check_repo_settings.py --fixture tests/data/wp78
    uv run python scripts/check_repo_settings.py --record tests/data/wp78

``--runner`` is the workflow token's run (the ``controls`` job): a section the declaration marks
``checked_on = "local"`` is not read; its fields are listed in the report under "Not checked on the
runner" with the declaration's reason and leave the exit code alone, and the verdict counts them
(``conforming (N fields on the runner; M local-only)``). Without the flag every field is read.
A field-level override, ``[rulesets.fields.bypass_actors]`` with ``checked_on = "local"``, does the
same for one field of a section (bypass actors: the API returns them to administrators only).
``--report`` writes the comparison as Markdown (the job summary). ``--fixture DIR`` reads recorded
responses instead of calling ``gh`` (the tests); ``--record DIR`` writes the responses it reads,
one JSON file per endpoint, for a new fixture. ``--declaration`` and ``--repo`` override the
defaults (the file in the tree; its ``repository`` key).

Endpoints, relative to ``repos/{owner}/{repo}/``, and the fine-grained permission each needs
(GitHub's "Permissions required for fine-grained personal access tokens"; the workflow token has
Metadata always, Actions and Pages when the job declares them, Administration never):

    rulesets, rulesets/{id}                                   Metadata (read)
    environments, environments/{name}/deployment-branch-policies   Actions (read)
    pages                                                     Pages (read)
    collaborators/{login}/permission                          Metadata (read)
    actions/permissions/workflow                              Administration (read)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECLARATION = ROOT / ".github" / "governance.toml"
RANK = {"none": 0, "read": 1, "triage": 1, "write": 2, "maintain": 2, "admin": 3}
# A section's scope: checked on the runner and locally ("both", the default), or locally only
# ("local": its endpoint needs a permission the workflow token never has, named in local_reason).
SCOPES = {"both", "local"}
SCOPE_KEYS = ("checked_on", "local_reason", "fields")
BRANCH_POLICY = {
    "all": None,
    "protected": {"protected_branches": True, "custom_branch_policies": False},
    "selected": {"protected_branches": False, "custom_branch_policies": True},
}


class Unreadable(Exception):
    """An endpoint the token could not read: named, never skipped."""

    def __init__(self, endpoint: str, reason: str):
        super().__init__(f"{endpoint}: {reason}")
        self.endpoint = endpoint
        self.reason = reason


@dataclass
class Row:
    path: str
    expected: object
    found: object
    ok: bool


Fetch = Callable[[str], object]


def _code_owners_module():
    spec = importlib.util.spec_from_file_location(
        "_admissibility", ROOT / "scripts" / "admissibility.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def code_owners(path: Path) -> set[str]:
    """The logins on the ``*`` line of CODEOWNERS (``scripts/admissibility.py`` reads the same)."""
    return _code_owners_module().code_owners(path)


def paper_approvers(path: Path) -> set[str]:
    """The logins on the ``paper/`` line of CODEOWNERS (the same reader as the merge check)."""
    return _code_owners_module().paper_approvers(path)


# ---------------------------------------------------------------------------------------- sources


def fixture_name(endpoint: str) -> str:
    """The file of a recorded response.

    >>> fixture_name("environments/pypi/deployment-branch-policies")
    'environments__pypi__deployment-branch-policies.json'
    """
    return endpoint.replace("/", "__") + ".json"


def gh_fetch(repo: str, record: Path | None = None) -> Fetch:
    """Read ``repos/{repo}/{endpoint}`` with ``gh api``; record each answer when asked."""

    def fetch(endpoint: str):
        r = subprocess.run(
            ["gh", "api", f"repos/{repo}/{endpoint}"], capture_output=True, text=True, check=False
        )
        if r.returncode != 0:
            lines = [ln for ln in (r.stderr + r.stdout).splitlines() if ln.strip()]
            raise Unreadable(endpoint, lines[-1] if lines else f"gh exited {r.returncode}")
        if record is not None:
            record.mkdir(parents=True, exist_ok=True)
            (record / fixture_name(endpoint)).write_text(r.stdout, encoding="utf-8")
        return json.loads(r.stdout)

    return fetch


def load_fixture(directory: Path) -> dict[str, object]:
    """Every recorded response of a fixture directory, by endpoint."""
    out = {}
    for path in sorted(directory.glob("*.json")):
        endpoint = path.name.removesuffix(".json").replace("__", "/")
        out[endpoint] = json.loads(path.read_text(encoding="utf-8"))
    return out


def dict_fetch(payloads: dict[str, object]) -> Fetch:
    """A fetch over recorded payloads; an endpoint absent from them is unreadable."""

    def fetch(endpoint: str):
        if endpoint not in payloads:
            raise Unreadable(endpoint, "no recorded response")
        return payloads[endpoint]

    return fetch


# ------------------------------------------------------------------------------------- comparing


def _actors(actors: list[dict]) -> list[str]:
    return sorted(f"{a['actor_type']}:{a['actor_id']}:{a['bypass_mode']}" for a in actors)


def _policies(policies: list[dict]) -> list[str]:
    return sorted(f"{p['type']}:{p['name']}" for p in policies)


def _branch_policy_word(found: dict | None) -> str | None:
    for word, shape in BRANCH_POLICY.items():
        if found == shape:
            return word
    return json.dumps(found, sort_keys=True) if found is not None else None


class Comparison:
    """The rows of one run: every compared field, and the endpoints that could not be read."""

    def __init__(
        self,
        declaration: dict,
        fetch: Fetch,
        owners: set[str],
        runner: bool = False,
        approvers: set[str] = frozenset(),
    ):
        self.decl = declaration
        self.fetch = fetch
        self.owners = owners
        self.approvers = approvers
        self.runner = runner
        self.rows: list[Row] = []
        self.unreadable: list[str] = []
        self.local_only: list[tuple[str, str]] = []

    def local_only_section(self, section: dict, fields: list[str]) -> bool:
        """In runner mode a section marked ``checked_on = "local"`` is listed, not fetched.

        The fields are named in the report with the declaration's reason and leave the exit code
        alone; a code owner's local run (no ``--runner``) checks them.
        """
        if not (self.runner and section.get("checked_on", "both") == "local"):
            return False
        reason = section.get("local_reason", "marked local in the declaration")
        self.local_only += [(field, reason) for field in fields]
        return True

    def local_only_field(self, section: dict, key: str, path: str) -> bool:
        """A field-level override: ``[<section>.fields.<key>]`` with ``checked_on = "local"``.

        In runner mode the field is neither fetched nor compared, and is listed with its reason.
        """
        scope = (section.get("fields") or {}).get(key) or {}
        if not (self.runner and scope.get("checked_on", "both") == "local"):
            return False
        self.local_only.append((path, scope.get("local_reason", "marked local in the declaration")))
        return True

    def read(self, endpoint: str):
        try:
            return self.fetch(endpoint)
        except Unreadable as e:
            self.unreadable.append(f"{e.endpoint} ({e.reason})")
            return None

    def eq(self, path: str, expected, found) -> None:
        self.rows.append(Row(path, expected, found, expected == found))

    def run(self) -> Comparison:
        self.rulesets()
        self.environments()
        self.pages()
        self.code_owners()
        self.paper_approvers()
        self.actions()
        return self

    def rulesets(self) -> None:
        listing = self.read("rulesets")
        if listing is None:
            return
        live = {r["name"]: r for r in listing}
        declared = {r["name"]: r for r in self.decl.get("rulesets", [])}
        self.eq("rulesets", sorted(declared), sorted(live))
        for name, d in declared.items():
            if name not in live or self.local_only_section(d, [f"rulesets.{name}"]):
                continue
            detail = self.read(f"rulesets/{live[name]['id']}")
            if detail is None:
                continue
            p = f"rulesets.{name}"
            self.eq(f"{p}.target", d["target"], detail.get("target"))
            self.eq(f"{p}.enforcement", d["enforcement"], detail.get("enforcement"))
            if d["target"] != "push":  # a push ruleset has no ref condition
                cond = (detail.get("conditions") or {}).get("ref_name") or {}
                self.eq(f"{p}.include", sorted(d["include"]), sorted(cond.get("include") or []))
                self.eq(
                    f"{p}.exclude", sorted(d.get("exclude", [])), sorted(cond.get("exclude") or [])
                )
            if not self.local_only_field(d, "bypass_actors", f"{p}.bypass_actors"):
                self.eq(
                    f"{p}.bypass_actors",
                    _actors(d.get("bypass_actors", [])),
                    _actors(detail.get("bypass_actors") or []),
                )
            live_rules = {r["type"]: r.get("parameters") or {} for r in detail.get("rules") or []}
            self.eq(f"{p}.rules", sorted(r["type"] for r in d["rules"]), sorted(live_rules))
            for rule in d["rules"]:
                found = live_rules.get(rule["type"], {})
                for key, want in (rule.get("parameters") or {}).items():
                    got = found.get(key)
                    if key == "required_status_checks":
                        want = sorted(want)
                        got = sorted(c["context"] for c in got or [])
                    elif isinstance(want, list) and all(isinstance(x, str) for x in want):
                        want = sorted(want)  # a list of names (restricted file paths): order free
                        got = sorted(got) if isinstance(got, list) else got
                    self.eq(f"{p}.rules.{rule['type']}.{key}", want, got)

    def environments(self) -> None:
        listing = self.read("environments")
        if listing is None:
            return
        live = {e["name"]: e for e in listing.get("environments", [])}
        declared = {e["name"]: e for e in self.decl.get("environments", [])}
        self.eq("environments", sorted(declared), sorted(live))
        for name, d in declared.items():
            if name not in live or self.local_only_section(d, [f"environments.{name}"]):
                continue
            e, p = live[name], f"environments.{name}"
            self.eq(f"{p}.can_admins_bypass", d["can_admins_bypass"], e.get("can_admins_bypass"))
            rule = next(
                (
                    r
                    for r in e.get("protection_rules") or []
                    if r.get("type") == "required_reviewers"
                ),
                {},
            )
            reviewers = sorted(r["reviewer"]["login"] for r in rule.get("reviewers") or [])
            self.eq(f"{p}.reviewers", sorted(d.get("reviewers", [])), reviewers)
            if "prevent_self_review" in d:
                self.eq(
                    f"{p}.prevent_self_review",
                    d["prevent_self_review"],
                    rule.get("prevent_self_review"),
                )
            self.eq(
                f"{p}.deployment_branches",
                d["deployment_branches"],
                _branch_policy_word(e.get("deployment_branch_policy")),
            )
            policies = self.read(f"environments/{name}/deployment-branch-policies")
            if policies is not None:
                self.eq(
                    f"{p}.policies",
                    _policies(d.get("policies", [])),
                    _policies(policies.get("branch_policies") or []),
                )

    def pages(self) -> None:
        if self.local_only_section(self.decl["pages"], ["pages.build_type"]):
            return
        pages = self.read("pages")
        if pages is not None:
            self.eq("pages.build_type", self.decl["pages"]["build_type"], pages.get("build_type"))

    def code_owners(self) -> None:
        """The code owners (the ``*`` line): at least one, each with the declared minimum access."""
        if self.local_only_section(self.decl["code_owners"], ["code_owners"]):
            return
        self.access_rows("code_owners", self.owners, self.decl["code_owners"])

    def paper_approvers(self) -> None:
        """The paper's approvers (the ``paper/`` line), when the declaration has the section."""
        section = self.decl.get("paper_approvers")
        if section is None or self.local_only_section(section, ["paper_approvers"]):
            return
        self.access_rows("paper_approvers", self.approvers, section)

    def access_rows(self, label: str, logins: set[str], section: dict) -> None:
        minimum = section["minimum_permission"]
        self.rows.append(Row(label, "at least one login", sorted(logins), bool(logins)))
        for login in sorted(logins):
            answer = self.read(f"collaborators/{login}/permission")
            if answer is None:
                continue
            found = answer.get("permission")
            self.rows.append(
                Row(
                    f"{label}.{login}.permission",
                    f"{minimum} or more",
                    found,
                    RANK.get(found, -1) >= RANK[minimum],
                )
            )

    def actions(self) -> None:
        section = self.decl["actions"]
        fields = [k for k in section if k not in SCOPE_KEYS]
        if self.local_only_section(section, [f"actions.{k}" for k in fields]):
            return
        answer = self.read("actions/permissions/workflow")
        if answer is None:
            return
        for key in fields:
            self.eq(f"actions.{key}", section[key], answer.get(key))

    # ------------------------------------------------------------------------------ results

    @property
    def differences(self) -> list[Row]:
        return [r for r in self.rows if not r.ok]

    @property
    def exit_code(self) -> int:
        if self.unreadable:
            return 2
        return 1 if self.differences else 0

    @property
    def verdict(self) -> str:
        local = f"; {len(self.local_only)} local-only" if self.runner else ""
        if self.unreadable:
            return f"{len(self.unreadable)} endpoint(s) unreadable{local}"
        if self.differences:
            return f"{len(self.differences)} difference(s){local}"
        if self.runner:
            return f"conforming ({len(self.rows)} fields on the runner{local})"
        return f"conforming ({len(self.rows)} fields)"

    def lines(self) -> list[str]:
        out = [
            f"{r.path}: expected {fmt(r.expected)}, found {fmt(r.found)}" for r in self.differences
        ]
        out += [f"unreadable: {u}" for u in self.unreadable]
        out += [f"local-only: {field} ({reason})" for field, reason in self.local_only]
        return out

    def markdown(self, repo: str, declaration: Path) -> str:
        head = [
            f"## Controls: `{repo}` against `{declaration}`",
            "",
            f"**{self.verdict}**",
            "",
        ]
        if self.local_only:
            head += ["Not checked on the runner (needs a code owner's local run):", ""]
            head += [f"- `{field}`: {reason}" for field, reason in self.local_only]
            head += [""]
        if self.unreadable:
            head += [
                "Unreadable (the token lacks the endpoint's permission, or the call failed):",
                "",
            ]
            head += [f"- `{u}`" for u in self.unreadable]
            head += [""]
        table = ["| Field | Expected | Found | |", "|---|---|---|---|"]
        for r in self.rows:
            mark = "ok" if r.ok else "**differs**"
            table.append(f"| `{r.path}` | `{fmt(r.expected)}` | `{fmt(r.found)}` | {mark} |")
        return "\n".join(head + table) + "\n"


def fmt(value) -> str:
    """One line for a compared value.

    >>> fmt(["b", "a"]), fmt(True), fmt(None)
    ('["b", "a"]', 'true', 'null')
    """
    return json.dumps(value)


def load_declaration(path: Path) -> dict:
    """The declaration; each section's ``checked_on`` is ``both`` (the default) or ``local``."""
    decl = tomllib.loads(path.read_text(encoding="utf-8"))
    sections = [decl["actions"], decl["pages"], decl["code_owners"]]
    sections += [decl["paper_approvers"]] if "paper_approvers" in decl else []
    sections += decl.get("rulesets", []) + decl.get("environments", [])
    for section in sections:
        for scope in (section, *(section.get("fields") or {}).values()):
            if scope.get("checked_on", "both") not in SCOPES:
                raise ValueError(f"checked_on must be one of {sorted(SCOPES)}: {scope}")
    return decl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--declaration", type=Path, default=DECLARATION)
    parser.add_argument("--repo", help="OWNER/NAME; default: the declaration's repository")
    parser.add_argument(
        "--codeowners", type=Path, help="default: the declaration's code_owners.file"
    )
    parser.add_argument("--fixture", type=Path, help="read recorded responses from this directory")
    parser.add_argument("--record", type=Path, help="write the responses read into this directory")
    parser.add_argument("--report", type=Path, help="write the comparison as Markdown here")
    parser.add_argument(
        "--runner",
        action="store_true",
        help='the workflow token\'s run: fields marked checked_on = "local" are listed, not read',
    )
    args = parser.parse_args(argv)
    decl = load_declaration(args.declaration)
    repo = args.repo or decl["repository"]
    owners_file = args.codeowners or (ROOT / decl["code_owners"]["file"])
    owners = code_owners(owners_file)
    approvers: set[str] = set()
    if "paper_approvers" in decl:
        approvers = paper_approvers(args.codeowners or (ROOT / decl["paper_approvers"]["file"]))
    fetch = dict_fetch(load_fixture(args.fixture)) if args.fixture else gh_fetch(repo, args.record)
    result = Comparison(decl, fetch, owners, runner=args.runner, approvers=approvers).run()
    for line in result.lines():
        print(line)
    print(f"check_repo_settings: {result.verdict}")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("a", encoding="utf-8") as fh:
            fh.write(
                result.markdown(
                    repo,
                    args.declaration.relative_to(ROOT)
                    if args.declaration.is_relative_to(ROOT)
                    else args.declaration,
                )
            )
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
