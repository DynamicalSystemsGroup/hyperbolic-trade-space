# The synthetic three-metric case: material for `docs/examples.md#the-synthetic-three-metric-case`

The root page's two figures (the triangle and the slices) are drawn from one constructed table and one fit. The page
tells the story; this is the construction, for the documentation example that the slices caption links to. Everything is
in `scripts/build_site_figures.py` and reproduces with `uv run python scripts/build_site_figures.py`.

## The table

`fit_why()` draws it with the package's `make_frontier_data(900, 3, n_terms=3, random_state=11, **PLANT)`:

- three metrics, three planted terms, 900 designs, data seed `DATA_SEED = 11`; the planted exponent vectors are the
  package's seeded draw (Dirichlet, every pair at least 0.3 apart in L1), unchanged;
- `PLANT = {"frontier_fraction": 0.7, "interior_scale": 0.25, "noise": 0.07}`: 70% of the designs lie on the planted
  surface, the rest lie below it by an exponential depth of mean 0.25 (in log V), and the surface rows scatter by 0.07 in
  log V, so the data reach the surface along its whole length and about a tenth of the designs (11% measured) lie beyond
  it.

## The fit

`HyperbolicTradeSpace(n_terms=3, temperature=50.0, random_state=0).fit(X)` (`TEMPERATURE`, `FIT_SEED`): one fit, shared
by both figures (a test asserts that no second fit happens). The temperature is the figure's to tune: it sets how closely
the entropic offsets pull the surface to the data (at 10 more than half the designs lie beyond it, at 100 almost none; 50
gives the 11%). The surface drawn is the exact maximum over the terms, `log V = max_k (w_k . log m - beta_k)`.

## The triangle (`build_story`, `plot_ternary`)

Each design by its shares of the three metrics (each in units of its typical size), shaded by the term that leads there,
with a numbered marker at each term's exponent vector (star, diamond, square for terms 1, 2, 3).

## The regions of the triangle

Each shaded region is where one term binds. The rule is `plotting._ternary_region_of`: at a point of shares `c`, the term
with the largest `a_k + s * sum_j w_kj log c_j` (with `a_k = w_k . colmean - beta_k`, `s = 1` for the figure). "Binds" is
used in the infinite-temperature sense, the term whose piece the surface follows at the exact maximum (an active
constraint; the surface drawn is that maximum). At a finite temperature the term carries the largest weight, and the
surface lies within 1/tau of the binding piece (glossary entry `binding-term`; the designs so assigned are the term's cell).

## The slices (`draw_slices`, `build_slices`)

- Rows the three pairs of metrics; the third metric held at its median over the table (`held_at`); the exact section of
  the surface in the pair's plane (`slice_pieces`), one piece per term that leads along it, in the term's colour.
- Columns: the metric space (exp of the log section), the log space (the envelope), the chart: the surface laid flat as
  a line at log V = 0 with the position along the pair's axis, `(log m_i - log m_j) / sqrt(2)` (the difference of the two
  log metrics scaled to unit length), as its horizontal coordinate and the designs below it at their log V.
- The dots: designs whose third metric lies within `SLICE_BAND = 0.15` (log) of the held median, the opacity running from
  0.95 at the held value to 0.15 at the band's edge, the farthest drawn first.
- The three markers (`marker_points`) are the terms' characteristic points (glossary entry `characteristic-point`): by the
  weighted inequality of the means, among points with the same total of the metrics (each in units of its typical size) a
  term's monomial is largest where the shares equal its exponents; equivalently, on the term's piece of the surface the
  characteristic point is the point with the smallest total. The triangle's markers read as shares `c = w_k`, taken to the
  surface. The ray
  `m = t c` (in units of typical size) meets the surface once, at `t = 1 / V(c)`, because V is homogeneous of degree one;
  the log of that point is the log-metric point and its chart point is (position along the pair's axis, log V = 0). They
  are drawn on the chart column only, where they lie exactly on the line; the other two columns are a section at one value
  of the third metric, which three such points cannot share (tried: hollow markers floating off the curve, and a shaded
  band between the sections at the 20th and 80th percentile of the third metric; `figure-loop/rework-round3-*-markers-*.png`
  and the readers' words in `figure-review.md`).
- What the caption says about the third metric (a term enters or leaves) is pinned by the test that at the 20th, 50th and
  80th percentile of the third metric the set of terms drawn differs, for every pair.

## The earlier fan figure (before the rework)

Three overlaid sections per pane at the third metric's 20th, 50th and 80th percentile (faint to strong), stacked bars on
the chart column and a star for one design: `figure-loop/after-site-fan-*.png`. It was dropped because the three overlaid
sections hid the one connected surface the readers needed to see.

## The docs section, as reviewed by the driver (2026-11-15, 01:15 EST)

`docs/examples.md`, "The synthetic three-metric case" (36465be), run and read on the staged site at 8861
(`docs-example-top.jpg`, `docs-example-bottom.jpg`). Its code blocks run as written: the planted exponents, the fit's
exponents and term shares, 11 percent of designs beyond the surface at temperature 50, the three characteristic points
(term 1 at shares 0.53, 0.21, 0.26; term 2 at 0.19, 0.05, 0.76; term 3 at 0.00, 0.17, 0.83) and the terms drawn per
pair all match the page's sentences, and `fit_why()` in `scripts/build_site_figures.py` returns the same table and
the same exponents as the page's own fit (checked with `numpy.allclose`), so the figures and the section describe one
fit. The square root of two is stated where it belongs, in the chart's position formula, not in the figure. No figure
added; the section refers to the root page's images. Rows C791 to C797, kind S.
