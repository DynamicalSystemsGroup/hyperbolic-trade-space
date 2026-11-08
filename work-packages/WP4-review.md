# WP4 — Review report (third pass)

| | |
|---|---|
| **Scope of work** | `work-packages/WP4-scope-of-work.md`, including Amendment 1 |
| **Scope approval verified** | The project has no PRs, so the recorded act is `work-packages/WP4-decisions.md`: "Scope approval" (supervisor mzargham, verbatim "double check with the github cli but then let's move forward", with the later approval-record note that the CI check was done first) and "Scope amendment 1" (verbatim choice "310.6 pin; per-column tolerances"). Both records are typed by the agent, so this review cannot confirm the chat itself. "Acceptance" reads "pending". |
| **Work reviewed** | `main` at `ea3105b` (WP4 delivery `932bbe4`, `9227f47`, `3864a8a`; tolerance commits `234ee2c`, `b95a0d4`; amendment `b138b6d`; test change `ef79e83`). Only review reports changed after `4ce27d4`, where my checks were run. |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP4-decisions.md`, after this report |

A complete rerun from step 1 against the amended scope, by a reviewer who built none of WP4. Every command was run in this session with `unset VIRTUAL_ENV`.

## Does Amendment 1 apply the recorded choice?

The supervisor's verbatim choice is "310.6 pin; per-column tolerances". The amendment (`b138b6d`) sets R-2's baseline to 310.6 ± 0.5 s and R-9 to per-column tolerances, and the driver corrected the port note. The two reasons it gives are correct: the source repo pins 310.6 (checked in the second pass), and CI differs from the CSV by up to 2.6e-5 on `control_effort` and 6.1e-3 on `torque_saturated_frac`. These match the values quoted in the test comments, but I did not re-observe them on CI.

Items the choice does not literally fix, which the agent set and listed under Agent's defaults ("Tolerance choices after Amendment 1"):
- the numbers rtol 1e-4 and 2e-2;
- the same-platform exactness clause on 40 designs.

The justification holds: 1e-4 is about 4 times 2.6e-5, and 2e-2 is about 3 times 6.1e-3. Nothing else in the scope changed (goals, non-goals, deliverables and good enough are as approved). The wording "per-column tolerances" is faithful. The specific values and the exactness clause are the agent's, and the supervisor should know that when accepting (see G-1).

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `examples/adcs/adcs_sim.py` exists; defines `BASELINE`, `inertia_tensor`, `pointing_budget`, `make_config`, `SRP_TORQUE_NM`; departures marked `# CHANGED:`. |
| D-2 | met | `examples/adcs/design_space.py` with `sample_designs`, `evaluate_design`, `FAST_SIM` and the class tables (tests below use them). |
| D-3 | met | `examples/adcs/generate_dataset.py`; `--help` run. |
| D-4 | met | pandas: shape (1000, 16), 0 NaN, `design_id` increasing, columns match the default column list. |
| D-5 | met | `examples/adcs/extended_design_space.sysml` (read in earlier passes; `test_sysml_documentation_file` passes). |
| D-6 | met | `tests/test_adcs_case.py`: 16 tests, all pass. |
| D-7 | met | `work-packages/WP4-decisions.md` holds the approval and the amendment records; acceptance pending. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `-k inertia`: 1 passed. `pytest examples/adcs`: 1 passed (doctest). |
| R-2 | met (amended) | `-k regression`: 4 passed, including (1, 10) -> 310.6 ± 0.5 and the three ±0.2 pins. The second pass reproduced the source simulator at 310.626, 77.966, 87.396 and 120.498 s. `grep 201.6` finds the number only in the amendment text, the decisions record, the port note's correction sentence and the test comment, plus unrelated CSV digits. |
| R-3 | met | `test_no_forbidden_imports_and_license` passes (full suite). Imports in `adcs_sim.py` are dataclasses, numpy, scipy only. |
| R-4 | met | `-k evaluate_design`: 1 passed. pandas: four attributes finite and > 0 for all 1000 rows. |
| R-5 | met | `-k pointing`: 2 passed (monotone-in-Kp test and the new SRP test). |
| R-6 | met | `-k effort`: 1 passed. |
| R-7 | met | `-k sampling`: 1 passed. Trial B confirms the prefix check bites. |
| R-8 | met | `--help` lists `--n --seed --out --workers --force --fast`. `--n 40 --seed 0 --workers 4 --force` to a scratch path: "wrote 40 designs". A second run without `--force`: "exists; skipping (use --force to regenerate)". |
| R-9 | met (amended) | `-k reproduc`: 2 passed (`test_dataset_reproducible_first_20`, `test_sampling_reproducible_and_prefix_stable`). `test_dataset_same_platform_exact` (selected by `-k same_platform`, not by `-k reproduc`; it passes in the full suite) regenerates 40 designs twice with `check_exact=True`. In the test, `_20` has categoricals and flags equal, settling atol 0.5, eight continuous columns rtol 1e-4, `torque_saturated_frac` rtol 2e-2, matching the amended text. My own regeneration of 40 designs vs the CSV: max relative difference 0.0 on every float column on this machine. CI at `ef79e83` (run 42439886689) and at the head is **success**. This shows the tolerance is wide enough on CI; it does not show it is tight (I could not observe the CI differences, only that CI passes). Scope text says "`-k reproduc`" regenerates 20 and 40 designs; the exactness test is not selected by that string (O-6). |
| R-10 | met | `-k dataset_summary`: 1 passed. pandas: settled 0.960, `momentum_ok` 0.953; log10 spreads settling 1.24, pointing 1.15, mass 0.43, effort 2.23 (three above one decade). |
| R-11 | met | Test passes; file read in earlier passes. |
| R-12 | met | `uv run pytest`: **381 passed, 3 skipped** (42 s). `ruff check .`: All checks passed. `ruff format --check .`: 60 files already formatted. `uv lock --check`: Resolved 153 packages. WP4 commits touch only `examples/adcs/`, `tests/test_adcs_case.py`, one line of `pyproject.toml`, `work-packages/`, plus `docs/superpowers/notes/adcs-port.md` (the driver's correction named in Amendment 1; `docs/` is not in R-12's listed set, see Outside the scope). |
| R-13 | met | Over `932bbe4^..HEAD --all`, grep for `co-authored`, `generated with`, `claude`: 0 matches. All 23 commits in the range have author and committer Michael Zargham. `gh run list`: latest runs success, including head `ea3105b`. |

## Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| Deliverables D-1 to D-7 exist | met | See Deliverables. |
| R-1 to R-13 pass as checked, with evidence | met (against the amended text) | All thirteen met above. |
| Non-goals untouched | met | See below. |

## Definition of good (judgment, not gated)

Unchanged from the second pass in substance. Honesty of the case is met (illustrative hardware, `# CHANGED:` marks, `settled`, `momentum_ok`, `peak_momentum_nms`). Attribute tension is partly met (effort against pointing and mass against pointing are in tension; settling against mass is weak; settling and pointing both improve with Kp). Speed is met (about 0.11 s per design). Reproducibility is exact on one platform and within the amended tolerances across platforms. Recognisably the source is met.

## Trials (never committed; restored with `git checkout -- <file>`; `git status` clean)

- **A. Parallel-axis term removed** (`panel = panel_cm`): 6 failed (`test_inertia_baseline`, all four regression pins, `test_dataset_reproducible_first_20`), 10 passed.
- **B. Seeds made n-dependent** (`SeedSequence(seed + n)`): 2 failed (`test_sampling_reproducible_and_prefix_stable`, `test_dataset_reproducible_first_20`), 14 passed.
- **C. SRP removed from the pointing budget** (`(tau_gg + SRP_TORQUE_NM) / Kp` -> `tau_gg / Kp`): 2 failed, 14 passed. The failures are `test_dataset_reproducible_first_20` and the **new** `test_pointing_budget_srp_term` (`assert 0.0013...`). The new test fails on its own; in the second pass the dataset test was the only detector.

## Outside the scope

- **Out-of-scope changes:** none in the WP4 commits beyond the allowed set, with these notes. `docs/superpowers/notes/adcs-port.md` (one-line correction, `eae37e0`) is outside R-12's list but is named and approved in Amendment 1. WP4 commits also touch `work-packages/README.md`, `WP2-decisions.md` and `WP5-decisions.md` (inside `work-packages/`; shared status and decision records). Commits `b138b6d` and `ef79e83` touch only the scope file and the test file.
- **Non-goals touched:** none. No estimator or conditioning code, no notebook, no forbidden dependency, no `wheel_momentum_bound_symbolic`, no docs site; source repo untouched.

## Observations (not counted as failures)

- **O-1.** The note's 201.6 s error: resolved (note corrected to 310.6 by `eae37e0`).
- **O-2.** No SRP magnitude test: resolved (`test_pointing_budget_srp_term`; trial C).
- **O-3.** The licence header names "Copyright 2026 Michael Zargham" under the Apache 2.0 text; the source holder's notice may belong there. Open.
- **O-4.** The SysML test's name check has loose fallbacks. Open.
- **O-5.** Default `pytest` collects the `adcs_sim` doctest only when `examples/adcs` is named. Open.
- **O-6.** `-k reproduc` selects the sampling test and does not select the new same-platform exactness test, whereas R-9's "checked by" says `-k reproduc` covers both regenerations. Open, trivial.
- **O-7.** Mass has nine discrete values; WP3/WP7 conditioning must treat it as stratified. Open.
- **O-8.** Pin value 77.97 against scope 78.0: both inside the ±0.2 band. Open, trivial.
- **O-9.** Regeneration is bit-identical on this machine, and only within the amended tolerances on CI, so downstream work should read the committed CSV rather than regenerate it. Now documented by Amendment 1. Open as a downstream note.
- **O-10 (new).** The tolerance numbers and the exactness clause are agent-chosen under the supervisor's "per-column tolerances"; the exactness test uses `workers=1` (the dataset itself is made with a Pool), so it checks solver determinism, not pool scheduling. I did not observe the CI deltas myself.

## Open decisions (for the supervisor)

- **G-1 (observations, one item).** O-3 to O-10 above remain; O-1 and O-2 are resolved. Notably O-3 (copyright line), O-6 and O-10 (the amendment's agent-chosen values). — options: accept as is / fix before acceptance / follow-up work package.

## Gap dispositions

Decision records go in `work-packages/WP4-decisions.md` (no PRs in this project).

| Gap | Disposition | Reason or follow-up |
|---|---|---|
| G-1 observations O-3 to O-10 | pending | |

## Recommendation

**Recommend acceptance with the listed gaps noted**, because all of D-1 to D-7 and R-1 to R-13 are met against the amended scope (381 passed, 3 skipped; ruff, format and lock clean; CI green at the head), the amendment applies the recorded choice "310.6 pin; per-column tolerances" and its stated justification matches the CI-observed 2.6e-5 and 6.1e-3, the new SRP test is shown to fail when SRP is removed, no attribution lines exist, and no out-of-scope files were touched beyond those the amendment names. The only open item is the observations (G-1), which affect neither a good-enough item nor a non-goal.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
