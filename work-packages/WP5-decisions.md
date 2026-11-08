# WP5 — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Scope approval (approval gate)

- **Document:** `work-packages/WP5-scope-of-work.md` (draft committed by the PM).
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

- **Date:** 2026-11-08. Review: `work-packages/WP5-review.md` (1c71306).
- **Items put as one question (G-2 to G-5, touching R-5/R-6):** COLS attribution to Aigner & Chu
  1968 unconfirmed (driver's plan error; COLS is usually attributed to Richmond 1974 / Greene 1980,
  to be verified); no Pareto gap/spacing source; Ross et al. called "closest named prior art"
  without support; Magnani & Boyd cited after the project's own mathematics; Aigner & Chu 1968 and
  Cobb–Douglas 1928 on secondary records.
- **Supervisor (mzargham), verbatim choice:** "Fix before acceptance"
- **Disposition:** fix before acceptance: verify and add COLS and spacing-metric sources, drop the
  unsupported superlative, move the Magnani & Boyd citation, label secondary-record entries; the
  driver corrects the spec attribution once WP5 reports the verified sources. G-1 and G-6 accept as
  is (approval note above; minor items). The whole review reruns after the fix.

## Review gaps, round 2 (second review, 1783375)

- **Date:** 2026-11-08. G-2..G-5 verified fixed. Observations O-6..O-8 put to the supervisor as one
  item (together with WP2 G-5 and WP4 O-3..O-10). The driver corrected the spec §4 COLS sentence to
  the verified sources (7f3d589).
- **Supervisor (mzargham), verbatim choice:** "Fix WP2 tolerance to 1e-10" (i.e. the WP5 observations accepted as is)
- **Disposition:** O-6..O-8 accept as is.

## Acceptance (acceptance gate)

- Review: `WP5-review.md` (second pass, 1783375), recommend acceptance with the listed gaps noted; every gap has a disposition.
- Acceptance act named in the scope: verbal acceptance in chat.
- **Date:** 2026-11-08
- **Supervisor (mzargham), verbatim:** "accept" (given for WP4 and WP5 together, after the driver
  presented both gates in one message)
- **Status:** accepted. WP5 is done.
