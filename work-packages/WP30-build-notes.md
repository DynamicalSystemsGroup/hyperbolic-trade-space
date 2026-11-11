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
