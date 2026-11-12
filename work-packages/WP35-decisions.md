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
