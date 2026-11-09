# WP8a: docsite figure review (P8), reassessed by intent (Amendment 3)

Method: `docs/superpowers/notes/figure-review.md` (intent first; a cold read; the smallest change; no
overtuning; no phone requirement for paper figures).

History, short. The first pass (fb8fbe1) judged the nine figures on five tests and proposed reworks
for most; the supervisor overruled it: Figure 8 stays ("this one is great"), the tension heatmap is
liked ("you can resize it but don't rework it"), "there is a risk that you will overtune here", and
the figures are to be reassessed "with a focus on what they are intended to convey and whether they
succeed in doing so". That pass's candidate images for Figure 7 are kept in
`docs/superpowers/notes/figure-candidates/` and are not proposed here. Its limits stay: dark scheme
and phone width were not inspected, and are not required now.

Method of this pass. The author's intended takeaway for each figure was written first (column 2, from
the figure's page and purpose). One fresh-context Sonnet reader per figure (no repo access) was given
the light-scheme PNG built by `scripts/build_figures.py` at the docs' size, wrote what it conveyed,
then was given the page's caption and wrote it again. Reader's words are quoted. Nothing on any page,
script or test is changed; no candidate image was produced (no figure needed a redraw).

| Figure | Intended to convey | Succeeds? Reader's words (image alone; with caption) | Smallest action |
|---|---|---|---|
| 1 first-fit (getting-started) | The frontier of two metrics is a straight line in the log plane, the designs lie below it, a few just beyond, the nearest in a band. | Yes. "the line looks like an upper envelope of the data in log space, with the band marking 'near-frontier'"; with caption: "most designs fall below it, a few just beyond it, and the band picks out the nearest ones". Open: what V is (the page's job, not the picture's). | None |
| 2 three-facets (fitting) | With K = 3 the frontier is bent: the envelope of three straight facets. | Yes. "the data sit on or below a convex, kinked boundary. Each color hugs a different segment"; with caption: "the frontier is the upper envelope of three log-linear facets". Orange and green overlap near the corner; assignment rule unsaid. | None |
| 3 tension-report (tensions) | All three metrics are mutually traded (negative association) and all three contend. | Yes. "Every pair of metrics is in tension, and m1 and m2 conflict most (-0.62)". Outlines read as "decoration" until the caption: "the outline on each diagonal cell reads as grouping". "Association" undefined. | Caption: one clause defining association and saying the diagonal outlines mark the contending set |
| 4 log-plane (chart) | One facet in the log plane: the line is V = 1, and the band below it has width 1/tau. | Yes. "one facet of the frontier is a straight line V = 1, and a thin tolerance band of width 1/tau below it marks 'near-frontier'". Band faint; legend shows log V >= -0.05 where caption says 1/tau (tau = 20 is on the page). | None (a reader gets the intent; it differs from Figure 1 only by band width, which is its point) |
| 5 chart-holes (chart) | Grid positions far from every design inside the cloud are candidates for white space. | Partly. Alone: "a roughly elliptical ring of orange squares" around the blue points, "mark its edge or the zone just outside it". With caption: "Orange squares mark empty regions of the design space ... that may be unexplored opportunities", but "why the orange cells ring the data and none fall inside it ... despite the 'chart with holes' title", and "red" in the caption against orange squares. The seeded data are a blob with no interior hole, so the function returns rim positions. | Caption (and alt text): "orange" for "red", and say that in this seeded blob the positions fall at the rim, a blob having no interior hole. No redraw: the plot shows what the function returns |
| 6 adcs-tensions (examples) | Of ten metrics six contend (outlined), four do not; strong redundant pairs and the sign structure are visible. | Yes. "Metrics fall into clusters: settling time and slew time agree (0.91) ... power margin/energy balance (0.98) ... near-duplicate pairs"; with caption: "of ten metrics, the fit puts nonzero weight on six that actually compete". Unclear to a newcomer: association, weights, why outlines sit on the diagonal (text matters, not the picture). The supervisor likes it. | Resize only (display it at the column width; no rework) |
| 7 adcs-coordinates (examples) | Where the 706 designs sit in the first two position coordinates (coverage), with the nearest-frontier ringed; it does not show the frontier. | Yes with the caption, no without. Alone: "I don't know what the black outlines mean. I also don't know why the right edge is so sharp"; with caption: "designs plotted by their first two coordinates, with the frontier-adjacent ones ringed, cluster toward the right and center of the cloud". Open: "what 'position coordinates' are", "how many designs are ringed". The first pass found the figure weak at showing the frontier; the intent as written is coverage, which it conveys. | Caption: say Z0 and Z1 are the first two of nine coordinates with no meaning alone, give the ring count, and say it shows coverage, not the frontier |
| 8 ternary-planted (examples) | Three metrics as shares of a total: regions where one facet dominates, numbered exponent vectors, lines of equal V. | Yes enough, and the supervisor has confirmed it ("this one is great"). "divided into three regions, each labeled by which metrics trade against each other"; with caption the markers are "exponent vectors ... one per region". Grey dots and marker shapes unexplained. | None (stays as drawn) |
| 9 ternary-cubesat (examples) | Only facet 3 of the cubesat fit carries mass (0.18); facets 1 and 2 lie on the power and attitude control edge. | The picture conveys it, but only after the caption, and the caption already says all of it. Alone: "Design 1 leans almost fully toward attitude control" (misread as designs); with caption: "only term 3 involves mass, at 0.18", and "0.18 appears only in the caption, not on the plot". The supervisor's WP18 word stands: "pretty vacuous. doesn't seem to earn its place". | Drop (the caption's sentence is the content; keep it as text) |

Summary: no redraw. Keep as drawn: 1, 2, 4, 8. Caption fixes: 3, 5, 7. Resize only: 6. Drop: 9.

Cold-read details (full reader text is in the P8 session transcript): readers of 1, 2, 4, 6 and 8 reached
the intended takeaway from the image alone or with one caption sentence; readers of 3, 5 and 7 needed the
caption for the outlines, the squares and the rings; the reader of 9 misread markers as designs until the
caption, then read it correctly.
