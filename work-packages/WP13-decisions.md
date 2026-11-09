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

## Delivery notes (PM, factual; not decisions)

- Execution on `dev`: commits "WP13: ..." from c61ff49 to c3cbec4; the fresh-context review is `WP13-review.md` (40062f6); the response letter is in `external-review-2026-11.md`.
- Deviations from the scope's wording, for the acceptance gate: (1) a sixth termination status `uncertified` (fixed assignment, gap above EPS_KKT) beyond the five listed; (2) margin positivity implemented as gamma > EPS_FEAS (1e-9) rather than gamma > 0; the two readings coincide on all planted data; (3) the guard tolerance moved planted seed 8 at tau = inf, step B, from certified to stationary_without_margin (recovery 17/20 to 16/20; disclosed in the method page and the letter); (4) per-reach values in the K = 2, 3 cubesat record moved at the sixth decimal only (ten values, listed in `docs/superpowers/notes/k3-cubesat.md`).
- Review gaps G-A to G-D fixed in c3cbec4 (format, ledger sd labels, stale ranges, register wording in README and spec).

## Acceptance gate (2026-11-08)

- Review of record: `work-packages/WP13-review.md` (40062f6; R-10 re-check appended in 1406261,
  letter fixes 19747fe). Delivery: `dev` c61ff49..655d978 (29 commits incl. the four draft scopes and
  records). Manual Tests run on dev green at 42541989924 (655d978); two earlier dev runs failed on
  Linux-only platform ties (a floored-gap test against a hard-coded tolerance; a tied-row argmax
  counted as an assignment change; a tied τ = ∞ seed stopping at the iteration cap), fixed by
  comparing against the module tolerances and by accepting either stop status on zero-margin seeds;
  recorded as evidence under ledger gap G-10. Driver's own checks on 655d978: 1188 passed, 11
  skipped, 1 xfailed; ruff, format, lock clean; ALL LEMMAS PASS; attribution grep 0.
- Measured (planted data, 20 seeds): max facet gap after the polish 2e-15 (τ = ∞) and 5e-15 (τ = 50);
  certified 20/20 at τ = 50 and 16/20 at τ = ∞ with seeds 1, 3, 8, 16 stationary without margin;
  the LP gap equals the duality gap to 1e-12; labels unchanged under 100 perturbations within the
  radius on every fit; the Corollary bound holds on all 40 fits. Cubesat K = 2, 3: all certified; only
  ten reach values moved at the sixth decimal; K = 1 unchanged.
- **Bundle (G-E, G-I, platform ties as ledger G-10, G-F).** **Supervisor (mzargham), verbatim:**
  "Accept the bundle as is". Disposition: accepted with the reviewers' reasons; no open item remains
  before the acceptance question.
