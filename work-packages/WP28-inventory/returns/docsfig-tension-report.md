# docsfig-tension-report

## Q5

(a) Before the caption: a 3-by-3 heat map titled "trilemma (3 metrics contend)". Rows and columns are three metrics, m0, m1, m2, each labelled with a weight (w=0.30, 0.37, 0.33). The diagonal cells are 1.00 in dark purple; every off-diagonal value is negative (m0-m1 -0.49, m0-m2 -0.38, m1-m2 -0.62) and drawn in shades of orange. The colour bar runs from -1 to 1 and is labelled "association (negative = tension)". The diagonal cells have heavy black borders, which look like one block per metric. My reading: each pair of the three metrics pulls against the others, m1 and m2 most strongly, so all three are in mutual tension, which the title calls a trilemma.

(b) After the caption: yes, the image shows what the caption says. The colour scale is association, the three off-diagonal cells are negative and orange (traded), and the diagonal outlines mark all three metrics as the contending set, which matches the alt text. What it does not show: the caption does not say what the "w=" numbers beside each metric are (I take them to be the contending exponents, but neither the caption nor the page names them); it does not show the elasticities, the band that picked the near-frontier rows, how many rows that was, or whether the correlation is Pearson or Spearman. The page warns that a binding constraint produces negative association by itself and that association is evidence only together with the exponents and directions; the figure gives the exponents (if that is what w is) but not the directions, and the caption does not repeat the warning, so the orange can read as "these metrics were traded" more strongly than the page allows.

(c) The sentence: "On the three-metric example, all three metrics contend (a trilemma, exponents about 0.30, 0.37, 0.33), and near the frontier each pair is negatively associated, m1 and m2 most strongly (-0.62)." The figure conveys a little more than that sentence: it shows the user what plot_tensions draws, so they can recognise the output of the call just above it (layout, colour convention, outlines, weight labels). The numbers themselves are all in the sentence.

## Q1

On the page's three-metric example, the tension report finds all three metrics contending, with every pair negatively associated near the frontier, and this is what plot_tensions draws.

## Q2

Home page: "It then tells you which metrics contend, with what elasticity"; root page: "a guide per task from conditioning your attributes to reading a tension report".

## Q3

advances. The Home page promises the package tells you which metrics contend, and the root page promises a guide to reading a tension report; this figure is the one place that shows the user the plot_tensions output for the call they have just been given, so they know what to look for in their own report. The case-study figure on Examples (docsfig-adcs-tensions) may show a tension report too, but on the cubesat table, not on the minimal code the guide runs, so it does not carry this. The figure is weaker than it could be because "w=" is unexplained and elasticities, which the Home sentence names, are not shown.

## Q4

Not "repeats". The nearest unit is docsfig-adcs-tensions (Figure 6 on 'Examples'), which I have not read.

## Q8

- Home page ("tells you which metrics contend, with what elasticity"): helps for "which metrics contend" (outlines, title "trilemma"); does not help for "with what elasticity", which the figure does not show.
- Root page ("a guide per task ... to reading a tension report"): helps; it is the picture of the report the guide teaches the user to read, placed right after the call that draws it.
- Page's opening sentence ("returns a frozen TensionReport that says which metrics contend and how they trade"): helps for which metrics contend; for how they trade it shows association only, which the page itself says is not enough on its own.

## Q9

- "w=0.30", "w=0.37", "w=0.33": the labels on the axes are not named in the caption or the page; I assume contending exponents but could not confirm it.
- "diagonal outlines mark the contending set": read twice; the heavy borders around each diagonal cell look like separate boxes per metric rather than one outline of a set, so with fewer contending metrics I would not be sure how it looks.
