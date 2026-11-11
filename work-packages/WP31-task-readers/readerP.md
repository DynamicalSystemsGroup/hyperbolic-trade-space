# WP31 task reader P (planted table P, K0 hidden), verbatim return

READER P REPORT

(1) CHOICE: K = 2. Colleague version: the mean slack drops by about 0.27 going from K=1 to K=2, then only 0.003-0.005 per extra term. That is the "one large drop then small ones" break the page describes. At K=2 the two terms are fairly balanced (thinnest term share 0.25 at tau=50, 0.48 at tau=20). Refits on resampled rows barely move the exponents (0.02 at K=2, but 0.05-0.07 at K=3 and 4), and the K=2 fit is certified. K=3+ buys almost nothing (slack 0.626 to 0.621 to 0.617 to 0.614) and has thinner terms. Caveat I would tell them: the slack keeps falling by construction, so this is a judgment call. The page gives no threshold and no held-out criterion. I also had to guess the temperature (see 4).

(2) EVIDENCE (400x4 table, min value 0.00186, all positive). Tau was my guess; I used 50, 20 and 100.
tau=50, K=1..5:
- mean slack 0.897, 0.626, 0.621, 0.617, 0.614
- thinnest share 1.00, 0.25, 0.33, 0.13, 0.12
- status: K=1 not_applicable, K>=2 certified
- radius: K=2 3e-04, K=3 3e-05, K=4 2e-05, K=5 9e-06
- drops: 0.271, 0.005, 0.004, 0.003
- movement over 3 draws: K=2 0.02/0.02/0.02; K=3 0.05/0.07/0.05; K=4 0.06/0.07/0.07
tau=20:
- slack 0.822, 0.575, 0.563, 0.555, 0.549
- thinnest 1.00, 0.48, 0.10, 0.09, 0.10
- drops 0.247, 0.011, 0.008, 0.006
- movement at K=2: 0.03, 0.04, 0.04
tau=100:
- slack 0.931, 0.644, 0.642, 0.639, 0.637
- thinnest 1.00, 0.00, 0.00, 0.00, 0.00
- drops 0.287, 0.002, 0.002, 0.002
- movement at K=2: 0.01 each
All K>=2 fits were certified. The break at K=2 is present at all three taus. The thinnest-term share at K=2 is not stable across taus (0.25, 0.48, 0.00).

(3) WHAT HELPED, in order of use:
1. The "Methods" bullet list, especially "Mean slack against K" (read the drop per added term).
2. The helper code block (fit_k, sweep, movement). I copied it nearly as is.
3. The planted-table paragraph, to see what a clear break looks like (a big first drop, then 0.005 or less).
4. The cubesat paragraph on thinnest-term share and the overlapping movement ranges, as a warning against over-reading either check.
5. The PCA-elbow paragraph, for the idea that slack keeps falling and there is no floor.

(4) STUCK POINTS AND CONFUSION:
- Temperature: "every check below reads fits at one temperature, selected at K = 1 (Fitting)". The page never says how to select it for my own table. Its examples use tau=50.0 for the planted tables and `case.fit_study(s, K=1).tau` for the cubesat. I had no recipe for my table and guessed 50, then tried 20 and 100. The conclusion held, but the thinnest-term numbers changed a lot.
- "Fitting": I was not allowed to open that page, so I could not follow the pointer to it.
- "thinnest... depends on the band": "band" is never defined (near-frontier band?). I could not tell what sets it or whether I can change it.
- "radius" and "certified": "assignments hold under small changes of the terms". I can read the status, but I have no idea what radius size is good or bad. The page only says "it does not say K is right".
- "unmatched" and "found" apply only to planted tables. That is fine, but the sweep helper has the `planted` argument and I had no use for it.
- Movement: "at most 2" and "offers no threshold". I got 0.02-0.07 and cannot say whether that is stable. The only reference points are cubesat ranges of 0.09-0.69 and planted values of 0.02-0.24. By comparison mine is small, so I read it as stable, but that is my inference.
- The sweep helper asserts `drops[-1] > 0.002`. With tau=100 my last drop was 0.002 (rounded), so it might trip. I removed the asserts in my copy, so I do not know if it would have run as written there.
- Planted check: "Fit make_frontier_data(n_terms=K0) at your number of designs and metrics". I did not know which K0 to try for my table, or how to compare. I skipped it. I did not run the planted-table or cubesat blocks beyond the imports.
- The page gives no decision rule that combines the checks. "A break is read together with..." leaves the final call to me.

(5) CODE BLOCKS: The helper block ran as written, apart from my removal of the `assert` lines in sweep (not tested with them). `sys.path.insert(0, "examples/adcs"); import case` succeeded because I ran from the repository worktree root. A reader who runs from elsewhere would hit an ImportError, and the page does not say to run from the repo root. The first attempt of mine failed only on my own relative CSV path. `sweep` and `movement` ran on my table with no errors or warnings. I did not run the planted-table blocks, the K0 loops or the cubesat blocks (case.load_study), so I cannot say whether they ran as written.

(6) SCREENSHOT: I took only a 0.5-scale screenshot, which the tool returned inline, so there is no saved file at /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp31readers/returns/readerP-page.png. Description: dark-theme MkDocs page with a left header, the "Choosing K" title, the Methods bullet list with inline code styling, and the start of the code block with a copy button. It rendered fine, and I saw nothing broken in the top section. I did not scroll through the rest visually, only via get_page_text. Scripts: /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp31readers/returns/readerP.py and /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp31readers/returns/readerP2.py.
