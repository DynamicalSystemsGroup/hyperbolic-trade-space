# Note: porting the ADCS simulation for the case study (WP4)

Source repo: `/Users/z/Documents/GitHub/adcs-lifecycle-demo` (DynamicalSystemsGroup/ADCS-lifecycle-demo).
Explored 2026-11-07. Copy only numpy/scipy code; carry the source LICENSE notice in the header of
`examples/adcs/adcs_sim.py`. Do not depend on rdflib, sympy, opensysml or Flexo.

## What to copy

- `analysis/numerical.py`: `SimConfig` (dataclass: Jxx, Jyy, Jzz, Kp, Kd, n_orbital, max_torque,
  max_momentum, t_span, max_step=0.5, q0, omega0), `SimResult` with `.summary()` (final_error_deg,
  peak_error_deg, settling_time_s = last time error exceeds 1 % of initial, peak_wheel_momentum =
  ‖∫tau_ctrl dt‖, peak_control_torque, final_omega_norm, duration_s, n_steps), `simulate_adcs`
  (scipy `solve_ivp` RK45, rtol 1e-10, atol 1e-12, max_step 0.5; full quaternion kinematics + Euler
  equations with diagonal J; linearised gravity-gradient torque; PD law tau = -Kp/2·q_vec - Kd·ω
  clipped to max_torque; wheel momentum observed, not enforced). `make_config_from_params` imports a
  sympy inertia; replace with the numeric `inertia_tensor` below. `run_step_response` = 10° slew
  about X for 360 s.
- `analysis/symbolic.py` L99–143: composite inertia = box bus + two thin-plate panels offset along
  Y (center at Ly/2 + span/2) + disk antenna offset along Z, parallel-axis theorem. Port numerically.
  L199–275: gravity-gradient torque τ_gg = 3 n² |ΔJ| · 0.1°, steady-state error θ_ss = 4 τ_gg,max / Kp
  (effective stiffness Kp/4 on θ), star-tracker floor = stAccuracy/3600 deg, linear settling
  estimate −4 / worst Re(λ). Note the known units issue in `wheel_momentum_bound_symbolic`
  (N·m, not N·m·s) — do not port that function.

## Baseline parameters (from `structural/parameters.ttl`)

| name | value | unit |
|---|---|---|
| mass | 550.0 | kg |
| bodyLength / bodyWidth / bodyHeight | 0.90 / 1.00 / 1.10 | m |
| orbitalRate | 7.2722e-05 | rad/s |
| panelSpan / panelChord / panelMass (×2) | 2.50 / 0.90 / 30.0 | m, m, kg |
| antennaDiameter / antennaOffset / antennaMass | 0.80 / 0.75 / 18.0 | m, m, kg |
| maxTorque / maxMomentum / wheelMass | 0.1 / 4.0 / 2.5 | N·m, N·m·s, kg |
| stAccuracy / stUpdateRate / stMass | 5.0 / 4.0 / 2.0 | arcsec (1σ), Hz, kg |
| gyroARW / gyroBias / controlBandwidth / imuMass | 0.0017 / 0.0001 / 1.0 / 0.5 | rad/s/√Hz, rad/s, Hz, kg |
| Kp / Kd | 1.0 / 10.0 | N·m/rad, N·m·s/rad |

Resulting inertia ≈ (327.14, 107.48, 303.45) kg·m².

## Regression pins (from the source `tests/test_sysml_evidence.py`, ±0.2 s)

X-axis 10° slew, 360 s horizon, tight tolerances: (Kp, Kd) = (4, 30) → 78.0 s; (8, 30) → 87.4 s;
(4, 25) → 120.5 s. Baseline (1, 10) → 310.6 s (source repo pin; reproduced 310.626 s on 2026-11-08; an earlier planning note said 201.6 s, which was wrong). Measured cost ≈ 0.11 s per design at 360 s.

## What the source does not have (so the case must add)

Only Kp, Kd vary; no categorical hardware choice, no mass/power/cost attributes, no Monte Carlo or
sampling code. The case adds wheel class and star-tracker grade (categorical), MC perturbation of
panel/antenna mass, and the attributes listed in the spec §8. Settling time is quantized by
`max_step` and censored at `t_end`; keep a `settled` flag. Peak momentum varies ~4 % between
max_step 0.5 and 2.0; use 0.5 for the dataset and fast settings only in tests.

## Other conventions worth copying

- Notebook plots: matplotlib only; axis colours in the JAXA notebook: X `#1f77b4`, Y `#2ca02c`,
  Z `#9467bd`; limit colour `#d62728`.
- The SysML v2 text (`sysml/satellite.sysml`) documents the design; the Python reads TTL
  parameters. Our `extended_design_space.sysml` is documentation only.
