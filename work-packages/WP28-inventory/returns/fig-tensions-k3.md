# fig-tensions-k3

## Q5

### (a) What the image shows (written before the caption)

A figure about three "terms", each described as a "lemma" with a count of metrics "in the exact-maximum support". Term 1 (a 4-lemma) has no plot, only a line saying there are too few near-frontier designs for an association reading (3 of ten). Terms 2 and 3 (both 5-lemmas) each get an 8 by 8 symmetric matrix over the same eight metrics (settling time, pointing error, total mass, control effort, power margin, energy balance, peak slew power, depth of discharge). Each metric label carries a per-term weight w; metrics with w = 0.00 are greyed out. Cells are coloured on a diverging orange-to-purple scale from -1 to 1 labelled "association (negative = tension)", with values printed in each cell. Some diagonal cells have a thick black outline, apparently marking the metrics in the support.

What can be read off: in term 2, settling time is in strong tension with peak slew power (-0.85) and total mass (-0.67), pointing error with total mass (-0.65); power margin and energy balance move together (0.96). In term 3, pointing error and peak slew power are in perfect tension (-1.00), pointing error against total mass and control effort (-0.68 each); power margin and energy balance again move together (0.99). The two terms show different tension patterns, which suggests each term describes a different region or regime of the trade space.

Things that look odd on first sight: in term 3 energy balance has w = 0.00 (greyed) but its diagonal cell seems outlined, while power margin (w = 0.02) is not outlined; and I cannot clearly see which fifth diagonal cell is outlined in term 3 (settling time's border is hard to make out). Associations among greyed (zero-weight) metrics are still shown at full strength.

### (b) After the caption

Mostly yes. The caption explains the two things I could not place: the colours are Pearson correlations of the log-metrics among the near-frontier designs in each term's cell (an analysis of designs, not of the model), and the outline marks the contending set at the exact maximum while w is the exponent at the fit temperature, greyed below a participation threshold, "so an outlined metric can be grey". That accounts for energy balance in term 3 (outlined, w = 0.00) and power margin in term 3 (w = 0.02, grey and not outlined, which tells me the threshold is above 0.02). The missing term-1 map is explained by the "fewer than ten" rule.

What it does not show: term 1's map, so the figure covers only two of the three terms it is captioned for; term 1's contending set is given only in the section text. In term 3 I still cannot make out the fifth outlined cell with confidence (four are clear: pointing error, total mass, energy balance, peak slew power; settling time's border is faint against its dark fill). The colour scale and the outlines speak different languages (associations among designs versus the fit's support), and nothing on the image itself says which is model and which is analysis; that is only in the caption. The figure does not show elasticities, the quantity the story says each term reports.

### (c) Sentence test

Sentence: "On the K = 3 fit, term 2's contending set is settling time, pointing error, total mass, energy balance and depth of discharge, led by energy balance (0.42); term 3's is led by peak slew power (0.61) with pointing error (0.23), and among each cell's near-frontier designs pointing error trades against peak slew power (-1.00) on term 3 while settling time trades against peak slew power and total mass on term 2."

The figure conveys more than that sentence: the full set of pairwise associations per term (28 pairs each), showing which pairs do not trade (near zero) and which move together (power margin with energy balance at 0.96 and 0.99), and the exponent of every metric including the small ones. Whether that extra is needed by the story is less clear; the story's claim is about the contending sets, which the outlines and w labels carry, not about the associations.

## Q1

For terms 2 and 3 of the K = 3 fit, the figure names each term's contending set with its exponents and shows, among the near-frontier designs of that term's cell, which metric pairs are in tension, so that the two terms visibly have different sets and different tensions.

## Q2

Main-results item 7 ("the terms separate contending sets that one term blends"), and the abstract's closing "three terms separate the contending sets".

## Q3

advances. Item 7 needs the reader to see that the K = 3 terms have different contending sets, and this is the only unit in Section 9 that shows the sets of terms 2 and 3 in full: the text gives their sizes (4, 5, 5) and term 1's members, but not the members of terms 2 and 3, and Figure 6 shows only each term's two heaviest metrics. The weakness is that most of the ink is the association heatmap, which the section itself calls an analysis of designs rather than of the model, and one of the three terms has no map at all.

## Q4

Not applicable (verdict is not "repeats").

## Q9

- "grey below the participation threshold": the threshold's value is not given on the page; I can only infer from term 3 that it lies above 0.02.
- Term 3's fifth outlined metric: on the image I cannot tell with confidence whether settling time's diagonal cell is outlined, and the section text does not list term 3's contending set.
- "the figures of this section and the association reading use the K = 1 band at every K (gap G-9)": I could not place how this band defines which designs count as near-frontier in each term's cell, or why it is the K = 1 band.
- "The term shares are 0.03, 0.24 and 0.72": not clear how a term share relates to the count of near-frontier designs in its cell (term 1 has 3).
