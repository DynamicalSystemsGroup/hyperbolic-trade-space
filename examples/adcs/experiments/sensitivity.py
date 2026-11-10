"""WP16 D-6: the sensitivity of the paper's conclusions to the step-quantized times.

``settling_time_s`` (and ``slew_time_s``, before WP23 G5 left one time metric) was read off the
accepted steps of an adaptive RK45 integration (the oracle's ``"steps"`` method), so it moves by
up to 1.3 percent under perturbations of one unit in the last place
(``work-packages/swap-evidence.md``). This module measures what that does to the paper.

**Regeneration.** Each of the two cubesat datasets (primary: aggressive gain box; baseline: stock
gain box) and the six check designs are regenerated through the clean oracle
(``cubesat_oracle.CubesatOracle``, the same sampler, design ids and seeds as the v2 generation,
the same worker pool) with ``Kp``, ``Kd``, ``panel_span_m`` and ``battery_wh`` of every design
multiplied by ``1 + e``, ``e`` uniform in ``[-1e-12, 1e-12]`` drawn per design and variable from
``numpy.random.default_rng(seed)`` for ``seed`` in 1 to 5 (:func:`perturb`). Seed 0 is the
unperturbed control. Datasets are written to a scratch directory only; :func:`guard` refuses a
directory inside ``examples/adcs/data``, and nothing here touches the ledger.

**Analysis.** For the committed data and each regeneration, :func:`quantities` runs the paper's
computations through ``case.py`` (the one-term fit with the temperature re-selected, K = 2 and 3,
the regime comparison, the nondominated counts, propose-predict-check, the candidates and the
Appendix D tables) and the paper's generated sentences, and :func:`compare_runs` sets every
quantity of the regenerations against the committed one at the precision the paper prints.

From the repository root::

    PYTHONPATH=examples/adcs uv run python -m experiments.sensitivity regenerate --out SCRATCH
    PYTHONPATH=examples/adcs uv run python -m experiments.sensitivity analyse --out SCRATCH

Doctest of the perturbation (bounded, seeded, reproducible):

>>> import pandas as pd
>>> d = pd.DataFrame({"Kp": [1.0, 2.0], "name": ["a", "b"]})
>>> p = perturb(d, 1, columns=("Kp",))
>>> bool((abs(p["Kp"] / d["Kp"] - 1) <= EPS).all()), p["name"].tolist()
(True, ['a', 'b'])
>>> perturb(d, 1, columns=("Kp",)).equals(p)
True
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import json
import math
import shutil
import sys
import time
from collections.abc import Iterable, Mapping
from pathlib import Path

import numpy as np
import pandas as pd

from . import definitions as df_
from . import ledger as lg
from .check_designs import CheckOracle
from .cubesat_oracle import ATTRIBUTE_NAMES, CubesatOracle, build_sampler

EPS = 1e-12
SEEDS = (1, 2, 3, 4, 5)
PERTURBED = ("Kp", "Kd", "panel_span_m", "battery_wh")
PRIMARY_FILE = "adcs_designs_cubesat_gains.csv"
BASELINE_FILE = "adcs_designs_cubesat.csv"
CHECKS_FILE = "check_designs_cubesat.csv"
PREDICTIONS_FILE = "check_predictions_cubesat.csv"
COMMITTED_CHECKS_FILE = "check_designs_committed.csv"  # the committed measurements, for the variant
FLAG_COLUMNS = ("settled", "momentum_ok", "power_ok", "dod_ok")
DATA_ROOT = lg.REPO_ROOT / "examples" / "adcs" / "data"
V2_DATA = DATA_ROOT / "v2"
LABELS = {PRIMARY_FILE: "v2-primary", BASELINE_FILE: "v2-baseline"}


# -- the perturbation --------------------------------------------------------------------------
def perturb(
    designs: pd.DataFrame,
    seed: int,
    eps: float = EPS,
    columns: Iterable[str] = PERTURBED,
) -> pd.DataFrame:
    """Designs with ``columns`` multiplied by ``1 + e``, ``e`` uniform in ``[-eps, eps]``.

    ``e`` is drawn per design and variable from ``numpy.random.default_rng(seed)`` (one
    ``(n, len(columns))`` draw, columns in the order given), so the result depends only on
    ``(seed, n, columns)``. Other columns, the index and the order are unchanged; the input is not
    modified. ``seed = 0`` or ``eps = 0`` returns an equal copy.

    Parameters
    ----------
    designs : pandas.DataFrame
    seed : int
    eps : float, default 1e-12
    columns : iterable of str

    Returns
    -------
    pandas.DataFrame
    """
    cols = list(columns)
    out = designs.copy()
    if not cols or len(out) == 0 or seed == 0 or eps == 0:
        return out
    e = np.random.default_rng(int(seed)).uniform(-eps, eps, size=(len(out), len(cols)))
    for j, c in enumerate(cols):
        out[c] = out[c].to_numpy(float) * (1.0 + e[:, j])
    return out


def guard(path: Path | str) -> Path:
    """The resolved scratch directory; raises ``ValueError`` for one inside ``examples/adcs/data``.

    >>> guard(DATA_ROOT / "v2")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: refusing to write inside examples/adcs/data: ...
    """
    p = Path(path).expanduser().resolve()
    root = DATA_ROOT.resolve()
    if p == root or root in p.parents:
        raise ValueError(f"refusing to write inside examples/adcs/data: {p}")
    return p


# -- regeneration ------------------------------------------------------------------------------
def _experiment(label: str):
    return next(e for e in df_.V2 if e.id == label)


def _write(table: pd.DataFrame, path: Path) -> None:
    """CSV as the runner writes it (``%.9g``), through a temporary name."""
    path = guard(path)
    tmp = path.with_suffix(".tmp")
    table.to_csv(tmp, index=False, float_format="%.9g")
    tmp.replace(path)


def regenerate(out_dir: Path | str, seed: int, workers: int | None = None, n: int | None = None):
    """Regenerate both datasets and the six check designs for ``seed`` into ``out_dir/seed{seed}``.

    The designs are those the v2 generation draws (``build_sampler``; ``design_id`` and ``seed``
    columns unchanged), perturbed by :func:`perturb`, evaluated by the clean oracle and written
    sorted by ``design_id`` with ``%.9g``. Files already present are kept (the run resumes). The
    committed predictions and the committed check measurements are copied alongside for the
    analysis. Returns the directory.

    Parameters
    ----------
    out_dir : path
        Scratch directory (:func:`guard` refuses ``examples/adcs/data``).
    seed : int
        1 to 5 for the sensitivity runs; 0 for the unperturbed control.
    workers : int, optional
        Pool size of the oracle (default: the oracle's: ``EXPERIMENTS_WORKERS`` or CPUs minus one).
    n : int, optional
        Only the first ``n`` designs of each dataset (a quick check, not for the evidence).
    """
    target = guard(Path(out_dir) / f"seed{seed}")
    target.mkdir(parents=True, exist_ok=True)
    for name in (PREDICTIONS_FILE,):
        shutil.copyfile(V2_DATA / name, target / name)
    shutil.copyfile(V2_DATA / CHECKS_FILE, target / COMMITTED_CHECKS_FILE)
    for file, label in LABELS.items():
        if (target / file).exists():
            continue
        exp = _experiment(label)
        text = (lg.REPO_ROOT / exp.model_path).read_text()
        designs = build_sampler(exp).draw(n or exp.count, exp.seed)
        oracle = CubesatOracle(text, exp.scenario, exp.gain_box, workers=workers)
        table = oracle.evaluate(perturb(designs, seed)).sort_values("design_id")
        _write(table.reset_index(drop=True), target / file)
    if not (target / CHECKS_FILE).exists():
        exp = _experiment("v2-check-designs")
        text = (lg.REPO_ROOT / exp.model_path).read_text()
        committed = pd.read_csv(V2_DATA / CHECKS_FILE)
        designs = committed[["role", "design_id", "name", "seed", *oracle_config_names()]]
        inner = CubesatOracle(text, exp.scenario, exp.gain_box, workers=1)
        table = CheckOracle(inner).evaluate(perturb(designs, seed))
        _write(table.reset_index(drop=True), target / CHECKS_FILE)
    return target


def oracle_config_names() -> tuple[str, ...]:
    from .cubesat_oracle import CONFIG_NAMES

    return CONFIG_NAMES


# -- deviation of the data ---------------------------------------------------------------------
def column_deviation(
    a: pd.DataFrame, b: pd.DataFrame, columns: Iterable[str] = ATTRIBUTE_NAMES
) -> pd.DataFrame:
    """Per column the largest relative and absolute deviation of ``a`` from ``b``, rows aligned.

    Relative deviation is ``|a - b| / |b|`` over rows where ``b != 0``.

    >>> x = pd.DataFrame({"u": [1.0, 2.0]}); y = pd.DataFrame({"u": [1.0, 2.2]})
    >>> r = column_deviation(y, x, ["u"]).loc["u"]
    >>> round(float(r["max rel"]), 3), round(float(r["max abs"]), 3)
    (0.1, 0.2)
    """
    rows = {}
    for c in columns:
        x, y = a[c].to_numpy(float), b[c].to_numpy(float)
        d = np.abs(x - y)
        nz = y != 0
        rel = d[nz] / np.abs(y[nz]) if nz.any() else np.zeros(1)
        rows[c] = {"max rel": float(np.max(rel)), "max abs": float(np.max(d)) if len(d) else 0.0}
    return pd.DataFrame(rows).T


def table_differences(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """What differs between two datasets besides the numbers: rows, flags, feasibility, labels."""
    out = {"rows": (len(a), len(b))}
    out["flag cells changed"] = int(sum((a[c] != b[c]).sum() for c in FLAG_COLUMNS if c in a))
    feas = [c for c in ("settled", "power_ok", "momentum_ok") if c in a]
    ma, mb = a[feas].all(axis=1), b[feas].all(axis=1)
    out["feasible designs changed"] = int((ma != mb).sum())
    text = [c for c in ("wheel_class", "st_grade") if c in a]
    out["label cells changed"] = int(sum((a[c] != b[c]).sum() for c in text))
    return out


# -- the quantities the paper reports -----------------------------------------------------------
def _fmt(value, floatfmt: str = ".4g") -> str:
    """The text a table of the paper prints for a value (``paper_common.cell_text``)."""
    if isinstance(value, (bool, np.bool_)):
        return str(bool(value))
    if isinstance(value, (float, np.floating)):
        return "nan" if math.isnan(value) else format(float(value), floatfmt)
    return " ".join(str(value).split())


def _flat(prefix: str, frame: pd.DataFrame, key: str | None = None) -> dict:
    """Every cell of ``frame`` as ``prefix | row | column``; rows named by ``key`` or number."""
    out = {}
    for i, row in frame.reset_index(drop=True).iterrows():
        label = str(row[key]) if key else f"row {i + 1}"
        for col in frame.columns:
            if col == key:
                continue
            v = row[col]
            if isinstance(v, (list, tuple, np.ndarray)):
                v = str(list(v))
            elif isinstance(v, (np.integer,)):
                v = int(v)
            elif isinstance(v, (np.floating,)):
                v = float(v)
            elif isinstance(v, (np.bool_,)):
                v = bool(v)
            out[f"{prefix} | {label} | {col}"] = v
    return out


@contextlib.contextmanager
def _default_spec(case, spec):
    """``case.regime_comparison()`` called without arguments reads ``spec`` (the paper's call)."""
    saved = case.regime_comparison.__defaults__
    case.regime_comparison.__defaults__ = (spec, None)
    saved_spec = case.CUBESAT
    case.CUBESAT = spec
    try:
        yield
    finally:
        case.regime_comparison.__defaults__ = saved
        case.CUBESAT = saved_spec


def _paper_modules():
    paper = str(lg.REPO_ROOT / "paper")
    if paper not in sys.path:
        sys.path.insert(0, paper)
    adcs = str(lg.REPO_ROOT / "examples" / "adcs")
    if adcs not in sys.path:
        sys.path.insert(0, adcs)
    import case
    import generate_findings as gf

    return case, gf


def quantities(data_dir: Path | str) -> dict:
    """Everything the paper reports, computed by ``case.py`` on the files in ``data_dir``.

    Returns a mapping ``name -> value`` (floats, ints, bools, strings), names of the form
    ``group | row | column``. Groups: ``sentence`` (the paper's generated sentences, verbatim),
    ``contending`` (contending sets), ``leading`` (each facet's leading metrics), ``tension``
    (association signs and values), ``tau``, ``certificate``, ``regime``, ``nondominated``,
    ``candidate``, ``predict`` (and ``predict, committed checks``), and the Appendix D tables
    (``D k_table``, ``D exponents``, ``D facets``, ``D tau_sweep``, ``D sensitivity``,
    ``D refits``).
    """
    case, gf = _paper_modules()
    spec = dataclasses.replace(case.CUBESAT, data_dir=Path(data_dir))
    q: dict = {}
    studies = {r: case.load_study(r, spec) for r in spec.regimes}
    fits = {r: case.k_fits(s) for r, s in studies.items()}
    prim, stock = studies["primary"], studies["stock"]
    k1 = fits["primary"][1]
    with _default_spec(case, spec):
        q["sentence | nondominated | text"] = str(gf.nondominated_sentence(prim))
        q["sentence | datasets | text"] = str(gf.datasets_sentence(prim, stock))
        q["sentence | temperature | text"] = str(gf.temperature_sentence(prim, k1))
        q["sentence | K = 1 contending | text"] = str(gf.k1_sentence(prim, k1))
        q["sentence | K sweep | text"] = str(gf.k_sweep_sentence(prim, fits["primary"]))
        q["sentence | certificate | text"] = str(gf.certificate_sentence(fits["primary"]))
        q["sentence | regime | text"] = str(gf.regime_sentence())
        regime_table = case.regime_comparison(spec)
    q.update(_flat("regime", regime_table, key="quantity"))
    for r, st in studies.items():
        f = fits[r]
        base = f[1]
        e = base.estimator
        q[f"fit | {r} K=1 | frac_above_"] = float(e.frac_above_)
        q[f"fit | {r} K=1 | n_eff_"] = float(e.n_eff_)
        rep1 = case._reports(st, base)[0]
        q[f"fit | {r} K=1 | near-frontier designs"] = int(rep1.n_near_frontier)
        q[f"fit | {r} K=1 | band"] = float(rep1.band)
        for K in (1, 2, 3):
            q[f"tau | {r} K={K} | tau selected (printed .1f)"] = f"{f[K].tau:.1f}"
            q[f"fit | {r} K={K} | tau selected (raw)"] = float(f[K].tau)
        for K in (1, 3):
            tt = case.tension_table(st, f[K], band=base.band)
            ft = case.facet_table(st, f, K=K, band=base.band)
            for _, row in tt.iterrows():
                q[f"contending | {r} K={K} facet {int(row['facet'])} | set"] = row["contending set"]
                q[f"contending | {r} K={K} facet {int(row['facet'])} | n_lemma"] = int(
                    row["n_lemma"]
                )
            for _, row in ft.iterrows():
                lead = [s.rsplit(" ", 1)[0] for s in row["largest exponents"].split(", ")]
                q[f"leading | {r} K={K} facet {int(row['facet'])} | metrics"] = ", ".join(lead)
        # facets of K = 2 and 3 compared without their labels (a permutation is not a change)
        for K in (2, 3):
            ft = case.facet_table(st, f, K=K, band=base.band)
            sets = sorted(
                f"{row['contending set']} / "
                + ", ".join(x.rsplit(" ", 1)[0] for x in row["largest exponents"].split(", "))
                for _, row in ft.iterrows()
            )
            q[f"contending | {r} K={K} facets as an unlabelled set | sets"] = " ;; ".join(sets)
        q.update(_flat(f"certificate | {r}", case.certificate_table(f), key="K"))
        q.update(_flat(f"nondominated | {r}", case.nondominated_counts(st), key="view"))
        q.update(_flat(f"D k_table | {r}", case.k_table(st, f), key="K"))
        q.update(_flat(f"D exponents K=1 | {r}", case.exponent_table(st, f[1]), key="metric"))
        q.update(_flat(f"D exponents K=3 | {r}", case.exponent_table(st, f[3]), key="metric"))
        q.update(
            _flat(f"D facets K=3 | {r}", case.facet_table(st, {1: f[1], 3: f[3]}), key="facet")
        )
        q.update(_flat(f"D tau_sweep | {r}", case.tau_sweep(st)))
        q.update(_flat(f"D sensitivity | {r}", case.sensitivity_table(st), key="variant"))
        q.update(_flat(f"D refits | {r}", case.category_refits(st), key="wheel_class"))
    # signs of the tensions: the associations among the near-frontier designs, K = 1, both regimes
    for r, st in studies.items():
        assoc = case.association_table(st, fits[r][1])
        for _, row in assoc.iterrows():
            pair = f"{row['metric a']}, {row['metric b']}"
            q[f"tension | {r} | {pair} | pearson sign"] = _sign(row["pearson"])
            q[f"tension | {r} | {pair} | spearman sign"] = _sign(row["spearman"])
            q[f"tension | {r} | {pair} | pearson"] = float(row["pearson"])
            q[f"tension | {r} | {pair} | spearman"] = float(row["spearman"])
    # the candidates and propose-predict-check on the primary regime
    q.update(_flat("candidate", case.candidate_table(prim, k1), key="candidate"))
    reg = case.fit_regressor(prim)
    pc = case.predict_check(prim, reg)
    q["sentence | candidates | text"] = str(gf.candidates_sentence(case.candidate_table(prim, k1)))
    q["sentence | predict-check | text"] = str(gf.predict_check_sentence(pc, reg))
    q["predict | regressor | tau"] = float(reg.tau)
    # the numbers of the generated sentences that no table row carries, so that the paper can
    # quote their ranges from the results file (``paper_stability``)
    cand = case.candidate_table(prim, k1)
    q["sentence | candidates | lowest log V"] = float(cand["log V"].min())
    q["sentence | candidates | highest log V"] = float(cand["log V"].max())
    q["sentence | candidates | lowest rank"] = float(cand["rank among training"].min())
    q["sentence | candidates | highest rank"] = float(cand["rank among training"].max())
    q["sentence | predict-check | band"] = float(1.0 / reg.tau)
    q["sentence | predict-check | lowest position error"] = float(pc["||dZ|| / band"].min())
    q["sentence | predict-check | highest position error"] = float(pc["||dZ|| / band"].max())
    q["sentence | temperature | band"] = float(fits["primary"][1].band)
    cert = case.certificate_table(fits["primary"])
    cert = cert[cert["K"] > 1]
    q["sentence | K sweep | largest facet gap"] = float(cert["max gap"].max())
    q["sentence | K sweep | smallest margin"] = float(cert["gamma"].min())
    q["sentence | K sweep | smallest radius"] = float(cert["radius"].min())
    q.update(_flat("predict", pc, key="proposal"))
    for _, row in pc.iterrows():
        q[f"predict | {row['proposal']} | outcome"] = (
            f"log V {'pass' if row['log V within band'] else 'miss'}, "
            f"position {'pass' if row['Z within band'] else 'miss'}"
        )
    kept = (
        COMMITTED_CHECKS_FILE if (Path(data_dir) / COMMITTED_CHECKS_FILE).exists() else CHECKS_FILE
    )
    committed_spec = dataclasses.replace(spec, checks_file=kept)
    pc_c = case.predict_check(dataclasses.replace(prim, spec=committed_spec), reg)
    q.update(_flat("predict, committed checks", pc_c, key="proposal"))
    for _, row in pc_c.iterrows():
        q[f"predict, committed checks | {row['proposal']} | outcome"] = (
            f"log V {'pass' if row['log V within band'] else 'miss'}, "
            f"position {'pass' if row['Z within band'] else 'miss'}"
        )
    return q


def _sign(x: float) -> str:
    return "+" if x > 0 else ("-" if x < 0 else "0")


# -- comparison ---------------------------------------------------------------------------------
def compare_runs(committed: Mapping, runs: Mapping[str, Mapping]) -> pd.DataFrame:
    """Every quantity: committed value, range over the runs, and whether the printed text changes.

    Numeric quantities get ``min`` and ``max`` over the runs; text and boolean quantities get the
    number of runs that equal the committed value. ``printed change`` is true when any run prints
    differently from the committed value (floats at ``.4g``, as the paper's tables do; text
    verbatim). Columns: ``quantity``, ``committed``, ``min``, ``max``, ``runs equal``,
    ``printed change``, ``identical`` (the exact value, not only the printed one).

    >>> c = {"a | r | x": 1.0, "a | r | s": "u"}
    >>> r = {"1": {"a | r | x": 1.00001, "a | r | s": "u"},
    ...      "2": {"a | r | x": 1.0, "a | r | s": "v"}}
    >>> t = compare_runs(c, r).set_index("quantity")
    >>> bool(t.loc["a | r | x", "printed change"]), bool(t.loc["a | r | s", "printed change"])
    (False, True)
    """
    rows = []
    for name, base in committed.items():
        vals = [run.get(name) for run in runs.values()]
        numeric = isinstance(base, (int, float)) and not isinstance(base, (bool, np.bool_))
        printed = [_fmt(v) for v in vals]
        row = {
            "quantity": name,
            "committed": base,
            "runs equal": int(sum(p == _fmt(base) for p in printed)),
            "printed change": any(p != _fmt(base) for p in printed),
            "identical": all(_same(v, base) for v in vals),
        }
        row["numeric"] = bool(numeric and all(isinstance(v, (int, float)) for v in vals))
        row["min"] = min(vals) if row["numeric"] else None
        row["max"] = max(vals) if row["numeric"] else None
        rows.append(row)
    return pd.DataFrame(rows)


def _same(a, b) -> bool:
    if isinstance(a, float) and isinstance(b, float):
        return (math.isnan(a) and math.isnan(b)) or a == b
    return a == b


CONCLUSIONS = (
    ("the contending sets (K = 1, both regimes; each facet at K = 3)", ("contending |",)),
    ("each facet's leading metrics", ("leading |",)),
    ("the signs of the tensions (the reported pairs, both regimes)", ("tension |",)),
    ("the selected temperatures (K = 1, 2, 3, both regimes)", ("tau |",)),
    ("the certificate statuses (K = 1, 2, 3, both regimes)", ("certificate |",)),
    ("the regime comparison", ("regime |", "sentence | regime")),
    ("the nondominated counts", ("nondominated |", "sentence | nondominated")),
    ("the check designs' outcomes (pass or miss)", ("predict |", "predict, committed checks |")),
)


def verdicts(table: pd.DataFrame) -> pd.DataFrame:
    """For each conclusion of ``CONCLUSIONS``: identical across the runs and to the committed?

    The conclusion is judged on the quantities that carry it: text, booleans and signs verbatim;
    numbers at the printed precision. A quantity named ``... | pearson`` or ``... | spearman`` (the
    values, not the signs) belongs to the numeric tables, not to the verdict on the signs.
    """
    rows = []
    for label, prefixes in CONCLUSIONS:
        sel = table[table["quantity"].str.startswith(prefixes)]
        if "tension" in prefixes[0]:
            sel = sel[sel["quantity"].str.endswith("sign")]
        if "predict" in prefixes[0]:
            sel = sel[sel["quantity"].str.endswith("outcome")]
        if "tau" in prefixes[0]:
            sel = sel[sel["quantity"].str.contains("tau selected")]
        if "certificate" in prefixes[0]:
            sel = sel[sel["quantity"].str.endswith("| status")]
        bad = sel[sel["printed change"]]
        rows.append({
            "conclusion": label,
            "quantities checked": len(sel),
            "identical": bool(len(bad) == 0 and len(sel) > 0),
            "differing": list(bad["quantity"]),
        })  # fmt: skip
    return pd.DataFrame(rows)


# -- the compact results file the paper reads ----------------------------------------------------
SUMMARY_FILE = lg.REPO_ROOT / "examples" / "adcs" / "experiments" / "reports" / "sensitivity.json"
SIGNIFICANT = 10  # digits kept in the file, so that it is deterministic across platforms


def _round(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return x
    if isinstance(x, float) and (math.isnan(x) or x == 0.0):
        return x
    return float(f"{x:.{SIGNIFICANT}g}") if isinstance(x, float) else x


def summarise(committed: Mapping, runs: Mapping[str, Mapping]) -> dict:
    """The compact record the paper reads: seeds, perturbation, and per quantity the range.

    Every numeric quantity carries the committed value and the ``min`` and ``max`` over the
    regenerations *and* the committed value (the range a reader would see across the six
    datasets); text and truth values carry only ``identical`` (equal in every run). Values are
    rounded to :data:`SIGNIFICANT` digits and keys are sorted, so the file is deterministic.

    >>> r = summarise({"a | x": 1.0, "a | s": "u"}, {"1": {"a | x": 2.0, "a | s": "u"}})
    >>> r["quantities"]["a | x"], r["quantities"]["a | s"]
    ({'committed': 1.0, 'min': 1.0, 'max': 2.0, 'identical': False}, {'identical': True})
    """
    table = compare_runs(committed, runs)
    out = {}
    for _, r in table.iterrows():
        if r["numeric"]:
            lo, hi = min(r["min"], r["committed"]), max(r["max"], r["committed"])
            out[r["quantity"]] = {
                "committed": _round(r["committed"]),
                "min": _round(lo),
                "max": _round(hi),
                "identical": bool(r["identical"]),
            }
        else:
            out[r["quantity"]] = {"identical": bool(r["identical"])}
    return {
        "perturbation": {
            "relative_half_width": EPS,
            "variables": list(PERTURBED),
            "distribution": "uniform per design and variable, numpy.random.default_rng(seed)",
        },
        "seeds": [int(k) for k in runs],
        "quantities": dict(sorted(out.items())),
    }


def write_summary(path: Path, committed: Mapping, runs: Mapping[str, Mapping]) -> dict:
    """Write :func:`summarise` as JSON (sorted keys, two-space indent); return the record."""
    record = summarise(committed, runs)
    guard(path).write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    return record


# -- the report ---------------------------------------------------------------------------------
def _md(headers, rows) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |" for r in rows]
    return "\n".join(out)


def _g(x, fmt=".4g") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "nan" if x is not None else ""
    return format(x, fmt) if isinstance(x, (int, float)) and not isinstance(x, bool) else str(x)


def _range_row(r: Mapping, n: int) -> list:
    num = bool(r["numeric"])
    return [
        r["quantity"].split(" | ", 1)[1],
        _g(r["committed"]),
        _g(r["min"]) if num else "-",
        _g(r["max"]) if num else "-",
        f"{r['runs equal']}/{n}",
        "YES" if r["printed change"] else "no",
    ]


def _headline(name: str) -> bool:
    """Quantities shown in full when they change: sentences, regime table, nondominated counts."""
    return name.startswith(("sentence |", "regime |", "nondominated |", "predict |")) or (
        name.startswith(("contending |", "leading |", "tau |"))
    )


def _deviation_section(runs_dirs: Mapping[int, Path], committed_dir: Path) -> list[str]:
    lines = ["### Deviation of the attributes from the committed data", ""]
    for f, title in (
        (PRIMARY_FILE, "Primary (1000 designs)"),
        (BASELINE_FILE, "Baseline (1000 designs)"),
        (CHECKS_FILE, "Check designs (6)"),
    ):
        com = pd.read_csv(committed_dir / f)
        regs = {s: pd.read_csv(d / f) for s, d in runs_dirs.items()}
        devs = {s: column_deviation(t, com) for s, t in regs.items()}
        rows = []
        for c in ATTRIBUTE_NAMES:
            cells = [
                f"{devs[s].loc[c, 'max rel']:.1e} / {devs[s].loc[c, 'max abs']:.1e}" for s in devs
            ]
            rows.append([
                c, *cells,
                f"{max(devs[s].loc[c, 'max rel'] for s in devs):.1e}",
                f"{max(devs[s].loc[c, 'max abs'] for s in devs):.1e}",
            ])  # fmt: skip
        lines += [
            f"{title}: largest relative / absolute deviation from the committed file, per column "
            "and regeneration.", "",
            _md(["column", *[f"seed {s}" for s in devs], "max rel", "max abs"], rows), "",
        ]  # fmt: skip
        for col in ("settling_time_s",):
            moved = [
                f"seed {sd}: {int(((t[col] - com[col]).abs() > 0.5).sum())} of {len(t)}"
                for sd, t in regs.items()
            ]
            lines += [
                f"Designs whose `{col}` moved by more than 0.5 s: " + "; ".join(moved) + ".",
                "",
            ]
        diffs = [
            f"seed {s}: {d['flag cells changed']} flag cells, {d['feasible designs changed']} "
            f"feasibility verdicts, {d['label cells changed']} label cells"
            for s, d in ((s, table_differences(t, com)) for s, t in regs.items())
        ]
        lines += ["Changed against the committed file: " + "; ".join(diffs) + ".", ""]
    return lines


def report(
    out_dir: Path | str,
    committed_dir: Path | str,
    runtime_s: float | None = None,
    json_path: Path | str | None = None,
) -> str:
    """The generated section of ``swap-evidence.md`` from the regenerations in ``out_dir``.

    With ``json_path``, also writes the compact results file the paper reads
    (:func:`write_summary`).
    """
    out_dir, committed_dir = Path(out_dir), Path(committed_dir)
    runs_dirs = {
        s: out_dir / f"seed{s}" for s in SEEDS if (out_dir / f"seed{s}" / CHECKS_FILE).exists()
    }
    cache = out_dir / "quantities.json"
    qs = json.loads(cache.read_text()) if cache.exists() else {}
    if "committed" not in qs:
        qs["committed"] = quantities(committed_dir)
    for s, d in runs_dirs.items():
        if f"seed{s}" not in qs:
            qs[f"seed{s}"] = quantities(d)
        cache.write_text(json.dumps(qs))
    runs = {str(s): qs[f"seed{s}"] for s in runs_dirs}
    if json_path:
        write_summary(Path(json_path), qs["committed"], runs)
    table = compare_runs(qs["committed"], runs)
    ver = verdicts(table)
    n = len(runs_dirs)
    lines = ["## Sensitivity of the conclusions to the step-quantized times", ""]
    lines += [
        "Generated by `examples/adcs/experiments/sensitivity.py` (WP16 Amendment 1, D-6); "
        "no Docker.", "",
        "**Method.** Each of the two cubesat datasets (primary, aggressive gain box; baseline, "
        "stock gain box) and the six check designs were regenerated "
        f"{n} times through the clean oracle (`CubesatOracle`; the sampler, design ids and seeds "
        "of the v2 generation; the same worker pool) with `Kp`, `Kd`, `panel_span_m` and "
        f"`battery_wh` of every design multiplied by `1 + e`, `e` uniform in [-{EPS:g}, {EPS:g}] "
        "per design and variable from `numpy.random.default_rng(seed)`, seeds "
        f"{', '.join(map(str, runs_dirs))}. The regenerated files were written to a scratch "
        "directory (never `examples/adcs/data`, never the ledger). For each regeneration "
        "`case.py` was run as the paper runs it: the one-term fit with the temperature "
        "re-selected, the K = 2 and K = 3 fits (`spec.seed`), the regime comparison, the "
        "nondominated counts, the candidates and propose-predict-check (the regressor refit on "
        "the regenerated primary data; the recorded predictions; the check designs regenerated "
        "with the same kind of perturbation, and, as a second reading, the committed check "
        "measurements). Every table of Appendix D and every generated sentence of the case "
        "sections was computed, and each quantity is compared at the precision the paper prints "
        "it (tables at four significant digits, temperatures at one decimal, sentences "
        "verbatim). The facets of K = 2 and K = 3 are compared as labelled and, separately, as "
        "an unlabelled set.", "",
    ]  # fmt: skip
    if runtime_s is not None:
        lines += [f"Run time of the regenerations on this Mac: {runtime_s / 60:.0f} minutes.", ""]
    lines += ["### Verdict on the conclusions", ""]
    ok = bool(ver["identical"].all())
    lines += [
        "**Every listed conclusion is identical across the regenerations and to the committed "
        "data.**" if ok else
        "**NOT IDENTICAL: at least one listed conclusion differs; see the rows below.**", "",
        _md(
            ["conclusion", "quantities compared", f"across {n} regenerations and committed"],
            [[r["conclusion"], r["quantities checked"],
              "IDENTICAL" if r["identical"] else "NOT IDENTICAL: " + "; ".join(r["differing"])]
             for _, r in ver.iterrows()],
        ), "",
    ]  # fmt: skip
    shown = [q for q in table.loc[table["printed change"], "quantity"] if _headline(q)]
    if shown:
        lines += [
            "### Headline quantities that print differently",
            "",
            "The committed value and each regeneration's value, for the quantities of the "
            "verdict, the nondominated counts and the paper's generated sentences that change "
            "at the printed precision.",
            "",
            _md(
                ["quantity", "committed", *[f"seed {s}" for s in runs_dirs]],
                [
                    [q, _g(qs["committed"][q]), *[_g(qs[f"seed{s}"][q]) for s in runs_dirs]]
                    for q in shown
                ],
            ),
            "",
        ]
    lines += _deviation_section(runs_dirs, committed_dir)
    lines += [
        "### Every quantity the paper reports", "",
        f"Per quantity: the committed value, the minimum and maximum over the {n} regenerations "
        "(numbers; `-` for text and truth values), how many regenerations print the same as the "
        "committed value, and whether anything changes at the printed precision.", "",
    ]  # fmt: skip
    for g in dict.fromkeys(q.split(" | ")[0] for q in table["quantity"]):
        sub = table[table["quantity"].str.startswith(g + " | ")]
        body = [_range_row(r, n) for _, r in sub.iterrows()]
        lines += [f"#### {g}", "",
                  _md(["quantity", "committed", "min", "max", "regenerations printing as committed",
                       "changes at printed precision"], body), ""]  # fmt: skip
    changed = table[table["printed change"]]
    lines += [f"Quantities compared: {len(table)}; changing at the printed precision: "
              f"{len(changed)}.", ""]  # fmt: skip
    if len(changed):
        lines += [
            "Those that change: " + "; ".join(f"`{q}`" for q in changed["quantity"]) + ".",
            "",
        ]
    return "\n".join(lines)


# -- command line -------------------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="sensitivity", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser(
        "regenerate", help="regenerate the datasets for the seeds into a scratch dir"
    )
    g.add_argument("--out", type=Path, required=True)
    g.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    g.add_argument("--workers", type=int, default=None)
    g.add_argument("--n", type=int, default=None, help="first n designs only (a quick check)")
    a = sub.add_parser("analyse", help="run the paper's computations on each regeneration; report")
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--md", type=Path, default=None, help="write the generated section here")
    a.add_argument("--runtime-s", type=float, default=None)
    a.add_argument("--committed", type=Path, default=V2_DATA)
    a.add_argument(
        "--json",
        type=Path,
        default=None,
        help=f"write the compact results file (paper reads {SUMMARY_FILE.name})",
    )
    args = p.parse_args(argv)
    if args.cmd == "regenerate":
        out = guard(args.out)
        t0 = time.time()
        for s in args.seeds:
            t = time.time()
            d = regenerate(out, s, args.workers, args.n)
            print(f"seed {s}: {d} in {(time.time() - t) / 60:.1f} min", flush=True)
        print(f"total {(time.time() - t0) / 60:.1f} min")
        return 0
    out = guard(args.out)
    md = guard(args.md) if args.md else None
    text = report(out, args.committed, args.runtime_s, args.json)
    if md:
        md.write_text(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
