# WP73 — Scope of work: the process record leaves the tree before 0.1

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under his answer of 2026-11-16 ("Before 0.1") and his rule on repository, history and index (CLAUDE.md, 2026-11-15) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; branch `dev`, after WP67 lands and before WP68's pull request |
| **Approval record** | His answer "Before 0.1" to the question when the process record leaves the tree (asked with the external review's disposition), quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's independent run and read of the index; his read of `supervisor-review-list.md` before WP68's pull request |

## Purpose

His rule: the repository's job is the current state, git history's job is the trajectory, and the indexes and ledgers
in the tree make the historical material discoverable and dereferenceable (`git show <hash>:<path>`). A package's
documents leave the tree at its landing. Forty-odd packages have landed with their documents still in place: 709 of
1,113 tracked files and 51 MB under `work-packages/`, most of it review captures. The external review of 2026-11-16
named the same gap. Before the first merge into `main`, the tree holds only what the rule keeps.

## Goals

- G1. For every package whose index state is landed, accepted, delivered or superseded, its documents (`WPn-scope-of-work.md`,
  `WPn-rounds/`, `WPn-review.md`, spike outputs, design documents and captures) leave the tree, and its `INDEX.md`
  row names the commit at which each is read (`git show <hash>:work-packages/<file>`), in the index's existing form.
- G2. What the rule keeps stays: `INDEX.md`, `driver-log.md`, every `WPn-decisions.md`, the length ledger, the claims
  register, `PM-BRIEF.md`, `README.md`, the interface contract and its manifest, `release-candidate.md`, the two
  release checklists, `release-punch-list.md`, `paper-requirements.md`, `milestones.md`, `review/open-questions.md`,
  `review/external-review-2026-11-16.md`, `supervisor-review-list.md`, `WP65-design/his-items.md` (WP68 reads it),
  `WP67-rounds/record.md` (WP68's release issue cites it), the documents of packages in flight (WP8b, WP11, WP58,
  WP68 when scoped).
- G3. Every reference into a removed path from outside the record is resolved: a test or a generator that reads a
  data file of a package (WP11-final, WP30's ladders, WP51's data and the like) gets that file at a place of the
  current state (`tests/data/`, `examples/`, `paper/`), moved with `git mv` so history follows; a citation from the
  paper, the docs or a note is repointed to the pinned blob URL at the archive commit; a link that did no work is
  dropped.
- G4. The material he has not yet read (the index's "his read pending": WP55, WP56, WP57's review, WP63, WP70, WP71,
  WP72 and the rest so marked) is listed in `supervisor-review-list.md`, one row per item with its blob URL at the
  archive commit and the question it carries.
- G5. A test backs the index: every "in history" row's hash and path dereference (`git cat-file -e <hash>:<path>`), and
  no tracked path outside `work-packages/` names a path the archive removed.

## Non-goals

No change to any document's content before it leaves; no history rewrite or force push; nothing removed from the
decisions files or the driver log; no change to the package, the docs' pages, the paper's content or the site beyond
the repointed links; no `.gitattributes` or LFS; no archive outside git.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The archive commits on `dev` (one per group of packages, each message naming the packages and the hash to read them at) | G1 |
| D-2 | `INDEX.md` rows updated; the "Documents" column of every archived package reads "in history: `git show <hash>:work-packages/<file>`" | G1 |
| D-3 | Data files moved with `git mv`; citations repointed; a table of every reference and what was done with it in `WP73-rounds/references.md` (which itself leaves at WP73's landing, its hash in the index) | G3 |
| D-4 | `supervisor-review-list.md` with the pending reads and their URLs | G4 |
| D-5 | `tests/test_index.py` | G5 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | After the archive, `git ls-files work-packages` holds only G2's list plus in-flight packages' documents | the listing, read against G2 |
| R-2 | Every removed document is readable at the hash the index names | `uv run pytest -q tests/test_index.py` |
| R-3 | Nothing outside the record names a removed path | the same test; `grep -rn "work-packages/" src tests docs paper site scripts` read against D-3's table |
| R-4 | The software suite, the register, the residual and vocabulary checks, the docs build and the site stage pass after the move | `uv run pytest -q -m "not slow"`, `tests/test_claims_register.py`, `scripts/check_residuals.py --compare --strict`, `scripts/check_vocabulary.py`, `mkdocs build`, `scripts/stage_site.py` |
| R-5 | The paper's tests that read moved data still pass | `HTS_PAPER_TESTS=1 uv run pytest -q -m paper -k "data or record or ladder or grid"` and the names D-3's table lists |
| R-6 | No attribution line; no metanarration | the grep; a read |

## Definition of good

A clone of `dev` shows the method, the package, the docs, the paper and the live ledgers, and nothing of how they
were made except through the index; every historical document is one `git show` away, named in the index.

## Definition of good enough

R-1 to R-6 met; the driver's acceptance as proxy; `supervisor-review-list.md` ready for his read; landed on `dev`
before WP68's pull request.

## Definition of done

Good enough met; WP68's pull request opened on his word with the tree in this state.

## Open decisions

None. The rule and the timing are his; the list of what stays (G2) follows the rule's own enumeration plus what an
open package reads.

## Agent's defaults

- The material pending his read leaves with the rest and is read at its blob URL from `supervisor-review-list.md`
  (the alternative, keeping it until he reads, would carry 30 MB of captures into the release).
- Captures and images leave with their packages; no thumbnail or summary image is kept in their place.
- Data files move to `tests/data/<wpN>/` when only tests read them, to `paper/data/` when the paper's generators read
  them, with the path constant in each reader changed and nothing else.
- One unit, in a worktree on `dev` after WP67 lands; archive commits grouped by tens of packages so each message
  stays readable.
