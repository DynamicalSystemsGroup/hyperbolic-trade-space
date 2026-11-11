# WP31 task reader Q (planted table Q, K0 hidden), verbatim return

(1) CHOSEN K = 3 (moderate confidence; K=2 is the nearest alternative).
Colleague version: At tau=50 (a number I took from the page's planted example, not from my table), mean slack on our 400x4 table drops 0.146 (K1->2), 0.060 (2->3), then 0.004 and 0.004. That is a break at K=3: the third term still pays, later ones don't. The fit is certified at every K>=2. Resampling movement at K=3 is small (0.03 on both draws) but at K=4 it is 0.28/0.19 and at K=5 0.19/0.48, so K=4+ is unstable. The thinnest term at K=3 holds 0.22 of the near-frontier designs, so it is not a sliver (K=4 drops to 0.11). The pattern is the same at tau=20 (drops 0.132, 0.058, 0.010, 0.008) and tau=100 (0.162, 0.061, 0.002, 0.002). At tau=100 the thinnest share at K>=3 is 0.00, which is a warning sign. Caveat: the page says no check decides K alone and there is no held-out criterion. I can't say how many of the three terms are real versus fitted-alone designs.

(2) EVIDENCE (table 400x4, min 0.0037, all >0; scripts in /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp31readers/returns/readerQ.py and readerQ2.py)
tau=50:
K=1 slack 0.833 (thinnest 1.00)
K=2 0.687 (0.20, certified, radius 1e-04)
K=3 0.628 (0.22, certified, 5e-05)
K=4 0.624 (0.11, certified, 1e-04)
K=5 0.619 (0.17, certified, 4e-05)
drops 0.146 0.060 0.004 0.004
movement (2 draws): K=2 0.03/0.08; K=3 0.03/0.03; K=4 0.28/0.19; K=5 0.19/0.48
tau=20: slack 0.756, 0.624, 0.565, 0.556, 0.548; drops 0.132 0.058 0.010 0.008; thinnest 0.23, 0.26, 0.14, 0.11
tau=100: slack 0.872, 0.711, 0.650, 0.648, 0.646; drops 0.162 0.061 0.002 0.002; thinnest 0.37, 0.00, 0.00, 0.00
Planted reference, 400x4, tau=50 (the page's planted check): K0=2 drops 0.108, 0.005, 0.004, 0.003 (matches the page's 0.108 and 0.005); K0=3 drops 0.163, 0.029, 0.005, 0.004 (matches the page). Our table's second drop (0.060) is larger than the planted K0=3 table's (0.029), so a break at 3 looks real in shape, but I only compared by eye.
Default temperature of HyperbolicTradeSpace(n_terms=1) is 10.0 (get_params). I did not use it, because I could not tell whether it is the "selected at K = 1" temperature.

(3) WHAT HELPED, in order of use
- The Methods list, especially "Mean slack against K" (read drops, look for one large drop then small ones) and "Thinnest term".
- The helper code block (fit_k, sweep, movement), which I copied nearly verbatim.
- The planted-table paragraph, whose numbers I could reproduce and use as a yardstick for what a break looks like.
- "Movement under resampling" plus the cubesat paragraphs showing movement ranges overlap, which told me to treat that check as weak.
- The closing paragraph on the elbow and large K ("A break is read together with the thinnest-term and resampling checks").

(4) STUCK POINTS AND CONFUSIONS
- Temperature: "Every check below reads fits at one temperature, selected at K = 1 (Fitting)". The page gives no recipe and the link was off limits. I guessed tau=50 from the planted example and bracketed it with 20 and 100. A first-time user can't do the task as stated without leaving the page. The cubesat block uses case.fit_study(s, K=1).tau, which needs the repo's examples/adcs and isn't usable on a user's own table.
- "mean_slack_ is comparable across K at one temperature, and objective_ is not": I don't know what slack is (units, scale) or why objective_ isn't comparable. Is 0.004 small? Only the page's own thresholds ("0.002" in the assert, "0.005 or less") hint at it.
- "the near-frontier designs", "the thinnest term's cell", "depends on the band": undefined jargon (near-frontier band, cell). The thinnest-term check has no usable threshold, since 0.22 vs 0.11 vs 0.00 gives no stated cutoff.
- "the assignments hold under small changes of the terms" and "radius": I can't tell what certification means in practice. The page says it "does not say K is right", so I ignored it.
- "conditioning_. The smallest eigenvalue per term ... (Termination)": listed as a check, but no helper code uses it and I couldn't tell how to act on it, so I skipped it.
- "Movement ... offers no threshold": I got 0.03 vs 0.28, but with only 2 draws I can't judge significance.
- The helper's assert `drops[-1] > 0.002` failed to hold for me at tau=100 (0.002), so I removed the assert. Asserts in a user-facing helper are surprising.
- The page says nothing on how to decide when drops are ambiguous, e.g. K=2 vs K=3 when the second drop is 0.06 against a first of 0.146. I chose 3 by judgment.
- The page says "the planted check ... at your number of designs and metrics", but it doesn't say which K0 to plant or how to compare, so I tried K0 = 2 and 3 only.

(5) CODE BLOCKS
Ran as written: the imports; the fit_k, sweep and movement helpers (apart from my removing the assert, and the sys.path/case import which I omitted since it needs the repo and isn't needed for a user table). The planted-table loop was run with the same sweep calls minus the `planted` argument, because the sweep(..., np.asarray(info["exponents"])) form needs the planted argument. I did not rerun it with the argument, so found/unmatched counts were not reproduced. The cubesat blocks (case.load_study etc.) were not run: they depend on examples/adcs and a relative path, so they fail for a pip-installed user. The planted slack drops matched the page's numbers (0.108/0.005; 0.163/0.029/0.005). The movement figures for planted table 0 were not rerun.

(6) SCREENSHOT
Tool could not save to file. A partial screenshot (top of page, mobile-width, dark theme) showed the title "Choosing K", the intro paragraph, the Methods bullet list and the start of the first code block, rendering cleanly. The intended file /private/tmp/claude-501/-Users-z--claude-spares-spare-4Zb8mW/71474a52-35d3-48fa-82b0-c1328e96b5d6/scratchpad/wp31readers/returns/readerQ-page.png was NOT written. I read the rest of the page via get_page_text only, so I did not see rendered code blocks or any figures lower down.
