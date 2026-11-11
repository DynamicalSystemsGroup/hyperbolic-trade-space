# Cold read, reader 2 (systems architect, multi-objective trade studies)

Protocol followed: image alone, no caption; questions 1-6 per image, then ranking. Images viewed in the order given.

## 1. ternary-cubesat-textured-A-dark.png

1. Shows: a triangle whose corners are "favours pointing error" (top), "favours total mass" (bottom left), "favours control effort" (bottom right). Position in the triangle is a weighting among three objectives. The triangle is split into two coloured regions (green on the left, blue on the right) with nested white contour lines and grey dots scattered through. A blue star sits in the blue region, a green diamond in the green region.
2. Meaning, as far as I can tell: the two colours are regions where a different pairing of objectives dominates (labels: region 1 "pointing error trades against control effort", region 2 "total mass trades against pointing error"). Contours look like levels of a fitted surface over the weighting, with closed rings around the green marker (a peak or optimum). Markers 1 and 2 are the best point in each region. Grey dots: candidate designs, placed by their weightings, with a faint second dot cloud (small, dim) behind them. Could not tell: what the contour values are (no scale), whether dots are data or samples from the model, what dot position means for a design (best-fit weighting?), why the faint dots differ from bold ones, what the contour lines in the blue region (open, crowding to the right edge) represent, and why the thin tick-like kink near the region boundary appears.
3. Takeaway: "In this design space the frontier has two zones: one where mass fights pointing accuracy and one where pointing accuracy fights control effort."
4. Ink: mostly data (regions, contours, dots). The big label boxes are annotation but earn their place. The faint corner labels are near-decoration in effect because they are hard to see.
5. Legibility: region callouts are bold and readable. Corner labels are very low contrast (pale grey on dark), small, and nearly lost; these are the axis labels, so that is a real problem. White contours on dark green are fine. Grey dots against green are readable; the faint dots are noise. The label box in the green zone covers the contour peak and part of the data.
6. False ideas: the two solid colours read as two clusters of designs even though the dots cross both. The "1/2" markers look like cluster centres. The star and diamond differ in shape for no stated reason.

## 2. ternary-cubesat-textured-C-light.png

1. Shows: same kind of triangle, corners "favours pointing error" (top), "favours energy balance" (bottom left), "favours depth of discharge" (bottom right). Three pastel regions: pink at the top, green bottom left, blue bottom right, each with its own contours and a black-outlined marker (square 3, diamond 2, star 1). Dots scattered throughout. Labels say each region is driven by one objective "alone".
2. Meaning: three regions, each one dominated by a single objective (pointing error alone, energy balance alone, depth of discharge alone). Contours are black nested curves, again levels of something, shrinking toward the markers, which sit at corners. Markers are the optimum of each region and sit on the corner or edge (bottom-left diamond at the corner; star at the lower right edge; square at the top vertex). Could not tell: what the contours measure, what the dots are, why the contours in green and blue are sweeping arcs that do not close, why the regions have jagged or small notched boundaries at the centre (a little wedge at the centre-bottom), whether "alone" means the other objectives do not matter or are at the corner.
3. Takeaway: "The weighting space splits into three regions, each led by a single objective; trade-offs only occur at the boundaries."
4. Ink: nearly all data. Colour fill, contours and dots all carry something. The centre notch is a feature of the data or an artefact; unclear. Label boxes overlap data but are placed near empty spots.
5. Legibility: best of the four. Black on light, corner labels strong and readable, region boxes readable. Contour lines crisp. Dots grey on pastel is fine. Marker numbers 1/2/3 are small but legible.
6. False ideas: three pastel blobs with dots reads as a three-cluster picture (the idiom of clustering), though dots cross region boundaries. "Alone" invites reading that the three regions are pure single-objective, which makes it look like there is no trade-off in the region at all, the opposite of a trade-off figure.

## 3. ternary-cubesat-trilemma-dark.png

1. Shows: a triangle, corners "favours settling time" (top), "favours pointing error" (bottom left), "favours total mass" (bottom right), filled with one uniform brown/amber colour, nested rounded contour rings around a centre point, a gold star marked 1 near the centre, and grey dots all over. Label: "all three trade" (cut off: reads "all three trade" with the box edge clipping the text; likely "all three trade against each other").
2. Meaning: a single region, one optimum near the middle: all three objectives are in tension and the best balance is interior. Contours are concentric levels. Dots as before. Could not tell: contour values, the dot meaning, and the label is truncated so I cannot read the whole claim.
3. Takeaway: "Here there is just one region; the best compromise is the middle and every objective gives something up."
4. Ink: contour rings are data; the flat fill adds nothing; empty space is not a problem. Overall less information than the others, because there is only one region. Label box is clipped, a defect.
5. Legibility: corner labels pale and low contrast on dark, hard to read (same issue as A). Label text clipped by its box. Contours clear. Dots fine.
6. False ideas: none strongly; the single colour could read as "one cluster". Not an idea beyond the data, but it also does not show the thing the document wants (several regions).

## 4. ternary-cubesat-textured-B-dark.png

1. Shows: a triangle with corners "favours settling time" (top), "favours control effort" (bottom left), "favours depth of discharge" (bottom right). Two regions: a large green one on the left and a smaller blue one on the right and bottom right corner, with a ragged boundary (small steps along it). Contours: closed rings in the green zone, arcs in the blue. Star 1 at the lower-right corner, diamond 2 inside green. Dots throughout.
2. Meaning: two regions, green "settling time trades against control effort" with an interior optimum, blue "depth of discharge alone" with the optimum at the corner. Could not tell: same list as A (contour values, dot meaning), plus the ragged boundary: is it real structure or numerical resolution? Contours cut off abruptly at the boundary in places.
3. Takeaway: "Two zones: a large one where settling time and control effort trade off, and a smaller corner where depth of discharge decides alone."
4. Ink: mostly data. The jagged boundary and clipped contours suggest rendering artefact, which weakens the data claim.
5. Legibility: corner labels pale and hard to read; region boxes legible; the blue box lower right sits on top of contour lines and near the marker. White contours on dark fine.
6. False ideas: two big solid colour blocks read as two clusters of designs; the ragged boundary suggests noisy classification, which the model should not have.

## Ranking for a figure meant to show that the frontier model has several regions with different leading trade-offs

1. C-light. Three regions, three different leading objectives, strongest legibility, labels readable, corner labels visible. Weak point: "alone" wording and clusterish pastel blobs.
2. A-dark. Two regions with different trade-off pairs (this carries the "different trade-offs" idea better in words than C, since the labels name pairs), but only two regions and weak corner labels.
3. B-dark. Two regions, one of them "alone", ragged boundary looks like artefact, weak corner labels.
4. trilemma-dark. One region only; does not show several regions at all; label clipped.

If only one: C-light, because it shows the most regions and is the only one I could read without squinting. A fix I would want regardless: say what the contour lines and dots are, and make the region fill read as model regions rather than clusters (for example lighter fill, outlined boundaries).
