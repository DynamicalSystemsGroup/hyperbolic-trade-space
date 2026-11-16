# WP57e — Scope of work: re-lettering the appendices in the order of first mention

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy; runs after WP57d lands, one unit, one writer across the paper, the supporting material and every file that names an appendix |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `wp57e` in its own worktree off `dev` at WP57d's landing (c8f8407b or later) |
| **Approval record** | The driver's approval under his mandate, quoted in `WP57-decisions.md` |
| **Acceptance record** | The driver's soft-confirm on the unit's captures of the rendered pages; his read afterwards |

## Purpose

His rule, as the driver recorded it (`WP57-decisions.md`, the map's call 4): the appendices are re-lettered "by first
mention of any subsection in reading order, computed by WP57e on the text as it then stands (after WP56 and WP57a to
d), since those packages move citing sentences; his rule is the order of first mention." The parent's G4
(`WP57-scope-of-work.md`): "Re-lettering once, last: the appendices in the order of their first mention in the paper,
every reference, anchor, proof-map section and register row following." The inventory of what follows a change of
letter is the map's section 4 (`WP57-rounds/map.md`). On the paper at c8f8407b, `map_counts.py` gives the order G, D,
H, A, B, C, E, F (Section 2 names Appendix G beside Table 1, then D.16 and H in the HoroPCA paragraph; Section 3 names A
and B; Section 5 names C.4; Section 6 names E; Section 11 names F.3), so every letter changes.

## Goals

- G1. **The letters.** The unit recomputes the order of first mention on the paper as it stands at its start
  (`uv run python work-packages/WP57-rounds/map_counts.py`, "first mention"; the rule: the first mention of the
  appendix or of any of its subsections, in the paper's cell order, front matter to works cited) and records it in the
  review with each first-mention sentence. The appendices take the letters A to H in that order, and the supporting
  material's cells are reordered so the appendices appear in letter order.
- G2. **The subsections.** Within each appendix the subsections are renumbered consecutively from 1 in their current
  order (D.3 to D.19 become .1 to .14 of their new letter; E.1 to E.3, F.1 to F.4, B.1 to B.3, C.1 to C.8, H.1 to H.4
  keep their numbers under the new letter). Headings, `(appendix-x)=` and `(sub-x-n)=` anchors, cell ids (`app-X`,
  `app-X-n`, `tab-X-*`, `sent-X-*`) and table labels follow the new letter and number; one object, one name, so no old
  anchor is kept as an alias.
- G3. **Everything that names a letter follows**, by the map's inventory: the paper's `{ref}` and `{numref}` roles and
  "Appendix X" text (the only main-text edit); the generators' `appendix_link` constants, captions, docstrings and
  comments; `generate_proofs.PARTS`; the register's `anchor` fields (ids unchanged, append-only); `paper/length_ledger.toml`
  ceiling keys (the dated rows stay as written); `scripts/residuals_baseline.json` and `scripts/vocabulary_baseline.toml`
  surface keys (regenerated with the checkers' `--write-baseline`, every count equal to before under the renamed key);
  `scripts/check_vocabulary.py` and `scripts/prose_surfaces.py` patterns; the tests' literals; `docs/`, `examples/adcs/`,
  `glossary.yaml` `defined_in` fields, `paper/prior_art.yaml`, `paper/reading_pass.yaml`, `paper/supplement/*.md`,
  `paper/myst.yml`, `paper/paper_common.py`, `paper/regenerate_row.py`, `paper/container/build-paper.sh`, the root and
  docs pages, the reviewer's guide if it names a letter. Dated records stay as written: `paper/container/RECORD.md`,
  `derivation/PROOF_MAP_FINDINGS.md`, `work-packages/*`, `docs/superpowers/notes/*`, `notes/directions/*` readouts and any
  note that reports a state at a date; a note that states the current structure follows. The review lists every file
  touched and every dated file left, with its reason.
- G4. **The numbering test restored.** `tests/test_paper.py` asserts, for every appendix, consecutive subsection numbers
  from 1 under its letter and the appendices' headings A to H in order (WP57c relaxed the D test to order only); the
  tests that name cell ids, anchors and labels follow G2.
- G5. **Nothing else changes.** No sentence is reworded beyond its letter and number; no cell is cut or added; the
  derivation chain and proof map are unchanged (22 lemma files, 549 tagged steps); the paper's figures, tables and
  generated numbers are unchanged; `paper/stability_extra.json` and the data of record are unchanged.

## Non-goals

- Any rewording, cut or addition to the paper or the supporting material beyond letters and numbers; any judgement on
  content (WP57-review, the parent's D-3, reads the whole supporting material after this package).
- Alias anchors or redirects for the old names (the site is not yet published).
- Any edit to `derivation/`, `examples/adcs/data/`, `examples/adcs/model_v2/`, or to dated records.
- WP58's sweep (the reviewer's guide's G.2 item, the stale `myst.yml` comment "(Appendices A to G)" is fixed here only if
  it names a letter range; the dead glossary entry; the CHANGELOG).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/paper.ipynb`, `paper/supporting_material.ipynb` re-lettered, reordered and re-executed (`paper/execute_notebooks.py`) | G1, G2, G3 |
| D-2 | Every file of G3 updated; `claims_register.toml` anchors; ledger keys; baselines regenerated | G3 |
| D-3 | `tests/test_paper.py` and the other tests following; the numbering test restored | G4 |
| D-4 | `work-packages/WP57e-review.md`: the computed order with its first-mention sentences, the letter map old to new, the subsection map, the file list (touched; dated and left), the checks with exit codes; captures in `work-packages/WP57-rounds/e/` with a cold read | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | The letters are the order of first mention on the paper as it stands | `map_counts.py` output in the review; `test_appendix_headings_a_to_h_in_order` (or its successor) |
| R-2 | Every cross-reference resolves to the object it resolved to before | `cd paper && BASE_URL=/paper uv run --frozen myst build --html` with a clean log; the `references_resolve` test; a table in the review pairing each paper pointer's old and new target heading |
| R-3 | No old-sense anchor or letter survives | a grep over the tree (excluding `.git`, `_build`, `.venv`, `site`, `_stage`, the dated records) for every `appendix-x`, `sub-x-n`, `app-X`, `tab-X-`, `sent-X-` and "Appendix X" occurrence, each classified in the review as new-sense or dated |
| R-4 | Nothing but letters and numbers changed | `git diff dev --stat`; a word-level diff of the paper's and the supporting material's markdown showing only letter and number tokens changed (script in `WP57-rounds/e/`); proof map 22 files, 549 steps; `git diff dev -- derivation examples/adcs/data examples/adcs/model_v2` empty; every residual and vocabulary count equal to before under its renamed key |
| R-5 | The suites, lint, format, lock, vocabulary, supplement check, mkdocs pass; residuals at or below dev on every surface | `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `uv run python -m derivation.proofmap`, `uv run python scripts/check_vocabulary.py`, `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` (exits 1 on dev; no new rise), `uv run python paper/generate_supplement.py --check`, `uv run pytest -q tests/test_claims_register.py`, `MPLCONFIGDIR=<warm cache> uv run pytest -q -m "not slow" -n auto`, `MPLCONFIGDIR=<warm cache> uv run pytest -q -m slow -n auto tests/test_paper.py tests/test_case.py::test_docstrings_run_and_are_numpydoc`, `uv run mkdocs build -q`; every exit code captured to a file |
| R-6 | No AI attribution on the commit | `git log --format=%B` |

## Definition of good

The appendices read in the order the paper calls on them, each name used once and everywhere the same, and nothing
else about the paper or the supporting material has moved.

## Definition of good enough

R-1 to R-6 met; the captures show the supporting page's navigation A to H in the new order, each appendix opening
under its new letter, and two main-text pointers (Section 2's to the PCA chaining subsection and Section 6's to the
assumptions section) landing on their targets; the review's file list complete.

## Definition of done

Good enough met, no open item, the driver's soft-confirm on the captures recorded in `WP57-decisions.md`, landed on
`dev` with CI on both platforms; his read afterwards.

## Agent's defaults

- One commit, or two if the unit prefers the notebooks and the rest apart; each passing the suite.
- Cell ids keep their shape (`app-X`, `app-X-n`, `tab-X-*`, `sent-X-*`); the irregular ids of C (`app-C-5-metrics` for
  C.5, `app-C-5` for C.6, `app-C-6` for C.7) and D (`app-D-sens`, `app-D-own`, ...) are normalized to the new letter and
  number where a number is the id's suffix, and otherwise keep their word suffix under the new letter.
- `generate_repro.READS_BY_CALL` and F.4's one-row-per-table listing follow by regeneration.
- The `appendix_link` constant names in `generate_findings.py` are renamed to the new letters (`_B14` for the old
  `_D16`, and so on) so the name and the target agree.
- Register ids, if any row must be added, from C1051.
- Captures at 1,280 px: the supporting page's "In this article" navigation, each of the eight appendix openings, the
  two pointers of good enough, taken from a served `myst build`; the server stopped after.

## Open decisions

None. The rule and its computation are his call 4 as recorded; the result on the paper as it stands (G, D, H, A, B, C,
E, F) is reported to him for his read, where he may revise the rule; the package is rerunnable.
