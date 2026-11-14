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
