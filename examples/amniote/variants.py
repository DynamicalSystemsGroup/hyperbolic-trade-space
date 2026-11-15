"""WP59 conditioning ladder on the amniote table.

``uv run --frozen python examples/amniote/variants.py`` loads the cached archive through
``run.load`` (manifest checks run on every load) and fits the primary rule and the variants below,
one change at a time, writing ``variants.json`` beside this file. The fit, the temperature rule
(a tenth of rows above the surface) and the seeds are those of ``run.py``; the existing chain, PCA
after the fit on the near-frontier chart, is the ``spread_first_direction`` of every variant.

Each variant is one row of the table in ``work-packages/WP59-rounds/amniote.md``; the first row
is the record's primary rule. The last row changes two things, stated in its rule.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
import run  # noqa: E402
import variantkit  # noqa: E402

ORIENT_UNINVERTED = [1, 1, 1, 1]


def rows(raw):
    """The ladder as (label, rule, frame, options)."""
    x = run.complete(raw)
    y = raw.dropna(subset=run.COLS)
    y = y[(y[run.COLS] > 0).all(axis=1)]
    yield (
        "primary",
        "record's rule: complete cases of the four metrics and mass; log, orientation (+,+,+,-), "
        "standard scaler; mass kept in the metrics",
        x,
        {},
    )
    yield (
        "no_scaler",
        "pure log, no scaler (metric = attribute, maturity as 1/days)",
        x,
        {"scaler": None},
    )
    yield (
        "robust_scaler",
        "robust scaler of the log (median and interquartile range)",
        x,
        {"scaler": "robust"},
    )
    yield (
        "quantile",
        "QuantileTransformer uniform of each oriented attribute, shifted into (0, 1]",
        x,
        {"quantile": True},
    )
    yield (
        "maturity_not_inverted",
        "maturity read as larger is better (orientation +,+,+,+)",
        x,
        {"orient": ORIENT_UNINVERTED},
    )
    yield (
        "mass_partialled_out",
        "linear effect of log mass removed from each oriented log metric",
        x,
        {"partial_out": True},
    )
    yield "mass_dropped", "mass not required: complete cases of the four metrics only", y, {}
    yield (
        "annual_fecundity_added",
        "derived metric litter size x litters per year added as a fifth",
        x,
        {"derived": True},
    )
    yield (
        "maturity_not_inverted_quantile",
        ("two changes: maturity not inverted and the quantile map"),
        x,
        {"quantile": True, "orient": ORIENT_UNINVERTED},
    )


def metrics(frame, opt):
    """The conditioned metrics and their names for one variant."""
    orient = opt.get("orient", run.ORIENT)
    names = list(run.NAMES)
    if opt.get("quantile"):
        M = variantkit.quantile_metrics(frame[run.COLS].to_numpy(float), orient)
    else:
        M = run.condition(
            frame,
            orient=orient,
            partial_out=opt.get("partial_out", False),
            scaler=opt.get("scaler", "standard"),
        )
    if opt.get("derived"):
        # the product of two attributes, then the primary conditioning of the new column
        a = frame["litter_or_clutch_size_n"].to_numpy(float)
        b = frame["litters_or_clutches_per_y"].to_numpy(float)
        z = np.log(a * b)
        extra = np.exp((z - z.mean()) / z.std())
        M = np.column_stack([M, extra])
        names.append("annual_fecundity")
    return M, names


def main():
    raw = run.load()
    out = {"variants": {}}
    x = run.complete(raw)
    out["log_spread_of_attributes"] = {
        n: float(np.log(x[c]).std()) for n, c in zip(run.NAMES, run.COLS, strict=True)
    }
    for label, rule, frame, opt in rows(raw):
        M, names = metrics(frame, opt)
        res = variantkit.fit_variant(M, names, k2=True)
        res["rule"] = rule
        out["variants"][label] = res
        print(label, res.get("n_lemma"), res.get("contending_set"), flush=True)
    variantkit.dump(out, HERE / "variants.json")


if __name__ == "__main__":
    main()
