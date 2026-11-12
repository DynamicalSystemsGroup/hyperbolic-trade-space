# Return: U2

```
Header
  model:       Sonnet
  persona:     U2
  head:        9d83355
  table:       ./table.csv
  stage URL:   http://127.0.0.1:8791/
```

## 1. The code (final script, as run: `hts/.venv/bin/python run.py`)

```python
import numpy as np, pandas as pd
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
                                    select_temperature, tension_report)
df = pd.read_csv("table.csv")
cols = ["flow_lps", "head_m", "power_kw", "mass_kg"]
orient = [1, 1, -1, -1]            # flow, head larger-better; power, mass smaller-better
A = df[cols].to_numpy()
pre = LogAffinePreconditioner(orientation=orient)
M = pre.fit_transform(A)
print("round trip", np.allclose(pre.inverse_transform(M), A), "logstd", np.log(M).std(axis=0).round(2))

tau = select_temperature(M, 0.25, bounds=(3, 1000))
print("tau", round(tau, 1))
for K in range(1, 5):
    ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, "slack", round(ts.mean_slack_, 3), "share", ts.term_share_.round(2),
          ts.termination_.status, "frac_above", round(ts.frac_above_, 2))
    print(ts.exponents_.round(2))

K = 1
ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
rep = tension_report(ts, M)
print(rep.lemma_name, rep.contending_set, rep.contending_exponents.round(3))
print("exponents", rep.exponents.round(3))
print("elasticities\n", np.round(rep.elasticities, 2))
print("association\n", np.round(rep.association, 2), rep.association_kind)
print("explained_spread", np.round(rep.explained_spread, 2))
import matplotlib; matplotlib.use("Agg")
from hyperbolic_trade_space.plotting import plot_tensions
ax = plot_tensions(rep, names=cols)
import matplotlib.pyplot as plt
plt.savefig("tensions.png", dpi=100, bbox_inches="tight")

# pull back to attributes (K=1)
from hyperbolic_trade_space import frontier_in_original_units
out = frontier_in_original_units(ts, pre)
print("pullback", out)
e = out[0] if isinstance(out, tuple) else out["exponents_orig"]
e = np.ravel(e); print("exponents on raw (flow, head, power, mass):", e.round(3), "ratio to flow:", (e/e[0]).round(2))
# robustness: other scaler
pre2 = LogAffinePreconditioner(orientation=orient, scaler="robust")
M2 = pre2.fit_transform(A)
tau2 = select_temperature(M2, 0.25, bounds=(3, 1000))
ts2 = HyperbolicTradeSpace(temperature=tau2, random_state=0).fit(M2)
r2 = tension_report(ts2, M2); print("robust:", r2.lemma_name, r2.contending_set, r2.exponents.round(3), round(tau2,1))
from hyperbolic_trade_space.plotting import plot_frontier_coordinates
plt.figure(); ch = ts.transform(M); plot_frontier_coordinates(ch[:, :-1], log_v=ch[:, -1]); plt.savefig("chart.png", dpi=100, bbox_inches="tight")
```

## 2. Pages opened, in order
1. tasks.md (task text)
2. hts/README.md
3. table.csv (head, describe) and model.sysml
4. http://127.0.0.1:8791/ (project page)
5. http://127.0.0.1:8791/docs/
6. /docs/getting-started/
7. /docs/user-guide/conditioning/
8. /docs/user-guide/fitting/
9. /docs/user-guide/choosing-k/
10. /docs/user-guide/tensions/
11. /docs/user-guide/chart/
12. /docs/user-guide/overview/
Also: help() on plotting.plot_frontier_coordinates, grep of hts/src for "sysml|configuration" (no SysML mention in the package). Own tab: tab-83.

## 3. Errors
1. Install: README `uv sync` inside hts/ worked first time; `import hyperbolic_trade_space` works. No stop. (README says "Quickstart" only; no clone/git line needed because I was given the checkout. The docs site's install page says to git clone, which I did not need.)
2. Step 3, `select_temperature(M, 0.10, bounds=(3, 1000))` (the "start at the default 0.10" advice from /fitting/):
```
ValueError: target frac_above 0.1 is not bracketed by bounds (3, 1000): frac_above_ is 0.605 at tau=3 and 0.215 at tau=1000 (frac_above_ is still above the target at the largest tau). Try: raise the target or raise the upper bound; or fit at a fixed temperature (the closest end of bounds is temperature=1000, or select it at n_terms=1 and compare fits with mean_slack_); or widen bounds.
```
   Did next: followed the message, raised the target to 0.25 -> tau = 695.5. The message was enough; the docs say "for real data start at the default 0.10" and my real data did not reach it, so the docs advice failed on the first real table.
3. Step 5, `plot_frontier_coordinates(ts, M)` (guessed the estimator is the first argument, as with plot_log_plane):
```
TypeError: float() argument must be a string or a real number, not 'HyperbolicTradeSpace'
```
   (raised at `Z = np.asarray(Z, dtype=float)`). Fixed with help(): it takes Z and log_v from `ts.transform(M)`. Also stderr noise "findfont: Failed to find font weight normal for Lucida Grande" on every plot (harmless).

## 4. Questions for a colleague
- How do I pick the target fraction above V=1 for real data when 0.10 is not reachable? What does 0.25 mean statistically, and is tau=695 (near the exact maximum, a fit dominated by a few designs) trustworthy?
- Should deterministic model outputs (no noise, a sweep of a model) be treated differently from measurements? The table has a planted exact relation; frac_above stays above 0.2 even at tau=1000.
- Does a heatmap label like "power_kw" mean the raw column or its inverted metric? (It is the inverted metric; the sign of the association then reads opposite to a raw-correlation reading.)
- plot_frontier_coordinates showed no ringed near-frontier points (band default 0.1 against tau 695); what should I read from that chart for a 4-metric fit? It looked like a blob.
- Which of my columns are "attributes"? I decided the three design variables (diameter, speed, width) are configuration, not quantities. The docs say "configuration c" only in the overview/prediction; is there a recipe for including them?

## 5. Steps to the need
1. README -> `uv sync` -> import ok (no trouble).
2. README points to docs Home only; I went Home -> /docs/ -> Getting started (synthetic first fit; fine) -> Conditioning (orientation, scaler; clear).
3. Fitting page for temperature -> got the 0.10 advice -> hit the ValueError -> raised target.
4. Choosing K page: long, helper code uses cubesat blocks that need the repo root (`examples/adcs`, which I do not have in the checkout); I skipped those and wrote my own K sweep. Slight detour.
5. Tensions page -> report -> heatmap; chart page for the plot; one wrong call (error 3). Overview page read last, which I would have wanted first (it says the evaluation step "may be a simulator, a test or an assessment; the package never sees how").
Lost/backtracked: temperature (once), chart function signature (once), the choosing-K helpers I could not run.

## 6. Standing question
No. The pages talk about "cubesat" and "attitude control" only in examples and the home page, set aside as an example; nothing required SysML v2, satellites or a spacecraft model. Closest lines: home "Examples: a cubesat trade study across power, mass and attitude control", and choosing-K "The cubesat blocks run from the repository root, where examples/adcs is" (a code block I could not run without the repo, but not needed).

## Plain-sentence answers

Step 2 (conditioning). Quantities: flow_lps and head_m (larger is better), power_kw and mass_kg (smaller is better). design_id, diameter_m, speed_rpm and width_ratio are identifiers and design variables, not outcomes, so I left them out. All values positive. I used LogAffinePreconditioner(orientation=[1,1,-1,-1]) with the default standard scaler; the round trip is exact and each log-metric has unit spread.

Step 3 (fit). HyperbolicTradeSpace with tau chosen by select_temperature at K=1. The default target 0.10 raised ValueError (above); target 0.25 gave tau = 695.5. Fits ran at K = 1 to 4 and all converged (K>=2 reported "certified").

Step 4 (K). I chose K = 1. I swept K = 1..4 at fixed tau, and mean_slack_ went 0.010, 0.007, 0.005, 0.004: it falls with every added term and shows no break. The thinnest-term share fell (0.83/0.17 at K=2, down to 0.02 at K=4), and the extra terms' exponent vectors are near the first one's (0.28, 0.23, 0.49 vs 0.37, 0.14, 0.41), so extra terms bought almost nothing and became thin. This is the docs' own check; the docs warn that it cannot decide K alone, and there is no held-out criterion.

Step 5 (tensions). Report: trilemma, contending set flow, head, power (exponents 0.28, 0.23, 0.49 on the conditioned metrics); mass has exponent 0 and does not contend. Elasticities say a one percent rise in flow costs roughly 0.84 percent of head or 1.74 percent of power-inverse; ie flow, head and power-efficiency trade against each other. Association of near-frontier log-metrics: flow vs 1/power -0.97, head vs 1/power -0.96, flow vs head +0.85 (aligned); mass has a strong negative association with flow (-0.93, since big pumps are heavy), but it is not in the contending set. Pulling the surface back to raw units gave exponents (flow 0.198, head 0.199, power -0.198, mass 0.000), i.e. flow x head / power is the bound, which matches the pump model's own law (power = flow x head / efficiency). Confidence: the contending set is stable under the other scaler (robust gives the same set and exponents), and the pullback matches the model's physics, so I am fairly sure about the set. I am less sure about the elasticities' exact values: tau of about 700 is near the exact maximum and the table is a deterministic sweep, so a few designs dominate, and the chart (Z0 vs Z1) showed no structure I could read (no ringed near-frontier points at the default band). Not tested: K>1 term reports, resampling.

Step 6 (the model). The model helped, but only as a reader's aid, not as input to the tool. It told me which columns were design variables and which were outputs, their units and directions, and its efficiency/power calc let me check the answer: the fitted pullback exactly matches flow x head / power. The package has no connection to SysML v2: grep of the source shows no mention, and the docs say the package "never sees how" attributes are produced. I could connect my model only by the table export (the CSV I was given): model -> evaluated designs -> table -> pandas -> conditioning -> fit. Nothing in the docs shows how to go from a SysML v2 model to the table (not needed here, the export was supplied) or says which model elements (calc outputs vs. parameters) should become attribute columns, so I decided that myself.
