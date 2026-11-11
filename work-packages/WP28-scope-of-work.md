# WP28 — Scope of work: improvement by subtraction (step 5a of the path)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` when the driver judges it merits CI |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`, "The mandate"), quoted verbatim in `work-packages/WP28-decisions.md`, section "Scope gate" *(default heading)* |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP28-decisions.md`, after `work-packages/WP28-review.md`; listed for the supervisor's review at the PR with every cut |

**Header note.** Step 5a of `release-candidate.md` ("Improvement by subtraction ... once the content is complete, one
disciplined pass over the whole paper and the docs"), which depends on steps 3f, 3g, 4 (all accepted) and 5 (WP11,
whose round 3 and maths-check unit are pending: OD1). Drafted 2026-11-10 from `origin/dev` at 195bd81. Sources: the
supervisor's words of 2026-11-09, 23:05 and 23:10 (`PM-BRIEF.md`, "Negative edits are welcome, even preferred" and
"Stuck means assess removal"; `driver-log.md`, the clarification of 23:10), the length-ledger rule in
`paper/length_ledger.toml`'s header, the figure review (`docs/superpowers/notes/figure-review.md`), the claims
review (`docs/superpowers/notes/claims-review.md`), the vocabulary review's dead-entry rule
(`docs/superpowers/notes/vocabulary-review.md`), and the reader grid (`docs/superpowers/notes/reader-grid.md`).

**Sizing at 195bd81 (what the inventory covers).** The paper (`paper/paper.ipynb`): 14 sections (12 of prose,
Acknowledgments, Works cited), 9,805 rendered words against the ledger's ceiling of 10,107; 10 floats (9 figures:
`fig-nlemma`, `fig-assembly-view`, `fig-behavioural-view`, `fig-tau-sweep`, `fig-planes-k1`, `fig-planes-k3`,
`fig-chart-level`, `fig-tensions-k3`, `fig-regimes`; 1 table, `tab-families`); 27 boxed statements (9 definitions,
12 theorems, 3 propositions, 2 lemmas, 1 corollary, each result with its sketch and script box). The supporting
material (`paper/supporting_material.ipynb`): 7 appendices (A to G) with 40 generated tables (A 1, B 5, C 9, D 19,
E 1, F 3, G 2). The docs: 14 hand-written pages (6,792 prose words against the budget of 7,600; `fitting.md` at its
budget, four pages within 5 words of theirs) with 8 figures (each in a light and a dark render), the root page
`site/index.html` with 2 images, and `README.md`. Per the records: 413 register rows (`claims_register.toml`), 55
glossary entries, 104 ledger raise rows and no cut row yet. Orphans seen while sizing, for the streams' cruft
lists: `paper/figures/fig-chart-k3.png` and `fig-predict-check.png` (figures that left the body; files still
tracked); `docs/generated/figures/ternary-cubesat-*.png` and `three-facets-*.png` (generated, not tracked, read by
no page). In all: 14 sections, 27 statements, 10 floats, 7 appendices with 40 tables, 14 pages, 8 docs figures, the
root page, the README: 122 units (corrected by WP25-4; the scope's terms sum to 122, `WP28-inventory.md`) with a verdict each.

## Purpose

The supervisor, 2026-11-09, 23:10, verbatim (`driver-log.md`): "i will eventually have to rewrite the abstract by
hand so don't stress about that specifically. i mean more like making sure we're not jamming in plots or arguments
for their ownsake that don't advance the narrative of the paper. we got a bit bloated early n and i want a
disciplined improvement by subtraction pass once we have have complete content. or if something is stuck in a loop
or cannot be made clear rather than agonize assess removal". And at 23:05: "negative edits are welcome even
preferred. the marginal value of content covers prose and figures and really any content. it is not just for
whether something should be added that still leads to unbounde growth but should also be applied regarding whether
to delete something".

The disposition recorded with them (`PM-BRIEF.md`): one pass over the whole paper and the docs, run once the
content is complete, judging every figure, argument and section by whether it advances the paper's narrative; what
does not, goes; what is stuck in a review loop or cannot be made clear is assessed for removal, not reworked again;
the length ledger records removals; each deletion names what the content no longer did.

The content is complete in the sense the path meant: the data of record (step 4), the eight-metric model (3f), the
rename (3g) and WP11's two rounds have landed. What this package does is subtract from it. Nothing here adds.

## Goals

- G1. **An inventory with a verdict for every unit.** For every section, boxed statement, float, appendix and its
  tables, docs page, docs figure, the root page and the README: the one sentence of the story it serves (the story as
  the paper states it, cited by cell or heading) and a verdict, advances / repeats / does not advance / stuck, with
  the reason, from fresh readers who do not know the records (the supervisor: "whether it advances the narrative").
- G2. **A cut list from the verdicts.** Each cut (goes, merged, shortened to a pointer) names what the content no
  longer did and what the narrative loses, and is checked against the claims register, the interface contract and its
  test, the figure review's principle, the word ceilings, the glossary and the tests that pin sentences (the
  standing order: "each deletion names in its commit what the content no longer did").
- G3. **The cuts executed as net-negative units** by the paper stream and the docs stream, the notebooks re-executed
  on the host, the appendices regenerated where a cut touches a registered or generated cell, the ledger recording
  every removal.
- G4. **Nothing the narrative needs is lost**: a cold read of the cut paper at depths B and C by fresh readers, by the
  reader grid's protocol (recall and friction, no ratings), marked against the answer key, shows no wrong belief and
  no main result lost (the supervisor: "if you present the information badly i wont be able to sign off on it").
- G5. **An acceptance review that runs the thing**: the staged site built and looked at in the browser at every
  changed page, the checks run, each requirement with its evidence (the standing order "Reviews run the thing").

## Non-goals

- New content, new prose that replaces what was cut (a pointer sentence is the one exception, G2), new figures, new
  mathematics, new lemmas, new register rows for new claims.
- Rework of a stuck passage, figure or argument: the pass assesses its removal; a passage that is kept is kept as it
  is (the supervisor: "rather than agonize assess removal").
- The abstract: the notebook's front matter is byte-identical at the end (his: "i will eventually have to rewrite
  the abstract by hand").
- The two Discussion candidates C406 and C407 and the proposals' future-work sentence (`WP23-review.md`, "Pending
  with the supervisor"): unchanged, waiting for him; the inventory records their verdicts and stops.
- "Energy differential" (CR-5, his decision: keep it, gloss it) and anything else recorded as his decision in a
  `WPn-decisions.md`: inventoried, never cut by this package; a verdict against one is a candidate for him in the
  cut list's "for the supervisor" section (OD4 for the figures he fixed).
- The docsite's structure (WP8a's; the pinned pages of `interface-contract.toml` `docs.pages` stay as they are): a
  page may lose content, no page leaves, none is merged into another, the navigation is unchanged.
- The code: `src/`, `derivation/`, `examples/adcs/` (the case module's figure functions stay even when the cell that
  called one goes), `pyproject.toml`, `uv.lock`, the data of record, the container of record.
- WP11's open items (the maths-check questions (a) to (g), the P6-B confirmation read) and WP8b's release items.
- The appendices' own prose is cut only where its table or its section goes; the reproduction's cold read (L-E) is
  not repeated here.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | **The inventory**, `work-packages/WP28-inventory.md` *(default)*: one row per unit of the sizing above (cell id or heading for the paper and the appendices; page path and figure file for the docs; the root page; the README) with the reader's sentence, the story sentence it serves with its citation, the verdict and the reason; the readers' returns verbatim in `work-packages/WP28-inventory/` *(default)*, one file per reader, committed before the triage | G1 |
| D-2 | **The cut list**, `work-packages/WP28-cut-list.md` *(default)*, by the PM's triager: one row per cut with its form (goes / merged into a named unit / shortened to a pointer to a named appendix section or docs page), what the content no longer did, what the narrative loses, and the six checks with their outcome (the register rows that go with it or are re-pointed; the contract pin, if any; the figure review's sentence test; the ceiling and the ledger row; the glossary entries made dead; the pinned tests and the recorded decision each one cites); a "kept, with reason" section for every unit whose verdict was not "advances"; a "for the supervisor" section for cuts this package may not make | G2 |
| D-3 | **The paper units**: the cuts of D-2 in `paper/paper.ipynb` and `paper/supporting_material.ipynb`, each a net-negative commit; the notebooks re-executed on the host with outputs committed; Appendix F.4's reproduction table regenerated when a `fig-` or `tab-` cell goes, Appendix A when a glossary entry goes; the ledger's cut rows; the register rows; orphan figure files deleted | G3 |
| D-4 | **The docs units**: the cuts of D-2 in the docs pages, the root page and the README, each a net-negative commit; `scripts/build_site_figures.py` loses a figure that goes; the register rows; the vocabulary tool green | G3 |
| D-5 | **The re-test**, `work-packages/WP28-retest.md` *(default)*: fresh readers at depth B (six personas) and depth C (five, P4-C held out as in round 2) on the staged paper at a named commit after D-3 and D-4, their reports verbatim in `work-packages/WP28-retest/` *(default)*, marked against the answer key by the triager, with the round 2 outcome beside each cell (`WP11-round-1/triage.md`, "Round 2") | G4 |
| D-6 | **The acceptance review**, `work-packages/WP28-review.md` and `work-packages/WP28-review/` (screenshots) *(default)*: R-1 to R-16 with evidence, the staged site looked at in the browser at every changed page | G5 |
| D-7 | **The decision records**, `work-packages/WP28-decisions.md` (the driver writes it): the scope gate, the cut list's gate if OD6 makes one, the acceptance, verbatim | all |

## Requirements

`<start>` is the `dev` head at approval; it is named in the scope gate's record.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The inventory is complete: every unit of the sizing has exactly one row with a sentence, a story citation, a verdict from the four and a reason | a script in the review (D-6) lists the paper's section cells, `prf:` blocks and `fig-`/`tab-` cells, the appendices' headings and `tab-` cells, `mkdocs.yml`'s hand-written pages, the docs' `![` figures, the root page and the README, and diffs that list against the inventory's first column: no difference |
| R-2 | The inventory's readers are fresh and know no record: each reader's brief contains the unit, the story as rendered (Section 1 and the abstract) and the questions, and no path under `work-packages/`, no review, no triage, no change request | the PM reads every brief's text before it is sent and says so in D-1; the briefs are committed with the returns |
| R-3 | A figure is read image first: the reader states what it shows before seeing its caption or page, then with the caption, then answers the sentence test (`figure-review.md`, tests 1 and 2) | the return's order, read by the PM; the brief's text |
| R-4 | Every cut row names what the content no longer did and what the narrative loses, and carries the six checks with an outcome each; a cut with a failing check is not executed until the check is resolved (a row re-pointed, an amendment recorded, a decision cited) | D-2 read by the reviewer against the executed commits' messages, which carry the same "no longer did" line |
| R-5 | Every executed unit is net negative in the prose a reader sees: the paper by `words_by_section()` (`tests/test_paper.py`), the docs by `prose_words()` (`tests/test_site.py`); no section, page or appendix grows; a pointer sentence counts against its cut | the review's table: per unit, the words before and after; `git diff --stat <start>..HEAD` |
| R-6 | The claims register holds: no row names cut prose; a row of a cut sentence is removed in the same commit or re-pointed at the sentence that carries the claim; no new row | `uv run pytest tests/test_claims_register.py`; `git diff <start>..HEAD -- claims_register.toml` shows removals and re-pointings only |
| R-7 | The interface contract holds: nothing pinned leaves without an amendment; the docs' pinned pages are all present; the case's figure directory holds exactly its pinned files (none) | `uv run pytest tests/test_interface_contract.py tests/test_site.py`; the contract's version unchanged unless an amendment is recorded in D-7 |
| R-8 | The ledger records every removal: one `[[cut]]` row per executed cut with its section, the words removed and what the content no longer did; the ceilings follow OD5 | `uv run pytest tests/test_paper.py -k ledger`; the review sums the cut rows against R-5's table |
| R-9 | No dead glossary entry: an entry whose last use leaves goes with it (or is marked `reserved` with its reason in the cut row), and Appendix A is regenerated in the same push | `uv run python scripts/check_vocabulary.py` exits 0; `uv run pytest tests/test_paper.py -k register` |
| R-10 | A test that pins a cut sentence, figure or appendix row changes only when the cut row cites the recorded decision (the cut list's approval under OD6, or the driver's call in D-7) and never weakens a requirement the cut did not change | `git diff <start>..HEAD -- tests/` read against the cut list; every changed test names its cut row in the commit message |
| R-11 | The notebooks are re-executed on the host after the last paper unit, with no error, no stderr and no warning in the committed outputs; Appendix F.4 has a row for every remaining `fig-`/`tab-` cell and none for a cut one; every appendix is still cited from the body | `uv run python paper/execute_notebooks.py`; `uv run pytest tests/test_paper.py tests/test_paper_static_figures.py` |
| R-12 | The non-goals hold: the abstract (front matter), C406, C407, the proposals' future-work sentence and every decision-recorded passage are unchanged; the navigation and the pinned pages are unchanged; nothing under `src/`, `derivation/`, `examples/adcs/` changed | `git diff <start>..HEAD` on the front-matter cell, the three fragments (by their register rows) and the named paths: empty; `mkdocs.yml` unchanged |
| R-13 | The re-test shows nothing lost: no wrong belief from the key's list in any cell; every main result of the key stated at depth B in every cell; at depth C no "why" that round 2 did not already carry; no replicated friction that names a cut or a pointer | D-5's per-cell table against round 2's; the triager's marks |
| R-14 | The whole suite is green on the head of each stream's last push and on the package's head on this Mac; Linux per batch by the driver; the fast suite before each push | `uv run pytest -q` on the head; the watcher's row in `driver-log.md`; the CI run id |
| R-15 | The staged site builds and every changed page was looked at in the browser, light and dark, at desktop width, with screenshots in `WP28-review/` and the reviewer's one-line reading of each | `uv run python scripts/stage_site.py` in a clean worktree at the head; the screenshots and lines in D-6 |
| R-16 | No AI attribution on any commit or file; one object, one name in every record a test or the paper reads | `git log <start>..HEAD --format=%B` grepped for the CI's whole-word pattern: nothing; `scripts/check_vocabulary.py` |

## Blast radius

By stream; anything else is a stop and a question to the PM. Two streams never write the same file; register rows
follow the file of the sentence they pin (the stream that cuts the sentence owns its rows); glossary entries go
through the PM, who regenerates Appendix A in the same push (`pm5-rules.md`).

- **The inventory readers**: nothing (read only). The PM writes `work-packages/WP28-inventory.md` and
  `work-packages/WP28-inventory/`.
- **The triager**: `work-packages/WP28-cut-list.md`.
- **The paper stream**: `paper/paper.ipynb` and `paper/supporting_material.ipynb` (Markdown cells; a code cell
  only as a whole `fig-`/`tab-` cell that goes, with its `remove-input` sentence cell when the sentence goes);
  `paper/length_ledger.toml`; `paper/figures/` (a figure's file and its generator when its cell goes; the two
  orphan files); `scripts/build_figures.py` (the entry of a figure that goes); `paper/generate_*.py` only to remove
  a generator whose table goes; `claims_register.toml` rows of the paper's files; `tests/test_paper.py` (the ledger
  reader for the cut rows under R-8; a pinned sentence only under R-10), `tests/test_paper_static_figures.py` (under
  R-10); `docs/superpowers/notes/paper-sources/` only where a pinned test of a cut sentence reads it.
- **The docs stream**: `docs/*.md`, `docs/user-guide/*.md`, `site/index.html`, `README.md`,
  `scripts/build_site_figures.py` (a figure that goes); `claims_register.toml` rows of those files;
  `tests/test_site.py` (`BUDGETS` under OD5; a pinned sentence under R-10), `tests/test_docs.py` (under R-10).
- **The PM**: `glossary.yaml` (dead entries) and `tab-A-register`'s regeneration in the same push; the `stage`
  worktree for D-5's build.
- **The re-test readers**: nothing. The triager writes `work-packages/WP28-retest.md` and `work-packages/WP28-retest/`.
- **The reviewer**: `work-packages/WP28-review.md`, `work-packages/WP28-review/`.
- **The driver**: `work-packages/WP28-decisions.md`, this file (amendments only).
- **Never**: the abstract; `src/`, `derivation/`, `examples/adcs/`, the data, `paper/container/`,
  `paper/environment_values.toml`, `pyproject.toml`, `uv.lock`, `mkdocs.yml`, `work-packages/interface-contract.*`
  (an amendment, if a check needs one, is a unit on the driver's go).

## Definition of good

The supervisor's: a paper in which nothing is there for its own sake ("making sure we're not jamming in plots or
arguments for their ownsake that don't advance the narrative of the paper"); "each word earns his place, and more
text has a higher burden" (the ledger's rule); a presentation he can sign off on ("i am a human not a computer ...
if you present the information badly i wont be able to sign off on it"). Every figure that remains earns its place
as rendered (`figure-review.md`: "A figure whose intent a sentence carries as well does not earn its place and
goes"). Every claim that remains has its backing beside it and no caveat added to keep it. What is stuck is gone,
not polished. The reader at depth B still states the main results and what is not claimed; the reader at depth C is
owed no new "why". The ledger shows the paper shorter than it started, section by section, with a reason per cut.

## Definition of good enough

- D-1: every unit of the sizing has its row (R-1, the script's diff empty); every reader's return is verbatim and
  committed before the triage; every brief is free of records (R-2); every figure was read image first (R-3).
- D-2: every unit with a verdict other than "advances" is either a cut row or a "kept, with reason" row; every cut
  row has its six checks with outcomes (R-4); the "for the supervisor" section lists what this package may not cut.
- D-3 and D-4: every cut row of D-2 that is not "for the supervisor" is executed, or is listed as not executed with
  the failing check that stopped it; every unit is net negative (R-5); the notebooks re-executed, the appendices
  regenerated, the outputs committed (R-11); the register, the contract, the ledger, the glossary and the pinned
  tests as R-6 to R-10; the suite green (R-14).
- D-5: the re-test ran on the staged paper at a named commit after the last unit; no wrong belief; every main result
  stated at depth B; no new "why" at depth C; no replicated friction naming a cut (R-13).
- D-6: every changed page looked at in the browser with its screenshot (R-15); R-12 and R-16 hold; every requirement
  has its evidence.
- The counts in the review: units inventoried; verdicts by kind; cuts by form; words removed per section and per
  page; register rows removed and re-pointed; glossary entries removed; tests changed under R-10, each with its
  decision.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

The supervisor approves or changes this list as one item.

- **Files and names**: `WP28-inventory.md` with `WP28-inventory/`, `WP28-cut-list.md`, `WP28-retest.md` with
  `WP28-retest/`, `WP28-review.md` with `WP28-review/`, `WP28-decisions.md`; the ledger's removal rows as `[[cut]]`
  tables with `date`, `section`, `words_removed`, `no_longer_did` (and `[[abstract.cut]]` unused, the abstract being
  a non-goal); the decision-record headings "Scope gate", "Cut list" (if OD6 (a) or (c)), "Acceptance".
- **The story the readers are given**: the rendered Section 1 (`sec-decision` to `sec-decision-3`, the main-results
  list and "Organization") and the rendered abstract, as the paper states its narrative; a reader cites the item or
  sentence a unit serves by that list's number or the abstract's sentence. The docs' story is the Home page
  (`docs/index.md`) and the root page; a docs unit is judged against those and the page's own opening sentence.
- **The verdicts, defined for the readers**: *advances*: a sentence of the story needs this unit and no other unit
  carries it; *repeats*: another unit (named) already carries what this one carries; *does not advance*: no sentence
  of the story needs it; *stuck*: the reader cannot say what the unit is for or what it conveys after reading it
  twice. The triager adds the record's meaning of stuck (named in two or more review rounds with change requests and
  still drawing friction in the last: `WP11-round-1/triage.md`, "Round 2"; `WP19-figure-review.md`, "Round 2") to
  the verdicts, and says which source each "stuck" comes from.
- **Fan-out**: one fresh reader per paper section (14), per appendix (7, its tables inside), per docs page (14), the
  root page with the README (1), and per figure (9 paper, 8 docs, 2 root page), each figure image first; the readers
  spread over two models as the grid asks; a boxed statement is read by its section's reader. About 55 reads.
- **The triager** is one agent that is neither a reader nor an author of the cut passages, with the records
  (round 2's friction counts and its "The worst cells"; WP19's round 2) as input beside the inventory.
- **The forms of a cut**: goes; merged into a named unit (the surviving unit does not grow beyond the merged
  sentence); shortened to a pointer (one sentence naming the appendix section or docs page that holds the full
  version). A paragraph is the smallest unit cut in the paper; a sentence inside a paragraph goes only when a
  register row or a reader names it.
- **Execution order**: the inventory, then the triage, then (the gate of OD6, if any) the paper stream and the docs
  stream in parallel in their own worktrees, each unit pushed to `dev` after the stream's tier-0 and tier-1 checks;
  no push that regenerates paper outputs while a gate's container regression runs (`pm5-rules.md`); then the stage
  at a named commit (the `stage` worktree, with the theme-template note of `parallel-board.md`), the re-test, the
  review.
- **The re-test's size and marking**: as round 2 (six at B, five at C, P4-C held out; two models; the brief wordings
  of round 2 not reused for a persona that read them), marked against answer key version 2 with its "key stale"
  lines as the driver recorded them, so that the comparison with round 2 is cell for cell. The docs are re-tested by
  the three task reads of the docs loop (R1 to R3) only on pages the cut list changed; a page not changed is not
  re-read.
- **The reviewer** is one agent that was neither a reader, the triager nor a stream author; the driver's browser
  pass at the gate stays the driver's.
- **Cruft met on the way** (the two orphan figure files; a generator that nothing calls after a cut) is deleted by
  the stream that owns the path, with the "no longer did" line, as WP25's rule says (git keeps history).

## Open decisions (for the supervisor; the driver under the mandate)

- **OD1. When the pass runs, against WP11's open round.** Step 5a depends on step 5, and WP11's round 3 (the re-test
  of the cells that found something) and its maths-check unit have not run. Options: (a) WP28 starts after WP11's
  round 3 and the maths unit have landed, on that head / (b) WP28 starts now and its re-test (D-5) is WP11's round 3,
  one read serving both, the maths unit landing before the stage / (c) the inventory and the triage start now, the
  execution waits for WP11's round 3.
- **OD2. Which appendices are in the pass.** The supporting material's readers are depth D (the full version of
  what the main text points to) and depth E (the reproduction, Appendix F). Options: (a) every appendix and table
  is in the pass, judged by the narrative like the body / (b) an appendix is judged by its depth's job: a table goes
  only when nothing in the main text points to it and no reader at depth D would look for it; Appendix F is out /
  (c) Appendices A to E and G are in, F is out.
- **OD3. A figure that passed its cold read but serves no sentence of the main text.** The figure review keeps a
  figure that conveys its intent; the narrative test asks whether a sentence of the story needs it. Options: (a) it
  goes: the sentence test is the rule, and a "good for" line is not a sentence of the story / (b) it stays when its
  "shows, does not show, good for" line names a use a reader has / (c) it moves to the supporting material with its
  caption, as the full version a depth-D reader is pointed to.
- **OD4. The figures the supervisor fixed in WP19** (`WP19-slots.md`, "Fixed by the supervisor": the tension heatmap
  "don't rework it", docs Figure 8 as drawn, the three-pane figure out of the body) and the two model views he
  directed. Options: (a) in the pass like every other figure / (b) inventoried with a verdict; a cut of one is a
  row in "for the supervisor", not executed / (c) out of the pass, no verdict.
- **OD5. The ceilings after the pass.** Options: (a) the paper's ledger ceilings drop by the cut rows and the docs'
  budgets are lowered to the counts after the pass, so that nothing cut can grow back without a row or a decision /
  (b) the ceilings stay where they are; the cut rows are recorded and not subtracted / (c) the paper's ceilings drop
  by the cut rows; the docs' budgets stay.
- **OD6. The cut list's gate.** The cuts remove content the supervisor calls his core intellectual contribution;
  the mandate lets the driver define and accept scopes. Options: (a) the driver approves the cut list before any cut
  is executed, recorded in D-7 / (b) the cuts execute on the triager's list and the driver judges them at
  acceptance, each cut one reversible commit / (c) cuts of a boxed statement, a figure, a table or a whole
  subsection wait for the driver's approval; cuts of paragraphs and sentences execute.
- **OD7. The Agent's defaults**, as one item.
