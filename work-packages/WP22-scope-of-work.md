# WP22 — Scope of work: The system model's two views (configuration and assessment in one SysML v2 model)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | The driver's approval under the mandate, quoted verbatim in `work-packages/WP22-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP22-decisions.md`, after `work-packages/WP22-review.md` |

**Header note: the goal is bigger than one package.** The whole goal (every traded metric traced to the model)
needs a modeller loop that settles requirement values the project does not yet have. Breakdown, in order:
**WP22a (this scope)**: the loop's first round, covering every metric whose requirement can be stated from values
already in the project, the structure of the two views, and the guards (equivalence, ledger, toolkit). **WP22b**:
the requirements whose thresholds the supervisor must give (those flagged OD1), with their `satisfy` and `verify`
elements. **WP22c**: `satisfy` for configurations of the trade space (today only `cubesatBaseline` is
satisfied), and model checking claims over ranges tied to the metrics. **WP22d**: swap-over of paper and docs
onto the new model version (the existing swap gate, not this package). Only WP22a is scoped here; the rest is revisited at its acceptance.
Drafted 2026-11-09 from the inputs listed under Purpose and the repository at `dev` (`e89b2bd`).

## Purpose

The supervisor, 2026-11-09, verbatim (`WP15-decisions.md`, last entry): "i think we have a new open package
regarding the system model because we're discussing extending/refactoring/tightening in a manner that makes the
behavioral view with requirements, and measurements (via simulation or model checking in our case) that help us
trace to our metrics back to model. we have 2 views of the model: one on how its configured and one on how its
assessed. two view, the same sysmlv2 model i strongly expect this will require a serious modeler loop to preserve
the results but make the sysmlv2 model a more obvious connection between the configuration variables, the assessed
attributes and metrics we're trading." And: "if necessary we can extend the scope of the sysmlv2 model to be more
explicit about requirements, verification cases. we want to have a clear logical train of reasoning from the sysmlv2
model to the metrics we're trading".

Inputs: `docs/superpowers/notes/system-model-tidy.md`, `WP15-scope-of-work.md`, `WP15-decisions.md`,
`examples/adcs/case-model.md`, `docs/superpowers/notes/opensysml-usage.md`, the spike report "Revision 2" and its gap
list (`docs/superpowers/notes/spike-sysml-diagrams/report.md`), `WP19-backlog.md`, `release-candidate.md`.

## Goals

- G1. One model, `examples/adcs/model_v2/cubesat.sysml`, with two explicit views: configuration (parts, alternatives as
  categorical variables, parameters as continuous variables) and assessment (requirements, verification cases,
  measurements by simulation or model checking).
- G2. The chain configuration variables, assessed attributes, traded metrics is stated in the model's own elements,
  for every metric of the gap list whose requirement needs no new value (slew time, eclipse reserve, power margin,
  energy balance, depth of discharge, settling time), and the model says plainly which metrics are not yet covered.
- G3. Both WP19 diagrams are generated from those elements, with nothing typed in the projection script that the model could state.
- G4. Everything committed is preserved: datasets, committed numbers, the ledger's history.

## Non-goals

- The datasets (`examples/adcs/data/*.csv`), the paper, the docs pages, the dependencies: unchanged.
- Any new requirement value (see OD1): the requirements for pointing error, control effort, total mass and peak slew
  power wait for WP22b.
- The swap of the paper and records onto the new model version; changes to the evaluation itself (physics in `adcs_sim.py`).
- `satisfy` for trade-space configurations and range claims (WP22c); rendering polish and light/dark diagram variants.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | Revised `examples/adcs/model_v2/cubesat.sysml`: requirement defs over the metrics' own quantities, `slewTime` in `SlewMeasurement`, `verify` objectives naming the metric quantities, the two views marked in the model (packages or documented sections) | G1, G2 |
| D-2 | Matching changes to `cubesat_model.py` and its tests (the opensysml client reads the new elements) | G1, G4 |
| D-3 | `docs/superpowers/notes/spike-sysml-diagrams/project.py` revised to derive the metric-to-element table from the model; regenerated two views (`out/`) | G3 |
| D-4 | A new ledger entry recording the model's new version with outputs unchanged | G4 |
| D-5 | An equivalence test (`tests/test_system_model_v2.py` or a sibling) on regenerated designs; `work-packages/WP22-review.md` holding the per-round modeller-loop record and a metric-by-metric trace table | G2, G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every metric in G2 has a model element that relates a requirement to the metric's own quantity or calc, and that relation is read from the model, not from prose | The projection script run on the model: the behavioural view shows a thick line for each, none dashed or prose-only; the metric-by-metric table in `WP22-review.md` names the element |
| R-2 | Each metric in G2 has a `verify` in a verification case (`SlewVerification` or `ConfigurationVerification`) | `uv run pytest tests/test_system_model_v2.py` plus the opensysml client reading the verification cases (a test that lists them) |
| R-3 | A metric without a requirement (the WP22b four) is named as such in the model, in a `doc` on the verification case, so the behavioural view shows it as open rather than silently missing | Inspection of the model and the dashed boxes of the regenerated view |
| R-4 | Every added requirement threshold is an existing config value (for example `environment.maxDepthOfDischarge`, `nominalSlew.horizon`, `c.momentumCapacity`, zero for a margin or balance); none is invented | Review table column "value taken from"; grep of the model diff for numeric literals not already in the base |
| R-5 | Committed datasets and every committed number are unchanged | `git diff --stat main -- examples/adcs/data docs paper` is empty; `uv run pytest tests/test_system_model_v2.py tests/test_cubesat_model.py tests/test_adcs_case.py`; `REQUIRE_OPENSYSML=1` run |
| R-6 | Regenerated designs equal the committed ones to the existing tolerances (same seeds, both gain boxes) | The equivalence test (D-5) |
| R-7 | The ledger records the new model version, outputs unchanged | `PYTHONPATH=examples/adcs uv run python -m experiments verify` passes with the new entry, output hashes equal the previous entry's |
| R-8 | The toolkit gates pass on the new model | `tests/test_model_checking_v2.py` (check, lint, verify --solve), with the pinned binary |
| R-9 | Both views regenerate from the model and change with it | The spike's mutation check re-run on the new model: an added alternative changes only the assembly view; an added requirement changes only the behavioural view; three runs byte-identical |
| R-10 | Each round of the loop ends in a review by a fresh-context modeller against each view's stated intent (the report's intents for images 1 and 2); findings and dispositions recorded | Rounds in `WP22-review.md`, each with reviewer findings and what was done |
| R-11 | Repository gates: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check` | The commands |
| R-12 | The seam is the dataset at the interface contract: the package touches nothing in `src/` and nothing the method reads except through that seam. The supervisor (WP15-decisions.md, last entry): "within reason you should be able to keep the modeling loop bounded away from the core machinery of the hts because tightening the model implementation should not alter the findings about it" | `git diff --stat origin/dev...HEAD` lists no path under `src/`, `derivation/`, `paper/`, or the committed datasets |
| R-13 | A material change of regenerated results against the committed data is a STOP: treated as a probable defect in the earlier model ("if in the process the model cleaning materially alters the results then most likely our earlier versions were buggy"), investigated, and reported to the driver before any other step | the loop's equivalence report is attached to every round; a round with a difference above the existing tolerances halts the loop and is recorded in the decisions file |
| R-14 | The new model replaces the old one only at a recorded gate after a comparison report (the shape of WP16's data gate), never by default ("don't swap the new model in in place of the old model blindly"); until that gate the old model stays what the committed data and the paper cite, and the new one lives beside it | the comparison report exists; `git diff` shows the old model files unchanged before the gate; the gate is recorded in `WP22-decisions.md` |

## Definition of good

- A reader of the model alone can follow, for each traded metric, the line from the configuration variables
  through the measurement or analysis to the requirement and the verification that assesses it, with no prose
  step; the two diagrams then need no analyst's reading beyond the subsystem grouping; the model stays short.

## Definition of good enough

- R-1 to R-11 hold for the G2 metrics; the loop has run at least two rounds and the last found nothing that
  changes a view; the four uncovered metrics are named in the model and in `WP22-review.md` with the value each
  needs (feeding WP22b); the review file carries the trace table. Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- Method: the modeller loop of the supervisor's text, in rounds: model change, toolkit checks, regenerate the two
  views, equivalence test, fresh-context review against each view's intent *(default)*.
- WP22a covers the six metrics that need no new value; the four that do (pointing error, control effort, total
  mass, peak slew power) move to WP22b *(default, a consequence of the threshold rule below)*.
- Threshold rule: thresholds are taken from existing config values (zero for a margin or balance, the 0.3 depth of
  discharge limit, the 600 s horizon, the wheel's momentum capacity); none is invented *(default)*.
- Eclipse reserve, depth of discharge, power margin and energy balance are restated over the metric calcs
  (`EclipseReserve >= 0`, `DepthOfDischarge <= maxDepthOfDischarge`, and so on) as the gap list proposes *(default)*.
- Names of new elements follow the existing style (`<Metric>Requirement`, `baseline<...>`) *(default)*.
- The two views are marked by packages inside the one file, not by two files *(default)*.
- Ledger entry id follows the existing pattern, for example `v2-model-r1` *(default)*.

## Open decisions (for the supervisor)

- **OD1.** Pointing error, control effort, total mass and peak slew power have no value in the project's config to
  bound them, so no threshold can be taken from it. Options: leave those four uncovered in this package and give
  the values at WP22b, or name the values now so WP22a covers them — options: defer to WP22b / state values now
- **OD2.** Slew time is bounded today only by the horizon and the pointing band (`censored == false`); bounding it
  by the existing horizon makes the requirement the same as the settled requirement. Options: accept that
  (the requirement states the slew time is below the horizon) / treat slew time as needing a value too (moves it to WP22b)
