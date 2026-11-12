# WP32 — Scope of work: package-user tests (U1 to U4)

| | |
|---|---|
| **Status** | DRAFT, for the chief engineer's approval. Approved only by the recorded act below; nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The chief engineer's approval, quoted verbatim in `work-packages/WP32-decisions.md` |
| **Acceptance record** | The chief engineer's acceptance, quoted verbatim in `WP32-decisions.md`, after `WP32-review.md` |

## Purpose

The supervisor's standing order, verbatim (`reader-grid.md`, "Axis 3: package users"): "make sure to add more user test
cases for people who show up and just want to pull the package and read the docs. do personas for both humans coding and
coding agents coding. this is specifically for the HTS package, from that perspective they no little if anything about
satellites or even sysmlv2 they just want to use our feature engineering tool. we want users with and without sysmlv2
models generatign their data (it could just be measured, or generated another way), and users with and without sysmlv2
model experience because we don't want to scare not sysmlv2 users away from using the package".

Four cells: U1 human coder, no SysML v2; U2 human coder, SysML v2 model behind the table; U3 coding agent, no SysML v2;
U4 coding agent, table exported from a model. Each runs one task on the staged site (http://127.0.0.1:8791/, head
named per round; the WP30 cascade has landed; the package tests run on Linux and Windows). Returns are recorded
verbatim, stumbles become docs or package change requests, fixes land, fresh cells re-run until one of each kind
completes without a stop the docs owe. The standing question: did anything make them think they need SysML v2 or
satellites to use the tool. The tests judge documentation and interface, not the method (`PM-BRIEF.md`, "Package-user
tests").

## Goals

- G1. **One task text,** written before any cell runs: install as the README says; condition the table; fit; choose K;
  read the tension report and the chart; say which metrics trade; for U2 and U4 also whether the case model helps or
  distracts and whether they could connect their own model.
- G2. **Two tables that are not the cubesat:** a plain CSV; a table exported from a small non-satellite SysML v2 model.
- G3. **Four cells with only what a user has:** the README, the docs site at the stage URL, the package installed in a
  clean worktree. Nothing else in reach.
- G4. **Returns verbatim, then triaged,** each change request naming a page or function.
- G5. **Fixes landed;** G6. **the loop closed** (re-runs until one cell of each kind completes);
  G7. **the review runs the cells' code and looks at the rendered pages.**

## Non-goals

- Cells that read the paper, `work-packages/`, the notes, the records or the tests.
- A real human (human cells are fresh agents in the human's role); scoring or ranking personas.
- Changing the method, case model, paper or interface contract; new features, pages or figures beyond a triaged request;
  teaching SysML v2 or making the tool need it; PyPI work.
- Journeys and first screens (WP33). These returns double as WP33's wayfinding data for U1 to U4, so the task text asks
  for steps to the need and where the cell got lost.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP32-cells/tasks.md`: task text, standing question, return format | G1 |
| D-2 | `tests/fixtures/user-tests/`: synthetic CSV (from `make_frontier_data`, generic column names); small SysML v2 model source, export script, exported table | G2 |
| D-3 | `WP32-cells/round-1/`: four returns verbatim, with head, stage URL and setup | G3, G4 |
| D-4 | `WP32-cells/triage.md`: each stumble, disposition, and a column "content that did not earn its place" | G4 |
| D-5 | The fixes: docs edits; a code unit with a test only for a defect | G5 |
| D-6 | `WP32-cells/round-N/`: re-runs verbatim | G6 |
| D-7 | `WP32-review.md` with screenshots; `WP32-decisions.md` | G7 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The task text covers G1, adds model-side questions for U2 and U4 only, names nothing internal beyond the README | read it; grep for private-module, notes and paper names finds none |
| R-2 | The CSV has no model behind it, no satellite vocabulary, loads with `pandas.read_csv`, and needs conditioning (a real step) | run it; grep; inspect minima |
| R-3 | The exported table comes from a model sharing no element with `examples/adcs/`; the script reproduces it | run the script, compare |
| R-4 | Each cell runs on Sonnet in a clean worktree at the named head, with no path to `work-packages/`, notes or tests; the model is named in the return header | worktree listing recorded; pages-opened list holds only the README and the stage URL |
| R-5 | Each return holds the code, pages opened in order, every error and where it stopped, what it would ask a colleague, steps to the need, and the answer to the standing question | check the six fields |
| R-6 | Returns are unedited and committed before triage | the commit does not touch `triage.md`; diff against the agent's text is empty |
| R-7 | Every stop and error has a triage row: a request, or "no change" with a reason | sample all against `triage.md` |
| R-8 | A code change is only for a defect, its own unit with a test, citing a row; contract check passes | `git log` on `src/`; `uv run pytest tests/test_interface_contract.py` |
| R-9 | After the fixes each cell's final code runs and yields the fit, the K, the tension report and the chart | run each with `uv run` |
| R-10 | A fresh cell of each kind completes without a stop the docs owe (it could not proceed, or proceeded wrongly, for want of a page, sentence or example the docs could carry) | read final returns and triage; remaining stops marked "not owed" with a reason a second reader accepts |
| R-11 | The standing question is "no" for U1 and U3; for U2 and U4 the model side is described as optional | read the final answers |
| R-12 | Pages the cells used render without a stderr line, broken link or placeholder | reviewer's own pane tab; screenshots |
| R-13 | Docs fixes follow the repository's rules | `uv run python scripts/check_vocabulary.py`; whole-repo `uv run ruff check .` and `uv run ruff format --check .`; docs build |
| R-14 | The record shows what the round removed or narrowed as well as added | the D-4 column |

## Definition of good

- A user who knows pandas and scikit-learn and nothing else gets from the README to a fitted model, a chosen K and a
  read tension report in one sitting, and never meets a satellite unless they went looking.
- A SysML v2 user finds one short path from the model's export to the table; a non-SysML v2 user never feels it is the
  main one. The round's changes were deletions and reorderings as often as additions.

## Definition of good enough

- G1 to G7 delivered; R-1 to R-14 met; one fresh cell each of U1 to U4 completes in the final round (R-10).
- Every triage row has a disposition; every request it names has landed or is deferred with a reason.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent models by role

Sonnet for every cell, reader, triager, implementer and reviewer; Haiku for mechanical units (copying returns
verbatim, listing pages opened, screenshot runs, greps); nothing larger than Sonnet. A re-run cell is a new agent; no
cell sees another's return or the triage; no agent spawns another without the PM.

## Agent's defaults

- Recorded 2026-11-11 (`WP32-decisions.md`), restated for approval: synthetic CSV, no public dataset; a small
  non-satellite model built for the test (a pump, bicycle or heat exchanger trade, three or four metrics); fixtures under
  `tests/fixtures/user-tests/`, cells' code and returns under `WP32-cells/`.
- U4 is given the model source and the exported table; U3 the CSV. Cells are in worktrees under the session scratchpad;
  the browser tab is the reader's own; tab-23 is not touched.
- Install is whatever the README says. If it gives a package-only user no path, that is a triage finding, fixed in the
  docs; the cell is not handed a path.

## Open decisions (for the chief engineer)

- **Q1. When does the loop stop if a stop the docs owe persists?** Options: after three re-runs, open stops go to the
  chief engineer / after two / no limit until R-10 holds.
- **Q2. A code defect a cell finds.** Options: fixed in this package as its own unit with a test / recorded as a change
  request for a later package.

## Blast radius

- Creates: `WP32-decisions.md`, `WP32-review.md`, `WP32-cells/`, `tests/fixtures/user-tests/`.
- Edits, only what a request names: `README.md`, `docs/getting-started.md`, `docs/index.md`, `docs/user-guide/`,
  `docs/examples.md`, `docs/api.md`, `docs/api-reference.md`, `docs/theory.md`; docstrings in `src/` only for a defect
  unit (Q2).
- Never: `derivation/`, `pyproject.toml`, `uv.lock`, `examples/adcs/`, the paper, the interface contract, data of
  record, the `verify` and `stage` worktrees.

## Lifecycle stages

(1) Spike: Sonnet readout of what README and site offer each persona and how the model exports a table; no product
change. (2) Decide. (3) Build: D-1, D-2, round 1. (4) Quality control: R-4 to R-7. (5) Integrate: D-5, re-runs.
(6) Cascade review, then acceptance: the reviewer runs the cells' code and screenshots the pages.
