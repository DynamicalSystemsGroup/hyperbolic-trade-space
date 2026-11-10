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

## Two calls on the gap units (2026-11-10, 06:35; the driver)

- G-3: revision 7 of the behavioural view (type size, the legend's kinds, the `totalMass` label, the derived-from
  line) gets one fresh cold read, image first, by a P3 reader before WP23 is final; the author's own check is not a
  review (the standing order of 2026-11-09). If nothing blocks, WP23 is final at that hash.
- G-17's new clause cites the settling time's 1.5e-10 relative move from a decision record. A decision record is
  not a generated value: either the gaps generator computes that number from the data of record in the container
  (then it is a generated value and may be printed) or the clause is narrowed to no number ("moves at the rounding
  level under the integrator's jitter"). The stream chooses; no number from a record.

**G-3 closed; WP23 final at revision 8 (2026-11-10, 07:10).** The fresh P3 read of revision 7 (b0a9a92) read every
label and legend entry; one finding is on the drawing: the analysis box's line "No slew for pointing error, total
mass" beside "returns 8 of 9" reads as "not returned" until the caption. Decision: (b), a revision-8 unit fixes
that one line of box text (generator, views, the paper's byte copy); WP23 is final at that hash on the author's
700 px check, a one-line wording change needing no further cold read. The arrows finding (read backwards, then
right through the legend in the image) is no change. With this, every gap of the acceptance review is disposed and
**WP23 is accepted**; the supervisor's three items stay under "Waiting for the supervisor".

**WP23 final hash: db59365** (revision 8 of the behavioural view; the analysis box reads "returns 8 of 9 metrics,
computed with no slew: pointing error, total mass"; the paper's byte copy updated). Accepted by the driver under the
mandate, 2026-11-10, 07:25.

## The four thresholds (2026-11-10, 07:55; the supervisor, from the pass-fraction tables in `WP23-review.md`)

**Driver's popup, four questions with the candidates and the share of feasible designs each admits (primary /
baseline).** **Supervisor (mzargham), verbatim:** peak slew power "2.6 W, all small and medium"; pointing error
"0.0085 deg, admits 95 % of primary"; control effort "0.059 N.m.s, admits 90 % of baseline"; launch budget
"90,643 USD (15.11 kg, admits 95 %)".

**Disposition.** The model's four requirements take these values (PeakSlewPowerRequirement 2.6 W, admitting every
small and medium wheel and no saturating large wheel, 62.2 % / 67.3 %; PointingErrorRequirement 0.008495 degree,
94.9 % / 63.7 %; ControlEffortRequirement 0.05922 N·m·s, 58.9 % / 90.0 %; LaunchBudgetRequirement 90,643 USD at
the illustrative 6,000 USD/kg, 15.107 kg, 94.9 % / 95.6 %), each labelled as his choice from the loop's ladder and
no longer "illustrative 20 %". The datasets do not change (the four are requirements read against the metrics,
not feasibility flags of the generation); the model, its toolkit gates, the views, the coverage table, the case
prose's threshold sentences and the register rows regenerate in the container in one unit; the gate's pass
fractions are the recorded reading of what each admits.

## The two metric redundancies (2026-11-10, 08:00)

**Driver's popup:** eclipse reserve and depth of discharge are one quantity; power margin and energy balance are
both affine in the generated power. Options: keep all nine and state it / drop one of each pair / drop one pair
only. **Supervisor (mzargham), verbatim:** "if the redundancy is a modelling issue then you clean it up. otherwise
i think the correct version in the full case is to try identifying the redundancy and simplying the analysis to be
an outcome of the analysis. do a short research spike to see which makes more sense. note that putting this in
the full case analysis is not the same as forcing into the paper narrative which we're trying to keep tight"

**Disposition.** A short spike, one agent, one report (`work-packages/WP23-rounds/spike-redundancy.md`), per pair:
is the redundancy a modelling issue (two metrics or requirements defined from one quantity, or a power model
linear in one tune with constant loads, which a cleaner model would not have) or a property of the system in its
ranges that the analysis should identify and simplify as an outcome (the association reading at ±1, the exponents
splitting across collinear columns, a stated step of the case analysis that merges them)? For each: the evidence
from the model's definitions and the data of record, what a model clean-up would change, what the analysis
outcome would look like in the full case analysis (Appendix D and the docs' case pages), and a recommendation with
plain options. The paper's narrative is kept tight: whatever is chosen lands in the full case analysis, not as a
new thread of the paper.

## Requirements and the trade study: two research spikes (2026-11-10, 08:05)

**Driver's popup on the proposals that fail the depth-of-discharge requirement** (keep and say it / train on
feasible rows / drop). **Supervisor (mzargham), verbatim:** "i want us to do the trade study with and without the
data for the infeasible designs. again these are research spikes to decide how we want to present the models in
the paper. in practice requirements analysis may result in changes to the requirements themselves. the trades in
the metrics can help inform that. we don't want to over complicate our paper but our case is exploratory and we're
learning the various ways HTS can help us. my gut is that we want to see the model fit without the requirements
imposed then see how it changes if we had preimposed the requirements. this is also akin to looking at
constrained versus unconstained optimization. i am headed to take my daughter to school so you should continue in
autonomous model but do some guided research spikes to make sense of how our HTS model helps us with trade studies
including different ways of using it alongside a set of threshold requirements; including how it might help us if
the requirements are deemed infeaible. might we use it to justify a request to relax a requirement"

**Disposition.** Two spikes, the driver's, read-only on the repository, one report each under
`work-packages/WP23-rounds/spikes/`: (A) the fit with and without the infeasible designs (all designs; the
feasible set; the set that also passes his four thresholds), K = 1 and K = 3 in both regimes, what changes and how
to present it as constrained against unconstrained in the full case analysis; (B) the fitted model alongside
threshold requirements: what the elasticities say about the cost of meeting each requirement at the frontier, which
requirements exclude the near-frontier designs, whether a set of requirements is jointly infeasible on the
frontier, and the form of a case for relaxing one, with worked numbers from the data of record. The proposals'
question is answered through (A): the check designs are read in both settings. Both spikes feed the full case
analysis (Appendix D, the docs' case pages); the paper's narrative stays tight, with at most one candidate
paragraph for the supervisor's review.

## The redundancy spike's answer and the driver's calls (2026-11-10, 08:20; `WP23-rounds/spike-redundancy.md`)

- **Eclipse reserve and depth of discharge: a modelling issue.** Both calcs are functions of the same two
  quantities (capacity C and eclipse demand D: D/C and 0.3·C − D, the 0.3 baked into the metric), and the two
  requirements are the same inequality on every one of the 2,000 designs. Clean-up, option A1: depth of discharge
  stays the traded metric and its requirement; the eclipse-reserve calc and requirement leave the model; eight
  traded metrics; contract amendment; one regeneration of the datasets and the paper's numbers; and the hidden
  dependency the spike found is honoured: `dod_ok` enters the case's flags, since today the 131 failing designs
  leave the fit only through the reserve's positivity.
- **Power margin and energy balance: a property of the system in its ranges**, two distinct power-budget quantities
  sharing one source (generated power, linear in panel span with constant loads per cell), exact only within a
  wheel-and-tracker cell and ordering oppositely at a named pair of designs. Analysis outcome, option B1: the case
  reports the association of every pair of traded metrics over the feasible designs, names pairs at |Spearman| ≥
  0.99 as one axis (the eclipse pair would have passed, the power pair does not at 0.98), and the exponent reading
  sums a named pair per term; it lives in Appendix C.5, D.3 and D.4 and one sentence of the docs' case page; no
  model, data or contract change; the paper's narrative unchanged.
- **Sequencing.** A1 rides with the thresholds unit as one model change and one regeneration after WP24 push 4,
  so the datasets and the paper regenerate once more, not twice; spikes A and B read the nine-metric data of record
  and their findings carry over (the reserve carries no exponent in the fits of record). B1 lands in the same
  paper regeneration. The supervisor sees both at his review; this is the driver's call under his rule.

## Spike B, requirements and the fit (2026-11-10, 08:35; `WP23-rounds/spikes/spike-B-requirements-and-the-fit.md`)

The answer to "might we use it to justify a request to relax a requirement": yes, in a bounded form. The fit prices a
requirement at the frontier (the elasticities of the contending metrics along the surface, and which near-frontier
designs the requirement excludes), so a request carries three numbers: what meeting the requirement costs at the
frontier in the other metrics, how many near-frontier designs a relaxation admits, and how much the best attainable
contending metric improves among them. On the case: the four thresholds are not jointly infeasible on the frontier
(66 % of the primary band and 44 % of the baseline band pass all four); the argument has teeth in the baseline
regime (pointing error 0.0085 degree excludes 42 of 77 near-frontier designs; relaxing to 0.0118 admits 24 more and
improves the best attainable control effort by 41 %) and argues against relaxing in the primary regime (control
effort excludes 18 of 56 but the surface does not trade it; relaxing moves one other metric by 8 %). The method
does not say a requirement is wrong; it says what it costs on this table's fitted frontier. A caution for spike A:
hold the conditioning and the temperature fixed when comparing design sets, or the comparison shows conditioning
artefacts.

**The driver's calls.** The full case analysis takes the one table (requirements by regime: limit, pass fraction,
band designs excluded, K = 1 exponent, price against the band, the two largest elasticities, a joint row) in
Appendix D and the docs' case page, in the close-out regeneration; no figure (the table says what the ladder figure
would). The paper's Discussion is the supervisor's: options D1 (one short paragraph), D2 (one sentence pointing to
Appendix D), D3 (nothing); recorded under "Waiting for the supervisor" with the driver's recommendation, D2.

## Spike A, the fit with and without the infeasible designs (2026-11-10, 08:45; `WP23-rounds/spikes/spike-A-with-and-without-infeasible.md`)

The reading: removing the infeasible designs changes the fit little (the flag failures lie inside the surface in
the primary regime; in the baseline regime they cut the frontier's ends and the set narrows from seven to five with
the same leaders); imposing the four requirements changes it a lot: the requirement-constrained set (288 / 302
designs, no large wheel) drops the designs that carried one trade and promotes another, the one the unconstrained
one-term fit had blended away (the primary regime's one-term fit becomes pointing error 0.30 against peak slew
power 0.24). In both regimes the constrained set keeps the feasible fit's highest level: the requirements cut the
frontier's flanks, not its top. Two facts for the close-out: a nine-metric fit of all designs is impossible because
the eclipse reserve is a signed slack at or below zero on the 131 depth-of-discharge failures (a second reason it
leaves the model); and the proposals reached the four-metric frontier they were aimed at by spending the battery,
so they are infeasible by depth of discharge and sit below the eight-metric surface.

**The driver's calls.** The full case analysis takes one merged table (a new Appendix D section: the three design
sets per regime, their sizes, the one-term contending set and leaders, the three-term term types, the zero set,
and where the baseline configuration and the check designs sit), in the close-out regeneration; no figure (the
table says it; a log-plane figure of the constrained against the unconstrained surface is a candidate for the
subtraction pass to weigh, not placed). The proposals stay as check designs with the check section saying plainly
what spike A found (they reached the four-metric frontier by spending the battery and fail the depth-of-discharge
requirement); training the proposer on the fully feasible rows is future work. Spike B's caution holds: the
comparison holds the conditioning and the temperature rule fixed, as the spike did. The paper's sentence is the
supervisor's (with the Discussion option); the driver recommends the short one: "Pre-imposing the four requirements
changes the contending set; removing the infeasible designs does not."

## The supervisor on the spikes' presentation (2026-11-10, 08:50)

**Supervisor (mzargham), verbatim:** "my take is that with and without the requirements enforced is interpretable
as constrained versus unconstrained optimization and that i'd lean toward fitting without threshold requirement,
then treat the cuts along the requirements as an after the fact analysis. we can keep that in repo but we should
restrict how much the paper covers this since the case is just for numerical experiments to show the method, its
scope drift to get too far into the options in how we use it in detail. a sentence or two in the dicussion suffices
since it will be backed up by our research records in the repo"

**Disposition.** The fit of record stays the fit on the feasible set (the generation's flags; no threshold
requirement imposed before the fit), as it is today. The cuts along the four requirements are after-the-fact
analysis: spike B's requirements table and spike A's constrained-against-unconstrained table live in Appendix D and
the docs' case page, with the spike reports as the research record in the repository. The paper's Discussion
carries one or two sentences, drafted by the paper stream as candidates for his review, in the spirit of: fitting
first and reading the requirements after is the unconstrained-then-constrained reading; pre-imposing the four
requirements changes the contending set while removing the infeasible designs does not; Appendix D prices each
requirement at the frontier. Nothing more of the options enters the paper. This resolves the Discussion item
under "Waiting for the supervisor".

**The pointing-error threshold stands (2026-11-10, 08:55).** **Driver's popup:** it excludes the baseline
configuration (0.0155 against 0.0085 degree). Options: keep / 0.0136 / 0.0118. **Supervisor (mzargham),
verbatim:** "Keep 0.0085 deg". Disposition: the model keeps it; the case prose and the model's doc say the
baseline configuration fails the pointing-error requirement; the baseline regime's pass fraction (63.7 %) is
stated with it.

## The close-out scope approved; OD10 (2026-11-10, 09:50; the driver)

`WP23-closeout-scope-of-work.md` (bcc7d26). **OD10, which conditioning the constrained-against-unconstrained table
uses:** (a). Comparing fits across design sets requires the same coordinates, so the feasible set's conditioning
is applied to every set; spike A's constrained rows are recomputed under it, the comparison lists the differences
from the spike's own-rows numbers, and the Discussion candidate follows the recomputed table (if the constrained
set's contending set then stands, the sentence says so; a sentence is not kept because a spike's artefact made it
striking). Spike A's report stays as the research record with its conditioning rule stated and spike B's caution
beside it. No second column. **Approved for execution by the driver under the mandate**; the Agent's defaults as
one item; the container regression and the Linux dispatch are the driver's at the gate.

**Close-out blast radius (2026-11-10, 10:35; the driver, answering the executor directly while the PM's turn was
blocked).** `paper/generate_results.py` joins the close-out's radius for thin wrappers only: three functions that
format the case module's association, requirements and design-sets tables for Appendix D, and one sentence each
in the existing exponents-and-terms and regime-comparison generators; the notebook's cells stay one call each
through `paper_common`. Option (a) of the executor's three; (b) would put Appendix D tables in Appendix C's
generator and (c) would break the appendix's one-call rule.

**Close-out finding under OD10 (a) (2026-11-10, 11:50; the executor's milestone).** With one conditioning for every
design set, the requirement-constrained set's one-term contending set is the same as the feasible set's in the
primary regime and differs by one metric in the baseline regime. Spike A's striking constrained fit was the
conditioning artefact spike B warned of; the Discussion candidate therefore says that the four requirements cut
designs, not what the frontier trades, and the "with and without" reading is: neither removing the infeasible
designs nor pre-imposing the thresholds changes the trades the frontier reports. For the supervisor's review with
the close-out's comparison.

**R-31, mathematics inside notebook HTML outputs (2026-11-10, 12:20; the driver).** The site typesets no
mathematics inside a notebook's HTML output, so Appendices A and E show raw `$...$` spans. Not (b): a visible
rendering defect in two appendices is not accepted into the candidate when it is cheap to fix; not (c): the
one-call-per-table-cell convention stays. First the no-dependency path: `paper_common.py`'s `Md._repr_html_`
emits each span in the theme's own math markup (what the built page uses for Markdown math, checked in the
built HTML), and the result is verified rendered in the browser; if the theme does not typeset it there, (a):
`latex2mathml` (pure Python, no transitive weight) converts the spans to MathML at render time, and the driver
makes the `pyproject.toml` and `uv.lock` change on the executor's request. One small unit after the data-gate
review; Appendix A's register table takes the same path.

**Close-out data-gate review (ebd7dfe; 2026-11-10, 12:40).** 29 met, 8 not met, 3 not checkable; the PM fixes
forward without asking (defects against stated requirements: a nine-metric test file, stale counts the comparison
does not list, the comparison's missing placement numbers, a grep reason, two roundings and a naming), then the
gaps are re-checked. The record stays in `WP23-review.md` (one record file per package). R-31: the reviewer saw
Appendix E typeset on the staged page after the generator change; the fix unit confirms A and E in the browser
before anything else is done. The container regression and the swap call wait for the re-check.
