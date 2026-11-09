# hyperbolic-trade-space

Python package `hyperbolic_trade_space` (import alias `hts`); the method is the *posynomial invariant form*.

Learn the shape of a design trade space. From noisy, biased observations of a design problem
(configuration variables and empirically assessed attributes), the method learns a hyperbolic
"space": a monomial, later posynomial, frontier V(m) = Π m_j^{w_j} whose unit level set is the
Pareto frontier, together with an invertible coordinate chart (position along the frontier, and
log V, the energy differential to it). It is a scikit-learn-compatible unsupervised estimator, with
SymPy-verified derivations and an ADCS trade-study case.

Status: WP0 (setup) complete; the package code arrives in later work packages. See
`work-packages/README.md` for the plan and `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`
for the design.

## Quickstart

```bash
uv sync          # reproducible environment from uv.lock (Python 3.12)
uv run pytest    # tests
```

## Layout

- `src/hyperbolic_trade_space/` — the package
- `derivation/` — SymPy axiom and lemma scripts (WP1)
- `examples/adcs/` — the ADCS trade-study case (WP4, WP7)
- `docs/` — mathematics, preconditioning, API, literature; site in WP8
- `work-packages/` — scopes, reviews and decision records per work package
