# WP4b — Decision records

Records typed by the agent (driver session). Decisions are the supervisor's.

## Pre-approval decision: OD1, fifth attribute and model coherence (2026-11-08)

- **Question put:** besides the scenario and wheel-set enrichment, should the case gain a fifth,
  cost-like attribute (keep four / illustrative power proxy / illustrative sensor cost)?
- **Supervisor (mzargham), verbatim:** "do both mass and power, sizing the solar panels impacts the
  power generation, batterys for storage, mass and power effect the controls most naturally. can also
  add star tracker grade. the whole sysml model for the satelite illustrative but it should make
  sense. and the modeling language with abstract and concrete parts lines up really nicely with
  sampling the space (configuring) then running model testing to get the measurements"
- **Disposition (driver's reading):** WP4b is re-scoped from a scenario tweak to a coherent
  illustrative satellite model: design variables include solar-panel sizing (feeding both power
  generation and inertia through the existing inertia model), battery storage (mass and energy),
  wheel class, star-tracker grade and the controller gains; attributes include both mass and power
  (a power or energy budget attribute alongside control effort), plus settling and pointing; the
  couplings reach the controls through the physics. The SysML text models the satellite with
  abstract part definitions and concrete sampled configurations, mirroring configure → model test →
  measurements. Scope to be redrafted by the PM; open decisions for the supervisor only where the
  model's meaning is at stake.


## Pre-approval decisions: SysML tooling, scale, OD1, OD2 (2026-11-08)

- **SysML tooling, verbatim:** "you may want to pull uptodate opensysml and/or sysml-toolkit packages
  and make sure you use them. you should get a lot for free. no need to go crazy just make a simple
  demonstrative cubsat config space using sysml" and, pointing at a reference repo: "this almost
  certainly does not use the latest releases so you should find them upstream but you can learn a lot
  from looking at this /Users/z/Documents/GitHub/toaster". Disposition: the configuration space is a
  SysML v2 model handled with the current `opensysml` (0.12.1 on PyPI, 2026-11-06; Open-MBEE/sysml-toolkit
  checked as optional tooling); cubesat-class satellite; the physics port's geosat pins stay as port
  verification only; `toaster` is read for usage patterns, not for its pinned versions.
- **OD1 (power attribute), verbatim:** "all of the above i think. the point was to get a rich set of
  relevant phenomena so we can discover trade offs". Disposition: four power attributes: sunlit power
  margin (W, larger better), orbit-average energy balance (Wh, larger better), eclipse energy reserve
  (Wh, larger better), peak slew power draw (W, smaller better).
- **OD2 (depth of discharge), verbatim choice:** "Metric". Disposition: eclipse depth of discharge is
  a metric (smaller is better), in addition to a `dod_ok` feasibility flag if useful.
- Resulting attribute set (d ≈ 9): settling time, pointing error, total mass, control effort, the
  four power attributes, depth of discharge; the fit, not the author, decides which contend.

## Scope approval (approval gate)

- **Document:** `work-packages/WP4b-scope-of-work.md` at d27c177 (draft 4 plus the toaster amendment).
- **Date:** 2026-11-08
- **Context:** the driver presented four gates together (accept WP2; approve WP3, WP6 and WP4b with their defaults lists as one item each) and said one line could cover all four.
- **Supervisor (mzargham), verbatim:** "okay proceed"
- **Disposition:** approved; defaults list approved as one item; open decisions: none.

## Scope amendment 1: R-14 threshold (stop rule, 2026-11-08)

- **Context:** the implementers hit the stop rule after the three allowed adjustments: median
  `torque_saturated_frac` for small wheels 0.237 against R-14's 0.25 (the PM's own default number),
  while the relative clauses pass widely (saturation ratio small/large ≈ 17, need 3; settling ratio
  3.2, need 1.25) and the richness test R-13 passes fully (contending set of size 6 incl. mass 0.266;
  agility-vs-mass −0.57; earlier tensions retained). They did not tune further.
- **Supervisor (mzargham), verbatim choice:** "Amend R-14 to its intent; keep the dataset"
- **Disposition:** R-14 is amended to its two relative clauses (saturation ratio ≥ 3, settling ratio
  ≥ 1.25) with the absolute 0.25 removed and recorded as arbitrary; no new simulation; the committed
  dataset stands; the xfail marker comes off; the review proceeds with a fresh reviewer.

## Review gaps, round 1 (review 70081fb) and amendment 2 (2026-11-08)

- **Physics item (G-2), put on its own:** 55 % of designs (93 % of small-wheel designs) exceed wheel
  momentum storage during the 90° slew; the simulator does not clip momentum; the flag was
  informational and such designs remained in the fit.
- **Supervisor (mzargham), verbatim choice:** "Enforce as feasibility"
- **Disposition (amendment 2):** `momentum_ok = False` designs are excluded from the fit (feasible =
  settled ∧ power_ok ∧ momentum_ok); the richness test R-13 reruns on the feasible set; if it fails,
  the stop rule returns to the supervisor (agility-vs-mass may collapse). No tuning.
- **Other gaps (G-1 scans and multi-constant adjustments, G-3 threshold margin, G-4 comment edit,
  G-5 small items) put as one item. Supervisor, verbatim choice:** "Fix the stale help text, accept
  the rest". Disposition: fix the `--slew-deg` help text; G-1, G-3, G-4 and the rest of G-5 accept
  as is. The whole review reruns after amendment 2 and the fix.

## Stop rule under amendment 2, and amendment 3 (2026-11-08)

- **Finding:** with momentum enforced, 346/1000 designs are feasible (small wheels 7/344); total mass
  leaves the contending set (exponent 0.000; 0 % bootstrap support); the frontier no longer spans
  wheel classes; the torque-binding ratio is 1.9 (need 3). The earlier richness result rested on
  designs that violated wheel momentum storage. Settling–effort, pointing–effort, pointing–mass, a
  strong peak-power–settling tension and a settling–mass association still hold.
- **Supervisor (mzargham), verbatim choice:** "Reopen levers for a physically consistent scenario"
- **Disposition (amendment 3):** momentum stays enforced (feasible = settled ∧ power_ok ∧ momentum_ok,
  with dod_ok as decided for OD2: a metric, not a filter, unless the scope states otherwise). The
  scenario is regenerated: slew angle and horizon chosen so that small-wheel designs stay within
  momentum storage while torque still binds, and, if needed, wheel momentum capacities made
  consistent with their torque classes (illustrative, plausibility rule). The richness test R-13/R-14
  is unchanged; the stop rule applies again after the allowed, recorded adjustments; if no scenario
  satisfies both physics and richness, that is reported as a finding (for small wheels the
  agility–mass trade appears as a feasibility boundary rather than a frontier tension) and the
  notebook says so.

## Stop rule under amendment 3, and amendment 4 (2026-11-08)

- **Finding at 30° with momentum enforced:** physics consistent (small wheels 81 % feasible; saturation
  ratio 5.1; settling ratio 1.85), but mass has exponent 0.000 and the wheel-class clauses of R-13
  fail. Reviewer's corrected explanation: wheel mass is the largest single mass lever; mass is absent
  because heavier wheels do not settle faster: 1 % settling is set by the controller's slow pole
  (log settling vs log(Kd/Kp) correlation 0.993 for large wheels), so wheel class separates settling
  only at the most aggressive gains.
- **Supervisor (mzargham), verbatim choice:** "One physics-justified lever: slew-time attribute"
- **Disposition (amendment 4):** add an actuator-limited agility attribute, the slew time to first
  entry into a tolerance band (e.g. 1°), alongside settling, with the reasoning written before any
  simulation; recorded as adjustment 4; richness test R-13 unchanged in its clauses (mass must enter
  the contending set and settling- or slew-time-vs-mass across wheel classes); if it still fails, the
  finding is accepted and the notebook reports wheel class as a feasibility boundary. Probe-note
  defects G-2 and G-3 fixed in the same pass.

## Stop rule under amendment 4, and amendment 5 (2026-11-08)

- **Finding after amendment 4:** with momentum enforced at 30°, wheel class is a feasibility boundary
  (small wheels lose 19.2 % of designs to momentum; large 0 %); slew time to a 1° band tracks settling
  (correlation 0.947) and Kd/Kp (0.998 for large wheels); mass exponent 0.000; "not found with these
  measures and this gain box", not "cannot exist" (wheel class separates agility only at Kd/Kp ≲ 5).
- **Question put:** record the finding and accept, or spend another lever (aggressive-gain regime;
  momentum headroom attribute; peak slew rate; wheel mass scaled with capacity).
- **Supervisor (mzargham), verbatim:** "try both new levers then report back"
- **Disposition (amendment 5):** two further levers, each tried and recorded separately and then
  together: (i) resample the gain box toward the aggressive regime (Kd/Kp ≲ 5) where wheel class
  separates agility; (ii) add momentum headroom (peak momentum / capacity) as an attribute so wheel
  class enters through storage. Momentum stays enforced; the richness test R-13 is unchanged in its
  clauses; reasoning written before simulation; report the outcome of each lever and the combination;
  the stop rule applies after that, and the finding is then recorded if R-13 still fails.

## Amendment 5 outcome and review gaps, round 4 (review 2258281, 2026-11-08)

- **Outcome:** lever (i), the aggressive-gain regime (Kp 0.2–2.0, Kd 0.3–1.5; median Kd/Kp ≈ 1.06),
  passes the full richness test (contending set of 6 with mass 0.223 and bootstrap support 1.00;
  settling–mass −0.50; slew-time–mass −0.45; R-14 13.1 / 4.85); lever (ii), momentum utilisation,
  alone does not; lever (iii) adds nothing needed. On the baseline gain box the null finding stands.
  The failure at amendment 4 came from the gain box, not from the case or the measures.
- **G-1, standing dataset. Supervisor (mzargham), verbatim choice:** "Both, as two regimes"
- **Disposition:** the aggressive-gain dataset (`adcs_designs_cubesat_gains.csv`) is the primary case
  dataset (R-13 met); the baseline (`adcs_designs_cubesat.csv`) is kept as the regime comparison;
  WP7 shows that the wheel-class tension appears only when the loop is driven hard enough for the
  wheel to be the bottleneck (shape of the trade space conditional on the operating regime).
- **G-3..G-8. Supervisor, verbatim choice:** "Fix G-6 note, G-5 to follow-up, accept the rest"
- **Disposition:** G-6 fix before acceptance (complete the prediction-miss list in the probe note:
  settling class ratio, mass as the largest weight, lever (iii) outcome); G-5 follow-up item:
  investigate run-to-run nondeterminism of the generator on identical code (likely adaptive-step
  integration sensitivity in the saturated-fraction and continuous columns) instead of tolerating a
  10 % tolerance; G-3, G-4, G-7, G-8 accept as is (the finding is stated as conditional on the
  stiff-loop regime). The whole review reruns after the note fix.

## Review gaps, round 5 (review 2a4051e, fifth pass, against amendment 6)

- Items: G-A prediction-miss list omits two lever-(i) predictions; G-B the baseline regime test
  asserts one-sided thresholds, not recorded values within bands; G-C stale section labels and a
  stale DRAFT status line.
- **Supervisor (mzargham), verbatim choice:** "Fix all three"
- **Disposition:** fix G-A, G-B, G-C; the whole review reruns once; then the acceptance gate.

## Review gaps, round 6 (review 3f5a00f, sixth pass)

- Items: G-D factual typo in the probe note's primary-dataset paragraph ("Kp 0.3 to 3"; committed box
  Kp 0.2–2.0, Kd 0.3–1.5), which WP7 reads; G-E residual stale labels and the scope status line.
- **Disposition (driver, maintenance):** both corrected by the driver in one commit before presenting
  the gate (note paragraph and labels fixed; status line records the approval and six amendments);
  presented to the supervisor with the acceptance gate, who may ask for a rerun instead.

## Acceptance (acceptance gate)

- Review: `WP4b-review.md` (sixth pass, 3f5a00f), recommends acceptance; G-D/G-E corrected by the
  driver (3cd043d) before the gate.
- Acceptance act named in the scope: verbal acceptance in chat.
- **Date:** 2026-11-08
- **Supervisor (mzargham), verbatim:** "accept 4b and approve 7 and 8. given how long its been remember to send the notebook author to look at the acds-lifecycle-demo and hc-marimo repos and pages sites to get a sense of my style"
- **Status:** accepted. WP4b is done.

## Follow-up candidates

- **Generator nondeterminism (review G-5).** Investigate the run-to-run nondeterminism of the dataset
  generator on identical code (likely adaptive-step integration sensitivity in the saturated-fraction
  and continuous columns; CI differed from the author's platform and from itself, 3.8 % then 6.2 % on the
  saturated fraction). The 10 % saturated-fraction tolerance (and rtol 1e-3) for the aggressive box in
  `tests/test_cubesat_model.py` is a stopgap, to be replaced by a fixed-step or tighter-tolerance
  integration or a documented cause.
- **Unused levers from the review observations:** peak slew rate as an attribute; wheel mass scaled
  with capacity; a milder gain box between the baseline and the aggressive one (to map where the
  wheel-class tension appears); the headroom difference (capacity minus peak) form as an attribute.
