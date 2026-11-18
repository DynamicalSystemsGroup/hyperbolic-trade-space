# WP11 — Decision records (readability and correctness loops)

Records typed by the driver. This package is defined and approved by the driver under the
supervisor's mandate (`release-candidate.md`); the calls below are the driver's, for his review at
the PR. The supervisor's words on the grid and the personas ("Use these six") are in
`WP10-decisions.md`, "The reader grid".

## The driver's calls

- **2026-11-09. Scope defined and approved** (`WP11-scope-of-work.md`). Basis: the grid and protocol
  note; the first cold reads (`WP10-cold-reads.md`), which showed that fresh readers given only a
  slice produce specific, checkable findings, and that one reader per cell is enough to start if
  replication is read across cells. Added to the note's protocol: the answer key is kept out of the
  repository while the loops run and its hash is committed first; six core cells are held out by a
  seeded draw; at most four rounds before reporting non-convergence.
- **2026-11-09. The answer key is fixed; its hash and the held-out draw, committed before any persona
  read.** Answer key version 1, written by the driver from the recorded story, the outline, the
  register and the accepted results, and kept outside the repository: sha256
  `4fdbaefd37ab13e8e490380c40685b2b8c26088cd1f69299773db823a51b90bf`. If the supervisor's pending
  choice on the two step-read times changes a fact in it, a new version is made before the next
  round and its hash recorded here beside this one. Held-out cells, one core cell per persona, by
  Python's `random.Random(20261109).choice` over each persona's core depths in the grid's order:
  P1 at L-A, P2 at L-A, P3 at L-D, P4 at L-C, P5 at L-D, P6 at L-B.
- **Correction.** The grid has 24 core cells and 6 edge cells; the note, the scope and the driver's
  report to the supervisor said 23. Round 1 therefore reads 18 core cells and three edge cells.

## Answer key, version 2 (2026-11-09, 17:50)

- The triager (the driver) updated the key for the supervisor's decisions of the day (elasticity for
  exchange rate; the fit stated without membership; depth A is the title and abstract since the
  three-pane figure left the paper's body; posynomial as the model class; the data as what is
  modelled; the two named uses). Held outside the repository as before. SHA-256 of version 2:
  `e72f3eeac76089d8657add60ac1b7553ac8fcfd022cc6cb0b69fb050931ad638`. Round 1 begins with the L-A and L-B cells of all six personas on the staged paper at
  20fa550, the stable part of the paper while the narration and figure passes run.


- **2026-11-10, 16:00. The answer key, version 3**, fixed by the driver before the held-out reads of round 2 and
  kept out of the repository: the word is monomial term, never facet (W7 reads "exponents or terms"); the case has
  eight traded metrics on the model of record with the settling time by event detection and launch cost as the
  measure of effectiveness on mass; the finding reads "one term blends the subsystems' trade-offs into a single
  tension; three terms separate the contending sets"; the propose-predict-check numbers and the proposals'
  depth-of-discharge failure; the four requirements read after the fit, cutting designs and not trades; the
  baseline failing the pointing-error requirement; the case called exploratory with the author's thresholds. SHA-256
  of the file: `2c1f9672ebd634429b820e4940edd39632c9d29963e4190c955567b2bcc993da`. Version 2's lines marked "key stale" by round 2's triager are read against version 3.

**Answer key version 4 (2026-11-10, 17:05).** Version 3 with one word: S7's "exchange rates" is now "elasticities",
the word the key's own header fixed at version 2. Nothing else changed. SHA-256 of the file held outside the
repository: `aee912f94a17834bc3a99cee591660c9c491d7bf5ee83b3d5a482e314c9f2a0c`. The round-2 "key stale" lines resolve as: S4 (terms, the cell an analysis reading) and S6 (eight
metrics; 659 of 706 nondominated on eight; a 5-lemma) were already version 3's text, so the readers' statements are
"stated"; S7's line is version 4's; the nine figures stay uncounted.

**Answer key, version 5 (fixed 2026-11-12 05:00, the assistant).** Version 4 updated for the model revision (thirteen
traded metrics, the fleet size, 3,000 designs per regime, the cost coverage and the two budgets), the case read at
K = 2 by the package's own checks, the term order, the six requirements read after the fit, the data of record
(the container's `@12` entries) and the noise corollary; wrong beliefs W9 to W12 added. Kept outside the repository
and never shown to a reader, triager or author; sha256 `a041bc84c27f144a8ea7339ec59059f20e37a816d0f5d64bf4cb4e784ccc5bc4`. The final reader round reads against it.

## The final reader round: the assistant's settings (2026-11-14, 01:25; plan and briefs in the scratchpad, written without the key; dev at 6891eae)

Against answer key version 5 (sha256 a041bc84…, held by the assistant). The PM's plan asked five questions with plain
options; the assistant's settings, verbatim:

**Assistant, verbatim:** "1 (c): depths A and B as captured files and images, C and D as the live pages, and a
root-page arrival at depth A for P1 and P8, so the root page's new order is read cold. 2 (b): two readers per core
cell on two models and two brief wordings, 56 reads in eight waves; this is the release's evidence and the grid note's
protocol asks for two. 3 (a): no edge cells; a fifth batch only if the triage shows a persona weak across depths.
4 (a): the mathematics pair as built, the lemma scripts withheld, since the contract's depth D has no repository.
5 (b): the six held-out cells are read in a batch after the other twenty-two are triaged and any change has landed,
so they stay unseen by the revision loop. The triage is the assistant's, against the key, one form per report; every
report is committed verbatim before any triage; the stopping rule stands as the plan states it."

## The abstract pass (2026-11-14, from 11:35): the supervisor's draft and his rulings, verbatim

The supervisor posted a freehand draft of the abstract and asked for a review; the assistant's review is in the chat
record and its substance in `WP11-final/triage/` (the abstract's cells). The draft and the rulings are recorded here;
the abstract stays the supervisor's hand and lands by his word.

**Supervisor, verbatim (11:50):** "let's talk through it. obviously i was freehanding so i expected it to be imperfect.
that said we have a clear sense of what i am hoping to achieve, and some places we need to align the facts. mostly i
want to align my claims in the abstract to the facts. though i want to entertain the possibility that in some cases we
can achieve support for what i'd like to claim. we also have language questions. i have used "objective" because we've
described a multi-objective optimization problem. i think we may need both "metric" and "objective" and we may need to
distinguish them in use between the objectives of the optimization and metrics we have in our model. i think in our
case we have metrics which do not end up being objectives."

**Supervisor, verbatim (11:58), on the vocabulary:** "on the metrics vs objectives thing. there is no way around having
multiple definitions for the concepts of loss, metric, attribute, objective. there is inherent conflict in the terms
use across decision analysis, optimization, and machine learning. we need to make some minor corrections but i link we
probably need to deal with this at the glossary level then hold ourselves to our glossary definitions. of the possible
configurations of the terms i am most interested in the top level descriptions being intuitive. caveats or detailed
clarifications are okay in deeply detailed content but not in intuitive descriptive sections"

**Applied as:** a glossary unit (folded into the tension package, `WP42`): entries for objective (a metric a
decision-maker wants more of), constraint, trade-off, tension, loss or the solver's objective (his call pending), MoE
and MoP; each entry says which register uses it; the checker's stems extended; the intuitive surfaces carry the plain
words and the caveats live in the entries and the detailed sections.

**Supervisor, verbatim (12:00), on tension:** "i think tension should be partial derivative computed between 2 metrics
measured (potentially measured at a point on our surface since i think its going to be peice-wise)"

**Supervisor, verbatim (12:08):** "tension should be in metrics so its well behaved mathematically but it should be
possible to compute back to the attribute and design space given the various methods we're supporting, and we should
provide guidance on how to do this in our documentation. / since its defined in metrics, the partials will be negative
valued for trade-offs but not everwhere negative valued because not every metrics trades-off with every metric. we're
already sort of seeing this in our heatmaps. i think we're talking about something pretty close to one cell in a
heatmap."

**Supervisor, verbatim (12:40), on where the matrix is evaluated:** "these are two different things. one is from the fit
and one is from the sampled data."

**Applied as:** tension between metrics i and j on term k at a point of the surface, in the conditioned metrics, is
the partial derivative of m_j along the surface as m_i moves, minus (w_ki/w_kj)(m_j/m_i); negative where both contend,
zero where i carries no exponent, blank where j carries none; reciprocal across the diagonal; piecewise at K > 1; the
elasticity is its log-log, constant-per-term form. Two objects: the term's tension matrix, from the fit, at the term's
balanced point (the paper's figure beside Figure 7's data correlations); a design's tensions, from the data, the
formula at the design's metric ratios (the decision section's number at a pick, in metrics and through Theorem 7 in
attribute units). Guidance on the routes back to attributes and to the design space goes to the docs. Scoped as WP42
(the tension spike, six stages).

**Supervisor, verbatim (12:55), on length:** "i want a 500 word cap not a 200 word cap form my abstract. (and to be
honest that number is still pretty arbitrary)"

**Applied as:** `paper/length_ledger.toml` `[abstract] cap = 500` with this ruling as its authority; the test
`test_abstract_within_200_words` is renamed and reads the ledger's cap; lands with the abstract.

**Supervisor, verbatim (13:05), on "directions of energy increase represent Pareto improvements":** "reading this now, i
cannot tell if we're talking about a round trip through a design which we cannot guarantee will be a pareto improvement
or just the predicted value. my intuition is that the predicted value will be a pareto improvement but the measured
value need not be. is that correct?" The assistant: partly; along the ascent direction every contending metric
improves together (Definition 9); other level-raising directions trade metrics; every Pareto improvement raises the
level (L11); a measured design need not follow (D.10).

**Supervisor, verbatim (13:10):** "i don't want to jam the predicted versus carried distinction into the abstract but i
do want it covered in the paper"

**Applied as:** the abstract states the two backed facts; the predicted-against-measured distinction is added to WP41's
Section 7 paragraph (D-3), citing D.10.

**Supervisor, verbatim (13:20), on "embeds datapoints within a dimensionally reduced space":** "both in the order
above", choosing the sentence: "Like PCA, HTS is unsupervised. Where PCA fits a subspace and projects the data onto it,
HTS fits a surface one dimension below the metrics and gives every design a position on that surface and a level
relative to it; projecting onto the surface drops the level, and keeping both loses nothing." (Backed by Theorem 1's
V(m/V(m)) = 1, Theorem 6 and D.16.)

**Supervisor, verbatim (13:30), on the pull-back sentence:** "i like #1", choosing: "Every chart point pulls back
exactly to attribute units; a point with a datum is a design in the table; a point without one is a conjecture about a
design, proposed by a rule and settled by building and measuring it." (Theorem 7; the table's rows; Section 7 and
WP41's page.)

**Supervisor, verbatim (15:50), on the solver's word:** ""Loss for the solver's function everywhere (scikit-learn's
word)" yes. though we need to make sure we're clear that we've chosen that, and it frees up the objective phrase so it
fits in the what subset of the metrics do we care about optimizing for from the perspective of the decision analysis
problem, rather than getting it bound up in the solver level"

**Applied as:** WP42's open decision closes on (a): loss names the function the solver minimizes (J_tau at one term,
the mean slack at several) everywhere, with the choice stated once where the notation is set (Section 3's sentence on
Boyd and Vandenberghe and the scikit-learn terms, and the glossary's entries for loss and objective); objective names,
in the decision-analysis frame, the subset of the metrics the decision-maker optimizes for; the solver level never
uses the word. The theorems, Appendix A, the lemma scripts' docstrings and the tests move with it in WP42's build.

**Supervisor, verbatim (16:00), on the nested layers:** "our fundamental challenge is we have nested layers of
optimizations: a design optimization problem, wherein we construct a novel unsupervised learning method, which has its
properties from optimization. so we're dealing with optimization in both the application domain (decision analysis)
and the methods (ML for detecting and interpreting trade-offs latent in the design space)"

**Supervisor, verbatim (16:05), on where the three-layer statement goes:** "definitely goes in the glossary. i think
we should cover it in brief in the paper and cite to the relevant appendix for more details"

**Applied as:** the three layers (the decision layer: objectives, constraints, Pareto notions; the design layer: the
model as a function of the metrics inside a designer's optimization, where GGP and log-convex belong; the method
layer: the fit as an optimization over the exponents, whose word is loss) are stated in full in the glossary's
preamble, with each entry naming its layer, and in brief in Section 3 with a citation to Appendix A (the register) for
the detail. Added to WP42's G3 and deliverables; the Section 3 paragraph lands with WP42's build.

**Supervisor (16:55, by popup), approving WP42:** "WP42,WP46" (the approvals question). WP42 is approved as drafted,
with its open decision already closed on loss (15:50) and G3b added (16:05); execution begins in the background.

**Supervisor, verbatim (17:35), on two abstract sentences and the length:** ""Our proofs are scripted with SymPy, and HTS
is implemented as a scikit-learn estimator, so it works with existing pipelines and tools." / approve this change and
the change about "piecewise hyperbolic frontiers". i am fine with 505. i am currently thinking of 500 word as the
target length but with slight under or overshot okay"

**Applied as:** both sentences stand in the draft (`WP11-final/abstract/draft-2026-11-14.md`) in his wording; the
abstract's length rule is a target of 500 words with a slight overshoot or undershoot allowed; the ledger's `[abstract]`
entry carries target 500 and the test's bound allows five percent over (525), with this ruling as its authority, landing
with the abstract. Earlier at 15:50 his words on the draft's register: "i find the way you write pretty obtuse and often
overly specific for an abstract. although we're correcting my technical term choice, the flow and balance of the
abstract should not be significantly changed from my version" (applied: the light-touch draft).

**Supervisor, verbatim (17:50):** "we're getting close on the abstract but i think this is a bit obtuse still "One term
merges the subsystems' trade-offs; two terms separate them." my gut is we can just drop the sentence"

**Applied as:** dropped from the draft. The answer key's depth-A line (the finding in one sentence) reads, from its
next version, the sentence that follows it in his abstract: high-dimensional n-lemmas detected and used to inform the
decision; the ledger raise of 2026-11-09 that paid for the old finding sentence (7 words) lapses with the new cap.

**Supervisor, verbatim (17:55):** "you can land the abstract now based on my edits."

**Applied as:** the abstract lands as the draft stands at 49e7838 (`WP11-final/abstract/draft-2026-11-14.md`, 497
words), by a unit the assistant spawns: the notebook's front matter replaced word for word; the length ledger's
`[abstract]` entry set to target 500 with a five percent tolerance (the test's bound 525) citing the 17:35 ruling; the
three tests that pinned the old abstract's phrases rewritten to pin the new text; claims rows for the new sentences;
vocabulary clean; no other surface changed without the assistant's word. The unit lands after the third paper unit if
that lands first, rebased and fast-forwarded; the assistant verifies before the stage is rebuilt for the held-out reads.

**Supervisor, verbatim (18:15), on the entry surfaces against the new abstract:** "make sure the small edits are
captured in a relevant workpackage. broadly its a good sign that we didn't cause edit cascades."

**Applied as:** the four small edits and the two naming items of
`WP11-final/abstract/entry-surfaces-consistency.md` are entered in WP42's scope (G3, the surfaces brought into line
with the glossary), as its build's first list; the root page's summary paragraph and "bespoke or opaque" stay on the
supervisor's review list as his hand.

**Supervisor (2026-11-15, 10:05 EST), on the abstract's sentence "Pareto improvements increase energy, and a design that
maximizes energy is weakly Pareto-efficient", after the held-out round's one wrong belief (F15 reversed it) and three
options (keep; "though not the reverse"; "since energy rises with every metric"):** "Keep as is"

Request 172's Pareto item is closed with no change; the sentence stands as written. The other abstract phrases of
request 172 remain his list.


## The abstract, his review of the candidate (2026-11-15 08:40 EST)

**Supervisor, verbatim** (quoting the sentence "HTS fits a surface one dimension below the data and places each design
by its position on it and its level above or below it, losing nothing"): "surface one dimension below the data and
places each design by its position on it and its level above or below that surface."

**Applied as:** the sentence now ends "its level above or below that surface." ("losing nothing" dropped, "it" made
"that surface") in `paper/paper.ipynb`; the register row's fragment follows the text.

**Supervisor, verbatim (the same sitting):** "i don't think i can say it is a "scikit-learn estimator" since we're not
literally adding it scikit-learn, i think we need to say. "HTS is implemented with a scikit learn compatible API, so it
integrates naturally with existing pipelines and tools.""

**Applied as:** the abstract's sentence reads "HTS is implemented with a scikit-learn-compatible API, so it
integrates with existing pipelines and tools." ("naturally" dropped as a word doing no work; hyphenation per the
glossary). The two other surfaces that say "scikit-learn estimator" (the docs home's quickstart line and the
package docstring) are put to him as one question before any sweep.

**Supervisor, verbatim (the same sitting):** (quoting "The worked example is a cubesat design optimization problem
with competing objectives in performance and cost.") "cut the "with competing objectives in performance and cost."
since its said later. putting that qualification twice in the abstract feels like space waste"

**Applied as:** the sentence reads "The worked example is a cubesat design optimization problem."; the register
fragment follows.

**Supervisor, verbatim (the same sitting, on "weakly Pareto-efficient" and the driver's note that "increase energy"
is strictly "do not decrease"):** "i think that the level of the abstract "weakly" and "nondecreasing" in place of
increasing is overly specific. technically correct but its essentially pre caveating. we have the precise results
with their conditions in the body"

**Applied as:** the abstract reads "Pareto improvements increase energy, and a design that maximizes energy is
Pareto-efficient."; the precise statement with its conditions stays in the body (Lemma 11, Theorem thm-pareto:
weakly Pareto-efficient, V nondecreasing in each metric). The paper test's phrase and the register fragment follow.
The "scikit-learn estimator" ruling applied to the docs home ("It has a scikit-learn-compatible API") and the
package docstring ("A scikit-learn-compatible estimator").

**Supervisor, verbatim (the same sitting):** "drop weakly and stick with the increases energy language"; "future work
edit is approved" (the driver's draft: "Future work has three thrusts: (1) searching the design space for designs that
push the frontier outward, (2) finding and filling the holes within it by topological data analysis, and (3) formal
verification and performance, moving beyond Python into Rust and using theorem provers."); and, on Section 1's
opening sentence ("This paper is for readers deciding whether to rely on a trade study, checking the mathematics
(Section 4, Appendix B), or placing the method among prior methods (Section 2, Appendix G).") "cut this on the basis
of the anti meta narration rule. Section 1 should start with "Decision analysis has two products: an answer, and a
justification an accountable executive can follow and defend.""

**Process ruling, verbatim:** "this is really slow (and thus bad UX) on the review and revise loop. i think we might
need to work with cached version together. it feels a bit like you are calling some one who call someone who then
makes an edit. i get that we have a process for autonomous work but when I am the worker you need to be able to edit
a cached file in place with me then submit that as a batch to the workers to intergrate"

**Applied as:** the abstract is edited in place in `work-packages/review/abstract-draft.md` (one sentence per line),
each edit applied at once with no tests or rebuilds between; body edits go straight into the notebook the same way;
one integration pass at the end of the sitting writes the abstract back, updates the register and the tests, runs
them, commits and rebuilds the staged site.

**Supervisor, verbatim (Section 1):** ""recognized, rigorous and reproducible." i reordered them and included the
"and"" (the sentence "The justification is the hard product: the process turning much data into little must be
recognized, reproducible, rigorous.")

**Applied as:** "...must be recognized, rigorous and reproducible." in the notebook (batch; integration at the end
of the sitting).

**Supervisor, verbatim (Section 1):** ""handle real data's scale, complexity and noise while remaining
interpretable."" (for "...noise interpretably.")

**Applied as:** "To displace the document, a method must handle real data's scale, complexity and noise while
remaining interpretable." (batch).

**Supervisor, verbatim (Section 1, the PCA paragraph; screenshot of the rendered paragraph attached in chat):** "this
paragraph needed a rewrite: extra transition sentence, align with abstract and clearer why not pca "Techniques from
machine learning such as feature engineering and dimensionality reduction provide interpretability at scale. For
example, principal component analysis (PCA) identifies basis vectors which explain the variance in a dataset(citation).
However, identifying how linearly independent vectors explain variance tells a decision-maker very little to judge a
trade-off.""

**Applied as:** his three sentences replace the paragraph, the Jolliffe and Cadima citation kept where "(citation)"
stood (batch).

**Supervisor, verbatim (Section 1, the paragraph "Objectives may align in one region..."):** "drop the forward link
to definition 1. we may need a citation related to using trade studies or decision analysis in configuration
management for a fielded system. its okay if the citation says its impractical because it takes to long since our
approach addresses that speed issue by making a decision analysis pipeline built a design time available to refit with
new data from the fielded system."

**Applied as:** the link dropped ("The fitted reference surface, a posynomial fitted to the data underlying the
table, gives them a coordinate system."); the citation is searched for and put to him with its DOI before it enters
`docs/references.bib`.

**Supervisor, verbatim (Section 1, four more):** "incorporate my comment here into the contribution statement. our
contribution is interpretability at scale and reusability of the decision analysis code."; on the generated
sentence "Of 2,134 feasible cubesat designs, the nondominated set ... holds 236 on 4 attributes ... and 2,134 on all
13 ...": "this is out of place in Section 1"; on the "Organization." paragraph: "this does not belong"; ""The method
claims nothing as novel and does not replace PCA or Pareto analysis." this can get cut. its metanarration"

**Applied as:** the contribution reads "Interpretability at scale, and reuse of the decision analysis. The fit reads
trade-offs on a table too large for dominance to shortlist (on this case the nondominated set is the whole table),
and names them as n-lemmas with elasticities. The pipeline built at design time refits on new data from the fielded
system, so the decision analysis is reused in configuration management instead of rebuilt for each change." (the
driver's draft of his intent, his to strike); the generated nondominated sentence (a code cell) moved to the opening
of Case analysis; the Organization paragraph and the novelty sentence cut (batch).

**Supervisor, verbatim (Section 1, the "Main results" list):** "this needs to be replaced with a prose paragraph that
walk through the outline of the paper. this is the only place where metanarration and forward links are allowed. it
should be concise, and provide a clear description of the contents of the paper. you can find examples in the IEEE
papers i shared as references when we started"

**Applied as:** the numbered list replaced by one roadmap paragraph ("The paper proceeds as follows. Section 2 places
the method among the families it borrows from ... Section 13 closes with future work."), with the forward links; the
results it listed stay stated in Section 6 (batch; the register rows that quoted the list are resolved at integration).

**Supervisor, verbatim:** "i accept your suggestion to cite Fulcoly, Ross and Rhodes 2012, for the configuration
management statement"

**Applied as:** `docs/references.bib` gains `fulcoly2012evaluating` (Procedia Computer Science 8, 22–30, DOI
10.1016/j.procs.2012.01.009, resolved through Crossref); Section 1's sentence reads "...and configuration management,
where a system in service is changed in response to a changed context [Fulcoly, Ross and Rhodes 2012]." (batch).

**Supervisor, verbatim (the roadmap paragraph):** "i am not sure if we want to cite the appendices in this outline.
that feels over the top. one thing it does call to mind though is the order of the appendices. it seems like they
should roughly match the order of the paper and that can be handled by reordering them to be lettered in the order they
first appear the paper. i would recommend we take that reordering approach but hold off on applying it until the paper
prose is reviewed so we do not need to reorder multiple times"

**Applied as:** the three appendix mentions dropped from the roadmap (batch). Deferred, in
`work-packages/review/deferred.md`: re-letter the appendices in the order of their first mention in the paper, once
the prose review is done.

**Supervisor, verbatim:** "the contribution section is too long and too detailed. i think it may be just
"Contribution. Interpretability at scale, and reuse of the decision analysis.""

**Applied as:** exactly that sentence (batch).

**Supervisor, verbatim:** "and i think it may be better to simple say "Our contribution is interpretability at scale,
and reuse of the decision analysis via unsupervised learning." as the last sentence of the previous paragraph. its
metanarration but its also the transition sentence for the paper outline in prose that follows"

**Applied as:** the bold "Contribution." paragraph removed; his sentence closes the preceding paragraph, before the
roadmap (batch).

**Supervisor, verbatim:** ""Our contribution is interpretability at scale, and reuse of the decision analysis
pipeline via unsupervised learning." add the word pipeline, its the pipeline that is reused"

**Applied as:** so worded (batch).

**Supervisor, verbatim (Section 2):** "on to Section 2. Just "Prior Art" not "by family" "We claim no priority. Table 1
lists the families and what we share with each. Appendix G is the larger register and says for every entry how this work
differs." drop this and instead we need a simple prose paragraph summarizing the families of prior art we draw on. this
is not supposed to be long so don't list everything out. its basically the following 3 layers: The engineering decision
problem itself (Decision Analysis, MBSE and Multidisciplanary decision optimization; multiply objective optimization);
the next layer down is Machine learning methods primarily unsupervised dimensionality reductions, the lowest level is
optimization theory but focused on solvers (convex optimization, GGPs, etc). this opening paragraph should present a
coherent story of we want to analyze a multi objective design optimization, we want an unsupervised ML method that
uncovers trade-off, we need to actually be able to solve the underlying optimization that fits it. can you draft a short
summary paragraph for the prior art section for me"

**Applied as:** heading "Prior art"; the opening paragraph replaced by the driver's draft of his three layers (about
150 words, citing keys already in the bibliography), his to rewrite; the family table and the family paragraphs
untouched (batch).

**Supervisor, verbatim:** "you took my prose input too literally."

**Applied as:** the three-layer paragraph redrafted as prose without the layer scaffolding or his sentence echoed
(batch).

**Supervisor, verbatim (the Section 2 drawing):** "the stacked is decent. easier to read than the nested one let's
change the text to "which objectives trade, and a choice that can be defended" "a recognized, rigorous and
reproducible technique" i closed it (by accident) before i could offer text for the lowest layer"

**Applied as:** the stacked drawing kept (`work-packages/review/prior-art-layers-stacked.svg`), its top and middle
glosses replaced by his; the bottom gloss awaits his text.

**Supervisor, verbatim (the bottom band):** "convergence and performance of the underlying fit"

**Applied as:** the drawing complete with his three glosses, copied to `paper/figures/fig-prior-art-layers.svg` and
placed under Section 2's opening paragraph as `fig-prior-art`; the paragraph revised to follow the drawing band by
band. At integration the drawing gets a generator beside it (the paper's figures come from called code,
`paper/figures/chart_level.py` is the pattern) so Section 11's claim holds.

**Supervisor, verbatim (the figure's caption):** "rephrase "Each layer consumes capabilities provided by the one below
it.""

**Applied as:** the caption's last sentence is his (batch).

**Supervisor, verbatim (Section 2, the spot check):** "otherwise section 2 looks mostly good. though i need you to do a
spot check for concepts from our later definitions used before they are defined." then, on the seven remediations
walked through: "you can apply your edits and rerender for me to review. after that i'd also like you make sure our
Table one is clustered by the 3 layers we introduced. it should flow from top to bottom (from the decision making
problem down to the solvers). i realized its not going to necessarily fit perfectly into clusters but i think it should
flow from closest to the justifying a decision to closest to the solver. that way the prior art flows from why we're
doing this down through what we're doing down into how"

**Applied as:** the seven edits (fitted value for V, fitted surface for terms, weight vector and softened maximum in
the DEA contrast, the title sentence cut, planted trade-offs, our coordinates, the Appendix G pointer cut); Table 1's
order to follow.

**Applied as (Table 1 and Appendix G):** `paper/prior_art.yaml` reordered into the three layers, top to bottom
(decision problems: practice, decision analysis, MBSE, MDAO, tradespace, Pareto; machine learning: PCA, log-ratio,
kernel PCA, HoroPCA; solvers: DEA and its relatives, production and distance functions, frontiers, GP and max-affine,
entropic risk), the `group` field renamed to the three layers so Appendix G follows the same flow; the table's stored
output refreshed for the review render, the notebooks re-executed at integration (batch).

**Supervisor, verbatim:** "i also want to drop the phrase "the frontier method nearest in spirit", also i think DEA is
probably the middle layer."

**Applied as:** the phrase dropped; DEA named in the middle sentence ("data envelopment analysis scores each design
against the edge of the table"); in the register and Table 1, DEA, multiplicative DEA, the hyperbolic graph measure,
production and distance functions and the frontier family move to the machine-learning layer after the PCA family;
the solver layer is geometric programming with max-affine fitting and entropic risk (batch).

**Supervisor, verbatim:** "drop this awkward qualifier "though what principal component analysis finds is variance,
not trade-offs," you don't need to jam every point in every time. that shows up elsewhere"

**Applied as:** dropped (batch). Standing note for the driver: one point per place; the paper's other passages
carry the rest.

**Supervisor, verbatim:** "the figure 1 cite is dangling. let's give it a sentence "Figure 1 disambiguates the use of
optimization literature for developing unsupervised machine learning techniques from the optimization literature
applied to decision analysis." something along these lines"

**Applied as:** "Figure 1 separates two uses of the optimization literature: as the solver beneath an unsupervised
learning technique, and as a method of decision analysis in its own right." closing the paragraph (batch).

**Supervisor, verbatim:** "drop "in its own right:"

**Applied as:** dropped (batch).

**Supervisor, verbatim:** "drop "Open. Which part of the Pareto boundary the fitted surface reaches is our reading: the theorem gives efficiency of a maximizer, not the converse.""

**Applied as:** dropped from the Pareto paragraph (batch; its register row resolved at integration).

**Supervisor, verbatim:** ""Combining these pieces in one estimator is our design. We did not find the combination in the sources reviewed." cut this metanarration"

**Applied as:** cut from the Lineage paragraph (batch; its register rows resolved at integration).

**Supervisor, verbatim (Section 3):** "I am in Section 3 now and one thing i am noting is that there are a lot of
forward references which are not about notation. i think we need to start with a cleaning pass that removes out of
place content. we'll get to it when we get to it (eg the implementation and the example). "Mathematical notation
follows Boyd and Vandenberghe ... Appendix A is the full register of symbols and terms." is fine but cut "The package
is the scikit-learn estimator of Section 5 and Appendix F." we can define a pipeline in mathematical notation but we
should not be talking about the cubsat example yet"

**Applied as (the cleaning pass):** cut from Section 3: the package sentence; the cubesat sentence in the pipeline
paragraph; "done with scikit-learn tools (Section 5)" from stage 2; "Section 5 adds the regularity conditions R1, R2
and R3"; the two Appendix E sentences closing "Map and territory"; "Appendix A gives each word with its layer" closing
"Layers". Kept: the Appendix A register sentence he approved, the pipeline's stages and symbols, the assumptions, the
first two sentences of "Map and territory", the three layers' words, and "Words" with Definition 1 (batch).

**Supervisor, on the pipeline figure for Section 3 (verbatim, in order):** "i think we may need a figure for our our
pipleline. should flow left to right. look at existing visual semantics for pipelines from the scikit-learn
documentation and/or recent works in ML pipelines"; "its a bit crowded, and may have more detail than we need. includes
some inconsistent visual semantics but i think if you iterate on it, it will converge. keep in mind that diagrams are
communication devices, you do not need to jam every potentially relevant fact into the diagram. we are in the
preliminaries and notation section and we cannot assume our readers are familiar with ML pipelines so we're providing
it as a preliminary"; "i think you can drop the "the method" box. i think we need a variable and name for the arrow
between identify and analyze"; "V hat feels wrong to me since V is the value of the level sets and in practice we're
more interested in the tensions, the n-lemmas, etc"; ""the analyst's step" -> "feature engineering" and "the fitted
terms" -> "the trade-offs""

**Applied as:** `work-packages/review/pipeline.svg`, four stages left to right (evaluate, condition, identify,
analyse) in one fill, the data on the arrows as c, a, m and w, β with the names configurations, attributes, metrics,
the trade-offs; under the stages: a black box, feature engineering, fit the surface, read it. Not yet placed in
Section 3; it goes in with a generator at integration.

**Supervisor, verbatim:** ""read it" becomes "interpret it""

**Applied as:** so labelled; the figure placed under the pipeline paragraph of Section 3 as fig-pipeline with a one-sentence caption (batch).

**Supervisor, verbatim:** "change "interpret it" to "decision analysis""

**Applied as:** so labelled (batch).

**Supervisor, verbatim:** "this works. let's put it in and then look at how the prose fits around it"

**Applied as:** the pipeline paragraph rewritten to follow the figure (the figure referenced in its heading; evaluate, feature engineering, identification of the trade-offs as terms with exponents and offsets, the analysis into a decision; the stage numbers and the bold dropped), the caption shortened to one sentence (batch).

**Supervisor, verbatim (Section 3):** "your phrasing is weird. speak plainly: "A featuring engineering step is applied
to condition the attributes into metrics m, strictly positive and larger is better." also this is where we're
introducing notation be explicit and direct about exactly that. the notation. you do not need to go into all the
assumptions that show up later, you just need to provide the notation. to the greatest extent possible we're doing
nothing fancy or novel here. its simply a quick start for reading the math to follow. you can drop map and territory,
layers (since we addressed it in the previous section) and the words part reads as weird metanarration. Definition 1
as written is overly dense (its actually 3 definitions) and its not obvious what it means from what we said above. we
should not be forward referencing Definition 4 in definition 1"

**Applied as:** Section 3 is now the notation sentence, the pipeline paragraph (his sentence, plain), the figure, and
one "Notation" paragraph (N, d, M, U, u_i, Δ, K, w_k, β_k, V, τ, κ, ∞, vectors). The assumptions paragraph moved
verbatim to the head of Methods, before the conditions R1 to R3. Map and territory, Layers and Words dropped.
Definition 1 split into three plain definitions (the fitted reference surface, the supporting envelope, the Pareto
boundary), placed in Section 4 after the temperatures so none refers forward (batch).

**Supervisor, verbatim:** "once we clean it up. i also think definition 1 belongs in Definitions section but it needs to clearly follow from the preliminaries and notation"

**Applied as:** the three definitions open Section 4, worded in the notation paragraph's symbols (V, tau, the table's rows), before the invariant value (batch).

**Supervisor, verbatim:** ""logarithms are natural" no one would ever say it this way."

**Applied as:** "U = log M its natural logarithm, taken entrywise, with rows u_i." (batch).

**Supervisor, verbatim (Section 3, the build-up):** "now that we've clean up the extraneous stuff. you need to define
an optimization problem in terms of a decision variable and a loss function. you need to be clear whether V is a value
or a function. in short this sections job is to provide the minimum viable notation kit and background so the
Definitions section is readable. then the definitions provide what we need to describe our method, which then allows
us to provide our results. this is incrementally building up the math. as you have it written now its kinda kludged
together, unnatural and impossible for a human to follow"

**Applied as:** after the notation sentence, the pipeline paragraph and the figure, four short paragraphs in order:
The data (N, d, M, U, u_i, the simplex); A model is a function of the metrics (the monomial term with parameters w
and β, V the function and V(m) its value, the unit level set a surface, K terms with their parameters); The soft
maximum (the log-mean-exp with τ, τ = ∞ the exact maximum, κ over terms); The fitting problem (parameters θ as the
decision variables, a loss J(θ; U), θ* the minimizer over the feasible set Θ; loss versus objective). The one-term
instance stays in Methods, which the last sentence points to (batch).

**Supervisor, verbatim (structure, 2026-11-15 ~11:30 EST):** "i think it may be time for me to give you some space to
iterate. i have a few other concerns. "search of the design space preliminary" belongs in the future work section.
not its own section. the future work section can be just called future work not "future work and final remark"
Reproducibility and your own case can be pruned and what needs to be kept can be integrated into the acknowledgements
and process section. that section should be renamed AI acknowledgement and Reproducibility. it should cover both that
we did and did not use AI as well as how the results can be reproduced and adapted. do not make this section long, do
not make this section verbose or metanarration. its purely informational: what we did, how we did it and how you can
reproduce it. let's step back and structure some work packages together now"

**Recorded as:** three structural rulings for the next packages (Section 7 folded into Future work; the section named
"Future work"; Reproducibility merged into a short "AI acknowledgement and Reproducibility" section replacing
"Acknowledgments and process"); the review loop moves to packages the driver iterates on and he reviews when ready.
