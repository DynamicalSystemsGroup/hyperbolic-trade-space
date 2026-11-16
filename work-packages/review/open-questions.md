# Open questions that left the paper's narrative

One entry per item: the section it left, what is open, and its record. WP57 decides what enters the appendix section
"Assumptions, limitations and open questions".

## OQ-1. The outer loop of the search: outward in expectation

- **Left:** Section 7, "Search of the design space (preliminary)", removed by WP54; the search now appears once, as the
  first direction of Future work, without this point.
- **Open:** the loop (propose, evaluate, append the row, refit) is not expected to move outward at every step; it may
  move inward on a step. The conjecture is that it is a submartingale, outward in expectation. No conditions under which
  it holds are derived.
- **Record:** `work-packages/WP36-decisions.md`, "The search's outer loop" (the supervisor, 2026-11-14, 12:20);
  `work-packages/WP41-rounds/spike/readout.md`, sections 1 and 5; `docs/bridge.md`, "The outer loop, and what is open".

## OQ-2. A convergence result when the expected progress ceases

- **Left:** the same section, its closing sentences ("A convergence theorem for the nested scheme is a goal").
- **Open:** a convergence result for the nested scheme, once the expected progress ceases. No conditions are derived,
  and the theory treats variables as continuous within a category.
- **Record:** `work-packages/WP36-decisions.md` (same entry); the gaps ledger row that names it
  (`docs/superpowers/notes/abstraction-gaps.md`).

## OQ-3. Ascent may reach only the log-convex part of the Pareto boundary

- **Left:** the same section.
- **Open:** whether a move along the ascent direction can reach beyond the log-convex part of the boundary; a design
  built to reach a predicted improvement need not follow it, which only the check finds out.
- **Record:** `work-packages/WP41-rounds/spike/readout.md`, sections 3 and 5 (one run each on three targets, a record
  and not a rate; the rule that reaches farthest and the confirmation rate are not established).

## OQ-4. How a sampling strategy enters the nested loops

- **Left:** the same section (the sentence that the method assumes nothing about how designs were drawn).
- **Open:** how a sampling strategy enters the search loops is not studied; the method itself assumes nothing about how
  a table's designs were drawn.
- **Record:** `paper/length_ledger.toml`, the raise row of 2026-11-11 (the supervisor, 12:25).

## OQ-5. Global convergence of the several-term alternation (Q1)

- **Left:** Section 6, Results, the subsection "Open questions" (WP55), where it stood as Q1, "not pursued".
- **Open:** whether the alternation converges globally. The levels of guarantee are local: descent (L15), the term gap
  (L12) and local optimality with the cells held fixed (L13, L14), and a finite stop is a pigeonhole count, not a
  practical bound. Section 6 keeps the sentence that stationarity of the stop and convergence otherwise are not claimed.
- **Record:** gaps ledger G-14 (`docs/superpowers/notes/abstraction-gaps.md`; Appendix E of the paper);
  `work-packages/external-review-2026-11.md`, item E-10.

## OQ-6. Statistical consistency under noise and refitting (Q2)

- **Left:** Section 6, the subsection "Open questions" (WP55), as Q2.
- **Open:** a consistency theorem for the fit under noise and refitting. L6 gives the population cumulant identity and
  L20 the first-order size of the noise shift of the minimizer of the expected noisy loss; neither is a statement about
  one noisy fit.
- **Record:** gaps ledger G-11; `work-packages/external-review-2026-11.md`, item E-10.

## OQ-7. Identifiability of the active metrics under finite, biased observations (Q3)

- **Left:** Section 6, the subsection "Open questions" (WP55), as Q3.
- **Open:** whether the contending set is identified from a finite, biased sample. It is identified only where the
  restricted Hessian is positive definite (R3) and the term's frontier rows determine its plane.
- **Record:** gaps ledger G-12; `work-packages/external-review-2026-11.md`, item E-10.

## OQ-8. When the fitted reference surface recovers the Pareto boundary (Q4)

- **Left:** Section 6, the subsection "Open questions" (WP55), as Q4.
- **Open:** the conditions under which the fitted reference surface recovers the Pareto boundary and not the supporting
  envelope of the sample. Recovery is measurable only where the boundary is planted; real data have no known boundary.
- **Record:** gaps ledger G-13; `work-packages/external-review-2026-11.md`, item E-10.

## OQ-9. The tie at the exact maximum for several terms

- **Left:** Section 5, Methods, "Thresholds and ties" (WP55 revision), where it stood as "gap G-10".
- **Open:** when several terms are fitted at the exact maximum the solver resolves a tie by a fixed tie rule; that the
  contending sets do not depend on the rule is checked on the case, not proved.
- **Record:** gaps ledger G-10 (`docs/superpowers/notes/abstraction-gaps.md`; Appendix E of the paper).

## OQ-10. A log-convex surface only

- **Left:** Section 5, Methods, the "Simplifying assumptions" paragraph, item (vi) (WP55 revision).
- **Limit:** the fitted surface is log-convex, since the logarithm of the posynomial is convex in u = log m; no number of
  terms K represents structure that is not log-convex.
- **Record:** Appendix B, L10 (the posynomial extension); `work-packages/review/open-questions.md` is its place until
  WP57 decides the appendix section "Assumptions, limitations and open questions".
