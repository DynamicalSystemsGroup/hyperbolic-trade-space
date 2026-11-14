# WP45 — Scope of work: two public case studies and a two-metric example for the documentation

| | |
|---|---|
| **Status** | DRAFT. Approved only by the recorded act below; nothing is built before then. |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; work on `dev` |
| **Approval record** | The supervisor's verbal approval, quoted verbatim in `work-packages/WP44-decisions.md` |
| **Acceptance record** | The supervisor's acceptance, quoted verbatim, after `WP45-review.md` |

## Purpose

The supervisor's purpose, verbatim (`WP44-decisions.md`, 15:00): "the point here is to truly show the method works, for
that we need a variety of unrelated cases" and "this will do double duty by populating an examples section of the
documentation and help us harden our understanding of our own method". Each case is a known-answer test against the
field's named trade-off on data the method's authors did not make, reported whether the fit names it or not; the three
differ in domain, in who produced the data, in dimension and in whether a designer exists.

The supervisor's choice from the WP44 readout (`WP44-decisions.md`, 14:55, verbatim): both the Perovskite Database
Project and the Amniote life-history database become documentation case studies, independent of the synthetic
cubesat; and (14:50) Rothamsted's Broadbalk wheat yields become a two-metric example for intuition if the data are
good and the story is clear. The aim is the package's usefulness and its documentation (his priority of 14:20); the
paper is unchanged.

## Two requirements, kept apart

The supervisor's ruling (15:15, verbatim in `WP44-decisions.md`): the work that tests the method and the didactic story
drawn from it for the user are two requirements; the page is not written to convince. So each case has two
deliverables in order: the test record first (the expected n-lemma written from the literature before any fit, the
fit, pass or fail, sensitivity to conditioning and temperature, counts and limits; in `work-packages/WP45-rounds/`), then
the docs page drawn from it (what the data are, how to condition, how to fit, how to read, for a user with their own
table; no test apparatus on the page; the record cited once for the reader who wants it).

## Goals

- G1. **A reader can run each example from the docs alone:** each page states the dataset, its licence and source
  (DOI), the fetch step (at build time, nothing redistributed that the licence does not allow), the configuration
  and attribute columns, the conditioning rule with each orientation stated and why, the fits at K = 1 and 2 with their
  temperatures, the n-lemma read against the field's named trade-off, and what the example cannot show.
- G2. **The perovskite page shows design choices as configurations:** the four JV attributes on the default scan,
  efficiency set aside as derived (as launch cost is in the cubesat), zeros and fill factors above one dropped, the
  expected dilemma (voltage against current) checked against the fit; a second, smaller table for stability (T80) if it
  carries a reading.
- G3. **The amniote page shows natural science without a designer:** the -999 sentinel, a complete-case subset whose
  size is stated, taxonomy as the categorical configuration, body mass as the covariate with the choice (partial out or
  keep) stated, the orientation of the time costs (maturity, gestation) stated as a choice that decides what trades,
  the fast-slow continuum read against the fit, and the sentence that says where the design-space story stops.
- G4. **The wheat page shows the method in two metrics**, if its checks hold: grain and straw yield per plot and year,
  treatments and cultivar as configuration, the surface a line in log units, the simplex a segment, the chart one
  position and one level, the harvest-index story read against the fit; if the checks fail, the readout says why and
  the page is not built.
- G5. **The claims are backed:** every sentence of the three pages has a claims row; every citation enters
  `docs/references.bib` with a resolved DOI; the trade-off citations the hunt left unresolved (the fast-slow continuum;
  charging against cycle life is not needed here) are found and resolved first.

## Non-goals

- Any change to the paper, the abstract or the supporting material.
- Redistributing the datasets in the repository; the fetch runs at build time and the derived tables are cached in
  the build's folder with their licence file beside them.
- A scientific claim about photovoltaics, life history or wheat beyond what the cited sources say and the fit shows.
- The tension matrix on these tables before WP42 lands (added then, as one block per page).

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-0 | `work-packages/WP45-rounds/<case>/test-record.md` per case: the expected n-lemma from the literature, committed before the first fit; the fit, pass or fail against it; sensitivity to conditioning and temperature; counts and limits; written to test, reported either way | G5 |
| D-1 | `examples/perovskite/`, `examples/amniote/`, `examples/wheat/` (if built): the fetch step, the conditioning rule, the fit script, the generated figures and tables, each reproducible by one command | G1 to G4 |
| D-2 | `docs/examples-perovskite.md`, `docs/examples-amniote.md`, `docs/examples-wheat.md` (or one page with three sections, per the defaults), built into the docsite and linked from Examples and the docs home | G1 to G4 |
| D-3 | Claims rows and references for every sentence and citation; tests that the pages' numbers are the scripts' outputs | G5 |
| D-4 | `work-packages/WP45-review.md`: a fresh reader per page (P3, P4, P9) given the page alone, asked to say what trades and to run the example; screenshots held per the WP40 rule | all |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R-1 | Each fetch step records the source URL or DOI, the file hash and the licence text, and fails loudly when the source changes | the fetch script's manifest; a test that the hash matches |
| R-2 | Each page's numbers regenerate from the scripts in the container | `uv run` of each example's command; the docs build |
| R-3 | Each conditioning rule states orientation, shift and scale per attribute and the reason | the page's conditioning table against the script |
| R-4 | The n-lemma each page reads is the fit's at the stated temperature and K, and the named trade-off is cited with a DOI | the claims rows; `uv run pytest -q -m "not slow"` |
| R-5 | No file under `paper/` changes | `git diff --stat` |
| R-6 | The three fresh readers state the trade-off each page shows and run the example without a question | `WP45-review.md` |
| R-7 | Each test record's expected n-lemma is committed before the case's first fit, and the page carries no sentence whose job is to convince (the review reads for it) | `git log` order; `WP45-review.md` |

## Definition of good

- A user with their own table reads one of these pages and knows how to condition, fit and read theirs, and what the
  method will not tell them.

## Definition of good enough

- D-1 to D-4 delivered; R-1 to R-6 pass; the wheat page built or its checks' failure recorded.

## Definition of done

Good enough is met, no open item remains unresolved, and the supervisor has accepted the work by the acceptance record
above.

## Agent's defaults

- Three pages, one per dataset, listed under Examples after the cubesat; the Examples page gains one line naming them
  *(default)*.
- The perovskite table is the default-scan JV columns with complete cases; the amniote table is the complete-case
  subset of longevity, maturity, litter size, litters per year and body mass, with mass as a covariate; the wheat table
  is grain and straw yield with treatment and cultivar as covariates *(default)*.
- Fetch at docs-build time with a cache under `examples/<name>/data/` ignored by git, and a hash manifest committed
  *(default)*.
- Units run on Sonnet in worktrees, one per dataset, in parallel; the readers are Haiku *(default)*.

## Open decisions (for the supervisor)

- **OD1.** Place: (a) in the 0.1 candidate, before the release PR, so the docs ship with three examples beside the
  cubesat; (b) the first package of 0.2, with 0.1's Examples page naming them as coming.
