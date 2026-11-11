# Spike D — decision record (commercial cubesat economics for the cost model and the H-2 budget)

## Origin

The supervisor's direction of 2026-11-10 on H-2, verbatim in `work-packages/WP27-decisions.md` ("H-2"): a budget, a
research spike on commercial space economics, a fleet-size configuration variable, per-part pricing curves with a
fixed base and a falling unit cost, two pricing metrics (unit cost; fleet cost = unit cost times units), the model
still priced per unit and not a model of the fleet.

## The driver's decisions on the readout's options (2026-11-10, 23:50; Track B stage (2), the cost part)

- **A-1.** Wright cumulative-average curves with a fixed share and a slope per part, as section 3 proposes: the form
  he described (a fixed base plus a falling unit cost; different curves per part; the total growing in n at a
  decreasing rate), and every term stays a posynomial in (n, x) (section 7).
- **B-2.** Fleet size 1 to 30: the sources' learning bands cover it and 30 reads as a small constellation; beyond it the
  guidance thins.
- **C-3, the values his.** Both pricing metrics carry a requirement: a unit build cost limit read at the
  configuration's own n, and a fleet cost limit (build and launch) with the fleet size free. The two values are the
  supervisor's, chosen from a pass-fraction ladder as his earlier thresholds were (`admit-shares.txt` is the first
  rung; the fleet ladder is computed by the model developer); the build proceeds with the form and placeholders,
  and the values land at the data gate.
- **D-1, with his confirmation.** Launch at 7,000 USD/kg (the 2026 rate), replacing 6,000; the 50 kg minimum slot
  stays outside the model (a note in the view, not a limit). His launch budget was chosen as a mass (15.11 kg, 95 %
  admitted) and stated in USD at 6,000/kg; at 7,000/kg the same mass reads 105,770 USD. He confirms the restated
  figure, or keeps 90,643 USD at the new rate (12.95 kg), in the morning.
- **E-1.** The three coefficients the sources move are updated (tracker 150,000; panels 250,000 USD/m²; battery 150
  USD/Wh) and assembly, integration and test enters at 100,000 USD with its curve.
- Defaults left to the model developer, listed in the scope: how n is sampled over 1 to 30 (uniform on the integers
  unless the sweep shows a reason), the names of the two metrics and their units, the view's grouping (a "cost"
  group beside controls, power and energy, and mass; launch cost joins it), the glossary entries.

Stage (2) is taken for both parts of Track B (the momentum headroom, spike C; the cost model, here). One data gate.
