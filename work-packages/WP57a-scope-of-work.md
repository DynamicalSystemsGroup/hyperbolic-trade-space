# WP57a — Scope of work: the front matter and Appendices A, F and G

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy; runs after WP55 lands, a then b, one unit, one writer on the supporting notebook |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `wp57ab` in its own worktree |
| **Approval record** | The driver's approval under his mandate, quoted in `WP57-decisions.md` |
| **Acceptance record** | The driver's soft-confirm of each appendix on screenshots; his read afterwards |

## Purpose

His direction (`WP57-decisions.md`): the appendices "need to be tightened down ... material that doesn't earn its
place in the appendices can still live [in the repository] ... primarily as one step deeper where needed. do not
metanarrate. the appendices job IS NOT to opine on the text of the paper." His WP38 words: "we
keep it in its yaml form for our own checking but we may want to drop it from the supporting materials ... i want to
keep traceability records and assessments without giving the feeling that no human validated the citations."

## Goals

- G1. **Front matter:** the companion paragraph cut; title and import cell stay. No longer tells the reader which
  appendix is for whom.
- G2. **Appendix A:** the Job block cut (no longer says what main text, appendix and repository each keep). `register_table` shortened to the entries the paper or the appendices use (62 of 72), the Layer column
  dropped. The four `defined_in` fields naming decision files point to the defining place in the paper or the package.
- G3. **Appendix F:** the Job block cut (no longer says what Section 11 and the repository keep); F.1 to F.4 kept.
- G4. **Appendix G:** the Job block cut (no longer argues with an objection or counts Section 2's words); the scope
  sentence queued for WP57d's assumptions section; the pointer cell to Appendix H cut; G.1 kept; G.2 moved to
  `paper/supplement/reading-pass.md`, written by `reading_pass_table` from the YAML, cited in one line at the end of
  G.1. G no longer prints a table about the paper's text inside the paper.
- G5. **Section 2 names Appendix G** in one sentence beside Table 1.

## Non-goals

- Any other appendix. Any lemma script or the derivation chain. Any main-text edit except G5's sentence. The rows of
  `prior_art.yaml` and `reading_pass.yaml`. Re-lettering (WP57e). Opinions on the paper's text.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/supporting_material.ipynb`: cells 0, 3, 89, 99, 100, 103, 104 and 105 edited or removed; re-executed | G1 to G4 |
| D-2 | `paper/generate_register.py`; `glossary.yaml` (`defined_in`) | G2 |
| D-3 | `paper/generate_supplement.py` (new), `paper/supplement/reading-pass.md`, the citing line in G.1 | G4 |
| D-4 | `paper/paper.ipynb`, cell `sec-prior-art`: the sentence naming Appendix G | G5 |
| D-5 | `work-packages/WP57-rounds/assumptions-queue.md`: G's scope sentence, for WP57d | G4 |
| D-6 | Register rows (C131, C161 retired or re-anchored; ids append-only); `tests/test_paper.py` (`test_reading_pass_table_is_in_appendix_g_and_current` becomes the supplement's staleness test); the length ledger; both baselines | R-5 |
| D-7 | `work-packages/WP57a-review.md`: before-and-after words per subsection by `map_counts.py`; screenshots of the rendered front matter, A, F, G and the Section 2 sentence | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every subsection kept is cited by a paper sentence or is its step deeper | `grep -c` of each kept anchor in `paper/paper.ipynb` |
| R-2 | No sentence in the four appendices is about the paper's text | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict`; the driver's read |
| R-3 | Nothing cut is lost: the supplement equals `reading_pass_table()` and G.1 cites it; the cut text is in git | the staleness test; `git show c89843a:paper/supporting_material.ipynb` |
| R-4 | The derivation chain and proof map unchanged | `uv run python -m derivation.proofmap` unchanged; `git diff --stat dev` lists nothing under `derivation/` |
| R-5 | Register rows follow (ids append-only); lint, format, lock, vocabulary, suites, build, CI | `uv run pytest -q -m "not slow"` and the paper tests; `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `scripts/check_vocabulary.py` 0 new; the MyST build log clean; CI green |

## Definition of good

Each of the four is the one step deeper its citing sentence needs, in the register of the main text, and nothing more.

## Definition of good enough

A's table lists only terms the paper uses, F has no preamble, G is the register with one line citing the reading pass,
no Job block or companion paragraph on the rendered page, Section 2's sentence present, the four `defined_in` fields
repointed, R-1 to R-5 met, each appendix soft-confirmed.

## Definition of done

Good enough met, no open item remaining unresolved, landed on `dev` after WP55, the soft-confirm recorded in
`WP57-decisions.md`.

## Agent's defaults

- `paper/generate_supplement.py` writes each supplement file from its generator function; a test compares file and
  output.
- The Section 2 sentence closes the paragraph introducing Table 1, under 25 words.
- The register filter counts uses by `scripts/check_vocabulary.py`'s rule. A fifth `defined_in` naming
  `WP23-decisions.md` is repointed if it renders.
- One commit per child on `wp57ab`, merged to `dev` by the driver.

## Open decisions

None for him. The driver's calls 2, 5 and 6 (`WP57-decisions.md`) are recorded.
