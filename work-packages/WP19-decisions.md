# WP19 — Decision records (figures: selection, generation and narration)

Approval: by the driver under the mandate, 2026-11-09 (`WP19-scope-of-work.md`, gate outcomes). The supervisor
reviews every slot and figure; his verdicts are recorded here verbatim.

## Figures 3 and 4 present facets as clusters (2026-11-09, 20:55)

**Supervisor (mzargham), verbatim,** looking at Figure 3 (log-metric planes at K = 3, designs coloured by facet,
facet lines drawn) and Figure 4 (the chart at K = 3, coloured by facet): "i think the confusion about the "facet"
concept comes from these plots. they are reminiscent of how the scikit-learn documentation deals with clusters which
is why the cluster confusion but they don't really show clusters. in fact i am having a hard time understanding the
role they plan. they may be left over from you trying to mimick scikit-learn style and inadvertently introducing
false anologies"

**Reading.** The colour of a design in these figures is the facet whose term scores it highest: an analysis choice
(the assignment), drawn in the idiom scikit-learn uses for cluster membership. The model in Figure 3 is the black
lines and the kink (the facets as pieces of the surface) and the near-frontier band; the colours present the
analysis as if it were the model's structure, and the reader grid's "facet as cluster" reading (rounds 1 and 1b)
follows from it. Figure 4 draws no model at all: coloured points on chart axes, least helpful for readers in both
rounds.

**Principle, added to the figure review** (`docs/superpowers/notes/figure-review.md`): a figure borrows no idiom
that carries a false analogy; colouring designs by facet is the cluster idiom and is not used; what a figure shows
of the model (surface, band, lines) is drawn as the model, and what it shows of the analysis (assignment, shares) is
named as analysis in the caption or not drawn. Every current figure, paper and docs, is checked against this once.

**Slot decisions (the driver, under the mandate; candidates for his judgement).**
- Figure 3 (S-d2): keep the slot; redraw without facet colouring: the designs in one neutral colour, the facet
  lines and the band as the model, near-frontier designs outlined if the sentence test needs them. The caption step
  already drafted (C-d2) is re-read against the redrawn figure. Regenerated with the WP23 data like every figure.
- Figure 4 (S-d3): the sentence test stands (C-d3): if the chart has a sentence it alone can carry (the chart
  separates position along the surface from level: one picture of Z against log V), it is redrawn to show that
  with no facet colouring; otherwise it is dropped.

**The driver's image reads of the redraws (2026-11-09, 21:15; 141653c; candidates for his judgement).**
- Figure 3 redrawn (`fig-planes-k3.png`): grey designs, the surface as black segments labelled by facet, the band
  as a thin strip; the kink in the middle panel is the picture's content. Cold sentence: the surface in each
  slice is one segment per facet, bending where two facets meet; designs sit on either side of it. The cluster
  idiom is gone; what is drawn is the model. Passes as a candidate.
- Figure 4 redrawn as position against level (`fig-chart-level.png`): the surface is the line log V = 0, the
  designs hang below it, a few sit just above, the band a thin strip under the line; the x-axis is the first
  position coordinate, labelled as having no meaning alone. Cold sentence: the chart puts every design at a
  position along the surface and a level below it; the surface is a soft support that a few designs exceed. That is
  the abstract's sentence drawn, so it earns its place if the caption says it. Passes as a candidate.

## The principle check over every figure (2026-11-09, 21:20; findings at 3cd2722; the driver's dispositions)

- Paper Figure 2 (planes at K = 1, designs labelled "facet 1"): the membership idiom in one-facet form; redraw with
  the same generator as Figure 3 (grey designs, the surface, the band).
- Paper Figures 5 and 6 (tension heatmaps, the drawing he liked): keep the drawing; the caption names the cells as
  analysis of the designs assigned to each facet.
- The index page's three-pane figure (designs coloured by facet in every pane; a chart pane drawing "facets as
  regions", exact only for two metrics): designs in one colour; the regions pane passes the sentence test as
  analysis named in its caption or is dropped. The index figure is the high-level story arc he asked for; it keeps
  that job.
- Docs Figure 2 (three facets, the cluster idiom) and docs Figures 3 and 6: as the paper's 3, 5 and 6.
- The package default: `plot_log_plane` colours designs by facet for K > 1, which draws the idiom by default for
  every user. The default becomes one colour with the facet lines drawn; colouring by assignment stays available
  as an explicit option, documented as analysis. A small package unit outside WP19 (WP21's successor or WP8b's
  punch list), with the interface contract amended if it names the function's behaviour.
- Docs Figure 8 (the planted ternary he called great; near-frontier designs coloured by facet): his to judge; put
  to him as one popup.
- No issue: the paper's Figure 1 (the n-lemma ternary), the two views, docs 1, 4, 5, 7.

**Docs Figure 8, the planted ternary (2026-11-09, 21:25).** **Driver's question (popup):** recolour the
near-frontier designs to one neutral colour, keep the facet colouring with the caption naming it as analysis, or
look again. **Supervisor (mzargham), verbatim:** "Recolour". Disposition: the designs go to one neutral colour; the
stars, squares and triangles (exponent vectors and planted answers) carry the figure as before; the docs prose
about the values at the marked points is unchanged.

## The tension heatmap's missing term (2026-11-11, 12:10; the supervisor, verbatim, on the K = 3 tension figure)

"leaving the first term off the picture feels wrong to me." (The figure draws terms 2 and 3 and replaces term 1's
panel with the line "Too few near-frontier designs for an association reading: 3 of ten".)

**The assistant's call.** Every term is drawn. A term whose cell holds too few near-frontier designs for a correlation
gets its panel like the others: its title with the n-lemma count, its metrics with their exponents, the contending set
outlined, and the correlation cells left empty (no colour, no number) with the reason written inside the panel in one
line ("3 near-frontier designs; no association reading"). The fix goes in the plotting function that draws the per-term
panels, so it holds for any fit, with a test on a planted case that has a thin term; contract row 11 unchanged (no
signature change); the paper's and the docs' renders regenerate from the same function; a cold read of the redrawn
figure image first, then the caption says what an empty panel means. It lands before the WP30 regeneration so the
regenerated figure inherits it; the thin term after the regeneration is whatever the data give.
