# WP4 — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Scope approval (approval gate)

- **Document:** `work-packages/WP4-scope-of-work.md` (draft committed by the PM).
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

## Scope amendment 1 (approved at the acceptance gate)

- **Date:** 2026-11-08. Review: `work-packages/WP4-review.md` (second pass, cbedabe) found R-2 and
  R-9 wrong as written (both originated in the driver's plan): the baseline (Kp, Kd) = (1, 10)
  settling pin of 201.6 s is wrong (source repo pins 310.6 s; reviewer reproduced 310.626 s), and
  rtol 1e-6 cross-machine reproducibility is unachievable (CI differs by up to 2.6e-5 on
  control_effort and 6.1e-3 on torque_saturated_frac).
- **Supervisor (mzargham), verbatim choice:** "310.6 pin; per-column tolerances"
- **Disposition:** amend R-2 to 310.6 ± 0.5 s and correct `docs/superpowers/notes/adcs-port.md`;
  amend R-9 to rtol 1e-4 on continuous columns with a looser tolerance for `torque_saturated_frac`
  only, plus same-platform exactness on 40 designs. Review gaps G-3 (observations O-1 to O-9) are
  re-listed by the rerun review. The whole review reruns after the amendment and the test change.

## Review gaps, round 2 (third review, 9680193, against Amendment 1)

- **Date:** 2026-11-08. R-1..R-13 met. Observations O-3..O-10 put to the supervisor as one item
  (together with WP2 G-5 and WP5 O-6..O-8).
- **Supervisor (mzargham), verbatim choice:** "Fix WP2 tolerance to 1e-10" (i.e. the WP4 observations accepted as is)
- **Disposition:** O-3..O-10 accept as is; the committed CSV is the authoritative dataset.

## Acceptance (acceptance gate)

- pending `work-packages/WP4-review.md`
