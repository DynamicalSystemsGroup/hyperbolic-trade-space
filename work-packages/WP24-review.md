# WP24 — Review report (the vocabulary rename)

| | |
|---|---|
| **Scope of work** | `work-packages/WP24-scope-of-work.md` |
| **Approval** | `work-packages/WP24-decisions.md` (the driver under the mandate, 2026-11-09, 22:50; the gate line in the scope) |
| **Work reviewed** | the pushes below, in order |

The review proper (the checklist against D-1 to D-14 and R-1 to R-16, and the cold reads of R-16) is written by the fresh
reviewer after the last push. The per-push sections below are the evidence trail, written as each push landed from the
repository's own records and from commands run at the time of writing.

## Push 1 (src, contract row 14, tests, case code, generators; the container regeneration)

Commits: `204e7c3` (the rename) and `5b01248` (the regeneration in the container of record).

### Files changed

`git show --stat` of each commit, by surface.

| Surface | `204e7c3` | `5b01248` |
|---|---|---|
| `src/` | 6 files (`datasets`, `estimator`, `plotting`, `solvers`, `tensions`, `tuning`) | 0 |
| `tests/` | 17 files (plus `tests/data/soft_fit_default_reference.npz` among them) | 1 (`test_paper.py`) |
| `examples/adcs/` | 10 files (`case.py`, `k_terms.py`, `experiments/sensitivity.py`, `experiments/reports/sensitivity.json`, six deleted PNGs) | 0 |
| `paper/` | 11 files (generators, `paper_facets.py` moved to `paper_terms.py`, `environment_values.toml`, `supporting_material.ipynb`) | 9 (`container/RECORD.md`, `environment_reference.npz`, `environment_values.toml`, three figures, `figure1.svg`, both notebooks) |
| `scripts/` | 2 (`build_figures.py`, `build_site_figures.py`) | 0 |
| `work-packages/` | 2 (`interface-contract.md`, `interface-contract.toml`) | 0 |
| other | 1 (`claims_register.toml`) | 0 |

Totals: `204e7c3` 49 files, 1156 insertions, 1307 deletions; `5b01248` 10 files, 1091 insertions, 1056 deletions.

### The renamed identifiers (A2)

From the commit message of `204e7c3`: the package's `facet_` and `facet_share_` are `cell_` and `term_share_`;
`assign_facets`, `facet_step`, `facet_gap`, `facet_objective`, `single_facet_termination` are `assign_cells`,
`refit_step`, `term_gap`, `term_objective`, `single_term_termination`; `color="facet"` is `color="cell"`;
`info["facet"]` is `info["term"]`; the report prefix is "term k: "; the case's `facet_record` and `facet_table` are
`term_record` and `term_table`; `paper/paper_facets.py` is `paper/paper_terms.py`; the plotting label helper is
`cell_labels`. Each new name found in the tree now (files containing the name as a whole word):

| Name | `src/` | `examples/adcs/` |
|---|---|---|
| `cell_` | 1 | 3 |
| `term_share_` | 1 | 3 |
| `assign_cells` | 3 | 0 |
| `refit_step` | 2 | 0 |
| `term_gap` | 1 | 0 |
| `term_objective` | 1 | 0 |
| `single_term_termination` | 2 | 0 |
| `cell_labels` | 1 | 1 |
| `term_record` | 0 | 1 |
| `term_table` | 0 | 3 |

### Checks run now

| Check | Command | Output |
|---|---|---|
| R-4, no old name in the package | `grep -rn facet src/` | no output (exit status 1) |
| R-14, attribution | `git log --format=%B 204e7c3^..5b01248 \| grep -ci "co-authored-by\|generated"` | **3** (the scope expects 0) |
| R-14, attribution, the trailer alone | `git log --format=%B 204e7c3^..5b01248 \| grep -ci "co-authored-by"` | 0 |

The three lines the pattern matches (`grep -in`) are words, none an attribution line: the subject of `5b01248` ("...outputs
and figures **regenerated** in hts-paper..."), its body line "The **generated** recovery sentence's pin follows its word", and
the last line of the body of `204e7c3` ("The **generated** outputs follow from the container run"). The trailer search alone
returns 0. The R-14 command as the scope words it does not return 0 for this range; whether the check is the trailer or
the pattern is the reviewer's call.

### The container regeneration (`paper/container/RECORD.md`, the entry for WP24 push 1)

- Image `hts-paper` `9c8a0c616386` (`sha256:9c8a0c61638691f5374ec857604eabfc0f960aeef3a48a10caaf622082c779bc`), built by
  `sh paper/container/build.sh` at local head `541efcd` (31 s, cached layers); the previous image `8e91e07fb08f` removed
  in the same step. Every step `--network none`, in `hts-*` containers only; `hts-wp24` created, started and removed by
  name.
- `uv run python paper/paper_common.py` (3 s): the array `figure1_facet` is now `figure1_term`, bytes unchanged, the other
  eight arrays unchanged; `environment_values.toml` not rewritten by it.
- `uv run python paper/execute_notebooks.py` (116 s): both notebooks; 4 output cells of the paper and 12 of the supporting
  material change in words only; `tab-F-toolchain` prints the build commit.
- `sh paper/container/build-paper.sh` (5 s): the site built.
- `uv run python scripts/build_figures.py` (98 s): `fig-planes-k3` (segment labels "term 1" to "term 3") and `fig-nlemma`
  (its key) rewritten; the other figures and the two model views unchanged.
- `uv run python paper/figures/figure1.py`: `figure1.png` and `figure1.svg` (labels "term k", third pane "terms laid flat").
- Tests inside the image (`uv run pytest -q -n 4` on `test_paper`, `test_case`, `test_k_terms_case`,
  `test_paper_sources`, `test_paper_static_figures`, `test_narrative`, `test_claims_register`, `test_sensitivity`,
  `test_interface_contract`, `test_soft_fit`, 222 s): **399 passed, 1 failed, 4 skipped**. The failure was a pin of the
  generated recovery sentence still reading "facet"; corrected, then `uv run pytest -q tests/test_paper.py -k "figure1 or
  cr2_the_planted"` (20 s): **4 passed**.
- `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or term_order"` (406 s):
  **4 passed**.
- The record's ledger line, from an earlier entry of the same file (not a WP24 run): `uv run python -m experiments verify`,
  "34 entries (11 current); 0 drifts". RECORD.md carries no ledger run for this push; **R-5's "0 drifts" at the push-1 head
  is not recorded** in any file I could read.

### R-5 and R-6 evidence as the records state it

- No number of the paper moved (RECORD.md). Outputs change in words only (`5b01248` message).
- `examples/adcs/experiments/reports/sensitivity.json` was not re-run (its regeneration is the oracle's): keys renamed and
  the file re-serialized as the writer writes it (sorted keys); every number and string value equal under the rename;
  `test_sensitivity`'s comparison of the committed column with the live case results passed in the image.
- `tests/data/soft_fit_default_reference.npz`: 94 keys `.../facet_` and `.../facet_share_` renamed `.../cell_` and
  `.../term_share_`; all 1274 arrays equal in dtype, shape and value; `test_soft_fit` passed in the image (exact branch).
- `paper/environment_reference.npz`: `figure1_facet` is `figure1_term`, bytes unchanged.
- Figure 1's data hash: the key name enters the hash. New pin `ec68f512...` in the image; with the old key the same arrays
  give `4040cb8e...`, the earlier pin (macOS `d3a29d79...` against `f9d7219d...`); `paper/environment_values.toml` carries
  both, with the sentence that the key was "facet". The data are unchanged; the hash moved because the key name is in it.
- "Tests change by identifier and phrase only" (message of `204e7c3`); `tests/test_vocabulary.py`'s made-up term is "tile" (A9).
  I did not diff the test files for this review; the reviewer runs the R-6 command and the diff.

### Statement blocks touched

`claims_register.toml` (48 lines changed in `204e7c3`): the identifier-only edits of the `backing` and `note` fields, each
the old name replaced by its new one, for example `test_k_terms_recovers_planted_facets` is `..._planted_terms`;
`test_assignment_margin_values_and_duplicate_facets` is `..._duplicate_terms`; `test_k3_reports_one_per_facet_recover_planted_supports`
is `..._one_per_term_...`; and the notes "facet_ is argmax over the fitted scores..." read "cell_ is argmax..."; "exponents_,
facet_, coefficients_, facet_share_ exist at K=1 and K>1" reads "exponents_, cell_, coefficients_, term_share_ ...". The full
before and after is `git show 204e7c3 -- claims_register.toml`.
`paper/environment_values.toml`: the comment rows of the table of what moves, "facet planes" and "thin-facet rows" read
"term planes" and "thin-term rows"; the row "facet numbering, order of facet sizes and shares" reads "term numbering, ...";
the key `values.facet_numbered_tables` is `values.term_numbered_tables`; the Figure 1 hash sentence (above). Full diff:
`git show 204e7c3 5b01248 -- paper/environment_values.toml`.
The paper's and the supporting material's prose cells were **not** edited in this push (see below); their output cells
were regenerated (4 and 12, above).

### The tau = infinity sentences list

Not a push-1 item (no sentence of the paper was edited in push 1); the list belongs to the prose pushes.

### Deletions

- `examples/adcs/figures/k3_frontier_coordinates_{primary,stock}.png`, `k3_log_planes_{primary,stock}.png`,
  `k3_tensions_{primary,stock}.png` (six files; the directory no longer exists), and `k_terms.save_figures` with the helpers
  only it used (`log_plane_slices`, `cond_label`, `UNITS`). What they no longer do: they coloured the designs by cell, the
  cluster idiom `figure-review.md` forbids, and nothing read them (message of `204e7c3`); the paper's log-plane slices are
  drawn by `paper/figures/planes.py`. `run_regime` loses its `figs` argument and `make_figures`; `case.figures` pins no file.
- The nine `NN_name.png` pins of contract row 14's predecessor, whose files went with the WP7 case notebook in `4bd6bac`,
  leave the manifest in the same amendment (contract version 13 to 14), so the R-4 test asserts the directory holds exactly the
  pinned files (message of `204e7c3`). Contract check performed for the deletion: the pins left the manifest and the prose
  in the same commit (`git show 204e7c3 -- work-packages/interface-contract.md work-packages/interface-contract.toml`).

### Left for later pushes

- The paper's and the supporting material's prose cells: `grep -c facet` at this head gives 62 lines in `paper/paper.ipynb` and
  256 in `paper/supporting_material.ipynb` (notebook JSON lines, outputs included). The counts of 37 paper and 9 supporting
  prose cells are not stated in any file I read and are left out.
- `examples/adcs/model_v2/diagnostic_pair.py`: done by WP23's stream, `3ad66fe` (identifiers follow `term_table`, `cell_`,
  `term_share_`; the column-name regex dropped), as `WP24-decisions.md` assigned.
- `tests/test_narrative.py`: `204e7c3` added a `RENAMED` map (four names: `facet_objective`, `facet_gap`,
  `single_facet_termination`, `assign_facets`) resolving the renamed names the preserved sources keep. The map is still in
  `tests/test_narrative.py` at this head (`RENAMED` at line 132). `WP24-decisions.md` (06:35 and 06:45) records the driver's
  decision that the records take identifier edits and both test maps are dropped; the call on the test file itself is pending.

## Push 2 (derivations)

Commits on dev: `a5c67f2` (the rename in the derivation), `27dab4d` (Appendix B regenerated in the container of record),
`9b1152e` (the paper-sources notes take the vocabulary; the test map of old names dropped), `a9e23b2` (RECORD.md notes
the rebase). Written from the records below, at the push-3 head.

### Files changed

| Commit | Files |
|---|---|
| `a5c67f2` | 14 files, 226 insertions, 226 deletions: `derivation/axioms.py`, `lemma_02_shift.py`, `lemma_04_convexity.py`, `lemma_11_pareto.py`, `lemma_12_facet_gap.py` moved to `lemma_12_term_gap.py` (`git mv`), `lemma_13_margin.py`, `lemma_14_assignment_stable.py`, `lemma_15_descent.py`, `run.py`, `proof_map_record.json`, `PROOF_MAP_FINDINGS.md`; `paper/paper.ipynb` (the moved module's name in the L12 box's script pointer only); `tests/test_derivation.py`, `tests/test_proof_map.py` |
| `27dab4d` | `paper/container/RECORD.md`, `paper/supporting_material.ipynb` (225 insertions, 176 deletions) |
| `9b1152e` | `docs/superpowers/notes/paper-sources/{api,limitations,method}.md`, `tests/test_narrative.py`, `work-packages/WP24-scope-of-work.md` (A5's amendment) |
| `a9e23b2` | `paper/container/RECORD.md` (6 lines) |

### The moved steps and the statements (A10, R-12)

- The checker's listing before `--update`: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24p2/proofmap-moved-steps.txt`, "PROOF MAP FAILED (46 problem(s))": 46 lines,
  each a step, result, hypothesis list or file whose text moved (L4.24's script line; the L12 file gone from the record and
  its new name not yet in it; L13.1 to L13.17 and L13's results and hypotheses; L14.10, L14.11, L14.18 and L14's imported
  results; L15's steps). The record's diff after `uv run python -m derivation.proofmap --update`:
  `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24p2/proofmap-update-diff.txt`.
- Every line of the derivation's text touched, before and after, by kind (STEP, STATEMENT/TITLE, LEDGER, HYPOTHESIS,
  DOC, MSG, TEST, REF): `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24p2/statements.md`, "Count: 123 lines in 13 files". Each differs by the vocabulary (term for
  the model object, cell for the assignment, "term gap", "maximizing term") and nothing else; R1's statement keeps the
  textbook word (A1), as does L11's "The facet that blocks u'" (docstring).

### Checks (from `paper/container/RECORD.md`, the entry for WP24 push 2, image `e852cde39180`, head 90c8848)

| Check | Command | Output |
|---|---|---|
| R-7, the chain | `uv run python derivation/run.py` | "ALL LEMMAS PASS." (9 s) |
| R-7, the proof map | `uv run python -m derivation.proofmap` | "PROOF MAP OK: 17 lemma files, 371 tagged steps" |
| R-7, Appendix B (the mechanical rule) | `uv run pytest -q tests/test_paper.py -k appendix_b` | "8 passed, 140 deselected" (`/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24p2/container.log`) |
| R-7, R-8 | `uv run pytest -q -n 4 tests/test_derivation.py tests/test_proof_map.py tests/test_matches_derivation.py tests/test_claims_register.py` | "248 passed" |
| R-9 | `uv run python paper/execute_notebooks.py` | `paper/paper.ipynb` byte-equal; in the supporting material the Appendix B cells in words and the moved file's name, `tab-A-register` (three glossary entries of da2984e compiled), `tab-F-toolchain` |
| R-14, the trailer pattern (the amendment of 2026-11-10) | `git log --format=%B a5c67f2^..a9e23b2 \| grep -ciE "co-authored-by\|generated with"` | 0 |

The image `hts-paper` `e852cde39180` was built at 90c8848 (the previous `9c8a0c616386` removed in the same step); the
rebase before the push brought no change to `derivation/`, `paper/*.py`, `src/` or the notebooks, so the outputs stand
(`a9e23b2`). No number of the paper moved.

### Decisions this push needed (`WP24-decisions.md`)

- 06:35 and 06:45: records a test reads take identifier edits (A5 amended), and `docs/superpowers/notes/paper-sources/*.md`
  take the vocabulary as the paper's source text (A5 amended in the scope, `9b1152e`); both test maps of old names
  dropped. Decision records and quotations keep their wording.
- 07:20: on 7fad5ff (a text-only row of `PROOF_MAP_FINDINGS.md` pushed by WP25-2 without an Appendix B run): no revert;
  the paper unit's container run runs the Appendix B test and settles it (push 3, below).

## Push 3 (the paper notebooks' prose)

Commit: the one carrying this section, "WP24 push 3: the word 'facet' leaves the paper's prose" (the prose, the register, the pins, the ledger, the container run's record). Built on 3a66e78.

### What changed

- `paper/paper.ipynb`: 37 Markdown cells (every cell that carried the word), `paper/supporting_material.ipynb`: 9 cells
  (app-B-2, app-D-job, app-D-3, app-D-5, app-D-5-margin, app-D-cond, app-D-own, app-D-recovery-text, app-D-pca-text).
  "term" or "monomial term" for the model object, "cell" for the designs a term scores highest (an empty cell, another
  cell, the near-frontier designs in a term's cell), "n-lemma" unchanged, "trade-off" once ("one per trade-off").
  Headings: "The algorithm for several terms", "B.2 The several-term fit and its levels of guarantee (L12 to L17)",
  "D.3 Exponents and terms", "D.13 The refit on a term's own rows".
- The abstract's gloss (A7): "Each monomial term (a product of powers of the metrics) reports its contending metrics,
  an n-lemma (by analogy with dilemma and trilemma), with elasticities".
- The quilt sentence (A6), in the Preliminaries' "Words": "A posynomial is a sum of monomial terms, each a product of
  powers of the metrics. The fitted reference surface is a quilt of trade-offs, each monomial term one patch, flat in log
  space, meeting its neighbours at the ridges." It replaces "A term, a monomial and a facet are one object: ..." and "We
  say facet for the geometry and term for the algebra." "Quilt" and "patch" are in no glossary entry, caption or statement.
- No output cell changed: after the container run every code cell of both notebooks is byte-equal to 3a66e78; only the
  46 Markdown cells differ.

### The A1 sentences kept (the R-1 exemption list)

| Notebook | Cell | Sentence | Marker |
|---|---|---|---|
| `paper/paper.ipynb` | `sec-methods` | "R1: the balanced point lies in the relative interior of a facet of the supporting envelope with positive normal" | `<!-- vocab-exempt: facet -->` at the paragraph's end |
| `paper/paper.ipynb` | `res-L3` | Theorem L3's hypotheses: "R1 for the facet-normal reading" | `<!-- vocab-exempt: facet -->` at the line's end |
| `paper/supporting_material.ipynb` | `tab-B-proofs-fit` (generated) | step L3.9: "by declared axiom R1 (regularity): the balanced point lies in the relative interior of a facet of the frontier" | push 4 |

The tool reads notebooks and honours the marker per paragraph; it renders as nothing (MyST keeps it as a comment node,
not in the page text). Two Markdown cells keep the record folder name `docs/superpowers/notes/spike-facet-refit/` as a
path (`app-D-own`, `app-D-recovery-text`): a path to a record, not the word.

### Statements touched (R-12)

Every definition, theorem, lemma, proposition, corollary, condition, caption and listed result touched, each pair the
exact replaced text before and after. Each differs by the vocabulary and, where named, the clause the new word needs:
"a facet:" dropped from Definition 3 (the identification it made is gone with the word); "those whose largest term is
facet k's" dropped from Definition 7 (the cell, defined in Definition 3, says it); "each term nonnegative" in L14's sketch
reads "each summand nonnegative" (term is reserved for the model object, R-11); "dominates" reads "scores ... highest"
(the assignment, not Pareto dominance); "the facet's rows" reads "the term's cell"; "that facet's near-frontier designs"
reads "the near-frontier designs in that term's cell"; "Our facets are piecewise log-linear" reads "Our surface is
piecewise log-linear" (a single term is log-linear; the surface is the piecewise object). Model, fit and analysis are
kept apart as before (the assignment is "cell" and analysis; the term is the model).

- **Main results list (Section 1), items 1, 2, 4, 7** (`paper/paper.ipynb`, cell `sec-decision-3`):
  - before: and each facet's elasticities, are read
    after: and each term's elasticities, are read
  - before: The one-facet fit is a geometric program
    after: The one-term fit is a geometric program
  - before: The several-facet fit, not convex in the terms,
    after: The several-term fit, not convex in the terms,
  - before: the facets separate contending sets that one facet blends
    after: the terms separate contending sets that one term blends
- **Preliminaries, Words (A6)** (`paper/paper.ipynb`, cell `sec-preliminaries`):
  - before: **Words.** A posynomial is a sum of monomials. A term, a monomial and a facet are one object: the term of the posynomial, the product of powers, the flat piece in log space. We say facet for the geometry and term for the algebra. Three objects
    after: **Words.** A posynomial is a sum of monomial terms, each a product of powers of the metrics. The fitted reference surface is a quilt of trade-offs, each monomial term one patch, flat in log space, meeting its neighbours at the ridges. Three objects
- **Definitions: prose before Definition 3 and 4; Definition 3 (def-posynomial); Definition 4 (def-temperature); Definition 6 (def-nlemma)** (`paper/paper.ipynb`, cell `sec-definitions`):
  - before: a sum of such terms, one per facet.
    after: a sum of such terms, one per trade-off.
  - before: Each term is a facet: a piece of the surface, not a set of designs;
    after: Each term is a piece of the surface, not a set of designs;
  - before: over designs and over facets; at infinity
    after: over designs and over terms; at infinity
  - before: how sharply facets meet.
    after: how sharply terms meet.
  - before: The contending set of facet $k$ is the support
    after: The contending set of term $k$ is the support
  - before: fit to the facet's rows;
    after: fit to the term's cell;
  - before: draws the n-lemma of each facet for three metrics.
    after: draws the n-lemma of each term for three metrics.
- **Caption of the n-lemma figure (fig-nlemma) and its Shows lines** (`paper/paper.ipynb`, cell `fig-nlemma-caption`):
  - before: three planted facets). A facet is one piece
    after: three planted terms). A term is one piece
  - before: names the facet's n-lemma:
    after: names the term's n-lemma:
  - before: *Shows:* each facet's exponent vector
    after: *Shows:* each term's exponent vector
  - before: which metrics contend on a facet before
    after: which metrics contend in a term before
- **Definition 7 (def-reach), Definition 8 (def-exchange), Definition 9 (def-ascent)** (`paper/paper.ipynb`, cell `sec-definitions-2`):
  - before: The facet share is the fraction of near-frontier designs in the cell of facet $k$, those whose largest term is facet $k$'s; it shows which facets carry
    after: The term share is the fraction of near-frontier designs in the cell of term $k$; it shows which terms carry
  - before: Along facet $k$,
    after: Along term $k$,
  - before: On facet $k$ the tangent space
    after: On term $k$ the tangent space
- **Conditions R1 and R2; the model paragraph; conditioning** (`paper/paper.ipynb`, cell `sec-methods`):
  - before: of design $i$ against facet $k$.
    after: of design $i$ against term $k$. [exempt marker]
  - before: At finite $\tau$ one facet is a geometric program
    after: At finite $\tau$ one term is a geometric program
  - before: Several facets alternate weights with one program for all terms
    after: The several-term fit alternates weights with one program for all terms
  - before: changes which facet is tangent
    after: changes which term is tangent
- **Simplifying assumptions (i), (ii), (iv)** (`paper/paper.ipynb`, cell `sec-simplifying`):
  - before: (i) *One facet at $K=1$:*
    after: (i) *One term at $K=1$:*
  - before: facets are fitted at $\kappa=\infty$ with kinks on the ridges. For given facets
    after: terms are fitted at $\kappa=\infty$ with kinks on the ridges. For given terms
  - before: leaves the facets unchanged;
    after: leaves the terms unchanged;
  - before: the case needs three facets;
    after: the case needs three terms;
- **Theorem (L3, thm-kkt), hypotheses (kept, A1)** (`paper/paper.ipynb`, cell `res-L3`):
  - before: R1 for the facet-normal reading; $w$ minimizes $J_\tau$ on $\Delta$.
    after: R1 for the facet-normal reading; $w$ minimizes $J_\tau$ on $\Delta$. [exempt marker]
- **Sentence before L15** (`paper/paper.ipynb`, cell `run-L15`):
  - before: stationarity by the facet gap (L12)
    after: stationarity by the term gap (L12)
- **Theorem, Level 1, descent (L15, thm-descent)** (`paper/paper.ipynb`, cell `res-L15`):
  - before: one per facet: a cell is a set of rows, a facet a piece of the surface)
    after: one per term: a cell is a set of rows, a term a piece of the surface)
  - before: the cell of its maximizing facet lowers or keeps $F$, and refitting each facet on its new cell
    after: the cell of its maximizing term lowers or keeps $F$, and refitting each term on its new cell
- **Lemma, Level 2 (L12, lem-gap): title and statement** (`paper/paper.ipynb`, cell `res-L12`):
  - before: numerical stationarity: the facet gap (L12)
    after: numerical stationarity: the term gap (L12)
  - before: the facet gap is $G_k(w)
    after: the term gap is $G_k(w)
- **Lemma (L13, lem-margin): statement and sketch** (`paper/paper.ipynb`, cell `res-L13`):
  - before: If every facet score changes
    after: If every term score changes
  - before: each row's maximizing facet is unchanged
    after: each row's maximizing term is unchanged
  - before: to every other facet falls
    after: to every other term falls
- **Proposition (L14, prop-local): sketch** (`paper/paper.ipynb`, cell `res-L14a`):
  - before: R2 keeps each row's maximizing facet, so
    after: R2 keeps each row's maximizing term, so
  - before: regroup the rows by facet, each term nonnegative.
    after: regroup the rows by cell, each summand nonnegative.
- **Corollary (L14, cor-bound): hypotheses** (`paper/paper.ipynb`, cell `res-L14b`):
  - before: the facet gaps of
    after: the term gaps of
- **The stopping declaration** (`paper/paper.ipynb`, cell `sec-results-stopping`):
  - before: that the facet gaps hold
    after: that the term gaps hold
- **Caption of the K = 3 planes (fig-plane-3)** (`paper/paper.ipynb`, cell `fig-planes-k3-caption`):
  - before: one straight segment per facet (named on it), with the other seven metrics held at the median of that facet's near-frontier designs
    after: one straight segment per term (named on it), with the other seven metrics held at the median of the near-frontier designs in that term's cell
- **Caption of the regimes figure (fig-regimes-1)** (`paper/paper.ipynb`, cell `fig-regimes-caption`):
  - before: (one facet, so one cell:
    after: (one term, so one cell:
- **Appendix B.2 heading and algorithm paragraph** (`paper/supporting_material.ipynb`, cell `app-B-2`):
  - before: ### B.2 The several-facet fit and its levels
    after: ### B.2 The several-term fit and its levels
  - before: every facet is fitted against every design
    after: every term is fitted against every design
  - before: which facet dominates a design is analysis
    after: which term scores a design highest is analysis
- **Appendix D.8, what each status asserts** (`paper/supporting_material.ipynb`, cell `app-D-5`):
  - before: no facet is empty and
    after: no cell is empty and
  - before: a zero margin or an empty facet;
    after: a zero margin or an empty cell;
  - before: or a single facet;
    after: or a single term;
  - before: the largest facet gap,
    after: the largest term gap,

### The claims register (R-8)

`[[claim]]` rows: **399 before, 399 after**; none dropped. 29 rows changed: 26 fragments followed their sentences (C007,
C008, C013, C016, C020, C022, C034, C035, C060, C065, C072, C073, C094, C097, C105, C106, C108, C126, C132, C146,
C148, C149, C151, C152, C153, C156) and 5 anchors follow the
heading "The algorithm for several terms" (C019 to C023). `uv run pytest tests/test_claims_register.py`: 21 passed.

### The length ledger

Removed (comment block, no row): the two "Words" sentences that explained the old word (net -2 in "Preliminaries and
notation" after the quilt sentence); "a facet:" in Definition 3 and the clause of Definition 7 (-8 in "Definitions").
Added within the ceilings: +1 "The decision problem", +1 "Results", +3 "Case analysis" (the K = 3 caption's cell
clause). Raised: "Methods" +2 ("The several-term fit alternates", where a word swap would say that several terms
alternate); the abstract +8 (the gloss of A7), cap 241 to 249, the abstract at 247. The row of 2026-11-10 on the
proposer's radius: its job text no longer names "that the earlier radius was a typed constant" (the clause was cut).

### Pins (never weakening)

`tests/test_paper.py`: the positive pins follow the wording ("One term", "beyond one term", "leaves the terms
unchanged", "in the cell of term $k$", the B.2 heading); the abstract test gains the gloss phrase, "facet" absent from the
abstract, and "monomial term" before the first "monomial,"; the negative guards on the old phrases are kept; docstrings
and comments in the vocabulary. `tests/test_paper_sources.py` and `tests/test_narrative.py` needed no change.

### Checks

| Check | Command | Output |
|---|---|---|
| ruff | `uv run ruff check . && uv run ruff format --check .` | "All checks passed!"; "321 files already formatted" |
| lock | `uv lock --check` | "Resolved 178 packages" |
| fast suite | `uv run pytest -q -m "not slow" -n auto` | 1742 passed, 2 failed, 16 skipped, 1 xfailed: the two register-phrase tests (below) |
| vocabulary | `uv run python scripts/check_vocabulary.py` | "70 new violation(s), 0 known" (70 before; only the section name of three rows moved) |
| the word in the sources | a script over both notebooks' Markdown | `sec-methods` and `res-L3` (the A1 sentences, with the marker) and the two record paths |
| container (`hts-paper` `e852cde39180`) | `paper_common.py`, `execute_notebooks.py`, `build-paper.sh` | unchanged values, outputs byte-equal, site built (RECORD.md, this push's entry) |
| container | `HTS_ENVIRONMENT_OF_RECORD=1 uv run pytest -q -n 4 tests/test_paper.py tests/test_paper_sources.py tests/test_narrative.py tests/test_claims_register.py tests/test_paper_static_figures.py` | 187 passed, 2 failed, 4 skipped (the Appendix B tests pass: 7fad5ff settled) |
| container | `PAPER_EXECUTE=1 uv run pytest -q tests/test_paper.py -k "perturbation or clean_kernel or term_order"` | 4 passed (411 s) |
| R-14, the trailer pattern | `git log --format=%B 3a66e78..HEAD \| grep -ciE "co-authored-by\|generated with"` | 0 |

The two failures: `test_register_phrases_are_used_in_the_body` and `test_register_phrases_are_used_in_the_main_text_itself`
read the "Register phrases" list of `docs/superpowers/notes/notation.md`, which names `facet gap`; the paper now says
"term gap". The fix is one line in that note, outside this push's blast radius (a question to the PM).

### The rendered page (staged build, the browser pane)

`uv run python scripts/stage_site.py --serve` (port 8791; 8777 was held by another process), page text of the paper:
`facet` 3 times: R1's sentence, L3's hypotheses (both A1) and the family table's DEA row "One exponent vector per facet"
(generated from `paper/prior_art.yaml`, outside this push). The supporting material's page: 70, all in generated tables
(Appendix A from `glossary.yaml`, Appendix B's L3.9, Appendix E from the gaps ledger, Appendix G from
`paper/prior_art.yaml`) and the two record paths. Screenshots: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24p3-renders/` (`paper-abstract-gloss.jpg`,
`paper-preliminaries-quilt.jpg`, `paper-definitions-7-9.jpg`, `paper-L15-L12.jpg`, `supporting-toc-B2-D3.jpg`).

### Left for push 4 or for the PM

- Generated tables still carrying the word, from sources outside this push: `tab-families` and `tab-G-register`
  (`paper/prior_art.yaml`), `tab-A-register` (`glossary.yaml`, push 4), `tab-E-gaps`
  (`docs/superpowers/notes/abstraction-gaps.md`), `tab-B-proofs-fit` L3.9 (A1, the tool's exempt handling).
- `docs/superpowers/notes/notation.md`: the register phrase `facet gap` (and its other rows) read by two tests.
- The docs pages, `site/index.html`, the glossary and the tool's `avoid` and `stems` (push 4).
