# WP68 — Scope of work: the first merge into `main` (integration, stage 5)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under his approval of the plan (2026-11-16, `WP64-decisions.md`); the pull request and the merge are his alone |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; `dev` after WP67, WP73 and WP74 land; the pull request from `dev` into `main` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md`; his word for the pull request, quoted there when given |
| **Acceptance record** | The merge of the pull request by him; the release run green; `driver-log.md` |

## Purpose

Carry the candidate through the first live run of the software's release control model: version 0.1.0, the
changelog entry, the local and hosted checks at the head, the staged site looked at, the release issue, the pull
request on his word, and the steps after the merge (`WP65-design/build-plan.md`, section 6;
`release-checklist-software.md`, rows A1 to A4, B1 to B5, E1, E3s, F1, F3s to F7, G1, G2s).

## Goals

- G1. Version 0.1.0 in `pyproject.toml`, `uv.lock`, `src/hyperbolic_trade_space/__init__.py` and `CITATION.cff`
  (with `date-released`), the last change before the pull request (A1); `uv lock --check` passes (A6).
- G2. `CHANGELOG.md`: `[Unreleased] - target 0.1.0` becomes `[0.1.0] - <date>`; nothing reads "Unreleased" or
  "target"; every package that changed what a user sees since WP19 is named (A2, A3); `scripts/release_checks.py`'s
  changelog check passes on the head.
- G3. `release-punch-list.md` has no line the tree contradicts; its version box ticked (A4).
- G4. Local checks on the head (B1 to B5): the software suite with paper tests deselected, lint, format, lock, the
  lemma chain and the proof-map checker; the vocabulary check on the software surfaces; the claims register for
  the software surfaces; no attribution line in any commit; the docs build strict in both slots.
- G5. The site staged at the head and looked at: `/`, `/paper/` (abstract), one docs page, 1,280 and 375 px,
  light and dark, captures in `WP68-rounds/` (E1, E3s); the WP67 pass covers the pinned modes.
- G6. The release issue "Release 0.1.0" drafted in `WP68-rounds/release-issue.md`: the packages carried since
  e7fd1165, the WP67 record cited, the staged-site review, the checks' run links, his keyboard items as a checklist
  (R1). Opened on GitHub together with the pull request, on his word.
- G7. His keyboard items (`WP65-design/his-items.md`) read back with `gh api` once he says they are done: the
  rulesets on `main`, `dev` and `paper`, the environments, Pages from Actions, the pending publishers (by his
  word, since they are not readable), Zenodo switched on.
- G8. The pull request from `dev` into `main` opened on his word, closing the release issue, its required checks
  `test (fast)`, `test (slow)`, `test (docs)` and `admissibility` green (C6, F1); CI on Windows at the head by
  dispatch (C7).
- G9. After his merge: the release run watched (tag `v0.1.0`, PyPI, the site, the GitHub release, Zenodo); then
  `git branch paper dev && git push origin paper`; the punch list's post-release checks loaded live (G1, G2s); the
  three hosted-runner paper-test failures of WP67 filed as the paper branch's first items in
  `release-checklist-paper.md`.

## Non-goals

No pull request, merge, tag, publish or deploy before his word; no change to the paper's content or the residual
baseline; no repair of the hosted-runner paper tests (the paper branch's); no change to his keyboard settings by
an agent; no edit to `CLAUDE.md`'s Branching line (his file, on his read).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The version commit (four files and the lock) | G1 |
| D-2 | The changelog entry | G2, G3 |
| D-3 | `WP68-rounds/checks.md`: every check of G4 with its command, exit code and run link | G4 |
| D-4 | `WP68-rounds/captures/` and the browser pass table in `WP68-rounds/record.md` | G5 |
| D-5 | `WP68-rounds/release-issue.md`, then the issue and the pull request on his word | G6, G8 |
| D-6 | The read-back of his settings in `WP68-rounds/record.md` | G7 |
| D-7 | The after-merge record: the release run's jobs, the `paper` branch, the live checks ticked | G9 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | The version is written in the four places and nowhere reads 0.0.1 | `grep -rn "0\.0\.1" pyproject.toml CITATION.cff src/ CHANGELOG.md` empty; `uv run python -c "import hyperbolic_trade_space as h; print(h.__version__)"` |
| R-2 | Admissibility passes on the head before the pull request | the `qc/release` dry run at the head: `admissibility`, `test`, `build`, `site` green, the rest skipped |
| R-3 | Nothing outward before his word | `gh pr list`, `gh issue list`, `git ls-remote --tags` unchanged until his word is quoted in `WP64-decisions.md` |
| R-4 | No attribution line | the step in `test.yml`; `git log --format=%B e7fd1165.. \| grep -ciE "co-authored-by\|generated with"` is 0 |
| R-5 | The pull request's checks are the four required ones and green | the pull request's checks page |

## Definition of good

The merge is the first live run of a flow already seen green in WP67, with every check's evidence in the record
and nothing left for him but his settings, his read and the merge button.

## Definition of good enough

G1 to G6 done and recorded; R-1 to R-4 met; G7 to G9 wait on him and are done as he acts.

## Definition of done

Good enough met; the pull request merged by him; the release run green; the `paper` branch exists; the live checks
ticked; his acceptance recorded.

## Open decisions

None for the scope. The changelog's date is the merge's day, written when he says the word (a dry run before it
uses the day of the dry run and is rewritten).

## Agent's defaults

- One unit for G1 to G3 and D-3 (the version, the changelog, the punch list, the checks), after WP73 and WP74 land,
  so the tree it versions is the tree the pull request carries; the driver does G5 to G9.
- The release issue text names packages by their index rows, newest first, in one line each.
- The `qc/release` dry run at the head is the last run before the pull request; its branch is deleted afterwards.

## Amendments

- Amendment 1 (2026-11-17, his word in `WP64-decisions.md`, "Zenodo stays off"): Zenodo leaves G7 and G9; the 0.1
  release is not archived and mints no DOI. G8 waits, besides his settings and his word, on his click-through of
  the documentation and the top-level site (`WP68-rounds/his-site-review.md`).
