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
- G2. One rule for citing the paper from the docs, decided once (OD1) and written where authors find it, so later
  packages cite the paper the same way.

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
| D-1 | The reworded pointers: the sentences carrying the 18 `paper:` citations on `docs/index.md`, `docs/theory.md` (6), `docs/bridge.md` (4), `docs/user-guide/temperature.md` (4), `docs/examples.md`, `docs/further-reading.md`, `docs/user-guide/fitting.md`, `docs/user-guide/termination.md`; the prose mentions of the paper on `docs/user-guide/limitations.md` ("Appendix E of the paper"), `docs/api-reference.md`'s docstring index ("Theorem 1", if the docstring is the docs' own text and not the package's), `docs/code-owners.md` where it describes the paper's lifecycle; the root page `site/index.html` (the sentence "The paper makes the argument and gives the proofs" and the card "Read the paper"); `README.md` (the first paragraph's "the paper" and the repository map) | G1 |
| D-2 | The rule, `notes/paper-references.md` *(default path)*: how a docs page cites the working paper (the words, the link, what a key may point at), the inventory of every pointer with its disposition (kept and reworded; replaced by the docs' own statement; removed), and the test that holds the rule | G2 |
| D-3 | The claims register rows re-anchored where a registered sentence changed; the vocabulary baseline untouched | G1 |
| D-4 | The records: `WP81-decisions.md` (his approval, OD1, the acceptance), `WP81-review.md`, the WP81 row in `work-packages/INDEX.md`, `WP81-rounds/` (the site read, the captures, the cold reads) | the gates |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The inventory is complete and every pointer has a disposition | `grep -rn "paper:" docs README.md site/index.html` and `grep -rn -i "the paper\|the working paper" docs/*.md docs/user-guide/*.md README.md site/index.html` list exactly the rows of D-2's inventory; each row says kept, replaced or removed |
| R-2 | Every surviving pointer tells the reader what it points at and what is published (G1) | a read of each sentence against the rule; the test of D-2 (`tests/test_site.py`, a new test *(default)*) asserts the rule mechanically for every `paper:` citation on every docs page, in the form OD1 decides |
| R-3 | The root page and the README say the same thing as the docs about the paper | a read; `uv run pytest -q tests/test_site.py -k "root_index or history"`; the root page's register rows (`claims_register.toml`, file `site/index.html`) re-anchored and `uv run pytest -q tests/test_claims_register.py` green |
| R-4 | The docs build in both slots | `HTS_PAPER_SLOT=abstract uv run mkdocs build --strict` and `HTS_PAPER_SLOT=pin uv run mkdocs build --strict`, after `build_generated.py`, `build_figures.py` (with `MPLCONFIGDIR` set) and `build_site_figures.py` |
| R-5 | The prose rules hold on every touched page | no metanarration (`scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` reports no new rise on a touched surface; the checker's patterns run over the touched example or root text where it is not a surface); `uv run python scripts/check_vocabulary.py` 0 new; `uv run pytest -q tests/test_site.py -k budget` (no page over its budget; a reworded sentence pays for itself) |
| R-6 | The pages are read as rendered | each touched page served from the strict build and captured at 1280 and 375 px, light and dark (`WP81-rounds/capture.mjs`, the WP76 script moved or copied); a fresh cold reader given the home and the theory page says in one sentence each what the paper is, where it is, and what following a link gets them, and is right |
| R-7 | The checks are green at the branch's head | `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `MPLCONFIGDIR=<scratch> uv run pytest -q -m "not slow and not paper"`; the site, docs, register, references, contract and index tests; `grep -rn "Co-Authored-By\|Generated with" <the files of D-1 to D-4>` finds nothing; `git diff --name-only <WP81 base>..HEAD` names only D-1 to D-4's files |

## Definition of good

A reader of any docs page knows, from the sentence in front of them, that the paper is a working paper, what of it
is published, what the pointer names, and how to build the full text; no link surprises them with an abstract; and an
author of a later page has one rule to follow and a test that fails when they break it.

## Definition of good enough

- R-1 to R-7 met on one commit of `v0.2`, with the evidence in `WP81-review.md` from a fresh-context reviewer.
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
- **The words.** "The working paper" names the paper on every surface; the first pointer on a page says what is
  published ("its abstract is published; the full text builds from the repository, `paper/`"), later pointers on the
  same page name their target only; a key that names a result (`thm-`, `def-`, `fig-`, `appendix-`) is cited as
  "Theorem such-and-such of the working paper" in the docs' words, never as a bare "the paper".
- **The test** lives in `tests/test_site.py`: for every `paper:` citation on a docs page, the sentence or the page's
  first paper pointer carries the words the rule prescribes; it runs in both slots.
- **The abstract page's own wording** (that the paper is a working paper and how the full text builds) is the paper
  branch's: one request to the v0.1 session, recorded; nothing here depends on it.
- **The root page** is in scope as a surface that points at the paper (the sentence and the card), nothing else on it
  changes; its register rows are re-anchored.
- **The API reference**: a docstring that cites "Theorem 1" is the package's text, out of scope (no change to
  `src/`); the note records it as a candidate for the package's next release.
- **Budgets.** Every touched page stays within its budget; a longer sentence is paid for on the same page; the
  docsite total stays.
- **Captures and reads** as in WP76: the capture script and eight-plus captures in `WP81-rounds/`; the cold reader a
  fresh-context subagent; the review a fresh-context reviewer; `MPLCONFIGDIR` set for every build and test.
- **The breakdown's row** on `work-packages/milestones.md` ("After 0.1") is proposed to the v0.1 session, which owns
  the board on `dev`; this branch does not edit `milestones.md`.

## Open decisions (for the supervisor)

- **OD1.** The rule for `paper:` links while the paper is in abstract mode (they resolve to the abstract page with
  no anchor). Options: (a) keep every link, each in a sentence that names the working paper and its target, so the
  reader lands on the abstract knowing why; (b) remove the links from the docs until a pin is served, each pointer
  replaced by the docs' own statement of the result (the theory page carries the definitions) and one sentence on
  the home and in Further reading naming the working paper and how to build it; (c) keep a link only where a named
  result is cited (a theorem, definition, figure or appendix key) and drop the general "the paper makes the argument"
  pointers, replacing those with the docs' own words.
- **OD2.** The Agent's defaults, as one item: approve the list, or change items.
