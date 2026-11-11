# Cold read, reader 1 (trade-study engineer, no project context)

Protocol per figure-review.md: cold read, sentence test, ink is data, legibility, shows/does not show, false analogy. Images viewed in the order B, trilemma, C, A. Names below are mine, from the file names.

## 1. textured-B (settling time / control effort / depth of discharge)

1. Shows: a triangle whose corners are "favours settling time" (top), "favours control effort" (bottom left), "favours depth of discharge" (bottom right). Inside, two shaded regions (large green one over the left and middle, smaller blue one in the bottom right), nested contour lines, grey dots scattered throughout, a green diamond labelled 2 and a blue star labelled 1.
2. Meaning, as far as I can tell: position in the triangle is a weighting of the three objectives (a point near a corner favours that objective). Dots are candidate designs or sampled weightings (two sizes, big and small, unexplained). The contours look like level sets of some score over the triangle, tightening toward the diamond and the star, which I read as the best points. The green label says settling time trades against control effort in that region; the blue label says depth of discharge alone. Could not tell: what the contours measure and their values; what the two dot sizes are; whether the dots are designs or weightings; why the star sits on the edge at the bottom-right corner and the diamond floats inside; what the numbers 1 and 2 rank; what the region boundary is a boundary of; why the contours have abrupt steps and kinks along the right edge and bottom edge.
3. Sentence: "Most of the weighting space is a settling-time versus control-effort trade; only near the depth-of-discharge corner does that objective dominate."
4. Ink: mostly data (regions, contours, dots). The label boxes are large and sit on top of the dots; the depth-of-discharge box covers dots next to the star. The stair-step contours at the upper right edge and the bottom edge read as plotting artefacts, not data.
5. Legibility: corner labels and region labels are readable. The marker numbers are small. Dots and contours are fine. The depth-of-discharge label crowds the star.
6. False ideas: two colours with grey dots over them read as two clusters of designs. The green blob around the diamond reads as a basin or hill, which may be intended. The jagged edge suggests the boundary is arbitrary.

## 2. trilemma (settling time / pointing error / total mass)

1. Shows: a triangle with corners favours settling time, favours pointing error, favours total mass, one beige region, concentric rounded-triangle contours around the centre, grey dots, one orange star labelled 1 near the centre with the text "all three trade".
2. Meaning: same coding as B. One region and one best point: a balanced weighting. The label is cut off ("all three trade" then the box ends), so the sentence is incomplete (probably "all three trade off"). Could not tell: contour values, dot meaning, why the star is at the centre rather than somewhere else.
3. Sentence: "With these three objectives there is one region and the best point is the balanced one." That is weak for a trade study: it says nothing happens.
4. Ink: contours and dots are data, but the picture is one smooth bump with no structure; the label is clipped and sits on the star and the dots. Nearly all of it says one thing.
5. Legibility: corners readable; the in-plot label is truncated and overlaps markers, which is a defect.
6. False ideas: dense contours near the edges suggest steep falloff toward the edges; the dots look uniform, so no idea of clusters here. It does suggest the model has a single interior optimum, which may be the true data.

## 3. textured-C (pointing error / energy balance / depth of discharge)

1. Shows: a triangle with corners favours pointing error (top), favours energy balance (bottom left), favours depth of discharge (bottom right). Three regions meet near the middle: pink on top, green on the left, blue on the right. Each has its own contour family and a marker at its nearest corner (3 square, 2 diamond, 1 star). Labels: "pointing error alone", "energy balance alone", "depth of discharge alone".
2. Meaning: each region is the part of the weighting space where one objective's term governs; the marker is the best point of that region and sits at the corner. Contours look like level sets within each region. Dots are designs or samples. Could not tell: contour values; dot sizes; whether the boundaries are exact or the result of a computation; what the small notch where the three regions meet means; whether markers 1, 2, 3 are ranks or just names.
3. Sentence: "The weighting space splits into three regions, one per objective, and within each the best design is the one at that objective's corner."
4. Ink: nearly all data. Regions, contours and dots fill the frame; labels sit in open space and do not cover markers. The notch at the junction is a bit of noise.
5. Legibility: best of the four. Corner labels, region labels and marker numbers are all readable; label boxes have room.
6. False ideas: three colours with dots on top invite reading them as three clusters of designs. The "alone" labels say each region is single-objective, so it shows different leading objectives rather than trade-offs between pairs. The contour kinks at the region edges look like model discontinuities, which may be real (a max over terms) but I would not know that cold.

## 4. textured-A (pointing error / total mass / control effort)

1. Shows: a triangle with corners favours pointing error (top), favours total mass (bottom left), favours control effort (bottom right). Two regions, green on the left and blue on the right strip, with contours bending around them, a blue star 1 near the right edge high up, a green diamond 2 on the left. Labels: "pointing error trades against control effort" (blue) and "total mass trades against pointing error" (green).
2. Meaning: as the others, but here each label names a pair that trades. Could not tell: why the green region is much bigger; what the contours represent; why contours pile up at the top and along the bottom edge; why the star sits on the edge while the diamond is interior; what 1 and 2 are. The labels are wordy and I had to re-read to see they name different pairs.
3. Sentence: "On one side pointing error trades against control effort, on the other total mass trades against pointing error." True to the request but the picture makes me work for it.
4. Ink: data fills the frame, but the labels are large, wrap to four lines, and sit on the dots and contours. The blue label is in small type and the green label is in large type for the same kind of content.
5. Legibility: mixed. The blue label is small and cramped, the green one is large and breaks one word per line. Corner labels fine. Sharp kinks in the contours on the right (horizontal runs) are distracting.
6. False ideas: strongly suggests two clusters of dots (blue strip versus green mass). The star on the edge and the diamond inside look like cluster centres.

## Ranking for "the frontier model has several regions with different leading trade-offs"

1. C. Three regions, clearly different, labels placed in clean space, markers at corners, easiest to read and the sentence test passes. Weakness: its labels say "alone", so it shows different leading objectives rather than trade-offs between pairs.
2. A. Its labels are the only ones that name different pairwise trade-offs in different regions, which is the literal request, but there are only two regions, the labels are cramped and inconsistent in size, and it reads as two clusters.
3. B. Mixes one trade-off region with one "alone" region; clear but the jagged contours and the label over the star hurt; two regions only.
4. trilemma. One region; the picture does not show several regions at all, and the label is clipped.

If only one: C. Caveat: if the point must be trade-offs between pairs, A has the right claim but needs a cleaner redraw of labels.
