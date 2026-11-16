# WP64 — Scope of work: the paper's lifecycle mode, apart from the software's release

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy on his direction of 2026-11-16 (quoted in `WP64-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`, branch `dev`; `scripts/assemble_site.py`, `scripts/stage_site.py`, `scripts/paper_keys.py`, `site/`, `tests/test_site.py`, `work-packages/WP8b-release-checklist.md`, `work-packages/release-candidate.md`, `CHANGELOG.md`, `README.md` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's soft-confirm on captures of the assembled site in each mode; his read afterwards |

## Purpose

His direction (`WP64-decisions.md`, verbatim there): the paper gets "a simple life cycle mode": first the abstract
only, "then its a working paper, while i am iterating on it", then pinned to a submission, then pinned again for
revisions; "the paper should get a paper lifecycle and the package should get an open source software lifecycle"; "at
release of the software i think the abstract is sufficient and the abstract is approved"; and, since the repository is
open source and anyone who pulls it can build the paper, the site does not call the paper forthcoming: "we can just say
we're iterating towards a paper release".

## Goals

- G1. **One declared mode in one place**, read by the site assembly: `abstract` (the abstract only), `working` (the
  whole paper, iterated), `submitted` (pinned to a commit or tag for a submission) and `revision` (pinned again). The
  mode carries the pin where one applies. Changing the mode is one edit; nothing else moves.
- G2. **The paper slot of the site per mode.** In `abstract` mode `/paper/` is one page: the paper's title, the
  author, the approved abstract (read from `paper/paper.ipynb`'s front matter at build time, so the page cannot drift
  from it), one or two sentences that the paper is being iterated towards release and builds from the repository, with
  the command, and the links to the documentation and the project home. In `working` mode the whole paper as today,
  with the mode stated once on the article (working paper, the commit). In the pinned modes the whole paper built from
  the pin, the pin stated once.
- G3. **The root page's card for the paper per mode**: in `abstract` mode it names the abstract and the iteration
  towards release; in the other modes as now.
- G4. **The docs' `paper:` citations in `abstract` mode** resolve as today at build time (the keys exist in the
  notebooks) and render as links to the abstract page, so no docs sentence changes and no link breaks; in the other
  modes as today.
- G5. **Two release checklists.** `WP8b-release-checklist.md` split: the software's (version, changelog, lock; local
  checks; CI on both platforms; the docs' reader round; the staged site in `abstract` mode; merge, tag, PyPI; after the
  tag) and the paper's (the container regression and re-pinning, the cold reproduction from the reproducibility
  appendix, the paper's reader round, the pin per mode, the repository links to `blob/main` at release per his answer of
  2026-11-16). `release-candidate.md` gains a dated section stating the two lifecycles; `CHANGELOG.md` and `README.md`
  say the paper's mode where they name the paper.

## Non-goals

No change to the paper's content, build or tests; no change to the package; no deploy, tag or PyPI step; no change to
the docs' prose beyond what G4 requires (none expected); no removal of the `docs-paper` CI job (the repository still
guards the paper); the mode for 0.1 is `abstract` and the switch to `working` is his.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | The mode file and its reader in `scripts/` (default: `paper/lifecycle.toml` with `mode` and `pin`), `assemble_site.py` and `stage_site.py` rendering the slot per mode; the stale placeholder page replaced by the abstract page's template | G1, G2 |
| D-2 | The root page's card per mode | G3 |
| D-3 | `scripts/paper_keys.py` rendering per mode; tests | G4 |
| D-4 | `work-packages/WP8b-release-checklist.md` split into `release-checklist-software.md` and `release-checklist-paper.md` (the old file's rows kept with their states, each row in one of the two); the dated section in `release-candidate.md`; `CHANGELOG.md`; `README.md` | G5 |
| D-5 | `work-packages/WP64-readout.md` with captures under `work-packages/WP64-rounds/`: the root page and `/paper/` in `abstract` mode, a docs link landing there, and `/paper/` in `working` mode | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | In `abstract` mode `stage_site.py` exits 0 without building the paper and without a kernel; in `working` mode it builds the paper as today | the two runs' exit codes and the staged tree |
| R-2 | The abstract on the page equals the notebook's front-matter abstract, the title the notebook's title | a test in `tests/test_site.py` that reads `paper/paper.ipynb` |
| R-3 | Every `paper:` key in the docs resolves in every mode; the docs build passes | `uv run mkdocs build -q` in each mode; a test |
| R-4 | The site's existing tests hold (the root-page register, the phone rule, word budgets, figure numbers) | `uv run pytest -q tests/test_site.py tests/test_docs.py` |
| R-5 | No metanarration; the page says the paper is iterated towards release and builds from the repository, never "forthcoming" or a date | `scripts/check_residuals.py --compare scripts/residuals_baseline.json --strict` with no new rise; `check_vocabulary.py` 0 new; a read |
| R-6 | Lint, format, lock; fast suite; no attribution line; nothing outside the named files | `uv run ruff check .`; `uv run ruff format --check .`; `uv lock --check`; `uv run pytest -q -m "not slow" -n auto`; `git diff --stat dev` |
| R-7 | Each checklist row of the old file appears in exactly one of the two new files with its state | a diff of the row ids |

## Definition of good

A reader of the public site at 0.1 reads the paper's abstract, learns the paper is being iterated towards release and
builds from the repository, and reaches the docs in one click; the paper's mode changes by one value; each lifecycle
has its own checklist and neither waits on the other.

## Definition of good enough

D-1 to D-5 delivered; R-1 to R-7 met; the mode set to `abstract`; the driver's soft-confirm on the captures; landed on
`dev` for his read.

## Definition of done

Good enough met, no open item, his read recorded in `WP64-decisions.md`.

## Open decisions

None for him before the delivery; the abstract page's wording and the split checklists go to his read.

## Agent's defaults

- Mode names `abstract`, `working`, `submitted`, `revision`; the file `paper/lifecycle.toml`; `pin` a commit or tag,
  required for the pinned modes and refused otherwise.
- The abstract page is served at `/paper/` in the root page's style (`site/` templates), not the article theme.
- In `abstract` mode the `paper:` citation renders `/paper/` without an anchor; the supporting material's keys the same.
- One unit on branch `wp64`, worktree prepared by the driver; captures by headless Playwright at 1,280 px from a stage
  served on a port above 8880, stopped after.
