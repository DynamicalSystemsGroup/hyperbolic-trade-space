# WP30 build notes, stream 3a (the momentum headroom as the ninth traded metric)

Worktree `wp30a`, branch `wp30a` (from `origin/dev` at 3c9e1c1, rebased on eb48f4e). Authority: `WP30-decisions.md`
("Scope gate": OD1 (a), OD2 (a), OD5 (b), OD6 (a)); spike C's `decisions.md` (D-1 (a), D-2 (a), the supervisor's
"Confirm"). The branch is not on `dev`: see "Why the branch is not on dev".

## Units

| Unit | What | Commit |
|---|---|---|
| A | `cubesat.sysml`: calc `MomentumHeadroom` (MoP), returned by `SlewExperiment` as the eighth computed attribute, `MomentumRequirement` restated on it (headroom >= 1), claim `BatteryPeakPowerRequirementHoldsInRange`, header and docs say nine; `views.sysml` count; oracle column (`ATTRIBUTE_NAMES`, units, `OUTPUT_NAMES`, after `dod_eclipse`); model and oracle tests read nine | 7af0925 |
| B | `case.py` spec: nine attributes (unit ratio, orientation +1, group controls: 4 + 4 + 1), baseline record 6.437201, doctest (60, 9); `test_case.py` structural pins | e735c15 |
| C | box reasons (D-2 (a)): `coverage.py` `box_reasons`, `project.py` caption, views and coverage regenerated, reason tests with a negative control, `scripts/check.py` map | 036c6ff |

## Decisions inside the stream (each is a choice, not a finding)

- The headroom is `c.momentumCapacity / peakMomentum`, a ratio, strictly positive; `>= 1` is `momentum_ok`
  (the verdicts of `MomentumRequirement` are unchanged: R-1). Column name `momentum_headroom`; it is not the frozen
  helper's `momentum_headroom_nms` (capacity minus peak, N.m.s), which stays in `cubesat_model.py`.
- Placement: last in the return tuple, after `dod_eclipse` in `ATTRIBUTE_NAMES` and `OUTPUT_NAMES`, last in the
  case spec, so no existing column or conditioned column moves.
- The reason (D-2 (a)) is two computed parts. In-range: the solver's verdict on a claim named
  `<Requirement>HoldsInRange` (the power one existed; the battery peak power one is new: 20 W against at most 19.4 W,
  proved, the false variant `tau <= 0.020` violated with a witness, each literal tied to the model in
  `test_battery_peak_power_claim_literals_are_the_models_own_numbers`). Association: Spearman of the requirement's
  quantity (`BOX_QUANTITY`, typed once: available power; battery peak power ratio rebuilt from `battery_wh` and
  `peak_slew_power_w` with the model's rate and housekeeping) with the traded metrics over the feasible designs of each
  regime; one axis at `case.ONE_AXIS` (0.99), tracks at `NEAR_DUPLICATE` (0.95, spike C's near-duplicate rule),
  else not traded. A boxed requirement with neither a claim nor a quantity has no reason, and the test names it.
- The box is the requirements no traded metric's quantity feeds (`coverage.box_requirements`); the view's own box
  (`project.py`, `no_line`) is checked equal to it by a test.

## Evidence

| Check | Result |
|---|---|
| `REQUIRE_OPENSYSML=1 uv run pytest -m "not slow"` on `test_system_model_v2.py`, `_r1.py`, `test_model_checking_v2.py`, `test_cubesat_oracle.py`, `test_model_coverage.py`, `test_diagnostic_pair.py`, `test_check_script.py` | green (87 on the last run of the subset above) |
| `uv run ruff check .`, `uv run ruff format --check .`, `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` | clean; 0 new violations |
| Claim `BatteryPeakPowerRequirementHoldsInRange`, engine `solve` | holds, proved; false variant violated, witnessed |
| Reason numbers against spike C | power: +0.9996 primary, +0.9997 baseline, one axis with the energy balance; battery: +0.9703, +0.9753, tracks the depth of discharge |
| Oracle on the baseline configuration | `momentum_headroom` 6.437201363621915 = 0.030 / 0.00466041037173962; the case record equals it |
| Momentum headroom through the model equals capacity over the measured peak on 5 configurations (frozen comparison) | max relative difference 1.8e-16 |
| Behavioural view rendered (PlantUML, 700 px) and looked at | the headroom in the controls lane with its requirement line; the box holds two requirements; the analysis box reads "returns 8 of 9" |
| Coverage regenerated on the host | the 8 existing columns' empirical magnitudes equal the committed (container) values to the printed digits; 7 disagreements, the same seven cells as before |
| Nine-metric fit on the existing data with the headroom column added in a scratch copy (never committed): `case.fit_study`, `case.k_fits` | tau 38.1 and 45.7 at K = 1 (spike C's values); K = 1, 2, 3 select a temperature in both regimes |

## Held for the data gate (red on this branch by design)

The fast suite on the tip: 18 red, 1739 green. Each red test reads the column that the data of record lacks, the ledger
hash of the model, the contract, the paper, or a generated block:

- ledger and data: `test_experiments::test_committed_ledger_verifies...`, `test_mutation_v2` (three), `test_v2_data`
  (two: ledger verify, check designs regenerate);
- contract: `test_interface_contract::test_r3_v2_traded_metrics_are_the_oracles_attribute_names`;
- paper (reads the study, a table or the committed view copy): nine tests in `test_paper.py`, and
  `test_paper_static_figures::test_model_views_in_the_paper_equal_the_models_views`;
- a generated block: `test_case_model_howto::test_sections_block_is_generated_from_the_model` (the section line ranges
  of `cubesat.sysml` in `examples/adcs/case-model.md`; regenerated with `uv run python tests/test_case_model_howto.py
  --write` after the last edit to `cubesat.sysml`, 3b's too).
- slow, not run in the fast suite: the record-bound numbers in `test_case.py` (K record, contending sets, counts) and
  the K-terms record script, which re-pin on the regenerated data.

## Why the branch is not on dev

Any edit to `cubesat.sysml` changes the model hash the five current ledger entries record, and the oracle's new column
is not in the data of record, so the ledger tests and the committed-values tests cannot be green on `dev` before the
gate regenerates (the scope's own default: "the code and the regenerated data cannot be green apart"). The branch is
pushed as `origin/wp30a`; `wp30b` rebases onto it (the scope's default). Unit A is the `cubesat.sysml` commit.

## Items the gate and the other streams need (outside 3a's files)

- `examples/adcs/k_terms.py` has its own list of eight attributes (`ATTRS`, `SHORT`, `ORIENT`); the K record script and
  `tests/test_k_terms_case.py` (`exponents_.shape == (3, 8)`) read it. The ninth metric enters both at the gate.
- `docs/examples.md` and `examples/adcs/case-model.md` state counts and the sections block (see above).
- `paper/figures/fig-behavioural-view.png` is the paper's copy of `views/behavioural_view.png`; the test that equals them
  is red until the gate copies the new view.
- `experiments/compare.py` needed no change: its richness report reads the attributes the frozen frames and the v2
  frame share (eight); its sentence "eight since the eclipse reserve left the v2 data" stays true of that shared set.
- The contract is at version 17 already (WP31 U3); WP30's amendment is therefore version 18, not 17 as the scope says.
- Any later edit to `cubesat.sysml` changes the sha256 that `coverage.md` names; `uv run python
  examples/adcs/model_v2/coverage.py` regenerates it (about 16 s on the host).

# WP30 build notes, stream 3b (the cost model)

Worktree `wp30b`, branch `wp30b` (from `origin/wp30a` at 79ca1d8). Authority: `WP30-decisions.md` ("Scope gate": OD1 (a),
OD2 (a), OD5 (b), OD6 (a); OD3 and OD4 the supervisor's, placeholders now); spike D's `decisions.md` (A-1, B-2, C-3,
D-1, E-1) and `README.md` sections 3, 4 and 7. The branch is not on `dev` (same reason as 3a).

## Units

| Unit | What | Commit |
|---|---|---|
| A | `cubesat.sysml`: fleet size `fleetSize` (1 to 30), `Prices` and `PricingCurves` parts, calcs `PartTotal`, four single-unit prices, six part totals, `FleetBuildCost`, `FleetCost`, `UnitCost`, analyses `UnitCostExperiment` and `FleetCostExperiment`, `UnitCostRequirement` and `FleetCostRequirement` with placeholder limits, launch rate 7,000, launch budget 105,770; `stakeholders.sysml` (`CostToBuild` a roll-up of `FleetBuildCost`, the two requirements in `lowCost` with satisfy statements); `views.sysml`; the model tests re-pinned | aa73149 |
| B | oracle and sampler: `fleet_size` in `CONFIG_NAMES` (default one satellite), own generator, `unit_cost_usd` and `fleet_cost_usd` in `ATTRIBUTE_NAMES` and `OUTPUT_NAMES`, check-design pool, legacy shared subspace, sensitivity; oracle and sensitivity tests | cba85e5 |
| C | `case.py` (eleven attributes, group cost, `fleet_size` design variable), `coverage.py` and `project.py` (read every analysis, cost subsystem, fleet size a decision element), `scripts/check.py`, `test_case.py`, `test_model_coverage.py` | 433c145 |
| D | `tests/test_cost_model.py` (R-4, R-5, R-6 in code, R-7, a negative control) and `examples/adcs/experiments/cost_form.py` (plain SymPy form check) | 950451c |

## Decisions inside the stream (each is a choice, not a finding)

- **The unit cost is `FleetCost / fleet size`, launch included** (scope G5: "unit cost U = F / n"), and its requirement reads
  that metric (`UnitCostRequirement`: `UnitCost(c) <= budgets.unitCostLimit`), so each requirement reads a traded metric's
  own quantity and the box stays at two. The ladder of spike D's `admit-shares.txt` is on the unit *build* cost (no
  launch); the placeholder 450,000 USD is its top rung read as a unit cost with launch (baseline 443,040 at n = 1). The
  `CostToBuild` roll-up is the build cost per satellite (no launch), the sponsor's illustrative measure.
- **Two analyses for the two cost metrics.** An analysis's result is a unique feature: two equal entries are refused
  ("written at positions 9 and 10 of a unique feature"), and the unit cost equals the fleet cost at one satellite, so
  the pair cannot be returned together (`nonunique` is refused: the redefined feature is unique; only one `return` is
  allowed). `UnitCostExperiment` and `FleetCostExperiment` return one metric each; `SlewExperiment` still returns eight.
  `coverage.py` and `project.py` read all analyses (the slew experiment first); the view's analysis box names the other
  two.
- **`fleet_size` is a configuration variable of the oracle** (last in `CONFIG_NAMES`, so no existing column moves) with the
  default one satellite when a configuration or a design table names none (the named configurations are at one). It is
  drawn from its own stream of each design's child seed (`SeedSequence(child, spawn_key=(1,))`), uniform on the integers
  1 to 30 read from `designRanges`; a test shows every existing column equal to the old sampler's exactly, and design `i`
  independent of the count.
- **Check designs.** The proposal pool draws `fleet_size` from its own generator (the same rule, `SeedSequence(seed,
  spawn_key=(1,))`); the three named candidates stay at one (`Checks.draw` fills it); the predictor's features stay the six
  (the four traded metrics it fits do not include a cost). `make_check_designs.py` (the frozen v1 script) and
  `definitions.CANDIDATES` are unchanged: a test ties them to each other and the frozen script has no fleet.
- **Shares, slopes, prices** are spike D's table (labelled choices in the model's docs); the all-flat and all-strong
  envelopes stay in the spike's record (`economics-output.txt`).
- **Placeholders:** unit cost limit 450,000 USD, fleet cost limit 3,000,000 USD (the baseline at ten satellites, 2,857,334),
  each documented `PLACEHOLDER, not the supervisor's value` in `budgets`; verdict only, not a flag (OD2 (a)); the
  stakeholder layer's satisfy statements for them (agile `not satisfy` unit cost at n = 1) stand until his values.
- **Launch budget 105,770 USD** is the recorded OD4 (a) figure (15.11 kg at 7,000). The supervisor's mass is 15.107 kg
  (90,643 / 6,000), whose price at 7,000 is 105,750; 105,770 uses the rounded mass. `case.py`'s mass threshold follows the
  model (105,770 / 7,000 kg).
- **Test line cap.** `test_every_constant_has_a_doc_rationale` capped the model at 900 lines (898 after 3a); the cost model
  is about 230 lines (mostly the rationale of each price and curve), so the cap is 1,150.
- **Cost group.** `LaunchCost` moves from the mass subsystem to a new cost subsystem in the coverage graph (the scope: "launch
  cost joins it"); total mass stays in mass.

## Evidence

| Check | Result |
|---|---|
| Model values against spike D (R-5): `FleetBuildCost` at the baseline, n = 1, 3, 10, 30 per satellite | 350,000 / 248,464 / 192,693 / 160,910 USD; launch 93,040 USD per satellite at 13.291 kg; compact and agile at one satellite 281,300 and 501,000; unit cost 443,040 / 341,504 / 285,733 / 253,950, fleet cost 443,040 / 1,024,513 / 2,857,334 / 7,618,505 (`test_the_models_prices_are_the_spikes_table`) |
| The model against `economics.py` (loaded without `main()`), 12 sampled designs at n = 1 and 7 | relative difference below 1e-12 on build, mass, fleet and unit cost |
| Monotone, concave, unit cost falls, F = U n, launch linear, n = 1 identity (R-4) | the three named configurations at n = 1, 2, 3, 5, 10, 17, 30; every part and the assembly |
| Plain-SymPy form (`cost_form.py`) | seven statements yes: each total and the fleet and unit cost a posynomial in (n, span, capacity); nondecreasing, concave; unit cost falls; n = 1 identity |
| Negative control | busSlope 1.10 fails "concave" and "unit cost falls" |
| R-6 in code | `fleet_size` integers 1 to 30, all thirty present in 1,000 designs; the other columns equal the old sampler's exactly; the oracle's output differs between n = 1 and n = 30 in the two cost columns only |
| `REQUIRE_OPENSYSML=1 uv run pytest -m "not slow"` on the whole suite | 23 failed, 3 errors, 1,746 passed (3a's tip: 18 red); the 26 are listed below by cause |
| `uv run ruff check .`, `uv run ruff format --check .`, `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` | clean; clean; 0 new violations |
| Behavioural view of the new model rendered (PlantUML) and looked at | the cost group holds the two requirements and the two metrics; the analysis box says "returns 8 of 11 ... An analysis each, no slew: unit cost and fleet cost"; the arrows to the two cost metrics start at that box (the gate regenerates the committed views and looks again) |

## Held for the data gate (red on this branch by design)

The fast suite on the tip: 26 red (3a's 18 plus 8 from 3b), the rest green. By cause:

- **Data of record lacks the columns or the fleet size** (3a's, unchanged in kind): `test_experiments::test_committed_ledger_verifies...`,
  `test_mutation_v2` (three), `test_v2_data` (two), and `test_paper` (nine) read the study or a table; `test_diagnostic_pair`
  (three errors, new in 3b: the case spec's eleven attributes and `fleet_size` against the committed data).
- **Contract:** `test_interface_contract::test_r3_v2_traded_metrics_are_the_oracles_attribute_names` (version 18 names eleven,
  `fleet_size` among the configuration names).
- **Committed generated files** (re-generated at the gate): `test_model_coverage` (three: `coverage.md` and `coverage.csv` name the
  committed model's hash and nine metrics; `coverage.py` rerun, about 16 s on the host, the container's files at the gate),
  `test_system_model_v2_r1` (two: `behavioural_view.*` and `behavioural_caption.md` against the generator),
  `test_paper_static_figures::test_model_views_in_the_paper_equal_the_models_views` (the paper's copy), and
  `test_case_model_howto::test_sections_block_is_generated_from_the_model` (the section line ranges: `uv run python
  tests/test_case_model_howto.py --write` after the last edit to `cubesat.sysml`).
- slow, not run in the fast suite: the record-bound numbers in `test_case.py`, `test_k_terms_case.py` and the K-terms record script.

## Items the gate and the other streams need (outside 3b's files)

- `examples/adcs/k_terms.py`: `ATTRS`, `SHORT`, `ORIENT` now eleven (and the design variables); `tests/test_k_terms_case.py`
  pins `exponents_.shape == (3, 8)`.
- The contract amendment is version 18: eleven traded metrics, `fleet_size` in `config_names` and in the dataset column
  tables (a float column holding integers 1 to 30), the two cost columns after `momentum_headroom`, `case.v2.traded_metrics`.
- The data: every v2 file gains `fleet_size` (after `Kd`), `momentum_headroom`, `unit_cost_usd`, `fleet_cost_usd`; the proposals of
  `v2-check-predictions` now carry a pool-drawn fleet size (a gate choice whether the check designs stay at one satellite:
  `Checks.draw` already fills one for the candidates); the scope-sensitivity ledger entry records a changed `FIXED_V2`
  (`fleet_size: 1.0`).
- `docs/examples.md`, `examples/adcs/case-model.md` (counts, the sections block), the paper cells and tables that state the metric count,
  the launch rate or a cost figure, `glossary.yaml` (fleet size, unit cost, fleet cost, pricing curve, the cost group; an entry
  regenerates Appendix A in the same push), the answer key, the figures.
- `WP30-rounds/cost-ladders.md` (D-6): the pass fractions of the two limits on the regenerated data (per regime and per n for the
  unit cost, across n for the fleet cost); not computable before the data.
- `project.py` wording of the analysis box and the caption for the two cost analyses is the model developer's first
  choice; the gate's reader pass may reword it.

# WP30 build notes, status after the supervisor's values (stages 3a and 3b, before the regeneration)

Branches `wp30a` and `wp30b` rebased onto `origin/dev` 8b5c4f4 (`wp30b` carries `wp30a`; nine WP30 commits over `origin/dev`).
The model, tests and ladder script carry the final values; the data are not regenerated, nothing is on `dev`.

## Values and where they landed

| Value | Where |
|---|---|
| Unit cost limit 350,000 USD per satellite, on the covered cost, at the design's own fleet size | `budgets.unitCostLimit` and `UnitCostRequirement` (`cubesat.sysml`); `lowCost` concern (`stakeholders.sysml`) |
| Fleet cost limit 6,000,000 USD on the covered cost (build and launch, n free 1 to 30); the sponsor's full fleet budget 8,000,000 USD, 2,000,000 the allowance for what is not scoped | `budgets.fleetCostLimit`, `FleetCostRequirement`, the `lowCost` concern |
| Launch 7,000 USD/kg linear; 50 kg minimum slot in the text, not modelled; launch budget 105,770 USD (15.11 kg) | `launchRate` doc, requirement and limit docs; `launchBudget` (the "pending" wording removed) |
| 2026 coefficients (spike D2): panels 340,000 USD/m^2, battery 70 USD/Wh, wheels 4,000 + 2,000,000 USD per N.m (medium 8,000), bus block 80,000 and tracker relation held, assembly 100,000 marked unsourced | `part def Prices` doc (source and date per part), `panelPerArea`, `batteryPerEnergy`, `wheelBase` |
| Coverage statement (included; excluded in the supervisor's order; lower bound; the 12U class note) | the cost model's header doc, both limits' docs, both requirements' docs, the `lowCost` concern |

Choice inside the stream: spike D2 prices one wheel per scenario (8,000 for the baseline's medium wheel) and gives no class
relation; the model keeps its linear relation in the peak torque with the base moved to 4,000 USD (the SpaceWheel30 listing) so the
medium wheel is exactly 8,000, the small 4,600 (the NanoAvionics RW0 listing) and the large 24,000 (the Space Inventor WHL-100
listing is 27,500). The class prices of a small and a large wheel are this relation's, not listings.

Consequences in the model: each of the three named configurations, as a single satellite, is over the unit cost limit
(461,360, 371,455 and 636,380 USD), so `stakeholders.sysml` and `cubesat.sysml` state `not satisfy` for the unit cost on
the baseline and the compact (the agile already was); the baseline's unit cost crosses 350,000 between 3 and 5 satellites
(354,661 at 3, 325,213 at 5); its fleet cost passes 6,000,000 up to 17 satellites (4.72 million) and fails at 25 (6.66 million;
under the 8,000,000 full budget) and 30 (7.84 million). Baseline per satellite, build only, at n = 1, 3, 10, 25, 30: 368,320;
261,621; 202,334; 173,167; 168,259 (spike D2's table).

## Evidence

| Check | Result |
|---|---|
| Repricing in the code against spike D2's table (its own `build()` at the 2026 central scenario, baseline, n = 1, 3, 10, 25, 30) | equal to relative 1e-12; the readout's per-unit figures to the dollar (`tests/test_wp30_cost_ladders.py`) |
| The model's calcs against the repricing, 12 sampled designs at n = 1 and 7 | relative difference below 1e-12 on build, mass, fleet and unit cost (`tests/test_cost_model.py`) |
| The ladder script's price functions | spike D's curves, bus, tracker and assembly with the three 2026 coefficients patched in `load_prices()`; `--no-launch` no longer reproduces spike D's `admit-shares.txt` (that test is replaced by the D2 one) |
| `rg PLACEHOLDER` over the model files, tests and scripts for WP30 | none left (test `test_the_two_cost_limits_are_the_supervisors_values_with_the_coverage_statement` asserts it, the exclusion order, the class note and the 8,000,000 / 2,000,000 relation) |
| `ruff check .` | clean except `work-packages/WP23-rounds/spikes/spike-D2-prices-2026/economics2026.py` (18, a separate unit); `ruff format --check`, `check_vocabulary.py --baseline`: clean |
| Fast suite | see the red set below |

## Stale in the checklist

Steps 8 and 14: the model already carries the values at the regeneration, so there is no "placeholder model" and no second
`--wp30 values` run; the container run is one run (entries `@10`, shared `@9`), and step 11's model edit and neutrality run
reduce to re-reading the ladders and printing the admitted shares for the record. The gate's `WP30_NOTE` (ledger text) now says
the limits are the supervisor's values. The step 10 pass fractions in `WP30-decisions.md` (82 percent, 71 percent, 93 percent)
are on the earlier calibration and are recomputed from the regenerated data. Docs (`docs/examples.md`, `examples/adcs/case-model.md`)
carry no cost sentence yet: the docs statement of the 8,000,000 / 6,000,000 / 2,000,000 relation and the coverage statement
is step 15's.
