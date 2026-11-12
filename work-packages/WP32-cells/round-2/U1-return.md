# U1 cell return

Header
- model: Sonnet
- persona: U1
- head: a3a61af
- table: ./table.csv
- stage URL: http://127.0.0.1:8791/ ; round 2

## 1. The code (analysis.py, as run)

```python
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
                                    select_temperature, tension_report)
from hyperbolic_trade_space.plotting import plot_tensions, plot_log_plane

df = pd.read_csv("table.csv")
print(df.describe().T[["min", "max"]])
print(df.isna().sum().sum(), "NaNs;", (df.select_dtypes("number") <= 0).sum().to_dict())
cols = ["strength_mpa", "weight_kg", "stiffness_gpa", "cost_usd"]
orient = [1, -1, 1, -1]          # weight and cost: smaller is better
A = df[cols].to_numpy()
pre = LogAffinePreconditioner(orientation=orient)
M = pre.fit_transform(A)
print("log std", np.log(M).std(axis=0).round(2))

tau = select_temperature(M, 0.10, bounds=(3, 1000))
print("tau", round(tau, 1))
for K in (1, 2, 3, 4):
    f = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, "slack", round(f.mean_slack_, 3), "thin", f.term_share_.min().round(2), f.termination_.status)

ts = HyperbolicTradeSpace(temperature=tau).fit(M)
r = tension_report(ts, M)
print(r.lemma_name, r.contending_set, r.contending_exponents.round(3))
print(pd.DataFrame(r.elasticities.round(2), index=cols, columns=cols))
print(pd.DataFrame(r.association.round(2), index=cols, columns=cols))
plot_tensions(r, names=cols); plt.savefig("tensions.png", bbox_inches="tight"); plt.close()

# chart: strength vs 1/weight plane, and the transform chart
M2 = M[:, :2]
ts2 = HyperbolicTradeSpace(temperature=tau).fit(M2)
ax = plot_log_plane(ts2, M2, band=1/tau)
ax.set_xlabel("log strength (metric 0)"); ax.set_ylabel("log 1/weight (metric 1)")
plt.savefig("logplane.png", bbox_inches="tight"); plt.close()
print("frac_above", round(ts.frac_above_, 2), "n_eff", round(ts.n_eff_, 1), "conditioning", ts.conditioning_)
# sensitivity: robust scaler, and by batch
for sc in ("robust",):
    M_r = LogAffinePreconditioner(orientation=orient, scaler=sc).fit_transform(A)
    t_r = select_temperature(M_r, 0.10, bounds=(3, 1000))
    r_r = tension_report(HyperbolicTradeSpace(temperature=t_r).fit(M_r), M_r)
    print(sc, round(t_r,1), r_r.lemma_name, r_r.contending_set, r_r.contending_exponents.round(3))
for b, g in df.groupby("batch"):
    Mb = LogAffinePreconditioner(orientation=orient).fit_transform(g[cols].to_numpy())
    tb = select_temperature(Mb, 0.10, bounds=(3, 1000))
    try:
        rb = tension_report(HyperbolicTradeSpace(temperature=tb).fit(Mb), Mb)
        print("batch", b, len(g), round(tb,1), rb.contending_set, rb.contending_exponents.round(3))
    except ValueError as e:
        print("batch", b, len(g), "ERROR", e)
```

Run with `uv run --project hts python analysis.py` (matplotlib Agg; prints a harmless "findfont ... Lucida Grande" line repeatedly).

## 2. Pages opened, in order

1. hts/README.md
2. http://127.0.0.1:8791/docs/ (home, in my own tab; nav link list read from it)
3. /docs/getting-started/
4. /docs/user-guide/conditioning/
5. /docs/user-guide/fitting/
6. /docs/user-guide/choosing-k/
7. /docs/user-guide/tensions/
8. /docs/user-guide/chart/

Pages 3-8 were fetched as HTML from inside my tab and read as text, not navigated visually. Not opened: overview, prediction, termination, limitations, API, API reference, examples, theory, glossary, further reading. hts/src/hyperbolic_trade_space/tensions.py appeared in a traceback only.

## 3. Errors

- Batch B and C subset checks (my own robustness check, 79 and 86 rows, tension_report):
  `ValueError: only 5 near-frontier rows (|log V| < 0.00323591) but min_near_frontier = 10; use a larger band, band=0.0097 (the smallest round band with 10 rows on this term), or fit at temperature=103 (the band is 1/temperature), or lower min_near_frontier`
  and for C: `only 8 near-frontier rows (|log V| < 0.00512342) but min_near_frontier = 10; ... band=0.0069 ... temperature=145 ...`. I caught it in the script and moved on; the message was clear. Batch A (85 rows) worked.
- Install: no error. README says git clone then uv sync; I was given the checkout, so I ran only `uv sync` in hts/ (1.3 s, warm cache). `import hyperbolic_trade_space` worked first time. I did not run the README snippet verbatim.
- Install to first fit: about 100 s wall (uv sync 1.3 s; the rest was reading pages and writing the script). Install to finished script with all checks: 171 s.

## 4. What I would ask a colleague

- The report says "trilemma" because cost has exponent 0.004. The docs say read contending_exponents before the name, but what exponent makes a metric a real member of the set? The participation threshold is 1e-3 and 0.004 passes it.
- What do the grey "w=0.00" (stiffness) versus "w=0.01" (cost) mean in the heatmap labels? The caption does not say.
- Is 250 rows enough? n_eff_ is 13.2; the pages do not say when n_eff_ is too small.
- What does conditioning_ = 52.6 tell me? The pages send me to the Termination page, which I did not open.
- What should I do with a categorical column (batch)? The pages are silent; I only used it as a subset check.
- The tail of cost spans 28 to 500,000; is the log-standard scaler the right call there, or robust? (I tried both; the answer did not move.)

## 5. Steps to the need

README -> uv sync -> docs home -> getting-started (first fit, API) -> conditioning (orientation, scaling) -> fitting (temperature recipe) -> choosing-k -> tensions -> chart. Conditioned with LogAffinePreconditioner(orientation=[1,-1,1,-1]) after checking ranges. select_temperature(M, 0.10, bounds=(3,1000)) gave tau 178. K sweep 1..4, tension_report, plot_tensions, plot_log_plane on the two traded metrics. Went back once, to the tensions page, to understand a "trilemma" with one near-zero exponent. No searching outside the pages. Friction: nothing told me to drop `sample` (index) and `batch` (label); I inferred it. choosing-k mixes in cubesat blocks that need the repo root (flagged on the page; I skipped them). The log-plane plot needed me to pick the two metrics myself, from the heatmap.

## 6. Standing question

No. Nothing made me think I needed SysML v2, satellites or a spacecraft model. Satellite words I met: the home page lists "Examples: a cubesat trade study across power, mass and attitude control"; choosing-k has a section "The cubesat" and says "the case study's cubesat blocks run from the repository root". Those read as optional examples I could skip.

## Plain-sentence answers to steps 2 to 5

2. Quantities: strength_mpa and stiffness_gpa (larger is better); weight_kg and cost_usd (smaller is better, orientation -1). `sample` is an index and `batch` a label, so both dropped. All values positive, no zeros, so shift 0; default standard scaler on the log gives each metric log-std 1 (checked).
3. Fitted HyperbolicTradeSpace at tau 178.2 (select_temperature, target 0.10). frac_above_ 0.09, n_eff_ 13.2.
4. K = 1. I swept K = 1..4 at that tau: mean_slack_ 0.578, 0.575, 0.573, 0.572, so a drop of 0.003 or less per added term and no break, while the thinnest term shrinks (0.24, 0.17, 0.13). More terms buy nothing visible on this table. The docs say no check decides K alone, so this is a judgement.
5. Strength and weight trade against each other almost one for one: exponents 0.49 and 0.51 (weight inverted), elasticity about -1, near-frontier association -1.00, and the log-plane picture shows the designs under one straight line. Cost has exponent 0.004; the report counts it and names a trilemma, but I read it as a weak third member (association with strength -0.37, no weight in the fit). Stiffness is not involved (exponent about 0). Sure about strength versus weight: it held with the robust scaler (tau 204) and on batch A alone. Unsure about cost: batches B and C raised the near-frontier-count error, so I could not check it there. Orientation of weight and cost was my judgement, as the conditioning page says.
