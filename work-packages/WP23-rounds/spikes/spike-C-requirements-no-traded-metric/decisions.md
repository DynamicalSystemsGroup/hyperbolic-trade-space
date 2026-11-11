# Spike C — decision record (the three requirements that read no traded metric)

## Origin (2026-11-10; the supervisor, relayed by the driver)

Said of the paper's Figure 3, the behavioural view, whose box "requirements that read no traded metric" holds
`BatteryPeakPowerRequirement`, `MomentumRequirement` and `PowerRequirement`. **Supervisor (mzargham), verbatim:**
"this one brings to mind a modeling question. why are these requirements not related to metrics. my intuition is
that these metrics should be in the trade and should into the existing groupings. my recommendation is keep but also
use it as view ensure our model and our study are well matched. you can kick off a modeler research spike then a
model developer to refine the model based on the modelling spike."

**Disposition (the driver, through the PM).** A modeller research spike, read-only on the model, data, paper and
docs (this folder). It feeds the scope of a model-developer package. The box stays in the view.

## The readout in three lines

- `MomentumRequirement`: momentum headroom (capacity / peak momentum) is a candidate. It is positive on the feasible
  set, spread over a factor 18 / 97, and a near-duplicate of no traded metric (largest |Spearman| 0.62). It enters the
  K = 1 fit at 0.154 / 0.229 and changes the baseline regime's leading trade. Group: controls.
- `PowerRequirement`: available power is not a candidate. It is one axis with the energy balance (Spearman +0.9996 /
  +0.9997), every in-range configuration meets it, and added to the fit it takes the energy balance's exponent.
  Group: power and energy.
- `BatteryPeakPowerRequirement`: the battery peak power ratio is not a candidate. Every in-range configuration meets
  it (20 W against at most 19.4 W), it tracks the depth of discharge (+0.970 / +0.975), and the fit gives it exponent
  0. Group: power and energy.

## Open decision D-1: which quantities become traded metrics

The problem: the box shows one quantity the model bounds that the study does not trade (momentum headroom) and two
the study already trades under another name. Adding a metric is a problem change (`WP23-decisions.md`, OD7) and costs
a data gate. The cost list is in `README.md` (5), and the paper's baseline-regime trade moves.

- (a) Add the momentum headroom as the ninth traded metric (MoP, controls), in one model-developer package with a data
  gate. The power and battery peak power requirements stay requirements only.
- (b) Add none. The box stays as the honest view, and the caption says why each requirement is there.
- (c) Add all three (eleven traded metrics). The association step then names available power and energy balance one
  axis, and the battery peak power ratio carries no exponent.

## Open decision D-2: how the box serves as the check the supervisor asked for ("use it as view ensure our model and our study are well matched")

The problem: today the box lists requirements without saying whether the study covers their quantity. Each of the
three has a different reason, and only the momentum requirement's points to a gap.

- (a) The caption names each requirement in the box with its reason, one clause each: holds at every in-range
  configuration, one axis with a traded metric (with its Spearman), or not traded. The coverage generator prints the
  same reason from a computed check, and a test fails when a requirement in the box has no stated reason.
- (b) The box and caption stay as they are, and this readout is the record.

## The driver's decisions (2026-11-10, 23:05)

- **D-1 (a), executed inside Track B.** The momentum headroom becomes the ninth traded metric (MoP, controls); the
  power and battery peak power requirements stay requirements only. It is not a package of its own: the supervisor's
  direction on the cost model (`WP27-decisions.md`, "H-2": a fleet-size configuration variable, per-part pricing
  curves, two pricing metrics) is the same kind of change, so the two land in one model revision with one data gate,
  one container re-run, one key version and one cascade review, after the B2 economics spike reports and the driver
  takes stage (2) on both readouts together.
- **D-2 (a).** The box becomes the check the supervisor asked for: the caption names each requirement in it with its
  computed reason (holds at every in-range configuration; one axis with a named traded metric and its Spearman; not
  traded), the coverage generator prints the same reason, and a test fails on a requirement in the box with no stated
  reason. Lands with the revision.
- **For the supervisor, in the morning, one question:** the revision changes the baseline regime's leading trade (from
  control effort against settling time to momentum headroom, mass and settling time), which is a changed conclusion of
  the case; he confirms it before stage (3) builds.
