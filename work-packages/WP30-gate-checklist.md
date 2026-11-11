# WP30 data gate: checklist

Prepared 2026-11-11 for the PM; revised the same day after the supervisor's values, "No floating requirements" and "Sampling" (items
that these made stale are marked **resolved** or rewritten, not left as they were). Sources: `WP30-scope-of-work.md`
(R-6 to R-15, "Where the gate looks"), `WP30-decisions.md` (OD1 (a), OD2 (a), OD5 (b), OD6 (a); stage 3b questions),
the held branches' `WP30-build-notes.md`, `WP23-decisions.md` (the close-out gate), `WP11-decisions.md` (the key
procedure), `PM-BRIEF.md` ("container is a gate check", "full lifecycle", the eighth PM's item 4). Nothing here
changes a decision; where the scope and the head disagree the head wins (marked **stale**).

Roles: PM = the ninth PM; driver = the driver; impl = one Sonnet implementer in its own worktree under
`scratchpad/pm-worktrees/`; rev = a fresh reviewer. Every command is `uv run ...`; set `MPLCONFIGDIR` under the
scratchpad for anything that draws.

## The supervisor's inputs: all in, nothing waits on him

| Value | Where it is | Gate step |
|---|---|---|
| Unit cost limit 350,000 USD per satellite (covered cost, at the design's own fleet size) | in the model (`budgets.unitCostLimit`), `WP30-decisions.md` verbatim | **resolved**: no step edits it |
| Fleet cost limit 6,000,000 USD (covered cost, n free 1 to 30); the sponsor's full fleet budget is 8,000,000 USD, the other 2,000,000 the allowance for what is not scoped | in the model and the stakeholder layer | **resolved** in the model; the relation is stated in the docs at step 15 |
| Launch 7,000 USD/kg; launch budget 105,770 USD (15.11 kg) | in the model and `case.py` | **resolved** |
| Sampling: more designs per regime, no assumption about the draw | `experiments.definitions.SAMPLE_PER_REGIME = 1250`, the contract's two `rows`; the arithmetic is in `WP30-build-notes.md`, "Sampling" | **resolved** (changing it is one number and two tests) |
| Thirteen traded metrics (the available power and the battery peak power ratio traded, so no requirement floats) | model, oracle, `case.py`, `k_terms.py`, contract version 20: built in the branch | **resolved**; data at step 8 |

There is no placeholder model and no second regeneration (OD5 (b) stands, and the model already carries his values): the gate has one
regeneration, one container run, and the supervisor's step is the review of the changed conclusion (step 10 onward).

## A. Preconditions (before the values are read)

1. **Head and contract number.** PM. `git fetch origin; git show origin/dev:work-packages/interface-contract.toml | grep ^contract_version`.
   Read at `origin/dev` (2026-11-11, again after a fetch): `contract_version = 19` (WP31 took 17, WP25-4 18, WP8b 19). **The WP30 amendment is version 20**
   and is already edited in the branch (`interface-contract.md` row 20 and the quoted number, `.toml` thirteen metrics, the columns, 1,250 rows);
   if the head shows 20 or more at the gate, renumber the row, the quoted number and `contract_version` in one commit. Scope says 17 and the 3b
   build notes say 18: both stale. Files: none unless the number moves.
2. **Rebase the held branches.** impl (3a/3b owner) or PM. Both were rebased onto `origin/dev` 8b5c4f4 (`wp30a` four commits, `wp30b` over it); `origin/dev`
   moves, so rebase `wp30a` onto it, then `wp30b` onto `wp30a` (`git rebase --onto`); expect conflicts only in `scripts/check.py` / records.
   Pass: `git log origin/dev..wp30b` lists only WP30 commits (3a, 3b, the values, the thirteen-metric revision), no attribution trailer.
3. **The red set is the expected one.** impl. `REQUIRE_OPENSYSML=1 uv run pytest -q -m "not slow"` on the rebased `wp30b`.
   Pass: only the 36 below (33 failed, 3 errors), all data-bound or generated files, nothing else (the table with the reason of each is in `WP30-build-notes.md`, "Red set").
   - ledger/data: `test_experiments::test_committed_ledger_verifies...`; `test_mutation_v2` (3); `test_v2_data` (6).
   - contract: `test_interface_contract::test_r3_v2_data_file_header_dtypes_rows` (4).
   - paper: `test_paper` (9); `test_paper_static_figures::test_model_views_in_the_paper_equal_the_models_views`.
   - `test_diagnostic_pair` (3 errors): case spec thirteen attributes and `fleet_size` against the committed data.
   - generated files: `test_model_coverage` (4); `test_system_model_v2_r1` (2); `test_case_model_howto::test_sections_block_is_generated_from_the_model`.
   - reasons from the data: `test_model_coverage::test_every_reasoned_requirement_has_a_computed_reading` and `::test_the_reason_numbers_are_the_spearman_of_the_stated_pair`.
   - slow, not in the fast run: record-bound numbers in `test_case.py`, `test_k_terms_case.py`, the K-terms record script.
   Also: `ruff check .`, `ruff format --check .`, `check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` clean.
4. **QC done.** rev. Stage 4 record `WP30-qc.md` exists, both builds accepted into QC (scope: nothing in (5) starts before).
5. **Freeze.** PM tells every stream: no push that regenerates paper outputs or v2 data from step 6 until the PM says the regression has landed (prose, docs, records may land).

## B. The gate, in order

6. **Merge the builds to dev.** PM. `git checkout dev; git merge --no-ff` (or fast-forward) the rebased `wp30b`
   (carries `wp30a`); push with `git fetch origin && git rebase origin/dev && git push origin HEAD:dev`. dev is red by design for the 26 until step 8-9;
   the Mac watcher and CI will show it: tell the driver first.
7. **k_terms to thirteen. Resolved in the branch.** `examples/adcs/k_terms.py` (`ATTRS`, `SHORT`, `ORIENT`: thirteen; `DESIGN_VARS` with `fleet_size`) and
   `tests/test_k_terms_case.py` (`exponents_.shape == (3, 13)`) are edited. What is left is the re-pin at step 8: the temperatures
   (38.10, 45.68), the margins and radii of the K = 2 and 3 fits, and the K = 3 contending sets, all on the 1,250-design thirteen-metric data
   (host-recorded; the whole module is slow, run it with `uv run pytest -q tests/test_k_terms_case.py`).
8. **One regeneration, on the host (the model carries the supervisor's values; no placeholder).** impl.
   Sample: 1,250 designs per regime (`SAMPLE_PER_REGIME`; timing and arithmetic in `WP30-build-notes.md`, "Sampling": 203 to 207 s per 1,000 designs at
   three workers, 12 N designs in all, 51 minutes of oracle time at N = 1,250, about 60 with the analysis steps); same seeds, the first 1,000 designs are the
   earlier sample; check designs, predictions and shared-subspace sample as before (6, 3, 20). Set `EXPERIMENTS_WORKERS=3` for the ledger run so the figure holds.
   `EXPERIMENTS_WORKERS=3 REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_gate.py --host --wp30 regen --dry` then without `--dry`
   (the five entries re-run: `v2-primary`, `v2-baseline`, `v2-check-predictions`, `v2-check-designs`,
   `scope-sensitivity-shared-subspace-v2`; `--wp30 regen` writes the WP30 note, no hash is required of the outputs because the columns are new).
   Then the two records, in this order, on the regenerated data (the commands of the WP23 close-out gate, `paper/container/RECORD.md`; nothing
   new is needed, `k_terms.py` is the K record's script, run from the repository root):
   - K = 1, 2, 3 record: `uv run python examples/adcs/k_terms.py` (about 50 s at 1,000 designs and eight metrics; expect more at 1,250 and thirteen; prints the per-K summary and the per-term record for both
     regimes; record the contending sets, the temperatures and the K = 3 margin in `WP30-build-notes.md` or the data-gate comparison, then re-pin
     `tests/test_k_terms_case.py` and `test_case.py`'s record-bound numbers).
   - Sensitivity record (five regenerations at a perturbation of one part in 10^12 of the seven design variables, 10 N designs: 43 minutes at N = 1,250 with three workers,
     scratch directory under the scratchpad, never inside `examples/adcs/data`; it draws `SAMPLE_PER_REGIME` designs by itself):
     `PYTHONPATH=examples/adcs uv run python -m experiments.sensitivity regenerate --out $SCRATCH/sens --workers 3`, then
     `PYTHONPATH=examples/adcs uv run python -m experiments.sensitivity analyse --out $SCRATCH/sens --json examples/adcs/experiments/reports/sensitivity.json --md $SCRATCH/sens/generated-section.md`
     (a few minutes; the generated section stays in the scratchpad), then `uv run python paper/stability_extra.py $SCRATCH/sens`
     (a few minutes; writes `paper/stability_extra.json`). Pass: `uv run pytest -q tests/test_sensitivity.py`; the report's sentence
     "Every listed conclusion is identical across the regenerations and to the committed data", or the listed exceptions, go to the data-gate comparison.
   Check designs: they keep the pool-drawn `fleet_size` of the proposals and a fleet of one for the three named candidates (3b build notes: "a gate choice"); record the choice.
   Expected: every v2 file gains `fleet_size` (after `Kd`; after `st_grade` in the predictions), and the main files and check designs gain, after `dod_eclipse`,
   `momentum_headroom`, `available_power_w` (moved up from the auxiliary block), `battery_peak_power_ratio`, `unit_cost_usd`, `fleet_cost_usd`;
   the first 1,000 rows give 706 and 780 feasible designs (R-6; the 1,250 give more, record the counts); `PYTHONPATH=examples/adcs uv run python -m experiments verify` reports 0 drifts; no entry dirty.
   Files: `examples/adcs/data/v2/*`, `tests/data/v2_first_designs_of_record.csv`, `examples/adcs/experiments/ledger/ledger.jsonl`, `experiments/reports/*`, `paper/stability_extra.json`.
   Re-record only arrays the change affects; mark any exact reference "host-recorded, re-pin at the gate" (R-10).
9. **Regenerate the generated files.** impl. `PYTHONPATH=... uv run python examples/adcs/model_v2/coverage.py` (about 16 s; names the model hash);
   regenerate the views (`docs/superpowers/notes/spike-sysml-diagrams/project.py`, PlantUML) and copy the behavioural view to
   `paper/figures/fig-behavioural-view.png`; `uv run python tests/test_case_model_howto.py --write` (after the last edit to `cubesat.sysml`).
   `coverage.py` computes the reasons from the regenerated data (the box is gone: the three requirements that floated carry a reading each, "participates", "one axis with X at rho" or "exponent zero"); if a reading differs from the one the tests pin
   (power requirement one axis with the energy balance, battery ratio exponent zero, momentum headroom participates), re-pin the test with the data's numbers and carry the change to the paper's sentence at step 15.
   Pass: `uv run pytest tests/test_model_coverage.py tests/test_system_model_v2_r1.py tests/test_case_model_howto.py tests/test_paper_static_figures.py`.
   Rerun this step after any later model edit (step 11 edits the model).
10. **Cost ladders and the data-gate comparison (D-6, D-8).** impl then rev.
    D-6: `uv run python scripts/wp30_cost_ladders.py --write` writes `WP30-rounds/cost-ladders.md` from the regenerated data (the script prices every
    feasible design at each n from its configuration and total mass, and checks the repricing against the data's `fleet_size`, `unit_cost_usd` and
    `fleet_cost_usd`: exit 2 on a difference above 1e-9, which is a defect of the model or of the script, to be run down before any row is shown). It gives: share of the feasible designs admitted by each candidate unit-cost value, per regime and per n (1, 3, 10, 30 at least), and each fleet-cost value across n.
    D-8: new section of `work-packages/swap-evidence.md`, form of "WP23 close-out: nine metrics against eight": "Changed conclusions (read first)"; old against new hashes; every moved number with size and cause; contending sets, leading metrics, tension signs, selected tau, certificates, check outcomes, counts, flags.
    Pass (R-6, R-9): existing columns of the first 1,000 design ids equal exactly (exact-equality branches are in the container; on the host, to tolerance, differences listed); 706/780 stand on those rows; the baseline regime's leading trade is momentum headroom, total mass and settling time as confirmed (spike C, on the first 1,000 designs; re-read on the 1,250), **if not, stop and bring the driver before anything downstream moves.** The three readings of "No floating requirements" are read here too: the available power one axis with the energy balance (the association step names the pair at 0.99), the battery peak power ratio at exponent zero, the momentum headroom taking part; a different reading is a changed sentence for step 15, not a stop.
    The cost ladder fractions in `WP30-decisions.md` (82, 71 and 93 percent) are on the earlier calibration: print the admitted shares of the two limits (350,000 and 6,000,000 USD) on the regenerated data for the record; they inform no edit.
11. **The supervisor's values. Resolved before the gate.** The model carries 350,000 and 6,000,000 USD and the launch budget 105,770 USD; the `PLACEHOLDER` wording is gone (a test asserts it) and the data are regenerated once on that model, so there is no model edit, no second step 9 and no neutrality run (`--wp30 values` stays in the tool for a later limit change, not used here). What remains of this step: PM shows the supervisor the printed admitted shares (step 10) beside the changed conclusion, for his review, not for a value. Pass: `uv run pytest tests/test_cost_model.py tests/test_case.py -k "not slow"`; no numeric literal left marked placeholder (R-7 grep).
12. **Contract amendment, version 20. Prepared in the branch; verify at the gate.** impl. `interface-contract.md` (row 20, the quoted `contract_version`, section 7) and `interface-contract.toml` (`contract_version = 20`; thirteen `case.v2.traded_metrics`; `fleet_size` and the five metric columns in the four `case.v2.data` header tables, a float column of whole numbers 1 to 30; 1,250 rows for the two regime files, tied by a test to `SAMPLE_PER_REGIME`) are edited. At the gate: re-read the head's version (step 1), and `uv run pytest tests/test_interface_contract.py` must pass once the data are regenerated (the header and row tests are data-bound). The text states the metric count once, from the manifest.
13. **Answer key v5.** driver (never an author, never a reader; the key is not opened by anyone else). The driver writes v5 outside the repository with the changed conclusion, thirteen metrics (two of which do not bind: the available power is one axis with the energy balance, the battery peak power ratio has exponent zero), the 1,250-design sample, the cost facts; the PM commits the SHA-256 of the file in `WP11-decisions.md` ("Answer key, version 5", with date and the reason) **before** any reader or reviewer that uses the key runs; the hash is of the held file. Versions 1 to 4 are recorded there (v4 `aee912f9...`). Files: `work-packages/WP11-decisions.md`. Order: the hash commit precedes steps 15 to 18's reader passes.
14. **Container regression (one run; the values are in the model).** The container's five entries (`@10`, shared `@9`) are the regression; there is no second `--wp30 values` run, because no limit changes after the regeneration. Hash equality with the host is not claimed (last-digit drift is the registered platform difference); the container run is the reference the later runs compare to. At three workers the five entries take 2 N designs, about 9 minutes at N = 1,250. Driver dispatches; PM waits and says nothing pushes (the freeze of step 5 holds until it lands). Per `paper/container/README.md`: `sh paper/container/build.sh` (commit first: HEAD goes in as a bundle), `sh paper/container/build.sh hts-alt`, regenerate the five ledger entries in `hts-paper` (`PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_gate.py --image <id> --wp30 regen`, spelled out in `paper/container/README.md`), execute the paper (`docker run ... build-paper.sh`), re-pin the exact outputs, full suite in `hts-paper` and `hts-alt`.
    Expected: ledger entries numbered from the ledger as it stands (read from `ledger.jsonl`, 2026-11-11: `v2-primary@8`, `v2-baseline@8`,
    `v2-check-predictions@8`, `v2-check-designs@8`, `scope-sensitivity-shared-subspace-v2@7` are current). Step 8's host regeneration takes
    `@9` (`scope-sensitivity-shared-subspace-v2@8`); this step's container run takes `@10` (`scope-sensitivity-shared-subspace-v2@9`), because
    the host entries stay in the ledger (the earlier gates did the same: close-out host `@6`, container `@7`). Re-read the ledger before each run:
    `uv run python examples/adcs/model_v2/ledger_gate.py --host --wp30 regen --dry` prints the numbers it will take. 0 drifts; hts-alt 0 failed; host comparison shows last-digit drift and the registered platform difference only. Pass: no conclusion, flag or count moves; a changed one reopens the gate. Files: `paper/container/RECORD.md` (every re-pinned file, old and new), the exact reference files, the ledger. **PM announces "regression landed"** and lifts the freeze.
15. **Paper and docs numbers.** impl (paper stream), after step 14. Regenerate with `uv run python paper/execute_notebooks.py` (both notebooks; no stderr); then the sentences that state the metric count (eight to thirteen, "nine" where the box counts; one sentence in the body that two of the thirteen do not bind and why, the detail in Appendices C and D), the baseline regime's leading trade (control effort and settling time to momentum headroom, total mass and settling time), the cost figures (launch 7,000 USD/kg, budget, `CostToBuild` gone; the 8,000,000 / 6,000,000 / 2,000,000 relation and the coverage statement in `docs/examples.md` and `examples/adcs/case-model.md`, which carry no cost sentence yet),
the sampling sentences from "Sampling" (Section 8: the sample is a design choice of the case, the method assumes nothing about how the designs were drawn; Section 7, the search: one or two sentences on how the sampling strategy enters the broader optimisation loop; a ledger raise row quoting the supervisor; "effective sample size" and every number of record move with the 1,250), Section 8, Appendices C and D, `paper/length_ledger.toml`, `claims_register.toml` rows (next free C id after a fetch; run `tests/test_claims_register.py` for any cited sentence), `docs/examples.md`, `examples/adcs/case-model.md`. Pass: `uv run pytest tests/test_claims_register.py tests/test_paper.py tests/test_paper_static_figures.py`; `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` exits 0.
16. **Glossary and Appendix A.** impl. `glossary.yaml` entries (fleet size, unit cost, fleet cost, pricing curve, the cost group, MoP's short form); the same push regenerates Appendix A (`tab-A-register`, via `paper/generate_register.py` / the notebook). Pass: vocabulary check, `tests/test_site.py` (stage first: it reads the local built paper).
17. **Figures.** impl. Figure 3 (behavioural view), the regime and metric figures, the exponent and K tables: regenerated by step 15; drawn from the data; each judged by the figure loop (`docs/superpowers/notes/figure-review.md`: image before caption, ink as data, no facet colouring). The docs figures: `uv run python scripts/build_figures.py`.
18. **Behavioural view and stakeholder layer.** impl. View and caption (no box; the reading per requirement whose metric the fit may leave unweighted, cost group, the 50 kg slot as a note), `stakeholders.sysml` (the cost curves, the launch rate 7,000, the restated launch budget), regenerated and copied (step 9 again if the model changed). Pass: `tests/test_model_coverage.py -k "reason or floats or reads_no"` plus the negative control (a planted requirement reads no traded metric and is named).
19. **Stage the site.** PM or driver. `uv run python scripts/stage_site.py` (strict; fails if the paper does not build). Own browser tab via `tabs_create`; never tab-23.

## C. Stage 6

20. **Cascade review.** rev (Haiku for the greps and counts, Sonnet for reading). Re-run every pattern of "Where the gate looks" and record the remainder, each with a reason or a fix: metric count in words (`eight ... metric`, `eight-metric`, `eight traded`, `eleven`, `nine`) and digits (`8 ... metric`, `11 ... metric`); the sample size (`1000 designs`, `1,000 designs`, `1000-design`, `1 000`); the traded-metric list as columns (`dod_eclipse`); the old cost model (`CostToBuild`, `cost-to-build`); the launch rate and budget (`launchRate`, `6,000 USD`, `90,643`, `15.1`); the feasible-set counts (`706`, `780`: expected to stay; list by `grep -rIlE '706|780' paper docs tests examples claims_register.toml`); the changed conclusion (`control effort ... settling`); contending sets and leading trades; the box (`no traded metric`, `read no traded`, `requirements that read no`: gone from the paper, the view and the docs); exponents and K = 1 results. Also the contract's row 12 "nine" in history and `experiments/compare.py`'s "eight" sentence. Pass: zero stale hits outside record files; no edit to `docs/superpowers/` records except the one generator.
21. **Acceptance review that runs the thing.** rev, own worktree and tab. Run: `uv run pytest`, `ruff check .`, `ruff format --check .`, `uv lock --check`, `uv run python paper/execute_notebooks.py` (no stderr); look in a browser, light and dark, at the behavioural view and caption, Figure 3, the regime figures and every changed page; screenshots saved as files in `work-packages/WP30-review/`, one-line reading each (R-14). Two cold readers (Sonnet, no repository access; one P1, one P2 of `reader-grid.md`), shown the changed Section 8 and the regime figure, briefs read by the PM first, returns committed verbatim. Linux dispatch at the head. Grep `git log <start>..HEAD --format=%B` for the CI's attribution pattern. Output: `work-packages/WP30-review.md`.
22. **Acceptance.** driver, in `WP30-decisions.md`, listing the changed conclusion and the two cost limits for the supervisor.

## What waits on whom

| Waits | On | Until |
|---|---|---|
| Step 8 regeneration | PM freeze (5), rebased branches (2), QC (4) | nothing from the supervisor (his values are in the model) |
| Step 11 (his review of the shares) | supervisor | printed admitted shares (step 10) shown to him with the changed conclusion |
| Step 13 key v5 | driver | the changed conclusion read in step 10 |
| Step 14 container | driver | steps 8 to 13 pushed; the key hash committed |
| Steps 15 to 19 | the container regression | PM's "landed" |
| Step 22 | driver | WP30-review.md |

## Gaps (named by the scope, no command or file found): status after the preparation units (branch `wp30prep`)

| # | Gap | State |
|---|---|---|
| 1 | `ledger_gate.py` had no WP30 mode | **closed** (63b1d2e): `--wp30 regen` (note only; outputs move) and `--wp30 values` (note, and exit 1 naming the entries when an output hash differs); `tests/test_ledger_gate_wp30.py`. Step 8 uses it. |
| 2 | no neutrality mode for a limit change | **resolved by the order of events**: the supervisor's values arrived before the regeneration and the model carries them, so no limit changes after it; `--wp30 values` (closed in tooling at 63b1d2e) stays for a later change. The container run is one run (step 14). |
| 3 | no ladder script; ladders not computable before the data | **closed** (d61f860): `scripts/wp30_cost_ladders.py`. The inputs exist in the repository (`WP23-rounds/spikes/spike-D-cubesat-economics/economics.py` and `admit-shares.txt`); the prices depend on the design columns and total mass only, so the ladders are computable now from the data of record (without waiting for the regeneration), and `--no-launch` reproduces `admit-shares.txt` exactly (tested). With launch included (the metric as built, 3b question 1) the first rung moves: the 450,000 USD placeholder admits 41 percent of the feasible baseline designs at n = 1, not 91 percent (that was the build cost alone). The regenerated data check the repricing at the gate; since the supervisor's values the script prices at the 2026 coefficients and the limits 350,000 and 6,000,000 USD (`tests/test_wp30_cost_ladders.py`). |
| 4 | no named command for the sensitivity and K = 1, 2, 3 records | **closed** (e9f00d1): `k_terms.py` is the K record's script and `experiments.sensitivity` plus `paper/stability_extra.py` the sensitivity record's; the exact commands and times (from `paper/container/RECORD.md`) are in step 8. No new script was needed. |
| 5 | answer key v5's items are not in the repository | **open by design**: the key is the driver's; the PM verifies nothing against it. |
| 6 | `length_ledger.toml` rule and register rows (D-12) have no generator command | **open**: not prepared (outside this brief); `paper/length_ledger.toml` is edited by hand at step 15 and the register id read after a fetch. |
| 7 | stale contract numbers (scope 17, 3b notes 18) | **closed**: `contract_version = 19` at `origin/dev`, next free 20; the amendment is edited in the branch; step 1 re-reads the head. |
| 10 | placeholder model and a second run | **resolved**: see the inputs table and steps 11 and 14. |
| 11 | thirteen traded metrics, sample size, fleet cost 6M / 8M relation | **built or stated**: metrics and the contract in the branch (`WP30-build-notes.md`); `SAMPLE_PER_REGIME = 1250`; the relation is in the model's docs and goes to the docs pages at step 15. |
| 8 | the `hts-paper` ledger re-run not spelled out | **closed** (f337d72): `paper/container/README.md`, "The five-entry ledger re-run in the image". |
| 9 | entry numbers inferred, not read | **closed** (7974796): current entries are `@8` (the shared-subspace entry `@7`); host regeneration `@9` (`@8`), container `@10` (`@9`); there is no `values` run (`@11`) now. `--dry` prints the numbers it will take. |

The cost model's code is on `wp30b`, not on `dev`. Nothing prepared here depends on it: the ladder script prices from the spike's table (the model states it, relative difference below 1e-12 per the 3b notes) and verifies against the regenerated cost columns when they exist, so no patch file is needed.
