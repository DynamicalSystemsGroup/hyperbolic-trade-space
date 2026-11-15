# Drafts for the build (WP42): the preamble's reading, Section 3's paragraph, Section 9's sentence

These are the texts the readout names, kept in one file so the vocabulary dry run reads them as the checker reads the
docs. Numbers in the Section 9 sentence come from `section9.py` and are not typed by hand.

## Section 3, three layers in brief (with a pointer to Appendix A)

Three optimizations are nested here, and each keeps its own words. The decision-maker chooses a design by objectives (the metrics wanted more of) and constraints (a requirement's limit). The designer's optimization uses the fitted model as a function of the metrics, which is where the geometric-program form belongs. The fit is an optimization over the exponents, and the function its solver minimizes is the loss, scikit-learn's word; we choose it so that objective stays with the decision. {ref}`Appendix A <appendix-a>` gives each word with its layer.

## Section 9, one sentence on the pick's tension

At the picked fleet (5 medium-wheel, fine-tracker satellites) the surface's tension between the operator's pointing error and the sponsor's fleet cost is -1.4 M USD per arcsecond: along the surface, one percent more pointing error goes with 2.4 percent less fleet cost. It is a rate at that design with the other metrics held, not the price of the better tracker, and on the other term of the fit it is -0.4 M USD per arcsecond.
