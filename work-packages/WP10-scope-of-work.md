<!-- The first draft of this file (written as WP9, the readability package) was superseded on 2026-11-08 by the supervisor's redirection (WP10-decisions.md) and replaced by the second draft. This is the THIRD draft (revision 2, 2026-11-08): it adds the separation of concerns recorded in WP8a-decisions.md (the paper absorbs the how and why from the docsite), marks the decisions taken at the scope gate as decided, and keeps OD4 open. Earlier drafts remain in git history. -->

# WP10 — Scope of work: The paper, working draft

| | |
|---|---|
| **Status** | DRAFT (revision 2). Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP10-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP10-decisions.md`, after `work-packages/WP10-review.md`. Acceptance is STRUCTURAL (see "Acceptance is structural"). |

Replaces the superseded first draft in `work-packages/WP10-scope-of-work.md` (history only; its readability-loop content is WP11's).

## Purpose

The research is hardened (WP1 to WP9, WP13); the supervisor views the paper as "a narrative view on
the research itself" (`WP10-decisions.md`, "Sequencing"). This package writes that narrative as a
working draft: a mystmd article in which the notebook is the paper, in the manner of his SciPy 2026
proceedings article, organized as an academic paper (motivation, prior art, notation, definitions,
methods, results stated as theorems with proof sketches, case, discussion, future work, works cited)
with every claim backed by computationally verifiable supporting material in the repository.
**The paper is the home of the how and why underneath** (see "Separation of concerns"). Presentation
polish and the cold-read loops are WP11's; deployment is WP8a/WP8b's.

## Separation of concerns (supervisor, recorded in `WP8a-decisions.md`, 2026-11-08, "The supervisor's staged-site review")

Verbatim: "i need a seperation of concerns between the paper and the doc site the doc site is for a
user of the package. the paper is for someone who wants to understand the how and why underneath".
Verbatim, on the lemmas: "the lemmas for example are not very readable and might be better organized
as traditional theorem like statements from academic papers but with the proof sketches narrative and
the reader directed to the specific scipy scripts or independent verification. some of that can be
relegated to appendices if it helps with the flow." Verbatim, on the two registers: "actually i think
you muddle togethe the doc site and the paper. i cannot tell what is what. i want the docsite to be
more like scikit learn docs and the paper to me more like my scipy paper."

Consequences for this package:

- The paper **absorbs** the paper-register material now in the docsite: the mathematics narrative of
  `docs/method.md`, the lemmas recast as **theorem-style statements** (Definition / Lemma /
  Proposition / Theorem, numbered, hypotheses explicit) each followed by a **narrative proof sketch**
  and a **pointer to the derivation script** `derivation/lemma_NN_*.py` and its `verify`; the
  derivation ledger; the prior-art review of `docs/literature.md`; the long limitations; the
  abstraction-gaps ledger as an appendix; the full case.
- The docsite (a user's guide in the scikit-learn manner) is restructured by **WP8a Amendment 2**
  (separate package, drafted in parallel). WP10 **reads** the moved text as sources under
  `docs/superpowers/notes/paper-sources/` (which Amendment 2 proposes to preserve there) and **edits no
  `docs/*.md`**. The docsite keeps a one-page theory-in-brief that links to the paper.
- The paper is modelled on the SciPy article's build and register
  (`/Users/z/Documents/GitHub/hc-scipy-2026/papers/michael_zargham/`: `myst.yml`, `paper.ipynb`,
  `supporting_material.ipynb`, `derivations.py`).

## Acceptance is structural (supervisor, `WP8a-decisions.md`, verbatim)

"the paper is not something i've done a full read on yet. fist pass seems okay but it will definitely
need readability and correctness loops. we'll need to run a grid of user reads (cold) at the depth
levels previously outlined and with differing personas. this means the paper acceptance is stuctural
not final sign off on content or aesthetics." WP10's acceptance therefore checks that the paper has
the agreed structure and that every claim has its pointer; it is **not** a sign-off on content or
aesthetics. WP11 carries the cold-read grid (depth levels x personas) and the content loops.

## Story (settled with the supervisor, `WP10-decisions.md`, "The paper's story"; final for scoping: "great. thats what we needed")

Why before what.

1. **Why.** A decision analysis must produce an answer and an interpretable, intuitive justification
   for an accountable executive; the process that turns much data into little must be recognized,
   reproducible and rigorous. Trade studies today are mostly documents, grids and tables, and detail
   is lost; computational alternatives are bespoke and opaque, which is why documents stick. A
   model-based method must handle scale, complexity and noise consistently and interpretably so the
   method itself is trusted. PCA has that standing but explains variance, which is analysis and says
   nothing about trade-offs; decision-makers need what trades against what, to make and defend a
   judgement call; an answer far from the frontier is hard to justify; the analysis must rerun on
   empirical data for configuration management. Backed by the fifteen adopted state-of-practice sources.
2. **Contribution.** Scaling up trade studies and equipping them with a reproducible computational
   method with a PCA-like feel; plus (outline v2) a reproducible, interpretable, trade-off-aware
   search that raises the attainable level and stops short of selecting a design, which is the experts'.
3. **What.** The trade space is a manifold; posynomials fit it to a coordinate system for data-driven
   choices; "what trade-offs explain this trade space" as PCA asks which vectors explain variance; the
   n-lemma (a power-weighted product) is the analogue of a principal component; kernel functions
   are the trade-offs, within generalized geometric programming; level surfaces of V exist at every
   value and V = 1 is placed at the frontier by normalization (the invariant form), with a reversible
   transformation to the tractable log space of the fit; many plots because the method is
   unsupervised; the three earlier spines (tensions not variance; n-lemmas found; a learned chart) as
   sections. The method belongs to unsupervised learning and feature engineering beside PCA: kin, not
   substitute, and the two chain (supervisor, `WP10-decisions.md`: "it can also be chained with pca its
   not a strict substitute. it just belongs in unsupervised learning / feature engineering").
4. **Case** at K = 1 and K = 3 (the cubesat, two regimes). **Final remark** (the hook): a novelty or
   impact score for new capabilities from how far above V = 1 they are forecast to sit.

## The abstraction the method keeps (supervisor, `WP10-decisions.md`, 2026-11-08, verbatim: "those repos and the supporting tools for that ecosystem are developing quickly. we're keeping an abstraction of config variables and measured attributes so our method is relevant even as tools move, or in cases where scoring comes from physical systems or human assessments")

A framing requirement. The method's input is a table of configurations $c$ and attributes $a$; stage 1
of the pipeline (configuration to attributes) is a black box to the method: a simulator behind a
system model, a physical test campaign, or a human assessment. The cubesat model is one instance
behind that abstraction, not part of the method. The paper states this in Preliminaries (stage 1 of
the pipeline) and in the Discussion of cross-application, using the register's wording for $a$
(`notation.md`, row $a$: "The evaluation is a black box to the method ..."), and names no tooling
versions anywhere in the body.

## Reader model (supervisor, `WP10-decisions.md`, "Redirection")

Assumed mathematics: multivariate calculus, linear algebra, convex optimization. Notation anchored on
the scikit-learn documentation and glossary, and on Boyd and Vandenberghe for mathematics and
algorithm descriptions. The paper must read "well" at six drill-down levels: **L-A** abstract and hero
image; **L-B** headers, main results and figures; **L-C** the whole paper; **L-D** the paper and the
supporting materials ("computationally verifiable appendices"); **L-E** pull the code and reproduce;
**L-F** pull the code and adapt it to one's own case. (Statement blocks are written so that L-B reads
the statements alone and L-C reads the sketches; L-D follows the script pointers.)

## Decided at the scope gate (supervisor's words, `WP10-decisions.md`, "Scope gate decision loop")

Not open. Recorded here so the scope is self-contained; the verbatim records are in the decisions file.

- **Title and byline.** Supervisor, verbatim: "Working title now, final at WP11"; his proposal: "Scaling
  Decision Analysis with Hyberbolic trade space identification" (normalized in the record to **Scaling
  Decision Analysis with Hyperbolic Trade Space Identification**, working title). The author proposes
  a subtitle for his pick at the first reading; the final title and subtitle are set in WP11. Byline:
  sole author, Dynamical Systems Group, ORCID 0000-0001-5279-690X as in the SciPy article.
- **Figure 1.** Supervisor, verbatim: "yes s4 is the direction but i liked it better when the first pane
  was kinky. more realistic". Figure 1 is the three-pane S4 schematic (metric space with the
  hard-max envelope drawn with sharp corners between the hyperbolic sheets as in S1 → log space with
  flat facets → the chart), from the spike `docs/superpowers/notes/spike-figure1/`
  (`make_schematics.py`, `S4.png`); the author produces the final figure to that design, with the
  register's words in the caption. Earlier, verbatim: "a hero image is a hook. its okay for it to be
  conceptual and to convey the idea if it pulls the reader in and does not misrepresent the content".
- **The WP7 notebook.** Supervisor, verbatim: "archive it with banner for now so we can use it as
  reference but plan to clean out the archive before the first release". It moves to
  `examples/adcs/archive/` with a first cell pointing to the paper; its guard tests move into the
  paper's tests where they still apply; the archive's removal is a WP8b release-punch-list item.
- **Tools statement.** Supervisor, verbatim: "look at my scipy paper; you can use a similar disclosure
  as i followed similar methods. you can also cite my incose IS 2026 paper which is specifically about
  documents, requirements and accountability". The Acknowledgments carry a tools-and-process disclosure
  modelled on the SciPy 2026 article's (read from its source), adapted to this repository's process
  (gated work packages, machine-checked derivations, the external review), and cite Zargham 2026
  (INCOSE International Symposium 36(1), doi 10.1002/iis2.70203; supervisor: "my INCOSE IS paper is no
  longer forthcoming it is out"), entered in `docs/references.bib` as `zargham2026incose` under the
  WP5 rule. The repository's no-attribution rule for commits and documents is unchanged; the
  disclosure is the supervisor's own statement, in his voice.
- **How the drill-down levels are judged at acceptance.** Supervisor, verbatim: "Automated checks plus
  cold-reader trials". A fresh-context reviewer is given only what each level's reader sees and
  reports per level in `WP10-review.md`; the supervisor's own reading and the cold-read grid are WP11's.

## Goals

- G1. A mystmd article `paper/paper.ipynb` (notebook is the paper), about 5,500 counted words (cap
  6,000), in the section order of the table below (outline v2 reconciled with the external reviewer's
  paper map, E-10, and with the SciPy paper's build), that tells the Story and reads well at L-A to L-F.
- G2. A supporting notebook `paper/supporting_material.ipynb` of lettered, computationally verifiable
  appendices (A to H) that the paper cites claim by claim; it carries the full proofs' detail, the
  ledger, the abstraction gaps and the long case detail.
- G3. The paper keeps the configuration-to-attributes abstraction. Every computation the paper shows
  is a call into a tested module `examples/adcs/case.py` (cubesat specifics as data), so another table
  runs through the same functions.
- G4. The prior work is a prior-art review by family (claiming nothing as novel), with the Pareto and
  DEA contrasts, absorbing `docs/literature.md`; the fifteen state-of-practice sources plus Miettinen,
  Ehrgott and the three DEA references are in `docs/references.bib`.
- G5. **The mathematics is the paper's** (new). Every lemma L1 to L14 is stated as a numbered
  theorem-style block (hypotheses explicit), followed by a narrative proof sketch and the pointer to
  its derivation script and `verify`; the algorithm part of Results follows E-8's structure; every
  statement is marked Derived / Numerical / Open (E-10); every simplifying assumption is named where
  made, defended there in a sentence, and taken up in Future work with how to go beyond it.
- G6. **The abstraction gaps and the limits are the paper's** (new). The one policy paragraph ("Map and
  territory", `docs/method.md`) appears once in the body; the abstraction-gaps ledger
  (`docs/superpowers/notes/abstraction-gaps.md`) is an appendix; the long limitations are in the
  Discussion and the appendix.
- G7. The trade-off-aware search appears as a section marked preliminary until WP12 lands.
- G8. A test file that guards the paper's structure, budget, register and source coverage so later
  loops (WP11) cannot silently break them.

## Non-goals

- Readability loops, the cold-read grid (levels x personas) and rendered-browser verdicts (WP11); the
  paper's publication under `/paper/`, the Pages workflow and the docsite, including its restructure
  (WP8a and its Amendment 2); PDF/release machinery beyond what OD4 selects; PyPI and the release (WP8b).
- **Editing any `docs/*.md`** or the docsite: WP10 reads the moved material from
  `docs/superpowers/notes/paper-sources/` (and the current `docs/` pages until Amendment 2 lands) and
  edits none. Likewise no change to `derivation/` or the package source while WP13 runs.
- New mathematics (the paper cites lemmas, it does not add them); the search's code, lemmas and
  results (WP12).
- Final sign-off on content or aesthetics (acceptance is structural; WP11 does the loops).
- Submission to a venue or venue-specific compliance (the SciPy proceedings are the structural
  reference only).
- Reworking the system model (the separate SysML tidying package); a rewrite of the data or the
  simulator; K selection rules, scalability, kernels beyond what the discussion states.
- Claiming novelty; the response letter to the external reviewer (WP13).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/paper.ipynb`, executed, outputs committed, with the front matter (title, abstract, keywords, abbreviations), numbered definition / lemma / proposition / theorem blocks with hypotheses, captions, Derived/Numerical/Open badges, the cross-references to Appendices A to H | G1, G5, G7 |
| D-2 | `paper/supporting_material.ipynb`: **A** the register (`docs/superpowers/notes/notation.md`) as a table; **B** the theory in full: conditions of the theory, the full statements and proof detail of L1 to L14 with each lemma's `derive`/`verify` output, the derivation ledger and the summary of lemma coverage; **C** full case detail (sensitivity variants, per-category refits, regime tables, the K = 1/2/3 diagnostic table, propose-predict-check with its mixed result, candidates, the nondominated counts); **D** the algorithm in full: the posynomial and GGP extension, the solver for small K, the three levels of guarantee and the stopping declaration, with the WP13 certificates (`termination_`, `conditioning_`, margin, radius, Corollary 4 bound) as printed by the code; **E** the abstraction gaps: the ledger G-1 to G-16 evaluated on the planted data and the cubesat tables, "what is proved, inherited, observed", the simplifying assumptions; **F** verification audit (tests by area, lemma PASS list, sklearn checks and expected failures, cross-checks) and what remains for a human; **G** the search's evidence (a marked stub until WP12 lands); **H** the prior-art review in full (the by-family review absorbing `docs/literature.md`, the state-of-practice section, the dropped candidates and the sources for the inherited axioms) | G2, G4, G5, G6, G7 |
| D-3 | `paper/myst.yml` (project, authors, keywords, abbreviations, bibliography, build settings), modelled on `hc-scipy-2026/papers/michael_zargham/myst.yml` | G1, G2 |
| D-4 | `examples/adcs/case.py`: load, feasibility, conditioning, temperature selection and fit, K sweep, report and figure helpers, regime comparison, candidates, propose-predict-check, nondominated counts; cubesat specifics as data; lifts from the WP7 notebook and `examples/adcs/k_terms.py`. The WP7 notebook is archived with a banner (decided) | G3 |
| D-5 | `docs/references.bib` additions (fifteen sources; Miettinen 1998; Ehrgott 2005; Banker, Charnes and Cooper 1984; Allen et al. 1997; Dyson et al. 2001; `zargham2026incose`) under the WP5 rule. The state-of-practice review text lives in Appendix H of the paper (not in `docs/literature.md`, which WP10 does not edit) | G4 |
| D-6 | `tests/test_paper.py` (and `tests/test_case.py` for D-4), including the statement-block, script-pointer and source-coverage tests of the Requirements | G8, G3 |
| D-7 | The prior-art review: the family table, the Pareto and DEA paragraphs and the lineage paragraph in section 2; the full review in Appendix H | G4 |
| D-8 | `WP10-review.md` evidence inputs: the structural check results and the L-A to L-F cold-reader trial reports | G8 |
| D-9 | **The source map** (new): `paper/source_map.md` (rendered also as a table in Appendix F): every moved `docs/` page and section, and every file under `docs/superpowers/notes/paper-sources/`, mapped to the paper section or appendix that carries it (provisional homes below) | G5, G6, G8 |
| D-10 | **The theorem-style statements with proof sketches and script pointers** (new): the L1 to L14 blocks in section 6 (and the Definitions in section 4), each with its hypotheses, a narrative sketch, and the path of its derivation script and `verify`; full detail in Appendix B (L1 to L11, L-conditions) and Appendix D (L12 to L14) | G5 |
| D-11 | **The abstraction-gaps appendix** (new): Appendix E, and the one policy paragraph in the body | G6 |

### Where the moved material goes (provisional, D-9; to be re-pinned against WP8a Amendment 2 when it lands)

| Docs source (page, section) | Home in the paper |
|---|---|
| `method.md` "The pipeline and where the mathematics sits" | §3 Preliminaries |
| `method.md` "Conditions of the theory" | §5 Methods; Appendix B |
| `method.md` "The model" | §5 Methods |
| `method.md` "The fit" | §6 Results (theorem-style) with Appendix B detail |
| `method.md` "What the stage learns, and why it is shape" | §6 Results (theorem-style) |
| `method.md` "Tensions, not variance" and "n-lemmas are discovered, not assumed" | §6 Results (theorem-style) |
| `method.md` "Interpretation" | §10 Discussion |
| `method.md` "Novelty and white space" | §10 Discussion; §12 final remark |
| `method.md` "Prediction from configuration" *(default: not in the supervisor's list; follows the Results it extends)* | §6 Results (one proposition) or §10 Discussion |
| `method.md` "Lineage"; all of `literature.md` | §2 Prior art; Appendix H |
| `method.md` "The posynomial and GGP extension", "The solver for small K", "Three levels of guarantee" (Levels 1 to 3, "The stopping declaration") | §6 Results algorithm subsection (E-8 form); Appendix D |
| `method.md` "What is proved, what is inherited, what is only observed", "Simplifying assumptions"; `abstraction-gaps.md` | Appendix E (gaps); §3 policy paragraph; assumptions named where made, listed in §12 |
| `method.md` "Research direction: kernel methods under the GGP constraint" | §10 Discussion; §12 Future work |
| `method.md` "Summary of lemma coverage" | Appendix B |
| `limitations.md` "Limits of the method" (the long part) | §10 Discussion; Appendix E |
| `limitations.md` "What the contrast with PCA does and does not claim" | §10 Discussion |
| `limitations.md` "Extensions" | §12 Future work |
| `preconditioning.md` (the derivation parts: what the theory asks of stage 2, orientation, shift, scaling, invertibility, zeros, the pull-back) | §5 Methods; Appendix C for the worked nine-attribute case |
| `why-and-how.md`, `case.md`, `api.md`, `api-reference.md`, `index.md` | stay in the docsite (user-facing); the paper links to them from §11 and cites the package API |

## Paper structure (reconciled outline v2, E-10, and the separation of concerns)

Section word budgets are defaults. Counted words: prose and captions of `paper.ipynb`; abstract,
code, tables of the appendices and references excluded *(default)*. Total about 5,550 counted against
the cap of 6,000. **The target of the first draft was 5,000; absorbing the how and why raises it to
about 5,500 under the supervisor's unchanged cap of 6,000; the detail that does not fit moves to the
supporting material (Appendices B, D, E, H)** *(default)*.

| § | Title | Budget | Content and badge |
|---|---|---|---|
| Abstract + Fig. 1 | | 200 (not counted) | the Story in six sentences, the cubesat finding in one sentence; Figure 1 (three-pane S4) |
| 1 | The decision problem | 500 | why; contribution; main-results list (the L-B anchor); organization |
| 2 | Prior art, by family | 600 | the family table (produces / shares / differs / cites); the Pareto, DEA and lineage paragraphs; the state-of-practice sources; claims nothing as novel. Full review: Appendix H |
| 3 | Preliminaries and notation | 450 | pipeline c → a → m, stage 1 a black box in the register's words for a; assumptions A1 to A6 (E-10); notation anchored on the sklearn glossary and Boyd and Vandenberghe; **the "Map and territory" policy paragraph, once**; the register phrases |
| 4 | Definitions | 300 | numbered definitions (invariant form, posynomial, τ and κ, chart, n-lemma, reach, share, exchange rate, ascent direction) |
| 5 | Methods | 450 | the conditions of the theory; the model; the fit; preconditioning (stage 2) as the analyst's step; the estimator interface in one paragraph |
| 6 | Results | 1,400 | L1 to L11 as numbered theorem-style blocks (hypotheses, statement, narrative proof sketch, script pointer and `verify`), badge Derived; then the algorithm subsection in E-8 form (the posynomial and GGP extension; the solver for small K; Lemma 1, Lemma 2, Proposition 3, Corollary 4 of E-8 carrying L12 to L14; the three levels; the stopping declaration), *written last against the delivered WP13 text*, badge Numerical where only observed; Open: Q1 to Q4 |
| 7 | Search of the design space (preliminary) | 200 | the nested loops, the procedure, the honest limits; no results until WP12 |
| 8 | Case construction | 300 | cubesat, two regimes, ten attributes, feasibility, conditioning, temperature; planted multi-facet example |
| 9 | Case analysis | 500 | K = 1, K = 3, regime comparison, candidates, propose-predict-check; Pareto counts from `case.py` |
| 10 | Discussion | 450 | interpretation as human validation; cross-application (the abstraction); the long limitations in brief with the pointer to Appendix E; verify versus validate; the PCA contrast (what it does and does not claim); novelty and white space; the kernel direction; one line on log-convexity and holes |
| 11 | Reproducibility and your own case | 150 | exact commands; the recipe and `case.py` interface; links to the docsite for use |
| 12 | Future work and final remark | 250 | organized by named assumptions (from the gaps and the simplifying assumptions); the final remark hook |
| | Acknowledgments, Works cited | not counted | tools-and-process disclosure (decided) and the INCOSE citation; bibliography |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Section order matches the table above; headers are the L-B skim. | `tests/test_paper.py` reads the notebook's markdown headers |
| R-2 | Counted body prose is at most 6,000 words (about 5,500 targeted); per-section budgets reported; where a section exceeds its budget the excess is moved to the supporting material, not trimmed from the statement blocks. | test counting the counted cells |
| R-3 | Every code cell in `paper.ipynb` makes exactly one call into `case.py` (or the package), and defines nothing else. | test parsing cell ASTs |
| R-4 | Every figure has a numbered, self-contained caption and is referenced in the text; every definition, lemma and appendix reference resolves. | test; `myst build --check` |
| R-5 | The prose uses the register's phrase for each object and contains none of the register's forbidden phrases; the three objects (surface, frontier, facet-level) are distinguished as the register says. | test using the register's phrase lists |
| R-6 | Each simplifying assumption on the supervisor's list is named in the body where made, defended in a sentence there, and appears in Future work with a way beyond it. | test for the eight assumptions' markers; inspection |
| R-7 | The Derived / Numerical / Open badge on each Results statement matches the ledger status (proved / inherited / observed); Q1 is marked Open and not pursued. | test cross-checking against `derivation/axioms.py` and `abstraction-gaps.md` |
| R-8 | The Pareto contrast and the DEA contrast appear in section 2, one compressed paragraph each; nondominated counts (671/706; 146/706; 8/706) are produced by `case.py`, not typed. | test of `case.py` outputs; inspection |
| R-9 | The prior-art table has a row per family in `paper-outline-v1-baseline.md`, each with produces / shares / differs / cites, and claims nothing as novel (no "novel", "first", "new" claims about the method). | test on the table; inspection |
| R-10 | All fifteen state-of-practice, two multiobjective, three DEA records and `zargham2026incose` are in `docs/references.bib` with a resolved DOI or stable URL and a `verified` field, even if the text cites only a subset; Appendix H carries the state-of-practice review. | `tests/test_references.py` |
| R-11 | The algorithm subsection follows E-8, cites L12 to L14 and states the three levels (descent, numerical stationarity, conditional local optimality) with the stopping declaration, as in the `method.md` headings "Three levels of guarantee", "Level 1" to "Level 3" and "The stopping declaration" (or the equivalent text in `paper-sources/`); Appendix D reports `termination_` (status, gap G_k, margin, radius, Corollary 4 bound) and `conditioning_` for the planted data and cubesat tables, as printed by the code. | inspection against the source text; test of cited lemma ids and of Appendix D numbers against `termination_` |
| R-12 | Preliminaries state stage 1 as a black box in the register's wording for a, the Discussion's cross-application paragraph does likewise, and the body names no tooling versions. | test for the register phrase and for absence of version strings; inspection |
| R-13 | Drill-down checks (structural): L-A: abstract within 200 words and Figure 1 present with caption; L-B: headers, main-results list, statement blocks and figure captions alone state the Story and the finding; L-C: no unresolved forward reference; L-D: every appendix cited at least once from the body and every lemma has a runnable script pointer; L-E: each command in section 11 exists and runs in the smoke test; L-F: `case.py` runs end to end on a second table (the planted data) with no cubesat-specific edit. Plus the cold-reader trial per level (decided). | `tests/test_paper.py`; cold-reader reports in `WP10-review.md` (D-8) |
| R-14 | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check` pass; notebooks execute from a clean kernel with committed outputs equal to a re-run (seeded). | local checks; an execution test marked slow |
| R-15 | Section 7 and Appendix G are labelled preliminary and contain no result numbers until WP12 lands. | test for the label; inspection |
| R-16 | No AI attribution in commits or documents, per the repository's rule; the Acknowledgments disclosure is the supervisor's own statement (decided). | attribution grep in the local checks |
| R-17 | **Theorem-style statements (new).** Every lemma L1 to L14 appears in `paper.ipynb` as a numbered block of the kinds Lemma / Proposition / Theorem (Definitions in section 4) with (i) explicit hypotheses, (ii) a statement, (iii) a narrative proof sketch, (iv) a pointer naming its script `derivation/lemma_NN_*.py` and `verify`; the statement block's derivation tag (L-number) is unique and complete (L1 to L14, none missing, none duplicated); the paper's own numbering follows the order of the paper. | `tests/test_paper.py` parsing the blocks against the file list of `derivation/` |
| R-18 | **Script pointers resolve (new).** Every `derivation/lemma_NN_*.py` path named in the paper exists, defines `verify`, and passes (`derivation/run.py`); the Appendix B outputs are the scripts' printed results. | test; `uv run python -m derivation.run` |
| R-19 | **Every moved section has a home (new).** `paper/source_map.md` lists every `docs/` page and section moved, and every file in `docs/superpowers/notes/paper-sources/`, with a paper section or appendix that exists in the notebook; no listed source is unmapped; no mapped home is missing. | test comparing the map with the source directory and the headers |
| R-20 | **The policy paragraph appears once (new).** The "Map and territory" paragraph appears exactly once in the body (section 3), and the abstraction-gaps ledger G-1 to G-16 exactly once, in Appendix E, with each gap evaluated on the planted and cubesat tables as printed by the code. | test counting occurrences; inspection |
| R-21 | **Separation of concerns (new).** `paper/` does not duplicate user-guide material (install, how to run, API tables, parameter lists): those are linked to the docsite from section 11; WP10 edits no file under `docs/` other than `docs/references.bib`. | test for the absence of install/API sections in the paper headers; `git diff --stat` shows no other `docs/` file |
| R-22 | **Acceptance is structural (new).** `WP10-review.md` reports R-1 to R-22 and the L-A to L-F structural checks; it states that content and aesthetics are not signed off and lists improvements for WP11. | inspection of `WP10-review.md` |

## Definition of good

A reader who stops at the abstract and Figure 1 knows the decision problem, the idea (tensions, not
variance) and the finding; who skims headers, statement blocks and figure captions can state the main
results; who reads the whole paper has an academic paper's argument, with the mathematics as
theorem-style statements and narrative proof sketches, spaced out with MyST affordances, with one
claim per block and each claim one click from its derivation script or test; who pulls the code
reproduces every number and, with the `case.py` recipe, runs their own table. The paper is
recognizably a different document from the docsite: the how and why, not the how to. The paper never
overstates: map and territory are kept apart as the abstraction-gaps ledger does, and the register's
words are used and no others.

## Definition of good enough

- D-1 to D-11 delivered; R-1 to R-22 pass; OD4 decided.
- The Story's four parts, the L-A to L-F structural checks, the L1 to L14 theorem-style blocks with
  proof sketches and script pointers, the Pareto and DEA contrasts, the prior-art table, the gaps
  appendix, the policy paragraph and a complete source map are present.
- The algorithm subsection is written against the delivered (and, by acceptance time, accepted) WP13 text.
- The search section is present and marked preliminary; Appendix G is a marked stub.
- No readability or aesthetic polishing beyond the structural checks; remaining improvements are
  listed for WP11 (whose cold-read grid does the content loops).

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above (a structural acceptance, not a sign-off on content or aesthetics).

## Order of work (default)

1. Early (parallel with WP13 and WP8a Amendment 2, files disjoint): `case.py` and its tests,
   bibliography, `myst.yml`, notebook and appendix shells, `tests/test_paper.py` skeleton, the
   archive of the WP7 notebook; read the `paper-sources/` text and draft `paper/source_map.md`.
2. Prose and appendices that need no new numbers: sections 1 to 5, 8 to 12; Appendices A, C, E, F, H.
3. Results: the L1 to L11 theorem-style blocks and Appendix B (statements first, then sketches,
   then the script pointers verified), then **last**: the algorithm subsection with Appendix D's
   certificates, written against the delivered WP13 material on `dev` and the L12 to L14 scripts.
4. The structural tests (R-17 to R-22) green; the cold-reader trials per level.
5. The search section (preliminary) and Appendix G stub; WP12's results fill them by an amendment
   or a follow-up when WP12 lands.

Dependencies: WP13 (delivered on `dev`; its acceptance gate still precedes WP10's acceptance, and the
text follows any change it makes); **WP8a Amendment 2** (the source of `paper-sources/` and the final
list of moved pages; this scope's moved-material table is provisional until it lands, and is re-pinned
by an amendment or in the source map); WP14 interface contract (paths and build commands; this draft
uses the paths above and re-pins when needed); WP12 (only for step 5's later fill). File ownership:
`paper/`, `examples/adcs/case.py`, `examples/adcs/archive/`, `tests/test_paper.py`,
`tests/test_case.py`, `docs/references.bib`, and `work-packages/WP10-*`. **Read, never edited:** every
`docs/*.md`, `docs/superpowers/notes/paper-sources/`, `docs/superpowers/notes/*`, `derivation/`,
`src/` (while WP13 runs).

## Agent's defaults

All marked *(default)* in this list; the supervisor approves or changes the list as one item.

- Notebook outputs are committed; seeds fixed; kernel is the project's `uv` environment.
- mystmd is installed from PyPI through a `paper` dependency group in `pyproject.toml` so every command stays `uv run myst ...`; `ipykernel` and `nbclient` in the same group.
- `paper/myst.yml` is standalone (not `extends: ../papers.yml`), with `project.index: paper.ipynb`, the supporting notebook as the second page, and `docs/references.bib` as the bibliography.
- Word count: prose and captions of `paper.ipynb` counted; abstract, code, tables of the appendices, references excluded. Target about 5,500 counted words (raised from 5,000 by the absorbed mathematics, the prior-art review and the gaps), the supervisor's cap of 6,000 unchanged; the budget table is the allocation, and detail that does not fit moves to Appendices B, D, E, H rather than the cap being raised.
- The theorem-style blocks: each lemma keeps its derivation tag (L1 to L14) and takes the paper's own sequential number (Definition 1, Lemma 2, Proposition 3, Theorem 4 and so on, in paper order); the author classes each as Lemma, Proposition or Theorem by its role (headline results as Theorems), with E-8's Lemma/Proposition/Corollary labels used inside the algorithm subsection with the L-tag alongside. The proof sketch is a short narrative paragraph; the script pointer is a one-line admonition giving the path, the `verify` entry point and the command; the full derivation output is in Appendix B or D.
- Source map at `paper/source_map.md`, mirrored as a table in Appendix F; its home labels are the section numbers and appendix letters above.
- Appendix letters A to H are stable labels, not the order of first citation.
- Search section inside the body at section 7, about 200 words, before the case; no results numbers.
- Badge implementation: a labelled admonition on each Results block (Derived / Numerical / Open) driven from a small table in the notebook's setup cell.
- Case tests live in `tests/test_case.py` beside `tests/test_paper.py`; `examples/adcs/k_terms.py` is kept and `case.py` imports from it rather than duplicating.
- The archive of the WP7 notebook is `examples/adcs/archive/` with the banner as its first cell.
- Figure files are generated by the notebook into `paper/figures/` and committed; Figure 1 is produced by a script derived from the spike's `make_schematics.py`; the plotting module's vocabulary is reused.
- Appendix G's later fill is an amendment to this package, unless WP12's scope assigns it otherwise.
- Cold-reader trials (decided) are structural: one fresh-context reviewer per level, given only what that level shows, reporting what the reader can and cannot state; findings feed `WP10-review.md` and WP11.
- Bibliography keys follow the repo's existing pattern (`authorYEARword`).
- The 15 sources not all cited; the paper cites the subset its text needs (supervisor: "keep all of them in our bibtex records").
- `method.md` "Prediction from configuration" has no home in the supervisor's provisional list; it goes to Results as one proposition or to the Discussion, wherever it reads better.

## Open decisions (for the supervisor)

- **OD4. PDF export through the SciPy typst template.** Options: (a) now, as an export in `paper/myst.yml` that WP10 builds and checks; (b) later, in WP8a/WP8b, with WP10 leaving the export block out.

Decided at the scope gate and no longer open (title and byline, Figure 1, the WP7 notebook, the tools
statement, how the drill-down levels are judged): see "Decided at the scope gate" above with the
supervisor's verbatim words. No new open decision arises from the separation of concerns: the paper's
sections, appendices and word allocation are defaults; the cap of 6,000 is unchanged.

## Gate outcomes (2026-11-08, `WP10-decisions.md`)

No open decision remains. OD4: "Later, once the content has settled" (no PDF export block in WP10;
on the punch list). Figure 1, the supervisor's specification: "the first panel is kinked and the
second panel is peicewise linear and the 3rd panel is a single horizontal like with colored regions.
this give the best intuition and accuracy balance" (pane 1 metric space with sharp corners between
the hyperbolic sheets; pane 2 log space with a piecewise-linear frontier, the normals and the
highlighted design's energy differential; pane 3 the chart with the frontier as one horizontal line
and the facets as coloured regions). The register table is compiled from the shared `glossary.yaml`
(WP8a Amendment 2 OD5). The docsite carries no citations into the paper for now (WP8a Amendment 2);
the paper may link to the docsite's user pages. Defaults approved as one item: "Yes, approve the
rest as listed". Decided 6, deferred 0, raised 0.
Correction at the gate (supervisor, verbatim): "the infrastructure is modeled on my scipy paper but
the we discussed the outline of paper seperately, its development based on my IEEE papers". Wherever
this scope says the paper is modelled on the SciPy article, read: the build infrastructure is; the
outline and development follow the IEEE-paper structure recorded in `WP10-decisions.md` and
`docs/superpowers/notes/paper-outline-v2-search.md`.

## Amendment 1 (2026-11-08; approved by the recorded act in `WP10-decisions.md`): the appendices as a bridge

Why: the supervisor's words after approval (`WP10-decisions.md`, "Appendices sketched in advance"):
no source map; a computational reproducibility appendix "that suffices to reproduce the materials in
the paper"; no appendix "for their own sake"; "their purpose is to build a bridge at an intermediate
depth between the paper and cloning the repo"; C and D apart, "disjoint and complementary to the
greatest extent possible"; "the larger register of prior art as an appendix", in which "for
everything in our extended lit review we need to clarify what our work does differently, extends,
adds". The sketch is `docs/superpowers/notes/paper-appendices-sketch.md`. Where this
amendment and the text above differ, the amendment governs.

What changes:

- **D-2 (the supporting notebook's appendices)** is replaced by the sketch's set, each written to
  the sketch's three tiers (main text, appendix, repository) and opening with its job: **A**
  notation and terms; **B** proofs (the fit and its geometry, L1 to L11; the solver for K > 1 and
  its three levels of guarantee, L12 to L14); **C** the case's model: how the table of metrics came
  to be; **D** extended results: what the method found in the table, with the solver's printed
  termination records; **E** assumptions and abstraction gaps; **F** computational reproducibility
  (new); **G** the register of prior art.
- **The proofs appendix (B) is step for step with the scripts** (the supervisor's rule,
  `WP10-decisions.md`): "every step in the prose proof should be mapped to a step in a sympy
  script. we should explain this at the beginning of that appendix then each proof is one file, and
  and each step in the proof is a line in that file. make sure you give yourself a tool for checking
  this we don't want any regressions to go unnoticed". This adds a deliverable, **D-12: the step
  tags in `derivation/lemma_01` to `lemma_14` and the proof-map checker with its committed record**
  (sketch, "B. Proofs, step for step with their scripts"), and **widens what WP10 may edit**: the
  fourteen lemma scripts, `derivation/axioms.py`, `derivation/run.py`, one new helper module and
  one new checker module under `derivation/`, and a new `tests/test_proof_map.py`, limited to
  giving each existing step its line, tag, claim and kind, and to declaring each ledger entry's
  SymPy form once in the ledger with the scripts taking it from there (the supervisor's decision:
  "Once, in the ledger"; a result with no useful SymPy form is declared as a named proposition). No mathematics, `TITLE`, `STATEMENT` or `AXIOMS_USED` changes; the
  interface contract's pinned names stay; `tests/test_derivation.py` and
  `tests/test_matches_derivation.py` are not edited and pass. D-10's pointers in the main text
  stay narrative.
- **D-9 and R-19 (the source map) are withdrawn**, with the table "Where the moved material goes"
  kept above as the author's working aid only, and "a complete source map" removed from the
  definition of good enough. `docs/superpowers/notes/paper-sources/` stays as working material.
- **The search's appendix (approved G) is withdrawn**; R-15 reads "Section 7 is labelled preliminary
  and contains no result numbers until WP12 lands". Whether the search's evidence becomes an
  appendix is for WP12's scope.
- **The verification audit (approved F)** is reduced to the commands and pass criteria in the new F;
  "what remains for a human" is a paragraph of the Discussion.
- **D-7 and R-10 (prior art)** read: section 2 keeps the concise record of the most immediately
  relevant material; Appendix G is the larger register (approved H), not exhaustive and saying so,
  with the dropped candidates left in the repository.
- **Section 11 of the main text** shrinks to a pointer to F and to the docsite; its words are not
  reallocated.
- **Letter references follow:** D-10 (full detail in B for L1 to L14); D-11 and R-20 (gaps in E,
  unchanged); R-11 (the printed certificates in D); the budget note (detail that does not fit moves
  to B, D, E, G).
- **New requirements.**
  - R-23 (reproducibility): Appendix F has a row for every figure, table and reported number of the
    paper (item, command or call, input, output), states the environment and the datasets'
    provenance, and every command in it runs. Checked by a test comparing the paper's figures and
    tables with the rows, and a smoke test of the commands.
  - R-24 (generated, not typed): the tables of C, D and F are produced by calls into the model, the
    ledger, the case module or the paper's cells. Checked by a test that the cells are calls;
    inspection.
  - R-25 (no appendix for its own sake): no appendix is empty or a stub; each opens with its job
    and is cited from the main text at least once. Checked by a test.
  - R-26 (C and D disjoint and complementary): C contains no fitted quantity and D no definition of
    the system; every table of D cites its dataset by the label C defines; no table or figure
    appears in both; each points to the other in its opening sentence. Checked by a test on the
    cells' calls and on the dataset labels; inspection.
  - R-27 (the register says what is different): every entry of Appendix G has the four fields, the
    field "what this work does differently, extends or adds" is never empty, the nearest neighbours
    named in the sketch each carry a "why this is not just X" sentence, section 2's table is a
    subset of the register with the same wording, and R-9's rule on the words "novel", "first" and
    "new" holds in G as in section 2. Checked by a test on the register's source file; inspection.
  - R-28 (proofs step for step): Appendix B opens with the rule and with what the correspondence
    does and does not establish; each proof names exactly one file; two results may share a file, a
    step's address being its file and its tag, unique within the file, and every step of every
    lemma file belonging to exactly one proof; prose steps and script steps correspond one to one
    and in order; each
    step is a line of code and shows its kind (computed, or by a declared axiom with the entry's
    name, class and citation), its formal claim and its line link, the last two compiled from the
    script; there is no prose-only kind, and a step that is neither is reported to the supervisor;
    every computed step passes; every step by a declared axiom names an existing ledger entry, and
    the entries a file's steps apply are exactly the entries in its `AXIOMS_USED`. Every ledger entry carries
    its SymPy form (or is declared as a named proposition), and a step by a declared axiom takes
    the entry from the ledger. Checked by the proof-map checker (`uv run python -m derivation.proofmap`)
    and `tests/test_proof_map.py`.
  - R-29 (no silent regression): the committed record holds a fingerprint of every step's script
    line and of its prose; the checker fails on any difference, on any unmatched, duplicated or
    reordered step, and on any broken tag; refreshing the record is an explicit command. Checked by
    tests that alter a copy of a script step, of a prose step, and of the order, and expect the
    checker to fail each time.
  - R-30 (pinned toolchain, stated): Appendix F states the Python version, the package manager and
    its version, the versions of the packages the results depend on most directly, and the commit,
    and points to `uv.lock`, `pyproject.toml` and `.python-version` for the rest; the stated
    versions are generated from the lock and equal it. Checked by a test.
  - R-31 (environment of record): a Dockerfile at the repository root (**D-13**, new; WP10 may add
    it and a `.dockerignore`) with its base image pinned by digest, installing the committed lock;
    the paper's committed outputs are produced in that container; the container builds and the
    paper executes in it locally (Colima) before delivery, with the commands and the result in
    `WP10-review.md`; Appendix F names it as the environment of record and states the known
    differences outside it (G-10). No image is published by this package (the supervisor: "we don't need the image on a registry
    just document it in the appendix for now and we can optionally publish it to a registry later"). Checked by a test of the
    Dockerfile's pins (digest present, lock used); the recorded local run; inspection.
- **Order of work:** the step tagging and the checker come first, by their own bounded
  implementer, before any proof is written in prose.
- **Dependency added:** C describes the model behind the data the paper uses (the frozen data until
  the swap gate; the WP15 model after it) and is regenerated at the swap.

Open decisions: none. Decided by the supervisor (`WP10-decisions.md`): C and D apart; the register as
an appendix; the proofs step for step with their scripts; cited results as steps in code; results
may share a script; each cited result's SymPy form declared once in the ledger; the pinned toolchain
stated in F; a pinned container image as the environment of record ("Reference environment now"). Defaults for approval as one item: those listed at the end of the sketch.

Clarification after approval (supervisor, verbatim, `WP10-decisions.md`): "its python we can handle
the axioms as import statements. if needed we can cite the import statements instead of the location
they are imported from". Within R-28: a lemma script imports the ledger entries it uses by name; the
appendix may cite the import line in the proof's file as the declaration's address; the checker
requires that a file's ledger imports, the entries its steps apply and its `AXIOMS_USED` are the same
set. No change to scope, deliverables or files.

Second clarification (supervisor, verbatim, `WP10-decisions.md`): "this also elegantly handles the
case where multiple lemmas use the same axiom, or where one lemmas result is important by another
proof script as a proven result". Within R-28: one ledger entry imported by several scripts is one
declaration cited from each; a script that builds on an earlier lemma imports that lemma's proved
result, and the step that applies it is of a third kind, *by a proved result*; the checker requires
that the imported result belongs to a lemma earlier in the chain, is exported by it as proved, and is
applied by a step. Today's four dependencies (L4 on L3, L7 on L1, L12 on L4, L14 on L12 and L13) are
declared this way. No change to scope, deliverables or files.

Third clarification, an instruction (supervisor, verbatim, `WP10-decisions.md`): "its a best bet to
factor helper tools into their own file". Within D-12: the helper functions defined in
`derivation/lemma_03_gradient_kkt.py` and imported by other lemma scripts move to
`derivation/sumtools.py`, and the shared index symbols to `derivation/symbols.py` (both files become
editable by WP10 for this move only), with no change in behaviour; the checker requires that a lemma
script imports from another lemma script nothing but a proved result. The existing derivation tests
stay unedited and pass, including the test that every load-bearing symbol assumption is declared.

## Amendment 2 (2026-11-08; defined and approved by the driver under the mandate, `release-candidate.md`; for the supervisor's review at the PR): closing what the tagging found

Why: the step tagging (D-12, commits d45ef4d and 78b29e2) recorded its findings in
`derivation/PROOF_MAP_FINDINGS.md` instead of relabelling them. They show where the scripts fall
short of the supervisor's rule ("every step in the prose proof should be mapped to a step in a
sympy script"; "proof steps that cite an inherited result are still steps ... which still needs to
happen in the code"): seven steps argued only in prose; premises carried as assumptions on local
symbols; ledger entries listed as used that no step depends on, which the tagging could only
reconcile with lines that do nothing; forced log expansions with no licence. The driver's own
instruction not to change `AXIOMS_USED` caused the do-nothing lines and is withdrawn here.

Principles (so that the result is true, not merely consistent):

1. **A listed axiom is one a step depends on.** Lines that apply an entry without effect are
   removed. `AXIOMS_USED` is corrected to the dependencies that exist. Where an entry is a real
   premise (positivity licensing a logarithm or a power), the operation takes the entry as its
   licence and a negative control shows the step fails without it, as L8 does for I6.
2. **Every step is a line.** Each of the seven prose-only steps becomes a computed step, or a step
   by a declared entry. Two are textbook results and become inherited entries with a verified
   citation (the first-order condition with a linear equality constraint; convexity as nonnegative
   second derivative along every line). The others are coded: the regrouping over facets from a
   declared partition relation; complementary slackness as a declared relation applied termwise;
   the strict inequality for n >= 2; the corollary on the shifted minimizer; the contrapositive
   and the efficiency deductions as propositional steps SymPy checks.
3. **No premise hides in a symbol.** A local symbol created with a sign or positivity assumption
   that stands for a premise is tied to the ledger entry, or to the earlier lemma's proved result,
   that licenses it; the checker fails on an unlicensed one. Forced expansions take a licence.
4. **Entries no proof consumes are said to be so.** They move to a class reported apart from the
   lemma-consumed entries, as the solver-level class already is, or leave the ledger; each is
   listed with its reason.
5. **The earlier instructions still to land:** the helper functions out of L3's script into the
   tools module, as its own commit first; earlier lemmas' results taken by import, with the step
   kind "by a proved result".

Guards. No `TITLE` or `STATEMENT` changes and no change to what is proved. **If a finding cannot be
closed without changing a statement (in particular the strict inequality of L5, which the statement
claims and the script does not assert), the work stops there and the driver takes it to the
supervisor.** Every change to an `AXIOMS_USED` list, every new or reclassified ledger entry and
every edit to `tests/test_derivation.py` (allowed only where a test pins a list this amendment
corrects; no negative control is removed) is listed in a table (before, after, why) in the
findings file, which becomes the record of how each finding was closed.

New requirement R-32: `derivation/PROOF_MAP_FINDINGS.md` shows every finding of sections 1 to 4
closed with its address, or open with the reason; the checker enforces principles 1 and 3 (no
do-nothing application; no unlicensed assuming symbol; imports, applied entries and `AXIOMS_USED`
equal); the chain and the suite pass; a fresh reviewer confirms that no statement changed and that
each closure is a real dependency, by withholding the entry and seeing the step fail.

## Amendment 3 (2026-11-09; the driver, under the mandate; for the supervisor's review at the PR): what the reviews and the cold reads added

Why: the second review (`WP10-review-2.md`, G-9) noted that WP10 had changed files its written scope
excludes. Those changes were ordered by the driver from the first review and from the triage of the
cold reads; this amendment records them as scope.

- **Reporting at reproducible precision.** The paper prints no number, status or hash beyond what
  reproduces: ranges over perturbed regenerations for the fragile quantities, bounds for numerical
  residues, and for the planted tables only what is the same on both platforms. A new entry in the
  abstraction-gaps ledger (the times read as first crossings) and its row in Appendix E.
- **The proofs.** L15, the descent guarantee as a script, added to the chain; ledger entries I10 to
  I12 and A8; the edits to `tests/test_derivation.py`, `proof-conventions.md` and
  `references-verified.md` that follow, each recorded in `derivation/PROOF_MAP_FINDINGS.md`.
- **A reading pass** on what cited sources say (Appendix G.2), with rows marked for the author.
- **The package and the docsite, from the cold reads (triage items 19 to 22):** fitted attributes at
  one term; `mean_slack_` for every K; error messages that say what to try; the docsite passage on
  choosing K, the temperature and the band; the Termination page; the interface contract at
  version 3. R-21's "no `docs/` edit but the bibliography" is lifted for these.
- **The word cap** counts the prose the page shows, generated sentences included, with per-section
  ceilings at the budgets plus 15 percent. The builder's own labels ("Theorem 3.", "Figure 2:") and
  the citations of Table 1's sources column are not counted. On that count the paper is at 5,881.
- **Environment of record:** linux/arm64 (the driver's spike); exact comparisons only there. The
  container deliverables (D-13, R-30's container part, R-31) stay open until container work resumes.

## Amendment 4 (2026-11-09; on the supervisor's direction, quoted in `WP10-decisions.md`, "The supervisor's reading of the abstract, second pass"; scoped by the driver): one name for the model class, the data as what is modelled, and the vocabulary review

**Why.** The supervisor read "A fitted generalized posynomial reference surface" and "a model of the
table, not the Pareto boundary, gives the table a coordinate system" in the abstract and found both
off. The first gave one object two names across the paper and the docsite. The second named the
table as the thing modelled, where the thing modelled is the data and the table is a view of it.

**Scope (the paper, and with it the docsite pages and the glossary that share the words; the
docsite files are WP8a's and change under this amendment by the same direction).**

- R-33. *The surface is posynomial.* The abstract says "a fitted posynomial reference surface". The
  Definition names the posynomial as the sum of monomials, the invariant V_K as its root, and the
  reference surface as the sum equal to one. Section 5 keeps one cited sentence that V_K is a
  generalized posynomial in the sense of Boyd et al. 2007, including the exact-maximum default.
  "Generalized" appears nowhere else for the surface or the model. The docsite's theory page
  follows. Sentences that report a source (Appendix G, Further reading) stay. *Check:* the
  vocabulary tool's `avoid` list carries the withdrawn phrases and passes; a scripted step or an
  existing one (L10: the power of the invariant is a posynomial) is cited beside the Definition.
- R-34. *The data is what is modelled; the table and the reading are views.* Wherever the surface is
  called a model of the table (abstract; section 1), it is a model of the data underlying the table
  (the evaluated designs), not of the Pareto boundary; the table and the interpretation drawn from
  it (the chart, the contending sets) are views of that data. The glossary's entry for the fitted
  reference surface says so. *Check:* no "model of the table" or "models the table" remains in any
  prose the tool reads; the abstract stays within its word ceiling.
- R-35. *The glossary carries the class words.* `glossary.yaml` gains entries for monomial,
  posynomial, generalized posynomial, geometric program and generalized geometric program (each with
  what it is not), and the fields `aliases`, `avoid`, the lists `assumed` and `stems`
  (`docs/superpowers/notes/vocabulary-review.md`). The interface contract is amended for the
  glossary's schema. *Check:* the glossary tests; the contract test.
- R-36. *The vocabulary review exists and has been run once in full.* The tool
  `scripts/check_vocabulary.py` as specified in the note, in the test suite, with tests that plant
  each kind of violation; one full pass of the tool and of the reading (fresh-context reviewers, in
  the browser, the three lists) over the paper, the supporting material, the docsite and the root
  page; every item triaged with one of the five dispositions; the record committed as
  `work-packages/WP10-vocabulary-review.md`. *Check:* the tool exits zero on the head of `dev`; the
  record lists every item with its disposition; the driver reads the record and the rendered pages.

**Non-goals.** No change to a mathematical statement, a number or a figure. No new term coined to
replace an old one where plain words serve. No rewrite of prose the review does not flag.

**Good enough.** R-33 to R-36 checked; the suite green on both platforms; word ceilings held; the
driver's own browser read of the abstract, section 1, the Definition, section 5 and the theory page.

