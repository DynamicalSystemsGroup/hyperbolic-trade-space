# WP57e review: the appendices re-lettered in the order of first mention

Branch `wp57e` (worktree off `dev` at 6d86038d), one commit. The re-lettering is computed and applied by
`work-packages/WP57-rounds/e/reletter.py` in one regular-expression pass per file (no replacement is read again, so D to
B and B to E never chain); the package is rerunnable from its base. Every other script named here is in the same
directory with its output beside it. Captures and the unit's cold read: `WP57-rounds/e/*.png`, `WP57-rounds/e/cold-read.md`.

## The order (G1, R-1)

`uv run python work-packages/WP57-rounds/map_counts.py --paper paper/paper.ipynb --supp paper/supporting_material.ipynb`
on the paper at the base (`WP57-rounds/e/counts-before.txt`) gives, as (letter, paper cell, offset): G (7, 1336), D (13,
943), H (13, 1291), A (14, 218), B (16, 2428), C (20, 2290), E (54, 0), F (105, 256). The first-mention sentences, at
the base (`WP57-rounds/e/first-mention.txt`, which also shows the same positions after, reading A to H):

| New | Old | Section | First-mention sentence (at the base) |
|---|---|---|---|
| A | G | 2, Prior art | The table summarizes the register of prior art in {ref}`Appendix G <appendix-g>`. |
| B | D | 2, Prior art | We borrow that setting and the estimator interface of scikit-learn, and use PCA as a downstream step ({ref}`Appendix D.16 <sub-d-16>`). |
| C | H | 2, Prior art | In a prospectively specified test, ..., recovered the planted trade-offs only where they were the direction of largest spread; the tables are clean, so it demonstrates a mechanism and does not measure how often recovery succeeds ({ref}`Appendix H <appendix-h>`). |
| D | A | 3, Preliminaries and notation | Mathematical notation follows Boyd and Vandenberghe ... ; {ref}`Appendix A <appendix-a>` is the full register of symbols and terms. |
| E | B | 3, Preliminaries and notation | Under the log change of variables ... convex in $w$ ({ref}`Appendix B, L4 <appendix-b>`). |
| F | C | 5, Methods | The case's conditioning rule is {ref}`Appendix C.4 <sub-c-4>`'s. |
| G | E | 6, Results | {ref}`Appendix E <appendix-e>` records what the results leave open. |
| H | F | 8, Case analysis (its closing paragraph) | {ref}`Appendix F.3 <sub-f-3>` gives the commands; outside the environment of record values differ in the last digits ({ref}`Appendix F.2 <sub-f-2>`). |

The order is the one the scope recorded (G, D, H, A, B, C, E, F). One detail differs from the scope's purpose line: F's
first mention is Section 8's closing paragraph (cell 105, `sec-case-analysis-close`), not Section 11; the order is the
same. `test_the_letters_are_the_order_of_first_mention_in_the_paper` (new) recomputes it on every run.

## The letter map and the subsection map (G1, G2)

Letters: G to A, D to B, H to C, A to D, B to E, C to F, E to G, F to H. Subsections, consecutive from 1 in their
current order (`reletter.py --map` prints the maps and the cell ids):

| Old | New | Old | New |
|---|---|---|---|
| G.1 | A.1 | A (no subsection) | D |
| D.3, D.4, D.5 | B.1, B.2, B.3 | B.1 to B.3 | E.1 to E.3 |
| D.8, D.9, D.10, D.11 | B.4, B.5, B.6, B.7 | C.1 to C.8 | F.1 to F.8 |
| D.13, D.14, D.15, D.16 | B.8, B.9, B.10, B.11 | E.1 to E.3 | G.1 to G.3 |
| D.17, D.18, D.19 | B.12, B.13, B.14 | F.1 to F.4 | H.1 to H.4 |
| H.1 to H.4 | C.1 to C.4 | | |

Anchors follow (`(appendix-x)=`, `(sub-x-n)=`), no alias kept. Cell ids follow by the scope's default, computed from the
notebook's structure at the base: a numbered `app-` id takes the new number of the subsection it sits in (`app-C-5-metrics`
to `app-F-5-metrics`, C's `app-C-5` (C.6) to `app-F-6`, `app-C-6` (C.7) to `app-F-7`; D's `app-D-3` (D.3) to `app-B-1`,
`app-D-5` (D.8) to `app-B-4`, `app-D-5-margin` to `app-B-4-margin`, `app-D-6` (D.9) to `app-B-5`, `app-D-7` (D.10) to
`app-B-6`; `app-H-4b` to `app-C-4b`); worded ids keep their word under the new letter (`app-D-sens` to `app-B-sens`,
`app-B-job` to `app-E-job`); `tab-X-*` and `sent-X-*` change letter only; the table labels `tab-e-*-1` to `tab-g-*-1`,
`tab-h-hypothesis-1` to `tab-c-hypothesis-1`. The supporting notebook's cells are reordered so the appendices appear A to
H, each appendix's cells a block in their own order; 112 cells before and after.

## Files

Touched (43 tracked files, plus the package's own directory `work-packages/WP57-rounds/e/` and this review):

- The notebooks: `paper/paper.ipynb` (the only main-text edit: 74 `{ref}` roles and their "Appendix X" text in 45
  markdown cells), `paper/supporting_material.ipynb` (headings, anchors, cross-references, cell ids, labels, cell order;
  re-executed).
- Generators and paper code: `paper/generate_findings.py` (the eleven `appendix_link` constants renamed `_B1`, `_B3`,
  `_B4`, `_B5`, `_B7`, `_B9`, `_F5`, `_G`, `_B10`, `_B12`, `_B14`, so each name is its target; docstrings),
  `generate_gaps.py`, `generate_model.py`, `generate_prior_art.py`, `generate_proofs.py` (its docstring; `PARTS` names no
  letter, so nothing else), `generate_reading_pass.py`, `generate_register.py` (the `^## Appendix D\.` filter of the
  notation table), `generate_repro.py`, `generate_results.py` (two table captions, "the generator of Appendix F"),
  `generate_supplement.py`, `paper_common.py`, `regenerate_row.py`, `figures/chart_level.py` (comments only),
  `style.css` (a comment), `myst.yml` (two comments; "(Appendices A to G)" is now "(Appendices A to H)"),
  `container/build-paper.sh`, `environment_values.toml` (comments; the phrase "with D.2's and D.12's tables since WP57c",
  naming subsections that no longer exist, reads "with the tables merged into it at WP57c"), `prior_art.yaml` (16
  comments, two text fields that print: "Appendix C", "Appendix D"), `reading_pass.yaml` (two letters in one `now`
  field), `paper/supplement/metric-associations.md` (by its generator; `generate_supplement.py --check` passes).
- Records that list the current structure: `claims_register.toml` (96 `anchor` fields and two `fragment` fields, ids
  unchanged, nothing appended); `paper/length_ledger.toml` (the `[baseline.sections]` keys and their comments, and each
  row's `section` field, which is the key a row adds to; every row's text, date and authority as written; see
  Amendments); `scripts/residuals_baseline.json` (surface keys; see the checks).
- Checkers: `scripts/check_vocabulary.py`, `scripts/prose_surfaces.py` (the notation table's special case reads
  "Appendix D"; the surface-id pattern `^(Appendix [A-G]|[A-G]\.\d+|L\d+)` widened to `[A-H]`, so H's subsections get
  `h-n` ids as F's had `f-n`, and the HoroPCA appendix, whose letter the old pattern missed, gets `appendix-c` in place of
  a slug of its title), `scripts/check_residuals.py` (the link cue that counts a link to the notation table as a
  definition: `appendix-a`/`sub-a-` to `appendix-d`/`sub-d-`).
- Tests: `tests/test_paper.py` (literals; `APPENDICES` in the new order; the numbering test restored, see below),
  `tests/test_site.py`, `tests/test_vocabulary.py` (the fixture heading "## Appendix D. Notation and terms").
- Docs and the case: `docs/bridge.md`, `docs/user-guide/limitations.md`, `docs/user-guide/temperature.md`,
  `examples/adcs/case-model.md`, `examples/adcs/case.py`, `examples/adcs/experiments/sensitivity.py`,
  `examples/adcs/noise_injection.py`, `glossary.yaml` (two `defined_in` fields, B.12 and B.6).
- Notes that state the current structure: `notes/reader-grid.md` (the levels' pointers to H, F, E),
  `notes/verification-strategy.md` ("the Appendix E test"), `notes/vocabulary-review.md` ("(Appendix A, Further
  reading)"), and `docs/superpowers/notes/abstraction-gaps.md`, the gaps ledger, which G.2's Table prints row by row: its
  six pointers (Appendix B (proofs), D.11, D.13, D.14 twice, D and D.18) now read E, B.7, B.8, B.9, B and B.13. It sits
  in a folder the scope lists as dated; it is the source of a table on the page, so it follows (without it the page
  printed "Appendix D.11" for B.7).

Dated and left as written:

| File | Why |
|---|---|
| `paper/container/RECORD.md` | the container's dated runs (scope) |
| `derivation/PROOF_MAP_FINDINGS.md` | dated findings; `derivation/` untouched (non-goal) |
| `work-packages/*` | decisions, reviews, rounds, the queue, the spike's draft, the reviewer's guide's items (WP58) |
| `docs/superpowers/notes/*` but the gaps ledger | design notes at their dates (`notation.md` "Appendix A", `paper-sources/*`, the spike's `tables.npz`) |
| `notes/directions/wp35-*`, `wp41-*`, `wp50-*` | readouts (scope) |
| `notes/user-journeys.md` | a WP33 note built from dated returns |
| `notes/references-verified.md`, `notes/paper-prior-art-sources.md` | verification logs with dated entries |
| `examples/adcs/experiments/reports/change-register.md` | a dated report |
| `scripts/vocabulary_baseline.toml` | three `reason` strings dated "WP10 re-triage 2026-11-09"; the file has no surface key, and `check_vocabulary.py` has no `--write-baseline`; nothing to regenerate |
| `paper/length_ledger.toml` row text | dated rows (scope): their `job`, `reader`, `no_longer_did`, `authority` and comments keep the letters of their date |
| `claims_register.toml` `source` and `note` fields | provenance of each row at its date |
| `tests/test_paper.py` function names (`test_appendix_h_*`, `test_d16_*`, ...) and `tests/test_site.py`'s comment "(+24, D.12 moved in)" | the names are cited by 56 register backings (`test:tests/test_paper.py::...`), by `scripts/check.py` (`-k appendix_b`, mapped for `derivation/`) and by dated records; renaming them is not a letter in the paper, and is left to the driver. History comments in tests that name a cut subsection now say "the old D.7" |

## R-2: every pointer of the paper and its target

`WP57-rounds/e/pointers.py` (output `pointers.txt`): the paper's 74 roles and the generator's 11 links, 85 pointers to 30
targets, each label resolved to its heading in the supporting material of the same commit; 0 differ beyond letter and
number. The MyST build's log is clean. Grouped by target:

| Before: label, heading | After: label, heading | Pointers (cell: text before -> after) |
|---|---|---|
| `appendix-g` Appendix G. Register of prior art | `appendix-a` Appendix A. Register of prior art | bibliography, sec-prior-art: Appendix G -> Appendix A (x2) |
| `sub-d-16` D.16 Chaining with PCA: the principal directions of the near-frontier chart | `sub-b-11` B.11 Chaining with PCA: the principal directions of the near-frontier chart | fig-chart-level-caption, sec-prior-art-3: Appendix D.16 -> Appendix B.11 (x2) |
| `appendix-h` Appendix H. HoroPCA beside this work: a tested hypothesis | `appendix-c` Appendix C. HoroPCA beside this work: a tested hypothesis | sec-prior-art-3: Appendix H -> Appendix C |
| `appendix-a` Appendix A. Notation and terms | `appendix-d` Appendix D. Notation and terms | sec-preliminaries: Appendix A -> Appendix D |
| `appendix-b` Appendix B. Proofs, step for step with their scripts | `appendix-e` Appendix E. Proofs, step for step with their scripts | 977883ab, noise-asm, res-L1, res-L10, res-L11, res-L12, res-L13, res-L14a, res-L14b, res-L15, res-L17, res-L2, res-L20, res-L21, res-L3, res-L4, res-L5, res-L6, res-L7, res-L8, res-L9, sec-definitions, sec-methods, sec-methods-several, sec-preliminaries-b, sec-results: Appendix B, L4 -> Appendix E, L4 (x4); Appendix B, L10 -> Appendix E, L10 (x4); Appendix B, L5 -> Appendix E, L5 (x2); Appendix B, L16 -> Appendix E, L16 (x5); Appendix B, L5.25 -> Appendix E, L5.25; Appendix B, L9 -> Appendix E, L9 (x3); Appendix B -> Appendix E (x2); Appendix B, L1 -> Appendix E, L1; Appendix B, L2 -> Appendix E, L2; Appendix B, L3.9 -> Appendix E, L3.9; Appendix B, L3 -> Appendix E, L3; Appendix B, L6 -> Appendix E, L6; Appendix B, L18 -> Appendix E, L18; Appendix B, L19 -> Appendix E, L19; Appendix B, L20 -> Appendix E, L20; Appendix B, L7 -> Appendix E, L7; Appendix B, L21 -> Appendix E, L21; Appendix B, L8 -> Appendix E, L8; Appendix B, L11 -> Appendix E, L11; Appendix B, L17 -> Appendix E, L17 (x2); Appendix B, L15 -> Appendix E, L15; Appendix B, L12 -> Appendix E, L12; Appendix B, L13 -> Appendix E, L13; Appendix B, L14 -> Appendix E, L14 (x2); Appendix B, L17.19 -> Appendix E, L17.19; Appendix B, L17.13 -> Appendix E, L17.13 |
| `sub-d-5` D.5 Sensitivity variants | `sub-b-3` B.3 Sensitivity variants | generated `_D5` -> `_B3`, sec-methods: Appendix D.5 -> Appendix B.3 (x2) |
| `sub-c-4` C.4 Conditioning | `sub-f-4` F.4 Conditioning | sec-methods: Appendix C.4 -> Appendix F.4 |
| `sub-d-11` D.11 Stability of the conclusions under rounding-level jitter | `sub-b-7` B.7 Stability of the conclusions under rounding-level jitter | generated `_D11` -> `_B7`, sec-case-analysis-1, sec-methods-thresholds: Appendix D.11 -> Appendix B.7 (x2); D.11 -> B.7 |
| `sub-b-2` B.2 The several-term fit, its levels of guarantee and the tension (L12 to L22) | `sub-e-2` E.2 The several-term fit, its levels of guarantee and the tension (L12 to L22) | sec-methods-several, sec-results-stopping: Appendix B.2 -> Appendix E.2 (x2) |
| `sub-d-13` D.13 The refit on a term's own rows | `sub-b-8` B.8 The refit on a term's own rows | sec-methods-several: Appendix D.13 -> Appendix B.8 |
| `sub-d-18` D.18 The noise-ridge corollary against injected noise | `sub-b-13` B.13 The noise-ridge corollary against injected noise | res-L20: Appendix D.18 -> Appendix B.13 |
| `sub-d-14` D.14 Does the fit recover a planted answer: twenty tables | `sub-b-9` B.9 Does the fit recover a planted answer: twenty tables | generated `_D14` -> `_B9`, res-L15: Appendix D.14 -> Appendix B.9 (x2) |
| `sub-d-8` D.8 The solver's termination records | `sub-b-4` B.4 The solver's termination records | generated `_D8` -> `_B4`, res-L15, sec-case-analysis-2, sec-results-stopping: Appendix D.8 -> Appendix B.4 (x4) |
| `appendix-e` Appendix E. Assumptions, limitations and open questions | `appendix-g` Appendix G. Assumptions, limitations and open questions | generated `_E` -> `_G`, sec-discussion, sec-results-open: Appendix E -> Appendix G (x3) |
| `appendix-c` Appendix C. The case's model: how the table of metrics came to be | `appendix-f` Appendix F. The case's model: how the table of metrics came to be | sec-case-construction: Appendix C -> Appendix F |
| `sub-c-1` C.1 Configurations (the design variables and their ranges) | `sub-f-1` F.1 Configurations (the design variables and their ranges) | fig-assembly-caption: Appendix C.1 -> Appendix F.1 |
| `sub-c-6` C.6 The datasets | `sub-f-6` F.6 The datasets | sec-case-construction-1b: Appendix C.6 -> Appendix F.6 |
| `appendix-d` Appendix D. Extended results: what the method found in the table | `appendix-b` Appendix B. Extended results: what the method found in the table | sec-case-analysis-1: Appendix D -> Appendix B |
| `sub-c-7` C.7 The planted example | `sub-f-7` F.7 The planted example | sec-case-analysis-2: Appendix C.7 -> Appendix F.7 |
| `sub-d-15` D.15 Choosing K for the case | `sub-b-10` B.10 Choosing K for the case | fig-chart-level-caption, generated `_D15` -> `_B10`: Appendix D.15 -> Appendix B.10 (x2) |
| `sub-d-4` D.4 The regimes side by side | `sub-b-2` B.2 The regimes side by side | sec-case-analysis-3b: Appendix D.4 -> Appendix B.2 |
| `sub-d-10` D.10 Propose, predict, check | `sub-b-6` B.6 Propose, predict, check | sec-case-analysis-5: Appendix D.10 -> Appendix B.6 |
| `sub-d-19` D.19 The decision: the shortlist and the rules | `sub-b-14` B.14 The decision: the shortlist and the rules | generated `_D19` -> `_B14`, tab-decision-caption: Appendix D.19 -> Appendix B.14 (x2) |
| `sub-f-3` F.3 Commands | `sub-h-3` H.3 Commands | sec-case-analysis-close: Appendix F.3 -> Appendix H.3 |
| `sub-f-2` F.2 The environment of record | `sub-h-2` H.2 The environment of record | sec-case-analysis-close: Appendix F.2 -> Appendix H.2 |
| `appendix-f` Appendix F. Computational reproducibility | `appendix-h` Appendix H. Computational reproducibility | acknowledgments: Appendix F -> Appendix H |
| `sub-d-3` D.3 Exponents and terms | `sub-b-1` B.1 Exponents and terms | generated `_D3` -> `_B1`: Appendix D.3 -> Appendix B.1 |
| `sub-d-9` D.9 Comparison with nondominated sorting | `sub-b-5` B.5 Comparison with nondominated sorting | generated `_D9` -> `_B5`: Appendix D.9 -> Appendix B.5 |
| `sub-c-5` C.5 The table of metrics | `sub-f-5` F.5 The table of metrics | generated `_C5` -> `_F5`: Appendix C.5 -> Appendix F.5 |
| `sub-d-17` D.17 The requirements read after the fit | `sub-b-12` B.12 The requirements read after the fit | generated `_D17` -> `_B12`: Appendix D.17 -> Appendix B.12 |

85 pointers to 30 targets, 0 differ

## R-3: what survives

`WP57-rounds/e/r3_grep.py` greps the tracked tree for `appendix-x`, `sub-x-n`, `app-X`, `tab-X-`, `sent-X-`, "Appendix X"
and "X.n" and classes each occurrence: dated (a dated file; a ledger row's text; a register row's `source` and `note`; a
test comment marked "the old") or new. Output:

| File | new | dated | dated kind |
|---|---|---|---|
| `claims_register.toml` | 100 | 155 | dated (row text) |
| `docs/bridge.md` | 2 | 0 |  |
| `docs/superpowers/notes/abstraction-gaps.md` | 8 | 0 |  |
| `docs/user-guide/limitations.md` | 2 | 0 |  |
| `docs/user-guide/temperature.md` | 4 | 0 |  |
| `examples/adcs/case-model.md` | 2 | 0 |  |
| `examples/adcs/case.py` | 1 | 0 |  |
| `examples/adcs/experiments/sensitivity.py` | 3 | 0 |  |
| `examples/adcs/noise_injection.py` | 1 | 0 |  |
| `glossary.yaml` | 2 | 0 |  |
| `notes/reader-grid.md` | 4 | 0 |  |
| `notes/verification-strategy.md` | 2 | 0 |  |
| `notes/vocabulary-review.md` | 1 | 0 |  |
| `paper/container/build-paper.sh` | 1 | 0 |  |
| `paper/environment_values.toml` | 12 | 0 |  |
| `paper/figures/chart_level.py` | 3 | 0 |  |
| `paper/generate_findings.py` | 53 | 0 |  |
| `paper/generate_gaps.py` | 3 | 0 |  |
| `paper/generate_model.py` | 8 | 0 |  |
| `paper/generate_prior_art.py` | 4 | 0 |  |
| `paper/generate_proofs.py` | 1 | 0 |  |
| `paper/generate_reading_pass.py` | 1 | 0 |  |
| `paper/generate_register.py` | 9 | 0 |  |
| `paper/generate_repro.py` | 2 | 0 |  |
| `paper/generate_results.py` | 12 | 0 |  |
| `paper/generate_supplement.py` | 1 | 0 |  |
| `paper/length_ledger.toml` | 49 | 146 | dated (row text) |
| `paper/myst.yml` | 2 | 0 |  |
| `paper/paper.ipynb` | 208 | 0 |  |
| `paper/paper_common.py` | 1 | 0 |  |
| `paper/prior_art.yaml` | 18 | 0 |  |
| `paper/reading_pass.yaml` | 2 | 0 |  |
| `paper/regenerate_row.py` | 4 | 0 |  |
| `paper/style.css` | 1 | 0 |  |
| `paper/supplement/metric-associations.md` | 1 | 0 |  |
| `paper/supporting_material.ipynb` | 569 | 0 |  |
| `scripts/check_vocabulary.py` | 2 | 0 |  |
| `scripts/prose_surfaces.py` | 3 | 0 |  |
| `scripts/residuals_baseline.json` | 48 | 0 |  |
| `tests/test_paper.py` | 267 | 27 | dated (history comment) |
| `tests/test_site.py` | 4 | 0 |  |
| `tests/test_vocabulary.py` | 1 | 0 |  |

Dated files, left as written (5,831 occurrences): `work-packages/` (175 files, 5,740), `paper/container/RECORD.md` (49), `docs/superpowers/notes/` (three files but the gaps ledger, 13), `notes/directions/` (three readouts, 10), `notes/user-journeys.md` (10), `scripts/vocabulary_baseline.toml` (3), `derivation/PROOF_MAP_FINDINGS.md` (2), `notes/references-verified.md` (2), `notes/paper-prior-art-sources.md` (1), `examples/adcs/experiments/reports/change-register.md` (1).

Three lines are read in the new letters and name a subsection the new structure lacks; each is meant: `tests/test_paper.py` 2186 and 2190 assert that Appendix A has no A.2 (the old G.2, the reading pass, moved to the supplement at WP57a); `tests/test_site.py` 83 is a dated comment, "743 until WP57c (+24, D.12 moved in)", the old D.12. Every other new-sense occurrence names a subsection the structure has.

## R-4: nothing but letters and numbers

`WP57-rounds/e/word_diff.py` pairs the two notebooks' cells by id through the id map and compares each source word by
word; every changed run must be what the letter map makes of the old one (`word-diff.txt`, summary):

    paper/paper.ipynb: 110 cells at the base, 110 now
    markdown: 77 cells paired, 45 changed, 148 words changed
    code: 33 cells paired, 0 changed, 0 words changed
    paper/supporting_material.ipynb: 112 cells at the base, 112 now
    order changed: True
    markdown: 62 cells paired, 52 changed, 171 words changed
    code: 50 cells paired, 0 changed, 0 words changed
    {"other_changes": 0}

The distinct token pairs and their counts are in `word-diff.txt` (for example `<sub-d-16>` to `<sub-b-11>`, `(sub-h-4)=` to `(sub-c-4)=`, `Appendix B, L4` to `Appendix E, L4`).

The outputs (`output_diff.py`, `output-diff.txt`), code cells paired by id, execution counts aside (the new cell
order renumbers them): `paper/paper.ipynb` 24 cells' outputs unchanged and 9 changed in letters only, each a generated
sentence whose link carries a letter; `paper/supporting_material.ipynb` 38 unchanged and 12 changed in letters only, two
of which also changed beyond their letters: H.1's toolchain table (its commit row reads the branch's base, as at every
execution) and H.4's one row per figure and table (in page order, so its rows move with the appendices; the same rows).

The proof map: 22 lemma files, 549 tagged steps, as dev. `git diff --stat dev -- derivation examples/adcs/data
examples/adcs/model_v2` is empty; `paper/stability_extra.json` is unchanged; no figure file changed (`paper/figures/chart_level.py` has three comments re-lettered; no image).

Residuals (`residual_keys.py`, `residual-keys.txt`): every surface count of the report equal to before under its renamed
key, with one reading of the checker: the front matter (two words) is folded into the next surface of its status, which
is now Appendix A (before, the generated notation table followed it, of another status), so A's counts are read under
`appendix/title`; compared as one surface, front matter and A, the counts are equal. Two document counts fell, both
first-use counts that follow the order of the page: `paper/supporting_material.ipynb` terms undefined at first use 16 to
6, acronyms 7 to 6 (the first use of a term now falls in another appendix). The baseline
(`scripts/residuals_baseline.json`) is dev's with its keys renamed by the same map (`reletter.py`), not regenerated:
`--write-baseline` would also write today's counts on every other surface and absorb the rises dev already carries
(docs, site, glossary); the stale entries of earlier packages (`d-1`, `d-2`, `d-6`, `d-7`, `d-12`, and the old G.2's
`g-2`, moved to `a-2` because G.2 is now the limitations) keep their counts, so each file's totals are the same. The
strict comparison lists the same 125 rises as on dev less one (the supporting material's terms undefined at first use,
which fell below its baseline), each under its renamed key.

## G4: the numbering test

`test_appendix_headings_a_to_g_in_order` is `test_appendix_headings_a_to_h_in_order` (the headings A to H, in order, with
`APPENDICES` in the new order); `test_every_appendix_numbers_its_subsections_from_one` (new) asserts, under every letter,
the subsections 1, 2, 3, ... with no gap (D has none) and every `###` heading under its own letter;
`test_the_letters_are_the_order_of_first_mention_in_the_paper` (new) recomputes R-1. The F and B test that WP57c relaxed
to order only no longer carries its own numbering clause. Two literals read dated records and keep their old letters,
each with a comment: the assumptions queue (`WP57-rounds/assumptions-queue.md`, "E.2"/"E.3") and the spike's draft
(`h-sections.md`, `=== app-H-2`). The plain-text check of `test_appendix_and_section_references_resolve` read
`Appendix [A-G]`, all letters but H's; re-lettered it reads `Appendix [ABD-H]`, all but the HoroPCA appendix's (see Left
for the driver). The plain-text checks of subsection numbers read `[B-G]\.\d`; they now read `[A-H]`, and pass.

## Checks

Every exit code captured to a file (`cmd > log 2>&1; echo NAME=$? >> exits.txt`; `scratchpad/wp57e-checks/`).

| Check | Command | Output | Exit |
|---|---|---|---|
| Notebooks | `cd paper && MPLCONFIGDIR=<warm cache> uv run python execute_notebooks.py` (both, after the edits; then the supporting notebook again after the gaps ledger followed) | executed paper.ipynb, executed supporting_material.ipynb | 0, 0 |
| Lint, format, lock | `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check` | All checks passed; 638 files already formatted; resolved 194 packages | 0, 0, 0 |
| Proof map | `uv run python -m derivation.proofmap` | PROOF MAP OK: 22 lemma files, 549 tagged steps (as dev) | 0 |
| Vocabulary | `uv run python scripts/check_vocabulary.py` | 0 new violation(s), 67 known | 0 |
| Residuals | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` | exits 1 as on dev: 125 rises, dev's 126 less the supporting material's terms undefined at first use (16 against a baseline of 11 on dev; 6 now); every other rise the same count under its renamed key | 1 |
| Supplement | `uv run python paper/generate_supplement.py --check` | the four files equal their generators | 0 |
| Register | `uv run pytest -q tests/test_claims_register.py` | 21 passed | 0 |
| Data and derivations | `git diff --stat dev -- derivation examples/adcs/data examples/adcs/model_v2` | empty | 0 |
| Word diff, outputs, pointers | `word_diff.py`, `output_diff.py`, `pointers.py` in `WP57-rounds/e/` | 0 other changes; 0 other outputs; 85 pointers, 0 differ | 0, 0, 0 |
| Docs | `uv run mkdocs build -q` | built (the MkDocs 2 notice only) | 0 |
| Fast suite | `MPLCONFIGDIR=<warm cache> uv run pytest -q -m "not slow" -n auto` | 2,097 passed, 17 skipped, 2 xfailed (dev: 2,095; two tests added) | 0 |
| Slow paper tests | `MPLCONFIGDIR=<warm cache> uv run pytest -q -m slow -n auto tests/test_paper.py tests/test_case.py::test_docstrings_run_and_are_numpydoc` | 31 passed in 14 min 15 s (after the last edit) | 0 |
| Paper build | `cd paper && BASE_URL=/paper uv run --frozen myst build --html` | no warning or error in the log (R-2) | 0 |
| R-3 | `uv run python work-packages/WP57-rounds/e/r3_grep.py` | the table above; three meant lines | 0 |

`WP57-rounds/e/exits.txt` is the run's exit file.

The site was served on port 8907 (`scratchpad/serve57e`, a link to `paper/_build/html`) for the captures and stopped.

## Register

Ids: none added, none retired. Re-anchored: 96 `anchor` fields and 2 `fragment` fields follow the new letters (the
subsection headings "G.2 Limitations" (39 rows), "G.3 Open questions" (15), "C.4 What the table shows" (7), "C.1 The
hypothesis and what would refute it" (7), "H.2 The environment of record" (6), and the rest); `tests/test_claims_register.py`
passes.

## Amendments

None to the scope. Readings recorded:

1. The ledger's rows: the scope keeps the dated rows as written and renames the ceiling keys. A row's `section` field is
   the key it adds to (`ledger_ceilings` sums the rows by it), so it follows the key; the row's text, date, words and
   authority are as written. Without it the old rows would add to the wrong appendix (an "Appendix H" row to the
   reproducibility appendix).
2. The residual baseline: renamed, not regenerated (above), so no rise of dev is absorbed.
3. The gaps ledger in `docs/superpowers/notes/` follows, as the source of G.2's table (above).
4. Test function names keep their letters (above).

## Left for the driver

- Soft-confirm on the captures; landing on `dev`; CI on both platforms.
- The table caption of C ("Appendix C's hypothesis table: ...") names its own appendix in plain text; before, the
  references test's plain-text check read `[A-G]` and so never read H's caption. Re-lettered the check keeps its old
  reach (all but the HoroPCA appendix). A role or a cut of the self-reference is a wording edit, outside this package.
- The register's `note` and `source` fields and the length ledger's row text keep their dated letters; the test
  function names keep theirs (56 register backings cite them). A rename of the test names, with the backings, is a
  small package of its own if wanted (WP58's sweep).
- The supporting page's tables are numbered by MyST in page order, so every table number moved: the HoroPCA table is
  Table 1, G's assumptions Table 2 (was 1), cited Table 3, gaps Table 4. No sentence types a table number (the
  references test forbids it).
- The parent's D-3 (a read of the whole supporting material) and WP58 follow.
