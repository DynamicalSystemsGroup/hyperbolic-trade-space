# WP30 data gate: checklist

Prepared 2026-11-11 for the PM, to run the hour the supervisor's values arrive. Sources: `WP30-scope-of-work.md`
(R-6 to R-15, "Where the gate looks"), `WP30-decisions.md` (OD1 (a), OD2 (a), OD5 (b), OD6 (a); stage 3b questions),
the held branches' `WP30-build-notes.md`, `WP23-decisions.md` (the close-out gate), `WP11-decisions.md` (the key
procedure), `PM-BRIEF.md` ("container is a gate check", "full lifecycle", the eighth PM's item 4). Nothing here
changes a decision; where the scope and the head disagree the head wins (marked **stale**).

Roles: PM = the ninth PM; driver = the driver; impl = one Sonnet implementer in its own worktree under
`scratchpad/pm-worktrees/`; rev = a fresh reviewer. Every command is `uv run ...`; set `MPLCONFIGDIR` under the
scratchpad for anything that draws.

## The supervisor's inputs (name, where it enters, step)

| Value | Source | Enters | Step |
|---|---|---|---|
| Unit build cost limit (USD per satellite, read at the configuration's own n) | one rung of the unit-cost ladder (D-6, `WP30-rounds/cost-ladders.md`), per regime and per n; placeholder now 450,000 | `UnitCostRequirement` limit in the stakeholder budgets of `examples/adcs/model_v2/` (`stakeholders.sysml` / `budgets`), and the `WP30-decisions.md` record, his words verbatim | 4 |
| Fleet cost limit (USD, build and launch, n free) | one rung of the fleet-cost ladder (across n); placeholder now 3,000,000 | `budgets.fleetCostLimit`, same | 4 |
| Restated launch budget | OD4: 105,770 USD (15.11 kg x 7,000 USD/kg), recorded; 105,750 USD (15.107 kg) shown beside it; he picks | the launch budget in the budgets, `WP30-decisions.md` | 4 |
| Confirmation that the unit cost includes launch (stage 3b (1) (a)) | already the driver's; no value | none | none |

OD1/OD2/OD5 are settled, so no value changes the feasibility flags and none needs a second regeneration (OD5 (b)).

## A. Preconditions (before the values are read)

1. **Head and contract number.** PM. `git fetch origin; git show origin/dev:work-packages/interface-contract.toml | grep ^contract_version`.
   Read at `origin/dev` (9340212, 2026-11-11): `contract_version = 19` (WP31 took 17, WP25-4 18, WP8b 19). **The WP30 amendment is version 20**
   (the next free number; the toml and the md header both say 19 until step 12). Scope says 17 and the 3b
   build notes say 18: both stale. If the head shows 20 or more, take the next free number. Files: none.
2. **Rebase the held branches.** impl (3a/3b owner) or PM. `wp30a` is at 79ca1d8 on eb48f4e, `wp30b` at 4040f08 on
   `wp30a`; `origin/dev` has moved (6745b88 when written). Rebase `wp30a` onto `origin/dev`, then `wp30b` onto it
   (`git rebase --onto`); expect conflicts only in `scripts/check.py` / records. Pass: `git log origin/dev..wp30b` shows exactly
   the nine WP30 commits (3a: 7af0925, e735c15, 036c6ff, 79ca1d8; 3b: aa73149, cba85e5, 433c145, 950451c, 4040f08, hashes change on rebase).
3. **The red set is the expected one.** impl. `REQUIRE_OPENSYSML=1 uv run pytest -q -m "not slow"` on the rebased `wp30b`.
   Pass: only the 26 below (23 failed, 3 errors), nothing else.
   - ledger/data (3a): `test_experiments::test_committed_ledger_verifies...`; `test_mutation_v2` (3); `test_v2_data` (2: ledger verify, check designs regenerate).
   - paper (3a): `test_paper` (9); `test_paper_static_figures::test_model_views_in_the_paper_equal_the_models_views`.
   - `test_diagnostic_pair` (3 errors, 3b): case spec eleven attributes and `fleet_size` against committed data.
   - contract: `test_interface_contract::test_r3_v2_traded_metrics_are_the_oracles_attribute_names`.
   - generated files: `test_model_coverage` (3); `test_system_model_v2_r1` (2); `test_case_model_howto::test_sections_block_is_generated_from_the_model`.
   - slow, not in the fast run: record-bound numbers in `test_case.py`, `test_k_terms_case.py`, the K-terms record script.
   Also: `ruff check .`, `ruff format --check .`, `check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` clean.
4. **QC done.** rev. Stage 4 record `WP30-qc.md` exists, both builds accepted into QC (scope: nothing in (5) starts before).
5. **Freeze.** PM tells every stream: no push that regenerates paper outputs or v2 data from step 6 until the PM says the regression has landed (prose, docs, records may land).

## B. The gate, in order

6. **Merge the builds to dev.** PM. `git checkout dev; git merge --no-ff` (or fast-forward) the rebased `wp30b`
   (carries `wp30a`); push with `git fetch origin && git rebase origin/dev && git push origin HEAD:dev`. dev is red by design for the 26 until step 8-9;
   the Mac watcher and CI will show it: tell the driver first.
7. **k_terms to eleven.** impl. Edit `examples/adcs/k_terms.py` (`ATTRS`, `SHORT`, `ORIENT`: eleven, plus the design variables incl. `fleet_size`)
   and `tests/test_k_terms_case.py` (`exponents_.shape == (3, 8)` becomes the eleven-metric shape). Pass: `uv run pytest -q tests/test_k_terms_case.py` (the whole module is marked slow, so `-k "not slow"` selects nothing; it
   pins the K = 3 margin and the temperatures, which re-pin at step 8's data).
8. **One regeneration, on the host, with the placeholder limits (OD5 (b)).** impl.
   `REQUIRE_OPENSYSML=1 PYTHONPATH=examples/adcs uv run python examples/adcs/model_v2/ledger_gate.py --host --dry` then without `--dry`
   (the script's header names the five entries re-run: `v2-primary`, `v2-baseline`, `v2-check-predictions`, `v2-check-designs`,
   `scope-sensitivity-shared-subspace-v2`; `ledger_gate.py` needs a WP30 note constant, the build did not add one: **gap 1**).
   Then the two records, in this order, on the regenerated data (the commands of the WP23 close-out gate, `paper/container/RECORD.md`; nothing
   new is needed, `k_terms.py` is the K record's script, run from the repository root):
   - K = 1, 2, 3 record: `uv run python examples/adcs/k_terms.py` (about 50 s; prints the per-K summary and the per-term record for both
     regimes; record the contending sets, the temperatures and the K = 3 margin in `WP30-build-notes.md` or the data-gate comparison, then re-pin
     `tests/test_k_terms_case.py` and `test_case.py`'s record-bound numbers).
   - Sensitivity record (five regenerations at a perturbation of one part in 10^12 of the four design variables, about 38 minutes with three
     workers, scratch directory under the scratchpad, never inside `examples/adcs/data`):
     `PYTHONPATH=examples/adcs uv run python -m experiments.sensitivity regenerate --out $SCRATCH/sens --workers 3`, then
     `PYTHONPATH=examples/adcs uv run python -m experiments.sensitivity analyse --out $SCRATCH/sens --json examples/adcs/experiments/reports/sensitivity.json --md $SCRATCH/sens/generated-section.md`
     (about 3 minutes; the generated section stays in the scratchpad), then `uv run python paper/stability_extra.py $SCRATCH/sens`
     (about 3 minutes; writes `paper/stability_extra.json`). Pass: `uv run pytest -q tests/test_sensitivity.py`; the report's sentence
     "Every listed conclusion is identical across the regenerations and to the committed data", or the listed exceptions, go to the data-gate comparison.
   Check designs: decide whether they keep `fleet_size` drawn from the pool (build notes: "a gate choice"); record it.
   Expected: every v2 file gains `fleet_size` (after `Kd`), `momentum_headroom`, `unit_cost_usd`, `fleet_cost_usd`; flags give 706 and 780 (R-6);
   `PYTHONPATH=examples/adcs uv run python -m experiments verify` reports 0 drifts; no entry dirty.
   Files: `examples/adcs/data/v2/*`, `tests/data/v2_first_designs_of_record.csv`, `examples/adcs/experiments/ledger/ledger.jsonl`, `experiments/reports/*`, `paper/stability_extra.json`.
   Re-record only arrays the change affects; mark any exact reference "host-recorded, re-pin at the gate" (R-10).
9. **Regenerate the generated files.** impl. `PYTHONPATH=... uv run python examples/adcs/model_v2/coverage.py` (about 16 s; names the model hash);
   regenerate the views (`docs/superpowers/notes/spike-sysml-diagrams/project.py`, PlantUML) and copy the behavioural view to
   `paper/figures/fig-behavioural-view.png`; `uv run python tests/test_case_model_howto.py --write` (after the last edit to `cubesat.sysml`).
   Pass: `uv run pytest tests/test_model_coverage.py tests/test_system_model_v2_r1.py tests/test_case_model_howto.py tests/test_paper_static_figures.py`.
   Rerun this step after any later model edit (step 11 edits the model).
10. **Cost ladders and the data-gate comparison (D-6, D-8).** impl then rev.
    D-6: write `WP30-rounds/cost-ladders.md` from the regenerated data: share of the feasible designs admitted by each candidate unit-cost value, per regime and per n (1, 3, 10, 30 at least), and each fleet-cost value across n.
    D-8: new section of `work-packages/swap-evidence.md`, form of "WP23 close-out: nine metrics against eight": "Changed conclusions (read first)"; old against new hashes; every moved number with size and cause; contending sets, leading metrics, tension signs, selected tau, certificates, check outcomes, counts, flags.
    Pass (R-6, R-9): existing columns of the same design ids equal exactly (exact-equality branches are in the container; on the host, to tolerance, differences listed); 706/780 stand; the baseline regime's leading trade is momentum headroom, total mass and settling time as confirmed, **if not, stop and bring the driver before anything downstream moves.**
11. **The supervisor's values.** PM puts the ladder rows (D-6) in front of the supervisor; on his words: quote them verbatim in `WP30-decisions.md`; impl edits the two limits and the launch budget in the model (replace the "PLACEHOLDER" docs, `cubesat.sysml` lines about `budgets`); rerun step 9; the verdicts of the two cost requirements and the requirements table re-pin; the flags and the data are byte-identical, so the ledger entries stay: prove it by `ledger_gate.py --host --wp26`-style neutrality run (**gap 2**: the model hash changes, ledger entries cite it; WP26's `--wp26` mode is the precedent, a WP30 mode must be added or the entries re-run).
    Pass: `uv run pytest tests/test_cost_model.py tests/test_case.py -k "not slow"`; no numeric literal left marked placeholder (R-7 grep).
12. **Contract amendment, version 20.** impl. In one commit: `work-packages/interface-contract.md` (change-log row 20 with cause; the quoted "contract_version" number) and `interface-contract.toml` (`contract_version = 20`; eleven `case.v2.traded_metrics`; `fleet_size` in `config_names` and the dataset column tables, a float column of integers 1 to 30; cost columns after `momentum_headroom`); amend ownership paths if a new file is added. Pass: `uv run pytest tests/test_interface_contract.py`. The text states the metric count once, from the manifest.
13. **Answer key v5.** driver (never an author, never a reader; the key is not opened by anyone else). The driver writes v5 outside the repository with the changed conclusion, eleven metrics, the cost facts; the PM commits the SHA-256 of the file in `WP11-decisions.md` ("Answer key, version 5", with date and the reason) **before** any reader or reviewer that uses the key runs; the hash is of the held file. Versions 1 to 4 are recorded there (v4 `aee912f9...`). Files: `work-packages/WP11-decisions.md`. Order: the hash commit precedes steps 15 to 18's reader passes.
14. **Container regression.** driver dispatches; PM waits and says nothing pushes (the freeze of step 5 holds until it lands). Per `paper/container/README.md`: `sh paper/container/build.sh` (commit first: HEAD goes in as a bundle), `sh paper/container/build.sh hts-alt`, regenerate the five ledger entries in `hts-paper` (`ledger_gate.py --image <id>`), execute the paper (`docker run ... build-paper.sh`), re-pin the exact outputs, full suite in `hts-paper` and `hts-alt`.
    Expected: ledger entries numbered from the ledger as it stands (read from `ledger.jsonl`, 2026-11-11: `v2-primary@8`, `v2-baseline@8`,
    `v2-check-predictions@8`, `v2-check-designs@8`, `scope-sensitivity-shared-subspace-v2@7` are current). Step 8's host regeneration takes
    `@9` (`scope-sensitivity-shared-subspace-v2@8`); this step's container run takes `@10` (`scope-sensitivity-shared-subspace-v2@9`), because
    the host entries stay in the ledger (the earlier gates did the same: close-out host `@6`, container `@7`). Re-read the ledger before each run:
    `uv run python examples/adcs/model_v2/ledger_gate.py --host --wp30 regen --dry` prints the numbers it will take. 0 drifts; hts-alt 0 failed; host comparison shows last-digit drift and the registered platform difference only. Pass: no conclusion, flag or count moves; a changed one reopens the gate. Files: `paper/container/RECORD.md` (every re-pinned file, old and new), the exact reference files, the ledger. **PM announces "regression landed"** and lifts the freeze.
15. **Paper and docs numbers.** impl (paper stream), after step 14. Regenerate with `uv run python paper/execute_notebooks.py` (both notebooks; no stderr); then the sentences that state the metric count (eight to eleven, "nine" where the box counts), the baseline regime's leading trade (control effort and settling time to momentum headroom, total mass and settling time), the cost figures (launch 7,000 USD/kg, budget, `CostToBuild` gone), Section 8, Appendices C and D, `paper/length_ledger.toml`, `claims_register.toml` rows (next free C id after a fetch; run `tests/test_claims_register.py` for any cited sentence), `docs/examples.md`, `examples/adcs/case-model.md`. Pass: `uv run pytest tests/test_claims_register.py tests/test_paper.py tests/test_paper_static_figures.py`; `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` exits 0.
16. **Glossary and Appendix A.** impl. `glossary.yaml` entries (fleet size, unit cost, fleet cost, pricing curve, the cost group, MoP's short form); the same push regenerates Appendix A (`tab-A-register`, via `paper/generate_register.py` / the notebook). Pass: vocabulary check, `tests/test_site.py` (stage first: it reads the local built paper).
17. **Figures.** impl. Figure 3 (behavioural view), the regime and metric figures, the exponent and K tables: regenerated by step 15; drawn from the data; each judged by the figure loop (`docs/superpowers/notes/figure-review.md`: image before caption, ink as data, no facet colouring). The docs figures: `uv run python scripts/build_figures.py`.
18. **Behavioural view and stakeholder layer.** impl. View and caption (reasons per boxed requirement, cost group, the 50 kg slot as a note), `stakeholders.sysml` (the cost curves, the launch rate 7,000, the restated launch budget), regenerated and copied (step 9 again if the model changed). Pass: `tests/test_model_coverage.py -k reason` plus the negative control.
19. **Stage the site.** PM or driver. `uv run python scripts/stage_site.py` (strict; fails if the paper does not build). Own browser tab via `tabs_create`; never tab-23.

## C. Stage 6

20. **Cascade review.** rev (Haiku for the greps and counts, Sonnet for reading). Re-run every pattern of "Where the gate looks" and record the remainder, each with a reason or a fix: metric count in words (`eight ... metric`, `eight-metric`, `eight traded`) and digits (`8 ... metric`); the traded-metric list as columns (`dod_eclipse`); the old cost model (`CostToBuild`, `cost-to-build`); the launch rate and budget (`launchRate`, `6,000 USD`, `90,643`, `15.1`); the feasible-set counts (`706`, `780`: expected to stay; list by `grep -rIlE '706|780' paper docs tests examples claims_register.toml`); the changed conclusion (`control effort ... settling`); contending sets and leading trades; the box (`no traded metric`, `read no traded`); exponents and K = 1 results. Also the contract's row 12 "nine" in history and `experiments/compare.py`'s "eight" sentence. Pass: zero stale hits outside record files; no edit to `docs/superpowers/` records except the one generator.
21. **Acceptance review that runs the thing.** rev, own worktree and tab. Run: `uv run pytest`, `ruff check .`, `ruff format --check .`, `uv lock --check`, `uv run python paper/execute_notebooks.py` (no stderr); look in a browser, light and dark, at the behavioural view and caption, Figure 3, the regime figures and every changed page; screenshots saved as files in `work-packages/WP30-review/`, one-line reading each (R-14). Two cold readers (Sonnet, no repository access; one P1, one P2 of `reader-grid.md`), shown the changed Section 8 and the regime figure, briefs read by the PM first, returns committed verbatim. Linux dispatch at the head. Grep `git log <start>..HEAD --format=%B` for the CI's attribution pattern. Output: `work-packages/WP30-review.md`.
22. **Acceptance.** driver, in `WP30-decisions.md`, listing the changed conclusion and the two cost limits for the supervisor.

## What waits on whom

| Waits | On | Until |
|---|---|---|
| Step 8 regeneration | PM freeze (5), rebased branches (2), QC (4) | nothing from the supervisor (OD5 (b)) |
| Step 11 (limits into the model) | supervisor | ladder rows (step 10) shown to him |
| Step 13 key v5 | driver | the changed conclusion read in step 10 |
| Step 14 container | driver | steps 8 to 13 pushed; the key hash committed |
| Steps 15 to 19 | the container regression | PM's "landed" |
| Step 22 | driver | WP30-review.md |

## Gaps (named by the scope, no command or file found)

1. `ledger_gate.py` has no WP30 note or mode (it has `--host`, `--image`, `--wp26`); the five-entry re-run for this gate needs one (step 8).
2. The values re-pin after the regeneration (OD5 (b)) changes the model hash that the entries record; no neutrality mode for a limit change exists (step 11).
3. `WP30-rounds/cost-ladders.md` and its generator do not exist on `wp30b` (D-6 is "not computable before the data"); `admit-shares.txt` (first rung) is in the spike folder only. No script computes per-n, per-regime pass fractions.
4. No command is named for the sensitivity record and the K = 1, 2, 3 record regeneration beyond the ledger entries; confirm `k_terms.py` has a record script.
5. The answer key v5's content is the driver's; no checklist of its items exists in the repository (by design), so the PM cannot verify the items that state the baseline trade.
6. The scope's "length_ledger.toml" rule and the register rows (D-12) have no generator command; the register id after C447 is read after a fetch.
7. The contract number in the scope (17) and the 3b notes (18) are stale; the amendment is 20 (derived above), and the build notes' "version 18" text will be wrong if copied.
8. The container steps' exact `docker` arguments for the ledger re-run inside `hts-paper` are in `paper/container/README.md` only for the suite and the paper build; the five-entry re-run (`ledger_gate.py --image`) is not spelled out there.
