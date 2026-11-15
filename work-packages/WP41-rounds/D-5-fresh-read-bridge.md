# D-5: fresh cold read of docs/bridge.md (Haiku; page text alone)

Returned as the reader's final message, because its Write call was refused; committed as returned.

(1) What the page lets you do. It gives two routes from a chart point back to a design. The sampled route is a lookup when the point has a datum. The conjecture route proposes a configuration for a point without a datum, with a predicted chart point and a tolerance, then checks it by building or evaluating the design. It also shows code for a proposal: a TradeSpaceRegressor, a target position, and a nearest-in-seeded-pool selection rule. It states what ships now (the regressor and the lookup) and what is case-only or planned. Convergence of the loop is not studied.

(2) What a proposal is worth. It is a conjecture, not a result. The page gives three reasons: the regressor predicts and does not evaluate; the preimage is not unique, so a selection rule must pick one configuration; and a built design may land elsewhere. The check settles it by comparing the measured chart point with the predicted one within the default tolerance 1/tau. Confirmed means within tolerance; the page says one confirmed design "is not a rate." Refuted means outside tolerance, so the measurement is appended and the fit refit. Infeasible means the design fails a feasibility condition, so the row is kept with its flags and refit.

(3) Confusions.
- tau is never defined. I guessed it is the code's temperature (20.0), making the band about 0.05 in log units. Unconfirmed.
- Feasibility conditions and flags are never stated; only the cubesat depth-of-discharge failure is given.
- The comment says the target is "a position on the surface (log V = 0)", but Z_target = reg.predict_coordinates(C)[0].mean(axis=0) does not set the level to zero.
- The distance uses (2 * lv) ** 2 with no explanation of the factor 2.
- "Submartingale" is used without definition, and no conditions are derived.
- Cross-references (paper:thm-pullback, paper:sect-search, paper:sub-d-10, user-guide/prediction.md) could not be followed.
- "Two of the three are the same configuration, since two holes had one pooled configuration nearest" is unclear to me.

(4) Next steps. Follow the pull-back and chart theorems for tau and feasibility. Read the prediction page for the error model and the meaning of position and level. Open the cubesat check script and appendix D.10. Run the code block, first checking that the target lies at log V near 0. Ask the author what tau is, how feasibility is defined, and why the factor is 2.

(5) Open questions. What is tau, and why is the tolerance 1/tau? What are the feasibility conditions and flags? Does Z_target lie on the surface? Is the factor 2 part of the method or a convenience? What does "submartingale" mean precisely? What are "holes" and "white space" in the search framing? Should lookups be treated as uncertain, since a noisy evaluation can move a configuration?
