# WP3 — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Scope approval (approval gate)

- **Document:** `work-packages/WP3-scope-of-work.md` (06dd10f and later).
- **Date:** 2026-11-08
- **Context:** the driver presented four gates together (accept WP2; approve WP3, WP6 and WP4b with their defaults lists as one item each) and said one line could cover all four.
- **Supervisor (mzargham), verbatim:** "okay proceed"
- **Disposition:** approved; defaults list approved as one item; open decisions: none.

## Review gaps, round 1 (2026-11-08)

- **Review:** `work-packages/WP3-review.md` (a0db131). Items: G-2 `frac_above_` overshoots 0.5 below
  τ ≈ 3, disclosed only in a test comment; G-3 no true beyond-frontier novelty test (generator never
  exceeds log V = 0); G-4 observations; G-1 approval wording.
- **Supervisor (mzargham), verbatim choice:** "Fix G-2 docs before acceptance"
- **Disposition:** G-2 fix before acceptance (document the small-τ overshoot in the docs and the
  `select_temperature` docstring); G-3 follow-up candidate (needs WP2's generator); G-1, G-4 accept
  as is. The whole review reruns after the fix.

## Review gaps, round 2 (review 4fbc6ea)

- Items: G-5 the docs fix also edited WP6's limitations page and that push went red (fixed next
  commit); G-6 `select_temperature` default lower bound 0.1 below the recommended τ ≈ 3 without
  saying so; G-3 follow-up (planted beyond-frontier novelty test needs WP2's generator).
- **Supervisor (mzargham), verbatim choice:** "Fix G-6 docstring line, accept the rest"
- **Disposition:** G-6 fix before acceptance (one docstring sentence); G-5 accept as is; G-3 on the
  follow-up list. The whole review reruns after the fix.

## Acceptance (acceptance gate)

- Review: `WP3-review.md` (third pass, a63f6f5), recommends acceptance; G-3 on the follow-up list.
- Acceptance act named in the scope: verbal acceptance in chat.
- **Date:** 2026-11-08
- **Supervisor (mzargham), verbatim:** "accept" (given for WP3 and WP6 together, after the driver
  presented both gates in one message)
- **Status:** accepted. WP3 is done.

## Follow-up candidates

- G-3: a planted beyond-frontier row for a true novelty test needs a hook in WP2's `datasets.py`
  generator (not in WP3's scope).
