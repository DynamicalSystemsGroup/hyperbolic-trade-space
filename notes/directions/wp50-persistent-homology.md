# WP50 D-4: readout, holes in the chart by persistent homology

Read 2026-11-14 at `dev` a1879e6. Sources: `objects-and-distances.md` (D-1), `construction-and-tools.md` (D-2), `instance.md`
(D-3). This readout defines nothing in the package or the paper and changes no file outside `work-packages/WP50-rounds/` (`git show 5233126:work-packages/WP50-rounds/`).
The sentences in "The boundary" are drafts for the supervisor's decision.

## The frame: two aims

The search has two aims, in the supervisor's words (22:25): "find and where possible characterize and potentially 'fill in'
holes within the envelope, and push the envelope". They are "fundamentally complementary" (22:27). Finding and characterizing
holes (their size, their persistence, which metrics bound them, whether a design can be sampled in them) and filling them in
serve the first; advancing the frontier, the level `log V` that the fit measures, serves the second. Filling in makes the
envelope's interior known: each design sampled is measured, tightens the fit and settles a candidate. Pushing the envelope
opens new interior to fill. A sampling rule serves both in turn; "trade the two" (22:15) is read as allocating effort between
complementary aims, not as a conflict.

Two words are kept apart throughout. **White space** is 0.1's word: a region of the chart no evaluated design occupies, as
the paper and the glossary have it. **Hole** is reserved for the object below, and is undefined in 0.1.

## What was found, in six lines

1. The chart is the place to ask what is near what: its distances do not depend on the units of the metrics (changing units
   moved raw-metric distances by factors 0.018 to 40 and chart distances by 2.7e-15), the frontier is flat in it, and position
   is independent of the fit (a refit moved no `Z`) (`objects-and-distances.md`).
2. On a planted table with two unsampled disks, the persistence diagram of the chart's positions shows two classes above a
   hole-free null, and the circumcentres of the triangles that kill them lie within 0.04 of the planted centres (`instance.md`).
3. Sampling at the circumcentre found a witness for the attainable disk on the first attempt and none for the other in twelve:
   the class of the first disappeared from the above-null list, the second stood unchanged. That is two of the three outcomes
   in the next section; the third needs a certificate the planted oracle does not give.
4. On the cubesat chart of record (K = 2, a random draw, 2,134 designs) no class is above a hole-free smooth null in six
   readings: position, near-frontier band, three-dimensional chart at two level weights, four-metric chart by landmarks.
   The case, drawn at random, has white space and no candidate hole at this null.
5. The reading depends on the weight of the level against the position (planted table: 2, 2, 3, 0, 0 classes above the null
   as the weight grows), and white space that opens to the outside of the sample, a bay, is not a class of the plain construction (a property of the construction; not measured here).
6. The literature read establishes stability of the diagrams and a one-way coverage criterion; it contains, in my search, no
   use of diagram classes as an objective scored beside the level when choosing the next design (`construction-and-tools.md`).

## What a hole is: a hypothesis until sampled

His direction (22:20): "its not TDA for its own sake. we don't want to mistake an absense of witnesses for a hole, we can try
to sample to find witnesses". A hole is therefore defined by a test, not by a diagram.

**Candidate hole.** For a table of designs placed in the chart, a distance on it (position, or position and weighted level), a
family of complexes (alpha, Rips, witness) and a hole-free null: a class of degree 1 or higher (a loop, a void) whose
persistence exceeds the null's longest class of that degree. Its *size* is its death scale, its *location* the circumcentre
of the simplex that kills it (in the alpha complex: the centre of the largest empty ball the class encloses), its *persistence*
the length of its interval. A degree 0 class is a *gap* between two parts of the sample, read the same way. A candidate is a
statement about the sample: it may be nothing but an absence of witnesses.

**Witness.** A measured design within a stated distance of the candidate's location, feasible and evaluated. "Measured" is the
paper's word: a point of the chart without data is a conjecture about a design, proposed by a rule and settled by building and
measuring it.

**Resolution, three outcomes** (as in the bridge, WP41):

| Outcome | What was done | What it says |
|---|---|---|
| Filled | A witness was found and measured | The candidate was white space; it is filled, the diagram loses the class, the fit gains a design |
| Stands | No witness after a stated effort (number of proposals, radius, the budget) | A hole *with that evidence*: not shown infeasible, not shown attainable |
| Infeasible | The proposals reach the region and the evaluation finds them infeasible (the case's flags: settled, power, momentum, depth of discharge), or a constraint excludes the region | A true hole of the attainable set |

The planted instance reaches the first two; for the second it cannot tell "stands" from "infeasible", because its oracle returns
nothing in both. On the case the third is observable, since a proposal that fails a feasibility flag is a measured fact.

## Hole against white space, and where they meet

White space, the envelope method's object, is what the fit and the data disagree about: the fit reaches a region (a point of
the chart with its level) where no evaluated design sits. The bridge of WP41 acts on it by proposing the pooled configurations
predicted nearest the most isolated points of the chart (the paper's propose-predict-check, Appendix D.10). A candidate hole is a
different object: a class of the sample that persists. They coincide where empty regions are enclosed by designs,
and differ elsewhere.

| Where | White space | Candidate hole |
|---|---|---|
| An empty disk enclosed by designs | An isolated point at its centre, ranked high | A loop that dies at the radius of the disk; counted, with persistence; located at the centre (planted instance) |
| An empty region open to the sample's edge (a bay) | An isolated point, ranked high | Not a class: homologically a disk (needs the fence of de Silva and Ghrist, or a band-and-boundary construction; a first question of a build) |
| The sparse tail of a random draw | Many isolated points | Short loops, below a hole-free null (the case, `instance.md`) |
| A narrow empty strip that separates two parts of the sample | Isolated points along it, each only slightly isolated | A degree 0 class whose persistence is the gap's width |
| How many, and when to stop | A ranking; no count and no stopping rule | A count of classes above a threshold; the total persistence falls as candidates are settled (0.741 to 0.379 on the planted table) |
| Dependence on the fit | The level of the point depends on it | A position-only class does not depend on it (a refit moved no `Z`) |

So the diagram adds three things to the ranking of isolated points: enclosure, a measure that has a size and a count, and a
natural definition of "settled". It loses the bays. Where both see the same region the sampling rule is the same.

## Strategic sampling, with the two aims kept apart

**The two measurable objectives.** Advancing the frontier: the level the fit already measures, `log V` of a proposal, and how far
beyond the surface the fit has now it lies (the novelty of the paper). Filling in: the persistence measure of the table's
candidate holes. A measure that is plain: `M(T) = sum over candidate classes above the null of their persistence` (the
`total persistence` row of `instance.md`); `M` is zero when nothing is a candidate. Its count and its largest class are the
other two numbers a reader would want.

**Scoring a proposed sample.** For a proposal at chart position `x`: the filling score is the predicted drop `M(T) - M(T plus x)`,
computed by adding the point and recomputing the diagram (one alpha complex of the table; seconds at 2,000 designs). After the
design is measured, the same quantity with the measured point is the realised score, and the check is the difference, as in
propose-predict-check. The level score is the predicted `log V` beyond the surface and, after measuring, the measured `log V`.
On the planted table the one witness took `M` from 0.741 to 0.379, with a measured level 0.19 above the predicted one.

**Where the score sits in the loop of Section 7.** The inner loop identifies (fits the terms, computes the chart and the
diagram), the middle loop proposes (the ascent proposals of the paper for pushing; the circumcentres of the candidates'
killing simplices, realised as configurations through the regressor and the pool, for filling in), the outer loop evaluates,
appends, refits and recomputes. A rule is a way of dividing a round's budget between the two kinds of proposal: a fixed split,
alternation, or taking each proposal's two scores and keeping the non-dominated ones. Each is a rule to be built and measured,
and none is claimed here.

**How a rule makes holes emerge.** Sampling that follows ascent from near-frontier designs puts its designs along the paths
and leaves the regions between them; the unvisited regions that become enclosed are the candidates. This is a mechanism
proposed by the supervisor ("these will emerge naturally when we start sampling strategically") and is plausible; it was not
run here, and the case's random draw shows none.

**What a definition of hole must satisfy to survive refits.**

1. *Defined on the chart, in stated units.* The distance is the chart's, with the level weight stated; the units of the metrics
   do not enter (shown).
2. *Position-only candidates do not move with the fit*: `Z` is fit-independent (shown: zero change in a refit).
3. *Candidates with the level move by a bounded amount.* A refit that moves each design's chart point by at most `e` moves the
   Rips diagrams by at most `2e` in the bottleneck distance, so a class of persistence above `4e` is matched to a class in the
   refit; the instance checks the bound once (0.040 against 0.133), and `e = 0.066` on the case makes the guard 0.27, large
   against the null, which is the reason for the position-only form as the default.
4. *The threshold is a function of the table.* The null is recomputed for the table and the distance; it is stated with its
   bandwidth (the case's reading held at three bandwidths).
5. *The boundary is stated.* What a candidate is allowed to touch (the edge of the sample, the frontier, the infeasible
   region) is part of the definition, since a loop needs designs on every side.
6. *The test is part of it.* A candidate has a location, a stated distance for a witness and a stated effort, and a resolution of one
   of three kinds; a hole is a candidate that remains after the test.

## Plain options for the first package of the later release

Each is a package of the release after 0.1; none is placed before his word. In no order.

- **A. The definition as code on planted tables.** A module that takes a table and a chart, builds the complex, applies a null
  and returns candidates with location, size, persistence and score; tests on planted tables whose holes are known (the
  instance, generalised). Settles: that the definition can be stated in the package's own terms and tested. Does not touch the
  case or any sampling.
- **B. The emergence study on the case.** Run the bridge's loop (WP41) for rounds on the cubesat, with the diagram computed each
  round, and look for holes to emerge; settle any candidate with the case's simulation oracle (`cubesat_oracle.py`).
  Settles: whether strategic sampling makes the candidates the supervisor expects. Needs A, or the instance's script, as its
  instrument.
- **C. The boundary question as research.** Settle what a hole is where the sample has an edge and a frontier: relative
  persistent homology with a fence on the near-frontier band, the infeasible region as part of the boundary, bays. Settles:
  the object on non-convex supports. A research package with a readout, no code.
- **D. A controlled comparison with a space-filling rule.** On planted tables and the case, compare designs-per-candidate-settled
  of the topological rule with a largest-empty-ball (minimax) rule and with the isolation ranking the bridge uses. Settles:
  whether the topology earns its place against what is simpler (Johnson, Moore and Ylvisaker for the baseline).

A dependency choice sits across all four and is also his: the alpha complex (GUDHI, with a GPL v3 dependency for the Euclidean
versions) or the Rips complex (ripser, MIT) with scipy's Delaunay triangulation for the locations (`construction-and-tools.md`).

## The boundary

**Is the direction fruitful enough to name in the abstract?** Yes as a direction, not as a result. For: the object is well
posed (a definition with a test and three outcomes), the chart gives it units-free distances and a fit-independent position,
the planted instance locates and settles a known hole at the cost of one recomputed diagram, stability is a published bound that
the case's refit respects, and the coverage work states the same asymmetry the supervisor drew (a certificate of no hole is
possible; a class that persists is a hypothesis). Against: the case of record shows no candidate, the emergence mechanism is
not demonstrated, a bay is invisible to the plain construction, the reading depends on the level weight, the nearest search
did not find the sampling-rule combination in the literature (which says the search did not, not that nobody has), and the
first package would be a build. Naming it plants a flag the paper does not have to defend; the decision is his.

**The abstract's closing sentence as a list of three** (his 23:15 and 23:20; the abstract is untouched). The sentence now:
"Future work has two key thrusts: (1) searching the design space by sampling white space and pushing the frontier, and (2)
formal verification and performance by moving beyond Python into Rust and using theorem provers." (35 words; the abstract
is 497 words by the test's count, whose bound is 525.)

- Draft A (44 words; the abstract 506): "Future work has three key thrusts: (1) searching the design space by sampling white
  space and pushing the frontier, (2) identifying and filling holes by topological data analysis, and (3) formal verification
  and performance by moving beyond Python into Rust and using theorem provers."
- Draft B (53 words; the abstract 515), with the object glossed in place: "Future work has three key thrusts: (1) searching
  the design space by sampling white space and pushing the frontier, (2) finding holes, regions the sample encloses and no
  design occupies, and filling them by topological data analysis, and (3) formal verification and performance by moving
  beyond Python into Rust and using theorem provers."

Only the structure he gave changed: three items, the topological item second, the formal methods and performance clause
third and kept as it was; the second item is in his terms ("hole identification and filling by topological data analysis"). I
corrected nothing else. His own words in item three read "formal methods"; the sentence has "formal verification" now, the
abstract's, and he may prefer his.

**What 0.1 may say now.** At most one sentence of future work, for his acceptance. Draft: "Beyond white space, persistent
homology on the chart's distances would name candidate holes, regions the sample encloses and no design occupies, each a
hypothesis to be settled by sampling a design there." (And, if the abstract takes the list above, the section on future work
can use this sentence as the one place that explains item 2.) The existing "Beyond a log-convex surface, the detection of dents
and holes" in the paper's future-work section uses the reserved word for a different object (dents of a non-log-convex
surface); the sentence above would sit beside it and the two would need to be told apart.

**What 0.1 may not say.** That holes exist in the case; that a persistent class is a region with no attainable design; that
strategic sampling makes holes emerge (not run); that the topological measure beats a space-filling or isolation rule (not
compared); that the method is new in the literature (not established); any result of this spike as a result of the paper.
The word hole as a defined term, anywhere in 0.1. Vocabulary
that already uses it and needs his attention before 0.1 (not edited by this unit): the glossary's `white space` entry (short
and formal text use "hole"), `docs/theory.md` ("Holes in the Z plane are candidates for white space"), and the paper's
Section 7 and Discussion ("nearest a hole of the four-metric chart", "the 300 most isolated holes", "A hole in the chart is an
opportunity", cells of `paper/paper.ipynb`).

**What the next release builds.** A hole module in the package, in stages: (1) the definition as code on planted tables, with the
distances of `objects-and-distances.md`, a null, candidates with location, size, persistence and a filling score, and the
resolution record (option A); (2) the emergence study on the cubesat with the case's oracle as the settling step (option B);
(3) the boundary question and the comparison with a space-filling rule, which decide whether the object earns a place in the
loop (options C and D). The first package to name is his to pick from the four above; whichever it is, the instrument is the
instance script of this spike, which reruns byte for byte and is the test the build starts from.
