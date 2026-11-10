# WP23 — Decision records (the model-realism loop)

Origin: `WP22-decisions.md`, "The model-realism loop" (the supervisor's words of 2026-11-09, 20:35 and 20:50,
verbatim; "0.1 waits for it"). Scope draft: `WP23-scope-of-work.md` (7ffb719). The driver triages the draft's open
decisions; the supervisor answers only those that change the problem, one at a time.

## OD1 and OD2, how launch cost enters (2026-11-09, 21:05)

**Driver's question (popup):** a launch cost proportional to mass is, in the log metrics the fit reads, the same
column as total mass shifted by a constant, so it never trades against mass. Options: MoE on mass, no new column /
Launch cost replaces mass / Both columns. **Supervisor (mzargham), verbatim:** "MoE on mass, no new column".

**Disposition.** Total mass stays the traded metric (an MoP). Launch cost is the MoE the model ties to it: cost =
rate × total mass with an illustrative $/kg constant labelled like the model's other constants (OD1: illustrative; a
cited price is a later claims item if he wants one), and a launch-budget requirement reads it. No `launch_cost` column;
the interface contract changes only by the slew-time column. The draft's G2, R-2 and defaults follow.

## OD7, metrics beyond the present ones (the driver, under the mandate)

The loop proposes candidates the model already computes, each added only on the supervisor's decision at the gate.
Adding metrics is a problem change; proposing them is the loop's work.

## OD8, the Agent's defaults (the driver, under the mandate)

Approved as one item, with `launch_cost` struck (OD2) and `SlewBandRequirement` folding with `SlewTimeRequirement`
into `SettledRequirement` as drafted.

## OD3 to OD6, the four thresholds (2026-11-09, 21:10)

**Driver's question (popup):** who sets the thresholds for pointing error, control effort, peak slew power and total
mass (with launch cost as its MoE)? Options: Loop proposes, you approve / I give values now / MoEs, no bounds.
**Supervisor (mzargham), verbatim:** "Loop proposes, you approve".

**Disposition.** The modeller loop proposes an illustrative threshold for each of the four from the baseline
configuration (the baseline's value with a stated margin, or a stated rationale), labelled illustrative like the
model's other constants; the four values go to the supervisor at the data gate, one popup, before the swap; the
requirements are built on the proposed values during the loop so the views and the coverage table are complete, and
re-pinned to his values if he changes them.

## Scope gate (2026-11-09, 21:10)

No open decision remains (OD1 to OD8 above; OD9 is not a decision: his direction of 2026-11-09 covers conclusion
changes from dropping slew time, "expect changes of this order", so the gate lists and explains moves). **Approved
for execution by the driver under the mandate**, with the draft amended to these decisions (no `launch_cost`
column; launch cost the MoE on mass with a launch-budget requirement; thresholds proposed by the loop and approved
by the supervisor at the gate). The supervisor accepts the delivery at the data gate.

## Supervisor input for the coupling check (2026-11-09, 22:05)

**Supervisor (mzargham), verbatim** (while reading a stale staged build of the paper): "while i look at it and think
hey "maybe we should have 2 to 3 battery options with different weights, storage capacities, peak charge rate and
peak power, etc" in order to make sure our sysmlv2 model provides a fully coupled set of paths from the config values
to the metrics of interest without missing anything that is obviously coupled. i realize i may just be looking at an
out of date model."

**Disposition (the driver).** Into WP23's first round as an input to the coverage and coupling table (G1, G3): the
battery is today a tuned continuous capacity (20 to 200 Wh) with no mass or power-rate coupling of its own; the loop
assesses 2 to 3 battery alternatives (swap) each carrying mass, capacity, peak charge rate and peak power, so that
one configuration choice reaches total mass and launch cost, energy balance, eclipse reserve and peak slew power
through the model's own calcs; the general test behind it: every configuration value has its obviously coupled paths
to the metrics present in the model, and the table says so. The loop reports what it adopted and why.

**Supervisor (mzargham), verbatim (22:15), on "fully coupled":** "by the way i don't mean fully coupled like all to
all, i just meant connect graph. think of this in terms of the coupling variables between subsystems in the MDAO lit"

**Disposition.** The coverage and coupling table is a graph, not a matrix of everything against everything:
configuration values feed subsystem calculations, subsystems exchange named coupling variables (mass to launch cost
and to the slew dynamics; power generated and stored to the energy balance and the peak power available to the
slew), and the metrics are read off the subsystems; the test is connectivity, every configuration value reaching at
least one metric and every metric reached, with the coupling variables between subsystems named as the MDAO
literature names them (a design structure matrix or XDSM reading). The MDAO paper unit (P-11) and this table cite
the same family.

## The data gate overnight (2026-11-09, 22:30)

**Driver's question (popup):** how should WP23's data gate behave while he sleeps (it needs his approval of the four
illustrative thresholds and then the swap)? Options: Proceed, I review after / Regenerate, hold the swap / Wait for
me. **Supervisor (mzargham), verbatim:** "Proceed, I review after".

**Disposition.** The loop regenerates on the proposed thresholds and the swap is made at the gate on the driver's
verification (the comparison report with every moved number and changed conclusion explained; both platforms
green); the four values and the report go under "Waiting for the supervisor" in the driver log for his review on
waking; if he changes a value the gate re-runs with it. Downstream re-tests (reader rounds at depths B and C, the
figure redraws on the new data) proceed on the swapped model.

## The proposer's reach on the settling-time view (2026-11-10, 00:50; the driver, under "Proceed, I review after")

The gate's regeneration stopped at the check designs: `check_designs.Proposer.draw` finds fewer than three
reachable, separated holes with REACH = 0.35, the constant WP7 set for the slew-time view; the proposer's
four-metric view now carries the settling time (D-3), and the same failure occurs on the old data with the new
view, so it is the view change, not the new data. The PM's options: raise REACH to the smallest round value that
yields three proposals (0.6); re-derive it by WP7's own rule if the record states one; drop the proposals and keep
the three hand-written check designs (a paper change); restate the criterion relative to the pool (a method change).

**Decision.** REACH is set by a stated rule, not by the number that makes the method produce output. First, WP7's
record: if it states how 0.35 was set, apply that rule to the new view and record the value. If it states none, the
rule is defined now and recorded: the reach is a stated quantile of the pool's nearest predicted distances to the
holes on the view in use (the agent names the quantile from what REACH means in the check, the radius within which a
seeded configuration is close enough to be proposed), and the rule is checked on the old slew-time view: a rule that
returns about 0.35 there is the rule WP7 used in effect; a rule that does not shows 0.35 was arbitrary, and the
paper's check section then says the radius is a chosen constant, set by the stated rule, for both views. If the rule
yields fewer than three holes on the new view, the check reports the number it yields (two proposals are a result,
not a failure), and the paper's sentence follows the number; the proposals are not dropped and the criterion is not
restated. One constant and one sentence of rule in `check_designs.py`, recorded here, the gate re-run. The
supervisor sees it with the gate's comparison.

**Facts found under the rule (2026-11-10, 01:20; the gate agent via the PM).** WP7 set REACH = 0.35 with no stated
rule (67eea92, a comment only); on the old slew-time view the smallest reach giving three separated holes was
0.339, so 0.35 sat just above the method's own minimum; the first-300 nearest distances were min 0.161 and tenth
percentile 0.444 on the old view (six holes within 0.35, about the second percentile) against min 0.484 and tenth
percentile 0.717 on the new view (none within 0.35; three separated holes need 0.58); old and new data agree to the
third decimal on the new view, so the change is the metric swap. The rule adopted: a stated quantile of the pool's
nearest predicted distances to the 300 most isolated holes, checked on the old view and applied to the new; the
proposer no longer raises below three proposals; the paper's check sentence follows the count. For the
supervisor: the earlier 0.35 was a constant that happened to work, which the record now says.

## The data gate: the comparison read, two calls (2026-11-10, 02:25; the driver under "Proceed, I review after")

D-9 is `work-packages/swap-evidence.md`, "WP23 data gate: old v2 ... against new v2", read by the driver; its method
separates causes (old data at ten metrics, old data at nine, new data at nine). Every moved number has a cause: the
column change (slew time out) changes the contending sets and the leaders; the event-detected settling time moves
the K = 3 shares by at most the jitter's size; flags, feasible sets and certificate statuses are unchanged.

**The swap.** Accepted on the comparison and the Linux verdict (8507bd9 green in three shards); the Mac tier 2
verdict on the same head is owed before the call is final (the watcher's worktree had gone dirty and was cleaned at
02:20). A red Mac reopens the call. With it, the WP23 model is the model of record, the nine-metric datasets are the
data of record, and the paper moves onto them.

**The per-term report on the primary regime at K = 3 (the PM's question).** The report refuses because one term
(share 0.034) has fewer near-frontier rows than its guard of ten; it refuses on the old data at nine metrics too, so
the cause is the column change. Decision: the fit is reported from the estimator (three terms, their exponents, cells,
shares and certificate: the model's contending sets exist for all three), and the association reading (the
analysis, which needs rows) is drawn per term where the rows meet the guard, with the thin term's panel replaced by
its reason in one sentence ("too few near-frontier designs for an association reading: n of ten"). No third band
(a loosened band is a tuning), no K = 2 in its place (a substitution would add where the rule says cut). The
generators `num-k-sweep`, `fig-tensions-k3` and Appendix D.3 are adapted to per-term availability. The case claim
"one term blends the subsystems' trade-offs into a single tension; three terms separate the contending sets" is
read from the exponents and stands with sharper content: one term in the primary regime no longer sees the control
trade-off at all (control effort 1e-17); three terms find it in a term of its own. For the supervisor's review.

**The swap is final (2026-11-10, 02:45).** The Mac tier 2 watcher is green on 241c63d (2166 passed, all checks),
a head that contains the gate unit 8507bd9; Linux was green on 8507bd9 in three shards. The WP23 model is the model
of record, the nine-metric datasets the data of record; the paper moves onto them (the fifth PM's first unit).

## Acceptance review (f5a63c2): the driver's gap dispositions (2026-11-10, 05:20)

The review recommends acceptance with ten gaps. Dispositions: G-1 the amended reading of R-5 is accepted (the
model's section-4 `SlewTime` names are closed-form calcs; the frozen generator keeps its outputs by the scope's
non-goal). G-2 the two paper view copies, authorized at the push, are a recorded exception, not a drift. G-3 is a
real gap: two fresh P2 and P3 cold reads of the committed views at revision 6, image first, before acceptance is
final. G-4 is closed by subtraction: round 2's pair is not regenerated; round 3 and the gate carry the record. G-5
is a real gap: the before-and-after texture record is D-9's "Changed conclusions" item on the zero-exponent sets
(it stays unchanged: three metrics in the primary regime, one in the baseline) and the review cites it; the case
prose's outcome paragraph is rewritten on the data of record in the paper's next prose unit. G-6: the decision is
the one recorded with the PM on 2026-11-10, 03:20: an entry is added when the corpus uses its term; MoE and MoP
enter with the paper's Section 8 sentence. G-7 is a real gap: `case-model.md` joins the vocabulary tool's corpus and
its two stem findings are fixed. G-8 the files outside the blast radius are accepted as recorded. G-9 the gate
folder is the record of the gate at its commit, which its README says. G-10 is fixed at 126e1ea.

**Decision:** WP23 accepted, final when G-3, G-5 and G-7 land (three small units, one push each), recorded here
with their hashes. The supervisor's items (the four thresholds, the two redundancies, the proposals' feasibility)
stay under "Waiting for the supervisor".
