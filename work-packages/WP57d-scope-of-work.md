# WP57d — Scope of work: Appendix E as "Assumptions, limitations and open questions", and Appendix H

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy; runs after the regime rename lands, one unit, one writer on the supporting notebook |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `wp57d` in its own worktree off `dev` at the rename's landing |
| **Approval record** | The driver's approval under his mandate, quoted in `WP57-decisions.md` |
| **Acceptance record** | The driver's soft-confirm of each appendix on screenshots; his read afterwards |

## Purpose

His direction (`WP57-decisions.md`): the appendices are "one step deeper where needed. do not metanarrate. the
appendices job IS NOT to opine on the text of the paper." The parent's brief (`WP57-scope-of-work.md`, G3): "The
'Assumptions, limitations and open questions' section built from Appendix E and the ledger
`work-packages/review/open-questions.md`: each item with the section it left, what is assumed or not established, and
its record; no caveat repeated in the main text." The shape is the map's (`WP57-rounds/map.md`, section 2.2) and its
inventory is 2.1; the sentences the children moved here are `WP57-rounds/assumptions-queue.md` (nine entries). For H,
the driver's call 3 (`WP57-decisions.md`): kept, shortened to what Section 2's HoroPCA sentence needs.

## Goals

- G1. **Appendix E becomes "Assumptions, limitations and open questions"** in the map's three parts, each a list or a
  table and no prose about the page: (1) the assumptions table, generated from `derivation/axioms.py` by an addition to
  `paper/generate_gaps.py` (rows A0 to A11 and R1 to R3: id, the statement in one line, where the main text states it,
  the results that import it, from the proof map; the I- and F-entries by id with their citation, one line each);
  (2) the limitations, one line per item grouped by the section it left (Sections 2 to 9 as the paper stands after
  WP55 and WP56, then the appendices): what is not established and its record (a gap id, a lemma, a subsection, a
  page); then the gaps table in its four-column form (gap, bridging assumption, what cannot be proved, interpretive
  consequence; one link per row to the ledger row; the formal-object and sensitivity columns stay in
  `docs/superpowers/notes/abstraction-gaps.md`); (3) the open questions: every open entry of
  `work-packages/review/open-questions.md` (OQ-1 to OQ-10, OQ-12 to OQ-14; OQ-11 is closed) in one line each with its
  record, and the research questions Section 9 and the queue name (successive trade-offs and PCA; the kernel direction)
  in one line each pointing at the readout in `notes/directions/`. Each item once; a caveat Section 6 states at its
  result is a pointer here, not a restatement.
- G2. **The queue placed.** Each of the nine entries of `WP57-rounds/assumptions-queue.md` lands as one line of G1's
  part (2) or (3), in the section's own words, or is recorded as already covered by another line; every entry marked
  with where it landed.
- G3. **Appendix H by the map:** the Job block cut; H.1's self-describing sentence cut (C591 retires); H.2, H.3 and
  H.4 kept, the three reading limits (a) to (c) listed in E's part (2) by reference to H.4, not repeated; H.5 ("How the
  formalism and the solvers differ") moves to the repository with one citing line at the end of H.4 unless a sentence
  of Sections 2 to 9 needs it, which the unit checks first.
- G4. **Pointers.** Section 6's and Section 9's sentences that name Appendix E keep resolving to the renamed section
  (anchor `appendix-e` kept; the letter E until WP57e); Section 2's HoroPCA sentence keeps resolving to H. Main-text
  edits are these pointers' text only, if the new title needs it.
- G5. **Register, tests, ledger, baselines:** ids from C997; one register row per typed line that makes a claim; the
  generated parts carry none; a test that the assumptions table's rows equal the ledger of `derivation/axioms.py`; a
  test that the open-questions list names every open OQ of the ledger once and no closed one; the queue's lines
  marked; `paper/length_ledger.toml`; `scripts/residuals_baseline.json` lowered only where E and H counts fell;
  `paper/stability_extra.json` only where a recorded sentence changes.

## Non-goals

- Appendices A, B, C, D, F, G (landed). Re-lettering (WP57e). Main-text edits beyond G4's pointers. New caveats: the
  section lists what the paper and the records already state, it invents nothing. The substance of the OQ ledger (an
  entry may gain a "listed in the section" line, nothing else). The data of record, the lemma scripts and
  `derivation/axioms.py`, the SysML v2 model files, `docs/superpowers/notes/abstraction-gaps.md`'s rows. Opinions on
  the paper's text inside an appendix.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/supporting_material.ipynb`, the E and H cells; `paper/paper.ipynb` only if a pointer's text changes; both re-executed | G1 to G4 |
| D-2 | `paper/generate_gaps.py` (the assumptions table from `derivation/axioms.py` and the proof map; `gaps_table` in four columns); `paper/generate_prior_art.py` where H's cut touches it | G1, G3 |
| D-3 | H.5's text at its repository path, if moved, cited from H.4 in one line | G3 |
| D-4 | `claims_register.toml`, `tests/test_paper.py`, `paper/length_ledger.toml`, `scripts/residuals_baseline.json`, `paper/stability_extra.json` if needed; `WP57-rounds/assumptions-queue.md` with each line marked | G2, G5 |
| D-5 | `work-packages/WP57d-review.md`: the section's items in a table (item, part, section it left, record, register row), before-and-after words for E and H by `map_counts.py`, the checks with their outputs; captures in `WP57-rounds/d/` of E's top, each of the three parts, H.1 and H.4 at desktop width, with the unit's cold read (`cold-read.md`) | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every item of the section appears once, with a record that resolves; every open OQ of the ledger is listed and no closed one; every queue line is placed or covered | the review's item table; the G5 tests; `uv run pytest tests/test_paper.py -k references_resolve` |
| R-2 | No sentence in E or H is about the paper's text or the page; no Job block renders in E or H | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` (the supporting notebook at or below dev on every count); the driver's read |
| R-3 | Nothing cut is lost: H.5 at its path if moved, cited in one line; the rest in git | the review's dispositions with paths; `git show <dev hash>:paper/supporting_material.ipynb` |
| R-4 | The assumptions table is generated from `derivation/axioms.py` and never typed; the main text's caveats are not restated | the G5 test; the driver's read against the map's 2.1 |
| R-5 | The derivation chain, proof map and data of record unchanged | `uv run python -m derivation.proofmap` identical to `dev` (22 files, 549 steps); `git diff --stat dev -- derivation examples/adcs/data examples/adcs/model_v2` empty |
| R-6 | Lint, format, lock, vocabulary, the fast suite, the slow paper tests with the docstring test, the builds, CI | `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `scripts/check_vocabulary.py` 0 new; `uv run pytest -q -m "not slow" -n auto`; `uv run pytest -q -m slow -n auto tests/test_paper.py tests/test_case.py::test_docstrings_run_and_are_numpydoc`; `uv run mkdocs build -q`; the MyST build log clean; CI green on both platforms |

## Definition of good

A reader who asks "what does this paper assume, what does it not establish, what is open" finds each answer once, in
one place, with the record that backs it, and finds nothing there that the paper's own sections state better.

## Definition of good enough

The three parts render as lists or tables with each item once and its record resolving; the nine queue lines marked;
H's Job block and self-description gone and H.5 placed; R-1 to R-6 met; E and H soft-confirmed on screenshots.

## Definition of done

Good enough met, no open item remaining unresolved, landed on `dev`, the soft-confirm recorded in `WP57-decisions.md`.

## Agent's defaults

- The section's heading is "Appendix E. Assumptions, limitations and open questions" until WP57e re-letters; the
  anchor `appendix-e` and the sub-anchors `sub-e-1` to `sub-e-3` for the three parts.
- The limitations lines are written from the map's inventory 2.1, re-read against the paper as it stands (Sections 7
  to 9 after WP56; Section 9's limits passage is the source for the case's items); where 2.1 and the paper differ, the
  paper wins and the review says so.
- The open-questions lines quote nothing from the ledger; each is the OQ's title in the ledger's words with its
  section and record. OQ-14's two retirements are listed as open until WP58 resolves them.
- H.5's repository home, if moved: `notes/directions/`, appended to the existing HoroPCA readout if one is there,
  else a new file named for it; the unit checks the directory first.
- One or two commits on `wp57d` (E first, then H), merged to `dev` by the driver after the soft-confirm.
- The unit's cold read of each rendered appendix at desktop width goes in the review; the driver reads the captures.

## Open decisions

None for him. The driver's calls: the map's shape (2.2) is taken as written; H by the map and call 3; the queue's
Section 9 items are limitations or open questions, not restored to Section 9.
