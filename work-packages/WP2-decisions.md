# WP2 — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Pre-approval decisions (2026-11-08, while the WP2 scope was at the gate)

- **Class name.** Supervisor, verbatim: "2. rename HTS (HyberbolicTradeSpace) is a good name. i will
  rename the repo too." Disposition: the estimator class is `HyperbolicTradeSpace`.
- **Package name.** Asked whether the Python package should follow the repo rename before WP2 writes
  code. Supervisor's choice: "Rename package to hyperbolic_trade_space". Disposition: distribution
  `hyperbolic-trade-space`, import `hyperbolic_trade_space` (alias `hts` in docs); "posynomial
  invariant form" remains the name of the method/representation. Applied by the driver across the
  repo (package directory, pyproject, docs, notes, scopes) in one commit; the git remote and local
  repository path keep the old name until the supervisor renames the GitHub repository.

## Scope approval (approval gate)

- **Document:** `work-packages/WP2-scope-of-work.md` at 67fff4e.
- **Date:** 2026-11-08
- **Context:** the driver presented the WP2, WP4 and WP5 scopes together, asked for explicit
  confirmation of the WP4 physics additions (SRP torque 1e-5 N·m in the analytic pointing budget,
  pointing error = RSS of the steady-state error and the star-tracker floor, control effort ∫‖τ‖dt
  as the power proxy, peak wheel momentum as a feasibility flag, illustrative hardware classes; SRP
  not in the simulated dynamics), and listed the approvals as pending. The naming decisions were
  taken separately (see WP2-decisions.md).
- **Supervisor (mzargham), verbatim:** "double check with the github cli but then let's move forward"
- **Disposition (driver's reading, stated to the supervisor):** approval of this scope and its
  Agent's defaults as one item; for WP4, confirmation of the physics additions. Open decisions: none.

## Acceptance (acceptance gate)

- pending `work-packages/WP2-review.md`
