# fig-planes-k3

## Q5

### (a) What the image shows (written before the caption)

Three stacked scatter plots, each titled "term k" and each pairing two log-metrics (all "larger is better"): term 1 is settling time against control effort, term 2 is total mass against energy balance, term 3 is pointing error against peak slew power. Each panel shows the design points in two greys (dark: designs whose other six metrics are near the median, within 0.1 in log V; light: the rest) and one straight black line of negative slope, "the term's line in this slice". In every panel the line runs along the upper-right edge of the cloud, so most points lie below or on it and a few sit above it. Term 1's cloud is irregular, with diagonal streaks of points (lines of positive slope) rather than a filled region. Term 2's cloud is a diffuse filled blob. Term 3's points sit in discrete horizontal bands (two levels per pointing-error cluster), clearly quantized in both metrics, and almost all of them are dark; the line touches the upper bands. The picture says: for each of three pairs of metrics, a straight trade-off line in log space bounds the designs from above, and which pair goes with which term is fixed.

### (b) After the caption: does the image show what the caption says? What does it not show?

Mostly yes. The three panels are the three K = 3 terms, each in a different pair of metrics, each with its own line and its own slope. The structural details the caption explains are all visible and match: the top panel has two straight streaks of slope about +1 (consistent with control effort = torque times settling time once both are inverted and logged), one mostly light and long, one shorter and lower; the bottom panel has the two narrow columns (near -1.1 and near 0), the wide band (about 0.4 to 2), six upper horizontal bands (two per column/grade) and a lower cloud near -1.1 to -1.4; and nearly all points in the bottom panel are dark, as the caption says.

Where it falls short of its own "Shows" line ("the designs near its slice's median stopping at its line"):
- Top panel: the dark designs do not visibly stop at the line. Many dark points lie far below it, light points sit above it as often as dark ones, and the left half of the line (log settling time below about -1) has no designs near it at all. The panel reads as "a line drawn over a cloud", not "an edge the dark designs reach".
- Bottom panel: the upper bands reach the line only at the right end (fine grade); at the left the coarse column sits just under it and the lower cloud is far below. The line is fitted across stepped alternatives, which the image shows and Section 9 says, but "stopping at its line" is only partly seen.
- Middle panel: the claim holds best here; dark points reach the line with a few beyond it.

What it does not show: the slope value (the elasticity) is not printed on any panel, so the -1.7 for term 2 quoted in the text has to be read off the axes; which designs belong to each term's cell (the median is taken over them but they are not marked); the term shares (term 1 carries 0.03, term 3 0.72), so the three panels look equally weighty when they are not; the other metrics of each contending set (term 1's set has four, term 2's and 3's five); and, as the caption says, no place where two terms meet. The legend appears only in the middle panel.

### (c) The sentence test

"At K = 3 each term has its own trade-off: control effort against settling time, total mass against energy balance (elasticity -1.7), and peak slew power against pointing error, stepped by the tracker grade and wheel class."

The figure conveys more than that sentence: it shows that the three terms sit in different pairs of metrics with visibly different slopes; it shows the term-3 trade is between discrete part choices, not a continuous trade (the bands and columns), which the text leans on ("the bottom panel of the K = 3 planes"); it shows the torque-limited streaks in term 1; and it is the only picture of term 1, which has no association map in Figure 8. It conveys less than the sentence in one respect: the slopes are not labelled, so the elasticity number is not readable without the text.

## Q1

At K = 3 each of the three terms has its own trade-off, drawn as a line with its own slope (elasticity) in its own pair of metrics, with the designs near each term's slice lying below it.

## Q2

Main-results item 7: "the terms separate contending sets that one term blends (Section 9)"; also the abstract's closing words, "three terms separate the contending sets".

## Q3

advances. Item 7 says the terms separate what one term blends, and Section 9 argues the terms add a model over a clustering because they give elasticities; this figure is the one place those per-term elasticities appear as slopes, each in a different pair, against Figure 5's single line. Figure 8 names the contending sets but gives no slope and has no map for term 1, and the text cites the bottom panel to explain why term 3's elasticity is read across part swaps; no other unit carries that. The top panel is the weak part: its line does not visibly bound the dark designs, so the "stopping at its line" claim is not seen there.

## Q4

Not "repeats". Partial overlap: Figure 8 (unit fig-tensions-k3) carries the contending sets per term; Figure 5 (unit fig-planes-k1) carries the same kind of plot for K = 1. Neither carries the per-term slopes or the term-1 trade.

## Q9

- "the median of the near-frontier designs in the term's cell (the designs the term scores highest)": what a term's cell is, and how a design is assigned to it, is given only in this parenthesis; I could not tell how many designs are in each cell or see them in the image.
- "No drawn pair is weighed by a second term": term 1's contending set includes pointing error, which is also term 3's drawn metric; I read this twice and could not tell whether "pair" means both metrics together, so whether the claim needs that reading.
- "the term's line in this slice" versus Figure 5's "the line is the surface in this slice": at K = 3 is each term's line the surface in that slice, or only that term's piece of it, which the surface lies above where another term dominates?
- "the figures of this section ... use the K = 1 band at every K (gap G-9, Appendix E)": I could not place what this changes in Figure 6 (the 0.1 dark/light threshold is stated in log V, not in bands).
