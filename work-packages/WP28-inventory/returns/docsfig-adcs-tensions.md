# docsfig-adcs-tensions

## Q5 (a) What the image shows (written before the caption)

An 8-by-8 heatmap of pairwise association between eight spacecraft-style metrics (settling time, pointing error, total mass, control effort, power margin, energy balance, peak slew power, depth of discharge). Title: "term 1: 5-lemma (5 metrics in the exact-maximum support)". Each row/column label carries a weight w (0.14, 0.16, 0.36, 0.00, 0.00, 0.18, 0.00, 0.16). Cells are numbers from -1 to 1 on a purple (positive) to orange (negative) scale, labelled "association (negative = tension)". The diagonal is 1.00. Five of the diagonal cells (settling time, pointing error, total mass, energy balance, depth of discharge) have thick black boxes; the other three metrics (w=0.00) have greyed labels. Strongest negative: pointing error vs peak slew power -0.95. Strongest positive: power margin vs energy balance 0.99. Total mass is negative with settling time, pointing error and depth of discharge (about -0.5 to -0.64) and positive with control effort and peak slew power.

## Q5 (b) After the caption

Mostly yes. The caption says cells are the correlation of the log-metrics near the frontier, outlined is the contending set, grey is metrics that do not participate. The image has all three: numbers in cells, five outlined diagonal cells, three greyed labels. It does not show: the weights are on the image but the caption never explains "w" or "term 1" or "5-lemma" or "exact-maximum support"; the outline marks only diagonal cells, not the pairs among the contending set, so the eye cannot read "contending set" as a block; and nothing shows how many designs are "near the frontier". The alt text says "association", the caption "correlation", the colour bar "association": three words for one thing. The image shows no frontier, no designs, and no consequence of a tension.

## Q5 (c) The sentence test

Sentence: "In the one-term fit of the cubesat study, five of the eight metrics (total mass, energy balance, pointing error, depth of discharge, settling time) carry the weight and are the ones that contend; mass trades against most of the others."

The figure conveys more than that sentence: the full pairwise values (pointing error vs peak slew power -0.95 for a non-participating metric; power margin vs energy balance 0.99) and the weights (mass 0.36 largest). The page text already gives the five names, so the figure's extra is the matrix and the weights.

## Q1 What does this figure convey?

The pairwise tensions among the cubesat's eight metrics near the frontier, with the five that the one-term fit weights marked.

## Q2 Sentence served

Home: "It then tells you which metrics contend, with what elasticity" (the contending part, not the elasticity). Page: "The tension report finds a contending set ... of five metrics". Root: "PCA explains variance; this explains tensions."

## Q3 Verdict

repeats. The figure is the worked-case instance of the tension report; the page text already names the five metrics, and a figure of the same kind of report sits on the tension guide page. What the example adds (the real values) is not discussed in the page text, so a reader does not know what to take from them.

## Q4 If "repeats"

docsfig-tension-report (Figure 3 on 'User guide: Tensions'), which I have not read; I name it from the unit list on the strength of its title. In the paper, fig-tensions-k3 is the three-term version.

## Q8 Against Home, root, page opening sentence

- Home: partly helps ("which metrics contend"); it shows a result but not how to read one, and "elasticity" is not shown.
- Root: weakly; "explains tensions" is shown as numbers, with no link to the n-lemma wording beyond "5-lemma" in the title.
- Page opening sentence ("a cubesat trade study across power, mass and attitude control"): helps; it shows the eight named metrics of that study and where mass sits.

## Q9 Could not place

- "5-lemma" and "exact-maximum support" in the title
- "w=0.00" (weights; unexplained in caption)
- "association" vs "correlation of the log-metrics"
- Page text says "No pair of the eight metrics reaches a rank correlation of 0.99" while the figure shows 0.99 (power margin, energy balance); the two measures differ but the page does not say how
- The -0.95 pair involves a grey metric (peak slew power), but the page never says what a strong tension outside the contending set means
