# WP4 — Review report (second pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4-scope-of-work.md` |
| **Scope approval verified** | The project has no PRs (`gh pr list --state all` is empty), so the recorded act is the verbal approval in `work-packages/WP4-decisions.md`, section "Scope approval" (commit `bcfe110`): supervisor mzargham, verbatim "double check with the github cli but then let's move forward", 2026-11-08. The record states the physics additions (SRP in the analytic pointing budget only, RSS pointing error, effort as the integral of the torque norm, momentum as a flag, illustrative hardware) were put to the supervisor and that open decisions were none. The record is typed by the agent, so this review cannot confirm the chat itself. The "Acceptance" section reads "pending". |
| **Work reviewed** | `main` at `b95a0d4`. WP4 commits `932bbe4`, `9227f47`, `3864a8a` (delivery) and two later tolerance commits `234ee2c`, `b95a0d4`. Diff base `1c71306`. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4-decisions.md`, after this report |

Fresh review from step 1, replacing the first-pass report (`087f2ed`). Every command below was run in this session with `unset VIRTUAL_ENV`. CI status of the current head `b95a0d4`: `gh run list` shows run 42439164704 **success** (38 s). Earlier runs at `3864a8a`, `087f2ed`, `a60b57c` and several WP2 commits are failures (the WP4 ones from the cross-platform reproducibility test; see G-2).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/adcs_sim.py` (286 lines): `BASELINE`, `inertia_tensor`, `pointing_budget`, `make_config`, `SimConfig`, `simulate_adcs`, `run_step_response`, `SRP_TORQUE_NM`; departures marked `# CHANGED:`. |
| D-2 | met | `examples/adcs/design_space.py` (138 lines): `WHEEL_CLASSES`, `STAR_TRACKERS`, `KP_RANGE`, `KD_RANGE`, `sample_designs`, `evaluate_design`, `FAST_SIM`. |
| D-3 | met | `examples/adcs/generate_dataset.py` (85 lines). |
| D-4 | met | `examples/adcs/data/adcs_designs.csv`: pandas shape (1000, 16), columns equal the default column list, no NaN, `design_id` strictly increasing. |
| D-5 | met | `examples/adcs/extended_design_space.sysml` (44 lines). |
| D-6 | met | `tests/test_adcs_case.py` (214 lines, 14 tests). |
| D-7 | met | `work-packages/WP4-decisions.md` holds the approval record; acceptance "pending". |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `-k inertia`: 1 passed. `uv run pytest examples/adcs`: 1 passed (module doctest). |
| R-2 | **not met as written; met as delivered** (G-1) | `-k regression`: 4 passed. Independent run of the source simulator (`/Users/z/Documents/GitHub/adcs-lifecycle-demo/.venv`, `analysis.numerical.run_step_response` with `analysis.load_params.load_params()` plus Kp, Kd; X-axis 10 deg slew, 360 s; bytecode writing off; source `git status` clean afterwards): (1,10) -> **310.626 s**, (4,30) -> 77.966 s, (8,30) -> 87.396 s, (4,25) -> 120.498 s. Source `tests/test_sysml_evidence.py` line 26 pins `r["x"] == approx(310.6, abs=0.2)` for `ev.INITIAL = (1, 10)`; `jaxa_notebook.ipynb` prints 310.6 s five times; `sysml/probe/FINDINGS.md` and `run_probe.py` give 310.63. `grep -rnE '201\.6'` over the whole source repo (excluding `.venv`, `.git`, `uv.lock`) returns nothing; 310.6 appears in six places. So the scope's "baseline (1, 10) ≈ 201.6 s ±0.5" is a scope error (the same wrong number sits in `docs/superpowers/notes/adcs-port.md`), not a competing physical result. The port test pins 310.6 ±0.5 (comment in `tests/test_adcs_case.py` lines 33-34: "scope R-2 says 201.6; source repo pins 310.6; amendment pending"). The three tight pins match the scope and source (port test 77.97, 87.4, 120.5 within ±0.2). As delivered the port reproduces the source's own results; as written the requirement cannot be satisfied by any faithful port. |
| R-3 | met | Imports in `adcs_sim.py`: only `dataclasses`, `numpy`, `scipy.integrate` (plus `__future__`). Header carries the Apache 2.0 notice; `test_no_forbidden_imports_and_license` passes. Observation O-3. |
| R-4 | met | `-k evaluate_design`: 1 passed (three designs, `FAST_SIM`; four attributes finite and positive; mass = 3 wheels + star tracker + IMU; flags present). In the CSV all four attributes are finite and > 0 (pandas). |
| R-5 | met | `-k pointing`: 1 passed. `pointing_budget` reads `degrees(4 (tau_gg + SRP_TORQUE_NM)/Kp)` RSS `stAccuracy/3600` via `hypot`; test asserts strictly decreasing over a Kp grid and above the floor. `grep` shows `SRP_TORQUE_NM` is used only in `pointing_budget`, never in the dynamics, as the approved default says. |
| R-6 | met | `-k effort`: 1 passed. `control_effort` is the trapezoid integral of the torque norm over the horizon; `momentum_ok` is peak <= wheel `maxMomentum`; peak momentum is a column, not one of the four attributes. |
| R-7 | met | `-k sampling`: 1 passed (equal seeds equal frames; `sample_designs(50, 7)` prefix equals `sample_designs(20, 7)`; ranges; lognormal sigma 0.10 within 0.01; Generator input). Trial B confirms the prefix check bites. |
| R-8 | met | `--help` lists `--n --seed --out --workers --force --fast`. Fresh regeneration `--n 40 --seed 0 --workers 4` to a scratch path: "wrote 40 designs", 4.5 s wall. A second run without `--force` printed "exists; skipping (use --force to regenerate)". The 40 fresh rows equal the first 40 committed rows (max relative difference 0.0 in settling, effort, saturated fraction, pointing, on this machine). `test_generator_cli_skip_and_force` passes. |
| R-9 | **not met as written; met as delivered** (G-2) | `-k reproduc`: 2 passed (includes `test_sampling_reproducible_and_prefix_stable`; the regeneration test is `test_dataset_reproducible_first_20`, about 5 s). Scope text: continuous columns within rtol 1e-6, settling within 0.5 s. The test now uses `rtol=3e-2, atol=1e-12` for all nine continuous columns (`tests/test_adcs_case.py`, comment lines citing CI differences of about 2.6e-5 in `control_effort` and about 6.1e-3 in `torque_saturated_frac`). The scope's own checking method with 1e-6 failed on CI (runs at `3864a8a` and later were failures until `b95a0d4`). On this machine regeneration is bit-identical, so 1e-6 passes locally and fails on ubuntu-24.04: the committed CSV is not exactly reproducible across platforms, a fact the scope did not anticipate. The test uses one tolerance for every column, so the tight columns (all except `torque_saturated_frac`, observed up to 2.6e-5) lose about four orders of magnitude of drift sensitivity because of the one loose column. Categoricals and flags are still compared exactly; settling within 0.5 s unchanged. |
| R-10 | met | `-k dataset_summary`: not settled 0.040, momentum violated 0.047, log10 spreads settling 1.24, pointing 1.15, mass 0.43, effort 2.23. My pandas figures: settled 0.960, `momentum_ok` 0.953, three attributes above one decade; `momentum_ok` by wheel class small 0.863, medium 1.0, large 1.0. |
| R-11 | met | File read: `package ExtendedDesignSpace`, wheel classes, star-tracker grades, gains, four `attribute def`s, header "Documentation only". `test_sysml_documentation_file` passes (its name check is loose, O-4). |
| R-12 | met | `uv run pytest`: 366 passed, 3 skipped. `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 60 files already formatted. `uv lock --check`: Resolved 153 packages. Per-commit `git show --stat`: `932bbe4` touches `adcs_sim.py`, `pyproject.toml` (one line, `pythonpath = [".", "src", "examples/adcs"]`), `tests/test_adcs_case.py`; `9227f47` touches `design_space.py` and the test; `3864a8a` touches the CSV, SysML, `generate_dataset.py` and the test. All inside the allowed set. |
| R-13 | met | `git log 932bbe4^..HEAD --format=%B \| grep -ciE 'co-authored\|generated with'` returns 0; same with `--all` returns 0. All 15 commits in the range have author and committer Michael Zargham. CI on the head is green. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-7 exist at the stated paths | met | See Deliverables. |
| R-1 to R-13 pass as checked, with evidence | **not met as written** | R-2 and R-9 are not met as written (G-1, G-2); both are met as delivered once the scope text is amended; the other eleven are met. |
| Non-goals untouched | met | See below. |

## Definition of good (judgment, not gated)

- **Honesty of the case: met.** Illustrative hardware in docstrings and the SysML header; `# CHANGED:` marks departures; quantized and censored settling, unenforced momentum and stratified mass are visible in docstrings and the `settled`, `momentum_ok`, `peak_momentum_nms` columns.
- **Attribute tension: partly met.** Spearman on the committed data: control effort rises with Kp while pointing error falls with Kp (effort vs pointing -0.43); fine star trackers cost mass and buy pointing; settling vs pointing is positive (+0.27) because both improve with Kp, so they are not in tension with each other; settling vs mass about -0.08, and mass takes nine discrete values determined only by the two hardware classes. A frontier exists (effort vs pointing, mass vs pointing) but the settling-vs-mass edge is weak. Honest, and not a defect against the scope.
- **Physics.** SRP (1e-5 N·m) enters only the analytic pointing budget. The gravity-gradient contribution is far smaller (order 1e-9 N·m), so pointing is effectively 1/Kp plus the star-tracker floor, independent of Kd and wheel class. That is what the approved default intends, but it means the "tension" between settling and pointing is carried by Kp alone.
- **Speed and reproducibility: met locally, partly across platforms.** About 0.11 s per design at 4 workers; bit-identical regeneration on this machine; not exact on CI (G-2).
- **Recognisably the source: met.** Reproduces the source pins to within 0.04 s.

## Trials (restored with `git checkout -- <file>`, never committed; `git status` clean)

- **A. Parallel-axis term removed** (`panel = panel_cm`): 6 failed, 8 passed (`test_inertia_baseline`, all four regression pins, `test_dataset_reproducible_first_20`).
- **B. Seeds made n-dependent** (`SeedSequence(seed + n)`): 2 failed, 12 passed (`test_sampling_reproducible_and_prefix_stable`, `test_dataset_reproducible_first_20`).
- **C. SRP term removed from `pointing_budget`**: 1 failed, 13 passed (only `test_dataset_reproducible_first_20`, even at rtol 3e-2); no unit test pins the SRP term (O-2).

## Outside the scope

- **Out-of-scope changes:** none in the three delivery commits (R-12). The two later commits `234ee2c` and `b95a0d4` each touch only `tests/test_adcs_case.py` (5 lines each: tolerance 1e-6 -> 1e-3 -> 3e-2 and an explanatory comment), verified with `git show --stat`. They change a tested tolerance that the scope fixes, which is why they are a gap (G-2), not out-of-scope files.
- **Non-goals touched:** none. No estimator or conditioning code, no notebook, no forbidden dependency, source repo untouched (read-only runs, clean `git status`), no `wheel_momentum_bound_symbolic`, no docs site.

## Observations (not counted as failures)

- **O-1.** `docs/superpowers/notes/adcs-port.md` carries the same wrong 201.6 s baseline as the scope (part of G-1). Spec section 8 does not state it.
- **O-2.** No test asserts the SRP magnitude directly.
- **O-3.** The licence header names "Copyright 2026 Michael Zargham" under the Apache 2.0 text; the source copyright holder's notice may belong there.
- **O-4.** The SysML test's name check has loose fallbacks; my reading of the file found all names.
- **O-5.** Default `pytest` now collects the `adcs_sim` doctest only via the path option; passes when named (`pytest examples/adcs`).
- **O-6.** `-k reproduc` also selects the sampling test; harmless.
- **O-7.** Mass has nine distinct values; WP3/WP7 conditioning must treat it as stratified.
- **O-8.** The scope's "(4,30) -> 78.0" and the test's 77.97 are both inside the ±0.2 band.
- **O-9.** The CSV reproduces bit-for-bit only on the generating platform; the committed CSV is the authoritative dataset, and downstream work should read the CSV, not regenerate it.

## Open decisions (for the supervisor)

- **G-1.** R-2 as written (baseline (1, 10) ≈ 201.6 s ±0.5) is wrong; the source, and so the port, give 310.6 s. Delivered: the test pins 310.6 ±0.5 and the other three pins as written. Scope amendment options: (i) amend R-2 to 310.6 ±0.5 and correct `docs/superpowers/notes/adcs-port.md` (line "Baseline (1, 10) ≈ 201.6 s") to 310.6; (ii) amend R-2 only and leave the note; (iii) drop the baseline pin from R-2. — options: accept as is / fix before acceptance / follow-up work package. **Disposition: pending.**
- **G-2.** R-9 as written (rtol 1e-6 on continuous columns) fails on CI because of platform differences (up to 2.6e-5 in `control_effort`, 6.1e-3 in `torque_saturated_frac`). Delivered: single rtol 3e-2 for all nine continuous columns (CI green). Scope amendment options: (i) keep rtol 3e-2 for all continuous columns and amend R-9 to say so; (ii) amend R-9 to a tight rtol (about 1e-4, above the observed 2.6e-5) for all columns except `torque_saturated_frac`, and 3e-2 (or an absolute tolerance) for that column only, which needs a small test change; (iii) require same-platform exactness only (not CI-checkable). — options: accept as is / fix before acceptance / follow-up work package. **Disposition: pending.**
- **G-3 (observations, one item).** O-1 to O-9 (notably O-2 no SRP pin test, O-3 copyright line, O-9 platform-dependent regeneration). — options: accept as is / fix before acceptance / follow-up work package. **Disposition: pending.**

## Gap dispositions

Decision records go in `work-packages/WP4-decisions.md` (no PRs in this project).

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 R-2 baseline 201.6 s vs source 310.6 s | pending | |
| G-2 R-9 tolerance 1e-6 vs delivered 3e-2 | pending | |
| G-3 observations O-1 to O-9 | pending | |

## Recommendation

Provisional on the dispositions above: **recommend acceptance with the listed gaps noted**, because the delivered work is complete, within scope, and correct against the source (all four source pins reproduced independently; lint, lock, tests and CI green on `b95a0d4`; no attribution lines; no out-of-scope files; trials caught each injected fault). Two requirements, R-2 and R-9, are not met as literally written because of scope errors and a CI-observed platform effect the scope did not anticipate; both are met as delivered, and need a supervisor-decided scope amendment (G-1, G-2) before the good-enough item "R-1 to R-13 pass" can be called met. If the supervisor prefers R-9 amended to per-column tolerances (G-2 option ii), a small test change is separate work and the whole review reruns.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
