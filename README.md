# hyperbolic-trade-space

Python package `hyperbolic_trade_space` (import alias `hts`); the method is the *posynomial invariant form*.

The docsite's [Home page](docs/index.md) says what the method does and where to start.

Status: a 0.1 release candidate in preparation on `dev`. See `work-packages/README.md` for the
packages and their state and `docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md`
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
