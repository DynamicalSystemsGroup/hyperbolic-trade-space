# WP4 — Scope of work: ADCS case generator (simulation port, design space, dataset)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/posynomial-invariant-form` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP4-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4-decisions.md`, after the review report `work-packages/WP4-review.md` |

## Purpose

The case study (WP7) needs a realistic, reproducible trade-space dataset for a geostationary satellite attitude
determination and control system (ADCS): a design space with two categorical hardware choices and continuous
gains, a numerical simulator that evaluates each design into four competing attributes, and a committed seeded
dataset. WP4 builds these from the numpy/scipy parts of `/Users/z/Documents/GitHub/adcs-lifecycle-demo` as described
in `docs/superpowers/notes/adcs-port.md` and spec §8. It is independent of the estimator (WP2, WP3): it
produces attributes, and conditioning them into metrics is WP3/WP7.

## Goals

- G1. A numerical ADCS simulator ported from the source repo (rigid-body quaternion dynamics, gravity gradient, PD control, composite inertia) that reproduces the source's known results.
- G2. A design space (wheel class, star-tracker grade, Kp, Kd, mass perturbations) with a seeded sampler and an `evaluate_design` function that returns the case's four attributes and feasibility flags.
- G3. A reproducible dataset generator and a committed seeded dataset of 1000 designs.
- G4. A SysML v2 text file documenting the extended design space.
- G5. Tests that pin the port to the source (inertia, settling-time regression pins), check reproducibility, and exercise `evaluate_design`.

## Non-goals

- No estimator, preconditioning, analysis or plotting code, and no notebook (WP2, WP3, WP7); attributes are produced raw and unconditioned.
- No dependency on rdflib, sympy-based SysML tooling, opensysml or Flexo; only numpy, scipy and pandas, which are already dependencies.
- No change to the source repository; code is copied and adapted, with its LICENSE notice carried in the header of `adcs_sim.py`.
- No calibration to real hardware: wheel and star-tracker class values are labelled illustrative.
- No port of `wheel_momentum_bound_symbolic` (known units issue in the source note) and no symbolic analysis.
- No documentation pages or site (WP8).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/adcs/adcs_sim.py`: port, `BASELINE`, `inertia_tensor`, `pointing_budget`, `make_config`, simulator | G1 |
| D-2 | `examples/adcs/design_space.py`: `WHEEL_CLASSES`, `STAR_TRACKERS`, `KP_RANGE`, `KD_RANGE`, `sample_designs`, `evaluate_design`, `FAST_SIM` | G2 |
| D-3 | `examples/adcs/generate_dataset.py`: command-line generator | G3 |
| D-4 | `examples/adcs/data/adcs_designs.csv`: committed dataset, 1000 designs, seed 0 | G3 |
| D-5 | `examples/adcs/extended_design_space.sysml`: documentation only | G4 |
| D-6 | `tests/test_adcs_case.py` | G1–G3, G5 |
| D-7 | `work-packages/WP4-decisions.md` (approval record) | G1–G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | `inertia_tensor` at the baseline parameters equals (327.14, 107.48, 303.45) kg·m² within 0.01 | `uv run pytest tests/test_adcs_case.py -k inertia` |
| R-2 | The simulator reproduces the source regression pins for the 10° X-axis slew, 360 s horizon, tight tolerances: (Kp, Kd) = (4, 30) → 78.0 s, (8, 30) → 87.4 s, (4, 25) → 120.5 s, each within ±0.2 s, and the baseline (1, 10) → 310.6 s within ±0.5 s (amended, see Amendment 1) | `-k regression` |
| R-3 | `adcs_sim.py` has no import of rdflib, sympy, opensysml or Flexo and carries the source LICENSE notice in its header | `grep` and inspection |
| R-4 | `evaluate_design(row, t_end=900, ...)` returns `settling_time_s`, `pointing_error_deg`, `adcs_mass_kg`, `control_effort` and the flags `settled`, `momentum_ok`, `torque_saturated_frac`, with every attribute finite and strictly positive for a designs batch; mass is 3 wheels + star tracker + IMU | `-k evaluate_design` (three designs with `FAST_SIM`) |
| R-5 | Pointing error is the root-sum-square of the steady-state disturbance error (gravity gradient plus a constant solar-radiation-pressure torque of about 1e-5 N·m, divided by an effective stiffness proportional to Kp) and the star-tracker floor, so that it varies continuously with Kp | `-k pointing`: error decreases monotonically with Kp over a grid and exceeds the star-tracker floor |
| R-6 | Control effort is ∫‖τ_ctrl‖ dt over the simulated slew; peak wheel momentum is reported as a feasibility flag (`momentum_ok` = peak ≤ the wheel class's maxMomentum), not as an attribute | `-k effort`; inspection |
| R-7 | `sample_designs(n, rng_or_seed)` draws wheel class and star-tracker grade uniformly, Kp and Kd log-uniformly in `KP_RANGE`, `KD_RANGE`, and perturbs panel and antenna mass by about 10 % lognormal, with a child seed per design; the same seed gives the same designs and design i does not depend on n | `-k sampling` |
| R-8 | `generate_dataset.py` supports `--n 1000 --seed 0 --out data/adcs_designs.csv --workers --force --fast`, uses multiprocessing, and skips generation when the output exists unless `--force` | `uv run python examples/adcs/generate_dataset.py --help`; run it to a temporary path |
| R-9 | `data/adcs_designs.csv` has 1000 rows with the configuration columns, the four attributes and the flags; regenerating a subset reproduces the committed rows: for the first 20 designs against the committed file: categorical columns and flags equal, settling time within 0.5 s, continuous columns within rtol 1e-4 except `torque_saturated_frac` within rtol 2e-2 (amended, see Amendment 1); and regenerating 40 designs twice on the same platform gives identical rows (exact) | `-k reproduc` (regenerates 20 designs against the committed file and 40 designs twice) |
| R-10 | The dataset behaves as the case needs: all four attributes vary over at least one order of magnitude of spread in log space for at least three of them, `settled` is True for most designs, and the fraction not settled and the fraction violating `momentum_ok` are reported by the test | `-k dataset_summary` |
| R-11 | The SysML file parses as text, is non-empty, names the wheel-class and star-tracker-grade choices and the four attributes, and states that it is documentation only | inspection |
| R-12 | Suite, linters and lock pass and nothing outside scope changed: `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `git diff --stat` shows only `examples/adcs/`, `tests/test_adcs_case.py`, `pyproject.toml` (pytest path option only) and `work-packages/` | run the commands; inspect the diff |
| R-13 | No AI attribution lines; commits authored as Michael Zargham | `git log` grep returns 0; CI check |

## Amendment 1 (after the first review, approved at the acceptance gate)

What changed and why, per scope-of-work section 6; the supervisor's choice "310.6 pin; per-column tolerances" is recorded verbatim in `work-packages/WP4-decisions.md` ("Scope amendment 1"). Both requirements were wrong as originally written and originated in the plan, not in the delivered work.

- R-2: the baseline (Kp, Kd) = (1, 10) pin changes from 201.6 s to 310.6 s ± 0.5 s. The source repository's own tests pin 310.6 s, no source file contains 201.6, and the review reproduced 310.626 s by running the source simulator.
- R-9: cross-machine reproducibility changes from rtol 1e-6 to rtol 1e-4 on continuous columns, with rtol 2e-2 for `torque_saturated_frac` only, plus exact reproduction on the same platform (40 designs regenerated twice). The GitHub runner differs from the generating machine by up to 2.6e-5 relative on `control_effort` and 6.1e-3 on `torque_saturated_frac`; exact cross-machine equality of an ODE-solver output is not achievable.
- `docs/superpowers/notes/adcs-port.md` was corrected from 201.6 to 310.6 by the driver. Nothing else changes: goals, non-goals, deliverables and the definitions of good and good enough are as approved.

## Definition of good

- The case is honest about what it is: illustrative hardware, documented physics additions, stratified mass (hardware-class gaps are structural), and the pitfalls of the source (settling time quantized by `max_step` and censored at `t_end`; momentum observed not enforced) are visible in docstrings and flags.
- The four attributes are in genuine tension (faster settling and better pointing cost mass and effort) so that a frontier exists to be learned.
- Generation is fast enough to rerun (about a few minutes for 1000 designs with workers) and exactly reproducible per design.
- The simulator code stays recognizably the source's, with the changes marked.

## Definition of good enough

- Deliverables D-1 to D-7 exist at the stated paths.
- R-1 to R-13 pass as checked, with evidence in the review report.
- Non-goals untouched (no estimator or conditioning code, no notebook, no forbidden dependencies).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

All marked *(default)* where they appear; the supervisor approves or changes the list as one item. The first group is the spec §8 modelling defaults, which the spec says to confirm at this scope gate; the supervisor's approval of this list confirms them.

- Physics additions *(spec §8 default, confirmed by approving this list)*: constant solar-radiation-pressure disturbance torque of 1e-5 N·m (GEO-typical, illustrative); total pointing error = RSS(θ_ss, star-tracker floor); control effort = ∫‖τ_ctrl‖ dt over the slew as a continuous power/energy proxy; peak wheel momentum as a feasibility flag, not a metric; hardware class values labelled illustrative.
- Hardware classes *(spec §8 default)*: `WHEEL_CLASSES` small/medium/large = (maxTorque N·m, maxMomentum N·m·s, mass kg) = (0.05, 2, 1.5), (0.1, 4, 2.5), (0.2, 8, 4.0); `STAR_TRACKERS` coarse/medium/fine = (accuracy arcsec, mass kg) = (15, 1.0), (5, 2.0), (1.5, 3.5).
- Attribute computation split *(default)*: `settling_time_s`, `control_effort`, peak momentum and `torque_saturated_frac` come from the simulation; `pointing_error_deg` comes from the analytic `pointing_budget` (θ_ss = 4(τ_gg,max + τ_srp)/Kp following the source's effective-stiffness form, RSS with the star-tracker floor stAccuracy/3600 deg), so SRP does not enter the simulated dynamics.
- Scenario *(default)*: 10° slew about X as in the source; dataset horizon `t_end=900` s; `max_step=0.5` for the dataset; `FAST_SIM` (coarser `max_step`, shorter `t_end`) used only in tests; pins at the source's 360 s horizon with tight tolerances.
- Settling time: last time the error exceeds 1 % of the initial error, as in the source; `settled` is False when that time reaches `t_end` (censored value `t_end` kept in the column) *(default)*.
- Design-space ranges *(default)*: `KP_RANGE = (0.5, 16.0)`, `KD_RANGE = (5.0, 60.0)`, log-uniform; wheel class and star-tracker grade uniform over three values each.
- Perturbation *(default)*: panel mass and antenna mass multiplied by independent lognormal factors with σ = 0.10 (median 1); all other baseline parameters fixed.
- Sampling and seeds *(default)*: `numpy.random.SeedSequence(seed).spawn(n)` gives one child seed per design, so design i is independent of n; `sample_designs(n, rng)` accepts a seed integer or a `Generator` (a Generator draws the child seeds from its bit stream).
- Dataset columns *(default)*: `design_id, seed, wheel_class, st_grade, Kp, Kd, panel_mass_kg, antenna_mass_kg, settling_time_s, pointing_error_deg, adcs_mass_kg, control_effort, settled, momentum_ok, torque_saturated_frac, peak_momentum_nms`.
- Generator command line *(default)*: argparse flags `--n` (1000), `--seed` (0), `--out` (`examples/adcs/data/adcs_designs.csv`), `--workers` (cpu count − 1), `--force`, `--fast`; a `multiprocessing.Pool` maps `evaluate_design` over designs; rows are written sorted by `design_id`; CSV written with a fixed float format (`%.9g`).
- Tests import the example modules by adding `examples/adcs` to the pytest `pythonpath` in `pyproject.toml` *(default)*; the reproducibility test regenerates 20 designs with the default (not fast) settings and takes a few seconds *(default)*.
- Regression-pin tolerance for the baseline run is ±0.5 s *(default)*; its value is 310.6 s after Amendment 1.
- Tolerance choices after Amendment 1 *(default)*: rtol 1e-4 is about 4 times the largest CI-observed relative difference on the continuous columns (2.6e-5 on `control_effort`); `torque_saturated_frac` is a fraction of time steps and moved 6.1e-3 on CI, so its rtol is 2e-2 (about 3 times the observed difference). Same-platform exactness means two regenerations of the same 40 designs in one process on one machine are identical.
- `evaluate_design` input is a mapping or `pandas.Series` of the configuration columns and returns a `dict` *(default)*.
- Adapted code is marked with `# CHANGED:` comments where it departs from the source; `make_config_from_params` is replaced by the numeric `make_config(params, Kp, Kd, wheel, ...)` using `inertia_tensor` *(default)*.
- SysML text *(default)*: a `package ExtendedDesignSpace` with part definitions for the wheel classes, star-tracker grades and gains, four attribute definitions, and a header comment "documentation only".
- Ruff configuration unchanged; the examples directory is linted by `ruff check .` *(default)*.
- Commits prefixed "WP4: "; one commit per module with its tests, then dataset, then status table and decisions file; files `work-packages/WP4-decisions.md` and `WP4-review.md` follow the WP1 format *(default)*.
- Order *(default)*: `adcs_sim.py` and its pins, `design_space.py`, `generate_dataset.py`, the committed CSV, the SysML text; TDD; main stays green on every push.

## Open decisions (for the supervisor)

None at problem level: spec §8 and the adcs-port note answer them, and the spec's modelling defaults that it asks to be confirmed at this gate are the first group of the defaults list, approved or changed as part of that one item. The Agent's defaults list above is the one item for the supervisor to approve or change at the scope gate.
