# Reviewer's guide, skeleton (DRAFT, for the PM)

Working document, not for users. Headings and a one-line intent each; the paths are the records that fill the
section. Sittings by output, one entry point each (`release-candidate.md`, "The hand-off"; `WP8b-scope-of-work.md`,
D-7, R-7, R-8). Sized for a person: at most about ten checklist lines per sitting.

## 0. Front page

One screen: the named head, what the package is, the order to take the sittings, what a pass looks like.
Records: `release-candidate.md` ("What candidate means"); `deliverables-grid.md`; `status-report-template.md`.

## 1. What is in the package, by deliverable

The rows of the deliverables grid in one table: deliverable, what it is, where to open it, state, last evidence.
Records: `deliverables-grid.md`; `CHANGELOG.md`; `release-candidate.md` ("The path to the candidate").

## 2. How to read it

Two ways in, same material.

- **In an hour.** The shortest path per journey (Explore, Use, Theory, Model, Evaluate): which page, which figure,
  which proof. Records: `deliverables-grid.md` (journey columns, personas); `docs/superpowers/notes/reader-grid.md`;
  `PM-BRIEF.md`, "One size fits none: journeys and signposting".
- **In a day.** The four sittings, each a checklist and a localhost entry point:
  1. the paper (and its appendices); 2. the docsite and root page; 3. the code and derivations; 4. the calls made for
  him. Records: `WP8b-scope-of-work.md` (D-7); `scripts/stage_site.py`; `reviewers-guide/` (to be created).

## 3. What was verified, and how

Machine verification and human validation kept apart (glass-box seams).

- **Machine verification.** Suite, lint, format, lock check, lemma chain and proof map; claims register;
  vocabulary check; container regression; CI on three platforms with the run links.
  Records: `WP8b-release-checklist.md` (B, C); `paper/container/RECORD.md`; `WP34-review.md`;
  `derivation/` and the proof-map output; `claims_register.toml`; `WP30-gate-checklist.md`.
  The residual pass's machinery (WP38): the reader's brief `docs/superpowers/notes/residual-review.md`, the surface
  inventory `scripts/prose_surfaces.py`, the checker `scripts/check_residuals.py` with its committed baseline
  `scripts/residuals_baseline.json` (re-run it with `--compare` to see no count has risen), `tests/test_residuals.py`.
- **Human validation.** Reader rounds, the reader grid and its worst cells, the browser pass with screenshots,
  the expert and novice mathematics reads, package-user tests. Records: `WP11-decisions.md`; `WP28-retest.md`;
  `WP29-review.md`; `WP30-review.md`; `WP32-*`, `WP33-*` records; `docs/superpowers/notes/presentation-framing.md`.
  The residual pass (WP38): a fresh reader's flag table and a second reader's confirmation for every prose surface,
  and the checker's counts before and after. Records: `WP38-scope-of-work.md`; `WP38-flags/`; `WP38-confirmations/`;
  `WP38-review.md`; `WP38-decisions.md`.

## 4. What the supervisor must decide

The decisions only he holds, as plain options with no steering; and the calls he may revert.

- Calls the assistant made, each with reason, record and landing commit. Records: `supervisor-review-list.md`;
  `driver-log.md`.
- Entry surfaces (the five entry surfaces' changes since the data gate, each with reason and commit): the
  "Entry surfaces" section of `supervisor-review-list.md`.
- Questions genuinely held for him (values only he holds, changes to his stated intent, outward acts), e.g. the
  sample size, the Figure 1 footer wording, the "no candidate meets the requirements" finding.
  Records: `PM-BRIEF.md` (current handover); `WP30-decisions.md`; `deliverables-grid.md` (open items).
- The merge itself: his alone. Record: `release-candidate.md` ("The mandate").

## 5. Every number that changed

Changed conclusions first, then each moved number with its reason. Records: `swap-evidence.md`;
`WP30-decisions.md` and the data-gate comparison; `WP8b-decisions.md` (D-2 entry).

## 6. Known gaps

What is weak or not done, stated once each, with where it is tracked. Records: `deliverables-grid.md` (cells not
`A`); `release-punch-list.md` (post-release items); `WP8b-review.md` (gaps G-1 to G-6 and later reviews); reader-grid
worst cells; Windows docs-paper shard (Linux and macOS only, `WP34-decisions.md`); after 0.1: search (WP12),
PyPI, PDF export.

## 7. Where the evidence lives

An index: each record type, its path, its owner. Records: `README.md` (work-packages board and gates table);
`parallel-board.md`; the `WPn-decisions.md` and `WPn-review.md` files; the residual pass's records (`WP38-flags/`,
`WP38-confirmations/`, the baseline `scripts/residuals_baseline.json`); screenshot directories named in the reviews;
`paper/container/RECORD.md`; the CI run links.
