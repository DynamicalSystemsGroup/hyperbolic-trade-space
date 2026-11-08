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
