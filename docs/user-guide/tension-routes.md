# From a tension to attributes and design variables

A tension is read in the conditioned metrics. Two routes lead out of them, and only one is a calculation.

## To the attributes' own units

The conditioning is log-affine, `log m = alpha log(a + s) + b`, so a tension in the metrics
maps to the attributes by the chain rule: `d s_j / d s_i = -(w_i alpha_i)/(w_j alpha_j) (a_j + s_j)/(a_i + s_i)`.
Give `design_tensions` the fitted preconditioner and the raw attributes and it returns this as
`attribute_tensions`.

```python {.runnable}
import numpy as np
from tradespace import (
    HyperbolicTradeSpace,
    LogAffinePreconditioner,
    design_tensions,
)

rng = np.random.default_rng(0)
S = rng.uniform(1.0, 5.0, size=(300, 3))
pre = LogAffinePreconditioner(orientation=[-1, -1, 1]).fit(S)
M = pre.transform(S)
est = HyperbolicTradeSpace(temperature=10.0).fit(M)
dt = design_tensions(est, M, preconditioner=pre, attributes=S)
print(dt.attribute_tensions[0].round(2))
```

The sign in attribute units is minus the sign of `alpha_i alpha_j`: negative for two attributes
of one orientation (two costs), positive for one of each. "Negative where both contend" is a
statement about the metrics only.

## To the design variables

The fit never sees the configuration, and the evaluation behind the attributes is a black box. A
tension is a derivative along the fitted reference surface, not the effect of changing a design variable. What
you can compute is each sampled design's tensions beside its configuration, and a
[regressor](prediction.md) from configuration to metrics, whose slopes at the sampled designs are
estimates of the evaluation's own. Past the sampled designs, a tension translated into a design
variable is a conjecture: propose the configuration, build it and measure it.
