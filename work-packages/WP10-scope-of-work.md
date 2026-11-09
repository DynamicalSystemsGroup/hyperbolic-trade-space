<!-- The first draft of this file (written as WP9, the readability package) was superseded on 2026-11-08 by the supervisor's redirection (WP10-decisions.md) and is replaced by this draft; it remains in git history. -->

# WP10 — Scope of work: The paper, working draft

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`) |
| **Approval record** | Verbal approval in chat, quoted verbatim in `work-packages/WP10-decisions.md` |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `work-packages/WP10-decisions.md`, after `work-packages/WP10-review.md` |

Replaces the superseded first draft in `work-packages/WP10-scope-of-work.md` (history only; its readability-loop content is WP11's).

## Purpose

The research is hardened (WP1 to WP9, WP13); the supervisor views the paper as "a narrative view on
the research itself" (`WP10-decisions.md`, "Sequencing"). This package writes that narrative as a
working draft: a mystmd article in which the notebook is the paper, in the manner of his SciPy 2026
proceedings article, organized as an academic paper (motivation, prior art, notation, definitions,
results, case, discussion, future work, works cited) with every claim backed by computationally
verifiable supporting material in the repository. Presentation polish is WP11's; deployment is WP8's.

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
   unsupervised; the three earlier spines (tensions not variance; n-lemmas found; a learned chart) as sections.
4. **Case** at K = 1 and K = 3 (the cubesat, two regimes). **Final remark** (the hook): a novelty or
   impact score for new capabilities from how far above V = 1 they are forecast to sit.

## Reader model (supervisor, `WP10-decisions.md`, "Redirection")

Assumed mathematics: multivariate calculus, linear algebra, convex optimization. Notation anchored on
the scikit-learn documentation and glossary, and on Boyd and Vandenberghe for mathematics and
algorithm descriptions. The paper must read "well" at six drill-down levels: **L-A** abstract and hero
image; **L-B** headers, main results and figures; **L-C** the whole paper; **L-D** the paper and the
supporting materials ("computationally verifiable appendices"); **L-E** pull the code and reproduce;
**L-F** pull the code and adapt it to one's own case.

## Goals

- G1. A mystmd article `paper/paper.ipynb` (notebook is the paper), about 5,000 words (cap 6,000), in the
  section order of `paper-outline-v2-search.md` reconciled with the external reviewer's paper map
  (E-10), that tells the Story above and reads well at L-A to L-F.
- G2. A supporting notebook `paper/supporting_material.ipynb` of lettered, computationally verifiable
  appendices (A to F) that the paper cites claim by claim.
- G3. Every computation the paper shows is a call into a tested module `examples/adcs/case.py` (cubesat
  specifics as data), so another table runs through the same functions.
- G4. The prior work is a prior-art review by family (claiming nothing as novel), with the Pareto and
  DEA contrasts, and the fifteen state-of-practice sources plus Miettinen, Ehrgott and the three
  DEA references are in `docs/references.bib` and `docs/literature.md`.
- G5. Mathematical statements are marked Derived / Numerical / Open (E-10), the algorithm part of the
  Results follows E-8's structure (after WP13 lands), and every simplifying assumption is named where
  made, defended there in a sentence, and taken up in Future work with how to go beyond it.
- G6. The trade-off-aware search appears as a section marked preliminary until WP12 lands.
- G7. A test file that guards the paper's structure, budget and register so later loops (WP11) cannot
  silently break them.

## Non-goals

- Readability loops with the supervisor and rendered-browser verdicts (WP11); the paper's publication
  under `/paper/`, the Pages workflow and the docsite (WP8a); PDF/release machinery beyond what an
  Open decision below selects; PyPI and the release (WP8b).
- Any change to `docs/method.md`, `derivation/`, or the package source while WP13 runs; new
  mathematics (the paper cites lemmas, it does not add them); the search's code, lemmas and results (WP12).
- Submission to a venue or venue-specific compliance (the SciPy proceedings are the structural
  reference only).
- Reworking the system model (the separate SysML tidying package); a rewrite of the data or the
  simulator; K selection rules, scalability, kernels beyond what the discussion states.
- Claiming novelty; the response letter to the external reviewer (WP13).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/paper.ipynb`, executed, outputs committed, with the front matter (title, abstract, keywords, abbreviations), numbered definition/lemma/figure blocks with captions, Derived/Numerical/Open badges, the cross-references to Appendices A to F | G1, G5, G6 |
| D-2 | `paper/supporting_material.ipynb`: A the register (`docs/superpowers/notes/notation.md`) as a table; B the derivation ledger and each lemma's output (L1 to L14); C full case detail (sensitivity variants, per-category refits, regime tables, the K = 1/2/3 diagnostic table, propose-predict-check with its mixed result, candidates, the nondominated counts); D verification audit (tests by area, lemma PASS list, sklearn checks and expected failures, cross-checks, the WP13 certificates on the planted data and cubesat tables); E what remains for a human; F the search's evidence (a marked stub until WP12 lands) | G2, G5, G6 |
| D-3 | `paper/myst.yml` (project, authors, keywords, abbreviations, bibliography, build settings), modelled on `hc-scipy-2026/papers/michael_zargham/myst.yml` | G1, G2 |
| D-4 | `examples/adcs/case.py`: load, feasibility, conditioning, temperature selection and fit, K sweep, report and figure helpers, regime comparison, candidates, propose-predict-check, nondominated counts; cubesat specifics (attribute names and orientations, feasibility checks, configuration columns, data paths) as data; lifts from the WP7 notebook and `examples/adcs/k_terms.py` | G3 |
| D-5 | `docs/references.bib` additions (fifteen sources; Miettinen 1998; Ehrgott 2005; Banker, Charnes and Cooper 1984; Allen et al. 1997; Dyson et al. 2001) under the WP5 rule; `docs/literature.md` new section "State of practice in trade studies"; plus the search-family entries of `search-prior-art.md` only if the paper cites them | G4 |
| D-6 | `tests/test_paper.py` (and tests of D-4) | G7, G3 |
| D-7 | The prior-art review table (paper section 2) and the Pareto and DEA paragraphs | G4 |
| D-8 | `WP10-review.md` evidence inputs: the L-A to L-F check results | G7 |

## Paper structure (reconciled outline v2 and E-10)

Section word budgets are defaults; total about 5,150 against the 5,000 target (within 10 %) (abstract, captions of
code-free figures, tables in appendices, references and appendices excluded from the count *(default)*).

| § | Title | Budget | Content and badge |
|---|---|---|---|
| Abstract + Fig. 1 | | 200 | the Story in six sentences, the cubesat finding in one sentence; E-9 strengths as framing |
| 1 | The decision problem | 600 | why; contribution; main-results list (the L-B anchor); organization |
| 2 | Prior art, by family | 600 | the table (outline v1 prior-art table plus the three search families when cited): produces / shares / differs / cites; the Pareto and DEA paragraphs |
| 3 | Preliminaries and notation | 400 | pipeline c → a → m; assumptions A1 to A6 (E-10); notation table anchored on sklearn glossary and Boyd and Vandenberghe; the register phrases |
| 4 | Definitions | 400 | numbered definitions (invariant form, posynomial, τ and κ, chart, n-lemma, reach, share, exchange rate, ascent direction) |
| 5 | Results | 1,000 | L1 to L11 as numbered blocks with proof dropdowns, badge Derived; the K > 1 algorithm in E-8 form (Lemma 1, Lemma 2, Proposition 3, Corollary 4, the stopping declaration; *written last, after WP13 lands*), badge Numerical where only observed; Open: Q1 to Q4 |
| 6 | Search of the design space (preliminary) | 250 *(default)* | the nested loops, the procedure, the honest limits; no results until WP12 |
| 7 | Case construction | 350 | cubesat, two regimes, ten attributes, feasibility, conditioning, temperature; planted multi-facet example |
| 8 | Case analysis | 650 | K = 1, K = 3, regime comparison, candidates, propose-predict-check; Pareto counts from `case.py` |
| 9 | Discussion | 400 | interpretation as human validation; what the decision-maker holds; limits; verify versus validate; one line on log-convexity and holes |
| 10 | Reproducibility and your own case | 200 | exact commands; the recipe and `case.py` interface |
| 11 | Future work and final remark | 300 | organized by named assumptions; the final remark hook |

(Exact allocation is a default; the cap of 6,000 is the supervisor's.)

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Section order matches the table above; headers are the L-B skim. | `tests/test_paper.py` reads the notebook's markdown headers |
| R-2 | Body prose is at most 6,000 words and within 10 % of 5,000 unless the supervisor changes it; per-section budgets reported. | test counting the counted cells |
| R-3 | Every code cell in `paper.ipynb` makes exactly one call into `case.py` (or the package), and defines nothing else. | test parsing cell ASTs |
| R-4 | Every figure has a numbered, self-contained caption and is referenced in the text; every definition, lemma and appendix reference resolves. | test; `myst build --check` |
| R-5 | The prose uses the register's phrase for each object and contains none of the register's forbidden phrases; the three objects (surface, frontier, facet-level) are distinguished as the register says. | test using the register's phrase lists |
| R-6 | Each simplifying assumption on the supervisor's list is named in the body where made, defended in a sentence there, and appears in Future work with a way beyond it. | test for the eight assumptions' markers; inspection |
| R-7 | Each of Derived / Numerical / Open applied to each Results statement matches the ledger status (proved / inherited / observed); Q1 is marked Open and not pursued. | test cross-checking against `derivation/axioms.py` and `abstraction-gaps.md` |
| R-8 | The Pareto contrast (object, question, scale with d, noise, what is returned, relation, generation vs identification) and the DEA contrast appear in section 2 in one compressed paragraph each; nondominated counts (671/706; 146/706; 8/706) are produced by `case.py`, not typed. | test of `case.py` outputs against these values; inspection |
| R-9 | The prior-art table has a row per family listed in `paper-outline-v1-baseline.md`, each with produces / shares / differs / cites, and claims nothing as novel (no "novel", "first", "new" claims about the method). | test on the table; inspection |
| R-10 | All fifteen state-of-practice, two multiobjective and three DEA records are in `docs/references.bib` with a resolved DOI or stable URL and a `verified` field, even if the text cites only a subset; `docs/literature.md` has the new section. | `tests/test_references.py` |
| R-11 | The algorithm part of Results follows E-8, cites the WP13 lemmas L12 to L14 and states the three-level claim with the stopping declaration; Appendix D reports the certificates for the planted data and cubesat tables. | inspection against `docs/method.md`; test of cited lemma ids |
| R-12 | Drill-down checks: L-A: abstract within 200 words and Figure 1 present with caption; L-B: headers, main-results list and figure captions alone state the Story and the finding; L-C: no unresolved forward reference; L-D: every appendix cited at least once from the body and every lemma has a runnable proof dropdown; L-E: each command in section 10 exists and runs in the smoke test; L-F: `case.py` runs end to end on a second table (the planted data) with no cubesat-specific edit. | `tests/test_paper.py`; D-8 |
| R-13 | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check` pass; notebooks execute from a clean kernel with committed outputs equal to a re-run (seeded). | local checks; an execution test marked slow |
| R-14 | Search section and Appendix F are labelled preliminary and contain no result numbers until WP12 lands. | test for the label; inspection |
| R-15 | No AI attribution in commits or documents, per the repository's rule (subject to OD5). | attribution grep in the local checks |

## Definition of good

A reader who stops at the abstract and Figure 1 knows the decision problem, the idea (tensions, not
variance) and the finding; who skims headers and figure captions can state the main results; who reads
the whole paper has an academic paper's argument, spaced out with MyST affordances, with one
claim per block and each claim one click from its lemma output or test; who pulls the code reproduces
every number and, with the `case.py` recipe, runs their own table. The paper never overstates: map and
territory are kept apart as the abstraction-gaps ledger does, and the register's words are used and no others.

## Definition of good enough

- D-1 to D-8 delivered; R-1 to R-15 pass; every OD below decided.
- The Story's four parts, the six reader levels' checks (R-12), the Pareto and DEA contrasts and the
  prior-art table are present.
- The Results' algorithm subsection is written against the accepted WP13 text.
- The search section is present and marked preliminary; Appendix F is a marked stub.
- No readability polishing beyond R-12; remaining improvements are listed for WP11.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Order of work (default)

1. Early (parallel with WP13, files disjoint): `case.py` and its tests, bibliography and literature
   section, `myst.yml`, notebook and appendix shells, `tests/test_paper.py` skeleton.
2. Prose and appendices A, B, C, E; sections 1 to 4, 7 to 11.
3. Results lemma blocks L1 to L11, then **last**, after WP13 is accepted: the algorithm subsection,
   Appendix D's certificates, and the section 2 to 5 text that depends on the WP13 register.
4. The search section (preliminary) and Appendix F stub; WP12's results fill them by an amendment
   or a follow-up when WP12 lands.

Dependencies: WP13 (accepted before step 3), WP14 interface contract (paths and build commands; not
yet scoped, so this draft uses the paths above and re-pins when WP14 lands), WP12 (not yet scoped;
only for step 4's later fill). File ownership: `paper/`, `examples/adcs/case.py`, `tests/test_paper.py`,
`docs/references.bib`, the new section of `docs/literature.md`. Not touched: `docs/method.md`,
`derivation/`, `src/` while WP13 runs.

## Agent's defaults

All marked *(default)* in this list; the supervisor approves or changes the list as one item.

- Notebook outputs are committed; seeds fixed; kernel is the project's `uv` environment.
- mystmd is installed from PyPI through a `paper` dependency group in `pyproject.toml` so every command stays `uv run myst ...`; `ipykernel` and `nbclient` in the same group.
- `paper/myst.yml` is standalone (not `extends: ../papers.yml`), with `project.index: paper.ipynb`, the supporting notebook as the second page, and `docs/references.bib` as the bibliography.
- Word count: prose and captions of `paper.ipynb` counted; abstract, code, tables of the appendices, references excluded; the budget table above is the allocation.
- Search section inside the body at section 6, about 250 words, before the case; no results numbers.
- Badge implementation: a labelled admonition on each Results block (Derived / Numerical / Open) driven from a small table in the notebook's setup cell.
- Case tests live in `tests/test_case.py` beside `tests/test_paper.py`; `examples/adcs/k_terms.py` is kept and `case.py` imports from it rather than duplicating.
- Figure files are generated by the notebook into `paper/figures/` and committed; the plotting module's vocabulary is reused.
- Appendix F's later fill is an amendment to this package, unless WP12's scope assigns it otherwise.
- Cold-reader trial for the drill-down levels follows OD6.
- Bibliography keys follow the repo's existing pattern (`authorYEARword`).
- The 15 sources not all cited; the paper cites the subset its text needs (supervisor: "keep all of them in our bibtex records").

## Open decisions (for the supervisor)

- **OD1. Title and byline.** What are the paper's title, subtitle, author list, affiliation and ORCID? Options: (a) a title you give, with you as sole author, Dynamical Systems Group as affiliation; (b) a title you give with additional co-authors you name; (c) a working title now, final at WP11.
- **OD2. Figure 1 (the hero image for L-A).** Options: (a) the cubesat trade space with the K = 3 fitted facets and the contending metrics named (one chart from the K = 3 record); (b) a schematic of the idea (data cloud, facets, chart coordinates, V = 1 at the frontier) with no case data; (c) a pair: facets of the trade space and the frontier rising over rounds of the search (needs WP12's results); (d) your own choice.
- **OD3. The WP7 notebook (`examples/adcs/adcs_trade_study.ipynb`) when the paper lands.** WP7 was accepted "as the baseline ... notebook retired when the WP9 paper lands". Options: (a) delete it (git history keeps it) together with `tests/test_notebook.py` guards moved into `tests/test_paper.py`; (b) move it to an archive directory with a banner pointing to the paper; (c) keep it in place as the long tutorial and link it from the paper's section 10.
- **OD4. PDF export through the SciPy typst template.** Options: (a) now, as an export in `paper/myst.yml` that WP10 builds and checks; (b) later, in WP8a/WP8b, with WP10 leaving the export block out.
- **OD5. Tools statement.** The SciPy article carries an Acknowledgments section naming the AI tools and process used; this repository's rule is no AI attribution on documents. Options: (a) no tools statement in the paper; (b) a tools-and-process statement in Acknowledgments in the manner of the SciPy article, in your words; (c) none now, decided at submission.
- **OD6. How the drill-down levels are judged at acceptance.** Options: (a) the automated checks R-12 only, with your reading at WP11; (b) the automated checks plus a cold-reader trial per level by a fresh-context reviewer given only what that level shows, reported in `WP10-review.md`; (c) the automated checks plus your own reading of the draft before acceptance.
