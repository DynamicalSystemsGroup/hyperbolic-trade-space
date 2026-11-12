# WP35, Amendment 1 — Scope of work: Appendix H, the HoroPCA comparison as a tested hypothesis

| | |
|---|---|
| **Status** | DRAFT, for the assistant's approval. Approved only by the recorded act below; nothing is built before then. |
| **Amends** | `WP35-scope-of-work.md` (approved at 1d27f8c): it adds Appendix H, replaces D-2 and the Appendix G part of G1, and lifts one non-goal. Everything not named under "What it lifts" and "What it replaces" stays as approved. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The assistant's approval, quoted verbatim in `work-packages/WP35-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim in `WP35-decisions.md`, after `WP35-review.md` |

## Purpose

The supervisor's amendment, verbatim (`WP35-decisions.md`, 2026-11-13, 13165e8):

> i think the horoPCA comparison analysis needs its own appendix, and i need it broken down a bit cleaner. we need
> an explicit (and falsifiable) hypothesis about how our method differs from theres. then a computational
> experiment that can assess (validate or invalidat) that hypothesis, then results, then interpretation. this
> section should probably also include some explanation of how the underlying formalism and solvers differ but the
> critical result is to demonstrate that the methods are doing different things, that renders them complementary
> rather than competitive.

Stage 1b ran the experiment: the hypothesis and its refutation conditions were committed before any table was
generated (830cf54), the outputs after (`WP35-rounds/spike-h/{hypothesis.md, readout.md, results.json, summary.txt}`,
ef4d118); every pre-registered part survived; the assistant reproduced the record and decided the content
(`WP35-decisions.md`, 2026-11-13 09:20: Q1 (a), Q2 (b), Q3 (a), Q4 (a), Q5 (a)). This amendment is the build, quality
control, integration and review of that appendix. Head: `dev` at `5a5b40c` or later.

## What it adds

- **Appendix H** of the supporting material (`paper/supporting_material.ipynb`), after Appendix G, titled for what it
  is (default: "Appendix H. HoroPCA beside this work: a tested hypothesis"). Its sections, in the supervisor's order:
  1. **Hypothesis**, with its refutation conditions: H1 to H4 as pre-registered (hypothesis.md at 830cf54), each with the
     result that would have refuted it, stated before the results.
  2. **Design**, in one paragraph: the three arms (A: edge fixed, spread varied; B: the package's generator with the
     planted vector moved off the depth axis; C: the same spread with no edge), 6 tables per cell, the three methods,
     the measure (absolute cosine with the planted vector), the threshold fixed before the run.
  3. **Results**: one table built from arms A to C with a verdict column (below).
  4. **Interpretation**: what each method estimates, shown by the table in which the two part; the methods are
     complementary, not competitive; the chain to D.16; the smallest-variance component as the part not in the hypothesis.
  5. **How the formalism and the solvers differ**: a short account from the readout's section 5 (what is estimated,
     the criterion and the parameter space, convex against nonconvex, a certificate against none, the interface), each
     statement with its source.
- **The results table**, generated from `work-packages/WP35-rounds/spike-h/results.json` by a function in
  `paper/generate_prior_art.py` (`horopca_hypothesis_table()`, the supporting material's generator; no hand-typed
  number). One row per cell of arms A, B and C (or per part of H where cells are pooled): this work's recovered count,
  PCA's first component, HoroPCA's first direction at R = 0.25 and R = 1, and a **verdict** column that the function
  computes from the pre-registered refutation conditions applied to the cells (survives / refuted), not typed. The
  threshold 0.9 on |cos| and the chance rates (0.037 for a random direction, 0.152 for a random point of the simplex)
  stand beside it, read from the same file. Arm D, the cubesat rows, the loadings and HoroPCA at R = 3 are not in the
  table (R = 3 is named in a sentence as reported, not tested).
- **The two sentences on the smallest-variance component**, as the part not in the hypothesis: it recovers the planted
  vector in 5 of 6 tables at rho = 0.25 and at t = 0.9, and in none of the other nine cells; the analyst cannot pick it
  without knowing the vector (counts read from the record by the same function or checked by the test).
- **The chain to D.16, in words**: Appendix D.16 runs a principal component analysis on the chart coordinates of the
  near-frontier designs, a reading of the trade-offs the sampling exercised; a HoroPCA of the chart would be the same
  kind of chain and was not run. A pointer to D.16 and no new analysis.
- **The embedding stated as ours in the reading limits**: log-metrics are Euclidean coordinates; the centre, the scale
  R and the map into the ball are our choices (three scales); a second embedding was not run and would add whether
  HoroPCA's R = 3 behaviour belongs to the embedding or to the method. The other reading limits of the readout's
  section 7 that bear on a claim (tables not tree-like; a construction of our making in d = 4, noise-free; six tables
  per cell; k at most 2, default hyperparameters; targets compared as vectors in one space) are one short list.
- **Plain first-use lines** for R, PC, |cos|, span alignment, frame and horosphere (one plain line each, at the point
  of first use in Appendix H), and a **caption and a source link** on the table (`results.json`, `hypothesis.md` at
  830cf54, `readout.md`).
- **Word budget and ledger.** `paper/length_ledger.toml` gains a section `"Appendix H" = 0` under
  `[baseline.sections]` and one `[[raise]]` row, section "Appendix H", words_added about 900 *(default; the ceiling is
  fixed at the build from the written appendix and may not be exceeded without a new row)*, with its job and reader
  ("the expert who asks whether the closest existing analog does what this work does, and what the experiment would
  have shown otherwise"). Appendix H's count is by the visible prose rule of `tests/test_paper.py`.
- **Claims register and reading pass.** One `claims_register.toml` row for every sentence of Appendix H that a reader
  can rely on (each backed by the generated table, the test, `hypothesis.md` at 830cf54 or `readout.md`); the existing
  rows that backed the removed passage (C529 and the rows citing `test_the_horopca_*`) re-pointed or retired with the
  disposition stated. `paper/reading_pass.yaml` row 44 (HoroPCA) re-pointed from "Section 2 and Appendix G" to
  "Section 2 and Appendix H", the abstract reading unchanged.
- **Tests** (`tests/test_paper.py`): (i) the printed table equals `results.json`, read independently of the generator,
  cell by cell, and the verdicts equal the pre-registered rules recomputed in the test; (ii) the threshold and the two
  chance rates printed equal the file's; (iii) Appendix H has its five sections in order; (iv) no sentence of Appendix H
  or Section 2 says HoroPCA is worse, poorer or inferior (a phrase list, default) and none calls this work a PCA of any
  kind or HoroPCA "PCA with a kernel"; (v) `generate_repro.py`'s source map names the new function and file.

## What it lifts

- The WP35 non-goal "no new section, figure or page" is lifted for this appendix **by the supervisor's word** (the
  amendment quoted above; `WP35-decisions.md`, 2026-11-13). No other new section, figure or page.

## What it replaces

- **D-2 and G1's "in full in Appendix G".** The full version of the HoroPCA distinction is Appendix H. The earlier
  passage in Appendix G (cells `app-G-horopca`, `tab-G-horopca`, `app-G-horopca-reading` of the supporting material;
  about 650 words and the spike's table generated by `horopca_rows()` and `horopca_table()`) is removed.
  **What it no longer did:** it asserted a causal reading ("recovered only where the generator made them the direction of
  largest spread") from a handful of tables where the factor was never varied, with an undefined "recovered", terms
  (PC, |cos|, span alignment, distortion, frame, horosphere) left unexplained, a cubesat "target" that was our own fit,
  numbers without a source or command, and a table without a caption or source; Appendix H states the claim as a tested
  hypothesis and carries each of those fixes. The earlier generated table, its generator functions and its two tests
  (`test_the_horopca_table_equals_the_spike_record`, `test_the_horopca_passage_numbers_are_in_the_record`) leave with
  it; their requirement (every number is in a record, the table is generated) is carried by the new tests. The spike
  folder `docs/superpowers/notes/spike-horopca/` stays untouched as the first spike's record and is linked from H.
  The ledger: a `[[cut]]` row on "Appendix G" for the words removed (measured at the build), authority "WP35 amendment 1,
  the supervisor's request that the comparison have its own appendix".
- **Appendix G keeps** the HoroPCA row of the register of prior art (the row's text unchanged except its
  `differs` pointer) and one sentence pointing at Appendix H.
- **Section 2's HoroPCA paragraph** (`sec-prior-art-3`) points at Appendix H instead of Appendix G, and its claim about
  the exponents is reworded to what Appendix H tests (recovered where the planted vector is the direction of largest
  spread, not elsewhere), net words not higher than now (a ledger row only if they are).
- **D-3's `prior_art.yaml` horopca row**: any pointer to "Appendix G's passage" in `cites`, `does`, `differs` or
  comments becomes "Appendix H"; the convention test stands.
- R-2 (the table equals the spike's record), R-3 (the embedding stated as ours, the limits, the cited folder) and R-13
  (the cold reader) are re-pointed from "Appendix G" to "Appendix H" and restated under Requirements below; R-14
  (the P9 and P10 balance) names Appendix H.

## What stays

Goals G2 to G5 and deliverables D-1, D-3 (the split rows, the convention), D-4 to D-8 as approved and, where already
built, as landed. Non-goals as approved, plus the amendment's own below. The sequencing rule, the agent models by role
and the blast radius of the WP35 scope; this amendment adds to the blast radius `paper/supporting_material.ipynb`
(Appendix G passage out, Appendix H in), `paper/generate_prior_art.py`, `paper/generate_repro.py` (its source map only),
`tests/test_paper.py`, and read-only `work-packages/WP35-rounds/spike-h/`.

## Goals

- A1. **Appendix H presents the comparison as a falsifiable hypothesis, an experiment, results, an interpretation and
  an account of the formalism and solvers, in that order,** so a reader can see the methods do different things.
- A2. **The methods are shown complementary, not competitive:** the table in which they part is the evidence; no
  sentence says HoroPCA is worse at what it was built for.
- A3. **Every number of Appendix H is generated from the record or cited to a command,** and the earlier passage's
  causal claim is now tested rather than asserted.

## Non-goals

- No second embedding (Q2 (b): the embedding is stated as ours in the reading limits).
- No third arm and no HoroPCA or PCA run on this work's chart (Q3 (a): the chain is in words, pointing at D.16).
- No rerun of the HoroPCA fits and no change to `results.json`, `summary.txt`, `hypothesis.md` or the scripts of
  `spike-h/`; the table reads them.
- No change to Appendix D.16 or to any other part of D.
- No arm D, cubesat rows or loadings in Appendix H (they stay in the notes and readouts, linked).
- No claim about HoroPCA on the data of its own tasks, none that it is worse at anything it was built for, none that no
  embedding gives it the edge.
- No new reference, no change under `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, the data, the interface
  contract, the title, section order or the entry surfaces (`site/index.html`, `README.md`, the abstract,
  `site/history.html`, `docs/index.md`).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| A-1 | Appendix H in `paper/supporting_material.ipynb`: the five sections in the supervisor's order; the plain first-use lines; the reading limits with the embedding stated as ours; the two sentences on the smallest-variance component; the chain to D.16 in words | A1, A2 |
| A-2 | `horopca_hypothesis_table()` (and a helper that evaluates the refutation conditions) in `paper/generate_prior_art.py`, reading `work-packages/WP35-rounds/spike-h/results.json`; threshold and chance rates beside it; `generate_repro.py` source map | A3 |
| A-3 | Appendix G: the earlier HoroPCA passage, its table, generator functions and tests removed; the register row kept; a pointer to H. Section 2's paragraph and `prior_art.yaml` pointers re-pointed to H | A1 |
| A-4 | `paper/length_ledger.toml`: the "Appendix H" baseline entry, one raise row, one Appendix G cut row; `claims_register.toml` rows for Appendix H, the re-pointed or retired rows; `paper/reading_pass.yaml` row 44 | A3 |
| A-5 | New tests in `tests/test_paper.py` (table equals record, verdicts recomputed, chance rates, section order, register words) | A3 |
| A-6 | Notebooks re-executed with their figure files in one commit | A1 |
| A-7 | `WP35-review.md` and `WP35-review/` extended: screenshots of the rendered appendix and Section 2, the fresh readers' words, the reader-criticism checks; `WP35-decisions.md` updated | A1 to A3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RA-1 | Appendix H's section headings are, in order: hypothesis (with its refutation conditions), design (one paragraph), results (one table), interpretation, how the formalism and solvers differ | read the rendered appendix; the section-order test |
| RA-2 | Every number in the results table is generated from `results.json` by the paper script; the verdict column is computed from the pre-registered conditions; "recovered" is defined at first use as |cos| at least 0.9 with the chance rates 0.037 and 0.152 beside the threshold | `uv run pytest tests/test_paper.py -k horopca`; a grep for typed digits in the cell that holds the table |
| RA-3 | The smallest-variance component is reported in two sentences, as the part not in the hypothesis, with the counts and the reason it is not a method | read the rendered appendix; the count test |
| RA-4 | The chain to D.16 is in words and points at D.16; no new analysis | read; grep for the D.16 anchor |
| RA-5 | The reading limits state the embedding as ours and not natural for the data (the tables are not tree-like), the construction, the six tables per cell, the defaults, and that HoroPCA at R = 3 is reported not tested | read; the readout's section 7 compared line by line |
| RA-6 | Register: the appendix says what each method estimates; no sentence says HoroPCA is worse, poorer or inferior, or calls this work a PCA, or HoroPCA "PCA with a kernel" | the phrase test; the fresh readers' reads |
| RA-7 | The earlier Appendix G passage, table, generator functions and tests are gone; Appendix G keeps the row and a pointer; Section 2 and `prior_art.yaml` point at H; no "Appendix G" pointer to HoroPCA results remains | `grep -rn "app-G-horopca\|horopca_table\|horopca_rows" paper tests docs`; the cross-reference check of the paper build |
| RA-8 | Words: Appendix H within its ledger row; the Appendix G cut recorded with its measured words; Section 2 not higher than now; no budget moves without a row | `uv run pytest tests/test_paper.py tests/test_site.py::test_word_budgets_hold`; counts in `WP35-review.md` |
| RA-9 | Claims: a register row for every relied-on sentence of Appendix H; reading-pass row 44 re-pointed; the register tests green | `uv run pytest tests/test_claims_register.py` |
| RA-10 | The reader criticisms of the earlier passage hold as checks on the finished appendix: (1) "recovered" has a stated threshold (0.9 on |cos|); (2) the causal claim is tested (arm A varies the spread with the edge fixed); (3) R, PC, |cos|, span alignment, distortion (if used), frame and horosphere have one plain line each at first use; (4) every kept number has a source or command; (5) the table has a caption and a source link; (6) at 390 px the table's right columns are not clipped | the rendered appendix at 1280 by 800 and 390 by 844 with screenshots; the readers' re-run |
| RA-11 | Acceptance by a cold read of the rendered appendix in the browser with a screenshot: fresh P9, P10 and R-13 readers re-run on the finished Appendix H and Section 2 (the P9 and P10 balance rule of R-14), the readers' words verbatim beside the intended reading, the reader criticisms above carried in as checks; a stderr line or broken link is a finding | `WP35-review.md`, `WP35-review/` screenshots from `scripts/stage_site.py` on a port other than 8791 |
| RA-12 | The suite and the repository checks: whole-repo `uv run ruff check .` and `uv run ruff format --check .`; `uv lock --check`; `uv run pytest -q -m "not slow"` on the touched tests (`tests/test_paper.py`, `tests/test_claims_register.py`, `tests/test_site.py`, `tests/test_docs.py`), `tests/test_text_encoding.py`, `uv run python scripts/check_vocabulary.py`; the ledger check (`tests/test_paper.py` ledger tests); no AI attribution | the commands, their one-line results in the review |
| RA-13 | No number of record moves: `results.json`, `summary.txt`, `hypothesis.md`, the scripts of `spike-h/`, the model and data outputs are unchanged; `git diff origin/dev -- src derivation pyproject.toml uv.lock` is empty | `git diff --stat`; the paper tests |

## Definition of good

- A reader who knows HoroPCA reads Appendix H, sees what would have refuted the claim, sees the table in which the two
  methods part, and leaves understanding that each does a different job and that a table can use both; a reader who
  does not know it is not lost at the first undefined term.
- The paper does not grow by more than the appendix's stated job; the old passage's words are gone.

## Definition of good enough

- A-1 to A-7 delivered; RA-1 to RA-13 hold, each with its evidence in `WP35-review.md`.
- The fresh readers' reads match the intended reading (the methods estimate different things and are complementary),
  or the mismatch is fixed or listed for the supervisor.
- The cascade review finds the repository in a clean merged state: ledger, register, reading pass, repro map, Section 2,
  Appendix G and Appendix H, docs and tests consistent; the staged site screenshots seen.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Sequencing

Appendix H is edited in `paper/supporting_material.ipynb` and Section 2 in `paper/paper.ipynb`; both are single-writer
files. The notebook edits and the re-execution **queue after the WP36 integration unit** (the future-directions
paragraph, which also goes through the paper notebook's single-writer queue). The generator function, the tests, the
ledger and register rows, `reading_pass.yaml` and `prior_art.yaml` may be prepared in a parallel worktree and land
with or before the notebook unit. While a gate's container regression runs, nothing that regenerates paper outputs is
pushed (standing rule). The WP33 repeat round (the paper-side wayfinding read on the changed surfaces) follows the
build as already sequenced.

## Agent's defaults

- The appendix title, "Appendix H. HoroPCA beside this work: a tested hypothesis".
- The word budget of about 900 for Appendix H, fixed at the build from the written appendix; the Appendix G cut equals
  the words measured for the removed cells.
- The table has one row per cell of arms A, B and C (pooling the cells of a part where the pre-registered rule pools
  them), with the verdict column computed from the record; HoroPCA's columns are k = 1 at R = 0.25 and R = 1; R = 3 is
  named in a sentence.
- The verdict wording is "survives" or "refuted", as in the readout.
- The phrase list of RA-6 ("worse", "poorer", "inferior", "outperform", "beats") and its scope (Appendix H and
  Section 2's paragraph).
- Code locations in the account of the solvers are cited to the authors' commit `c9a9996` and this repository's files, as
  in the readout's section 5; the table of that section is condensed to the statements the argument needs.
- One unit per surface and one push each (generator and tests; ledger, register, reading pass, repro map; notebooks and
  figure files; review), all on `dev`; `main` gets a no-ff merge only at the accepted package.
- The agent models by role of the WP35 scope: Sonnet for the implementer and for the fresh readers, Haiku for mechanical
  units; no sub-agent without the PM.

## Open decisions (for the supervisor)

None. The structure and order are the supervisor's words; the content was decided by the assistant under the
supervisor's amendment (Q1 (a), Q2 (b), Q3 (a), Q4 (a), Q5 (a), each revertible by the supervisor).

## Blast radius

- Owned, in addition to the WP35 scope's: `paper/supporting_material.ipynb` (Appendix G's HoroPCA cells out, Appendix H
  in), `paper/paper.ipynb` (Section 2's HoroPCA paragraph, the pointer only), `paper/generate_prior_art.py`,
  `paper/generate_repro.py` (the source map), `paper/length_ledger.toml`, `claims_register.toml`,
  `paper/reading_pass.yaml` (row 44), `paper/prior_art.yaml` (pointers), `tests/test_paper.py`, `work-packages/WP35-*`.
- Read, never written: `work-packages/WP35-rounds/spike-h/`, `docs/superpowers/notes/spike-horopca/`,
  `docs/references.bib`.
- Never: `src/`, `derivation/`, `pyproject.toml`, `uv.lock`, data, the model, the interface contract, the entry
  surfaces, the `verify` and `stage` worktrees, port 8791, tab-23, and any file under another agent's worktree.

## Lifecycle stages

(1b) Research spike: done, `WP35-rounds/spike-h/`. (2) Decide: done, `WP35-decisions.md` (Q1 to Q5 of 2026-11-13).
(3) Build: the generator and tests, the ledger, register and reading-pass rows, then the notebooks through the queue
after the WP36 integration unit. (4) Quality control: RA-2, RA-7, RA-8, RA-9, RA-12, RA-13 on the head. (5) Integrate:
Section 2's pointer, Appendix G's pointer, `prior_art.yaml`, the repro map, notebooks re-executed. (6) Review the
cascade to a clean merged state: the fresh P9, P10 and R-13 readers on the finished Appendix H and Section 2 with the
reader criticisms as checks (RA-10, RA-11), screenshots in the browser, then `WP35-review.md` for the supervisor's
acceptance.
