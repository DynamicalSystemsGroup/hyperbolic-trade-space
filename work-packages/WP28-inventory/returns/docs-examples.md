# docs-examples

## Q1. What the page conveys

It shows the package run end to end on one real table (the cubesat study): what the fit found (contending sets, term shares, mean slack, regime dependence), how to draw it with a few lines of code, how requirements are read after the fit, a ternary plot on synthetic data, and the command that reruns the study.

## Q2. Which story sentence it serves

Home page: "Examples: a cubesat trade study across power, mass and attitude control." It also serves the Home page's "It then tells you which metrics contend, with what elasticity, where each design sits ... and where the table has gaps", and the root page's "let the analysis be rerun" (the Run it section).

## Q3. Verdict and reason

advances. The Home page promises a cubesat trade study as the docs' worked example, and this is the only docs page that carries it; a practitioner gets to see what the fit reports on a real table and how to reproduce it. The paper's case sections (sect-case-analysis, appendix-d) cover the same study for the paper's reader, but the docs story needs a usage-shaped version with code, and only this page gives it.

## Q4. Unit already carrying it

Not applicable (verdict is advances). Overlap worth noting: the findings list (contending set, 0.243 / 0.132 / 0.088 mean slack, 17 / 10 / 73 percent shares, regime dependence) likely restates sect-case-analysis and appendix-d of the paper.

## Q8. Three judgements

- Against the Home page: it delivers the promised cubesat study and shows contention, position of designs relative to the surface (Figure 7), and the estimator's transform in use. It does not show the "with what elasticity" part explicitly (no exponents are reported), nor where the table has gaps beyond "max gap" named as a column.
- Against the root page: it meets the bar "let the analysis be rerun" (the Run it section, the committed table) and "show its reasoning" in part (tension report figure). "Say where the data do not reach" is only touched (Figure 7 "shows coverage").
- Against its own opening sentence ("The worked case is a cubesat model coupling power, mass and attitude control"): the first four sections do this. The ternary section switches to a synthetic table and says eight metrics cannot be drawn for the cubesat, so it does not do what the opening sentence says the page is about.

Serves none of the three:
- "A ternary plot places a design by its shares of a total among three metrics..." (the whole "Three metrics as shares of a total" section, including "Reading it" and "Limits"): a plotting helper on synthetic data, not the cubesat study, and no story sentence asks for it. It would sit better with the chart or plotting guidance.
- "Refitted on three design sets in one conditioning, the one-term contending set barely moves": a robustness check of the case, not something a first-time practitioner needs to use the package; arguably paper material.
- "No metric twice. No pair of the eight metrics reaches a rank correlation of 0.99..." is borderline: useful reading advice, but not tied to any story sentence.

## Q9. Read twice and could not place

- "With the fit temperature chosen by select_temperature for a tenth of designs above V = 1": what "a tenth of designs above V = 1" means is not explained on the page.
- "At the one-term temperature (case.mean_slack_fixed_tau) the mean slack falls": mean slack, and why the temperature is fixed, are not defined here.
- "status certified": not explained on the page.
- "a price at the one-term frontier, in band widths": "band widths" and "price" are not defined here.
- "Z0 and Z1, the first two of seven position coordinates, meaningless alone": I could not tell why they are shown if meaningless alone, beyond the "coverage" remark.
- The Run it column list ("tau, band 1/tau, objective_, ... gamma, radius, bound"): a run of names with no reading for a newcomer.
