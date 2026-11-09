# Reader P2-B (trade-study practitioner, skim)

## 1. What this is about
A way to analyse a trade-study table of many candidate designs. It fits a smooth reference surface to the data and then reads off, for each cluster ("facet") of designs, which metrics are in tension and how much of one you give up per unit of another (elasticities). It is pitched as a PCA-like tool, but for trade-offs rather than variance. The example is a cubesat (power, mass, attitude control).

## 2. The main results, as I understood them
The fitted surface is not the Pareto boundary. The single-facet fit is convex, so it is solved reliably. The exponents act as percent-for-percent exchange rates. A design's position along the surface is kept separate from its level relative to it. With several facets the fit is not convex, so the paper gives tiered guarantees and a stopping rule. On the cubesat, three facets separate tension sets that one facet blends together.

## 3. Claims / does not claim
It claims a reproducible, explainable way to find and quantify tensions. It says outright that it does not claim the Pareto boundary, global optimality for several facets, or priority. Nothing here says it replaces weighted tables or tells me which design to pick.

## 4. Next
I would not run it myself yet. I would ask whether Section 11 ("your own case") lists the inputs I'd need to supply, and what conditioning of my metrics it expects.

## 5. One sentence for a colleague
It is a statistical fit that tells you which requirements fight each other, and by what exchange rate, instead of a weighted score.

## 6. Figures
Most helpful: Figure 2, a scatter of slew time against control effort with a straight descending line. I could see a tradeoff cloud and a line through it. Figure 5, the colour grids with the boxed sets, is dense but showed which metrics oppose each other. Least helpful: Figure 7, blue dots with a few pink diamonds and open circles, no axes meaning, and I could not tell good from bad. Figure 4 was also opaque: coloured dots on unexplained Z coordinates. Figure 3's bottom panel shows banded horizontal stripes, which looked odd.

## 7. Confusion
"The fitted reference surface is the unit level set of a degree-one weighted geometric mean". I stopped there. Also "energy differential" and "Theorem 12 ... Hessian H = D − κM".

## 8. Guessed terms
Facet (a cluster of designs?), n-lemma, tau (temperature, apparently how hard the maximum is), conditioned metric, support, "reach and share", stock versus primary regime.

## 9. Read the whole paper?
Probably only skim Sections 1, 9, 11. The theorems are beyond my use. I would read further if the case shows a decision changing.
