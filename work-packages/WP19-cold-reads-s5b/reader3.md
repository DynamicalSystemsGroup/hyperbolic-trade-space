# Cold read, reader 3 (GNC research engineer, trade studies; images only, no captions)

Order read: B-light, A-dark, A-light, B-dark. Protocol from figure-review.md (tests 1 to 4 plus the borrowed-idiom check).

## 1. B-light (corners: settling time / control effort / depth of discharge)

(1) Shows: a ternary plot. Each corner "favours" one quantity. The triangle is split by a thick dashed curve into a large pale-green region (left, most of the area) and a pale-blue region (lower right). Nested thin contour rings sit inside each region, centred on a green diamond "2" in the green region and a blue star "1" at the bottom-right corner. About 300 grey dots (some larger) are scattered over the whole triangle.

(2) Key and marks. Thin lines = "lines of equal V (0.3 to 0.97 of the peak)": the key does not say what V is, so I can read the rings as a hill or value surface but not what it measures. Dashed = "where the leading term changes": "term" is undefined for me; I infer a piecewise max, so the dashed line is a switch between two dominant pieces. Dots = designs, larger near "the frontier" (which frontier?). Diamond/star = "a term's exponent vector": jargon; I cannot tell why one is a star and one a diamond (colour matches the region tint and box outline, shape does not obviously mean anything). The meaning of a point in the triangle (a weighting? a normalised outcome?) is never stated. Callouts: "settling time trades against control effort" (green) and "depth of discharge alone" (blue). Colour linking box to region to marker works. Unclear: whether dots are plotted at their own ternary coordinates, and what "near the frontier" is measured against.

(3) Takeaway: the model has two zones: one where settling time and control effort trade off, and one near the depth-of-discharge corner where only that attribute matters.

(4) Ink as data: contours, boundary, dots and the two markers are all data; roughly 85 percent of the triangle carries ink. Decoration is minimal (tints, callout boxes). The dot cloud is dense and busy but it is the data. The title-less frame and the large legend block below carry the explanation; whitespace below the triangle is fine.

(5) Legibility: corner labels and key readable. Defects: the "depth of discharge alone" box sits on the dashed line and on a cluster of dots at the bottom; the "settling time trades against control effort" box hides a patch of dots and contour lines; marker "1" label box is jammed against the bottom-right corner and the star sits on the corner/edge so half of it looks clipped by the frame; at the top-right the dashed line runs along and almost on top of the triangle edge, near-invisible. The dashed line and the nearby solid contours converge near the bottom edge and are hard to separate.

(6) Ideas the data may not carry: the dot cloud makes the green region look like a hill whose peak is the diamond with dots "clustered" around it; the nested rings look like density contours of the dots. A reader may read rings as a kernel density of designs, not as a model surface. The blue "region" at the corner reads as a small cluster of designs. The star at the corner may read as an optimum design. "Depth of discharge alone" suggests a single-attribute regime that the data may only extrapolate to (corner, sparse dots).

## 2. A-dark (corners: pointing error / total mass / control effort)

(1) Shows: same construction on dark ground. Dark green region (left and bottom, the larger part) and dark blue region (upper right) divided by a white dashed curve running from near the top, down and to the right to the bottom-right corner. Rings around a green diamond "2" in the left part; rings around a blue star "1" in the upper right, appearing as bands parallel to the right edge. Dots everywhere.

(2) Key as in B. Callouts: "total mass trades against pointing error" (green), "pointing error trades against control effort" (blue). Here both regions are named as a pair trade, so the key plus callouts say something I can use. Same unclear terms (V, leading term, exponent vector, frontier). The meaning of position in the triangle is still unstated. In the blue region the contours are open bands cut by the edges; I cannot tell whether they are meant to be rings around the star.

(3) Takeaway: depending on where you are in the triangle the leading trade is mass versus pointing error (left) or pointing error versus control effort (right); two different trades.

(4) Ink as data: high; the whole frame is data, callouts are the only added ink. Dots dense near the left edge and top apex.

(5) Dark legibility: contrast of white lines and light-grey dots is good. Corner labels strong. Dark green vs dark blue tint difference is real but subtle; I would not distinguish them without the dashed line. The white dashed line and white contour lines are the same colour, so the dashed boundary gets lost where contours run alongside it (upper left of the line near the apex, and near x=410, y=435 where it bends). Callout boxes have opaque dark fill and cover dots; the blue callout sits right on the boundary neighbourhood and nearly touches the dashed line. Marker "1" box close to the star but not overlapping. Dashed line at the bottom-right corner runs into the corner and the edge.

(6) False ideas: the green and blue shaded zones read as two clusters of designs; the diamond looks like a cluster centre or best design; dots clump near the left edge and apex, which can read as populations rather than as sampling density.

## 3. A-light

(1) Shows: same as A-dark in light theme.
(2) Same key; callouts identical to A-dark.
(3) Same takeaway as A-dark.
(4) Same ink as A-dark.
(5) Legibility: best of the four. Black dashed vs thin black contour lines are distinguishable by weight, but still close in colour. Pale tints are easy to separate (mint vs pale blue) with the dashed line. The callout boxes still hide dots; the blue box is wide and crosses the dashed line's neighbourhood but not the line itself. Dots near the left callout are partly hidden. The star "1" and its box are clear. Bottom-right the dashed line exits the triangle at the corner.
(6) Same false ideas: tints as clusters; contours as density.

## 4. B-dark

(1) Shows: B on dark ground: dark-green big region with rings around diamond "2", dark-blue region lower right, white dashed boundary, star "1" at the corner.
(2) Same as B-light.
(3) Same takeaway as B-light.
(4) Same ink as B-light.
(5) Legibility: contrast of lines and corner labels is good. Dashed white and white contours merge, particularly near the bottom where the boundary curls along the bottom edge and where the callout "depth of discharge alone" sits on the dashed line and dots. The blue-tinted region is the darkest and the rings in it are hard to follow near the bottom-right. Star "1" and its box are again against the corner, and the star appears partly cut by the frame.
(6) Same false ideas as B-light, the blue corner as a cluster.

## Which of A or B for "the frontier model has regions with different leading trade-offs"

A. Both regions are interior, both are named as a trade between two attributes, and the two trades differ in pair (mass/pointing versus pointing/control). The dashed line is a clear curve crossing the middle of the triangle, so the "regions" are balanced in size and the claim is visible. B has one region that is a trade and one that is a single attribute at a corner ("alone"), which shows a regime change from trade-off to dominance, not two different trade-offs; the blue region is small and sits on the corner/edge with a marker clipped by the frame. Within A, I would use A-light (dashed line and tints separate best); A-dark only if the dashed line and contours get different treatment.

## Remaining defects, in order of importance

1. Undefined terms in the key: V, "leading term", "exponent vector", "frontier". A reader cannot say what the rings or the dashed line are without outside text. Also the meaning of a position in the triangle is nowhere stated.
2. The dot cloud plus nested rings invite a cluster/hill/density reading (the false idiom the project note warns about); tinted zones read as groups of designs.
3. Callout boxes cover dots, contours, and in B sit on the dashed line.
4. Dark: dashed boundary and contours are the same white; boundary lost where they run together. Tint difference faint.
5. Marker/shape semantics (star versus diamond) unexplained; star "1" and its box crowd the frame (B: corner, half clipped; A: fine).
6. Dashed line runs along or exits at the triangle edge/corner in places (A: bottom-right corner; B: top-right and bottom), looking like a frame artefact.
7. Contours in the blue region of A are open bands cut by the frame, not rings, but are styled identically to the closed rings of the green region.
8. Dot sizes ("larger: near the frontier") are hard to see; two-size encoding is subtle at this size.
