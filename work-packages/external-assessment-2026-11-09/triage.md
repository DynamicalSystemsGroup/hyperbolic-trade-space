# Triage of the independent assessment of 2026-11-09 (the driver, same day)

The supervisor ran "a concurrent independent review and test session with a clean context and a
different genai stack" and asked the driver to "go through it and harvest feedback". The assessment
(`assessment.md`, `verification.json`, copied verbatim beside this file) applied the package unchanged
to two outside cases (Filecoin weekly data; a RAI collateral replay) at commit c46832c and inspected
the history to b653e98. Its own framing: "inputs for author triage, not proposed release blockers".

What it confirms: the package runs on outside data without change; the termination distinctions are
useful in practice; the tension report refuses a facet with too few rows rather than manufacture an
answer; a sharp K sweep shows diminishing returns and repeated terms rather than rising error.

## Findings and dispositions

| # | Finding (the assessment's words, shortened) | What the repository has today | Disposition |
|---|---|---|---|
| A1 | Keep three claims distinct: numerical success on the objective (a certificate), descriptive success on the observed geometry, and predictive or decision usefulness outside the observations; the third needs its own validation. Certified fits with bad downstream reconstruction were observed. | The register separates the surface from the Pareto boundary; limitations say V above 1 is possible at finite temperature; the certificate's meaning is stated in the termination page. The three-way distinction is not stated in one place. | **Accept.** One short paragraph near fitting and termination in the paper (section 6 or the discussion) and on the docs' termination page; each sentence a claims-register row. |
| A2 | A one-term fit can select a flat cap (weights (0, 1), a monolemma) without the design space lacking a trade-off. | The tensions page names the monolemma; nothing says a cap can hide a trade-off elsewhere in the space. | **Accept.** One compact note with a planted cap-plus-slope example on the docs' fitting or tensions page; no economic case. |
| A3 | Requested K versus effective K: larger requested models repeat terms and report stationary_without_margin; show distinct terms and validation beside training slack. | The termination record reports n_empty and the margin; the paper's D.15 gives mean slack across K; no count of distinct terms is reported. | **Accept, small.** The termination record or the tension report gains the number of distinct terms (exponent vectors within a stated distance); the docs' K-sweep example and D.15 show it beside the slack. A new automatic selector is not in scope (the assessment agrees). |
| A4 | Soft term aggregation is unnormalized: duplicating a term improves the objective by log 2 / kappa without new geometry (0.0347 of a 0.0437 improvement in the Filecoin case). Document the convention and the duplicated-term calculation. | The paper's L10 states max <= Phi_K <= max + (log K)/kappa, so the fact is derived but not read as a bias. The project's own rule for the fit temperature is the opposite convention: log-mean-exp, never the unnormalized log-sum-exp. | **A decision for the supervisor** (it changes a definition in his paper): normalize the term aggregation as a log-mean-exp over the K terms, consistent with the rule for tau (a constant shift of log K / kappa; the default kappa = inf is untouched; soft fits' minimizers unchanged; cross-K comparisons honest), or keep the sum and document the effect as a convention note. Put to him below. |
| A5 | Equal training loss can conceal different boundaries: a five-facet envelope on the same rows had the same mean slack as the three-term fit and a different boundary. Reaching the loss floor does not identify every supporting facet. | The paper says the surface models the data and not the boundary; open question Q4 and the gaps ledger do not record this specific non-identifiability. | **Accept.** A ledger gap (G-18) with the assessment as its evidence, one sentence in the open questions, and a small frozen planted fixture that shows two envelopes with equal mean slack and different boundaries. No change to the objective now. |
| A6 | Inverting the finite-temperature reference into a bounded outcome is a downstream task that can fail while the certificate holds (impossible breach fractions at K = 5; 742 percent). State the responsibility and reject invalid intersections in an example. | The prediction page describes propose, predict and check; nothing warns that an inverted level can leave the quantity's admissible range. | **Accept.** One paragraph on the docs' prediction and limitations pages, and the check in the paper's propose-predict-check reading (Appendix D) that an intersection outside the admissible range is reported as invalid, never clipped. |
| A7 | Conditioning belongs to the question: a different geometric reference centre turned the one-term weights from a cap into a slope; a stable fitted direction is not a context-free discovery. Designed grid points are not independent observations. | The preconditioning note says rescaling one metric changes the geometry; the paper names conditioning as the analyst's step. | **Accept, wording only.** One sentence each in the paper's conditioning paragraph and the docs' conditioning page; one sentence in limitations on designed versus observed samples. |
| A8 | The assessment's study bundles resolve dependencies at installation and are not equivalent to the pinned container record; nothing was committed or sent externally. | The container of record is approved. | **No action.** Noted so no one cites the bundles as reproductions of the record. |

Deferred, with the assessment's agreement: automatic K selection or pruning; objectives that identify
unsampled boundary structure; probabilistic calibration; the economic studies themselves. Recorded as
candidates for after 0.1.

## Routing

A1 to A3 and A5 to A7 form one package, WP21, "response to the independent assessment", scoped by the
PM in the template and approved by the driver; its paper sentences go through the paper stream, its
docs sentences through the docs stream, the distinct-terms count through the package's owner with a
contract amendment, the fixture through the tests. A4 waits for the supervisor's answer.

## A4, the supervisor's answer (2026-11-09)

Driver's question: define the term aggregation as a log-mean-exp over terms, or keep the log-sum-exp
and document the duplicated-term effect. **Supervisor (mzargham), verbatim:** "really the package
should support both setups. think of it as weighted vs not weighted and normalized vs not normalized.
in practice these should be keyword based. it should be pretty normal stuff to toggle in scikit-learn
style unsupervised learning. you can also defer weighted versus not weighted since i dont think we have
that yet".

**Disposition:** A4 joins WP21 as a package item. A keyword parameter of the estimator selects the
term aggregation: unnormalized (the sum, today's behaviour and the default, so no committed number
moves) or normalized (the mean over the K terms, the same convention as the fit temperature);
stored verbatim and validated in `fit` as the scikit-learn conventions require; the interface
contract amended; L10 states the bound for both forms (sum: max <= Phi_K <= max + (log K)/kappa;
mean: max - (log K)/kappa <= Phi_K <= max); the paper's Definition 3 and the docs name the toggle in
one clause each; the duplicated-term effect is documented for the unnormalized form as the
assessment's note. Weighted versus unweighted terms (per-term weights in the aggregation) is
deferred, recorded as a candidate for after 0.1 (the supervisor: "you can also defer weighted versus
not weighted since i dont think we have that yet").

