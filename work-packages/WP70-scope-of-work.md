# WP70 — Scope of work: the iron triangle as an HTS study (stage 1, the probe)

| | |
|---|---|
| **Status** | DRAFT for his approval in chat (quoted in `WP70-decisions.md`); one open decision below |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; the probe writes only under `work-packages/WP70-rounds/` |
| **Approval record** | His plain OK in chat, quoted verbatim in `WP70-decisions.md` |
| **Acceptance record** | His read of the pitch; his choice among its options recorded in `WP70-decisions.md` |

## Purpose

His direction (`WP70-decisions.md`, verbatim): a study of project management's iron triangle with HTS; the triangle
read as an n = 3 + m lemma (schedule slack, budget slack, scope as story points, plus m quality metrics of the project
at hand); ideally built on a big open-access dataset, else a synthetic case structured to his story; possibly more
than one example, a research programme in time; for now a probe that explores and returns a pitch for a bounded
model and analysis; the first audience is project-management people (a COO who is a PE and PMP).

## Goals

- G1. **The metric mapping, written once:** the three sides as HTS metrics in his terms (schedule slack, larger is
  better, as a share of the planned schedule if wanted; budget slack likewise, with the conditioning that keeps an
  over-budget project strictly positive stated and justified; scope as delivered story points, a floating unit the
  empirical method tolerates), and how the m quality metrics enter; what each needs from a dataset (which columns, at
  which grain: a project, a release, a sprint, a work item).
- G2. **The data survey:** open-access datasets that carry at least two of the three sides and one quality measure,
  from software and agile project archives (issue trackers with story points, sprint and release records), public
  project portfolios (government and development-bank project records with planned and actual cost and schedule and
  an outcome rating), and construction or infrastructure records where open; for each: the source, the licence and
  whether a derived table may be committed (the repository's manifest pattern: DOI, licence, hash), the grain, the
  rows, which sides and quality measures it carries, what it lacks, and the fetch (open, behind a form, or by request).
- G3. **The synthetic alternative, designed:** a generator structured to his story (a planned schedule and budget, a
  scope in story points, m quality metrics; the trade-offs planted and the noise), what it can show that a dataset
  cannot (planted answers recovered) and what it cannot (anything about real projects).
- G4. **The pitch:** two or three bounded options for the first study, each with the dataset or the generator, the
  metrics, the unit of analysis, the questions the fit is asked in project-management terms (which sides trade near
  the frontier, how many terms, where the quality metrics sit), the analysis plan (the arc of `notes/examples-template.md`),
  the deliverable (an example page in this repository, or a study of its own), the cost, and what would make it fail;
  written for the project-management reader first, with the method's terms in a second part; what each option
  would tell a PE and PMP that they do not already know.

## Non-goals

No fit committed to the tree in this package; no dataset committed; no change to the package, the docs or the paper;
no claim about the iron triangle beyond what the survey and the design support.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `work-packages/WP70-rounds/pitch.md`: G1, G4, and the summary of G2 and G3 | G1 to G4 |
| D-2 | `work-packages/WP70-rounds/datasets.md`: the survey table of G2 with every source cited | G2 |
| D-3 | `work-packages/WP70-rounds/synthetic.md`: the generator's design of G3 | G3 |
| D-4 | *(open decision 1)* a throwaway probe fit on the best candidate dataset, its numbers and one figure in the pitch, the notebook under `WP70-rounds/` and not in the tree's examples | G4 |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every dataset row cites a resolvable source and states its licence and fetch; none is invented | the links resolve (WebFetch) |
| R-2 | The metric mapping keeps every metric strictly positive and larger-is-better, with the conditioning named | a read against `docs/user-guide/conditioning.md` |
| R-3 | Each pitch option names its data, metrics, unit, questions, deliverable, cost and failure condition | the pitch's option table has no empty cell |
| R-4 | The pitch's first part reads for a PE and PMP: no method term before its plain meaning; no metanarration | a cold read by a reader in the P1 or P8 persona of `notes/reader-grid.md`, quoted in the pitch |
| R-5 | Nothing outside `work-packages/WP70-rounds/` changes; no attribution line | `git diff --stat dev` |

## Definition of good

He can choose a first iron-triangle study from the pitch knowing what data it stands on, what it will ask, what it
will show a project manager, and what it costs; the mapping of the three sides to HTS metrics holds under the
package's conditioning rules.

## Definition of good enough

D-1 to D-3 (and D-4 if chosen) delivered; R-1 to R-5 met; his read and his choice recorded.

## Definition of done

Good enough met; the first study scoped as its own package from his choice.

## Open decisions

1. **Does the probe include a throwaway fit** on the best open dataset it finds (D-4), so the pitch shows a first
   result, or is the probe survey and design only? *(to him)*

## Agent's defaults

- One unit, time-boxed to about a day of work; WebFetch and WebSearch for the survey; sources cited with the date
  read.
- Candidate families to search first: issue-tracker archives with story points and sprints (public Jira datasets,
  Apache projects, the agile story-point corpora used in effort-estimation research); public portfolios with planned
  and actual cost and schedule and an outcome rating (the US Federal IT Dashboard, the UK Infrastructure and Projects
  Authority annual data, development-bank project databases with evaluation ratings); software-engineering effort
  datasets (PROMISE, ISBSG where open subsets exist); construction and infrastructure cost-overrun collections where
  the data, not only the paper, is open.
- Budget and schedule slack conditioned as a share of the plan with a positive shift (the package's shift
  parameter) so an overrun stays strictly positive; the shift's choice reported as a conditioning choice, as the
  examples template asks.
- The pitch's options bounded to one dataset or one generator each; "more than one example" is the programme the
  pitch sketches in a closing paragraph, not the first study.
