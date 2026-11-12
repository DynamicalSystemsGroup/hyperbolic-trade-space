# U1 return

Header
- model: Sonnet
- persona: U1
- head: 9d83355
- table: ./table.csv
- stage URL: http://127.0.0.1:8791/

## 1. The code (run.py, as run: `uv run --project hts python run.py` from this directory)

```python
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
from hyperbolic_trade_space.plotting import plot_tensions

df = pd.read_csv("table.csv")
print(df.describe().T)
cols = ["strength_mpa", "weight_kg", "stiffness_gpa", "cost_usd"]
orient = [1, -1, 1, -1]   # weight and cost: smaller is better
A = df[cols].to_numpy()
pre = LogAffinePreconditioner(orientation=orient)
M = pre.fit_transform(A)
print("log std", np.log(M).std(axis=0).round(2))

tau = select_temperature(M, 0.10, bounds=(3, 1000))
print("tau", round(tau, 1))
for K in range(1, 5):
    f = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, round(f.mean_slack_, 3), f.term_share_.round(2), f.termination_.status)
    print(f.exponents_.round(2))

K = 1
ts = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
rep = tension_report(ts, M)
print(rep.contending_set, rep.lemma_name, rep.contending_exponents.round(3))
print(rep.exponents.round(3))
print(rep.elasticities.round(2))
print(rep.association.round(2), rep.association_kind)
fig, ax = plt.subplots()
plot_tensions(rep, names=cols, ax=ax)
fig.savefig("tensions.png", dpi=100, bbox_inches="tight")
```

## 2. Pages opened, in order
1. tasks.md (task text)
2. hts/README.md
3. http://127.0.0.1:8791/ (project page)
4. http://127.0.0.1:8791/docs/ (docs home)
5. http://127.0.0.1:8791/docs/getting-started/
6. http://127.0.0.1:8791/docs/user-guide/conditioning/
7. http://127.0.0.1:8791/docs/user-guide/fitting/
8. http://127.0.0.1:8791/docs/user-guide/choosing-k/
9. http://127.0.0.1:8791/docs/user-guide/tensions/
10. http://127.0.0.1:8791/docs/user-guide/chart/
Also read: table.csv (head, describe), my own output tensions.png. I did not use help() or read docstrings.

## 3. Errors
- No error from the package. The README quickstart `uv sync` (run in hts/, the checkout) gave a working `import hyperbolic_trade_space` first time. Note the README never says to import it or gives a first call; the first fit is on the docs site, reached through a link in README line 2 ("docs/index.md", a repo path, not a URL; I found the site from the task text).
- My own mistake: running `uv run python ../run.py` from hts/ gave
  `FileNotFoundError: [Errno 2] No such file or directory: 'table.csv'`. I reran from the table's directory with `uv run --project hts`. Not a doc gap.
- Noise on every run: repeated stderr lines `findfont: Failed to find font weight normal for Lucida Grande, now using 500.` (matplotlib font fallback when plotting; harmless).

## 4. Questions for a colleague
- Is a negative association of exactly -1.00 between strength and weight real, or an artefact? The tensions page says a binding constraint produces negative association near the surface "even where no designer traded the metrics"; but the raw log-correlation of those two is only -0.19, so I read -1.00 as the band holding few, nearly collinear designs. How many designs are in the band? The report does not print it.
- The contending set is [0 1 3] with exponent 0.004 on cost. Is a trilemma with a 0.004 member a trilemma or a dilemma? The docs say participation uses a 1e-3 threshold; is that meant to be read as "cost contends"? I treated it as no.
- The task data has a `batch` column (A/B/C). Is fitting per batch the intended use? Nothing says how to handle a categorical column; I dropped it.
- tau was selected at 178 with default target 0.10 and bounds (3, 1000): does the 1/tau band (0.006 in log V) make sense when metrics are scaled to unit log-std? Unsure.
- Does the tool have a number-of-designs-in-band or bootstrap stability readout for "how sure"? I found none on the pages I read; the tensions page says only "depends on the band".

## 5. Steps to the need
1. README: `uv sync` (worked). Nothing in README to tell me what to do next; followed the task text to the site.
2. Docs home, then Getting started (first fit on synthetic data; code to copy). Clear.
3. Getting started "Your own data" sent me to Conditioning. Used LogAffinePreconditioner(orientation=[1,-1,1,-1]) (weight and cost smaller-is-better). Worked first try. The "diagnostics" list was useful (log std 1.0 confirmed).
4. Fitting page: select_temperature(M, 0.10, bounds=(3,1000)) gave tau 178.2.
5. Choosing K page: its helper code needs `import case` from examples/adcs, which I do not have ("cubesat blocks run from the repository root"); I only used the first method (mean slack against K) with my own loop. Got lost briefly: the page is long, the planted blocks are not about my data.
6. Tensions page; tension_report on K=1; plotted with plot_tensions (names argument found on the page, chart read from my image).
No going back or searching beyond the pages listed. Chart page read but only plot_tensions used; I did not run plot_log_plane (four metrics, not two) and did not find a plot for four metrics other than the tension heatmap.

## 6. Standing question
No. Nothing made me think I need SysML v2, satellites or a spacecraft model. The docs mention a cubesat example and that the Choosing K code "runs from the repository root, where examples/adcs is" (choosing-k page), which is the one place a non-satellite user hits satellite material, but it is skippable.

## Plain-sentence answers to steps 2 to 5

Step 2 (conditioning): my four quantities are strength (MPa, larger better), weight (kg, smaller better), stiffness (GPa, larger better), cost (USD, smaller better). I left out `sample` (an index) and `batch` (a category). All values were positive, so shift 0. I used LogAffinePreconditioner with orientation [1,-1,1,-1] and its default standard scaling, giving four positive larger-is-better metrics with unit log spread.

Step 3 (fit): HyperbolicTradeSpace with temperature 178.2 chosen by select_temperature (target 0.10 above the surface), fitted on the 250 x 4 conditioned matrix.

Step 4 (K): I fitted K = 1 to 4 at that one temperature and read mean slack: 0.578, 0.575, 0.573, 0.572, so there is no break and added terms barely help. The extra terms are also only variants of the same two-metric exponent pattern (about 0.5 on strength and 0.5 on weight), and the thinnest term at K = 4 holds 0.13 (against 0.25 if equal). So I chose K = 1. This follows the Choosing K page, which says no check decides K alone; I did not run its resampling-movement check.

Step 5 (tensions): strength and weight trade off: the fitted frontier weights them about equally (0.49 and 0.50), meaning the frontier is roughly "strength divided by weight" (a specific-strength ceiling), and their near-frontier association is -1.00. Cost has a tiny weight (0.004 in the exact-maximum fit, 0.005 at the fit temperature), stiffness essentially none (0.000), so in this table those two do not bind the frontier; their association with the others (strength-cost -0.37, weight-cost +0.36) is weak and the docs say association alone is only evidence. The report names a trilemma because cost passes the 1e-3 threshold, but I read it as a strength-weight dilemma. How sure: moderately sure of the strength-weight pairing (exponents are stable across K = 1 to 4 and sit at 0.5/0.5); less sure of the -1.00 (probably a band artefact) and of cost being excluded (0.004 is near the threshold). I did not test sensitivity to scaler or shift (the docs suggest it).
