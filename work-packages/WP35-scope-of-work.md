# WP35 — Scope of work: HoroPCA acknowledged and distinguished, "hyperbolic" defined once, Table 1's "differs" column made uniform

| | |
|---|---|
| **Status** | DRAFT, for the assistant's approval. Approved only by the recorded act below; nothing is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The assistant's approval, quoted verbatim in `work-packages/WP35-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim in `WP35-decisions.md`, after `WP35-review.md` |

## Purpose

The supervisor's words, verbatim (`WP35-decisions.md`, 2026-11-12):

> there are several places where we compare to hyperbolicPCA and i think we could do a better job differentiating
> ourselves. to my knowledge that work is PCA with a specific kernel. we are not actually doing PCA at all, we're
> just borrowing some of its intuition, and looking at it as an example of how how scikit learn handles
> unsupervised learning in general. it seems like we should address this directly and concisely in the paper in
> the related work section, and in the associated appendix. the other reference that say its different can remain
> brief and point to the paper

> also since we're talking about wording, its worth noting that "hyperbolic" in our paper seems to reliably refer
> to negative curvature geometry, it may be helpful to clarify, potentially in the glossary and limit the number of
> times and places we need to caveat about it
> the table of comparisons to prior art as a row about how our method differs from the method the row references.
> its not always clear whether the difference described is about our method or the method we're distinguishing it
> form

> sounds like HoroPCA is the closest existing analog to our work and we need to acknowledge it more clearly and
> better distinguish from it. that may require a spike, and involve writing and testing code to make sure we're not
> just saying what we want to be true

> you don't necessarily need to reimplement it, you need to import it and run it, i want to understand how it
> differs in behavior and usefulness, not necessarily how its constructed. that said looking through its code to
> see how its solvers work is merited

The spike (stage 1) ran the authors' HoroPCA beside PCA on the paper's own tables and is read out in
`work-packages/WP35-rounds/spike/readout.md`; the assistant's decisions on it (Q1 to Q4, each revertible by the
supervisor) are in `WP35-decisions.md` and settle this scope. This package is stages 3 to 6: build, quality control,
integrate, review the cascade. Head: `dev` at `fe7b45d` or later.

## Goals

- G1. **HoroPCA is acknowledged as what it is and distinguished from this work, once and concisely, in Section 2**, and
  in full in Appendix G with the spike's results table (Q1 (a), Q4 (a) qualified).
- G2. **Table 1 and Appendix G read the same way in every row:** each row's `differs` cell is a sentence whose subject
  is this work; the kernel-PCA and HoroPCA row is two rows; a test keeps the convention (Q2 (a)).
- G3. **"Hyperbolic" is defined in one place, the glossary,** printed in Appendix A; the body's Definitions sentence
  stays the one place in the body; every other mention is a pointer or goes (Q3 (a)).
- G4. **The docs point, not repeat:** the limitations page's second definition and the further-reading line become
  pointers to the glossary and the paper.
- G5. **Every claim added or moved is backed and every surface is net neutral or negative in words** where it can be
  (the register, the ledger and the site budgets show it).

## Non-goals

- No change to the model, the fit, the data, or any number of record; the spike's numbers are quoted, not recomputed
  into the paper's results.
- No title change (Q3 (a)); no new section, figure or page.
- No code of HoroPCA in the package, `pyproject.toml`, `uv.lock` or any dependency; no re-implementation. The spike
  folder `docs/superpowers/notes/spike-horopca/` stays untouched as the record (ruff excludes it).
- No claim that this work is a PCA of any kind (Q4 (a)); no claim that HoroPCA "is PCA with a kernel" (the readout
  found no kernel and no Gram matrix); no claim about HoroPCA on the data of its own tasks (graphs), which the spike
  did not run.
- No change under `src/`, `derivation/`, the interface contract, the theme, section order or appendix letters.
- No work on Windows or container gates, and nothing that regenerates paper outputs beyond what the notebook
  re-execution below requires.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | Section 2 (`sec-prior-art-3`, `paper/paper.ipynb`): one concise paragraph: HoroPCA as the closest existing analog in setting and the farthest in what is estimated; what it generalizes (the components of PCA carried into hyperbolic space with horospherical projections); what this work borrows (the unsupervised setting, the estimator interface, PCA as a downstream step, chained in D.16); that runs on the paper's own tables recovered the exponents only where the generator made them the direction of largest spread. The two existing caveats in that section reduced to pointers (the Färe, Grosskopf and Lovell one to at most a half-clause pointing at the glossary) | G1, G3 |
| D-2 | Appendix G's full version (the HoroPCA row and a short passage): the spike's results table, the plain statement that the embedding was ours and not natural for the data (the tables are not tree-like), the solver contrast (nonconvex variance over frames by gradient ascent with restarts and no certificate, against convex programs on a simplex with one), what HoroPCA does that this work does not, and `docs/superpowers/notes/spike-horopca/` cited as the record | G1 |
| D-3 | `paper/prior_art.yaml`: the `kernel-hyperbolic-pca` row split into kernel PCA and HoroPCA; every `differs` cell (short and full) rewritten to the one convention, a sentence whose subject is this work ("This work ..."), the "by elision" rows given their subject, the "mixed" rows' family half moved into `does`; the Färe et al. row's `differs` likewise; a test in `tests/test_paper.py` pins the convention; `paper/reading_pass.yaml` row 44 and the generators' outputs regenerated | G2 |
| D-4 | `glossary.yaml` gains `hyperbolic` (the level curves of V: products of powers of metrics, the rectangular hyperbola in two; not negative-curvature geometry; not the Färe, Grosskopf and Lovell graph measure); Appendix A (`tab-A-register`) regenerated; the Definitions sentence kept as the body's one place | G3 |
| D-5 | `docs/user-guide/limitations.md` ("Name.") and `docs/further-reading.md` (the HoroPCA line) become pointers to the glossary and the paper | G4 |
| D-6 | `claims_register.toml` rows re-pointed or added for every changed sentence; `paper/length_ledger.toml` rows with the net words stated; the register, site, encoding and vocabulary tests green | G5 |
| D-7 | Notebooks re-executed with their figure files in one commit | G1 to G3 |
| D-8 | `WP35-review.md` with screenshots (`WP35-review/`) and `WP35-decisions.md` updated | G1 to G5 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Section 2 has exactly one paragraph on HoroPCA; it contains the phrases of Q1 (a) and Q4 (a): closest in setting, farthest in what is estimated; the borrowings; the exponents recovered only where the generator made them the direction of largest spread; it does not call this work a PCA of any kind and does not say "PCA with a kernel" of HoroPCA | read the rendered Section 2; `grep -n -i "with a kernel\|kernel PCA" ` over the paragraph; a register row per sentence |
| R-2 | Every number in Appendix G's results table equals the spike's `results.json` / `analysis.txt` (to the printed digits); the table is generated from the spike's record, not typed | a test comparing the printed table with `docs/superpowers/notes/spike-horopca/results.json`; `uv run pytest tests/test_paper.py` |
| R-3 | Appendix G says the embedding was ours and not natural for the data, names the limits of the comparison the readout lists (embedding scale, subsample for the cubesat, default hyperparameters, spike not benchmark), and cites the spike folder | read the rendered appendix; grep for the folder path |
| R-4 | `prior_art.yaml` has separate `kernel-pca` and `horopca` rows; every `differs` and `short.differs` cell begins with "This work" (or names this work as grammatical subject); no `does` cell does | the new test; `uv run pytest tests/test_paper.py -k prior_art` |
| R-5 | The mixed rows' family half is in `does`, not `differs`; the Pareto row's "Returns" no longer reads as a deficiency of the family | diff of `prior_art.yaml`; read Table 1 and Appendix G rendered |
| R-6 | The glossary entry `hyperbolic` exists and Appendix A prints it, regenerated in the same push; `uv run python scripts/check_vocabulary.py` passes | `uv run pytest tests/test_paper.py tests/test_vocabulary.py`; `uv run python scripts/check_vocabulary.py` |
| R-7 | The body defines "hyperbolic" in the Definitions sentence only; elsewhere in the paper, docs, README and notebooks every mention of the word as a caveat is a pointer or a half-clause; the title is unchanged | the spike's `grep_table.py` re-run over the same files, row by row, compared with `readout.md` 1a; `git diff` on `paper/myst.yml` shows no title change |
| R-8 | Moved or added claims keep their backing; every changed sentence has a register row | `uv run pytest tests/test_claims_register.py` |
| R-9 | Words: per touched surface the prose word count is not higher than at the start head, or the net rise is stated in a ledger row with its job; `BUDGETS`, `TOTAL_BUDGET` and the paper ceiling move only by a ledger row | `uv run pytest tests/test_site.py::test_word_budgets_hold tests/test_paper.py`; counts per surface in `WP35-review.md` |
| R-10 | No number of record moves: the paper's results, the model and data outputs are byte-identical to the start head apart from the intended text and the generated Appendix A/G tables | `git diff --stat` on `paper/` outputs and `examples/`; the paper tests |
| R-11 | Nothing of HoroPCA in the package or its lock | `git diff origin/dev -- pyproject.toml uv.lock src/` is empty; `uv lock --check` |
| R-12 | Notebooks are re-executed with their figure files in one commit; the paper notebook has one writer at a time (see Sequencing) | `git log --stat` of the commit; `paper/execute_notebooks.py` run; paper tests |
| R-13 | A fresh Sonnet reader, given only Section 2 and Appendix G as rendered at a named head, says in their own words what HoroPCA is, how this work differs, and what is shared, without being told; the reader finds no sentence that implies this work is a PCA, a hyperbolic-geometry method or a kernel method | `WP35-review.md`: the reader's words verbatim beside the intended reading |
| R-14 | The P9 and P10 balance rule holds: the paragraph and the appendix are read as a pair (a novice who follows the thread, an expert who finds nothing incorrect); a change requested by one lands only where the other does not lose the thread; detail the expert wants goes to the appendix or the spike record, not Section 2 | `WP35-review.md`: the pair's reads and the triage (`docs/superpowers/notes/reader-grid.md`, "P9 and P10, the balance") |
| R-15 | Every figure-free page touched (limitations, further reading, the glossary page, Appendix A, Table 1 as rendered) is screenshotted as rendered in a browser at 1280 by 800 and 390 by 844, a stderr line or broken link being a finding | `WP35-review/` screenshots with a one-line reading each; `scripts/stage_site.py` |
| R-16 | Whole-repo `uv run ruff check .` and `uv run ruff format --check .`; `uv run pytest -q -m "not slow"` on touched tests (full suite at the gate); `tests/test_text_encoding.py`; `uv lock --check`; no AI attribution in commits or files | the commands; grep of `git log` |

## Definition of good

- A reader meets HoroPCA in one paragraph that is fair to it, says what it is the closest to and what it is the
  farthest from, and could be checked against a table the reader can open; the word "hyperbolic" needs no caveat at
  the point of use because the glossary says it once; Table 1 reads down its "differs" column as one voice, this
  work's.
- The paper is shorter or equal in words; the appendix holds the numbers so the paragraph does not.

## Definition of good enough

- D-1 to D-8 delivered; R-1 to R-16 hold, each with its evidence in `WP35-review.md`.
- The fresh reader's read (R-13) matches the intended reading, or the mismatch is fixed or listed for the supervisor.
- The cascade review (stage 6) finds the repository in a clean merged state: ledger, register, glossary, Appendix A,
  docs and tests consistent; the staged site screenshots seen.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent models by role

Sonnet for the implementer and for the fresh reader of the review; Haiku for mechanical units (greps, counts,
screenshot runs, the grep-table re-run); nothing larger than Sonnet. The reader gets rendered pages only. No sub-agent
without the PM.

## Sequencing (the paper notebook has one writer at a time)

The paper notebook (`paper/paper.ipynb`) is edited by one unit at a time. WP35's notebook edits queue behind WP33's
paper unit (landed at `d8d650e`) and behind any other paper unit in flight. The order is: WP35 build, then the WP33
repeat round (the paper-side wayfinding read on the changed surfaces). WP37 touches no paper. Edits to
`prior_art.yaml`, `glossary.yaml`, the docs lines and the tests may proceed in parallel worktrees; only the notebook
edit, re-execution and the figure-file commit are serialized. While a gate's container regression runs, nothing that
regenerates paper outputs is pushed (standing rule); prose, docs and records may land.

## Agent's defaults

- The Appendix G table is generated from the spike's `results.json` by the prior-art or supporting-material
  generator, and shows the planted and cubesat targets at R = 1 only with the other two scales summarized in a
  sentence *(default; the full grid is in the spike folder)*.
- The two new rows are ids `kernel-pca` and `horopca`; the Färe et al. row keeps its id *(default)*.
- The convention test accepts "This work" as the opening of every `differs` and `short.differs` cell *(default)*.
- The glossary entry is one sentence of definition plus one of what it is not *(default)*.
- The docs pointers are one line each, linking the glossary and the paper section *(default)*.
- Word counts by visible text; the review and decisions files follow WP32 and WP33 form *(default)*.
- One unit per surface and one push each (paper notebook, prior-art register, glossary and Appendix A, docs), all on
  `dev`; `main` gets a no-ff merge only at the accepted package *(default)*.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (`WP35-decisions.md`: Q1 (a), Q2 (a) widened to a convention
for every "differs" cell, Q3 (a) with no title change, Q4 (a) qualified).

## Blast radius

- Owned: `paper/paper.ipynb` (Section 2, the DEA paragraph's caveat, the Definitions sentence untouched), the
  supporting material's generated Appendices A and G, `paper/prior_art.yaml`, `paper/reading_pass.yaml` row 44,
  `paper/generate_prior_art.py` (only if the table needs it), `paper/length_ledger.toml`, `glossary.yaml`,
  `claims_register.toml`, `docs/user-guide/limitations.md`, `docs/further-reading.md`, `tests/test_paper.py` (the
  convention and table tests), down-only `tests/test_site.py` budgets, `work-packages/WP35-*`.
- Read, never written: `docs/superpowers/notes/spike-horopca/`, `docs/references.bib` (`chami2021horopca` and
  `schoelkopf1998nonlinear` already resolved; a new reference needs a resolved DOI or stable URL and a PM check first).
- Never: `src/`, `pyproject.toml`, `uv.lock`, `derivation/`, data, the model, the interface contract, the `verify` and
  `stage` worktrees, tab-23, and any file under another agent's worktree.

## Lifecycle stages

(1) Research spike: done, `WP35-rounds/spike/readout.md`. (2) Decide: done, `WP35-decisions.md` Q1 to Q4. (3) Build: a
unit per surface as in Sequencing. (4) Quality control: R-2, R-4, R-6, R-8 to R-12, R-16 run on the head. (5) Integrate:
glossary, Appendix A, register rows, ledger, docs pointers, notebooks re-executed. (6) Review the cascade to a clean
merged state: the fresh reader (R-13), the P9 and P10 pair (R-14), the figure-free pages screenshotted (R-15), then the
WP33 repeat round on the changed surfaces, then `WP35-review.md` for the supervisor's acceptance.
