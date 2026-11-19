# WP82 — Review report: the 0.2 governance update

**Scope reviewed against:** `WP82-scope-of-work.md`, approved verbally on 2026-11-17 ("Approved", quoted in
`WP82-decisions.md`). **Delivery:** branch `governance-bypass-removal`, content head 9fa94658, records d57ac6d1,
over `dev` 7b0d7cdf. **Reviewer:** the v0.2 session, with an independent fresh-context reader over the branch (its
findings below). **The acceptance act:** his word, quoted in the decisions file; the pull request into `dev` opens
after 0.1 and is merged by `danlessa`.

## Deliverables

| Item | State | Evidence |
|---|---|---|
| D-1 the declaration | met | `.github/governance.toml` at 9fa94658: `main-review` bypass actors `[]`; `[actions]` read, approving reviews false; `controls` first in `main-checks`' required checks; `[[rulesets]] governance-files` (push, `file_path_restriction`, nine paths, `RepositoryRole:5:always`); each `governed_files` entry's `codeowners` pattern and `control` sentence |
| D-2 CODEOWNERS and its reader | met | nine anchored lines, each `@mzargham @danlessa @rororowyourboat`; `scripts/admissibility.py` `GOVERNED_PATTERNS`, `governed_owners` (doctest); `tests/test_admissibility.py::test_this_repository_codeowners_names_the_code_owners_and_the_paper_approvers` holds the file to them |
| D-3 the checker, fixture and tests | met | `scripts/check_repo_settings.py` compares a push ruleset (no ref condition; string lists order-free); `tests/data/wp78/`: three recorded files edited to the declared state, `rulesets__1.json` hand-made, `rulesets.json` listing it, `README.md` saying which are not recordings; `tests/test_repo_settings.py`: 69 fields, 7 local-only, `test_a_governed_path_missing_from_the_push_ruleset_is_named`, `test_the_governed_files_are_the_push_rulesets_paths_and_each_has_its_codeowners_line` |
| D-4 the documents | met | `GOVERNANCE.md` (the control on the governed files, five rulesets, the window after a merge, the judged rows' guidelines); `.github/ISSUE_ADMISSIBILITY.md` (four rows for a bug report and a question); `.github/PR_ADMISSIBILITY.md` (the `controls` job in the conformance row; four judged rows naming their guideline); `.github/RELEASE_ADMISSIBILITY.md` (the judged row's guideline); `docs/code-owners.md` (the window; the governed files; adding a code owner to the governed lines); `CHANGELOG.md` (`[Unreleased]`: Removed, Changed) |
| D-5 workflow permissions declared | met | `tests/test_workflow_permissions.py`: ten workflows, every job's permissions declared, no workflow line writes contents; read as the default therefore changes nothing that runs |
| D-6 the issue and the pull request description | prepared, not posted | drafts in the sessions' shared note `0.2-pull-requests-readiness.md` (Issue A, Pull request 1); posted on his word after 0.1 |

## Requirements

| Item | State | Evidence |
|---|---|---|
| R-1 fixture and runner conforming | met | `check_repo_settings: conforming (69 fields)`; `--runner`: `conforming (62 fields on the runner; 7 local-only)` |
| R-2 live run reports exactly the settings he changes | met | five lines, quoted verbatim in `WP82-decisions.md` ("Execution"): the missing ruleset, the `main-review` bypass, `controls` missing from the required checks, the two workflow-permission fields; nothing else |
| R-3 suite, lint, format, lock at the head | lint, format, lock met; suite see below | `ruff check .` clean; `ruff format --check .` clean; `uv lock --check` resolved; the governance, admissibility, workflow, register and doctest cases 135 passed; the fast suite at 9fa94658: its line is appended under "Results that arrived after the first pass" |
| R-4 no setting changed before the merge | met | the live run (R-2) reads the settings as they were; nothing was changed on GitHub by this session |
| R-5 the window written down | met | `GOVERNANCE.md` ("The declaration and the check"), `docs/code-owners.md` ("Repository settings"), `WP82-decisions.md` ("Execution": the five steps in order, the two runner-checked ones first) |
| R-6 no AI attribution | met | `git log dev..HEAD --format=%B` carries no trailer; the documents name none |
| R-7 claims backed; vocabulary and residual checks | met | each document sentence states a setting in the declaration, a test, or his recorded word; `check_vocabulary.py` 0 new violations; the residual rises are on `docs/index.md`, `choosing-k.md`, `tensions.md`, `termination.md`, pages this branch does not touch (the baseline drift recorded by WP76 and WP81) |

## Definition of good enough

| Item | State | Evidence |
|---|---|---|
| R-1 and R-3 pass at the head | R-1 yes; R-3 see the appended line | above |
| R-2's live differences are the four settings, listed in the pull request | met | the decisions file and the pull request draft quote them |
| `tests/test_admissibility.py` holds CODEOWNERS to the `*`, paper and governed lines | met | the extended test; 9 governed patterns, each the code owners |
| The window and the order are in `docs/code-owners.md` and the pull request | met | the page's "Repository settings"; the pull request draft's "What changed" |
| The admissibility rows read as rows | met | each new or changed row has a condition, a kind and an enforcer |
| The pull request carries the bypass removal and the four picked items, nothing else | met | `git diff --stat dev..HEAD`: 22 files, all within the blast radius (below) |

## Outside the scope

`git diff --name-only dev..HEAD`: `.github/CODEOWNERS`, `.github/governance.toml`, `.github/ISSUE_ADMISSIBILITY.md`,
`.github/PR_ADMISSIBILITY.md`, `.github/RELEASE_ADMISSIBILITY.md`, `CHANGELOG.md`, `GOVERNANCE.md`,
`docs/code-owners.md`, `scripts/admissibility.py`, `scripts/check_repo_settings.py`, `tests/data/wp78/` (five files),
`tests/test_admissibility.py`, `tests/test_repo_settings.py`, `tests/test_workflow_permissions.py`,
`work-packages/INDEX.md`, `work-packages/WP82-{scope-of-work,decisions,review}.md`. Every one is in the blast radius
the scope names. No non-goal touched: no setting changed; gap 2, gap 5 and gap 8 untouched; no new workflow.

## Observations (not counted as failures)

- The rebase onto `dev` 7b0d7cdf (WP79's paper route landed while the package was scoped) conflicted in one test
  hunk, resolved by taking dev's `compare(payloads, runner=True)` helper with this package's fixture change.
- With the push ruleset in force, Dependabot's pin moves and any pull request touching the workflows are merged by a
  Repository admin; Rohan reviews, an admin merges. Said in the readiness note for Danilo.
- `tests/test_workflow_permissions.py` accepts a workflow whose own line reads contents and writes issues or pull
  requests for its one job (the five event workflows), which is the state on `dev`.
- The docs page `docs/code-owners.md` changed by two paragraphs and one sentence; its rendered capture is in the
  appended results.

## Open decisions (for the supervisor)

None. The scope's decisions are his (`WP82-decisions.md`); the defaults decided during execution are listed there.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| The fast suite at the head, the rendered page and the independent read were still running at the first pass | see the appended results | appended below once each finished |

## Recommendation

Recommend acceptance: the declaration carries his five decisions and nothing else, the fixture and the runner mode
conform, the live run reports exactly the settings he changes after the merge, the tests hold the governed set to one
list across the table, the ruleset and CODEOWNERS, the documents say what the declaration says, and the window after
the merge is written down where a merger looks. The pull request into `dev` waits for 0.1 to be in `main`, by his word.

## Results that arrived after the first pass

- The fast suite at 9fa94658 (`uv run pytest -q -m "not slow and not paper"`): 2,036 passed, 12 skipped, 2 xfailed
  in 308 s. R-3 and the first good-enough item are met.
- The independent fresh-context read of the branch (its commands and quotations in the session's record): conformance
  holds (the three checker runs and the five live lines character for character; 78 tests; ruff; the vocabulary check);
  22 files, all in the blast radius; no attribution trailer; CODEOWNERS syntax valid (the anchored directory lines
  cover their files, later-line-wins changes no owner since the lines name the `*` line's logins); the hand-made
  payload's fields and types match the REST reference (`target` push, `file_path_restriction`,
  `restricted_file_paths`; `bypass_mode` always, since `pull_request` is for branch rulesets only). Its findings and
  their dispositions:
  - F1, blocks pending his check: GitHub's documentation offers push rulesets for "a private or internal repository"
    and this repository is public. Asked; his answer "Yes, it is offered" (quoted in `WP82-decisions.md`). Closed.
  - F2, the ordered settings list the scope asks for on `docs/code-owners.md` was only in the decisions file. Fixed:
    the list is on the page under "Repository settings" (the capture `WP82-rounds/code-owners-1280-{light,dark}.png`,
    the budget test passing).
  - F3, `GOVERNANCE.md` said the local run reports "the one difference" (the state of the bypass-only commit). Fixed:
    each setting a declaration change names is a difference until it is changed.
  - F4, `GOVERNANCE.md` said the gaps readout's items were decided; gap 2 (the local-only fields) stays open. Fixed:
    the sentence names WP82's items and the open one.
  - F5, index row 82 had four cells and sat between rows 79 and 80. Fixed: six cells, after row 80.
  - F6, "its attestation shows the rule in effect" where the runner cannot see the bypass. Fixed: attested by a code
    owner's local run.
  - F7, the conformance row's "both platforms" against an enforcer that runs Linux only on a push and on the release
    pull request: pre-existing condition text; left, recorded here as an observation for the admissibility rows.
  - The checker decided branch against push by the presence of `include`. Fixed: by `target`.
  - Observations kept as they are: the CODEOWNERS directory lines cover every file where the ruleset's and the table's
    patterns cover `*.yml` (every file there is `.yml` today); `pyyaml` is a transitive test import with precedent;
    the strict residual baseline is stale against `dev` on pages this branch does not touch.
- The code owners' page rendered from the branch (mkdocs strict build; 1280 px, light and dark): the three paragraphs
  under "Repository settings" read as the file says; no sideways scroll; the one console error is the theme's fetch
  of the latest release (none exists yet), present on every page of the site today.
- After the second pass: `tests/test_repo_settings.py`, `test_admissibility.py`, `test_workflow_permissions.py`,
  `test_contributing_links.py` 78 passed; `ruff check` and `ruff format --check` clean; the page budget holds.

The recommendation stands: recommend acceptance.
