# docsfig-adcs-coordinates

## Q5

(a) A scatter plot of several hundred points in a plane with axes labelled Z0 (horizontal, about -3 to 2) and Z1 (vertical, about -3 to 3). Most points are small blue dots; a subset (perhaps a hundred) are drawn with a black outline. The outlined points are spread through the cloud rather than sitting on its edge, with some concentration along a band from the left (around Z0 = -2.5, Z1 = 0) through the centre and down to the lower right (around Z0 = 1.5, Z1 = -1). There is no legend, title or colour scale, so I cannot tell what Z0 and Z1 are or what the outline marks.

(b) Yes, as far as it goes: it is the 706 feasible designs in two coordinates with a ringed subset, which the caption says are the 193 nearest the frontier (I guessed about a hundred; I cannot count them to check 193). The caption itself says the two coordinates are "meaningless alone" and that it "shows coverage, not the frontier". What it does not show: what Z0 and Z1 mean in terms of the metrics, the other five coordinates, the frontier or any fitted term, and any gap in the table that a reader could name. Nothing in the image says what "ringed" means; only the caption does. Because the ringed designs are scattered across the whole cloud, the figure also does not show where near-frontier designs sit in any reading I can act on.

(c) Sentence: "In the first two of the seven chart coordinates the 706 feasible designs spread over the plane without an obvious hole, and the 193 designs nearest the frontier are scattered among them rather than in one place." The figure conveys a little more than that sentence: the actual shape of the cloud (wider in Z1 near Z0 = -0.5, thinner to the left) and that the ringed designs lean toward a diagonal band. But since the caption says the coordinates mean nothing alone, that extra shape is not something I can use.

## Q1

It shows the cubesat's feasible designs spread over the first two of seven chart coordinates, with the near-frontier designs ringed, as an example of what plot_frontier_coordinates draws.

## Q2

None directly. The nearest is the Home page's "where each design sits relative to the fitted reference surface, and where the table has gaps", but the figure, by its own caption, shows neither the frontier nor a gap I can read off two coordinates that are "meaningless alone".

## Q3

does not advance. The caption disowns the two things a reader would want from it (the coordinates mean nothing alone; it does not show the frontier), and what is left, "coverage" in two of seven coordinates, does not let me say where the table has gaps or where a design sits relative to the surface. Its remaining job is to show that the plotting call runs and what its output looks like, which the code block above it already tells me.

## Q4

Not applicable (verdict is not "repeats").

## Q8

- Home page (learn the shape of a trade space; which metrics contend, where each design sits, where the table has gaps): no; it names no metric, no term and no gap, and its axes carry no meaning.
- Root page (learn the shape of a trade space from evaluated designs; show its reasoning, say where the data do not reach): no; it does not say where the data do not reach, since coverage in two of seven coordinates cannot establish that.
- Examples page opening sentence ("The worked case is a cubesat model coupling power, mass and attitude control"): barely; it is the cubesat's designs, but nothing in it ties to power, mass or attitude control.

## Q9

- "the first two of seven position coordinates, meaningless alone": read twice; I could not place why a figure is drawn in coordinates the caption says are meaningless, or what "position coordinates" are on this page (the code calls them chart[:, :-1]).
- "It shows coverage, not the frontier.": coverage of what, judged how; the page never says what a reader should conclude about coverage from this plot.
- "193 ringed designs lie nearest the frontier": nearest by what threshold; the requirements table below speaks of 56 near-frontier designs for the primary regime, and I could not reconcile 193 with 56.
