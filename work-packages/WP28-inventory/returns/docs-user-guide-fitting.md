# docs-user-guide-fitting

## Q1
The page shows how to fit the frontier model with HyperbolicTradeSpace: one term, how to pick the temperature tau, several terms and their options, and how to choose K, tau and the band, with the attributes to read after a fit.

## Q2
Home page: "User guide: one page per task, from conditioning your attributes to reading what the fit reports." Also "fits a frontier model in the posynomial invariant form: a sum of monomial terms". Root page: "a guide per task from conditioning your attributes to reading a tension report".

## Q3
advances. The Home page promises one page per task, and fitting is the task between conditioning and reading the report. The page gives the fit call, the attributes to read, and the choices of tau and K that a practitioner has to make. No other listed unit says how to call the fit or how to choose K and tau. Getting started runs a first fit, but I have not read it, and this page goes well past a first fit.

## Q4
Not applicable. (Possible partial overlap with docs-getting-started on the first fit, and with docs-user-guide-termination on termination_ and conditioning_, which this page defers to.)

## Q8
- Against the Home page: it serves the "one page per task" line and the "fits a frontier model" sentence, and it says what the fit returns. It matches the scikit-learn claim (fit, transform, inverse_transform, score_samples, no predict).
- Against the root page: it serves "a guide per task". The root page's "what trades against what" and tensions content is left to the Tensions page.
- Against its own opening sentence ("fits the frontier model to conditioned metrics. At one term it solves a convex problem and returns the minimizer. It follows the scikit-learn decomposition family"): the one-term section does this. The sections on tau, several terms, and choosing K go beyond "fits to conditioned metrics" but still fall under fitting. The convex-problem claim is not shown or explained on the page. For several terms the page does not say what the fit returns instead of a minimizer.

Parts that serve none of the three:
- "Synthetic data: make_frontier_data plants a frontier..." is a tool note, not part of the fit story.
- The paragraph "tension_report takes its band from the temperature, 1/tau..." concerns tensions, not fitting.
- The two-metric log-plane plot and Figure 2 ("Three terms fitted to two metrics") serve the several-terms idea but sit under the "Choosing K" heading, away from the "Several terms" section.
- The bootstrap code block under "Choosing K" depends on `examples/adcs` and `case`, which a practitioner may not have.

## Q9
- "(at one term they coincide when the log-metrics are centred, as the cubesat's are)": I could not place which centring is meant or why the cubesat is mentioned this early.
- "carries no local-optimality status": unclear without the termination page.
- "Read kappa on the scale of tau: far below it, terms merge." It was unclear what "merge" means in practice.
- "Keep min_exponent (a floor on every exponent) at 0 to read the contending set": unclear what the contending set is.
- "the cell of new rows" and "cell_": the cell is not defined on this page.
- "Use tau of 3 and above: below that frac_above_ is not monotone in tau": the reason is not given.
- "term_aggregation ... a repeated term shifts the soft maximum by log 2 / kappa": a dense aside whose use I could not place.
