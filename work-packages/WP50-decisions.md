# WP50 — Decisions: topological holes in the chart, a future direction by persistent homology (research spike)

## The direction (2026-11-14, 20:35), given while naming the chart's unoccupied regions (WP42 item 1)

**Supervisor, verbatim:** "whitespace. we should reserve hole for future work where we use this peicewise-affine space and data to create distances and
then simplicial complexes to find topological holes. these will emerge naturally when we start sampling strategically, and we
need a way to define them which will allow us to go beyond the envelope method. this is its research spike but to characterize
a direction of future work that leverages our coordinate system and data points along with persistent homology. you will
notice from my other work that i am very interested in topological data analysis. white space for now. hole reserve for future
work. current spike is just research to establish a clear future direction based on TDA"

**Applied as:** a research spike with a readout, `WP50-scope-of-work.md`: how the chart's coordinates and the sampled
designs give distances, which simplicial complexes those distances build, what persistent homology would report as a
hole there and how that differs from the white space the envelope method sees, how strategic sampling would make holes
emerge, and what the tools and the literature offer; the readout ends with what 0.1 may say about it (at most a
future-work sentence, his to accept), what it may not, and what a later release would build. The word hole is reserved
for this object and left undefined in 0.1.

## Approval (2026-11-14, 21:35)

**Supervisor, verbatim:** "you can approve WP50, you may also want to look at my knowledgecomplex repo and our past conversations about topological
data analysis. but don't bias toward my work, just use that as a source of understanding of my intrerests and intuitions. to
greatest extent possible i think Ghrist's barcodes paper and the topological landmarks and sensor network coverage work  as
point of departure for theory, we're just using out learned coordinate system to figure out what is near what"

**Applied as:** WP50 approved as scoped, with G2 amended to name the point of departure he gives: Ghrist's barcodes
paper (persistent homology as barcodes), the topological-landmarks work (landmark and witness complexes) and the
sensor-network coverage work (coverage by persistent homology without coordinates), with the thesis in his words: the
learned coordinate system (the chart) is used to decide what is near what. His `knowledgecomplex` repository and his
earlier work on topological data analysis are read by the unit as a source of his interests and intuitions, not as the
literature to build on and not to be favoured. Dispatched to PM15.

