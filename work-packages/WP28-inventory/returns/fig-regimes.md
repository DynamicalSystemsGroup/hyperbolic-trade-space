# fig-regimes

## Q5 (a) What the image shows (written before the caption)

Two stacked heatmaps of an 8 by 8 matrix, one titled "primary: 5-lemma (5 metrics in the exact-maximum support)" and one titled "stock: 5-lemma (...)". The same eight metrics label rows and columns: settling time, pointing error, total mass, control effort, power margin, energy balance, peak slew power, depth of discharge. Each label carries a weight w (for example w=0.36 for total mass in the top panel, w=0.43 for control effort in the bottom). Some labels are greyed with w=0.00. The cells hold numbers between -1 and 1, diagonal 1.00, colour from brown (negative, "tension") through white to purple (positive). Some diagonal cells have a thick black box (the ones with nonzero weight, except in places where two metrics seem boxed together). The two panels differ: in the top, pointing error and peak slew power are -0.95; in the bottom, settling time and control effort are -0.95. Power margin and energy balance are 0.99 in both. Different metrics get the weight in the two panels.

## Q5 (b) After the caption

Mostly yes. The caption says association of log-metrics among near-frontier designs at K = 1, primary (aggressive gains) above and stock below, outlined = contending set, w = fitted exponent; the image has exactly that, and in each panel five metrics are outlined, matching "5-lemma". Small mismatches: energy balance in the stock panel has w=0.02 and is not outlined while its twin power margin (w=0.18) is, which the page text explains (a near-identical pair counted as one); and the image's own titles say only "primary" and "stock", so the reader needs the caption to learn these are controller-gain regimes. It does not show the K = 3 terms, the model, or what changes between regimes in one view (the reader must compare the two panels cell by cell), and it does not mark which metrics are shared.

## Q5 (c) Sentence test

"Under aggressive controller gains the contending set is settling time, pointing error, total mass, energy balance and depth of discharge; under stock gains, control effort and power margin take the places of total mass and energy balance." The figure carries more than the sentence: the sign and size of every pairwise association (settling time against control effort -0.95 in stock; pointing error against peak slew power -0.95 in primary; power margin and energy balance 0.99 in both) and the weights. But the page text already states the set difference in words, so the extra is the numbers behind it.

## Q1 What it conveys

That changing the controller gains changes which five metrics trade against each other (the contending set) and how the metrics associate.

## Q2 Sentence of the story served

None. Main-results item 7 says the terms separate contending sets that one term blends (K = 3); this figure is at K = 1 and compares regimes, not terms. The abstract has no sentence about two regimes or controller gains. Closest in spirit is item 7, but it does not need this figure.

## Q3 Verdict

does not advance. No sentence of the abstract or Section 1 needs the comparison of the primary and stock regimes; the story's case claim is about K = 1 versus K = 3. The figure is a legible, honest side-by-side, but what it supports (the problem's contribution versus the gains') is a Section 9 aside.

## Q4 If repeats

Not applicable (the same encoding appears in Figure 8, unit fig-tensions-k3, but it carries different content, so it is not a repeat).

## Q9 Could not place

- "5-lemma" in the panel titles (the story defines n-lemma; the K = 1 5-lemma is placed only on the page)
- "exact-maximum support" in the titles
- "the problem's contribution from the gains'" (page text, before the figure)
- the stock panel: energy balance w=0.02 not outlined, power margin outlined, without a mark on the figure saying they are a counted-as-one pair
