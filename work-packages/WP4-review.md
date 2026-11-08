# WP4 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP4-scope-of-work.md` |
| **Scope approval verified** | Verbal approval recorded in `work-packages/WP4-decisions.md` (section "Scope approval", commit bcfe110): supervisor (mzargham), verbatim "double check with the github cli but then let's move forward", dated 2026-11-08 in the record; the record states the physics additions (SRP in the analytic pointing budget only, RSS pointing error, effort as the integral of the torque norm, momentum as a flag, illustrative hardware) were put to the supervisor explicitly and that open decisions were none. The project has no PRs, so this is the recorded act the scope names. The record is typed by the agent, so the review cannot confirm the chat itself. The acceptance section of that file reads "pending". |
| **Work reviewed** | `main` at `6b5a6a5` after `git pull --rebase origin main` (already up to date). WP4 commits `932bbe4`, `9227f47`, `3864a8a`; no later WP4 commit exists. Diff base `1c71306`. Trial edits were restored per file with `git checkout`; none committed. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4-decisions.md`, after this report |

Every command below was run in this session (`unset VIRTUAL_ENV`, `uv run ...`). Note: the working tree briefly showed an uncommitted change to `src/hyperbolic_trade_space/coordinates.py` mid-review (another session working on WP2); it was gone on the next look and is not part of this review.

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/adcs_sim.py` (286 lines): `BASELINE`, `inertia_tensor`, `pointing_budget`, `make_config`, `SimConfig`, `simulate_adcs`, `run_step_response`; departures marked `# CHANGED:`. |
| D-2 | met | `examples/adcs/design_space.py` (138 lines): `WHEEL_CLASSES`, `STAR_TRACKERS`, `KP_RANGE`, `KD_RANGE`, `sample_designs`, `evaluate_design`, `FAST_SIM`. Class values equal the scope defaults. |
| D-3 | met | `examples/adcs/generate_dataset.py` (85 lines). |
| D-4 | met | `examples/adcs/data/adcs_designs.csv`: 1000 rows, 16 columns (pandas). |
| D-5 | met | `examples/adcs/extended_design_space.sysml` (44 lines). |
| D-6 | met | `tests/test_adcs_case.py` (210 lines, 14 tests). |
| D-7 | met | `work-packages/WP4-decisions.md` holds the approval record (verbatim quote above); acceptance "pending". |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `pytest tests/test_adcs_case.py -k inertia`: 1 passed (abs 0.01 on all three). The module doctest also passes (`uv run pytest examples/adcs`: 1 passed). |
| R-2 | **not met as written** (G-1); the three tight pins are met, the baseline value stated in the scope is wrong | `-k regression`: 4 passed, but the baseline case passes only because the test pins 310.6 +-0.5, not 201.6 (comment in the test: "scope R-2 says 201.6; source repo pins 310.6; amendment pending with supervisor"). Independent check of the source repo (read-only, its own `.venv`, `PYTHONDONTWRITEBYTECODE=1`): `make_config_from_params` + `simulate_adcs`, X-axis 10 deg slew, 360 s, gives (1,10) -> 310.626 s, (4,30) -> 77.966 s, (8,30) -> 87.396 s, (4,25) -> 120.498 s. Its `tests/test_sysml_evidence.py` line 26 pins `r["x"] == approx(310.6, abs=0.2)` for `ev.INITIAL`, and line 89 pins 310.6 again; `jaxa_notebook.ipynb` prints "settling_time_s = 310.6 s (budget 120 s)"; `sysml/probe/FINDINGS.md` reports "weak settling 310.63 s". `grep -rnE '201\.6\|310\.6'` over the whole source repo (excluding `.venv`, `.git`, lock) finds 310.6 in six places and 201.6 nowhere. The (4,30), (8,30), (4,25) pins in the port agree with the source to 0.04 s or better (port test: 77.97 +-0.2, 87.40, 120.50). The `sysml/evidence` module could not be imported (the source venv lacks `opensysml`); I used `analysis.numerical` directly, which `slew_settling` wraps. So 310.6 is correct and the number 201.6 in the scope and the adcs-port note is an error, not an alternative physical result. The port reproduces the source's own value. |
| R-3 | met | `grep -nE '^\s*(import\|from)'` over `adcs_sim.py`: only `dataclasses`, `numpy`, `scipy.integrate`. Header carries the Apache License 2.0 notice (the source LICENSE is Apache 2.0; copyright line reads "Copyright 2026 Michael Zargham"). `test_no_forbidden_imports_and_license` passes. Observation O-3 on the copyright line. |
| R-4 | met | `-k evaluate_design`: 1 passed (three designs, `FAST_SIM`, all four attributes finite and > 0, flags present, mass = 3 wheels + star tracker + 0.5 asserted). `evaluate_design` returns the four attributes, `settled`, `momentum_ok`, `torque_saturated_frac` (plus `peak_momentum_nms`). In the committed CSV all four attributes are finite and > 0 (min of mass 6.0, pointing 4.4e-4). |
| R-5 | met | `-k pointing`: 1 passed. Read `pointing_budget`: `theta_ss = degrees(4(tau_gg + tau_srp)/Kp)`, RSS with `stAccuracy/3600` via `np.hypot`. Test asserts strictly decreasing over an 8-point geomspace grid across `KP_RANGE` and `min > floor`. SRP is only in `pointing_budget` (analytic), not in `simulate_adcs` dynamics, as the approved default says. Sensitivity: with the SRP term removed (trial c) the monotone test still passes, and only the CSV reproduction test fails (see Trials), so no test pins the SRP magnitude directly (O-2). |
| R-6 | met | `-k effort`: 1 passed. `summary()`: `control_effort = np.trapezoid(||tau_ctrl||, t)` over the whole simulated horizon, an N·m·s quantity; `momentum_ok = peak_wheel_momentum <= max_momentum` (read in `evaluate_design`); peak momentum is returned as a column but excluded from the four attributes; test asserts the flag equals the comparison. |
| R-7 | met | `-k sampling`: 1 passed. Read `sample_designs`: `SeedSequence(seed).spawn(n)`, per-design `default_rng(child)`, wheel and star tracker by uniform integer, Kp and Kd via `exp(uniform(log range))`, masses times `exp(0.10 * normal)`. Test checks equal seeds give equal frames, `sample_designs(50, 7).iloc[:20]` equals `sample_designs(20, 7)`, a different seed differs, a `Generator` input is reproducible, ranges hold, log-median near range centre, and lognormal sigma 0.10 +-0.01 on 2000 draws. Trial b confirmed the prefix check catches an n-dependent seed. |
| R-8 | met | `generate_dataset.py --help` lists `--n --seed --out --workers --force --fast` (defaults per scope; `multiprocessing.Pool`). Ran `--n 40 --seed 0 --workers 4 --out <scratch>/t.csv`: "wrote 40 designs", 4.4 s wall (about 110 s extrapolated for 1000, consistent with "a few minutes"). Re-ran without `--force`: "exists; skipping (use --force to regenerate)". The first 40 rows of the fresh file equal the committed CSV rows (max settling difference 0.0, max relative effort difference 0.0). `test_generator_cli_skip_and_force` passes. |
| R-9 | met | `-k reproduc`: 2 passed (this selector also matches `test_sampling_reproducible_and_prefix_stable`; the regeneration test is `test_dataset_reproducible_first_20`, 5 s). Committed CSV: 1000 rows, columns equal the `COLUMNS` list, `design_id` monotone. Test compares categoricals and flags exactly, continuous columns at rtol 1e-6, settling within 0.5 s, all as the scope states. |
| R-10 | met | `-k dataset_summary` prints `not settled: 0.040, momentum violated: 0.047, log10 spreads: {'settling_time_s': 1.24, 'pointing_error_deg': 1.15, 'adcs_mass_kg': 0.43, 'control_effort': 2.23}`. My own pandas figures agree: settled 0.960, `momentum_ok` 0.953; three attributes exceed one decade (settling, pointing, effort), mass does not (nine discrete values 6.0 to 16.0 kg). The test asserts `settled.mean() > 0.5` (scope: "most"). Unsettled rows carry settling = 900 (all 40 of them), as designed. Momentum violations are concentrated in the small wheel class (`momentum_ok` 0.863 for small, 1.000 for medium and large). |
| R-11 | met | `extended_design_space.sysml` read: `package ExtendedDesignSpace`; `WheelClass` with small/medium/large instances, `StarTrackerGrade` with coarse/medium_st/fine, `ControlGains`, `MassPerturbation`, four `attribute def`s (`settling_time_s`, `pointing_error_deg`, `adcs_mass_kg`, `control_effort`), header "Documentation only: this file is not parsed or executed", values match the code, flags listed in a comment. `test_sysml_documentation_file` passes. Not parsed by a SysML tool (none in scope); the test's name check is loose (see O-4). |
| R-12 | met | `uv run pytest`: 342 passed, 3 skipped (20 s; includes other packages' tests). `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 58 files already formatted. `uv lock --check`: Resolved 153 packages. `git diff --stat` for the three WP4 commits: `examples/adcs/{adcs_sim.py, design_space.py, generate_dataset.py, extended_design_space.sysml, data/adcs_designs.csv}`, `tests/test_adcs_case.py`, `pyproject.toml` (one line: `pythonpath = [".", "src", "examples/adcs"]`). Nothing else. |
| R-13 | met | `git log --format=%B 932bbe4^..HEAD \| grep -ciE 'co-authored-by\|generated with'` returns 0; same over `--all` returns 0. `git log --format='%an %cn'` over `932bbe4^..HEAD`: all author and committer "Michael Zargham". |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-7 exist at the stated paths | met | See Deliverables. |
| R-1 to R-13 pass as checked, with evidence | **not met** | R-2 is not met as written (G-1); the other twelve are met. |
| Non-goals untouched | met | See below. |

## Definition of good (judgment, not gated)

- **Honesty of the case: met.** Hardware is labelled illustrative in the module docstrings and the SysML header; `# CHANGED:` marks every departure; the quantized and censored settling time, the unenforced momentum and the stratified mass are stated in `design_space.py` and `adcs_sim.py` docstrings and carried as the `settled`, `momentum_ok`, `peak_momentum_nms` columns.
- **Attribute tension: partly met.** From the committed data (Spearman): control effort rises with Kp (+0.82) while pointing error falls with Kp (-0.52), so effort against pointing is a real trade (corr -0.43). Fine star trackers cost mass and buy pointing (pointing/mass -0.27, floor 0.00044 deg for fine against 0.0042 for coarse). Settling and pointing are positively correlated (+0.27) because both improve with Kp: not in tension with each other. Settling against mass is nearly uncorrelated (-0.08); mass is a pure function of the two hardware classes (nine values, no dependence on gains or on the panel/antenna perturbation), so the frontier in mass is structural strata, as the scope says. A frontier exists but the settling-mass edge is weak. Honest, and not a defect against the scope.
- **Physics.** SRP (1e-5 N·m) enters only the analytic pointing budget; the gravity-gradient part of the budget is about 6e-9 N·m, so SRP dominates the steady error by roughly three orders of magnitude and pointing is effectively 1/Kp plus the star-tracker floor, independent of Kd and wheel class. This is what the approved default intends (continuous in Kp) but readers should know that "gravity gradient" in the budget is negligible next to the SRP term. The simulation clips torque per axis rather than by vector norm (source behaviour, kept). Peak momentum is the norm of the cumulative integral of the clipped command, observed not enforced, as stated.
- **Speed and reproducibility: met.** About 0.11 s per design at 4 workers; the first 40 designs regenerate bit-identically on this machine.
- **Recognisably the source: met.** Equations and structure follow `analysis/numerical.py`; the port reproduces its pins to within 0.04 s.

## Trials (fresh checkout, restored with `git checkout -- <file>`)

- **(a) Parallel-axis term removed** (`panel = panel_cm`): 6 failed, 8 passed: `test_inertia_baseline` ("assert 143.38..."), all four `test_regression_pins`, and `test_dataset_reproducible_first_20`.
- **(b) Seed logic made n-dependent** (`SeedSequence(seed + n)`): 2 failed: `test_sampling_reproducible_and_prefix_stable` and `test_dataset_reproducible_first_20`.
- **(c) SRP removed from `pointing_budget`**: only `test_dataset_reproducible_first_20` failed (1 failed, 13 passed); no unit test pins the SRP term (O-2).
- Working tree clean for my files after each trial; none committed.

## Outside the scope

- **Out-of-scope changes:** none in the WP4 commits (see R-12). `pyproject.toml` changed in the one permitted line.
- **Non-goals touched:** none. No estimator or conditioning code, no notebook, no rdflib/sympy/opensysml/Flexo import, no change to the source repo (I ran its simulator read-only with bytecode writing disabled; `git status` there is clean), no `wheel_momentum_bound_symbolic`, no docs site. The status table and README of `work-packages/` were not edited by WP4 commits (scope's commit plan mentioned a status table; not required by a deliverable).

## Observations (not counted as failures)

- **O-1.** `docs/superpowers/notes/adcs-port.md` ("Baseline (1, 10) ≈ 201.6 s") carries the same wrong number as the scope; it is the likely origin of the error (spec section 8 itself does not state it). Not edited by this review.
- **O-2.** No test asserts the SRP term directly (for instance `theta_ss` at a given Kp equal to 4(tau_gg + 1e-5)/Kp); removal is caught only by the CSV reproduction test.
- **O-3.** The licence header names "Copyright 2026 Michael Zargham" under the Apache 2.0 text. The source repo is Apache 2.0 with its own LICENSE; the port is a derivative of that code, so the source copyright holder's notice may belong in the header. R-3 says "carries the source LICENSE notice"; the Apache text is carried, the source's copyright attribution is not named.
- **O-4.** The SysML test's name check is loose (`name.replace(...)` fallbacks), so it would pass with some names missing; my reading of the file found all names present.
- **O-5.** Default `pytest` (testpaths `tests`) does not collect the `adcs_sim` doctest; it runs only when `examples/adcs` is named.
- **O-6.** `-k reproduc` also selects the sampling test; harmless.
- **O-7.** Mass has only nine distinct values; any downstream conditioning (WP3/WP7) must treat it as stratified, as the scope already says.
- **O-8.** The (4,30) pin in the test is 77.97, the scope says 78.0; both within the +-0.2 band.

## Open decisions (for the supervisor)

- **G-1.** R-2 states the baseline (Kp, Kd) = (1, 10) settling time as about 201.6 s within +-0.5 s. The source repo (its own tests, notebook, probe findings, and my independent run) gives 310.6 s, the port gives 310.6 s, and 201.6 appears nowhere in the source. R-2 therefore cannot be met as written; the test pins 310.6 +-0.5 with a comment awaiting this decision. Options: (a) amend R-2 and `adcs-port.md` to 310.6 s (+-0.5, or +-0.2 as in the source); (b) other, for example drop the baseline pin from R-2. Dispositions: accept as is / fix before acceptance / follow-up work package. Pending.
- **G-2** (one item, observations O-1 to O-8): accept these as is, or pick any to act on. Options: accept as is / fix before acceptance / follow-up work package. Pending.

## Gap dispositions

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 R-2 baseline value (201.6 vs 310.6) | pending | Decision loop not yet run. A scope amendment is needed whatever the choice, because R-2 as approved is unsatisfiable. |
| G-2 Observations O-1 to O-8 | pending | Decision loop not yet run. |

## Recommendation

Provisional: do not recommend acceptance yet, because R-2 is not met as written and a good-enough item (R-1 to R-13 pass) therefore fails on the letter of the scope. The cause is an error in the scope (and the adcs-port note), not in the delivered work: the port reproduces the source's three tight pins and its baseline value (310.6 s), all other requirements are met with evidence, nothing is out of scope, and the trials show the tests catch an inertia error and an n-dependent sampler. Once G-1 is amended (option a is the minimal change) the recommendation becomes: recommend acceptance with the listed observations noted.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
