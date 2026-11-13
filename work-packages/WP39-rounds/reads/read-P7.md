# Read P7 (R-7): Section 9 decision close and Appendix D.19

- Persona: P7, systems engineer on flight hardware (reads numbers and configuration choices, wants the reduction traceable)
- Head: a538fc4 (staged site http://127.0.0.1:8791)
- Pages: /paper/ (Section 9, "Case analysis", through "What the executives decide" and its six-row table); /paper/supporting-material/ (Appendix D.19; also D.17 and C.8 for the requirements and the budget)
- Viewport: browser pane tab-120, innerWidth 840 px. Text was read from the rendered DOM. No screenshots: my tab was not fronted, so the pane refused to composite frames, and I did not front it so as not to disturb other readers. The place to look: /paper/, the last table of Section 9 (scroll to it), and /paper/supporting-material/ at the D.19 heading.

## Own-words summary of the call
Of 2,134 feasible designs, 28 meet all six requirements and sit inside the fitted band of both the K = 1 and K = 2 fits. What is left is a single value judgement: is a fine star tracker (pointing error about 0.003 down to 0.0008 degree) worth about 0.56 M USD of a 6 M USD fleet budget? If yes, buy 5 medium-wheel, fine-tracker satellites at 1.69 M USD (337,000 USD each), the one with least regret among the 5 designs that trade pointing error against fleet cost. If no, buy 4 small-wheel, medium-tracker satellites at 1.13 M USD, the cheapest. The method prices the question but does not answer it, the numbers are nominal, and it says nothing on schedule, risk, parts beyond the model or a larger fleet.

## Q1: could I follow the reduction without the subsystem detail?
Yes for the arithmetic and the logic of 2,134 to 28 to a two-way choice. I stopped at "lie within the band of both fits": the band and the "six requirements" are not defined in Section 9, and I had to go to D.19 and D.17 to know what they are.

## Q2: easier or harder?
Easier. The sentence: "The method prices the question and does not answer it; the numbers are nominal (Appendix C.8)."

## Findings

| # | Severity | Place | Verbatim quote | What happened | Expected |
|---|---|---|---|---|---|
| 1 | slows | Section 9, opening sentence | "(the executives’ call: Table ??; tables: Appendix D; digits that hold: D.11)" | The cross-reference to the closing table renders as "Table ??", unresolved. | A resolved table number, or a link to the closing subsection. |
| 2 | polish | Section 9, "What the executives decide" | "worth about 0.56 M USD of a 6 M USD fleet budget" | The 6 M USD is the covered-cost requirement (D.17), not the budget: C.8 says it sits "inside the sponsor’s full budget of 8,000,000 USD", with 2,000,000 USD for what is not covered. The paragraph names no basis for the 6 M. | "of the 6 M USD fleet-cost limit", or the budget stated consistently. |
| 3 | polish | Section 9, same paragraph vs D.19 | "regrets least of the 5 that trade the two measures" | D.19 also says "11 are nondominated on pointing error and fleet cost, and 1 of them lies within the band of both fits" (over the 548); the 5 are nondominated within the 28. A reader meeting both numbers can take them as conflicting. | One clause saying the 5 are the nondominated designs within the 28. |
| 4 | polish | Section 9, table caption | "The baseline configuration does not meet the requirements." | Not shown in the section; the table shows unit cost 461,360 USD against the 350,000 limit (D.17), which supports it, but the section does not point to that. | Name the requirement it misses (unit cost). |
| 5 | polish | D.19 prose vs table | "balanced between the terms, the design where the K = 2 fit’s two term levels are closest" | The table, in both Section 9 and D.19, gives one "level (K=2)" per design, not the two term levels, so I could not check that rule. | Show the two term levels, or say that the level shown is the larger one. |

## Numbers cross-check

| Number | Result |
|---|---|
| 2,134 | agree (D.? data section: "cubesat-primary: 2,134 designs by 13 metrics"; also "all 2,134 feasible designs") |
| 548 | agree (D.19: "over all 548 designs that pass the six requirements") |
| 28 | agree (the D.19 table has 28 rows, counted in the DOM) |
| 5 (trade the two measures) | agree: the table marks 5 rows nondominated on pointing error and fleet cost (999, 190, 766, 1858, 2950) |
| 0.56 M | agree: 1,686,142 minus 1,127,465 = 558,677 USD |
| 6 M | agree with the fleet-cost limit in D.17 (6,000,000 per fleet); see finding 2 for calling it a budget |
| 1.69 M | agree: design 1858, 1,686,142 USD |
| 337,000 | agree: design 1858, 337,228 USD each (1,686,142 / 5 = 337,228) |
| 1.13 M | agree: design 999, 1,127,465 USD, fleet 4, small wheel, medium tracker |

Other checks:
- Pointing error "about 0.003 to 0.0008": agree (0.00295 for 999, 0.00080 for 1858).
- "regrets least of the 5": agree. I recomputed minimax regret on the 28, with each measure scaled over the shortlist range. Design 1858 has max regret about 0.118, against about 0.27 to 0.29 for 766, 999 and 190, and about 0.198 for 2950.
- "if not ... is cheapest": agree, 1,127,465 is the smallest fleet cost on the shortlist.
- Every design named in the section's six-row table is in the D.19 shortlist (999, 2950, 1858, 766, 2356), with matching pointing error, unit cost, fleet cost and level to rounding. The baseline row is not in the shortlist, as intended.
- Consistency with the requirements I could check from D.17: all 28 have pointing error at most 0.008495 (maximum 0.00846), unit cost at most 350,000 (maximum 343,961) and fleet cost under 6,000,000 (maximum 5,846,300). The slew power, control effort and mass requirements cannot be checked because those columns are not in the table.
- "sponsor alone" has the smallest fleet cost, "operator alone" the smallest pointing error (0.00074), and "cheapest unit cost" the smallest unit cost on the shortlist (233,852): all agree.

## Sentences implying the method chooses or ranks
None that I would block. "regrets least" and "is cheapest" are stated as outputs of named rules, and the table is captioned "the designs the rules pick". The nearest to the line is the table label "balanced between the terms", which reads as an endorsement but is defined as a rule in D.19.

## The nominal clause and the does-not-tell sentence
- Nominal: "The method prices the question and does not answer it; the numbers are nominal (Appendix C.8)." It points to C.8, which says the model is "a demonstration and its numbers are illustrative" and that cost is a lower bound. It is present, and the pointer works.
- Does-not-tell: "The method does not tell the schedule or the risk, what to buy beyond the modelled parts, or what a larger fleet is worth." It is present. It sits in the caption after the table rather than in the paragraph, and the table has fleets up to 25, so "a larger fleet" means beyond 30 or beyond the modelled range; that could be made explicit.

## What I could not tell
- What the band of both fits means in physical terms; I only know how D.19 defines it.
- Whether "balanced between the terms" is the design the rule says (see finding 5).
- Whether the slew power, control effort and mass requirements hold for the 28 (columns absent).
- How the unit cost and the fleet cost scale with fleet size; the section takes that from C.8, and I did not follow it.
- The appearance of the rendered table: no screenshot.
