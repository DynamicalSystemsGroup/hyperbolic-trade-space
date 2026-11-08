# WP4b — Review report (third pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4b-scope-of-work.md` with Amendment 1 (R-14 to its relative clauses), Amendment 2 (momentum enforced as feasibility), Amendment 3 (physically consistent scenario) and Amendment 4 (slew-time attribute, the last adjustment, ten attributes) |
| **Scope approval verified** | The project has no PRs, so the recorded act is `work-packages/WP4b-decisions.md`: "Scope approval (approval gate)", supervisor mzargham, verbatim "okay proceed", document at `d27c177`, defaults list approved as one item. Amendment 1: "Amend R-14 to its intent; keep the dataset". Amendment 2: "Enforce as feasibility" and "Fix the stale help text, accept the rest". Amendment 3: "Reopen levers for a physically consistent scenario". Amendment 4: "One physics-justified lever: slew-time attribute" (record `aec9276`, scope text `92b58ed`). The record states that if R-13 still fails the finding is accepted and the notebook reports wheel class as a feasibility boundary; the scope text of Amendment 4 repeats "the supervisor has agreed to accept that finding". Records typed by the agent, decisions are the supervisor's. |
| **Work reviewed** | `main` at `6c8c3e9`. Amendment 4 delivery: Step A note `25517f0`, model/dataset/tests `a27502e`, results note `6c8c3e9`. Earlier delivery `5dfbc8c`, `379dee0`, `c89b5d0`, `b8fd0cc`, `7704ab7`, `354bffd`. Start for diffs `5dfbc8c~1`; WP4 state `932bbe4` (simulator) / `9680193` (WP4 tests, CSV, design space). |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4b-decisions.md`, after this report |

A fresh reviewer who built none of WP4b and wrote none of its earlier reviews (replaces the second-pass report, `b16e1b7`). Every command below was run in this session with `unset VIRTUAL_ENV`. Review only: two trial edits were made and undone with `git checkout`; `git status` is clean. R-13 is judged under the Amendment 4 stop rule.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/cubesat_tradespace.sysml`; amendment 4 changed only the `ModelTest` documentation (ten attributes, slew time described), `git show a27502e`. |
| D-2 | met | `examples/adcs/cubesat_model.py`: new `slew_time(res, band_deg)` helper (post-processes `res.t`, `res.q`; error angle `2 norm(q[:3])` in degrees, first entry, censored at the last time), `SLEW_BAND_DEG = 1.0`, `SLEW_BAND_SENSITIVITY_DEG = 0.5`, `measure` returns `slew_time_s` and `slew_time_05deg_s`. |
| D-3 | met | `generate_dataset.py`: docstring only (columns come from `measure`). |
| D-4 | met | `data/adcs_designs_cubesat.csv`: 1000 rows, 35 columns incl. `slew_time_s`, `slew_time_05deg_s`; 30 degrees, 600 s, seed 0. |
| D-5 | met | `uv lock --check`: "Resolved 173 packages". |
| D-6 | met (3 strict xfails) | `REQUIRE_OPENSYSML=1 uv run pytest -q -rx tests/test_cubesat_model.py tests/test_adcs_enrichment.py`: 35 passed, 3 xfailed in 27 s. xfails: `test_a_`, `test_b_`, `test_c_` (strict, reason STOP4 with the numbers). `test_e_` lost its marker (it now passes, see R-13). Two new tests: `test_slew_time_definition_and_ordering`, `test_slew_time_helper_first_entry_and_censoring`. |
| D-7 | met | Probe note: Step A, results, corrected mass explanation, stale sections fixed (see verification 4). |
| D-8 | met | `WP4b-decisions.md` holds the approval, amendments 1 to 4 and every disposition; acceptance pending. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `git diff 932bbe4..HEAD -- examples/adcs/adcs_sim.py` empty; `git diff 9680193..HEAD --stat` over `adcs_sim.py`, `tests/test_adcs_case.py`, `design_space.py`, `adcs_designs.csv` empty. WP4 tests pass inside the full suite. |
| R-2 | met | Original CSV, `design_space.py`, `test_adcs_case.py` untouched; WP4 reproducibility tests pass. (No separate defaults test: accepted in round 1.) |
| R-3 | met | `test_cubesat_model.py`: 27 passed under `REQUIRE_OPENSYSML=1`. |
| R-4 | met | Range/enum edit and no-duplicate-constants tests pass; amendment 4 added the two band constants to the scenario-parameter exemption in the scan (scenario parameters, not model constants). |
| R-5 | met | Unchanged code path; sweep/accounting tests pass. |
| R-6 | met | Flag and negative-control tests pass. |
| R-7 | met | Trial 1 below (breaking the slew helper) and the second-pass coupling trial both fail tests; panel monotonicity test passes. |
| R-8 | met | Battery and baseline-inertia tests pass. |
| R-9 | met | Power-cap and slew-energy tests pass. |
| R-10 | met | Mass identity test passes. |
| R-11 | met | `test_measure_returns_attributes_and_flags` covers ten attributes and five flags; `test_attributes_are_documented` passes (slew time documented in the module docstring). |
| R-12 | met | `uv lock --check` ok; hard-failing fixture, `REQUIRE_OPENSYSML=1` in CI; CI green. |
| R-13 | **not met, under the Amendment 4 stop rule** | See "R-13 clause by clause" below: (a), (b), (c) fail; (d) and (e) hold. |
| R-14 | met (amended) | Own computation on 780 feasible rows: median saturated fraction small 0.0409, large 0.0080, ratio 5.1 (needs 3); median settling small 128.3 s, large 69.3 s, ratio 1.85 (needs 1.25). `test_torque_binds_for_small_wheels` passes without marker. |
| R-15 | met | 1000 designs, settled share 0.978, feasible 780; violation shares settled 0.022, momentum_ok 0.081, power_ok 0.000, dod_ok 0.131. |
| R-16 | met | `test_dataset_reproducible_first_20` (now also checks the two slew-time columns within 0.5 s) and the same-platform exactness test pass. Trial 2 shows the first fails when slew time is wrong. |
| R-17 | met | The note records every attempt including the four-lever history, the Step A expectation, the results with near-frontier sizes, the SysML client account, and explicit physical explanations; the wrong Step A expectation is reported as wrong (verification 4). |
| R-18 | met | SysML unchanged in substance; plausible cubesat. |
| R-19 | met | `uv run pytest`: 844 passed, 8 skipped, 4 xfailed (69.7 s; 3 WP4b strict xfails plus 1 WP3 scikit-learn xfail). `ruff check .`: All checks passed. `ruff format --check .`: 95 files already formatted. `uv lock --check`: ok. |
| R-20 | met | Grep of all commit messages and authors in `5dfbc8c~1..HEAD` for `co-authored`, `generated with`, `claude`: 0. All 41 commits authored and committed by Michael Zargham. `gh run list --limit 8`: all 8 green including `6c8c3e9` (1m37s). Over the last 40 runs only two were red, `8f49253` (WP6) and `f635a04` (WP3), both `test_narrative` failures belonging to WP3/WP6 and fixed later; neither WP4b. |

### R-13 clause by clause (my own probe, committed CSV, ten attributes)

Feasible = settled and `power_ok` and `momentum_ok` and all ten attributes positive (780 rows: small 239, medium 279, large 262). Reciprocal for settling, slew time, pointing, mass, effort, peak slew power and depth of discharge; direct for margin, balance, reserve; log; standardize; `solve_lp(U, 0)`; 300-point tau grid to `frac_above_` nearest 0.10; near-frontier |log V| < 1/tau; 100 bootstrap resamples seeded 0.

| Quantity | Mine | Implementer's | Verdict |
|---|---|---|---|
| Contending set, tau = inf | effort .434, slew .253, power margin .179, settling .081, pointing .040, reserve .013 (size 6); **mass 0.000**, energy balance, peak power, depth of discharge 0 | identical | (a) needs mass >= 0.05: **fails** (size >= 3 and a power attribute hold) |
| Working tau, frac_above | 43.0, 0.100 | 42.8, 0.101 | about 0.10 |
| Near-frontier rows (small/medium/large) | 104 (79/24/1) | 102 (78/23/1) | difference is the tau grid |
| Bootstrap support (median exponent) | mass **0.00** (0), power margin 0.66 (0.155), reserve 0.58, balance 0.50, depth of discharge 0.43; slew 1.00, effort 1.00, pointing 0.95, settling 0.88 | mass 0.00, margin 0.66, reserve 0.58 | (b) **fails** on both mass (needs .90) and the best power attribute (.66 < .90) |
| Settling-mass / slew time-mass association | **-0.13 / -0.11** | -0.13 / -0.11 | (c) needs either at most -0.30: **fails**; the class-count clause (small 79, medium 24 with >= 10) holds |
| Power tensions | mass with depth of discharge -0.66; pointing with peak slew power -0.61; mass with reserve -0.58 | -0.65, -0.61, -0.58 | (d) holds |
| Previous tensions | settling-effort -0.95, pointing-effort -0.68, pointing-mass -0.34, settling-pointing +0.66 | -0.95, -0.70, -0.36, +0.68 | (e) holds (pointing-mass now passes) |
| Slew-settling | corr 0.947 over the feasible set, 0.98 near the frontier | 0.947, 0.99 | |

Every number reproduces within the tau-grid tolerance. `test_e_previous_tensions_retained` passes unmarked.

## Independent verification asked for

**(1) Ordering.** `git log`: `25517f0` "probe note, amendment 4 step A (slew-time definition and expectation, before any simulation)" 00:40:58 is an ancestor of `a27502e` (model, dataset, tests) 00:47:12 and of `6c8c3e9` (results note). `git show 25517f0` changes only the note (+48 lines): definition, band choice (1 degree, 0.5 as sensitivity only), where it is computed, four expectations. Ordering is verified from git. What git cannot show is that nobody simulated slew time privately before 00:40:58; the Step A numbers for saturation (0.0409/0.0080, ratio 5.1) are the earlier dataset's, which is legitimate. Note `a27502e` and `6c8c3e9` carry the same commit second (00:47:12); only order matters and it is as required.

**(2) Slew time recomputed.** My own post-processing (`argmax(err < 1 degree)` on `simulate_adcs` output, rebuilt through `CubesatModel.configure/sim_params` and `make_config` at 30 degrees, 600 s, 0.5 s step) on designs 0, 1, 5, 17, 99, 250, 500, 777: differences from the CSV 0.0000 s in all; settling recomputed equal too. Censoring: exactly 4 designs have `slew_time_s` = 600 (ids 222, 308, 345, 438; Kp about 0.031, Kd about 1.4), all of them also unsettled (22 unsettled in total), so none is in the feasible set; designs 222 and 308 recomputed as censored. Also: slew time never exceeds settling time (0 violations), the 0.5 degree time is never earlier than the 1 degree time.

**(3) Probe.** Reproduced above, including contending set, bootstrap, near-frontier counts and associations.

**(4) Probe-note corrections.** G-2 fixed: the note now says wheels weigh 0.36 / 0.75 / 1.80 kg, std 0.60 of 0.84 kg total (my data: wheel 0.36 to 1.80, std 0.599; total std 0.837; panel std 0.169, battery std 0.350); the old sentence is quoted as the wrong one. Minor: the note says wheel mass "explains 55 %" of mass variance; my full-dataset variance share is 51 % (about 56 % as squared correlation on the feasible set), so the figure is right only on the feasible-set reading. G-3 fixed: the R-14 status section now says R-13 (a), (b), (c) fail, (d), (e) hold, labelled superseded; the old constants section is retitled "Phase 2 ... (history)" with the final scenario stated; `grep` finds no remaining "all of a to e holds" claim. Honesty of the Step A correction: the note says the expectation was partly wrong (levels 82.7 vs 70 and 51 vs 35 s; slew about 0.74 of settling, not half; small/large ratio 1.60, not above settling's 1.85; correlation 0.947, not 0.5 to 0.8) and gives the reason ln 30 / ln 100 = 0.74. I verified: ratio median 0.745, ln30/ln100 = 0.739, correlation 0.947, class medians 82.7 / 50.7 / 51.8 vs settling 128.3 / 67.1 / 69.3, slew corr with log(Kd/Kp) 0.998 / 0.990 / 0.971 (large/medium/small; settling 0.992 / 0.924 / 0.707), and at Kd/Kp below 5 (494 designs) slew medians small 35.5, medium 29.7, large 27.6 s against settling 88, 42, 36 s. All as stated. One thing the note could say more directly: the Step A rationale itself argued that the 1 degree band sits "before the slow tail"; it does not, and the note says so.

**(5) Is the finding supported?** Yes. "Wheel class is a feasibility boundary; agility by slew time does not trade against mass" rests on: small wheels lose 19.2 % of designs to momentum at 30 degrees (medium 4.3 %, large 0 %; my numbers from `momentum_ok`; the 98 % at 90 degrees is from the prior dataset and was verified in the second pass by the h_max^2/(T J) bound); mass exponent 0.000 and bootstrap support 0.00; slew-mass and settling-mass associations -0.11 and -0.13 (-0.06 at 0.5 degrees). The caveat is that the null is partly built in: slew time at a 1 degree band is almost the same quantity as settling (0.947), so the fourth adjustment did not add independent evidence about actuator-limited agility; it confirmed that the first-entry time at this band is in the same slow tail. The finding is therefore "not found with these measures and this gain box", not "cannot exist".

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-8 exist | met | See Deliverables. |
| R-1 to R-20 pass as checked | **not met (R-13)** | R-13 (a), (b), (c) fail; every other requirement is met. |
| R-13 and R-14 hold on the committed dataset | **not met (R-13)** | R-14 holds; R-13 does not. This is the pre-agreed finding; accepting it means the supervisor records R-13 as a finding rather than a passed requirement. |
| Non-goals untouched | met | See below. |

## Outside the scope

- **Out-of-scope changes:** none by WP4b beyond those accepted earlier (`.github/workflows/test.yml` cache edit, `pyproject.toml`, `uv.lock`, a comment-only edit to `extended_design_space.sysml`). `git diff --stat 5dfbc8c~1..HEAD -- . ':!work-packages'` also lists `docs/api.md`, `docs/limitations.md`, `docs/method.md`, `docs/preconditioning.md`, `docs/why-and-how.md`, `tests/test_docs.py`, `src/hyperbolic_trade_space/__init__.py`, `tuning.py`: these are commits by WP3 and WP6 (`git log` shows `f6d9b9a`, `94fbe72`, `07fe9d3`, `e82594b`, `8f49253`, `f635a04`, `0815c82`, `c793e10`), not WP4b. Amendment 4 touched only the six files in `git show --stat a27502e` and the note.
- **Non-goals touched:** none. `adcs_sim.py` byte-identical; no estimator, solver, coordinates, WP2/WP3 or notebook change by WP4b; no `sysml-toolkit` dependency; WP4 CSV and tests untouched.

## Trials (undone)

1. Broke the helper (`err_deg < band_deg` to `err_deg < 2 * band_deg`): `test_slew_time_helper_first_entry_and_censoring` and `test_dataset_reproducible_first_20` fail, 2 failed 25 passed. Restored by `git checkout`.
2. Replaced `slew_time_s` in `measure` by the settling time: `test_slew_time_definition_and_ordering` and `test_dataset_reproducible_first_20` fail. Restored by `git checkout`. `git status` clean.

## Observations (not counted as failures)

Levers still unused, for the supervisor (none was allowed by Amendment 4, which was the last adjustment):
- **Momentum headroom as an attribute.** `peak_momentum_nms` is already in the CSV. A larger-is-better headroom (h_max over peak momentum) would put wheel class on the frontier directly (heavier wheel, more headroom), instead of only as a feasibility filter; a natural physics lever and a change to the attribute set, not the scenario.
- **Gain box.** Wheel class only separates agility at Kd/Kp below about 5 (494 of the feasible designs; slew small 35.5 s vs large 27.6 s, settling 88 vs 36 s). Narrowing or re-sampling the Kd/Kp range, or per-class gains, would put more designs in the torque-limited regime.
- **Larger tolerance band** (for example 5 or 10 degrees at 30 degrees) or peak slew rate, which sit in the saturated phase rather than the tail; the 1 degree band was fixed in Step A before data and is in the tail (3.4 slow-pole time constants).
- **Wheel mass.** Scaling wheel mass with momentum capacity (which grows tenfold while mass grows fivefold) or a wider spread would strengthen the mass lever. Wheel mass is already the largest single mass lever.
- **Sampled or per-class slew angle**, so each class operates at its own boundary (h_max^2 / (T J)).
- **Cost of two near-duplicate attributes.** Settling and slew time (0.947) now both sit in the fit; the LP splits weight between them (slew .253, settling .081). WP7 must not read these as independent findings (the note already lists the pair under the redundant pairs).
- **Large wheels on the frontier rest on 1 design** (near-frontier counts 79/24/1).
- The note's "55 %" wheel-mass variance share is feasible-set-specific (51 % on all 1000).
- Strict xfail on `test_a_`, `test_b_`, `test_c_` is a useful tripwire: a later change that makes any pass fails the suite. The suite shows 4 xfails, one of which (scikit-learn) belongs to WP3.
- Earlier dispositions on record: round 1 G-1, G-3, G-4, rest of G-5 accept as is, stale help text fixed (verified); G-2 momentum "Enforce as feasibility" (amendment 2); second-pass G-1 (R-13 under the stop rule) answered "Reopen levers for a physically consistent scenario" then "One physics-justified lever: slew-time attribute" (amendments 3 and 4); second-pass G-2 and G-3 (probe-note defects) fixed in amendment 4 and verified here.

## Open decisions (for the supervisor)

- **G-1. R-13 (a), (b), (c) remain unmet after the last adjustment** (total mass exponent 0.000, bootstrap support 0.00; settling-mass -0.13, slew time-mass -0.11; (d) and (e) hold; R-14 holds). The supervisor pre-agreed to accept this finding in Amendment 4, but good enough requires R-13 to hold, so acceptance needs the supervisor to record R-13 as the finding (wheel class is a feasibility boundary; agility by slew time does not trade against mass) and the notebook to say so. — options: accept as is / fix before acceptance (reopen levers, see observations) / follow-up work package (accept the rest, move the richness question to a later package). **pending**
- **G-2.** Slew time is near-redundant with settling (0.947), so the fourth adjustment adds little independent evidence; the unused levers above are candidates if the richness question is revisited. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-3.** Small items: the "55 %" figure in the note is feasible-set-specific; Step A ordering is verifiable from git but not that no private simulation preceded it; suite shows one non-WP4b xfail. — options: accept as is / fix before acceptance / follow-up work package. **pending**
- **G-4.** WP7 facts (power never limits a slew, redundant pairs including slew-settling, class counts 239/279/262, near-frontier 79/24/1, finding statement) are verified and should be carried into WP7's scope. — options: accept as is (WP7 will carry them) / fix before acceptance / follow-up work package. **pending**

## Gap dispositions

Resolved through the decision loop (`~/.claude/skills/CLAUDE.md`); records go in `work-packages/WP4b-decisions.md`.

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | pending | |
| G-2 | pending | |
| G-3 | pending | |
| G-4 | pending | |

## Recommendation

**Recommend acceptance with the listed gaps noted, conditional on the supervisor recording R-13 as the pre-agreed finding.** The evidence supports that recommendation. The stop rule was triggered by a lever the supervisor chose, run in the stated order (Step A in git before the model and dataset change, verified), with the implementer's own wrong expectation reported honestly; the slew times in the CSV reproduce exactly from the simulator output; my independent probe reproduces every R-13 number; R-14 and R-1 to R-12, R-15 to R-20 are met; the full suite, both WP4b files under `REQUIRE_OPENSYSML=1`, ruff, lock, attribution, authors and CI (last 8 runs) are clean; `adcs_sim.py` and the WP4 tests are untouched; two trials break tests as they should. R-13 (a), (b), (c) fail on numbers that are not near the thresholds (mass 0.000 against 0.05; bootstrap 0.00 against 0.90; associations -0.13 and -0.11 against -0.30), so the finding is firmly established and not a near miss. Whether to accept a package whose approved richness requirement is unmet is the supervisor's scope decision (G-1); the evidence does not contradict the finding, but it is weaker than it looks because slew time and settling are nearly the same measure (G-2).

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
