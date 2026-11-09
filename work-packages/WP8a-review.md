# WP8a — Review report

| | |
|---|---|
| **Scope of work** | `work-packages/WP8a-scope-of-work.md` with its "Gate outcomes" and link policy, as modified by `work-packages/WP8a-decisions.md` |
| **Scope approval verified** | `WP8a-decisions.md`, "Scope approval": supervisor (mzargham), verbatim "Approved", 2026-11-08. Verbal record, as the scope names. |
| **Work reviewed** | Commits 53919c3, 1f4a29c, f4bcab3, 1c06335, 8ec4ba3, d39ac6c, 17a5a8a, plus the later `pages.yml` permissions edit (328371a) on `dev` |
| **Supervisor (accepts)** | mzargham |
| **Acceptance record** | Verbal acceptance in chat, quoted verbatim in `WP8a-decisions.md`, after this report |

Reviewer: fresh context, did not build the work. Nothing fixed; the only file written is this report.
Amendments applied while reviewing: Pages workflow triggers on tag `v*` and `workflow_dispatch` only, nothing deploys, R-11 moves to WP8b, evidence is the staged localhost site plus a dispatch build on `dev`, paper card links to the placeholder, placeholder links are allowed and listed, no caveat text, `pyproject.toml` and `uv.lock` are driver-owned.

## Checks run

| Check | Result |
|---|---|
| `uv run python scripts/stage_site.py` | exit 0; `_stage/` has `index.html`, `docs/` (all pages), `paper/index.html` |
| `uv run mkdocs build --strict` | succeeds; only two INFO lines (relative links `../` and `../../paper/` "left as is", expected: they point outside the docsite) |
| `uv run pytest tests/test_site.py tests/test_build_generated.py -q` | `30 passed` |
| `uv run pytest tests/test_interface_contract.py -q` | `85 passed, 2 skipped` |
| Fresh clone of `dev`, `uv sync --locked`, `uv run python scripts/assemble_site.py` | succeeds; `_site/index.html`, `_site/docs/index.html`, `_site/paper/index.html` present |
| `ruff check .`, `ruff format --check .`, `uv lock --check` | all clean (141 files formatted; 173 packages resolved) |
| Staged site served with `http.server` | 200 for `/`, `docs/`, `docs/method/`, `docs/generated/derivations/`, `docs/generated/verification/`, `docs/api-reference/`, `docs/literature/`, `paper/` |
| Attribution | `git log 53919c3~1..HEAD` message grep for co-authored / generated / claude: 0; all 12 commits authored by Michael Zargham |
| Dispatch build on `dev` | **pending** (the PM runs it after this review) |
| Browser view, light and dark | not done by me (HTTP and built-HTML inspection only); the supervisor's localhost review covers it. Source check: root and paper CSS define a `prefers-color-scheme: dark` palette; Material palette has light and slate. |

## Goals

| ID | Verdict | Evidence |
|---|---|---|
| G1 | met | Nav in `mkdocs.yml` has all eleven pages in the stated order; ten built pages render a `world-line` (`docs/index.md` carries none by design; it maps all three). |
| G2 | met | `scripts/build_generated.py` writes `docs/generated/derivations.md` and `verification.md` from the run (see R-5, R-6). |
| G3 | met | `site/index.html` thin HTML, three cards, source link, add-a-card comment. |
| G4 | met | `site/paper/index.html` placeholder at `/paper/`; one paper step in `assemble_site.py`. |
| G5 (as amended) | met | `pages.yml`: tag `v*` and dispatch triggers only; builds `_site/`; deploy job tag-only. |
| G6 | met except the dispatch run | strict build, link tests, workflow and layout tests pass; dispatch build pending. Live reachability moved to WP8b. |

## Deliverables

| ID | Verdict | Evidence |
|---|---|---|
| D-1 | met | `mkdocs.yml`: Material, arithmatex generic, mkdocstrings (numpy), bibtex, `site_url` under `/docs/`, repo link, `exclude_docs` for `superpowers/` and `references.bib`. |
| D-2 | met | `docs/index.md`, `docs/case.md`, `docs/api-reference.md`, `overrides/partials/content.html`. |
| D-3 | met | `scripts/build_generated.py`, `tests/test_build_generated.py`. |
| D-4 | met | `site/index.html`, `site/paper/index.html`. |
| D-5 | met | `scripts/assemble_site.py` (plus `scripts/stage_site.py`, the WP14 R-12 one-command staging, recorded in the gate). |
| D-6 | met (as amended) | `.github/workflows/pages.yml`. |
| D-7 | met | `tests/test_site.py`, 19 tests. |
| D-8 | met (driver-owned) | `default-groups` change is commit ee68bfa, before the range, by the driver; `.gitignore` ignores `_site/`, `_stage/`, `docs/generated/`; `site/` is tracked (`git ls-files site` lists both pages). |
| D-9 | met | `git show d39ac6c`: only 4 added lines per file (`---`, `world: ...`, `---`, blank) in six files, +24 total, no deletions. Listed in `WP8a-decisions.md`. |
| D-10 | partly met | Decisions file complete. The WP8a row of `work-packages/README.md` (line 100) still says "the Pages workflow deploying from `main` on merge" and "in execution on `dev`". See G-1. |

## Requirements

| ID | Verdict | Evidence |
|---|---|---|
| R-1 | met | Fresh-clone assembly above; strict build; broken links, missing pages, unresolved citations are errors (`strict: true`; `test_citations_resolve`, link tests). |
| R-2 | met | Nav order as G1. World lines rendered: embodied (Why and how, Case), symbolic (Preconditioning, API, API reference), formal (Mathematics, Derivations, V&V, Limitations, Literature). `test_world_lines_render` passes. |
| R-3 | met | arithmatex markers in built HTML: method 613, preconditioning 56, api 188, why-and-how 17, limitations 43, literature 33. |
| R-4 | met | Strict build with bibtex; literature page lists the bibliography (43 entries); tests pass. |
| R-5 | met | Both generated pages have the contract sections (Lemmas, Axiom ledger; Tests by area, Conformance, Lemma checks, Validated by a human); 1317 tests grouped in seven areas; 14 lemmas PASS. |
| R-6 | met | Compared against `derivation.axioms.AXIOMS` programmatically: all 22 axioms' text fields (statement, role, failure mode) found in the page; ids and tags grouped in POSITED / INHERITED / INHERITED solver level / REGULARITY / Fallbacks as in `run.py`; 14 lemma PASS lines equal the 14 sections. |
| R-7 | met | All nine names in `hyperbolic_trade_space.__all__` appear in the built API reference; strict build clean; `test_api_reference_names_equal_the_contract` and `..._renders_every_public_name` pass. |
| R-8 | met | Root is hand-written HTML, no `<script>`, no external resources (only repository links), inline CSS with light and dark palettes, relative card hrefs `paper/`, `docs/`, `docs/api-reference/`, repository link; "Start wherever suits you" paragraph; source footer; HTML comment marks where a new card goes. Link test resolves hrefs against the assembled site. |
| R-9 | met | Placeholder says "The paper is in preparation", links to `../docs/` and `../`; it is the only paper-side file. |
| R-10 (as amended) | met | Triggers: `push: tags: ["v*"]`, `workflow_dispatch`; no push-to-main trigger. Build job `permissions: contents: read`, checkout, setup-uv, `uv sync --locked`, `uv run pytest -q`, assemble, upload-pages-artifact of `_site`. Deploy job `needs: build`, `if: startsWith(github.ref, 'refs/tags/v')`, `pages: write`, `id-token: write`, environment `github-pages`, deploy-pages. Asserted in `test_workflow_*`. Dispatch run pending. |
| R-11 (as amended) | moved to WP8b | Punch list `work-packages/release-punch-list.md` lists three expected-at-release links, the PyPI note and eight live checks matching the R-11 URLs. |
| R-12 | met | `tests/test_site.py` runs in the default suite, no network; includes the full-build test. |
| R-13 | met | `ruff`, `format`, `lock` clean; WP8a diff touches only owned paths (below). `docs/*.md` edits are the six front-matter blocks only. Full `uv run pytest` was not rerun in full by me; the WP8a and contract tests were. |
| R-14 | met locally | No attribution lines; author Michael Zargham; dispatch build and CI on `dev` pending. |

Owned-path check (`git diff --stat 53919c3~1..HEAD`, excluding `work-packages/`): `.github/workflows/pages.yml`, `.gitignore` (1 line), `docs/{index,case,api-reference}.md`, six front-matter blocks, `mkdocs.yml`, `overrides/`, `scripts/{assemble_site,build_generated,stage_site}.py`, `site/`, `tests/{test_site,test_build_generated}.py`; `tests/test_interface_contract.py` is WP14's. Nothing in `src/`, `derivation/`, `examples/`, `pyproject.toml`, `uv.lock`.

## Link policy, caveats, working-draft label

- No "working draft" label anywhere on the root, docs home or placeholder (grep: 0). Respected (OD2).
- Caveat and hedging scan of the new pages (`site/*.html`, `docs/index.md`, `case.md`, `api-reference.md`, override): zero hits for draft, WIP, may, might, perhaps, probably, currently, not yet, subject to change. The only status wording is "The paper is in preparation" on the placeholder, which the scope calls for (R-9).
- Placeholder links: the paper card links to `paper/` (placeholder); the repository releases link, the root URL and the paper URL are on the punch list as expected-at-release. The `case.md` link to `examples/adcs/` on `main` resolves today (`git ls-tree main` shows it). The `og:url` metas in `site/*.html` use the future public URL; the root URL is on the punch list.

## Gaps (open decisions, suggested dispositions)

- **G-1. README status row stale.** `work-packages/README.md` line 100 still describes deployment "from `main` on merge". Suggested: PM updates the row to the amended trigger (release tag and dispatch) and sets the status at acceptance. Record edit, no new scope.
- **G-2. Math needs network in the localhost review.** `mkdocs.yml` loads MathJax from `cdn.jsdelivr.net`; offline, formulas show as raw markers. R-8's no-external-scripts rule applies to the root only, so this is within scope. Suggested: accept; mention in the review hand-off that the supervisor's staged review needs a network connection.
- **G-3. Permissions edit not recorded.** The least-privilege build job (328371a) is a PM change after approval, not noted in `WP8a-decisions.md`. Suggested: add one line to the decisions file; the change is within R-10 and tightens it.
- **G-4. Two files outside the ownership table.** `scripts/stage_site.py` (the WP14 R-12 command) and `tests/test_build_generated.py` (D-3's tests). Suggested: accept; both are covered by the gate outcomes and D-3, and the ownership table never listed them by name.
- **G-5. Pending evidence.** The green dispatch build on `dev` (R-10, G6, R-14) and the supervisor's browser review of the staged site. Suggested: the PM runs the dispatch after this review and records the run URL; acceptance waits on both.

No blocking defect found. Acceptance is the supervisor's.

## Browser pass (implementer, round 2)

2026-11-09, by the implementer, in the built-in browser on the site staged from `dev` after the
fixes to the driver's first pass (`uv run python scripts/stage_site.py --serve --port 8791`: the root
page, the real paper built by MyST for `/paper`, the sixteen docsite pages). Looked at rendered, at
1280 px and at 375 px (the browser's mobile preset), in the light and the dark scheme (Material keeps
the palette in local storage, so the scheme was switched by clearing it and reloading), scrolled to
the bottom where noted. A strict build, the link tests and page text were not counted as the look.

**What was done in the browser.** Root page at 1280 (top to bottom, the map at its width, the Package
card) and at 375 dark; the paper page at 1280 and 375 (images load, no sideways scroll); every
docsite page at 1280 light and at 1280 and 375 by an in-browser measurement of each page (page and
element overflow, code, tables, images loaded, display mathematics, MathJax containers) in an
iframe of that width; screenshots of Getting started, Tensions, Chart and Examples (light and dark,
1280), of Theory in brief, Tensions, API, API reference, Termination, Examples and Limitations at 375;
the phone navigation drawer opened, "User guide" expanded and "Tensions" followed; the search box used
on the phone ("certified": three matching documents, the first result opened) and at 1280
("exchange": nine matching documents); an in-page link followed (Fitting to the termination page); the
console read in fresh tabs.

| | Result |
|---|---|
| D1 figures | Seven, all loaded and legible in both schemes at 1280 and 375 (Getting started, Fitting, Tensions, Chart x2, Examples x2). Dark variants use white frontier lines and light axes on a transparent background. |
| D2 code | No code block scrolls at 1280 on any hand-written page (the pre holds 80 characters at 1280; the longest line is 72). At 375 a block scrolls inside itself (a scrollbar shows), as every code block does at that width. The API reference's docstring examples (seven blocks at 1280, up to 107 characters) still scroll: they are docstring text in `src/`. |
| D3 tables | No table remains on a hand-written page; the API reference has none (parameters are lists). At 375 the lists read without clipping. The API reference is 21,800 px at 1280 and 30,300 px at 375: the list style removed the tables and the clipping, and did not shorten the page much. |
| D4 | The first display equation is on two lines at 375 and fully visible; seventeen MathJax containers on Theory, none clipped. |
| D5 | Fitting, Chart and Tensions read as short lists; no paragraph over 110 words on Chart. |
| D6 | No 404 on any docsite page in a fresh tab and none in the server log. The 404 seen on the root page was the browser's `/favicon.ico` request; gone after `<link rel="icon" href="data:,">`. The paper page logs two 404s from its own scripts' CDN requests (thebe, MathJax 2). |
| R1 | The map is 1203 px wide at 1280 and readable; at 375 it is 335 px wide and the plain link opens the full-size file. |
| R2 | The install command wraps as "pip install" / "git+https://github.com/" / "DynamicalSystemsGroup/" / "hyperbolic-trade-space.git" at 1280 and 375. |
| R3 | The real paper is staged at `/paper/` (16 of 16 images load, no overflow at 375). |

**Remaining (not fixed here).**

1. `plot_tensions` draws its cell values in black: on the dark purple cells (the diagonal, and the
   strongly aligned pairs) the value is hard to read in both schemes. A change to `src/` (the
   technical side).
2. A docstring in the API reference carries a raw Sphinx role (`:func:~hyperbolic_trade_space.solvers.solve_terms`
   under `n_terms`), and docstring examples are up to 107 characters wide (`src/`).
3. On the phone the first search keystroke after "Initializing search" shows no results until another
   key is typed (Material's behaviour in this emulation); results then appear.
4. Chrome keeps a visited page and its images in cache across rebuilds of the staged site; a
   reload that bypasses the cache is needed after a rebuild while reviewing.
