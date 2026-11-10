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
