# WP24 review: the word "facet" goes

Scope: `WP24-scope-of-work.md` (approved 2026-11-09, 22:50, the driver under the mandate; A1 to A10 accepted as
one item). Sequenced after WP23's regeneration and data gate, so each surface is touched once. This record is
written in the order of the work: the preparation first, then one section per surface push (A3), the
statements touched, the vocabulary tool's result and the two cold reads (R-16).

## Preparation (no surface touched; `dev` at `abdb88f` when the dry run was taken)

### The rename script

`scripts/rename_facet.py` applies the rename one surface at a time, in the order of the pushes:
`--surface code | derivation | paper | docs | all`, with `--dry-run` (counts per file, nothing written) and
`--verbose` (the lines the script leaves for the hand pass). Per file it protects the τ = ∞ polyhedral
sentences (A1) and the names of files a later surface moves, applies the file-specific literals (the cell
wording of the assignment sense), the name table (A2 and the private names), a generic identifier rule
(`facet` inside an identifier becomes `term`) and the prose vocabulary (word-boundary swaps, the hyphenated
compounds, `several-facet` and `multi-facet` to `several-term`, `one-facet` and `single-facet` to
`one-term`), restores the protected text and, in Markdown, prepends `<!-- vocab-exempt: facet -->` to a
paragraph that keeps the polyhedral word. Notebooks: cell sources and cell ids only; outputs are regenerated
in the container. The claims register moves row by row: backing references (test and function names) with
the code push, a row's fragment, anchor and note with the push of the file the row cites, `glossary:facet`
with the docs push. File moves are `git mv` (A10): `paper/paper_facets.py` to `paper/paper_terms.py` in
push 1, `derivation/lemma_12_facet_gap.py` to `derivation/lemma_12_term_gap.py` in push 2.

Never edited by the script: `work-packages/*.md` (the contract's pinned sections 4 and 7 and its new row are
a hand edit), `docs/superpowers/notes/` (A5), `paper/container/RECORD.md` (A4), `examples/adcs/model_v2/`
(the scope's never list), `tests/test_vocabulary.py` (A9), `glossary.yaml` (the patch below, last push),
the generated files (`proof_map_record.json`, `figure1.svg`, the notebook outputs).

Idempotent: a second run over a fully renamed copy of the tree changes no file (`files changed 0` on every
surface). Unit test: `tests/test_rename_facet.py` (34 checks: the name table applied, the polyhedral
sentence kept verbatim and marked, the records untouched, the register rows moving with their surface, the
dry run writing nothing, two runs equal). `scripts/check.py` maps the script to its test.

### Dry run over `abdb88f`, by surface

Columns: `names` identifier, literal and reference replacements; `prose` word swaps; `kept` polyhedral
sentences left as they are (A1); `review` sentences flagged for the hand pass (membership wording, the
geometry sentences); `left` occurrences the script does not change in that push (for a names-only file, its
prose, which moves with its own surface); `outputs` occurrences in committed notebook outputs (regenerated).

| Push | Surface | Files changed | names | prose | kept | review | left after the push | outputs to regenerate |
|---|---|---|---|---|---|---|---|---|
| 1 | `code` (src, tests, case code and report, paper and figure generators, scripts, manifests; notebook code cells and ids; register backing refs) | 38 (+ 1 move) | 329 | 643 | 4 | 55 | 297, all prose of later surfaces (`paper.ipynb` 95, `claims_register.toml` 112, `test_paper.py` 46, `supporting_material.ipynb` 19, `test_proof_map.py` 11, `test_derivation.py` 5, `test_site.py` 5, the case notebook 3, `test_build_generated.py` 1) | 714 |
| 2 | `derivation` (lemma scripts, findings, the two derivation tests; the module reference in `paper.ipynb`) | 13 (+ 1 move) | 15 | 122 | 3 | 35 | 94 (`paper.ipynb` prose, push 3) | 18 (Appendix B) |
| 3 | `paper` (both notebooks' sources, the case notebook, length ledger, prior art, `test_paper.py`, `test_narrative.py`, the register's paper rows) | 7 | 25 | 252 | 3 | 34 | 87 (the register's docs rows 79, R1 and its marker) | 714 (the container run) |
| 4 | `docs` (docs pages, site, README, vocabulary baseline, `test_site.py`, `test_docs.py`, `test_build_generated.py`, the register's docs rows; the glossary patch) | 13 | 25 | 135 | 0 | 14 | 0 | 0 |

Per file counts: `uv run python scripts/rename_facet.py --surface all --dry-run` at the head of the push.
Largest single files: `sensitivity.json` 149 prose (generated keys, text only; the ledger verify must report
0 drifts, R-5), `paper.ipynb` 94 prose, `solvers.py` 31 names and 57 prose, `generate_results.py` 53 prose,
`test_paper.py` 20 names and 46 prose.

After all four pushes applied to a copy of the tree (plus the glossary patch), the word remains only in: the
kept sentences and their markers (below), the committed notebook outputs and `proof_map_record.json` and
`figure1.svg` (regenerated), `tests/test_vocabulary.py` (A9, by hand), `paper/container/RECORD.md` (A4), and
the files of the questions below. The vocabulary tool on that copy, with the patched glossary and the
repository baseline: 2 new violations, both `avoid: facet` in notebook outputs not yet regenerated; no dead
entry, no new first-use failure, the R1 paragraph passes by its marker.

### The τ = ∞ sentences that keep the word (A1)

| Where | Sentence (the kept phrase) | Marker |
|---|---|---|
| `paper/paper.ipynb`, Conditions of the theory | "R1: the balanced point lies in the relative interior of a facet of the supporting envelope with positive normal" | the script prepends `<!-- vocab-exempt: facet -->` to the paragraph (push 3) |
| `derivation/axioms.py`, R1 statement | "the balanced point lies in the relative interior of a facet of the frontier with positive normal" | none needed (the tool does not read `derivation/`); Appendix B's compiled text is checked at push 2 |
| `derivation/axioms.py`, R1 failure mode | "at a vertex, an edge or a facet with a zero normal component" | as above |
| `derivation/lemma_11_pareto.py`, docstring | "The facet that blocks u′ is one active at u, not at u′" | as above |
| `scripts/build_generated.py`, the generated regularity paragraph | "R1 (the balanced point lies in the relative interior of a facet with positive normal)" | the generated page is under `docs/generated/`, which the tool does not read; the generator string is kept verbatim |
| `examples/adcs/adcs_trade_study.ipynb`, the conditions cell | "R1, the balanced point lies in the relative interior of a facet with positive normal ... (a vertex, an edge or a facet with a zero normal" | the script prepends the marker (push 3) |

The glossary patch lists `facet` under `assumed` with this reason and under the `term` entry's `avoid`
(so a return of the word anywhere else fails the check, G6).

### What the script leaves to the hand pass, by push

- Push 1 (`code`): the contract's sections 4 and 7 and the new change-log row (below), with the manifest's
  pinned lists moved by the script; the tautologies the swap produces where a sentence said "the facet whose
  term scores" (the script maps the common form to "the term that scores"; the diff is read for the rest);
  the `plotting` legend tests (`cell 1 .. cell K` for colouring by assignment, `term k:` for the tension
  heatmaps; the script applies both, the tests decide); `tests/test_vocabulary.py`'s made-up term (A9);
  regeneration: `scripts/build_figures.py`, `scripts/build_site_figures.py`, the committed exact tables of
  the supporting material in `hts-paper` (table headers "facet rows", "facet shares", "facet k" change),
  `environment_values.toml` section `term_numbered_tables`, the ledger verify (`experiments verify`, 0 drifts).
- Push 2 (`derivation`): read L13 to L15's "maximizing term" (the swap of "maximizing facet"; the cell
  wording where the sentence is about rows), `proof_map_record.json` regenerated, Appendix B in the container,
  `uv run pytest -q tests/test_paper.py -k appendix_b` output in this record (the mechanical rule).
- Push 3 (`paper`): the sentence rewrites the spike classed R, flagged by the dry run (`--verbose`): the
  Preliminaries' "A term, a monomial and a facet are one object ... facet for the geometry and term for the
  algebra" (A6: the quilt sentence), "how sharply facets meet", the membership sentences ("the designs that
  facet k dominates", "the cell of its maximizing facet", "regroup the rows by facet"), the captions "one
  straight segment per facet", "**Three facets.** At K = 3 the tension separates into three facets", the
  supporting material's "D.13 The refit on a facet's own rows" and "a facet's near-frontier designs"; the
  gloss at the first use of "monomial term" in the abstract (A7); the register fragments of the rewritten
  sentences; the `test_paper.py` phrase pins of the rewritten sentences; the length ledger's `job` and `reader`
  texts that describe the facet-is-not-a-cluster sentences (they describe sentences that change: reword or
  retire with the sentence); both notebooks re-executed in `hts-paper`; `paper/container/RECORD.md` entry.
- Push 4 (`docs`): `fitting.md` "One term is one flat facet in log space" (the swap gives "one flat term";
  rewrite), `tensions.md` "the rows that facet dominates", `termination.md` "which facet dominates which
  design", `examples.md`'s ternary alt text and region sentence; the gloss at the docs' first use (A7, the
  home or getting-started page); then the glossary patch applied, `docs/generated/glossary.md` recompiled,
  `scripts/check_vocabulary.py` exit 0 with the baseline.

### The interface-contract amendment (draft; the version is one above whatever it is at push 1)

The manifest is at `contract_version = 11` today (row 11 is WP19's colour amendment; the scope was drafted
against 10). The draft row, for section 14 of `interface-contract.md`, with `contract_version = 12` in both
files if nothing lands between:

> | 12 | 2026-11-10 | The word "facet" goes (WP24; the supervisor's "Everything before 0.1", `WP10-decisions.md`): the pinned names of the model object and of the assignment are renamed, with no alias and no deprecation period (pre-0.1, nothing released; the deprecation clause of this section is not invoked). Estimator: fitted attributes `facet_` to `cell_` and `facet_share_` to `term_share_`; method `assign_facets` to `assign_cells`; constructor keyword `facet_step` to `refit_step` (values `"support"`, `"tangent"` unchanged). `solvers`: `facet_gap` to `term_gap` (signature `["U", "w", "ubar", "tau", "min_exponent", "p"]` unchanged), `facet_objective` to `term_objective`, `single_facet_termination` to `single_term_termination`. `plotting`: `facet_labels` to `cell_labels` (labels `"cell 1" .. "cell K"`); the option value `color="facet"` of rows 11's plots becomes `color="cell"`. Case (`case.signatures.k_terms`): `facet_record` to `term_record`, parameters unchanged. `datasets`: the `info` key `"facet"` to `"term"`. Non-additive: pinned names are renamed; no fitted number, no figure content and no data file changes (the regenerated tables and reports differ in text only) | both | `WP24-scope-of-work.md`, gate outcome 2026-11-09 22:50 (the driver under the mandate); `WP24-decisions.md` |

Sections 4 and 7 of the document change by the same names (the quoted manifest block in section 2 follows
the `.toml`); rows 3, 7, 8 and 11 keep their wording (A4).

### Held in the worktree `wp24` (not pushed)

- `wp24-glossary.patch` (80 lines changed in `glossary.yaml`): the entry `facet` removed; `facet-gap` becomes
  `term-gap`; the `term` entry becomes the model object's full name `monomial term` with aliases `term`,
  `terms`, `monomial terms`, its `short` glossing the term as a product of powers of the metrics and its
  `not` carrying the polyhedral exclusion; `facet` under that entry's `avoid` with the reason; the
  cross-references in `cell`, `n-lemma`, `elasticity` (and its `avoid` reasons), GP and GGP, `assignment
  margin`, `stable radius`, `conditioning of the exponents`, `ternary plot`, `share`, `region` rewritten;
  `facet` added to `assumed` with the polyhedral reason; `facet` removed from `stems`. It lands with push 4
  (A3: a `facet` entry would be dead before the docs drop the word).
- A fully renamed copy of the tree under the session scratchpad (`wp24-cumulative`), the evidence for the
  counts above; it is not a worktree and nothing is pushed from it.

### Questions for the PM (problem level; found by the dry run, not decided here)

1. `examples/adcs/model_v2/diagnostic_pair.py` is on the scope's never list, yet it calls `case.facet_table`,
   reads `est.facet_` and `est.facet_share_` and strips the column name `facet` from the case tables
   (`TERM = re.compile(r"^facet\b")`, "a round's record says term"). After push 1 it breaks (no shim).
   Options: (a) the scope's blast radius admits this one file for the identifier renames only (the data,
   ledger and model code stay untouched); (b) WP23 (its owner) makes the identifier change in its own unit,
   sequenced right after push 1.
2. Three files carry the word and are in no list of the scope: `CHANGELOG.md` (one line, the K > 1 entry),
   `paper/BROWSER_NOTES.md` (8, browser-pass notes), `docs/superpowers/specs/2026-11-07-...-design.md` (17,
   the design spec). Options: (a) records, kept as written like `docs/superpowers/notes/`; (b) `CHANGELOG.md`
   alone is a reader surface and gets the word swap in push 1, the other two are records.
3. `tests/test_diagnostic_pair.py` asserts that no header carries "facet" (the WP23 round records say
   "term"); the script skips it so the assertion keeps its meaning. No decision needed; noted so the executing
   unit does not "fix" it.

Note, no decision needed: `docs/generated/figures/` is not committed (`.gitignore`), so D-10's
`three-facets-*.png` rename is a path change in `docs/user-guide/fitting.md` and the pin in `tests/test_site.py`
(push 4, the script does both); the images are rebuilt by `scripts/build_site_figures.py`.

### Estimated time per surface push (agent time, one stream)

| Push | Script | Hand pass and tests | Regeneration | Total |
|---|---|---|---|---|
| 1 `code` | 1 min | 1.5 to 2 h (the diff of 38 files, the contract's sections and row, the legend tests, A9) + fast suite | figures 10 min; the supporting material's committed tables in `hts-paper` (as WP23 timed its runs); the ledger verify | 3 to 4 h |
| 2 `derivation` | 1 min | 30 to 45 min (step text read, `derivation/run.py`, the proof-map checker) | `proofmap --update`; Appendix B in the container; the appendix test in a clean worktree | 1.5 to 2 h |
| 3 `paper` | 1 min | 2 to 3 h (about 20 sentence rewrites with their register fragments and pins, A6, A7, the ledger texts) | both notebooks in `hts-paper`; `RECORD.md` entry | 3 to 4 h |
| 4 `docs` | 1 min | 1 to 1.5 h (the R sentences, A7's docs gloss, the glossary patch, the compiled glossary, the tool green, `test_site`, `test_docs`) | `docs/generated/glossary.md` | 1.5 to 2 h |
| Cold reads (R-16) | | two fresh readers from the staged build, dispositions | | about 1 h |

## Push 1: code (to be written at the push)

## Push 2: derivation (to be written at the push)

## Push 3: paper (to be written at the push)

## Push 4: docs and glossary (to be written at the push)

## Statements (R-12: before and after, to be written per push)

## Cold reads (R-16: to be written after the last push)
