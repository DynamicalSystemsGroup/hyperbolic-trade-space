# docsfig-log-plane

## Q5

(a) A scatter of a few hundred blue points on axes "log m0" (horizontal, about -7 to 2.5) and "log m1" (vertical, about -6 to 2). A straight black line of slope about -0.8 runs from upper left (-2.5, 2) to lower right (2.4, -2.1), labelled "frontier V = 1", with a very thin grey strip just below it labelled "band (log V >= -0.05)". All points lie on or below/left of the line; many crowd tightly along it, the rest spread down and to the left, sparser with distance, a few far out near (-6.6, -5.9). Nothing lies above the line. The grey band is barely visible because it is so thin and the points on the line cover it.

(b) Mostly yes. The line is V = 1 and there is a grey strip below it. The caption gives the strip as log V from -1/tau to 0. The legend gives it as log V >= -0.05. These agree only if tau = 20, and the caption does not say so. The code above the figure sets temperature=20.0, so a reader has to connect temperature to tau and work out 1/20 = 0.05.

What it does not show:
- The strip is so thin that it is hard to see at all. The near-frontier designs read as "points on the line", not as "points in a band".
- "One term" is not shown as such. Nothing in the image says the straight line is a single monomial term, or that a multi-term fit would bend it.
- The page later says that "some training designs lie beyond V = 1 by construction" and that the band is |log V| below 1/tau, which is both sides of the line. The figure shows no points above the line and only the lower half of the band. A reader who carries the figure into "Reading log V" gets the opposite picture.
- The alt text calls the band "near-frontier designs". The caption calls it a range of log V. These are close, but they are not the same thing.

(c) Sentence: "With two metrics, a one-term fit is a straight line in the log plane; designs lie on or below it, and log V measures how far below, with the near-frontier ones within 1/tau of it."

The figure conveys a little more than that sentence. It shows the shape of the data: a dense pile-up along the line and a thinning cloud toward the lower left. It shows the line's slope, which is the trade rate between the two metrics. And it shows that the frontier is a supporting line on the upper-right edge of the cloud, not a line fitted through its middle. It adds nothing about where log V is positive.

## Q1

With two metrics, a one-term fitted frontier is a straight line in log coordinates that bounds the designs from above, and most designs sit just inside it.

## Q2

Home page: "where each design sits relative to the fitted reference surface". It also loosely serves "PCA finds where the data spread, this finds where they stop".

## Q3

advances. The Home page promises to show where each design sits relative to the fitted reference surface. On this page, this figure is the only picture of a design's offset (log V) from the surface in the metrics themselves, before the chart coordinates are taken. Figure 5, the other figure on the page, shows positions and holes, not the frontier line. Within the docs I was given, no other unit carries it.

## Q4

Not applicable.

## Q8

- Home page ("where each design sits relative to the fitted reference surface"): it helps. You can see designs on the line and inside it, and how far inside. It does not show any design beyond the surface, although the page says such designs exist.
- Root page ("learn the shape of a trade space ... where they stop"): it helps, in the simplest case. The stopping edge is visible as a line over the cloud. The "shape" here is only a line, and the figure does not say that more terms would bend it.
- Page opening ("two kinds of coordinate ... log V ... negative inside, positive beyond"): it partly helps. Negative inside is visible. Positive beyond is not shown. The d - 1 position coordinate, which here is where along the line a design sits, is not marked or named on the figure.

## Q9

- "One term in the log plane": I could not tell from the figure or the page why "one term" is singled out, or what a second term would look like here.
- "log V from -1/tau to 0" against the legend's "-0.05": I placed it only by guessing that tau is the temperature=20.0 in the code.
- "the near-frontier band, |log V| below 1/tau" (later on the page) against the figure's one-sided strip and its empty region above the line: I could not square the two.
