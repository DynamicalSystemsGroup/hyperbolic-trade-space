# U3 return

Header: model Sonnet; persona U3; head a3a61af; table ./table.csv; stage http://127.0.0.1:8791/; round 2.
Install to first fit: `uv sync` took 6 s wall (import worked immediately); first fit ran in the same minute; whole task about 3 min of tool time.

## 1. The code (analyze.py, as run with `uv run --project hts python analyze.py`)
```python
import numpy as np, pandas as pd
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
df = pd.read_csv("table.csv")
cols = ["strength_mpa","weight_kg","stiffness_gpa","cost_usd"]
A = df[cols].to_numpy(float)
assert (A>0).all()
pre = LogAffinePreconditioner(orientation=[1,-1,1,-1])
M = pre.fit_transform(A)
print(np.log(M).std(axis=0))
tau = select_temperature(M, 0.10, bounds=(3,1000))
print("tau", tau)
for K in range(1,5):
    f = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    t=f.termination_
    print(K, round(f.mean_slack_,3), f.term_share_.round(2), t.status, f.exponents_.round(2).tolist())
ts = HyperbolicTradeSpace(temperature=tau).fit(M)
r = tension_report(ts, M)
print(r.contending_set, r.lemma_name, r.contending_exponents.round(3))
print(r.exponents.round(2)); print(r.elasticities.round(2))
print(r.association.round(2), r.association_kind, r.n_near_frontier)
from hyperbolic_trade_space.plotting import plot_tensions
import matplotlib; matplotlib.use("Agg")
ax = plot_tensions(r, names=cols); ax.figure.savefig("tensions.png", dpi=80)
for b in (0,1):
    d = df[df.batch.isin(["A","B","C"])]
print(df.batch.value_counts().to_dict())
from hyperbolic_trade_space import frontier_in_original_units
print(frontier_in_original_units(ts, pre))
```

## 2. Pages opened, in order
1. hts/README.md
2. table.csv (head, wc, pandas describe)
3. http://127.0.0.1:8791/docs/ (home)
4. /docs/getting-started/
5. /docs/user-guide/conditioning/
6. /docs/user-guide/fitting/
7. /docs/user-guide/choosing-k/
8. /docs/user-guide/tensions/
9. /docs/user-guide/chart/
(No browser used; pages read by curl and stripped to text. Rendered chart not viewed on the site; I saved plot_tensions to tensions.png and looked at it.)

## 3. Errors
- `table.corr(numeric_only=True)` with system python3's old pandas: "TypeError: corr() got an unexpected keyword argument 'numeric_only'". It was a stray exploration command on the system python, not the package. I reran under `uv run`.
- Stderr noise from matplotlib: "findfont: Failed to find font weight normal for Lucida Grande, now using 500." (cosmetic).
- The README's clone line was not run: the checkout was already given; I ran `uv sync` in it. No other failure; no step blocked.

## 4. Questions for a colleague
- Is the `batch` column (A/B/C) a grouping to respect, or ignorable? I ignored it and used the 4 numeric columns; `sample` is an index.
- Are the rows all feasible designs? (Docs say remove infeasible rows first; there were no zeros or NaNs.)
- Which direction is better for each quantity? I assumed strength up, stiffness up, weight down, cost down.
- Does "contending" with a -1.00 association on 22 near-frontier rows mean a hard physical law or a sampling closure? The pages say association alone is weak evidence; no page gives a rule for how many near-frontier rows is enough.
- No page says how to choose the quantile target if 0.10 gives a tau (178) this large; it worked, so fine.

## 5. Steps to the need
README -> uv sync (6 s) -> README example read (it conditions with LogAffinePreconditioner) -> docs home -> getting-started -> conditioning (orientation, scaling) -> fitting (select_temperature, default target 0.10, bounds) -> choosing-k (recipe: tau at K=1, sweep mean_slack_) -> tensions -> chart. Went back once to choosing-k for the sweep helper idea (I wrote a shorter loop). Did not get lost; did not search. The chart page was read for completeness; I used only plot_tensions (from the tensions page).

Answers to steps 2 to 5:
- Step 2 (conditioning): all four columns are positive with no zeros. Oriented strength_mpa +1, weight_kg -1, stiffness_gpa +1, cost_usd -1; default standard scaling in log space (log-std was 1 per column, as the docs' diagnostic says). The batch and sample columns were dropped.
- Step 3 (fit): temperature chosen with select_temperature(M, 0.10, bounds=(3,1000)) = 178.2; K=1 fit exponents [0.49, 0.50, 0.00, 0.01].
- Step 4 (K): swept K = 1..4 at tau 178.2. Mean slack 0.578, 0.575, 0.573, 0.572: drops of 0.003, 0.002, 0.001, no break. K=2..4 are certified but the thinnest terms hold 0.24, 0.17, 0.13 and the extra terms have nearly the same exponents as the first. I chose K = 1 because adding terms buys almost nothing and the added terms are near duplicates. I did not run the resampling check; this is a judgement from slack only, which the docs say cannot decide K alone.
- Step 5 (tensions): contending set [0 1 3], called a trilemma, but the exponents are 0.49, 0.506, 0.004, so effectively a dilemma: strength_mpa against weight_kg, elasticity about -1 (a percent more strength goes with about a percent more weight at the edge of the table). Cost's exponent is 0.004-0.01 (weak; its 'contending' status is the 1e-9 threshold reading the page warns about). Pull-back to raw units: 0.44 on strength, -0.44 on weight, ~0 on stiffness, -0.003 on cost. Stiffness does not contend at all. Association among 22 near-frontier designs: strength-weight -1.00, cost vs strength -0.37, cost vs weight +0.36, stiffness near 0. How sure: moderately for strength/weight (exponents stable across K=1..4, near +0.5 each in every term), low for cost and stiffness (small exponents, 22 near-frontier rows, one temperature, one conditioning). I did not refit under a second scaling, which the conditioning page recommends. The -1.00 association is partly the closure the tensions page describes, so I treat the exponents, not the association, as the evidence.

## 6. Standing question
No. Nothing I read required SysML v2, satellites or a spacecraft model. The home page lists "a cubesat trade study" as one example and the choosing-k page has a cubesat section ("The cubesat ... run from the repository root"), but both are optional and the install-to-answer path used none of it. Only a small friction: choosing-k's sweep helper is shown inside the page, not importable from the package.
