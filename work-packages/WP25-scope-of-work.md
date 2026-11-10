# WP25 — Scope of work: Repository tidiness, first instance (cruft deleted, drift and gaps listed; step 3h, recurring)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP25-decisions.md` |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `work-packages/WP25-decisions.md`, after `work-packages/WP25-review.md` |

**Header note: a recurring package; this is its first instance, small, one stream.** The supervisor asked for
periodic clean-up packages (`WP25-decisions.md`, "Origin"); the driver's disposition makes it step 3h of the path,
"one small instance at each gate and one before the PR". This instance runs now that WP23's first round has landed
(`work-packages/WP23-rounds/round-1`, c0f43f2 green at tier 2) and WP24 is approved (its "Gate outcomes",
2026-11-09 22:50). It touches nothing in WP23's blast radius (`WP23-scope-of-work.md`, "Blast radius") and none of
WP24's surfaces (`WP24-scope-of-work.md`, "Blast radius") until those packages' gates: deletions on those surfaces
and every drift fix on a docs page are listed here with the instance that lands them, not made. Later instances (at
WP23's data gate, WP24's acceptance, WP16's gate, WP11's rounds, and once before the PR) are each a short amendment
to this document: one new line in this note naming the gate, the head and the counts, approved by the driver and
quoted in `WP25-decisions.md`; the inventory and the review are rewritten to the present each time (A3).

- Instance 1 (WP23 round 1 landed, WP24 approved): 2026-11-10, head 73c5bff; 346 rows, 169 deleted (09117d8), 33 held
  (WP23's), 144 kept; inventory db150fc; review `WP25-review.md`: 18 drift rows, 9 gap rows.
- Instance 2 (WP23 accepted at db59365; WP24 at push 2): 2026-11-10, head a9e23b2; scope `WP25-2-scope-of-work.md` (own file:
  it carries its sequencing against WP24); 198 rows, 31 deleted in unit A (the commit "WP25: 31 files deleted (second instance, unit A)"), 29 held,
  138 kept; inventory and review `WP25-inventory.md`, `WP25-review.md`.
- Instance 3 (the WP23 close-out accepted, WP24 final): 2026-11-10, scoped at fbee839, executed at ca6ce94 to the head of
  `WP25-review.md`; scope `WP25-3-scope-of-work.md` (own file: the two open file decisions and the survey); 209 rows, 1
  deleted (de3ce61, `spike-ternary/report.md`), 61 held (WP11's, WP26's and WP27's files, `search-prior-art.md`,
  `P10-review.md`), 148 kept; OD2's file held for the PM (a test reads it); inventory and review rewritten.

Sizing at `dev` cc409f8: 622 tracked files. A first pass (each tracked file's basename grepped across every other
tracked file; it credits a reference to any file sharing the name, so it undercounts) finds under
`docs/superpowers/notes/` 235 files of which 83 are referenced nowhere (75 of them under `spike-sysml-diagrams/`,
whose `project.py` is live and WP23's); under `work-packages/` 125 files of which 19 (13 of them the raw reader
reports and a slice of `WP11-round-1/`, whose `triage.md` is the kept record); under
`examples/adcs/experiments/reports/` 3 files, all referenced, and in WP23's blast radius. No scratch folder is
tracked. The spike folders the supervisor's disposition names for deletion hold 31 (`spike-ternary`), 2
(`spike-ggp-fit`), 3 (`spike-soft-fit`), 4 (`spike-facet-rename`) and 108 of 109 (`spike-sysml-diagrams`, all but
`project.py`) files. Drafted 2026-11-09 from the inputs under Purpose.

## Purpose

The supervisor, 2026-11-09, 22:20, verbatim (`WP25-decisions.md`): "i appreciate you clean up all the images, i think
we are also starting to accumulate a pretty big documentation cruft/drift/gap i want you to periodically deploy clean
up work packages to address repo tidiness, this is essentially context management. the git history keeps everything
so tidying doesnt eliminate history, history keeping is gits job the repo state itself does not need to duplicte that
effort".

His two standing orders govern every unit (`PM-BRIEF.md`, 23:05 and 23:10; `CLAUDE.md`): the marginal-value test,
does this earn its place, "applies to every piece of content ... and to what already exists, not only to what a unit
would add"; "each deletion names in its commit what the content no longer did"; and "stuck means assess removal".
The driver's disposition (`WP25-decisions.md`) fixes the three parts and their checks: cruft, with an inventory of
every file not referenced by the docs navigation, a test, a script, the paper or another live document, each with
its disposition; drift, the docs and notes saying what the code and the glossary say now, checked by the vocabulary
tool, the claims register, the doctests and a read of each docs page against the current API and defaults; gaps,
what exists in the code or the paper with no documentation, listed and either filled or scheduled. "The repository
state is the present; the history is git's."

The need, in his words, is context management: a fresh PM, a reviewer or the supervisor at his review reads the tree
as the present, and a file that is no longer true or no longer read costs each of them the work of finding that out.
The outcome of this instance: every tracked file either has a named reader or is gone; what the docs say that the
code no longer says is listed with its fix and the push that lands it; what the code and the paper do that no page
says is listed with where it will be said.

Inputs: `WP25-decisions.md`, `release-candidate.md` (step 3h; and step 5a, which this package is not), `PM-BRIEF.md`
("Repository tidiness", "Negative edits are welcome", "Parallel streams and pushing", "Verification in tiers"),
`CLAUDE.md`, `WP24-scope-of-work.md` (its blast radius; A5: the notes are records and the spike folder is WP25's to
delete), `WP23-scope-of-work.md` (its blast radius and non-goals), `WP10-decisions.md` ("one stream owns it"),
`mkdocs.yml` (the navigation), `scripts/check.py` (the path-to-test map), `glossary.yaml` (the six entries of
73c14e5: cell, reach, near-frontier band, effective sample size, mean slack, certificate), `interface-contract.toml`
(the pinned public names), `docs/superpowers/notes/{vocabulary-review,claims-review}.md`.

## Goals

- G1. **Cruft gone.** An inventory of every tracked file not referenced by the live set (A1) with one of three
  dispositions, keep (its reader named), delete, or hold (the package whose gate it waits for, and the instance that
  deletes it); the delete rows removed in one commit whose message lists each path and what the content no longer did.
  Named by the supervisor's disposition and the driver's brief: the spike folders whose result is in a decision record
  or a note (`docs/superpowers/notes/spike-ternary`, `spike-ggp-fit`, `spike-soft-fit`, `spike-facet-rename` now that
  WP24 is approved, the superseded outputs of `spike-sysml-diagrams`), the raw reader reports and slices after triage
  (`work-packages/WP11-round-1/P*-{A,B}.md`, `slice-*.md`; `triage.md` stays), superseded reports and retired scripts
  (the older comparisons of `examples/adcs/experiments/reports/` and the round scripts of the modeller loop, held
  for WP23's gate), outputs nothing reads. Each package's scope, decisions and review stay.
- G2. **Drift listed, and closed where a surface is free.** Each page of the docs navigation (`mkdocs.yml`, 15 pages
  and the compiled glossary), `README.md` and `site/index.html` read against the current API and defaults
  (`term_aggregation` and its default `"sum"`; the `color` option of the plotting functions and its values; the six
  glossary entries of 73c14e5 used where the page says the thing; the adopted model's two views and the chain they
  make explicit), with the vocabulary tool and the claims register as checks and the doctests as the suite runs them;
  each finding with its fix drafted and the push that lands it. In this instance every docs page is WP24's surface,
  so the fixes land in WP24's docs push or in the next instance; a fix is made now only on a surface no executing
  package owns.
- G3. **Gaps listed.** Every pinned public name of `interface-contract.toml` and every feature the paper or the case
  exercises that no docs page names, listed with a disposition: filled (on a free surface, now) or scheduled (the
  package or instance, named).
- G4. **Checked as run.** The docs strict build, the suite, the two guards and `git show --stat` of the deletion
  commit, with their output lines in the review; the review's reviewer runs them.

## Non-goals

- No change to any statement, number or figure of the paper, and nothing under `paper/` or `derivation/` (the
  record `paper/container/RECORD.md` included).
- Not step 5a: the improvement-by-subtraction pass over the paper and the docs, which runs once the content is
  complete (`release-candidate.md`), is not this package; this package deletes files nothing reads and lists drift
  and gaps, it does not judge prose, figures or arguments.
- No archive folder, no `attic/`, no renaming into an "old" path: deletion only; git keeps the history.
- Nothing under `src/` except dead code shown unreachable by a test and a grep, each item listed in the review with
  the grep; none is expected in this instance.
- Not WP23's files until its data gate and not WP24's surfaces until its acceptance (the header note): `examples/adcs/`
  (the model, the views, the case code, `experiments/reports/*`, `ledger_swap.py` and its successors,
  `case-model.md`), `work-packages/WP23-rounds/`, `docs/superpowers/notes/spike-sysml-diagrams/project.py` and what
  it reads; `docs/*.md`, `docs/user-guide/*.md`, `site/index.html`, `README.md`, `glossary.yaml`,
  `scripts/vocabulary_baseline.toml`, `claims_register.toml`, `tests/`. A deletion or a fix on these is a hold or a
  scheduled row, never an edit.
- The frozen data and the ledgers stay: `examples/adcs/data/*` (the cited comparison, `release-candidate.md`),
  `examples/adcs/experiments/ledger/*`.
- No new tooling beyond A2: no script, no test, no CI step is added for the inventory in this instance.
- Not a vocabulary or claims pass: the two tools are run as checks; a failure they report on a free surface is fixed,
  one on an owned surface is a drift row.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP25-inventory.md`: the command (A2) and the live set (A1) in its header; one row per tracked file outside the live set with path, what references it (or "nothing"), disposition (keep: reader / delete / hold: package, instance) and, for delete rows, what the content no longer does | G1 |
| D-2 | The deletion commit: every delete row of D-1 removed, nothing else in the commit, its message listing each path with what the content no longer did; `scripts/check.py`'s path map edited in the same commit only if a deleted path is mapped there | G1 |
| D-3 | `work-packages/WP25-review.md`, "Drift": one row per page of G2 (page, read against, finding or "none", fix drafted, lands in), and the output lines of the vocabulary tool, the claims register test and the doctests | G2 |
| D-4 | `work-packages/WP25-review.md`, "Gaps": one row per gap (the name or feature, where it lives in code or paper, disposition: filled where / scheduled to which package or instance) | G3 |
| D-5 | `work-packages/WP25-review.md`, "Checks": the docs strict build, the suite, the two guards, `git show --stat` of D-2, each with its command and its result line; the reviewer's own rerun | G4 |
| D-6 | `work-packages/WP25-decisions.md`: the driver's approval and the acceptance, verbatim; this document's header note amended per instance (A3) | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The inventory is complete and decided: every tracked file outside the live set has exactly one row, every row one of the three dispositions, no row undecided | the reviewer reruns the inventory command (D-1 header) at the head and diffs the path set against D-1's rows (empty); `grep -ciE "undecided\|tbd\|\?\?" work-packages/WP25-inventory.md` returns 0 |
| R-2 | The deletions are one commit whose message lists each path with what the content no longer did, and the commit's paths equal the inventory's delete rows one to one | `git show --stat <hash>` against D-1's delete rows; `git show --format=%B -s <hash>` names each path |
| R-3 | Nothing deleted was read: the docs build strictly, the suite is green, and each deleted basename grepped over the remaining tree is found only in records (listed in the review) | `uv run mkdocs build --strict -f mkdocs.yml -d <tmp>` (or `uv run python scripts/assemble_site.py`); `uv run pytest -q`; `git grep -n -F <basename>` per deleted file, hits listed in D-5 |
| R-4 | The two guards pass at the head | `uv run python scripts/check_vocabulary.py` (exit 0); `uv run pytest -q tests/test_vocabulary.py tests/test_claims_register.py` |
| R-5 | The paper, the derivations and the package are untouched; no file is renamed or moved; no archive path appears | `git diff --stat <start>..HEAD -- paper derivation src` is empty; `git diff --diff-filter=R --stat <start>..HEAD` is empty; `git diff --diff-filter=A --name-only <start>..HEAD` lists only `WP25-inventory.md`, `WP25-review.md` and `WP25-decisions.md` |
| R-6 | WP23's blast radius and WP24's surfaces are untouched | `git diff --stat <start>..HEAD -- examples work-packages/WP23-rounds docs/superpowers/notes/spike-sysml-diagrams/project.py docs/*.md docs/user-guide site README.md glossary.yaml scripts/vocabulary_baseline.toml claims_register.toml tests` is empty |
| R-7 | Every page of G2 has a drift row; every finding has a drafted fix and a named landing push; the three checks' output lines are in the review | inspection of D-3: 16 navigation rows (15 pages and the compiled glossary) plus `README.md` and `site/index.html`; `uv run python scripts/check_vocabulary.py`, `uv run pytest -q tests/test_claims_register.py`, `uv run pytest -q --doctest-modules src` lines present |
| R-8 | Every pinned public name of the contract manifest appears on a docs page or has a gap row; every feature the review names as exercised by the paper or the case and absent from the docs has a gap row with a disposition | the command recorded in D-4 (each name of `interface-contract.toml`'s pinned lists grepped over `docs/*.md docs/user-guide/*.md docs/api-reference.md`), its misses equal to D-4's name rows |
| R-9 | Each commit's message names the unit and, for a deletion, what the content no longer did; no commit carries an attribution line; each push leaves `dev` green at tier 2 | `git log --format=%B <start>..HEAD \| grep -ciE "co-authored-by\|generated"` returns 0; the push hashes with the watcher's verdict in D-5 |
| R-10 | The recurrence is recorded: this document's header note carries the instance line (gate, head, counts), and `WP25-decisions.md` the approval | inspection |

## Blast radius

The files this package may change; anything else is a stop and a question to the PM. One stream owns all of it.

- Delete only, per the inventory's delete rows: `docs/superpowers/notes/spike-ternary/`, `spike-ggp-fit/`,
  `spike-soft-fit/`, `spike-facet-rename/`, `spike-sysml-diagrams/` except `project.py` and any file it reads (A4),
  and any other spike folder or note whose result the inventory shows recorded elsewhere (A1); `work-packages/
  WP11-round-1/` except `triage.md`; `work-packages/streams/`, `work-packages/external-assessment-2026-11-09/` except
  its `triage.md`, `work-packages/PM-HANDOVER-2026-11-09.md`, as the inventory decides; `examples/adcs/figures/*.png`
  only if the inventory shows no notebook, page or test reads them and WP23's blast radius does not name them.
- Edit: `scripts/check.py` (the path map, only if a deleted path is mapped there).
- Records of this package: `work-packages/WP25-scope-of-work.md` (the header note, per instance), `WP25-inventory.md`,
  `WP25-review.md`, `WP25-decisions.md`.
- Never in this instance: everything the Non-goals list; `pyproject.toml`, `uv.lock`, `.python-version`, `mkdocs.yml`,
  the CI workflow, `docs/superpowers/specs/`, the standing notes `CLAUDE.md` and `PM-BRIEF.md` name, every other
  `work-packages/*.md`.

## Definition of good

- A tree in which every tracked file has a reader a newcomer can name, nothing is kept because deleting feels
  risky, the docs say what the code says today with its defaults, and nothing the code or the paper does goes unsaid;
  a fresh PM handed the repository reads only the present, and finds the past where it belongs, in `git log`.

## Definition of good enough

- The inventory has no undecided row (R-1).
- The deletions are in one commit whose message lists them, each with what the content no longer did (R-2).
- The docs build strictly and the suite is green at the head (R-3); the vocabulary and claims guards pass (R-4).
- The paper, the derivations and the package are untouched, nothing is moved or archived, WP23's and WP24's
  surfaces are untouched (R-5, R-6).
- Every page of G2 has its drift row and every finding its fix and landing push (R-7); every pinned name and every
  named feature has a page or a gap row (R-8).
- No attribution line; `dev` green at tier 2 after each push; the instance recorded (R-9, R-10). Stop there and
  present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

Approved or changed as one item at the scope gate. Each is marked *(default)* where it appears.

- **A1. The live set, and what a reference is.** A file is referenced when a file of the live set names its path or
  basename. The live set: the pages of `mkdocs.yml`'s navigation, `README.md`, `site/index.html`, `CLAUDE.md`,
  `glossary.yaml`, `claims_register.toml`, everything under `src/`, `tests/`, `scripts/`, `derivation/`, `paper/`,
  and `examples/adcs/`, the design spec under `docs/superpowers/specs/`, the standing notes named
  by `CLAUDE.md` or `PM-BRIEF.md`, `work-packages/{README,PM-BRIEF,release-candidate,parallel-board,driver-log,
  release-punch-list,swap-evidence,interface-contract}.*`, and the scope, decisions and review of every package not
  yet accepted. A reference from an accepted package's record (its scope, decisions or review), from a note, or from
  a spike's own files does not keep a file: the record names what was, and git holds it (the supervisor: "history
  keeping is gits job"). Each package's scope, decisions and review are kept whatever references them
  *(default)*.
- **A2. The inventory method.** A one-off command, recorded verbatim in `WP25-inventory.md`'s header so the next
  instance reruns it: `git ls-files` minus the live set, each remaining file's path and basename grepped
  (`git grep -l -F`) over the live set, misses becoming rows; the referenced rows the rule lets through are triaged
  by hand against the disposition classes (spike with a recorded result, raw report after triage, superseded report,
  retired script, output nothing reads). No script enters `scripts/` and no test is added; a later instance may
  promote the command to a script if two reruns show it stable (the alternative, a script now, adds two files the
  present does not read) *(default)*.
- **A3. One inventory and one review, rewritten per instance.** `WP25-inventory.md` and `WP25-review.md` describe the
  present instance; earlier instances are in git. `WP25-decisions.md` accumulates every instance's approval and
  acceptance. Each instance is one amendment line in this document's header note (gate, head, counts), approved by
  the driver *(default)*.
- **A4. `spike-sysml-diagrams`.** `project.py` is in WP23's blast radius and is read by `tests/test_system_model_v2_r1.py`
  and `examples/adcs/case-model.md`; it and any file it reads (the `model/` inputs, if the grep shows them read) are
  hold rows for WP23's gate; `out/`, `evidence/`, `render.sh`, `SCOPE.md` and `report.md` are delete rows if the
  inventory shows their result in `WP22-review.md` or `WP22-decisions.md` *(default)*.
- **A5. Order of the units.** (1) the inventory, committed on its own, then the deletion commit, then the docs build,
  the suite and the guards, then the push; (2) the drift read, fanned out one read-only agent per page returning
  rows, assembled into the review; (3) the gaps list; then the review's reviewer reruns R-1 to R-8. Deletions land
  before the drift read so that the read is of the present tree *(default)*.
- **A6. Where drift fixes and gap fills land.** A fix on a docs page, `README.md` or `site/index.html` is scheduled to
  WP24's docs push (its A3, push 4) when the sentence it touches is one WP24 rewrites, and to the next WP25 instance
  otherwise; the drift row says which. A fix on a surface no package owns is made in this instance in its own commit
  *(default)*.
- **A7. "Nothing reads it" for outputs.** A committed image, CSV or JSON is an output nothing reads when no notebook,
  page, test, script or generator names its path, and it is not pinned by the interface contract or
  `paper/environment_values.toml`; `examples/adcs/figures/*.png` are tested by this rule and held for WP23's gate if
  the case notebook or its tests name them *(default)*.
- **A8. The deletion commit's message.** Subject: "WP25: <n> files deleted (first instance)"; body: one line per
  path, "path: what it no longer did" (for example "spike-ternary/make_why.py: drew a mock for the spike; the spike's
  result is recorded in WP8a-decisions.md and WP18-scope-of-work.md"); the inventory's delete rows carry the same line *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (decided by the supervisor before this draft: the package's
existence, its three parts, deletion rather than archiving, the records kept; decided here as Agent's defaults: one
item, A1 to A8, for the driver under the mandate; deferred 0; raised 0).

## Gate outcomes

- 2026-11-09, 23:20: approved for execution by the driver under the mandate; no open decision; the Agent's defaults
  A1 to A8 accepted as one item; governing rule: negative edits (the supervisor's standing order); the paper, the
  derivations, the package and WP23's and WP24's surfaces untouched by this instance; recurs at each later gate.
