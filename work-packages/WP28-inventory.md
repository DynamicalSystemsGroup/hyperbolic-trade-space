# WP28 D-1 — The inventory

| | |
|---|---|
| **Date** | 2026-11-10 |
| **Staged head** | fbeede5 (`fbeede50cdc195ee7d590825a987321f0a7969eb`), served at http://127.0.0.1:8791/ |
| **Readers** | 56 fresh readers over 122 units (14 paper sections, 7 appendices, 14 docs pages, the root page with the README, 9 paper figures, 1 paper table, 8 docs figures, 2 root-page images); a boxed statement read by its section's reader, an appendix's tables by its appendix's reader |
| **Models** | two, 28 readers each (`WP28-inventory/readers.tsv`, column `model`) |
| **Files** | the returns verbatim in `WP28-inventory/returns/`, the briefs in `WP28-inventory/briefs/`, the seven templates in `WP28-inventory/templates/`, the unit list `WP28-inventory/units.tsv`; how the slices were made in `WP28-inventory/README.md` |

**R-2.** The PM read the seven templates in full and one assembled brief, and grepped all 56 assembled briefs
(case-insensitive) for work-packages, review, triage, change request, round, wp[0-9], persona, decision, supervisor,
driver, PM, inventory: 0 hits; the briefs differ from the templates only in the unit's name, its slice paths and its
return path.

**How the table is read.** One row per unit of `units.tsv`, in its order. The cells quote the readers verbatim; a cut
is marked "...". A statement row carries its section reader's Q6 line (label and words in the sentence column). An
appendix-table row carries its appendix reader's Q7 line verbatim in the sentence column, with "pointed to" and
"would look for it" tabulated in the story column. The root page and the README carry the root-readme reader's Q1 to
Q4 for each. The root page's two images are not units of `units.tsv`; their readers' rows follow the table, under
"The root page's two images". Where a reader's verdict is conditional or qualified, the words are quoted and the
nearest of the four is in brackets.

## The inventory

| unit_id | kind | parent | reader's sentence (Q1) | story sentence served (Q2) | verdict | reason (Q3) | named unit if repeats (Q4) | return file |
|---|---|---|---|---|---|---|---|---|
| `sect-problem` | section | — | It frames the problem (a trade study needs an answer plus a defensible justification; weighted tables and PCA fall short on trade-offs), introduces the method's vocabulary (reference surface, chart, n-lemma), states the cubesat dominance finding, and lists the paper's main results. | Abstract: "A trade study must produce an answer and a justification an accountable executive can follow", and "PCA ... explains variance. We explain tensions." | advances | The abstract's opening problem statement and the "explain tensions where PCA explains variance" contrast are motivated only here, and the 706 / 126 / 659 dominance counts (why dominance stops shortlisting) appear only here in the story. The main-results list is a map to later sections and mostly restates the abstract, but the motivation and the dominance counts are carried by no other unit I can see. | — | `returns/sect-problem.md` |
| `sect-prior-art` | section | — | It places the method among eleven nearby families (Pareto methods, data envelopment analysis, production and distance functions, frontier estimation, PCA and its compositional and kernel variants, geometric programming, MDAO, tradespace exploration, decision analysis, MBSE). | Section 1, paragraph 2: "the computational alternatives are bespoke and opaque", and the abstract and Section 1 sentence "Like PCA, our method is unsupervised feature engineering; the two answer different questions". | advances | Section 1 says the existing alternatives fall short and that the method differs from PCA. A first-time reader then needs to know, in the body of the paper, how the method differs from the obvious near neighbours: a nondominated set, DEA, frontier estimation and fitting with geometric programming. | — | `returns/sect-prior-art.md` |
| `tab-families` | float | sect-prior-art | For eleven neighbouring families of methods it states, in a line each, what the family produces, what this work has in common with it and how it differs, with the citations. | None of the seven numbered main results. ... Otherwise, none. | repeats | The Pareto, DEA, PCA, production, frontier, geometric programming, kernel PCA, tradespace and the compositional rows are each said again, in fuller and clearer sentences, in the prose directly under the table ("Pareto methods", "Data envelopment analysis", "Lineage"), and the Section 2 introduction already points to Appendix G for the full register. What the table alone adds is the four-way layout and the rows for MDAO, decision analysis and MBSE, which have no paragraph below; but Section 1 already places the method against MDAO, decision analysis and MBSE, and no sentence of the story needs the row. | sect-prior-art (the prose of Section 2 under the table), and for the full register appendix-g (Appendix G, Register of prior art). | `returns/tab-families.md` |
| `sect-notation` | section | — | It sets out the pipeline (configuration, then attributes, then conditioned metrics, then identification and analysis), the symbols for the table of metrics ($M$, $U=\log M$, the simplex $\Delta$), the assumptions A1 to A7, a caution that the formal results are about mathematical objects and not the real table, and Definition 1, which separates the fitted reference surface, the supporting envelope and the Pareto boundary. | Main-results item 1 (it cites Definition 1 directly: the surface "is not the Pareto boundary"), and the Section 1 sentence "The surface is not the Pareto boundary, and the table and its reading are views (Definition 1)". | advances | The story twice leans on Definition 1 to say the fitted surface is not the Pareto boundary, and this section is where that definition is stated; no other unit is named as carrying it. The pipeline paragraph also carries the abstract's and Section 1's "a configuration is evaluated into attributes whose trade-offs the fit reads" and says which stages are the method. | — | `returns/sect-notation.md` |
| `def-objects` | statement | sect-notation | Definition 1 (Three objects): It is the definition the story cites for item 1 and for "not the Pareto boundary"; it separates the fitted surface (some designs exceed it), the $\tau=\infty$ envelope (none exceeds it) and the Pareto boundary (a property of the system). | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-notation.md` |
| `sect-definitions` | section | — | It gives the paper's working definitions (Definitions 2 to 9): the invariant value V and its log as the energy differential, the posynomial sum of terms, the two temperatures and the near-frontier band, the chart (Z, log V), the n-lemma of a term, reach and share, elasticity, and the ascent direction. | Main-results item 1 (the invariant value, the surface where it equals one, position and level, elasticities, "Definition 1") and item 2 (exponents are elasticities, the chart is reversible). | advances | The story uses the terms energy differential, chart, n-lemma, elasticity, band and posynomial, and this is the place where each gets a precise form (a formula or a rule), which Section 1 and the abstract only name by analogy. Not every definition is needed by the story (see Q6). | — | `returns/sect-definitions.md` |
| `def-invariant` | statement | sect-definitions | Definition 2 (Invariant form): Gives V as a weighted geometric mean, scaled to 1 on the surface; the story's invariant value. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `def-posynomial` | statement | sect-definitions | Definition 3 (Posynomial): The several-term model; "a piece of the surface, not a set of designs" matches Section 1. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `def-temperature` | statement | sect-definitions | Definition 4 (Temperatures and band): Fit and term temperature and the near-frontier band; the band and the soft support are in the story. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `def-chart` | statement | sect-definitions | Definition 5 (The chart): The reversible rewriting (Z, log V) of the abstract and of item 2. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `def-nlemma` | statement | sect-definitions | Definition 6 (The n-lemma): The contending set is how the abstract's n-lemma is found; Figure 1 illustrates it. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `fig-nlemma` | float | sect-definitions | The figure shows that a term's exponent vector is a point of the simplex whose face (corner, edge, interior) names the term's n-lemma, and that on a synthetic three-metric table the fit recovers three planted terms (two dilemmas and a trilemma) at or near their planted points. | The abstract sentence "Each monomial term ... reports its contending metrics, an n-lemma (by analogy with dilemma and trilemma)", repeated in Section 1 ("Each monomial term ... names the metrics that contend on it ... an n-lemma"). | advances | The abstract and Section 1 rest on the word n-lemma, coined by analogy, and Definition 6 defines it only as the support of an exact-maximum fit to a cell; this figure is the one place in the paper (by the units list) that makes the analogy concrete, showing dilemma and trilemma as the edge and interior of a simplex, with a recovery check against planted terms. No other unit in the paper is named as carrying that picture; its value is limited by the unpopulated corner and the unexplained gap of term 2 from its ring. | — | `returns/fig-nlemma.md` |
| `def-reach` | statement | sect-definitions | Definition 7 (Reach and share): reach advances (it scales V to 1 on the surface); the term share does not advance, since no story sentence uses it. | — | split: advances (reach) / does not advance (term share) | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `def-exchange` | statement | sect-definitions | Definition 8 (Elasticity): The percent-per-percent trade-off in the abstract and item 1. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `def-ascent` | statement | sect-definitions | Definition 9 (Ascent direction): No sentence of the abstract or Section 1 mentions tangent space or gradient of log V. | — | does not advance | — (Q6 gives a verdict and a few words only) | — | `returns/sect-definitions.md` |
| `sect-methods` | section | — | It states how the one-term fit is posed (an entropic soft maximum minimized over weights, with a target fraction of designs above the surface), what the analyst must do to the data first (log-affine conditioning), what the estimator's interface is, and which simplifying assumptions the method makes. | Main-results items 2 and 3 (the one-term fit is a geometric program; the chart is reversible) and, in the abstract, "Modelling a single n-lemma fits a monomial, which transforms into a convex program", plus "fitted to the outer edge of the data, not through its middle: a soft support". | advances | The story says the surface is fitted to the outer edge, not the middle, and that the fit is convex; the section is the only place that gives the actual objective (the log-mean-exp, the target fraction tau, the weights on a simplex) and the conditioning the theory requires. The estimator paragraph and the list of assumptions are the reader's only statement of what is being fitted and what is assumed, though several parts are compressed enough that a first reader must take them on trust. | — | `returns/sect-methods.md` |
| `sect-results` | section | — | It states, with hypotheses, a sketch and a script for each, the results the method rests on. | Main results 1, 2, 3, 4 and 6. | advances | Section 1 names Section 6 as the home of main results 1 to 4 and 6, and no other unit is named as carrying the boxed statements; the appendices hold the full proofs, not the statements the story points to. Without this section, the story's claims of convexity, global minimizers, elasticities, reversibility, Pareto efficiency and the levels of guarantee would have nothing on the page to stand on. | — | `returns/sect-results.md` |
| `thm-invariant` | statement | sect-results | Theorem 1 (Homogeneity and the invariant form (L1)): Main result 1; it is what makes "a weighted geometric mean that doubles when every metric doubles" true. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `prop-shift` | statement | sect-results | Proposition 1 (Uniform shift (L2)): No story sentence asks for it; it supports the offset's meaning and the shift property used in Theorem 8. | — | does not advance | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-kkt` | statement | sect-results | Theorem 2 (Gradient and the simplex KKT conditions (L3)): Main result 2. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-convex` | statement | sect-results | Theorem 3 (Convexity of the fit (L4)): Main result 2 ("every minimizer is global"). | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-lme` | statement | sect-results | Theorem 4 (Log-mean-exp against log-sum-exp (L5)): No story sentence cites it; it supports the squeeze that Theorem 8 reuses and the project's choice of the log-mean-exp. | — | does not advance | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `prop-cumulant` | statement | sect-results | Proposition 2 (Gaussian cumulant (L6)): The story mentions noise only as something a method must handle; this population identity is not cited and is not used by any later box in the section. | — | does not advance | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-elasticity` | statement | sect-results | Theorem 5 (Elasticities and improvement factors (L7)): Main result 2 and the abstract's "elasticities". | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-chart` | statement | sect-results | Theorem 6 (The chart (L8)): Main result 2 ("its chart is reversible") and the abstract's "reversible chart". | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-pullback` | statement | sect-results | Theorem 7 (Pull-back to attributes (L9)): No story sentence asks to read the result back in attributes. The nearest is "a configuration is evaluated into attributes whose trade-offs the fit reads", which does not need it. | — | does not advance | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-extension` | statement | sect-results | Theorem 8 (The posynomial extension (L10)): Main result 3 and the abstract's GGP compatibility. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-pareto` | statement | sect-results | Theorem 9 (A maximizer of V is Pareto-efficient (L11)): Main result 3. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-soft` | statement | sect-results | Theorem 10 (Soft-weight alternation (L16)): Main result 4 ("not convex in the terms"). | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-descent` | statement | sect-results | Theorem 11 (Level 1, descent (L15)): Main result 4, first level. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `lem-gap` | statement | sect-results | Lemma 1 (Level 2, numerical stationarity: the term gap (L12)): Main result 4, second level. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `lem-margin` | statement | sect-results | Lemma 2 (Assignment margin and stable radius (L13)): Main result 4; it is the tool for the third level, and the case's stable radius comes from it. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `prop-local` | statement | sect-results | Proposition 3 (Level 3, conditional local optimality (L14)): Main result 4, third level. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `cor-bound` | statement | sect-results | Corollary 1 (Approximate certificate (L14)): Item 4 does not cite it by name, but the stopping declaration ("certified" for a sharp fit) invokes it, and item 4 names the stopping declaration. | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `thm-certificate` | statement | sect-results | Theorem 12 (Soft-fit certificate (L17)): Main result 4 ("a soft fit has a second-order certificate"). | — | advances | — (Q6 gives a verdict and a few words only) | — | `returns/sect-results.md` |
| `sect-search` | section | — | It sketches a nested-loop scheme (fit, propose along each term's normal, evaluate and refit) for choosing what to evaluate next, and says plainly that it is future work with no results and an open convergence question. | Main-results item 6, only its last clause: "Open: ... the monotonicity of the search (Section 7)". | advances | Section 1 points to Section 7 for the open monotonicity question, and no other unit is named as carrying the search scheme, so the pointer needs this section. It carries a single open item and no result, so the story needs little from it, but it is not carried elsewhere. | — | `returns/sect-search.md` |
| `sect-case-construction` | section | — | It builds the cubesat case that the story's last result reads: the design variables (Figure 2), the eight attributes and the requirements that read them (Figure 3), the two regimes and their feasible counts (706 of 1000, 780 of 1000), the conditioning, and how the fit temperature is picked for the K = 1 fit (Figure 4, tau = 38.1). | Main result 7 ("On a cubesat model coupling power, mass and attitude control the terms separate contending sets that one term blends"). | advances | Result 7 and the abstract's last sentence need a case whose variables, attributes, feasibility and conditioning are stated, and this is the only section in the paper body that states them. Section 9 reads the case and Appendix C gives the model in detail, but neither stands in for this setup as the reader meets it. | — | `returns/sect-case-construction.md` |
| `fig-assembly-view` | float | sect-case-construction | It conveys which parts of the cubesat model are swapped among alternatives, which are tuned continuously, and which are fixed, i.e. where the six configuration variables live in the part hierarchy. | None directly. | does not advance | No sentence of the story needs it: the story's cubesat sentences concern what the terms separate, and the six design variables are already named in Section 8's first paragraph. The figure is a clear, correct map for someone mapping the case onto their own system model (its own "Good for" line), but that is not a sentence of the story. | — | `returns/fig-assembly-view.md` |
| `fig-behavioural-view` | float | sect-case-construction | It traces each of the eight traded metrics to the requirement in the cubesat system model that reads it, grouped by subsystem, and to the measurement or analysis that supplies its value. | At most, the abstract's "On a cubesat model coupling power, mass and attitude control, one term blends the subsystems' trade-offs into a single tension" and main result 7. | does not advance | The story needs the cubesat's eight metrics and their grouping by subsystem, and the text of Section 8 already gives both in one sentence. What only this figure adds is the requirement-to-metric traceability, the MoE/MoP marking and the supply path of each value. | — | `returns/fig-behavioural-view.md` |
| `fig-tau-sweep` | float | sect-case-construction | How the K = 1 fit changes with its temperature, which temperature was chosen (where about a tenth of designs lie above the surface), what that leaves in effective sample (about 23 designs), and which metrics carry the exponents there. | Two, both loosely. The abstract's "a soft support that a few designs may exceed, not a regression" ... And main-results item 7 ("on a cubesat model ... the terms separate contending sets that one term blends") | advances | The soft-support claim and the one-term "blend" in item 7 each need to be seen at least once on the case: the abstract only asserts that some designs may exceed the surface, and the figure is where one sees how many (the target 0.1) and what that costs in effective sample. I found no other unit named in what I was given that carries the sweep, though the page itself points to Section 5 for the convention and Figure 9 for the stock regime, which I did not read. | — | `returns/fig-tau-sweep.md` |
| `sect-case-analysis` | section | — | On the cubesat case, one term blends power, energy, mass and control into a single 5-lemma, while three terms split it into terms with different contending sets, each with its own elasticities. | Main result 7 ("the terms separate contending sets that one term blends (Section 9)"). | advances | Main result 7 points to this section by name, and no other unit in the list is the case reading. The One term and Three terms parts carry that result directly: a 5-lemma at K = 1, then sets of 4, 5 and 5 metrics at K = 3, with control effort and peak slew power each leading a term of their own. | — | `returns/sect-case-analysis.md` |
| `fig-planes-k1` | float | sect-case-analysis | At K = 1 the one-term surface appears in the plane of the two heaviest metrics as a straight line whose slope is their elasticity, with the designs plotted around it. | Main-results item 7 ("on a cubesat model ... the terms separate contending sets that one term blends"), as its one-term baseline. | advances | Figure 6 refers back to it ("Dark and light as in Figure 5"), and it is the only picture of the one-term fit that the K = 3 comparison in item 7 rests on. It makes the idea of a term's line in a slice concrete before the three-term panels use it. | — | `returns/fig-planes-k1.md` |
| `fig-planes-k3` | float | sect-case-analysis | At K = 3 each of the three terms has its own trade-off, drawn as a line with its own slope (elasticity) in its own pair of metrics, with the designs near each term's slice lying below it. | Main-results item 7: "the terms separate contending sets that one term blends (Section 9)"; also the abstract's closing words, "three terms separate the contending sets". | advances | Item 7 says the terms separate what one term blends, and Section 9 argues the terms add a model over a clustering because they give elasticities; this figure is the one place those per-term elasticities appear as slopes, each in a different pair, against Figure 5's single line. Figure 8 names the contending sets but gives no slope and has no map for term 1, and the text cites the bottom panel to explain why term 3's elasticity is read across part swaps; no other unit carries that. | — | `returns/fig-planes-k3.md` |
| `fig-chart-level` | float | sect-case-analysis | Each design's level relative to the surface can be read apart from its position along the surface's direction of main spread, and in this case the designs lie inside the flat surface and hug it. | Abstract: "A reversible chart separates a design's position along the surface from its energy differential." Also main results item 1, "the level from which every design's position and level... are read". | advances | The story says the chart splits position from level, and this is the only figure of the case that draws it, so a reader sees what "level" and "position" are for the data. The advance is modest. | — | `returns/fig-chart-level.md` |
| `fig-tensions-k3` | float | sect-case-analysis | For terms 2 and 3 of the K = 3 fit, the figure names each term's contending set with its exponents and shows, among the near-frontier designs of that term's cell, which metric pairs are in tension, so that the two terms visibly have different sets and different tensions. | Main-results item 7 ("the terms separate contending sets that one term blends"), and the abstract's closing "three terms separate the contending sets". | advances | Item 7 needs the reader to see that the K = 3 terms have different contending sets, and this is the only unit in Section 9 that shows the sets of terms 2 and 3 in full: the text gives their sizes (4, 5, 5) and term 1's members, but not the members of terms 2 and 3, and Figure 6 shows only each term's two heaviest metrics. The weakness is that most of the ink is the association heatmap, which the section itself calls an analysis of designs rather than of the model, and one of the three terms has no map at all. | — | `returns/fig-tensions-k3.md` |
| `fig-regimes` | float | sect-case-analysis | That changing the controller gains changes which five metrics trade against each other (the contending set) and how the metrics associate. | None. | does not advance | No sentence of the abstract or Section 1 needs the comparison of the primary and stock regimes; the story's case claim is about K = 1 versus K = 3. The figure is a legible, honest side-by-side, but what it supports (the problem's contribution versus the gains') is a Section 9 aside. | — | `returns/fig-regimes.md` |
| `sect-discussion` | section | — | It sets the limits on what the fit's output may be taken to mean: the certificate shows that the optimizer reached a local minimizer. | The abstract's opening sentence ("an answer and a justification an accountable executive can follow"), with Section 1's "the justification is the hard product". | advances | The story promises a justification an executive can follow and defend. That needs a plain statement of what the method's outputs do and do not support. | — | `returns/sect-discussion.md` |
| `sect-reproducibility` | section | — | It says every reported number comes from a tested module, that Appendix F holds the pinned setup and commands, and that a reader wanting to run their own table should supply configurations, attributes and a conditioning rule and start at the docsite's Getting started page. | Main-results item 6 only loosely (the reproducible record). | repeats | The story names reproducibility as a requirement and points to Appendix F for it, and this section only points to Appendix F and the docsite. It adds a short pointer for running one's own case, which no story sentence needs. | Appendix F (unit appendix-f) carries the toolchain, environment and commands; the docs page 'Getting started' (unit docs-getting-started) carries the start for your own table. | `returns/sect-reproducibility.md` |
| `sect-future` | section | — | It lists the directions the authors leave open, each paired with an assumption the paper made (one term, sharp weights, the analyst's choice of K, small K, log-affine conditioning, continuous variables, a log-convex envelope, illustrative hardware values, the search, Q1 to Q4, other lifecycle cases), and closes with a speculative idea: scoring a new technology by how far above V = 1 it is forecast to sit. | None directly. | does not advance | No sentence of the story needs a future-work list. The pieces that touch the story (Q1 to Q4, the search's convergence, GGP-compatible kernels) are already pointed to Section 6 and Section 7 by item 6, so this section only restates them as open, and the rest (selection rules for K, discrete variables, datasheet values, dents and holes, configuration management of a fielded system) are new directions that no story sentence asks for. | — | `returns/sect-future.md` |
| `sect-process` | section | — | It tells the reader that the work was done in supervisor-approved work packages, that an AI coding assistant drafted code, derivation scripts and text within them, that the derivations are machine-checked, and that the author is responsible. | None. | does not advance | The story is about the surface, the chart, n-lemmas, the convex fit, PCA composition and the cubesat case. None of its sentences depends on how the work was organized or on an AI assistant's role. | — | `returns/sect-process.md` |
| `sect-cited` | section | — | It is the numbered reference list: the full bibliographic record, with a DOI or stable URL, for each work the paper cites, from decision analysis and trade studies through DEA and frontier estimation, compositional data, geometric programming, kernel and hyperbolic PCA, entropic risk, MDO and tradespace exploration, to scikit-learn. | Section 1's cited sentences, not a numbered main result. | advances | Section 1's case for the problem (decision analysis has two products, trade studies rest on biased weights, practice is moving to model-based work, PCA explains variance) rests on cited works. A reader can check them only through this list. | — | `returns/sect-cited.md` |
| `appendix-a` | appendix | — | Appendix A is a single register of about 70 terms and symbols, giving for each its meaning in this paper, what it is not, and where it is defined. | No numbered main-results item. | advances | A reader of the abstract and Section 1 meets many coined or re-purposed terms (n-lemma, energy differential, fitted reference surface, term versus cell, frontier). The "Not" column carries the distinctions the story relies on: the surface is not the Pareto boundary, a term is not a set of designs, and the energy differential is not a physical energy. | — | `returns/appendix-a.md` |
| `tab-A-register` | appendix-table | appendix-a | the main text points to it (yes: Section 3 "Appendix A is the full register of symbols and terms", and the Section 1 list of appendices). A reader wanting the full version of the notation would look for it (yes: the meaning of any symbol or term, and what it is not). Verdict: advances, as the one full glossary of the paper's vocabulary. Caveat: a few rows are not needed by the story, such as the ternary plot, share, region, MoE, MoP and launch cost. Those serve the case study and could be judged separately. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-a.md` |
| `appendix-b` | appendix | — | For each of the 19 results behind the paper's theorems, it gives the statement, its file, and the proof as numbered steps. | Main results items 1 to 4, through the line "Main results (Section 6; each has hypotheses, a sketch and a script)". | advances | The story says each main result has a script. This is the only unit that shows those scripts step by step against the proof's prose, and it holds the axiom ledger entries each step uses. | — | `returns/appendix-b.md` |
| `tab-B-how-to-read` | appendix-table | appendix-b | main text points to it: no (no pointer names this part). Would a reader wanting the full version look for it: yes, to learn how to read a step, its address and its three kinds. Verdict: advances. It is the key to the step tables. On the page it is prose and bullets, not a table. | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-b.md` |
| `tab-B-proof-map` | appendix-table | appendix-b | points to it: no, not by name, though the bare "Appendix B, L1" to "L17" pointers land on its rows. Would a reader look for it: yes, as an index of results with step counts by kind. Verdict: advances, as the index. It lists L-numbers only and never the paper's Theorem numbers. | pointed to: no, not by name; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-b.md` |
| `tab-B-proofs-fit` | appendix-table | appendix-b | (the per-step tables for L1 to L11): points to it: yes (Appendix B, L1 to L11; L3.9, L4.14 to L4.24, L5.25). Would a reader look for it: yes, for the full proofs of items 1 to 3 (homogeneity, convexity, the geometric program, elasticities, chart, Pareto efficiency). Verdict: advances. Long, so I skimmed it after L5. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-b.md` |
| `tab-B-proofs-solver` | appendix-table | appendix-b | (the per-step tables for L12 to L17): points to it: yes (Appendix B, L12 to L17, L17.12, L17.13, L17.19, B.2). Would a reader look for it: yes, for the full proofs of item 4 (the levels of guarantee, the stopping declaration and the soft-fit certificate). Verdict: advances. Skimmed. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-b.md` |
| `tab-B-checker` | appendix-table | appendix-b | points to it: no, though Section 10's "Appendix B gives one line of code to read each proof step against" is about what it checks. Would a reader look for it: yes, a reader who wants to rerun the check, for the commands and the record's hash. Verdict: advances, though thinly for the story. Its per-file rows largely repeat the ledger lines already given under each proof and the counts in `tab-B-proof-map`. Only the commands, the hash and the signed-symbol counts are new. | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-b.md` |
| `appendix-c` | appendix | — | It follows the cubesat model from its configuration space through evaluation, feasibility and conditioning to the table of metrics, and names the datasets and the planted example, so a reader can judge whether the case is a fair test and build a comparable one. | Main-results item 7 (on a cubesat model coupling power, mass and attitude control...), and the abstract's last sentence ("On a cubesat model coupling power, mass and attitude control, one term blends..."). | advances | The story rests on the cubesat case, and a reader who wants to judge it needs how the metrics were made from configurations; the main text keeps this to a short section and points here five times (C.1, C.4, C.7 twice, and the general sentence). No other unit that I can see from the list carries the construction. | — | `returns/appendix-c.md` |
| `tab-C-configuration_space` | appendix-table | appendix-c | points from main text: yes (C.1). Reader looks for it: yes, the design-variable ranges and covariate levels. advances (ranges the model view does not draw). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-evaluation` | appendix-table | appendix-c | points: no (only a general sentence on the evaluation). Reader looks for it: yes, the eight attributes, their units and direction, and the scenario constants. advances (the full version of "eight attributes"). | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-attribute_sources` | appendix-table | appendix-c | points: no. Reader looks for it: yes, which file produces each attribute and whether it is measured or computed (the black-box point). advances. | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-feasibility` | appendix-table | appendix-c | points: no. Reader looks for it: yes, how 1000 sampled designs became 706 (and 780 for stock). advances. | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-conditioning` | appendix-table | appendix-c | points: yes (Section 5, C.4). Reader looks for it: yes, orientation, raw ranges and log-spread for each attribute. advances. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-metric_table` | appendix-table | appendix-c | points: no. Reader looks for it: partly, the formula for m_j (carried in the text above the table); the five sample rows only show the shape. does not advance (the rows; the repository holds the data and the formula is in the prose). | pointed to: no; would look for it: partly | does not advance | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-metric_associations` | appendix-table | appendix-c | points: no from C (Section 9 points to D.3 for the same Spearman values). Reader looks for it: yes, for the strongest pair and the 0.99 test. repeats appendix-d (D.3, which the main text cites for these Spearman values; I have not read D.3, so this is from the pointer). The 28-pair listing may be its only full home, in which case it advances. | pointed to: no; would look for it: yes | repeats | — (in the Q7 line) | appendix-d (D.3) ("from the pointer") | `returns/appendix-c.md` |
| `tab-C-datasets` | appendix-table | appendix-c | points: no directly ("names each dataset" is general). Reader looks for it: yes, file, command, counts and hashes to rebuild the data. advances (it may overlap Appendix F's commands and rows, which I have not read). | pointed to: no, not directly; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `tab-C-planted_example` | appendix-table | appendix-c | points: yes (C.7, twice). Reader looks for it: yes, the generator arguments and planted exponents. advances (its arguments are also in the planted row of the datasets table, but the exponent matrix reads clearly here). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-c.md` |
| `appendix-d` | appendix | — | The full numerical record of the cubesat case and the planted-term checks: how the temperature was chosen, what the one- and three-term fits returned (exponents, contending sets, shares, termination status), how stable those answers are under changed settings and rounding-level jitter, the nondominated counts, the candidate and proposed designs, the PCA reading of the near-frontier chart and the four requirements read after the fit. | Main-results item 5 (PCA on the near-frontier chart, Appendix D.16), item 6 (the termination status read from the fit's record, D.8), item 7 (the cubesat terms, through the tables behind Section 9: D.3, D.4, D.15), and the Section 1 contribution sentence on the nondominated counts, 126 of 706 on 4 attributes and 659 on 8 (D.9, with their stability in D.11). | advances | Section 1 points into this appendix by section number three times (D.16 twice, D.11 once), and the nondominated counts it states are printed only here (D.9); main-results items 5 and 6 rest on D.16 and D.8, and no other unit in the list is described as carrying the case's full tables. Some of its tables are not needed by the story and two overlap each other (see Q7), but the appendix as a whole carries what the main text states briefly. | — | `returns/appendix-d.md` |
| `tab-D-temperature_selection` | appendix-table | appendix-d | pointed to: no. A reader would look for it: yes, for how tau = 38.1 and 45.7 were chosen by the 10 percent target fraction. Verdict: repeats, if Figure 4 (unit fig-tau-sweep) draws the same sweep, as its name suggests; otherwise it carries the selection rule's evidence that no pointer asks for. | pointed to: no; would look for it: yes | repeats ("repeats, if Figure 4 (unit fig-tau-sweep) draws the same sweep") | — (in the Q7 line) | fig-tau-sweep (conditional) | `returns/appendix-d.md` |
| `tab-D-k_diagnostics` | appendix-table | appendix-d | pointed to: no (only the general "tables: Appendix D" of Section 9; D.15 names it). A reader would look for it: yes, for the temperatures, mean slacks and term shares at K = 1, 2, 3 that Section 9 quotes. Verdict: advances (item 7; the mean slack figures quoted in Section 9 are here). | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-exponents_and_terms` | appendix-table | appendix-d | pointed to: yes (Section 9: term shares, the near-coincident pair, the Spearman figures). A reader would look for it: yes, for the exponents and contending sets of the one- and three-term fits. Verdict: advances (item 7 and the abstract's last sentence). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-regime_comparison` | appendix-table | appendix-d | pointed to: no. A reader would look for it: yes, for the side-by-side of the two regimes that Section 9 summarizes ("a 5-lemma and a 5-lemma sharing 3 metrics"). Verdict: repeats tab-D-exponents_and_terms in large part (the contending sets, and its Spearman paragraph is word for word the one under D.3); the pair tensions are its own, and may be drawn in Figure 9 (unit fig-regimes). | pointed to: no; would look for it: yes | repeats | — (in the Q7 line) | tab-D-exponents_and_terms ("in large part") | `returns/appendix-d.md` |
| `tab-D-sensitivity_variants` | appendix-table | appendix-d | pointed to: yes (Section 5 and Section 8: halving or doubling the target fraction leaves the contending set unchanged). A reader would look for it: yes, for that claim. Verdict: advances (backs the robustness claim the main text makes). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-refits_by_category` | appendix-table | appendix-d | pointed to: no. A reader would look for it: no; nothing in the story or the pointers asks what the fit returns per wheel class. Verdict: does not advance. | pointed to: no; would look for it: no | does not advance | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-candidate_designs` | appendix-table | appendix-d | pointed to: yes (Section 9, candidates scored against the K = 1 fit). A reader would look for it: yes, for the candidates' log V and rank. Verdict: advances only for Section 9; no sentence of the story needs it, so against the story: does not advance (it belongs as the main text's full version, which is its job). | pointed to: yes; would look for it: yes | "advances only for Section 9; ... against the story: does not advance" [does not advance] | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-termination_records` | appendix-table | appendix-d | pointed to: yes (Section 6, "each returned fit carries the levels it meets"; Section 8, the worked example's record). A reader would look for it: yes, for the termination statuses of item 6. Verdict: advances for item 6 and the planted 3-term record; but its cubesat rows repeat the last six columns of tab-D-k_diagnostics exactly. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-margin_reading` | appendix-table | appendix-d | pointed to: no (Section 6's "about 70 times smaller than the band" points to D.11, while the margin and band it compares are here). A reader would look for it: yes, for that comparison of the certified radius with the band. Verdict: advances (the only place the margin is set against the band and the median score gap). | pointed to: no; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-nondominated` | appendix-table | appendix-d | pointed to: no by section number (the Section 1 sentence points to D.11 for the stability, not to D.9). A reader would look for it: yes, for the 126 and 659 of 706 in Section 1. Verdict: advances (the contribution sentence's numbers; the main text should point to D.9). | pointed to: no, not by section number; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-propose_predict_check` | appendix-table | appendix-d | pointed to: yes (Section 9, proposals predicted then measured). A reader would look for it: yes, for the predicted and measured values. Verdict: does not advance against the story (no Section 1 item names propose-predict-check), though it is the full version of a Section 9 paragraph. | pointed to: yes; would look for it: yes | does not advance | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-stability` | appendix-table | appendix-d | pointed to: yes (Section 1, Section 6, Section 8, Section 9). A reader would look for it: yes, for which conclusions and digits hold over five regenerations. Verdict: advances (Section 1's parenthesis on the counts rests on it). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-conditioning_diagnostic` | appendix-table | appendix-d | pointed to: no. A reader would look for it: no; the story claims no uniqueness, and nothing asks for the smallest Hessian eigenvalue per term. Verdict: does not advance (it might back item 2's "uniqueness is not claimed", but nothing says so). | pointed to: no; would look for it: no | does not advance | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-own_rows_refit` | appendix-table | appendix-d | pointed to: yes (Section 6, the own-rows refit is ill-posed). A reader would look for it: yes, for that observation. Verdict: advances for item 4's several-term fit as Section 6 states it; against the story's sentences it is indirect. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-planted_recovery` | appendix-table | appendix-d | pointed to: yes (Section 8 and Section 9, 16 of 20 recovered). A reader would look for it: yes, for the recovery count and the four failures. Verdict: advances (the only evidence that the fit recovers a known answer, behind item 7's reading of terms). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-mean_slack_fixed` | appendix-table | appendix-d | pointed to: yes (Section 9, mean slack refitted at the K = 1 temperature). A reader would look for it: yes, for that comparison. Verdict: advances (item 7's claim that three terms fit better than one, compared at one temperature). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-pca_chain` | appendix-table | appendix-d | pointed to: yes (Section 1 twice, Section 9). A reader would look for it: yes, for the shares and loadings of the principal directions. Verdict: advances (main-results item 5 is this table). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-requirements_at_the_frontier` | appendix-table | appendix-d | pointed to: yes (Section 8, Section 10). A reader would look for it: yes, for the price of each requirement at the fitted frontier. Verdict: does not advance against the story (no sentence of the abstract or Section 1 mentions requirements), though it is the full version of Section 10's sentence. | pointed to: yes; would look for it: yes | does not advance | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `tab-D-design_sets_comparison` | appendix-table | appendix-d | pointed to: yes (D.17 as a whole, Section 8 and Section 10). A reader would look for it: only partly; the pointers describe pricing and exclusion counts, not three refits. Verdict: does not advance against the story; its second part (baseline, candidates and proposals across three fits) is the widest table here and no sentence asks for it. | pointed to: yes; would look for it: only partly | does not advance | — (in the Q7 line) | — | `returns/appendix-d.md` |
| `appendix-e` | appendix | — | It lists, for each of 18 places where the model and the data (or the proofs and the data) part, the assumption that bridges the gap, what cannot be proved, the numbers showing how sensitive the results are, and how to read the result in light of it. | Main-results item 6 ("Open: Q1 to Q4, four questions not established"), which the body ties to gaps G-14, G-11, G-12 and G-13. | advances | The story claims that the surface is not the Pareto boundary, that the several-term fit has limited guarantees, and that four questions are open. A reader who wants to know under what assumptions and with what sensitivity those statements hold has nowhere else to look, and the main text points here for exactly that (Sections 3, 6, 9 and 10). | — | `returns/appendix-e.md` |
| `tab-E-gaps` | appendix-table | appendix-e | main text points to it: yes (Section 3 "gaps ledger in Appendix E", Section 6 "Appendix E records them as gaps G-14, G-11, G-12 and G-13", Section 9 "gap G-9, Appendix E", Section 10 "Appendix E gives the ledger"). A reader wanting the full version would look for it: yes, for the assumptions, the unprovable parts and the sensitivity evidence behind the open questions and the Pareto-boundary caveat. Verdict: advances (the only carrier of the full gap-by-gap account). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-e.md` |
| `appendix-f` | appendix | — | It tells a reader how to regenerate the paper's numbers, tables and figures: the pinned software versions, the one environment where results reproduce exactly (and how other platforms differ only in last digits), the commands with what a pass looks like, and, for each table and figure, the call that makes it, what it reads and where it writes. | The Contribution sentence of Section 1, "Scaling up trade studies with a reproducible method", together with Section 1's demand that the justification be "recognized, reproducible, rigorous" and the line "each has hypotheses, a sketch and a script" introducing the main results. | advances | The story claims a reproducible method, and this is the only unit that says concretely how to reproduce it: the versions, the environment of record and the commands. Section 11 keeps only a few sentences and points here for exactly these four things, so no other unit carries them. | — | `returns/appendix-f.md` |
| `tab-F-toolchain` | appendix-table | appendix-f | pointed to, yes (Section 11: "Appendix F gives the pinned toolchain"). A reader wanting the full version would look for it, yes, for the exact versions behind "reproducible". Verdict: advances; the only place the versions and the build's commit and platform are stated. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-f.md` |
| `tab-F-commands` | appendix-table | appendix-f | pointed to, yes (Section 11: "the commands"). A reader would look for it, yes, for how to rerun the tests, the lemma scripts and the notebooks and what success looks like. Verdict: advances; it turns "each has a script" into commands with pass criteria. The notebook-execution row is long and dense in its pass column. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-f.md` |
| `tab-F-reproduction` | appendix-table | appendix-f | pointed to, yes (Section 11: "one row per item"). A reader would look for it, yes, to find which call produces a given table or figure. Verdict: advances, with the caveat that most of its 44 rows repeat the same "Reads" entry (the regimes' CSV directory), and it lists only three main-text figures, not all nine, so it is less complete than its job statement promises. | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-f.md` |
| `appendix-g` | appendix | — | It lists, family by family, the earlier methods this work resembles (Pareto, DEA, production frontiers, PCA, log-ratio analysis, geometric programming, MDAO, tradespace exploration and others), saying for each what it does, what is shared and what is different, and then reports how closely each citing sentence in the paper was checked against what the cited work says. | Item 5 and the abstract's "Like PCA, our method is unsupervised feature engineering; the two answer different questions" are served only in part (the PCA entry). | advances | The story invites the objection "this is just PCA, or Pareto, or DEA", and the register is the one place that answers it for each neighbour with a "why this is not just the neighbour" line; nothing else in the story carries that. The reading-pass half is checking of the paper's own citations rather than anything the story says, so the appendix advances on the strength of its first half. | — | `returns/appendix-g.md` |
| `tab-G-register` | appendix-table | appendix-g | main text points to it: yes (Section 2, "Appendix G is the larger register"). A reader wanting the full version would look for it: yes, for the fuller entries behind the family table and the "not just the neighbour" answers. Verdict: advances (the longer version of the family table). | pointed to: yes; would look for it: yes | advances | — (in the Q7 line) | — | `returns/appendix-g.md` |
| `tab-G-reading_pass_table` | appendix-table | appendix-g | main text points to it: no (Section 2 says only that Appendix G "lists" the sources reviewed). A reader wanting the full version would look for it: only a reader who doubts a citation, to see what was read and how a sentence was changed; not for anything in the story. Verdict: does not advance (a record of checking, not something the story needs). | pointed to: no; would look for it: only a reader who doubts a citation | does not advance | — (in the Q7 line) | — | `returns/appendix-g.md` |
| `docs-index` | docs-page | — | It says what the package does with a table of evaluated designs (fits a posynomial frontier, then reports contending metrics, each design's position against the fitted reference surface, and gaps), places it as a scikit-learn estimator beside PCA, and points to where in the docs to start. | This page is the docs Home page itself, so it is one half of the story. | advances | The root page promises a documentation entry point for a user of the package, and this page is that entry point; no other unit gives the docs' one-paragraph statement of what the package does plus the map of the docs. It is identical to the Home page of the story, which is expected, since it is that page. | — | `returns/docs-index.md` |
| `docs-getting-started` | docs-page | — | It shows how to install the package from source and run a first fit on a synthetic table of 300 designs and 3 metrics, then explains the report (contending set, exponents, elasticities) and the other fitted outputs (score_samples, transform, inverse_transform), and points to the user guide for real data. | Home page: "Getting started: install from source and run a first fit." Root page: "the documentation shows how to use the package ... a first fit" and "Install from source". | advances | The Home page names this page for exactly two jobs, install from source and a first fit, and the root page promises "a first fit" in its documentation card. No other listed unit carries an install-and-run walkthrough with a worked output; the User guide pages start at conditioning and fitting, which this page hands off to. | — | `returns/docs-getting-started.md` |
| `docsfig-first-fit` | docs-figure | docs-getting-started | On two metrics the fitted frontier is a straight line in the log plane along the outer edge of the designs, with a thin band of near-frontier designs just under it. | Home page: "where each design sits relative to the fitted reference surface" (and, for the page, "Getting started: install from source and run a first fit"). | advances | The Home page promises that the package tells you where each design sits relative to the fitted reference surface, and this is the first and only place in the getting-started path where a user sees that picture for their first fit: a frontier on the edge of the data, not through it. Other figures (the root page's, and the log-plane figure in the user guide's Chart page, which I have not read) may carry a similar picture, but none of them sits on the page where a new user runs the first fit and needs to see what "frontier" means for that fit. | — | `returns/docsfig-first-fit.md` |
| `docs-user-guide-overview` | docs-page | — | The page tells a practitioner what the package does with a table of evaluated designs (finds the weights of the contending metrics and a score V against a fitted reference surface), where the package sits in a five-stage study, and what the fit returns. | Home: "It then tells you which metrics contend, with what elasticity, where each design sits relative to the fitted reference surface, and where the table has gaps." Also Home: "User guide: one page per task, from conditioning your attributes to reading what the fit reports." | advances | The Home sentence listing what the package tells you is expanded here in a practitioner's terms (weights, elasticities, energy differential, white space, stopping record), and the five-stage pipeline showing which stages the package covers appears nowhere in the story. It overlaps with the "Theory in brief" page on the weights and V, but this page frames it as use, not model. | — | `returns/docs-user-guide-overview.md` |
| `docs-user-guide-conditioning` | docs-page | — | How to turn raw attributes (kilograms, dollars, error rates, some smaller-is-better) into the strictly positive, larger-is-better metrics the fit needs, using LogAffinePreconditioner (orientation, shift, reference point, scaler), how to check the result, and how to read the fitted surface back in the original units with frontier_in_original_units. | Home: "User guide: one page per task, from conditioning your attributes to reading what the fit reports", together with the Home page's condition on the input, "each scored on several metrics where larger is better". | advances | Both the Home page and the root page name conditioning as the first task of the user guide, and the Home page's promise depends on the reader having larger-is-better metrics, which a practitioner with a raw table does not have. This page is the one that says how to get them, and nothing in the unit list other than this page is named for that task. | — | `returns/docs-user-guide-conditioning.md` |
| `docs-user-guide-fitting` | docs-page | — | The page shows how to fit the frontier model with HyperbolicTradeSpace: one term, how to pick the temperature tau, several terms and their options, and how to choose K, tau and the band, with the attributes to read after a fit. | Home page: "User guide: one page per task, from conditioning your attributes to reading what the fit reports." Also "fits a frontier model in the posynomial invariant form: a sum of monomial terms". | advances | The Home page promises one page per task, and fitting is the task between conditioning and reading the report. The page gives the fit call, the attributes to read, and the choices of tau and K that a practitioner has to make. | — | `returns/docs-user-guide-fitting.md` |
| `docsfig-three-terms` | docs-figure | docs-user-guide-fitting | With several terms, the fitted frontier of two metrics is a bent line in log space, straight within each term's region, with the designs lying below it. | The Home page: "a sum of monomial terms, where a monomial term ... is one trade-off." | advances | It is the only picture on the Fitting page, and the only one I was given in the docs, of what several terms do to the frontier: the bend, where the trade-off rate changes from region to region, which is the reason the page gives for choosing K > 1, and it is the output of the plot_log_plane call printed just above it. It advances weakly, because it does not show what its caption and alt text promise: I count two pieces, not three; the term lines are not drawn separately; and the band in the legend and alt text cannot be seen. | — | `returns/docsfig-three-terms.md` |
| `docs-user-guide-tensions` | docs-page | — | The page shows how to call `tension_report` and read each field of what it returns (contending set and n-lemma, participation and elasticities, near-frontier association, tension directions, the K > 1 case), with a worked example where a one-term fit hides a cap and a slope, and a closing statement of what a report cannot say. | Home page: "It then tells you which metrics contend, with what elasticity, where each design sits relative to the fitted reference surface, and where the table has gaps" and the "User guide: one page per task, from conditioning your attributes to reading what the fit reports." Root page: "a guide per task from conditioning your attributes to reading a tension report." | advances | The Home page promises that the package tells you which metrics contend and with what elasticity, and the root page names "reading a tension report" as the end of the guide. This page is the only one in the list of units that explains how to read the report's fields (contending set, elasticities, association, directions). | — | `returns/docs-user-guide-tensions.md` |
| `docsfig-tension-report` | docs-figure | docs-user-guide-tensions | On the page's three-metric example, the tension report finds all three metrics contending, with every pair negatively associated near the frontier, and this is what plot_tensions draws. | Home page: "It then tells you which metrics contend, with what elasticity"; root page: "a guide per task from conditioning your attributes to reading a tension report". | advances | The Home page promises the package tells you which metrics contend, and the root page promises a guide to reading a tension report; this figure is the one place that shows the user the plot_tensions output for the call they have just been given, so they know what to look for in their own report. The case-study figure on Examples (docsfig-adcs-tensions) may show a tension report too, but on the cubesat table, not on the minimal code the guide runs, so it does not carry this. | — | `returns/docsfig-tension-report.md` |
| `docs-user-guide-chart` | docs-page | — | The page shows how to turn a fitted model's output into a chart (position coordinates plus log V), how to read log V and find holes in the table, and which plots draw these. | Home page: "where each design sits relative to the fitted reference surface, and where the table has gaps." Also the Home "User guide: one page per task... reading what the fit reports." Root page: "a guide per task." | advances | The Home page promises two things the page delivers: where each design sits relative to the reference surface (log V, improvement factors) and where the table has gaps (holes). I cannot tell from the story that another unit carries the chart coordinates, the hole finder or the plot list, though I have not read the other units. | — | `returns/docs-user-guide-chart.md` |
| `docsfig-log-plane` | docs-figure | docs-user-guide-chart | With two metrics, a one-term fitted frontier is a straight line in log coordinates that bounds the designs from above, and most designs sit just inside it. | Home page: "where each design sits relative to the fitted reference surface". | advances | The Home page promises to show where each design sits relative to the fitted reference surface. On this page, this figure is the only picture of a design's offset (log V) from the surface in the metrics themselves, before the chart coordinates are taken. | — | `returns/docsfig-log-plane.md` |
| `docsfig-chart-holes` | docs-figure | docs-user-guide-chart | That the hole finder's output is a set of grid squares overlaid on the position-coordinate scatter, and that on this sample they sit at the rim because there is no interior gap. | Home page: "where the table has gaps". | does not advance | The sentence the figure serves (gaps) needs a picture of a gap, and this one shows none; its own caption says so. The rim squares are the boundary effect of the grid, which is not something a user needs in order to use find_holes, and the one sentence in Q5 (c) carries all of it. | — | `returns/docsfig-chart-holes.md` |
| `docs-user-guide-prediction` | docs-page | — | It shows how to use `TradeSpaceRegressor` to predict where a configuration that has not been evaluated would fall: its metrics, its chart coordinates and its novelty (V - 1) relative to the fitted reference surface. | Home page: "The workflow serves design optimization and configuration management: choosing among configurations, and tracking a configuration's evaluation against the fitted reference surface." It also serves the Home page's "User guide: one page per task", with prediction as one of those tasks. | advances | The Home page promises a workflow for choosing among configurations, and only this page goes from configuration to the trade space. Every other part of the story starts from a table of metrics that has already been evaluated. | — | `returns/docs-user-guide-prediction.md` |
| `docs-user-guide-termination` | docs-page | — | Every fit records how it stopped in `termination_` (and `conditioning_`): a status from a fixed list, built on three levels of assurance (descent, stationarity, conditional local optimality), with a field list and a note that a "certified" status covers only the local optimum of the objective, not held-out validity. | Home: "reading what the fit reports" (User guide: one page per task). | advances | The Home page promises a guide "to reading what the fit reports", and the termination record is part of what a fit reports. No Home or root sentence mentions certification, statuses or how a fit stopped, so the page is the only place that carries it, though the story only needs it in a thin way. | — | `returns/docs-user-guide-termination.md` |
| `docs-user-guide-limitations` | docs-page | — | It lists the ways a fit can mislead a user (conditioning, log-convexity, one term per tension, sample versus Pareto boundary, temperature, small samples, local optima, novelty, prediction), and for several of them says what to do about it. | Root page, Why: "it has to show its reasoning, say where the data do not reach". | advances | The root page sets a bar a trustworthy model-based method has to clear, and saying where the method does not reach is part of that bar. For a reader of the documentation, this is the one page that gathers those limits for a practitioner. | — | `returns/docs-user-guide-limitations.md` |
| `docs-api` | docs-page | — | The page lists the package's public names (classes, functions, submodule contents, two constants) with a short phrase each saying what it is for, and points to the API reference and user guide for detail. | Home page: "API and API reference: the public names and their docstrings." The root page's "Package" block ("API reference →") points the same way. | advances | The Home page promises a page of public names, and the API reference alone is generated docstrings with no grouping by purpose. This page is the only one that gives a first-time user a map: which name transforms, which fits, which reports, which plots. | — | `returns/docs-api.md` |
| `docs-examples` | docs-page | — | It shows the package run end to end on one real table (the cubesat study): what the fit found (contending sets, term shares, mean slack, regime dependence), how to draw it with a few lines of code, how requirements are read after the fit, a ternary plot on synthetic data, and the command that reruns the study. | Home page: "Examples: a cubesat trade study across power, mass and attitude control." It also serves the Home page's "It then tells you which metrics contend, with what elasticity, where each design sits ... and where the table has gaps", and the root page's "let the analysis be rerun" (the Run it section). | advances | The Home page promises a cubesat trade study as the docs' worked example, and this is the only docs page that carries it; a practitioner gets to see what the fit reports on a real table and how to reproduce it. The paper's case sections (sect-case-analysis, appendix-d) cover the same study for the paper's reader, but the docs story needs a usage-shaped version with code, and only this page gives it. | — | `returns/docs-examples.md` |
| `docsfig-adcs-tensions` | docs-figure | docs-examples | The pairwise tensions among the cubesat's eight metrics near the frontier, with the five that the one-term fit weights marked. | Home: "It then tells you which metrics contend, with what elasticity" (the contending part, not the elasticity). | repeats | The figure is the worked-case instance of the tension report; the page text already names the five metrics, and a figure of the same kind of report sits on the tension guide page. What the example adds (the real values) is not discussed in the page text, so a reader does not know what to take from them. | docsfig-tension-report (Figure 3 on 'User guide: Tensions') | `returns/docsfig-adcs-tensions.md` |
| `docsfig-adcs-coordinates` | docs-figure | docs-examples | It shows the cubesat's feasible designs spread over the first two of seven chart coordinates, with the near-frontier designs ringed, as an example of what plot_frontier_coordinates draws. | None directly. | does not advance | The caption disowns the two things a reader would want from it (the coordinates mean nothing alone; it does not show the frontier), and what is left, "coverage" in two of seven coordinates, does not let me say where the table has gaps or where a design sits relative to the surface. Its remaining job is to show that the plotting call runs and what its output looks like, which the code block above it already tells me. | — | `returns/docsfig-adcs-coordinates.md` |
| `docsfig-ternary-planted` | docs-figure | docs-examples | It shows, for three metrics, a fitted three-term frontier as a partition of the triangle of metric shares into regions where each term is largest, with each term's best point and lines of equal V around it. | Partly the Home sentence "a sum of monomial terms, where a monomial term ... is one trade-off", and "which metrics contend". | does not advance | The cubesat example the Home page promises has eight metrics, and the page itself says "eight metrics do not separate in three, so none is drawn for the cubesat", so this figure belongs to a different (synthetic) table that the story never mentions. The idea that different trades dominate in different places is already carried by the root page's first figure and the User guide's three-terms figure. | — | `returns/docsfig-ternary-planted.md` |
| `docs-theory` | docs-page | — | It states the model in definitions: a weighted geometric mean V of the metrics (one term, K terms as a posynomial), the surface V = 1 as the fitted reference surface (kept apart from the supporting envelope and the Pareto boundary), the chart coordinates (Z, log V), the constant elasticities and the n-lemma, and the model's assumptions. | Home page: "Theory in brief: the model on one page." Also the root page's Documentation card, "the model in brief", and the Home page's "it fits a frontier model in the posynomial invariant form ... which metrics contend, with what elasticity". | advances | The Home page promises one page that states the model, and this is that page: it defines V, the fitted reference surface, the chart, the elasticity formula and the n-lemma in one place, which the task pages of the user guide lean on. No other unit in the documentation is named as carrying the model on one page; the paper's Definitions section carries it for paper readers, but the docs story names this page for the package user. | — | `returns/docs-theory.md` |
| `docs-further-reading` | docs-page | — | It lists twelve sources the method builds on, grouped by what a reader may want from each (using the package, geometric programming, charts and neighbouring methods), each with a one-line note on its role. | Home page: "Further reading: the sources the method builds on." It is the last item under "Where to start". | advances | The Home page promises a page of sources the method builds on, and only this page delivers it. The paper's Works cited and Appendix G (register of prior art) may hold overlapping references, but I have not read them. | — | `returns/docs-further-reading.md` |
| `root-index` | root | — | why a trade-study method has to show its reasoning, say where the data stop and be rerunnable; what this method is (it explains tensions where PCA explains variance, it is a scikit-learn estimator); then it sends the reader to one of three places: the paper, the docs or the package. | "The project page links the paper, ... these docs and the package." | advances | The Home page's closing sentence needs a project page that links the paper, the docs and the package, and only the root page does that. The "Why" section (what a decision-maker needs before trusting a model-based method) is also not carried on Home. | — | `returns/root-readme.md` |
| `readme` | readme | — | a one-paragraph technical description of the method (a monomial frontier V(m) = Π m_j^{w_j}, a coordinate chart, a scikit-learn estimator, SymPy derivations, an ADCS case), then a contributor's status line, a `uv sync` / `uv run pytest` quickstart and the repository layout keyed to work packages. | none directly. | repeats | Its description says what Home's first paragraph and the root page's opening sentence already say, in different and harder words. What it adds (the status line pointing to `work-packages/`, the layout with "WP1", "WP4, WP7", "site in WP8") is for someone working on the repository, and no sentence of the story needs it. | docs-index (Home page, first paragraph) and the root page (its opening sentence and its "What" section's "scikit-learn-compatible estimator") | `returns/root-readme.md` |

### The root page's two images (inside unit `root-index`)

| unit_id | kind | parent | reader's sentence (Q1) | story sentence served (Q2) | verdict | reason (Q3) | named unit if repeats (Q4) | return file |
|---|---|---|---|---|---|---|---|---|
| `root-index-fig-why-regions` | docs-figure | root-index | The trade-off that binds between three metrics differs by region of the design space, and the evaluated designs fall into several of those regions. | Home page: "It then tells you which metrics contend, with what elasticity, where each design sits". | advances | The Home page promises that the package tells you which metrics contend and where each design sits, and the root page says the n-lemma names which metrics compete on one part of the trade space; this figure is the only unit on the root page that shows contention changing by region. The second root figure (root-index-fig-figure1) shows the three fitted terms and an energy differential, not which metrics trade against which by region. | — | `returns/root-index-fig-why-regions.md` |
| `root-index-fig-figure1` | docs-figure | root-index | That a fitted frontier made of three terms can be redrawn from curved (metric space) to straight (log space) to flat (chart), and that each design's distance to it is the same step in all three. | Home page: "where each design sits relative to the fitted reference surface"; and "learns the shape of a design trade space from evaluated designs" / "a sum of monomial terms". | advances | The root page has one other figure, which (by its caption) is about which metric a design favours; this one is the only picture on the root page of the fitted model itself and of the step from a design to it, which the Home page names as one of the things the method tells you. The reason is thin, though: the root page text never uses the figure's terms, and the paragraph above it is about something else, so the figure carries a sentence of the Home page, not of the root page. | — | `returns/root-index-fig-figure1.md` |

## Verdicts by kind

Counts of the table's 122 rows. "split" is Definition 7, whose reader gave reach and share separate verdicts.
`tab-D-candidate_designs` is counted under "does not advance" (its reader's verdict against the story); the three
conditional or qualified "repeats" of Appendix C and D tables are counted under "repeats". The root page's two images
(both "advances") are not counted here.

| kind | advances | repeats | does not advance | stuck | split | not returned | total |
|---|---|---|---|---|---|---|---|
| section | 11 | 1 | 2 | 0 | 0 | 0 | 14 |
| statement | 21 | 0 | 5 | 0 | 1 | 0 | 27 |
| float | 6 | 1 | 3 | 0 | 0 | 0 | 10 |
| appendix | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| appendix-table | 29 | 3 | 8 | 0 | 0 | 0 | 40 |
| docs-page | 14 | 0 | 0 | 0 | 0 | 0 | 14 |
| docs-figure | 4 | 1 | 3 | 0 | 0 | 0 | 8 |
| root | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| readme | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| all | 93 | 7 | 21 | 0 | 1 | 0 | 122 |

## Figures: image first (R-3)

The 20 figure and table readers (9 paper figures, the paper table, 8 docs figures, the 2 root-page images), each
return read in file order: does Q5 (a) come before Q5 (b) and (c), all three before Q1?

| reader | template | Q5 (a) before (b) and (c), and before Q1 |
|---|---|---|
| `tab-families` | paper-table | yes |
| `fig-nlemma` | paper-figure | yes |
| `fig-assembly-view` | paper-figure | yes |
| `fig-behavioural-view` | paper-figure | yes |
| `fig-tau-sweep` | paper-figure | yes |
| `fig-planes-k1` | paper-figure | yes |
| `fig-planes-k3` | paper-figure | yes |
| `fig-chart-level` | paper-figure | yes |
| `fig-tensions-k3` | paper-figure | yes |
| `fig-regimes` | paper-figure | yes |
| `docsfig-first-fit` | docs-figure | yes |
| `docsfig-three-terms` | docs-figure | yes |
| `docsfig-tension-report` | docs-figure | yes |
| `docsfig-log-plane` | docs-figure | yes |
| `docsfig-chart-holes` | docs-figure | yes |
| `docsfig-adcs-tensions` | docs-figure | yes |
| `docsfig-adcs-coordinates` | docs-figure | yes |
| `docsfig-ternary-planted` | docs-figure | yes |
| `root-index-fig-why-regions` | docs-figure | yes |
| `root-index-fig-figure1` | docs-figure | yes |

Twenty of twenty: yes.

## Q9: read twice, still unplaced

Every reader's Q9, verbatim, by reader, in `readers.tsv` order. This is the readers' stuck list; a statement or table
inside a section or appendix appears under its section's or appendix's reader.

### `sect-problem`

- "the process turning much data into little must be recognized, reproducible, rigorous": clear enough, but "recognized" is vague.
- "a weighted geometric mean of the metrics that doubles when every metric doubles" (item 1): invariant value and V are used before definition; read from the story alone, V in item 3 ("a maximizer of V") is undefined here.
- "three levels of guarantee and a stopping declaration" (item 4): not explained in this section.
- "Q1 to Q4, four questions not established" (item 6): the questions are not stated here.
- "the near-frontier chart" (item 5): not defined here.

### `sect-prior-art`

- "a band, not extreme units" (Table 1, DEA row) and "a band of near-frontier designs and an effective sample size": the band and the effective sample size are not defined in the story or before this point.
- "A smooth soft maximum over a simplex-constrained geometric mean": which simplex. The story does not say the exponents lie on a simplex.
- "We solve one convex program and K refits, and return coordinates with a pull-back to attribute units": what a refit and a "pull-back" are.
- "the soft maximum is an entropic risk functional Föllmer, n.d.": an undated citation, and the link to the soft maximum is asserted without explanation.
- The Pareto row's "Shares" cell, "A maximizer of a weighted geometric mean with positive exponents is Pareto-efficient": this is the paper's own Theorem 9, so it is unclear what Pareto methods share here.
- "Open. Which part of the Pareto boundary the terms reach is our reading": an "Open." label inside a prior-art paragraph. Is this one of Q1 to Q4 from item 6 or something else?
- "Attributes in place of inputs" (production-function row) against "Our metrics are larger-is-better ... in place of inputs, outputs": attributes or metrics?
- "the feature-engineering kin of the direction in Section 10": which direction (the kernel extension?).
- "the hyperbolic graph measure of efficiency of Färe, Grosskopf and Lovell": useful as a disambiguation, but the source is not in Table 1.

### `tab-families`

- "global exponents per term, not per-unit weights; a band, not extreme units" (DEA row, Differs): I can place the first half after the prose, not before it; "a band" is not defined at that point.
- "A smooth soft maximum over a simplex-constrained geometric mean" (frontier row, Differs): the words are all defined later; unreadable at the point of the table.
- "the feature-engineering kin of the kernel direction" (kernel PCA row, Shares): "the kernel direction" points to Section 10, which I have not read.
- "The weights are trade-off rates" (decision analysis row, Shares): unclear whose weights and in what sense they are shared with that family.
- "Attributes in place of inputs" (production row, Differs): too terse to say what the difference is.
- The Production row's "Produces" cell ("The Cobb-Douglas production form, and the Shephard distance function") reads as the thing the family is, not what it produces.

### `sect-notation`

- "$V=1$ at finite $\tau$" and "the $\tau=\infty$ fit": $\tau$ is used here (and in A3, "$\tau>0$") without being said what it is; I take it to be a softness or temperature of the fit, but the section does not say so.
- "A6: $\kappa>0$": $\kappa$ appears nowhere else in what I was given; I cannot say what it is.
- "A7: the chart's basis is orthonormal and sums to zero": the chart's basis is not introduced in this section, so I could not tell what the assumption is about.
- "where the posynomial equals one" next to "$V=1$": the story describes $V$ as a weighted geometric mean (a monomial), while here the surface is where "the posynomial" equals one; I could not tell whether $V$ is the posynomial or one term of it when there are several terms.
- "Three objects carry the word frontier": the definition then names them without using the word "frontier" for any of them, so it is unclear which of the three the paper means elsewhere when it says "frontier" (Section 1 speaks of the "near-frontier chart").
- "A2: exponents lie on the simplex" and "A6: ... each term's exponents lie on the simplex": I could not tell whether A6 is the several-term version of A2 or a separate condition.
- "a quilt of trade-offs ... meeting its neighbours at the ridges": the picture is clear as a metaphor, but "ridges" is not tied to anything defined.

### `sect-definitions`

- "Term aggregation: the formula is the sum; the package's mean subtracts the constant (log K)/kappa" (a package detail inside a definition; its job is unclear for the story).
- "the term refit f_k of Section 6 on the cell's rows alone" (points forward to a later section I have not read).
- "the title's word" (the title shown in the story does not contain "hyperbolic" in a way I could tie to this sentence; the title does say Hyperbolic).
- Definition 1 is cited by the story as the home of "table and reading are views", but it is not in this section; the numbering starts at Definition 2.
- "participation threshold (Section 5)" (defined elsewhere, not placeable here).

### `fig-nlemma`

- "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)" against the caption's "the weight the three carry is printed": one weight is described, three are printed; I could not place what each 1.00 refers to.
- "drawn beside the planted one (open ring)" with term 2 sitting off its ring: neither the caption nor the text says whether that gap is a recovery error, an effect of the fit temperature, or within tolerance.
- "its exponent vector at the fit temperature is a point of the triangle" against Definition 6, where "the contending set ... is the support ... of the exact-maximum ($\tau=\infty$) fit to the term's cell": which fit's vector the dot is, and why the face read off it names the n-lemma, I could not reconcile on two readings.
- "(corner: it binds alone)": what a one-metric "n-lemma" means as a tension is not said, and the figure has no term there.

### `sect-methods`

- "R1: the balanced point ... lies in the relative interior of a facet of the supporting envelope with positive normal": I could not place facet, supporting envelope or subgradient choice at this point; they are used before they are defined.
- "R2: the assignment margin gamma": I could not say where it is used in this section or why it is needed.
- "never the unnormalized log-sum-exp ... (Theorem 4)": the claim reads clearly, but the reader is sent to a theorem not seen here.
- "membership: Definition 6" and the thresholds "10^-3" and "10^-12": I could not say what participation is used for.
- "(Theorem 8)" cited for the kappa bound, while the story's item 3 cites Theorem 8 for the monomial extension: I could not tell whether these are the same statement.
- "$V_K$ is a generalized posynomial, the term maximum at the default kappa = infinity": kappa is not introduced in the section.

### `sect-results`

- "Refitting a term on its own rows alone ... is ill-posed" next to Theorem 11's hypothesis "step B, the refit of each term on its cell": I could not tell whether step B is the ill-posed plain fit or $f_k$, or what "$f_k$ itself on the cell's rows" means when the text says "the refit of record is $f_k$ over all rows".
- "R1 is a statement about the exact-maximum ($\tau=\infty$) geometry; it does not imply that the finite-$\tau$ minimizer is interior", next to the hypothesis "R1's relation at the fit temperature". Read together, these leave unclear whether the facet-normal reading holds at the fit's $\tau$.
- "at $K>1$, $\kappa=\infty$, through an active term" (Theorem 9): too compressed to tell what is claimed at $K>1$.
- "for a soft fit ... stationary that the term gaps hold and the curvature is not positive": the term gaps are defined for the sharp, per-term $f_k$, and I could not place what they mean for a soft fit.
- Main result 3, "With one term the posynomial extension is the monomial": the section gives this as the formula $\Phi_1=w_1\cdot u-\beta_1$ inside Theorem 8. The sentence is fine, but at first I could not find where it is stated.

### `sect-search`

- "the supporting envelope stops moving beyond the noise band": the envelope is not defined here.
- "a diffusion with drift along the tangent spaces": an analogy with no support in the section.
- "Ascent may reach only the log-convex part of the Pareto boundary (our reading)": claimed without a lemma; unclear how it relates to the "monotonicity" item in Section 1 (Section 1 says "monotonicity of the search", this section says "outward monotonicity").

### `sect-case-construction`

- "the launch cost and the pointing error are MoEs, the other seven traded metrics MoPs": that makes nine, but the section says there are eight traded metrics, and the Figure 3 caption calls the launch cost "derived, not traded". I could not tell which seven metrics are meant, or whether the launch cost is counted among the traded metrics.
- "the effective sample size is 23.1 designs" and then "the exponents at the fit temperature rest on about 25 of the 706 designs": I could not tell why the number changes from 23.1 to "about 25".
- "Figure 1 drew a three-metric table; the case plants its own" and the paragraph after it (the 900-row worked example, the 20 tables of 400 rows): I could not tell what the planted tables have to do with the cubesat case built in this section.
- "so at $K=1$ the fit's objective of equation (2) ... is that of equation (1)": equations (1) and (2) are not in this section. I could not tell why the case needs this, beyond the fact that the conditioning centres the log-metrics.
- "Section 12 says how to go beyond that": I could not tell what "beyond" illustrative hardware values would involve.

### `fig-assembly-view`

- "panelPlus, panelMinus" in the SolarPanel box: not explained anywhere I read.
- "(wheel)", "(tracker)", "(bus)", "(imu)" in lowercase under part names: presumably the usage names in the model, not explained.
- "«part def»" and "«abstract»": modelling-language notation not explained in the caption or text.
- The caption says "open arrow" while the image draws hollow triangles: a small mismatch, not a barrier.

### `fig-behavioural-view`

- "returns 7 of 8 metrics ... settling time (not returned)" (purple box) against the caption's "the analysis passes on" the control effort. Where the settling time enters the table if the analysis does not return it, and why one measured value is passed on and the other is not, I could not place.
- "Every traded metric is read by a requirement" against "The fit ignores the four" threshold requirements and "Feasibility removes designs that do not settle, saturate the momentum budget or discharge the battery too deeply". I could not tell which boxes in the figure are feasibility filters, which are the four threshold requirements, and which are neither.
- "the launch cost and the pointing error are MoEs, the other seven traded metrics MoPs": launch cost is not traded, so "the other seven" took a second reading to reconcile with eight traded metrics.

### `fig-tau-sweep`

- "white rows last in the table's order" (caption): I could not tell what "the table's order" is; the three white rows appear in an order (control effort, power margin, peak slew power) that I could not trace to anything on the page.
- "the band 1/tau is 0.0262" (text under the figure): what the band is, and why it is 1/tau, is not explained on this page.
- "within 0.01 of the target (a convention, Section 5)": why 0.1 is the target and why within 0.01 is the rule is deferred to Section 5, which I was not given.
- "Figure 4 shows how the temperature is selected. Where the answer must be known, we plant it": the jump from selecting the temperature to planting an answer has no link on the page; I could not see how the one follows from the other.
- "the exponents at the fit temperature rest on about 25 of the 706 designs" against the figure's and the text's n_eff of 23 (23.1): two numbers for the same quantity on one page.

### `sect-case-analysis`

- "On the 20 planted tables the fit recovers all three terms to within 0.05 in 16": the section never says what the planted tables are or what "within 0.05" measures. The story does not mention a known-answer check.
- "Two regimes ... separates the problem's contribution from the gains'": no story sentence asks for a regime comparison, so I cannot tell which claim it supports.
- "energy balance and power margin, one in each regime's own part, are the strongest-associated pair of traded metrics": I could not work out what "each regime's own part" refers to.
- "the figures of this section and the association reading use the K = 1 band at every K (gap G-9, Appendix E)": I could not tell why the K = 1 band is used at every K, or what it costs.
- "refitted at the K = 1 temperature it falls to 0.13 and 0.09": "it" seems to be the mean slack at K = 2 and K = 3, but the sentence does not say so.
- "Candidates" and "Propose, predict, check": the story has no sentence about candidates, regressors or proposals. I could not tell what these paragraphs contribute to the case's result, apart from the remark that the proposals fail depth of discharge.
- "a tenth of all designs lie above V = 1, by the fit's convention" (Figure 5 caption): I could not tell whether this is a setting the analyst chooses or a property of the fit.

### `fig-planes-k1`

- "the line is the surface to within 0.1 in log V". The quantity "log V" is not defined on the figure, and the legend's "(within 0.1 in log V)" is not placed by the figure alone.
- "at the balanced point" (Section 9, "one tension at the balanced point"). I could not tell what point this is.
- "primary regime". The figure caption names it, but the reader has not met it in the story slice.
- "a tenth of all designs lie above V = 1, by the fit's convention". The figure does not show V, so the dark points beyond the line cannot be matched to this tenth.
- The axis label "inverse kg" next to "conditioned total mass". I could not place how conditioning gives inverse kg.

### `fig-planes-k3`

- "the median of the near-frontier designs in the term's cell (the designs the term scores highest)": what a term's cell is, and how a design is assigned to it, is given only in this parenthesis; I could not tell how many designs are in each cell or see them in the image.
- "No drawn pair is weighed by a second term": term 1's contending set includes pointing error, which is also term 3's drawn metric; I read this twice and could not tell whether "pair" means both metrics together, so whether the claim needs that reading.
- "the term's line in this slice" versus Figure 5's "the line is the surface in this slice": at K = 3 is each term's line the surface in that slice, or only that term's piece of it, which the surface lies above where another term dominates?
- "the figures of this section ... use the K = 1 band at every K (gap G-9, Appendix E)": I could not place what this changes in Figure 6 (the 0.1 dark/light threshold is stated in log V, not in bands).

### `fig-chart-level`

- "the K = 1 fit's band as at every K": why the K = 1 band is drawn on a K = 3 chart is explained only by a pointer to gap G-9 (Appendix E), which I was not given.
- "energy differential" is in the caption but the axis says "level"; I took them to be the same thing.
- "44% of it": I read it as the share of the spread along this direction, as the caption's pointer to Appendix D.16 suggests, but the figure does not say share of what.
- "to the right, better total mass and control effort; worse pointing error": it is not clear whether the direction is a trade or a cost, and the figure shows no sign of either.

### `fig-tensions-k3`

- "grey below the participation threshold": the threshold's value is not given on the page; I can only infer from term 3 that it lies above 0.02.
- Term 3's fifth outlined metric: on the image I cannot tell with confidence whether settling time's diagonal cell is outlined, and the section text does not list term 3's contending set.
- "the figures of this section and the association reading use the K = 1 band at every K (gap G-9)": I could not place how this band defines which designs count as near-frontier in each term's cell, or why it is the K = 1 band.
- "The term shares are 0.03, 0.24 and 0.72": not clear how a term share relates to the count of near-frontier designs in its cell (term 1 has 3).

### `fig-regimes`

- "5-lemma" in the panel titles (the story defines n-lemma; the K = 1 5-lemma is placed only on the page)
- "exact-maximum support" in the titles
- "the problem's contribution from the gains'" (page text, before the figure)
- the stock panel: energy balance w=0.02 not outlined, power margin outlined, without a mark on the figure saying they are a counted-as-one pair

### `sect-discussion`

- "Two of the three proposals are one configuration": I could not tell which proposals these are, who made them, or why it matters that two coincide. Neither proposals nor a proposer appears in the story.
- "the regressor places the energy differential of a proposal within its band (3 of 3)": the story never introduces a regressor or a proposer.
- "inside the band 0.094" and "meaningful relative to the band $1/\tau$": the band and $\tau$ are not defined in the story or in this section.
- "Proposition 3 and Corollary 1 for a sharp fit": the story never defines "sharp fit" as opposed to "soft". Corollary 1 is not among the story's listed results.
- "Why a frontier. An answer far from the frontier is hard to justify, and the analysis must rerun on empirical data to support configuration management.": the two halves seem unrelated, and I could not see how the second answers the heading.
- "A hole in the chart is an opportunity only where the trade space is log-convex around it": the story does not mention holes in the chart.

### `sect-reproducibility`

Nothing I could not place. "one row per item" refers to Appendix F, which I have not read.

### `sect-future`

- "Beyond one term, K > 1 is built": if K > 1 is already built, I cannot tell what the future work in this item is; the sentence states a present fact where the others state a gap.
- "beyond sharp weights with smoothing on request, a nonsmooth search on the tangent cones of the ridges, whose generalized gradient is the convex hull of the active normals": "sharp weights", "smoothing on request" and "ridges" are not defined in the story, and I cannot tell what object has the kinks or which search would tolerate them.
- "GGP-compatible kernels, the generalization the search motivates": I cannot tell how the search motivates kernels; the abstract presents kernels as already generalizing the method.
- "Beyond a log-convex envelope, the detection of dents and holes": the story does not say the surface is a log-convex envelope, or what a dent or hole would be.
- "how far above $V=1$ it is forecast to sit": the story defines the surface as where the invariant value equals one and names V only in item 3 ("a maximizer of V"); it does not say that V and the invariant value are the same quantity, so I could not be sure what "above V = 1" means here. The $V=1$ also appears as raw LaTeX source on the page, not rendered.

### `sect-process`

- "whose deterministic checks and named human approver are the verification mechanism this paper inherits": it is unclear what the inherited mechanism is, since Zargham, 2026 is not described here.
- "The derivations are machine-checked": I could not place which derivations, or by what tool.

### `sect-cited`

- "64." at the end of the list: a numbered entry with no content. It reads as a rendering or build defect (an empty or unresolved reference).
- "Föllmer, H. (n.d.). Entropic Risk Measures on Wiener Space. Unpublished notes": an undated, unpublished source with only a personal-page URL. I could not tell from this section which claim it backs or whether that URL counts as a stable source.
- Entry 63 (Zargham, 2026, document assurance): the story does not say which claim it supports. Its placement suggests it backs the process or verification framing rather than the method.

### `appendix-a`

- Rows with an empty Symbol and a leading "/" in the meaning cell (for example "conditioning", "cell"): the slash looks like a rendering artifact from a column shift, and I could not tell whether it is meant.
- "Defined in" entries such as "A4", "L9", "G-1", "R2", "I16": the codes are not explained on this page, so the reader cannot follow them without the other appendices.
- "level offset" and "energy differential" are both given the symbol log V with near-identical meanings; I could not place the difference.
- "frontier | not a defined object": clear in intent, but it sits oddly in a register of defined terms.

### `appendix-b`

- "per proof, in the paper's numbering": the appendix numbers results L1 to L17, while the story numbers Theorem 1 to Theorem 12, Lemma 1, Lemma 2 and Proposition 3. Nothing on this page maps Theorem n to Lk, except L14, which is named "Proposition 3". A reader starting from "Theorem 9" cannot tell which entry to open.
- The parts list says "The solver for K > 1 and its three levels of guarantee (L12 to L17)", but the heading reads "B.2 The several-term fit and its levels of guarantee". Two names for the same part.
- "L14. Proposition 3": unlike every other entry, the title gives no statement, so the proof map row says nothing about what is proved.
- Step kinds that do not match their prose. L1.8 is listed "by declared axiom A1", but its prose is about the simplex sum (A2). L5.10 is listed under A3 alone, but its prose cites "F5, A3".
- "Signed symbols declared as hypotheses" (the checker table: 5 for L11, 10 for L13): the term is not explained on the page. The checker text says only "no premise hides in a signed symbol".

### `appendix-c`

- "The association of every pair of traded metrics ... is the step that would find two metrics the data cannot tell apart": placed it in the end, but it sits in the middle of the metric-table section and the link to the formula above it is unclear.
- "cubesat-stock ... Kp 0.03011 ... 0.999" against declared 0.2 to 2: the stock regime's gain range is outside the declared range and the appendix does not say why here.
- "peak slew power ... m min 0.2554" equals design 0's value in the sample rows: no problem, but the repeated values (2.191, 3.591, 1.998) in that column look like ties and are not explained.

### `appendix-d`

- The "all jointly" rows of D.17's first table ("| / 40.8 % | 19 of 56 | | / | / | / | |"): the columns do not line up and the slashes are not explained.
- D.3, term 1: "3 of ten" near-frontier designs; "ten" is not defined anywhere I read.
- D.4 cells such as "settling time, total mass | -0.50 (-0.50)": what the number outside and the number in parentheses each are.
- D.8, the planted-3-term table with a second header row inside it ("Planted terms | Largest exponent deviation after matching terms"): two tables run together.
- D.2's "objective_" against D.15's "mean_slack_": D.15 says they differ at K = 1, but D.2 is described in D.15 and Section 9 as the mean slack.
- D.11: "685 quantities, of which 243 numbers move at all", while the second table lists nine; where the other 234 are printed.
- The n_eff of 23.1 (D.4) against Section 8's "about 25 of the 706 designs" (the pointers file): which one the main text uses.
- References to "gap G-17", "gap G-10", "L12" and "level 2": named, but not resolvable from this appendix.
- D.17's design-sets table, "three terms (share)" column: three cells per row, separated by the same bars as the columns.

### `appendix-e`

- "G-1 to G-17" in the opening description, while the table has 18 rows (G-18 is present); the count does not match.
- "step B" and "step D" (G-6, G-8, G-14): not defined on the page I read; only the main text could say.
- Codes such as "L11", "I7", "I8", "R2", "A5", "M3", "F12": used without a key in this appendix.
- "conditioning_" and "objective_" with a trailing underscore, read as fitted attributes but not explained here.
- "Mean slack ... $-\overline{\Phi}$" in G-18: the sentence "mean slack equal to $10^{-12}$" for two different boundaries took a second read.
- G-17: "74 of 685 quantities" not identical at printed precision: clear as a count, but I could not tell which quantities are meant.

### `appendix-f`

- "the ledger" (in "The repository keeps: ... the Dockerfile and the ledger"): which ledger is meant (the gaps ledger of Appendix E, or a proof ledger) is not said here.
- "the history layer carries the commit" and "a git bundle that paper/container/build.sh passes in": I can tell this is container mechanics, but not why a reader of the paper needs it.
- "every figure" in the Job line against F.4: Figures 1, 2, 3, 5, 6 and 7 of the main text have no row; I could not tell whether they are made elsewhere or simply omitted.

### `appendix-g`

- "(same sentence)" and "(same)" in the Sentence column: rows cannot be read alone.
- The empty "In the paper" column at the end of every reading-pass row.
- "accessible (own work)" and "listed for the supervisor, unchanged": a verdict outside the four defined and a reader of the paper would not know who "the supervisor" is.
- "lemma L11" and "Föllmer n.d." in the register: L11 is a pointer into another appendix that this appendix does not explain.
- The register entries are given as lists of fields while the page marks them as one table; I could not tell from the page whether they render as a table or as the lists shown.

### `docs-index`

- "with what elasticity": the term is not explained on the page and a first-time practitioner does not know what elasticity of a contention means here.
- "PCA finds where the data spread, this finds where they stop, and the two chain": "the two chain" is unclear (chain how, in which order); the root page's parenthetical about the tension report running PCA explains it, but this page does not.
- "API and API reference": two list items' names run together; I could not tell whether these are two pages or one.

### `docs-getting-started`

- "temperature, the one parameter set, is tau, how hard the maximum is": I could not place "how hard the maximum is" on first reading.
- "(choosing the temperature)": a bare parenthetical pointer with no link target visible in the text; I could not tell where it leads.
- "a weighted geometric mean of the metrics, 1 on the fitted reference surface, so negative inside and positive beyond": "inside" and "beyond" are not defined on this page, and "log V" is used before V is introduced.
- "the grey strip under the line is the region up to 0.5 below the frontier in log V": the figure was not opened, so the "strip" and the 0.5 cannot be checked against it here.

### `docsfig-first-fit`

- Page text before the figure: "the designs lie on or just beyond a straight frontier". The figure shows most designs well below the line, and the caption says "fall below it or just beyond it"; the page sentence and the caption disagree, and the page sentence disagrees with the image.
- "the grey strip under the line is the region up to 0.5 below the frontier in log V" vs the legend "band (log V >= -0.5)" vs "the band of near-frontier designs has width 1/tau": with tau = 20, 1/tau is 0.05, not 0.5. I could not place whether the drawn band (0.5) is the same band the 1/tau sentence names, or a wider display band.
- "the first fit seen on two metrics" (caption) vs `ts2 = HyperbolicTradeSpace(temperature=20.0).fit(X2)` (code): is the figure a view of the three-metric fit or a new fit? The code says new fit; the caption reads as the same one.
- The outlier near (-9, -9) and the tail of designs toward it: nothing on the page says what they are.

### `docs-user-guide-overview`

- "a small weight at the fit temperature is weaker participation" (tau and the fit temperature are not introduced on this page).
- "After a one-time normalization V = 1 is the fitted reference surface" (the normalization is not said).
- "novelty score and candidate white space" (named, not explained here).

### `docs-user-guide-conditioning`

- "It fixes what V = 1 means in practice": V is not defined on this page or in the story; I can guess it is the value of the fitted surface but cannot place it from what I read.
- "the temperature of the next page: it is quoted in inverse log-spread": the reason given for scaling depends on a term from another page, so the scaling advice cannot be judged from this page alone.
- "The pulled-back exponent on a raw attribute is w_j * alpha_j": neither w_j nor alpha_j is introduced here.
- "If the contending set moves": "contending set" is not defined on this page (the Home page says "which metrics contend", which suggests the meaning, but the page does not tie it).
- "they show whether the story is sensible": unclear which "story" is meant (the conditioning choice, the fit's findings, or the documentation's).
- "its chart coordinates are nan": the chart is not introduced on this page.

### `docs-user-guide-fitting`

- "(at one term they coincide when the log-metrics are centred, as the cubesat's are)": I could not place which centring is meant or why the cubesat is mentioned this early.
- "carries no local-optimality status": unclear without the termination page.
- "Read kappa on the scale of tau: far below it, terms merge." It was unclear what "merge" means in practice.
- "Keep min_exponent (a floor on every exponent) at 0 to read the contending set": unclear what the contending set is.
- "the cell of new rows" and "cell_": the cell is not defined on this page.
- "Use tau of 3 and above: below that frac_above_ is not monotone in tau": the reason is not given.
- "term_aggregation ... a repeated term shifts the soft maximum by log 2 / kappa": a dense aside whose use I could not place.

### `docsfig-three-terms`

- "band (log V >= -0.02)" in the legend, and "a grey band below it" in the alt text: no band is visible on the image.
- "Three terms" in the caption: I could find only two straight pieces in the frontier line.
- "frontier V = 1 (envelope)": whether this is the envelope of the three term lines or the fitted reference surface (the page distinguishes the supporting envelope at infinite tau from the fitted surface at finite tau, and this fit uses temperature=50.0).

### `docs-user-guide-tensions`

- "min_exponent must be 0 for this reading" and "the report warns when the estimator was fitted with a floor": I could not place what min_exponent is, because it is not introduced on this page.
- "absolute log V below band" and "closure_note": V is never defined on this page.
- "The report solves the tau = infinity program itself, independent of the fit temperature": I could place the claim, but not why a first-time user needs it.
- The figure label "Figure 3" on a page that shows only one figure.

### `docsfig-tension-report`

- "w=0.30", "w=0.37", "w=0.33": the labels on the axes are not named in the caption or the page; I assume contending exponents but could not confirm it.
- "diagonal outlines mark the contending set": read twice; the heavy borders around each diagonal cell look like separate boxes per metric rather than one outline of a set, so with fewer contending metrics I would not be sure how it looks.

### `docs-user-guide-chart`

- "(level offset)" in the opening paragraph: a bare gloss, placed oddly after a line break.
- "d - 1 say where along the surface the design sits, free of overall scale": the phrase "free of overall scale" is not explained.
- "the grey strip below it is log V from -1/tau to 0" in Figure 4: tau is not defined on this page.
- "(example)" after plot_ternary: it is unclear what it points to.
- Figure numbering starts at 4 and the other figures are not seen on this page.

### `docsfig-log-plane`

- "One term in the log plane": I could not tell from the figure or the page why "one term" is singled out, or what a second term would look like here.
- "log V from -1/tau to 0" against the legend's "-0.05": I placed it only by guessing that tau is the temperature=20.0 in the code.
- "the near-frontier band, |log V| below 1/tau" (later on the page) against the figure's one-sided strip and its empty region above the line: I could not square the two.

### `docsfig-chart-holes`

- "black-ringed dots": no key anywhere in the caption, alt text or page text.
- "This seeded blob has no interior hole": why choose a sample with no hole to illustrate hole finding.
- "grid positions far from every design" at the rim: the page says find_holes only takes grid points "inside the convex hull", yet the squares sit at the visible edge of the cloud, and I could not tell how the hull relates to the squares.
- "Z0", "Z1": the page calls these position coordinates but the axis labels do not say so.

### `docs-user-guide-prediction`

- "it can leave the quantity's admissible range while the certificate holds": the page never says what "the certificate" is.
- "a breach fraction or a probability": I could not tell which outcome is meant, or why it belongs on this page.
- "predict_novelty(X_config): V - 1": V is not defined on this page. I could not tell whether V is the energy differential named on the root page or something else.
- "the pair (Z, log_v)": Z and log_v are not introduced here.
- "The regressor declares positive_only targets": I could not tell whether "declares" refers to an estimator tag or to something the user does.

### `docs-user-guide-termination`

- "Conditional local optimality: if no design sits exactly on a seam between terms..." (what a seam is and why the fixed assignment is then optimal; no pointer to where it is shown).
- "stable radius is the perturbation provably leaving every design's assignment unchanged" (perturbation of what, in what units).
- "term gaps within eps_kkt and min_curvature above eps_feas" (why the curvature is compared with a feasibility tolerance).
- "A soft fit leaves gamma, radius and bound nan." (floating line in the fields list, after the min_curvature item).
- "uncertified: as above." under the soft-fit list (as above refers to the hard-fit status, not to something in the soft list).
- "the tightest design sits a hundredfold nearer a seam than the typical one" (0.0020 versus 0.21 is about a hundredfold, but the "1/tau" band of 0.02 is not discussed in the result sentence).
- Terms gap G_k, tau, eps_kkt, eps_feas, mean_slack_ are used without definition on this page.

### `docs-user-guide-limitations`

- "A hole is an opportunity only if the trade space is log-convex around it": I could not tell which hole is meant (one in the data or one in the surface), or how a user would check log-convexity.
- "Moving the reference or the scale of one metric changes which term is tangent": the page does not say tangent to what.
- "Away from that point a design can score below 1 while locally on the frontier"
- "If the balanced point sits on a vertex or edge of the weights' simplex": neither "balanced point" nor "the weights' simplex" is introduced on this page.
- "Judge a score against the band 1/tau": I could not tell whether the band is around 1 or how wide it is.
- "graded participation at a fit temperature"
- "negative association near the surface is partly a closure effect"

### `docs-api`

- "12" after "scikit-learn conventions": a citation marker that rendered as bare digits.
- "(fitting)" and "(chart)" after the coordinates and gaps entries: I could not say what they tag.
- "the soft fit (Reading termination)": a reference to a section I could not place from this page.
- "a transformer: fits the surface and gives the chart of position and log V": "position" and "log V" are not defined here.
- "mean_slack_ (the mean slack, to compare fits across numbers of terms)": unclear without the user guide.

### `docs-examples`

- "With the fit temperature chosen by select_temperature for a tenth of designs above V = 1": what "a tenth of designs above V = 1" means is not explained on the page.
- "At the one-term temperature (case.mean_slack_fixed_tau) the mean slack falls": mean slack, and why the temperature is fixed, are not defined here.
- "status certified": not explained on the page.
- "a price at the one-term frontier, in band widths": "band widths" and "price" are not defined here.
- "Z0 and Z1, the first two of seven position coordinates, meaningless alone": I could not tell why they are shown if meaningless alone, beyond the "coverage" remark.
- The Run it column list ("tau, band 1/tau, objective_, ... gamma, radius, bound"): a run of names with no reading for a newcomer.

### `docsfig-adcs-tensions`

- "5-lemma" and "exact-maximum support" in the title
- "w=0.00" (weights; unexplained in caption)
- "association" vs "correlation of the log-metrics"
- Page text says "No pair of the eight metrics reaches a rank correlation of 0.99" while the figure shows 0.99 (power margin, energy balance); the two measures differ but the page does not say how
- The -0.95 pair involves a grey metric (peak slew power), but the page never says what a strong tension outside the contending set means

### `docsfig-adcs-coordinates`

- "the first two of seven position coordinates, meaningless alone": read twice; I could not place why a figure is drawn in coordinates the caption says are meaningless, or what "position coordinates" are on this page (the code calls them chart[:, :-1]).
- "It shows coverage, not the frontier.": coverage of what, judged how; the page never says what a reader should conclude about coverage from this plot.
- "193 ringed designs lie nearest the frontier": nearest by what threshold; the requirements table below speaks of 56 near-frontier designs for the primary regime, and I could not reconcile 193 with 56.

### `docsfig-ternary-planted`

- "V, the invariant value, also depends on the total, so a marker is not where V = 1": I read it twice; the figure's contours give no V value so I cannot check it.
- "lines of equal V ... closing around each marker": the lines are unlabelled, so what a line stands for stays unplaced.
- "a numbered marker is a term's exponent vector": the marker sits in a place on the triangle, but an exponent vector and a position are not obviously the same thing to a first-time reader.
- The two sizes of grey dot: not explained on the page or in the caption (the root page's "larger dots are nearest the frontier" is the only hint, and it is about another figure).
- "an analysis of the fit, not a label on a design": clear in words, but the in-image labels "all three trade" read like labels on designs.

### `docs-theory`

- "The model is a root of that sum, so the surface V = 1 is where the posynomial equals one." (a root in what sense: the K-th root, a root-finding root? Not defined.)
- "at the fit temperature tau" (tau appears without definition; its relation to term_temperature, introduced a paragraph earlier, is not stated.)
- "set by a participation threshold" (no parameter or value given.)
- "designs are chosen by an evaluator and not drawn from the attainable set" (what this assumption means for the user is deferred entirely to another page.)
- "Holes in the Z plane are candidates for white space." ("white space" is not the Home page's word "gaps" and is not defined here.)

### `docs-further-reading`

- The bare numbers after titles ("scikit-learn and its API design 12", "Convex Optimization 3", "Kernel PCA 10") read like page numbers or a count until I saw the numbered list below. They are footnote markers, and the "12" after the first entry looks like twelve, not references 1 and 2.
- "Enhancing sparsity by reweighted $\\ell \_1$ minimization" in reference 7: the raw LaTeX in the rendered text. Also "Reweighted $\ell_1$ minimization 7" in the bullet.
- "the sparsity option, penalty="reweighted_l1"": a parameter name with no explanation on this page. It is fine for a user of the package but arrives without context.
- "the family the multi-term fit stays inside" and "the second source of the multi-term fit": the multi-term fit is not defined here. Home says only "a sum of monomial terms".

### `root-index-fig-why-regions`

- "the larger dots are nearest the frontier": the frontier is not named before this on the root page, and nothing in the image encodes "nearest" (no legend).
- "all three trade": does it mean all three metrics are in mutual tension, or that no single pair dominates? I could not place it.
- "placed by which metric it favours": placed by what computation (shares of the metrics, of the fitted exponents, something else)? Not said.

### `root-index-fig-figure1`

- "energy differential" (caption and middle pane): never defined on the root page.
- "V = 1" and "V > 1: beyond": what V is.
- "supporting envelope": a term not used on the root page.
- "terms laid flat" and "Z (position along the frontier)": why the flat chart is useful.
- The dotted curves in the left and middle panes, and the arrows w1, w2, w3.
- The "What" paragraph's "n-lemma": the figure sits beneath it, yet nothing in the figure is labelled n-lemma.

### `root-readme`

- Root page: "Its unit is the n-lemma": I cannot tell from the page alone whether the n-lemma is Home's "monomial term" or something else.
- Root page: "a design's energy differential to that surface": not defined on the page; I assume it is how far the design is from the reference surface, but the page does not say so.
- README: "a monomial, later posynomial, frontier": "later" could mean a later release or a later step of the fit.
- README: "learns a hyperbolic \"space\"": the quotation marks around "space" are not explained.
- README: "From noisy, biased observations": nothing else in the README, the root page or Home says what the method does about noise or bias.

## Gaps

None. Every section reader's Q6 has one line for each statement `units.tsv` lists under it (1, 8 and 18 lines for
Sections 3, 4 and 6), and every appendix reader's Q7 has one line for each of its tables (1, 5, 9, 19, 1, 3, 2): no
verdict cell reads "not returned".

## R-1 check

Rows by kind against the sizing: section 14 (14), statement 27 (27), float 10 (10), appendix 7 (7), appendix-table 40
(40), docs-page 14 (14), docs-figure 8 (8), root 1 (1), readme 1 (1): 122 rows, 122 units. The scope's sizing totals
"123 units", an arithmetic slip: its own counts (14, 27, 10, 7, 40, 14, 8, 1, 1) sum to 122.
