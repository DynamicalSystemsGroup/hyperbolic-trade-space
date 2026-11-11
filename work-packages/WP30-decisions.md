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
