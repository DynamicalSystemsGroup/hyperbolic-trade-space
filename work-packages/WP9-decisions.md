# WP9 — Decision records (posynomial solver for K > 1)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- The supervisor's direction, during the scoping of the paper (verbatim in `WP10-decisions.md`, "The paper's story"): a solver for K = 3, showing K = 1 to K = 3, mostly extensions of earlier packages, starting with a second solver used when K > 1, required to work in practice for small K, scalability and performance as future work, as little code as possible on mathematical insights and existing optimization and ML tools. Breakdown revision OK'd verbatim: "OK, work from this list".

## Decision loop (2026-11-08)

- **OD1, selection of K.** Options: K stays the analyst's parameter with a diagnostic table / also a
  selection helper. **Supervisor (mzargham), verbatim:** "Analyst's parameter, diagnostic table".
  Disposition: decided; no automatic selection; the record tabulates objective and `frac_above_` at
  K = 1, 2, 3; selection of K named as future work in `docs/limitations.md`.

- **OD2, what the solver fits.** Options: hard-facet envelope / smooth posynomial at finite κ /
  hard fit with finite-κ smoothing on request. **Supervisor (mzargham), verbatim:** "i have a feeling
  we need a regularization option. i also want you to give me a more intuitive explanation of the
  difference between the size of the length of the vectors (metrics we care about) and number of
  product terms in our posynomial". Disposition: OD2 stays open; a new item **OD4, regularization**
  *(raised by OD2)* is added; the driver explains d versus K in chat before asking further.

- After the driver's explanation of d (metrics), K (terms) and n (contending metrics per term) and
  three regularization candidates. **Supervisor (mzargham), verbatim:** "we need to be a little
  careful with \"zero\" weights since we're working with log/exp transformations but i think were
  okay. the key is that the dimensions are not in a particular monomial. the monomials are the
  equivalent of the principle components but we need them to be sparse so we need one of the
  metaparameters to be how we keep them sparse. you have one such rule already and i want a
  regularization based alternative and for that to be a key word argument. our analog of singular
  values is the lead coef for each monomial and the vectors are the mononomials themselves. is that
  matching what we've done?"
- Disposition: OD4 (regularization) is decided in substance: a sparsity-promoting regularization of
  each term's exponents as an estimator keyword argument, alongside the existing rule (the τ = ∞ LP
  support and the working-temperature threshold); the scope's deliverables and defaults are updated.
  The PCA correspondence (monomials as components; the lead coefficient of each monomial as the
  analogue of a singular value) is answered in chat, with the two places it differs from the code
  as built.

- On the notation table and the "reach" row. **Supervisor (mzargham), verbatim:** "seems fine. its a
  bit wordier than i had hoped but we need to capture it for now and worry about how to present it
  in the paper writing. we're close to being able to save the table. one thing though. this
  discussion of novelty can be left out of the table since its just a final remark on what this
  could be useful for BUT what we can include is the tangent space for each monomial, something
  like a local partial via chain rule back to the configurations to tell us something about what
  trade-off breaking could look like. we are not assuming our data is exhaustive. if we're
  searching for \"better\" solutions we want to move UP the energy levels and we want to provide an
  intuition for how this method provides guidance on how to do exactly that. in computational
  setting this would support dynamically scoping new experiments for exploring the design space.
  this belongs in the discussion and future work section."
- Disposition: the novelty row leaves the table (it stays the paper's final remark); a tangent-space
  row is added (the gradient of log V on facet k is w_k in log-metric space, L3; chained through the
  conditioning (L9) and the configuration-to-metric map to a direction in configuration space that
  moves a design up the level surfaces; guidance for scoping new experiments; Discussion and Future
  work in the paper). The table is saved as a note once the supervisor says so.

- On the tangent-space row. **Supervisor (mzargham), verbatim:** "save it now. then give me the
  outline of the paper with key points and a summary of the material that backs it up"
- Disposition: the table is saved as `docs/superpowers/notes/notation.md` (the source of the paper's
  notation block and of the WP9 docs' vocabulary); the paper outline is saved as
  `docs/superpowers/notes/paper-outline.md` for the WP10 scope.

- **Supervisor (mzargham), verbatim** (during the Pareto and DEA discussion for the paper): "i also
  might want a proof that a V max solution is pareto efficient. that seems like a great (and
  straightforward result and its the intuition that kicked this off)"
- Disposition: a new derivation lemma L11 (`derivation/lemma_11_pareto.py`) enters this package as
  an extension of WP1, with its statement in `docs/method.md` and the test and ledger updates; the
  scope's D-8 and a new R-12 carry it. The paper (WP10) states it among the first results.

- **OD2, re-asked.** **Supervisor (mzargham), verbatim:** "i think fitting at k=infty is right. but
  like with PCA where you explain all the variance if you keep all the principle components we
  need to truncate in practice. i think this means hard fit with finite-kappa smoothing on request
  but i want you to explain to me what that \"means\" and how it relates to pca. to make sure it
  makes sense in context". Disposition: leaning "hard fit, finite-κ smoothing on request";
  confirmed only after the driver's explanation (chat) is accepted.

- After the driver's explanation of the hard fit, the smoothing and the PCA mapping (K as the
  number of retained components, facet share as explained variance, the by-K diagnostic as the
  scree plot, κ as the hard-versus-soft assignment of a mixture of local models, τ as the thickness
  of the edge). **Supervisor (mzargham), verbatim:** "i want you to document the choice to keep
  things smooth but note that our methods for searching likely tolerate cones so kinks are not the
  end of the world. let's record that for future work. we have chosen to make simplifying
  assumptions. we want to name them, defend them and then talk about how we approach going beyond
  them in the future"
- **Disposition: OD2 decided** as "hard fit, finite-κ smoothing on request", with a documentation
  requirement: the method page names the smoothing as a simplifying assumption (differentiability
  of the frontier for gradients and plots), defends it (L10's bound log K/κ; facets unchanged
  underneath; the kinks sit exactly on the ridges), and records for future work that the search
  likely tolerates the kinks, since the max of smooth functions has a tangent cone at a ridge and
  its generalized gradient is the convex hull of the active normals, which common-direction
  methods already work with. The "name, defend, go beyond" pattern applies to every simplifying
  assumption of WP9 and of the paper (recorded in `WP10-decisions.md`).

- **OD3, where K = 3 is demonstrated.** Options: primary dataset only / both regimes.
  **Supervisor (mzargham), verbatim:** "do experiments on both and we can decide what to use after
  we see the results". Disposition: decided; the K = 3 record covers the primary (aggressive-gains)
  and the stock-gains datasets; which the paper uses is WP10's decision after the results are seen.

- **OD4, regularization** *(raised by OD2)*: decided in substance by the supervisor's words above
  ("a regularization based alternative and for that to be a key word argument"); form (reweighted
  ℓ1, `penalty`/`alpha`) in the defaults.
- **Agent's defaults, as one item.** **Supervisor (mzargham), verbatim:** "Approve the defaults as
  listed". Disposition: approved.
- Loop closed: decided 4 (OD1, OD2, OD3, OD4), deferred 0, raised 1 (OD4), defaults approved as one
  item.

## Scope approval (approval gate)

- **Document:** `work-packages/WP9-scope-of-work.md` at commit d3abf28 (loop closed, no open items).
- **Date:** 2026-11-08.
- **Driver's question:** "WP9, the posynomial solver for K > 1, has no open items. Do you approve the
  scope of work for execution?" (options: Approved / Not yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; `work-execution` starts for WP9 under the PM/implementer pattern;
  commits prefixed "WP9: ", local only while the push hold stands.

## Push hold lifted (2026-11-08)

- Driver's question: whether to lift the push hold set on 2026-11-08 (three local commits ahead of
  `origin/main`). **Supervisor (mzargham), verbatim:** "Lift it, push main now"
- Disposition: hold lifted; `main` pushed; WP9 commits are pushed as they land, each green.

## Delivery (2026-11-08, PM)

- Delivered `main` 3bebe3e..6c304a8; review `WP9-review.md`. Gaps G-1 to G-9 await the driver's
  triage with the supervisor; PM suggestions: G-5 (recovery rate wording) and the G-1 docstring
  line fixed after the review in the follow-on commit; the rest accept as is, G-7 (frac_above_
  rises with K) a follow-up candidate.
- Post-review fix 2: CI on Linux failed one plotting test through facet relabelling of duplicate
  facets (d = 2, K = 3); the test is now permutation-robust (see `WP9-review.md`).
- CI green on 0a91cb7: run 42518908382.

## Acceptance gate: review gaps (2026-11-08)

- Review of record: `work-packages/WP9-review.md` (28caf5b; post-review fixes 1 and 2 at 28caf5b
  and 0a91cb7; CI green at run 42518908382). Gaps G-1 to G-9 taken through the decision loop; the
  ones touching a good-enough item one at a time, the rest as one item.
- **G-1 (facet refit and objective).** Options: accept as is / fix before acceptance / follow-up
  package. **Supervisor (mzargham), verbatim:** "Fix before acceptance". Disposition: fix is
  separate work and the whole review is rerun afterwards; before dispatching, the driver states in
  chat why the per-facet-rows min-max refit is ill-posed in principle and asks one question a level
  up about what the fix should be (decision loop, step 4).
- The driver explained (chat) that the per-facet-rows min-max is ill-posed in principle (the
  support function of a sliver is minimized at a simplex vertex) and that the built solve is the
  one-sided analogue of per-partition least squares (supporting hyperplane of all rows, tightest on
  the facet's rows), and asked what the fix should be. **Supervisor (mzargham), verbatim:** "do a
  research spike. what function did this fulfill and what are some ways to handle that function
  which is better fit with our evidence". Disposition: a throwaway research spike (scratch code
  outside the repository; a note of findings in `docs/superpowers/notes/`) that names the function
  of the per-facet step, enumerates ways to fulfil it, and measures them on the planted data
  (including the seeds where recovery failed) and on the cubesat tables; the G-1 fix is chosen
  from its findings; acceptance waits.
- Spike delivered (`docs/superpowers/notes/spike-facet-refit/README.md`, scripts and tables beside
  it). Findings in brief: the per-facet step as built (B, supporting hyperplane of all rows tightest
  on the facet's rows) recovers 60 of 60 planted facets when given the true labels, including facets
  with 2 to 4 frontier rows; the approved default (A, per-facet min-max) recovers 0 of 60 and is
  ill-posed in principle; the failures on seeds 1, 3, 8, 16 are the alternation's: on those seeds the
  planted partition has a higher mean slack than the found one, so the objective prefers splitting a
  populated facet to keeping a sparse one. A tangent-plane direction from the facet's near-frontier
  rows with B as the base (D, or its shrinkage form E) raises single-start recovery (16 to 19 of 20
  against 12 to 19) and recovers seed 8, at the cost of a non-monotone step, about 30 lines and one
  constant; responsibility weighting (C) degenerates to the K = 1 fit; fixed candidate directions (F)
  cannot resolve d = 10. On the cubesat primary table B, D and E agree on four seeds of five and share
  the same other local optimum on the fifth. The spike ranks E or D-with-fallback first, B-as-is with
  corrected docs second, and raises the objective (mean slack versus a frontier-weighted slack) as
  the question a fix must settle. Put to the supervisor.
- Driver's question on the G-1 fix given the spike (options: tangent-plane step D/E with B base /
  keep B and fix the account of it / change the objective first). **Supervisor (mzargham),
  verbatim:** "Change the objective first". Disposition: a second spike round on the alternation's
  objective (candidates: slack over near-frontier rows only; support-weighted slack; the entropic
  soft minimum of the slacks, the method's own kind of weighting) measured with the B and D steps
  on the planted seeds, in particular whether the planted partition becomes the optimum on seeds
  1, 3, 8 and 16, and on the cubesat tables; the fix is chosen after it; acceptance waits.
- Spike round 2 delivered (`docs/superpowers/notes/spike-objective/README.md`, scripts and tables
  beside it). Findings in brief: three of the four candidate objectives (support-weighted slack,
  the entropic soft minimum of slacks, the per-facet support-gap sum) are identically zero at
  τ = ∞ and discriminative rather than edge-tight at finite τ; the step that minimizes them
  destroys the fit (0 of 20 planted, 5 signatures of 5 on the cubesat). Seeds 1 and 16 are not
  identifiable from their frontier rows (3 and 2 rows for a facet in R^4), so no objective or
  restart recovers them; seeds 3 and 8 are identifiable and are recovered by selecting among
  restarts with an edge count (exact touches or band mean) with mean slack as tie-break, at τ = ∞:
  18 of 20 with the built step B. Only mean slack (built) is monotone under B; nothing is monotone
  under the tangent-plane step D. The mean slack is the honest K > 1 analogue of the K = 1 reach
  (the one-sided volume between cloud and envelope); the interior rows it uses are the only
  information that locates a facet with fewer than d frontier rows. The cubesat main basin is
  unchanged under every sensible selector. Ranking offered: keep mean slack, add an edge-count
  restart selector at τ = ∞ (4 to 5 lines); or keep everything and make the planted generator and
  R-1 state the identifiability condition (≥ d + 1 frontier rows per facet); or D with a selector,
  non-monotone. Put to the supervisor.
- Driver's question on the G-1 fix given round 2 (options: keep mean slack and add an edge-count
  restart selector / keep everything and fix the generator and the claim / tangent-plane step with
  edge selection). **Supervisor (mzargham), verbatim:** "keep both B and D in the code base, and
  evidence base but paper should focus on the mean slack approach because of the monotone
  guarantee"
- **Disposition (G-1 decided: fix before acceptance, as Amendment 1 of the scope):** the solver
  keeps the built per-facet step B (supporting hyperplane of all rows, tightest on the facet's
  rows; mean-slack objective; monotone) as the default and adds the tangent-plane step D (direction
  from the facet's near-frontier rows where it has at least d + 1 of them, B otherwise; no monotone
  objective) as a keyword option; both are tested on the planted data and both spikes' evidence
  enters the documentation; the paper (WP10) presents the mean-slack approach because of the
  monotone guarantee and names D as the evidence-driven alternative. Details the supervisor did not
  state are defaults in the amendment (keyword name, the identifiability condition in the planted
  generator and in R-1, the recovery claim quoted as measured). The whole review is rerun after the
  fix (work-acceptance rule).

## Acceptance gate, second review (2026-11-08)

- Review of record: `work-packages/WP9-review.md`, "Second review (after Amendment 1)" (b61df28;
  CI green at run 42525071154 on 27d5b04). Driver's own checks: 1115 passed, 11 skipped, 1 xfailed;
  ruff, format, lock clean; attribution grep 0 over 3bebe3e..HEAD.
- **G2-1 (recovery 16 to 17 of 20 against "works in practice for small K").** Options: accept as
  is / fix before acceptance / follow-up package. **Supervisor (mzargham), verbatim:** "accept as is
  and document why, document the option to do more restarts etc. this is a good \"good enough\"
  result we just need to make sure we understand it and that this understanding is documented".
  Disposition: accepted as is, with a documentation condition checked by the driver before the
  acceptance record: the docs state why recovery fails (thin facets, a local optimum), and name the
  options an analyst has (more restarts, a better start, the tangent step), so the understanding is
  recorded.
- **G2-3 (R-6 literal wording; six old test lines changed).** Options: accept as is / fix before
  acceptance. **Supervisor (mzargham), verbatim:** "Fix before acceptance". Disposition: fix is
  separate work and the review is rerun; the driver asks one question a level up on which of the
  six edits must be undone, since two are forced by the feature existing (the not-implemented test
  and the lemma ceilings).
- On the driver's question which edits the G2-3 fix must undo. **Supervisor (mzargham),
  verbatim:** "i am unclear about what you are proposing and why. lay out in detail for me what you
  are proposing we do and why". Disposition: the driver lays out R-6, the six edits, why each was
  made and what undoing each would mean, in chat, before asking again.
- After the driver's lay-out of R-6 and the six edits. **Supervisor (mzargham), verbatim:** "i think
  the lemma count is arbitrary and i don't want you to mess up the logical structure or clarity to
  game a metric". Disposition: no restructuring of tests or ledger to satisfy R-6's literal wording;
  the lemma-count ceilings stay as edited numbers; the driver asks what the G2-3 fix is, since the
  tests are not it.
- Driver's question: what the G2-3 fix is (fix the requirement / restore the audit's meaning only /
  accept as is). **Supervisor (mzargham), verbatim:** "start by relaxing artificial constraints
  then tell me what gap remains and propose how to address remaining gaps". Disposition: Amendment 2
  restates R-6 to its intent (K = 1 results and the notebook unchanged; pre-existing K = 1
  assertions intact; edits forced by approved deliverables listed with their reasons) and drops
  "additions only" and the hard-coded lemma counts as constraints; the driver then names the gap
  that remains and proposes how to address it.
- The driver named the remaining gap (the ledger's new "solver level" class is printed by the chain
  runner but defined nowhere a reader of the ledger looks) and proposed a paragraph in the
  proof-conventions note and a sentence on the method page, plus the `n_restarts` keyword for the
  G2-1 condition. **Supervisor (mzargham), verbatim:** "Yes, do that and rerun the review".
  Disposition: G2-3 fix = document the solver-level ledger class where the ledger's rules live; G2-1
  condition = `n_restarts` (default 5) on `solve_terms` and the estimator, with the docs naming more
  restarts as the analyst's option; a fresh third review of the delta; then the gate resumes with
  G2-7 and the bundle.
- Third review delivered (`WP9-review.md`, "Third review"; commits bdf17b2 and 96044fe; CI green at
  run 42528218236). Driver's own checks: 1116 passed, 11 skipped, 1 xfailed; ruff, format, lock
  clean; attribution grep 0 over 3bebe3e..HEAD; the solver-level ledger class is defined in
  `proof-conventions.md` and cited on the method page; `n_restarts` exists with default 5. G3-1
  (the reviewer found that more restarts do not recover seeds 1, 3, 16 and can lose seed 8, so the
  docs now call `n_restarts` a cost-for-robustness knob with the measured limits): fixed by the PM
  before hand-back; noted here as the kind of understanding the supervisor asked to have documented.
- **G2-7 (τ not re-selected at K; stock log-plane figure legibility).** Options: follow-up package
  and WP10 figures / fix before acceptance / accept as is. **Supervisor (mzargham), verbatim:** "Fix
  before acceptance". Disposition: Amendment 3 of the scope: the cubesat record re-selects τ at each
  K by the same criterion as at K = 1 (a target fraction of designs above V = 1, now of the K-facet
  envelope), reports the re-selected fits as the record and keeps the fixed-τ table as the
  diagnostic that shows why; the log-plane figures draw each facet's envelope only in slices where
  that facet has weight on both plotted metrics, or choose slices that have it; a fresh fourth
  review of the delta; then the bundle and acceptance.
- Fourth review delivered (`WP9-review.md`, "Fourth review (after Amendment 3)"; commits a15566b
  (E-4), 094e86d (Amendment 3) on main before the dev-branch rule reached the PM, c4133c8 (review,
  two figure titles, status) on dev; manual Tests run on dev green at 42531411476; main CI green at
  094e86d). Driver's own checks on dev: 1122 passed, 11 skipped, 1 xfailed; ruff, format, lock
  clean; attribution grep with the CI pattern 0 over the package. Re-selected τ: primary 38.10 /
  113.22 / 195.18 and stock 41.72 / 78.75 / 162.78 for K = 1 / 2 / 3, each with about a tenth of
  designs above the envelope; the peak-slew-power facet's share rises under re-selection (primary
  0.669 → 0.778, stock 0.161 → 0.590); every facet visible in at least one log-plane panel. Fourth
  review gaps: G4-1 stale figure titles (fixed), G4-2 the reports use K = 1's band because 1/τ_K
  leaves some facets with 3 to 6 designs (accept; carry into WP10), G4-3 the peak-slew-power slices
  are legible but uninformative (accept), G4-4 long lines in method.md (accept), G4-5 τ re-selection
  on Linux as a watch item (accept). No component of G2-7 remains.
- **Bundle of the remaining items** (first review G-2, G-3, G-8, G-9; second review G2-2, G2-4,
  G2-5, G2-6, G2-8; G3-1 and G4-1 fixed before hand-back; fourth review G4-2 to G4-5). **Supervisor
  (mzargham), verbatim:** "Accept the bundle as is". Disposition: all accepted with the reviewers'
  reasons; G4-2 (the reports use K = 1's band) and G4-3 (two uninformative slices) carried into
  WP10's figure and band decisions.
- Loop status: G-1 (Amendment 1), G2-3 (Amendment 2, docs of the solver-level ledger class),
  G2-1 (documented understanding, `n_restarts`), G2-7 (Amendment 3), E-4 (folded in) all closed;
  no open item remains before the acceptance question.

## Acceptance (acceptance gate)

- **Reviews of record:** `work-packages/WP9-review.md`, first review (28caf5b), second (b61df28, after
  Amendment 1), third (96044fe, after Amendment 2), fourth (c4133c8, after Amendment 3 and E-4).
- **Delivery:** `main` cbd618c..094e86d plus `dev` c4133c8 and the records; merged into `main` with
  a no-ff merge after this acceptance.
- **Date:** 2026-11-08.
- **Driver's question:** "WP9, the posynomial solver for K > 1, with Amendments 1 to 3 and the E-4
  correction: four reviews, every gap dispositioned, no open item. Do you accept the work?"
- **Supervisor (mzargham), verbatim:** "Accepted"
- **Disposition:** accepted. Carried forward: G4-2 and G4-3 into WP10; candidates for later
  packages (from the PM's reports): a K-specific target fraction, a better start for thin facets,
  nonsmooth search on the ridges, a K-selection helper, a readable multi-metric envelope plot,
  scalability and performance, kernels; the external review's items E-1 to E-10 (E-4 done) into
  WP13.
