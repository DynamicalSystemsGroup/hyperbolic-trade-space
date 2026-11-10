# WP22 — Decision records (the system model, two views)

Origin, boundary and escalation rule: `WP15-decisions.md` (the supervisor's words of 2026-11-09, verbatim).

## Gate decision on the model swap (2026-11-09, 19:50; the driver's call under the mandate, for the supervisor's review)

Evidence: `WP22-review.md`, "Gate comparison report" (produced in a clean worktree at 3cd4c5a, toolkit v0.12.0,
`REQUIRE_OPENSYSML=1`): the old file is byte-unchanged since WP15 and its hash is the ledger's; the new file
`cubesat_r1.sysml` passes the same strict load, check, lint and `verify --solve`; on the regenerated designs of both
datasets the outputs are byte-identical to the old model's (analysis agreement 1.8e-16, flags and verdicts equal), so
the swap moves no committed number; it adds four requirements and restates one, with their verification structure and
the two views.

The supervisor's conditions (`WP15-decisions.md`): the modelling loop bounded away from the core machinery (met: the
seam is the dataset; the paper reads the ledger and names no model file); "don't swap the new model in in place of the
old model blindly" (met: this report is the comparison, not a blind swap; the results did not change, so no earlier
version is implicated).

**Decision:** swap. WP22d as listed in the report (path constants, tests re-pinned to the new hash, ledger entries
superseding the five old ones, generated provenance rows regenerated in the container, `cubesat_r1.sysml` becomes
`cubesat.sysml` with the old file in history only, the views generator's output becomes the model's views). One unit,
one push, with the regeneration and its tests in the same push; the tier 2 watcher and a Linux dispatch verify it.
WP16 Amendment 2 (event detection and regeneration) then runs on the swapped model. Open items R3-2 and R3-3 of the
picture loop are accepted as the PM recommends; WP22b (the four thresholds) and WP22c stay with the supervisor.
