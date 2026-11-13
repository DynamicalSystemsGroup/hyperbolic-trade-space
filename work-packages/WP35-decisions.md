# WP35 decisions: the word "hyperbolic", the HoroPCA comparison, and Table 1's "differs" column

Supervisor: Michael Zargham (`mzargham`). Decisions and acceptances are verbal and quoted verbatim here. The
package runs through the standard channels (a scope by the PM, the assistant's approval, units in their own
worktrees, a review that runs the thing); the supervisor asked for exactly that.

## The supervisor's feedback (2026-11-12, afternoon, verbatim)

> there are several places where we compare to hyperbolicPCA and i think we could do a better job differentiating
> ourselves. to my knowledge that work is PCA with a specific kernel. we are not actually doing PCA at all, we're
> just borrowing some of its intuition, and looking at it as an example of how how scikit learn handles
> unsupervised learning in general. it seems like we should address this directly and concisely in the paper in
> the related work section, and in the associated appendix. the other reference that say its different can remain
> brief and point to the paper

> also since we're talking about wording, its worth noting that "hyperbolic" in our paper seems to reliably refer
> to negative curvature geometry, it may be helpful to clarify, potentially in the glossary and limit the number of
> times and places we need to caveat about it
> the table of comparisons to prior art as a row about how our method differs from the method the row references.
> its not always clear whether the difference described is about our method or the method we're distinguishing it
> form
> don't disrupt work by jumping in and editing, this is feedback to you that should be processed through the
> standard work channels

## The assistant's reading (2026-11-12)

What the records say now. The body uses "hyperbolic" in the title and twice in Section 2 (`sec-prior-art-3`): once
against the Färe, Grosskopf and Lovell hyperbolic graph measure, once as '"hyperbolic" here is unrelated to
hyperbolic PCA [@chami2021horopca]'. Table 1's row "Kernel and hyperbolic PCA" (from `paper/prior_art.yaml`,
`kernel-hyperbolic-pca`) has a "differs" cell that states what our term means ('"Hyperbolic" here means the level
surfaces of V in metric space'), not how this work differs from that family: the ambiguity the supervisor names.
Appendix G prints the full sentences; the reading pass (row 44) records HoroPCA from its abstract. The docs carry
two further one-line caveats (`docs/user-guide/limitations.md`, `docs/further-reading.md`). `glossary.yaml` has no
entry for "hyperbolic".

What HoroPCA is, from the verified abstract on record (`docs/references.bib`, `chami2021horopca`): the components of
PCA (subspace parameterization, projection, variance objective) carried into hyperbolic space, with horospherical
projections. That is a generalization of PCA to a negative-curvature geometry, not PCA with a kernel; kernel PCA
(Schölkopf, Smola and Müller 1998) is the other member of the same table row. The paper's sentence should say the
precise thing. The spike confirms this against the source before the build.

Path (the six stages, scaled to the size): a research spike (every occurrence of "hyperbolic" and its caveats
across paper, docs, glossary and register; Table 1 row by row, which "differs" cells read as this work's and which
as the family's; HoroPCA from the source), a readout with options to the assistant; the decision; the build; QC;
integrate (glossary, Appendix A, register rows, docs pointers, ledger); the review that reads the rendered pages.

Defaults the assistant brings to the scope: one glossary entry says what "hyperbolic" means in the name and what
it is not, and Appendix A carries it; Section 2 holds the one direct, concise differentiation from HoroPCA (what
that work is, what this work does instead, what it borrows from PCA and from scikit-learn's unsupervised
estimators, and that the two chain in D.16); Appendix G holds the full version; every other mention becomes a
pointer or goes; Table 1's "differs" column is rewritten so every row's sentence has this work as its subject, and
a test keeps it so.

## The supervisor, later the same afternoon (verbatim)

> sounds like HoroPCA is the closest existing analog to our work and we need to acknowledge it more clearly and
> better distinguish from it. that may require a spike, and involve writing and testing code to make sure we're not
> just saying what we want to be true

## The assistant's reading

WP35 is a bigger candidate edit and runs the full lifecycle. Stage 1 becomes a code spike: HoroPCA's reference
implementation (the authors' repository, pinned by commit, in the spike's own environment, never a dependency of
the package) is run on the paper's own tables, the planted tables of `make_frontier_data` and the cubesat
log-metrics of record, after whatever embedding HoroPCA needs; the spike reports what it recovers against the
planted exponents and the fitted terms, whether a hyperbolic embedding of log-metrics is a natural input at all,
and what the two methods share in the scikit-learn sense (an unsupervised fit and transform that gives the data a
coordinate system). The spike's code carries tests, lives under `docs/superpowers/notes/spike-horopca/` (ruff
excludes the spike folders), and its readout states what HoroPCA does well that this work does not, as plainly as
the converse. The paper's acknowledgement and distinction are written from the readout, not before it.

**The spike's code, a boundary (the assistant, same afternoon).** Fetching and running the authors' HoroPCA
implementation from their repository was refused by the session's permission classifier (external code). The spike
therefore implements the method's core from the published description (the hyperboloid or Poincaré model, the
horospherical projection, the variance objective), with tests against the paper's stated properties on synthetic
hyperbolic data, and states the limits of a re-implementation in its readout. If the supervisor prefers the
authors' code for fidelity, he can install it into the spike's environment himself or grant the fetch; the spike
then swaps it in and re-runs. Recorded for his decision.

## The supervisor, on the spike's code (verbatim)

> you don't necessarily need to reimplement it, you need to import it and run it, i want to understand how it
> differs in behavior and usefulness, not necessarily how its constructed. that said looking through its code to
> see how its solvers work is merited

**The assistant's reading.** The spike imports and runs the authors' HoroPCA (the HazyResearch repository of the ICML
2021 paper, pinned by commit, installed in the spike's own environment only, licence noted), on the paper's own
tables after the embedding the method needs, beside ordinary PCA, and reports behaviour and usefulness: what each
recovers, whether any of it names which metrics trade or at what rate, what each is good for. The spike also reads
HoroPCA's solver code (how the horospherical projections and the variance objective are optimized) and says in a
paragraph how its solvers compare with this work's convex programs. No re-implementation. The supervisor's words
are the authorization for the fetch; nothing from the repository enters the package or its dependencies.

## Stage 2: the assistant's decisions on the spike readout (2026-11-12, 17:30; readout at ace2840)

The spike ran the authors' HoroPCA (pinned commit, spike environment only) beside PCA on the planted tables and the
cubesat tables after embedding the log-metrics in the ball, read its solvers, and found: where a planted term is
also the direction of largest spread both PCA and HoroPCA recover it, elsewhere neither does; on the cubesat tables
neither captures more than 0.06 of our K = 1 exponent; neither names which metrics trade or at what rate; the
tables are not tree-like, so nothing in the data asks for a hyperbolic embedding; HoroPCA maximizes a nonconvex
variance over frames by gradient ascent with restarts and no certificate, where this work solves convex programs
on a simplex with one; the two share the unsupervised setting and the estimator interface, and chain through PCA;
"PCA with a specific kernel" does not describe HoroPCA on the evidence (no kernel, no Gram matrix; the paper's
baseline, tangent PCA, is PCA after a fixed feature map).

Decisions, each the supervisor may revert.

- **Q1 (a).** Section 2 holds one concise paragraph: what HoroPCA generalizes, what this work borrows (the
  unsupervised setting, the estimator interface, PCA as a downstream step), and that runs on the paper's own tables
  recovered the exponents only where the generator made them the direction of largest spread. Appendix G carries
  the full version with the spike's results table and says plainly that the embedding was ours and not natural for
  the data. The spike's code and results stay under `docs/superpowers/notes/spike-horopca/` and are cited as the
  record. (The supervisor asked for code-backed differentiation; the numbers earn their place in the appendix.)
- **Q2 (a).** Table 1's row splits into kernel PCA and HoroPCA, each `differs` cell with this work as its subject.
  Beyond that row, every `differs` cell in Table 1 and Appendix G is rewritten to the one convention, a sentence
  whose subject is this work ("This work ..."), the rows "by elision" given their subject and the "mixed" rows
  split into what the family does (in `does`) and what this work does (in `differs`); a test pins the convention.
- **Q3 (a).** One glossary entry for "hyperbolic" (the level curves of V, products of powers of metrics, the
  rectangular hyperbola in two; not negative-curvature geometry; not the Färe, Grosskopf and Lovell graph measure);
  Appendix A prints it; the Definitions sentence that already says it stays as the body's one place; Section 2's
  two caveats and the docs' second definition become pointers or go; the DEA paragraph keeps at most a half-clause
  pointing at the glossary. No title change.
- **Q4 (a), qualified.** HoroPCA is named the closest existing analog in setting (unsupervised, a table in,
  coordinates out), and the same sentence says it is the farthest in what is estimated (a variance over frames
  against a one-sided edge). The paragraph does not call this work a PCA of any kind.
- **Reach.** The paper and Appendix G, `prior_art.yaml`, the glossary and Appendix A, the two docs lines, the claims
  rows and the ledger; the register test and the site tests; the paper notebook through the single-writer queue
  behind WP33's paper unit. No model, data or number of record moves.

## Approval of the scope (2026-11-12, 18:50; the assistant, under the supervisor's mandate; scope at 1d27f8c)

**Assistant, verbatim:** "WP35-scope-of-work.md at 1d27f8c is approved as written: goals G1 to G5, the non-goals, the
sequencing behind WP33's paper unit, the agent models and the defaults as one item. The build starts now."

## The supervisor, on the HoroPCA comparison (2026-11-13, verbatim)

> i think the horoPCA comparison analysis needs its own appendix, and i need it broken down a bit cleaner. we need
> an explicit (and falsifiable) hypothesis about how our method differs from theres. then a computational
> experiment that can assess (validate or invalidat) that hypothesis, then results, then interpretation. this
> section should probably also include some explanation of how the underlying formalism and solvers differ but the
> critical result is to demonstrate that the methods are doing different things, that renders them complementary
> rather than competitive.

**The assistant's reading.** WP35's scope is amended: the comparison leaves Appendix G's passage and becomes its own
appendix (the next letter, H), in the order he names: a hypothesis stated so that an experiment can refute it; the
computational experiment designed to test it; the results; the interpretation; and a part on how the formalism
and the solvers differ (a one-sided edge on a simplex by convex programs with a certificate, against a variance
over frames in negative curvature by gradient ascent with restarts). The critical result the appendix must carry
is that the two methods estimate different things, which makes them complementary (the paper already chains PCA
on the chart in D.16), not competitors. Appendix G keeps the register row and a pointer; Section 2's paragraph
points at H. The spike's runs are the first evidence; the hypothesis and the experiment are designed before the
appendix is written, as the lifecycle asks: a hypothesis of the form "each method recovers a planted exponent
vector only under its own condition, this work whenever the planted edge is present, HoroPCA and PCA only when
that vector is also the direction of largest spread", tested on tables built so that the edge and the spread are
decoupled by design (the generator's depth distribution controls this), beside the tables already run; the
experiment is specified with its measure (the cosine between the recovered direction and the planted vector, and
the share of the planted vector recovered) and its refutation condition before it runs. Stage 1b of the spike
does this; the assistant decides on its readout; the build, QC, integration and the P9/P10-balanced review follow
through the paper notebook's single-writer queue. The scope's non-goal "no new section, figure or page" is lifted
for this appendix by the supervisor's word.

## Stage 2 for the appendix: the 1b readout accepted and the content decided (2026-11-13, 09:20; the assistant, under the supervisor's amendment of 13165e8)

The stage-1b readout (`WP35-rounds/spike-h/readout.md`, ef4d118) is accepted as the record: the hypothesis and its
refutation conditions were committed before the run (830cf54), every part survived under the pre-registered rule, and
the assistant reproduced the record on this Mac (the 70 tables regenerated from their seeds in 3 s, this work's refit
with them; `results.json` and `summary.txt` regenerated identical from the committed HoroPCA record; five cells
recomputed by hand: arms A and B 6/6 at cosine 1.000, arm C 0/6 at median cosines 0.318 and 0.577).

**Assistant, verbatim, in the readout's numbering:** "Question 1: (a). Appendix H carries the hypothesis with its
refutation conditions, the design in a paragraph, one results table built from 3a to 3c with the verdict column, the
interpretation and the formalism-and-solvers comparison; arm D, the cubesat rows and the loadings stay in the notes and
the readouts, linked. Question 2: (b), not run; the embedding is stated as ours in the reading limits. Question 3: (a),
the chain in words with the pointer to D.16. Question 4: (a), the smallest-variance component reported as the part not
in the hypothesis, in two sentences. Question 5: (a), 0.9 with the chance rates beside it. The appendix is
complementary in register, as the supervisor ruled: what each method estimates, shown by a table in which the two part;
no sentence says HoroPCA is worse at what it was built for. The scope amendment names Appendix H, its word budget in
the length ledger, the results table generated from `results.json` by a paper script, the claims-register rows and
the reading-pass row for HoroPCA, and the removal of the earlier Appendix G passage that this replaces, with what it
no longer did."

## Approval of amendment 1, Appendix H (2026-11-13, 10:30; the assistant, under the supervisor's amendment; scope at dae99a6)

**Assistant, verbatim:** "WP35-amendment-1-scope.md at dae99a6 is approved as written, with one default pinned: the
Appendix H ceiling is 900 words by the visible-prose rule, fixed now rather than at the build, and it is not raised
without a new ledger row and my word; the Appendix G cut is measured as the scope says. The sequencing stands: the
generator, tests, ledger, register, reading-pass and prior-art rows may be prepared in a parallel worktree; the
notebook edits and the re-execution queue after the WP36 integration unit. Open decisions: none; the five content
calls remain the supervisor's to revert."

## A reviewer's judgment of the stage-1b design, relayed by the supervisor (2026-11-13, 19:20)

The supervisor's question to the reviewer: "did you find the experimental design to distinguish our method from
horoPCA acceptable". The reviewer's answer, verbatim as relayed (the reviewer read the design, scripts and recorded
results at dc80457 and did not rerun the HoroPCA experiment):

> Yes—for distinguishing what the methods estimate, I find the design acceptable and quite persuasive. I would accept
> it as a bounded synthetic experiment supporting the paper's positioning, rather than a general performance
> benchmark. My earlier summary did not explain that judgment adequately.
> The strongest design choice is varying spread while holding the planted boundary fixed. That directly tests the
> proposed distinction instead of merely showing that the methods return different vectors.
> Three additional controls make it convincing:
> * Removing the planted boundary: the Gaussian-cloud arm shows PCA recovering the dominant spread direction while HTS
>   does not recover that designated vector. HTS is not simply winning every constructed task.
> * Breaking the package generator's accidental alignment: moving the planted normal away from the all-ones depth
>   direction interrogates why the earlier methods appeared to agree.
> * Reporting stronger alternatives and inconvenient results: the last principal component sometimes recovers the
>   boundary normal; two-component spans sometimes contain it; HoroPCA's larger-radius runs show restart sensitivity.
>   Those results remain visible.
> Using the authors' HoroPCA implementation, selecting restarts by its own loss, recording all restarts, and committing
> refutation rules before the experiment are also sound choices. The prior exploratory spike informed the design, so I
> would describe this as a prospectively specified follow-up experiment, without implying it arose without prior
> exploration.
> My acceptance has three boundaries:
> 1. The embedding is part of the treatment. HoroPCA receives your chosen embedding of log-metrics into hyperbolic
>    space. The experiment distinguishes the implemented pipelines under those embeddings; it cannot establish that
>    HoroPCA could never recover boundary information.
> 2. The tables deliberately favor clean identification. Noise-free data, 30% of rows on the boundary, four dimensions,
>    and a fixed HTS temperature make this a mechanism demonstration. That is appropriate here; robustness under
>    realistic sampling remains separate.
> 3. Six tables per cell establish separation here, not reliable population recovery rates. The large observed
>    differences are informative, but "6/6" should stay a count rather than become a broad reliability claim.
> I would also soften two phrases in the readout: "the two-component plane is not a rescue" and "the analyst cannot
> pick [the last component] without knowing w." An analyst might select components using other domain information.
> The defensible point is that variance ranking alone does not identify which component represents the relevant
> boundary.
> The conclusion I would endorse is:
> In these controlled constructions, HTS tracks the planted upper boundary while leading PCA and HoroPCA directions
> track variation in the sampled designs. Their agreement therefore depends on the relationship between boundary
> orientation and sample spread; the methods answer different questions.
> That is a useful result for 0.1. I would not require another experimental arm before including it. This judgment
> comes from reviewing the design, scripts, and recorded results—not independently rerunning the HoroPCA experiment.

**Applied as (the assistant):** Appendix H carries the reviewer's framing and boundaries. The design is described
as a prospectively specified follow-up to the exploratory spike, a bounded synthetic experiment supporting the
positioning and not a benchmark. The reading limits state the three boundaries in that order: the embedding is part
of the treatment and the experiment distinguishes the implemented pipelines under it; the tables favour clean
identification, so this is a mechanism demonstration and robustness under realistic sampling is separate; six
tables per cell establish separation, not population recovery rates, and every "6/6" stays a count. The two
phrases are softened to the defensible point: variance ranking alone does not identify which component represents
the boundary (an analyst with other domain information might choose otherwise). The interpretation's lead is the
endorsed conclusion, in the paper's vocabulary: in these controlled constructions this work tracks the planted
upper boundary while the leading directions of PCA and HoroPCA track the variation in the sampled designs, so their
agreement depends on how the boundary's orientation relates to the sample's spread, and the methods answer different
questions. No further arm. The readout at ef4d118 stays as the record and gains a short section quoting the two
softened phrases and their replacement, pointing here. The claims-register rows for the counts say "count" where
they say "rate".
