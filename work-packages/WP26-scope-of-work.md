# WP26 — Scope of work: the model in the view editor (a modeller and a UX researcher, one round)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` when the driver judges it merits CI |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`, "The mandate"), quoted verbatim in `work-packages/WP26-decisions.md`, section "Scope gate" *(default heading)* |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `work-packages/WP26-decisions.md`, after the PM's review of D-1 to D-3 |

**Header note: two agents, two deliverables, one browser.** The modeller drives the editor's pane and changes the
model; the UX researcher never drives the pane and writes the feedback report. Their files do not overlap. IDs are
new to this package. Drafted 2026-11-10 from `dev` at cc0e1c9.

## Purpose

The supervisor, verbatim (2026-11-10): "i want you to have the PM scope and deploy 2 agents to collaborate; one is
tasked with using the view editor to further improve the quality of the model for our papers case. i see the view
editor as enabling constraints plus a useful integrated modeling environment that helps us ensure our sysmlv2 model is
conformant, intuitive, interpretable and aligned with our intents. it will help us make the most of the sysmlv2
affordances without requiring open ended exploration of text. the other agents job is to sit over the shoulder of the
modeler and doing UX research. the second agents output is a report for the person who built the view editor aimed at
providing productive and constructive feedback covering what worked well, what didn't work well and logging bugs if
and when they are encountered, as well as documenting workarounds. the reason i need 2 agents is i want each to have
clearly scoped deliverables which are distinct. the modeler is going to improve our model, the UX reseacher captures
feedback for the provider of the view editor."

State at drafting (the driver, 2026-11-10): the OpenMBEE View Editor (https://openmbee-view-editor.vercel.app/app) has
a project "cubesat" holding `examples/adcs/model_v2/cubesat.sysml` applied verbatim (51,749 characters, revision 2).
The first exploration (`scratchpad/view-editor/report.md`) found that the editor parses the model with no issues and
lists its elements in the model tree, but draws no diagram for it: the editor draws named `view` usages, and the model
declares none (the editor's rover example declares them in its own `views.sysml`). The intents the model must serve
are the supervisor's, recorded in `WP22-decisions.md` ("The model-realism loop": "a space of configs on one side (how
its constructed) and a space of metrics on the other (how its evaluated)") and `WP23-decisions.md` (every traded metric
marked MoE or MoP and tied to a requirement; the coverage table as a connected graph of configuration values,
coupling variables and metrics, "think of this in terms of the coupling variables between subsystems in the MDAO
lit"). The model as it now stands is the WP23 close-out's: eight traded metrics, his four requirement values, `dod_ok`
a flag (`WP23-closeout-scope-of-work.md`).

## Goals

- G1. **The model's quality, read through the editor.** The modeller uses the editor's parser, issues panel, model
  tree, requirements table and traceability matrix to find where the model falls short on four counts: conformance
  (what the editor accepts and flags), intuitiveness and interpretability (names, `doc`s, structure, as the editor's
  tables show them), alignment with the intents above, and use of the editor's affordances. Each finding becomes a
  change with its checks, or a held change with its reason (the driver, 2026-11-10).
- G2. **Views the editor draws.** The model gains a `view` package so that the editor renders the model's own two
  views (the assembly view: the configuration space; the behavioural view: the metric space, the requirements and how
  the metrics are obtained) or better ones, and its requirements table and traceability matrix read the model's
  `satisfy` and `verify` statements (the driver, 2026-11-10).
- G3. **Feedback for the editor's author.** The UX researcher's report tells the editor's author what worked well,
  what did not, each bug with steps a stranger can follow and a screenshot, the workarounds used, and suggestions; in
  a constructive tone, for an outside reader, since the supervisor sends it (the supervisor, Purpose; the driver,
  2026-11-10).

## Non-goals

- No change to the data of record or to any output (datasets, ledger outputs, the paper's numbers, the coverage
  table's content, the committed views) in this package without the data gate. A change that alters a calc or an
  output is written up and sequenced as a later unit needing the driver's go, after the close-out's gate has landed.
- No new metric, requirement value, configuration variable or calc that an output reads.
- No paper prose and no docs page (`paper/`, `docs/` outside the generator named below).
- No account and no sign-in on the editor; nothing of the repository goes to the editor except the model text (the
  supervisor's request) and the `view` package of D-1.
- The UX researcher writes no model change and does not drive the pane.
- No change under `src/`, `derivation/`, `examples/adcs/data/`, `examples/adcs/experiments/` (the ledger included,
  unless OD1 decides (b)), `pyproject.toml`, `uv.lock`.
- A second round (another two hours each): a later unit, on the driver's word.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The modeller's units, each committed and pushed to `dev` with its checks: (a) the `view` package as its own file beside the model, `examples/adcs/model_v2/views.sysml` *(default; the rover example's pattern)*, declaring the views of G2 by `expose` and `filter` on the model's own packages, each view's `doc` naming the intent it shows; (b) the changes list `work-packages/WP26-model-changes.md` *(default)*: every finding of G1 with the intent it serves, its class (landed: outputs byte-identical and checked; held: inside `cubesat.sysml`, waiting on OD1's outcome or the next regeneration; gate: alters a calc or an output), its diff, and its check results; (c) the in-file changes that OD1's outcome lets land in this round, with the model tests' pins and, if a name the generator reads changed, the views regenerated by `docs/superpowers/notes/spike-sysml-diagrams/project.py` | G1, G2 |
| D-2 | The feedback report, `work-packages/WP26-view-editor-feedback.md`: what worked well; what did not; bugs (title, numbered steps from the editor's landing page, expected, observed, screenshot, whether the modeller reproduced it); workarounds; suggestions; with the screenshots it cites copied to `work-packages/WP26-view-editor-feedback/` *(default)* so the report travels whole | G3 |
| D-3 | The step log and screenshots: `scratchpad/view-editor/wp26/steps.md` and one screenshot per step beside it (not committed; the PM's review reads them) | G1, G2, G3 |
| D-4 | The decision records, `work-packages/WP26-decisions.md`: the scope gate, OD1, the milestone calls, the driver's go for any gate-class change, the supervisor's acceptance, verbatim | all |

## Requirements

`<start>` is cc0e1c9, or the `dev` head at approval if later; it is named in the scope gate's record.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every output stays byte-identical: the ledger verifies with no drift | `PYTHONPATH=examples/adcs uv run python -m experiments verify` prints "0 drifts" after every landed unit |
| R-2 | The model's toolkit gates and pins pass | `REQUIRE_OPENSYSML=1 uv run pytest tests/test_model_checking_v2.py tests/test_system_model_v2.py tests/test_system_model_v2_r1.py tests/test_mutation_v2.py tests/test_model_coverage.py tests/test_interface_contract.py` |
| R-3 | The coverage table and the committed views are unchanged (under OD1 (b), the coverage table differs only in its model-hash line) | `uv run python examples/adcs/model_v2/coverage.py --out <tmp>` and `diff -r <tmp> examples/adcs/model_v2/views/` on the coverage files; the views tests of R-2 (`test_committed_views_are_the_generators_output_on_the_model`) |
| R-4 | The `view` package parses with the model in the editor with 0 issues, and each of its views renders a diagram or a populated table; the requirements table lists every requirement of the model and the traceability matrix shows the `satisfy` relations | the step log's screenshots of the Issues panel ("No issues ...") and of each view, read by the PM; where the pinned toolkit loads two files, a test in `tests/test_system_model_v2.py` loads `cubesat.sysml` with `views.sysml` and finds every exposed name *(default)* |
| R-5 | Each view and each changes-list entry names the intent it serves, quoted from `WP22-decisions.md` or `WP23-decisions.md`; one object, one name (the glossary's terms in `doc`s and in the list) | read; `uv run python scripts/check_vocabulary.py` exits 0 |
| R-6 | No gate-class change lands: every landed entry of the changes list has R-1 to R-3 green at its commit; every gate-class entry is unlanded and listed for the driver | `git diff --stat <start>..HEAD -- examples/adcs/model_v2/cubesat.sysml` is empty under OD1 (a); the changes list read against `git log <start>..HEAD` |
| R-7 | Each bug in D-2 has numbered steps a stranger can follow from the editor's landing page, the expected and observed behaviour, a screenshot, and the modeller's one reproduction (reproduced / not reproduced) | read; the PM follows one bug's steps on the screenshots cold |
| R-8 | D-2 carries no internal project detail beyond what a reproduction needs, and no attribution | `grep -nE "WP[0-9]\|driver\|\\bPM\\b\|supervisor\|ledger\|work-packages\|Claude\|agent" work-packages/WP26-view-editor-feedback.md` finds nothing a reproduction does not need |
| R-9 | D-2's tone is constructive: each "did not work" item is paired with what was tried, the workaround if any, and a suggestion where one is evident | read by the PM |
| R-10 | One screenshot per step: the step log's rows and the screenshot files agree; each step records the editor's revision and its issues count | `ls scratchpad/view-editor/wp26/*.jpg \| wc -l` equals the log's step count; read |
| R-11 | No account, no sign-in; nothing pasted into the editor but the model text and the `view` package | the step log names the source of every paste; read |
| R-12 | The seam holds: only the blast radius changes; no AI attribution on any commit or file | `git diff --stat <start>..HEAD`; `git log <start>..HEAD --format=%B \| grep -iE "co-authored\|generated by\|claude"` returns nothing |
| R-13 | The time box: two hours of editor work for the modeller and two hours for the researcher in this round | the step log's first and last times; the researcher's report date and its milestone notes |

## Blast radius

The files this package may change; anything else is a stop and a question to the PM.

- The modeller: `examples/adcs/model_v2/views.sysml` (new); `work-packages/WP26-model-changes.md` (new);
  `examples/adcs/model_v2/cubesat.sysml` only as OD1's outcome allows; `examples/adcs/model_v2/views/*` only through
  the generator; `docs/superpowers/notes/spike-sysml-diagrams/project.py` only if a name it reads changed; the model
  tests' pins (`tests/test_model_checking_v2.py`, `tests/test_system_model_v2.py`, `tests/test_system_model_v2_r1.py`,
  `tests/test_mutation_v2.py`, `tests/test_model_coverage.py`), never weakened; `examples/adcs/model_v2/ledger_gate.py`
  only if a gate reads a changed name, or its note under OD1 (b); under OD1 (b) only,
  `examples/adcs/experiments/ledger/ledger.jsonl` (five appended entries) and `examples/adcs/model_v2/views/coverage.md`
  (the model-hash line); the scratch folder `scratchpad/view-editor/wp26/`.
- The UX researcher: `work-packages/WP26-view-editor-feedback.md` and `work-packages/WP26-view-editor-feedback/`
  (the cited screenshots); the scratch folder (its notes only).
- The PM and the driver: `work-packages/WP26-decisions.md`, this file (amendments only).
- Never: the data, the ledger (outside OD1 (b)), the paper, `docs/` pages, `src/`, `derivation/`, `glossary.yaml`,
  `claims_register.toml`, `work-packages/interface-contract.*`.

## Definition of good

- A systems engineer opening the project in the editor sees, without reading the text, the configuration space (what
  a configuration is and which parts it swaps and tunes), the eight traded metrics each marked MoE or MoP, the four
  requirements at the supervisor's values tied to the metrics they read, and the traceability from configuration to
  requirement; the issues panel is empty; every name and `doc` reads plainly and once; elements that do no work are
  gone. The editor's author receives a report that a stranger can act on: what to keep, what to fix, each bug
  reproducible from its steps.

## Definition of good enough

- D-1 (a) is pushed, R-4 holds on screenshots, and R-1, R-2, R-3 hold at its commit.
- The changes list exists with every finding of the round classed (landed, held, gate) and each with its intent; the
  landed entries pass R-6; the held and gate entries are listed for the driver.
- D-2 is pushed with at least the four sections and, if any bug was met, each bug meeting R-7; R-8 and R-9 hold.
- The step log meets R-10 and R-11; the time box R-13 is kept or its overrun stated.
- R-12 holds. Stop there and present to the PM.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

One item for the driver's approval. Each is marked *(default)* where it appears.

- **The two briefs' shape.** Each brief cites this scope and `pm5-rules.md`; names its deliverable, blast radius,
  checks and time box; and names the other agent and the channel (messages through the PM's `SendMessage` names).
  The modeller works in its own worktree from `origin/dev` (with `uv sync --locked`: it runs the model tests); the
  researcher works without syncing (prose only) and commits its own two paths.
- **The milestone cadence.** The modeller messages the researcher and the PM at M0 (the editor open on project
  "cubesat", revision and issues count), M1 (the `view` package applied and the first view rendered), M2 (the
  requirements table and traceability matrix read against the model's `satisfy` and `verify`), M3 (the changes list
  drafted), M4 (units pushed, checks green), and at any bug the moment it is met. The researcher may ask up to three
  short questions per milestone and asks the modeller to reproduce each bug once.
- **The step log's format.** `scratchpad/view-editor/wp26/steps.md`: one row per step: number, time (UTC), action,
  editor state (revision, issues count), screenshot file (`NN-slug.jpg`), expected and observed where they differ.
- **How the model text gets into the editor.** The project already holds the file verbatim (revision 2). A new text
  goes in by the first exploration's chunk recipe (`scratchpad/view-editor/chunk*.js` regenerated from the file,
  joined in the page, set into the source pane, Apply source), or by select-all and paste where the clipboard works;
  each apply is checked by the source pane's character count against `wc -c`. The `view` package goes in as a
  second file of the editor's project if the editor offers one, else appended to the editor's copy only; the
  repository keeps it as its own file.
- **The project name in the editor:** "cubesat" (as it stands).
- **Names and placement:** `views.sysml` beside the model, so `cubesat.sysml`'s bytes (and the ledger's model hash)
  do not move for a view; the changes list `WP26-model-changes.md`; the report's screenshots in
  `work-packages/WP26-view-editor-feedback/`; the decisions heading "Scope gate".
- **What counts as gate class.** Any change the oracle, the coverage table, the generator or the contract reads: a
  calc, a value, a configuration range, a metric or requirement name, a `satisfy` or `verify` relation, the analysis's
  return tuple. A name or `doc` change to anything else is landed or held class.
- **The parse test** of R-4 is added only if the pinned toolkit loads two files together; otherwise the editor's
  issues panel is the check and the changes list says so.

## Open decisions

- **OD1. Whether changes inside `cubesat.sysml` can land in this round** *(raised by the scope's trace check)*. The
  driver's rule lets "a change to docs, names, structure or a `view` package that leaves every output byte-identical"
  land with `experiments verify` at 0 drifts. But `verify` compares the model file's own hash with the five current
  ledger entries (`examples/adcs/experiments/ledger.py`, `verify`: `check(i, "model", e["model_path"],
  e["model_sha256"])`), `tests/test_mutation_v2.py` asserts the same equality, and `views/coverage.md` prints the
  model's hash. So any byte change to `cubesat.sysml`, a `doc` edit included, gives five "model changed" drifts, a
  failing test and a changed coverage table, while every output stays byte-identical. A `view` package in its own file
  avoids this (D-1 (a)). Options: (a) the model file's bytes stay fixed this round; every change inside it is written up
  with its diff in the changes list as held, and lands with the next data-gate regeneration as a later unit on the
  driver's go / (b) in-file changes that leave the outputs byte-identical land this round through one re-run of the
  five ledger entries on the host at the round's end (`ledger_gate.py --host`, entries `@7` with a WP26 note), each
  output's hash required equal to its `@6` hash (a change that moves one is reverted to held); the ledger,
  `ledger_gate.py`'s note and the coverage table's hash line join the blast radius.
