"""Tests for the abstract derivation chain (derivation/).

Chain and hygiene checks. Substitution cross-checks (test_crosscheck_L<n>) and the numeric
checks of inherited facts (I1 LP duality, I2 replication) are added alongside the lemmas.
"""

import importlib.util
import io
from contextlib import redirect_stdout

import pytest
import sympy as sp

from derivation import axioms as AX
from derivation import symbols as S
from derivation.run import CHAIN, CHAIN_NAMES, print_audit, run_chain

ALL_PRESENT = all(
    importlib.util.find_spec(f"derivation.{name}") is not None for name in CHAIN_NAMES
)


def test_full_chain_runs():
    ctx, used = run_chain(verbose=False)
    assert "S" in ctx
    for name in used:
        assert name in AX.AXIOMS


def test_each_lemma_verifies():
    ctx = {"S": S.make_symbols()}
    for lemma in CHAIN:
        lemma.derive(ctx)
        lemma.verify(ctx)  # raises AssertionError "L<n> FAIL ..." on failure
        for attr in ("TITLE", "STATEMENT", "AXIOMS_USED"):
            assert hasattr(lemma, attr), f"{lemma.__name__} missing {attr}"


def test_no_phantom_axioms():
    for lemma in CHAIN:
        for name in lemma.AXIOMS_USED:
            assert name in AX.AXIOMS, f"{lemma.__name__} cites undeclared axiom {name}"


def test_inherited_axioms_are_cited():
    inherited = AX.by_tag(AX.INHERITED)
    assert {"I1", "I2", "I3", "I4", "I5"} <= {a.name for a in inherited}
    for a in inherited:
        assert a.citation.strip(), f"inherited axiom {a.name} has no citation"


def test_regularity_and_fallbacks_state_role_and_failure_mode():
    for a in AX.by_tag(AX.REGULARITY) + AX.fallbacks():
        assert a.role.strip(), f"{a.name} has no interpretive role"
        assert a.failure_mode.strip(), f"{a.name} has no failure mode"
    assert AX.get("R1").tag == AX.REGULARITY


def test_load_bearing_symbol_assumptions_are_declared():
    """Every strong assumption in the namespace (incl. IndexedBase) is registered and licensed."""
    ns = S.make_symbols()
    registered = {(name, assumption) for (name, assumption, _) in S.SYMBOL_ASSUMPTIONS.values()}

    for tag, (name, assumption, axiom_name) in S.SYMBOL_ASSUMPTIONS.items():
        assert axiom_name in AX.AXIOMS, f"{tag}: licenses missing axiom {axiom_name}"
        obj = getattr(ns, name)
        assert getattr(obj, f"is_{assumption}", None) is True, (
            f"{tag}: {name} is not actually {assumption}"
        )

    for name, obj in vars(ns).items():
        if isinstance(obj, (sp.Symbol, sp.IndexedBase)):
            for assumption in S.STRONG_ASSUMPTIONS:
                implied_by = {"nonnegative": "positive", "nonpositive": "negative"}.get(assumption)
                if implied_by and (name, implied_by) in registered:
                    continue  # derived from a registered stronger assumption
                if getattr(obj, f"is_{assumption}", None) is True:
                    assert (name, assumption) in registered, (
                        f"{name} is {assumption} but is not registered in SYMBOL_ASSUMPTIONS "
                        f"with a licensing axiom"
                    )


def test_every_used_axiom_resolves_and_all_tags_valid():
    _, used = run_chain(verbose=False)
    for name in used:
        assert AX.get(name).tag in AX.TAGS
    for a in AX.AXIOMS.values():
        assert a.tag in AX.TAGS, f"{a.name} has invalid tag {a.tag}"
    if ALL_PRESENT:
        assert "R1" in used, "R1 is never invoked"


def test_fallbacks_are_declared():
    """Every fallback axiom is listed in the ledger; an empty list prints 'none'."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_audit([])
    out = buf.getvalue()
    assert "FALLBACKS" in out and "HEADLINE" in out
    fb = AX.fallbacks()
    if fb:
        for a in fb:
            assert a.name in out, f"fallback {a.name} missing from ledger"
            assert a.role.strip() and a.failure_mode.strip()
    else:
        assert "none" in out
    for a in AX.by_tag(AX.REGULARITY):
        assert "interpretive role" in out and "failure mode" in out and a.name in out


@pytest.mark.skipif(not ALL_PRESENT, reason="needs all ten lemma modules")
def test_every_axiom_is_used():
    _, used = run_chain(verbose=False)
    unused = [n for n in AX.AXIOMS if n not in used and n not in AX.STRUCTURAL]
    assert not unused, f"axioms never used by any lemma: {unused}"


# --- lemmas L6,L8 ---
def _run_lemma(mod_name):
    import importlib

    mod = importlib.import_module(f"derivation.{mod_name}")
    ctx = {"S": S.make_symbols()}
    mod.derive(ctx)
    mod.verify(ctx)
    return mod, ctx


def test_L6_gaussian_cumulant_abstract():
    mod, ctx = _run_lemma("lemma_06_gaussian_cumulant")
    assert {"A2", "A5", "I5"} <= set(mod.AXIOMS_USED)
    r = ctx["L6"]
    assert sp.simplify(r["mgf1"] - sp.exp(ctx["S"].sigma ** 2 * r["t"] ** 2 / 2)) == 0
    assert r["norm2"].limits[0][2] == ctx["S"].d  # symbolic d, not a number


def test_L8_chart_abstract():
    mod, ctx = _run_lemma("lemma_08_helmert_chart")
    assert "A7" in mod.AXIOMS_USED
    assert AX.get("A7").tag == AX.POSITED
    assert AX.get("A7").role.strip() and AX.get("A7").failure_mode.strip()
    r = ctx["L8"]
    assert r["shifted"] == r["Z"]
    assert r["Q"].shape == (ctx["S"].d, ctx["S"].d)


def test_L8_A7_fails_without_kernel_hypothesis():
    """Negative control: without B 1 = 0 the shifted chart keeps the c*B*1 term."""
    from sympy.matrices.expressions import OneMatrix

    S_ = S.make_symbols()
    one = OneMatrix(S_.d, 1)
    u = sp.MatrixSymbol("u_vec", S_.d, 1)
    assert (S_.B * (u + S_.c * one)).expand() != S_.B * u


def test_crosscheck_L8_helmert_realization_d4():
    """Concrete realization check only (NOT the theorem): Helmert basis at d = 4 satisfies A7."""
    d = 4
    rows = []
    for k in range(1, d):
        row = [1] * k + [-k] + [0] * (d - k - 1)
        rows.append([sp.Integer(x) / sp.sqrt(k * (k + 1)) for x in row])
    Bc = sp.Matrix(rows)
    assert Bc.shape == (d - 1, d)
    assert sp.simplify(Bc * Bc.T) == sp.eye(d - 1)
    assert sp.simplify(Bc * sp.ones(d, 1)) == sp.zeros(d - 1, 1)


# --- lemmas L3,L4 ---
from derivation import lemma_03_gradient_kkt as _L3  # noqa: E402
from derivation import lemma_04_convexity as _L4  # noqa: E402


def _ctx_l3_l4():
    ctx = {"S": S.make_symbols()}
    _L3.derive(ctx)
    _L3.verify(ctx)
    _L4.derive(ctx)
    _L4.verify(ctx)
    return ctx


def test_L3_L4_verify_abstractly_with_declared_axioms():
    ctx = _ctx_l3_l4()
    for mod in (_L3, _L4):
        assert all(a in AX.AXIOMS for a in mod.AXIOMS_USED)
    assert "R1" in _L3.AXIOMS_USED and "A3" in _L3.AXIOMS_USED
    assert "A3" in _L4.AXIOMS_USED
    assert ctx["L3"]["KKT"].rhs == _L3.LAM  # (U^T p)_{j0} = lambda
    assert ctx["L4"]["convex"] is True


def test_L3_directional_derivative_is_softmax_weighted_and_wrong_claim_fails():
    ctx = _ctx_l3_l4()
    Sy, c = ctx["S"], ctx["L3"]
    wrong = sp.Sum(c["sv"](Sy.i), (Sy.i, 1, Sy.n)) / Sy.n  # uniform weights, not softmax
    wrong_L = sp.Sum(c["sv"](_L3.L), (_L3.L, 1, Sy.n)) / Sy.n
    assert wrong != wrong_L
    assert sp.simplify(_L3.linearize(c["dJ"]) - _L3.linearize(wrong_L)) != 0


def test_L4_second_derivative_is_tau_variance_and_needs_normalization():
    ctx = _ctx_l3_l4()
    Sy, c = ctx["S"], ctx["L4"]
    # a wrong factor (tau**2 instead of tau) is rejected by the same check
    p_def, sv = ctx["L3"]["p_def"], ctx["L3"]["sv"]
    n = Sy.n
    var = (
        sp.Sum(p_def(_L3.L) * sv(_L3.L) ** 2, (_L3.L, 1, n))
        - sp.Sum(p_def(_L3.L) * sv(_L3.L), (_L3.L, 1, n)) ** 2
    )
    assert sp.simplify(_L3.linearize(c["d2"]) - Sy.tau**2 * _L3.linearize(var)) != 0


def test_L4_sign_argument_is_per_term_then_net():
    ctx = _ctx_l3_l4()
    Sy, c = ctx["S"], ctx["L4"]
    a_r, s_r = c["a_r"], c["s_r"]
    term = sp.exp(Sy.tau * a_r[Sy.i])
    assert term.is_positive is True
    # without realness the per-term sign is not available
    plain = sp.exp(Sy.tau * Sy.u[Sy.i, Sy.j])
    assert plain.is_positive is not True
    assert (s_r[Sy.i] - s_r[Sy.k]) ** 2 >= 0
