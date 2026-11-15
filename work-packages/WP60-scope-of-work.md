# WP60 — Scope of work: the three example pages (perovskite, amniote, Broadbalk wheat)

| | |
|---|---|
| **Status** | DRAFT for the driver's approval as his proxy (autonomous mode); executes in parallel with the paper packages (docs and examples only) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; `docs/examples/` and `examples/<case>/`, on a branch `wp60` in its own worktree |
| **Approval record** | The driver's approval under his mandate, quoted in `WP60-decisions.md` |
| **Acceptance record** | The driver's soft-confirm of each page on screenshots; his read afterwards |

## Purpose

His purpose for the cases (`WP44-decisions.md`): "truly show the method works, for that we need a variety of unrelated
cases", "double duty by populating an examples section of the documentation and help us harden our understanding of
our own method". His takeaway from WP59 (`WP59-decisions.md`): "'bigger is better' is a normative judgement which is
why the feature engineering and conditioning have to be part of using the method, rather than predefined by the
method itself". The pages are written from the WP45 records and the WP59 readout, for a user with a table of their
own who is not a machine-learning engineer.

## Goals

- G1. **Three pages a reader can run from the docs alone** (WP45 G1): each states the dataset, its licence and source
  (DOI), the fetch step, the configuration and attribute columns, the conditioning rule with each orientation and its
  reason, the fits at K = 1 and 2 with their temperatures, the reading against the field's named trade-off, and what
  the example cannot show, once.
- G2. **Each page shows what WP59 says to show:** the contending set and the association signs with each exponent's
  range across the scaler ladder and the extremes rule, not one exponent; the orientation stated with its reason
  (the amniote page opens on it); the extremes rule (perovskite); the derived metrics set aside and why (PCE; annual
  fecundity; biomass and the harvest index); the covariate's three treatments (amniote); why PCA before the fit is
  not used at two metrics (wheat). The readout's checks appear as the calls a reader runs on their own table.
- G3. **Figures that carry the page on a skim:** per page at most two, built from the record's script by the docs'
  figure builder (a `{.runnable}` block directly above, light and dark, a numbered caption in the docsite's sequence,
  the eight-figure budget respected: count first; if the budget binds, the ternary for the three-metric cases and the
  log plane for wheat); each through the figure loop at the first three depths with screenshots.
- G4. **The examples index routes to them** (one row each under the existing examples page, after the synthetic
  case), and the breadth record `examples-coverage.md` takes each case's row from its record.
- G5. **Backed:** a claims row for every sentence that states a number or a fact of the data; every citation in
  `docs/references.bib` with a resolved DOI (the WP45 keys already there).

## Non-goals

- Any change to the paper. New fits beyond the records and the ladders (the pages report; they do not explore).
  Redistributing data beyond the records' rules. A battery or other fourth case.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `docs/examples/perovskite.md`, `amniote.md`, `wheat.md`, each under a stated word budget in `tests/test_site.py` (default 700 each) with the figures' runnable blocks | G1 to G3 |
| D-2 | The figures, built by `scripts/build_figures.py` from the pages' blocks, with the screenshots of the loop in `WP60-rounds/` | G3 |
| D-3 | `docs/examples.md` rows and `mkdocs.yml` navigation; `examples-coverage.md` rows | G4 |
| D-4 | Register rows; references checked; `WP60-review.md` with the checks and a reviewer's run of each page's blocks from a clean cache | G5, acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every number on a page comes from `results.json` or `variants.json` of its case, named | the review's trace per number |
| R-2 | The orientation of every time or cost metric is stated with its reason on the page that uses it | a read; the amniote page's first paragraph |
| R-3 | No weight stated as a result; ranges only | `grep` for single exponents in prose against the register rows |
| R-4 | The docs' figure rules and budget (`tests/test_site.py`); light and dark images differ; alt text names what is shown | the slow figure test |
| R-5 | The register's rules for every section applied to the pages (no metanarration, one point per place, the glossary's words, "dataset" where his word applies to a user's table) | `scripts/check_residuals.py`, `scripts/check_vocabulary.py`, the driver's read on screenshots |
| R-6 | Lint, format, lock, the site, docs, register and references tests, CI | as WP53 |

## Definition of good

A decision analyst with a table of their own reads one page and knows what to state, what to test and what a stable
reading looks like, and can rerun the page.

## Definition of good enough

R-1 to R-6 met; the driver's soft-confirm of each page on screenshots at the three depths; his later edits light.

## Definition of done

Good enough met, landed on `dev`, his read recorded in `WP60-decisions.md`.

## Open decisions

None for him.

## Agent's defaults

- One unit per page, in parallel, each in its own worktree on `wp60-<case>`, touching only its page, its figure block
  and its register rows; the driver merges the three and edits the index and the coverage record.
- Figures: perovskite, the ternary of Voc, Jsc, FF with the three terms' regions; amniote, the ternary of longevity,
  earliness and litters per year at the fit's exponents (litter size named in prose); wheat, the log plane of grain
  against straw with the fitted line and the band. If the docs' eight-figure budget binds, the wheat figure goes
  first.
- Page budgets 700 words each; the examples index row 40 words each.
