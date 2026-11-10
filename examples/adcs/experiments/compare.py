"""The v1 to v2 comparison report (WP15 15.4, R-15): a report, not a pin.

``uv run python -m experiments compare`` (``PYTHONPATH=examples/adcs`` outside pytest) writes
``experiments/reports/v1-v2-comparison.md``. Per dataset it reports the shared and differing
columns; the agreement of design ids, seeds, categorical values and flags; the maximum relative
difference per column on the shared design ids; quantiles and flag shares side by side. It adds
the swap checklist (the files that read the frozen CSVs, from a grep), the WP4b richness
conditions (a) to (e) on both generations (reported, no pass requirement) and the solver's
exclusion summary from the ledger. The hand-written ``reports/change-register.md`` is included
verbatim; this module never writes it. The columns the two generations do not share (the frozen
slew-time columns, which v2 lost with WP23 G5) are reported per dataset as differing columns.

The difference ids (``<dataset>:<column>``, ``<dataset>:share[<flag>]``,
``<dataset>:median[<column>]``, ``<dataset>:ids``, ``<dataset>:columns``) are what the register's
"covers" cells name: ``exceeded_differences`` lists those whose difference exceeds the
reproducibility tolerance, and ``tests/test_v2_data.py`` requires the register to cover exactly
that set.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from . import ledger as lg

ADCS = "examples/adcs"
DATASETS = {
    "primary": "adcs_designs_cubesat_gains.csv",
    "baseline": "adcs_designs_cubesat.csv",
    "check_predictions": "check_predictions_cubesat.csv",
    "check_designs": "check_designs_cubesat.csv",
}
FROZEN_ENTRY = {
    "primary": "adopted-adcs_designs_cubesat_gains",
    "baseline": "adopted-adcs_designs_cubesat",
    "check_predictions": "adopted-check_predictions_cubesat",
    "check_designs": "adopted-check_designs_cubesat",
}
V2_ENTRY = {
    "primary": "v2-primary",
    "baseline": "v2-baseline",
    "check_predictions": "v2-check-predictions",
    "check_designs": "v2-check-designs",
}
IDENTITY = ("design_id", "seed", "wheel_class", "st_grade", "role", "name")
FLAGS = ("settled", "momentum_ok", "power_ok", "dod_ok")
# the time column read off an adaptive integration (one since WP23 G5: the settling time)
TIME_COLUMNS = ("settling_time_s",)
SATURATION = "torque_saturated_frac"
SHARE_TOL = 0.01  # a flag share moving by more than this (absolute) is a difference
# the aggressive-box reproducibility test (WP4b), used where a frozen entry records no tolerance
DEFAULT_TOL = {"rtol": 1e-3, "atol": 1e-6, "time_atol": 0.5, "sat_rtol": 1e-1, "sat_atol": 1e-12}
REGISTER = "change-register.md"
REPORT = "v1-v2-comparison.md"
FROZEN_FILES = re.compile(
    r"adcs_designs(?:_cubesat(?:_gains)?)?\.csv|check_(?:designs|predictions)_cubesat\.csv"
)


def paths(root: Path) -> dict[str, Path]:
    base = Path(root) / ADCS
    return {
        "frozen": base / "data",
        "v2": base / "data" / "v2",
        "reports": base / "experiments" / "reports",
        "ledger": base / "experiments" / "ledger" / "ledger.jsonl",
    }


def tolerances(entries: list[dict], dataset: str) -> dict:
    """Reproducibility tolerances of a dataset: its adopted entry's, else the aggressive box's."""
    e = lg.find(entries, FROZEN_ENTRY[dataset])
    t = (e or {}).get("inputs", {}).get("tolerances", {})
    if "continuous_rtol" not in t:
        return dict(DEFAULT_TOL)
    return {
        "rtol": t["continuous_rtol"],
        "atol": t.get("continuous_atol", DEFAULT_TOL["atol"]),
        "time_atol": t.get("time_columns_atol", DEFAULT_TOL["time_atol"]),
        "sat_rtol": t.get("torque_saturated_frac_rtol", DEFAULT_TOL["sat_rtol"]),
        "sat_atol": DEFAULT_TOL["sat_atol"],
    }


def _close(column: str, a: np.ndarray, b: np.ndarray, tol: dict) -> np.ndarray:
    """Elementwise: do ``a`` and ``b`` agree within the tolerance that covers ``column``?"""
    if column in TIME_COLUMNS:
        return np.abs(a - b) <= tol["time_atol"]
    if column == SATURATION:
        return np.isclose(a, b, rtol=tol["sat_rtol"], atol=tol["sat_atol"])
    return np.isclose(a, b, rtol=tol["rtol"], atol=tol["atol"])


def _symmetric_rel(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    denom = np.maximum(np.maximum(np.abs(a), np.abs(b)), 1e-300)
    return np.abs(a - b) / denom


@dataclass
class ColumnStat:
    column: str
    kind: str  # "value" or "exact"
    max_rel: float = 0.0
    worst_id: int | None = None
    n_differ: int = 0  # rows outside the tolerance (value) or unequal (exact)
    exceeds: bool = False
    q1: tuple = ()
    q2: tuple = ()


@dataclass
class DatasetComparison:
    name: str
    present: bool
    n1: int = 0
    n2: int = 0
    shared_columns: list = field(default_factory=list)
    only_v1: list = field(default_factory=list)
    only_v2: list = field(default_factory=list)
    order_equal: bool = True
    ids_equal: bool = True
    n_shared_ids: int = 0
    stats: list = field(default_factory=list)
    flag_rows: list = field(default_factory=list)  # (flag, share v1, share v2, rows differ)
    exceeded: list = field(default_factory=list)
    tol: dict = field(default_factory=dict)


def compare_dataset(name: str, v1: pd.DataFrame, v2: pd.DataFrame, tol: dict) -> DatasetComparison:
    """Compare a frozen and a v2 frame of one dataset on their shared design ids."""
    out = DatasetComparison(name, True, len(v1), len(v2), tol=tol)
    c1, c2 = list(v1.columns), list(v2.columns)
    out.shared_columns = [c for c in c1 if c in c2]
    out.only_v1 = [c for c in c1 if c not in c2]
    out.only_v2 = [c for c in c2 if c not in c1]
    out.order_equal = c1 == c2
    if out.only_v1 or out.only_v2:
        out.exceeded.append(f"{name}:columns")
    ids1, ids2 = set(v1["design_id"]), set(v2["design_id"])
    out.ids_equal = ids1 == ids2
    if not out.ids_equal:
        out.exceeded.append(f"{name}:ids")
    shared = sorted(ids1 & ids2)
    out.n_shared_ids = len(shared)
    a = v1.set_index("design_id").loc[shared]
    b = v2.set_index("design_id").loc[shared]
    for col in out.shared_columns:
        if col == "design_id":
            continue
        x, y = a[col], b[col]
        numeric = pd.api.types.is_numeric_dtype(x) and x.dtype != bool
        s = ColumnStat(col, "value" if numeric else "exact")
        if numeric:
            xv, yv = x.to_numpy(float), y.to_numpy(float)
            rel = _symmetric_rel(xv, yv)
            ok = _close(col, xv, yv, tol) if col not in IDENTITY else xv == yv
            s.max_rel = float(rel.max()) if len(rel) else 0.0
            s.worst_id = int(shared[int(np.argmax(rel))]) if len(rel) else None
            s.n_differ = int((~ok).sum())
            s.q1 = tuple(np.quantile(xv, [0.05, 0.5, 0.95])) if len(xv) else ()
            s.q2 = tuple(np.quantile(yv, [0.05, 0.5, 0.95])) if len(yv) else ()
            xm, ym = np.median(xv), np.median(yv)
            if col not in IDENTITY and not _close(col, np.array([xm]), np.array([ym]), tol)[0]:
                out.exceeded.append(f"{name}:median[{col}]")
        else:
            s.n_differ = int((x.to_numpy() != y.to_numpy()).sum())
            if x.dtype == bool:
                s.kind = "flag"
                out.flag_rows.append((col, float(x.mean()), float(y.mean()), s.n_differ))
                if abs(float(x.mean()) - float(y.mean())) > SHARE_TOL:
                    out.exceeded.append(f"{name}:share[{col}]")
        s.exceeds = s.n_differ > 0
        if s.exceeds:
            out.exceeded.append(f"{name}:{col}")
        out.stats.append(s)
    out.exceeded = sorted(dict.fromkeys(out.exceeded))
    return out


def load(root: Path) -> dict[str, DatasetComparison]:
    """Compare every dataset whose v2 file exists."""
    p = paths(root)
    entries = lg.read(p["ledger"])
    result = {}
    for name, fname in DATASETS.items():
        f1, f2 = p["frozen"] / fname, p["v2"] / fname
        if not f2.exists():
            result[name] = DatasetComparison(name, False)
            continue
        result[name] = compare_dataset(
            name, pd.read_csv(f1), pd.read_csv(f2), tolerances(entries, name)
        )
    return result


def exceeded_differences(root: Path = lg.REPO_ROOT) -> dict[str, list[str]]:
    """``{dataset: [difference ids beyond tolerance]}`` for the datasets that exist in v2."""
    return {n: c.exceeded for n, c in load(Path(root)).items() if c.present}


def register_rows(register: Path) -> list[dict]:
    """Rows of the change register's table: ``{"n", "what", "why", "covers", "moves"}``."""
    rows = []
    if not Path(register).exists():
        return rows
    for line in Path(register).read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or not re.fullmatch(r"CR-\d+", cells[0]):
            continue
        covers = re.findall(r"`([^`]+)`", cells[3])
        rows.append(
            {"n": cells[0], "what": cells[1], "why": cells[2], "covers": covers, "moves": cells[4]}
        )
    return rows


def check_register(exceeded: dict[str, list[str]], rows: list[dict]) -> tuple[list[str], list[str]]:
    """``(unexplained, stale)``: differences beyond tolerance no row covers, and register rows
    that cover no difference (or name one that does not exist). Equality is not required."""
    every = {i for ids in exceeded.values() for i in ids}
    covered = {i for r in rows for i in r["covers"]}
    unexplained = sorted(every - covered)
    stale = sorted(r["n"] for r in rows if not r["covers"] or set(r["covers"]) - every)
    return unexplained, stale


# -- the swap checklist --------------------------------------------------------------------------
def frozen_consumers(root: Path) -> dict[str, list[str]]:
    """``{file: [frozen CSV names it mentions]}`` over the tracked text files (a grep)."""
    root = Path(root)
    try:
        listing = subprocess.run(
            ["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        listing = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    skip = (f"{ADCS}/experiments/reports/", f"{ADCS}/experiments/ledger/", f"{ADCS}/data/")
    hits: dict[str, list[str]] = {}
    for rel in listing:
        if rel.startswith(skip) or rel.endswith((".png", ".csv", ".lock", ".pdf", ".svg")):
            continue
        try:
            text = (root / rel).read_text()
        except (UnicodeDecodeError, OSError):
            continue
        names = sorted(set(FROZEN_FILES.findall(text)))
        if names:
            hits[rel] = names
    return dict(sorted(hits.items()))


# -- the richness conditions (WP4b R-13 (a) to (e), R-14) ----------------------------------------
# eclipse_reserve_wh stays in ORIENTATION and POWER: the frozen v1 frames this report reads carry it
# (the data of record has eight metrics without it, WP23 close-out).
ORIENTATION = {
    "settling_time_s": -1,
    "pointing_error_deg": -1,
    "total_mass_kg": -1,
    "control_effort": -1,
    "peak_slew_power_w": -1,
    "dod_eclipse": -1,
    "power_margin_w": +1,
    "energy_balance_wh": +1,
    "eclipse_reserve_wh": +1,
}
POWER = (
    "power_margin_w",
    "energy_balance_wh",
    "eclipse_reserve_wh",
    "peak_slew_power_w",
    "dod_eclipse",
)
SUPPORT_TOL = 1e-3
TARGET_FRAC_ABOVE = 0.10


def richness(
    df: pd.DataFrame, seed: int = 0, n_boot: int = 100, attrs: list[str] | None = None
) -> dict:
    """The hand version of the WP4b probe on a cubesat frame (as ``tests/test_adcs_enrichment``).

    ``attrs`` are the attributes read (default: those of ``ORIENTATION`` the frame carries); the
    report passes the attributes both frames carry, so the frozen and the v2 frames are read on
    one metric set (the eclipse reserve left the v2 data at the WP23 close-out). The feasible rows
    pass the four flags (``dod_ok`` with them since the close-out; on the frozen frames it removes
    exactly the rows the reserve's positivity removed) and have every attribute positive.
    """
    from hyperbolic_trade_space import HyperbolicTradeSpace
    from hyperbolic_trade_space import solvers as S

    attrs = [a for a in ORIENTATION if a in df.columns] if attrs is None else list(attrs)
    power = [a for a in POWER if a in attrs]
    ok = df.settled & df.power_ok & df.momentum_ok & df.dod_ok & (df[attrs] > 0).all(axis=1)
    f = df[ok].reset_index(drop=True)
    U = np.column_stack([ORIENTATION[a] * np.log(f[a].to_numpy(float)) for a in attrs])
    U = (U - U.mean(axis=0)) / U.std(axis=0)
    w_inf = dict(zip(attrs, S.solve_lp(U, 0.0).w, strict=True))
    X = np.exp(U)
    lo, hi, best = np.log(1.0), np.log(1000.0), None
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        hts = HyperbolicTradeSpace(temperature=float(np.exp(mid))).fit(X)
        gap = abs(hts.frac_above_ - TARGET_FRAC_ABOVE)
        if best is None or gap < best[0]:
            best = (gap, hts)
        lo, hi = (mid, hi) if hts.frac_above_ > TARGET_FRAC_ABOVE else (lo, mid)
        if gap < 0.002:
            break
    hts = best[1]
    near = np.abs(hts.training_log_v_) < 1.0 / float(hts.temperature)
    assoc = pd.DataFrame(np.corrcoef(U[near].T), index=attrs, columns=attrs)
    rng = np.random.default_rng(seed)
    boots = np.array([S.solve_lp(U[rng.integers(0, len(U), len(U))], 0.0).w for _ in range(n_boot)])
    j = {a: attrs.index(a) for a in attrs}
    frac = {a: float((boots[:, j[a]] > SUPPORT_TOL).mean()) for a in attrs}
    med = {a: float(np.median(boots[:, j[a]])) for a in attrs}
    wheel_near = f.loc[near, "wheel_class"].value_counts().to_dict()
    sat = f.groupby("wheel_class")[SATURATION].median()
    tim = f.groupby("wheel_class")["settling_time_s"].median()
    pairs = {
        (p, q): float(assoc.loc[p, q])
        for p in power
        for q in attrs
        if p != q and (q not in power or attrs.index(p) < attrs.index(q))
    }
    a = assoc
    conditions = {
        "a": (
            len([x for x in attrs if w_inf[x] > SUPPORT_TOL]) >= 3
            and w_inf["total_mass_kg"] >= 0.05
            and max(w_inf[x] for x in power) >= 0.05
        ),
        "b": (
            frac["total_mass_kg"] >= 0.90
            and med["total_mass_kg"] >= 0.05
            and any(frac[x] >= 0.90 and med[x] >= 0.05 for x in power)
        ),
        "c": (
            a.loc["settling_time_s", "total_mass_kg"] <= -0.30
            and len([w for w, c in wheel_near.items() if c >= 10]) >= 2
        ),
        "d": min(pairs.values()) <= -0.30,
        "e": (
            a.loc["settling_time_s", "control_effort"] <= -0.30
            and a.loc["pointing_error_deg", "control_effort"] <= -0.30
            and a.loc["pointing_error_deg", "total_mass_kg"] <= -0.30
            and a.loc["settling_time_s", "pointing_error_deg"] >= 0.0
        ),
        "R-14": bool(sat["small"] >= 3 * sat["large"] and tim["small"] >= 1.25 * tim["large"]),
    }
    return {
        "n_feasible": len(f),
        "tau": float(hts.temperature),
        "frac_above": float(hts.frac_above_),
        "n_near": int(near.sum()),
        "w_inf": w_inf,
        "contending": [x for x in attrs if w_inf[x] > SUPPORT_TOL],
        "frac": frac,
        "med": med,
        "wheel_near": wheel_near,
        "settling_mass": float(a.loc["settling_time_s", "total_mass_kg"]),
        "power_pair": min(pairs.items(), key=lambda kv: kv[1]),
        "settling_effort": float(a.loc["settling_time_s", "control_effort"]),
        "pointing_effort": float(a.loc["pointing_error_deg", "control_effort"]),
        "pointing_mass": float(a.loc["pointing_error_deg", "total_mass_kg"]),
        "settling_pointing": float(a.loc["settling_time_s", "pointing_error_deg"]),
        "sat_ratio": float(sat["small"] / sat["large"]) if sat["large"] > 0 else float("inf"),
        "settling_ratio": float(tim["small"] / tim["large"]),
        "conditions": conditions,
        "attrs": attrs,
    }


# -- the report ----------------------------------------------------------------------------------
def _fmt(x, digits: int = 4) -> str:
    if x is None:
        return "-"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    return f"{x:.{digits}g}"


def _table(header: list[str], rows: list[list]) -> list[str]:
    lines = ["", "| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return [*lines, ""]


def _dataset_section(c: DatasetComparison) -> list[str]:
    title = f"### {c.name} (`{DATASETS[c.name]}`)"
    if not c.present:
        return [title, "", "No v2 file yet.", ""]
    L = [title, ""]
    L.append(
        f"Rows: frozen {c.n1}, v2 {c.n2}; shared design ids {c.n_shared_ids}; design ids "
        f"{'agree' if c.ids_equal else 'DIFFER'}; columns "
        f"{'equal, same order' if c.order_equal and not c.only_v1 and not c.only_v2 else 'differ'}"
        f" ({len(c.shared_columns)} shared; only frozen: {c.only_v1 or 'none'}; "
        f"only v2: {c.only_v2 or 'none'})."
    )
    t = c.tol
    L.append(
        f"Tolerances (reproducibility test of the frozen file): rtol {t['rtol']:g}, atol "
        f"{t['atol']:g}; times within {t['time_atol']:g} s; saturated fraction rtol "
        f"{t['sat_rtol']:g}."
    )
    L.append("")
    exact = [s for s in c.stats if s.kind == "exact"]
    if exact:
        L.append("Identity and categorical columns (rows unequal on the shared ids):")
        L += _table(["column", "rows unequal"], [[s.column, s.n_differ] for s in exact])
    if c.flag_rows:
        L.append("Flag shares (share True) and rows where the flag differs:")
        L += _table(
            ["flag", "frozen", "v2", "rows differ"],
            [[f, _fmt(a), _fmt(b), n] for f, a, b, n in c.flag_rows],
        )
    vals = [s for s in c.stats if s.kind == "value" and s.column not in IDENTITY]
    if vals:
        L.append(
            "Numeric columns on the shared design ids: maximum symmetric relative difference "
            "(at design id), rows outside tolerance, and the quantiles 5 %, 50 %, 95 % of each "
            "generation."
        )
        L += _table(
            ["column", "max rel diff", "at id", "rows outside tol", "frozen q05/q50/q95",
             "v2 q05/q50/q95"],
            [
                [
                    s.column,
                    _fmt(s.max_rel, 3),
                    _fmt(s.worst_id),
                    s.n_differ,
                    "/".join(_fmt(v, 4) for v in s.q1),
                    "/".join(_fmt(v, 4) for v in s.q2),
                ]
                for s in vals
            ],
        )  # fmt: skip
    L.append(
        "Differences beyond tolerance (ids for the change register): "
        + (", ".join(f"`{i}`" for i in c.exceeded) if c.exceeded else "none")
        + "."
    )
    L.append("")
    return L


def _richness_section(frozen: dict, v2: dict) -> list[str]:
    L = [
        "WP4b R-13 conditions (a) to (e) and R-14 on the feasible designs (settled, power_ok, "
        "momentum_ok, dod_ok, every attribute positive), read on the attributes both frames carry "
        "(eight since the eclipse reserve left the v2 data), conditioned by hand as in the probe, "
        "`HyperbolicTradeSpace` at tau = infinity and at the working tau (frac above about 0.10); "
        "100 bootstrap resamples, seed 0. Reported; no pass is required of v2.",
        "",
    ]
    names = {
        "a": "(a) contending set at tau = inf: size >= 3, mass and a power attribute >= 0.05",
        "b": "(b) bootstrap support of mass and a power attribute >= 90 %, median >= 0.05",
        "c": "(c) settling time against mass <= -0.30; >= 2 wheel classes with >= 10 near rows",
        "d": "(d) a power or energy tension <= -0.30",
        "e": "(e) settling-effort, pointing-effort, pointing-mass <= -0.30; settling-pointing >= 0",
        "R-14": "R-14 torque binds: saturation ratio small/large >= 3, settling ratio >= 1.25",
    }
    for regime in ("primary", "baseline"):
        if regime not in v2:
            continue
        a, b = frozen[regime], v2[regime]
        L.append(f"#### {regime} regime")
        L.append("")
        rows = []
        for k, text in names.items():
            rows.append(
                [
                    text,
                    "pass" if a["conditions"][k] else "fail",
                    "pass" if b["conditions"][k] else "fail",
                ]
            )
        L += _table(["condition", "frozen", "v2"], rows)
        keys = [
            ("feasible designs", "n_feasible"),
            ("working tau", "tau"),
            ("frac above", "frac_above"),
            ("near-frontier rows", "n_near"),
            ("settling-mass association", "settling_mass"),
            ("settling-effort", "settling_effort"),
            ("pointing-effort", "pointing_effort"),
            ("pointing-mass", "pointing_mass"),
            ("settling-pointing", "settling_pointing"),
            ("saturation ratio small/large", "sat_ratio"),
            ("settling ratio small/large", "settling_ratio"),
        ]
        L += _table(
            ["quantity", "frozen", "v2"], [[n, _fmt(a[k], 4), _fmt(b[k], 4)] for n, k in keys]
        )
        L += _table(
            [
                "attribute",
                "exponent at tau = inf (frozen)",
                "(v2)",
                "bootstrap support (frozen)",
                "(v2)",
            ],
            [
                [
                    x,
                    _fmt(a["w_inf"][x], 3),
                    _fmt(b["w_inf"][x], 3),
                    _fmt(a["frac"][x], 2),
                    _fmt(b["frac"][x], 2),
                ]
                for x in b["attrs"]
            ],
        )
        L.append(
            f"Strongest power or energy tension (near-frontier association): frozen "
            f"{a['power_pair'][0][0]} with {a['power_pair'][0][1]} ({a['power_pair'][1]:.3f}); v2 "
            f"{b['power_pair'][0][0]} with {b['power_pair'][0][1]} ({b['power_pair'][1]:.3f}). "
            f"Wheel classes among near-frontier rows: frozen {a['wheel_near']}; "
            f"v2 {b['wheel_near']}."
        )
        L.append("")
    return L


def _exclusion_section(entries: list[dict]) -> list[str]:
    L = [
        "The solver (engine `solve`, z3) classifies the regions of each v2 experiment's declared "
        "ranges before any design is simulated (`experiments/exclusion.py`); a region proved "
        "infeasible is excluded, any other is kept, and the four flags are then observations of "
        "the measured slew. The classification is stored in each entry's `inputs.exclusion`.",
        "",
    ]
    rows = []
    for e in entries:
        ex = e.get("inputs", {}).get("exclusion")
        if e["kind"] != "generated" or not ex:
            continue
        v = ex["verdicts"]
        rows.append(
            [
                e["id"],
                v.get("design-space power", "-"),
                v.get("design-space battery", "-"),
                ", ".join(ex["excluded_regions"]) or "none",
                ex["variant_excluded"],
            ]
        )
    if not rows:
        return [*L, "No v2 entry records an exclusion block yet.", ""]
    L += _table(
        ["entry", "power region", "battery region", "excluded regions", "variant excluded"], rows
    )
    shown = next(
        e["inputs"]["exclusion"]
        for e in entries
        if e["kind"] == "generated" and e.get("inputs", {}).get("exclusion")
    )
    for r in shown["regions"]:
        box = ", ".join(f"{k} in [{v[0]:g}, {v[1]:g}]" for k, v in r["region"]["box"].items())
        L.append(
            f"- `{r['region']['name']}` ({r['basis']}): {r['verdict']}; {box}. {r['reason']}. "
            f"Witness of a violation: {r['witness_violation'] or 'none'}."
        )
    kept = sorted(set(shown["verdicts"].values()))
    L += [
        "",
        f"Result: the solver's verdicts on the declared ranges are {', '.join(kept)}; "
        f"{len(shown['excluded_regions'])} region(s) excluded"
        + (
            ", so every design of each dataset is simulated and the flags are observations. "
            "The standard space is not decided by the solver: the battery region is mixed "
            "(capacities below the eclipse base load floor fail the depth of discharge, the rest "
            "depend on the slew loss energy)."
            if not shown["excluded_regions"]
            else "; the designs in them are not simulated."
        )
        + " The agreement of observation with verdict is tested on excluded sub-regions "
        "(`tests/test_cubesat_oracle.py`): a battery region of 20 to 26 Wh is proved infeasible "
        "and every design sampled in it simulates `dod_ok` False.",
        "",
    ]
    return L


def _entries_section(entries: list[dict]) -> list[str]:
    rows = []
    gone = lg.superseded_by(entries)
    for e in entries:
        if not e["id"].startswith("v2-"):
            continue
        rows.append(
            [
                e["id"],
                f"superseded by {gone[e['id']]}" if e["id"] in gone else "current",
                e["time_utc"],
                e["output_rows"],
                e["output_sha256"][:12],
                e["git_commit"][:7],
                e["git_dirty"],
                e["platform"],
            ]
        )
    return _table(
        ["entry", "status", "time (UTC)", "rows", "sha256", "commit", "dirty", "platform"], rows
    )


def build_report(root: Path) -> str:
    root = Path(root)
    p = paths(root)
    entries = lg.read(p["ledger"])
    comps = load(root)
    L = [
        "# Comparison of the frozen generation and v2",
        "",
        "Generated by `PYTHONPATH=examples/adcs uv run python -m experiments compare`; do not edit "
        "(the change register is hand-written in `change-register.md` and included below). "
        "The frozen files under `examples/adcs/data/` are never rewritten; v2 lives in "
        "`examples/adcs/data/v2/` with the same file names and column order. The geostationary "
        "file `adcs_designs.csv` has no v2 (OD1: retired to the record, frozen and runnable).",
        "",
        "## Ledger entries of the v2 generation",
        "",
    ]
    L += _entries_section(entries)
    L += ["## Per dataset", ""]
    for c in comps.values():
        L += _dataset_section(c)
    cd = comps["check_designs"]
    if cd.present:
        p1 = pd.read_csv(p["frozen"] / DATASETS["check_designs"])
        p2 = pd.read_csv(p["v2"] / DATASETS["check_designs"])
        cfg = ["panel_span_m", "battery_wh", "Kp", "Kd", "wheel_class", "st_grade"]
        m = p1.merge(p2, on="design_id", suffixes=("_1", "_2"))
        same = []
        for _, r in m[m["role_1"] == "proposal"].iterrows():
            same.append(
                all(
                    (r[f"{c}_1"] == r[f"{c}_2"])
                    if isinstance(r[f"{c}_1"], str)
                    else np.isclose(r[f"{c}_1"], r[f"{c}_2"], rtol=1e-6)
                    for c in cfg
                )
            )
        L += [
            "The three hand-written candidates are identical in both generations by "
            "construction. The three proposals are re-proposed from the v2 primary data: "
            f"{sum(same)} of {len(same)} coincide with the frozen proposals (configuration "
            "columns within 1e-6 relative).",
            "",
        ]
    L += ["## Swap checklist: files that read the frozen CSVs", ""]
    cons = frozen_consumers(root)
    own = (f"{ADCS}/experiments/", "tests/test_cubesat_oracle.py", "tests/test_v2_data.py")
    groups = {
        "Code and tests that read or cite the frozen files (re-point at the swap gate)": [
            f
            for f in cons
            if not f.startswith(("work-packages/", "docs/")) and not f.startswith(own)
        ],
        "Records and documentation that cite them": [
            f for f in cons if f.startswith(("work-packages/", "docs/"))
        ],
        "WP15's own files (they name the frozen files to compare, adopt or test)": [
            f for f in cons if f.startswith(own)
        ],
    }
    for title, files in groups.items():
        L += [f"**{title}** ({len(files)})", ""]
        L += _table(["file", "frozen files named"], [[f"`{f}`", ", ".join(cons[f])] for f in files])
    L += ["## Richness conditions on v2 (WP4b a to e)", ""]
    try:
        frozen_r, v2_r = {}, {}
        for regime in ("primary", "baseline"):
            f2 = p["v2"] / DATASETS[regime]
            if f2.exists():
                old, new = pd.read_csv(p["frozen"] / DATASETS[regime]), pd.read_csv(f2)
                both = [a for a in ORIENTATION if a in old.columns and a in new.columns]
                frozen_r[regime] = richness(old, attrs=both)
                v2_r[regime] = richness(new, attrs=both)
        L += _richness_section(frozen_r, v2_r)
    except ImportError as exc:
        L += [f"The estimator could not be imported ({exc}); not evaluated.", ""]
    L += ["## Exclusion by the solver", ""]
    L += _exclusion_section(lg.current(entries))
    L += ["## Change register", "", "<!-- change-register:begin -->"]
    reg = p["reports"] / REGISTER
    L += [reg.read_text().rstrip() if reg.exists() else "(change-register.md is not written yet)"]
    L += ["<!-- change-register:end -->", ""]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(L)) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="experiments compare", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=lg.REPO_ROOT)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)
    p = paths(a.root)
    out = a.out or p["reports"] / REPORT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_report(a.root))
    print(f"wrote {out}")
    return 0
