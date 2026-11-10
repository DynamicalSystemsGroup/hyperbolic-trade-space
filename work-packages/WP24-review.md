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

### Records a test reads

On the PM's direction (option 1, under the driver's rule of 06:35, "the same rule for any other record a test reads"),
`docs/superpowers/notes/notation.md`, the paper's notation source, takes the vocabulary by A2's semantics; no quotation
in it carried the word and it has no R1 sentence. Lines changed (numbers as after): 34 to 38 (exponent vector, n-lemma
size, reach, term share and its code name, the row "facet k; term k" now "term k" with "term; monomial term; monomial"
and the patch reading), 44, 45, 53 to 61 (conditioning, elasticity, the assignment row "cell of design i" with
`cell_`, `assign_cells(X)`, the term gap row with `term_gap`, the bound, the margin, the radius, the status, the
levels), 65, 67, the "Words" paragraph (69 to 75), 83, the register phrase `term gap` (98) and 125 ("A term of the fit
is a term, never a regime"). `grep -ci facet` on the note: 0. The two paper tests then pass (`-k register_phrases`: 2
passed), and `tests/test_docs.py::test_register_phrases_present` fails instead: the docs pages (push 4) still say
"facet gap" (`docs/user-guide/termination.md` lines 25, 52, 60). Put to the PM.

### Left for push 4 or for the PM

- Generated tables still carrying the word, from sources outside this push: `tab-families` and `tab-G-register`
  (`paper/prior_art.yaml`), `tab-A-register` (`glossary.yaml`, push 4), `tab-E-gaps`
  (`docs/superpowers/notes/abstraction-gaps.md`), `tab-B-proofs-fit` L3.9 (A1, the tool's exempt handling).
- `docs/superpowers/notes/notation.md`: the register phrase `facet gap` (and its other rows) read by two tests.
- The docs pages, `site/index.html`, the glossary and the tool's `avoid` and `stems` (push 4).

## Push 4 (the docs pages, the root page, the generated tables' sources, the glossary; the check turned on)

Commits on dev: "WP24 push 4: the word ... leaves the docs, the root page and the generated tables; the glossary turns
the check on" (the change) and the commit carrying this section (`paper/container/RECORD.md` and this review). Push 3's
two commits land in the same push, rebased, as the driver decided (`driver-log.md`, 2026-11-10: "push 3 is coherent
only with push 4; the two land together"). The hashes are in the PM's report (they move with the rebase before the push).

### What changed

- Docs pages (D-11): `docs/api.md` (the fitted attributes `cell_`, `term_share_`; `cell_labels`), `docs/theory.md`,
  `docs/examples.md` (the ternary section's alt text and two bullets), `docs/user-guide/{chart,fitting,tensions,
  limitations,termination}.md` (term for the model object, cell for the assignment, the renamed public names
  `assign_cells`, `refit_step`, `cell_`, `term_share_`, `term gap`). `README.md` and `mkdocs.yml` carried no
  occurrence and are unchanged.
- The gloss (A7), on the docs home page, `docs/index.md`, the first use of the term in the docs: "it fits a frontier
  model in the posynomial invariant form: a sum of monomial terms, where a monomial term (a product of powers of the
  metrics) is one trade-off." The quilt sentence (A6, optional on the index) is not carried: the page's word budget
  (250) holds the gloss and not both.
- `site/index.html`: Figure 1's alt text and caption ("the three terms of the fitted reference surface"; the figure's
  own labels say "term 1" to "term 3" and "terms laid flat" since push 1), the map's alt text, caption and reading
  paragraph ("the several-term extension", "the several-term algorithm").
- Figure (D-10): `three-facets-{light,dark}.png` is `three-terms-{light,dark}.png` (`docs/user-guide/fitting.md`,
  `tests/test_site.py`). `docs/generated/` is git-ignored: the figure and the compiled glossary page are built at
  staging (`scripts/build_figures.py` from the page's own name; `scripts/build_generated.py`); nothing committed.
- `glossary.yaml` (D-1): entries `facet` and `facet gap` removed; `term gap` present (id `term-gap`); the `term` entry's
  phrase is "monomial term" with `term` as an alias, its `not` carries the polyhedral exclusion in plain words ("a face
  of the Pareto boundary or of the data's convex hull"), and "facet" is under its `avoid` with the reason; "facet" is in
  `assumed` with its reason (polyhedral geometry, Boyd and Vandenberghe level, A1); the stem `facet` is out of `stems`;
  cross-references in `cell`, `n-lemma`, `elasticity`, GP and GGP `not`, `assignment margin`, `stable radius`,
  `conditioning of the exponents`, `ternary plot`, `share`, `region` rewritten; `defined_in` of `ternary plot` and
  `region` point at `plot_ternary (docstring, Notes)` (the spike-ternary report pointers, WP25's row). The held patch of
  the preparation worktree was the base.
- `scripts/vocabulary_baseline.toml` (D-12): the six reasons reworded ("term gap", "planted terms"); two rows removed
  because fixed (`docs/user-guide/fitting.md` "mean gap", `paper/paper.ipynb` "across temperature"); no row added.
- Generated tables' sources: `paper/prior_art.yaml` (the Pareto, DEA and frontier-estimation rows: the word was the
  model's, not DEA's polyhedral one, so reworded, no marker); `docs/superpowers/notes/abstraction-gaps.md` (the
  vocabulary, and the test names renamed in push 1; the record paths `spike-facet-refit/` and `dup_facets.py` kept);
  `paper/generate_proofs.py` (the exempt marker on a declared axiom whose statement uses the polyhedral word: R1 at
  step L3.9). The tool needed no change (`scripts/check_vocabulary.py` untouched).
- `claims_register.toml`: 24 docs fragments follow their sentences (C163, C183, C195, C196, C197, C198, C206, C271,
  C276, C286, C287, C295, C296, C310, C326 to C329, C332, C333, C338, C339, C378, C379); every `note` takes the
  vocabulary; `glossary:facet` and `glossary:facet-gap` backings are `glossary:term` and `glossary:term-gap`; C001's
  backing on the spike-ternary report dropped (its `func:` backing on `plot_ternary` stays). Row count unchanged.
- Tests: `tests/test_site.py` (the map caption pin, the figure name, three comments), `tests/test_build_generated.py`
  (the register phrase `term gap`). No requirement weakened.

### WP25 drift rows closed in the same edit

| Row | Where | Now |
|---|---|---|
| 10 | `chart.md` L112 | "The designs are one colour by default, whatever the number of terms; in `plot_log_plane` and `plot_frontier_surface_3d`, `color="cell"` colours them by cell ... and any other string raises `ValueError`" (plotting.py `_cell_option`) |
| 13 | `theory.md` L21-22 | "fitting several terms alternates assigning the designs to terms with a separate convex refit of each term" (`solve_terms`) |
| 14 | `theory.md` L22-23 | "By default (`term_temperature=np.inf`) the package takes the sharp limit of the weights, one label per design, and the labels drive the refit; reading off which term scores a design highest is analysis" |
| 15 | glossary mean slack | "The mean shortfall of the designs below the fitted reference surface, F(W) = ..., returned as mean_slack_; the several-term fit minimizes it; ..." |
| 16 | glossary termination status | adds "or stationary (soft fit only)" |
| 17 | glossary assignment | "Only the soft fit (finite term temperature) weighs every term against every design; at the default the labels drive the refit." |

Two sentences of rows 7 and 9 were rewritten because they carried the word, and say what the code does: `chart.md`
L60 ("log V is the maximum over terms at the default `term_temperature=inf`") and the Figure 4 caption ("the grey
strip below it is log V from -1/tau to 0"). Rows 4 to 9 and 12 otherwise stay with WP25-2 unit B.

### R-1: the sentences that keep the word (the A1 list)

The vocabulary tool reads them; each carries `<!-- vocab-exempt: facet -->` in its paragraph:

1. `paper/paper.ipynb`, cell `sec-methods`: R1, "the balanced point lies in the relative interior of a facet of the
   supporting envelope with positive normal".
2. `paper/paper.ipynb`, cell `res-L3`: Theorem L3's hypotheses, "R1 for the facet-normal reading".
3. `paper/supporting_material.ipynb`, cell `tab-B-proofs-fit` (generated): step L3.9, R1's ledger statement, "the
   relative interior of a facet of the frontier"; the marker is emitted by `paper/generate_proofs.py`.

Outside the tool's corpus, the same polyhedral sense at its source: `derivation/axioms.py` L600, L604, L607 (R1's
statement, role and failure mode); `derivation/lemma_11_pareto.py` L23 (L11's "the facet that blocks u'");
`scripts/build_generated.py` L87 (R1 on the verification page). The glossary's own lines: `glossary.yaml` L139 (the
`avoid` phrase), L595-596 (the `assumed` term and its reason). The rendered pages show the word only in items 1 to 3
(the browser read below).

### R-2: the grep against the list

`grep -rni facet glossary.yaml paper src tests examples derivation docs/*.md docs/user-guide docs/generated site scripts
claims_register.toml work-packages/interface-contract.md work-packages/interface-contract.toml README.md` at the head of
the push, by file:

| File | Lines | On the list as |
|---|---|---|
| `glossary.yaml` | 3 | the avoid entry and the assumed term (above) |
| `derivation/axioms.py`, `derivation/lemma_11_pareto.py`, `scripts/build_generated.py` | 3, 1, 1 | A1 sources (above) |
| `paper/paper.ipynb`, `paper/supporting_material.ipynb` | the three A1 sentences (source and rendered output lines); the record paths `spike-facet-refit/` (cells `app-D-own`, `app-D-recovery-text`, `tab-E-gaps`) and `dup_facets.py` (`tab-E-gaps`) | A1; record folder and file names |
| `paper/generate_proofs.py` | 4 | the marker constant, its docstring and its use (A1 handling) |
| `paper/generate_results.py` | 1 (L419) | the record folder `spike-facet-refit` |
| `paper/environment_values.toml` | 1 (L57) | a record of the old array key, the reason two hashes are kept (push 1) |
| `paper/container/RECORD.md` | 17 | past entries (A4); the new entry has none |
| `paper/BROWSER_NOTES.md` | 7 | a record (`WP24-decisions.md`, 00:35) |
| `paper/length_ledger.toml` | 27 | the ledger's past rows and push 3's comment block naming what was cut (records of rows; not in this push's blast radius) |
| `derivation/PROOF_MAP_FINDINGS.md` | 1 (L166) | the supervisor's quotation |
| `claims_register.toml` | 1 (C394's `source`, "leaves the term/facet naming to WP24") | the record of where the row came from |
| `tests/test_paper.py`, `tests/test_diagnostic_pair.py` | 5, 1 | negative guards (the word asserted absent) |
| `work-packages/interface-contract.md` | 5 | the change log's past rows 3, 7, 8, 11, 14 (A4) |
| `scripts/rename_facet.py`, `tests/test_rename_facet.py`, `scripts/check.py` L60 | 104, 70, 1 | the rename tool, its test and its map line (WP25-2 deletes them) |
| `src/`, `examples/`, `docs/*.md`, `docs/user-guide/`, `site/`, `README.md`, `work-packages/interface-contract.toml` | 0 | |

`docs/generated/` is git-ignored; in the staged build its glossary page has no occurrence. No remaining line is off
the list.

### Checks

| Check | Command | Output |
|---|---|---|
| R-1, the vocabulary tool | `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml` | "0 new violation(s), 69 known", exit 0 |
| the other violations | `uv run python scripts/check_vocabulary.py` | "69 new violation(s), 0 known" (70 before; none is the word) |
| R-1 tests | `uv run pytest tests/test_vocabulary.py tests/test_build_generated.py` | passed (in the fast suite) |
| register (R-8) | `uv run pytest tests/test_claims_register.py` | 21 passed; rows unchanged in number |
| docs, site, paper, gaps | `uv run pytest -q -n 8 tests/test_paper.py tests/test_gaps.py tests/test_claims_register.py tests/test_build_generated.py tests/test_vocabulary.py tests/test_docs.py tests/test_site.py tests/test_paper_sources.py tests/test_narrative.py` | 342 passed, 4 skipped after the fix of the one vocabulary hit ("log-linear surface" in the DEA row, reworded) |
| ruff | `uv run ruff check . && uv run ruff format --check .` | "All checks passed!"; "324 files already formatted" |
| lock | `uv lock --check` | "Resolved 178 packages" |
| fast suite | `uv run pytest -q -m "not slow" -n auto` | 1744 passed, 16 skipped, 1 xfailed |
| R-14, the trailer pattern | `git log --format=%B origin/dev..HEAD \| grep -ciE "co-authored-by\|generated with"` | 0 |

The word budgets of `tests/test_site.py` held by tightening, not by raising: `index.md` 239/250, `fitting.md`
795/800, `chart.md` 596/600, `termination.md` 599/600.

### The regeneration

On the host, per the supervisor's rule of 09:05 (container at the gate only): `tab-A-register`, `tab-B-proofs-fit`,
`tab-E-gaps`, `tab-G-register` and the paper's `tab-families` changed in words; `tab-B-proofs-solver` unchanged; every
other cell byte-equal. `paper/container/RECORD.md`, the entry for WP24 push 4. The image was not rebuilt.

### Read as rendered (the staged build, the browser pane at 1280 px)

`uv run python scripts/stage_site.py --serve --port 8811`; the root page, the docs home, theory, API, examples,
chart, fitting, tensions, limitations, termination, the compiled glossary and the API reference: no occurrence of the
word, no raw markup, the gloss present on the docs home, "monomial term" on the glossary page. The paper: the word only
in R1's sentence (and L3's hypotheses), the abstract's gloss present; the supporting material: only L3.9 (A1) and the
record paths; the marker renders as nothing. Screenshots:
`/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24p4-renders/`.
Seen there and not this push's: Appendix E's HTML table shows raw `$...$` (its committed output had it before).

### Open

- `site/paper-map.webp`, the map on the root page, is a raster from the external review with no source in the
  repository; its boxes say "Multi-Facet Algorithm", "Number of facets (terms)", "per-facet gap" and "each facet
  refit". The caption and alt text now say "several-term"; the image itself cannot be regenerated here.
- The two cold reads (R-16) follow this push.

## Acceptance review (work-acceptance, 2026-11-10)

| | |
|---|---|
| **Scope of work** | `work-packages/WP24-scope-of-work.md` (with the driver's amendments: A5 of 2026-11-10, R-14's trailer pattern; the contract version 14 explained in row 14) |
| **Scope approval verified** | The gate line "2026-11-09, 22:50: approved for execution by the driver under the mandate", committed in `1501c53` ("WP24 approved by the driver under the mandate", 22:43); `WP24-decisions.md` names it as the approval. The decisions file cites the gate line; it does not quote an approval sentence. |
| **Work reviewed** | `62a086a..944c564` on `dev`; WP24's commits `0be3449` (preparation), push 1 `204e7c3`, `5b01248`; push 2 `a5c67f2`, `27dab4d`, `9b1152e`, `a9e23b2`; pushes 3 and 4 (landed together) `9df7483`, `1b1249d`, `a2e6bd5`, `ee7704e`; review sections `f30a3ac` and inside the push commits. Worktree `wp24review` from `origin/dev` at `944c564`, `uv sync --locked`. Later commits on `origin/dev` read for R-15 only (`7d7c4a5`, `bb51b7e`). |
| **Supervisor (accepts)** | mzargham, at his paper review |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `WP24-decisions.md` |

Reviewed by a fresh reviewer that did not build the work. No file was changed except this one; the paper figures
regenerated for R-10 were restored with `git checkout` after the comparison.

### Cold reads (R-16, A8)

**How the slices were made.** `uv run python scripts/stage_site.py --serve --port 8831` from the worktree: the
docs, the root page and the paper built (MyST: "Built 2 pages for project"); no build error. The rendered paper was
captured at 1280 px wide, light scheme, with headless Chrome through the DevTools protocol (a capture script in the
session scratchpad, `wp24reads/tools/capture.py`), each slice clipped to its element, and the page text of each slice
saved beside it with the mathematics as its TeX. Folder:
`/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24reads/slices/`
(depth A: `A1-title-abstract`, `A2-figure1-image`, `A3-figure1-caption`; depth B: `B00-headers.txt`,
`B01-main-results-1`, 28 statement blocks `B02` to `B29` (Definitions 1 to 9, Theorems 1 to 12, Propositions 1 to 3,
Lemmas 1 and 2, Corollary 1), and the 9 figures `B08`, `B30` to `B37`, each as `-a-image` then `-b-caption`). The
paper's Figure 1 as rendered is the n-lemma figure (`fig-nlemma`). The prompts are in `wp24reads/prompts/`.

**The readers.** Two fresh general-purpose subagents (model sonnet), run in parallel, each given only its persona and
depth from `reader-grid.md`, its slice files (images first, each figure's image before its caption, then the text),
the grid's return format (recall and friction) and the spike's two questions. Neither saw the scope, the spike, this
review or the other's return. Depth A: P1, the accountable decision maker (core cell). Depth B: P4, the
machine-learning practitioner (core cell; the persona the cluster idiom would mislead first). Returns quoted as
written.

**The two questions, in short.** Both readers say a monomial term is a product of powers of the metrics and a piece
of the fitted surface (A: from the abstract's gloss; B: from Definition 3 and Theorem 8), and both put the contending
metrics on the term, not on a group of designs (A: "The contending metrics belong to a piece of the model, a term, and
not to a group of designs"; B: "So a group of designs is how the set is found, but the set is a property of the
term"). **No finding blocks** by the scope's test: no reader took a term for a group of designs, and both could say
what a term is from the gloss. No fix and no re-read is owed.

#### Depth A, P1 (the accountable decision maker), fresh context, image before caption. Verbatim.

> IMAGE-ONLY SENTENCE (Step 2, before the caption): A triangle with three metrics at its corners shows three numbered terms placed on an edge, an edge and the interior, each labelled as a "dilemma" or "trilemma" of particular metrics. Black rings sit very close to the coloured dots, so the method seems to recover known answers.
> DID THE CAPTION CHANGE IT: Yes, partly. I had read the rings as a marker of the fit. The caption says they are the "planted" (known) answer and the dots are the fit's recovery, so the figure is a recovery check on synthetic data (it says "a synthetic table with three planted terms"). I also learned that the position of a point is an "exponent vector" and that the printed label comes from the fit's support, "not read off the marker". The caption's "Does not show: designs, their levels or the surface" tells me this is a diagnostic picture, not a decision picture.
>
> RECALL
> 1. What this is about: a trade study with many competing metrics. It aims to give an accountable executive an answer and a justification. It fits a surface to the outer edge of the design data (a "posynomial reference surface") and reads off which metrics are in tension with which, and by how much.
> 2. The main result: each piece (term) of the fitted surface names a set of metrics that trade against each other (a dilemma, trilemma or n-lemma). It gives elasticities, i.e. the percentage of one metric you give up per percentage gained in another. The single-term case reduces to a convex program that is solved directly. The multi-term case stays compatible with generalized geometric programming. On a cubesat example (power, mass, attitude control), one term blends the subsystems' trade-offs into one tension and three terms separate them. Figure 1 shows the method recovering planted answers on synthetic data. The abstract gives no number on how well it recovers anything, and none on real data.
> 3. What I would do next: ask for a one-page statement of the cubesat decision, namely which design would be picked and what the elasticities told the decision maker that PCA or a plain Pareto plot did not. If that is persuasive, I would hand it to an analyst to run on one of our own trade tables.
> 4. What I would tell a colleague: "A method that tells you which of your criteria genuinely fight each other and at what exchange rate, rather than just which directions the data varies in. It is open source and unsupervised. It looks credible, but I have only seen the abstract and a synthetic-data figure."
> 5. What I think the method does not do: it does not choose a design or weigh the metrics for you. It does not model the Pareto boundary itself, since it fits a "soft support" that a few designs may exceed. It does not show designs or their levels (the figure's own "Does not show"). It does not replace PCA, and the abstract says the two compose. It needs the metrics conditioned to strictly positive, larger-is-better numbers, which I infer from "product of powers of the metrics" and not from anything stated. Nothing here says it validates the model against reality.
>
> THE TWO QUESTIONS
> Q1. Monomial term: "a product of powers of the metrics". Source: the abstract, in the parenthesis "Each monomial term (a product of powers of the metrics)". The Figure 1 caption and its legend add that it is "one piece of the fitted reference surface" whose exponents form a point on a triangle ("exponent vector", w = (0.44, 0.27, 0.28)). I could not tell from these slices whether "monomial term" and "term" are the same object (I assume so), or what the exponents are on, i.e. why they sum to 1.00 here.
> Q2. The contending metrics belong to a piece of the model, a term, and not to a group of designs. Sources: the abstract ("Each monomial term ... reports its contending metrics, an n-lemma") and the caption ("The face that holds the point names the term's n-lemma"). The abstract's last sentence, "three terms separate the contending sets", is a little ambiguous because "sets" could be read as sets of designs. The "sets" are sets of metrics, which the figure confirms.
>
> FRICTION
> - Title in the rendered slice is cut off at the right edge: "Scaling Decision Analysis with Hyperbolic Trade Sp" and then "Identification" on line two. This may be an artefact of the slice crop, but as rendered the title does not read.
> - "A fitted posynomial reference surface models the data underlying the table, not the Pareto boundary, and gives the data a coordinate system; the table and its reading are views of that model." I could not tell which table, or what "views of that model" means in practice. The word "table" appears without being introduced.
> - "A reversible chart separates a design's position along the surface from its energy differential: its level relative to the surface, by analogy with a potential, not a physical energy." This is hard going for a non-specialist. I understood only that a design has two readouts, where it sits and how far it is from the surface.
> - "Principal component analysis (PCA) is trusted as reproducible and interpretable, and explains variance. We explain tensions." This is a clear sentence and a good hook, but it appears before the problem is stated.
> - "Modelling a single n-lemma fits a monomial, which transforms into a convex program and is solved directly" is the one place where specialist vocabulary carries the claim with no plain-words gloss for me. I took it as "the single-tension case is easy and reliable".
> - Terms I guessed:
>   - "n-lemma" = the group of n metrics that fight each other in one term.
>   - "elasticity" = the exchange rate between two metrics in percent terms (the abstract defines it, so this was not really a guess).
>   - "exponent vector" = how much of each metric goes into the term, summing to 1.
>   - "binds alone" (corner) = that metric is the limiting one by itself.
>   - "planted" = a known answer built into synthetic data to test recovery.
>   - "soft support" = a surface hugging the outer edge that a few designs can poke through.
>   - "kernel" = an alternative functional building block (I did not need it).
>   - "unsupervised feature engineering" = it builds new descriptors of the data without being told a target.
> - The figure's right-hand panel says "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)". Three values of 1.00 look like a typo or a column that does not add up. I only half-understood it from the caption's "the weight the three carry is printed (here all of it)". "d = 3" is unexplained at this level.
> - The figure's edge labels read "dilemma of 1 and 2" and so on, rotated along the edges, and are small. They are readable. The figure's corner labels read "metric 1 (corner: it binds alone)". Both are fine.
> - Would I read one level deeper? Yes, but only to find the cubesat result, where the abstract promises a decision-relevant contrast (one blended tension vs three separated sets). Neither the abstract nor Figure 1 shows a real decision or a number. The figure is on synthetic data, and the reason to continue is to see whether the method tells an executive something on real data. I would stop if that were not there.
>
> FINDINGS
> 1. The title is truncated at the right edge in the rendering ("...Hyperbolic Trade Sp" and "Identification" on the next line), so the reader cannot read the full title. (A1-title-abstract.png)
> 2. The abstract never states the decision problem in concrete terms or a headline finding with a number. The cubesat sentence is the only example and says only that one term blends and three terms separate. (A1-title-abstract.txt)
> 3. "The table" is used ("the data underlying the table", "the table and its reading are views of that model") before any table has been introduced. (A1-title-abstract.txt)
> 4. The sentence about the "reversible chart" and "energy differential" is too dense and analogy-laden to follow at abstract level. (A1-title-abstract.txt)
> 5. "Monomial term" is defined in the abstract parenthesis, but the Figure 1 caption calls the same object "a term" and "a piece of the fitted reference surface". It would help to say once that they are the same. (A1-title-abstract.txt, A3-figure1-caption.txt)
> 6. "Contending sets" in the last sentence of the abstract is ambiguous (sets of metrics or of designs). The figure resolves it to metrics. (A1-title-abstract.txt)
> 7. The figure's image on its own does not say that the open rings are the known answer and the dots the fit. This is stated only in the legend ("planted (the known answer)") and the caption. It also does not say that this is synthetic. (A2-figure1-image.png)
> 8. The "Weight on these three metrics: 1.00, 1.00, 1.00 (all of it: d = 3)" line in the figure reads as a mistake without the caption, and "d = 3" is not explained. (A2-figure1-image.png)
> 9. Figure 1's job is a recovery check on synthetic data, so it does not show the method working on real data. For a decision maker at this depth the hero image does not carry the finding. The caption's "Good for" line is candid about this. (A2-figure1-image.png, A3-figure1-caption.txt)
> 10. The caption's "Shows / Does not show / Good for" lines are clear and useful. The "Does not show" line directly answers the question of what the picture leaves out. (A3-figure1-caption.txt)
> 11. The abstract does not say that metrics must be conditioned to positive, larger-is-better values. That is a prerequisite for anyone who wants to apply the method. (A1-title-abstract.txt)
> 12. The abstract has no claim about validation against real decisions or outcomes, so "whether to trust the method" is not answered at this depth. (A1-title-abstract.txt)

**Dispositions, depth A.** Nothing blocks. Each finding is listed for the supervisor's eye unless said otherwise.

- A-1 (title cut off): **a defect of the review's capture, not of the page.** The slice was clipped at 880 px; the full-page capture and the browser show the title whole on two lines ("... Hyperbolic Trade Space / Identification"). No action.
- A-2, A-3, A-4, A-11, A-12 (no concrete decision or number in the abstract; "the table" before it is introduced; the chart sentence dense; conditioning not stated; no validation claim): the abstract's content, not the vocabulary; the abstract is the supervisor's to rewrite (his standing order of 2026-11-09). Listed.
- A-5 ("monomial term" and "term" not said once to be the same object): vocabulary, the A7 gloss works but the shortening is not announced at depth A. Listed (the Preliminaries' "Words" sentence says it at depth C).
- A-6 ("three terms separate the contending sets": sets of metrics or of designs): vocabulary-adjacent; the reader resolved it to metrics from the figure. Not a block (the reader did not take a term for a group of designs). Listed.
- A-7, A-8, A-9 (Figure 1's rings unexplained without the legend; "1.00, 1.00, 1.00 (all of it: d = 3)" reads as an error; a synthetic recovery check as the hero image): figure findings for the figure loop (`figure-review.md`), not this package's (no change to what any figure shows). Listed.
- A-10: a positive note on the Shows/Does not show lines. No action.

#### Depth B, P4 (the machine-learning practitioner), fresh context, image before caption. Verbatim.

> RECALL
> 1. What this is about: Fitting a "reference surface" to a table of strictly positive, larger-is-better metrics. The surface is a weighted geometric mean V(m) = prod m_j^w_j with the weights on a simplex, set equal to 1 (log V = w·u − β). Optionally it is a sum of K such terms (a posynomial). It is a model of the trade-offs among the metrics, which the fit finds. The paper is built to analyse a trade space of designs. The case is a cubesat with 9 traded metrics.
> 2. The main result: Seven numbered results (B01). The ones I would state:
> - The fitted surface is the level set V=1. It is not the Pareto boundary. Position, level and elasticities are read from it (Thm 1).
> - The one-term fit is a geometric program, convex in the log variables (Thm 2, 3). Its exponents are elasticities (Thm 5) and the chart (Z, log V) is a reversible rewrite of the metrics (Thm 6).
> - At K=1 a maximizer of V is weakly Pareto-efficient (Thm 9). The converse is not claimed.
> - The several-term fit is not convex in the terms. It gets three levels of guarantee and a stopping declaration: descent never raises the mean slack (Thm 11), a numerical term-gap stationarity measure (Lemma 1), and conditional local optimality (Prop 3). The soft fit has a second-order certificate (Thm 12).
> - On the cubesat, terms separate contending metric sets that a single term blends (Sec 9).
> - PCA is chained after the fit: the principal directions of the near-frontier chart read the trade-offs the sampling exercised. This is billed as "a reading and not a result" (B01, item 5).
> 3. What you would do next with it: Fit K=1 on my own conditioned metrics, using the temperature sweep to choose tau. Compare the exponent table with PCA loadings on the same log-metrics. Then try K=3 and look at the per-term association maps. I would look for sklearn-style fit/transform, but I have not seen the code.
> 4. What you would tell a colleague: It is an exponent-weighted "efficient frontier" surface, fitted by convex optimisation. The exponents say which metrics trade against which, and the chart gives each design a position and a level relative to the surface. It is more interpretable than PCA because the weights are elasticities. It is also a different object: it is not a Pareto boundary, and with several terms it is only a local optimum with certificates.
> 5. What the method does not do: It does not give the Pareto boundary or a converse of efficiency (Thm 9). It does not give strict convexity (Thm 3) or global optimality for K>1 (Prop 3). It does not give convergence or stationarity (Thm 11). The bound in Cor 1 holds for the returned run, not across restarts. The Gaussian cumulant is "a population identity, with no consistency claim" (Prop 2). It does not model the evaluation itself, since the figures say they do not show physics or feasibility. The Fig 8 association map is "an analysis of those designs and not of the model". Conditioning of the metrics is left to the analyst. I could not see any fit-quality or out-of-sample claim in the slices.
>
> THE TWO QUESTIONS
> Q1. A monomial term is one product prod_j m_j^(w_kj) with its coefficient c_k = e^(−κβ_k) (Def 3, B04). The model is a sum of these, raised to the 1/κ power: V_K = (sum_k c_k prod_j m_j^(κ w_kj))^(1/κ). Def 3 also says "Each term is a piece of the surface, not a set of designs; the designs whose largest term it is form its cell." Thm 8 (B21) says that with K=1 the extension is the monomial. I get "monomial" from Def 3 plus Thm 8, and "piece of the surface" from Def 3 and the Fig 1 caption (B08).
> Q2. They belong to a piece of the model, a term. Def 6 (B07): "The contending set of term k is the support ... of the exact-maximum fit to the term's cell; its size n_k names it." Fig 1's caption (B08) says "A term is one piece of the fitted reference surface" and the term's exponent vector sits in a face that names its n-lemma. Item 7 of the main results says "the terms separate contending sets that one term blends". The set is found by fitting each term to its cell of designs, and Fig 8 (B36) draws it as the outlined metrics for each term, using the near-frontier designs of that cell. So a group of designs is how the set is found, but the set is a property of the term.
>
> FRICTION
> - Confusion: Def 6 says "found, not assumed" and defines the set through "the term's cell", which is a group of designs. The Fig 8 caption then says the map is "of those designs and not of the model". I had to work to see that the set belongs to the term but is estimated from the designs.
> - Confusion: "Z0 ... first of eight coordinates, no meaning alone" (Fig 7). Eight coordinates for nine metrics is explained only by the B1=0 constraint in Def 5, and I had to work that out.
> - Confusion: Def 4's "exact-maximum fit" versus "fit temperature" versus "term temperature" (tau versus kappa). The two temperatures are easy to mix up.
> - Confusion: the mean-versus-sum aggregation in Def 3 ("sum by default, or mean; the formula is the sum").
> - Confusion: Thm 2's "R1 for the facet-normal reading" and "Balanced hard-support geometry does not imply an interior minimizer at finite tau". Both mean nothing to me at this depth. The hypothesis labels (A1 to A8, F5, F10, F12, I5, I14, R2) are used without a key on the slice.
> - Confusion: Fig 5 says total mass and energy balance are "its two heaviest metrics", but the line sits well off most of the points. Only the caption's median-slice explanation resolves this.
> - Confusion: Fig 9 and Fig 8 both mark the outlined metrics with grey labels. "w=0.00" next to an outlined metric (for example power margin in Fig 8 term 1, outlined as grey) is explained only in the caption.
> - Guessed terms: "reach" β (I guessed the data's extent along w, a soft maximum of scores, which Def 7 does state). "Energy differential" for log V (I guessed it is the signed level relative to the surface; I did not see an energy defined). "Primary / stock regime" (I guessed two controller-gain settings; the Fig 9 caption confirms it). "Participation threshold" (I guessed exponents above 0.001). "n-lemma" (I guessed the count of metrics that contend in a term). "Cell" (I guessed the set of designs for which this term is the largest).
> - Would I read one level deeper? Yes. I would read the Sec 9 case and the sklearn-style usage section (Sec 11). I want to see what the chart and the sweep look like on my own data. I also want to see how PCA is chained (Appendix D.16) and what "reading, not a result" means in practice.
>
> FINDINGS
> 1. Figure 1 image (B08-a) alone gives a clear triangle of corner, edge and interior faces with three terms and planted rings. The caption added the labels "dilemma" and "trilemma" and the "Shows / Does not show / Good for" box, which I found useful. B08.
> 2. Figure 2 (assembly) shows a UML-like diagram of cubesat parts with swap and tune variables, which a non-systems reader can follow. The caption confirms that the diagram omits ranges and physics. B30.
> 3. Figure 3 (behavioural) is dense. The image alone showed requirements linked to metrics, but the caption was needed to say that the nine traded metrics are what the study trades and that mass reaches launch cost. The caption says "returns 8 of 9" and "seven" computed while the box mentions pointing error and total mass computed with no slew, so counting 9, 2 passed on and 7 computed requires careful reading. B31.
> 4. Figure 4 (tau sweep) alone shows the fraction above V=1 falling with tau and an exponent heat-map with a chosen column. The caption explained the "target 0.1" and the outlined column, and tau is chosen where the fraction first meets 0.1. A reader wonders why the target is 0.1; I found no justification on the slice. B32.
> 5. Figure 5 (plane-1) shows a scatter of designs with a straight line and a band. Many points sit beyond the line. It is "the surface in this slice", not a frontier, and the caption is needed to understand that. B33.
> 6. Figure 6 (plane K=3) shows three panels with one segment per term. Points above the line "still inside the surface" read oddly without the caption. The bottom panel (banded points) is explained at length in the caption, which borders on explaining the data rather than the method. B34.
> 7. Figure 7 (chart) shows the log V against Z0, with most designs below the flat line. The axis label "no meaning alone" makes the x-axis uninformative, so the figure carries only the distribution of levels. B35.
> 8. Figures 8 and 9 are heat maps of Pearson association with outlined contending sets and greyed labels. They are readable once the grey convention is understood, and the caption says "an analysis of those designs and not of the model". The caption for Fig 8 says a term with fewer than ten near-frontier designs has no map, which the term 2 panel shows as a sentence. B36, B37.
> 9. Item 5 of the main-results list cites Appendix D.16 and calls the PCA chaining "a reading and not a result". That is honest but leaves the PCA relationship (the practitioner's first question) unsupported in the main text. B01.
> 10. Def 3 and the main results use "term" for a monomial piece of the surface, and the same word is used for a set of designs' cell elsewhere ("a cell is a set of rows, a term a piece of the surface", Thm 11). Def 3 does disambiguate, but the caution is repeated several times, which suggests the confusion is expected. B04, B24.
> 11. Def 6 defines the contending set via the term's cell but Fig 8 says the map is of designs, not the model, so the ownership of "contending" (term versus designs) needs one explicit sentence. B07, B36.
> 12. Statement blocks cite hypotheses (A1 to A8, F5, F10, F12, I5, I14, I15, I16, R1, R2) with no key at the point of use. A practitioner skimming cannot tell what is assumed. B12 to B29.
> 13. Thm 2's final sentence ("Balanced hard-support geometry does not imply an interior minimizer at finite tau") is opaque without the definition of hard support. B14.
> 14. Thm 12 (soft-fit certificate) says "H = D − κM ... D and M both positive semidefinite" and asks the Hessian to be positive definite on the tangent space. The statement is clear, but the picture of what "the designs' ambiguity between terms" means in the data is not given. B29.
> 15. The "Main results" list item 6, "Numerical: the status a fit reaches. Open: Q1 to Q4 and the search's monotonicity", is cryptic: Q1 to Q4 are not defined on the slice. B01.
> 16. Def 4's near-frontier band, |log V| < 1/tau, with the e-factor reading, is a clear statement. It gives the band in the figures a definition. B05.
> 17. Thm 9 states a weak-efficiency result with the converse not claimed, and Thm 11, Prop 3 and Cor 1 each state a "not claimed" clause. The scope of claims is easy to extract. B22, B24, B27, B28.

**Dispositions, depth B.** Nothing blocks. Each finding is listed for the supervisor's eye unless said otherwise.

- B-10 ("term" used for the piece of the surface and, the reader says, near "a set of designs' cell"; the caution repeated): the reader quotes Theorem 11's "a cell is a set of rows, a term a piece of the surface" and kept the two apart. Vocabulary; not a block. Listed: the repeated disclaimers may be read as a sign of expected confusion.
- B-11 (the contending set is defined through the term's cell, Figure 8 says its map is of the designs): the semantics A2 chose (a thing of the model takes "term", of the assignment "cell"); the reader concluded "the set is a property of the term". Listed as the one sentence the reader asks for.
- B-12, B-13 and the friction on Theorem 2 ("R1 for the facet-normal reading" means nothing at this depth): the A1 word is the only "facet" a depth-B reader meets, unglossed, in a hypothesis line. A1 keeps it by decision; listed.
- B-9, B-15 (the PCA chaining "a reading and not a result"; "Q1 to Q4" undefined at the list): the main-results list; listed.
- B-3 to B-8, B-14 (figure and caption readings: the behavioural view's counts, the 0.1 target, the K = 1 and K = 3 planes, the chart's axis, the heat maps' grey convention, the soft certificate's picture): for the figure loop; no change to what any figure shows is in this package. Listed.
- B-1, B-2, B-16, B-17: positive notes. No action.

### Checklist

Each item checked now, at `944c564`, on this Mac (macOS, the locked environment), unless a record is named.

#### Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `glossary.yaml`: no `facet` or `facet gap` entry; `term-gap` at L431; the `term` entry's register "monomial term", "facet" under its `avoid` with the reason (L139-140), the polyhedral exclusion in its `not`; "facet" in `assumed` with the A1 reason (L595-596); `stems` (L598 on) has no `facet`. The compiled glossary page is git-ignored and built at staging: `_stage/docs/generated/glossary/index.html` has 0 "facet" and carries "monomial term". |
| D-2 | met | 37 Markdown cells of `paper/paper.ipynb` changed in `9df7483` (cell diff script); the abstract's gloss renders ("Each monomial term (a product of powers of the metrics)", browser and slice A1); the quilt sentence renders; headings "6.2 The algorithm for several terms" (rendered) and "B.2 The several-term fit" (supporting material's table of contents). Re-executed in `hts-paper` `e852cde39180` for push 3 (`RECORD.md`, entry of push 3). |
| D-3 | met | `paper/paper_terms.py` exists, `paper_facets.py` gone; `[values.term_numbered_tables]` in `environment_values.toml`; `RECORD.md` entries for pushes 1 to 4 (L314, L349, L405, L428; push 4 on the host by the supervisor's rule of 09:05). |
| D-4 | met | `uv run pytest -q tests/test_claims_register.py`: 21 passed. `[[claim]]` rows: 399 before and after each WP24 commit (`204e7c3^`, `204e7c3`, `a5c67f2`, `9df7483`, `a2e6bd5`: 399; 386 at `62a086a`, the 13 added by other packages meanwhile). |
| D-5 | met | `uv run python derivation/run.py`: "ALL LEMMAS PASS."; `uv run python -m derivation.proofmap`: "PROOF MAP OK: 17 lemma files, 371 tagged steps"; `derivation/lemma_12_term_gap.py` exists; the moved-steps listing and the update diff are in the session scratchpad (`wp24p2/`, as the push 2 section says); Appendix B test in the container for push 2 ("8 passed, 140 deselected", `wp24p2/container.log`) and now on the host (8 passed). |
| D-6 | met | `grep -rn facet src/`: no output (exit 1). The A2 names present (push 1 table above, reconfirmed by the passing suite). |
| D-7 | met | `work-packages/interface-contract.toml`: `contract_version = 14`; change-log row 14 says "Non-additive", lists every renamed pinned name, and cites "`WP24-scope-of-work.md`, gate outcome 2026-11-09 22:50 (the driver under the mandate); `WP24-decisions.md`". The scope's "version 11" is explained in the row (rows 12 and 13 landed first). `uv run pytest -q tests/test_interface_contract.py`: 90 passed. |
| D-8 | met | Test changes per WP24 commit compared after normalizing the renamed words (`wp24reads/tools/testdiff.py`): every change is a rename or phrase except (a) `test_interface_contract.py` R-4 and `test_k_terms_case.py` (three figure tests removed with the k3 case figures, see G-3), (b) `test_paper.py`'s Figure 1 hash (the key name enters the hash, see Observations), (c) `test_narrative.py`'s map added in push 1 and removed in push 2 (decided 06:35 and 06:45). `test_vocabulary.py`'s made-up word is "tile" (A9). No assertion weakened in what I read; `test_plotting.py`'s label guards now assert both words absent. |
| D-9 | met | `term_record` in `k_terms.py`, `term_table` in `case.py`; `examples/adcs/experiments/reports/sensitivity.json` at `204e7c3` equals its parent under the key rename (`json` comparison: "equal under rename: True") and is unchanged since. The case notebook went before this package (`4bd6bac`), so its prose is moot. |
| D-10 | met | Figures with changed labels read as images: `fig-nlemma` ("term 1" to "term 3", "Each term's exponent vector"), `fig-planes-k3` ("term 1" to "term 3", "one segment per term"), `figure1.png` ("term 1" to "term 3", "terms laid flat"), the docs' `three-terms-{light,dark}.png` (no word in the image). Reproduction: see R-10. |
| D-11 | met | The docs pages and the root page carry no "facet" (`grep` over the staged HTML: none outside the paper); the docs home renders the gloss ("a sum of monomial terms, where a monomial term (a product of powers of the metrics) is one trade-off"). `CHANGELOG.md`, added to the reader surfaces by the driver (00:35), still carries the word: G-1. |
| D-12 | met | `scripts/vocabulary_baseline.toml`: 0 lines with "facet". |
| D-13 | met | This file: per push the hashes (pushes 1 and 2 in their sections; pushes 3 and 4 in `WP24-decisions.md`, 09:30, and above), the checks, the A1 list, the statements, and the cold reads in this section. |
| D-14 | met | `WP24-decisions.md` records the approval by reference to the gate line and every decision of execution; the acceptance is pending, by design. |

#### Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | `uv run python scripts/check_vocabulary.py --baseline scripts/vocabulary_baseline.toml`: "0 new violation(s), 69 known", exit 0. Without the baseline: "69 new violation(s), 0 known", exit 1, none of them the word (the 69 are the known baseline rows). `uv run pytest -q tests/test_vocabulary.py tests/test_build_generated.py`: 42 passed. |
| R-2 | met | The scope's grep, per file, compared line by line with push 4's list: `glossary.yaml` 3, `derivation/axioms.py` 3 (L600, L604, L607), `lemma_11_pareto.py` 1 (L23), `scripts/build_generated.py` 1 (L87), `paper/paper.ipynb` 2 (the two marked A1 lines), `supporting_material.ipynb` 10 (L3.9 three times, the record paths `spike-facet-refit/` and `dup_facets.py`), `generate_proofs.py` 4, `generate_results.py` 1, `environment_values.toml` 1, `RECORD.md` 17, `BROWSER_NOTES.md` 7, `length_ledger.toml` 27, `PROOF_MAP_FINDINGS.md` 1 (the quotation), `claims_register.toml` 1 (C394's source), `tests/test_paper.py` 5 and `test_diagnostic_pair.py` 1 (negative guards), `interface-contract.md` 5 (rows 3, 7, 8, 11, 14), `scripts/rename_facet.py` 104, `tests/test_rename_facet.py` 70, `scripts/check.py` 1. Every line is on the list; nothing else. (`rename_facet.py` and its test are gone at `origin/dev`, deleted by WP25.) The scope's grep does not cover `CHANGELOG.md`: G-1. |
| R-3 | met | As D-7: 90 passed; version 14 equals the last row; the row says non-additive and cites the approval. |
| R-4 | met | `grep -rn facet src/`: nothing. `git diff 62a086a...HEAD -- src/` added lines matching `DeprecationWarning\|warnings.warn`: 1, from `18d0064` ("Estimator: the iteration-cap warning fires only when the fit is not stationary to tol", a ConvergenceWarning, not WP24's); no alias, property or `getattr` bridge among the added lines. |
| R-5 | met | `uv run pytest -q -n auto tests/test_paper.py tests/test_k_terms_case.py tests/test_sensitivity.py`: 163 passed, 4 skipped; `test_soft_fit.py` in the R-6 run below. `PYTHONPATH=examples/adcs uv run python -m experiments verify`: "34 entries (11 current); 0 drifts". Word diff of the WP24 commits only (the range from `62a086a` mixes in the data swap `ea46637`): `sensitivity.json` equal under the key rename; `environment_values.toml` (`204e7c3^..5b01248`) changes words only plus the Figure 1 data hash, whose input includes the array's key name (see Observations). |
| R-6 | met | `uv run pytest -q -n auto tests/test_estimator.py tests/test_solvers.py tests/test_soft_fit.py tests/test_sklearn_compat.py tests/test_matches_derivation.py`: 821 passed, 12 skipped, 1 xfailed. Test changes: as D-8. `tests/data/soft_fit_default_reference.npz`: keys renamed, arrays equal (push 1's record; the soft-fit tests pass against it). |
| R-7 | met | As D-5; `uv run pytest -q -n auto tests/test_proof_map.py tests/test_derivation.py`: 205 passed; `uv run pytest -q tests/test_paper.py -k appendix_b`: 8 passed, 140 deselected (host); the container run for push 2 recorded the same. |
| R-8 | met | As D-4: 21 passed; 399 rows before and after; push 3's 26 fragments and push 4's 24 followed their sentences (the push sections), none dropped by WP24. |
| R-9 | met | `uv run pytest -q tests/test_paper_sources.py tests/test_paper_static_figures.py tests/test_narrative.py`: 24 passed; `test_paper.py` as R-5. `tests/test_notebook.py` no longer exists (deleted with the case notebook, `4bd6bac`). `RECORD.md` names the image and head for pushes 1 to 3 (`9c8a0c616386` at `541efcd`; `e852cde39180` at `90c8848` and `3a66e78`); push 4 regenerated on the host by the supervisor's rule of 09:05 and names no image. The container regression re-pinning exact outputs for pushes 3 and 4 is the driver's at the gate and is not yet run (driver log, 09:40); not counted against R-9. |
| R-10 | met | `uv run python scripts/build_figures.py` (paper static figures written in place) and `uv run python paper/figures/figure1.py`: `fig-nlemma`, `fig-planes-k1`, `fig-planes-k3`, `fig-chart-level`, `figure1.png` are **pixel-identical** to the committed files (mean absolute difference 0.000, 0 pixels differing) but not byte-identical (PNG encoding on the host differs from the container's; `figure1.svg` differs in text); restored with `git checkout`. Docs figures rebuilt into a scratch folder: 16 of 16 byte-equal to the staged build; `scripts/build_site_figures.py`: both images byte-equal to the staged ones. `uv run pytest -q -n auto tests/test_plotting.py tests/test_site.py tests/test_docs.py`: 115 passed; `test_paper_static_figures.py` passed (R-9). |
| R-11 | met | Read: the abstract's first use "Each monomial term (a product of powers of the metrics) reports its contending metrics, an n-lemma"; the docs' first use (the docs home) "a sum of monomial terms, where a monomial term (a product of powers of the metrics) is one trade-off". Spot-check of push 3's statements list: "n-lemma" for the contending metrics only; "cell" for designs only ("an empty cell", "the term's cell"); "trade-off" once in the definitions ("one per trade-off") and in the abstract's "several trade-offs are active". No use of one word for another found. The docs home's "a monomial term ... is one trade-off" reads term and trade-off as one: an observation. The tool's first-use check passes (R-1). |
| R-12 | met | Sample of 12 cells of `paper/paper.ipynb` read word by word against push 3's list (`9df7483^..9df7483`): `sec-definitions`, `fig-nlemma-caption`, `sec-definitions-2`, `res-L15`, `res-L12`, `res-L13`, `res-L14a`, `res-L14b`, `res-L3`, `sec-methods`, `sec-simplifying`, `fig-planes-k3-caption` (`wp24reads/r12/paper-push3-sample.txt`). Every change is the word, the marker, or a clause the review lists ("a facet:" dropped in Definition 3; Definition 7's clause; "summand"; "the term's cell"; "The several-term fit alternates"). Derivation: `a5c67f2` for `axioms.py` and `lemma_13_margin.py` read: words only ("every cell is nonempty", "several-term objective"). |
| R-13 | not met (narrowly) | `git diff --stat 62a086a...HEAD -- work-packages docs/superpowers/notes`: 230 files, of which WP24's commits touch `WP24-review.md`, `WP24-scope-of-work.md` (A5's amendment), `interface-contract.md`, `interface-contract.toml`, `docs/superpowers/notes/paper-sources/{api,limitations,method}.md` (A5 amended), `docs/superpowers/notes/notation.md` (the PM's option 1 under the driver's rule of 06:35) and `docs/superpowers/notes/abstraction-gaps.md` (push 4; the source of Appendix E; no decision names it): G-2. Every other file in the stat belongs to WP23, WP25, WP25-2, WP19, WP10, the briefs and the driver's records (attributed by commit). |
| R-14 | met | Hashes as above. Verdicts from the driver's record: push 1, Mac watcher green at `1addf79` (2191 passed); Linux red at `bd017dc` on a stale Appendix A table from another package's glossary entries, green at `e89abee` (pushes 1 and 2); push 2, Mac green at `7ee26be`; pushes 3 and 4, Linux green on `ee7704e` (`7d7c4a5`, after this review's head), the Mac watcher's run "next" in that row; this review's own Mac run at `944c564` green (R-15). Pushes 3 and 4 landed as one push by the driver's decision (driver log, "push 3 is coherent only with push 4"). `git log --format=%B 62a086a..HEAD \| grep -ci "co-authored-by"`: 0; "generated with": 0. |
| R-15 | met | `uv run pytest -q -n auto` (the whole suite, slow included): 2191 passed, 16 skipped, 1 xfailed, exit 0 (6 min); `uv run ruff check .`: "All checks passed!"; `uv run ruff format --check .`: "325 files already formatted"; `uv lock --check`: "Resolved 178 packages". Linux: green on `ee7704e`, the rename's head (`7d7c4a5`). |
| R-16 | met | This section: two cold reads from the staged build, verbatim, with dispositions; nothing blocks. |

#### Definition of good enough

| Item | Verdict | Evidence |
|---|---|---|
| The tool finds no "facet" outside A1 and the records; the grep agrees with the list | met | R-1, R-2 (`CHANGELOG.md` sits outside the grep: G-1) |
| Public names renamed, contract at its version with the non-additive row, no shim | met | R-3, R-4 (version 14, not 11, as the row explains) |
| No number moved, the fit unchanged, statements listed and differing only by the vocabulary | met | R-5, R-6, R-12 |
| Derivation, proof map, Appendix B, register, paper build, figures, the gloss | met | R-7 to R-11 (figures pixel-identical, not byte-identical, on the host) |
| Records untouched; each push one surface, landed after or rebased, green at tier 2 | not met (narrowly) | R-13 (`abstraction-gaps.md`, G-2); R-14 met with pushes 3 and 4 as one push by decision |
| Suite green on both platforms | met | R-15 |
| Two cold reads, verbatim, dispositions; blocking findings fixed and re-read | met | R-16; none blocks |

#### Non-goals (touched?)

| Non-goal | Touched? | Evidence |
|---|---|---|
| No change of mathematics or statement beyond the word | no | R-12 sample; the derivation chain and the proof map pass |
| No change to the fit | no | R-6; the one new warning rule in `src/` is `18d0064`, not WP24's |
| No deprecation layer | no | R-4 |
| The records untouched (A5 as amended) | yes, one file | `docs/superpowers/notes/abstraction-gaps.md` (G-2) |
| No reopening of the vocabulary decision | no | |
| No new figure, no change to what any figure shows | yes, by deletion | push 1 deleted the six `examples/adcs/figures/k3_*.png`, `k_terms.save_figures` and its helpers, three figure tests, and the case figure pins of the contract (G-3) |
| Not this package (WP8b, WP11, WP16, WP23) | yes, a neighbour's items | push 4 closed WP25's drift rows 10 and 13 to 17 in the docs and the glossary, and edited `paper/prior_art.yaml` (outside the blast radius list) (G-4) |

### Outside the scope

`git diff --stat 62a086a...HEAD`: 95 files are touched by WP24's commits (list in the session scratchpad,
`wp24reads/wp24-files-unique.txt`); the rest of the range is WP23 (rounds, gate, the data swap `ea46637`, the
fix-forward, the close-out scope), WP16 step 4, WP25 and WP25-2 (deletions, drift rows, Appendix E), WP19, the
estimator's warning rule `18d0064`, and the driver's and PMs' records. WP24 files outside its blast radius:
`docs/superpowers/notes/abstraction-gaps.md`, `docs/superpowers/notes/notation.md`, `paper/prior_art.yaml`,
`scripts/rename_facet.py` with `tests/test_rename_facet.py` (the preparation tool; deleted since by WP25), and the six
deleted case figures.

- **Out-of-scope changes:** the k3 case figures' deletion with `save_figures` and the contract's case figure pins (G-3);
  WP25's drift rows closed in push 4 and `paper/prior_art.yaml` reworded (G-4); `abstraction-gaps.md` (G-2); the
  rename tool (preparation, gone since).
- **Non-goals touched:** the records (G-2), what figures exist (G-3), a neighbour package's items (G-4).

### Observations (not counted as failures)

- The root page still carried `site/paper-map.webp` at `944c564` (the driver's call of 09:30 that it goes); it went at
  `bb51b7e`, after this review's head, with claims C362 to C366.
- The supporting material's Appendix E shows raw `$...$` in its page text (seen in the browser); the driver routed it
  to the close-out's regeneration (09:30). Not WP24's.
- Figure 1's data hash moved (`environment_values.toml`, `tests/test_paper.py`) because the array's key name is an
  input of the hash; the arrays are byte-equal. Recorded in push 1; the number of a figure did not move.
- `docs/superpowers/notes/paper-sources/`: besides the A1 sentences, `why-and-how.md` L32 ("We use the term n-lemma for
  a facet of the achievable ...") and `literature.md` L79 (a quotation of the spec) keep the word. The amended A5 lets
  these notes take the vocabulary; they are outside the tool's corpus.
- Push 4's section says the new `RECORD.md` entry "has none" of the word; the entries of pushes 1 to 3 name the old word
  as what was removed (L316, L351, L407).
- The docs home's "a monomial term (a product of powers of the metrics) is one trade-off" equates the term and the
  trade-off; the supervisor's own framing ("monomial terms kernels representing trade-offs").
- `notation.md` took word edits, not only identifiers, under the PM's option 1; the driver's rule of 06:35 speaks of
  identifier edits for records a test reads.
- The cold-read findings listed above for the supervisor's eye (A-2 to A-9, A-11, A-12; B-3 to B-15).

### Open decisions (for the driver)

- **G-1.** `CHANGELOG.md` L20 still says "sharp facet assignment"; the driver made `CHANGELOG.md` a reader surface that
  takes the vocabulary (`WP24-decisions.md`, 00:35), and the scope's grep does not list it. Options: accept as is /
  fix before acceptance / follow-up work package.
- **G-2.** `docs/superpowers/notes/abstraction-gaps.md` (the gaps ledger, source of Appendix E) took the vocabulary and
  the renamed test names in push 4; A5 as amended names only `paper-sources/*.md`. Options: accept as is / fix before
  acceptance / follow-up work package.
- **G-3.** Push 1 deleted the six k3 case figures (`examples/adcs/figures/k3_*.png`, coloured by cell), `k_terms.save_figures`
  and its helpers, three figure tests, and the contract's case figure pins (row 14, citing "the PM's brief for WP24
  push 1"); no deliverable and no recorded decision of the driver cover it, and the non-goal is "no change to what any
  figure shows". Options: accept as is / fix before acceptance / follow-up work package.
- **G-4.** Push 4 closed WP25's drift rows 10 and 13 to 17 (`chart.md`, `theory.md`, three glossary entries) in the same
  edit and reworded `paper/prior_art.yaml` (outside the blast radius list). Options: accept as is / fix before acceptance /
  follow-up work package.
- **G-5 (observations, one item).** The observations above and the cold-read findings listed for the supervisor's eye.
  Options: accept these as is / pick any to act on.

### Gap dispositions

| Gap | Disposition (accept as is / fix before acceptance / follow-up work package) | Reason or follow-up |
|---|---|---|
| G-1 | open (the driver's) | |
| G-2 | open (the driver's) | |
| G-3 | open (the driver's) | |
| G-4 | open (the driver's) | |
| G-5 | open (the driver's) | |

### What was run and looked at

- Staged build (`stage_site.py --serve --port 8831`, stopped after); the browser pane at 1280 px: the paper (two
  "facet", both A1, the gloss and the quilt sentence present, no stderr or traceback text), the supporting material
  (the word only in L3.9 and the record paths), the docs home (the gloss), the fitting page's `three-terms` figure, the
  root page (the paper map present at this head).
- The slices and prompts: `/private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp24reads/`
  (`slices/`, `prompts/`, `returns/`, `figs/` with the host-built paper figures beside the committed ones, `r12/`,
  `full-suite.log`, `tools/`).
- Commands: every command in the tables above, at `944c564`.

### Recommendation

**Recommend acceptance with the listed gaps noted, once the driver has disposed G-1 to G-4**, because every
requirement but R-13 is met with evidence run now (the suite green on this Mac and Linux green on the rename's head; no
number moved; the A1 sentences are the only uses of the word on the rendered reader surfaces; the contract, the proof
map, Appendix B and the register hold), and both cold readers, at depth A and depth B, say what a monomial term is from
the gloss and put the contending metrics on the term, so no finding blocks. The gaps are a one-line reader surface the
grep missed (G-1), one record edited beyond A5 (G-2), and two out-of-scope edits that went in with the rename (G-3, G-4);
none moves a number or a statement.

Acceptance is the supervisor's act, recorded as named above. This report does not accept the work.
