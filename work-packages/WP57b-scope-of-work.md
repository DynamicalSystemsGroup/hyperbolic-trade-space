# WP57b — Scope of work: Appendix B

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy; runs after WP55 lands, a then b, one unit, one writer on the supporting notebook |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `wp57ab` in its own worktree |
| **Approval record** | The driver's approval under his mandate, quoted in `WP57-decisions.md` |
| **Acceptance record** | The driver's soft-confirm of the appendix on screenshots; his read afterwards |

## Purpose

His direction (`WP57-decisions.md`): the appendices "need to be tightened down ... primarily as one step deeper where
needed. do not metanarrate. the appendices job IS NOT to opine on the text of the paper." The parent's brief for B:
"The proofs Section 6 points to, each reachable by its lemma label ... scripts cited, not opined on." Dispositions:
the map, section 1.

## Goals

- G1. **The Job block cut** (112 words of cell `app-B-job`); "What the scripts establish" kept (C387 to C389).
  The appendix no longer says what the main text keeps and what the repository keeps.
- G2. **`how_to_read` shortened** in `paper/generate_proofs.py`: the rule kept (one file per proof, one line per step,
  the tag) with the three kinds and their counts; the two-parts list and the closing paragraph dropped. It no longer
  repeats Section 9's verify-and-validate sentence or narrates the page's structure.
- G3. **B.2 shortened** (cell `app-B-2`) to the restart rule (random centres in the chart, the restart with
  the smallest mean slack returned), the stop rule, the polish (five reduced Newton steps after each SLSQP refit, the
  joint polish, G-16) and that the status refers to the polished point: what Section 5's "steps: Appendix B.2" and
  Section 6's "Newton steps that close the gap the solver leaves" need. "L16 does not prove that the alternation
  converges" (C142) is queued for WP57d's assumptions section. B.2 no longer restates Section 5's alternation, labels
  and program, comments on each lemma before its table, or says which results the paper does not use.
- G4. **Every proof reachable by its lemma label:** the proof map, B.1 (`proofs_fit`), `proofs_solver` (L12 to L22,
  the record whole) and B.3 (the checker) unchanged; every L-pointer of Sections 3 to 6 lands on its step table.

## Non-goals

- Any other appendix. Any lemma script, the record under `derivation/`, the proof map or the lemma numbering. Any
  main-text edit. Opinions on the paper's text. Re-lettering (WP57e).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/supporting_material.ipynb`: cells `app-B-job` and `app-B-2` edited; re-executed | G1, G3 |
| D-2 | `paper/generate_proofs.py`, `how_to_read` | G2 |
| D-3 | `work-packages/WP57-rounds/assumptions-queue.md`: the L16 line appended, for WP57d | G3 |
| D-4 | Register rows (C132 to C146, C666, C667 retired or re-anchored; new ids append-only); `tests/test_paper.py` (`test_the_claims_of_c1_have_their_true_basis`, `test_appendix_b_shows_every_result_of_the_record_with_derived_counts`); `paper/length_ledger.toml`; `scripts/residuals_baseline.json` | R-5 |
| D-5 | `work-packages/WP57b-review.md`: before-and-after words per subsection by `map_counts.py`; screenshots of the rendered top of B, B.2 and one step table reached from a Section 6 pointer; every L-pointer with its landing anchor | G4, acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every subsection kept is cited by a paper sentence or is its step deeper; every lemma label cited resolves | `uv run pytest tests/test_paper.py -k references_resolve`; `grep -o 'Appendix B, L[0-9.]*' paper/paper.ipynb \| sort -u` against the rendered anchors |
| R-2 | No sentence in the appendix is about the paper's text; `how_to_read` states no sentence Section 9 states | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict`; the driver's read |
| R-3 | Nothing cut is lost: the L16 clause is in the queue; the cut text is in git | the queue file; `git show c89843a:paper/supporting_material.ipynb` |
| R-4 | The derivation chain and proof map unchanged | `uv run python -m derivation.proofmap` identical to its output on `dev`; `git diff --stat dev` lists nothing under `derivation/` |
| R-5 | Register rows follow (ids append-only); lint, format, lock, vocabulary, suites, build, CI | `uv run pytest -q -m "not slow"` and the paper tests; `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `scripts/check_vocabulary.py` 0 new; the MyST build log clean; CI green |

## Definition of good

Appendix B is the proofs Section 6 points to, each a step table reached from its label, with the one paragraph a
reader of Sections 5 and 6 needs on the restart, stop and polish rules, and nothing about the paper.

## Definition of good enough

Every "Proof: Appendix B, Ln" in Section 6 still lands on its step table, B.2 says only what Sections 5 and 6 point
at, `how_to_read` states no sentence Section 9 states, the Job block is gone from the rendered page, R-1 to R-5 met,
the appendix soft-confirmed.

## Definition of done

Good enough met, no open item remaining unresolved, landed on `dev` after WP57a, the soft-confirm recorded in
`WP57-decisions.md`.

## Agent's defaults

- B.2 about 120 words, the map's estimate, not a cap; a ledger row records the cut.
- A register row whose sentence goes is retired with the reason, never deleted.
- One commit on `wp57ab` after WP57a's, merged to `dev` by the driver.

## Open decisions

None for him. The driver's calls (`WP57-decisions.md`) are recorded.
