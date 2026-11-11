# WP32 — Scope of work: package-user tests (U1 to U4)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev` |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP32-decisions.md` |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP32-decisions.md`, after `work-packages/WP32-review.md` |

**Header note.** The origin is the supervisor's standing order of 2026-11-11, verbatim
(`docs/superpowers/notes/reader-grid.md`, "Axis 3: package users"): "make sure to add more user test cases for people who
show up and just want to pull the package and read the docs. do personas for both humans coding and coding agents
coding. this is specifically for the HTS package, from that perspective they no little if anything about satellites or
even sysmlv2 they just want to use our feature engineering tool. we want users with and without sysmlv2 models
generatign their data (it could just be measured, or generated another way), and users with and without sysmlv2 model
experience because we don't want to scare not sysmlv2 users away from using the package". The package is the UX loop of
the mandate ("Package-user tests", `PM-BRIEF.md`) and runs before the handover, after the two-panel figure and the
choosing-K page are on the staged site. It runs the full lifecycle ("Bigger candidate edits run the full lifecycle",
`PM-BRIEF.md`); the stage list is at the end. The author of this document is a scope drafter; nothing here is approved.

## Purpose

People will arrive at the repository or the docs site, install the package and try it on a table of their own, knowing
nothing of satellites and, often, nothing of SysML v2. The paper's readers are tested elsewhere; these users are not
readers of the paper. The outcome: the four personas of the reader grid (U1 human coder without SysML v2; U2 human coder
with a SysML v2 model behind the table; U3 coding agent without; U4 coding agent with a model-exported table) each run
the same task end to end on the staged site, their returns are recorded verbatim, every stumble becomes a docs or
package change request with a page or function named, the fixes land, and a fresh cell of each kind completes the task
without a stop the docs owe. The standing question is whether anything made a user think the tool needs SysML v2 or
satellites. Kept apart (`CLAUDE.md`): the **model** (the frontier), the **fit** (the estimator on a table) and the
**analysis** (the tension report and the chart); the tests judge the documentation and the interface, not the method.

## Goals

- G1. **A task per cell, defined and fixed.** The task text for U1 to U4 (install from the README; condition the table;
  fit; choose K; read the tension report and the chart; say which metrics trade; for U2 and U4 also whether the case
  model helps or distracts and whether they could connect their own model), written before any cell runs.
- G2. **Two tables that are not the cubesat.** A plain CSV with no model behind it, and a table exported from a small
  SysML v2 model that is not the cubesat.
- G3. **Fresh cells run with only what a user has.** Four cells, as fresh Sonnet agents (U1 and U2 in the human's role,
  U3 and U4 as agents), each with the README, the staged docs site and the package installed from the repository at a
  named head in a clean worktree.
- G4. **Returns verbatim and triaged.** Each cell's code, pages opened, errors hit and answer to the standing question,
  recorded as returned, then triaged into docs change requests and package change requests.
- G5. **The fixes landed.** Docs fixes by the docs stream; a package unit only where a defect is in the code, with the
  contract check.
- G6. **The loop closed.** A re-run of fresh cells until one of each kind (human without and with SysML v2; agent
  without and with) completes the task without a stop the docs owe.
- G7. **The review run, not read.** The acceptance review runs the cells' code, looks at the rendered pages and
  results, with screenshots in the record.

## Non-goals

- Cells that read the paper, `work-packages/`, the notes, the records or the tests; the paper-reader grid (axes 1 and 2)
  is not touched.
- A real human sitting down: human cells are played by fresh agents in the human's role until one does.
- Changing the method, the case model, the paper or the interface contract; a package change only for a defect found in
  the code, and then as its own unit.
- Teaching SysML v2, or making the tool require it; a SysML v2 path in the docs only as far as the cells show it is owed.
- Scoring the personas or ranking them: the returns are recall and friction, as in the reader rounds.
- A new feature, a new page or a new figure beyond what a triaged change request names.
- Packaging for PyPI or release work.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP32-rounds/tasks.md` *(default)*: the task text per cell, the standing question, and the return format (code, pages opened in order, every error, the result read off, answer to the standing question) | G1 |
| D-2 | `work-packages/WP32-rounds/tables/` *(default)*: the plain CSV (synthetic from `make_frontier_data` with renamed generic columns, or a public dataset of evaluated designs) and the table exported from a small non-cubesat SysML v2 model, with the model source and the export script | G2 |
| D-3 | `work-packages/WP32-rounds/round-1/` *(default)*: the four cells' returns verbatim, with the named head, the staged-site URL and the clean-worktree setup recorded | G3, G4 |
| D-4 | `work-packages/WP32-rounds/triage.md` *(default)*: every stumble as a docs or package change request, the page or function named, the disposition | G4 |
| D-5 | The fixes: docs edits per the docs change requests; a package unit and contract check only for a code defect | G5 |
| D-6 | `work-packages/WP32-rounds/round-N/` *(default)*: the re-run cells, verbatim, until one of each kind completes | G6 |
| D-7 | `work-packages/WP32-review.md` with screenshots, and `work-packages/WP32-decisions.md` | G7 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The task text covers every step of G1 for all four cells and adds the model-side questions for U2 and U4 only; it contains no hint of the package's internals beyond what the README names | Reviewer reads `tasks.md` against G1; a grep of it for names that appear only in `src/` private modules, the notes or the paper finds none |
| R-2 | The plain CSV has no model behind it, no satellite vocabulary in its column names or file, and is loadable with `pandas.read_csv` | Reviewer opens the file and runs `read_csv`; grep for satellite terms finds none |
| R-3 | The model-exported table comes from a SysML v2 model that is not the cubesat, small enough to read; the export script reproduces the table from the model source | Reviewer runs the export script and compares to the committed table; the model file shares no element with `examples/adcs/` |
| R-4 | Every table is strictly positive or states what conditioning the user must do, so the conditioning step is a real task and not a no-op | Reviewer inspects the tables' minima and the task text |
| R-5 | Every cell runs on a Sonnet agent in a clean worktree at the named head, with the package installed as the README says, and has no path to `work-packages/`, the notes or the tests | The worktree listing recorded in the round shows no such directories on the cell's path; the cell's pages-opened list contains only the README and the staged site; the model of each cell is stated in its return header |
| R-6 | Each return holds the code the cell wrote, the pages opened in order, every error and where it stopped, what it would ask a colleague, and the answer to the standing question (did anything make you think you need SysML v2 or satellites) | Reviewer checks the five fields on each return file |
| R-7 | The returns are recorded verbatim, unedited, before any triage | The commit that adds a return does not touch `triage.md`; the diff of a return against the agent's reported text is empty |
| R-8 | Each stumble in a return appears in the triage as a docs change request or a package change request, naming the page or function, or as "no change" with the reason | Reviewer samples every stop and error in the returns and finds its row in `triage.md` |
| R-9 | A package change exists only for a defect in the code, as its own unit with a test, and `src/` changes pass the interface contract check | Reviewer lists the commits touching `src/`; each cites a triage row; the contract check passes (command per `PM-BRIEF.md`, "Verification in tiers") |
| R-10 | After the fixes, the code each cell wrote runs on its table and produces the fit, the chosen K, the tension report and the chart | Reviewer runs each cell's final code from the clean worktree with `uv run` |
| R-11 | A fresh cell of each kind (U1, U2, U3, U4) completes the task without a stop the docs owe, on the fixed site at a named head; a stop the docs owe is one where the cell could not proceed or proceeded wrongly for want of a page, sentence or example that the docs could carry | Reviewer reads the final round's returns and the triage; each cell's stops, if any, are marked "not owed" with a reason a second reader accepts |
| R-12 | The answer to the standing question in the final round is "no" for the U1 and U3 cells; for U2 and U4 the model side is described as optional | Reviewer reads the answers in the final round's returns |
| R-13 | The staged site pages the cells used render without a stderr line, a broken link or a placeholder | Reviewer browses each page in the pane's own tab, with screenshots |
| R-14 | The docs fixes follow the repository's rules: glossary terms, claims backed or narrowed, figures only as already earned | `uv run python scripts/check_vocabulary.py`; `uv run ruff check .`; the docs build; the cold-read rules of `figure-review.md` for any figure touched |
| R-15 | The record shows what the round removed or narrowed as well as what it added (the marginal-value test applied to what is there) | `triage.md` carries a "content that did not earn its place" column; reviewer reads it |

## Definition of good

- A user who knows pandas and scikit-learn and nothing else gets from the README to a fitted model, a chosen K and a
  read tension report in one sitting with no stop, and never meets a satellite unless they went looking.
- A SysML v2 user sees one short path from their model's export to the same table, and a non-SysML v2 user never feels
  that path is the main one.
- Each of the four personas' final returns read as a short, confident success; the changes the round made were
  deletions and reorderings as often as additions.

## Definition of good enough

- G1 to G7 delivered; R-1 to R-15 met.
- One fresh cell of each kind (U1, U2, U3, U4) completed in the final round without a stop the docs owe (R-11).
- Every triage row has a disposition and every change request it names has landed or is recorded as deferred with a
  reason.
- The review is run with screenshots, and the driver has the list of what the round changed.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Lifecycle stages

| Stage | In this package |
|---|---|
| (1) Research spike | Cell definitions, the two tables and the export path from a small SysML v2 model: a spike by Sonnet agents reads what the README and site already offer for each persona and writes a readout with plain options, no change to the product (feeds D-1, D-2) |
| (2) Decision | The driver decides the open decisions below and whether and what to build, on the readout |
| (3) Build | D-1, D-2, then the round (D-3) on the named head with the staged site |
| (4) Quality control | R-5 to R-8: the isolation of the cells, the verbatim returns, the triage complete |
| (5) Integrate | D-5: the docs fixes (and a package unit only for a code defect); the re-run D-6 until R-11 holds |
| (6) Cascade review, then acceptance review | Every page, example and README line a fix moves is found and resolved; the review runs each cell's code and looks at the rendered pages (R-10, R-13), `WP32-review.md` with screenshots |

## Agent's defaults

- The paths under `work-packages/WP32-rounds/` and the file names in D-1 to D-7.
- Cells as Sonnet agents throughout (per "Models by role"); triage by the PM's Sonnet triager; Haiku for mechanical
  steps such as copying returns verbatim and listing pages opened.
- The named head is the tip of `dev` when the round starts, with the staged site built from it by the driver's `stage`
  worktree; the cell worktrees are under the session scratchpad, not the driver's.
- Install is the way the README states (`uv`, from the repository at the head).
- The browser-pane tab for the review is the reviewer's own, created and closed by it; tab-23 is not touched.
- The return format of R-6 and the "did not earn its place" column of R-15.
- A re-run cell is a new agent each time; a cell never sees another cell's return or the triage.
- The round stops at three re-runs; if R-11 does not hold then, it goes to the driver with the open stops.

## Open decisions (for the supervisor)

- **OD1.** Where the plain CSV comes from. Options: synthetic from `make_frontier_data` with renamed generic columns
  (known planted structure, so the reviewer can check the answer) / a public dataset of evaluated designs (a real table,
  no planted answer; needs a verified source and licence) / both, one cell on each.
- **OD2.** Which small SysML v2 model backs the exported table. Options: a toy design problem written for this package
  (a few parts, a few attributes, nothing from space) / an existing public SysML v2 example model with an export
  (nothing of ours in it, but its shape is not ours to choose).
- **OD3.** Where the cell code and the returns live. Options: committed in `work-packages/WP32-rounds/` as above (the
  repository as the research) / outside the repository, with only the triage and the decisions committed.

## Blast radius (files owned)

- Creates: `work-packages/WP32-scope-of-work.md`, `WP32-decisions.md`, `WP32-review.md`, and `work-packages/WP32-rounds/`
  (`tasks.md`, `tables/`, `round-*/`, `triage.md`).
- Edits, per the triage and only the pages a change request names: `README.md`, `docs/getting-started.md`,
  `docs/index.md`, `docs/user-guide/`, `docs/examples.md`, `docs/api.md`, `docs/api-reference.md`, `docs/theory.md`
  (docs stream); docstrings in `src/hyperbolic_trade_space/` only for a defect unit with its tests under `tests/`.
- Does not touch: `derivation/`, `pyproject.toml`, `uv.lock`, `examples/adcs/`, the paper, the interface contract, the
  data of record, the `verify` and `stage` worktrees, tab-23.
