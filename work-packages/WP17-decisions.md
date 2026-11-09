# WP17 — Decision records and delivery notes (the several-term fit with soft weights)

Delivery notes by the package implementer; factual. Decisions are the supervisor's.

## Origin

Scope: `WP17-scope-of-work.md` (R-1 to R-9, R-7 and R-8 as amended). Evidence:
`docs/superpowers/notes/spike-ggp-fit/report.md`, `docs/superpowers/notes/spike-soft-fit/report.md`
and its addendum. The supervisor's words are quoted in the scope of work and are not repeated here.

## Delivery notes (implementation)

- **R-2 first.** Before any code changed, `tests/data/soft_fit_default_reference.npz` recorded the
  fitted attributes at the default `term_temperature = inf`: `exponents_`, `log_offset_`,
  `objective_`, `mean_slack_`, `facet_`, `support_weights_`, `n_iter_`, `facet_share_`,
  `conditioning_` and every `Termination` field (status, reason, numbers, `gaps`, `shares`), for
  K = 1, 2, 3 at tau = inf and 50 on planted tables 0 to 5 (400 x 4, three terms, `facet_step`
  support), the tangent step at K = 3, tau = 50, one K = 2, tau = 10 table, and the four cubesat
  fits (primary and stock, K = 2 and 3, tau re-selected). Commit 45ef866. After the change the
  same fits are recorded again and compared: 1273 arrays, `np.array_equal` (NaN equal), all equal.
  `tests/test_soft_fit.py` asserts it: bit-identical on the arm64 Mac that recorded it and in the
  environment of record (`HTS_ENVIRONMENT_OF_RECORD=1`); elsewhere the floats agree within 1e-12
  and the discrete fields (status, facet labels) are equal; the iteration counts are compared on
  the exact path only.
- **Trigger and scope of the soft fit.** A finite `term_temperature` with `n_terms > 1` and
  `facet_step="support"` (the agent's default of the scope of work: no new parameter).
  `facet_step="tangent"` ignores kappa in the fit (the tangent step is defined on labels; its
  `mean_slack_` is the slack of the reported model like any finite kappa).
- **Statuses.** The new status is `"stationary"` (WP17 R-7). It is distinct from the label fit's
  `"stationary_without_margin"`, which never occurs for a soft fit. A soft fit at tau = inf, or
  with a penalty, is `"not_applicable"`. The field `min_curvature` is added to `Termination`
  (default `nan`, so existing constructions are unchanged). Positive curvature means above
  `EPS_FEAS` (1e-9); the gaps are the unscaled per-term gaps `G_k` of the weighted refits, within
  `EPS_KKT`. Terms with weight mass below 1e-9 rows count in `n_empty` with gap `nan`.
- **Polish.** The joint reduced-Newton polish on `H = D - kappa M` runs after the alternation, also
  when the alternation reached its iteration cap; a cap whose polished point meets the first-order
  test is judged by the second-order test (the tests do not depend on how the point was reached)
  and `success` is true. Without it the alternation alone stops near a gap of 1e-6.
- **Contract.** Version 6 (`work-packages/interface-contract.md`, `.toml`): the field, the status,
  the four `solvers` names (`soft_weights`, `soft_objective`, `soft_hessian`, `soft_certificate`),
  the two meanings of "certified" and the meaning of a finite `term_temperature`.
- **Tests that changed.** None of the existing assertions was weakened. `tests/test_sklearn_compat.py`
  gains one estimator (the soft fit at a finite temperature) with the same, empty, expected-failures
  dict.
- **Not done here (coordinated by the PM).** The scripted lemma step (R-8) and Appendix B; the words
  of R-9 (user guide fitting page, API prose, glossary, section 6 of the paper); only the
  termination page's status rows, the fields row and the API line were added, within the budgets.
