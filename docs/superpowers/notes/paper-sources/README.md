# Paper sources: pages and sections that left the docsite

Provenance note for the author of the paper (WP10). Each file here is a verbatim snapshot of a docsite
page as it stood at commit `d7673c6` (the WP13-accepted text); none was changed since. Git history
keeps the originals. This directory is read-only after this commit and is excluded from the site by the
`superpowers/` rule.

The rule behind the split: what a package user needs to run, read or trust a result stays on the
docsite, rewritten short for use; what someone who wants the how and why underneath needs moves to the
paper. The paper homes below are provisional; the paper's author owns the paper's structure and may
rename them. Section names follow the WP10 draft (section numbers in
`work-packages/WP10-scope-of-work.md`, "Where the moved material goes").

## `method.md` (about 11,900 words; leaves the docsite entirely)

| Section | Stays on the docsite (rewritten for use) | Moves; source for |
|---|---|---|
| Preamble and "Map and territory" | nothing restated | policy paragraph in the paper body (Methods opening) |
| The pipeline and where the mathematics sits | the pipeline in two sentences (User guide overview) | Preliminaries |
| Conditions of the theory | one line per condition that bears on use (user-guide limitations) | Methods (the conditions); Appendix B (the table) |
| The model | Theory in brief: the invariant form, V = 1 | Methods |
| The fit | Fitting page says what is fitted, not why it converges | Results (theorem-style, proof sketches pointing to `derivation/`) |
| What the stage learns, and why it is shape | none | Results (theorem-style) |
| Tensions, not variance | Tensions page: the idea in use | Results (theorem-style) |
| n-lemmas are discovered, not assumed | n-lemma in two sentences (Theory in brief, Tensions) | Results |
| Interpretation | how to read exchange rates and log V (Tensions, Chart) | Discussion |
| Novelty and white space | holes in use (Chart) | Discussion |
| Prediction from configuration | Prediction page | Methods (the model with covariates) |
| Lineage | one pointer (Further reading) | Related work |
| The posynomial and GGP extension | K > 1 in use (Fitting) | Results (algorithm subsection); Appendix D |
| The solver for small K | none | Results (algorithm); Appendix D |
| Three levels of guarantee | the statuses in use (Termination) | Appendix D (body keeps the statement of each level) |
| What is proved, what is inherited, what is only observed | one line in user-guide limitations | abstraction-gaps appendix; policy paragraph in the body |
| Simplifying assumptions | none | abstraction-gaps appendix |
| Research direction: kernel methods under the GGP constraint | one sentence "documented, not built" (Fitting) | Discussion (future work) |
| Summary of lemma coverage | none | Appendix B |

## The other pages

| Page | Stays on the docsite (rewritten for use) | Moves; source for |
|---|---|---|
| `why-and-how.md` | Getting started opening; User guide overview | "The frontier as V = 1" and "What the fit certifies": Methods; the PCA contrast: Discussion; the idea text: Introduction |
| `preconditioning.md` | User guide, Conditioning: orientation, shift, scaling, zeros, diagnostics, pull-back | "What the theory asks of stage 2", "Invertibility" and "Conditions under which these tools mislead" (derivation parts): Methods, Appendix B; "A worked case in general terms": the case section |
| `api.md` | API overview table; stage 2, 3, 4 and K > 1 usage into the User guide pages | lemma and ledger-id citations: Appendix B; "Kernel methods (documented, not built)": Discussion; the K > 1 mathematics: Results, Appendix D |
| `limitations.md` | User guide, Limitations: the limits that change what a user does | "Limits of the method" long text: Discussion, abstraction-gaps appendix; "What the contrast with PCA does and does not claim": Discussion; "Extensions": Discussion (future work) |
| `literature.md` | Further reading: a short list of key references | the whole survey, the dropped candidates, the sources for the axioms: Related work and the prior-art appendix |

Not snapshotted here, because they are generated or live elsewhere: `docs/generated/derivations.md`
and `docs/generated/verification.md` (still produced by `scripts/build_generated.py`, now for the
paper's build), and the abstraction-gaps ledger (`docs/superpowers/notes/abstraction-gaps.md`,
unchanged).
