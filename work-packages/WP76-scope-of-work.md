# WP76 — Scope of work: the iron-triangle example (Kitchenham-CSC software projects)

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below. Nothing in this package is executed before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; branch `claude/iron-triangle-example-12a7c6` (from `dev` 814853ad, the 0.1 candidate, in its own worktree); nothing on `dev` or `main`; the branch is merged into `dev` after 0.1 is out and after his review |
| **Approval record** | His word in chat, quoted verbatim in `work-packages/WP76-decisions.md` (the project's convention: verbal approvals for now) |
| **Acceptance record** | His word in chat after the technical verification and his author review of the interpretation (his memo, "Boundaries and integration"), quoted verbatim in `work-packages/WP76-decisions.md` |

## Purpose

His memo (2026-11-17, verbatim in `WP76-decisions.md`): "Produce one reproducible public example answering: Among
comparable projects, did greater delivered scope accompany less schedule and budget slack, and did those two slacks
move together?" The example "offers a familiar entry point for project-management readers and demonstrates an
important distinction: metrics can jointly constrain a frontier while some move together and others trade against one
another." It is built from the WP70 research packet (delivered at 4bf40d31, preserved at 4f81a4ea), whose findings on
141 Kitchenham-CSC projects "are findings to reproduce and assess, not predetermined acceptance outcomes", and it
"should not become a dependency for the first release". Developing it against the 0.1 candidate "will also test how
readily a contributor can produce a defensible new case."

## Goals

His five work items, in his words.

- G1. **Establish reproducibility.** "Verify the source, licence, checksum, exclusions and existing scripts against the
  current package. Preserve a permitted data artifact or reliable retrieval procedure. Record the exact package version
  and Git SHA used."
- G2. **Define the case in SysML v2.** "Record attributes, units, effort as the budget proxy, metric orientations,
  positivity transformations, conditioning alternatives and the frontier-band rule in the system model. The example
  page should explain their decision relevance and link to the definitions."
- G3. **Reproduce and challenge the result.** "Reproduce the one-term baseline and assess the previously investigated
  two-term alternative. Check sensitivity to plausible conditioning choices, frontier-band choices and influential
  observations. Retain the project-type and client subset contrasts."
- G4. **Present both kinds of relationship.** "Use signed near-frontier associations and scatter plots to distinguish
  shared movement from substitution. Present fitted frontier participation separately. Use a ternary only if it adds a
  clear, defensible reading."
- G5. **Publish one example page.** "Follow the repository's established example structure: management question, data,
  analysis, findings, practical interpretation and limitations. Keep detailed checks in analysis records and
  assumptions in the SysML v2 system model."

## Non-goals

His boundaries, and the standing rules that bind every package.

- No new estimator, no conic-expression implementation, no additional dataset, no broader research programme (his
  memo: "This package requires no new estimator, conic-expression implementation, additional dataset or broader
  research programme").
- Completing the conic-expression research (WP75, running in parallel) is not an acceptance condition; the research
  note of D-5 names what this case could test and defines nothing.
- No claim that the data establish the 3 + m extension: "Because the dataset has no quality measurements, it does not
  empirically establish the proposed 3 + m extension." The 3 + m idea does not appear on the public page at all (OD1,
  "Not on the page"): the page's limitations say only that the table carries no quality measure, so the case says
  nothing about quality; the framing stays in the research note (D-5) and the WP70 record.
- Nothing for 0.1: no commit on `dev` or `main`, no pull request, no tag, no deployment; the branch is the delivery.
- Package defects met on the way are recorded, not fixed on this branch ("Record package defects separately and
  resolve any blocking dependency explicitly"): a section of `WP76-decisions.md`, each with the evidence and whether it
  blocks.
- No new dependency and no change to `pyproject.toml` or `uv.lock`; no change to `src/` (the package is the 0.1
  candidate the example is developed against).
- No crypto-economic material on any public surface; no AI attribution anywhere.
- No change to the three existing example pages, the paper, or the user guide, beyond the one sentence on the Examples
  index that routes to the new page *(default)*.

## Deliverables

His five deliverables, with their places in the repository *(the paths are defaults)*.

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | One public example page with generated figures: `docs/examples/kitchenham.md`, in the five-part arc of `notes/examples-template.md`, with its `{.runnable}` blocks building its figures through `scripts/build_figures.py`; its row in `mkdocs.yml`, the one-sentence route on `docs/examples.md`, its word budget in `tests/test_site.py`, and interface-contract amendment 30 adding the page to `docs.pages` and `presentation_pages` | G4, G5 |
| D-2 | A SysML v2 system model defining the case: `examples/kitchenham/kitchenham.sysml`, one package, loaded strictly by the opensysml client; attributes with units, effort as the budget proxy, orientations, the positivity shift, the conditioning alternatives, the exclusion rule and the frontier-band rule as named elements with a `doc` rationale each | G2 |
| D-3 | Reproducible analysis code and data provenance under `examples/kitchenham/`: `manifest.toml` (source, DOI, licence, size, md5, sha256, exclusions, the retrieval command), `run.py` (fetch with the hash check, derive, condition, fit, write `results.json`) and `variants.py` (the sensitivity ladder, the band ladder, the influence study, the subsets; writes `variants.json`); the derived table `derived/projects.csv` with `LICENCE-DATA.txt` beside it (CC BY 4.0 with attribution, as the wheat example does); `results.json` records `hyperbolic_trade_space.__version__` and the Git SHA of the run; `docs/references.bib` gains the Kitchenham et al. (2002) entry with its verification | G1, G3 |
| D-4 | A compact verification record covering sensitivity and reproduction: `tests/data/wp76/kitchenham/verification-record.md` (the WP45 records' place since WP73), with the reproduction (the source checks, the re-run's agreement with the committed results), the baseline, the two-term assessment, the conditioning ladder, the band ladder, the influence study, the subset contrasts, the figure loop's cold reads and captures, and the project-management cold read; the record tests `tests/test_wp76_kitchenham.py` that read the page's and the record's numbers from `results.json` and `variants.json`; the claims rows in `claims_register.toml`; the case's row in `work-packages/examples-coverage.md` | G1, G3, G4 |
| D-5 | A short research note identifying what this case could test in a future conic-expression generalization: `notes/directions/wp76-iron-triangle-conic.md`, with its row in `notes/directions/README.md`; not public prose | (his deliverable; frames nothing on the page) |
| D-6 | The records: `work-packages/WP76-decisions.md` (his memo, his approval, the decisions, the package defects, his acceptance), the WP76 row in `work-packages/INDEX.md`, and `work-packages/WP76-rounds/` holding the captures the record names | the gates |

## Requirements

His acceptance criteria are R-1 to R-6; R-7 to R-12 are the repository's standing checks on anything public.

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | "A clean run reproduces the published tables and figures." | With `results.json` and `variants.json` deleted, `uv run python examples/kitchenham/run.py --fetch` and `uv run python examples/kitchenham/variants.py` rewrite them; `git diff --exit-code examples/kitchenham/` is clean on the same machine, and the record tests, which compare every number the page and the record quote to the regenerated files at the page's precision, pass (`uv run pytest -q tests/test_wp76_kitchenham.py`); `uv run python scripts/build_figures.py` builds the page's figures from its blocks, and the slow figure test passes (`uv run pytest -q tests/test_site.py -k figure`) |
| R-2 | "The narrative distinguishes frontier participation, positive association and negative association." | The page carries one sentence for each: which metrics are in the contending set (participation), which pair's near-frontier association is positive (shared movement), which pairs' are negative (substitution); each is a register row backed by `results.json`; the project-management cold read of R-5 names the three apart |
| R-3 | "The headline survives the stated sensitivity checks, or is narrowed to match their results." | The verification record's tables (conditioning ladder, band ladder, influence study) each say which rows hold the sign pattern of the headline; the page's statement of the headline is scoped to exactly those rows (a register row quoting the counts); the record test asserts the sign pattern on the rows the page says it holds on and nothing wider |
| R-4 | "Subset differences and influential observations are reported openly." | The page names each subset (project type, client) with its row count and what changed in it; the record's influence table lists every observation whose removal changes a sign of the near-frontier association or moves an exponent by more than the stated amount, and the page says how many there are and what they do; the record test reads the counts |
| R-5 | "A project-management reader can identify what was measured, what was found and what decisions the evidence cannot support." | A context-gapped reader with no repository access, in the persona of a project manager (a PMP), is given the rendered page alone and answers the three questions in one sentence each; the answers are quoted verbatim in the record; a mismatch sends the page back; his own read at acceptance is the gate |
| R-6 | "Claims remain observational and portfolio-specific. Because the dataset has no quality measurements, it does not empirically establish the proposed 3 + m extension." | Every kind-R claim on the page is a register row backed by `results.json` or `variants.json` (`uv run pytest -q tests/test_claims_register.py`); a read of the page for causal or general wording ("causes", "shows that projects", "in general") finds none, and every finding names the portfolio; no sentence on the page says the data establish, test or support quality measures as further sides |
| R-7 | The provenance is complete (G1) | `manifest.toml` names source, DOI, licence, size, md5 and sha256, and the fetch verifies them (`tests/test_wp76_kitchenham.py::test_manifest_names_source_doi_licence`, `::test_verify_fails_loudly` reuse the WP45 pattern); the exclusions (rows dropped and the rule) are stated in the manifest, the model and the page and agree; `results.json` carries `package_version` equal to `hyperbolic_trade_space.__version__` and `git_sha` equal to the commit of the run |
| R-8 | The model is the statement of record (G2) | `examples/kitchenham/kitchenham.sysml` loads strictly (`load_from_content(..., strict=True)`); a test reads from the model, through the opensysml client, every constant the analysis uses (the orientations, the shift, the exclusion rule's bound, the temperature target, the band rule's count, the alternatives' shifts and caps) and asserts the analysis module's values equal them; every constant in the model has a `doc` rationale (the cubesat model's test, applied to this file); the page links to the model |
| R-9 | The two-term alternative is assessed, not assumed (G3) | `results.json` holds the K = 2 fit at the K = 1 temperature (exponents per term, term shares, mean slack against K = 1, status, and the per-term contending sets where the guard of ten rows is met); the page states what the second term holds; the record test pins the shares |
| R-10 | The figures earn their place (G4) | Each figure through the figure loop of `notes/figure-review.md` (intent written first; two cold reads; the sentence test; ink as data; legible at the column width in light and dark); the reads and the captures in the record; a ternary appears only if the loop finds a reading the other figures do not carry; the figure count stays within `MAX_FIGURES` (raised from 10 to 12 in `scripts/build_figures.py` and `tests/test_site.py` *(default)*); figures numbered in navigation order (`uv run pytest -q tests/test_site.py -k "figure"`) |
| R-11 | The page is in the established structure and within budget (G5) | The five parts of `notes/examples-template.md` in order, headings in the page's words; at most 700 prose words (`uv run pytest -q tests/test_site.py -k budget`); the attributes as a text block; glossary links at first use; `uv run python scripts/check_vocabulary.py` reports no new violation; `uv run python scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` reports no rise (metanarration among its counts); the page looked at as rendered (`uv run mkdocs build --strict` after `build_generated.py`, `build_figures.py` and `build_site_figures.py`; served and captured at desktop width and 375 px, light and dark; the captures in `WP76-rounds/`) |
| R-12 | The checks are green at the branch's head | `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `uv run pytest -q -m "not slow and not paper"`; `uv run pytest -q tests/test_claims_register.py tests/test_site.py tests/test_interface_contract.py tests/test_references.py tests/test_index.py tests/test_docs.py`; `grep -rn "Co-Authored-By\|Generated with" examples/kitchenham docs/examples/kitchenham.md notes/directions/wp76* tests/data/wp76 work-packages/WP76*` finds nothing; `git diff --stat dev..HEAD` names only the paths of D-1 to D-6 and the files their defaults name |

## Definition of good

A project manager reads the page and takes away the distinction his memo names: three metrics bound one frontier, two
of them moved together there and the third traded against both; and knows what the evidence cannot decide. The
headline is no wider than the sensitivity evidence under it. A contributor with a table of their own can read the
page, the model and the record and produce a defensible new case the same way, which is the test his memo sets for the
package.

## Definition of good enough

- R-1 to R-12 met on one commit of the branch, with the evidence per requirement in the verification record.
- The project-management cold read's three answers match the page.
- The page looked at as rendered, with the captures in `WP76-rounds/`.
- Every package defect met on the way recorded in `WP76-decisions.md` with its evidence.
- A message to him naming the branch, the page, the record and what waits on the merge of 0.1.

## Definition of done

Good enough is met, **no open item remains unresolved**, and the supervisor has accepted the work by the acceptance
record above.

## Agent's defaults

- **Number and branch.** The package is WP76 (WP75 is the parallel scoping spike on branch `wp75`); the work stays on
  `claude/iron-triangle-example-12a7c6`, reset onto `dev` 814853ad (the 0.1 candidate) before any commit; its row is
  added to `work-packages/INDEX.md` as in flight, and WP75's row lands with its own branch.
- **Names.** Case folder `examples/kitchenham/`, page `docs/examples/kitchenham.md`, navigation title "Software
  projects (Kitchenham-CSC)", page title "Kitchenham-CSC software projects: scope against slack"; figure names
  `kitchenham-pairs` and `kitchenham-participation`; the record under `tests/data/wp76/kitchenham/`; the note
  `notes/directions/wp76-iron-triangle-conic.md`; the test file `tests/test_wp76_kitchenham.py`.
- **The data artefact.** The licence (CC BY 4.0) permits a derived table, so `derived/projects.csv` (141 rows: project
  id, type, client, the plans, the actuals, the three attributes) is committed with `LICENCE-DATA.txt`, as the wheat
  example does; the source file of record is fetched into the git-ignored `examples/kitchenham/data/` by
  `run.py --fetch` and checked against the manifest; the page's runnable block reads the committed derived table, so
  the docs tests run offline.
- **The scripts.** `run.py` and `variants.py` are new files written to the `examples/<case>/` pattern (`fitkit`,
  `variantkit`), carrying over the derivation and conditioning of `git show 4f81a4ea:work-packages/WP70-rounds/case/kitchenham.py`
  and citing that hash; the WP70 scripts are not copied into the tree.
- **The conditioning ladder.** The WP70 rungs: the primary (share of plan, shift 10, standard scaler of the log),
  robust scaler, no scaler, shift 20, shift 40, cap at 3 with shift 3, plan over actual with no shift; each a one-change
  variant recorded with its rule, as `variantkit` does.
- **The band ladder.** The near-frontier band at `1 / tau`, and at the smallest band holding 10, 15, 20 and 25 rows,
  with the association read at each; the primary reading uses the band that holds 15 rows when `1 / tau` holds fewer
  (the WP70 rule), stated in the model.
- **The influence study.** Leave-one-out over all rows for the K = 1 fit and the near-frontier association, reporting
  the rows whose removal changes a sign of the association or moves an exponent by 0.05 or more; plus the named
  extremes (the largest project by function points, the worst overruns) removed one at a time.
- **The two-term alternative.** K = 2 at the K = 1 temperature with five restarts and seed 0, as the other example
  pages fit it.
- **Figures.** Two, built by the page's blocks: the three pairwise scatter plots of the conditioned log-metrics with
  the near-frontier projects marked and each pair's signed association in its title (shared movement against
  substitution); and the participation figure, each metric's K = 1 exponent across the conditioning ladder with the
  contending set marked (participation apart from association). The ternary is not planned; the figure loop may add
  it under R-10. The site's figure cap rises from 10 to 12.
- **The headline.** Stated on the page only as the sensitivity evidence allows (R-3); the record test pins its scope.
- **Budgets.** The page at most 700 prose words; `TOTAL_BUDGET` in `tests/test_site.py` rises by 700 plus the route
  sentence's words on `docs/examples.md`; the index page's sentence becomes "Four public datasets".
- **The cold reads.** The figure loop's readers are fresh-context subagents given the image alone, then the caption;
  the project-management reader of R-5 is a fresh-context subagent given the rendered page, in a PMP persona, with no
  repository access; answers quoted verbatim.
- **The verification record** follows the WP45 records' sections (the coverage row, the source and reproduction, the
  counts and rule, the fit and the verdict, the limits, what it changes for the method), plus the sensitivity, band,
  influence and subset tables, the figure loop and the cold read.
- **The interface contract.** Amendment 30 (version 30): the page added to `docs.pages` and `presentation_pages`, as
  amendment 28 did for the three example pages; nothing else pinned.
- **The bibliography.** One entry, `kitchenham2002empirical` (JSS 64(1), doi:10.1016/S0164-1212(02)00021-3), with a
  `verified` field recording the Crossref read and the date; the Zenodo record is cited by DOI in the manifest and the
  page's first paragraph, as the other pages cite their data DOIs.
- **The changelog** is untouched: the next release's entry is written by that release's package.
- **Package defects** go in a section of `WP76-decisions.md` with the evidence, starting from WP70's three (the
  ternary's region label reads the two largest exponents as trading where their association is positive;
  `trade_off_report` raises when fewer than ten rows fall inside `1 / tau`; the `tau = inf` contending set includes a
  planted non-participant); any new one is added there and not fixed here.
- **The research note** is short (a page), names what this case could test under a conic-expression generalisation
  (the shift as an affine conditioning of the slack; the two slacks' shared movement as a candidate shared level; what
  a 3 + m table would need), cites WP75's readout where it exists at landing and defines nothing itself.
- **Captures** are kept as PNG tops under `work-packages/WP76-rounds/captures/` and named in the record; the folder
  follows the rounds protocol at landing.

## Open decisions (for the supervisor)

None. Every item was resolved through the decision loop (2 decided, 0 deferred, 0 raised; `WP76-decisions.md`, "Scope
gate"). OD1: the 3 + m idea does not appear on the public page ("Not on the page"); OD2: the Agent's defaults approved
as one item ("Approve the list").
