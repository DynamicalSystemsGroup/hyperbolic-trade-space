# U3 return

Header
- model: Sonnet
- persona: U3
- head: 9d83355
- table: ./table.csv
- stage URL: http://127.0.0.1:8791/

## 1. The code (fit.py, as run with `uv run --project hts python fit.py`)

```python
import time, numpy as np, pandas as pd
t0=time.time()
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
df = pd.read_csv("table.csv")
cols = ["strength_mpa","weight_kg","stiffness_gpa","cost_usd"]
print(df[cols].describe().T, df.batch.value_counts().to_dict(), "min", df[cols].min().to_dict())
A = df[cols].to_numpy()
pre = LogAffinePreconditioner(orientation=[1,-1,1,-1])
M = pre.fit_transform(A)
tau = select_temperature(M, 0.10, bounds=(3,1000)); print("tau", tau)
for K in (1,2,3,4):
    ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, round(ts.mean_slack_,3), ts.term_share_.round(2), ts.termination_.status, ts.exponents_.round(2).tolist())
ts1 = HyperbolicTradeSpace(temperature=tau).fit(M)
r = tension_report(ts1, M)
print(r.lemma_name, r.contending_set, r.exponents.round(2), "\n", r.elasticities.round(2), "\n", r.association.round(2), r.association_kind)
print("conditioning", ts1.conditioning_, "n_eff", ts1.n_eff_, ts1.termination_.status)
import matplotlib; matplotlib.use("Agg")
from hyperbolic_trade_space.plotting import plot_tensions
ax = plot_tensions(r, names=["strength","low weight","stiffness","low cost"]); ax.figure.savefig("tensions.png", dpi=80)
# second conditioning
pre2 = LogAffinePreconditioner(orientation=[1,-1,1,-1], scaler="robust")
M2 = pre2.fit_transform(A); tau2=select_temperature(M2,0.10,bounds=(3,1000))
r2 = tension_report(HyperbolicTradeSpace(temperature=tau2).fit(M2), M2); print("robust", tau2, r2.lemma_name, r2.contending_set, r2.exponents.round(2))
print("wall", time.time()-t0)
```

(A second small script, chk.py, only printed the raw log-correlations and drew the strength vs low-weight log plane with `plot_log_plane`; its outputs are quoted below.)

## 2. Pages opened, in order

1. hts/README.md
2. http://127.0.0.1:8791/ (project page; read as text, list of links)
3. http://127.0.0.1:8791/docs/ (Home)
4. /docs/getting-started/
5. /docs/user-guide/overview/
6. /docs/user-guide/conditioning/
7. /docs/user-guide/fitting/
8. /docs/user-guide/choosing-k/
9. /docs/user-guide/tensions/
10. /docs/user-guide/chart/
11. /docs/user-guide/limitations/
12. /docs/user-guide/termination/ (first 70 lines)
13. table.csv (head, describe, counts)
14. The installed package: `import hyperbolic_trade_space; dir(...)` only (no help() needed, no source read).

README's "Home page (docs/index.md)" link was not opened as a file; I used the site instead.

## 3. Errors and where they stopped me

- No error stopped me. `uv sync` ran clean, `import hyperbolic_trade_space` worked first time.
- Minor, mine: system `python3` pandas is old, `df.corr(numeric_only=True)` raised
  `TypeError: corr() got an unexpected keyword argument 'numeric_only'`. I switched to `uv run`. (Not the package's fault; it shows I ran a bare python3 once because the README only shows `uv run pytest`.)
- Noise: every plot run prints `findfont: Failed to find font weight normal for Lucida Grande, now using 500.` on stderr (matplotlib font fallback). Harmless.

## 4. Questions I would ask a colleague (not answered by the pages)

- Is a contending weight of 0.01 on cost a real trilemma member or noise? The report calls it a trilemma [0 1 3] but the weight on cost is 0.01; the docs say small weight is "weaker participation" but give no cutoff for when to ignore it in the name.
- Does the `batch` column (A/B/C) mean I should fit per batch? The package page has no guidance on categorical columns; I dropped it.
- What is the lemma "name" good for when the report's association matrix and exponents tell a different (two-metric) story?
- Is there a default `tau` rule for a conditioned real table besides select_temperature at target 0.10? (I used it; the docs say "start at 0.10".)
- Does the stiffness exponent of 0 mean stiffness never binds, or that it is redundant with others? (Raw log-correlation with strength is 0.49, so neither is clear.)

## 5. Steps to the need

1. README Quickstart: `uv sync` in hts/ (1.75 s wall, wheels cached). README gets to a working import with no gaps. It points to docs/index.md, which I swapped for the site.
2. Site home -> "Open the docs" -> Getting started (first fit on synthetic data, copy-paste worked in spirit).
3. Conditioning page: `LogAffinePreconditioner(orientation=[1,-1,1,-1])`. This is the page that tells an agent what to do with a real CSV. Reached it from the Getting-started "Your own data" link.
4. Fitting page: select_temperature, K=1 fit. Choosing K page for the sweep recipe (copied the idea, not the helpers, because the helpers import `case` from `examples/adcs`, which is not in the installed package; I rewrote a 5-line loop).
5. Tensions page for tension_report and plot_tensions.
6. Looked at the heatmap image and a log-plane plot.
- Went back once: to read the termination page after seeing `not_applicable` as the K=1 status, to learn it is expected at one term.
- Searched nothing outside the pages. Where I wavered: which `K` to pick (see answers) and whether `tension_report` at K>1 would work (not tried beyond K=1, since K=1 was chosen).
- Timing: `uv sync` 1.75 s; first complete script (load, condition, select tau, K=1..4 fits, report, plots, robust refit) 7.9 s wall. Install-to-first-fit (sync + script, excluding my reading time) about 10 s. Total elapsed from sync to finished answer including reading pages: about 150 s plus writing.

## 6. Standing question

No. No page or line sent me to SysML v2, satellites or a spacecraft model. The cubesat appears only as "an example" (Home: "Examples: a cubesat trade study...") and in the Choosing-K page's helper block, which imports `case` from `examples/adcs` ("The cubesat blocks run from the repository root"); that block is not needed for a CSV, but an agent who copies the `sweep` helpers verbatim hits `import case` which is not installed. The project page mentions the paper's "tension report ... near-frontier"; nothing requires a spacecraft.

---

## Answers in plain sentences

Step 2 (conditioning). The four numeric columns are the quantities: strength_mpa (larger is better), weight_kg (smaller is better), stiffness_gpa (larger is better), cost_usd (smaller is better). `sample` is an id and `batch` (A/B/C) is a label; both dropped. All values are strictly positive (minimums 0.42, 4.9, 0.059, 28), so no shift. I used `LogAffinePreconditioner(orientation=[1,-1,1,-1])` with the default standard scaler.

Step 3 (fit). `HyperbolicTradeSpace(temperature=tau).fit(M)` with tau = 178.2 from `select_temperature(M, 0.10, bounds=(3,1000))`, chosen at K=1 as the docs say. K=1 status is `not_applicable` (normal at one term); n_eff is 13.2 of 250, conditioning_ 52.6.

Step 4 (K). I swept K=1..4 at fixed tau and read mean_slack_: 0.578, 0.575, 0.573, 0.572. Drops are 0.003, 0.002, 0.001: no break, and the docs say slack falls with every term by construction. The extra terms are also near-duplicates of the first (exponents roughly [0.5, 0.5, 0, 0] in every term). So I chose K=1, because nothing paid for more, with the caveat that the docs offer no held-out criterion and this is a judgement.

Step 5 (tension). The tension report names a trilemma on strength, low weight and low cost, but the exponents are 0.49, 0.50, 0.00, 0.01. In substance the one real tension is strength versus weight (the heatmap association is -1.00; the elasticity is about -1.0, so a 1 percent rise in strength costs about a 1 percent rise in weight at the edge). Cost enters with a weight of 0.01 and a pulled-back association of only -0.37 with strength, so cost is a marginal member; stiffness has weight 0.00 and does not contend. How I know: exponents at tau=178 and the report's tau=infinity contending set [0 1 3]; a refit with the robust scaler gives the same set with cost weight near 0 (0.48, 0.52, 0, 0), and the two-metric log plane of strength against low weight shows a clean straight edge. How sure: fairly sure about strength versus weight (stable under a second conditioning, seen in the plot); not sure about cost (tiny weight, and the "trilemma" label overstates it); stiffness being absent is a statement about this table as conditioned, with n_eff of only 13, so it is weakly determined. Orientation signs were my assumption from the column names; the docs say a wrong sign is not detected.
