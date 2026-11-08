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

## Scope approval (approval gate)

- pending (draft 2)
