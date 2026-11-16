# WP66c — Scope of work: the composer, the abstract page and the docs' keys (stage 3, build)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under his approval of the plan (2026-11-16, `WP64-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; branch `wp66c`; the file set of `work-packages/WP65-design/build-plan.md`, section "WP66c, the composer, the abstract page and the docs' keys" (11 files) |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's independent run, a browser pass of `/paper/` in `abstract` mode and of a pinned slot from a local artefact, and his read of the abstract page's wording; landed second of the three units |

## Purpose

Build the site's composition as `work-packages/WP65-design/specification.md` specifies it (sections 3.2 to 3.5, 4
and 5.2): the paper slot per mode with no paper build in the composer; the abstract page from the notebook's front
matter and `myst.yml`'s author; the root card's line per mode; the docs' citations through the committed key
manifest; the site workflows as called workflows; the staged site offline with `--slot` and `--artefact`.

## Goals

- G1. `scripts/assemble_site.py` and `scripts/stage_site.py` per 3.4: the slot per mode (abstract page; a pinned
  artefact unpacked with one banner line per page; fallback to the abstract page, said on the page and in the run,
  with a strict flag turning it into exit 1); the composer never runs the paper's build; `--paper placeholder` gone.
- G2. `scripts/paper_abstract.py` and `site/paper/abstract.html` per 3.3 (title, author, the abstract verbatim, the
  line that the paper is iterated towards release and builds from the repository with the command, the docs and root
  cards; both colour schemes; no script; never "forthcoming", "in preparation", "coming soon", no date);
  `site/paper/index.html` removed; the root card's line per mode per 3.4.
- G3. `scripts/paper_keys.py` per section 4: the manifest as the only key source, failing on a missing key, `/paper/#key`
  in a pinned slot and `/paper/` in `abstract` mode.
- G4. `.github/workflows/site.yml` and `pages-deploy.yml` per 3.5, called workflows that compose and deploy and
  never trigger on a tag.
- G5. The tests the build plan's section 2 lists for WP66c (`tests/test_paper_slot.py`, the `test_site.py` changes
  with the three removals, the `test_build_generated.py` replacements).
- G6. The browser pass the build plan's section 3 asks of this unit: `/paper/` in `abstract` mode and a pinned slot
  from a local artefact, desktop and 375 px, light and dark, captures under `work-packages/WP66c-rounds/`.

## Non-goals

No file outside the unit's file set (the build plan's table is the contract; a file another unit owns is never
touched; a need for one is reported, not met); no deploy, tag, publish or push; no change to the paper's content or
the package's public surface; no change to his keyboard settings.

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every element of the specification's sections for this unit is implemented or reported as impossible with the reason | a table in the hand-back mapping section to file |
| R-2 | Every test the build plan lists for this unit exists, is named as listed, and passes | `uv run pytest -q <the unit's test files>` |
| R-3 | The software suite passes with the paper tests deselected; lint, format, lock | the build plan's section 3 commands, exit codes captured |
| R-4 | No attribution line; no metanarration in any page or record text; `git diff --stat dev` names only the unit's files | the grep; a read; the diff |

## Definition of good

The unit's part of the design works end to end on a local checkout exactly as the specification states, and its tests
would catch the regressions the specification names.

## Definition of good enough

R-1 to R-4 met; the driver's independent run green; landed on `dev` in the build plan's order.

## Definition of done

Good enough met; WP67's quality-control runs green on the unit's part.

## Open decisions

None; the design is approved and the questions that remain his do not change this unit's files beyond a one-line
switch named in the scope.

## Agent's defaults

- One unit, worktree prepared by the driver; the specification's section numbers are cited in commit messages.
