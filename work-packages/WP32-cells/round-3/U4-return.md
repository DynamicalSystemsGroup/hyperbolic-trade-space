# U4 round 3 return

Header
- model: Sonnet
- persona: U4
- head: 60f92d9
- table: ./table.csv
- model source: ./model.sysml
- stage URL: http://127.0.0.1:8791/

## 1. The code (final script, as run: run.py)

```python
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
                                    select_temperature, tension_report)
from hyperbolic_trade_space.plotting import plot_tensions
df = pd.read_csv("table.csv")
print(df.describe().T[["min","max"]])
cols = ["flow_lps","head_m","power_kw","mass_kg"]
A = df[cols].to_numpy()
print("any<=0:", (A<=0).any(), "nan:", np.isnan(A).any())
pre = LogAffinePreconditioner(orientation=[1,1,-1,-1])
M = pre.fit_transform(A)
tau = select_temperature(M, target_frac_above=0.10, bounds=(3,1e4))
print("tau", tau)
for K in (1,2,3):
    ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, "slack", round(ts.mean_slack_,3), "share", ts.term_share_.round(2),
          ts.termination_.status, ts.exponents_.round(2).tolist())
# the error message said: fit at temperature=4.76e+03 (band is 1/temperature)
ts = HyperbolicTradeSpace(temperature=4.76e3).fit(M)
r = tension_report(ts, M)
print("n_near", r.n_near_frontier, "band", r.band)
for t in (50.0, 200.0, 1000.0):
    tt = HyperbolicTradeSpace(temperature=t).fit(M); rr = tension_report(tt, M)
    print(t, rr.n_near_frontier, rr.exponents.round(2), np.round(rr.association[0],2).tolist() if hasattr(rr.association,'shape') else '')
print(r.lemma_name, r.contending_set, r.contending_exponents, r.exponents.round(2))
print(r.elasticities.round(2))
print(np.round(r.association,2))
ax = plot_tensions(r, names=cols); ax.figure.savefig("tensions.png", dpi=80)
```

## 2. Pages opened, in order
1. hts/README.md
2. ./model.sysml
3. http://127.0.0.1:8791/docs/ (home)
4. /docs/getting-started/
5. /docs/user-guide/overview/
6. /docs/user-guide/conditioning/
7. /docs/user-guide/fitting/
8. /docs/user-guide/choosing-k/
9. /docs/user-guide/tensions/
10. /docs/user-guide/chart/
Also ./table.csv (head, describe) and the package source traceback line (tensions.py, via the error). Read through curl as text, not a browser.

## 3. Errors
- Step 1: `uv sync` in hts/ worked; import worked. No stop. (I ran scripts with `uv run --project hts` from my own directory.)
- Step 5, first run, `tension_report(ts, M)` at K=1 with tau = 6023.1 (from select_temperature at target 0.10, bounds (3, 1e4)):
  `ValueError: only 6 near-frontier rows (|log V| < 0.000166027) but min_near_frontier = 10; use a larger band, band=0.00021 (the smallest round band with 10 rows on this term), or fit at temperature=4.76e+03 (the band is 1/temperature), or lower min_near_frontier`
  I refit at temperature=4.76e3 as the message said; it worked (10 near-frontier rows). I also tried tau 50, 200, 1000 for stability.
- 'not bracketed' was NOT raised by any call (select_temperature returned 6023.1 at the first try).
- Harmless stderr: matplotlib "findfont: Failed to find font weight normal for Lucida Grande, now using 500" (x3) on the plot.
- No code block copied verbatim from a page. I adapted the patterns from conditioning (LogAffinePreconditioner), fitting (select_temperature, n_terms), choosing-k (mean_slack_ sweep idea) and tensions (tension_report, plot_tensions) pages.

## 4. Questions for a colleague
- Is power really a separate attribute, or does the model define it from flow, head and efficiency (it does: ShaftPower = 9.81*Flow*Head/Efficiency)? The tool cannot know a column is a derived function of others; will it report that as a "tension"?
- Is it expected that tau comes out near 6000 on an exact-relation (simulated, noise-free) table, and that the default band is then too thin for the report? The fitting page warns tau moves with bounds on exact-relation tables, but not that tension_report then fails.
- Should design variables (diameter, speed, width ratio) be excluded, as the overview says ("Design variables and labels are configuration, not attributes")? I excluded them.
- Which temperature to quote in the answer, 4.76e3 or the lower ones? Results agreed.

## 5. Steps to the need
README (example uses make_frontier_data; no real-table path) -> docs home -> getting-started ("Your own data" points to conditioning) -> overview -> conditioning (orientation, shift) -> fitting (select_temperature, K) -> choosing-k (sweep) -> tensions (report, errors). I did not get lost; no searching. I had to skim choosing-k's cubesat parts as not mine. Detour: the first tension_report failure (above), cost one extra run. The tensions page says the band error message names the temperature; it does, and that worked.

## 6. Standing question
No. Nothing said SysML v2 or satellites were needed. The overview line "a SysML v2 model's exported table is one source" says any table works; the examples page is a cubesat but I did not need it.

## Answers to steps 2 to 6 in plain sentences
- Step 2 (conditioning): table has 200 designs, all positive. Quantities (attributes): flow_lps (larger better), head_m (larger better), power_kw (smaller better), mass_kg (smaller better). diameter_m, speed_rpm, width_ratio are design variables (configuration) and design_id is a label, so excluded. Orientation [1, 1, -1, -1] via LogAffinePreconditioner with default scaling, no shift (no zeros).
- Step 3 (fit): HyperbolicTradeSpace at K=1, temperature from select_temperature(M, 0.10, bounds=(3,1e4)) = 6023.1.
- Step 4 (K): I chose K=1. Mean slack at the same tau: 0.013 (K=1), 0.010 (K=2), 0.008 (K=3); no break, small drops. K=2 splits 0.89/0.11 of near-frontier share, with a second term that is mostly the same exponents (0.37, 0.14, 0.41, 0.07); K=3 has an empty third term (share 0.00). So the extra terms add little; the pump model is a smooth power-law-like relation, K=1 is enough. I did not run resampling movement.
- Step 5 (tensions): the report names a trilemma of flow, head and power (exponents 0.28, 0.23, 0.49); mass has exponent 0 (0.00) and does not contend, at tau 50, 200, 1000 and 4760. Association among near-frontier designs: flow with power -0.96, head with power -0.94, flow with head +0.80 (aligned), mass with flow -0.93 and with head -0.54 (mass is traded with flow, but is not binding). I am confident the contending set (flow, head, power) is stable across temperatures, and that power is the one pulling against flow and head. Caution: this is a near-exact relation (power = flow*head/efficiency in the model), so the "trade" is partly a definition, not a design choice; and that the negative association near the frontier follows from closure (the tensions page says so). I am less sure about mass: it never participates, which is consistent with mass depending only on diameter and width, not on the others.
- Step 6 (model help): the model source helped me read what the columns are (which are inputs and which are outputs, that power is derived from flow and head, which are ranges), and so to choose orientation and to drop the inputs. It did not get in the way, but the package has no hook to the model; I could not connect my own model to the tool other than by exporting the table (done for me) and reading the source by hand. The docs say any table works; no SysML reader is in the package, so I connected it only through the exported CSV and my own column choice.
