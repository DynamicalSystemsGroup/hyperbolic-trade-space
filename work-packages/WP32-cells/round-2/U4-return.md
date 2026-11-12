# U4 return (round 2)

Header
- model: Sonnet
- persona: U4
- head: a3a61af
- table: ./table.csv
- model source: ./model.sysml

## 1. The code (final script, ./analysis.py, run with `uv run --project hts python analysis.py` from this directory)

```python
import numpy as np, pandas as pd
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
df = pd.read_csv("table.csv")
names = ["flow_lps", "head_m", "power_kw", "mass_kg"]
orient = [1, 1, -1, -1]
A = df[names].to_numpy()
assert (A > 0).all()
pre = LogAffinePreconditioner(orientation=orient)
M = pre.fit_transform(A)
print("log std", np.log(M).std(axis=0).round(3))
tau = select_temperature(M, 0.10, bounds=(3, 1e4))
print("tau", round(tau, 1))
for K in range(1, 5):
    ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, round(ts.mean_slack_, 3), ts.term_share_.round(2), ts.termination_.status, ts.exponents_.round(2).tolist())
ts = HyperbolicTradeSpace(temperature=tau).fit(M)
r = tension_report(ts, M, band=0.00021)
print(r.contending_set, r.lemma_name, r.contending_exponents.round(3))
print(r.exponents.round(3)); print(r.elasticities.round(2)); print(r.association.round(2)); print(r.n_near_frontier)
# second conditioning for robustness
M2 = LogAffinePreconditioner(orientation=orient, scaler="robust").fit_transform(A)
ts2 = HyperbolicTradeSpace(temperature=tau).fit(M2)
r2 = tension_report(ts2, M2, band=0.00021); print("robust", r2.lemma_name, r2.exponents.round(3))
from hyperbolic_trade_space import frontier_in_original_units
print(frontier_in_original_units(ts, pre))
import matplotlib; matplotlib.use("Agg")
from hyperbolic_trade_space.plotting import plot_tensions
ax = plot_tensions(r, names=names); ax.figure.savefig("tensions.png")
```

Output of the final run (font warnings omitted):

```
log std [1. 1. 1. 1.]
tau 6023.1
1 0.013 [1.] not_applicable [[0.28, 0.23, 0.49, 0.0]]
2 0.01 [0.89 0.11] certified [[0.28, 0.23, 0.49, 0.0], [0.37, 0.14, 0.41, 0.07]]
3 0.008 [0.86 0.14 0.  ] certified [[0.28, 0.23, 0.49, 0.0], [0.37, 0.14, 0.41, 0.07], [0.26, 0.25, 0.48, 0.0]]
4 0.007 [1. 0. 0. 0.] certified [...]
[0 1 2] trilemma [0.28  0.234 0.487]
elasticities (rows j, cols k; order flow, head, power-metric, mass-metric):
[[-1.   -0.84 -1.74 -0.  ]
 [-1.2  -1.   -2.08 -0.  ]
 [-0.57 -0.48 -1.   -0.  ]
 [ nan   nan   nan   nan]]
association:
[[ 1.    0.77 -0.96 -0.94]
 [ 0.77  1.   -0.92 -0.54]
 [-0.96 -0.92  1.    0.82]
 [-0.94 -0.54  0.82  1.  ]]
n_near_frontier 10
robust-scaler refit: trilemma [0.281 0.23 0.489 0.]
pulled back: exponents_orig [0.198, 0.198, -0.198, -0] (flow, head, power, mass)
```

## 2. Pages opened, in order

1. ./model.sysml
2. ./table.csv (head, describe, corr via pandas)
3. hts/README.md
4. http://127.0.0.1:8791/docs/ (home)
5. http://127.0.0.1:8791/docs/getting-started/
6. http://127.0.0.1:8791/docs/guide/ (guessed address: 404, "Error code: 404 Message: File not found.")
7. http://127.0.0.1:8791/docs/user-guide/overview/
8. .../user-guide/conditioning/
9. .../user-guide/fitting/
10. .../user-guide/choosing-k/
11. .../user-guide/tensions/
12. .../user-guide/chart/
13. hts/src/hyperbolic_trade_space/tuning.py and tensions.py appear only in my traceback paths; I did not open them. Pages fetched with curl and stripped to text (no browser tab).

## 3. Errors

a. `FileNotFoundError: [Errno 2] No such file or directory: 'table.csv'`: my own mistake, ran the script from inside hts/. Reran from the cell directory with `uv run --project hts`.
b. `ValueError: target frac_above 0.1 is not bracketed by bounds (3, 1000): frac_above_ is 0.605 at tau=3 and 0.215 at tau=1000 (frac_above_ is still above the target at the largest tau). Try: raise the target or raise the upper bound; or fit at a fixed temperature (the closest end of bounds is temperature=1000, or select it at n_terms=1 and compare fits with mean_slack_); or widen bounds.` Doing: select_temperature(M, 0.10, bounds=(3, 1000)), the call copied from the fitting page. The same page says "for real data start at the default 0.10 ... a model sweep needed bounds=(3, 1e4)", so I raised the upper bound to 1e4 and got tau = 6023.1 (with bounds up to 1e6 the same target gives 8490, so the selected tau depends on the bounds: I did not resolve why).
c. `ValueError: only 6 near-frontier rows (|log V| < 0.000166027) but min_near_frontier = 10; use a larger band, band=0.00021 (the smallest round band with 10 rows on this term), or fit at temperature=4.76e+03 (the band is 1/temperature), or lower min_near_frontier` from tension_report(ts, M). I passed band=0.00021 as the message said; it worked.
d. Plot only: "findfont: Failed to find font weight normal for Lucida Grande, now using 500." (stderr, harmless).
Install (step 1): README `git clone ...; uv sync` is satisfied by the given checkout; `uv sync` ran and `import hyperbolic_trade_space` worked. No stop.

## 4. Questions for a colleague

- Is the table noise-free (a deterministic export)? tau ~ 6000 and a band of 2e-4 in log V suggest the frontier is nearly exact; I could not tell whether that is expected or whether a lower temperature is wiser.
- Why does select_temperature give 6023 with bounds up to 1e4 and 8490 with bounds up to 1e6 for the same target?
- Is a tension band of 0.00021 (10 rows) enough evidence for the association numbers? The tensions page gives no guidance on how few near-frontier rows is too few.
- Should design variables (diameter, speed, width) be used at all? The pages say they are "configuration, not attributes" and point to plot_v_by_variable and prediction; I did not use them.
- Does the package read the .sysml file? I assumed no (the overview says a table "is one source").

## 5. Steps to the need

README (quickstart snippet, uv sync) -> docs home -> getting-started (first fit; saw "Your own data" pointer) -> overview (pipeline: "a SysML v2 model's exported table is one source", "Design variables and labels are configuration, not attributes") -> conditioning (orientation, scaler) -> fitting (select_temperature) -> hit error b -> choosing-k (helper sweep pattern, mean_slack_) -> tensions (report reading) -> hit error c -> fixed with the band in the message -> chart page (plot list). Lost/went back: guessed /docs/guide/ (404); had to read the model source to decide orientation (flow, head larger-is-better; power, mass smaller-is-better; diameter, speed, width excluded as configuration). I did not look at plot_frontier_coordinates (chart of 4 metrics needs d-1=3 coords); I only drew plot_tensions.

## Answers in plain sentences

Step 2 (conditioning): quantities are flow_lps and head_m (larger is better) and power_kw and mass_kg (smaller is better); diameter_m, speed_rpm, width_ratio and design_id are configuration and left out. Everything is positive. LogAffinePreconditioner(orientation=[1,1,-1,-1]) with the default standard scaler gave unit log-spread in every column.

Step 3 (fit): HyperbolicTradeSpace(temperature=tau) with tau = select_temperature(M, 0.10, bounds=(3, 1e4)) = 6023, one term.

Step 4 (K): I fit K=1 to 4 at that tau. Mean slack goes 0.013, 0.010, 0.008, 0.007: no break, a gentle bend; at K=2 and 3 the added term holds 11 to 14 percent of near-frontier rows, and at K=3 the third term holds 0 and at K=4 the extra terms hold 0. Every K>=2 is certified, which the page says does not show K is right. I chose K=1 because slack shows no break, extra terms are thin or empty, and the extra terms' exponents stay close to the first (flow .26 to .38, head .12 to .26, power .39 to .50, mass 0 to .11). Confidence in K=1 is moderate; I did no resampling.

Step 5 (tension): The report names a trilemma among flow, head and power, with weights 0.28, 0.23 and 0.49. Mass has weight 0 and does not contend. Pulled back to attributes, the surface is flow^0.198 * head^0.198 / power^0.198 (a constant): flow times head over power is capped. Reading: more flow and more head cost power (a cap on hydraulic power per shaft power, which is what an efficiency ceiling looks like); elasticity of flow with respect to power-metric about -0.57 to -1.74 depending on direction. Mass association with flow is -0.94 but its weight is zero, so I read it as a correlation among near-frontier rows, not a binding trade. Evidence: the exponents, the association heatmap (flow vs power-metric -0.96, head vs power-metric -0.92), and the same trilemma under the robust scaler. Sureness: the exponents are stable across scalers and K; the association rests on only 10 near-frontier rows at band 0.00021, so I hold it loosely, and the table is one sample of the design ranges.

Step 6 (model side): The model source helped me decide orientation (the calc names Flow, Head, ShaftPower, Mass; ShaftPower = hydraulic power over Efficiency, which explains why flow and head trade with power) and what is configuration versus attribute (the three `in` variables are configuration, the four `return` values are attributes). It did not get in the way. I could not connect the model to the tool directly: no page showed how to hand a .sysml or an export to the package; the route is the exported table only, which I loaded with pandas. Orientation and which columns are quantities I had to decide myself from the source; nothing in the package reads the model. A programmatic route from model attributes to orientation (e.g. a smaller-is-better flag in the export) would be the missing piece.

## 6. Standing question

No. Nothing required SysML v2, satellites or a spacecraft model. Mentions seen: overview "a SysML v2 model's exported table is one source" (one option, not a requirement); the examples are cubesat-based (home: "a cubesat trade study across power, mass and attitude control") and the choosing-k page's cubesat blocks "run from the repository root", which I skipped without loss.
