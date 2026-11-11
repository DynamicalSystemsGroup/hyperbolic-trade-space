# docs-user-guide-limitations

## Q1. What the page conveys

It lists the ways a fit can mislead a user (conditioning, log-convexity, one term per tension, sample versus Pareto boundary, temperature, small samples, local optima, novelty, prediction), and for several of them says what to do about it.

## Q2. Which story sentence it serves

Root page, Why: "it has to show its reasoning, say where the data do not reach". The Home page has no sentence that needs it: its user-guide line promises "one page per task, from conditioning your attributes to reading what the fit reports", and limitations is not a task.

## Q3. Verdict and reason

advances. The root page sets a bar a trustworthy model-based method has to clear, and saying where the method does not reach is part of that bar. For a reader of the documentation, this is the one page that gathers those limits for a practitioner. The paper may carry a similar list (Appendix E, assumptions and abstraction gaps), but I have not read it. That would be the paper reader's copy, not the docs user's.

## Q4. If "repeats"

Not applicable.

## Q8. Three judgements

- **Against the Home page:** the Home page does not name a limitations page. Its promise of task pages "to reading what the fit reports" covers this page only loosely, as a caution attached to reading. The page fits the Home page but is not called for by it.
- **Against the root page:** a good match for "say where the data do not reach", and for "show its reasoning" through the closing paragraph on machine checks. The paragraphs on gaps ("Dents, holes and disconnected regions are invisible to it") and on small samples serve that sentence most directly.
- **Against its own opening sentence** ("These limits change what you do with a result."): the page keeps that promise only in part. Conditioning (refit and report what moves), one term (fit several terms), temperature (judge against the 1/tau band), small samples (read n_eff_ and conditioning_) and local fits (a larger sample) each name an action. Log-convexity, the Pareto boundary, contending sets, novelty and prediction state a limit but say little or nothing about what to do differently.
- **Serves none of the three:**
  - "Name. "Hyperbolic" describes the shape of the score..." is about the package's name and is not a limit on any result. Its footnote citing HoroPCA goes with it.
  - "Machine checks confirm that formulas follow..." does loosely serve the root page's "show its reasoning". But it is about the derivations, not about what you do with a result, so it falls outside the page's own opening.

## Q9. Read twice and still could not place

- "A hole is an opportunity only if the trade space is log-convex around it": I could not tell which hole is meant (one in the data or one in the surface), or how a user would check log-convexity.
- "Moving the reference or the scale of one metric changes which term is tangent": the page does not say tangent to what.
- "Away from that point a design can score below 1 while locally on the frontier"
- "If the balanced point sits on a vertex or edge of the weights' simplex": neither "balanced point" nor "the weights' simplex" is introduced on this page.
- "Judge a score against the band 1/tau": I could not tell whether the band is around 1 or how wide it is.
- "graded participation at a fit temperature"
- "negative association near the surface is partly a closure effect"
