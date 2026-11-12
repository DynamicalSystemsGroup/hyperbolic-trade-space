# WP37 — Scope of work: a history and acknowledgements page, linked from the root page

| | |
|---|---|
| **Status** | DRAFT, for the assistant's approval. Approved only by the recorded act below; nothing further is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The assistant's approval, quoted verbatim in `work-packages/WP37-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim in `WP37-decisions.md`, after `WP37-review.md` |

## Purpose

The supervisor's words, verbatim (`WP37-decisions.md`, 2026-11-12).

The purpose (decision record 6d70f44):

> the purpose of the history page is to acknowledge people and lineage of this work. some of these people worked
> for DSG, some still do, still some others were just our collaborators. some of the academic work predates DSG
> founding as blockscience (eg the GGP work with preciado on viral propogation and my own work on convex
> optimization). the goal is not to overload any one point, its mostly pointers. its just that most of the real
> history of this work does not fit nicely in the academic paper citations which necessarily focused on direct
> technical/mathematical lineage rather than the human lineage

The risk the page offsets (2f26713):

> critically, the history page offsets a risk that this work is treated as AI generated out of the blue, rather
> than synthesis and publication of long running endeavor

Its size (1179f7e):

> we're keeping this page as thin as we can while establshing the work arc over 10+ years

On running it as a package:

> you have the right idea; lets just make sure we have requirements, structure, assessment machinery etc

The page is stand-alone, linked off the root page, and touches neither the paper nor the documentation. A first
draft (`site/history.html`), its link checker (`scripts/check_history_links.py`) and four research tables
(`work-packages/WP37-rounds/`, W1 to W4) exist at head `b3919b1`. They are the first delivery against this scope, not
a substitute for it: this package fixes what the page must be, makes the checks repeatable, and routes the
supervisor's open items to him.

## Goals

- G1. **The people and the human lineage are acknowledged:** the supervisor's named list (thirteen at this head), each
  with a dated work or a stated role, and the three kinds of relation (worked for the firm, still do, collaborators)
  stated only where a public source or the team's own account says so.
- G2. **The page offsets the "generated out of the blue" reading:** a reader can walk dated pointers to public work
  from the early convex optimization and GGP work through cadCAD, GDS and PSuU to OpenMBEE, OpenSysML and this
  synthesis, and trace the line back.
- G3. **The arc is established over more than ten years, 2013 to now, with the fewest pointers that let a reader walk
  it:** thin, one screen, mostly pointers.
- G4. **The page is rigorously sourced:** every link resolves and matches its claim; every sentence is sourced, shown by
  a link, or marked as the team's own account.
- G5. **The register is the supervisor's:** no web3 vocabulary in the page's own words; the systems are described by
  attributes that bear on this work; the highly public special cases are marked as such.
- G6. **The assessment outlives the drafting unit:** the checks are scripts, tests and recorded tables that a later
  reviewer re-runs.

## Non-goals

- No change to the paper or the documentation; no new section, figure or page beyond `site/history.html`; no change to
  `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, the interface contract or the theme.
- No internal or private material of BlockScience or Dynamical Systems Group, inferred, reconstructed or implied;
  where the public record is thin the page says less.
- No web3, cryptocurrency or tokenomics vocabulary in the page's own words; a linked source's title may carry it.
  No implication that cryptocurrency is the firm's focus.
- No people added to or removed from the named list by an agent: the list is the supervisor's; proposed additions go to
  him (the open items).
- No role, background or relation attributed to a person that a public source or the marked team's account does not
  state; no client named; no project detail for the undisclosed client work.
- No argument for the page's purpose: it may say it in one plain sentence.
- No citation counts without source and date read.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `site/history.html`: the page, to the structure below | G1 to G5 |
| D-2 | A single link to it on `site/index.html` (a footer link, exactly one occurrence) | G2 |
| D-3 | `scripts/assemble_site.py` copying `site/history.html` into the assembled site | G2 |
| D-4 | `work-packages/WP37-rounds/` research tables W1 to W4, `open-items.md` and `draft-shots/`: the sources, dates read and what each shows | G4 |
| D-5 | `scripts/check_history_links.py`: the repeatable network check (status and match per external link), with a test of its parsing and classification in `tests/` | G4, G6 |
| D-6 | The tests in `tests/test_site.py`: one screen and register, one root link, links resolve, vocabulary, word ceiling | G3, G5, G6 |
| D-7 | `work-packages/WP37-rounds/trace.md`: the sentence classification table (sentence, kind, the link or account it rests on, what it lets a reader trace), re-run by the review | G4, G6 |
| D-8 | `WP37-review.md` with screenshots and a fresh reader's walk of the arc; `WP37-decisions.md` updated | G1 to G6 |

## Page structure

1. One opening sentence of purpose (people and the human lineage the paper's citations cannot carry), the firm as a
   contract research and engineering firm, and the activities sentence in the supervisor's wording.
2. The arc, in dated order: before the firm (2013 and 2014: convex optimization, the GGP work with Preciado),
   cadCAD, GDS and PSuU at the firm, then OpenMBEE, OpenSysML and this synthesis; each work one link and a clause.
3. The people: name, work, link; the undisclosed-projects sentence for Hackel and Riascos Álvarez, marked as the
   team's account; the contributors' backgrounds as one sentence, marked if it rests on no source.
4. The firm today: NumFOCUS, SciPy and PyData; OpenMBEE and OpenSysML.
5. The highly public special cases, each marked as such in the sentence that cites it.
6. The one closing phrase (open item).

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every external link resolves (2xx or 3xx), or is reported `blocked` (403 or 429, host refuses automated requests) and then confirmed by a person in a browser; none FAILs | `uv run python scripts/check_history_links.py`, output pasted in `WP37-review.md` |
| R-2 | Every link matches its claim: the target, fetched, says what the page says it does; a mismatch is fixed or the claim narrowed | the W3 table re-run on the final head (link, status, what the target says, claim, match); no `no` rows, each `partial` fixed or listed |
| R-3 | Every sentence is classified as sourced, shown by a link, or the team's own account; the team's account is marked in the sentence ("in our own account" or the like); each row says what the sentence lets a reader trace | `trace.md` complete for the final page; a reviewer re-derives the marks and finds no unmarked team's account |
| R-4 | Every work on the page carries a date; every person has at least one work, link or marked account | read against `trace.md`; a table of person, work, date in `WP37-review.md` |
| R-5 | Vocabulary: none of the banned web3 terms in the page's visible text; the glossary pass over the page is clean | `uv run pytest tests/test_site.py -k history`; `uv run python scripts/check_vocabulary.py` |
| R-6 | Word ceiling: visible words within the test's bounds (now 250 to 450; the aim is 350 or fewer, and the ceiling is lowered by the test as the page thins) | `uv run pytest tests/test_site.py -k one_screen`; the count in `WP37-review.md` |
| R-7 | Special-case rule: every sentence citing a work in a cryptocurrency setting says in that sentence that it is a special case where the work was highly public, and none implies a focus area | `trace.md` flag column; read of the rendered page |
| R-8 | Structure: the page has the six parts above in that order, the arc runs 2013 to now, and the purpose is one plain sentence | read of the rendered page against the structure; the fresh reader's walk (R-11) |
| R-9 | No private material: every linked repository and page returns 200 to an unauthenticated request | `check_history_links.py` run with no credentials; the GitHub links re-read by the W3 method without a token |
| R-10 | The paper and the docs are untouched; nothing under `src/`, `derivation/`, `pyproject.toml`, `uv.lock` | `git diff origin/dev --stat` for the package's commits names only the blast-radius files |
| R-11 | A fresh Sonnet reader, given only the rendered page, walks the arc in their own words (who, what, when, in what order) and says whether the work reads as the synthesis of a long-running endeavour or as appearing from nowhere, without being told the intent | `WP37-review.md`: the reader's words verbatim beside the intended reading |
| R-12 | Rendered check: the page is screenshotted at 1280 by 800 and 390 by 844, light and dark; it fits one 1280 by 800 screen with the footer link; no stderr line, no broken link | `WP37-rounds/draft-shots/` replaced by the final head's screenshots with a one-line reading each |
| R-13 | The root page links to it once; the assembler copies it; the assembled site serves it | `uv run pytest tests/test_site.py`; `uv run python scripts/assemble_site.py` output listed |
| R-14 | Whole-repo `uv run ruff check .` and `uv run ruff format --check .`; `uv lock --check`; `tests/test_text_encoding.py`; no AI attribution in commits or files | the commands; grep of `git log` |

## Assessment machinery (outlives the drafting unit)

| Piece | Where | Re-run by |
|---|---|---|
| Link statuses and parsing | `scripts/check_history_links.py` and its test | the review, and by hand whenever the page changes; Haiku may run it |
| Link-to-claim match | the W3 table form in `WP37-rounds/` | a Sonnet checker fetching each target |
| Sentence kind and trace column | `WP37-rounds/trace.md` | the review re-derives the classification from the page and compares |
| Vocabulary pass | `tests/test_site.py` (banned terms) and `scripts/check_vocabulary.py` | `uv run pytest` |
| Word ceiling and one-screen register | `tests/test_site.py` | `uv run pytest` |
| Fresh reader's walk of the arc | `WP37-review.md` | a Sonnet reader given the rendered page only |

## Definition of good

- A reader meets the page in one screen and can walk the line from the 2013 and 2014 optimization work to the
  present, each step a dated link, and sees a team of named people, not a method from nowhere; every person is credited
  without overstating a relation; nothing on it needs a caveat because the marks sit where they belong.
- The page is thinner than the draft at `b3919b1` where an item no longer earns its place, and the checks above are
  cheap enough to re-run whenever the page changes.

## Definition of good enough

- D-1 to D-8 delivered; R-1 to R-14 hold, each with its evidence in `WP37-review.md`.
- The fresh reader's walk (R-11) matches the intended reading, or the mismatch is fixed or listed for the supervisor.
- Every open decision below is answered by the supervisor or recorded as answered by a default he approves; each page
  claim that rests on an open item is narrowed or dropped until he answers.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent models by role

Sonnet for the research workers, the drafting unit, the checkers and the fresh reader; Haiku for mechanical units (link
statuses, counts, screenshot runs, verbatim copies); nothing larger than Sonnet. The fresh reader gets the rendered page
only. No sub-agent without the PM.

## Agent's defaults

- The research tables stay as `WP37-rounds/w1` to `w4` and `open-items.md`; `trace.md` and `WP37-review.md` sit beside them *(default)*.
- The link checker treats 2xx and 3xx as resolving and 403 or 429 as `blocked`; blocked links are confirmed in a browser *(default)*.
- Word bounds are the tests' current 250 to 450, lowered when the page thins *(default)*.
- Banned terms are those of `test_history_page_uses_no_cryptocurrency_or_web3_vocabulary` *(default)*.
- The trace table's kinds are `sourced`, `link`, `team` *(default)*; the person table follows the W2 form.
- The page's section order follows the structure above; the visual register is the root page's *(default)*.
- One unit per surface, all on `dev`; `main` gets a no-ff merge only at the accepted package *(default)*.

## Open decisions (for the supervisor)

Each is a problem-level question; the page says less on each until it is answered.

1. **Matthew Barlin's background.** The page may name only his role in cadCAD's design (AUTHORS.txt). Options: (a) name
   only that role; (b) add a background from a public source the workers find; (c) add it as the team's own account in
   the backgrounds sentence.
2. **Danilo Bernardineli's spelling.** Public sources read "Bernardineli"; the supervisor's list reads "Bernardinelli".
   Options: (a) "Bernardineli", as the sources; (b) "Bernardinelli", as the list; (c) the supervisor supplies his own
   form.
3. **Andrew Penland's surname and identity.** The firm's blog says "Octopus, a Research Engineer"; only a third-party team page
   gives "Andrew Penland, Ph.D. (a.k.a. Octopus)" and does not name the firm; the supervisor wrote "Pentland". Options:
   (a) "Penland", as the sources, the match confirmed by him; (b) "Pentland", as he wrote; (c) credit "Octopus" alone
   until he confirms.
4. **The unfetched posts.** Five firm posts (cadCAD origin, parameter selection, scientific-Python, the
   community-currency post, the 2021 GDS post) returned 403 or did not resolve. Options: (a) he supplies the links and
   dates to cite; (b) the page leaves them out; (c) the page links the known URLs with no claim resting on them.
5. **Carolina Riascos Álvarez's handle.** `CarolinaRiascos` is hers by her own site; no public repository of the firm ties
   it to the firm. Options: (a) credit the handle as given; (b) credit the name only; (c) he supplies a firm-linked
   handle or repository.
6. **The closing phrase** "With computers, fast but with confidence." Options: (a) keep; (b) cut; (c) he restates it.
7. **The Clark discrepancy.** His brief called the community-currency paper cryptocurrency-free; its abstract describes a blockchain
   form of local complementary currency. Options: (a) the page names the paper and the Red Cross and Grassroots
   Economics collaboration and describes no setting; (b) the page marks it a special case where the work was highly
   public; (c) the paper is dropped.
8. **The Edinburgh talk rests on the CV alone.** No page says the University of Edinburgh; the CV says ICMS, October 2024.
   Options: (a) keep it, linking the CV; (b) he supplies a conference page; (c) drop it.
9. **The later scope of the representation and presentation split.** The record `history.yaml` with the page as its view,
   a test tying every link, name and date to an entry, and a generated dated list, was ruled but this scope's deliverables
   are the page, the tables and the checks. Options: (a) a later package builds the record and the generated list;
   (b) it joins this package as D-9, with the tests; (c) the tables of D-4 stay the record and the split is dropped.

## Blast radius

- Owned: `site/history.html`, the one link in `site/index.html`, `scripts/assemble_site.py` (the copy line),
  `scripts/check_history_links.py`, the history tests in `tests/test_site.py` and the checker's test, and
  `work-packages/WP37-*`.
- Read, never written: the paper, the docs, `glossary.yaml` (the vocabulary pass reads it), the public sources.
- Never: `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, the interface contract, the theme, data, the model, the
  `verify` and `stage` worktrees, tab-23, and any file under another agent's worktree.

## Lifecycle stages

(1) Research spike: done, `WP37-rounds/` W1 to W4. (2) Decide: the supervisor's rulings in `WP37-decisions.md`, and the
open decisions above. (3) Build: the page, the root link, the assembler, the checker and the tests, as delivered at
`b3919b1` and revised to this scope. (4) Quality control: R-1 to R-9 and R-14 run on the head (links, trace,
vocabulary, ceiling). (5) Integrate: the root link, the assembler copy and the assembled site. (6) Review the cascade to
a clean merged state: the fresh reader (R-11), the screenshots (R-12), then `WP37-review.md` for the supervisor's
acceptance.
