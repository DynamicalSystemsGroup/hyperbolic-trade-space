# docs-getting-started

## Q1
It shows how to install the package from source and run a first fit on a synthetic table of 300 designs and 3 metrics, then explains the report (contending set, exponents, elasticities) and the other fitted outputs (score_samples, transform, inverse_transform), and points to the user guide for real data.

## Q2
Home page: "Getting started: install from source and run a first fit." Root page: "the documentation shows how to use the package ... a first fit" and "Install from source".

## Q3
Verdict: advances.

The Home page names this page for exactly two jobs, install from source and a first fit, and the root page promises "a first fit" in its documentation card. No other listed unit carries an install-and-run walkthrough with a worked output; the User guide pages start at conditioning and fitting, which this page hands off to.

## Q4
Not applicable (not "repeats").

## Q8
- Against the Home page: it does what the entry says, install from source and a first fit. It also shows the "which metrics contend, with what elasticity" claim in running code, and the sklearn methods (score_samples, transform, inverse_transform) the Home page lists.
- Against the root page: it serves "a first fit" in the Documentation card and the install line in the Package card (the pip line there and the uv clone here are two different install routes, which is a small mismatch, not a failure).
- Against its own opening sentence: the page opens only with a heading and "The package is installed from source for now." The rest goes well beyond install into fit, a plot, reading the output and a hand-off to the guide. The page's real promise is carried by the Home entry, and the page keeps it.

Parts that serve none of the three: none clearly. The nearest candidates are the sentence "The fitted object has more to give" and the paragraph after it on score_samples, transform and inverse_transform. They serve the Home page's list of estimator methods, but they preview material the User guide's Chart page presumably carries.

## Q9
- "temperature, the one parameter set, is tau, how hard the maximum is": I could not place "how hard the maximum is" on first reading.
- "(choosing the temperature)": a bare parenthetical pointer with no link target visible in the text; I could not tell where it leads.
- "a weighted geometric mean of the metrics, 1 on the fitted reference surface, so negative inside and positive beyond": "inside" and "beyond" are not defined on this page, and "log V" is used before V is introduced.
- "the grey strip under the line is the region up to 0.5 below the frontier in log V": the figure was not opened, so the "strip" and the 0.5 cannot be checked against it here.
