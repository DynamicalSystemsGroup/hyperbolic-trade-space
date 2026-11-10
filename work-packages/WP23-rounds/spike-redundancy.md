# Spike: the two metric redundancies (WP23)

Question (supervisor, `WP23-decisions.md`, "The two metric redundancies"): per pair, a modelling
issue to clean up, or a property of the system in its ranges that the full case analysis identifies
and simplifies as an outcome? Evidence: `examples/adcs/model_v2/cubesat.sysml` (calc defs, section
3; requirements, section 5) and the data of record `examples/adcs/data/v2/` (primary
`adcs_designs_cubesat_gains.csv`, stock `adcs_designs_cubesat.csv`; feasible by
`case.feasible_mask`, 706 and 780; K = 1 fits by `case.fit_study`).

**Verdict.** Eclipse reserve and depth of discharge: a modelling issue (one inequality stated
twice; a requirement's slack carried as a second metric). Power margin and energy balance: a
property of the system in its ranges (two distinct power-budget quantities sharing one linear
source), to be identified and read as one axis in the analysis.

## Pair 1: eclipse reserve and depth of discharge

**Definitions.** `EclipseDemand` D = `BaseLoad` × 0.6 h + E_slew (base load 12 W + tracker 0.4,
0.9 or 1.5 W + 0.9 W idle wheels). `DepthOfDischarge` = D / C (C the battery capacity);
`EclipseReserve` = 0.3 × C − D, 0.3 being `environment.maxDepthOfDischarge`. Both are functions of
(C, D) and nothing else; the reserve carries the environment's limit inside its definition.
`EclipseReserveRequirement` (reserve ≥ 0, added in WP22 beside the original `dod_ok`) and
`DepthOfDischargeRequirement` (D / C ≤ 0.3) are the same inequality for C > 0.

| evidence | primary | stock |
|---|---|---|
| designs with reserve ≤ 0; equal to `dod_ok` false on every row | 131 (identity holds on all 1000) | 131 (all 1000) |
| removed by "all attributes positive" after the three flags (the reserve is what removes them: `dod_ok` is not in `spec.flags`) | 105 | 117 |
| eclipse demand D over the feasible designs (Wh) | 7.98 to 8.68 (7.98 / 8.28 / 8.64 by tracker grade; slew loss ≤ 0.04) | 7.98 to 8.66 |
| Spearman reserve vs depth, feasible; within a tracker grade | −0.9994; −1.0000 (all three) | −0.9994; −1.0000 |
| design pairs the two metrics order differently (all across tracker grades) | 1.0 % | 1.0 % |
| Pearson of log reserve vs −log depth (the fit's space) | 0.92 | 0.92 |
| near-frontier association (`case.association_table`): Pearson / Spearman | 0.98 / 0.9986 | 0.90 / 0.9986 |
| K = 1 exponent reserve / depth | 0 / 0.158 | 3.7e-4 / 0.012 |

**Reading.** Given the tracker grade, D is constant to four parts in a thousand, so both metrics
are monotone functions of one tune, the battery capacity. They are not collinear in log space
(Pearson 0.92), so the linear program sees two curved columns and gives the depth of discharge the
weight in both regimes. The identity is in the definitions, not in the ranges: no battery range or
load separates a quantity from its own slack. A modelling issue: a cleaner model carries one metric
for the eclipse energy and one requirement on it.

**Clean-up.** The depth of discharge is the engineer's named MoP (cycle life, the environment's
0.3); the reserve is that requirement's slack in Wh with the threshold baked in. The clean-up drops
`EclipseReserve` as a traded metric and `EclipseReserveRequirement` (its `satisfy`, verification
entry, place in the experiment's return tuple and the header doc's list of nine) and keeps
`DepthOfDischarge` with its requirement. One dependency: today the 131 depth-of-discharge failures
leave the fit through the positivity of the reserve; after the clean-up `dod_ok` (a CSV column)
must enter `spec.flags` in `case.py`, or they enter the fit.

**What it touches.** The model and `coverage.py` / `coverage.md` / the views; the oracle's
`ATTRIBUTE_NAMES` and the frozen CSV header, so one regeneration in the container of record with a
ledger entry (or the column stays as a derived, non-traded column like `available_power_w`); the
contract (`case.v2.traded_metrics` 9 → 8, the column table) with an amendment row; `case.py`
(`_ATTRS` and its parallel tuples, `flags`); five test files that pin nine (`test_case`,
`test_cubesat_oracle`, `test_diagnostic_pair`, `test_model_coverage`, `test_interface_contract`);
the paper's numbers, refit once on eight metrics (the primary regime's 5-lemma already excludes
the reserve, so the contending sets are likely to stand); Appendix C.5.

## Pair 2: power margin and energy balance

**Definitions.** `GeneratedPower` G = 81.627 W/m × span (flux, efficiency, packing, degradation,
incidence and chord are constants; exact in the data). `PowerMargin` = G − 12 W −
`PeakSlewPower`, the latter tracker + 0.9 W + 5e4 × τ_peak² (0.0045, 0.2 and 5 W at the three
wheel caps): a power at the slew's peak in sunlight. `EnergyBalance` = G × (T − 0.6 h) −
`BaseLoad` × T − E_slew, T = 1.5445 h: an energy over one orbit. Eliminating G, inside one (wheel
class, tracker grade) cell,

margin = balance / 0.9445 h + 0.635 × base load − 5e4 × τ_peak² + E_slew / 0.9445 h,

the balance plus a per-cell constant, exact wherever the peak torque sits at the class cap.

| evidence | primary | stock |
|---|---|---|
| pooled fit margin on balance: slope, intercept, R², max residual | 1.0005, 7.97 W, 0.973, 4.18 W | 1.036, 7.76 W, 0.981, 4.18 W |
| largest residuals | large wheel, coarse tracker, span 0.340 to 0.346 m (the power-limited corner: usable torque below the cap) | same cell, 0.346 to 0.374 m |
| residual mean by wheel class small / medium / large | +1.56 / +1.69 / −2.68 W | +1.41 / +1.32 / −2.69 W |
| within a cell, small and medium wheels: slope, max residual | 1.0587 (= 1 / 0.9445 h), < 0.006 W | 1.0587, < 0.004 W |
| within a cell, large wheels: max residual | 0.68 to 0.93 W | 3.3 to 3.6 W |
| a configuration that separates them (medium tracker, span 0.605 vs 0.616 m) | small wheel: margin 35.6 W, balance 25.3 Wh; large wheel: 31.5 W, 26.2 Wh (opposite order) | span 0.602 vs 0.594: 35.4 / 25.1 against 29.7 / 24.5 |
| Pearson raw / of logs; Spearman, feasible | 0.987 / 0.960; 0.982 | 0.990 / 0.966; 0.988 |
| design pairs the two metrics order differently | 5.0 % | 4.2 % |
| near-frontier association: Pearson / Spearman | 0.994 / 0.9986 | 0.994 / 0.9978 |
| K = 1 exponent margin / balance; their sum | 0 / 0.184; 0.184 | 0.178 / 0.019; 0.197 |
| raw minimum margin, balance (no design is removed by either; both requirements hold over the ranges) | 6.57 W, 1.02 Wh | 6.57 W, 1.02 Wh |

**Reading.** Near, not exact: exact only inside a cell with the wheels at the cap, and the
per-cell constant moves with the wheel class (5 W of wheel loss enters the margin, not the balance)
and the tracker grade; the wheel class and the power-limited corner separate the pair in the data.
The two are distinct quantities any power budget carries, a peak-power check and an orbit-energy
check; they coincide because G is linear in one tune and the loads are constants inside a cell over
the declared ranges. A system with attitude-dependent incidence or mode-dependent loads might not
share this; a fixed-load bus with body-mounted panels would. Round 3 examined the one model change
the system would justify (recharge in sunlight inside the margin): the collinearity stays. A
property of the system in its ranges, not a defect of the model.

**How the analysis identifies and simplifies it.** The method already shows it: at K = 1 one of
the pair takes the whole weight and which one flips between regimes (balance 0.184 primary, margin
0.178 stock), the sign of a near-collinear pair; at K = 3 the two sit in different terms
(`WP23-review.md`, round 3); the near-frontier association is 0.999. Missing is a stated step that
makes the flip a non-event: `case.py` reports the association of every pair of traded metrics
over the feasible designs (not only the three `association_pairs`), names the pairs above a
declared level (|Spearman| ≥ 0.99 marks one axis: the eclipse pair at 0.9994 passes, the power
pair at 0.982 / 0.988 does not), and the exponent reading sums a named pair per term: the
generated-power axis carries 0.184 and 0.197, one number in both regimes. It lives in Appendix
C.5 (a row and a sentence), D.3 and D.4 of `paper/supporting_material.ipynb`, and one sentence in
`docs/examples.md`; the paper's narrative needs nothing, its contending-set sentences already
name one of each pair.

## Options

**Pair 1 (eclipse reserve, depth of discharge).**

- A1. Clean up: the depth of discharge stays as traded metric and requirement; the reserve calc
  and requirement go; `dod_ok` enters `spec.flags`. Blast: model, coverage, oracle, one data
  regeneration (or the derived-column sub-option), contract amendment (eight traded metrics),
  `case.py`, five pinned tests, every paper number once, Appendix C.5, `docs/examples.md`.
- A2. Clean up the other way: the reserve stays (a margin in Wh, like the energy balance), the
  depth of discharge goes. Same blast as A1; the environment's 0.3 then lives inside a metric's
  definition rather than in a requirement.
- A3. Keep both; the analysis step reads the pair as one axis and the model's doc states that the
  two requirements are one inequality. Blast: `case.py`, Appendix C.5 / D.3 / D.4,
  `docs/examples.md`, tests for the new table; no model, data or contract change.

**Pair 2 (power margin, energy balance).**

- B1. Keep both; add the stated association step and read the pair's exponents as one
  generated-power axis per term. Blast: `case.py`, Appendix C.5 / D.3 / D.4, `docs/examples.md`,
  tests; no model, data, contract or paper-narrative change.
- B2. Drop one before the fit by a stated rule (for example the quantity whose requirement is the
  looser one in the ranges: the margin, minimum 6.57 W against 1.02 Wh). Blast: the traded set is
  read from the model's marks and the experiment's return tuple, so this is A1's blast radius for a
  pair the model does not define as one quantity.
- B3. Change the power model so the pair separates (incidence or loads that vary with the
  configuration). Blast: a new model round, v3 data, every downstream number; round 3's rule was
  against texture the system's purpose does not ask for.

One rule serves both pairs: the all-feasible Spearman at 0.99 puts the eclipse pair on one axis
and keeps the power pair as two; the near-frontier association (0.999 for both) does not separate
them.
