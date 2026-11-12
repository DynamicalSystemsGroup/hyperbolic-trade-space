# P8 final read (new-space program/business-line executive), staged site at 8806b0e

Read, rendered in a browser tab: the paper at /paper/ (abstract, sections 1 to 14, the case sections 8 and 9, the
discussion) and the supporting material (C.8, D.7, D.17); the docs root page and /docs/examples/. Not read in the first
pass: notes, records, tests, other personas' reads. The second pass (section 6) read the baseline only.

## 1. What held my interest / what lost it (first pass)

Held:
- The contribution sentence with numbers: of 2,134 feasible designs the nondominated set is 236 on 4 attributes and
  2,134 on all 13. That is my trade table where everything is "Pareto". It is the one sentence in the front matter
  that I can repeat to a board.
- Section 8 now states money: the covered cost is a lower bound (bus, attitude-control parts, assembly and test,
  launch), the fleet limit is 6,000,000 USD inside the sponsor's 8,000,000 USD. The sentence that the fleet size is a
  design variable, "a count that is no part", is how a fleet budget really works.
- The requirements read after the fit (Examples page, D.17), with the finding that no design of fleet size one passes
  the unit cost limit, so the unit cost limit is a fleet-size choice and not a design-space one. That is a true
  statement about small-satellite economics and it is stated plainly.
- Discussion: "That the fit supports a decision is a third claim the certificate does not make." Honest.

Lost:
- The abstract. Its first sentence is right for me (an answer and a justification an accountable executive can
  follow). The next eight use surface, posynomial, n-lemma, energy differential, GGP, kernel. It ends "one term
  blends the subsystems' trade-offs into a single tension; two terms separate the contending sets": no number, no
  design, no money.
- Sections 8 and 9 give two money numbers (6,000,000 and 8,000,000 USD). The unit cost limit (350,000 USD per
  satellite) and the launch price (7,000 USD/kg) appear only in appendix C.8 and D.17. The Examples page names the
  limits without their values. On the screens I was pointed to I could not check the case's economics without opening
  the supporting material.
- Section 9 reads as description: "the terms' sets differ". Nothing says what a program does differently.

## 2. Findings

F1. The abstract does not let me find the use in minutes.
- Says: "Each monomial term (a product of powers of the metrics) reports its contending metrics, an n-lemma ... with
  elasticities: the percentage of one metric given up per percentage gained in another."
- The elasticity clause is the sentence an executive wants ("percent of mass or cost given up per percent of
  pointing gained"), and it is there, but it sits in the middle of a nine-sentence paragraph of method vocabulary.
  The abstract names no case number. The Examples page and docs root say nothing of money either.
- Severity: changes whether I read on.

F2. No decision is shown that the method changes.
- Says: the paper "stops short of selecting a design, which falls to experts"; section 9: "The finding: the terms'
  sets differ."
- Business: the case has no sentence of the form "with this reading we would relax X or buy Y". The nearest is the
  requirements finding (the contending set barely moves whether or not the requirements are imposed first), which
  is useful but sits in the discussion and D.17, not in the case.
- Severity: changes the decision (I cannot tell what I would do differently on Monday).

F3. Requirement prices are in bands and log V, not in program currency; only the limits are in USD.
- Says: D.17: unit cost price 5.31 bands (0.1274 log V), fleet cost 1.50 bands, total mass 0.24 bands; the limits
  are in USD and the mass limit comes with its launch budget (15.11 kg, 105,770 USD at 7,000 USD/kg).
- Business: the unit cost limit is by far the most expensive requirement to meet (5.31 bands against 1.50 and 0.24)
  and that is the finding I need, but it is not converted to dollars per satellite or satellites per fleet. The
  single conversion given (mass to launch USD) shows it can be done.
- Severity: changes the decision (cannot negotiate a requirement in bands).

F4. No hand-named candidate meets the four performance thresholds.
- Says: D.7 and D.17 candidate table: baseline, fast_effort_hungry, precise_heavy_sensor and light_slow all "passes
  the flags True, meets the thresholds False"; the three proposals all False on flags. On the thresholds-met fit
  the two sensible candidates score beyond the surface (+0.315 and +0.354 log V).
- Business: the program would carry a compliant baseline. The reading "on the constrained fit two candidates sit
  beyond the surface" is a real result and is not in the text.
- Severity: cosmetic for the method claim, changes the decision for the reading of the case.

F5. The economics of the case read sanely, with two soft spots.
- Launch 7,000 USD/kg and 15.11 kg giving 105,770 USD: sane for a rideshare price of 2026 for this class, the
  arithmetic checks. Unit cost limit 350,000 USD at the design's own fleet size, which "no single satellite of this
  class clears", with a 1U series below 40,000 USD a unit "for scale": plausible for a 12U bus with a 100,000 USD
  assembly line. 6,000,000 USD over fleets of one to thirty: about 17 satellites at the cap: plausible.
- Soft spot: the sponsor's 8,000,000 USD leaves 2,000,000 USD, a quarter, for payload, communications, operations,
  licensing and ground; for a real 12U program the payload and operations usually exceed the bus. C.8 says "none is
  flowed down from a mission" and lists what is left out, so this is a toy statement, not an error.
- Soft spot: C.8 names "launch slot minimum and broker fees" as left out. A flat linear launch price is the
  largest simplification a launch buyer would notice.
- Severity: cosmetic.

F6. Adoption cost is not stated.
- Says: section 11: supply configurations, attributes and a conditioning rule; section 10 limits: "Small samples
  determine exponents weakly." No minimum number of evaluated designs, no analyst effort, no skills line.
- Business: I would ask how many evaluated designs I need and who writes the conditioning. Real programs have tens
  of vendor options, not 2,134 simulated designs.
- Severity: changes the decision (what it costs me to adopt is the first question I ask).

F7. Schedule, lead time, qualification and reliability are absent, and said so in one place only.
- Says: C.8 "no schedule or qualification, no fault tolerance, no thermal or communications model"; section 8 says
  hardware values are illustrative and the cost is a lower bound.
- Severity: cosmetic for a method paper, changes the decision for a program. The statement is in an appendix; section
  8 and the Examples page carry only "illustrative" and "lower bound".

F8. Dense, long first screens for a reader at my level.
- Say: section 1's "Main results" list cites Theorems 1, 2, 3, 5, 6, 8, 9, 10, 11, 12 and lemmas; the executive
  contribution is two sentences.
- Severity: cosmetic if a reader stops after the contribution sentence and the case; it does not.

## 3. Numbers off by more than 2x (or implausible)

- 7,000 USD/kg: within the range I would quote for small-payload rideshare; not off.
- 105,770 USD launch for 15.11 kg: arithmetic correct; within 2x of a rideshare invoice excluding broker fees.
- 350,000 USD unit cost limit and 6,000,000 USD fleet limit: plausible for a lower-bound bus cost.
- 2,000,000 USD allowance for payload, communications and operations (25 percent of the 8,000,000 USD): low by
  more than 2x for a real program; the case says it is not flowed down from a mission.
- Fleet of one to thirty identical satellites with a learning curve: reasonable for the class; the curve's shares and
  slopes are "choices, not findings" (C.8).

## 4. What I would change first, in order

1. A two-line case result next to the abstract's last sentence, in program units (which requirement costs most, in USD
   per satellite or fleet size; which sets of metrics the second term separates).
2. Convert the unit cost and fleet cost requirement prices from bands to USD, as the mass limit is converted to
   launch USD in D.17.
3. State the case's gaps (no schedule, no payload, a flat launch price) in section 8 next to "illustrative", and put
   the 350,000 USD and 7,000 USD/kg figures in the main text or on the Examples page.
4. Say in the case what the constrained fit's result for the candidates means (two sensible candidates sit beyond
   the surface once the thresholds are imposed; none meets all four).
5. One paragraph on adoption: minimum number of designs, who writes the conditioning, how long a first fit takes.

## 5. Standing question and decision question

Realistic enough to keep me interested? Yes, more than before. A fleet size as a variable, a unit cost and a fleet
cost in the table, a 6,000,000 USD fleet limit inside an 8,000,000 USD budget and the finding that the per-satellite
limit is really a fleet-size choice are things I recognise from budgets I carry.

Would the method change a decision I make? Not from the paper as written; it would change how I prepare one. The
mechanism I could use is the requirements reading (which requirement is expensive at the frontier, and that imposing
constraints first barely changes what trades), provided its prices come in dollars. I would not adopt on this page
because the adoption cost is not stated.

What the method does not tell me, from the text: schedule and risk, what to buy, a design (stated), how many to fly
other than through the cost curve, whether the sample resembles what vendors sell, and what a requirement change of a
stated amount costs in USD.

## 6. Second pass: the baseline's findings (read after section 1 to 5 were written)

Baseline: work-packages/WP30-rounds/persona-baseline/P8-baseline.md (origin/dev 45180fd).

| Baseline finding | State at 8806b0e | Evidence |
|---|---|---|
| F1 no cost or schedule axis; launch only, flat 6,000 USD/kg | cost resolved; schedule narrowed to a toy statement | Section 8: the cost is a lower bound; thirteen traded metrics include unit cost and fleet cost (Figure 3 caption); C.8 prices parts, assembly, a fleet curve and launch at 7,000 USD/kg. C.8: "It has no schedule or qualification, no fault tolerance". Launch is still a flat linear price (broker fees and slot minimum named as left out). |
| F2 equal log-spread makes total mass lead; reads as importance | resolved on the case; the general statement narrowed | The one-term contending set on the Examples page no longer contains total mass (unit cost, available power, pointing error, fleet cost, momentum headroom, settling time, depth of discharge). Section 5: "rescaling one metric changes which term is tangent, so a stable fitted direction answers that question and is not a context-free discovery"; section 10: "The exponents depend on the conditioning." |
| F3 no candidate meets the requirements | still open | D.7/D.17 table: every candidate "meets the thresholds False"; proposals fail the flags. The constrained fit scores the sensible candidates beyond the surface (+0.315, +0.354) and the text does not read this. Main text: "0 of them lie beyond the fitted reference surface" (K = 1 fit of record). |
| F4 prices in bands, not program currency | narrowed, not resolved | D.17: limits now in USD and the mass limit carries its launch budget (105,770 USD at 7,000 USD/kg); prices remain "price (bands)" and "price (log V)" (unit cost 5.31 bands). |
| F5 random sampling over the design space, not how a bus is built | narrowed to a toy statement | Section 8: "worked example of design optimization, not a study of either use"; section 7: "the case's are a random draw". |
| F6 single scenario, no thermal, radiation, reliability | narrowed to a toy statement | C.8: "no thermal or communications model, no mass or power growth allowance and a constant 12 W load. Momentum is checked over one slew". Appendix only; section 8 carries "illustrative". |
| F7 Examples page: regime and requirements findings in one breath; two sets of numbers for three terms | resolved | Examples: "At the one-term temperature ... mean slack falls from 0.122 to 0.043. At the two-term fit's own temperature, status certified, the terms have contending sets of 8 and 7 metrics"; the three-design-sets block states what each set is and why the two cost limits are not among them. The page is at K = 2 as the paper's case is. |
| F8 no fleet or quantity | resolved | Section 8: fleet size a design variable; C.8: "fleet of one to thirty identical satellites", a learning curve, a 6,000,000 USD fleet limit; D.17 reads the fleet cost requirement. Launch packing is not modelled. |
| F9 an executive cannot follow log V, tau, n-lemma without translation | still open | Abstract and sections 1 to 4 use surface, posynomial, n-lemma, energy differential, GGP; first screens carry no case number and no money. The abstract's elasticity clause is the nearest to program language. |

Baseline's "what I would change first": (1) a stated list of what the case lacks, up front: narrowed (section 8 states
illustrative, lower bound; the full list is in C.8 and the Examples page points to it). (2) priced requirements in
program currency: narrowed (limits in USD, prices in bands). (3) one decision the method changes: still open (F2
above). (4) a named compliant candidate: still open (F3 above). (5) mass leading because of the scaling: resolved on
the case by the changed contending set. (6) reconcile the Examples and paper numbers: resolved (F7).

## 7. Verdict on the hard requirement

I read the hard requirement as: a new-space executive finds the method and its case, and reads the economics and
verdicts as sane, from the first screens without the derivations.
- Economics and verdicts reading sanely: met. The case now has unit cost, fleet cost, fleet size, a launch price and
  limits in USD that agree with each other and with launch-buying experience; its gaps are stated, though in the
  appendix.
- Finding it in minutes: not met. The abstract and the first screens give an executive no number and no money, and the
  350,000 USD and 7,000 USD/kg figures are only in the supporting material.
- Whether the method changes a decision: not shown (F2, F3, F6).
Overall: partly met. The case is credible to me; the front of the paper is not yet written for me.
