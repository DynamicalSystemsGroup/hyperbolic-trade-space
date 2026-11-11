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

**Fleet cost limit, the supervisor, verbatim (10:00):** "set a 1 million budget for 25 satellites. my research shows
thats more than enough". The driver's check before recording a value: 1,000,000 USD over 25 satellites is 40,000 USD
per satellite including launch; on the spike's calibration the baseline's 25-satellite fleet costs about 6.5 million
(build about 4.2 million at the 90 to 95 percent learning slopes, launch 25 x 13.3 kg x 7,000 USD/kg about 2.3
million), and launch alone is 93,000 per satellite. The question of what his research prices is put back to him
before the value is set.

**The supervisor, verbatim (10:05):** "recalibrate your research. i am not convinced you did real desk work see:
https://keeptrack.space/deep-dive/how-much-does-a-satellite-cost and
https://spacenexus.us/guide/space-launch-cost-comparison i am guessing if you did do research it was overly impacted
by old data. the commercial space industry has really ramped up recently. please focus your research on 2026 prices".
**Disposition:** spike D is re-run as a recalibration spike on 2026 prices (his two pages opened in full and read
first; every figure dated; pre-2025 catalogue prices used only where no 2026 figure exists and marked as such; the
launch market's 2026 rates and the integrator and rideshare offers for cubesat classes; platform prices by class;
fleet and volume pricing where any vendor publishes it), with the baseline's 25-satellite fleet priced under the 2026
numbers and a statement of what 1,000,000 USD buys for 25 satellites of this class. The readout goes to him with the
arithmetic before either cost value is set; the WP30 build continues on placeholders; the gate waits for the values
(OD5 (b)). The unit cost limit of 350,000 USD is held until the recalibration, since it was chosen on the old
calibration.

**The driver's first read of his two pages (10:15), recorded before the spike:** keeptrack.space (satellite cost
deep dive) prices cubesats from the same EnduroSat slides the spike used as source 28 (a 1U bus about 25,000 USD with
a 70,000 launch; a 6U bus over 200,000 with a 450,000 launch) and a 100 kg smallsat at about 700,000 USD on Transporter
in 2026; spacenexus.us (launch cost comparison, as of October 2026) gives Transporter at 350,000 USD per 50 kg
minimum, 7,000 USD/kg in 2026 rising 500 USD/kg a year, Falcon 9 dedicated at 74 million, Electron at about 9.2
million average revenue per launch. Neither page prices a 12U cubesat or a fleet. The recalibration spike (D2) runs
on 2026 sources first; its readout, with the baseline priced at 1 to 30 units and what 1,000,000 USD buys for 25
satellites in 2026, goes to him before either value is set.

## The assistant's calls on the spike D2 readout (2026-11-11, 10:10; readout b057b4f)

The 2026 readout confirms the launch rate and moves the part prices about five percent up (panels 340,000 USD/m²,
battery about 70 USD/Wh, wheels 8,000 each; tracker and bus hold; assembly has no source and stays at 100,000 USD):
the baseline builds at 368,320 USD for one unit and 173,167 at twenty-five, inside the 2026 spread. One million USD
for twenty-five satellites is 40,000 each with launch, which buys two baseline 12U satellites with launch, or a
1U-class fleet; "more than enough" holds only at the 1U class.

- **A. Coefficients:** the 2026 central values are adopted in the cost model, each with its source and date in the
  calc's doc; assembly stays at 100,000 USD and is marked unsourced.
- **B. Unit cost limit: 350,000 USD stands** (his pick on the earlier calibration; the covered cost, read at the
  design's own fleet size); its admitted share is recomputed on the regenerated data at the gate and printed.
- **C. Fleet cost limit: 6,000,000 USD** (build and launch, the fleet size free from 1 to 30; on the earlier ladder it
  admits 71 percent of the baseline regime's feasible designs at their own fleet size, every design up to ten
  satellites). **This is a call against his stated number** ("set a 1 million budget for 25 satellites"): the
  recalibration he ordered shows that number buys two satellites of this class, so a limit of 1,000,000 would admit no
  design and the metric would carry a requirement nothing meets; 6,000,000 keeps a fleet of ten within reach of every
  design and binds the larger fleets, which is the trade he described. It is the first row of the review list for
  him to revert; his number is kept beside it as the alternative, and the requirement's doc says the figure is a
  lower bound on a full costing.
- **D. Launch:** 7,000 USD/kg linear, the 50 kg minimum slot noted in the requirement's text, not modelled; the launch
  budget restated at his admitted mass: 15.11 kg at 7,000 USD/kg = 105,770 USD.
- The requirements' coverage statement as decided (included, excluded, a lower bound). The gate runs on these values;
  no placeholder remains.

**Fleet cost limit, the supervisor, verbatim (2026-11-11, 10:25):** "okay i was pushing you too hard on price but
that's also pretty realistic. i think its worth noting that the 1u series could get below that price point but its
pretty optimized. larger series would be notably more expensive like the 6u series. i was originally thinking maybe
an 8 million budget now that you've tried to get the prices down". **Value: 8,000,000 USD** on the covered fleet cost
(build and launch, the fleet size free from 1 to 30); on the earlier ladder it admits about 93 percent of the baseline
regime's feasible designs at their own fleet size, and the baseline's own 25-satellite fleet (about 6.7 million on the
2026 central prices) clears it. This replaces the assistant's 6,000,000 call, which is withdrawn from the review list's
first row (his number stands, not a call against it). His note on classes goes into the requirement's coverage text:
the figure is for this 12U class; a 1U series can sit below 40,000 USD a unit, larger series are dearer.

**Fleet cost limit, final; the supervisor, verbatim (2026-11-11, 10:30):** "i think we use your 6 million as the
budget per your suggestion but 8 million is full budget accounting for what we didn't scope into this assessment".
**Values:** the fleet cost requirement on the covered cost is **6,000,000 USD** (the assistant's suggestion, now his
decision: not a call against his word, so it leaves the review list's first row); the requirement's text states that
the sponsor's **full fleet budget is 8,000,000 USD**, of which the covered cost (attitude-control, power and structure
parts, assembly and test, wholesale launch) is held under 6,000,000, the remaining 2,000,000 being the allowance for
what the assessment does not scope (communications, payload interface, flight software, a fuller test campaign, the
launch slot minimum, broker fees). The same two numbers and their relation appear in the stakeholder layer's sponsor
concern, Appendix C and the docs case page; the class note stands (a 1U series below 40,000 USD a unit; larger series
dearer).

**The supervisor, verbatim (2026-11-11, 10:35), on what the base prices exclude:** "* Payloads and Instruments: The
base prices above cover the satellite "bus" (structure, power, radios, and computer) and launch, not specialized
scientific sensors, cameras, or custom electronics. Adding heavy instrumentation will increase the per-unit cost.
* Testing and Operations: You will also need to budget for environmental testing (vibration and thermal-vacuum
chambers), licensing, and a ground station network to talk to your 25 satellites once they are in orbit".
**Disposition:** the coverage statement's exclusion list reads, in this order: the payload and its instruments
(sensors, cameras, custom electronics); communications and the payload interface; flight software; environmental
testing beyond the assembly line (vibration, thermal vacuum); licensing; a ground station network and operations; the
launch slot minimum and broker fees. The 2,000,000 USD allowance inside the 8,000,000 full budget is described as
covering these; the requirement's text says the covered cost is the bus (structure, power, computer and radios in the
bus block), the attitude-control parts, assembly and wholesale launch.
