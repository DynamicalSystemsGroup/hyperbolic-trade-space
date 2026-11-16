# WP57c — Scope of work: Appendices C and D

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy; runs after WP56 lands, one unit, one writer on the supporting notebook |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `wp57c` in its own worktree off `dev` at WP56's landing |
| **Approval record** | The driver's approval under his mandate, quoted in `WP57-decisions.md` |
| **Acceptance record** | The driver's soft-confirm of each appendix on screenshots; his read afterwards |

## Purpose

His direction (`WP57-decisions.md`): the appendices "need to be tightened down ... primarily as one step deeper where
needed. do not metanarrate. the appendices job IS NOT to opine on the text of the paper." The parent's brief for C and
D: "C: what Section 7 narrates, one step deeper (the SysML v2 model is the model; the appendix refers to it). D: the
tables Section 8 reads and no more; of 19 subsections, each kept, shortened, moved to the repository or cut by the
map." Dispositions: `WP57-rounds/map.md`, section 1, every C and D row marked "pending WP56" re-read first. What WP56
moved out of Sections 7 to 9 for these appendices: `WP56-rounds/moved-to-appendix.md`.

## Goals

- G1. **The pending rows re-read at WP56's landing.** The citation column of every C and D row refreshed from the
  paper as landed (typed pointers now: C, C.1, C.4, C.6, C.7; D, D.4, D.5, D.8, D.10, D.11, D.13, D.14, D.15, D.16,
  D.19; generated: C.2, C.5, C.7, C.8, D.3, D.5, D.8, D.11, D.14, D.15, D.17, D.19), each provisional disposition
  confirmed or changed with the reason, before any edit. A subsection no sentence cites is kept only as the step
  deeper a named sentence needs (C.3 for Section 7's feasibility sentence; C.8 for Table 2's cost limits and
  Section 9's "a lower bound on a full costing"), else it moves or goes.
- G2. **WP56's moved material landed.** Each line of `WP56-rounds/moved-to-appendix.md` landed where it names, or
  marked with why not; the generated calls it lists moved into D.3, D.5, D.10, D.15 and D.19 beside what those
  subsections print; `tension_sentence` reworded without stakeholders or retired with its rows; D.19's rule
  paragraph rewritten to Section 8's four rules (sponsor: least fleet cost; manufacturer: least unit cost; operator:
  largest coverage probability; between sponsor and operator: the smallest larger shortfall on the two, each scaled
  from its best to its worst on the shortlist), with the coverage column and its nondominated mark in the shortlist
  table. Until this lands D.19 contradicts Section 8; it is the unit's first commit.
- G3. **Appendix C by the map.** The opening cell and the Job block cut (C032's sentence left Section 7 with WP56:
  re-anchor to Section 1 or retire; C147 retires). C.5 shortened to one five-row preview and the pairs at
  |Spearman| at least 0.5 with the one-axis sentence; the stock preview and the full pair table move to
  `paper/supplement/metric-associations.md`, cited in one line. C.8 shortened to the cost-model paragraph; the
  "What the case leaves out" paragraph and the omission items move to `examples/adcs/case-model.md`, cited in one
  line, the mirror `work-packages/WP30-rounds/appendix-c-leaves-out.md` and its test clause following; the
  launch-slot item stays only if a paper sentence still needs it. C.1, C.2, C.3, C.4, C.6, C.7 kept, the citing or
  step-deeper sentence of each named in the review.
- G4. **Appendix D by the map.** The Job block cut. D.1 and D.6 to `paper/supplement/`. D.2's table and D.12's
  table merged into D.8 (one table per regime), D.12's three paragraphs to `docs/user-guide/termination.md`. D.7
  merged into D.17. The narrating openers of D.13, D.15, D.18 and D.19 cut or stated directly. D.17's prose
  shortened to the thresholds' values, the price's definition and the design sets' rule. D.9 made reachable from the
  nondominated sentence (Agent's defaults). Corollary 1 gains its one-line pointer to D.18 (the main-text edit the
  driver's call 1 allows). No D subsection repeats another's columns.
- G5. **The record follows.** Register rows (ids from C988, append-only; a row whose sentence goes is retired with
  the reason), the paper tests, `paper/length_ledger.toml` (a cut row per subsection), both baselines;
  `review/open-questions.md` extended with anything found.

## Non-goals

- Appendices A, B, E, F, G, H (WP57a, b, d). Re-lettering (WP57e). Main-text edits beyond Corollary 1's pointer and
  the D.9 default. The decision's rules, picks and numbers (WP56's). The data of record, the lemma scripts, the
  SysML v2 model files (the stale pass rate in `cubesat.sysml`'s header is OQ-12, its hash pinned). Opinions on the
  paper's text inside an appendix.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `paper/supporting_material.ipynb`, the C and D cells; `paper/paper.ipynb` for the Corollary 1 pointer (and D.9's, if that default is taken); both re-executed | G2 to G4 |
| D-2 | Generators: `paper/generate_model.py` (`metric_table`, `metric_associations`), `paper/generate_results.py` (`termination_records` absorbing `k_diagnostics` and `conditioning_diagnostic`; `design_sets_comparison` absorbing the candidates' sentence), `paper/generate_findings.py` (`tension_sentence`, the moved calls' homes), `paper/generate_supplement.py` | G2 to G4 |
| D-3 | `paper/supplement/{metric-associations,temperature-sweep,refits-by-category}.md` (generated, with staleness tests); `examples/adcs/case-model.md`; `docs/user-guide/termination.md` | G3, G4 |
| D-4 | `claims_register.toml`, `tests/test_paper.py`, `paper/length_ledger.toml`, `scripts/residuals_baseline.json`, `scripts/vocabulary_baseline.toml`; `WP56-rounds/moved-to-appendix.md` with each line marked landed or not | G2, G5 |
| D-5 | `work-packages/WP57c-review.md`: the refreshed citation table (G1), before-and-after words per subsection by `map_counts.py`, the checks with their outputs, screenshots of the rendered top of C, C.5, C.8, the top of D, D.8, D.17 and D.19 at desktop width | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every C and D subsection kept is cited by a sentence of Sections 2 to 9 or is the step deeper a named sentence needs; every pointer resolves | the G1 table; `uv run pytest tests/test_paper.py -k references_resolve` |
| R-2 | No sentence in C or D is about the paper's text; no Job block renders | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` (the supporting notebook at or below its baseline on every count); the driver's read |
| R-3 | Nothing cut is lost: moved tables and paragraphs at their named paths, each cited from the appendix in one line; the rest in git | the review's disposition column with paths; `git show 23f7e17:paper/supporting_material.ipynb` |
| R-4 | D.19 states Section 8's rules and no other; the shortlist table carries the coverage column | a test that the four rule names of Table 3 appear in D.19's paragraph and the old rules' words ("pointing error" as a rule, "balanced between the terms") do not |
| R-5 | The derivation chain and proof map unchanged; the data of record unchanged | `uv run python -m derivation.proofmap` identical to `dev`; `git diff --stat dev -- derivation examples/adcs/data` empty |
| R-6 | Lint, format, lock, vocabulary, the fast suite, the slow paper tests, the build, CI | `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`; `scripts/check_vocabulary.py` 0 new; `uv run pytest -q -m "not slow"`; `uv run pytest -q -m slow tests/test_paper.py`; the MyST build log clean; CI green on both platforms |

## Definition of good

Appendix C is the one step deeper under Section 7's narration of the SysML v2 model and the data; Appendix D is the
tables Section 8 reads, each once, with nothing about the paper and nothing no sentence needs.

## Definition of good enough

Every C and D subsection kept has its citing or step-deeper sentence in the G1 table; the moved tables are in
`paper/supplement/` and the case page with one citing line each; D.19 states Section 8's rules; no D subsection
repeats another's columns; every line of `moved-to-appendix.md` is marked; R-1 to R-6 met; both appendices
soft-confirmed on screenshots.

## Definition of done

Good enough met, no open item remaining unresolved, landed on `dev`, the soft-confirm recorded in `WP57-decisions.md`.

## Agent's defaults

- The map's word estimates (C about 790 to 270 typed words, D about 1,620 to 1,000) are expectations, not caps; a
  ledger row records each cut.
- D.9: its four-row table merges into D.11 beside the stability of the counts the nondominated sentence already cites,
  or the generated sentence's parenthetical names D.9 for the counts; the unit picks on the rendered result and says
  which.
- `tension_sentence` is retired unless a D.19 sentence needs the pair's tension; its register rows (C797, C798) go
  with it or re-anchor.
- Supplement files are generated by `generate_supplement.py` with a staleness test each (the WP57a pattern). The case
  page's "What the case leaves out" takes C.8's items in the page's own words.
- Two commits on `wp57c`: D.19 and the moved material first, then the rest of C and D; merged to `dev` by the driver
  after the soft-confirm.
- The unit's cold read of each rendered appendix at desktop width goes in the review; the driver reads the captures.

## Open decisions

None for him. The driver's calls (`WP57-decisions.md`, the map's six items) are recorded.
