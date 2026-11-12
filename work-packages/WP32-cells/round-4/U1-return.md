# U1 cell return, round 4

Header
- model: Sonnet
- persona: U1
- head: df0cad9
- table: table.csv (scratchpad copy of tests/fixtures/user-tests/plain_table.csv)
- stage URL: http://127.0.0.1:8791/ ; round 4

## 1. The code (final script u1.py, run as `uv run python u1.py 1`; plus the robustness check u1_check.py)

```python
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
from hyperbolic_trade_space.plotting import plot_tensions

df = pd.read_csv("table.csv")
cols = ["strength_mpa", "weight_kg", "stiffness_gpa", "cost_usd"]
A = df[cols].to_numpy(float)
pre = LogAffinePreconditioner(orientation=[1, -1, 1, -1])
M = pre.fit_transform(A)

tau = select_temperature(M, 0.10, bounds=(3, 1e4))
print("tau", round(tau, 1))
for K in range(1, 5):
    f = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, round(f.mean_slack_, 3), f.term_share_.round(2), f.termination_.status)
    print(f.exponents_.round(2))

import sys
K = int(sys.argv[1]) if len(sys.argv) > 1 else 1
ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
rep = tension_report(ts, M)
reps = rep if isinstance(rep, list) else [rep]
for r in reps:
    print(r.lemma_name, r.contending_set, r.contending_exponents.round(3))
    print(r.exponents.round(2)); print(r.elasticities.round(2)); print(r.association.round(2))
    ax = plot_tensions(r, names=cols)
    ax.figure.savefig(f"tensions_{reps.index(r)}.png", bbox_inches="tight")
```

u1_check.py (conditioning robustness): same load/orientation, loops scaler in ["standard","robust"], each time select_temperature(M,0.10,bounds=(3,1e4)), K=1 fit, tension_report, prints lemma_name, contending_set, contending_exponents, n_near_frontier, elasticities.

Output as run: tau 173.2. Mean slack by K: K=1 0.578, K=2 0.574, K=3 0.572, K=4 0.572. K=1 exponents [0.49 0.5 0.0 0.01]. K=2 term shares [0.79 0.21], and every K>=2 term has exponents near [0.5, 0.5, 0, 0] or a variant of it. Report at K=1: trilemma, contending set [0 1 3], contending exponents [0.49 0.506 0.004]. Elasticity row for strength: [-1, -1.03, 0, -0.01]. Association strength vs weight metric -1.00, strength vs cost -0.27, stiffness vs the others |r| <= 0.19. Robust scaler: tau 202.9, same contending set [0 1 3], exponents [0.478 0.517 0.005], elasticity about -1.0 to -1.08.

## 2. Pages opened, in order
1. TASK.md
2. README.md (checkout) and pyproject.toml, head of table.csv
3. http://127.0.0.1:8791/ (root page, first 3000 chars only, which was CSS and header)
4. http://127.0.0.1:8791/docs/ (home)
5. docs/getting-started/
6. docs/user-guide/conditioning/
7. docs/user-guide/fitting/
8. docs/user-guide/choosing-k/
9. docs/user-guide/tensions/
10. docs/user-guide/chart/
Not opened: overview, prediction, termination, limitations, API, examples, theory, glossary, further reading.

## 3. Errors and where they stopped me
- No errors from the package. `uv sync` completed (it also installed the docs, paper and case groups: opensysml, z3-solver, mkdocs, etc.; slow, but it worked).
- Shell slip of my own: a mistyped bash function produced "(eval):7: =GS not found"; I wrote a small fetch script instead.
- No `import hyperbolic_trade_space` failure; I used `uv run python`, since the README says `uv sync` only and never says to use `uv run`.

## 4. Questions I would ask a colleague
- The README snippet fits `HyperbolicTradeSpace(temperature=20.0)` on a synthetic table. For my table, what temperature? The getting-started page says tau is "how hard the maximum is" but only the fitting page says to use select_temperature with target 0.10 and bounds (3, 1e4); I found it by reading on.
- Is a tension reported "strength vs weight, elasticity -1" a real physical trade-off or just the sample (the pages say it describes the sampled table and not a causal exchange)? What would I do to tell them apart?
- stiffness gets exponent 0.00: does that mean it does not trade with anything, or that it is never the binding quantity? The pages say "contending" means binding at the edge of the table, which is not what I would call "trade off".
- Which of my columns is "configuration" (batch, sample) versus an attribute? Getting-started says leave configuration out; I assumed batch is a label and dropped it. Could batch matter (per-batch fits)? Not covered.
- The chart: "look at the chart" is ambiguous. The plot functions plot_log_plane (2 metrics) and plot_frontier_surface_3d (3 metrics) do not take my 4 metrics; I used plot_tensions (the heatmap). Is that the intended chart? What is the best plot for d=4?
- A few extreme rows (max strength 796, cost 500443 against means 97 and 8830): outliers or real? The pages suggest the robust scaler but not how to judge.
- Why is the K=1 temperature chosen at 0.10 above frontier when the cell exponents are almost identical at all K? Is that a sign my table has one real trade-off?

## 5. Steps to the need
1. README: `git clone ... && uv sync`. My checkout was already local, so I ran `uv sync` only. It worked. The README snippet uses make_frontier_data and a pretend orientation, which I read as a template for my own conditioning step.
2. README gave me LogAffinePreconditioner(orientation=[...]); I decided strength and stiffness larger-is-better, weight and cost smaller-is-better (+1, -1, +1, -1) from the column names alone; checked no NaNs or non-positive values (none).
3. For the temperature, README's snippet used 20.0; the getting-started page repeated it. I did not know how to choose tau for my data, so I read the fitting page, found select_temperature, and used target 0.10 with bounds (3, 1e4). (A detour of about two pages.)
4. For K, I read the choosing-k page, which gives checks and no rule. I used a sweep of mean_slack_ over K=1..4 (my own short loop, not the page's sweep helper). The drop is 0.004 from K=1 to 2 and almost nothing afterwards, so I chose K=1. The page's thinnest-term and resampling checks I did not run.
5. Tension report: read the tensions page for what lemma_name, contending set, elasticities and association mean, ran tension_report and plot_tensions, then re-ran with the robust scaler. I got slightly lost on the chart page (plots for 2 or 3 metrics only) and went back to the tensions page for the heatmap.

Where I got lost: (a) which temperature to use (README and getting-started give 20.0 without telling me how to pick); (b) which plot is "the chart" for 4 metrics; (c) the elasticity wording ("with a minus sign") and what a trilemma means when one exponent is 0.004.

Plain-sentence answers
Step 2 (conditioning): The four measured quantities are strength_mpa, weight_kg, stiffness_gpa and cost_usd. I left out sample (an index) and batch (a label). Strength and stiffness are larger-is-better and weight and cost smaller-is-better, so the orientation is [1, -1, 1, -1]. LogAffinePreconditioner turned them into positive, larger-is-better metrics. The orientation is my judgement from the names, since the pages say a wrong sign is not detected.
Step 3 (fit): HyperbolicTradeSpace with tau = 173.2 chosen by select_temperature (target 0.10 above the surface, bounds (3, 1e4)) fit on the conditioned table without error.
Step 4 (K): I chose K = 1. Mean slack fell from 0.578 at K=1 to 0.574 at K=2 and 0.572 at K=3 and 4, so the extra terms barely reduce slack, and the exponents of the extra terms repeat the K=1 ones. This is a break-test by eye, and the page says it cannot decide K alone.
Step 5 (tension): Strength and weight trade off against each other, strongly. The fitted exponents are about 0.49 for strength and 0.50 for lightness (inverted weight); the elasticity is about -1, meaning, near the frontier, a 1% gain in strength goes with about a 1% loss in lightness (weight). Among the designs near the frontier, their log-metrics correlate at -1.00. Cost enters only faintly (exponent 0.004 to 0.01, association -0.27 with strength), and stiffness not at all (exponent 0.00, shown greyed). The report calls it a trilemma because it counts every exponent above 1e-9, which is misleading to me here. I read it as a dilemma of strength against weight. How sure: fairly sure of the strength-weight pair, which came out the same under the standard and robust scalers and at K=1 to 4, with 21 to 23 designs near the frontier; not sure it is physical and not an artifact of the sample, and the cost and stiffness conclusions rest on tiny exponents. I did not do the other robustness checks (resampling, shifts). The heatmap is tensions_0.png in my directory.

## 6. Standing question
No. Nothing made me think I need SysML v2, satellites or a spacecraft model. The docs home page says "See the worked case: a cubesat trade study, a synthetic satellite demonstrator" and README mentions "examples/adcs/ — the ADCS case study", but both read as an optional example, and I did not open them. The only slight friction was the "Bring my own system model, and know what must hold" bullet on the docs home page, which I did not follow, since I have a CSV and no model.
