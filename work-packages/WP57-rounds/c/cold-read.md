# WP57c: the unit's cold read of the rendered appendices (1,280 px)

The built site (`cd paper && BASE_URL=/paper uv run --frozen myst build --html`) served on port 8871, captured
headless by Playwright (Chrome) at 1,280 by 900. Page checks by the capture script: "Job." occurs twice on the
supporting page (E and H, WP57d's); every anchor `appendix-c`, `sub-c-5`, `sub-c-8`, `appendix-d`, `sub-d-8`,
`sub-d-9`, `sub-d-17`, `sub-d-18`, `sub-d-19` resolves; the old rules' words are absent and the four rule names
present; page scroll width 1,280 (no horizontal overflow of the page).

| Capture | What a reader meets | Found | Done |
|---|---|---|---|
| `C-top.png` | The heading, then C.1's two tables at once; no opening paragraph | the table of contents reads C.1 to C.8 in order; C.1's heading names its subject | nothing |
| `C5.png` | The metric rule, one five-row preview (primary), the one-axis paragraph with the supplement's link, the 17 pairs | the preview's thirteen columns scroll inside the table at this width (the table's own scroll, as before WP57c); the count line ("The 17 of 78 pairs at \|Spearman\| 0.5 or above in a regime") says what is printed | nothing; the width is the table's, unchanged |
| `C8.png` | The cost paragraph, the lower-bound sentence, the case page's link | "Its cost is a lower bound" followed "larger series are dearer", so "Its" read as the 1U series' | reworded to "The covered cost is a lower bound" (C994 follows); recaptured |
| `D-top.png` | The one line naming the two supplement files, then D.3 | the line says what the files hold and nothing about the page | nothing |
| `D8.png` | The status paragraph with the table's sentence and the termination page's link; one table per regime with `conditioning_`; the planted record | the case tables no longer carry term rows and shares (D.3's); the planted table keeps them, its only record of the planted cells | nothing |
| `D17.png` | The thresholds and their ladder; the price's definition; the first table | no column glossed; the paragraph reads as definitions | nothing |
| `D19.png` | The shortlist's rule, the four rules as a list, the coverage probability's source, the stock regime's funnel, then the shortlist table with coverage probability and the nondominated mark | the stock regime's sentence sits between the rules and the table it does not describe; it is the regime comparison the map keeps | moved below the shortlist table (cell `sent-D-decision-baseline` after `tab-D-decision_designs`); recaptured. At 1,280 px the table's last column, the nondominated mark, sits in the table's own horizontal scroll, as the old marks column did |
| `corollary1.png` | Corollary 1's commentary ends with the pointer to D.18 | the link resolves to D.18 | nothing |
