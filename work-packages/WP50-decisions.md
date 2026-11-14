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

## Two objectives of the search (2026-11-14, 22:15)

**Supervisor, verbatim:** "i want to add that this approach to TDA should make whitespace filling a measurable objective distinct from advancing the
frontier (of the envelope) because holes are measurable with persistent homology"

**Applied as:** G4 amended. The readout treats the search as having two measurable objectives and keeps them apart:
advancing the frontier (the envelope's level, log V, which the fit already measures) and filling white space, which
becomes measurable once holes are classes of a persistence diagram (their number, their persistence, and how a new
sample changes them). The readout says what the measure of a hole is, how a proposed sample would be scored against
it, and how that score sits beside the level in the search of Section 7, so a sampling rule can trade the two. The
word objective here is the decision layer's, as the glossary has it.

## A hole is a hypothesis until sampled (2026-11-14, 22:20)

**Supervisor, verbatim:** "its not TDA for its own sake. we don't want to mistake an absense of witnesses for a hole, we can try to sample to find
witnesses"

**Applied as:** the purpose is the search's measurement, not the topology. A persistent class in the sampled chart is a
candidate hole, which may be only an absence of witnesses; the sampling rule targets it to find witnesses. Three
outcomes, as the bridge's proposals have (WP41): a witness is found and the white space is filled; no witness can be
produced after a stated effort and the hole stands with that evidence; the region is infeasible, which is a true hole
of the attainable set. G3 and G4 amended so the readout defines hole with this test built in, and the instance shows a
candidate hole resolved both ways (one filled by a witness, one that stands).

## The search's two aims, in one line (2026-11-14, 22:25)

**Supervisor, verbatim:** "the two kinds of things we want to be able to do is find and where possible characterize and potentially \"fill in\" holes
within the envelope, and push the envelope"

**Applied as:** the readout's frame, stated in its first lines and used throughout: within the envelope, find holes,
characterize them where possible (size, persistence, which metrics bound them, whether witnesses can be sampled) and
fill them in where they can be; and push the envelope (advance the frontier). The same two aims are the search's in
WP41 (`WP41-decisions.md` carries the cross-reference), where filling in is the witness sampling of 22:20 and pushing is
the proposal beyond the surface, each a conjecture settled by building and measuring.

**Supervisor, verbatim (22:27), on the two aims:** "these are fundamentally complementary"

**Applied as:** the readout presents them as complementary, not competing: filling in makes the envelope's interior
known (each witness is a measured design that tightens the fit and settles a hole), and pushing the envelope opens new
interior to fill; a sampling rule serves both in turn rather than trading one away for the other, and the readout's
"trade the two" of 22:15 is read as allocating effort between complementary aims, not as a conflict.

## After the readout: the abstract's last sentence (2026-11-14, 23:15)

**Supervisor, verbatim:** "after you get through the WP 50 research spike, i want to assess changing the last sentence of the abstract to be a list of
3 items with TDA for hole identification and filling work second, and the formal methods and performance clause 3rd."

**Applied as:** a step after the WP50 readout, his to decide then: the abstract's closing sentence ("Future work has two
key thrusts: (1) searching the design space by sampling white space and pushing the frontier, and (2) formal
verification and performance by moving beyond Python into Rust and using theorem provers.") assessed as a list of three:
(1) the search of the design space, (2) hole identification and filling by topological data analysis, (3) formal
methods and performance. The readout's G5 drafts that three-item sentence beside the one-sentence future-work line, in
his register (a term corrected, nothing else), within the abstract's 500-word target with its tolerance, so the
assessment has the text in front of it. The abstract is not touched before his word.

**Supervisor, verbatim (23:20), on the same:** "the spike will tell us whether this is a fruitful enough research direction to name. i am inclined to name it in order to
plant a flag for future work, and will tolerate going a few words over 500."

**Applied as:** the readout's boundary section answers one question first, in a line: is the direction fruitful enough to
name in the abstract, with the reasons either way (what the instance showed, what the literature establishes, what the
first package would be). His inclination is to name it, to plant a flag for future work, and a few words over 500 are
tolerated for it (the ledger's tolerance of 25 already allows this; no ledger change). The decision is his after the
readout.

