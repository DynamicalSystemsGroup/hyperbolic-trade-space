# WP43 — Decisions: beyond the posynomial, the kernel direction tested (a research spike)

Verbal approvals and rulings, quoted verbatim, with the assistant's reading of each ("Applied as").

## The question and the direction (2026-11-14, 13:40 to 13:55)

**Supervisor, verbatim (13:40), with the redrawn Figure 5 attached:** "we'll come back to the negative curvature thing
in a moment. i want to address something else first. this is related to building out the scope boundary between 0.1
and future work, as well as ensuring our implementation is extensible without major reimplementation. / consider the
following drawing. the log affine fit is okay but actually there is still a curvature visible to the human eye.
supposing i wanted to pick a different kernel function something not just a posynomial so that when i fit that data it
hugged the curvature in the upper right right frontier of that data even though it bends down. what function would i
use and could i still solve my optimization if generalized my solver to support it? / this is research spike question
designed to test (and further define) or notion of moving beyond posynomial invariant forms to other generalized
geometric program invariant forms (or really anything we can find a solver to solve)."

**The assistant's answer, in short:** the downward bend is a concave edge in log units, which is what more terms give
(a second, steeper line; the case's K = 2 term 2 is it); the first kernel beyond a posynomial that keeps the fit convex
and the designer's problem convex is the log-quadratic invariant form, log V = w.u + (1/2) u'Qu - beta with Q positive
semidefinite and Q1 = 0, fitted as a conic program; it is not a posynomial, so the class's right name is "log-convex
invariant forms"; no kernel in that class bends the other way (a non-log-convex edge, assumption (vi)); the test is
out-of-sample slack on held-out rows, since in-sample slack falls with K by construction.

**Supervisor, verbatim (13:55):** "i want you to scope out the spike and work on more test cases. we're not going to
force this into the paper, instead its going to be used to further refine the implementation and to expand the example
cases in the documentation. the work is aimed at backing up some of our claims about alternatives in the paper without
introducing new complexity to the paper"

**Applied as:** WP43 is the research spike with test cases (the case's two regimes; planted tables with a piecewise
edge, a log-quadratic edge and a non-log-convex dent) and a readout at the decision gate. Its findings refine the
implementation (an extension point for the model's feature map and parameter set, built after the readout) and expand
the documentation's examples; the paper gains no result and no section. The paper's three sentences on alternatives
(the abstract's kernel sentence as the supervisor rewrites it; Section 10's "The kernel direction"; Section 12's
"kernels that keep the model a generalized geometric program (GGP) in the metrics") are the claims the spike backs or
narrows, by at most a word (GGP against log-convex). `WP43-scope-of-work.md` holds the scope; approval is the
supervisor's verbal word, quoted here when given.

## Approval (2026-11-14, 15:40)

**Supervisor, verbatim:** "i approve the Work Packages above. we can return to the open wording discussions"

**Applied as:** the scope as drafted is approved (WP41, WP43 and WP45 were the three listed; WP42 waits on its open
decision, the solver's word). Execution begins under `work-execution`: a unit per package in its own worktree on
Sonnet, in the background, with the scope file as the brief; the assistant verifies each delivery before the
supervisor's acceptance.
