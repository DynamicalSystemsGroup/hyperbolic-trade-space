"""Spike D2: the baseline configuration priced under 2026 figures (no model change).

Same curve as spike D (Wright cumulative average, fixed share f, slope s; section 3 of
../spike-D-cubesat-economics/README.md). Only the single-unit coefficients u_p change between scenarios.
Stdlib only. Run: uv run --no-project python economics2026.py
"""
import math

SPAN, CHORD, WH, MASS = 0.6, 0.34, 80.0, 13.291
AREA = 2 * SPAN * CHORD  # 0.408 m^2
LAUNCH = 7000.0  # USD/kg, Transporter 2026
SLOT = 350000.0  # USD, 50 kg minimum
CURVE = {  # part: (fixed share, slope)  -- spike D choices, unchanged
    "bus": (0.30, 0.90), "panels": (0.15, 0.90), "battery": (0.10, 0.90),
    "wheels": (0.15, 0.95), "tracker": (0.20, 0.95), "assembly": (0.50, 0.90),
}
# single-unit coefficients per scenario
SCEN = {
    "spike D (WP30 as set)": dict(bus=80000, panel_m2=250000, batt_wh=150, wheel=12000, tracker=20000, assembly=100000),
    "2026 central": dict(bus=80000, panel_m2=340000, batt_wh=70, wheel=8000, tracker=20000, assembly=100000),
    "2026 low": dict(bus=80000, panel_m2=200000, batt_wh=24, wheel=4500, tracker=20000, assembly=100000),
    "2026 high": dict(bus=80000, panel_m2=340000, batt_wh=200, wheel=27500, tracker=20000, assembly=100000),
}


def u1(c):
    return dict(bus=c["bus"], panels=c["panel_m2"] * AREA, battery=c["batt_wh"] * WH,
                wheels=3 * c["wheel"], tracker=c["tracker"], assembly=c["assembly"])


def build(c, n):
    out = {}
    for p, u in u1(c).items():
        f, s = CURVE[p]
        b = -math.log2(s)
        out[p] = u * (f + (1 - f) * n ** (1 - b))
    return out


def main():
    print("== baseline (medium wheels, medium tracker, span 0.6 m, 80 Wh, 13.291 kg), area %.3f m^2" % AREA)
    for name, c in SCEN.items():
        print(f"\n-- {name}: n=1 parts", {k: round(v) for k, v in u1(c).items()}, "sum", round(sum(u1(c).values())))
        print("   n   build_fleet  build_unit  launch_fleet(linear)  launch(50kg slot)  fleet(linear)  unit(linear)  fleet(slot)  unit(slot)")
        for n in (1, 3, 10, 25, 30):
            B = sum(build(c, n).values())
            L = LAUNCH * MASS * n
            Ls = max(SLOT, L)
            print(f"  {n:3d} {B:12,.0f} {B/n:11,.0f} {L:15,.0f} {Ls:18,.0f} {B+L:14,.0f} {(B+L)/n:12,.0f} {B+Ls:12,.0f} {(B+Ls)/n:11,.0f}")
    print("\n== what 1,000,000 USD buys of the baseline (build + launch)")
    for name, c in SCEN.items():
        best_lin = best_slot = 0
        for n in range(1, 200):
            B = sum(build(c, n).values())
            if B + LAUNCH * MASS * n <= 1e6:
                best_lin = n
            if B + max(SLOT, LAUNCH * MASS * n) <= 1e6:
                best_slot = n
        bb = max((n for n in range(1, 200) if sum(build(c, n).values()) <= 1e6), default=0)
        print(f"  {name}: build only n<={bb}; build+launch linear n<={best_lin}; with 50 kg slot n<={best_slot}")

    print("\n== 25 satellites of each class, no learning (list platform price + launch at class mass)")
    # platform price (USD, bus only), CDS Rev 14.1 max mass kg; TM2S = TakeMe2Space via satsearch 2026-08-26 'starts at'
    classes = [("1U", 26000, 25000, 2), ("3U", 65000, None, 6), ("6U", 243000, 200000, 12),
               ("12U", 275000, 449000, 24), ("16U", 300000, None, 32)]
    print("class  TM2S_platform  other_platform  mass_kg  launch_raw/sat  25x(TM2S+raw launch)  25x platform only")
    for cl, tm, other, mass in classes:
        raw = LAUNCH * mass
        print(f"  {cl:4s} {tm:10,d} {str(other):>14s} {mass:6d} {raw:12,.0f} {25*(tm+raw):18,.0f} {25*tm:16,.0f}")
    print("  25 x 1U at 2 kg = 50 kg = one slot: launch", f"{max(SLOT, 25*2*LAUNCH):,.0f}", "; plus 25 x 26,000 =", f"{25*26000+SLOT:,.0f}")
    print("  EnduroSat slide prices, 1U: 25 x (25,000 + 70,000) =", f"{25*95000:,}", "; 6U: 25 x (200,000 + 450,000) =", f"{25*650000:,}")


main()
