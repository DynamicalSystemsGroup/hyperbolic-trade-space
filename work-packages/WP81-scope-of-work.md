# WP81 — Scope of work: the paper as a working paper (0.2 documentation improvement, package 1)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/tradespace`; branch `v0.2` (the 0.2 integration branch, cut from WP76's head over `dev` c0e210cc, in this worktree); nothing on `dev` or `main`; `v0.2` merges into `dev` after 0.1 is out and after his review |
| **Approval record** | His word in chat, quoted verbatim in `work-packages/WP81-decisions.md` |
| **Acceptance record** | His word in chat after the technical verification and his read of the reworded pages, quoted verbatim in `work-packages/WP81-decisions.md` |

## Purpose

His direction (2026-11-17, `WP81-decisions.md`): "i also want to clean up the references to the paper which is
currently a working paper. only the abstract is published as a webpage but the full content can be built from the
repo. per our recent changes the paper gets its own development path." The docs cite the paper with `paper:` keys
that resolve, in the abstract mode the paper is in, to the abstract page with no anchor (`scripts/paper_keys.py`), so
every one of the 18 citations on nine pages, the root page's card "Read the paper: the argument and the proofs" and
the README's "the paper" sentence sends a reader to an abstract for an argument, a theorem, a definition, a figure
or an appendix it does not hold. The first package of the 0.2 documentation improvement (the breakdown he OK'd,
`WP81-decisions.md`): it fixes how every later page may cite the paper.

## Goals

- G1. Every pointer into the paper on the docs pages, the README and the root page reads true for a working paper
  whose abstract alone is published and whose full text builds from the repository on its own branch (his words
  above): a reader who follows one knows what they will and will not find, and how to build the rest.
- G2. One rule for citing the paper from the docs, decided once (OD1: "Remove until a pin") and written where authors
  find it, so later packages cite the paper the same way: while the paper is in abstract mode the docs carry no
  `paper:` link; each pointer becomes the docs' own statement of the result; one sentence on the home and one in
  Further reading name the working paper and how to build it; the links return under the rule when a pin is served.

## Non-goals

- No change to the paper, its branch, its mode (`paper/mode.toml`), its key manifest (`paper/paper-keys.json`), the
  composer or the release machinery; the paper's own abstract page is the paper branch's (a request to it is an
  Agent's default below, not a dependency).
- No change to `scripts/paper_keys.py` beyond what the rule of OD1 needs *(default: none)*.
- No content change beyond the sentences that point at the paper and the rule's note: the level-set figures are
  package 2, the home and Getting started split package 3, the reader's path package 4, the vocabulary package 5.
- Nothing for 0.1: no commit on `dev` or `main`, no pull request, no tag, no deployment.
- No change to `src/`, `pyproject.toml` or `uv.lock`; no new dependency; no AI attribution anywhere.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The pointers removed and their sentences rewritten as the docs' own statements: the sentences carrying the 18 `paper:` citations on `docs/index.md`, `docs/theory.md` (6), `docs/bridge.md` (4), `docs/user-guide/temperature.md` (4), `docs/examples.md`, `docs/further-reading.md`, `docs/user-guide/fitting.md`, `docs/user-guide/termination.md`; the prose mentions of the paper on `docs/user-guide/limitations.md` ("Appendix E of the paper"), `docs/api-reference.md`'s docstring index ("Theorem 1", if the docstring is the docs' own text and not the package's), `docs/code-owners.md` where it describes the paper's lifecycle; the root page `site/index.html` (the sentence "The paper makes the argument and gives the proofs" and the card "Read the paper"); `README.md` (the first paragraph's "the paper" and the repository map) | G1 |
| D-2 | The rule, `notes/paper-references.md` *(default path)*: no `paper:` link on a docs page while the paper is in abstract mode; the one sentence on the home and the one in Further reading that name the working paper and how to build it; how a link returns when a pin is served (the key, the words); the inventory of every pointer with its disposition (replaced by the docs' own statement; removed; the two naming sentences); and the test that holds the rule | G2 |
| D-3 | The claims register rows re-anchored where a registered sentence changed; the vocabulary baseline untouched | G1 |
| D-4 | The records: `WP81-decisions.md` (his approval, OD1, the acceptance), `WP81-review.md`, the WP81 row in `work-packages/INDEX.md`, `WP81-rounds/` (the site read, the captures, the cold reads) | the gates |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The inventory is complete and every pointer has a disposition | `grep -rn "paper:" docs README.md site/index.html` finds nothing on a docs page; `grep -rn -i "the paper\|the working paper" docs/*.md docs/user-guide/*.md README.md site/index.html` lists exactly the rows of D-2's inventory (the two naming sentences, the README, the root page, code owners); each row says replaced, removed or names |
| R-2 | Each replaced pointer states the result in the docs' own words, no wider than what backs it, and the two naming sentences say what is published and how the full text builds (G1) | a read of each rewritten sentence against its former target (a definition stays a definition; a theorem cited becomes a statement the register backs by its lemma); the test of D-2 (`tests/test_site.py`, a new test *(default)*) fails on any `paper:` citation on a docs page while `paper/mode.toml` is in abstract mode, and asserts the two naming sentences are present |
| R-3 | The root page and the README say the same thing as the docs about the paper | a read; `uv run pytest -q tests/test_site.py -k "root_index or history"`; the root page's register rows (`claims_register.toml`, file `site/index.html`) re-anchored and `uv run pytest -q tests/test_claims_register.py` green |
| R-4 | The docs build in both slots | `HTS_PAPER_SLOT=abstract uv run mkdocs build --strict` and `HTS_PAPER_SLOT=pin uv run mkdocs build --strict`, after `build_generated.py`, `build_figures.py` (with `MPLCONFIGDIR` set) and `build_site_figures.py` |
| R-5 | The prose rules hold on every touched page | no metanarration (`scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` reports no new rise on a touched surface; the checker's patterns run over the touched example or root text where it is not a surface); `uv run python scripts/check_vocabulary.py` 0 new; `uv run pytest -q tests/test_site.py -k budget` (no page over its budget; a reworded sentence pays for itself) |
| R-6 | The pages are read as rendered | each touched page served from the strict build and captured at 1280 and 375 px, light and dark (`WP81-rounds/capture.mjs`, the WP76 script moved or copied); a fresh cold reader given the home and the theory page says in one sentence each what the paper is, where it is, and what following a link gets them, and is right |
| R-8 | The review is visual and by journey, and the choices are made before the edits (his direction, `WP81-decisions.md`, "The review method") | Before any edit: the twelve journeys of `notes/user-journeys.md` (personas P1 to P8, U1 to U4 of `notes/reader-grid.md`) traced through every page that points at the paper, each as a fresh-context reader of the rendered page with a screenshot per step, in `WP81-rounds/journeys.md`; the findings organised per persona and per pointer; where personas want different things (a P5 reader who wants the theorem's link against a U1 reader who wants no detour) the competing preferences are written out with the choice and its reason before the sentence changes; after the edits the same journeys re-traced with screenshots, the before and after side by side |
| R-7 | The checks are green at the branch's head | `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `MPLCONFIGDIR=<scratch> uv run pytest -q -m "not slow and not paper"`; the site, docs, register, references, contract and index tests; `grep -rn "Co-Authored-By\|Generated with" <the files of D-1 to D-4>` finds nothing; `git diff --name-only <WP81 base>..HEAD` names only D-1 to D-4's files |

## Definition of good

A reader of any docs page knows, from the sentence in front of them, that the paper is a working paper, what of it
is published, what the pointer names, and how to build the full text; no link surprises them with an abstract; and an
author of a later page has one rule to follow and a test that fails when they break it.

## Definition of good enough

- R-1 to R-8 met on one commit of `v0.2`, with the evidence in `WP81-review.md` from a fresh-context reviewer.
- The cold reader's two answers right.
- His read of the reworded pages.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- **Number and branch.** WP81 (WP77 to WP80 exist on `dev` and its branches); on `v0.2` in this worktree, the base
  being the commit that adds this scope.
- **The note's path** is `notes/paper-references.md`, beside `notes/examples-template.md`; its inventory table is the
  record of R-1.
- **The words.** "The working paper" names the paper wherever it is named (the home, Further reading, the root page,
  the README, code owners); the naming sentence says that its abstract is published at `/paper/` and that the full
  text builds from the repository (`paper/`, its own branch); a replaced pointer states the result in the docs' words
  with no mention of the paper; a theorem's statement in the docs is backed in the register by its lemma, as the
  theory page's rows are today.
- **The test** lives in `tests/test_site.py`: while `paper/mode.toml` is in abstract mode no docs page carries a
  `paper:` citation, and the home and Further reading carry the naming sentence; the `paper_keys` hook and its tests
  stay as they are for the day a pin is served.
- **The abstract page's own wording** (that the paper is a working paper and how the full text builds) is the paper
  branch's: one request to the v0.1 session, recorded; nothing here depends on it.
- **The root page** is in scope as a surface that points at the paper (the sentence and the card), nothing else on it
  changes; its register rows are re-anchored.
- **The API reference**: a docstring that cites "Theorem 1" is the package's text, out of scope (no change to
  `src/`); the note records it as a candidate for the package's next release.
- **Budgets.** Every touched page stays within its budget; a longer sentence is paid for on the same page; the
  docsite total stays.
- **The order of work.** The inventory (R-1); the journeys traced with screenshots and the findings organised per
  persona and pointer, competing preferences written out, the disposition of every pointer recorded (R-8); only then
  the edits; then the rendered review (R-6) and the journeys re-traced (R-8); then the fresh-context review.
- **Captures and reads** as in WP76: the capture script and the captures in `WP81-rounds/`; the journey readers and
  the cold reader fresh-context subagents, one persona each; the review a fresh-context reviewer; `MPLCONFIGDIR` set
  for every build and test.
- **The breakdown's row** on `work-packages/milestones.md` ("After 0.1") is proposed to the v0.1 session, which owns
  the board on `dev`; this branch does not edit `milestones.md`.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (2 decided, 0 deferred, 1 raised and folded; `WP81-decisions.md`,
"Scope gate"). OD1: the paper links come out of the docs until a pin is served ("Remove until a pin"); OD2: the
Agent's defaults approved as one item ("Approve the list") after his review method was folded in as R-8.
