# WP31 task reader C (cubesat primary regime), verbatim return

READER C REPORT (cubesat, primary regime)

(1) CHOSEN K AND REASONS
I would tell a colleague: use K = 2 as a working choice, with low confidence, and say plainly that the data do not pick K.
- Mean slack gives no break. Drops per added term are 0.112, 0.044, 0.017, 0.010. The biggest single drop is the first added term (K=1 to 2), and K=2 already captures about half of the total fall to K=5.
- K=2 has the smallest resampling movement (0.09 to 0.45), versus 0.25 to 0.69 at K=3 and 0.17 to 0.54 at K=4. The page says these ranges overlap, so this does not exclude any K.
- Every fit at K>=2 is certified, so the certificate does not discriminate.
- The thinnest term holds 0.07 at K=2, which is small: one term is fitted to few near-frontier designs. K=3 gives 0.10 and K=4 gives 0.08, so going higher does not fix that.
- The page offers no held-out criterion, so no check settles K. K=2 is the simplest model that takes the largest drop, with the caveat that its thinnest term is thin. K=3 is a defensible alternative; I could not tell the two apart from the page's checks.

(2) EVIDENCE COMPUTED
Primary regime: M has shape (706, 8); K=1 tau = 38.096.
- K=1: slack 0.243, thinnest 1.00, status not_applicable
- K=2: slack 0.132, thinnest 0.07, certified, radius 1e-04
- K=3: slack 0.088, thinnest 0.10, certified, radius 1e-05
- K=4: slack 0.070, thinnest 0.08, certified, radius 4e-05
- K=5: slack 0.061, thinnest 0.04, certified, radius 3e-06
- Drops: [0.112 0.044 0.017 0.010]
- Movement over 3 draws:
  - K=2: [0.09 0.10 0.45]
  - K=3: [0.25 0.31 0.69]
  - K=4: [0.23 0.54 0.17]

(3) WHAT HELPED, IN ORDER OF USE
1. The opening paragraph: "you do" choose K, and no check decides alone.
2. The Methods list: it says what each check cannot say.
3. The helper code block (fit_k, sweep, movement), which I copied.
4. The cubesat section: its narrative gave expected numbers to compare against, and it states that the primary regime shows no break.

(4) STUCK POINTS AND CONFUSIONS
- The page never gives a decision rule. It ends with no stated choice for primary, which is what the task asked. I had to make the choice myself: "The ranges overlap, so this check excludes none."
- "selected at K = 1 (Fitting)": I do not know what temperature selection is or why it is fixed at K=1. The page points to another page that I was told not to open. I used case.fit_study(s, K=1).tau without understanding it.
- "mean_slack_": never defined on this page. I do not know what slack is, or whether 0.132 is good or bad in absolute terms.
- "near-frontier designs", "cell", and "the band" in "it depends on the band": these are unexplained. I could not tell what counts as a "thin" term (is 0.07 thin?). The page says "its thinnest term holds 0.07 already at K = 2", implying it is bad, but gives no threshold.
- "termination_.radius" and "certified": the radius is described only as "assignments hold under small changes of the terms". I could not judge what a radius of 1e-04 versus 3e-06 means.
- "Movement ... summed absolute differences, at most 2": at most 2 is unexplained (the exponent vectors presumably sum to 1). I could not tell whether 0.45 is big.
- The movement check seeds draws by seed=s, so numbers vary by draw. The page says "offers no threshold", so the check is of little use for choosing.
- The "stock" regime and the planted tables are irrelevant to the task. I skipped the planted code and did not run it.
- The sweep helper asserts drops[-1] > 0.002 and that all drops are positive. If an assert fails, a reader gets no explanation.
- The page uses relative sys.path "examples/adcs", so it only runs from the repo root. I used an absolute path instead.
- The "Large K and the elbow in PCA" section assumes I know the PCA elbow heuristic. Fine for me, but the section does not say what to do about it.

(5) DID CODE RUN AND NUMBERS REPRODUCE
The helper code ran without error (I dropped the planted/stock parts and the assert line, since I passed no planted array). On the primary regime the numbers reproduce, and the page's "drops by 0.112, 0.044, 0.017 and 0.010" matches exactly. Thinnest at K=2 is 0.07, as stated. Radii run from 3e-06 to 1e-04, as stated. Movement ranges are 0.09 to 0.45 at K=2, 0.25 to 0.69 at K=3 and 0.17 to 0.54 at K=4, all matching exactly. I did not run the planted-table blocks or the stock regime. I ran the sweep without its assert; the drops are all positive and the last drop is 0.010, so the assert would have passed. Everything I ran used the case.load_study and case.fit_study helpers from the examples directory, and both worked as the page shows. One caveat: the page does not show how to get tau, and it uses case.fit_study(s, K=1).tau without explanation; this works but is only visible in the code block.

(6) SCREENSHOT
The browser tool could not save a screenshot to a file, so no file exists at the requested readerC-page.png path. I took a half-scale screenshot of the rendered page (top part, dark theme). It showed a clean layout: the heading "Choosing K", the intro paragraph, the Methods bullet list with inline code styling, and the start of the code block. No rendering errors were visible in the top viewport. I did not scroll through the lower sections visually; I read them with get_page_text. The tab is closed.
