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


## Approval-record note (driver, 2026-11-08)

The reviewers flagged the approval wording as conditional. The condition ("double check with the
github cli") was satisfied before execution started: the driver ran `gh api .../check-runs` and
`gh run list` and reported to the supervisor that the head of main was green and only superseded
run 36 had failed; execution was dispatched after that report. Dates: commits are stamped in UTC,
the chat happened on the evening of 2026-11-07 local time.

## Review gaps, round 1 (decision loop at the acceptance gate)

- **Date:** 2026-11-08. Review: `work-packages/WP2-review.md` (second pass, e84bd7f).
- **Items put as one question:** G-1 approval wording; G-2 the chain cross-check overwrites fitted
  attributes for L1/L7 (checks formulas, not fitted values); G-3 documented departures from
  defaults; G-4 one intermediate red commit.
- **Supervisor (mzargham), verbatim choice:** "Fix G-2 before acceptance"
- **Disposition:** G-2 fix before acceptance (add a cross-check comparing a real fit's outputs to the
  L1/L7 formulas); G-1, G-3, G-4 accept as is. The whole review reruns after the fix.

## Review gaps, round 2 (third review, ea3105b)

- **Date:** 2026-11-08. G-2 verified fixed. New item G-5: fitted-model cross-check tolerance 1e-9
  vs R-16's 1e-10; chart-inverse formula derived inside the test. Put to the supervisor together
  with the WP4 and WP5 observations as one item.
- **Supervisor (mzargham), verbatim choice:** "Fix WP2 tolerance to 1e-10"
- **Disposition:** fix before acceptance (tolerance set to 1e-10); the whole review reruns.

## Acceptance (acceptance gate)

- Review: `WP2-review.md` (fourth pass, 39fa0c3), recommends acceptance; no pending gap.
- Acceptance act named in the scope: verbal acceptance in chat.
- **Date:** 2026-11-08
- **Context:** the driver presented four gates together (accept WP2; approve WP3, WP6 and WP4b with their defaults lists as one item each) and said one line could cover all four.
- **Supervisor (mzargham), verbatim:** "okay proceed"
- **Status:** accepted. WP2 is done.
