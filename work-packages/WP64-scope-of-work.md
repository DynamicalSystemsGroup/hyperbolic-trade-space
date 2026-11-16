# WP64 — Scope of work: two release control models (stage 1, the research spike)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy on his direction of 2026-11-16 (quoted in `WP64-decisions.md`); stage 1 of the six-stage lifecycle (research spike, decide, build, quality control, integrate, review the cascade) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; reads `.github/workflows/`, `scripts/assemble_site.py`, `scripts/stage_site.py`, `scripts/paper_keys.py`, `paper/`, `site/`, `pyproject.toml`, `work-packages/WP8b-release-checklist.md`, `work-packages/release-candidate.md` |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's acceptance of the readout against this scope; the design stage's scope goes to him with his decisions |

## Purpose

His direction (`WP64-decisions.md`, verbatim there): two separate release control models, "one for the paper which is
triggered event driven and probably builds from its own branch", and "the flow for the documentation and pypi release
which we gate around merging to main"; the paper on a four-mode lifecycle (the abstract only; working paper;
submitted, pinned; revision, pinned again), the abstract approved and sufficient for the software's release; the
repository is open source, so the site says the paper is iterated towards release and builds from the repository, not
"forthcoming"; "a significant reconfiguration", so a spike first, then design, implement, test, integrate, test again.

## Goals

- G1. **A map of the machinery as it is:** every workflow in `.github/workflows/` with its triggers, branches,
  environments and artefacts (tests, Pages deploy, TestPyPI and PyPI release, the PR gates); the site assembly and
  staging (`assemble_site.py`, `stage_site.py`, the root page, the paper slot and its placeholder); the docs' `paper:`
  citations (`paper_keys.py`: keys read from the notebooks at build time); the paper's build (`paper/`, mystmd, the
  container of record, `RECORD.md`); what the paper reads from the software side (the package, `examples/adcs`, the
  datasets, the generators) and what the software side reads from the paper (the docs' links, the root page, the
  reviewer's guide, the tests under `tests/test_paper.py`, the CI job `docs-paper`); the release checklist's rows by
  which side they serve.
- G2. **The couplings and the constraints:** everything that today forces the two releases to move together, each
  with the mechanism that couples it and what it would take to cut or to bridge it (for example: the docs' keys
  resolved against the paper's notebooks; the paper's data regenerated from the package; the suite running the paper's
  tests; one site build serving both; one version).
- G3. **Candidate designs, two or three, for each control model,** each with: the branch or branches (the paper on its
  own branch, as he expects; what lives there, how it takes software changes, how it feeds back); the events that
  trigger a build or a release (a push, a tag of a given shape, a manual dispatch, a mode change); the gates (what
  must be green; who approves; where the record lands); the artefacts (the paper's HTML and where it is served; the
  docs site; the wheel and sdist; the tags and versions; Zenodo or arXiv if the paper's lifecycle wants a DOI per
  pin); how the four paper modes map onto the events; and the failure modes (a paper build on the software's head
  that no longer matches; a docs link to a paper key the paper branch renamed; a Pages deploy that needs both). State
  for each design what it costs to build and what it costs the reader, the author and the maintainer.
- G4. **The decisions that are his,** each as a question with plain options and what each option implies, in the
  decision loop's form (one at a time, no recommended tag); the driver's own calls listed apart.
- G5. **The package sequence after the spike:** the design package (stage 2, scoped from the readout and his
  answers), build, quality control, integrate and the cascade review, each with its deliverable and its gate, and what
  of the release candidate (`release-candidate.md`, the checklist, the reviewer's guide) each one amends.

## Non-goals

No change to any workflow, script, page, test, checklist or record in this package; no deploy, tag or publish; no
opinion on the paper's content; the abstract page and the mode file are designed here and built in the build stage.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP64-rounds/readout.md`: the map (G1), the couplings (G2), the candidate designs (G3), his decisions (G4), the sequence (G5); diagrams as text tables or ASCII where a picture is shorter than prose | G1 to G5 |
| D-2 | `work-packages/WP64-rounds/machinery.toml` (or `.md`): the inventory of G1 in a form the design package can diff against after the build | G1 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every workflow, script and coupling named in the readout exists at the commit read, cited by path and line | a grep of each citation |
| R-2 | Each candidate design states its events, branches, gates, artefacts, the mode mapping and its failure modes; none is left implicit | the readout's design tables have no empty cell |
| R-3 | Each question for him has two to four plain options with their implications and no recommendation | a read |
| R-4 | The readout is under about 4,000 words with the inventory apart; no metanarration | `wc -w`; a read |
| R-5 | Nothing outside `work-packages/WP64-rounds/` changes; no attribution line | `git diff --stat dev` |

## Definition of good

The design stage can be scoped from the readout alone: the author decides the questions that are his, and a builder
knows what to change, in what order, with what tests, to give the paper an event-driven release from its own branch
and the software a release gated on the merge to main, with neither waiting on the other.

## Definition of good enough

D-1 and D-2 delivered; R-1 to R-5 met; the driver's acceptance recorded; his questions posed to him one at a time from
the readout.

## Definition of done

Good enough met; the design package scoped and approved; his decisions recorded in `WP64-decisions.md`.

## Open decisions

None before the readout; the readout produces them.

## Agent's defaults

- One unit on branch `wp64` in the prepared worktree; it reads GitHub's workflow docs with WebFetch where a trigger's
  semantics matter (tags on a commit of main; `pull_request_target`; Pages environments) and cites them.
- The paper's own branch is assumed to be named `paper` in the candidates, as a placeholder he can rename.
