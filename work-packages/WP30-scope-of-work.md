# WP30 — Scope of work: Track B, the model revision (momentum headroom as the ninth traded metric; the fleet-size variable and the cost model)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` when the driver judges it merits CI |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`, "The mandate"), quoted verbatim in `work-packages/WP30-decisions.md`, section "Scope gate" *(default heading)* |
| **Acceptance record** | The driver's acceptance under the mandate, quoted verbatim in `work-packages/WP30-decisions.md`, after `work-packages/WP30-review.md`; the changed conclusion and the two cost limits are listed for the supervisor's review with it |

**Header note: one package, six stages, one data gate.** Drafted 2026-11-10 (night) from `origin/dev` at a2d25f9 for the
eighth PM. It is Track B of the driver's plan (`driver-log.md`; `PM-BRIEF.md`, "Bigger candidate edits run the full
lifecycle"): the model revision the supervisor asked for twice, once on the behavioural view's box ("my recommendation is
keep but also use it as view ensure our model and our study are well matched ... a modeler research spike then a model
developer to refine the model", `WP23-rounds/spikes/spike-C-requirements-no-traded-metric/decisions.md`) and once on the
cost-to-build budget (H-2, `WP27-decisions.md`, quoted in Purpose). The two changes share one data gate, one container
re-run, one answer-key version and one cascade review, as the driver ruled ("D-1 (a), executed inside Track B"). Stages
(1) and (2) are done; this scope covers (3) to (6).

**The six stages and their owners.**

| Stage | What | Owner | State |
|---|---|---|---|
| (1) Research spike | Spike C (the three requirements) and spike D (commercial CubeSat economics); readouts with plain options, no change to the product | modeller research agents | done: `WP23-rounds/spikes/spike-C-requirements-no-traded-metric/`, `spike-D-cubesat-economics/` |
| (2) Decide | The driver decides what to build; the supervisor where it is his | driver, supervisor | done for both parts: C `decisions.md` (D-1 (a), D-2 (a), the supervisor's "Confirm" of 2026-11-10, 23:15); D `decisions.md` (A-1, B-2, C-3, D-1, E-1, 23:50). Open: the values (OD2, OD3) |
| (3a) Build, momentum headroom | The model calc, the oracle column, `case.py`'s spec, the tests that pin eight, the view, the box's computed reasons | one model-developer agent, own worktree `wp30a` | starts on approval of this scope |
| (3b) Build, cost model | The fleet-size variable, per-part pricing curves, the two pricing metrics, the requirements with placeholder limits | one model-developer agent, own worktree `wp30b`, sequenced after (3a)'s model commit lands | starts when (3a)'s `cubesat.sysml` commit is on `dev` |
| (4) Quality control | Tests, lemma-style checks, cold reads of the model and the views as the content demands | reviewer agents, fresh (not the builders) | after both builds |
| (5) Integrate: the data gate | Regeneration, contract amendment, container re-run, answer-key version, paper and docs numbers, figures, behavioural view, stakeholder layer | PM streams and the driver, in the order of D-9 | after (4); nothing in it starts before both builds are accepted into QC |
| (6) Review the cascade | Every number, figure and sentence the change moves is found and resolved; the acceptance review runs the thing; a cold read of the changed conclusion | a reviewer that runs the checks; the driver accepts | after (5) |

## Purpose

Two supervisor requests, one model revision.

1. **The box.** The supervisor on the paper's Figure 3, the behavioural view, whose box "requirements that read no
   traded metric" holds `BatteryPeakPowerRequirement`, `MomentumRequirement` and `PowerRequirement`, verbatim: "this one
   brings to mind a modeling question. why are these requirements not related to metrics. my intuition is that these
   metrics should be in the trade and should into the existing groupings. my recommendation is keep but also use it as
   view ensure our model and our study are well matched." Spike C found two of the three already traded under another
   name (available power is one axis with the energy balance, Spearman +0.9996 / +0.9997; the battery peak power ratio
   tracks the depth of discharge, +0.970 / +0.975, and takes exponent 0) and one missing: the momentum headroom (wheel
   momentum capacity over the slew's peak momentum). The driver ruled D-1 (a): it becomes the ninth traded metric (an
   MoP, group controls); D-2 (a): the box names each requirement's computed reason, with a test. The supervisor confirmed
   the change of conclusion it brings: the baseline regime's leading trade moves from control effort against settling
   time to momentum headroom, total mass and settling time. His word, verbatim: "Confirm".
2. **The cost model.** The supervisor on H-2, verbatim (`WP27-decisions.md`): "add one but do a research spike on
   commercial space economics so we can calibrate this to read data. it doesn't need to be perfect priced to speak but
   the ballpark for parts, assembly and launch costs need to be sane to a professional familiar with the economics of
   cube sats. its worth noting that cubesats are usually fleets so you may want to incorporate a config variable number
   of satellites in the fleet and a cost model that accounts for diminishing unit costs but increasing total cost for
   more satellite ... we are still pricing per unit though so we do not want to over complicate the model by making it
   a model of the fleet. that would also require us to start looking at the communication range and fidelity and
   networking which we don't want to do. this is still a demonstrative model. i think it suffices to simply clearly
   denote that we're looking at the manufacturing and launch costs of a fleet, there are 2 pricing metrics one for fleet
   cost at unit cost times number of units and one which is unit cost. all of the part then get their own pricing curves
   as a function of number but they can be different curves ... all costs need to have a fixed base cost plus a curve.
   total cost for any part (and total cost for assembly) is offset (fixed cost) + a discount applied as a falling unit
   cost and units go up. total cost in growing in units but at a decreasing rate." The driver's decisions on spike D's
   options: A-1 Wright cumulative-average curves with a fixed share and a slope per part; B-2 fleet size 1 to 30; C-3
   both pricing metrics carry a requirement (a unit build cost limit read at the configuration's own n; a fleet cost
   limit, build and launch, with n free), values the supervisor's, chosen from pass-fraction ladders, build with
   placeholders; D-1 launch at 7,000 USD/kg with the 50 kg slot as a note, his launch budget restated at the same mass
   (15.11 kg, 105,770 USD) pending his confirmation; E-1 tracker 150,000, panels 250,000 USD/m^2, battery 150 USD/Wh,
   assembly, integration and test 100,000 USD with its curve.

The outcome: the model and the study agree on what the system is traded on, the case prices a fleet of identical
satellites per unit with ballpark-sane parts, assembly and launch, and every number and sentence downstream that the
change moves is regenerated or rewritten at one gate.

## Goals

- G1. **The momentum headroom is the ninth traded metric.** A `MomentumHeadroom` calc (capacity over peak momentum)
  marked MoP in its `doc`, returned by `SlewExperiment`; `MomentumRequirement` restated on it (>= 1); the oracle column,
  `case.py`'s spec (nine attributes, units, orientation, subsystem group controls) and the pinned lists follow.
- G2. **The box is a check.** Each requirement in the behavioural view's box carries its computed reason (holds at every
  in-range configuration; one axis with a named traded metric and its Spearman; not traded) in the caption, the coverage
  generator prints the same reason from the same computation, and a test fails on a requirement in the box with no
  stated reason (D-2 (a)). With the momentum requirement now reading a traded metric, the box holds the other two.
- G3. **A fleet-size configuration variable.** `n`, 1 to 30, real-valued in the model and read as a count; sampled with
  the configuration; the three named configurations at n = 1. The model prices a fleet per unit and states, where it
  states its scope, that it covers the manufacturing and launch costs of a fleet and nothing of the fleet's
  communication, range or networking.
- G4. **Per-part pricing curves with a fixed base.** total_p(n; x) = u_p(x) [f_p + (1 - f_p) n^(1 - b_p)], b_p = -log2(s_p),
  for the bus block, panels, battery, wheels, star tracker and a new assembly, integration and test line; shares f_p and
  slopes s_p as spike D's section 3 table (labelled as choices, not findings); the coefficient updates of E-1; launch
  linear in n at 7,000 USD/kg times the total mass (D-1). Every term stays a posynomial in (n, x) (spike D, section 7).
- G5. **Two pricing metrics, each with a requirement.** Fleet cost F(n, x) = sum of part totals + assembly + launch, and
  unit cost U = F / n, as the supervisor's pair; each carries a requirement (C-3): a unit build cost limit read at the
  configuration's own n, and a fleet cost limit with n free. The limits are the supervisor's values, placeholders in the
  build and fixed at the data gate (OD2, OD3).
- G6. **One data gate.** After both builds and their quality control, the datasets, the K = 1, 2, 3 record, the check
  designs and the sensitivity record regenerate once on the host; the data-gate comparison lists every moved number
  and every changed conclusion with its cause; the contract, the key, the paper, the docs, the register, the figures
  and the views follow at the gate and nowhere before.
- G7. **The cascade is closed.** Stage (6): every place that states the metric count, the baseline regime's leading
  trade, a cost figure, or reads a moved number is found, resolved or recorded, and the acceptance review runs the
  thing and cold-reads the changed conclusion.

## Non-goals

- No model of the fleet. No communications, range, fidelity or networking (the supervisor, H-2). The model prices per
  unit; the fleet enters only as the variable `n` and the fleet cost metric.
- No integer fleet sizes in the optimisation, no 50 kg minimum launch slot as a limit or a `max(.)` (it is a note in the
  view, D-1), no broker fee, no communications hardware cost line, no cost of the payload.
- The power requirement's available power and the battery peak power ratio are not traded (spike C D-1 (a)): they stay
  requirements, and the box names why (G2). No other quantity is added to the trade.
- No change to the core machinery: nothing under `src/` or `derivation/`; the fit runs unchanged on nine (or eleven, OD1)
  columns (the supervisor, WP15: "within reason you should be able to keep the modeling loop bounded away from the core
  machinery of the hts"). A change to the sklearn estimator's contract is a stop and a question.
- No tuning of a limit or a curve to a figure: the two cost limits come from pass fractions on the regenerated data and
  are the supervisor's choice; the curve shares and slopes are spike D's, changed only by a recorded decision.
- No blind swap: the revised model and its data replace the adopted ones only at the recorded data gate (WP23's rule).
- No new simulator physics, scenario constants or sampling of the existing configuration variables; the existing
  columns of the same design ids stay as they are (R-6).
- The noise result (Track A), the figure loop, WP8b, and the subtraction pass (WP28) are separate.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | (3a) The model change in `examples/adcs/model_v2/cubesat.sysml`: the `MomentumHeadroom` calc (MoP), `SlewExperiment` returning it, `MomentumRequirement` restated, the header counts and the docs of sections 5 to 6 | G1 |
| D-2 | (3a) The oracle and case code: the column in `examples/adcs/experiments/cubesat_oracle.py` (`OUTPUT_NAMES`, the return entry), `compare.py`, `examples/adcs/case.py` (the spec: nine attributes, units, orientation, subsystems) | G1 |
| D-3 | (3a) The tests that pin eight, re-pinned to nine by the recorded decision: `tests/test_case.py`, `test_cubesat_oracle.py`, `test_k_terms_case.py`, `test_model_coverage.py`, and the v2 model tests; each change cites D-1 (a) in its commit message | G1 |
| D-4 | (3a) The behavioural view and caption with each requirement's computed reason, `model_v2/coverage.py` printing the same reason, the generator `docs/superpowers/notes/spike-sysml-diagrams/project.py`, and a test that fails on a boxed requirement with no reason | G2 |
| D-5 | (3b) The cost model: `n` in the design space and the model (`examples/adcs/design_space.py`, `generate_dataset.py`, `make_check_designs.py`, `cubesat.sysml`); `stakeholders.sysml`'s `unitCosts` and `CostToBuild` replaced by the per-part curves with the E-1 coefficients and the assembly line; the launch rate 7,000; the fleet cost and unit cost calcs; the two requirements with placeholder limits | G3, G4, G5 |
| D-6 | (3b) The ladders: for the unit build cost limit (read at the configuration's own n) and the fleet cost limit, the share of the feasible designs each candidate value admits, per regime and across n, computed on the regenerated data and written as `WP30-rounds/cost-ladders.md` *(default path)*, for the supervisor's pick | G5 |
| D-7 | (4) The quality-control record `work-packages/WP30-qc.md` *(default)*: tests and checks run, the cold reads of the model and views, findings and dispositions | G1 to G5 |
| D-8 | (5) The data-gate comparison, a new section of `work-packages/swap-evidence.md`: old v2 against new, every moved number with its size and cause, each conclusion identical or changed (contending sets, leading metrics, tension signs, selected tau, certificates, check outcomes, counts, flags), and the list of paper, docs and register slots that move | G6 |
| D-9 | (5) The regenerated data of record (`examples/adcs/data/v2/*`, `tests/data/v2_first_designs_of_record.csv`), the K record, the sensitivity record and the ledger entries (`examples/adcs/experiments/ledger/ledger.jsonl`, `model_v2/ledger_gate.py`), `paper/container/RECORD.md` after the container regression | G6 |
| D-10 | (5) The contract amendment (version 17): the new column, the traded metrics, `n`, the pricing metrics, any renamed pinned fact; the manifest and its document in one commit | G6 |
| D-11 | (5) The answer-key version 5, held outside the repository, its hash committed first (`WP11-decisions.md`'s rule) | G6, G7 |
| D-12 | (5) The paper and docs: numbers, tables and figures regenerated; the sentences that state the count, the baseline regime's trade and the cost figures rewritten; `length_ledger.toml`; the register rows; the glossary entries (MoP's short form, the new terms) with Appendix A regenerated in the same push | G6, G7 |
| D-13 | (6) The cascade review `work-packages/WP30-review.md`, with screenshots in `work-packages/WP30-review/`, and the cold read of the changed conclusion | G7 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The momentum headroom is computed by the model, marked MoP, returned by the experiment, present as an oracle column with the model's value, strictly positive on the feasible set, and equal to the inverse of `momentum_utilisation` where both exist | strict load and verify with the pinned toolkit (`REQUIRE_OPENSYSML=1 uv run pytest tests/test_model_checking_v2.py tests/test_system_model_v2.py`); `tests/test_cubesat_oracle.py`; a test that compares the column with capacity over `peak_momentum_nms` |
| R-2 | Every place that pins the traded-metric set agrees: `case.v2.traded_metrics`, `case.py`, the oracle's `OUTPUT_NAMES`, the coverage table, the view, the contract manifest; one count everywhere | `uv run pytest tests/test_case.py tests/test_k_terms_case.py tests/test_model_coverage.py tests/test_interface_contract.py`; the grep of "Where the gate looks" returns no stale count (zero hits for the old counts outside record files) |
| R-3 | The box carries a computed reason per requirement; the generator, the coverage output and the caption print the same reason; a test fails when a boxed requirement has none | `uv run pytest tests/test_model_coverage.py -k reason` *(default test name)*; a planted requirement with no reason fails the test (negative control); the rendered caption looked at (R-14) |
| R-4 | The cost model has the form the supervisor named: for every part and the assembly, total cost is a fixed base plus a falling-unit-cost curve; total cost is nondecreasing and concave in n; unit cost falls in n; fleet cost F = U n; at n = 1 each part total equals its single-unit price relation u_p(x); every term is a posynomial in (n, x) | a test over the calcs at a grid of (n, x): monotonicity, concavity, the n = 1 identity, F = U n to 1e-9; a plain-SymPy script (under `examples/adcs/` or the spike folder, since `derivation/` is not touched) checking the posynomial form of each term |
| R-5 | The cost model is sane to a professional: the baseline configuration's build cost and launch cost at n = 1, 3, 10, 30 reproduce spike D's table (350,000 / 248,464 / 192,693 / 160,910 per unit; launch 93,040 per satellite at 13.291 kg) to the dollar, with the E-1 coefficients and D-1's rate; the figures are cited to spike D's sources | `economics.py`'s printed totals diffed against the model's calcs for the baseline, compact and agile configurations (spike D: 350,000, 281,300, 501,000 at n = 1) |
| R-6 | The existing columns of the same design ids are unchanged by the new column and by `n`: `n` is drawn from its own generator so no existing draw moves; the feasible sets stay 706 and 780 unless a recorded reason says otherwise | at the gate, the old v2 files and the new compared column by column over the existing columns: exact equality (the exact-equality branches, run in the container), differences listed in D-8; counts 706 and 780 read from the flags |
| R-7 | Both pricing metrics exist with a requirement each, and the placeholder limits are marked as placeholders in the model (a comment and `WP30-decisions.md`) until the supervisor's values replace them; no limit is presented as his before he gives it | grep of the model diff for numeric literals, each traced to a source or marked placeholder; the decisions record |
| R-8 | The supervisor's two limit values are chosen from computed ladders: the ladder rows come from the regenerated data of record, per regime and per n (unit cost) and across n (fleet cost), and the values land with his words verbatim in `WP30-decisions.md` | D-6 read against `examples/adcs/data/v2/`; the decisions record |
| R-9 | The data-gate comparison lists every moved number with a cause and every changed conclusion resolved or brought to the driver; the baseline regime's leading trade is reported as the supervisor confirmed it or, if the regenerated data says otherwise, brought to the driver before anything downstream moves | D-8 read item by item; the gate decision in `WP30-decisions.md` |
| R-10 | The exact-equality references are handled by the rule: a host unit re-records only the arrays its change affects, leaves the rest untouched, and marks the file "host-recorded, re-pin at the gate"; the container regression re-pins; no stream pushes anything that regenerates paper outputs or the v2 data while the regression runs | the commit messages; `git diff --stat` of the reference files at each unit; the regression's output in `paper/container/RECORD.md` |
| R-11 | The interface contract is amended, never drifted: version 17, a change-log row with its cause, the manifest and the document in one commit; `tests/test_interface_contract.py` passes with the new pins | `uv run pytest tests/test_interface_contract.py`; `git diff` of the two contract files |
| R-12 | The seam holds: nothing under `src/` or `derivation/`; the frozen CSVs under `examples/adcs/data/*.csv` unchanged; the paper and docs are edited only at the gate and only in the changed numbers and sentences | `git diff --stat <start>...HEAD` against the blast radius |
| R-13 | The cascade is closed: after the gate the greps of "Where the gate looks" show no stale count and no stale conclusion; the claims register holds; the vocabulary check passes; the notebooks execute with no stderr | the greps; `uv run pytest tests/test_claims_register.py tests/test_paper.py tests/test_paper_static_figures.py`; `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml`; `uv run python paper/execute_notebooks.py` |
| R-14 | The reviewer ran the thing: the regenerated behavioural view and caption, Figure 3, the regime figures and the changed pages were looked at in a browser or as images, light and dark where the site has both, with screenshots in `WP30-review/` and a one-line reading of each; the changed conclusion was cold-read by two fresh readers who know no record | the screenshots and lines in D-13; the readers' briefs and returns committed; the PM reads each brief before it is sent |
| R-15 | Repository gates: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, on this machine, and a Linux dispatch at the gate; no AI attribution on any commit or file | the commands; the dispatch run; `git log <start>..HEAD --format=%B` grepped for the CI's whole-word pattern: nothing |

## Blast radius

The files each stream may change; anything else is a stop and a question to the PM. The two builds overlap in
`cubesat.sysml` only, which is why (3b) starts after (3a)'s model commit is on `dev`.

**Stream (3a), worktree `wp30a`.**
- `examples/adcs/model_v2/cubesat.sysml` (the momentum calc, the experiment's return, the requirement, the header);
  `examples/adcs/model_v2/coverage.py`; `examples/adcs/model_v2/views/*` (regenerated); `views.sysml` only if the box's
  reason needs a model element.
- `docs/superpowers/notes/spike-sysml-diagrams/project.py`.
- `examples/adcs/experiments/cubesat_oracle.py`, `compare.py`; `examples/adcs/case.py`.
- Tests: `tests/test_case.py`, `test_cubesat_oracle.py`, `test_k_terms_case.py`, `test_model_coverage.py`,
  `test_system_model_v2.py`, `test_system_model_v2_r1.py`, `test_model_checking_v2.py`, `test_mutation_v2.py`;
  `scripts/check.py` (the path-to-test map).
- Never: `src/`, `derivation/`, `paper/`, `docs/` pages, data files, the contract.

**Stream (3b), worktree `wp30b`.**
- `examples/adcs/model_v2/cubesat.sysml` (after 3a), `stakeholders.sysml` (the cost model), `views.sysml`.
- `examples/adcs/design_space.py`, `generate_dataset.py`, `make_check_designs.py`, `examples/adcs/experiments/definitions.py`
  and `cubesat_oracle.py` (after 3a) for `n` and the two metrics.
- A script and tests for the cost model: `examples/adcs/experiments/` or the spike folder `WP23-rounds/spikes/spike-D-cubesat-economics/`
  for the checks that compare with `economics.py`; `tests/test_cost_model.py` *(default name)*.
- `WP30-rounds/cost-ladders.md`.
- Never: the same list as (3a).

**The data gate (5), the PM's streams in sequence, the driver for the container.**
- Data and records: `examples/adcs/data/v2/*`, `tests/data/v2_first_designs_of_record.csv`, `examples/adcs/experiments/
  ledger/ledger.jsonl`, `model_v2/ledger_gate.py`, `examples/adcs/experiments/reports/*`, `paper/container/RECORD.md`,
  `work-packages/swap-evidence.md`.
- Contract: `work-packages/interface-contract.{md,toml}`, `tests/test_interface_contract.py`.
- Paper and docs: the cells and pages the gate list (below) names; `paper/length_ledger.toml`; `claims_register.toml`;
  `glossary.yaml` and Appendix A; `docs/examples.md`; `examples/adcs/case-model.md`.
- Never: `src/`, `derivation/`.

## Where the gate looks (the cascade list; counts at a2d25f9)

The greps below are the starting list for D-8 and for stage (6); the reviewer re-runs them after the gate and records
the remainder. Counts are matching lines / files, excluding `data/`, build output and `docs/superpowers/` (the notes
there are records and are not edited, except the one generator named in D-4). The patterns are loose on purpose.

| What | Pattern (case-insensitive) | paper | docs pages | tests | examples | register | contract |
|---|---|---|---|---|---|---|---|
| The metric count in words | `eight ... metric`, `metric ... eight`, `eight-metric`, `eight traded` | 7 / 3 | 4 / 1 (`docs/examples.md`) | 7 / 5 | 22 / 8 | 0 | 2 lines (md and toml) |
| The metric count in digits | `8 ... metric` | 5 / 1 | 0 | 0 | 5 / 4 | 0 | 0 |
| The traded-metric list as columns | `dod_eclipse` | 5 / 3 | 0 | 9 / 6 | 47 / 9 | 0 | 7 lines (toml) |
| The old cost model | `CostToBuild`, `cost-to-build` | 0 | 0 | 4 / 1 | 2 / 2 | 0 | 0 |
| The launch rate and the launch budget | `launchRate`, `6,000 USD`, `90,643`, `15.1` | 35 / 4 | 0 | 11 / 4 | 13 / 6 | 2 / 1 | 0 |
| The feasible-set counts (expected to stay) | `706`, `780` | 61 / 5 | 3 / 1 | 14 / 3 | 16 / 4 | 3 / 1 | 1 line (md) |
| The changed conclusion | `control effort ... settling`, `settling ... control effort` | 58 / 4 | 4 / 1 | 5 / 3 | not counted | 3 / 1 | 0 |
| Contending sets and leading trades | `contending`, `leading trade` | 104 / 7 | 30 / 10 | 50 / 8 | not counted | 50 / 1 | 0 |
| The box | `no traded metric`, `read no traded` | 2 / 2 | 0 | 5 / 2 | not counted | 0 | 0 |
| Exponents and K = 1 results | `K = 1`, `exponent` | 506 / 17 | 53 / 9 | 253 / 22 | not counted | 104 / 1 | 0 |

Files by name where the count is small: the word count of the metrics is in `paper/paper.ipynb`,
`paper/supporting_material.ipynb`, `paper/length_ledger.toml`; `docs/examples.md`; `examples/adcs/case-model.md`,
`experiments/compare.py`, `experiments/cubesat_oracle.py`, `experiments/ledger/ledger.jsonl`, `experiments/reports/
change-register.md`, `experiments/reports/sensitivity.json`, `model_v2/cubesat.sysml`, `ledger_gate.py`, `views.sysml`,
`views/behavioural_caption.md`, `views/behavioural_view.puml`, `views/coverage.md`; `tests/test_case.py`,
`test_cubesat_oracle.py`, `test_k_terms_case.py`, `test_model_checking_v2.py`, `test_model_coverage.py`. The
contract's text names `case.v2.traded_metrics` at version 15 and its row 12 says "nine" in history; the amendment
states the number once, from the manifest. The 706 and 780 files that the gate must still confirm are listed by
`grep -rIlE '706|780' paper docs tests examples claims_register.toml` (the list at a2d25f9 includes ten notes under
`docs/superpowers/notes/`, which are records and not edited).

What the gate changes, in kind: the K = 1 exponents, the contending sets, the tension signs, the selected tau, the
certificates and the regime comparison (nine columns, and eleven under OD1 (a)); Figure 3 and the other figures that
draw metrics; the exponent and K tables; Appendices C and D; the sensitivity record; the check designs and their
predictions; the baseline regime's leading trade; the answer key's items that state it; every cost figure in the case
prose; the stakeholder layer's budgets (`CostToBuild`, the launch budget) and the behavioural view.

## Definition of good

- A reader of the model alone sees one trade whose metrics are the ones the requirements read, each requirement tied to
  a traded metric or to a stated reason computed from the model; a professional who knows CubeSat economics reads the
  parts, assembly and launch as plausible, the unit cost falling and the fleet cost rising with n, and the model says
  in one sentence that it prices a fleet per unit; every number and sentence that moved is explained, and the changed
  conclusion reads as the case's finding, not as a patch.

## Definition of good enough

- (3a) lands: R-1, R-2 (model, oracle, case, tests) and R-3 hold; the `wp30a` branch is accepted into QC with the dev
  suite green or the data-reading tests held for the gate by the rule in the defaults.
- (3b) lands: R-4, R-5, R-7 hold; the ladders (D-6) are computed and the supervisor has the rows; or the placeholders are
  marked and the ladders delivered with the gate (OD2).
- The data gate: R-6, R-8 to R-11 hold; the comparison (D-8) is read item by item by the driver; the contract, the key
  version and the container regression are recorded.
- The cascade: R-12 to R-15 hold; the remainder of the greps is empty or listed with a reason; the two cold readers
  find nothing that blocks and nothing that changes a view, or each finding has a disposition.
- Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

Approved or changed as one item at the scope gate.

- Worktree names `wp30a`, `wp30b`; the build streams commit to `dev` as units when the dev suite stays green, but the
  case.py spec, the oracle column and the tests that pin eight land in the same push as the regenerated data (WP23's
  note: "the code and the regenerated data cannot be green apart"); until then they live on `wp30a`'s branch, which
  `wp30b` rebases onto. If the push order is wrong, the PM says so and the units are reordered.
- `n` is drawn from its own seeded generator (uniform on the integers 1 to 30, and kept as a real number in the model)
  so no existing draw moves (spike D, "how n is sampled", unless the sweep shows a reason); the check designs get `n`
  the same way.
- Names: the calcs `MomentumHeadroom`, `FleetCost`, `UnitCost`; the columns `momentum_headroom`, `fleet_size`,
  `unit_cost_usd`, `fleet_cost_usd` *(only if OD1 (a))*; the metric group "cost" beside controls, power and energy,
  and mass (launch cost joins it); the glossary entries; the requirement names. The vocabulary check settles disputes.
- Fixed shares f_p and slopes s_p as spike D's table; the all-flat and all-strong envelopes kept in the record as the
  sensitivity of the choice.
- The launch rate 7,000 USD/kg replaces 6,000 in the model; the 50 kg slot is a `doc` note in the view.
- The test `-k reason` name, `tests/test_cost_model.py`, `WP30-rounds/`, `WP30-qc.md`, `WP30-review.md` and the paths in
  D-6 and D-7.
- The reviewer's fresh readers for the cold read: two Sonnet agents with no repository access (one P1, one P2 of the
  reader grid, `docs/superpowers/notes/reader-grid.md`), shown the changed Section 8 and the regime figure.
- The sequence at the gate: regenerate on the host; D-8; the supervisor's limit values; the contract amendment; the
  container regression and re-pinning (the driver); the key version; the paper and docs numbers; the figures; the
  views; the register; stage (6).
- Model tiers by role (the eighth PM's rule): Sonnet for the builders, the readers and the reviewers; Haiku for the
  greps and counts of the cascade list; no sub-agent without the PM.

## Open decisions (for the driver; the supervisor where it is his)

- **OD1. Are the two pricing metrics traded metrics (columns in the fit) or measures the model computes and the
  requirements read, like the launch cost?** The supervisor said "2 pricing metrics" and spike D says both are "traded or
  budgeted". As traded metrics they are strictly positive, larger-is-better after conditioning, and are two more columns
  (eleven in all); fleet cost = unit cost times n makes the pair, together with `n`, strongly related, and the fit's
  conditioning reads that. Options: (a) both are traded metrics, eleven in all, with columns; (b) both are computed by
  the model and read by the requirements only, nine traded metrics, no columns; (c) unit cost traded, fleet cost
  computed only.
- **OD2. Do the two cost limits enter the feasibility flags or stay verdicts?** The launch budget and the four
  thresholds of WP23 are requirements the verdict reads and do not thin the feasible set (706 and 780 stand). If the
  limits enter the flags, the feasible sets change with the supervisor's values and the regeneration must wait for them
  (the data gate cannot close before his words). Options: (a) verdict-only: the limits do not enter the flags, the sets
  stay 706 and 780, the values can land after the data; (b) both limits enter the flags: the values are fixed before
  the regeneration.
- **OD3. The supervisor's values.** The unit build cost limit, read at the configuration's own n, and the fleet cost
  limit (build and launch, n free), from the pass-fraction ladders (D-6; the first rung is `admit-shares.txt`: at one
  unit 450,000 USD admits 91 percent and 350,000 about 40). Options, at the gate: (a) a value from the ladder that
  the supervisor picks per limit; (b) a limit only on the unit cost, the fleet cost carrying a requirement with a limit
  set from the ladder at a later gate; (c) the spike's unit-cost range of 300,000 to 450,000 USD kept for the build, the
  fleet cost limit left to the ladder. The values are not drafted here.
- **OD4. The restated launch budget (D-1), the supervisor's confirmation pending.** His budget was chosen as a mass of
  15.11 kg (95 percent admitted) and stated in USD at 6,000 USD/kg. Options: (a) 105,770 USD at 7,000 USD/kg, the same
  mass; (b) 90,643 USD kept at the new rate, which is 12.95 kg and admits fewer designs.
- **OD5. When the data gate closes if a cost limit is a placeholder.** Options: (a) the gate waits for the supervisor's
  values, then regenerates once; (b) the gate regenerates with placeholders and the values re-pin the requirement
  afterwards without a second regeneration (valid only under OD2 (a)); (c) the gate regenerates with placeholders and
  a second small regeneration follows the values.
- **OD6. Where the build streams push before the gate.** Options: (a) as the default says: model units to `dev` as they
  stay green, the spec, oracle column and pinned tests together with the data; (b) both streams keep their work on a
  branch `wp30` and one merge to `dev` lands the builds and the data together at the gate.
