# The paper, section by section: what each must hold, how it reads, and its state

The register the paper packages (WP53 to WP58) work against and the driver soft-confirms against, as the supervisor's
proxy (his ruling of 2026-11-15, ~12:20 EST, `driver-log.md`: autonomous mode; the driver confirms each section so he
reads a fresh candidate and makes light edits, not content or style revisions). One row of state per section:
*open* (not yet reworked), *soft-confirmed* (the driver has checked it against this file on the rendered page),
*read by him* (his edits applied). His words are in the decisions files named; this file paraphrases them.

## Rules for every section

- No metanarration: no sentence whose subject is the text, the page, a figure's placement or the reader; the one
  exception is the roadmap paragraph closing Section 1 (CLAUDE.md; WP11-decisions.md, "Main results").
- No forward reference to a definition or a result not yet given; Section 1's roadmap is the only place for forward
  links (WP11-decisions.md, Section 3).
- One point per place: a fact stated where it belongs and not repeated as a qualifier elsewhere ("you don't need to
  jam every point in every time", WP11-decisions.md, Section 2).
- Open questions and caveats leave the narrative for the appendix section "Assumptions, limitations and open
  questions" (WP55-decisions.md); a limit is stated once where a result is stated, not stacked.
- Conditions and precise statements live with the result, not in the abstract or the introduction (the "weakly"
  ruling, WP11-decisions.md).
- Every claim backed (a lemma step, a generated value, a test, a verified source) or narrowed; prose that states a
  number cites its generator; the model, the fit and the analysis kept apart (CLAUDE.md).
- The glossary's words; "dataset" is his word on the root page, "table" stays the paper's unless he rules otherwise.
- Figures earn their place, drawn by code (Section 11's claim), judged as rendered.
- Notation and presentation in the conventions of the Boyd and Vandenberghe lineage: the problem statement as
  "minimize ... subject to ..., with variable ...", theorems as "Suppose ... Then ...", proofs in the appendix
  (`WP55-rounds/spike-notation.md`).

## Abstract

- **Holds:** his text; the three thrusts closing (the search; holes by topological data analysis; formal
  verification and performance), the Pareto sentence without "weakly", "implemented with a scikit-learn-compatible
  API", the cubesat sentence without its qualification. About 500 words, under the test's 525.
- **Style:** his register; no conditions or qualifiers that belong in the body.
- **State:** read by him (WP11-decisions.md, 2026-11-15 08:40 onward); lands with WP53.

## Section 1, The decision problem

- **Holds:** opens "Decision analysis has two products"; the justification as the hard product, "recognized,
  rigorous and reproducible"; the PCA paragraph in his three sentences; the configuration-management sentence with
  Fulcoly, Ross and Rhodes 2012; the paragraph closing "Our contribution is interpretability at scale, and reuse of
  the decision analysis pipeline via unsupervised learning."; then the roadmap paragraph, prose, one per section, no
  appendix mentions.
- **Must not hold:** who the paper is for; a main-results list; the Organization paragraph; the novelty sentence; a
  generated sentence from the case (moved to Case analysis).
- **State:** read by him; lands with WP53.

## Section 2, Prior art

- **Holds:** the three-layer paragraph in prose (the decision problem; unsupervised learning with DEA in it; the
  solver), the figure with his three glosses and his caption sentence, the sentence giving the figure its job
  ("separates two uses of the optimization literature"); Table 1 and Appendix G's register in the three layers,
  top to bottom, DEA in the middle; the family paragraphs without Section 4's vocabulary (the fitted value, the
  fitted surface, a weight vector, a softened maximum) and without the Open sentence or the closing lineage
  sentences.
- **Style:** plain prose; no "by family" in the title.
- **State:** read by him; lands with WP53.

## Section 3, Preliminaries and notation

- **Holds, in order:** the notation sentence (Boyd and Vandenberghe; scikit-learn's estimator terms; Appendix A the
  register); the pipeline paragraph in his sentence ("A feature engineering step is applied to condition the
  attributes into metrics m, strictly positive and larger is better.") and the figure (evaluate, condition,
  identify, analyse; c, a, m, w and β; a black box, feature engineering, fit the surface, decision analysis); the
  data; a model as a function (V the function, V(m) its value, the unit level set a surface, the parameters); the
  soft maximum; the fitting problem (decision variables θ, a loss J, the minimizer over the feasible set).
- **Must not hold:** the assumptions list (moved to Methods), Map and territory, Layers, Words, implementation or
  the case. Only A1 to A3 may return here if WP55 follows the spike's recommendation.
- **Style:** a quick start for reading the mathematics; nothing fancy or novel; the minimum kit so Section 4 reads.
- **State:** read by him once; the build-up written after his last comment and *not yet read*; WP55 may still
  reshape it to the lineage's template (minimize ... subject to ..., β the optimal value).

## Section 4, Definitions

- **Holds:** opens with the three one-sentence definitions (the fitted reference surface, the supporting envelope,
  the Pareto boundary) in Section 3's symbols; then the invariant value, the posynomial, the temperatures, the
  chart, the n-lemma, reach and share, elasticity, tension, the ascent direction; definitions introduced in prose
  first, then formally, as the GP tutorial does.
- **Must not hold:** forward references to later definitions; threshold conventions and solver behaviour inside a
  definition (the n-lemma's thresholds belong in Methods); gap numbers and appendix pointers.
- **State:** open (WP55).

## Section 5, Methods

- **Holds:** the assumptions A1 to A11 as moved from Section 3 (or only those a result needs, stated at the result,
  per the spike); the one-term problem in the lineage's template with β the optimal value; the several-term
  alternation with its guarantees; the temperature choice; conditioning (stage 2) as the analyst's step; the
  estimator's names as the WP42 build renamed them (loss, trade_off_report, plot_association).
- **Must not hold:** results restated; caveats about what is not proved (the ledger).
- **State:** open (WP55).

## Section 6, Results

- **Holds:** theorems as "Suppose ... Then ...", each with its lemma label and a one-line proof pointer to
  Appendix B; Derived/Hypotheses labels and Script boxes gone from the main text; the open questions Q1 to Q4 moved to
  the ledger.
- **State:** open (WP55).

## Section 7, Case construction (Section 8 until WP54 renumbers)

- **Holds:** the cubesat case narrated from the model as it is now (WP22 adopted; WP23's coupling table, measures of
  effectiveness, launch cost reading mass, settling time the one time metric; the data of record), to make the
  approach actionable: what was built, how, and where the thread to code and data runs. Figures that carry the
  narrative; not every figure the repository has.
- **Must not hold:** stale sentences about an earlier model; apparatus the repository already documents.
- **State:** open (WP56, with its prework spikes).

## Section 8, Case analysis

- **Holds:** from the model to a decision: what contends, with what elasticities, where designs sit, the decision the
  executives make, the thread preserved through code and data; the generated nondominated sentence now opens it
  (keep or strike at WP56); K = 2 as the case's reading.
- **Style:** narrate the case and tie it to the thesis; the figures play the key role.
- **State:** open (WP56).

## Section 9, Discussion

- **Holds:** the value proposition of the abstract and Section 1 answered; the three layers of Section 2 revisited;
  interpretation as human validation; limits stated once; leads into Future work.
- **Must not hold:** only the case; caveat stacking.
- **State:** open (WP56).

## Section 10, Future work

- **Holds:** short; what this release accomplished first; the three directions of the abstract in its order, each
  written fresh from its spike record (WP41, WP43, WP48, WP50, WP36, the formal direction), within the readouts'
  boundary; the search's surviving sentences from the old Section 7.
- **Must not hold:** a separate search section; "final remark"; results.
- **State:** open (WP54).

## Section 11, AI acknowledgement and Reproducibility

- **Holds:** what AI assistance did and did not do; how the work was gated and checked; how every figure, table and
  number is reproduced (Appendix F, the commands) and how a reader adapts the pipeline to a table of their own.
  Under 200 words, informational.
- **Must not hold:** "machine-checked" or "formally verified" (scripted checks); metanarration; a separate
  Reproducibility section.
- **State:** open (WP54).

## Works cited

- **Holds:** every key in `docs/references.bib` resolved (DOI or stable URL) and cited.
- **State:** soft-confirmed by the references tests.

## The appendices (WP57 plans; one package per appendix or group)

- **Rule for all:** each appendix supports the prose one step deeper where the prose needs it; no opinion on the
  paper's text; no metanarration; material that does not earn its place moves to the repository, which the paper
  cites; re-lettered in the order of first mention, once, last.
- **A, symbols and terms:** the register; consistent with Section 3's kit.
- **B, the derivations:** the lemma scripts as pencil-and-paper substitutes, never formal verification; the proofs
  Section 6 points to.
- **C, the case model:** what Section 7 narrates, one step deeper.
- **D, the case tables:** the numbers Section 8 reads, no more.
- **E, the gaps ledger:** becomes "Assumptions, limitations and open questions": the open questions moved out of the
  narrative, each with its section and record.
- **F, reproduction:** the toolchain, environment and commands Section 11 points to.
- **G, the register of prior art:** the three layers' order; entries cited.
- **H, the HoroPCA comparison:** its three boundaries (WP35); kept if Section 2's paragraph needs it.
- **State:** open (WP57 and its children).
