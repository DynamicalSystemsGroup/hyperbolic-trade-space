# The breadth of the examples: an intent record (2026-11-14)

The supervisor's direction, verbatim in `WP44-decisions.md` ("The breadth of the examples"): the examples should show
the breadth of the model, and he gave the axes. He said he is "not exactly sure how this will fit into the build out";
this file captures the intent as an initial condition for the first release, not a requirement list. No scope changes
because of it. Each WP45 test record states its case's row; v0.2's example pages are chosen with the gaps in view.

## The axes, in his words

| Axis | His words | Values a case takes |
|---|---|---|
| Dimension | "high dimensional (number attributes, number of metrics, number of objectives can all vary), some are low dimensional" | counts of attributes, of metrics, of objectives (the decision-maker's subset) |
| Terms | "larger K number of posynomial terms and some are fewer" | the K the package's checks point to, and the K the record tests |
| Fit | "some will be tight fits and some will be softer" | the fit temperature and the band 1/tau at the K of record; the fraction above the surface |
| Origin | "real world measured cases and some are simulation based on models" | measured; simulated from a model; a mix |
| Lifecycle stage | "research to design to quality control to configuration management to end of life" | the stage the data come from |
| Measurement method | "a rich mix of data produced by different measurement methods synthetic and actual" | synthetic (a model's output), actual (an instrument's), or both in one dataset |

## The cases placed, from what is known today

Counts and K are read from the records named; a cell marked "to find" is filled by the case's test record, not guessed.

| Case | Attributes / metrics / objectives | K, fit | Origin | Stage | Method | Where |
|---|---|---|---|---|---|---|
| Cubesat (the paper's demonstrator) | 7 design variables; 13 traded metrics; 3 objectives in the decision of Section 9 (pointing error, unit cost, fleet cost) | K = 2 of record; tight (band 0.0088, D.2) | simulated from the system model | design | synthetic (the model's evaluations), with the launch cost derived | `examples/adcs/`, paper Sections 8 and 9 |
| Planted tables (the generator) | 4 metrics, 3 planted terms; varied by the generator | K planted and varied (D.13, D.14; WP43's two kinds) | simulated | research (a known answer) | synthetic | Appendix C, D.13, D.14, WP43 |
| Perovskite Database Project | hundreds of recorded columns; 3 traded device metrics (Voc, Jsc, FF) and stability; objectives to find | to find | measured | research (laboratory devices, many labs) | actual, heterogeneous instruments and protocols | WP45 test record |
| Amniote life histories | 11 life-history attributes; metrics after conditioning, to find | to find | measured | not an engineering lifecycle (natural science) | actual, compiled from literature | WP45 test record |
| Broadbalk wheat | 2 metrics (grain, straw) with treatment and year | small K expected; to find | measured | a long-run field experiment (research) | actual | WP45 test record (manual fetch pending) |
| ISU-ILCC battery ageing (candidate, not chosen) | 3 controlled stress factors; capacity fade, cycle life | to find | measured, a designed experiment | quality control and end of life | actual | `WP44-rounds/hunt/readout.md` |

## The gaps this shows

- **Stages.** Nothing yet from quality control, configuration management or end of life; the battery candidate would
  cover the first and last. Configuration management (fielded configurations with as-built and as-maintained data) has
  no candidate.
- **Mixed methods in one dataset.** No case mixes synthetic and actual measurements of the same designs; the
  propose-predict-check step of the search (Section 7) is where such a mix arises, and v0.2's interface and
  demonstration would produce it on the cubesat (predicted values from the fit against measured values from the model).
- **Soft fits and larger K.** Every fit of record so far is tight; a case whose checks point to K = 3 or more, or whose
  band is wide, is not yet placed. The perovskite database, with many laboratories' protocols, is the likeliest.
- **Objectives varying apart from metrics.** The cubesat has three objectives among thirteen metrics; a case with one
  objective and many metrics, and one where every metric is an objective, would show the decision layer's range.

## How the record is kept

A WP45 test record carries its row of the second table (the counts, the K and temperature found, the origin, the
stage, the method) as its first section, written before the fit where it can be and completed after it where it must
be; the row here is updated from the record when the record lands. The table is read, not argued from: a case that
turns out soft or many-termed is a finding, reported as such.
