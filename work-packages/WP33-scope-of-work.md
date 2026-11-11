# WP33 — Scope of work: journeys and signposting (one size fits none)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` when the driver judges it merits CI |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`, "The mandate"), quoted verbatim in `work-packages/WP33-decisions.md`, section "Scope gate" *(default heading)* |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP33-decisions.md`, after `work-packages/WP33-review.md`; the placements and cuts are listed for the supervisor's review with it |

**Header note.** Drafted 2026-11-11 from `origin/dev` at 45180fd for the ninth PM. It runs alongside WP32 (the
package-user tests, U1 to U4) and lands before the handover. It follows the lifecycle of `PM-BRIEF.md`, "Bigger
candidate edits run the full lifecycle", adapted: the content is placement and narrowing, not a new result, so stage (1)
is the journeys map and the wayfinding baseline, and stage (6) reviews the cascade of moved text (ledger, budgets, links,
the register).

## Purpose

The supervisor's standing order, verbatim (`PM-BRIEF.md`, "One size fits none: journeys and signposting", 2026-11-11,
10:35): "as we near the end, we need to be very clear about our wide range of users and their different user journeys
and make sure we're not doing the thing were what offer is "one size fits none" instead the top level index page, the
paper, the documentation, the api, the examples, the package itself, the repo organization all need to be fit for
purpose and aligned to a user need. the body of content needs to be signposted well enough that the user can quickly
find what they need, not get lost in content aimed at another user."

**Binding clause, the supervisor's, added the same hour, verbatim:** "do not bloat the repo to meet this requirement.
human (and machine) attention is scarce. more is not always better, and where does end up being a lot of content assume
the user drills down into it naturally don;t just hit them in the face with a ton of info. they will just bounce off".

The PM-BRIEF's reading of the clause, which this scope adopts as binding: signposting is done by subtraction and
layering, not by adding pages or banners; a first screen is a few lines that route, not a directory; whom-it-is-for is
one sentence, not a section; depth is reached by drilling down (a link, a fold, an appendix, the repository), never by
stacking it on the landing surface; every signposting unit is net neutral or net negative in words on the surface it
touches, with the ledger and the budgets showing it; the journeys map is a working note for the builders, not a page
for users.

The outcome: twelve kinds of arrival (P1 to P8, U1 to U4), seven surfaces, and for each pairing a short, measured path
to what the arriver needs, without walls of text aimed at someone else on the way.

## Goals

- G1. **The journeys are known.** One row per persona of `reader-grid.md` (P1 to P8, U1 to U4): arrival surface (the
  GitHub repository page, the root page, the docs Home, the paper, the API reference, the examples, the installed
  package), the first need, the path, and the content on that path aimed at another user.
- G2. **Every surface routes by need in the user's words.** Its first screen is a few lines that route (use the tool on
  your own table; read the paper; bring your own system model; check the mathematics; reproduce the results); its top
  says in one sentence whom it is for and where the others go.
- G3. **The repository's top level reads the same way.** The README's layout list says what each directory is for, and
  the list is true of the tree.
- G4. **Content on a path aimed at another user moves to that user's path or goes.** Placement is a negative-edit
  question: the marginal-value test asked of where content sits, not only of whether it exists.
- G5. **The paths are measured.** A fresh reader per persona, dropped at their arrival surface with their need, counts
  steps to what they need and reports where they got lost or skipped; the round repeats on the fixed surfaces.
- G6. **The whole is net neutral or net negative in words** on every surface touched, with the ledger and budgets
  showing it.

## Non-goals

- No new pages, banners, landing sections, navigation widgets, tables of contents or "who is this for" sections. A
  routing line, a link and a cut are the only instruments (the binding clause).
- No page of the journeys map in the site, the paper or `docs.pages`: it is a working note for the builders under
  `docs/superpowers/notes/`.
- No new content of substance: a unit may move or cut a claim; it adds none. A moved claim keeps its backing
  (claims register, lemma, test).
- No change under `src/` or `derivation/`; no change to the model, the data or any generated number.
- No redesign of the site's theme or of the paper's structure; the paper's section order and the appendices' letters
  stay (the paper's Organization paragraph is edited, the structure is not).
- WP32's tests (U1 to U4 task cells) are a separate package and are not re-run here; WP33's wayfinding readers measure
  steps and bounce points, not whether the fit worked. The two rounds share the personas and may share a staged head.
- Not a rewrite of the user guide's pages for style; a page is edited only to route, cut or place.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | **Journeys map** `docs/superpowers/notes/user-journeys.md`: twelve rows (P1 to P8, U1 to U4) with arrival surface, first need, path, and the content on the path aimed at another user, each cited to a file and heading; a closing list of the placements and cuts it implies | G1 |
| D-2 | **Signposting units, one per surface** (each a net-neutral-or-negative edit): the root page (`site/index.html`); the docs Home (`docs/index.md`); the paper's head and Organization paragraph (`paper/paper.ipynb` cells, routing by depth); the API reference (`docs/api.md`, `docs/api-reference.md`) top; the examples (`docs/examples.md`, `examples/adcs/` entry); the package (`src/` docstring top-lines are read-only here: see OD3); the repository (`README.md` layout list) | G2, G3, G6 |
| D-3 | **Placements and cuts**: the content D-1 finds on a path aimed at another user, moved to that user's path (a link, a fold, an appendix, the repository) or cut, each with a one-line reason in `work-packages/WP33-decisions.md` *(default)* and the ledger and budgets updated in the same push | G4, G6 |
| D-4 | **Wayfinding rounds** `work-packages/WP33-wayfinding.md` *(default path)* and `WP33-wayfinding/`: the baseline round at a named head and the repeat on the fixed surfaces; per reader: persona, arrival surface, need, steps counted, bounce points, what was skipped, the reader's words verbatim | G5 |
| D-5 | **Review** `work-packages/WP33-review.md` with screenshots of every first screen in `work-packages/WP33-review/`, light and dark where the site has both, and a one-line reading of each | G2, G5, G6 |
| D-6 | **Records**: `WP33-decisions.md` (scope gate, triage of the rounds, the driver's calls verbatim), the `length_ledger.toml` rows for the paper, the `tests/test_site.py` budget changes (down only unless OD2 says otherwise), a contract amendment only where a pinned surface changes (OD1) | G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The journeys map has one row per persona P1 to P8 and U1 to U4 with the four fields filled, each "aimed at another user" entry naming the file and heading and the user it is aimed at; no row says "none" without the path it walked | read `user-journeys.md`; a script `scripts/` need not exist: `grep -c '^| [PU][1-8] '` returns 12 (P1 to P8, U1 to U4) *(default check)* |
| R-2 | **Net neutral or negative in words, per surface.** Compared with the start head, the prose word count of each touched surface is not higher: the docs pages by the budgets' own counter (`tests/test_site.py::prose_words`, code blocks and tables excluded), the paper's sections by the ledger's counter (`tests/test_paper.py`), the root page and README by the same regex counting visible text *(default)*; the sum of changes across the package is negative | `uv run pytest tests/test_site.py::test_word_budgets_hold tests/test_paper.py`; before and after counts in `WP33-review.md`, one line per surface |
| R-3 | **Budgets only go down.** Each `BUDGETS` entry and `TOTAL_BUDGET` is at most its value at the start head; the paper's ceiling in `length_ledger.toml` is lowered by `[[cut]]` rows saying the section, `words_removed`, what the content no longer did and the authority | `git diff` of the two files; no `words_added` row in the package's commits unless OD2 admits one |
| R-4 | **A first screen is a few lines that route.** On each surface's first screen (the viewport at 1280 by 800 and at 390 by 844 phone width) the routing block is at most five lines of the user's-need phrases (the five above, or fewer) each a link; no directory listing, no section, no banner, no more than one sentence saying whom the surface is for | the screenshots of D-5 at both widths; a reader counts the lines; the wayfinding round |
| R-5 | **Whom-it-is-for is one sentence and where the others go is a link.** The top of each hand-written docs page, the paper, the root page and the README carries at most one such sentence (not a heading, not a box), and the sentence names a destination for the other users | grep of the first lines of each page; the review reads each |
| R-6 | **The README's layout list is true and says what each directory is for.** Every top-level directory (`src/`, `derivation/`, `examples/`, `docs/`, `paper/`, `work-packages/`, `scripts/`, `site/`, `tests/`) appears with a clause saying its job and for whom; no stale entry (the current list calls `docs/` "mathematics, preconditioning, API, literature; site in WP8"); the list is not longer than it needs to be (a directory no one arrives at may be one clause) | `ls` of the repository root against the list; read |
| R-7 | **The Organization paragraph routes by depth.** The paper's Organization paragraph says, by depth (abstract and figure, headers and results, the whole text, the appendices, the repository and container), where each reader stops or goes on, in no more words than now | the paper's rendered Organization paragraph, word count before and after; the L-A to L-F readers of the reader grid read it |
| R-8 | **Placement moves keep their backing.** Every moved claim still has its backing at its new place (claims register row, lemma, test or source); every link in or out of a moved or cut passage still resolves; the glossary and Appendix A stay consistent in the same push | `uv run pytest tests/test_claims_register.py tests/test_site.py tests/test_paper.py`; `uv run python scripts/check_vocabulary.py`; the docs build with no broken-link warning; the paper builds |
| R-9 | **Pinned surfaces are routed by amendment, not drift.** If a unit removes, adds or renames a page of `docs.pages`, the root page's pinned elements (`build.root_index_*`) or any other pinned name, the interface contract is amended in the same commit (manifest and document), with a change-log row; otherwise the contract is untouched | `uv run pytest tests/test_interface_contract.py`; `git diff work-packages/interface-contract.*` |
| R-10 | **The wayfinding round measures the right things.** Per persona one fresh Sonnet reader (no repository notes, no records), given only the arrival surface's rendered page on the staged site at a named head and the persona's need in the persona's words; each reports steps to the need (a step is one page opened or one link followed), where it got lost, what it skipped, and whether any surface made it skim past a wall of text; the baseline and the repeat use the same needs and a different reader each | `WP33-wayfinding.md`: twelve baseline rows, twelve repeat rows, the head named for each round, the readers' words verbatim |
| R-11 | **A skim-past is a defect to fix by cutting.** Each report of a surface that made a reader skim past a wall of text is triaged into a cut or a placement (D-3), not into an added explanation; a triage line that adds words is refused unless OD2 admits it | `WP33-decisions.md` triage table; R-2 and R-3 |
| R-12 | **Steps to the need do not rise and the bounce points fall.** At the repeat round no persona's step count is higher than at the baseline, the total steps are lower, and every bounce point of the baseline is either closed or listed with its disposition for the driver | the two tables of `WP33-wayfinding.md` compared row by row |
| R-13 | **No SysML v2 or satellite gate on the routes** (shared with WP32's standing question): a U1 or U3 arrival reaches the tool-on-your-own-table path without a page that presumes SysML v2 or satellites | the U1 and U3 wayfinding rows; the reader's statement |
| R-14 | **The reviewer ran the thing.** Every first screen (repository page rendering of the README, root page, docs Home, paper first screen, API reference, examples page, and the package's installed-view entry per OD3) was looked at as rendered on the staged site (not read as source), at both widths, with the screenshot and a one-line reading in D-5; a stderr line or broken link on a rendered page is a finding | the screenshots; the site staged at a named head with `scripts/stage_site.py` *(as the staging notes name it)* |
| R-15 | **Repository gates.** `uv run pytest -q -m "not slow"` on touched tests (full suite at the gate), `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; no AI attribution on any commit or file | the commands; `git log <start>..HEAD --format=%B` grepped for the CI's whole-word pattern: nothing |

## Definition of good

- A reader of any of the twelve kinds lands, sees in a few lines which door is theirs, and is through it in a click or
  two; nothing on the way is addressed to someone else; the whole repository is smaller than before the package.
- The surfaces read as parts of one design: the same five phrases of need, in the user's words, on every landing
  surface, and each page one sentence about whom it is for.
- The journeys map is short enough that a builder reads it in one sitting and uses it to decide where a new sentence
  belongs.

## Definition of good enough

- D-1 holds twelve rows; D-2's units are in on every surface; D-3's placements and cuts are recorded with reasons.
- R-2 and R-3 hold: the net word change is negative on every touched surface or neutral with a stated reason, budgets
  and ledger only lowered.
- The baseline and the repeat wayfinding rounds are recorded (R-10); R-12 holds: no persona's steps rose, the total
  fell, and every baseline bounce point is closed or listed.
- Every first screen has a rendered screenshot with a reading (R-14); R-4 and R-5 hold on each.
- The repository gates (R-15) pass; the contract is amended only if R-9 triggered it.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- Paths and names: `docs/superpowers/notes/user-journeys.md` (named by the supervisor's order); `WP33-decisions.md`,
  `WP33-wayfinding.md` with `WP33-wayfinding/`, `WP33-review.md` with `WP33-review/` *(default)*.
- The "step" unit in the wayfinding round: one page opened or one link followed *(default, R-10)*.
- The five need phrases are the order's own; the exact wording on each surface may differ by a word where the surface's
  voice needs it, the five destinations stay the same *(default, G2)*.
- Word counting on the root page and the README by visible text, markup excluded *(default, R-2)*.
- The first-screen test viewports: 1280 by 800 and 390 by 844 *(default, R-4)*.
- Readers: Sonnet; Haiku for counts, greps and screenshot runs; no Opus; no sub-agent without the PM (the standing
  rule). Readers get the rendered pages only, never the notes, records or tests; the persona's need is stated in the
  reader grid's words.
- Order of work: D-1 first; the baseline round on the start head in parallel with the first units; one unit per surface,
  one push each; the repeat round at the head after the last unit; at most two rounds unless OD4 says otherwise.
- Checks that name a script (`scripts/stage_site.py`) follow whatever the staging notes name at execution.
- A surface's one-sentence "for whom" uses the glossary's terms; the claims register and the vocabulary check follow.

## Blast radius

Owned files, per stream; anything else is a stop and a question to the PM.

- **Records and notes:** `docs/superpowers/notes/user-journeys.md`; `work-packages/WP33-*` (decisions, wayfinding,
  review and their folders); `work-packages/parallel-board.md` rows for this package.
- **Root page and README:** `site/index.html` (first screen and top sentence only), `README.md`.
- **Docs pages (routing, placement and cuts only):** `docs/index.md`, `docs/getting-started.md`, `docs/api.md`,
  `docs/api-reference.md`, `docs/examples.md`, `docs/theory.md`, `docs/further-reading.md`, and `docs/user-guide/*.md`
  where the journeys map names an aimed-at-another-user passage; `mkdocs.yml` only if OD1 routes a page.
- **Examples entry:** `examples/adcs/` README or case-model entry text (top lines and placement only; no code, no data).
- **Paper:** the cells carrying the title block and the Organization paragraph in `paper/paper.ipynb` and its
  generators where the text is generated; `paper/length_ledger.toml`; a moved passage's source cell and its new
  home. The paper's generated numbers are untouched.
- **Budgets and records the paper or docs read:** `tests/test_site.py` (the `BUDGETS` and `TOTAL_BUDGET` values, down
  only), `claims_register.toml` and `glossary.yaml` where a moved claim or term needs it (an entry regenerates
  Appendix A in the same push).
- **Contract, only on R-9:** `work-packages/interface-contract.{md,toml}`, `tests/test_interface_contract.py`.
- **Never:** `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, any data file, the model, any generated paper
  output while a container regression runs, the answer key, the staged-site worktrees `verify` and `stage`
  (the driver's), the browser pane's tab-23 (a reader opens its own tab and closes it).

## Lifecycle stages (adapted from the full lifecycle)

| Stage | What | Owner | State |
|---|---|---|---|
| (1) Research | The journeys map (D-1) from the repository and the reader grid; the baseline wayfinding round at a named head; the readout lists the aimed-at-another-user passages with word counts and plain options | Sonnet research agents | starts on approval |
| (2) Decide | The driver decides which placements and cuts go ahead (the supervisor where it is his); open decisions below | driver | after (1) |
| (3) Build | One signposting unit per surface (D-2), the placements and cuts (D-3), each net neutral or negative | Sonnet implementers, one worktree and file set each | after (2) |
| (4) Quality control | Tests, vocabulary, claims register, link check, the budgets; the repeat wayfinding round on the staged site at a named head | fresh readers; the PM | after (3) |
| (5) Integrate | Contract amendment if R-9 triggered, ledger and budgets, glossary and Appendix A, the register | PM streams | after (4) |
| (6) Review the cascade | Every moved sentence, link and count found and resolved; the reviewer runs the thing and screenshots every first screen (D-5); the driver accepts | a reviewer that runs the checks | after (5) |

## Open decisions (for the driver; the supervisor where it is his)

- **OD1. Does a surface's routing ever change a pinned name?** The docs pages (`docs.pages`) and the root page are
  pinned. Options: (a) none: routing is by lines and links inside existing pages and the contract is untouched; (b)
  amendment allowed where the journeys map shows a page serves no path and is removed or merged (a negative edit
  routed by an amendment, as WP31's contract version 17 did for an addition); (c) amendment allowed for removal and
  for a rename.
- **OD2. May a signposting unit add net words on a surface if the package as a whole is net negative?** Options: (a) no:
  every surface net neutral or negative on its own (the clause as written); (b) yes, up to a stated small number of
  words on a surface that has no first-screen routing today, paid for by a larger cut on the same journey (the
  trade named in the decision record and the ledger row); (c) no added words anywhere; a surface without routing gets
  it by replacing existing lines.
- **OD3. What is the "package itself" as a surface?** The installed package's first contact is `help(hts)`, the class
  docstrings and the README on the package index. Options: (a) out of scope: nothing under `src/` is edited, the
  wayfinding reader for U3 and U4 is given the installed package's docstrings and the findings go to a package change
  request for a later package; (b) docstring top-lines only (one sentence saying what the module or class is for and
  where the docs go), delivered as a separate unit with the interface contract's docstring pins checked; (c) as (b)
  plus the package metadata description and project URLs in `pyproject.toml`.
- **OD4. Rounds of wayfinding.** Options: (a) baseline plus one repeat, a second repeat only for a persona whose
  steps rose; (b) baseline plus up to three repeats until a fresh reader per persona completes without a bounce
  the surface owes (the WP32 stop rule); (c) baseline and one repeat only, remaining bounce points listed for the
  driver.
- **OD5. Whether WP32's U1 to U4 cells double as the wayfinding readers for those four personas.** Options: (a) yes,
  the WP32 protocol carries the wayfinding question and WP33 reads its returns for steps and bounce points; the other
  eight personas get WP33 readers; (b) no: twelve WP33 wayfinding readers, kept apart from WP32's cells so each
  measure stays clean.
