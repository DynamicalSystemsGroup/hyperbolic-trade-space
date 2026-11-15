# WP59 — Scope of work: conditioning and feature engineering on the three public cases (research spike)

| | |
|---|---|
| **Status** | Approved verbally, "ok" to the spike as described in chat (2026-11-15, `WP59-decisions.md`) |
| **Supervisor (accountable)** | mzargham |
| **Repository** | `DynamicalSystemsGroup/hyperbolic-trade-space`; the spike under `work-packages/WP59-rounds/`, scripts beside the records in `examples/{perovskite,amniote,wheat}/` |
| **Approval record** | His words, quoted verbatim in `WP59-decisions.md` |
| **Acceptance record** | His read of the readout; his word quoted verbatim in `WP59-decisions.md` |

## Purpose

His purpose, verbatim (`WP59-decisions.md`): "use these cases to further examine the conditioning step, and explore
the impact of feature engineering work, or chaining with other unsupervised ML methods ... we're trying to show that
this is comparable to other data science work. on the one hand its a highly reproducible procedure, on the other hand,
how the data represents the problem matters. conditioning sensitivity is not a surprise to a seasoned ML engineer, but
most decision analysts are not seasoned ML engineers so building out these examples with guidance about what was done
why is valuable". The readout is the material the documentation pages (WP60) are written from.

## Goals

- G1. **A conditioning ladder per case**, from each record's primary rule, one step changed at a time: no scaler,
  standard, robust, a rank or quantile transform; extremes capped or not; the orientation of each time or cost metric;
  the covariate kept, partialled out or dropped (amniote mass); derived metrics in or out (efficiency, harvest index).
  Each variant reports the contending set at tau = infinity, the exponents and elasticities at the fit temperature,
  the association signs near the frontier, the band and K = 2's second term, in one table per case.
- G2. **Chaining with other unsupervised methods.** On the perovskite table: PCA on the log-metrics before the fit, as
  a screen for which columns to carry and as a rewriting (the scores brought back to a positive, larger-is-better
  scale, the orientation of each component a stated choice); ICA or a factor model as a second comparison if PCA
  changes the reading. On all three: the package's existing chain, PCA after the fit on the near-frontier chart, so
  the two orders are compared.
- G3. **A readout for a decision analyst** (`work-packages/WP59-rounds/readout.md`): per case, what was done and why
  at each step, as the choices an analyst must make and the check that says when a choice mattered (the orientation
  test, the scaler test, the extremes test, the derived-metric test, the chaining test); what the three cases say in
  common and where they differ; what each page should show (the set and the signs with the weights' range, not a
  weight) and what it must state (the orientation with its reason).

## Non-goals

- Any page in `docs/` (WP60). Any new feature in the package: the variants are scikit-learn tools in a pipeline and
  the package's public calls. Any change to the paper. Any claim about a dataset beyond what its record and the rerun
  show.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| D-1 | `examples/<case>/variants.py` for each case: runs the ladder and the chains from the cached data, writes `examples/<case>/variants.json`; every number in the readout comes from it | G1, G2 |
| D-2 | `work-packages/WP59-rounds/<case>.md`: the variant table with the rule stated per row, and the reading | G1, G2 |
| D-3 | `work-packages/WP59-rounds/readout.md`: the guidance, under 1,500 words, in the register of the docs (plain sentences, the glossary's words, no metanarration) | G3 |
| D-4 | `work-packages/WP59-review.md`: a reviewer reruns one variant per case from a clean cache and compares the numbers; the checks run | acceptance |

## Requirements and checks

| ID | Requirement | Check |
|---|---|---|
| R-1 | Every variant is a stated rule, reproducible from the cached data by one command | the review's reruns match to the printed precision |
| R-2 | The primary row of each ladder reproduces the record's primary fit | the record's numbers against `variants.json` |
| R-3 | PCA-before-the-fit states how the scores are made positive and oriented, and the reading is reported either way | the case file |
| R-4 | No dataset content redistributed beyond the records' rules; manifests checked on every run | the scripts' manifest checks, as the records' |
| R-5 | Lint, format, lock, vocabulary and residuals on the new files; no AI attribution | the usual commands; `git log` |
| R-6 | The readout speaks to a decision analyst: each choice with its reason and its check; no sentence about the text | a read against CLAUDE.md's rules; `scripts/check_residuals.py` exit 0 |

## Definition of good

An analyst with a table of their own can read the readout and know which conditioning choices to make deliberately,
how to test whether each mattered, and what a stable reading of a soft fit looks like.

## Definition of good enough

D-1 to D-4 delivered; R-1 to R-6 met; the reviewer's reruns match; his read of the readout with no change asked, or
his edits applied.

## Definition of done

Good enough met, no open item, his acceptance quoted in `WP59-decisions.md`.

## Open decisions

None.

## Agent's defaults

- Two units: one for the perovskite and amniote cases, one for wheat; one reviewer. Each unit in its own worktree on a
  branch `wp59-<unit>`; the driver lands them.
- The rank transform is scikit-learn's `QuantileTransformer` with a uniform output shifted into the positive range;
  the robust scaler and the standard scaler are the package's existing `LogAffinePreconditioner` choices where they
  exist, scikit-learn's otherwise.
- PCA scores are made positive by exponentiation after centring (a log-affine map back), so the method's assumptions
  hold by construction; the orientation of each component is the sign that makes its leading loading positive, stated.
- Temperatures are chosen by the records' rule (a tenth of rows above the surface) unless a variant says otherwise.
