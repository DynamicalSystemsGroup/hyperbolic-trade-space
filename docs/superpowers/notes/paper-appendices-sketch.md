# Note: sketch of the paper's appendices (2026-11-08, for the supervisor's review)

Drafted by the driver as input to WP10 Amendment 1 (draft, not approved). Nothing here is executed
before the supervisor has reviewed it.

## The supervisor's words (2026-11-08, after WP10's approval)

"the paper will have several appendices which will keep us from crowding the main text. the full
proofs, the computational reproducibility, the full model for the case and more can go in
appendices. it make be worth sketching the appendices in advance to help prevent cluttering the main
paper text"

"i don't think i need a source map of what was moved from the docs. i do want a computational
reproducibility appendix that suffices to reproduce the materials in the paper. i am not sure what G
is supposed to be. its okay to work on sketching the appendices but i don't want to jam any in for
their own sake. their purpose is to build a bridge at an intermediate depth between the paper and
cloning the repo."

## The test each appendix must pass

An appendix exists only if it answers a question that a reader of the paper has and that the main
text is too short to answer, at a depth short of reading the repository. So each one below is laid
out as three tiers: what the main text keeps, what the appendix carries, what stays in the repository
and is only pointed to. An appendix with nothing in its middle tier is not written.

This also says what the main text must not carry: anything in the middle column below.

## What the approved scope had (D-2, appendices A to H), and what this sketch does with each

| Approved | Content in the approved scope | In this sketch |
|---|---|---|
| A | the register as a table | kept (A) |
| B | conditions of the theory, full statements and proofs of L1 to L14, `derive`/`verify` output, ledger, lemma coverage | kept, and takes the algorithm's guarantees from D (B) |
| C | full case detail (sensitivity, refits, regime tables, K = 1/2/3 table, propose-predict-check, candidates, nondominated counts) | split: the case's model (C, new, named by the supervisor) and the extended results (D) |
| D | the algorithm in full with the certificates as printed by the code | divided: statements and proofs to B, printed certificates to D |
| E | the abstraction gaps and the simplifying assumptions | kept (E) |
| F | verification audit, what remains for a human; the source map as a table | replaced by the reproducibility appendix (F); source map withdrawn; "what remains for a human" stays in the Discussion |
| G | the search's evidence, a marked stub until WP12 | not written (see below) |
| H | the prior-art review in full | open: see the one question below |

What G was meant to be: the round-by-round tables and convergence diagnostics of the trade-off-aware
search (outline v2; WP12). WP12 is not scoped, so today it would be an empty, labelled stub. By the
test above it is not written. Section 7 of the main text stays short and marked preliminary; whether
the search's evidence becomes an appendix is decided in WP12's scope, when there is evidence.

## The sketch

### A. Notation and terms

- **Reader's question:** what exactly does this symbol or word mean in this paper?
- **Main text keeps:** section 3's notation paragraph and the symbols introduced where first used.
- **Appendix carries:** one table: symbol or term, meaning in this paper, where defined, the
  scikit-learn or Boyd and Vandenberghe usage it anchors to. Compiled from `glossary.yaml`, never
  typed.
- **Repository keeps:** the register's reasoning and its phrase lists
  (`docs/superpowers/notes/notation.md`).

### B. Proofs

- **Reader's question:** why is each numbered statement true, in full?
- **Main text keeps:** each statement as a theorem-style block with hypotheses, a narrative proof
  sketch of a few sentences, and a one-line pointer to its script.
- **Appendix carries:** in the paper's numbering, each statement restated with its hypotheses and a
  complete proof in ordinary mathematical prose; its ledger status (proved, inherited from a cited
  source, or observed only); the one-line result of its verification script. Two parts: the fit and
  its geometry (L1 to L11); the solver for K > 1 and its three levels of guarantee (L12 to L14, the
  stopping declaration).
- **Repository keeps:** the SymPy scripts and their full output (`derivation/`), the axiom ledger.

### C. The case's model

- **Reader's question:** what system produced these numbers, precisely enough to judge the case or
  to build a comparable one?
- **Main text keeps:** section 8 in about 300 words: the cubesat, the two regimes, the ten
  attributes, feasibility, conditioning, the temperature.
- **Appendix carries:** tables generated from the model, not typed: the configuration variables with
  their ranges and alternatives; the attributes with their definitions and units; the feasibility
  constraints and how many designs each excludes; the scenario constants; the conditioning of each
  attribute into a metric (orientation, shift, scale), worked for the case; the planted multi-facet
  example's construction.
- **Repository keeps:** the SysML model file, the evaluation code, the experiment ledger, the data.
- **Dependency:** the appendix describes the model that produced the data the paper uses. That is
  the frozen data until the swap gate, and the tidied model (WP15) after it; because the tables are
  generated, the swap regenerates them.

### D. Extended results of the case

- **Reader's question:** what else was run that the main text only summarizes, and does it change
  the reading?
- **Main text keeps:** section 9 in about 500 words: K = 1, K = 3, the regime comparison, the
  candidates, propose-predict-check in one paragraph, the nondominated counts.
- **Appendix carries:** the full tables behind those sentences: the K = 1, 2, 3 diagnostic table
  with the temperature re-selected at each K; exponents, reach and facet share per term in both
  regimes; the sensitivity variants and per-category refits; propose-predict-check with its mixed
  result; and the solver's termination records for the planted data and the cubesat tables (status,
  gap, margin, radius) as printed by the code.
- **Repository keeps:** the datasets, the case module, the record scripts.

### E. Assumptions and abstraction gaps

- **Reader's question:** under what assumptions do the formal statements carry over to data, and how
  sensitive are the results to each?
- **Main text keeps:** the one "Map and territory" paragraph in section 3; each simplifying
  assumption named and defended in a sentence where it is made; Future work organized by them.
- **Appendix carries:** one table, a row per gap (G-1 to G-16): the formal assumption, why it cannot
  be established on data, what was measured about its sensitivity on the planted data and the case,
  and how to go beyond it.
- **Repository keeps:** the ledger with its evidence (`docs/superpowers/notes/abstraction-gaps.md`).

### F. Computational reproducibility

- **Reader's question:** how do I regenerate every figure, table and reported number in this paper
  without first learning the repository?
- **Main text keeps:** section 11 shrinks to a few sentences: everything is regenerable, the
  commands are in this appendix, use of the package on one's own table is on the docsite.
- **Appendix carries:** the environment (the tagged commit, Python version, `uv sync --locked`);
  one table with a row per figure, table and reported number: the paper item, the single command or
  function call that produces it, the file it reads, the output it writes; how to rebuild the paper
  itself; how to run the verification scripts and the test suite, with what a pass looks like; the
  provenance of each dataset (its ledger entry and hash) and the optional command that regenerates
  it; expected run times; known platform differences.
- **Repository keeps:** the code, the tests, the lock file, the ledger.
- **Check:** a test that every figure and table in the paper has a row, and that every command in
  the table runs.

## What is not an appendix

- **The source map** (approved D-9, R-19): withdrawn on the supervisor's word. The snapshot of the
  moved pages stays in `docs/superpowers/notes/paper-sources/` as the author's working material.
- **The search's evidence** (approved G): not written until WP12 has evidence.
- **The verification audit** (approved F: tests by area, the scikit-learn checks): reduced to the
  commands and pass criteria in F; the listing itself is the repository's.
- **"What remains for a human"**: a paragraph of the Discussion (verify versus validate), not a
  table in an appendix.

## The one question for the supervisor

The approved H is the prior-art review in full: the by-family review at length, the state-of-practice
section, the dropped candidates, the sources of the inherited axioms. Section 2 of the main text
already carries the family table, the Pareto and DEA paragraphs and the lineage in about 600 words,
and every adopted source stays in the bibliography whether or not the text cites it. H is a bridge to
the literature, not to the repository, so the test above does not settle it.

## Defaults in this sketch (for approval as one item with the amendment)

- Letters A to F in the order above; letters are assigned once and not reused for something else.
- B holds proofs in prose, not SymPy output; the scripts' output is the repository's.
- The algorithm's statements and proofs sit with the other proofs (B); its printed certificates sit
  with the other printed results (D).
- C and F are generated from the model, the ledger and the paper's own cells; nothing in them is
  typed by hand.
- C describes the model behind the data in use at the time, and is regenerated at the swap gate.
- Section 11 of the main text shrinks; its freed words are not reallocated (the cap is a cap).
