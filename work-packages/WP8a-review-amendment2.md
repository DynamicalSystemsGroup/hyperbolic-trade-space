# WP8a Amendment 2 — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP8a-scope-of-work.md`, "Amendment 2 (draft)" as modified by "Amendment 2: gate outcomes" (OD1 to OD5, G9 withdrawn, R-26 added) |
| **Approval verified** | `work-packages/WP8a-decisions.md`: "Approved" (mzargham, verbatim, 2026-11-08) for Amendment 2 and contract version 2; defaults "Approve the defaults as listed"; same quote in `WP14-decisions.md`, "Contract version 2". Verbal record. |
| **Work reviewed** | `dev` at 8f779d8, commits "WP8a: ..." since d7673c6 |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat after the second staged review and a green Pages dispatch build (pending, see below) |

Reviewer: fresh context, did not build the work. Nothing fixed. The only file written is this report. Other packages' files (`examples/adcs/`, `paper/`) are ignored.

## Checks run

| Check | Result |
|---|---|
| `uv run python scripts/stage_site.py` | built into `_stage/`; only INFO lines (see O-3) |
| `uv run mkdocs build --strict` | exit 0. **Caution (O-4):** run with its default `site_dir` it wipes the tracked root page `site/` (index.html, paper placeholder, image). I restored it with `git checkout -- site && git clean -fdq site`; the tree is clean apart from other packages' untracked files. Re-run with `-d <elsewhere>`: strict build passes. |
| `uv run pytest tests/test_site.py tests/test_build_generated.py tests/test_docs.py tests/test_narrative.py tests/test_paper_sources.py tests/test_interface_contract.py tests/test_references.py tests/test_notebook.py -q` | `232 passed, 1 skipped` (the first run showed failures only because of the `site/` wipe above; the rerun after restoring is green) |
| Runnable blocks | all 9 `{.runnable}` blocks executed by my own loop, exit 0; getting-started prints `trilemma [0 1 2] [0.3  0.37 0.33]`, matching the page's stated output |
| Word counts (prose, code excluded) | index 198/250, getting-started 229/400, overview 394/500, conditioning 564/700, fitting 428/800, tensions 445/700, chart 431/600, prediction 200/350, termination 611/600 with its table counted (the test excludes tables: passes), limitations 494/500, api 240/300, examples 310/400, theory 533/700, further-reading 188/300. Total 5,265 (cap 7,600). |
| Ruff | `ruff format --check .` clean; `ruff check .` 5 errors, all in `examples/adcs/experiments/cubesat_oracle.py` (another package, untracked) |
| Lock, attribution | `uv lock --check` ok; `git log d7673c6..HEAD` grep for co-author/generated lines: 0 |
| Browser (served `stage_site.py --serve --port 8791`, stopped afterwards) | root, a user-guide page (Tensions), Glossary, Theory viewed in the pane (about 660 px wide, a narrow layout, dark scheme): no horizontal overflow, MathJax rendered 17 containers on Theory. A separate 375 px emulation was not run (not checkable beyond the narrow pane). |
| Pages dispatch build | **pending**: cannot run until `pages.yml` is on `main`. |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-11 | met | 14 hand-written pages at the table's paths, within budget, nav in `mkdocs.yml` is Home, Getting started, User guide (8), API, API reference, Examples, Theory in brief, Glossary, Further reading. No Changelog and no generated Derivations/Verification (OD1, OD3). |
| D-12 | met | All six snapshots equal `git show d7673c6:docs/<page>` (diff per file: identical). `paper-sources/README.md` has the move table for every `method.md` section and every other page. |
| D-13 | met | `site/index.html` carries the paragraph under the figure (matches the default text), no `<script>`, thin; browser view confirms dark scheme. Text also states how the figure reads, as the supervisor asked. |
| D-14 | withdrawn | G9 withdrawn; no `paper_sections.toml` exists, none referenced. |
| D-15 | met | Contract v2 change-log row and manifest (`contract_version = 2`) agree; `test_interface_contract.py` passes; quote in `WP14-decisions.md`; no paper-anchors item, C-9 recorded as withdrawn. |
| D-16 | met | Repoints compared below. |
| D-17 | met | No changelog (OD3). `glossary.yaml` (37 entries) compiled to `docs/generated/glossary.md`. |
| D-18 | met | Moved pages, `overrides/` and the two generated pages absent from `docs/`; punch-list routes updated; decisions recorded. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-2' | met | `test_site.py` nav test passes; no `method.md` or `literature.md` under `docs/`. |
| R-3' | met | Math markers test passes; MathJax rendered on Theory in the browser. |
| R-4' | met | Strict build; citations render; further-reading bibliography test passes. |
| R-15 | met | Table above; total 5,265. |
| R-16 | met | Forbidden-content regex test passes; Theory has displayed formulas only (at most six). |
| R-17, G9 | withdrawn | No docs-to-paper citation anywhere in `docs/` (grep for "paper", "appendix", slugs). The only paper reference is Home's link to the project page. |
| R-18 | met | All 9 blocks run; five-line example is five code lines. |
| R-19 | met | Strict and staged builds pass; test suite resolves internal links. |
| R-20 | met | All ten register phrases present across the user pages (`grep` of the ten phrases lists theory, termination, chart, tensions); forbidden-phrase test passes. |
| R-21 | met | Six identical snapshots; `test_paper_sources.py` passes. |
| R-22 | met, partly browser-checked | See browser row. |
| R-23 | met | Contract test passes. |
| R-24 | met for 8a files | Files touched by "WP8a: " commits are all in the ownership table (tests repointed, `test_references.py` repointed). `src/`, `derivation/`, `pyproject.toml`, `uv.lock` untouched by WP8a (other packages changed them). |
| R-25 | not checkable by me | The supervisor's cold read. My read as a package user: install, first fit, tension report, termination record are all reachable and runnable from the docsite alone. |
| R-26 | met for pages and scripts, not met for the API reference | Grep over `docs/` (excluding `superpowers/`), `site/`, `scripts/`, `mkdocs.yml`, test route lists: no moved file names, routes, old anchors, Mathematics page, derivation or verification pages, world key. The built `_stage/docs/api-reference/` still carries lemma tags: see G-1. |

## Test repoints (weakening check)

- Method assertions (Map and territory exactly once, three-level headings, L12 to L14 cited, statuses/tolerances): removed from `test_docs.py` and present unchanged in `test_paper_sources.py` against the snapshots. Not weakened.
- `test_docs.py` register phrases still require all ten; the forbidden-phrase scan widened to docsite, snapshots and `glossary.yaml`. Lemma-tag/ledger-id range checks now run over every docsite page. The old "page cites a lemma/ledger id" assertion no longer applies to user pages, as the scope allows; it lives on the snapshots.
- `test_references.py`: `LIT` points at the snapshot of `literature.md`. Unchanged otherwise.
- `test_notebook.py`: unchanged, as the scope's table permits.

## Glossary (OD5)

37 `- **term**: short` lines equal the 37 `term`/`short` pairs of `glossary.yaml` exactly, no other text; the file is a build product of `scripts/build_generated.py`. No hand-written glossary text exists. `docs/generated/glossary.md` is tracked in git; see O-2.

## Gaps (open decisions)

| ID | Gap | Suggested disposition |
|---|---|---|
| G-1 | The API reference renders docstrings that cite "lemma L1 to L10", "assumption A4" and "spec section 4" (15 lemma tags, 3 assumption tags in the built page). With no derivation page on the docsite these are dangling references to content that is not there, which R-26 targets. The scope bars docstring edits. | Follow-up for the technical side (docstring edit to drop tags or name the paper appendix once stable), or accept as is until the paper's appendices exist, with a punch-list line. Decide before acceptance. |
| G-2 | Theory in brief says it gives "no proofs" but never says where the argument is; the definition of good wanted "the argument is in the paper". G9 withdrawal removes links, not a plain sentence. | Add one sentence naming the paper (link to the project page, as Home does). Small fix. |
| O-1 | Termination page is 611 words when its table is counted (budget 600); the test excludes tables. | Accept as is. |
| O-2 | `docs/generated/glossary.md` is committed although compiled. | Accept (the strict build needs it), or ignore it in git and generate in CI. |
| O-3 | Build INFO: Further reading has a footnote `magnani2009convex` never referenced; Home's `../` link is left as is. | Accept as is, or merge the double citation. |
| O-4 | `mkdocs build --strict` with the default `site_dir` clobbers the tracked root page. | Set a different `site_dir` in `mkdocs.yml` or document the `-d` flag. Follow-up. |
| O-5 | Pages dispatch build and 375 px emulation not run. | Pending items at acceptance. |

## Recommendation

Do not recommend acceptance yet. Everything in scope is met except G-1 and G-2, which need a disposition; the rest are observations to accept as one item. After G-1 and G-2 are decided, I recommend acceptance with the listed observations noted, once the supervisor's second staged review and the Pages dispatch run are done.
