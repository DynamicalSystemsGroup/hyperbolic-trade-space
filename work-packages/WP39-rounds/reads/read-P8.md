# Read P8 (new-space program/business-line executive)

- Persona: P8. Head a538fc4 (staged site, http://127.0.0.1:8791). Page: /paper/, Section 9 "Case analysis", read through to "What the executives decide" and its table; the paragraph before it for context.
- Viewport: 840 x 975 CSS px (dark theme). Screenshot taken at /paper/ scrolled so "What the executives decide" is at the top of the pane (not saved to disk; the tool only returned the image).

## Summary in my own words (written first)
The section ends by saying the screen of designs against the requirements leaves 28 candidates, and that one question remains that is mine: whether a better star tracker, which sharpens pointing from about 0.003 to 0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet budget. If yes, buy 5 satellites with the better tracker and medium wheel for 1.69 M USD; if no, buy 4 smaller-wheel satellites with the ordinary tracker for 1.13 M USD. The method does not answer that; it only puts a price on it. The numbers are "nominal", and the method does not cover schedule, risk, what else must be bought, or what a bigger fleet is worth. The baseline design fails the requirements, so "do nothing" is not on the table. I come away with a two-way call and a price tag, not a recommendation.

## Q1: could I follow the reduction from the feasible designs to the call without the subsystem detail?
Partly. I followed "2,134 feasible, cut to 28, then two named choices" and the arithmetic of 0.56 M (1.69 - 1.13) holds against the table. I stopped following at "lie within the band of both fits": I do not know what "the band" or "both fits" are, and nothing in the paragraph says why 28 becomes "the 5 that trade the two measures". I took on trust that 5 of 28 are the real choices.

## Q2: did the section make the decision easier or harder?
Easier. The sentence: "One question remains, and it is theirs: whether a fine star tracker, which brings the pointing error from about 0.003 to 0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet budget."

## Findings
| # | Severity | Place | Verbatim quote | What happened | What I expected |
|---|---|---|---|---|---|
| 1 | blocks | Section 9 opening paragraph | "(the executives' call: Table ??; tables: Appendix D; digits that hold: D.11)" | The pointer to the executives' table renders as "Table ??", an unresolved reference. The table at the end is unnumbered and uncaptioned as a table, so I could not tell it is the one pointed to. | A working link to a numbered table, "Table N". |
| 2 | slows | "What the executives decide", sentence 2 | "lie within the band of both fits" | "Band" and "both fits" are method words with no gloss at the point of use; this is the step I could not follow. | Plain words, e.g. what "within the band" means for a design and which two fits. |
| 3 | slows | same paragraph | "regrets least of the 5 that trade the two measures" | "Regrets least" is undefined here; the table's "between them" row has level -0.012, below the sponsor and operator rows, and I could not tell why it "regrets least". I also cannot tell which 5 of the 28 are "the 5". | A one-clause statement of what regret is measured against, and a list or pointer to the 5. |
| 4 | slows | table, column "level" | "level" with values "-0.330", "+0.016", "+0.010", "-0.012" | No unit or meaning stated for a business reader beyond "(log V at K = 2)" in the caption. I could not tell if higher is better or what -0.330 for the baseline means in schedule or money. | A plain-language one-liner (e.g. "how far a design sits inside or beyond the fitted frontier; higher means more capability per the model") or drop the column from the executive view. |
| 5 | slows | table, rows "balanced between the terms" and "cheapest unit cost" | "balanced between the terms" / "fleet 25" | The prose names only three decisions (baseline, sponsor, operator, between them); these two rows are not discussed, and "terms" is method vocabulary. "Cheapest unit cost" at fleet 25 costs 5,846,300 USD, almost the 6 M budget, and nothing says why it is listed or that it is not a candidate. | A sentence saying these two rows are context, and what each shows to a buyer. |
| 6 | slows | table, "configuration" column | "medium wheel, medium tracker, 0.60 m, 80 Wh, Kp 0.03, Kd 0.30, fleet 1" | Subsystem detail (0.60 m, Wh, Kp, Kd) sits in the executive table; I skipped it. Only wheel, tracker and fleet size matter for the call. | Wheel class, tracker grade and fleet size up front, the rest moved out (Appendix D.19 has it). |
| 7 | polish | "What the executives decide" | "about 0.003 to 0.0008 degree" vs table values 0.00295 / 0.00074 / 0.00080 | The prose is rounded and consistent, but I had to check; "0.0008" matches the "between them" row while the operator-alone row shows 0.00074. | Fine as is; mention only that the operator-alone design reaches 0.00074. |
| 8 | polish | Table caption | "The baseline configuration does not meet the requirements." | A strong, useful sentence but it sits in the caption under the table, after the call. | Say it with the decision in the paragraph. |
| 9 | polish | paragraph before the table | "Suppose the operator cares about the pointing error and the sponsor about the unit cost and the fleet cost." | "Operator" and "sponsor" first appear here as roles without introduction in this section; I assumed they are the two stakeholders in the case. | A glance back to who they are (Section 8 presumably). |

Counts: blocks 1, slows 5, polish 3 (9 total).

## The six-row table read aloud, in my words
- baseline configuration: where the satellite design starts today, one satellite, 0.0155 degree pointing, 461 k USD. It fails the requirements and scores worst (-0.330). Not an option.
- sponsor alone: if the sponsor's priority (cost) rules, buy 4 small-wheel satellites with the ordinary tracker; 1.13 M total, pointing 0.003 degree.
- operator alone: if pointing rules, buy 6 satellites with the fine tracker; 2.06 M total, pointing 0.0007 degree.
- between them: a compromise; 5 satellites with the fine tracker, 1.69 M total, pointing 0.0008 degree. This is the "if it is worth it" answer in the text.
- balanced between the terms: I cannot say what "terms" means for me; 6 ordinary-tracker satellites, 1.60 M, 0.0028 degree. I read it as another middle option that is not discussed.
- cheapest unit cost: lowest cost per satellite (234 k) but needs 25 of them, 5.85 M, nearly the whole 6 M budget, so I read it as a warning that cheap per unit is not cheap per fleet.

## Does any sentence say the method decides or ranks?
No. The paragraph says the opposite: "The method prices the question and does not answer it". The table is labelled by "rule" (who is speaking) and not as a ranking, though the "level" column reads like a ranking score (higher = better) and the "between them" row (-0.012) sits below two rows I am told it "regrets least" relative to. That is the nearest thing to an implied ranking.

## Were the "nominal" clause and the "does not tell" sentence noticed, and what did they do to my trust?
Both noticed. "The numbers are nominal (Appendix C.8)" raised my trust: it tells me not to take 1.69 M as a quote, though I do not know what makes them nominal (I did not follow the link, per rules). "The method does not tell the schedule or the risk, what to buy beyond the modelled parts, or what a larger fleet is worth." raised trust further and also told me what to bring my own team for (schedule, risk, larger fleet). It also made me ask whether the "regrets least" claim for the 5-satellite fleet survives a different fleet size.

## What I could not tell
- What "the band" and "both fits" are, and how 28 reduces to "the 5 that trade the two measures".
- What "regrets least" is measured against.
- What the "level" number means in money or schedule terms.
- Why the 6 M USD is the budget (set by the case, I assume) and whether 0.56 M comes from the table (1.686 - 1.127 = 0.559, yes) or from a separate calculation.
- What "Table ??" points to.
