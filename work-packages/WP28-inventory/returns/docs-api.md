# docs-api

## Q1
The page lists the package's public names (classes, functions, submodule contents, two constants) with a short phrase each saying what it is for, and points to the API reference and user guide for detail.

## Q2
Home page: "API and API reference: the public names and their docstrings." The root page's "Package" block ("API reference →") points the same way.

## Q3
Verdict: advances. The Home page promises a page of public names, and the API reference alone is generated docstrings with no grouping by purpose. This page is the only one that gives a first-time user a map: which name transforms, which fits, which reports, which plots. It is not the user guide (tasks) and not the reference (docstrings).

## Q4
Not applicable.

## Q8
- Against the Home page: matches "the public names and their docstrings". The names appear, though the docstrings sit in the reference, which the page says.
- Against the root page: the root says the package is a scikit-learn-compatible estimator with a log-ratio chart, tension reports and plotting helpers. The page covers each: the transformers, `tension_report`, the chart bases, the plotting submodule, and the scikit-learn conventions.
- Against its own opening sentence ("The public interface, by what each name is for"): mostly yes for the main list, with one-line purposes. The submodule list is less so. Several entries are bare name lists with a parenthetical tag, for example "(fitting)", "(chart)". The two constants carry the most detail. The last entry refers to "Reading termination" and "min_curvature" with little explanation.

Parts that serve none of the three:
- "Fitted attributes for every number of terms include exponents_, cell_..." is attribute-level detail that belongs in the reference, not an interface map.
- "hyperbolic_trade_space.estimator: EPS_ZERO_EXPONENT (1e-12)..." is threshold detail beyond a map of names.
- The two numbered references (Pedregosa et al.; Buitinck et al.) serve only the one conventions sentence. They are appropriate, but they take up as much room as the content.

## Q9
- "12" after "scikit-learn conventions": a citation marker that rendered as bare digits.
- "(fitting)" and "(chart)" after the coordinates and gaps entries: I could not say what they tag.
- "the soft fit (Reading termination)": a reference to a section I could not place from this page.
- "a transformer: fits the surface and gives the chart of position and log V": "position" and "log V" are not defined here.
- "mean_slack_ (the mean slack, to compare fits across numbers of terms)": unclear without the user guide.
