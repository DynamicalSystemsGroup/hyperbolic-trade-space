# Figure loop on Figures 3, 6 and 7 (paper unit paperwp30)

Screenshots for this record: commit `2a669de`, `git show 2a669de:<path>` with `<path>` under `work-packages/WP30-rounds/chooseK/screenshots/`, `work-packages/WP30-rounds/paperwp30/`.

Inputs: the cold reader's returns (`WP30-rounds/chooseK/cold-reads/cold-read-figs-6-7-8.md`, read from the rendered page with
captions hidden); my own check of each caption against the image file the caption sits under. The sentence test, ink as data and
legibility are applied to the images below, which are in this folder. Figure numbers are those of the page before this unit;
after it, the K = 2 planes figure is gone and the chart is Figure 6, the association Figure 7.

## Figure 3, the behavioural view: caption

The picture (`paper/figures/fig-behavioural-view.png`) is current: four groups (controls, power and energy, cost, mass), thirteen
traded metrics, `SlewExperiment` "returns 10 of 13 metrics" (three computed with no slew: pointing error, total mass, available
power), the settling time from the measurement and not returned, the unit cost and the fleet cost "an analysis each", two boxes that
say the baseline does not satisfy the pointing-error and the unit-cost requirement, the launch cost yellow (derived, not traded).
The caption said "eight metrics", three subsystems, "returns seven of the eight". New caption: the cold reader's proposal, with its
last sentence ("top: requirements that read no traded metric") dropped, because no such box is in the image (checked top to bottom
of the image: nothing sits above the controls group). Every clause was checked against the image, whole figure. Sentence test:
one claim, each traded metric traced to its requirement and its supplier.

## Figure 7, the chart: the axis label and the caption contradicted

Trace: the axis label is generated from the data (`paper/figures/chart_level.py::leading_direction`, the first direction of the
K = 1 fit's near-frontier chart, signed as Appendix D.16 signs it); at the data of record it reads "better unit cost, total mass
and peak slew power" and Appendix D.16's first row reads "unit cost +0.42, total mass +0.42, peak slew power +0.36": the image is
current. The caption's clause ("better total mass and control effort, worse pointing error") was typed on the eight-metric data
and is the stale one. Fix: the clause leaves the caption, which points at D.16 for the share and the loadings and at the axis for
the metrics (a typed list rots; the axis cannot); a test now compares the axis's metrics, by sign, with D.16's first row.
"The other six directions of position" read for eight metrics; with thirteen it is eleven. The line now says "the other
directions of position": a count typed in prose goes stale, and none carries a claim here.

## Figure 6, the K = 2 planes (the top panel a lattice): decision by the loop

Images: `fig6-before-two-panels.png` (as committed), `fig6-optionA-pointing-vs-unit-cost.png`, `fig6-optionB-single-panel.png`,
and `fig5-k1-plane-for-comparison.png`.

- **Option A, the top panel in pointing error against unit cost** (the cold reader's first try, redrawn through the figure
  module). The vertical axis is continuous, but pointing error stays in three columns (tracker grades), the panel then carries
  two terms' segments with a kink (term 2 owns the left half), and the pair is no longer term 1's two heaviest metrics, which is
  the rule the caption states. An improvement and not a cure; and it needs a caption caveat to explain why this pair. Rejected.
- **Option B, drop the top panel.** The redrawn figure is the bottom panel alone: available power against unit cost with the
  line and the near-median designs in dark grey. Laid beside Figure 5 (the K = 1 plane, the same pair of axes) the two are the
  same picture: the same cloud, a line with the same slope to within the eye (the K = 2 line in this slice is term 2's, and the
  K = 1 fit is dominated by that pair); the dark designs differ only in which median is held. The sentence test on it
  ("term 2 trades available power against unit cost and the designs fall on and below its line") is Figure 5's sentence again.
  The figure earns no place beside Figure 5.
- **Decision: retire the K = 2 planes figure; Figure 5 stays.** What the top panel carried is one sentence that already stands
  in the generated elasticity sentence ("Term 1's two leading metrics, peak slew power and pointing error, are stepped by the
  swaps of the tracker grade and the wheel class, so its elasticity is read across the swapped parts' alternatives rather than
  along one continuous trade"), and the association figure (now Figure 7) carries the within-term association of that pair
  (-0.97). The sentence that introduced the figure now introduces the chart and the association figure alone. The estimator, the
  plotting function (`planes_figure(n_terms=...)`, still tested) and the K = 1 plane are unchanged; only the paper's use ends.
  Removal is a negative edit against the marginal-value test, the stuck-means-assess-removal order, and costs the reader nothing
  the other figures and the sentence do not give.

Cascade of the removal: the two markdown cells of the figure (caption, Shows line) and `paper/figures/fig-planes-case.png`; claim
row C475 (the caption's sentence on the bottom panel); the float count of `test_every_figure_and_table_is_referenced_from_the_text`
(nine figures became eight); `planes.py::main` writes the K = 1 plane only. A ledger cut row records the 259 words.

## The rendered pass (my own browser tab, the site staged from this worktree at 78cd40a plus the re-executed notebooks)

Served from `scripts/stage_site.py --serve --port 8795`; the page's text read from the DOM and the pages looked at as screenshots
(this folder): `page-fig3-image-top.jpg`, `page-fig3-caption-and-coverage-sentence.jpg` (Figure 3 with its new caption and the
coverage sentence below it), `page-section8-participation-sentence.jpg` (the two-metrics sentence, the marks sentence),
`page-fig6-chart-caption-axis.jpg` (the chart as Figure 6: the axis reads "better unit cost, total mass and peak slew power",
the caption points at D.16 and at the axis; the association figure follows as Figure 7),
`page-section6-margin-and-section7-sampling.jpg` (the margin sentence at K = 2, the Section 7 sampling sentence),
`page-appendix-c8.jpg` (C.8). The page's width equals the viewport (scrollWidth 898 of 913). The page text carries "a 7-lemma
and an 8-lemma", "The designs are drawn at random, 3000 per regime", the K = 2 margin (0.0003768, 37 of the 2134), the D.3 summed
pairs at K = 1, K = 2 and K = 3, and no "Figure 6" for the removed planes figure (the numbering after Figure 5 is the chart,
the association figure, the ternary figure).
