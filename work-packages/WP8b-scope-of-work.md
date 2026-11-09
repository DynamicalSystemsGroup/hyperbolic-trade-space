# WP8b - Scope of work: release preparation for 0.1.0

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing new in this package is executed before then; the items already pushed (D-1 to D-4) are covered retroactively. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `posynomial-invariant-form` (branch `dev`); this document lives in `work-packages/` |
| **Approval record** | The driver's approval under the mandate of `work-packages/release-candidate.md`, quoted verbatim in `work-packages/WP8b-decisions.md` |
| **Acceptance record** | The supervisor's merge of the PR from `dev` to `main`, after the driver's verification |

## Purpose

`release-candidate.md` step 6 names this package: "version, license file, changelog, the archive
cleared, stable reference keys from the docsite into the paper, the punch list, the reviewer's guide
in sittings". Some of it was started before a scope existed (the board marks WP8b "NOT YET SCOPED").
The mandate: "your job is to loop on the dev using local host and all the tools at your disposal to
get me a candidate release ... i will do my own comprehensive review ... if you present the information
badly i wont be able to sign off on it". On the hand-off: "Sittings by output". On the references:
the docsite links into the paper by stable keys "once the paper and its appendices are stable (after
WP11)" (2026-11-08). On the archive: "archive it with banner for now so we can use it as reference
but plan to clean out the archive before the first release". License: "MIT, copyright
DynamicalSystemsGroup". PyPI is deferred.

## Goals

- G1. The repository carries what a 0.1.0 release needs: version, license, changelog, an empty archive, an up-to-date punch list.
- G2. The docsite refers into the paper through stable reference keys, so links survive section moves.
- G3. The supervisor can review the candidate in four sittings by output, each short enough for a person.
- G4. Existing early deliverables are brought under this scope and checked against it.

## Non-goals

- No tag, no merge to `main`, no deployment, no publishing (the PR itself is the supervisor's to merge).
- No PDF export, no PyPI or TestPyPI, no image on a registry.
- No WP12 search; no change to paper content, figures or numbers (WP10, WP11, WP19 own those).
- No change to the package's behaviour; the version string is the only source edit.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `LICENSE` (MIT, 2026 Dynamical Systems Group; pushed in fde5fc0, covered retroactively) | G1, G4 |
| D-2 | `CHANGELOG.md`, section 0.1.0 (fde5fc0, ce80b39; retroactive); dated at the candidate, no tag | G1, G4 |
| D-3 | `work-packages/release-punch-list.md` brought up to date (ce80b39; retroactive), items ticked or decided | G1, G4 |
| D-4 | The archive cleared: the retired WP7 notebook no longer shipped, with `tests/test_notebook.py` and `work-packages/interface-contract.toml` (and `.md`) amended together | G1, G4 |
| D-5 | Version 0.1.0 in `pyproject.toml`, `uv.lock` and `__version__` in `src/hyperbolic_trade_space/__init__.py` (driver-owned) | G1 |
| D-6 | Stable reference keys: a key registry resolved at build time; docsite pages cite the paper by key | G2 |
| D-7 | The reviewer's guide, `work-packages/reviewers-guide/`: four sittings (the paper; the docsite and root page; the code and derivations; the calls made for him), each with a short checklist and its own localhost entry point | G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `LICENSE` is MIT, names Dynamical Systems Group, and agrees with `license` in `pyproject.toml` | `head -5 LICENSE`; `grep -n license pyproject.toml` |
| R-2 | `CHANGELOG.md` has a 0.1.0 section; every entry names its package; nothing claims the data swap unless it is done | read the file; `grep -n -i swap CHANGELOG.md` against `driver-log.md` |
| R-3 | The punch list has no stale line: each item is ticked, or marked deferred with the supervisor's quoted reason | read `release-punch-list.md` beside the decisions files it cites |
| R-4 | No archived notebook or archive folder remains; no test, manifest line or doc points at it; the suite passes | `git ls-files examples/adcs \| grep -i -E "archive\|adcs_trade_study"` is empty; `uv run pytest`; contract test passes |
| R-5 | The version reads 0.1.0 in all three places and the lock is consistent | `grep -n version pyproject.toml`; `uv run python -c "import hyperbolic_trade_space as h; print(h.__version__)"`; `uv lock --check` |
| R-6 | Every docsite citation of the paper goes through a key; a renamed or moved section fails the build, not the reader | `uv run mkdocs build --strict`; rename a key in a scratch copy and see the build fail |
| R-7 | The guide has four sittings; each has a checklist of at most about ten lines and a localhost entry point that opens | open each entry point after the one-command staging (`scripts/stage_site.py`) |
| R-8 | The calls sitting lists every call in `driver-log.md` with its evidence, every changed number with its reason, and what is known weak | compare against `driver-log.md` and the data-swap record |
| R-9 | No file touched carries an attribution line; no tag, deployment or publication occurred | `git log` trailers check; `git tag`; the attribution test |
| R-10 | The whole suite, lint, format, lock check, lemma chain and proof-map checker pass | `uv run pytest`; `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check` |

## Definition of good

- A reader opens the guide, takes one sitting on one day, and knows what to look at, in what order, and
  what a pass looks like, without the driver present.
- The citations from docs to paper read as natural cross-references, as LaTeX labels do.
- The punch list at the end is the real list of what happens after the merge, in order.

## Definition of good enough

- R-1 to R-10 hold, each verified by the driver independently and recorded.
- D-1 to D-4, already pushed, have been checked against this scope and corrected where they differ.
- D-6 and D-7 begin only after WP11's stopping rule is met and the paper and its appendices are stable;
  D-5 last, so the version is not set before the content is.
- The guide is sized for a person: each sitting fits on one screen of checklist.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

### Blast radius

The package may touch: `LICENSE`, `CHANGELOG.md`, `work-packages/release-punch-list.md`, the archive
(the retired notebook and the lines that pin it in `tests/test_notebook.py` and
`work-packages/interface-contract.{md,toml}`), `pyproject.toml`, `uv.lock` and `__version__`
(driver-owned), `work-packages/reviewers-guide/`, and, only when D-6 starts, the docs files and
build scripts that resolve reference keys. It does not touch the paper's text, the case, the
derivations, `.github/workflows/`, or any other stream's files on `parallel-board.md`.

## Agent's defaults

- The guide lives in `work-packages/reviewers-guide/`, one file per sitting plus an index *(default)*.
- Reference keys are plain identifiers in a YAML registry read by the docs build, one key per paper section, figure and appendix *(default)*; the mechanism is chosen when D-6 starts.
- The checklist length (about ten lines) and the check commands in R-1 to R-10 *(default)*.
- The 0.1.0 changelog date is the date of the candidate PR *(default)*.
- Order of work: D-4, D-5 and D-7 scaffolding as inputs settle; D-6 after WP11 *(default)*.
- The driver verifies each deliverable independently and records the verdict in `WP8b-decisions.md` *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop: the supervisor's words settle the references (inside 0.1, after WP11: 2026-11-08 and the release-candidate path), the hand-off ("Sittings by output"), the license, and the archive. 0 decided here, 0 deferred, 0 raised.

## Gate outcomes

- 2026-11-09: approved for execution by the driver under the mandate (`release-candidate.md`), for the supervisor's review at the PR; no open decision remained. Recorded in `driver-log.md`.
