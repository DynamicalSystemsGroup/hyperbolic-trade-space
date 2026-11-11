# WP30 — Decisions

Approvals and acceptances are the driver's under the mandate; the supervisor's words are quoted verbatim where they bind.

## Scope gate (2026-11-10, 23:20; scope `WP30-scope-of-work.md` at 747a45e; Track B, the model revision with one data gate)

Origin: the supervisor on Figure 3 and on H-2 (`WP28-decisions.md` S-2; `WP27-decisions.md` "H-2"; his "Confirm" of
the changed baseline conclusion in spike C's `decisions.md`). Stage (2) taken by the driver on both readouts (spike C's
and spike D's `decisions.md`).

- **OD1 (a).** Both pricing metrics are traded metrics with columns, eleven in all: the unit cost falls and the fleet
  cost rises as the fleet grows, which is the trade the supervisor described ("diminishing unit costs but increasing
  total cost"); the fit reads it through the fleet-size variable, and the association step names a near-duplicate
  pair if one appears (it should not across 1 to 30 units).
- **OD2 (a).** Verdict-only: the two cost limits do not enter the feasibility flags; the feasible sets stay as the
  physics leaves them; the values can land after the data, as the WP23 requirements do ("read after the fit").
- **OD3 (a), the supervisor's, in the morning:** one value per limit from the ladders the model developer computes on
  the regenerated data.
- **OD4 (a) proposed, his confirmation in the morning:** 105,770 USD at 7,000 USD/kg, the same mass (15.11 kg).
- **OD5 (b).** The gate regenerates with placeholders; his values re-pin the two requirements afterwards without a
  second regeneration (valid under OD2 (a)); the pass fractions are printed from the data he sees.
- **OD6 (a).** Model units to `dev` as they stay green; the spec, the oracle columns and the pinned tests land together
  with the data at the gate.
- The Agent's defaults approved as one item.

**Driver, verbatim:** "WP30 approved with OD1 (a), OD2 (a), OD3 and OD4 his in the morning, OD5 (b), OD6 (a). The
model developer may start the build."

## Stage 3b questions (2026-11-11, 01:40; the driver)

- **(1) (a).** The unit cost includes launch, as built (U = F / n with launch in F): the supervisor's words were "the
  manufacturing and launch costs of a fleet ... one for fleet cost at unit cost times number of units and one which
  is unit cost"; "unit build cost" was the spike's phrase. The placeholder 450,000 USD is read with launch, and the
  morning ladder is on that metric.
- **(2) (a) recorded, (b) offered.** 105,770 USD (15.11 kg at 7,000 USD/kg) is the figure recorded for his confirmation;
  the exact-mass figure 105,750 USD (15.107 kg) is shown beside it in the morning question; he picks.
- **(3) (a).** The model's line cap rises to 1,150 with the reason in the record (eleven traded metrics and a cost
  section); no trimming of the model's docs for the cap's sake.
- **(4) (a).** The check designs draw fleet sizes as the scope says, so the pricing metrics are exercised by the checks.

**Gate checklist (450c65b), the driver (2026-11-11, 02:30):** the nine gaps are preparation units for the model
developer and the PM, to land before the supervisor's values arrive: a WP30 mode in `ledger_gate.py` for the
regeneration's entries; the ladder script (`WP30-rounds/cost-ladders.md` from a script on the regenerated data, per
regime and fleet size); named commands for the sensitivity and the K = 1, 2, 3 records; the container README's
paragraph on the ledger re-run inside `hts-paper`; the entry numbers read from `ledger.jsonl` before the run, not
inferred; the contract amendment numbered at the head when it lands. On gap 2: the supervisor's values change the
model's hash after the regeneration; under OD2 (a) the outputs do not move, so the gate ends with a container re-run
that proves hash-equal outputs against the new model hash (the WP26 precedent), not a second regeneration. The
answer key's version 5 is the driver's and is written when the data of record land. The check designs draw a fleet
size, as decided (3b question 4).

**Gap 2 ordering (2026-11-11, 02:55; the driver):** option B. The record's proof is container to container: step 14
runs the container on the placeholder model (@10, shared @9), and a second `--image <id> --wp30 values` run (@11,
shared @10) follows once the supervisor's values land, proving the outputs hash-equal against the new model hash.
Eight minutes buy the proof the wording claims; host-to-container last-digit drift is not a proof. The morning ladder
for the unit-cost limit is read from the with-launch table (3b question 1): at one unit the 450,000 placeholder admits
about 41 percent of the baseline regime's feasible designs with launch included, not the spike's 91 percent.

## The supervisor's values (2026-11-11, 09:50; the ladders in his pane, the desk research explained)

Asked for the unit cost limit after the correspondence to the sources was explained, he said, verbatim: "we should
find away to account for the fact that our price point is a lower bound. i think we can probably just be clear in the
requirement itself what aspects of cost are included and what is excluded. rather than trying to force every
concievable concept into every model we just need to be explicit about what our model does and does not cover and
insure it is interpretable and useful as such. a full costing would require these other subsystems to be accounted
for." **Disposition:** the two cost requirements and the pricing calcs in the model state their coverage in their own
text: included, the attitude-control, power and structure parts at vendor-bracketed prices, an assembly, integration
and test line, and launch at the wholesale per-kilogram rate; excluded, communications, the payload interface, flight
software, a test campaign beyond the assembly line, the launch slot minimum and any broker's fee; the figure is a lower
bound on a full costing, and the requirement reads it as such. The same sentence appears where the docs and the paper
name the cost metrics. The sponsor's stakeholder view carries it as the concern's note. His values follow.

**Unit cost limit, the supervisor, verbatim (09:55):** "i want to lean smaller and its fine that no single satellite
clears it. i think that's pretty realistic. we shouldn't be launching a single cube sat, i would expect the cost to be
prohibitive". **Value: 350,000 USD** per satellite on the covered cost, read at the design's own fleet size (admits 82
percent of the baseline regime's feasible designs at their own fleet size, none priced as a single satellite; the
primary regime's share from the same ladder).
