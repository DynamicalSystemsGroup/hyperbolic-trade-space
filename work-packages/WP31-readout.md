# WP31 stage 1 readout: choosing K

Gathering only; nothing in docs, paper or code changed. Scripts and outputs: `WP31-readout/` (`k_sweep.py`,
`aggregate.py`; CSVs; `planted-summary.txt`). All fits at one fixed temperature per table (cubesat: the K = 1
selection, 38.10 primary, 45.68 stock; planted: 50), solver defaults, `random_state=0`.

## 1. Methods we can stand behind

| Method | What it measures | User call | Backed by |
|---|---|---|---|
| Mean slack against K, one temperature | How far the designs sit below the K-term surface; the size of each drop | `mean_slack_` over a loop of `n_terms` | Falls with K by construction (L14, L15, glossary); fitting page; Appendix D.15; `test_case.py::test_mean_slack_by_k...`; sweep below |
| Thinnest term | Whether a term is a few designs | `term_share_`, `termination_.shares`, `cell_`; `case.has_reading` | Glossary (term share, row share); tension report guard (`min_near_frontier`, `test_tensions.py`); sweep |
| Resampling agreement (splinter) | Whether a term's exponents move under bootstrap or restart | `exponents_` over resampled `fit` | Fitting page; sweep below (noisy, see 2) |
| Planted-table calibration | What recovery looks like at your N and d when the answer is known | `make_frontier_data(n_terms=K0)` then `fit` | Appendix D.14 (16 of 20 at K0 = 3); `test_soft_fit.py::test_r5`; sweep below |
| Weak-direction flag | A nearly flat direction in a term | `conditioning_` | Docstring, L17 Hessian; sweep below (smallest value falls with K) |

Not a selector: the certificate (`termination_.status`, `max_gap`, `gamma`, `radius`; L12 to L17). Every fit in the
sweep is certified at every K 2 to 8 (max gap ~1e-15), and the stable radius is 1e-7 to 1e-4 with no trend in K. It
says the optimizer finished, not that K is right. No held-out criterion is built or studied.

## 2. What large K does, from the sweep

Cubesat, mean slack (`cubesat-*.csv`), K = 1..8: primary 0.243, 0.132, 0.088, 0.070, 0.061, 0.051, 0.045, 0.037
(drops 0.111, 0.044, 0.017, 0.010, 0.009, 0.006, 0.007: bending, no break). Stock 0.179, 0.114, 0.046, 0.035, 0.031,
0.028, 0.025, 0.021 (drops 0.065, **0.068**, 0.011, 0.004, ...: a break at K = 3). Smallest row share: primary
0.43, 0.22, 0.17, 0.15, 0.075, 0.064, 0.057 for K = 2, 3, 4, 5, 6, 7, 8; stock 0.41, 0.22, 0.21, 0.18, then 0.044, 0.051,
0.068 from K = 6.

Planted (12 tables each, 400 rows, 4 metrics, tau 50, `planted-summary.txt`; medians):

| K0 | K | slack | min term share | planted terms found | terms matching no planted term | splinter |
|---|---|---|---|---|---|---|
| 3 | 2 | 0.685 | 0.29 | 1.9 of 3 | 0.1 | 0.02 |
| 3 | 3 | 0.645 | 0.21 | 2.75 | 0.25 | 0.05 |
| 3 | 4 | 0.641 | 0.07 | 2.8 | 1.0 | 0.28 |
| 3 | 6 | 0.635 | 0.00 | 2.8 | 2.1 | 0.37 |
| 3 | 8 | 0.630 | 0.00 | 2.8 | 3.8 | 0.60 |
| 2 | 2 | 0.646 | 0.33 | 2 of 2 | 0 | 0.02 |
| 2 | 4 | 0.637 | 0.10 | 2 | 0.6 | 0.10 |
| 2 | 8 | 0.626 | 0.00 | 2 | 3.1 | 0.47 |

Findings: (a) mean slack never reaches a floor: after K0 it keeps falling by about 0.003 to 0.004 per added term
(planted) and about 0.004 to 0.01 (cubesat), at every K tried. (b) The planted terms are found at K0 and stay found
at larger K; each extra term is a spurious one (their count grows about K - K0), and the thinnest term's share
goes to 0 (an empty near-frontier cell) from K about 5 to 6. (c) Splinter agreement jumps beyond K0 on the planted
tables (K0 = 3: 0.05 to 0.28), but on the cubesat it is noisy: ten resamples (`*-B10.csv`) give primary 0.31, 0.55,
0.53 at K = 2, 3, 4 and stock 0.14 to 0.20 at K = 3 to 5 then 0.86 at K = 6. **The fitting page's "no term moves more
than 0.31 through K = 3" on the primary regime is not reproduced** (0.55 at K = 3 here with fresh resample draws per
K; the page's loop shares one random stream across K), so that sentence is draw-dependent as written.
(d) The cubesat K = 1 fit already has splinter 0.06 to 0.28: that is the noise floor of the measure.

## 3. PCA elbow kinship

The elbow in `mean_slack_` is the analogue where a break exists (stock at K = 3; planted at K0, drop 0.04 then
under 0.005); it stops at the tail: variance explained has a ceiling at d components, while here K has no ceiling,
slack keeps falling, and the added terms are spurious, thin and unstable (2b, 2c), so the elbow must be paired with
the thinnest-term and resampling checks, and the primary cubesat has no break to read.

## 4. What a docs page would need

Methods first (the table above, each with call and what it cannot say), the sweep as a runnable cell, then two
worked examples: planted K0 = 3 (known answer, the table in 2) and the cubesat both regimes (stock has a break,
primary does not; say so). The large-K statement is the sweep's, not an analogy's. Gaps to settle: the page's
splinter sentence (re-measure or drop); whether to introduce a held-out slack check (unstudied).

Options for placement, no ranking:
- A. New page "Choosing K": room for table, two examples and the sweep cell; costs a nav entry, a contract
  `docs.pages` amendment, glossary and claims-register rows, and the fitting section becomes a pointer.
- B. Expand the fitting section: no contract change, one place for K, temperature and band; costs a long fitting
  page and the examples compete with the fit's own material.
- C. Short section in fitting plus the worked examples on the examples page: lightest; costs the method and the
  examples living apart.
