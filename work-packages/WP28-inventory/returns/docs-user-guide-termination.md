# docs-user-guide-termination

## Q1. What does this page convey?

Every fit records how it stopped in `termination_` (and `conditioning_`): a status from a fixed list, built on three levels of assurance (descent, stationarity, conditional local optimality), with a field list and a note that a "certified" status covers only the local optimum of the objective, not held-out validity.

## Q2. Which sentence of the story does it serve?

Home: "reading what the fit reports" (User guide: one page per task). Loosely also the root page's "reading a tension report" is not this page; the match is only the Home sentence.

## Q3. Verdict

advances. The Home page promises a guide "to reading what the fit reports", and the termination record is part of what a fit reports. No Home or root sentence mentions certification, statuses or how a fit stopped, so the page is the only place that carries it, though the story only needs it in a thin way. As a practitioner I would need it the first time a fit warns.

## Q4. If "repeats"

Not applicable. (Possible overlap with docs-user-guide-fitting, which I have not read, on how a fit ends; I cannot say it repeats.)

## Q8. Three judgments

- Against the Home page: fits the "reading what the fit reports" line, but the Home page's promised outputs (which metrics contend, elasticity, where designs sit, gaps in the table) are not here; this page is about the fit's own health, not those results. Home never says a fit has a certificate.
- Against the root page: the root page's bar is "show its reasoning, say where the data do not reach, and let the analysis be rerun". The last section ("Keep three claims apart") serves "say where the data do not reach"; the status taxonomy serves "show its reasoning" only for the optimizer, not the trade space.
- Against its opening sentence ("Every fit records how it stopped"): the page does that, but it goes well beyond it: it also covers conditioning_ and a margin-scale discussion, and the opening sentence names neither.

Sections serving none of the three: "How small is a small margin" (a worked margin-versus-1/tau check on one table), and "## conditioning_" ("The smallest eigenvalue of the restricted Hessian...") which the opening sentence does not announce.

## Q9. Read twice, could not place

- "Conditional local optimality: if no design sits exactly on a seam between terms..." (what a seam is and why the fixed assignment is then optimal; no pointer to where it is shown).
- "stable radius is the perturbation provably leaving every design's assignment unchanged" (perturbation of what, in what units).
- "term gaps within eps_kkt and min_curvature above eps_feas" (why the curvature is compared with a feasibility tolerance).
- "A soft fit leaves gamma, radius and bound nan." (floating line in the fields list, after the min_curvature item).
- "uncertified: as above." under the soft-fit list (as above refers to the hard-fit status, not to something in the soft list).
- "the tightest design sits a hundredfold nearer a seam than the typical one" (0.0020 versus 0.21 is about a hundredfold, but the "1/tau" band of 0.02 is not discussed in the result sentence).
- Terms gap G_k, tau, eps_kkt, eps_feas, mean_slack_ are used without definition on this page.
