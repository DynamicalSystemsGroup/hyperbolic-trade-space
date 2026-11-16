# WP65 — Scope of work: the two release control models, designed (stage 2, decide)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy on his six answers of 2026-11-16 (`WP64-decisions.md`, verbatim); stage 2 of the lifecycle; the specification goes to his read before the build |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; reads the WP64 readout and `machinery.toml`; writes only under `work-packages/WP65-design/` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's acceptance of the specification against this scope and his answers; his read |

## Purpose

His six answers (`WP64-decisions.md`): the paper iterates on a `paper` branch and its full build runs there; `/paper/`
on `dev` is the title, the author and the abstract; the paper reaches the public site by merging `paper` into `dev`
and `dev` into `main`; one site; Zenodo through the GitHub integration archives every release; only the current pin is
served; all the paper's tests leave the software's gate; the merge of the `dev` pull request into `main` is itself the
software's release, with failure detection and a clean-up script. The design turns these into specifications a
builder implements without further questions, and names the few details that remain his.

## Goals

- G1. **The software's release workflow specified:** `release.yml` on push to `main` (and a dry-run dispatch on `dev`
  as today): the admissibility checks (tag equals version, changelog entry, lock current, pinned actions, the suite by
  `workflow_call`), the tag created by the workflow, the build, PyPI by trusted publishing, the site composed and
  deployed as called jobs (a tag made by the workflow's token starts no other workflow, so nothing may depend on a
  tag event); failure detection at every step with the failing step named in the run summary and a GitHub issue or
  check; `scripts/release_cleanup.py`, run by the workflow on failure and by hand, that deletes the tag and the draft
  release and reports what it removed and what a retry needs; the rulesets and environments that are his keyboard
  items, listed with their exact settings.
- G2. **The paper's workflow specified:** `paper.yml` on the `paper` branch: a push executes the notebooks, runs the
  paper's tests (all of `tests/test_paper.py` and the paper's rows of the claims register, the length ledger, the
  residual and vocabulary checks on the paper's surfaces), builds the HTML and checks the keys; a `paper-*` tag (shapes
  per mode: working, submitted with venue, revision with venue and round) publishes `paper-html.tar.gz` and
  `paper-keys.json` as a GitHub release, which Zenodo archives; the container re-pin as the gate before a submitted or
  revision tag; how the branch takes software changes (merge `dev` in) and how its content reaches `dev` (merge
  `paper` into `dev`, conflicts expected in links only).
- G3. **The mode and the slot specified:** `paper/mode.toml` (mode, pin, venue, date), its validation, and what the
  composer renders per mode: the abstract page in `abstract` mode (title, author, the abstract read from the
  notebook's front matter, the line that the paper is iterated towards release and builds from the repository with
  the command, the cards to the docs and the root); the published artefact of the pin in `working`, `submitted` and
  `revision`, with one banner line naming the mode, the tag, the date and the DOI; the composer never builds the
  paper and falls back to the abstract page, saying so, when the artefact cannot be fetched.
- G4. **The docs' citations specified:** `scripts/paper_keys.py` reading a committed `paper-keys.json` on the software
  side (refreshed from the paper's release by the merge of `paper` into `dev`), failing the docs build on a key the
  manifest lacks, rendering links to `/paper/#key` when the slot holds a pin and to `/paper/` in `abstract` mode.
- G5. **The software's test gate specified:** which tests leave `test.yml` (every paper test) and which stay; the
  `docs-paper` job's fate; the claims-register test filtering by surface; the strict site stage without the paper
  build.
- G6. **The records specified:** the interface contract amendment (`/paper/`, the build, the keys); the release
  checklist split into the software's and the paper's with every row of the old file placed; `release-candidate.md`'s
  dated section; `docs/code-owners.md`, `work-packages/README.md` and `CHANGELOG.md`'s corrections of the three
  drifts the spike found; the reviewer's guide recut in outline.
- G7. **The build plan:** the file set of each build unit (WP66a the software model, WP66b the paper model, WP66c
  the composer, the abstract page and the docs' keys), with no file in two units; the tests each unit adds; the
  quality-control dispatches (dry runs only) and the browser pass per mode; the order of landing and the first merge
  to `main` since e7fd1165.

## Non-goals

No change to any workflow, script, page, test or record outside `work-packages/WP65-design/`; no deploy, tag or
publish; no change to the paper's content; the branch name `paper` and the tag shapes are placeholders he can rename.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP65-design/specification.md`: G1 to G6, each workflow in outline (triggers, jobs, steps, permissions, environments, concurrency), each script's interface, each file's fields, each test by name and assertion | G1 to G6 |
| D-2 | `work-packages/WP65-design/build-plan.md`: G7, with the file sets, the tests, the dispatches and the landing order | G7 |
| D-3 | `work-packages/WP65-design/his-items.md`: the keyboard items (rulesets, environments, Pages, trusted publishers, the Zenodo switch) with exact settings, and the two or three details that remain his, each as a question with plain options | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every element of the six answers appears in the specification, cited to its answer | a table in D-1 mapping answer to section |
| R-2 | Every coupling C1 to C23 of the readout is either cut, bridged or left, with the mechanism named | a table in D-1 with 23 rows and no empty cell |
| R-3 | No step depends on a workflow event a workflow-created tag cannot raise; the failure path of each workflow is specified with the clean-up it triggers | a read; the GitHub docs cited |
| R-4 | The file sets of the three build units are disjoint | a check in D-2 |
| R-5 | Nothing outside `work-packages/WP65-design/` changes; no attribution line; no metanarration | `git diff --stat dev`; a read |

## Definition of good

A builder implements each unit from the specification without a question to him; the release of either side cannot
block the other; a failed software release is detected and cleaned up so the merge is retried; the public site at 0.1
shows the abstract and reaches the docs.

## Definition of good enough

D-1 to D-3 delivered; R-1 to R-5 met; the driver's acceptance; his read of D-3 and the build units scoped from D-2.

## Definition of done

Good enough met; his remaining items answered; WP66a to c approved.

## Open decisions

None before the specification; D-3 lists what remains his.

## Agent's defaults

- One unit on branch `wp65` in the prepared worktree; GitHub docs by WebFetch where a semantics matters, cited.
- The clean-up script is Python under `scripts/`, uv-run, with `--dry-run`; it uses `gh` for the tag and release.
