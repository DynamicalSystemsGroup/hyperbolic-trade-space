# Read P8 re-read (R-7): Section 9 to "What the executives decide"

Persona P8, new-space program/business-line executive. Page: http://127.0.0.1:8791/paper/ (head 8699324), Section 9 "Case analysis" through its closing subsection and Table 2. Read in own browser tab (tab-122), rendered page text only. No repository, notes or key opened.

## The call, in my own words

The paper ends the case with a single question that is mine to answer: is a finer star tracker, which cuts pointing error from about 0.003 to 0.0008 degree, worth about 0.56 M USD of a 6 M USD fleet cost limit? If yes, buy 5 satellites with medium wheel and fine tracker, 1.69 M USD for the fleet (337,000 USD each). If no, buy 4 satellites with small wheel and medium tracker, 1.13 M USD, the cheapest. The requirements and the method's frontier cut 2,134 feasible designs to 28 that pass everything, and the five-satellite fleet is the pick that sits between the two stakeholders (operator wants accuracy, sponsor wants low cost). The method does not decide: it "prices the question and does not answer it", and it says nothing on schedule, risk or what a larger fleet is worth. The numbers are nominal.

## Q1. Could I follow the reduction to the call without the subsystem detail?

Yes for the last paragraph taken alone; the route to it through the section I did not follow. I stopped following at "At K = 1 the exact-maximum fit has a 7-lemma across controls, power and energy, plus cost" (Section 9, third paragraph), and everything from there to "Two regimes" (terms, K, tau, Figures 5-8) was noise to me; I skipped to "What the executives decide", which stands alone.

## Q2. Easier or harder?

Easier at the end, harder in the middle: "One question remains, and it is theirs: whether a fine star tracker, which brings the pointing error from about 0.003 to 0.0008 degree, is worth about 0.56 M USD of a 6 M USD fleet cost limit." (What the executives decide, sentence 3.)

## Findings

| # | Severity | Place | Verbatim quote | What happened | Expected |
|---|----------|-------|----------------|---------------|----------|
| 1 | slows | Section 9, opening line | "what contends, how, and where designs sit (the executives' call: Table 2; tables: Appendix D; digits that hold: D.11)" | Points to the call early, which helps, but in the same breath names three other places; I did not know what "contends" or "digits that hold" meant | Say plainly: "the decision is in Table 2 at the end of this section" |
| 2 | slows | Section 9, "One term" | "the exact-maximum fit has a 7-lemma across controls, power and energy, plus cost" | Where I stopped following; "7-lemma" and "exact-maximum fit" are method words with no gloss | A plain phrase such as "seven of the thirteen measures drive the trade-off" |
| 3 | slows | Section 9, "Two terms" | "the mean slack, read at the K = 1 temperature, drops most at K = 2 (0.08 and 0.05)" | Unreadable for me; no sign whether it matters to the decision | Mark this stretch as method detail that can be skipped, and say what it means for the call |
| 4 | slows | "What the executives decide", sentence 4 | "gives up the least of either measure among the 5 of the 28 that no other beats on both" | Read twice; plain enough once I saw it as "the best compromise of the five undominated fleets", but "the least of either measure" is dense | Name the compromise and say what it costs against each end |
| 5 | polish | "What the executives decide", sentence 2 | "lie in the near-frontier band of both fits, the simpler and the richer" | "near-frontier band" and "both fits" are method vocabulary; I read them as "the designs closest to the best possible" | A short gloss or drop "of both fits" |
| 6 | polish | Table 2 caption | "level of each (log V at K = 2: the distance above or below the fitted reference surface, not a ranking)" | "log V at K = 2" means nothing to me; the "not a ranking" clause helps | Say "level: how far the design sits from the model's reference; not a score" and drop "log V at K = 2" from the caption |
| 7 | polish | Table 2 | row "operator alone", level "+0.010" next to "between them", level "-0.012" | A reader can take a higher level as better; the caption denies it but the column sits last and looks like a score | Put "not a ranking" in the column header |
| 8 | polish | Section 9 text | "Figure 5:Log-metric plane of the K = 1 fit..." and "enlarge" after Figure 7 | Caption text runs into the label with no space ("Figure 5:Log-metric"); stray "enlarge" is page chrome | Space after colon; hide the control from the text flow |

Counts: blocks 0, slows 4, polish 4.

## "Table 2" and "Table ??"

"Table 2" resolves: the opening line of Section 9 cites it, the caption reads "Table 2:The baseline configuration and the designs the rules pick...", and the table is present with six rows. A search of the whole rendered page text finds 0 occurrences of "Table ??". The caption has the same missing space after the colon as the figures.

## The three wordings

- "band": not plain. In "the near-frontier band of both fits" I read it as "close to the best", acceptable by guess; "within the regressor's own band 1/tau = 0.0935" is not plain at all (that sentence is in the part I skipped). In the final subsection the single use is tolerable.
- "gives up the least of either measure": plain after one re-read. It means the pick is the fairest compromise between pointing error and cost. It reads better than the old wording would have but it is still the densest phrase in the closing paragraph.
- "level": plain only through the caption's gloss ("the distance above or below the fitted reference surface, not a ranking"). Without the caption, "level" in the column header means nothing; with it, I understand it as "how far from the model's ideal" and I take it as not decision-relevant.

## The table read aloud

Six options. The baseline (medium wheel, medium tracker, one satellite) misses the requirements: pointing error 0.01553 degree, cost 461,360 USD. "Sponsor alone": small wheel, medium tracker, four satellites, 0.00295 degree, 281,866 each, 1,127,465 for the fleet; this is the cheap fleet that meets the requirements. "Operator alone": medium wheel, fine tracker, six satellites, 0.00074 degree, 343,961 each, 2,063,765 for the fleet; the most accurate. "Between them": medium wheel, fine tracker, five satellites, 0.00080 degree, 337,228 each, 1,686,142 for the fleet; nearly the operator's accuracy for about 380,000 USD less. The last two rows are context: a balanced pick of six at 1,597,160 and the cheapest unit, 233,852 each, which needs 25 satellites and 5,846,300, close to the 6 M limit. Level column: small numbers near zero, caption says not a ranking.

## Does any sentence say the method decides or ranks?

No. "The method prices the question and does not answer it" (What the executives decide) and "not a ranking" (Table 2 caption) say the opposite, and "One question remains, and it is theirs" puts the decision with the executives. One near miss: "the designs the rules pick" (Table 2 caption) reads as the method picking; "rules" are stated to be in Appendix D.19, so I took it as the analyst's selection rules, not the method deciding.

## What I could not tell

- Whether 0.56 M USD is the price of the fine tracker alone or the fleet difference between the options (the five-fleet at 1.69 M versus the four-fleet at 1.13 M is 0.56 M, so I infer the second, but the text does not say).
- Why the operator-alone fleet of six is not the answer when pointing error matters most to the operator; presumably the cost limit and the "no other beats on both" filter, but I cannot see it.
- What "the numbers are nominal (Appendix C.8)" means for the dollar figures: whether they are estimates or placeholders.
- How uncertain the 28-design shortlist is.
- What the schedule or the risk looks like; the page says outright the method does not tell it.

The Section 9 body before the final subsection (Figures 5-8, K, tau, terms) I could not follow, as noted in Q1.
