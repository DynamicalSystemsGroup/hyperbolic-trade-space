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

## Amendment 1 (2026-11-10): the remaining release items after WP28

**Status.** DRAFT, for the driver's approval; recorded in `WP8b-decisions.md` under "Amendment 1". Nothing below is
executed before then.

### What changes and why

The tree at afdb222 shows D-1 and D-4 done in substance (`LICENSE` is MIT, Dynamical Systems Group; the WP7
notebook, its test and its figures went at 4bd6bac), and the rest open. Four things the approved scope did not
carry have appeared since:

1. **The changelog stops at WP18.** `CHANGELOG.md` names no package after WP18, and its line 39 says the swap onto
   the new data (WP16) "is held at the time of writing"; WP16 was accepted on 2026-11-10 (`release-candidate.md`,
   step 4). D-2 is re-checked against WP19 to WP28, not only against the R-2 swap line.
2. **The punch list has drifted** (WP25-4 row T-8 hands it here): line 38 says the archive is "not yet archived" and
   cites `tests/test_notebook.py`, both gone at 4bd6bac; line 43 says the changelog is renamed "at the tag", where
   D-2 says at the candidate PR with no tag, and asks to confirm a version both places already read alike (0.0.1);
   lines 11-12 (root and paper URLs) and lines 24 and 32 (the `/` and `paper/` routes) list the same two pages;
   the reference-keys deferral (lines 40 and 49) and the container-image line (lines 41 and 50) appear twice. All
   22 boxes are unticked.
3. **A clean checkout does not stage** (`driver-log.md`, 2026-11-10, 19:05; WP25-4 row T-10 hands it here):
   `paper/myst.yml` line 65 reads `template: article-theme`, fetched at build time and not pinned (theme 1.4.1 in
   the main checkout's `paper/_build/templates`; `mystmd` 1.12.0 in `uv.lock`); `scripts/stage_site.py` in a fresh
   worktree fails at the theme's `/_public/` prerender unless that directory is copied in. A release must build
   from a clean checkout. This needs a file outside the scope's blast radius, so the amendment widens it by the
   files of the option the driver picks.
4. **D-6 is scoped** (the approved scope left "the mechanism chosen when D-6 starts").

The stale `examples/adcs/adcs_trade_study.ipynb` entry in `work-packages/interface-contract.toml` line 335
(`[ownership.technical].paths`) is WP25-4's row T-1 (contract amendment 17), not this amendment's; R-4 is met here
when T-1 lands.

### Remaining deliverables

| ID | Deliverable | Owner | Check |
|---|---|---|---|
| D-2 | `CHANGELOG.md`: line 39's swap sentence replaced by what WP16 changed; entries for WP19 to WP28 where they changed what a user, a reader of the docs or a reader of the paper sees, each naming its package; at the candidate PR the heading `[Unreleased] - target 0.1.0` becomes `[0.1.0] - <date of the PR>` and the "Not yet released" lines go | PM stream (entries now; the rename at the candidate PR) | R-2, R-11 |
| D-3 | `release-punch-list.md` brought current: line 38 ticked (archive cleared at 4bd6bac; T-1 cited for the contract line); line 43 rewritten to the version step as D-5 states it, with "at the candidate PR, no tag"; the root and paper pages listed once, in the post-release checks, with the expected-at-release section keeping the three URLs the link check reads; each duplicate (reference keys, container image) kept once; every one of the 22 boxes ticked, struck with the decision that moved it, or kept as a post-release check | PM stream | R-3, R-12 |
| D-6 | Stable reference keys from the docsite into the paper (below) | PM stream, after WP28 is accepted and subject to OD-A2 | R-6, R-13 |
| D-8 | The paper stages from a clean checkout: the article theme pinned or vendored, or the copy step made part of staging, per OD-A1 | the driver's call (OD-A1); a PM stream implements | R-14 |
| D-7 | The reviewer's guide in four sittings (unchanged) | the driver; goes last with D-5 | R-7, R-8 |
| D-5 | Version 0.1.0 in `pyproject.toml`, `__version__` and `uv.lock` (unchanged) | the driver; last | R-5 |

**D-6, scoped.** A *key* is the label the paper already gives an object: the 37 MyST `:label:` values in
`paper/paper.ipynb` (prefixes `def`, `thm`, `lem`, `prop`, `cor`, `fig`, `tab`), plus a label added to each
numbered section of the paper and each appendix of `paper/supporting_material.ipynb` (none carry one today; adding
them is the one paper edit D-6 makes, labels only, no text). The keys live where the paper defines them; the docs
build reads them from the built paper (the `myst build` output that `scripts/assemble_site.py` already stages) or
from the notebooks' sources, so there is no second list to keep in step. A docs page cites the paper with one
fixed syntax naming a key; the docs build resolves it to the paper's URL and anchor and fails on a key the paper
does not define. Today the docsite carries no citation into the paper, so the first citations are added in the same
unit, on the pages where a reader needs the proof or the figure. Files: the docs pages that cite, the resolver in
the docs build (`mkdocs.yml` hook or `scripts/build_generated.py`), the label lines in the two notebooks, a test in
`tests/test_site.py`.

**Changes to the approved scope.** Blast radius gains `paper/paper.ipynb` and `paper/supporting_material.ipynb`
(D-6 labels only, no text), and the files of OD-A1's chosen option: `paper/myst.yml` and the theme's location
(a), `paper/` vendored templates and `paper/myst.yml` (b), or `scripts/stage_site.py` and
`scripts/assemble_site.py` (c). The non-goal "no change to paper content" stands: labels are not content.

### Requirements added

| ID | Requirement | Checked by |
|---|---|---|
| R-11 | The changelog names every package from WP19 to WP28 that changed what a user or reader sees, or the driver's list says why one is left out; it claims the swap because WP16 is accepted; at the PR the 0.1.0 section is dated and nothing reads "Unreleased" or "target" | `grep -o 'WP[0-9]*[a-z]*' CHANGELOG.md \| sort -u` against `release-candidate.md`'s path; `grep -n -i 'swap\|unreleased\|target' CHANGELOG.md` |
| R-12 | The punch list holds no line the tree contradicts, no item twice, and 22 boxes each ticked, struck with a cited decision, or labelled post-release; `tests/test_site.py` still passes (it reads the "Expected-at-release links" URLs, the backticked live routes, "PyPI", "release notes" and "stable reference keys" from this file) | read beside `git log` and the decisions files; `uv run pytest -q tests/test_site.py -k punch_list` and the link-check tests |
| R-13 | Every docs citation of the paper goes through a key; an undefined or renamed key fails the docs build; the resolved links open the right anchor on the staged site | the D-6 test in `tests/test_site.py`; a key renamed in a scratch copy fails `uv run mkdocs build --strict`; a browser pass on the staged site |
| R-14 | A fresh worktree from `origin/dev`, with no `paper/_build/` copied in, stages the real paper | `git worktree add <tmp> origin/dev`; `uv run python scripts/stage_site.py`; the paper page loads at `/paper/` in the browser; the worktree removed |
| R-5 (restated) | The lock is consistent after the version step | `uv lock --check` |

R-1 to R-10 stand. The test reading `CHANGELOG.md`: none (grep of `tests/` and `scripts/`); the punch list is read
by `tests/test_site.py` only.

### Blast radius per item

| Item | Touches | Does not touch |
|---|---|---|
| D-2 | `CHANGELOG.md` | anything else |
| D-3 | `work-packages/release-punch-list.md` | `tests/test_site.py` (its requirement is unchanged) |
| D-6 | docs pages that cite, the resolver (`mkdocs.yml` hook or a script under `scripts/`), label lines in `paper/*.ipynb`, `tests/test_site.py` | paper text, figures, numbers |
| D-8 | per OD-A1: (a) `paper/myst.yml`; (b) `paper/myst.yml` and a vendored template directory under `paper/`; (c) `scripts/stage_site.py`, `scripts/assemble_site.py` and their tests | `.github/workflows/`, the paper's text |
| D-7, D-5 | as in the approved scope (driver-owned) | |

### Definition of good enough (amended)

The approved scope's list stands, with: R-11 to R-14 hold and are verified by the driver; D-2 and D-3 are done
before D-7 so the guide cites them; D-6 starts after WP28 is accepted (or moves after 0.1 by OD-A2); D-8 lands before
the driver's last staged-site pass; D-7 and D-5 go last. PyPI, the PDF export, an image on a registry, a tag, the merge
to `main` and any deployment stay non-goals.

### Agent's defaults (one item)

- D-6's keys are the paper's own labels, read from the paper, not a separate registry; this replaces the approved
  scope's default "a YAML registry read by the docs build" *(default)*.
- The changelog's 0.1.0 date is the candidate PR's date, as already defaulted; no tag *(default)*.
- The root and paper pages stay in the "Expected-at-release links" section (the link check reads them there) and
  their boxes move to the post-release checks *(default)*.

### Open decisions (for the driver)

- **OD-A1. How a clean checkout gets the article theme.** (a) Pin the theme version in `paper/myst.yml` (a
  versioned template reference, so `myst build` fetches 1.4.1 or the chosen version); (b) vendor the theme's
  templates under `paper/` and point `paper/myst.yml` at that path; (c) document the copy step and have
  `scripts/stage_site.py` fetch or copy the templates itself before the build.
- **OD-A2. When D-6 lands.** The approved scope records it inside 0.1, after WP11 (the supervisor's words of
  2026-11-08 and `release-candidate.md` step 6). (a) Inside 0.1, after WP28 is accepted, as recorded; (b) after 0.1,
  with the punch list's deferral line kept and the docsite still citing nothing in the paper at the candidate.
