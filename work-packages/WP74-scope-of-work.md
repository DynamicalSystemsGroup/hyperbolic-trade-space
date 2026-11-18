# WP74 — Scope of work: the requirement-usage type name, both forms accepted

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under the external review's disposition (2026-11-16) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/tradespace`; branch `dev`, after WP73 and before 0.1 |
| **Approval record** | Finding 7 of `work-packages/review/external-review-2026-11-16.md` and its disposition ("accept both type names wherever the type is matched"), recorded in `driver-log.md` (2026-11-16, 17:40) |
| **Acceptance record** | The driver's run of the checks below and read of the diff, as proxy |

## Purpose

An OpenSysML maintainer's review of `dev` (finding 7): three tests expect a `verify requirement` statement to
come back from `query` typed `SatisfyRequirementUsage`. That is what opensysml 0.12.1, the pinned client, returns;
on the engine's `develop` branch the same statement is typed `VerifyRequirementUsage`, so the tests fail there and
will fail on the next release. The same type name is matched in `scripts/sysml_project.py` and in
`examples/adcs/experiments/probes.py`. The repository pins a behaviour of one engine version where it should
accept what the standard library yields under either.

## Goal

- G1. Every place the repository matches the type of a requirement usage accepts both `SatisfyRequirementUsage`
  and `VerifyRequirementUsage`, through one named constant; a test plants a minimal element of each kind and sees
  it accepted; the probe record's kind counts are stable under either name.

## Non-goals

No change to the model (`cubesat.sysml`, `views.sysml`, `cubesat_tradespace.sysml`); no change to what the engine is
asked (the queries, the verification calls, the API-JSON projection); no engine or client upgrade (the lock keeps
0.12.1); no other finding of the external review.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `REQUIREMENT_USAGE_KINDS`, defined once in `examples/adcs/experiments/probes.py` (the probe that records what `query` returns), used at every match of what `query` returns: `tests/test_model_checking_v2.py`, `tests/test_system_model_v2_r1.py`, `probes.py` itself. The satisfy loop of `scripts/sysml_project.py` `behavioural` stays on `SatisfyRequirementUsage`: the API JSON it reads keeps satisfy statements and verify statements apart (the verify side is read from the verification cases), so widening it would count verify statements as satisfy statements on a corrected engine (the driver's correction at acceptance) | G1 |
| D-2 | The planted test in `tests/test_system_model_v2_r1.py`: a stand-in for the client's `query` surface holding one requirement usage of each kind, read by the same reader the engine-backed tests use | G1 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | No match of either type name outside the constant | `grep -rn "SatisfyRequirementUsage\|VerifyRequirementUsage" --include='*.py' .` reads one definition and membership tests only |
| R-2 | The planted element of each kind is accepted | `uv run pytest -q tests/test_system_model_v2_r1.py -k requirement_usage` |
| R-3 | The engine-backed tests and the probe record hold at 0.12.1 | `uv run pytest -q -k "model_checking or system_model_v2 or probes"` |
| R-4 | The register and the fast suite pass | `uv run pytest -q -k test_the_register_holds`; `uv run pytest -q -m "not slow and not paper"` |
| R-5 | Lint and format clean | `uv run ruff check .`; `uv run ruff format --check .` |
| R-6 | No attribution line; no metanarration | the grep; a read |

## Definition of good

A later opensysml that types a `verify requirement` by its own name changes nothing in the tests, the views or the
probe record; the only place that knows the two names is the constant.

## Definition of good enough

R-1 to R-6 met on one commit; the driver's acceptance as proxy.

## Definition of done

Good enough met; landed on `dev` with its index row.

## Open decisions

None.

## Agent's defaults

- The constant lives in `experiments/probes.py`, the module that records what the client returns, not in
  `cubesat_model.py`: the experiment ledger hashes that file for four recorded runs, and a line added there drifts
  them (`tests/test_experiments.py`, `tests/test_v2_data.py`), which no correction package re-records.
- The pinned engine cannot emit `VerifyRequirementUsage`, so the plant is a stand-in for `query`, not a loaded
  model; the engine-backed tests cover the first name as before.
- One unit, in a worktree on `dev`.
