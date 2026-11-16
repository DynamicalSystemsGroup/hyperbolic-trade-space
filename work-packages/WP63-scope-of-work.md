# WP63 — Scope of work: the examples with an arc (a spike: a template and the pages redrafted to it)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy on his direction of 2026-11-16 (quoted in `WP63-decisions.md`); a spike, stage 1 of the lifecycle; its drafts go to his read |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `dev`; the docsite's example pages `docs/examples.md`, `docs/examples/{perovskite,amniote,wheat}.md`; a template under `notes/` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP63-decisions.md` |
| **Acceptance record** | The driver's soft-confirm on captures of the rendered pages against this scope; his read afterwards |

## Purpose

His direction (2026-11-16, `WP63-decisions.md`): the example pages "did their job of showing the solver fits trades but
they are hard to understand for a reader and they offer no intuition"; each needs "a short prose summary of the research
or application the data was drawn from, a data dictionary for the data used, a short explanation in scientific or
engineering terms of the purpose of the analysis (avoiding prebaking the conclusion of the analysis) then the analysis
then the interpretation", "as concise as possible" and following "an arc the reader can interpret"; "rigor and
interpretability are part of our story"; the data, code and plots that demonstrate the method stay; no metanarration;
"maybe a template for examples would help".

## Goals

- G1. **A template for example pages**, the arc written once: (1) the research or application the data was drawn from,
  in a short paragraph; (2) the data dictionary: each attribute used, its meaning, unit, source column, orientation, the
  rows kept and the rule that dropped the rest; (3) the purpose of the analysis in the domain's scientific or
  engineering terms, stated as a question the analysis can answer either way, never as its conclusion; (4) the
  analysis: the conditioning, the fit, the code and the plots as they are; (5) the interpretation: what the result
  means in the domain's terms, and what the example cannot show. Each part says what it must contain, what it must
  not, and a length a reader will take.
- G2. **The three dataset pages redrafted to the template** (perovskite, amniote, wheat), every code block, plot and
  generated number kept, the existing sections folded into the arc.
- G3. **The cubesat example page (`docs/examples.md`) redrafted to the same arc**, with the model's page and the paper
  as its sources for part (1) and the thirteen metrics and the configuration variables as its data dictionary.
- G4. **A readout**: what each page did not do before and does now, in one line each; the calls that are his.

## Non-goals

No change to any fit, dataset, loader, conditioning rule, figure, number or code block; no new figure; no claim the
results do not back; no caveat added as a fix; no change to the paper or the user guide; no page outside the four named.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `notes/examples-template.md`: the template of G1 | G1 |
| D-2 | The four pages redrafted on branch `wp63`, one commit | G2, G3 |
| D-3 | `work-packages/WP63-readout.md` with captures under `work-packages/WP63-rounds/` of each page as rendered at 1,280 px, and the cold reads of R-5 | G4 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every number on a page stays backed by its register comment and results file; the record tests pass | `uv run pytest -q tests/test_wp45_examples.py tests/test_site.py tests/test_docs.py` |
| R-2 | The pages build and the runnable blocks execute; figure numbers run one to n in navigation order | `uv run mkdocs build -q`; the figure-numbering test in `tests/test_site.py` |
| R-3 | No metanarration, no forward reference, no sentence that states the conclusion before the analysis | `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` shows no new rise on the four pages; a read |
| R-4 | Vocabulary from `glossary.yaml`; one object one name | `uv run python scripts/check_vocabulary.py` 0 new |
| R-5 | A cold reader per page, given only the rendered page, states in one sentence each what the data is, why the analysis was done and what it found, and the three match the page's intent | the readout's cold-read table, one reader per page from the grid's P3 or P4 |
| R-6 | Lint and format; no attribution line; nothing outside the named files and the readout's folder changes | `uv run ruff check .`; `uv run ruff format --check .`; `git diff --stat dev` |

## Definition of good

A cold reader of any example page knows where the data came from, what each column means, what question the fit was
asked, and what the answer means in the field's terms, in the fewest words that carry the arc; the method is still what
the page shows.

## Definition of good enough

D-1 to D-3 delivered; R-1 to R-6 met; the driver's soft-confirm on the captures; the drafts landed on `dev` for his read.

## Definition of done

Good enough met, no open item, his read recorded in `WP63-decisions.md`.

## Open decisions

None for him before the drafts; the drafts and the template go to his read.

## Agent's defaults

- Headings say the thing in the page's words, not the template's part names ("Where the rows come from", "The
  attributes", "What the fit is asked", "The fit", "What the fit says", "What the example cannot show" are the kind).
- The data dictionary is a table; units and source columns from the manifests and loaders.
- Part (3) is one short paragraph; it names the pair or set the domain expects to trade without saying the fit found it.
- One unit on branch `wp63`, worktree prepared by the driver; captures by headless Playwright at 1,280 px; register ids,
  if any new backing row is needed, from C1051.
