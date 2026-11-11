# tab-families

## Q5 (a) What the table shows (written before the caption)

A comparison grid with eleven rows, each a family of existing methods with its citations (Pareto/multiobjective optimization, DEA, production and distance functions, frontier estimation, PCA, compositional PCA, geometric programming and max-affine fitting, kernel and hyperbolic PCA, MDAO, tradespace exploration, decision analysis, MBSE). For each family there are three short notes: what the family produces, what "this method" shares with it, and how "this method" differs. Taken together the rows say that the method in the paper borrows a piece from many neighbours: a one-sided envelope of data, a weighted geometric mean with simplex weights, a posynomial model class, a coordinate system, and a table of evaluated designs. It differs from each neighbour in a stated way: the criterion is a one-sided soft maximum, not variance; the weights are fitted from the data's edge, not elicited; and it fits an envelope rather than returning a set of designs or solving a coupled system. Some cells are terse and some are not parallel in form (for example "global exponents per term, not per-unit weights; a band, not extreme units"). I cannot tell from the rows alone what "this method" is called or what it does overall.

## Q5 (b) Does the table show what the caption says?

Mostly yes. The caption promises, per family, what it produces, what it shares, how this work differs, and the sources; the four columns do that (sources sit in the first column with the family name). It does not show: which of the shared or differing items matter most; any ordering of the families (by closeness, though the caption says "closest"); how a reader would check any cell (no pointer from a cell to a section, theorem or appendix entry, although the Section 2 intro says the table says "where to read it"); or what "this work" is, since the table never names it. Cells are uneven: some "Shares" or "Differs" cells are fragments ("Attributes in place of inputs", "global exponents per term, not per-unit weights; a band, not extreme units") that a reader at my level cannot unpack without the prose. Some "Produces" cells are really descriptions of a field ("Decision analysis with a normative versus descriptive distinction"), and one "Shares" entry ("The weights are trade-off rates") is a claim of the paper's own method, not something shared.

## Q5 (c) The sentence test

Sentence: "The method borrows its pieces (a one-sided envelope, a geometric mean with simplex weights, the posynomial model class, a chart, a table of evaluated designs) from neighbouring families, and differs from each in using a fitted one-sided soft maximum whose exponents are read as trade-offs, not a nondominated set, per-unit weights, variance, or an elicited ranking."

The table conveys more than that sentence in one way: it names the particular families and their sources in a scannable grid, and states a family-by-family difference. It conveys less in another way: it does not say what the method is, so the "Differs" column is only intelligible after the story and the prose below.

## Q1. What does this table convey?

For eleven neighbouring families of methods it states, in a line each, what the family produces, what this work has in common with it and how it differs, with the citations.

## Q2. Which sentence of the story does it serve?

None of the seven numbered main results. The nearest abstract sentences are "Like PCA, our method is unsupervised feature engineering; the two answer different questions and compose" and "not the Pareto boundary" (the abstract's "models the data underlying the table, not the Pareto boundary"); the Section 2 opening "We claim no priority" serves the story only in a general way. For item 3 (a maximizer of V is Pareto-efficient) the Pareto row repeats the sentence in compressed form. Otherwise, none.

## Q3. Verdict

repeats. The Pareto, DEA, PCA, production, frontier, geometric programming, kernel PCA, tradespace and the compositional rows are each said again, in fuller and clearer sentences, in the prose directly under the table ("Pareto methods", "Data envelopment analysis", "Lineage"), and the Section 2 introduction already points to Appendix G for the full register. What the table alone adds is the four-way layout and the rows for MDAO, decision analysis and MBSE, which have no paragraph below; but Section 1 already places the method against MDAO, decision analysis and MBSE, and no sentence of the story needs the row. A reader can follow the paper without it.

## Q4. Which unit already carries it

sect-prior-art (the prose of Section 2 under the table), and for the full register appendix-g (Appendix G, Register of prior art). For the Pareto row, also sect-problem (Section 1's contribution paragraph and the Theorem 9 statement in main result 3).

## Q9. Anything read twice and not placed

- "global exponents per term, not per-unit weights; a band, not extreme units" (DEA row, Differs): I can place the first half after the prose, not before it; "a band" is not defined at that point.
- "A smooth soft maximum over a simplex-constrained geometric mean" (frontier row, Differs): the words are all defined later; unreadable at the point of the table.
- "the feature-engineering kin of the kernel direction" (kernel PCA row, Shares): "the kernel direction" points to Section 10, which I have not read.
- "The weights are trade-off rates" (decision analysis row, Shares): unclear whose weights and in what sense they are shared with that family.
- "Attributes in place of inputs" (production row, Differs): too terse to say what the difference is.
- The Production row's "Produces" cell ("The Cobb-Douglas production form, and the Shephard distance function") reads as the thing the family is, not what it produces.
