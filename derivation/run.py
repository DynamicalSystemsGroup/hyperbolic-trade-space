"""Run the full abstract derivation chain L1 -> L16, then print the assumption audit.

    uv run python derivation/run.py

The chain is built from the lemma module names in ``CHAIN_NAMES``; modules whose file does
not exist yet are skipped so partial states run. Each lemma derives, verifies and reports the
axioms it used. The closing AUDIT separates what was DERIVED (SymPy-verified for symbolic
d, n, K) from POSITED, INHERITED and REGULARITY conditions and the FALLBACKS.
"""

import importlib
import importlib.util
import os
import sys

# Make `import derivation.*` work whether run as `python derivation/run.py` or `-m`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from derivation import axioms as AX
from derivation.symbols import make_symbols

CHAIN_NAMES = [
    "lemma_01_homogeneity",
    "lemma_02_shift",
    "lemma_03_gradient_kkt",
    "lemma_04_convexity",
    "lemma_05_lse_lme",
    "lemma_06_gaussian_cumulant",
    "lemma_07_elasticities",
    "lemma_08_helmert_chart",
    "lemma_09_pullback",
    "lemma_10_extension",
    "lemma_11_pareto",
    "lemma_12_facet_gap",
    "lemma_13_margin",
    "lemma_14_assignment_stable",
    "lemma_15_descent",
    "lemma_16_soft_fit_alternation",
]


def load_chain(names=CHAIN_NAMES):
    """Import the lemma modules whose files exist (skip the rest), in order."""
    mods = []
    for name in names:
        if importlib.util.find_spec(f"derivation.{name}") is not None:
            mods.append(importlib.import_module(f"derivation.{name}"))
    return mods


CHAIN = load_chain()


def lemma_number(mod):
    """L-number from the module name, e.g. lemma_03_x -> 3."""
    return int(mod.__name__.split(".")[-1].split("_")[1])


def run_chain(verbose=True):
    """Execute the chain, threading a shared context. Returns (ctx, axioms_used)."""
    ctx = {"S": make_symbols()}
    used = []
    for lemma in CHAIN:
        lemma.derive(ctx)
        lemma.verify(ctx)
        for name in lemma.AXIOMS_USED:
            if name not in used:
                used.append(name)
        if verbose:
            axset = ", ".join(lemma.AXIOMS_USED) if lemma.AXIOMS_USED else "(algebra only)"
            print(f"  [L{lemma_number(lemma)}] PASS  {lemma.TITLE}")
            print(f"         {lemma.STATEMENT}")
            print(f"         axioms: {axset}")
    return ctx, used


def _print_conditions(entries):
    for a in entries:
        print(f"  - {a}")
        print(f"      interpretive role: {a.role}")
        print(f"      failure mode:      {a.failure_mode}")


def print_audit(used):
    print()
    print("=" * 72)
    print("ASSUMPTION AUDIT - what the derivation actually leans on")
    print("=" * 72)

    def sel(tag):
        return [AX.get(n) for n in sorted(used) if AX.get(n).tag == tag and not AX.get(n).fallback]

    print("\nDERIVED here (SymPy-verified for symbolic d, n, K):")
    for lemma in CHAIN:
        print(f"  - L{lemma_number(lemma)}: {lemma.TITLE}")

    print("\nPOSITED (modelling choices we declare):")
    for a in sel(AX.POSITED):
        print(f"  - {a}")

    print("\nINHERITED (external theorems: USED and CITED, not proven here):")
    for a in sel(AX.INHERITED):
        print(f"  - {a}")

    solver = [AX.get(n) for n in AX.SOLVER_LEVEL]
    print("\nINHERITED, solver level (cited by the K > 1 solver, not consumed by a lemma):")
    _print_conditions(solver)

    print("\nINHERITED, cited context (recorded remarks; no proof step consumes them):")
    for name, reason in AX.CITED_CONTEXT.items():
        print(f"  - {AX.get(name)}")
        print(f"      why not consumed: {reason}")

    regularity = AX.by_tag(AX.REGULARITY)
    print("\nREGULARITY (interpretive conditions; hypotheses, not defects):")
    _print_conditions(regularity)

    fb = AX.fallbacks()
    print("\nFALLBACKS (steps not proved abstractly, stated as conditions):")
    if fb:
        _print_conditions(fb)
    else:
        print("  none")

    print()
    print("-" * 72)
    print("HEADLINE: results are proved for symbolic d, n, K (abstract spaces), not at chosen")
    print("sizes. The frontier reading of the balanced point requires R1.")
    for a in regularity + fb:
        print(f"  {a.name}: buys: {a.role}")
        print(f"  {a.name}: when it fails: {a.failure_mode}")
    if not fb:
        print("  No fallbacks: every step was proved abstractly.")
    print("-" * 72)


def main():
    print("=" * 72)
    print("Posynomial invariant form - axiom-explicit derivation (L1 -> L16)")
    print("=" * 72)
    print()
    _, used = run_chain(verbose=True)
    print_audit(used)
    print("\nALL LEMMAS PASS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
