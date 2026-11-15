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
