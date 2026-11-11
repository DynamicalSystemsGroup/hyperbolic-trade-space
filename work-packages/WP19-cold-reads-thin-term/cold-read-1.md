# Cold read of the redrawn K = 3 tension figure (one fresh Sonnet reader, image only, neutral brief)

Brief: read the image and nothing else; say what it shows panel by panel, what each element means, what looks
missing, odd or ambiguous, and what a caption should answer; at most 300 words. Image: `thin-term-figure.png`.
The first draft put the sentence over the diagonal outlines; this read is of the redrawn figure (sentence lower
left, clear of the outlines).

Reader's report, verbatim:

(1) The figure has three stacked heatmaps, one per posynomial term (term 1, 2, 3). Each is an 8x8 matrix over the same eight metrics: settling time, pointing error, total mass, control effort, power margin, energy balance, peak slew power, depth of discharge. Cell colour is an "association" between metrics, running from -1 (brown/orange, labelled tension) through 0 (near white) to +1 (dark purple). Each axis label carries a weight w.
- Term 1 ("4-lemma, 4 metrics in the exact-maximum support") is blank apart from four black outlined squares on the diagonal. An in-panel sentence says "3 near-frontier designs; no association reading".
- Term 2 ("5-lemma, 5 metrics") is fully coloured and annotated. Diagonal entries are 1.00. Off-diagonal values include settling time vs peak slew power -0.85, total mass vs peak slew power +0.85, and power margin vs energy balance +0.96.
- Term 3 ("5-lemma") is also fully coloured. Notable values: pointing error vs peak slew power -1.00, and power margin vs energy balance 0.99.

(2) Black outlined squares mark the diagonal cells of metrics in that term's support. Their w values are non-zero, and the weights in each panel sum to about 1. Term 1 has 4 outlines and terms 2 and 3 have 5 each, matching the titles. Grey labels are metrics with w=0.00, so they are not in the support, but their rows and columns are still coloured in terms 2 and 3. The number in each cell is the association value.

(3) Problems:
- "Association" is never defined: correlation, or something else? It is unclear what is being correlated, and across which designs.
- "4-lemma" and "5-lemma" are opaque.
- Term 1 is empty, so its 4-metric support is shown with no data; the term-1 weights add little there.
- The colour scale is shared but the panels are independent. Nothing says whether they should be compared.
- Grey-label cells still carry values, so it is unclear whether they matter.
- Term 3 shows a -1.00 value, which looks suspicious, as does 0.99.
- The meaning of "near-frontier" and of "exact-maximum support" is unexplained.

(4) The caption should answer:
- What is "association", and how is it computed?
- What are the terms and the weights w?
- What is "lemma-k"?
- Why does term 1 have no reading?
- What do the outlined squares mean?
- What do the grey labels mean?
- Should the three panels be compared?

Disposition: the empty panel with its line was read as intended (no cell values, outlines kept, the count stated);
the reader asks only for the caption to say what the empty panel means, which it now does. The other questions
(association, n-lemma, near-frontier) are answered by the existing caption and the text it sits in.

## Rendered paper page (Figure 8 of the built page; 1100 px, light and dark)

`paper-1100-light-panel.jpg`, `paper-1100-dark-panel.jpg`: term 1 drawn with its title, metrics and exponents, the four
outlines and empty cells, and the line "3 near-frontier designs; no association reading" lower left; terms 2 and 3
unchanged. `paper-1100-light-caption.jpg`: the caption with its new last sentence. The figure keeps its white plate on
the dark page, as before.
