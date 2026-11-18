# Directions: the spikes that felt them out, and the items planned (an index)

Housekeeping for the long-term development of the package, kept while the process record leaves the tree (WP73). Not
0.1 content and not a 0.2 plan: no item here has a priority or a release; the backlog and its order are a later
decision of the supervisor's. Two jobs only: a quick look-up for every research spike and where its record is, and a
record of every item planned or raised, each with the readout or ruling it comes from. His words live in
`candidates.md` (directions not yet spiked) and in the `WPn-decisions.md` files, cited by place and never requoted.

## 1. The research spikes

| WP | The question it felt out | What it found, in a line | Readout | Outputs and record |
|---|---|---|---|---|
| 35 | How HoroPCA's formalism and solver differ from this work's | HoroPCA fits a frame by a non-convex loss from random starts; this work minimizes a convex soft maximum over the simplex for one term and returns a gap | `wp35-horopca-formalism-and-solvers.md` | `git show 282b479:work-packages/WP35-rounds/spike-h/`; `WP35-decisions.md` in the tree |
| 36 | Formal results with Lean, and a Rust core compiled to WASM | Twelve lemma groups ranked by what Mathlib has; L1, L2, L5 the pilot, L3, L4 next; LP duality, KKT, second order and the pseudoinverse absent and stay hypotheses; a future direction, never a requirement | `wp36-formal-and-rust-wasm.md` | `git show 7b648a8:work-packages/WP36-rounds/spike/readout.md`; `WP36-rounds` and `WP36-decisions.md` in the tree (read by the claims register) |
| 41 | The bridge from the chart back to a design (propose, predict, check) | The chart and the conditioning are invertible except at the fit; three selection rules tie on reach, one run each; the interface's shape is a 0.2 question; the outer loop's conjecture is a submartingale, outward in expectation | `wp41-bridge-to-the-search.md` | `git show af54b3b:work-packages/`; `WP41-rounds` in the tree (read by the claims register); `docs/bridge.md` |
| 43 | Beyond the posynomial: a kernel that hugs a visible bend while keeping both problems convex | The log-quadratic form is in the log-convex class and is not a GGP; unconstrained it beats three terms by violating larger-is-better; monotone it sits between two and three terms; no model in the class follows a notch; the timings are the spike's cvxpy formulation | `wp43-kernel-direction.md` | `git show d0a97cd:work-packages/WP43-rounds/` (protocol, scripts, results, figures); `git show 4a76229:docs/superpowers/notes/kernel-direction.md` (the class on one page) |
| 44 | A second case study from a public, measured dataset | Thirteen candidates screened by licence, rows, measured outcomes and a named trade-off; perovskite, amniote and Broadbalk wheat became the example pages (WP45); battery ageing and others left as candidates | (none in this folder) | `git show d16309e:work-packages/WP44-rounds/hunt/` (candidates, readout, second pass, wheat check); `WP44-decisions.md`; `work-packages/examples-coverage.md` |
| 48 | Governance checks as verification cases for the release process | Three checks drafted against the repository's live settings (history protection, SBOM and immutable release, workflow files and default token); form, set and timing are his three questions; nothing runs yet | `wp48-governance-control-checks.md` | `git show ba62c15:work-packages/WP48-rounds/` |
| 50 | Holes in the chart by persistent homology | The chart is the right metric space (units-free, fit-independent); a planted hole is located and settled by one recomputed diagram; the case of record shows no candidate; a bay is invisible to the plain construction | `wp50-persistent-homology.md` | `git show 5233126:work-packages/WP50-rounds/` (objects and distances, construction and tools, the instance) |
| 52 | The governance lineage on the history page | A 92-word paragraph and `history.yaml` entries proposed; landed on his corrections | `wp52-governance-lineage.md` | `git show 03790a0:work-packages/WP52-rounds/`; `WP52-decisions.md` |
| 63 | The examples with an arc (a template; four pages redrafted for a cold reader) | Five parts with a must, a must-not and a length each; the four pages redrafted inside their budgets; the wheat figure's level sets his follow-up | `notes/examples-template.md` | `WP63-readout.md`, `WP63-rounds` (his read pending; leave at landing, hash in `INDEX.md`) |
| 70 | The iron triangle (time, cost, scope) as an HTS study | Kitchenham-CSC the one open table with all three sides; too sparse for a programme; smaller cases in the examples, option A first; his choice pending | (none yet) | `WP70-rounds` (his read pending); `WP70-decisions.md` |
| 72 | Learning the invariant rather than the trade (a two-sided, within-group estimator) | Planted invariants recovered; wheat's biomass is a size set by year and treatment, not conserved; a constant-product pool's weights recovered to the fee; five decisions his | `git show 4f81a4ea:work-packages/WP72-rounds/readout.md` (his read pending) | `WP72-rounds` (his read pending); `WP72-decisions.md` |

## 2. The items planned or raised, by stream

Each item names its source. "Options" means plain options drafted for him and not yet chosen; "ruled" means his word is
recorded; "direction" means raised and not yet spiked.

### The solver

- The extension point: a surface object with a feature map and a parameter set; consumers (elasticities, improvement factors, tensions) read a row-dependent gradient. Designed, not built (WP43 readout, section 5).
- Custom solvers, never a modelling layer: cvxpy proves a program feasible in a spike; the package solves it on numpy and scipy, as the monomial does (ruled, `candidates.md`, 2026-11-16).
- The log-quadratic kernel: build options A to D and the paper's word W1 to W3 (options, WP43 readout, section 7); the capacity-matched control, K = 4 to 7 on the same folds, not run (WP43, section 2).
- The separability estimator: the level explained twice, posynomial in one block and affine in another; monomial and a scalar first; the affine side written on a cone to learn what it admits and refuses (direction, `candidates.md`, 2026-11-16 17:19 and 17:27).
- The invariant estimator's five decisions: what it becomes, how groups enter, which market-maker data, several terms, whether the wheat page cites it (options, WP72 readout, section 5).
- K > 1 for the invariant: non-convex, restarts, no certificate (WP72 readout, section 4).
- The frontier solver chain for K > 1 as it stands: partition-and-refit, a local optimum (WP43 readout, section 3, the dent's 0.03).

### The examples library

- The breadth axes and the cases placed on them: dimension, terms, fit, origin, lifecycle stage, measurement method (`work-packages/examples-coverage.md`).
- Candidates not yet pages: ISU-ILCC battery ageing (quality control, end of life); TAWOS sprints (WP70 option B); Kitchenham-CSC (WP70 option A); the rest of the WP44 hunt table.
- One conventional-finance table to find; no crypto-economic example on any public surface; market-maker tables as internal test cases only (ruled, `WP72-decisions.md`, 16:11 and 16:13).
- The wheat figure with level sets (ruled, `WP63-decisions.md`, 15:51); the size-against-shape plot and a reusable plot beyond the ternary (ruled, `WP70-decisions.md`, 16:04); the dependence screen among metrics at conditioning (`WP70-decisions.md`).
- The docs example that explicates the synthetic three-metric case (`WP51-decisions.md`).
- Plotting step two: default levels, other uses, the ternary's region label rule (`release-candidate.md`).

### Thrust 1 of the abstract: searching the design space

- The selection rule for proposals: nearest in the pool, smallest change from a reference, a search over the surrogate (options, WP41 readout, section 4).
- The interface: `propose` and `check` on the regressor, a proposal object, or a recipe in the docs only (options, WP41, section 4); the feasibility condition as a flag or a constraint.
- The outer loop: not expected to move outward at every step; the conjecture is a submartingale, outward in expectation, with a convergence result when expected progress ceases; stated as future work, no conditions derived (ruled, `wp36-formal-and-rust-wasm.md`, 2026-11-14 12:20).

### Thrust 2: finding and filling holes by topological data analysis

- First package options: the definition as code on planted tables; the emergence study on the case; the boundary question as research; a controlled comparison with a space-filling rule (options, WP50 readout).
- The dependency: alpha complex (GUDHI, GPL v3 for the Euclidean versions) or Rips (ripser, MIT) with scipy's Delaunay (his, WP50).
- Open in the object itself: a bay, the level weight, relative homology with a fence on the near-frontier band (WP50, "The boundary").

### Thrust 3: formal results and performance

- Lean with Claude in the loop: the pilot L1, L2, L5, then L3 and L4; what a proof over the reals inherits and what floating point does not (WP36 readout, sections 1 and 2); never a requirement; the lemma scripts stay a pencil-and-paper substitute and no surface says "formally verified".
- A Rust core compiled to WebAssembly (WP36 readout, section 3).

### Governance and the release process

- Governance checks: form (SysML v2, the claims register, both), set (which checks), timing (gate, schedule, report with a baseline) (options, WP48 readout, section 4); the settings only he can change.
- From the external review of 2026-11-16 (`work-packages/review/external-review-2026-11-16.md`): widen the Python range with a CI matrix; `plotting` as an extra behind a lazy import; sympy out of the runtime set; the standard library's MoE and MoP metadata; `variation` and `variant`; `TradeStudy` (the model project's as much as this one's).

### Raised, with no readout

- Partial and quantile frontiers (`work-packages/milestones.md`, "After 0.1"; no other record).

## 3. How this index is kept

A direction enters `candidates.md` in his words with the date. A spike's readout lands in this folder as
`wpNN-<topic>.md`; its outputs leave the tree at landing and `INDEX.md` names the hash. A readout's landing adds a row
to section 1 and its items to section 2; a package's delivery removes the item it delivered. The order is decided when
the backlog is built, not here.
