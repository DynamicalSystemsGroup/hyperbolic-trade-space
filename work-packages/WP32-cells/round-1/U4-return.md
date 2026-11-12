import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
from hyperbolic_trade_space.plotting import plot_tensions

df = pd.read_csv("table.csv")
cols = ["flow_lps", "head_m", "power_kw", "mass_kg"]
orient = [1, 1, -1, -1]          # flow, head larger-better; power, mass smaller-better
A = df[cols].to_numpy()
print("min", A.min(0))
pre = LogAffinePreconditioner(orientation=orient)
M = pre.fit_transform(A)

tau = select_temperature(M, 0.25, bounds=(3, 1000))
print("tau", tau)
for K in range(1, 6):
    ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, round(ts.mean_slack_, 3), ts.term_share_.round(2), ts.termination_.status)

K1 = HyperbolicTradeSpace(temperature=tau).fit(M)
print("K=1 exponents", K1.exponents_.round(2))
r = tension_report(K1, M)
print(r.lemma_name, r.contending_set, r.exponents.round(2))
print("elasticities\n", r.elasticities.round(2))
print("association\n", np.round(r.association, 2))
print("directions", np.round(r.tension_loadings, 2), r.explained_spread)
ax = plot_tensions(r, names=cols)
ax.figure.savefig("tensions.png", dpi=100, bbox_inches="tight")

# robustness: other scaler
M2 = LogAffinePreconditioner(orientation=orient, scaler="robust").fit_transform(A)
t2 = select_temperature(M2, 0.25, bounds=(3, 1000))
r2 = tension_report(HyperbolicTradeSpace(temperature=t2).fit(M2), M2)
print("robust:", t2, r2.lemma_name, r2.contending_set, r2.exponents.round(2))
```

## 2. Pages opened, in order
1. hts/README.md
2. ./model.sysml
3. ./table.csv (head, shape, describe)
4. http://127.0.0.1:8791/ (project page, via curl, text and link list)
5. http://127.0.0.1:8791/docs/ (docs home)
6. http://127.0.0.1:8791/docs/getting-started/
7. http://127.0.0.1:8791/docs/user-guide/conditioning/
8. http://127.0.0.1:8791/docs/user-guide/fitting/
9. http://127.0.0.1:8791/docs/user-guide/choosing-k/
10. http://127.0.0.1:8791/docs/user-guide/tensions/
11. http://127.0.0.1:8791/docs/user-guide/chart/
12. Installed package: import only (dir of the module); no source read, no help() call.
Not opened: paper, API reference, examples, theory, limitations, termination, glossary.

## 3. Errors and where they stopped me
1. Ran `uv sync` in the cell directory instead of hts/ (my slip; README does not say to cd into the checkout):
   `error: No `pyproject.toml` found in current directory or any parent directory`
   Went into hts/ and re-ran `uv sync`: worked; `import hyperbolic_trade_space` works. README gets to a working import, with the cd implied.
2. `select_temperature(M, 0.10, bounds=(3, 1000))` (the default target the docs say to start at for real data):
   `ValueError: target frac_above 0.1 is not bracketed by bounds (3, 1000): frac_above_ is 0.605 at tau=3 and 0.215 at tau=1000 (frac_above_ is still above the target at the largest tau). Try: raise the target or raise the upper bound; or fit at a fixed temperature (the closest end of bounds is temperature=1000, or select it at n_terms=1 and compare fits with mean_slack_); or widen bounds.`
   I used target 0.25 (above 0.215), as the message suggested; got tau = 695.5.
3. `sed -i` on my own file failed on stdin (my shell slip, not the package). Used python to edit.
4. Harmless stderr: matplotlib `findfont: Failed to find font weight normal for Lucida Grande, now using 500.`

## 4. Questions for a colleague
- Is it right to take a target of 0.25 above V=1 for this table? The docs say start at 0.10; the data would not reach it. Here flow, head and power are tied by physics, so the table is not "a frontier with scatter below".
- Does mass_kg getting exponent 0 mean "not binding" or "mis-oriented"? (Docs say wrong orientation is not detected; I judged smaller-is-better is right for mass.)
- Should the three design variables (diameter, speed, width) be left out? I left them out as configurations, not metrics; docs for this package say attributes are what is conditioned, and I took that to exclude configuration columns, but nothing says so directly.
- Efficiency is computed in the model but not exported; would it be a useful fifth quantity? (Not answerable from the pages.)
- Does the model's note "illustrative constants" matter to what a trade-off finding means?

## 5. Steps to the need
README (install, tests) -> docs home -> getting started (first fit; worked) -> conditioning (orientation, preconditioner) -> fitting (temperature) -> hit error 2 -> choosing K (sweep recipe, adapted without the cubesat helper, which needs the repo root I do not have) -> tensions (report, heatmap). Went back once: to the Fitting page for the tau advice after the error. Searched: nothing (curl link lists). Got lost: the cd into hts/ (README silent), and the K=1 temperature when 0.10 failed (the error text carried the answer). The chart page was read but I produced the tension heatmap only (plot_tensions), not log-plane plots; four metrics have no 2-D plane.

## 6. Standing question
No. The docs say nothing that requires SysML v2, satellites or a spacecraft model. The pages that mention satellites are the cubesat example and its helpers in "Choosing K" (`import case` from `examples/adcs`, "run from the repository root"), which I could not run and did not need. The README's Layout list mentions "ADCS trade-study case" only as a directory.

## Answers in plain sentences

Step 2 (conditioning). I read model.sysml: three inputs (diameter, speed, width ratio) are design choices; the four outputs are flow, head, shaft power, mass. I took the outputs as quantities and the inputs as configuration. Flow and head: larger is better. Power and mass: smaller is better. LogAffinePreconditioner(orientation=[1,1,-1,-1]) turned them into positive larger-is-better metrics. All values were positive, so no shift. Efficiency, used inside the model, is not in the table.

Step 3 (fit). The default one-term fit at tau=695.5. Exponents: flow 0.28, head 0.23, power 0.49, mass 0.00.

Step 4 (K). By the mean-slack sweep at fixed tau: K=1 0.010, K=2 0.007, K=3 0.005, K=4 0.004, K=5 0.003. All K>=2 certified. There is no break: the drop from K=1 is already only 0.003 and falls smoothly after; K=1 slack is small to begin with. So I stayed at K=1 (the simplest that fits within about 0.01 of the frontier). Not a strong test; the docs state no criterion decides K. Not run: the thinnest-term, resampling and planted checks beyond reading the term shares (K=2 thinnest share 0.17).

Step 5 (tensions). The report names a trilemma of flow, head and power (as inverted, i.e. low power); mass is outside the contending set. Association among near-frontier designs: flow vs low-power -0.97, head vs low-power -0.96, flow vs low-mass -0.93, head vs low-mass -0.64, flow vs head +0.85. So: high flow and high head each trade against low power; flow and head move together, so you cannot get both low power and high flow or head. Mass gets association but no weight, so it follows flow (bigger pumps carry more) without being the binding quantity. How sure: moderately. Contending set was identical under the "robust" scaler (also tau 1000), the exponents are the exact-maximum fit, and the K=1 slack is small. Doubts: the target fraction 0.25 is unusual; power is computed in the model from flow, head and efficiency, so flow-head-power is nearly an identity of the physics, and the tension is partly the model's own arithmetic; the docs say association near a binding surface is negative even where nobody traded anything, and I did not run a second table.

Step 6 (model). The model helped me orient the columns (power and mass smaller-is-better is obvious from the calc defs) and separate inputs from outputs, and told me power depends on flow and head (a warning about the finding). It did not help connect to the tool: no page says how to go from a SysML v2 model to the table or to the package; the table was handed to me already as CSV, and I used only pandas and the conditioning page. I could connect my model's outputs by hand (pick output columns, orient them), but no docs path connects model to tool automatically, and I did not look for one.
