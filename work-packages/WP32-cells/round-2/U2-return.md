# U2 return (round 2)

```
Header
  model:       Sonnet
  persona:     U2
  head:        a3a61af
  table:       ./table.csv
  model source: ./model.sysml (opened and read; U2 has it)
  stage:       http://127.0.0.1:8791/ (own tab tab-86)
```

## 1. The code (final script as run, analysis.py; robust.py was a second check, quoted below it)

```python
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
                                    select_temperature, tension_report)
from hyperbolic_trade_space.plotting import plot_tensions, plot_log_plane

df = pd.read_csv("table.csv")
cols = ["flow_lps", "head_m", "power_kw", "mass_kg"]
orient = [1, 1, -1, -1]          # flow, head larger-better; power, mass smaller-better
A = df[cols].to_numpy()
pre = LogAffinePreconditioner(orientation=orient)
M = pre.fit_transform(A)
print("M min", M.min(), "log std", np.log(M).std(axis=0).round(3))

tau = select_temperature(M, 0.10, bounds=(3, 1e4))
print("tau", round(tau, 1))

slack = []
for K in range(1, 5):
    f = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(f"K={K} slack={f.mean_slack_:.3f} thinnest={f.term_share_.min():.2f} "
          f"{f.termination_.status} radius={f.termination_.radius:.0e} frac_above={f.frac_above_:.2f}")
    slack.append(f.mean_slack_)
print("drops", (-np.diff(slack)).round(3))

ts = HyperbolicTradeSpace(temperature=tau).fit(M)
r = tension_report(ts, M, band=2.1e-4)
print(r.lemma_name, r.contending_set, r.contending_exponents.round(3))
print("exponents", dict(zip(cols, ts.exponents_[0].round(3))))
print("elasticities\n", r.elasticities.round(2))
print("association\n", np.round(r.association, 2))
print("n_near", r.n_near_frontier, "conditioning_", ts.conditioning_, ts.termination_)
plot_tensions(r, names=cols); plt.savefig("tensions.png", bbox_inches="tight"); plt.close()
plot_log_plane(HyperbolicTradeSpace(temperature=tau).fit(M[:, :3:2]), M[:, :3:2]); plt.savefig("plane.png"); plt.close()

# configuration -> predicted position (the model's design variables are the table's first columns)
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from hyperbolic_trade_space import TradeSpaceRegressor
C = df[["diameter_m", "speed_rpm", "width_ratio"]].to_numpy()
reg = TradeSpaceRegressor(RandomForestRegressor(n_estimators=50, random_state=0),
                          HyperbolicTradeSpace(temperature=tau)).fit(C, M)
print("R2 coords (train)", round(reg.score(C, M), 3))
print("pred novelty first 3", reg.predict_novelty(C[:3]).round(3))
```

robust.py (second conditioning check, run separately):
```python
import numpy as np, pandas as pd
from hyperbolic_trade_space import *
df=pd.read_csv("table.csv");cols=["flow_lps","head_m","power_kw","mass_kg"]
A=df[cols].to_numpy()
for sc in ("standard","robust",None):
    pre=LogAffinePreconditioner(orientation=[1,1,-1,-1],scaler=sc);M=pre.fit_transform(A)
    ts=HyperbolicTradeSpace(temperature=np.inf).fit(M)
    r=tension_report(ts,M)
    print(sc,r.lemma_name,r.contending_set,r.contending_exponents.round(3))
    o=frontier_in_original_units(ts,pre);print("  orig exps",{k:np.round(v,3) for k,v in o.items()})
# bootstrap
rng=np.random.default_rng(0);pre=LogAffinePreconditioner(orientation=[1,1,-1,-1]);M=pre.fit_transform(A)
for i in range(5):
    Mi=M[rng.choice(len(M),len(M))];print(HyperbolicTradeSpace(temperature=np.inf).fit(Mi).exponents_[0].round(3))
```

## 2. Pages opened, in order

1. ./hts/README.md
2. ./table.csv (pandas describe/corr) and ./model.sysml (read)
3. http://127.0.0.1:8791/docs/
4. /docs/getting-started/
5. /docs/user-guide/overview/
6. /docs/user-guide/conditioning/
7. /docs/user-guide/fitting/
8. /docs/user-guide/choosing-k/
9. /docs/user-guide/tensions/
10. /docs/user-guide/chart/
11. /docs/user-guide/prediction/
12. /docs/api/, /docs/api-reference/, /docs/examples/, /docs/theory/, /docs/user-guide/limitations/ (rendered and read), /docs/user-guide/termination/, /docs/further-reading/, /docs/generated/glossary/: fetched in my tab by script and searched for "SysML|export|model source" only (zero hits in all eight); not read as text except limitations (page 12, read in full).
13. hts/src/hyperbolic_trade_space/*.py: grep for "sysml|export" only (zero hits); traceback source lines shown in errors.
14. Home page link list (hrefs) read once.

## 3. Errors

E1. Step 3, select_temperature(M, 0.10, bounds=(3, 1000)) (the docs' recipe, default target 0.10):
```
ValueError: target frac_above 0.1 is not bracketed by bounds (3, 1000): frac_above_ is 0.605 at tau=3 and 0.215 at tau=1000 (frac_above_ is still above the target at the largest tau). Try: raise the target or raise the upper bound; or fit at a fixed temperature (the closest end of bounds is temperature=1000, or select it at n_terms=1 and compare fits with mean_slack_); or widen bounds.
```
Did next: the fitting page says "a model sweep needed bounds=(3, 1e4)"; used that, got tau = 6023.1 (frac_above_ 0.10).

E2. Step 5, tension_report(ts, M) at tau 6023.1:
```
ValueError: only 6 near-frontier rows (|log V| < 0.000166027) but min_near_frontier = 10; use a larger band, band=0.00021 (the smallest round band with 10 rows on this term), or fit at temperature=4.76e+03 (the band is 1/temperature), or lower min_near_frontier
```
Did next: passed band=2.1e-4 as the message said. Worked.

E3 (my own mistake, not the package's): np.round on the dict returned by frontier_in_original_units: "TypeError: unsupported operand type(s) for *: 'dict' and 'float'". Fixed by reading the dict keys. The conditioning page names the return fields (exponents_orig, log_const, shift) but not that it is a dict.

Noise: matplotlib prints "findfont: Failed to find font weight normal for Lucida Grande, now using 500." on each plot (harmless, stderr).

Install: `uv sync` inside the checkout worked; import hyperbolic_trade_space worked. The README's `git clone` line was not needed (already in the checkout). The README snippet itself I did not run.

## 4. Questions for a colleague

- Is a table with no noise at all (it is a deterministic model's export) a fair input? The limitations page says designed samples carry no sampling error; the temperature recipe and the band minimum (10 rows) both struggled with it (E1, E2). Is a tiny band like 2e-4 meaningful, or is the thin band just the deterministic model's tightness?
- Why does tau=1000 give frac_above 0.215 but tau=1e4 give 0.09 (my own run)? Is that a feature of noise-free tables?
- scaler=None gives a monolemma on mass; standard and robust give a trilemma without mass. The conditioning page says a scaler is a choice, but not which to trust when they disagree. I took "standard" because the guide's examples use it.
- My model has a Flow/Head/Efficiency/ShaftPower/Mass chain; does the package have any way to take the model's own structure (which attribute is computed from which)? Nothing in the pages says.
- No page says how to get the table out of SysML v2 or which tool exports it; the overview only says "a SysML v2 model's exported table is one source".
- Does the README pip/uv path ever become a published install (the docs say "from source for now")?

## 5. Steps to the need

README -> uv sync -> import OK (1 step, no snag). Docs home -> getting-started (ran no code, read) -> overview -> conditioning (found orientation and standard scaler, decided orientation flow +, head +, power -, mass -) -> fitting (temperature recipe) -> choosing-k -> tensions -> chart -> prediction -> limitations. Went back to fitting page once for the "bounds=(3, 1e4)" hint after E1; went back to the tensions page for band/min_near_frontier after E2. Searched (script grep) for SysML across eight pages: nothing. Did not get lost.
Time from README to a tension answer: one script, three fixes (E1, E2 plus nothing else).

## Plain-sentence answers

Step 2 (conditioning): the model has three design variables (diameter, speed, width ratio; columns 2 to 4) and four outcomes. I treated flow_lps and head_m as larger-is-better and power_kw and mass_kg as smaller-is-better (orientation [1, 1, -1, -1]), no shift (all positive), standard scaler. design_id is a row label, dropped (it has a 0 and is not a quantity). Result: log-std 1 on every column, min metric 0.106.

Step 3 (fit): HyperbolicTradeSpace at tau = 6023 (select_temperature with bounds up to 1e4), K=1 exponents flow 0.28, head 0.234, power 0.487, mass 0.00.

Step 4 (K): I chose K = 1. The mean slack is 0.013, 0.010, 0.008, 0.007 for K = 1 to 4, drops 0.003, 0.001, 0.001: no break, and the slack is already small at one term; at K = 2 the thinnest term holds 0.11 of the near-frontier rows (against 0.5 expected if equal) and at K = 3 and 4 0.00, so extra terms are empty or thin; the certified radius is tiny (1e-5). The docs say no check decides K alone; this is "no sign that more terms pay", not proof.

Step 5 (reading): a trilemma on flow, head and power (mass has weight 0.00). The three trade: more flow and more head cost more power. In the original units the surface is flow^0.198 * head^0.198 * power^-0.198 = const, i.e. flow x head / power is capped; that matches the model file, where shaft power = 9.81 x flow x head / efficiency and efficiency is at most 0.82, so the tension is the efficiency ceiling. Mass does not bind in this table. How sure: the finding is stable under the other scaler (0.281, 0.230, 0.489) and under five bootstrap resamples at tau = inf (identical to 3 decimals), but it is conditioning-dependent (scaler=None gives a monolemma on mass), it rests on 10 near-frontier rows in a very thin band (2e-4), the table is noise-free, and the association numbers (flow-power -0.96, head-power -0.92) are partly a closure effect per the tensions page. I would say fairly sure of flow-head-power, which I could check by hand from the model; sure that mass is not on that frontier under the standard scaling only. The charts I looked at: the tension heatmap (plot_tensions) and the flow-vs-power log plane (frontier line above all points, grey band too thin to see at 1.7e-4).

Step 6 (the model): the model did not help or get in the way of using the tool; it was only the source of the table. The table's column names carry units (flow_lps, head_m) which is where I got orientation from; the model's comments told me nothing the table didn't, except that I could check the answer by hand afterwards (efficiency ceiling), which was useful for trusting the report. I could not connect my model to the tool in any way the pages describe: the package takes arrays; nothing in the docs or the source names SysML v2, an exporter or any model-side hook. What I could do by hand: the first three columns (diameter, speed, width ratio) are my configuration, so I fitted TradeSpaceRegressor(RandomForestRegressor, HyperbolicTradeSpace) from configuration to conditioned metrics (R2 in coordinate space 0.972 on train, predict_novelty returns small negatives), which stays on the table side; the model's calc definitions I could use as the evaluator for new proposed configurations, but that is my glue code, not a package feature.

## 6. Standing question

No. Nothing required SysML v2, satellites or a spacecraft model. The only SysML mention I saw is in the overview ("any table works, and a SysML v2 model's exported table is one source"), which says it is optional. The examples page (cubesat) I did not open as a requirement, and the getting-started page uses synthetic data. Satellite wording appears (ADCS case study, "the cubesat blocks run from the repository root" in choosing-k) but I did not need them; the choosing-k page's helper code partly imports `case` from "examples/adcs", which is only for the cubesat blocks.
