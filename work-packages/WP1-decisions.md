# WP1 — Decision records

Records typed by the agent (driver session, Claude Fable 5.1, 2026-11-07). Decisions are the supervisor's.

## Scope approval (approval gate)

- **Date:** 2026-11-07
- **Document:** `work-packages/WP1-scope-of-work.md` at commit 0b181d7 (draft 3), presented in chat
  with its Agent's defaults list as one item.
- **Supervisor directions incorporated before approval, verbatim:**
  - "your plan seems to be focused on enums and point evaluations rather than abstract values. we're
    using sympy so you don't need to enumerate values, you can use abstract spaces"
  - "you should not import from symproof but you may find some useful real analysis and convex
    analysis you can steal or mimick there"
  - "we do not strictly need our theoretical results to match our implementation. [...] we need to use
    the theory to ground our work but its okay for us to have criteria in our theorems that we don't
    know for sure are true. we need to explain why they help us understand and interpret our results
    (including the limitations of our method)"
- **Supervisor (mzargham), verbatim:** "OK"
- **Disposition:** approved; defaults list approved as one item; open decisions: none.

## Review gaps (decision loop at the acceptance gate), round 1

- **Date:** 2026-11-08
- **Review:** `work-packages/WP1-review.md` at dcfd527 (delivery 5e901aa..2e2eafc).
- **Item G-5** (affects good enough: L8 round trip asserted by self-comparison with a permissive
  check; L3/L4/L5 sub-claims resting on stated premises). Driver's assessment given: L3/L4/L5 sound
  and honestly labelled; L8 round trip is a test that cannot fail.
- **Supervisor (mzargham), verbatim:** "Fix L8 before acceptance"
- **Disposition:** fix before acceptance (inherited axiom for the square-matrix inverse step, round
  trip asserted from it, permissive escape removed, spec note that the strict LSE − max > 0 needs
  n ≥ 2). The whole review reruns after the fix; G-1 to G-4 and G-6 to G-8 are re-listed then.

## Review gaps, round 2 (after the L8 fix)

- **Date:** 2026-11-08
- **Review:** rerun by a fresh reviewer after the L8 fix. New gap G-9: the L8 fix commit carried a
  "Co-Authored-By: Claude Sonnet 5.5" trailer added by an implementer subagent, failing R-16.
- **Supervisor (mzargham), verbatim:** "Rewrite the message and force-push"
- **Disposition:** fix before acceptance. The driver rewrote the message (bd953c4 → 82fdd47, tree
  identical), rebased the two later commits (cc2453a → 2d12409, d9bcf63 → e534dee) and force-pushed
  main with a lease on d9bcf63. A CI step now fails any push whose history contains an attribution
  line. The whole review reruns again; G-1 to G-8 are re-listed then.

## Review gaps, round 3 (third full review, after the history rewrite)

- **Date:** 2026-11-08
- **Review:** `work-packages/WP1-review.md` (696aa1f); D-1..D-6 met, R-1..R-16 met.
- **G3-7** (documented premises in L3/L4/L5/L10): decided by the supervisor's round-1 disposition
  "Fix L8 before acceptance", which selected only the L8 derivation and the L5 n ≥ 2 note for fixing;
  the rest stand as documented premises and ledger conditions. Disposition: accept as is.
- **G3-1, G3-2, G3-3, G3-4, G3-5, G3-6, G3-8** put to the supervisor as one item.
- **Supervisor (mzargham), verbatim:** "Accept all as is"
- **Disposition:** accept as is. Reasons: CI edits are the driver's maintenance of a WP0 deliverable;
  the helper module and the added axioms (A0, A7, I5, I6, F5, F10) were anticipated by the scope's
  defaults and are all in the ledger; the spec's per-lemma axiom lists are updated to match the
  ledger in WP6; the `range(` uses do not enumerate sizes.

## Acceptance (acceptance gate)

- Review recommends acceptance with the listed gaps noted; every gap has a disposition.
- Acceptance act named in the scope: verbal acceptance in chat.
- **Date:** 2026-11-08
- **Supervisor (mzargham), verbatim:** "i accept"
- **Status:** accepted. WP1 is done.
