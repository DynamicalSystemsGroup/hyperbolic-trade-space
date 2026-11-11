# fig-tau-sweep

## Q5 (a) What the image shows (written before the caption)

Three panels under the title "The K = 1 fit against the fit temperature tau, primary regime". The x-axis everywhere is a fit temperature tau on a log scale, from 3 to 1000 (and an infinity "limit" in the heat map).

- Top left: the fraction of designs above V = 1 falls steadily from about 0.45 at tau = 3 to under 0.01 at large tau. A dashed horizontal line marks "target 0.1" and a solid vertical line at about 38 marks where the curve crosses it.
- Top right: an effective sample size falls from about 560 at tau = 3 to near zero at large tau. At the same vertical line (tau about 38) it is labelled n_eff = 23.
- Bottom: a heat map, rows are eight metrics (total mass, energy balance, pointing error, depth of discharge, settling time, control effort, power margin, peak slew power), columns are tau values, the colour is an exponent w (dark is large, white is at most 0.001). One column, tau = 38.1, is outlined and annotated with numbers: 0.36, 0.18, 0.16, 0.16, 0.14 for the first five metrics, and blank for the last three. Control effort has a non-zero exponent only for tau up to 15. Power margin and peak slew power are white throughout. Total mass is darkest everywhere.

So: as the temperature is raised the fit uses fewer and fewer designs, and the chosen tau of 38.1 is where about a tenth of designs are above V = 1; at that tau five of eight metrics carry non-zero exponents.

## Q5 (b) After the caption

Mostly yes. The caption's pieces are all in the image: the fraction above V = 1 with the dashed target 0.1, the effective sample size with its value at the fit temperature, the vertical line at the fit temperature, the exponent heat map with the last column the infinity limit, rows ordered by the exponent at the outlined column with values printed, white rows last, a white cell meaning an exponent of at most 0.001, and a scale topping at the largest exponent.

What it does not show (the paper's own "Does not show" line agrees): fit quality, the frontier or the designs near it, any K > 1 fit, why a metric has no exponent, and exponent values off the outlined column, where close exponents share a grey. Also, from the image alone: the vertical line is drawn at about 38 but the crossing of the curve with the 0.1 dashed line looks slightly below 0.1 (the text says 0.092), so the "within 0.01 of the target" is read from the text, not seen. The caption does not say what a number such as "n_eff = 23" is a count of until the text beneath it does, and the right panel's tail (values near zero beyond tau about 100) shows no visible differences.

## Q5 (c) Sentence test

"The fit temperature is chosen as the tau at which the fraction of designs above V = 1 is within 0.01 of 0.1 (tau = 38.1), which leaves an effective sample of about 23 designs, and at that tau five of the eight metrics carry exponents."

The figure conveys more than that sentence: the whole sweep (how fast the fraction and the effective sample fall as tau rises), that the effective-sample cost is steep and has mostly flattened by tau about 100, that total mass dominates at every tau, that control effort drops out above tau of about 15, that power margin and peak slew power never enter, and the shape of the limit. The text beneath already states 38.1, 0.092, 0.0262 and 23.1, so the sentence's numbers are carried twice.

## Q1. What the figure conveys

How the K = 1 fit changes with its temperature, which temperature was chosen (where about a tenth of designs lie above the surface), what that leaves in effective sample (about 23 designs), and which metrics carry the exponents there.

## Q2. Sentence of the story served

Two, both loosely. The abstract's "a soft support that a few designs may exceed, not a regression" (the fraction-above-V = 1 panel is the visible meaning of "a few designs may exceed"). And main-results item 7 ("on a cubesat model ... the terms separate contending sets that one term blends"), for which the bottom panel gives the one-term baseline: five metrics from controls, power and mass sharing one exponent vector. Neither sentence is about the temperature selection itself, which is a Section 5 convention.

## Q3. Verdict

advances

The soft-support claim and the one-term "blend" in item 7 each need to be seen at least once on the case: the abstract only asserts that some designs may exceed the surface, and the figure is where one sees how many (the target 0.1) and what that costs in effective sample. I found no other unit named in what I was given that carries the sweep, though the page itself points to Section 5 for the convention and Figure 9 for the stock regime, which I did not read. The claim is thin: the sentences that need it are served by the chosen column alone, and the sweep to the left and right of it is context.

## Q4. Repeats

Not applicable. (If anything, Section 5 carries the convention in words and Figure 9, second panel, the stock-regime counterpart; neither is a repeat of this sweep as far as I could read.)

## Q9. Read twice and could not place

- "white rows last in the table's order" (caption): I could not tell what "the table's order" is; the three white rows appear in an order (control effort, power margin, peak slew power) that I could not trace to anything on the page.
- "the band 1/tau is 0.0262" (text under the figure): what the band is, and why it is 1/tau, is not explained on this page.
- "within 0.01 of the target (a convention, Section 5)": why 0.1 is the target and why within 0.01 is the rule is deferred to Section 5, which I was not given.
- "Figure 4 shows how the temperature is selected. Where the answer must be known, we plant it": the jump from selecting the temperature to planting an answer has no link on the page; I could not see how the one follows from the other.
- "the exponents at the fit temperature rest on about 25 of the 706 designs" against the figure's and the text's n_eff of 23 (23.1): two numbers for the same quantity on one page.
