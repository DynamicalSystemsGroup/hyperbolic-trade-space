# WP13 — Decision records (response to the external review)

Records typed by the agent (driver session). Decisions are the supervisor's.

## Origin (2026-11-08)

- The third-party review, saved verbatim with its paper map in
  `work-packages/external-review-2026-11.md`, was triaged item by item with the supervisor on
  2026-11-08 (every disposition quoted there). Nothing was declined; E-4 was corrected within WP9
  (a15566b); the standing position (formal statements exact; one abstraction-gaps ledger; the
  register for the words; the policy stated once) was adopted in his words. The breakdown places
  WP13 after WP9 and before WP14, WP8a, WP10 and WP12 (`work-packages/README.md`).

## Decision loop (2026-11-08)

- **Agent's defaults, as one item.** **Supervisor (mzargham), verbatim:** "Approve the defaults as
  listed". Disposition: approved. Loop closed: decided 0 (all items were decided in the external
  review's triage), deferred 0, raised 0, defaults approved as one item.

## Scope approval (approval gate)

- **Document:** `work-packages/WP13-scope-of-work.md` at commit 093e8d3 (no open items).
- **Date:** 2026-11-08.
- **Driver's question:** "WP13, the response to the external review: E-1 in full (...), E-2 (...), E-5
  (...), E-6 (...), E-7 as classified, the abstraction-gaps ledger, the register completed, the
  response letter; no open items. Do you approve the scope for execution?" (options: Approved / Not
  yet).
- **Supervisor (mzargham), verbatim:** "Approved"
- **Disposition:** approved; `work-execution` starts under the PM/implementer pattern on `dev`;
  the acceptance merge to `main` is the driver's.

## Process note (2026-11-08, not a WP13 decision)

- The supervisor, verbatim: "its supposed to be one PM not multiple PMs but then the implementers
  and reviewers are clean sub agents with specific tasks who are not allowed to deviate from their
  scopes without explicit approvals and PM makes sure it all works together. the fable level is my
  assistant who decides whether what the PM escalates actually needs to go to me or not."
  Disposition: the WP13 PM becomes the single PM across packages; it drafts the WP14, WP8a and WP10
  scopes through bounded subagents while WP13 executes, and later runs the approved packages
  concurrently; `PM-BRIEF.md` and the README carry the hierarchy.
