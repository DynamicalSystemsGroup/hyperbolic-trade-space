# docs-user-guide-conditioning

## Q1. What the page conveys

How to turn raw attributes (kilograms, dollars, error rates, some smaller-is-better) into the strictly positive, larger-is-better metrics the fit needs, using LogAffinePreconditioner (orientation, shift, reference point, scaler), how to check the result, and how to read the fitted surface back in the original units with frontier_in_original_units.

## Q2. Which sentence of the story it serves

Home: "User guide: one page per task, from conditioning your attributes to reading what the fit reports", together with the Home page's condition on the input, "each scored on several metrics where larger is better". Root page: "a guide per task from conditioning your attributes to reading a tension report".

## Q3. Verdict

advances

Both the Home page and the root page name conditioning as the first task of the user guide, and the Home page's promise depends on the reader having larger-is-better metrics, which a practitioner with a raw table does not have. This page is the one that says how to get them, and nothing in the unit list other than this page is named for that task. The pull-back section also serves the Home page's "where each design sits relative to the fitted reference surface" by giving that surface in the units the reader started with.

## Q4. Unit that already carries it

Not applicable.

## Q8. Judged three ways

- Against the Home page: it does the first job the Home page lists for the user guide, and it keeps to the Home page's framing (a table of designs, metrics where larger is better). It fits well.
- Against the root page: it fits the root page's "conditioning your attributes" and its bar of letting the analysis be rerun and showing its reasoning (the Diagnostics section, the refit under a second conditioning). It does not touch the root page's tensions or gaps directly, and does not need to.
- Against its own opening sentence: the opening says the fit consumes strictly positive larger-is-better metrics and that the package supplies LogAffinePreconditioner and frontier_in_original_units. The page then covers both: orientation, shift, reference point, scaling and zeros for the preconditioner, and the last section for the pull-back. It does what it says. Two small gaps against that opening: the code block imports HyperbolicTradeSpace but never fits it, and it prints a check without showing the output, so the first-time reader does not see the conditioned matrix go into a fit.

Paragraphs or sections that serve none of the three: none outright. The weakest is "Infeasible rows are not the preconditioner's job...", which is advice about data preparation rather than conditioning, but it still serves the opening by saying what the preconditioner does not do.

## Q9. Read twice and still could not place

- "It fixes what V = 1 means in practice": V is not defined on this page or in the story; I can guess it is the value of the fitted surface but cannot place it from what I read.
- "the temperature of the next page: it is quoted in inverse log-spread": the reason given for scaling depends on a term from another page, so the scaling advice cannot be judged from this page alone.
- "The pulled-back exponent on a raw attribute is w_j * alpha_j": neither w_j nor alpha_j is introduced here.
- "If the contending set moves": "contending set" is not defined on this page (the Home page says "which metrics contend", which suggests the meaning, but the page does not tie it).
- "they show whether the story is sensible": unclear which "story" is meant (the conditioning choice, the fit's findings, or the documentation's).
- "its chart coordinates are nan": the chart is not introduced on this page.
