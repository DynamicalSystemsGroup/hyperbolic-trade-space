# WP23 — Scope of work: The model-realism loop (configuration space and metric space explicit, the case regenerated once)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP23-decisions.md` |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `work-packages/WP23-decisions.md`, after `work-packages/WP23-review.md` |

**Header note: one package, in rounds, ending at one data gate.** Each round of the modeller loop is bounded: change
the model; regenerate the two datasets (primary and baseline) with event detection (settling time only); re-fit
K = 1 and K = 3 with the fit unchanged; regenerate the diagnostic pair (the K = 1 exponent heatmap across τ and the
behavioural view) with the assembly view and the coverage table; cold read by a P2 and a P3 proxy. After the last
round, one regeneration in the container of record and one data gate. The package absorbs the regeneration step and
the data gate of WP16 Amendment 2 (its D-8 and D-9, and steps (2) and (3) of its order), so the datasets regenerate
once, on this package's model. WP16 keeps its event-detection change (D-7, settling time only, the slew-time path
dropped), which is an input here and lands on `dev` in the same push as this package's regeneration (77844c5: the
code and the regenerated data cannot be green apart). The paper's move onto the new data (WP16 order step (4)) and
the redraw of the figures (WP19) follow this package's gate in their own streams. Size: the goal fits one package
with a round cap; if the loop reaches its cap with a blocking finding open, the natural split is WP23a (the loop:
model, coverage, views, prose) and WP23b (regeneration, data gate, swap), proposed then rather than now.
Drafted 2026-11-09 from the inputs under Purpose and the repository at `dev` (`77844c5`).

## Purpose

The supervisor, 2026-11-09, 20:35, verbatim (`WP22-decisions.md`, "The model-realism loop"): "i have an idea. we can
make mass an explicit metric in our trade since the total mass directly impacts cost to launch into space. i think if
we introduce a cost to launch where lower mass is cheaper and more mass is more expensive we should ensure all the
decision elements were considering effect a least one metric. also i think we should more generally use this chart as
guide to do a loop to tighten up the model so the demonstrative case feels more realistic. the very fact that way the
system is specified and assembed (the other plantuml diagram) and the way that system maps to measurable MoEs and MoPs
which in turn cab be used to populate the data we want to learn trade-offs within is key to show this method is
practically useful for real engineering work not just a toy technique". On whether 0.1 waits: "0.1 waits for it".

At 20:50, reviewing Figure 1's exponent heatmap and the behavioural view together: "reviewing this and this together
it seems pretty clear we need to refine out sysmlv2 model so our trade space actually matches what the model is
trying to accomplish this means a bunch more metrics explicitly included but tied to our actual requirements. / the
whole thing is actually pretty simple: a space of configs on one side (how its constructed) and a space of metrics on
the other (how its evaluated). that clarity is why we wanted a sysmlv2 model in the first place. once thats done we
should see more texture int the grayscale plot attached".

On the time metric (`WP16-decisions.md`, latest): "we want the hold time one but its really the "settling time" in
control laguage"; and, two time metrics or one: "One: settling time".

The need: the case is the paper's evidence that the method serves real engineering work. Today four of the ten traded
metrics have no requirement in the model (control effort, pointing error, peak slew power, total mass), the K = 1
heatmap (`paper/figures/fig-tau-sweep.png`) shows four metrics at zero exponent at every τ (settling time, power
margin, eclipse reserve, peak slew power), and nothing checks that every swap and tune reaches a metric. The outcome:
a model in which the configuration space and the metric space are each explicit and joined by requirements, a case
regenerated once on it, and every moved number explained.

Inputs: the driver's brief (three messages, 2026-11-09), `WP22-decisions.md`, `WP16-decisions.md`,
`WP19-decisions.md`, `WP22-scope-of-work.md` and `WP22-review.md` (the trace table, the gate comparison report),
`WP16-scope-of-work.md` (Amendment 2), `interface-contract.md`, `examples/adcs/case-model.md`,
`examples/adcs/model_v2/cubesat.sysml` and its two views, `docs/superpowers/notes/reader-grid.md`,
`docs/superpowers/notes/figure-review.md`, `release-candidate.md` (step 3f).

## Goals

- G1. **Two spaces explicit.** The configuration space (how the system is constructed: the assembly view's swaps,
  WheelClass and TrackerGrade, and tunes, panelSpan, batteryCapacity, Kp, Kd) and the metric space (how it is
  evaluated: each traded metric named in the model as an MoE or an MoP) are each explicit in the one SysML v2 model.
- G2. **Launch cost on mass.** A launch cost that reads total mass (lower mass cheaper, more mass more expensive) is in
  the model, so mass enters the trade through a stated cost tied to a requirement or MoE (form: OD1; its relation to the
  total-mass column: OD2).
- G3. **Coverage of every decision element.** Every swap and tune affects at least one traded metric, shown by a
  coverage table generated from the model and checked by a test.
- G4. **Every traded metric tied to a requirement or a stated MoE.** The four uncovered today (control effort, pointing
  error, peak slew power, total mass) get a requirement with a threshold the supervisor gives, or are stated in the
  model as an MoE with no bound (OD3 to OD6); this absorbs WP22b.
- G5. **One time metric.** The settling time (the hold time: the first time after which the pointing error stays inside
  the band, computed by event detection as the last exit) is the case's only time metric; slew time leaves the traded
  metrics and the dataset; `SlewTimeRequirement` folds into `SettledRequirement`; `SlewExperiment`'s outputs and the
  measurement change accordingly; the interface contract is amended for the column change and the launch-cost column.
- G6. **The modeller loop with the diagnostic pair.** Rounds as in the header note, the heatmap and the behavioural view
  read together each round, until the stopping rule of good enough.
- G7. **The case prose in discipline language.** `case-model.md` states the chain assembly → MoEs and MoPs → dataset,
  each metric's definition in its discipline's language (control, power, mass, cost), MoEs and MoPs named as such; the
  heatmap's "more texture" stated there as a hypothesis the regenerated figure checks.
- G8. **One regeneration and the data gate.** After the loop, the datasets, the K = 1, 2, 3 record and the check designs
  regenerate once, with WP16's event detection, in the container of record; the comparison lists every moved number and
  every changed conclusion with its cause; the model and data swap is made at that gate, never blindly.

## Non-goals

- The core machinery: nothing under `src/`, `derivation/`, and no change to the fit (the supervisor, WP15: "within
  reason you should be able to keep the modeling loop bounded away from the core machinery of the hts"). Model, fit and
  analysis stay apart: the model changes, the fit runs unchanged, the analysis reads the result.
- No blind swap: the revised model and its data replace the adopted ones only at the recorded data gate ("don't swap
  the new model in in place of the old model blindly").
- No tuning the model to a figure. "More texture" in the heatmap is a hypothesis checked after the loop, never a target;
  a metric left at zero exponent is explained in the record and the prose (a legitimate reading, the n-lemma), not
  engineered away. No metric, threshold or constant is chosen because it moves the heatmap.
- No invented threshold: the values WP22b left to the supervisor are open decisions here (OD3 to OD6), not agent's
  values; an uncovered metric with no value given is stated as an MoE with no bound, never bounded by a guess.
- The paper and the docs pages: no prose, figure or number in `paper/` or `docs/` is edited here (the container
  record `paper/container/RECORD.md` and the views generator under `docs/superpowers/notes/` are the only files there
  it touches). The paper's move onto
  the new data, the regeneration of its numbers in the container and the redraw of its figures follow the gate (WP16
  order step (4), WP19); WP19's stage-1 decisions on slot purposes stand. This package hands over the list of slots
  whose axis or metric set changes (G5, OD2).
- The frozen data (`examples/adcs/data/*.csv`) and the paper's current case code paths that read it (`k_terms.py`,
  `case.py` constants): unchanged until the paper stream's swap.
- The physics of the simulator beyond what WP16 D-7 changes; sampling, seeds, scenario constants.
- `satisfy` over trade-space configurations and range claims tied to metrics (WP22c); the trade-off-aware search
  (after 0.1).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The model revision `examples/adcs/model_v2/cubesat_r2.sysml` *(default name)* beside the adopted `cubesat.sysml` until the gate, then `cubesat.sysml` (the old file in history only, as at WP22d): launch cost calc and its requirement or MoE; MoE/MoP marking of every traded metric; requirements or stated MoEs for the four; slew time removed, `SlewTimeRequirement` folded into `SettledRequirement`; the measurement and `SlewExperiment` returning the new metric set; the inputs the simulator reads stated on the measurement | G1, G2, G4, G5 |
| D-2 | The coverage table, generated from the model: `examples/adcs/model_v2/coverage.py` writing `examples/adcs/model_v2/views/coverage.md` and `coverage.csv` *(default paths)*, two tables (decision element × traded metric; traded metric → MoE/MoP, requirement or stated MoE, verification), with `tests/test_model_coverage.py` | G1, G3, G4 |
| D-3 | The case-code and test changes the column change needs: `cubesat_model.py`, `experiments/cubesat_oracle.py`, `experiments/definitions.py`, `experiments/compare.py`, `generate_dataset.py`, `make_check_designs.py`, and the tests that pin the model or the v2 columns | G2, G5 |
| D-4 | The interface-contract amendment: `work-packages/interface-contract.md` and `.toml` (the v2 datasets' headers pinned, slew-time columns out, the launch-cost column in, the traded-metric list of the v2 data; `contract_version` + 1) | G5 |
| D-5 | The two views regenerated from the model by `docs/superpowers/notes/spike-sysml-diagrams/project.py` (revised to draw MoE/MoP and launch cost), committed at the gate in `examples/adcs/model_v2/views/` | G1, G6 |
| D-6 | The diagnostic pair per round, with the assembly view and the coverage table: `work-packages/WP23-rounds/round-N/` (`heatmap.png`, `behavioural_view.png`, `assembly_view.png`, `coverage.md`, `k3_record.md`) generated by `examples/adcs/model_v2/diagnostic_pair.py` *(default paths)* | G6 |
| D-7 | The case-construction prose in `examples/adcs/case-model.md` (a section stating the chain, the MoEs and MoPs, the launch cost, the settling time, the texture hypothesis and its outcome), and glossary entries in `glossary.yaml` for the terms it introduces (MoE, MoP, launch cost) | G7 |
| D-8 | The regeneration record: new ledger entries (`<id>@<n>`, clean tree, commit, platform, image id) and `examples/adcs/data/v2/*`, the K = 1, 2, 3 record, the check designs, `paper/container/RECORD.md` and `tests/data/v2_first_designs_of_record.csv`, regenerated once in `hts-paper` | G8 |
| D-9 | The data-gate comparison, a new section of `work-packages/swap-evidence.md` *(default)*: old v2 against new, every moved number with size and cause, each conclusion (contending sets, leading metrics, tension signs, selected τ, certificates, check outcomes, counts, flags) identical or changed with its cause; the list of paper and docs slots whose axis or metric set changes | G8 |
| D-10 | The review record `work-packages/WP23-review.md`: per round the model change, the pair, the cold reads verbatim with findings and dispositions, the K = 1 and K = 3 readings; the trace table updated from WP22's; the texture hypothesis's outcome with each remaining zero exponent explained | G6, G7, G8 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Every decision element of the assembly view (two swaps, four tunes) has a non-empty row in the coverage table: at least one traded metric reached by a model path, and the empirical effect agrees | `uv run pytest tests/test_model_coverage.py` (no empty row; the committed table equals a fresh generation); inspection of `coverage.md` |
| R-2 | Every traded metric has, in the model, a requirement that reads its own quantity with a `verify` in a verification case, or a `doc` stating it as an MoE with no bound; each is marked MoE or MoP | the same test reading the model through the opensysml client; the behavioural view shows no dashed "no requirement" box |
| R-3 | Every threshold in the model is either an existing config value (WP22's R-4 rule) or a value the supervisor gave in `WP23-decisions.md` | review-table column "value taken from"; grep of the model diff for numeric literals, each traced |
| R-4 | Launch cost is a calc of total mass in the model, increasing in mass, in the form OD1 decides, and its constant(s) are labelled as the model labels its other constants (illustrative or cited) | inspection of the calc; a test that the calc increases with mass at the three named configurations; any cited figure has a verified source |
| R-5 | Slew time is gone from the traded metrics, the dataset, the measurement and the requirements; `SettledRequirement` carries the fold; the settling time is the event-detected last exit | `grep -rn "slew_time\|SlewTime" examples/adcs/model_v2/cubesat.sysml examples/adcs/data/v2` returns nothing; `grep` of `experiments/` and `cubesat_model.py` finds no slew-time output; WP16 D-7's tests pass |
| R-6 | The contract and the data agree: the v2 headers equal the manifest; the amendment row names the change, the side affected and the approval | `uv run pytest tests/test_interface_contract.py tests/test_v2_data.py` |
| R-7 | The seam holds: no path under `src/` or `derivation/`, no file in `paper/` other than `paper/container/RECORD.md`, no file in `docs/` other than the views generator, no frozen data file | `git diff --stat <start>...HEAD` at the gate |
| R-8 | Each round regenerates the pair from committed code and the round's data, re-fits K = 1 and K = 3 with the fit unchanged, and is cold read: a P2 and a P3 proxy, image first then caption, findings verbatim, against each view's stated intent and the figure review's five tests and its idiom principle | the round folders in D-6; the rounds in `WP23-review.md` |
| R-9 | The texture hypothesis is checked, not targeted: the review records the heatmap before and after, and every metric still at zero exponent across τ has a stated reason (which facet, which lemma or data property) | `WP23-review.md`, "Texture"; the case prose |
| R-10 | The views and the coverage table regenerate from the model and change with it; three runs are byte-identical | the existing views test, extended to the coverage table |
| R-11 | The toolkit gates pass on the revised model (strict load, check, lint, `verify --solve` with no violated row) | `REQUIRE_OPENSYSML=1 uv run pytest tests/test_model_checking_v2.py tests/test_system_model_v2.py` with the pinned binary |
| R-12 | The regeneration runs once, in `hts-paper`, after the last round; the ledger has the new entries, none dirty, `verify` reports 0 drifts | `PYTHONPATH=examples/adcs uv run python -m experiments verify`; `RECORD.md` names the image id |
| R-13 | The data gate lists every moved number and every changed conclusion with its cause; a changed conclusion is interrogated and resolved or brought to the driver with the record (the supervisor: "i do expect changes of this order of complexity due to the sysmlv2 model refactor ... focus on ensuring the integrity of the process"; "interrogate and resolve if possible, escalate to me only once there is no path forward") | D-9 read item by item by the driver; the gate decision in `WP23-decisions.md` |
| R-14 | The case prose states the chain assembly → MoEs and MoPs → dataset, each metric in its discipline's words; every term is the glossary's; every claim is backed | `uv run python scripts/check_vocabulary.py`; the claims register reading of `docs/superpowers/notes/claims-review.md` over the new section |
| R-15 | Repository gates: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, on this machine and on a Linux dispatch at the gate | the commands; the dispatch run |

## Blast radius

The files this package may change; anything else is a stop and a question to the PM.

- Model and views: `examples/adcs/model_v2/` (`cubesat_r2.sysml`, then `cubesat.sysml` at the gate; `coverage.py`,
  `diagnostic_pair.py`, `views/*`, `ledger_swap.py` or its successor); `docs/superpowers/notes/spike-sysml-diagrams/project.py`.
- Case code for the column change: `examples/adcs/cubesat_model.py`, `generate_dataset.py`, `make_check_designs.py`,
  `examples/adcs/experiments/{cubesat_oracle,definitions,compare}.py`, `examples/adcs/experiments/reports/*`,
  `examples/adcs/experiments/ledger/ledger.jsonl`; WP16 D-7's files (`adcs_sim.py`, the oracle's read-off) only as
  WP16 delivers them, landed in the same push.
- Data: `examples/adcs/data/v2/*`; `tests/data/v2_first_designs_of_record.csv`; `paper/container/RECORD.md`.
- Tests: `tests/test_model_coverage.py` (new), `test_system_model_v2.py`, `test_system_model_v2_r1.py`,
  `test_model_checking_v2.py`, `test_mutation_v2.py`, `test_cubesat_oracle.py`, `test_cubesat_model.py`,
  `test_v2_data.py`, `test_case_model_howto.py`, `test_interface_contract.py` (re-pinned only as the amendment says);
  `scripts/check.py` (the path-to-test map).
- Prose and records: `examples/adcs/case-model.md`, `glossary.yaml` (new entries only),
  `work-packages/interface-contract.{md,toml}`, `work-packages/swap-evidence.md` (new section),
  `work-packages/WP23-{review,decisions}.md`, `work-packages/WP23-rounds/`.
- Never: `src/`, `derivation/`, `paper/` (but `RECORD.md`), `docs/` pages, `examples/adcs/data/*.csv` (frozen),
  `examples/adcs/k_terms.py`, `examples/adcs/case.py`.

## Definition of good

- A systems engineer reading the model alone sees the configuration space on one side and the metric space on the
  other, every metric an MoE or MoP in its discipline's language and tied to a requirement or a stated purpose, every
  swap and tune reaching a metric, and launch cost making mass a real trade; the case reads as real engineering work,
  not a toy; the regenerated heatmap shows the trade space the model intends, whatever texture that turns out to have,
  and every number that moved is explained.

## Definition of good enough

- The coverage table is complete: six decision-element rows, none empty, the test passing (R-1, R-10).
- Every traded metric has its requirement or its MoE named in the model, and the behavioural view has no dashed
  "no requirement" box (R-2, R-3, R-4).
- Slew time is out and the fold is made; the contract is amended and its test passes (R-5, R-6).
- The loop ran at least two rounds *(default)*; the last round's P2 and P3 cold reads of both views found nothing that blocks and
  nothing that changes a view, or the round cap was reached and each open finding has a disposition.
- The outputs were regenerated once with WP16's event detection in `hts-paper` (R-12), and the data-gate comparison
  lists every moved number with its cause and every changed conclusion resolved or brought to the driver (R-13).
- The texture hypothesis's outcome and each remaining zero exponent are explained in the review and the prose (R-9).
- R-7, R-11, R-14, R-15 hold. Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

- File names and paths: `cubesat_r2.sysml` beside the adopted model until the gate; `coverage.py`, `coverage.md`,
  `coverage.csv`, `diagnostic_pair.py`, `work-packages/WP23-rounds/round-N/`; data gate as a new section of
  `swap-evidence.md` (as WP16 Amendment 2's default) *(default)*.
- Rounds: at least two (as WP22's good enough), at most four; a fifth only with the driver's call recorded *(default)*.
- Persona pairs: P2 practitioner at L-B and P3 modeller at L-C (`reader-grid.md`), two fresh contexts per round, never
  reused across rounds; image first, then caption; the intent written before the read *(default)*.
- How the coverage table is computed: the structural column by walking the model through the opensysml client from
  each traded metric (the analysis's return entry, the measurement attribute, the launch-cost calc) back through calc
  parameters and the measurement's stated inputs to the configuration features; the empirical column by a one-at-a-time
  change of each decision element at the three named configurations through the oracle, an effect counted when the
  metric moves beyond rounding (relative 1e-9); a disagreement between the columns is a finding *(default)*.
- How the pair is regenerated: each round's two datasets generated on the host with the event-detection change from
  WP16's branch; the K = 1 heatmap across τ and the K = 3 record from the existing `k_terms`/`case` functions, called
  with the round's metric list read from the coverage table, no change to the fit or its defaults; views by
  `project.py`; only the final regeneration runs in `hts-paper` *(default)*.
- MoE/MoP marking in the model by a `doc` tag or metadata on each metric's element, whichever the toolkit reads; the
  classification of each metric proposed by the modeller and read by the P2 proxy *(default)*.
- `SlewBandRequirement` (the band never entered) folds with `SlewTimeRequirement` into `SettledRequirement` if its
  quantity leaves the measurement; `slew_time_05deg_s` leaves the dataset with the slew-time path *(default)*.
- Launch-cost column name `launch_cost` with its unit in the contract *(default; the form is OD1)*.
- Contract amendment approval recorded by the driver under the mandate, as amendments 7 to 10 were *(default)*.
- New element names follow the model's style (`<Metric>Requirement`, `baseline<...>`); ledger ids `<id>@<n>` *(default)*.

## Open decisions (for the supervisor)

- **OD1. The form of the launch cost.** Options: a dollar figure per kilogram, labelled illustrative like the model's
  other constants / a dollar figure per kilogram from a cited published price (a verified source) / a dimensionless
  mass cost (mass over a stated reference mass).
- **OD2. Launch cost and the total-mass column.** A cost that only scales mass never trades against mass: in the log
  metrics the fit reads, cost proportional to mass is the same column shifted. Options: launch cost replaces total mass
  as the traded metric (mass stays the attribute it reads) / total mass stays the traded metric and launch cost is the
  MoE the model ties it to (no new column) / both are traded columns.
- **OD3. Pointing error.** Options: a requirement threshold, value given by him (an angle) / a stated MoE with no bound.
- **OD4. Control effort.** Options: a requirement threshold, value given by him (N.m.s) / a stated MoE with no bound.
- **OD5. Peak slew power.** Options: a requirement threshold, value given by him (W) / a stated MoE with no bound.
- **OD6. Total mass or launch cost (whichever OD2 makes traded).** Options: a requirement threshold, value given by him
  (kg or the cost unit) / a stated MoE with no bound.
- **OD7. Metrics beyond the ten less slew time plus launch cost.** Options: none beyond them / he names them / the loop
  proposes candidates the model already computes, each added only on his decision at the gate.
- **OD8. The Agent's defaults list**, approved or changed as one item.
