# HTS: an external-use assessment for the author

*November 9, 2026. Prepared from two deliberately small public-data studies, with suggestions sized for an actively developing paper and package.*

HTS made a promising transition from its own examples to two outside cases without changes to its source. The strongest result is a compact description of a controlled, history-driven collateral trade space: a few terms capture an active trade-off and a safety plateau, and a complexity sweep exposes diminishing returns. Equally useful, the experiments distinguish what a successful numerical fit establishes from what a user might mistakenly infer about a full empirical boundary or a predicted outcome. These distinctions can strengthen the paper’s contribution without requiring a broader economics paper or a new model-selection algorithm.

## Revision and review boundary

All empirical fits in this assessment use **`c46832c633ea7efc5ef0915372ba83ff03d46ea2`**, committed November 9 at 13:45:44 −05:00. [Tested revision](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/c46832c633ea7efc5ef0915372ba83ff03d46ea2).

The fetched `dev` tip inspected during preparation is **`b653e98a4c7cbe097b1c25c73b5d17d83e28ba59`**, committed November 9 at 16:40:36 −05:00: **62 commits later**. This is an observed tip, not a claim that development stopped there. [Inspected later revision](https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space/tree/b653e98a4c7cbe097b1c25c73b5d17d83e28ba59).

I reviewed the intervening history and selected documentation/scope changes, but did not rerun the studies on that later revision. The only changed file under `src/hyperbolic_trade_space/` in that interval is `plotting.py`; the estimator and solver sources are unchanged across these two revisions. That narrows the numerical relevance of the revision gap, but is not a substitute for testing the newer environment. The interval also adds the soft-fit certificate derivation, clearer temperature and termination documentation, a claims register, verification tiers, container records, and substantial paper/figure review. The feedback below should be read alongside those improvements, rather than as an assertion that their subjects are currently undocumented.

The studies ran in isolated research directories. No author checkout was edited, no HTS patch was needed, and nothing was committed, pushed, or sent externally. This is an independent application exercise conducted by one AI research assistant, not an independent human review panel or a complete release audit.

## What I did

I first inspected the repository’s implementation, derivation records, documentation, history, and development scopes. I then built two small cases from public sources, retained frozen inputs and source hashes, and recorded protocols separately from later diagnostics. The first case was chosen as a basic geometry check; its limitations motivated a more controlled second case.

**Filecoin:** BlockScience publications and its baseline-incentives repository grounded the metric interpretation. A frozen Filecoin Data Portal export supplied historical measurements. I used complete eligible weeks in 2021 for fitting (48) and 2022 for chronological comparison (42), excluding missing-reward and incomplete weeks without imputation. The metrics were network raw capacity and allocated miner reward per unit of that capacity. I compared one-term and two-term fits, an arithmetic control, simple reference curves, conditioning choices, and calendar-block resamples.

**RAI:** I used the public Reflexer digital-twin archive, checked valuation mechanics against public documentation and the BlockScience model, and constructed a minimal no-action SAFE replay. Fifty-one initial collateral ratios, 150%–400%, face identical seven-day historical windows within each suite. There are 53 earlier and 36 later windows. The replay freezes a 145% liquidation threshold and a 2% annual debt multiplier; it does not simulate interventions, auctions, liquidity, or borrower behavior. Borrowing capacity is `1/c`; sampled breach fraction is B; the positive safety metric supplied to HTS is `1/(1+B)`.

I independently checked replay counts using direct collateral/debt valuation and per-window required-collateral thresholds. All 102 candidate/suite counts agree, and six analytical fixtures pass. HTS fits use 26 alternating earlier candidates, leaving 25 intermediate candidates for interpolation validation. A later user request extended the experiment through K=10: three seeds for sharp, exact-maximum fitting, and a primary finite-temperature sweep with additional seed spot checks. Each fit uses five restarts. Independent geometric and linear-interpolation benchmarks use the same fitting rows.

This is deliberately a method check. Historical prices are observed; candidate SAFE outcomes are hypothetical replays. Neither study estimates a complete economic model.

## Observations: what the evidence shows

### 1. Filecoin passes a useful sanity check, with limited discovery content

The primary one-term fit has nearly equal weights, approximately (0.498, 0.502), and an original-log capacity/reward-density slope near −0.993. An independently constructed constant-reward-budget control recovers equal weights and the expected inverse relationship to numerical tolerance.

That result is reassuring about geometry and metric handling. It is not evidence of a newly discovered economic law: reward density is defined as R/P, so P times density equals R. Near-inverse geometry is partly arithmetic. Further, historical dates represent changing contexts, rather than interchangeable design alternatives under one fixed context.

Two terms describe the historical curve more closely. In the chronological comparison, median absolute log-density distance from the reference is about 0.178 for one term and 0.031 for the soft two-term fit, versus 0.170 for a constant-training-median-budget reference. All later capacities exceed the earlier capacity range. These are descriptive reference distances under extrapolation, not validated forecast errors.

A duplicated-term control is especially instructive: with unnormalized soft aggregation at kappa=20, duplicating one term changes the score by log(2)/20, approximately 0.0347, without adding a direction. Of the observed 0.0437 mean-slack improvement from one term to soft two terms, approximately 0.0090 remains beyond that control. This is a consequence of the aggregation convention, not an arithmetic defect. It helps users avoid interpreting every loss improvement across K as new geometry.

### 2. RAI contains a clear trade-off, with empirically meaningful plateaus

Increasing collateralization from 150% to 200% reduces borrowing capacity by 25%. Earlier sampled breaches fall from 32/53 to 1/53; later breaches fall from 23/36 to 8/36. The first zero-observed-breach grid point shifts from 210% earlier to 295% later.

The direction is built into the collateral mechanics. The magnitudes, steps, saturation point, and changes in dominance come from the historical relative-price paths. Earlier, ratios above 210% sacrifice capacity without adding measured safety. Later, 200% and 210% have identical measured risk, making the previously efficient 210% point dominated. HTS is therefore being asked to represent more than a generic negative correlation.

These are sampled breaches, not actual liquidations or estimates of zero population risk. The archive is irregular: tightening the maximum observation gap from six hours to two preserves all 53 earlier windows but only three later windows. Windows overlap, the stress-period choice is informed by known history, and the fee assumption is not a reconstruction of every historical update. Those limits materially constrain economic conclusions.

### 3. The sharp K sweep gives a useful complexity elbow

The primary exact-maximum, sharp-aggregation run gives:

| Requested K | Mean training slack | Reserved-candidate MAE, percentage points | Distinct terms |
|---|---:|---:|---:|
| 1 | 0.041471 | 3.698 | 1 |
| 2 | 0.005202 | 1.038 | 2 |
| 3 | 0.000935 | 0.526 | 3 |
| 4–10 | 0.000935 | 0.526 | 3 |

K=2 supplies most of the improvement; K=3 adds a smaller refinement. Larger requested models repeat terms and report `stationary_without_margin`, rather than adding independent structure. Some other initializations remain at the weaker two-term solution at K=3/4; all three seeds reach the common floor by K=5. This sweep shows diminishing returns and redundancy, rather than rising validation error.

One term selects the flat safety cap, with weights (0,1) and a `monolemma` report. That is locally informative but does not mean the whole design space lacks a trade-off. The two-term fit passes the original aggregate adequacy rule, yet only four of six reserved points in the active trade-off region meet its five-percentage-point tolerance. Reporting that region prevents the large, easy plateau from obscuring local errors. This regional diagnostic was added after inspecting the curve.

### 4. Equal training loss can conceal different boundaries

A five-facet upper log-convex envelope constructed from the same 26 fitting rows has the same mean slack as the primary three-term HTS fit, to numerical precision, but lower reserved error: 0.341 rather than 0.526 percentage points, with maximum error 3.11 rather than 6.83 points. It uses no reserved outcomes. Linear interpolation is also competitive: MAE 0.453 and maximum error 2.83 points.

Thus, reaching the training-loss floor does not identify every useful supporting facet. Additional facets can change the boundary between fitting points without changing the observed objective. Increasing K alone does not necessarily select them. This is a particularly valuable, small counterexample for explaining the difference between optimizing the stated objective and recovering an entire boundary.

### 5. Finite-temperature reference inversion can lose task usefulness

With fit temperature tau=20 and still **sharp term aggregation**, primary training slack improves as K increases while reserved breach-reconstruction MAE rises from 4.23 points at K=1 to about 41.46 at K=10. Some reference intersections imply impossible breach fractions; at K=5 one is about 7.42, or 742%. These values were retained, not clipped. Several such fits report certified termination.

This does not establish an optimizer bug. A finite-temperature V=1 reference is not guaranteed to be an empirical support boundary or a calibrated probability estimator. Inverting it into a bounded risk outcome is a downstream task that can fail even when the numerical certificate holds. This degradation is distinct from the soft-aggregation duplication effect in Filecoin.

The large MAE is not universal across seeds. At K=10, two other seeds have unavailable intersections for two candidates, and conditional MAEs around five points on the remaining 23. All three seeds have two invalid/unavailable outcomes and only 17/25 candidates within tolerance. The defensible conclusion is loss of reconstruction adequacy and initialization sensitivity, not a universal 41-point error or a clean attribution solely to statistical overfitting.

Finally, the earlier three-term reference has about 10.37-point MAE under later stress. More terms do not repair a changed stress distribution. After examining K, the reserved candidates are validation data, not an untouched final test.

## Interpretation: what this says about HTS

The encouraging result is that a small, unchanged implementation can summarize a nonlinear empirical trade space in interpretable regional terms. The package’s termination distinctions are useful in practice: certified low-K fits, repeated high-K terms, and insufficient regional sample sizes remain visible. The two-term regional tension report correctly refuses the default report when a facet has only five usable rows, below the default minimum of ten; I did not lower that threshold to manufacture an answer.

The main communication opportunity is to keep three claims distinct: **numerical success on an objective; descriptive success on observed trade-space geometry; and predictive or decision usefulness outside those observations.** These studies support the first two in bounded ways, and show why the third needs its own validation. This sharpens the contribution rather than diminishing it.

Conditioning also belongs to the question being asked. A diagnostic change in geometric reference center, while retaining the same constraint set, changes the RAI one-term weights from the safety cap to a sloped facet. A stable fitted direction is therefore not a context-free discovery. Likewise, 51 designed collateral ratios are not 51 independent economic observations.

## Suggestions sized to the current scope

These are inputs for author triage, not proposed release blockers or requests to absorb both economic studies into the paper.

| Suggested action | Smallest useful form | Scope judgment |
|---|---|---|
| Distinguish certificate, boundary, and prediction claims | A short paragraph near fitting/termination, linked to existing limitations | Near-term clarification if not already covered by the newer claims pass |
| Explain a one-term cap without implying absence of global tension | One compact cap-plus-slope example or note | Fits existing explanation/example work; no new economic case required |
| Explain requested versus effective K | Show distinct/assigned terms and validation alongside training slack in an example | Optional documentation improvement; a new automatic selector can wait |
| Document temperature/reference semantics and soft duplication | A brief convention note and duplicated-term calculation | Align with the newer temperature documentation; avoid duplicating it |
| Preserve equal-loss/different-boundary evidence | A small frozen fixture or supplemental note | Useful bounded follow-up; no requirement to redesign the objective now |
| Validate inversion into bounded outcomes | Explicit responsibility and an example that rejects invalid/unavailable intersections | Application guidance; not a request to make HTS a risk estimator |

The later history already shows substantial work on claims, vocabulary, figures, certificates, and reproducibility. I would route these observations into that process as concrete reader-confusion checks, with the author deciding whether a sentence, supplemental example, or backlog entry is sufficient. Existing package status and PyPI deferral should remain the author’s release decision. My research bundles resolve transitive dependencies at installation; they should not be presented as equivalent to the project’s newer pinned container record.

Broader questions can reasonably be deferred: automatic K selection or pruning, objectives that identify unsampled boundary structure, probabilistic calibration, a full multi-regime RAI study, Filecoin provider economics, and generalization across many domains. Each is potentially valuable; none is necessary to preserve the narrower result that HTS offers a useful coordinate and regional description of trade spaces.

## Evidence and reproducibility

The accompanying packet includes both original study bundles: protocols, frozen inputs, provenance, scripts, results, full K/seed tables, figures, and limitations. RAI’s public input is pinned to Reflexer digital-twin commit `24db92a6af8fded3e15e1de207162d093b32e531`; model context is pinned to BlockScience/reflexer `792d4c4a3ea52be96f3fb2c986e7d6c3c9644cd5`. Filecoin provenance distinguishes the frozen export from the repository revision used to inspect its definitions. The original RAI design is included separately so later diagnostics are distinguishable from the initial protocol.

Before issuing this assessment I retraced the source and saved outputs, then reran the analyses in fresh scratch copies. See `verification.json` for exact outcomes and numerical comparisons. This check does not constitute a complete rerun of the repository’s own test suite or testing of the later `dev` revision.

The most useful paper-level conclusion is modest and strong: these outside cases demonstrate a workable descriptive method, an interpretable complexity elbow, and practical limits that can be made explicit. The economic examples are supporting evidence for that claim, not a demand that this project solve economic forecasting.
