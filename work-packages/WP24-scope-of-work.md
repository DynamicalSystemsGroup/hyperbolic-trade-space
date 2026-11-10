# WP24 — Scope of work: The word "facet" goes (one name for the model object, on every surface, before 0.1)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space` (local: `/Users/z/Documents/GitHub/posynomial-invariant-form`); work on `dev`, merged to `main` at acceptance |
| **Approval record** | The driver's approval under the mandate (`release-candidate.md`), quoted verbatim in `work-packages/WP24-decisions.md` |
| **Acceptance record** | The supervisor's verbal acceptance, quoted verbatim in `work-packages/WP24-decisions.md`, after `work-packages/WP24-review.md` |

**Header note: one package, one stream, one push per surface.** The rename is one decision applied to every surface,
so one stream owns it end to end (the supervisor's disposition in `WP10-decisions.md`: "one stream owns it and it lands
after the executing packages' units or rebased onto them, in one push per surface with the regenerations in the same
push"). Each push leaves `dev` green: the generated artefacts that carry the old word (the paper's committed tables, the
proof-map record, Appendix B, the figures, the case's sensitivity report) are regenerated in the same push as the code
or text that produces them, in the container of record `hts-paper` where the committed value was produced there. The
spike sized the whole at 6 to 8 units plus the container regeneration and image rebuild
(`docs/superpowers/notes/spike-facet-rename/report.md`, section 1). Step 3g of the path (`release-candidate.md`); it
depends on 3d (WP19) and 3f (WP23) and lands after their units or is rebased onto them. Drafted 2026-11-09 from the
inputs under Purpose and the repository at `dev` (`62a086a`).

## Purpose

The supervisor, 2026-11-09, 21:55, verbatim (`WP10-decisions.md`, "The word facet"): "on wording i want to propose we
drop the use of the term "facet" and stick to "monomial term", "n-lemma", and if obvious from context we can call it a
"trade-off". facet even without the color coding semantically brings to mind the wrong concept. our model uses monomial
terms kernels representing trade-offs, and our solver finds a quilt of of trade-offs that explain a design space where
all the metrics are strictly positive values with bigger is better." Asked how far the rename goes: "so i realize its a
big change but i think its causing more confusion than it is saving. can you do a spike to assess the effort to benefit
ratio". On the spike's evidence, options Keep facet, fix the phrases / Prose now, API after 0.1 / Everything before
0.1 / Prose now, API as its own package: **"Everything before 0.1"**.

The spike (`docs/superpowers/notes/spike-facet-rename/report.md`, d1efdfe): across 18 abstract-only reads no reader
took a facet for a set of designs; the 7 cluster readings came at depth B from the facet-coloured figures (since
redrawn, WP19) and two membership phrases; the A/B placed the tension in the model 4 of 4 under either vocabulary; the
executive reading version B said "nobody has told me what a monomial is". What the rename buys that the readers cannot
show: the glossary's one-object-one-name rule (`docs/superpowers/notes/vocabulary-review.md`, rule 1). Today the paper
says "A term, a monomial and a facet are one object", kept apart by "facet for the geometry and term for the algebra";
the code says `facet_share_` where the prose says "term share". After this package the model object has one name on
every surface a reader or a user meets, and the geometry follows the model rather than leading it.

The vocabulary (the supervisor's, with the driver's mapping he accepted): the model object is the **"monomial term"**,
shortened to **"term"** where the sentence leaves no doubt, glossed at first use in the abstract and in the docs as a
product of powers of the metrics; the metrics in tension within a term are its **"n-lemma"** (the contending set);
**"trade-off"** where the context makes it obvious; the designs a term scores highest on are its **"cell"** (A8, already
in the glossary). "Facet share" becomes "term share", "facet gap" "term gap", "several-facet fit" "several-term fit".

Inputs: `WP10-decisions.md` ("The word facet"; the driver's question and his answer; the disposition),
`release-candidate.md` (step 3g), the spike report with `count_facet.sh` and `passages/`, `interface-contract.md` and
`.toml` (version 10), `glossary.yaml`, `docs/superpowers/notes/vocabulary-review.md`, `reader-grid.md`,
`figure-review.md`, `PM-BRIEF.md` (the mechanical rule for `derivation/`; parallel streams and pushing; verification in
tiers), `WP23-scope-of-work.md` (the house style).

## Goals

- G1. **One name in the prose.** "Facet" leaves the glossary (`glossary.yaml`, the entries `facet` and `facet gap` and
  the cross-references in `cell`, `term`, `n-lemma`, `elasticity`, `stable radius`, `ternary plot`, `region`, GP/GGP),
  the paper (`paper/paper.ipynb`: prose, statements, captions, headings), the supporting material
  (`paper/supporting_material.ipynb` and its generators, table headers and section titles), the docs pages
  (`docs/*.md`, `docs/user-guide/*.md`, `site/index.html`, the compiled `docs/generated/glossary.md`) and the
  docstrings under `src/`, for the vocabulary above.
- G2. **One name in the derivations.** The step text of `derivation/` (axioms, L2, L4, L11 to L15; the module
  `lemma_12_facet_gap.py`), `proof_map_record.json` and `PROOF_MAP_FINDINGS.md` carry the vocabulary; Appendix B is
  regenerated in the container of record and its test passes in the same push (the mechanical rule, `PM-BRIEF.md`).
- G3. **One name in the figures.** Every label, legend, annotation and caption that says "facet" (`paper/figures/*.py`,
  `scripts/build_site_figures.py`, the `plotting` legends, the figure files `three-facets-*.png`) is renamed and every
  such figure regenerated.
- G4. **One name in the public names.** The package's public names move in the same spirit (the table under Agent's
  defaults): `facet_share_` to `term_share_`, `facet_gap` to `term_gap`, and `assign_facets`, `facet_labels`,
  `facet_step`, `single_facet_termination`, `facet_objective`, `by_facet`, the `color="facet"` option value, the
  fitted attribute `facet_`, the case module's `facet_record` and `facet_table`, the module `paper_facets.py`; with a
  non-additive interface-contract amendment (`contract_version` 10 to 11) and no deprecation shim.
- G5. **The pinned artefacts move with their sentences.** `claims_register.toml` fragments, the `tests/` phrase pins,
  `paper/environment_values.toml` (section `facet_numbered_tables`), `paper/length_ledger.toml`, the committed exact
  tables of the supporting material, the case's `sensitivity.json` keys: each changes in the push that changes its
  sentence or its producer, so no push leaves a pin or a fragment pointing at a sentence that no longer exists.
- G6. **The tool enforces the drop.** `scripts/check_vocabulary.py` reports no "facet" outside the τ = ∞ polyhedral
  sense and the records: the glossary's `avoid` gains the word and the stem list loses it, so a return of the word
  fails the check.
- G7. **Read as rendered.** One cold read at depth A and one at depth B after it (`reader-grid.md`), image and page as
  rendered from the staged build, findings verbatim in `WP24-review.md`.

## Non-goals

- No change of mathematics and no change of any statement: no definition, lemma, result, theorem, hypothesis, axiom or
  caption claim changes beyond the word and the clause the word's replacement needs; no number changes anywhere (the
  regenerations change text only).
- No change to the fit: nothing in the solvers' or the estimator's behaviour moves; every renamed function and attribute
  returns what it returned (model, fit and analysis kept apart, the fit untouched).
- No deprecation layer: no alias, no `DeprecationWarning`, no "one amendment cycle" for the old names (pre-0.1, nothing
  released; the contract's deprecation clause is not invoked).
- The records untouched: `work-packages/*.md` keep their wording as written (the only work-package files this package
  edits are its own `WP24-*` and the interface contract's pinned sections and manifest); the notes under
  `docs/superpowers/notes/` are records too and keep theirs *(default)*; the spike folder stays for WP25.
- No reopening of the vocabulary decision on a cold-read finding: a reader who stumbles on "term" or "cell" is a finding
  for the review and the supervisor's eye at acceptance, not a reason to bring "facet" back.
- No new figure, no new section, no change to what any figure shows; the membership sentences change wording only
  (cell wording, CR-3's open item is closed by G1).
- Not this package: the release steps (WP8b), the reader-grid rounds (WP11), the data swap (WP16), the model loop (WP23).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `glossary.yaml`: entries `facet` and `facet gap` removed, `term gap` present, cross-references rewritten, "facet" under an entry's `avoid` with its reason, the stem `facet` removed from `stems`; the polyhedral sense handled as Agent's default A1 says; `docs/generated/glossary.md` recompiled | G1, G6 |
| D-2 | `paper/paper.ipynb`: the ~71 sentences (spike section 1) rewritten or word-swapped, the geometry sentences and the membership sentences among them; the first use of "monomial term" in the abstract glossed as a product of powers of the metrics; the heading "B.2 The several-facet fit" and its kin renamed; the notebook re-executed in `hts-paper` | G1, G5 |
| D-3 | `paper/supporting_material.ipynb`, `paper/*.py` (`paper_facets.py` renamed and its imports), `paper/environment_values.toml`, `paper/length_ledger.toml`: headers, section titles, module and section names; the committed exact tables regenerated in `hts-paper`; `paper/container/RECORD.md` gains the regeneration entry | G1, G4, G5 |
| D-4 | `claims_register.toml`: every fragment whose sentence changed moved with it in the same push; no claim dropped; the anchors and backing references that name `lemma_12_facet_gap` follow the module rename | G5 |
| D-5 | `derivation/`: step text, docstrings and the module `lemma_12_facet_gap.py` renamed per the defaults table; `proof_map_record.json` regenerated (`uv run python -m derivation.proofmap --update` or the project's equivalent) with the moved steps listed in the review; `PROOF_MAP_FINDINGS.md` wording; Appendix B regenerated in the container; pushed only with the Appendix B test's output in the report | G2 |
| D-6 | `src/hyperbolic_trade_space/`: the renames of the defaults table in `estimator.py`, `solvers.py`, `plotting.py`, `tensions.py` (the report prefix), `datasets.py` (`info` key and error texts), `tuning.py`, `__init__.py` (`__all__`); docstrings and doctests in the vocabulary | G1, G4 |
| D-7 | The interface-contract amendment: `work-packages/interface-contract.md` sections 4 and 7 and the manifest `.toml` (`fitted_attributes`, `submodule_names`, the `facet_gap` signature entry, `facet_record` in `case.signatures`, `plotting` names), `contract_version = 11`, a change-log row that says the change is non-additive (a rename of pinned names with no deprecation) and cites the approval | G4 |
| D-8 | `tests/`: the phrase pins, the reference keys, the figure-name pins and the fixtures that carried the word, following the renames (never weakening a requirement); `scripts/check.py`'s path map if a file moves | G4, G5 |
| D-9 | `examples/adcs/`: `k_terms.py` (`facet_record`, the "facet rows/shares" headers), `case.py` (`facet_table`), `sensitivity.py` and the regenerated `sensitivity.json`, the case notebook's prose | G1, G4, G5 |
| D-10 | Figures: `paper/figures/{figure1,planes,nlemma,chart_level}.py`, `scripts/build_site_figures.py`, `plotting`'s legends; every affected figure regenerated by `scripts/build_figures.py` and `scripts/build_site_figures.py`; `docs/generated/figures/three-facets-*.png` renamed with their references | G3 |
| D-11 | Docs pages: `docs/api.md`, `docs/theory.md`, `docs/examples.md`, `docs/user-guide/{chart,fitting,tensions,limitations,termination}.md`, `site/index.html`, `README.md` if it carries the word; the first use of "monomial term" in the docs glossed; the API reference follows the docstrings | G1 |
| D-12 | `scripts/vocabulary_baseline.toml`: the six reason texts reworded (no checked phrase carries the word) | G6 |
| D-13 | `work-packages/WP24-review.md`: per surface the push hash, the checks run with their output lines (the Appendix B test, the contract test, the register test, the proof-map checker, the paper tests, the regeneration record), the list of τ = ∞ sentences where the textbook word stays (A1), every statement block touched with its before and after, the two cold reads verbatim with findings and dispositions | G2, G5, G6, G7 |
| D-14 | `work-packages/WP24-decisions.md`: the approval under the mandate and the acceptance, verbatim | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | The vocabulary tool passes with "facet" in an `avoid` list and out of `stems`, and reports no use of the word outside the τ = ∞ polyhedral sentences (A1) and the records it skips | `uv run python scripts/check_vocabulary.py` (exit 0); `uv run pytest tests/test_vocabulary.py tests/test_build_generated.py` |
| R-2 | A grep over the reader and user surfaces finds the word only in the τ = ∞ sentences listed in the review and in the records kept as written (the contract's existing change-log rows and the past entries of `paper/container/RECORD.md`, A4) | `grep -rni facet glossary.yaml paper src tests examples derivation docs/*.md docs/user-guide docs/generated site scripts claims_register.toml work-packages/interface-contract.md work-packages/interface-contract.toml README.md` compared line by line with the review's list, `paper/container/RECORD.md`'s past entries excluded |
| R-3 | The contract and the package agree: the manifest's pinned lists carry the new names and none of the old; `contract_version` is 11 and equals the last change-log row, which says the change is non-additive and cites the approval | `uv run pytest tests/test_interface_contract.py`; inspection of the row |
| R-4 | No deprecation shim: no old name survives as an alias, no `DeprecationWarning` is added, no `getattr` or property bridges an old name | `grep -rn "facet" src/` returns nothing; `git diff <start>...HEAD -- src/ \| grep -c "DeprecationWarning\|warnings.warn"` returns 0 new lines |
| R-5 | No number changes: every committed exact value, figure datum, certificate, count and termination record is identical before and after; the regenerated tables differ in text only | `uv run pytest tests/test_paper.py tests/test_k_terms_case.py tests/test_sensitivity.py tests/test_soft_fit.py`; `git diff --word-diff <start>...HEAD` over the regenerated tables, `sensitivity.json` and `environment_values.toml` inspected for numeric tokens (none moved); the ledger `PYTHONPATH=examples/adcs uv run python -m experiments verify` reports 0 drifts |
| R-6 | The fit is unchanged: the estimator's fitted attributes under their new names equal the old ones value for value on the datasets of record and the planted tables | the existing estimator, solver, soft-fit and sklearn-conformance tests pass unchanged in substance (`uv run pytest tests/test_estimator.py tests/test_solvers.py tests/test_soft_fit.py tests/test_sklearn_compat.py tests/test_matches_derivation.py`); the review states that no test changed other than by the renamed identifiers and phrases |
| R-7 | The derivation chain and the proof map hold: every lemma passes, the checker accepts the regenerated record, the moved steps are listed, and Appendix B equals the record | `uv run python derivation/run.py` ends "ALL LEMMAS PASS."; `uv run python -m derivation.proofmap`; `uv run pytest tests/test_proof_map.py tests/test_derivation.py`; `uv run pytest -q tests/test_paper.py -k appendix_b` in a clean worktree at the commit pushed, output in the report (the mechanical rule) |
| R-8 | The claims register is whole: every fragment matches its sentence verbatim; the number of claims is the same before and after; no claim is dropped for fragment mismatch | `uv run pytest tests/test_claims_register.py`; a count of `[[claim]]` rows before and after in the review |
| R-9 | The paper builds and its pins hold: the notebooks execute in `hts-paper`, the committed outputs equal the regenerated ones, the phrase pins hold, the length ledger is within its bounds | `uv run pytest tests/test_paper.py tests/test_notebook.py tests/test_paper_sources.py tests/test_paper_static_figures.py tests/test_narrative.py`; `paper/container/RECORD.md` names the image id and the head |
| R-10 | Every figure whose label, legend, annotation, caption or file name carried the word is regenerated from committed code and reads in the vocabulary; no figure's content changes | `uv run python scripts/build_figures.py` and `scripts/build_site_figures.py` reproduce the committed images; `uv run pytest tests/test_plotting.py tests/test_site.py tests/test_docs.py tests/test_paper_static_figures.py`; the review lists each figure with its changed strings |
| R-11 | "Monomial term" is glossed at its first use in the abstract and at its first use in the docs as a product of powers of the metrics; "n-lemma", "trade-off" and "cell" are used as the vocabulary above says and nowhere as synonyms of each other | the tool's first-use check over `paper.ipynb`; inspection of the abstract and of the docs' first use; `tests/test_paper.py`'s abstract pin follows the wording |
| R-12 | No statement changed beyond the word: every definition, lemma, result, theorem, axiom and caption claim touched is listed in the review with its before and after, and each differs only by the vocabulary and the clause its replacement needs | `WP24-review.md`, "Statements"; `git diff <start>...HEAD -- paper/paper.ipynb derivation/` read against the list |
| R-13 | The records are untouched: no file `work-packages/*.md` changes other than `WP24-scope-of-work.md`, `WP24-decisions.md`, `WP24-review.md` and `interface-contract.md`; nothing under `docs/superpowers/notes/` changes (A5) | `git diff --stat <start>...HEAD -- work-packages docs/superpowers/notes` |
| R-14 | Each push is one surface with its regenerations in it, lands after the executing packages' units or is rebased onto them, and leaves `dev` green at tier 2; no commit carries an attribution line | the push hashes in the review, each with the watcher's verdict; `git log --format=%B <start>..HEAD \| grep -ci "co-authored-by\|generated"` returns 0 |
| R-15 | Repository gates on this machine and on a Linux dispatch at the gate | `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; the driver's dispatch run green on the exact commit |
| R-16 | Two cold reads after the last push, from the staged build: one at depth A (title, abstract, Figure 1 and its caption as rendered), one at depth B (headers, main results, statement blocks, figures and captions as rendered), image before caption, each returning what a "monomial term" is and whether the contending metrics belong to a piece of the model or to a group of designs, with recall and friction; findings verbatim with dispositions | `WP24-review.md`, "Cold reads"; the two reader returns in full |

## Blast radius

The files this package may change; anything else is a stop and a question to the PM. One stream owns all of it; no
other stream writes any of these files while the package executes (the supervisor: "one stream owns it").

- Glossary and tool: `glossary.yaml`, `scripts/vocabulary_baseline.toml`, `docs/generated/glossary.md`
  (`scripts/check_vocabulary.py` only if the τ = ∞ handling of A1 needs it).
- Paper: `paper/paper.ipynb`, `paper/supporting_material.ipynb`, `paper/*.py` (including the rename of
  `paper_facets.py`), `paper/figures/*.py`, `paper/figures/*.png`, `paper/environment_values.toml`,
  `paper/length_ledger.toml`, `paper/environment_reference.npz` only if the regeneration rewrites it unchanged in value,
  `paper/container/RECORD.md`; `claims_register.toml` (fragments, anchors and references of the sentences changed).
- Derivations: `derivation/*.py` (the rename of `lemma_12_facet_gap.py` among them), `derivation/proof_map_record.json`,
  `derivation/PROOF_MAP_FINDINGS.md`; `build/generated/` outputs that Appendix B compiles from.
- Package: `src/hyperbolic_trade_space/*.py`.
- Contract: `work-packages/interface-contract.md` (sections 4 and 7, the change log's new row; the existing rows stay as
  written), `work-packages/interface-contract.toml`.
- Tests: `tests/*.py` (pins, keys, fixtures, figure names), `tests/data/` only if a stored key carries the word,
  `scripts/check.py` (the path map, if a file moves).
- Case: `examples/adcs/k_terms.py`, `case.py`, `sensitivity.py`, `sensitivity.json`, the case notebook's prose and the
  experiments' report text that carries the word (no dataset, no ledger value).
- Figures and docs: `scripts/build_figures.py`, `scripts/build_site_figures.py`, `docs/generated/figures/*` (the
  `three-facets-*` files renamed), `docs/*.md`, `docs/user-guide/*.md`, `site/index.html`, `README.md`, `mkdocs.yml`
  only if a renamed figure path is referenced there.
- Records of this package: `work-packages/WP24-scope-of-work.md`, `WP24-decisions.md`, `WP24-review.md`.
- Never: `pyproject.toml`, `uv.lock`, `.python-version`, `examples/adcs/data/*`, `examples/adcs/experiments/ledger/*`,
  any other `work-packages/*.md`, anything under `docs/superpowers/notes/`, `examples/adcs/model_v2/*`, the CI workflow.

## Definition of good

- A 0.1 in which the model object has one name wherever a reader or a user meets it, "monomial term" or "term", with
  "n-lemma" for the metrics in tension within a term, "trade-off" where the context makes it obvious and "cell" for
  the designs a term scores highest; nobody translates between the paper, the docs, the API and the figures; the
  fitted surface reads, where its geometry is the point, as the supervisor put it: a quilt of trade-offs, each monomial
  term one patch; and nothing but words has moved, which the record shows.

## Definition of good enough

- The vocabulary tool, with "facet" in `avoid` and out of `stems`, finds no "facet" outside the τ = ∞ polyhedral sense
  (A1) and the records (R-1); the grep over surfaces agrees with the review's list (R-2).
- The public names are renamed per the defaults table, the contract is at version 11 with its non-additive row and its
  test passes, and no shim exists (R-3, R-4).
- No number moved and the fit is unchanged (R-5, R-6); every statement touched is listed with its before and after and
  differs only by the vocabulary (R-12).
- The derivation chain, the proof map and Appendix B hold, the Appendix B test's output is in the report for the
  derivation push (R-7); the register is whole (R-8); the paper builds in `hts-paper` and its pins hold (R-9); every
  affected figure is regenerated and reads in the vocabulary (R-10); "monomial term" is glossed at first use in the
  abstract and the docs (R-11).
- The records are untouched (R-13); every push is one surface with its regenerations, landed after or rebased onto the
  executing packages' units, `dev` green at tier 2 for each head (R-14).
- The suite is green on both platforms, the Linux dispatch the driver's (R-15).
- One cold read at depth A and one at depth B after the last push, image and page as rendered, recorded verbatim with
  dispositions; a finding that blocks (a reader taking a term for a group of designs, or unable to say what a term is
  from the gloss) is fixed and the depth re-read once; a finding that does not block is listed for the supervisor's
  eye (R-16). Stop there and present.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance record above.

## Agent's defaults

Approved or changed as one item at the scope gate. Each is marked *(default)* where it appears.

- **A1. The τ = ∞ polyhedral sense keeps the textbook word.** In the three or four sentences where a polyhedron is meant
  (R1's "relative interior of a facet of the supporting envelope with positive normal", L11's "the facet that blocks
  u′", L4's mention, the glossary's `not` on the Pareto boundary and the data's convex hull), "facet" stays as the
  standard word for a maximal face, listed in the glossary's `assumed` terms with its reason (Boyd and Vandenberghe
  level), and each such sentence carries the tool's `vocab-exempt` marker or whatever the `assumed` list already
  grants, so the check passes with the word present only there; the review lists the sentences. The alternative is
  "face of the supporting envelope", which would need "(d − 1)-dimensional face" to say what R1 says today, since a
  face of lower dimension has a cone of normals and the statement would weaken; the default keeps the statement
  exactly *(default)*.
- **A2. The new names.** The table; the rule behind it is the spike's semantics table (section 3): a thing of the model
  takes "term", a thing of the assignment takes "cell", a thing named for what it does takes that name.

  | Old | New | Where |
  |---|---|---|
  | `facet_share_` | `term_share_` | `estimator` fitted attribute (the supervisor's) |
  | `facet_gap` | `term_gap` | `solvers` certificate function (the supervisor's) |
  | `facet_objective` | `term_objective` | `solvers` |
  | `single_facet_termination` | `single_term_termination` | `solvers` |
  | `facet_step` | `refit_step` (values `"support"`, `"tangent"` unchanged) | estimator parameter and `solvers` keyword; it selects the refit step, so it is named for what it does (alternative: `term_step`) |
  | `facet_` | `cell_` | `estimator` fitted attribute: the cell of each training row |
  | `assign_facets` | `assign_cells` | `estimator` method: the cell of each design |
  | `facet_labels` | `cell_labels` (`"cell 1" .. "cell K"`) | `plotting` |
  | `color="facet"` | `color="cell"` | `plotting` option value (the spike: colours by assignment, so "cell" is the honest name) |
  | `by_facet` | `by_cell` | `plotting` internal |
  | `info["facet"]` | `info["term"]` | `datasets`: the planted term of each row (a thing of the model, not an assignment) |
  | report prefix `"facet k: "` | `"term k: "` | `tensions` |
  | `facet_record` | `term_record` | `k_terms` (pinned, `case.signatures`) |
  | `facet_table` | `term_table` | `case.py` |
  | `paper_facets.py` | `paper_terms.py` | paper generator module |
  | `lemma_12_facet_gap.py` | `lemma_12_term_gap.py` | `derivation/` (cited by the paper, the register and `generate_proofs.py`) |
  | `facet_numbered_tables` | `term_numbered_tables` | `paper/environment_values.toml` section |
  | `three-facets-{light,dark}.png` | `three-terms-{light,dark}.png` | `docs/generated/figures/`, `tests/test_site.py` |
  | sensitivity keys `... facet 1 ...` | `... term 1 ...` | `examples/adcs/sensitivity.json`, `tests/test_sensitivity.py` |

  Legends and markers number terms (`term 1`, `term 2`), and designs coloured by assignment take the cell labels
  *(default)*.
- **A3. The order of the pushes.** (1) `src` with the contract amendment, the tests, the case code, the paper and figure
  generators' code references, and the regenerated figures and generated values (a container run for the committed
  exact values); (2) `derivation/` with the proof-map record and Appendix B regenerated in the container, pushed only
  with the Appendix B test's output; (3) the paper notebooks' prose and headings, the register fragments, the paper pins,
  the supporting material regenerated in the container; (4) the docs pages, `site/index.html`, the compiled glossary and,
  last in the same push, the glossary entries and the `avoid` and `stems` edits that turn the tool's check on (the
  `facet` entry would be a dead entry before the docs drop the word, so the glossary lands with the last prose surface);
  then the two cold reads. Between pushes a prose surface may say "term" beside a code name not yet moved only in the
  direction code-first, which the order avoids *(default)*.
- **A4. The contract's change-log rows 3, 7 and 8 and the past entries of `paper/container/RECORD.md` keep their wording** as records of past amendments and runs (the new regeneration entry is written in the vocabulary); the pinned
  sections and the manifest change; the new row 11 names every renamed pinned item *(default)*.
- **A5. `docs/superpowers/notes/` are records** (spike reports, reviews, process notes) and keep their wording, as the
  spike counted them with `work-packages`; the spike folder is WP25's to delete once its result is recorded here
  *(default)*.
- **A6. "Quilt" once.** The supervisor's "quilt of trade-offs" replaces the Preliminaries' "A term, a monomial and a
  facet are one object" sentence: the fitted surface is a quilt of trade-offs, each monomial term one patch, flat in
  log space, meeting its neighbours at the ridges; the docsite index may carry the same sentence; "quilt" and "patch"
  enter no glossary entry, caption or statement and "patch" is not a noun for the term *(default)*.
- **A7. The gloss.** "a monomial term (a product of powers of the metrics)" at the first use in the abstract and at the
  first use on the docs' home or getting-started page, in those words or the glossary's `formal` field for `term`
  *(default)*.
- **A8. The cold readers.** Two fresh contexts, one per depth, given only the rendered slice from the staged build (image
  before caption), the grid's return format (recall and friction), and the spike's two questions; neither sees this
  scope, the spike or the other's return *(default)*.
- **A9. Tests change only by identifier and phrase**; a fixture that used the word as a made-up term (`test_vocabulary.py`)
  takes another made-up word; no assertion weakens *(default)*.
- **A10. The derivation module rename** is a `git mv` with the record regenerated; the checker's listing of moved steps
  goes into the review as the evidence that only text moved *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (decided by the supervisor before this draft: the drop, its
reach "Everything before 0.1", the vocabulary; decided here as Agent's defaults: one item, A1 to A10, for the driver
under the mandate; deferred 0; raised 0).
