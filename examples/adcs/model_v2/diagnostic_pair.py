"""The diagnostic pair of a WP23 round (D-6): the K = 1 heatmap across tau and the K = 3 record.

A round of the model-realism loop regenerates the two datasets on the round's model and reads the
fit's answer beside the model's views. This script writes that answer for one round, from the
round's two tables, the traded-metric list of the coverage table and an output folder:

* ``heatmap.png``: :func:`case.tau_sweep_figure` on the primary regime (the aggressive gain box):
  the fraction above V = 1 and the effective sample size against tau, and each metric's K = 1
  exponent across tau, the drawing of the paper's ``fig-tau-sweep``;
* ``heatmap_baseline.png``: the same drawing on the baseline regime (the baseline gain box), so a
  metric at zero exponent can be read against both gain boxes; each heatmap is titled with its
  regime;
* ``k3_record.md``: per regime, the K = 1 fit (temperature, fraction above, effective size, the
  contending set and its n-lemma) and the K = 3 fit per monomial term (its cell's rows and share,
  the contending set, the n-lemma, the leading metrics by exponent, the near-frontier count, the
  reach and the gap), as :func:`case.fit_line`, :func:`case.tension_table`,
  :func:`case.facet_table` and :func:`case.exponent_table` report them;
* ``coverage.md``, copied from beside the coverage table.

The two regimes are named ``primary`` and ``baseline`` in everything written here; the CaseSpec of
``case.py`` keys the baseline regime ``stock``, and that key is mapped to the word at the point of
writing (:data:`REGIME`), never changed.

The fit is ``case.py``'s and nothing here changes it: :func:`case.load_study` filters and
conditions the table, :func:`case.k_fits` re-selects the temperature at each K by the
fraction-above criterion with the spec's target and bounds, and the tables and the figure are the
case module's functions called read-only. What the round supplies is the data and the metric list:
the ``CUBESAT`` spec is copied (``dataclasses.replace``) with the round's folder, its two files and
the metrics the coverage table names (the ``metrics`` table of ``coverage.csv``, in its order,
mapped to dataset columns by the spec's own plain names). The frozen data and the paper's figure are
not read.

    uv run python examples/adcs/model_v2/diagnostic_pair.py --dataset D.csv --gains G.csv \\
        --coverage examples/adcs/model_v2/views/coverage.csv --out work-packages/WP23-rounds/round-N
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import os
import pathlib
import re
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
ADCS = HERE.parent
if str(ADCS) not in sys.path:  # the case module lives beside model_v2/ (pytest adds the path)
    sys.path.insert(0, str(ADCS))

import case  # noqa: E402

TERM = re.compile(r"^facet\b")  # the case tables' column names; a round's record says "term"
ZERO = 1e-3  # the figure's own threshold for a metric "with w > 1e-3" (case.tau_sweep)
REGIME = {"primary": "primary", "stock": "baseline"}  # the CaseSpec's key -> the round's word
FIGURES = {"primary": "heatmap.png", "stock": "heatmap_baseline.png"}


def metrics_from_coverage(path: pathlib.Path) -> list[str]:
    """The traded metrics of the coverage table's ``metrics`` rows, plain names in table order."""
    with open(path, newline="") as fh:
        rows = list(csv.reader(fh))
    names = []
    for row in rows:
        if row and row[0] == "metrics" and row[1] != "metric":
            names.append(row[1])
    if not names:
        raise ValueError(f"{path}: no 'metrics' table rows")
    return names


def round_spec(dataset: pathlib.Path, gains: pathlib.Path, metrics: list[str]) -> case.CaseSpec:
    """The case spec on the round's files and metric list; everything else is ``case.CUBESAT``."""
    spec = case.CUBESAT
    by_name = {v: k for k, v in spec.short.items()}
    unknown = [m for m in metrics if m not in by_name]
    if unknown:
        raise ValueError(f"metrics not in the case spec: {unknown}")
    attrs = tuple(by_name[m] for m in metrics)
    data_dir = dataset.resolve().parent
    return dataclasses.replace(
        spec,
        name=f"{spec.name} (round)",
        data_dir=data_dir,
        regimes={
            "primary": os.path.relpath(gains.resolve(), data_dir),
            "stock": os.path.relpath(dataset.resolve(), data_dir),
        },
        attributes=attrs,
        short={a: spec.short[a] for a in attrs},
        units={a: spec.units[a] for a in attrs},
        orientation={a: spec.orientation[a] for a in attrs},
        subsystems={a: spec.subsystems[a] for a in attrs},
        views={}, view="", association_pairs=(),
    )  # fmt: skip


def _md(df) -> str:
    cols = [TERM.sub("term", str(c)) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(_cell(v) for v in r) + " |")
    return "\n".join(lines)


def _cell(v) -> str:
    if isinstance(v, float):
        return f"{v:.4g}" if abs(v) >= 1e-3 or v == 0 else f"{v:.2e}"
    return str(v)


def zero_across_tau(study) -> list[str]:
    """The metrics whose K = 1 exponent is at most ``ZERO`` at every tau of the sweep."""
    hts, _, _ = case._lib()
    import numpy as np

    taus = [*np.geomspace(*study.spec.tau_bounds, 12), np.inf]  # case.tau_sweep's default grid
    W = np.array([
        hts.HyperbolicTradeSpace(temperature=t, random_state=study.spec.seed).fit(study.M)
        .exponents_[0] for t in taus
    ])  # fmt: skip
    return [n for j, n in enumerate(study.names) if (W[:, j] <= ZERO).all()]


def k1_reading(study, fits) -> str:
    """The K = 1 contending set as :func:`case.tension_table` reports it, or its refusal."""
    try:
        k1 = case.tension_table(study, fits[1]).iloc[0]
    except ValueError as exc:  # the report's own guard on the near-frontier count
        return f"K = 1 report refused at the band 1/tau = {fits[1].band:.4g}: {exc}"
    return (
        f"K = 1 contending set ({k1['n_lemma']}-lemma, {k1['near-frontier']} near-frontier "
        f"designs in the band 1/tau = {fits[1].band:.4g}): {k1['contending set']}. "
        f"Largest exponents: {k1['largest exponents']}."
    )


def term_cells(study, fits) -> str:
    """Rows and share of each monomial term's cell, read from the K = 3 estimator (no report)."""
    import numpy as np
    import pandas as pd

    est = fits[3].estimator
    sizes = np.bincount(est.facet_, minlength=3)
    cells = {
        "term": range(1, 4), "rows": sizes.astype(int), "share": est.facet_share_,
        "reach beta_k": est.log_offset_,
    }  # fmt: skip
    return _md(pd.DataFrame(cells))


def term_table(study, fits) -> tuple[str | None, str]:
    """:func:`case.facet_table` at K = 3 with a note naming the report band.

    The function's default band is the K = 1 band; when a term's cell has too few near-frontier
    designs there (the report refuses), the table is taken at its other documented default, the
    K = 3 fit's own band, and the note carries the refusal verbatim; when that refuses too, there is
    no report table and the note carries both refusals. The fit is the same in every case.
    """
    try:
        return _md(case.facet_table(study, fits, K=3)), f"the K = 1 band 1/tau = {fits[1].band:.4g}"
    except ValueError as first:
        try:
            table = _md(case.facet_table(study, {3: fits[3]}, K=3))
        except ValueError as second:
            return None, (
                f"no report: at the K = 1 band 1/tau = {fits[1].band:.4g} it refused ({first}); "
                f"at the K = 3 fit's own band 1/tau = {fits[3].band:.4g} it refused ({second})"
            )
        return table, (
            f"the K = 3 fit's own band 1/tau = {fits[3].band:.4g}; at the K = 1 band "
            f"1/tau = {fits[1].band:.4g} the report refused: {first}"
        )


def regime_record(study, fits) -> list[str]:
    """The K = 1 and K = 3 readings of one regime, as the case functions report them."""
    table, band_note = term_table(study, fits)
    lines = [
        f"### {REGIME[study.regime]} regime ({study.spec.regimes[study.regime]}): "
        f"{len(study.M)} feasible of {len(study.raw)} designs",
        "",
        "Fit lines (temperature re-selected at each K by the fraction-above criterion):",
        "",
        _md(case.fit_line(study, fits[1]).assign(K=1)),
        "",
        _md(case.fit_line(study, fits[3]).assign(K=3)),
        "",
        k1_reading(study, fits),
        "",
        "K = 1 exponents:",
        "",
        _md(case.exponent_table(study, fits[1])),
        "",
        f"Metrics at zero exponent (w <= {ZERO:g}) at every tau of the sweep: "
        + (", ".join(zero_across_tau(study)) or "none")
        + ".",
        "",
        "K = 3 cells (rows and share of each monomial term, from the estimator):",
        "",
        term_cells(study, fits),
        "",
        "K = 3 exponents per term:",
        "",
        _md(case.exponent_table(study, fits[3])),
        "",
        f"K = 3 report per term (band: {band_note}):",
        "",
        table or "(no report table)",
        "",
    ]
    return lines


def write_pair(dataset, gains, coverage, out) -> dict:
    """Write the pair into ``out``; return the metrics and the zero-exponent metrics by regime."""
    dataset, gains, coverage, out = map(pathlib.Path, (dataset, gains, coverage, out))
    metrics = metrics_from_coverage(coverage)
    spec = round_spec(dataset, gains, metrics)
    out.mkdir(parents=True, exist_ok=True)
    record = [
        "# K = 1 and K = 3 record of the round",
        "",
        f"Primary regime: `{gains.name}`; baseline regime: `{dataset.name}`; traded metrics "
        f"({len(metrics)}, from `{coverage.name}`): {', '.join(metrics)}. The fit is `case.py`'s "
        "with its defaults (target fraction above V = 1: "
        f"{spec.target_frac}, temperature bounds {spec.tau_bounds}, seed {spec.seed}); "
        "generated by `examples/adcs/model_v2/diagnostic_pair.py`.",
        "",
    ]
    zero = {}
    for regime, figure in FIGURES.items():
        study = case.load_study(regime, spec)
        fits = case.k_fits(study, Ks=(1, 3))
        fig = case.tau_sweep_figure(study, fits[1])
        # the heatmap panel (the third axes; the fourth is its colourbar) is titled with the regime
        fig.axes[2].set_title(
            f"K = 1 exponent of each metric across tau, {REGIME[regime]} regime",
            fontsize=case.FIGURE_MIN_FONT_PT,
        )
        fig.tight_layout()
        fig.savefig(out / figure, dpi=case.FIGURE_DPI)
        case._plt().close(fig)
        record += regime_record(study, fits)
        zero[regime] = zero_across_tau(study)
    (out / "k3_record.md").write_text("\n".join(record))
    source = coverage.with_suffix(".md")
    if source.exists():
        shutil.copyfile(source, out / "coverage.md")
    return {"metrics": metrics, "zero_across_tau": zero}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dataset", type=pathlib.Path, required=True, help="the baseline regime's CSV")
    ap.add_argument("--gains", type=pathlib.Path, required=True, help="the primary regime's CSV")
    ap.add_argument("--coverage", type=pathlib.Path, default=HERE / "views" / "coverage.csv")
    ap.add_argument("--out", type=pathlib.Path, required=True)
    a = ap.parse_args(argv)
    result = write_pair(a.dataset, a.gains, a.coverage, a.out)
    print(f"metrics: {', '.join(result['metrics'])}")
    for regime, names in result["zero_across_tau"].items():
        print(f"{REGIME[regime]} regime: at zero exponent across tau: {', '.join(names) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
