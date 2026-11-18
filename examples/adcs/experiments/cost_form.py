"""The form of the cost model, in plain SymPy (WP30 stage 3b, R-4).

A pencil-and-paper substitute for a derivation, not a formal verification: the symbolic cost of a
fleet is written from numbers read out of the model (``constants``), and four statements are
checked on it.

1. Every part's total price, ``total_p(n) = u_p [f_p + (1 - f_p) n^(1 - b_p)]`` with
   ``b_p = -log2(s_p)``, is a posynomial in the fleet size ``n`` and the span and capacity that
   its single-unit price ``u_p`` may be proportional to: a fixed term plus a positive coefficient
   times ``n`` to a positive real power.
2. The total is nondecreasing and concave in ``n`` (the first derivative positive, the second
   nonpositive for ``n > 0``) and its unit cost ``total_p / n`` falls (negative derivative).
3. The cost of a fleet, ``F = sum_p total_p + n * launch_rate * mass(span, capacity)``, is a
   posynomial in ``(n, span, capacity)``, and so is the unit cost ``F / n``: the cost model is
   compatible with a geometric program.
4. At ``n = 1`` each total is the single-unit price.

``constants(model, oracle_rows)`` reads the numbers; ``checks(c)`` returns the statements as a
dict of booleans. Run ``uv run python examples/adcs/experiments/cost_form.py`` for the printed
reading on the committed model.
"""

from __future__ import annotations

import math

import sympy as sp

PARTS = ("bus", "panel", "battery", "wheel", "tracker", "assembly")
n, span, cap = sp.symbols("n span capacity", positive=True)


def curve(unit_price, fixed_share, slope):
    """The total price of a part for a fleet of ``n``, as the model's ``PartTotal`` writes it."""
    exponent = sp.Float(1 + math.log2(float(slope)))
    return unit_price * (fixed_share + (1 - fixed_share) * n**exponent)


def posynomial_terms(expr, variables):
    """The terms of ``expr`` as ``(coefficient, {variable: exponent})`` when ``expr`` is a
    posynomial in ``variables`` (positive coefficients, real constant exponents), else None.

    >>> x, y = sp.symbols("x y", positive=True)
    >>> posynomial_terms(3 + 2 * x**sp.Rational(1, 2) * y, [x, y])
    [(3, {}), (2, {x: 1/2, y: 1})]
    >>> posynomial_terms(x - 1, [x]) is None
    True
    """
    out = []
    for term in sp.Add.make_args(sp.expand(expr)):
        coeff, rest = term.as_independent(*variables, as_Add=False)
        powers = rest.as_powers_dict()
        if not (coeff.is_number and coeff.is_positive):
            return None
        if any(k not in variables or not v.is_real for k, v in powers.items() if k != 1):
            return None
        out.append((coeff, {k: v for k, v in powers.items() if k != 1}))
    return out


def fleet_expressions(c: dict):
    """The symbolic totals, the fleet cost and the unit cost from the constants ``c``.

    ``c`` holds, per part, ``unit[part]`` (the single-unit price: a number, or a multiple of
    ``span`` or ``cap``), ``share[part]`` and ``slope[part]``; ``launch_rate``; and the mass as an
    affine function ``mass0 + mass_span * span + mass_cap * cap``.
    """
    totals = {p: curve(c["unit"][p], c["share"][p], c["slope"][p]) for p in PARTS}
    mass = c["mass0"] + c["mass_span"] * span + c["mass_cap"] * cap
    fleet = sum(totals.values()) + n * c["launch_rate"] * mass
    return totals, fleet, fleet / n


def checks(c: dict) -> dict[str, bool]:
    """The four statements of the module docstring on the constants ``c``."""
    totals, fleet, unit = fleet_expressions(c)
    out = {}
    out["each total is a posynomial in (n, span, capacity)"] = all(
        posynomial_terms(t, [n, span, cap]) is not None for t in totals.values()
    )
    out["each total is nondecreasing in n"] = all(
        bool(sp.diff(t, n).is_positive) for t in totals.values()
    )
    out["each total is concave in n"] = all(
        bool(sp.diff(t, n, 2).is_nonpositive) for t in totals.values()
    )
    out["each unit cost falls in n"] = all(
        bool(sp.diff(sp.expand(t / n), n).is_negative) for t in totals.values()
    )
    out["each total at n = 1 is its unit price"] = all(
        abs(sp.expand(totals[p].subs(n, 1) - c["unit"][p]).subs({span: 1, cap: 1})) < 1e-9
        for p in PARTS
    )
    out["the fleet cost is a posynomial in (n, span, capacity)"] = (
        posynomial_terms(fleet, [n, span, cap]) is not None
    )
    out["the unit cost is a posynomial in (n, span, capacity)"] = (
        posynomial_terms(unit, [n, span, cap]) is not None
    )
    return out


def constants(model, package: str, rows) -> dict:
    """The constants of ``fleet_expressions`` read from the loaded ``model`` (opensysml).

    ``rows`` are ``(symbol, span, capacity)`` triples naming configurations of the loaded model
    (one wheel class and one tracker grade) at fleet size 1; the affine mass and the price
    relations that are multiples of ``span`` or ``capacity`` are read from them.
    """

    def ev(expression: str, unit: str | None = None) -> float:
        out = model.eval(f"{package}::{expression}")
        out = out[0] if isinstance(out, list) else out
        if unit is not None:
            out = out.in_unit(model.eval(f"1.0 [{unit}]").unit)
        return float(out)

    s0 = rows[0]
    price = {p: lambda sym, p=p: ev(f"{p.capitalize()}Price({sym})") for p in
             ("panel", "battery", "wheel", "tracker")}  # fmt: skip
    mass = [ev(f"MassAccounting({sym})", "SI::kg") for sym, _, _ in rows]
    # mass = mass0 + mass_span * span + mass_cap * cap from three configurations, the fourth checks
    (_, a_span, a_cap), (_, b_span, _), (_, _, c_cap) = rows[:3]
    mass_span = (mass[1] - mass[0]) / (b_span - a_span)
    mass_cap = (mass[2] - mass[0]) / (c_cap - a_cap)
    mass0 = mass[0] - mass_span * a_span - mass_cap * a_cap
    _, d_span, d_cap = rows[3]
    assert abs(mass0 + mass_span * d_span + mass_cap * d_cap - mass[3]) < 1e-9, "mass is affine"
    unit = {
        "bus": ev("prices.bus") + ev("prices.antenna") + ev("prices.imu"),
        "panel": sp.Float(price["panel"](s0[0]) / s0[1]) * span,  # proportional to the span
        "battery": sp.Float(price["battery"](s0[0]) / s0[2]) * cap,  # proportional to the capacity
        "wheel": sp.Float(price["wheel"](s0[0])),
        "tracker": sp.Float(price["tracker"](s0[0])),
        "assembly": sp.Float(ev("prices.assembly")),
    }
    unit["bus"] = sp.Float(unit["bus"])
    for sym, sp_, cp_ in rows:  # the proportionality holds on every configuration
        assert abs(price["panel"](sym) / sp_ - price["panel"](s0[0]) / s0[1]) < 1e-6
        assert abs(price["battery"](sym) / cp_ - price["battery"](s0[0]) / s0[2]) < 1e-6
    return {
        "unit": unit,
        "share": {p: sp.Float(ev(f"pricing.{p}Share")) for p in PARTS},
        "slope": {p: ev(f"pricing.{p}Slope") for p in PARTS},
        "launch_rate": sp.Float(ev("environment.launchRate")),
        "mass0": sp.Float(mass0),
        "mass_span": sp.Float(mass_span),
        "mass_cap": sp.Float(mass_cap),
    }


def main() -> int:  # pragma: no cover - the printed reading
    import pathlib
    import sys

    here = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(here.parent))
    from experiments import cubesat_oracle as co

    text = (here.parent / "model_v2" / "cubesat.sysml").read_text(encoding="utf-8")
    oracle = co.CubesatOracle(text, "nominalSlew", "aggressive", workers=1)
    base = dict(wheel_class="medium", st_grade="medium", Kp=0.5, Kd=1.0, fleet_size=1.0)
    grid = [(0.3, 20.0), (1.0, 20.0), (0.3, 200.0), (0.7, 90.0)]
    loaded, symbols = oracle._configure(
        [
            {**base, "design_id": i, "panel_span_m": s, "battery_wh": b}
            for i, (s, b) in enumerate(grid)
        ]
    )
    rows = [(sym, s, b) for sym, (s, b) in zip(symbols, grid, strict=True)]
    for statement, ok in checks(constants(loaded, co.PACKAGE, rows)).items():
        print(f"{'yes' if ok else 'NO ':3s} {statement}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
