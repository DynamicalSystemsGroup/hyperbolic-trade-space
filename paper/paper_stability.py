"""The paper prints nothing to a precision at which it is not reproducible (WP10, WP16 D-6).

``settling_time_s`` is detected on the dense solution of an adaptive integration whose accepted
steps also sum ``control_effort`` and ``torque_saturated_frac``, so a rounding-level change in a
design variable moves some of what the case reports in the last digits.
``examples/adcs/experiments/sensitivity.py`` regenerates the data five times under perturbations of
one part in 10^12 and writes the committed results file read here: per quantity the committed value
and the range over the six datasets. The generators take their numbers through
this module, so a printed quantity carries only the digits that held in all six datasets, or its
range, in the shorter of the printed format and two digits more than held, where not even
two digits did, and a numerical residue is a bound.

>>> format_hold(0.2036, 0.2029, lambda v: format(v, ".4g"))
'0.20'
>>> format_hold(145.0, 146.0, lambda v: format(v, ".0f"), count=True)
'145 to 146'
>>> format_hold(0.0652, 0.0889, lambda v: format(v, ".3f"))
'0.065 to 0.089'
>>> format_hold(0.0, 5e-18, lambda v: format(v, ".4g"))
'below 1e-12'
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from functools import cache

import paper_paths  # noqa: F401  (puts the repository on sys.path)
from paper_paths import PAPER, ROOT

SUMMARY = ROOT / "examples" / "adcs" / "experiments" / "reports" / "sensitivity.json"
EXTRA = PAPER / "stability_extra.json"
"""The quantities added after the sensitivity run, measured on the same data (stability_extra)."""
RESIDUE = 1e-12
"""Quantities that move and stay below this are numerical residues, printed as a bound."""
HOLD_FROM = 4
"""Most digits tried for a quantity that moves."""
HOLD_MIN = 2
"""Fewer digits than this holding gives the range, to two digits more than held."""


@cache
def summary() -> dict:
    """The committed results file of the sensitivity run (seeds, perturbation, quantities)."""
    return json.loads(SUMMARY.read_text(encoding="utf-8"))


@cache
def extra() -> dict:
    """The committed results file of the added quantities, same layout as :func:`summary`."""
    return json.loads(EXTRA.read_text(encoding="utf-8"))


def entry(name: str) -> dict | None:
    """The record of a quantity (``committed``, ``min``, ``max``, ``identical``), or ``None``.

    The sensitivity file is read first, then the file of the added quantities.
    """
    return summary()["quantities"].get(name) or extra()["quantities"].get(name)


def _sig(x: float, p: int) -> str:
    """``x`` to ``p`` significant digits, fixed notation unless very small or very large."""
    if x == 0 or not math.isfinite(x):
        return format(x, "g")
    if abs(x) < 1e-3 or abs(x) >= 1e6:
        return format(float(f"{x:.{p}g}"), "g")
    d = max(0, p - 1 - math.floor(math.log10(abs(x))))
    return f"{round(x, d):.{d}f}"


def format_hold(
    lo: float,
    hi: float,
    orig: Callable[[float], str],
    *,
    count: bool = False,
    value: float | None = None,
) -> str:
    """The text of a quantity whose value over the datasets runs from ``lo`` to ``hi``.

    ``orig`` is the format the table or sentence prints in. The text is ``orig(value)`` when
    nothing changes at that format; ``below 1e-12`` for a residue; ``lo to hi`` for a count; else
    the value to the most significant digits (at most four, at least two) that agree at ``lo`` and
    ``hi``, or the range at two digits where fewer agree.
    """
    value = lo if value is None else value
    if orig(lo) == orig(hi) == orig(value):
        return orig(value)
    if max(abs(lo), abs(hi)) < RESIDUE:
        return f"below {RESIDUE:g}"
    if count:
        return f"{orig(lo)} to {orig(hi)}"
    held = next((p for p in range(HOLD_FROM, 0, -1) if _sig(lo, p) == _sig(hi, p)), 0)
    if held >= HOLD_MIN:
        return _sig(value, held)
    printed = f"{orig(lo)} to {orig(hi)}"
    digits = f"{_sig(lo, held + 2)} to {_sig(hi, held + 2)}"
    return digits if len(digits) < len(printed) else printed


def residue_bound(value: float, zero: bool = False):
    """``below 1e-12`` for a nonzero numerical residue under that bound; other values unchanged.

    With ``zero`` an exact zero is the bound too: an exponent under the participation threshold
    has one spelling, whatever the solver left (an exact 0 or a residue).

    >>> residue_bound(4.4e-16), residue_bound(0.5), residue_bound(0.0)
    ('below 1e-12', 0.5, 0.0)
    >>> residue_bound(0.0, zero=True)
    'below 1e-12'
    """
    return f"below {RESIDUE:g}" if (-1 if zero else 0) < abs(value) < RESIDUE else value


def _is_count(e: dict) -> bool:
    return isinstance(e.get("committed"), int) and not isinstance(e.get("committed"), bool)


def _count_text(v: float) -> str:
    return str(round(v))


def stable(name: str, orig: Callable[[float], str] | None = None) -> str:
    """The text of the quantity ``name`` of the results file, as :func:`format_hold`.

    Parameters
    ----------
    name : str
        ``group | row | column`` as ``sensitivity.quantities`` names it.
    orig : callable, optional
        The print format of the committed value (default ``.4g``).
    """
    e = entry(name)
    if e is None or "min" not in e:
        raise KeyError(f"{name!r} is not in {SUMMARY.name} or {EXTRA.name}")
    count = _is_count(e)
    orig = _count_text if count else (orig or (lambda v: format(v, ".4g")))
    return format_hold(e["min"], e["max"], orig, count=count, value=e["committed"])


def cell(name: str, value, orig: Callable[[float], str] | None = None):
    """A table cell: ``value`` unchanged where the quantity does not move at the printed format.

    Text, flags and quantities absent from the file are returned as they are.
    """
    e = entry(name)
    if e is None or "min" not in e or isinstance(value, (str, bool)):
        return value
    if not all(isinstance(e[k], (int, float)) and math.isfinite(e[k]) for k in ("min", "max")):
        return value
    count = _is_count(e)
    orig = _count_text if count else (orig or (lambda v: format(v, ".4g")))
    text = format_hold(e["min"], e["max"], orig, count=count, value=float(value))
    return value if text == orig(float(value)) else text


def stable_frame(df, prefix: str, key: str | None = None, orig=None):
    """``df`` with each cell that moves over the datasets replaced by its stable text.

    Cell names are those of ``sensitivity._flat``: ``prefix | row | column``, the row named by the
    ``key`` column or ``row n``.
    """
    out = df.astype(object).copy()
    for i in range(len(df)):
        label = str(df.iloc[i][key]) if key else f"row {i + 1}"
        for col in df.columns:
            if col == key:
                continue
            out.iat[i, out.columns.get_loc(col)] = cell(
                f"{prefix} | {label} | {col}", df.iloc[i][col], orig
            )
    return out
