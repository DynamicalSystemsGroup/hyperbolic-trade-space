# ruff: noqa: E501, SIM115, E731, B023, B007
"""Spike D: per-part pricing curves, the fleet totals and the budget band for the case model.

Run from the repository root:
    uv run python work-packages/WP23-rounds/spikes/spike-D-cubesat-economics/economics.py
Reads examples/adcs/data/v2 (read-only). Every parameter is a proposal; the sources are in README.md.
total_p(n) = u_p(x) * [f_p + (1 - f_p) * n**(1 - b_p)],  b_p = -log2(slope_p)
  u_p(x): the part's single-unit price at the configuration x (n = 1)
  f_p   : the fixed share of the single-unit price (paid once per fleet)
  slope : cumulative-average learning slope (Wright); average unit cost of n units = u1 * n**(-b)
"""

import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[4] / "examples/adcs/data/v2"
WHEEL_TORQUE = {"small": 0.0003, "medium": 0.002, "large": 0.010}  # N.m (cubesat.sysml)
TRACKER_ACC = {"coarse": 30.0, "medium": 10.0, "fine": 2.0}  # arcsec (cubesat.sysml)
PANEL_CHORD = 0.34
N_WHEELS = 3


# current roll-up (stakeholders.sysml UnitCosts), n = 1
def current_rollup(wheel, trk, span, wh):
    area = 2 * span * PANEL_CHORD
    return (
        60000
        + 150000 * area
        + 50 * wh
        + 15000
        + 5000
        + N_WHEELS * (8000 + 2.0e6 * WHEEL_TORQUE[wheel])
        + 5000
        + 300000 / TRACKER_ACC[trk]
    )


# proposed single-unit price relations u_p(x) (USD)
def u_bus():
    return 80000.0  # bus + antenna + IMU block (as the case: 60k + 15k + 5k)


def u_panels(span):
    return 250000.0 * 2 * span * PANEL_CHORD


def u_battery(wh):
    return 150.0 * wh


def u_wheels(wheel):
    return N_WHEELS * (8000.0 + 2.0e6 * WHEEL_TORQUE[wheel])


def u_tracker(trk):
    return 5000.0 + 150000.0 / TRACKER_ACC[trk]


U_ASSEMBLY = 100000.0

# (fixed share f, learning slope s) per part; slope 0.95 = flat band, 0.90 mid, 0.85 strong
CURVES = {
    "bus": (0.30, 0.90),
    "panels": (0.15, 0.90),
    "battery": (0.10, 0.90),
    "wheels": (0.15, 0.95),
    "tracker": (0.20, 0.95),
    "assembly": (0.50, 0.90),
}
LAUNCH_RATE = 7000.0  # USD/kg


def total(part, u1, n, curves=CURVES):
    f, s = curves[part]
    b = -math.log2(s)
    return u1 * (f + (1 - f) * n ** (1 - b))


def build_parts(wheel, trk, span, wh):
    return {
        "bus": u_bus(),
        "panels": u_panels(span),
        "battery": u_battery(wh),
        "wheels": u_wheels(wheel),
        "tracker": u_tracker(trk),
        "assembly": U_ASSEMBLY,
    }


def fleet_build(wheel, trk, span, wh, n, curves=CURVES):
    return sum(total(p, u, n, curves) for p, u in build_parts(wheel, trk, span, wh).items())


def metrics(wheel, trk, span, wh, mass, n, launch=True):
    build = fleet_build(wheel, trk, span, wh, n)
    lc = LAUNCH_RATE * mass * n if launch else 0.0
    fleet = build + lc
    return build, lc, fleet, fleet / n


CONFIGS = {  # name: (wheel, tracker, span m, battery Wh, total mass kg)
    "compact": ("small", "coarse", 0.35, 40.0, None),
    "baseline": ("medium", "medium", 0.6, 80.0, 13.291),
    "agile": ("large", "fine", 0.8, 140.0, None),
}


def mass_of(wheel, trk, span, wh):
    wm = {"small": 0.12, "medium": 0.25, "large": 0.60}[wheel]
    tm = {"coarse": 0.15, "medium": 0.35, "fine": 0.90}[trk]
    return 10 + 2 * 2.5 * span * PANEL_CHORD + wh / 140 + 0.5 + 0.1 + N_WHEELS * wm + tm


def main():
    out = []
    P = out.append
    P("== current roll-up (n=1) vs proposed build price at n=1 ==")
    for k, (w, t, s, b, _) in CONFIGS.items():
        P(
            f"{k:9s} current {current_rollup(w, t, s, b):10,.0f}   proposed build n=1 {fleet_build(w, t, s, b, 1):10,.0f}   "
            f"mass {mass_of(w, t, s, b):6.3f} kg"
        )
    P("")
    P("== per-part totals at the baseline configuration ==")
    w, t, s, b, _ = CONFIGS["baseline"]
    parts = build_parts(w, t, s, b)
    P(
        f"{'part':9s}{'u1':>10s}{'f':>6s}{'slope':>7s}{'b':>7s}"
        + "".join(f"{'n=' + str(n):>11s}" for n in (1, 3, 10, 30))
    )
    for p, u in parts.items():
        f, sl = CURVES[p]
        P(
            f"{p:9s}{u:10,.0f}{f:6.2f}{sl:7.2f}{-math.log2(sl):7.3f}"
            + "".join(f"{total(p, u, n):11,.0f}" for n in (1, 3, 10, 30))
        )
    P("")
    P("== representative design (baseline configuration), fleet n = 1, 3, 10, 30 ==")
    mass = mass_of(w, t, s, b)
    P(f"mass {mass:.3f} kg; launch rate {LAUNCH_RATE:,.0f} USD/kg (linear)")
    P(
        f"{'n':>4s}{'build total':>13s}{'build unit':>12s}{'launch total':>14s}{'fleet cost':>12s}{'unit cost':>11s}{'unit/unit(1)':>14s}"
    )
    base1 = None
    for n in (1, 3, 10, 30):
        bt, lc, fc, uc = metrics(w, t, s, b, mass, n)
        base1 = base1 or uc
        P(f"{n:4d}{bt:13,.0f}{bt / n:12,.0f}{lc:14,.0f}{fc:12,.0f}{uc:11,.0f}{uc / base1:14.3f}")
    P("")
    P(
        "== same, with the 50 kg minimum slot (350,000 USD) applied to the launch (not posynomial) =="
    )
    for n in (1, 3, 10, 30):
        bt = fleet_build(w, t, s, b, n)
        lc = max(350000.0, LAUNCH_RATE * mass * n)
        lc = max(350000.0, 7000.0 * mass * n)
        P(f"n={n:3d} launch {lc:11,.0f}  fleet {bt + lc:12,.0f}  unit {(bt + lc) / n:10,.0f}")
    P("")
    P("== sensitivity of the baseline unit build cost (no launch) to the learning slopes ==")
    for label, shift in (
        ("slopes as proposed", 0.0),
        ("all 0.95 (flat)", None),
        ("all 0.85 (strong)", 0.85),
    ):
        if shift == 0.0:
            cv = CURVES
        else:
            val = 0.95 if shift is None else shift
            cv = {k: (f, val) for k, (f, _) in CURVES.items()}
        P(
            f"{label:20s}"
            + "  ".join(
                f"n={n}: {fleet_build(w, t, s, b, n, cv) / n:9,.0f}" for n in (1, 3, 10, 30)
            )
        )
    P("")
    P(
        "== distribution of unit build cost over the 1000 + 1000 designs (proposed prices, n = 1, 10) =="
    )
    for fn in ("adcs_designs_cubesat.csv", "adcs_designs_cubesat_gains.csv"):
        rows = list(csv.DictReader(open(DATA / fn)))
        feas = [
            r
            for r in rows
            if r["settled"] == "True"
            and r["momentum_ok"] == "True"
            and r["power_ok"] == "True"
            and r["dod_ok"] == "True"
        ]
        for label, sel in (("all", rows), ("feasible", feas)):
            for n in (1, 10):
                v = sorted(
                    fleet_build(
                        r["wheel_class"],
                        r["st_grade"],
                        float(r["panel_span_m"]),
                        float(r["battery_wh"]),
                        n,
                    )
                    / n
                    for r in sel
                )
                q = lambda p: v[min(len(v) - 1, int(p * len(v)))]
                P(
                    f"{fn[:26]:26s} {label:8s} n={n:2d} N={len(v):4d} min {v[0]:9,.0f} p05 {q(0.05):9,.0f} median {q(0.5):9,.0f} "
                    f"p90 {q(0.9):9,.0f} p95 {q(0.95):9,.0f} max {v[-1]:9,.0f}"
                )
    P("")
    P("== current roll-up over the same designs (n=1) ==")
    for fn in ("adcs_designs_cubesat.csv", "adcs_designs_cubesat_gains.csv"):
        rows = list(csv.DictReader(open(DATA / fn)))
        v = sorted(
            current_rollup(
                r["wheel_class"], r["st_grade"], float(r["panel_span_m"]), float(r["battery_wh"])
            )
            for r in rows
        )
        P(
            f"{fn[:26]:26s} min {v[0]:9,.0f} median {v[len(v) // 2]:9,.0f} p95 {v[int(0.95 * len(v))]:9,.0f} max {v[-1]:9,.0f}"
        )
    P("")
    P(
        "== posynomial check: total(n) is a sum of c*n**e with c > 0, e = 1 - b in (0, 1), plus a constant =="
    )
    for p, (f, sl) in CURVES.items():
        P(
            f"{p:9s} exponent 1-b = {1 + math.log2(sl):.3f}  (total grows, concave in n; average unit cost falls as n^{math.log2(sl):.3f})"
        )
    text = "\n".join(out)
    print(text)
    (Path(__file__).parent / "economics-output.txt").write_text(text + "\n")


main()
