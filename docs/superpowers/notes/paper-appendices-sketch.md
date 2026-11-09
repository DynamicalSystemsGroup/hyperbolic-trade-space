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

On the driver's question why C and D are separate, and on the prior-art review:

"you can keep C & D apart but make their different purposes clear and make sure each does its job
well. they should by disjoint and complementary to the greatest extent possible."

"i do want the larger register of prior art as an appendix. its not supposed to be exhaustive thats
implausible but the idea is that we can keep a concise record of the most immediately relevant
material in the paper and expand to more literature in the appendix to make it clear we did our
homework. we don't want to be told this is just X where X is some existing work. for everything in
our extended lit review we need to clarify what our work does differently, extends, adds, etc."

On the default "proofs are written in prose; the SymPy output stays in the repository":

"every step in the prose proof should be mapped to a step in a sympy script. we should explain this
at the beginning of that appendix then each proof is one file, and and each step in the proof is a
line in that file. make sure you give yourself a tool for checking this we don't want any
regressions to go unnoticed"

On the driver's three kinds of step (computed, inherited, argued):

"proof steps that cite an inherited result are still steps. and in sympy we need to declare the
cited results as axioms to use them which still needs to happen in the code"

And on two results proved in one script:

"and if too results use the same script they can have the same file reference that should not break
our addressing scheme for proof steps"

On the defaults, put as one item of nine:

"you lumped a lot here. i think they are mostly fine. though make sure the reproducibility appendix
is specific about what out pinned tool chain is but it can provide a pointer to the uv.lock and/or
toml files required to reproduce. also may be worth awareness that on a mac. assuming we used a
linux box to stabilize our tests we may want to go even further to provide a docker image to make
this as reproducible as possible. (we have colima locally so we can test the use of a pinned image)"

And on the role of a pinned container image: "Reference environment now".

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
| C | full case detail (sensitivity, refits, regime tables, K = 1/2/3 table, propose-predict-check, candidates, nondominated counts) | split at the metric table: how the table came to be (C, named by the supervisor) and what the method found in it (D); disjoint and complementary (decided) |
| D | the algorithm in full with the certificates as printed by the code | divided: statements and proofs to B, printed certificates to D |
| E | the abstraction gaps and the simplifying assumptions | kept (E) |
| F | verification audit, what remains for a human; the source map as a table | replaced by the reproducibility appendix (F); source map withdrawn; "what remains for a human" stays in the Discussion |
| G | the search's evidence, a marked stub until WP12 | not written (see below) |
| H | the prior-art review in full | kept as the register of prior art (G), every entry saying what this work does differently, extends or adds (decided) |

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

### B. Proofs, step for step with their scripts

- **Job:** let a reader follow each proof in ordinary mathematics and, at any step, open the exact
  line of code that checks it.
- **Reader's question:** why is each numbered statement true, and where is each step checked?
- **Main text keeps:** each statement as a theorem-style block with hypotheses, a narrative proof
  sketch of a few sentences, and a one-line pointer to its file.
- **Appendix opens with the rule** (the supervisor's): each proof is one file; each step of the
  prose proof is one line of that file; the tag on a step is a link to that line; and what the
  correspondence does and does not establish (below).
- **Appendix carries,** per proof, in the paper's numbering: the statement with its hypotheses; its
  file; the proof as numbered steps, each with a sentence of prose, the step's formal claim, its
  kind, and its tag linking to the line; the ledger status of the statement. Two parts: the fit
  and its geometry (L1 to L11); the solver for K > 1 and its three levels of guarantee (L12 to L14,
  the stopping declaration).
- **Repository keeps:** the scripts, the axiom ledger, the runner, the checker.

How the correspondence is built (so that it can be checked, and cannot drift):

- **The address of a step is its file and its tag,** and the tag is unique within the file. Two
  results may therefore share a file (the supervisor's rule; today L14's script proves a
  proposition and its corollary): each names the same file, each owns its own steps, and no
  address collides. A later result in a file cites the earlier one as established; it does not
  re-own its steps.
- **In the script, a step is one line:** a call that carries the step's tag (L2.1, L2.2, ...), its
  formal claim as a short statement, its kind, and the condition SymPy checks. Today the scripts
  hold these as comments, intermediate results and 143 assertions across the fourteen files, with no
  tags; the work is to give each step its line and its tag, with the mathematics, the statements
  and the axioms used unchanged.
- **Every step is a line of code, including a step that cites a result** (the supervisor's rule).
  Two kinds, declared on the line and shown in the appendix: *computed* (SymPy derives the step's
  condition) and *by a declared axiom* (the line applies an entry of the axiom ledger, as code, to
  move the proof forward; the appendix shows the entry's name, its class and, for an inherited
  result, its citation). There is no third kind for arguments made only in prose: by the project's
  proof conventions a step that SymPy cannot derive becomes an explicit hypothesis or an inherited
  entry in the ledger. If the tagging finds a step that is neither, it is reported as a finding and
  taken to the supervisor, not given a softer label.
- **Where the scripts stand on this today:** inherited results are used in code at the point of
  use (for example L8 applies I6 as a substitution and has tests showing the proof fails without
  it; L12 carries I8 as an inequality), but each script writes the result's SymPy form itself. The
  ledger declares every entry in words only: none of its 23 entries carries a SymPy form, and no
  script takes an axiom from the ledger. A script's link to the ledger is its list of names.
- **In the appendix, the formal claim and the link are compiled from the script,** never typed: the
  claim shown beside a step is the script's own text, and the line number in the link is resolved
  at build time from the tag, so moving code cannot break or silently repoint a link.

The tool (the supervisor's instruction: no regression goes unnoticed):

- **A checker,** run as one command and by the test suite, that fails unless: every proof in the
  appendix names exactly one file; every step of every lemma file belongs to exactly one proof;
  within each proof, the prose steps and its script steps correspond one to one and in the same
  order, with no step on either side unmatched; every *computed* step's condition passes; every step *by a declared
  axiom* names a ledger entry that exists; the entries applied by a file's steps are exactly the
  entries the file lists as used (none listed and unused, none used and unlisted); and tags are
  unique and unbroken.
- **A committed record** of every step (its tag, a fingerprint of its line in the script and a
  fingerprint of its prose). The checker fails when either fingerprint differs from the record, so
  a script step cannot change without its prose being looked at again, nor the prose without the
  script; refreshing the record is an explicit command whose diff shows exactly which steps moved.
- **What it cannot check,** said plainly at the top of the appendix: that a sentence of prose means
  what its line computes. That reading is the human validation; the tool guarantees there is always
  exactly one line to read it against, and that the line passes.

### C and D: one boundary, two jobs

The boundary is the table of metrics. **C is how the table came to be; D is what the method found in
it.** The method treats everything in C as a black box, so a reader with a table from another model,
a physical test or a human assessment skips C and loses nothing in D; a reader who wants to judge
this case, or to build a comparable one from another system model, reads C and needs nothing from D.

Rules that keep them disjoint and complementary:

- C contains no fitted quantity: no exponent, temperature, value of V, facet, reach or share.
- D contains no definition of the system: no variable range, constraint, scenario constant or
  conditioning rule.
- C names each dataset once with a label, its size and its provenance; every table in D cites its
  dataset by that label and repeats nothing else from C.
- No table or figure appears in both. Anything computed from the metric table belongs to D, even
  when no fit is involved (the nondominated counts); anything that decides which rows are in the
  table belongs to C (feasibility).
- Each opens with one sentence stating its job and pointing to the other for the complementary half.

### C. The case's model: how the table of metrics came to be

- **Job:** let a reader judge whether the case is a fair test, and build a comparable one.
- **Reader's question:** what system produced this table, and by what steps?
- **Main text keeps:** section 8 in about 300 words: the cubesat, the two regimes, the ten
  attributes, feasibility, conditioning.
- **Appendix carries,** following the pipeline up to the method's input, as tables generated from
  the model and never typed:
  1. the configuration space: the design variables with their ranges and alternatives, per regime;
  2. the evaluation: the attributes with their definitions and units, and which part of the model
     or simulation produces each; the scenario constants;
  3. feasibility: the constraints, what the model checking establishes over the whole space, and
     how many sampled designs each constraint excludes;
  4. conditioning: each attribute's orientation, shift and scale into a strictly positive,
     larger-is-better metric, worked for this case;
  5. the datasets: label, regime, number of designs sampled and kept, seed, ledger entry and hash;
  6. the planted example: how the synthetic table with known facets is generated.
- **Repository keeps:** the SysML model file, the evaluation code, the experiment ledger, the data.
- **Dependency:** C describes the model behind the data the paper uses: the frozen data until the
  swap gate, the tidied model (WP15) after it. Because the tables are generated, the swap
  regenerates them.

### D. Extended results: what the method found in the table

- **Job:** let a reader check that the main text's summary of the analysis is fair, including the
  results that are mixed.
- **Reader's question:** what else was computed that the main text only summarizes, and does it
  change the reading?
- **Main text keeps:** section 9 in about 500 words: K = 1, K = 3, the regime comparison, the
  candidates, propose-predict-check in one paragraph, the nondominated counts.
- **Appendix carries,** each table citing its dataset by C's label:
  1. the selection of the temperature, and its re-selection at each K;
  2. the K = 1, 2, 3 diagnostic table; exponents, reach and facet share per term, per regime;
  3. the sensitivity variants and the per-category refits;
  4. the solver's termination records for the planted data and the case (status, gap, margin,
     radius), as printed by the code; recovery of the planted facets;
  5. the comparison with nondominated sorting (the counts on ten, four and two attributes);
  6. propose-predict-check, with its mixed result.
- **Repository keeps:** the case module, the record scripts, the full printed output.

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

- **Job:** let a reader regenerate every figure, table and reported number in the paper, in the
  same environment the authors used, without first learning the repository.
- **Reader's question:** what exactly do I run, in what environment, to get what the paper shows?
- **Main text keeps:** section 11 shrinks to a few sentences: everything is regenerable, the
  environment and the commands are in this appendix, use of the package on one's own table is on
  the docsite.
- **Appendix carries:**
  1. **the pinned toolchain, stated specifically** (the supervisor's instruction): the Python
     version, the package manager and its version, the versions of the packages the results depend
     on most directly, and the commit; with pointers to the files that pin everything else
     (`uv.lock`, `pyproject.toml`, `.python-version`), not a copy of them;
  2. **the environment of record: a pinned container image** (the supervisor's decision,
     "Reference environment now"): a Dockerfile in the repository with its base image pinned by
     digest and the locked environment installed inside; the paper's committed numbers and figures
     are produced in that container; how to build it and run the paper in it; what is known to
     differ outside it (the tied rows of gap G-10 on other platforms);
  3. one table with a row per figure, table and reported number: the paper item, the single
     command or function call that produces it, the file it reads, the output it writes;
  4. how to rebuild the paper itself; how to run the verification scripts, the proof-map checker
     and the test suite, with what a pass looks like;
  5. the provenance of each dataset (its ledger entry and hash) and the optional command that
     regenerates it; expected run times.
- **Repository keeps:** the code, the tests, the lock file, the Dockerfile, the ledger.
- **Check:** a test that every figure and table in the paper has a row and that every command in
  the table runs; a test that the toolchain stated in the appendix equals what the lock file and
  the Dockerfile pin; the container built and the paper run in it locally (Colima) before delivery.
- **Not in this package:** publishing the image to a registry (outward-facing; a release matter).

### G. Register of prior art

- **Job:** show that the homework was done, and answer in advance the objection that this work is
  "just X" for some existing X.
- **Reader's question:** how does this work stand to the method I already know?
- **Main text keeps:** section 2 in about 600 words: a concise record of the most immediately
  relevant material: the family table, the Pareto and DEA paragraphs, the lineage.
- **Appendix carries:** the larger register, grouped by family. One entry per work or family, each
  with the same four fields: what it does, in a sentence; what this work shares with it or takes
  from it; **what this work does differently, extends or adds**; the citations. The nearest
  neighbours (Pareto methods, DEA, PCA and log-ratio analysis, geometric programming and max-affine
  fitting, production and distance functions, tradespace exploration) get a plain "why this is not
  just X" sentence. It opens by saying it is not exhaustive and how the entries were chosen.
- **Rules:** no entry without the third field; the main text's table is a subset of the register,
  with the same wording; differences are stated as differences, without the words "novel", "first"
  or "new" about the method (the approved R-9 stands); every cited source has a verified record in
  the bibliography.
- **Repository keeps:** the long review with its dropped candidates
  (`docs/superpowers/notes/paper-sources/literature.md`), the bibliography of all adopted sources.

## What is not an appendix

- **The source map** (approved D-9, R-19): withdrawn on the supervisor's word. The snapshot of the
  moved pages stays in `docs/superpowers/notes/paper-sources/` as the author's working material.
- **The search's evidence** (approved G): not written until WP12 has evidence.
- **The verification audit** (approved F: tests by area, the scikit-learn checks): reduced to the
  commands and pass criteria in F; the listing itself is the repository's.
- **"What remains for a human"**: a paragraph of the Discussion (verify versus validate), not a
  table in an appendix.

## Open questions

None. Decided in the supervisor's words above: C and D apart; the register of prior art as an
appendix; the proofs step for step with their scripts; cited results as steps in code; results may
share a script. And, by his answer "Once, in the ledger" to the driver's question where a cited
result's SymPy form is declared: each ledger entry carries its SymPy form, and every script takes
it from the ledger, so the declaration and the use are one object. A result with no useful SymPy
form is declared as a named proposition, and the step that applies it says so.

## Defaults in this sketch (for approval as one item with the amendment)

- Letters A to G in the order above. G was the search's appendix in the approved scope; nothing has
  been built against the old letters.
- B (the supervisor's rule, not a default): each proof is one file, each prose step one line of
  it, explained at the head of the appendix, with a checker. Defaults under that rule: tags of the
  form L2.1; the two kinds of step (computed, by a declared axiom) and no prose-only kind; the
  step's formal claim and the line link compiled from the script; the committed record of
  fingerprints; the checker as a module beside the runner and a test in the suite.
- Two results sharing a script (the supervisor's rule, not a default) keep the file's tags in one
  sequence (L14.1, L14.2, ...), each step owned by one result; no file is split and the numbering
  L1 to L14 is unchanged.
- The main text's proof sketches stay narrative and are not step-tagged; they point to the appendix
  entry and the file.
- The sources of the inherited axioms are cited in B, at the step that inherits them.
- The ledger's forms (the supervisor's decision, "Once, in the ledger"); defaults under it: each
  entry's form is built from the shared symbols, so one declaration serves every size; a step by a
  declared axiom takes the entry from the ledger on its line; the checker fails if an entry has no
  form, or if a step names an entry without taking it from the ledger; the existing negative
  controls (a proof failing when its axiom is withheld) are kept as they are.
- The step tagging of the fourteen scripts is done first, by its own bounded implementer, before
  any proof is written in prose; together with the ledger's forms; it changes no mathematics, statement or axiom list,
  and the existing derivation tests stay as they are and pass.
- The algorithm's statements and proofs sit with the other proofs (B); its printed certificates sit
  with the other printed results (D).
- C, D and F are generated from the model, the ledger, the case module and the paper's own cells;
  nothing in them is typed by hand.
- The boundary between C and D is the metric table, with the five rules above; the planted example
  follows the same boundary (its construction in C, its results in D).
- The register (G) and the main text's family table are compiled from one skimmable source file
  (`paper/prior_art.yaml`), as the notation table is from `glossary.yaml`, so the two cannot drift
  and the "differs, extends or adds" field can be tested for presence.
- The dropped candidates of the long review stay in the repository and are not in G.
- Section 11 of the main text shrinks; its freed words are not reallocated (the cap is a cap).
- The container (the supervisor's decision; defaults under it): the environment of record is
  linux/amd64, the same as the CI runner, with what is observed on other platforms stated beside
  it; the image installs with `uv sync --locked` from the committed lock; the stated toolchain is
  generated from the lock and the Dockerfile, not typed. If the amd64 image cannot be run workably
  on this Mac, that comes back to the supervisor before anything else is chosen.
