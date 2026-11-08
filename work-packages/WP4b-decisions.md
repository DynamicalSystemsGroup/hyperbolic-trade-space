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

## Acceptance (acceptance gate)

- pending `work-packages/WP4b-review.md`
