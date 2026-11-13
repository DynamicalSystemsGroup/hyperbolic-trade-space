# U3 cell return, round 5

Header: model Sonnet; persona U3; head ff9c410; table table.csv (plain table); stage http://127.0.0.1:8791/ (round 5).

## 1. The code (u3.py, run as `uv run --no-default-groups python u3.py`)
```python
import numpy as np, pandas as pd
from hyperbolic_trade_space import (HyperbolicTradeSpace, LogAffinePreconditioner,
    select_temperature, tension_report)
d = pd.read_csv("table.csv")
cols = ["strength_mpa", "weight_kg", "stiffness_gpa", "cost_usd"]
print(d[cols].min())
A = d[cols].to_numpy()
pre = LogAffinePreconditioner(orientation=[1, -1, 1, -1])
M = pre.fit_transform(A)
tau = select_temperature(M, 0.10, bounds=(3, 1e4))
print("tau", tau)
for K in (1, 2, 3, 4):
    f = HyperbolicTradeSpace(n_terms=K, temperature=tau, random_state=0).fit(M)
    print(K, round(f.mean_slack_, 3), f.term_share_.round(2), f.termination_.status)
    for r in np.atleast_1d(f.exponents_): print("   ", r.round(2))
ts = HyperbolicTradeSpace(temperature=tau).fit(M)
rep = tension_report(ts, M)
print(rep.lemma_name, rep.contending_set, rep.contending_exponents.round(3))
print(rep.exponents.round(3)); print(np.round(rep.elasticities,2)); print(np.round(rep.association,2))
import matplotlib; matplotlib.use("Agg")
from hyperbolic_trade_space.plotting import plot_tensions
ax = plot_tensions(rep, names=cols); ax.figure.savefig("tensions.png")
```
Output highlights: min values all positive; tau 173.2; mean_slack_ by K = 0.578, 0.574, 0.572, 0.572 (K=2..4 certified); report: trilemma [0 1 3], contending_exponents [0.49 0.506 0.004]; exponents [0.49 0.505 0. 0.005]; association strength-weight -1.00, strength-cost -0.27, weight-cost +0.26, stiffness vs others about 0.19/-0.19/-0.05.

## 2. Pages opened, in order
TASK.md; README.md (checkout); table.csv (head, describe, corr); / (root, as text); /docs/getting-started/; /docs/user-guide/conditioning/; fitting/; choosing-k/; tensions/; chart/; tensions.png (own output).

## 3. Errors and where they stopped me
No errors. One divergence: README/getting-started say `git clone ...` then `uv sync`; I already had the checkout, so I ran `uv sync --no-default-groups` (the README's "package only" line). Import worked at once. Timing: sync 0.7 s (cached); first import plus first run about 30 s wall; the whole script after that about 8 s. Install to first successful fit: roughly 1 to 2 minutes including reading the README and Getting started and writing the script.

## 4. What I would ask a colleague
- Is the ordering "larger is better" for strength and stiffness and "smaller is better" for weight and cost right for your study? (I assumed so.)
- The batch column (A/B/C): analysed separately or pooled? (I pooled and dropped it.)
- The README example conditions with LogAffinePreconditioner but the Getting started page's example fits raw data; the docs say conditioning is mine to choose, but no page tells me which scaler ("standard" default vs "robust") to prefer for heavy-tailed columns like mine (values reach 500000 for cost). I used the default and did not refit with "robust", which the Conditioning page recommends as a robustness check.
- The association of exactly -1.00 between strength and weight near the frontier: a real trade or the closure artefact the Tensions page mentions? I could not tell which from the report alone.

## 5. Steps to the need
README (example, install) -> `uv sync --no-default-groups` -> import OK -> Getting started (first fit, reading output, "Your own data") -> Conditioning page (orientation, scaler) -> Fitting page (select_temperature recipe, bounds 3 to 1e4, target 0.10) -> Choosing K page (sweep on mean_slack_) -> Tensions page (contending set, elasticities, association, closure note) -> script -> chart. No backtracking, not lost. Never read Examples, Termination or Limitations.

## 6. Standing question
No. Nothing made me think I needed SysML v2, satellites or a spacecraft model. (The root page mentions a "cubesat case" only as "a synthetic demonstrator", which I read as an example.)

Plain-sentence answers
Step 2: strength_mpa and stiffness_gpa larger-is-better (+1), weight_kg and cost_usd smaller-is-better (-1); dropped sample and batch; no zeros or NaNs; conditioned with LogAffinePreconditioner(orientation=[1,-1,1,-1]) with default scaling.
Step 3: select_temperature (target 0.10, bounds 3 to 1e4) gave tau about 173; fitted HyperbolicTradeSpace at that temperature.
Step 4: tried K = 1 to 4 and compared mean_slack_ at the one temperature; it falls only from 0.578 to 0.574 to 0.572 to 0.572 with nearly identical exponents in every term, so kept K = 1; the page says no check decides K alone, so this is judgement, not a certificate.
Step 5: the report names a trilemma on strength, weight and cost, but the exponents are about 0.49 strength, 0.505 weight, 0.005 cost, stiffness 0. In practice a dilemma between strength and weight (elasticity about -1, association -1.00 near the frontier). Cost's exponent is tiny, marginal; stiffness does not take part. Fairly sure about strength versus weight (same for all K from 1 to 4 and in the chart), less sure about cost; did not test a second conditioning or resampling. The -1.00 association may partly be the closure effect the docs mention.
