# WP79 — Scope of work: the paper's own route (the `paper` branch rehearsed and the contribution route enabled)

| | |
|---|---|
| **Status** | DRAFT, approved by the driver as his proxy under the mandate (OD-1 answered by him, 13:05 EST); his words of 2026-11-17 in `WP64-decisions.md` ("No read-through before the release", "Contributing to the paper takes its own route") are the content |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/tradespace`; the `paper` branch (cut from `dev` at c0e210cc, 2026-11-17); the route's files land on `dev` after WP78 |
| **Approval record** | The driver's approval under his mandate, quoted in `WP64-decisions.md` |
| **Acceptance record** | The driver's verification; his read of the route as written |

## Purpose

His words: "we went to some pains to keep the work separable. i think the best move would be to create the paper
branch, and do some exploration and testing to make sure we have what we need in place to support parallel work";
"contributing to the paper should take a different route from contributing to code and documentation. we need to
make that clear and enable it in practice."

## Goals

- G1. Rehearsal, on `paper` and throwaway `qc/paper/**` branches, recorded in `WP79-rounds/rehearsal.md`: the paper
  built and tested from `paper` by `paper.yml` (dispatch); the three paper tests that fail on hosted runners
  (WP67 G4, G5) diagnosed, each with its cause and the smallest fix or a narrowed baseline; a paper-only edit on
  `paper` merged into `dev` to see where the branches touch (the design expects links only); the pin flow from a
  `paper-*` tag through the composer's pinned slot, on a `qc/paper/` branch so no release and no tag reach `main`
  (`paper-release` approval is exercised by the dry run's own approval step if the workflow has one; otherwise
  recorded as untested).
- G2. The route made clear: a "Contributing to the paper" section in `CONTRIBUTING.md` and in `GOVERNANCE.md`
  (WP78 writes that file first; WP79 adds its section): where the paper lives, that it is edited on `paper` by pull
  request, who reviews and approves, how it is published (a `paper-*` tag, the `paper-release` approval, the pin),
  how it reaches the site (merge into `dev`, then `dev` into `main`), and what is judged rather than checked
  (the paper's reviewer reads for the argument; the checks cover build, tests, residuals, keys).
- G3. The route enabled: a `paper/` ownership line in `.github/CODEOWNERS` naming the paper's approvers (the open
  decision); a pull request template for the paper (`.github/PULL_REQUEST_TEMPLATE/paper.md`, or one template with
  a paper section, the unit's default); `scripts/admissibility.py`'s merge row extended to pull requests into
  `paper` (merged by a paper approver who is not the author); the `paper` ruleset unchanged (no deletion, no force
  push; authors commit directly, contributors by pull request, as on `dev`).
- G4. The declaration of WP78 carries the `paper/` ownership and the paper reviewers, so the `controls` job checks
  them.

## Non-goals

No paper content changes beyond the rehearsal edit; no change to the software's route; no merge of `paper` into
`dev` outside the rehearsal; nothing outward (no `paper-*` tag on the real branch, no release) before his word.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `WP79-rounds/rehearsal.md` with run links, the three diagnoses, the merge's touch points | G1 |
| D-2 | The two sections (CONTRIBUTING, GOVERNANCE) | G2 |
| D-3 | The CODEOWNERS line, the template, the admissibility extension with tests | G3, G4 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | A pull request into `paper` by a paper approver, merged by another, passes the merge row; merged by its author, fails | `tests/test_admissibility.py` fixtures |
| R-2 | The paper builds green from `paper` on a hosted runner, or the failing tests are named with their cause | the `paper.yml` dispatch run's link |
| R-3 | The pin flow produces `/paper/` with the banner from a `qc/paper/` tag's artefact | the composer's `--strict-slot` run in the rehearsal |
| R-4 | No attribution line; lint, format, the fast suite green | the usual checks |

## Definition of good

A paper contributor reads one section, opens a pull request against `paper`, and is reviewed and merged by the
paper's approvers without touching the software's flow; a paper publication is one tag, one approval, one pin.

## Definition of good enough

G1 recorded with the three diagnoses; G2 and G3 landed on `dev` after WP78; G4 in the declaration.

## Definition of done

Good enough met; his read of the route.

## Open decisions

- OD-1, answered (his word, 13:05 EST, `WP64-decisions.md`: "paper PRs are approved by mzargham or jshorish"): the
  `paper/` line of CODEOWNERS names `@mzargham @jshorish`.

## Agent's defaults

- Unit A (the rehearsal, G1) runs now in a worktree on `qc/paper/**` branches and touches no file on `dev`; unit B
  (G2 to G4) runs after WP78 lands (default).
- One pull request template with a paper section rather than a second template file, unless GitHub's template
  chooser is wanted (default: one template).
