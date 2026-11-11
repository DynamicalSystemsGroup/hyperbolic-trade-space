# docsfig-chart-holes

## Q5 (a) What the image shows (written before the caption)

A two-axis scatter plot, axes Z0 (about -3 to 2.5) and Z1 (about -3.3 to 3). Many small blue dots fill a roughly round cloud, densest near the origin. A subset of the blue dots is ringed in black. Around the outside of the cloud, mostly at the edges and corners, sit small orange squares on a regular grid. The orange squares ring the blue cloud and are absent from the dense middle. There is no legend and no title. I cannot tell what the orange squares or the black rings mean from the picture alone.

## Q5 (b) After the caption

Yes, the image shows what the caption says: orange squares on a grid at the rim of the cloud, none in the interior, so "no interior hole" is visible. It does not show: what the black-ringed dots are (the caption never mentions them); what Z0 and Z1 are (the alt text says "two position coordinates", but the axes just say Z0, Z1); how far "far from every design" is (the threshold is in the code, not the picture); or any actual white space. A reader sees a cloud with a frame of squares, and the squares at the rim look like an outline of the cloud, not like gaps. The picture also has no legend for blue, black ring or orange.

## Q5 (c) The sentence test

"find_holes marks grid positions far from every design as orange squares; on this seeded sample none fall inside the cloud, so they only trace its rim."

The figure conveys little more than that sentence: the rough shape and extent of the rim band, and that the black-ringed dots exist (unexplained). It does not show a hole being found, which is what the section heading promises.

## Q1. What it conveys

That the hole finder's output is a set of grid squares overlaid on the position-coordinate scatter, and that on this sample they sit at the rim because there is no interior gap.

## Q2. Sentence of the story served

Home page: "where the table has gaps". The page opening sentence also touches it ("gaps in that picture are candidates for white space"). It serves them only weakly, since the figure shows no gap.

## Q3. Verdict

does not advance.

The sentence the figure serves (gaps) needs a picture of a gap, and this one shows none; its own caption says so. The rim squares are the boundary effect of the grid, which is not something a user needs in order to use find_holes, and the one sentence in Q5 (c) carries all of it.

## Q4. If "repeats"

Not applicable. (If a picture of holes is wanted, I have not read the Examples figures, so I cannot say whether the Examples figure on chart coordinates, unit docsfig-adcs-coordinates, carries it better.)

## Q8. Against the three sentences

- Home page ("where the table has gaps"): does not help a user find a gap; it shows a table with no gap and squares that read as an outline.
- Root page ("say where the data do not reach"): partly; the squares at the rim could be read as where the data stop, but the caption calls them candidates for white space, which is a different claim.
- Page opening sentence ("a reversible rewriting of the metrics", then the holes section's "gaps in that picture are candidates for white space"): the figure illustrates the code's output but not a usable gap; a user could run the code, see squares, and not know whether those matter.

## Q9. Read twice, could not place

- "black-ringed dots": no key anywhere in the caption, alt text or page text.
- "This seeded blob has no interior hole": why choose a sample with no hole to illustrate hole finding.
- "grid positions far from every design" at the rim: the page says find_holes only takes grid points "inside the convex hull", yet the squares sit at the visible edge of the cloud, and I could not tell how the hull relates to the squares.
- "Z0", "Z1": the page calls these position coordinates but the axis labels do not say so.
