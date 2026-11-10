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

## The model-realism loop (2026-11-09, 20:35; the supervisor, back at his computer)

**Supervisor (mzargham), verbatim,** looking at the behavioural view: "i have an idea. we can make mass an explicit
metric in our trade since the total mass directly impacts cost to launch into space. i think if we introduce a cost to
launch where lower mass is cheaper and more mass is more expensive we should ensure all the decision elements were
considering effect a least one metric. also i think we should more generally use this chart as guide to do a loop to
tighten up the model so the demonstrative case feels more realistic. the very fact that way the system is specified and
assembed (the other plantuml diagram) and the way that system maps to measurable MoEs and MoPs which in turn cab be
used to populate the data we want to learn trade-offs within is key to show this method is practically useful for real
engineering work not just a toy technique"

**Driver's question (popup):** does the 0.1 candidate wait for the model-realism loop (launch cost on mass, every
decision element reaching a metric, every traded metric reaching a requirement or a stated MoE, the datasets and paper
numbers regenerated once on the tightened model), or does 0.1 ship with the current case? Options: 0.1 waits for it /
Launch cost only / After 0.1. **Supervisor, verbatim:** "0.1 waits for it".

**Disposition.** A new package, WP23 (the model-realism loop), scoped by the PM for the driver's approval, guided by
the behavioural view: a launch cost that reads total mass (lower mass cheaper), a requirement or stated MoE for every
traded metric, a coverage check that every swap and tune reaches at least one metric, the modeller loop with the two
views re-read cold each round, and the interface contract amended if the dataset's columns change. WP16 Amendment 2
keeps its event-detection work but its regeneration step waits for WP23's model, so the datasets and the paper's
numbers regenerate once. Step 3f in `release-candidate.md`.

**Supervisor (mzargham), verbatim (2026-11-09, 20:50), reviewing Figure 1's exponent heatmap and the behavioural view
together:** "reviewing this and this together it seems pretty clear we need to refine out sysmlv2 model so our trade
space actually matches what the model is trying to accomplish this means a bunch more metrics explicitly included but
tied to our actual requirements. / the whole thing is actually pretty simple: a space of configs on one side (how its
constructed) and a space of metrics on the other (how its evaluated). that clarity is why we wanted a sysmlv2 model in
the first place. once thats done we should see more texture int the grayscale plot attached"

**Disposition, for WP23's scope.** The two pictures are the package's diagnostic pair, read from either side of the
seam: the heatmap (the K = 1 exponent of each metric across τ) shows four metrics at zero at every temperature
(settling time, power margin, eclipse reserve, peak slew power), so the fitted facet never trades them; the
behavioural view shows which traded metrics no requirement reads. Definition of good: the configuration space (how
the system is constructed: the assembly view's swaps and tunes) and the metric space (how it is evaluated: MoEs and
MoPs tied to the model's requirements) are each explicit in the model, and the trade space matches what the model is
trying to accomplish: more metrics included, each tied to a requirement. His expectation, "more texture" in the
heatmap after regeneration, is the hypothesis the regenerated figure checks; it is not a target the model is tuned to
(a metric at zero exponent in one facet is a legitimate reading, the n-lemma, when it is explained). Model, fit and
analysis stay apart: the model changes, the fit is re-run as is, the analysis reads the result.
