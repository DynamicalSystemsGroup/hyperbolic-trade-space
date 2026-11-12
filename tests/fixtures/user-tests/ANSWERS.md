# Planted facts (for the triage only; never given to a cell)

Conditioned as: larger-is-better after `LogAffinePreconditioner(orientation=...)`, `temperature=20`.

## plain_table.csv

Planted exponents on the four metrics: `[0.5, 0.5, 0, 0]`. The trade-off pair is `strength_mpa` and
`weight_kg` (weight inverted: smaller is better). `stiffness_gpa` and `cost_usd` are independent of
the frontier. Conditioning: orientation `[1, -1, 1, -1]` on the four numeric columns; `sample` and
`batch` are not attributes. Expected fit: exponents about `[0.48, 0.50, 0.01, 0.01]`; the
`contending_set` at the exact maximum may list a third metric (`cost_usd`) with a negligible exponent,
so the exponents, not the set alone, show the pair; the association of the pair is about -1.0.

## pump_table.csv

The model's calculations give flow and head by affinity scaling and shaft power as hydraulic power
over efficiency, so flow, head and shaft power are bound by one relation. Conditioning: orientation
`[1, 1, -1, -1]` on `flow_lps`, `head_m`, `power_kw`, `mass_kg`. Expected: a trilemma
(`contending_set` `[0 1 2]`), exponents about `[0.28, 0.23, 0.49, 0.00]`: flow, head and shaft power
trade; mass takes no part in the frontier (exponent 0), though its association with the others is
strong (about -0.9 with flow, -0.7 with head) because a larger impeller raises both. The design
variable columns (`diameter_m`, `speed_rpm`, `width_ratio`) and `design_id` are not attributes.
