"""Richness acceptance of the committed cubesat dataset (WP4b, R-13, R-14, R-15).

The probe of ``docs/superpowers/notes/adcs-tensions-probe.md`` as tests: feasible designs only,
the ten attributes oriented (reciprocal for smaller-is-better, direct for larger-is-better),
logged and standardized by hand; ``HyperbolicTradeSpace`` fitted at tau = inf (``min_exponent = 0``)
and at the working tau (bisection to ``frac_above_`` about 0.10); near-frontier rows
``|log V| < 1/tau``; Pearson association of the oriented log-metrics (negative = tension).
No simulation: only the committed CSVs, a few seconds. The same R-13, R-14 and R-15 checks run on
each dataset of ``DATASETS`` (WP4b amendment 5): the 30 degree baseline, the baseline with the
momentum utilisation attribute (lever ii), the aggressive-gain dataset (lever i) and that with the
attribute (lever iii). Only the two utilisation datasets need the opensysml client, once, to read
the wheel capacities from the SysML model. The thresholds are those of the approved scope and are
not to be tuned.

Two regimes (WP4b decision, "Both, as two regimes"): the aggressive-gain datasets (``gains``,
``gains_headroom``) are PRIMARY and carry the R-13 assertions (a), (b), (c), (e). The baseline
datasets (``baseline``, ``headroom``) are the regime comparison: they assert the recorded numbers
(wheel class is a feasibility boundary only in that regime; mass absent or weak, agility-mass
associations above -0.30) in ``test_regime_*``. R-14, R-15, (d) and the tension-report agreement
run on all four.
"""

from __future__ import annotations

import os
import pathlib

import numpy as np
import pandas as pd
import pytest

from hyperbolic_trade_space import HyperbolicTradeSpace, tension_report
from hyperbolic_trade_space import solvers as S

DATA = pathlib.Path(__file__).resolve().parents[1] / "examples" / "adcs" / "data"
CSV = DATA / "adcs_designs_cubesat.csv"  # the 30 degree baseline (kept, never altered)
CSV_GAINS = DATA / "adcs_designs_cubesat_gains.csv"  # lever i: aggressive-gain box

# attribute -> orientation: -1 smaller is better (reciprocal), +1 larger is better (direct)
ORIENTATION = {
    "settling_time_s": -1,
    "slew_time_s": -1,
    "pointing_error_deg": -1,
    "total_mass_kg": -1,
    "control_effort": -1,
    "peak_slew_power_w": -1,
    "dod_eclipse": -1,
    "power_margin_w": +1,
    "energy_balance_wh": +1,
    "eclipse_reserve_wh": +1,
}
# lever ii: momentum utilisation = peak momentum / wheel capacity, smaller is better
ORIENTATION_11 = {**ORIENTATION, "momentum_utilisation": -1}
# dataset name -> (csv, orientation of its attributes); the first is the baseline of the record
DATASETS = {
    "baseline": (CSV, ORIENTATION),
    "headroom": (CSV, ORIENTATION_11),
    "gains": (CSV_GAINS, ORIENTATION),
    "gains_headroom": (CSV_GAINS, ORIENTATION_11),
}
ATTRS = list(ORIENTATION)
POWER = [
    "power_margin_w",
    "energy_balance_wh",
    "eclipse_reserve_wh",
    "peak_slew_power_w",
    "dod_eclipse",
]
SUPPORT_TOL = 1e-3  # an exponent above this is in the contending set
TARGET_FRAC_ABOVE = 0.10


PRIMARY = ["gains", "gains_headroom"]  # aggressive-gain regime: R-13 (a), (b), (c), (e)
REGIME = ["baseline", "headroom"]  # stock-gain regime: the recorded comparison


def feasible(df: pd.DataFrame, attrs: list[str] = ATTRS) -> pd.DataFrame:
    """Feasible: settled, power_ok, momentum_ok, every attribute positive (amendments 2 and 3).

    ``dod_ok`` is a reported flag, not a filter; but a design with ``dod_ok`` false has a
    non-positive ``eclipse_reserve_wh`` (a larger-is-better attribute) and is excluded by the
    positivity condition for that reason (``test_dod_violation_is_a_non_positive_reserve``).
    """
    ok = df.settled & df.power_ok & df.momentum_ok
    ok &= (df[attrs] > 0).all(axis=1)
    return df[ok]


def conditioned(df: pd.DataFrame, orientation: dict = ORIENTATION) -> np.ndarray:
    """Standardized log larger-is-better metrics ``u`` (n, d), columns in ``orientation`` order."""
    U = np.column_stack([o * np.log(df[a].to_numpy(float)) for a, o in orientation.items()])
    return (U - U.mean(axis=0)) / U.std(axis=0)


def working_fit(U: np.ndarray, target: float = TARGET_FRAC_ABOVE):
    """Fit at the temperature whose ``frac_above_`` is closest to ``target`` (log-tau bisection)."""
    X = np.exp(U)
    lo, hi = np.log(1.0), np.log(1000.0)
    best = None
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        hts = HyperbolicTradeSpace(temperature=float(np.exp(mid))).fit(X)
        gap = abs(hts.frac_above_ - target)
        if best is None or gap < best[0]:
            best = (gap, hts)
        # frac_above_ falls as tau grows (a harder maximum leaves fewer rows above V = 1)
        if hts.frac_above_ > target:
            lo = mid
        else:
            hi = mid
        if gap < 0.002:
            break
    return best[1]


def richness(df: pd.DataFrame, orientation: dict = ORIENTATION, seed: int = 0, n_boot: int = 100):
    """The hand version of the probe on a cubesat frame; every quantity R-13 asks for."""
    attrs = list(orientation)
    f = feasible(df, attrs).reset_index(drop=True)
    U = conditioned(f, orientation)
    lp = S.solve_lp(U, 0.0)
    w_inf = dict(zip(attrs, lp.w, strict=True))
    hts = working_fit(U)
    tau = float(hts.temperature)
    near = np.abs(hts.training_log_v_) < 1.0 / tau
    assoc = pd.DataFrame(np.corrcoef(U[near].T), index=attrs, columns=attrs)
    rng = np.random.default_rng(seed)
    boots = np.array([S.solve_lp(U[rng.integers(0, len(U), len(U))], 0.0).w for _ in range(n_boot)])
    in_support = boots > SUPPORT_TOL
    j = {a: attrs.index(a) for a in attrs}
    return {
        "attrs": attrs,
        "n_feasible": len(f),
        "frame": f,
        "U": U,
        "w_inf": w_inf,
        "contending": [a for a in attrs if w_inf[a] > SUPPORT_TOL],
        "tau": tau,
        "frac_above": hts.frac_above_,
        "w_tau": dict(zip(attrs, hts.exponents_[0], strict=True)),
        "near": near,
        "n_near": int(near.sum()),
        "assoc": assoc,
        "wheel_near_counts": f.loc[near, "wheel_class"].value_counts().to_dict(),
        "boot_frac_in_support": {a: float(in_support[:, j[a]].mean()) for a in attrs},
        "boot_median_w": {a: float(np.median(boots[:, j[a]])) for a in attrs},
        "hts": hts,
    }


@pytest.fixture(scope="module")
def capacities():
    """Wheel capacities (N m s) read from the SysML model through the client (lever ii)."""
    import cubesat_model as cm

    try:
        return cm.load_model().wheel_capacities()
    except cm.OpenSysMLUnavailable as exc:
        flag = " (REQUIRE_OPENSYSML is set)" if os.environ.get("REQUIRE_OPENSYSML") else ""
        pytest.fail(f"the opensysml client could not start{flag}: {exc}", pytrace=False)


@pytest.fixture(scope="module", params=list(DATASETS))
def dataset(request):
    return request.param


@pytest.fixture(scope="module")
def df(dataset, request):
    csv, orientation = DATASETS[dataset]
    frame = pd.read_csv(csv)
    if "momentum_utilisation" in orientation:
        import cubesat_model as cm

        frame = cm.add_momentum_utilisation(frame, request.getfixturevalue("capacities"))
    return frame


@pytest.fixture(scope="module")
def attrs(dataset):
    return list(DATASETS[dataset][1])


@pytest.fixture(scope="module")
def probe(df, dataset):
    return richness(df, DATASETS[dataset][1])


# ---------------------------------------------------------------------------------------------
# R-15: dataset shape
# ---------------------------------------------------------------------------------------------
def test_dataset_shape_and_columns(df, attrs):
    design = ["design_id", "seed", "wheel_class", "st_grade", "panel_span_m", "battery_wh"]
    design += ["Kp", "Kd"]
    flags = ["settled", "momentum_ok", "torque_saturated_frac", "power_ok", "dod_ok"]
    scenario = ["slew_deg", "t_end_s", "max_step_s"]
    needed = [*design, *attrs, "slew_time_05deg_s", "adcs_mass_kg", *flags, *scenario]
    assert len(df) >= 1000
    assert set(needed) <= set(df.columns)
    assert df.design_id.tolist() == list(range(len(df)))
    assert np.isfinite(df[attrs].to_numpy(float)).all()


def test_settled_fraction_and_flag_shares(df, attrs, capsys):
    assert df.settled.mean() >= 0.85
    shares = {
        flag: float((~df[flag]).mean()) for flag in ("settled", "momentum_ok", "power_ok", "dod_ok")
    }
    print("violation shares:", shares)  # reported (pytest -s); the numbers are in the probe note
    assert all(0.0 <= v <= 1.0 for v in shares.values())
    ok = feasible(df, attrs)
    assert len(ok) > 0.5 * len(df)
    assert (ok[attrs] > 0).all().all()


def test_dod_violation_is_a_non_positive_reserve(df, attrs):
    """dod_ok false <=> eclipse reserve not positive: excluding on positivity covers dod_ok."""
    assert ((~df.dod_ok) == (df.eclipse_reserve_wh <= 0)).all()
    assert (df[attrs][df.dod_ok] > 0).all().all()


def test_momentum_utilisation_matches_the_momentum_flag(df, dataset):
    """Lever ii: utilisation <= 1 exactly when ``momentum_ok`` (a cross-check of the units)."""
    if "momentum_utilisation" in df.columns:  # the two datasets carrying the attribute
        assert ((df.momentum_utilisation <= 1) == df.momentum_ok).all()
        assert (df.momentum_utilisation > 0).all()


# ---------------------------------------------------------------------------------------------
# R-14: torque binds
# ---------------------------------------------------------------------------------------------
# R-14 as amended (WP4b scope amendment 1, work-packages/WP4b-decisions.md): only the two relative
# clauses remain; the absolute small-wheel level 0.25 was an arbitrary default and is dropped
# (the committed dataset has 0.237).
def test_torque_binds_for_small_wheels(df, attrs):
    ok = feasible(df, attrs)  # amendment 2: R-14 is evaluated on the feasible set
    med_sat = ok.groupby("wheel_class").torque_saturated_frac.median()
    med_t = ok.groupby("wheel_class").settling_time_s.median()
    small, large = med_sat["small"], med_sat["large"]
    assert small >= 3 * large, med_sat.to_dict()
    assert med_t["small"] >= 1.25 * med_t["large"], med_t.to_dict()


# ---------------------------------------------------------------------------------------------
# R-13: richness (clauses and thresholds unchanged by amendment 5)
# ---------------------------------------------------------------------------------------------
def test_working_temperature_found(probe):
    assert abs(probe["frac_above"] - TARGET_FRAC_ABOVE) < 0.03, (probe["tau"], probe["frac_above"])
    assert probe["n_near"] >= 10


@pytest.mark.parametrize("dataset", PRIMARY, indirect=True)
def test_a_contending_set_includes_mass_and_a_power_attribute(probe):
    w = probe["w_inf"]
    assert len(probe["contending"]) >= 3, w
    assert w["total_mass_kg"] >= 0.05, w
    assert max(w[a] for a in POWER) >= 0.05, w


@pytest.mark.parametrize("dataset", PRIMARY, indirect=True)
def test_b_bootstrap_support_of_mass_and_power(probe):
    frac, med = probe["boot_frac_in_support"], probe["boot_median_w"]
    assert frac["total_mass_kg"] >= 0.90 and med["total_mass_kg"] >= 0.05, (frac, med)
    assert any(frac[a] >= 0.90 and med[a] >= 0.05 for a in POWER), (frac, med)


@pytest.mark.parametrize("dataset", PRIMARY, indirect=True)
def test_c_agility_against_mass(probe):
    """Amendment 4: the settling-mass OR the slew_time-mass association is at most -0.30."""
    a = probe["assoc"]
    assert (
        min(a.loc["settling_time_s", "total_mass_kg"], a.loc["slew_time_s", "total_mass_kg"])
        <= -0.30
    )
    big = [w for w, c in probe["wheel_near_counts"].items() if c >= 10]
    assert len(big) >= 2, probe["wheel_near_counts"]


def test_d_a_power_tension(probe):
    a, attrs = probe["assoc"], probe["attrs"]
    pairs = {
        (p, q): a.loc[p, q]
        for p in POWER
        for q in attrs
        if p != q and (q not in POWER or attrs.index(p) < attrs.index(q))
    }
    assert min(pairs.values()) <= -0.30, sorted(pairs.items(), key=lambda kv: kv[1])[:4]


@pytest.mark.parametrize("dataset", PRIMARY, indirect=True)
def test_e_previous_tensions_retained(probe):
    a = probe["assoc"]
    assert a.loc["settling_time_s", "control_effort"] <= -0.30
    assert a.loc["pointing_error_deg", "control_effort"] <= -0.30
    assert a.loc["pointing_error_deg", "total_mass_kg"] <= -0.30
    assert a.loc["settling_time_s", "pointing_error_deg"] >= 0.0


@pytest.mark.parametrize("dataset", REGIME, indirect=True)
def test_regime_comparison_stock_gains(probe, dataset):
    """Regime comparison: at the stock gains (Kd/Kp 3.9) wheel class is a feasibility boundary.

    The slow pole of the PD loop hides the wheel class, so agility does not trade against mass
    (recorded numbers: settling-mass -0.13 / -0.13 and slew time-mass -0.11 / -0.08, baseline /
    headroom). On the baseline total mass is absent from the contending set (exponent 0.000,
    bootstrap support 0.00) and the near-frontier rows are small wheels (78) rather than large
    (1); with the utilisation attribute mass enters weakly (0.060, support 0.99) and the
    pointing-mass association falls to -0.11. The primary (aggressive-gain) dataset is the one
    that satisfies R-13; this is the same finding seen from the other side.
    """
    a, w = probe["assoc"], probe["w_inf"]
    assert a.loc["settling_time_s", "total_mass_kg"] > -0.30
    assert a.loc["slew_time_s", "total_mass_kg"] > -0.30
    assert w["total_mass_kg"] < 0.10, w
    near = probe["wheel_near_counts"]
    if dataset == "baseline":
        assert w["total_mass_kg"] < 0.05, w
        assert probe["boot_frac_in_support"]["total_mass_kg"] < 0.10
        assert near.get("small", 0) > near.get("medium", 0) and near.get("large", 0) <= 5, near
        assert a.loc["pointing_error_deg", "total_mass_kg"] <= -0.30  # previous tension retained
    else:
        assert w["total_mass_kg"] >= 0.05, w
        assert probe["boot_frac_in_support"]["total_mass_kg"] >= 0.90
        assert a.loc["pointing_error_deg", "total_mass_kg"] > -0.30


def test_hand_probe_agrees_with_tension_report(probe):
    """The WP3 tension report reproduces the hand quantities on the same conditioned data."""
    attrs = probe["attrs"]
    rep = tension_report(probe["hts"], np.exp(probe["U"]))
    assert rep.n_near_frontier == probe["n_near"]
    np.testing.assert_allclose(rep.association, probe["assoc"].to_numpy(), atol=1e-9)
    assert [attrs[i] for i in rep.contending_set] == probe["contending"] or set(
        attrs[i] for i in rep.contending_set
    ) >= set(probe["contending"])
