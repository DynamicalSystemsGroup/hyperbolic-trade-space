"""The proof-map checker (derivation/proofmap.py) and the tagged lemma scripts (WP10, R-28, R-29).

Every proof step is a tagged line of a lemma script; the checker fails on any drift. These tests
check the committed record, the equality of imported, applied and declared ledger names, and (on a
scratch copy of ``derivation/``, so the repository is never touched) that breaking a script step,
a prose step or the order, an untagged proof step and an unmatched import each make the checker
fail, naming the step.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from derivation import axioms as AX
from derivation import proofmap
from derivation.run import CHAIN, CHAIN_NAMES, lemma_number

# Slow module: shared fixtures cost minutes (verification in tiers); not in the fast suite.
pytestmark = pytest.mark.slow

ROOT = Path(__file__).resolve().parent.parent
DERIVATION = ROOT / "derivation"


def _record():
    return json.loads((DERIVATION / proofmap.RECORD_NAME).read_text())


@pytest.fixture
def scratch(tmp_path):
    """A scratch copy of derivation/ (the repository is untouched); returns its package dir."""
    dest = tmp_path / "derivation"
    shutil.copytree(DERIVATION, dest, ignore=shutil.ignore_patterns("__pycache__"))
    return dest


def run_checker(scratch_pkg, *args):
    """Run ``python -m derivation.proofmap`` from the scratch copy's parent directory."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-m", "derivation.proofmap", *args],
        cwd=scratch_pkg.parent,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return proc.returncode, proc.stdout + proc.stderr


def edit(scratch_pkg, filename, old, new, count=1):
    path = scratch_pkg / filename
    text = path.read_text()
    assert text.count(old) == count, f"{filename}: expected {count} of {old!r}"
    path.write_text(text.replace(old, new))


# ---------------------------------------------------------------- the committed record passes


def test_checker_passes_on_the_committed_record(capsys):
    assert proofmap.main([]) == 0
    assert "PROOF MAP OK" in capsys.readouterr().out


def test_checker_passes_on_an_untouched_scratch_copy(scratch):
    code, out = run_checker(scratch)
    assert code == 0, out
    assert "PROOF MAP OK" in out


def test_record_holds_every_step_with_tag_prose_and_code():
    rec = _record()
    assert len(rec["lemmas"]) == len(CHAIN_NAMES)
    for fname, lemma in rec["lemmas"].items():
        assert lemma["steps"], fname
        for pos, step in enumerate(lemma["steps"], start=1):
            assert step["tag"] == f"L{lemma['number']}.{pos}"
            assert step["prose"].strip() and step["code"].strip()
            assert step["kind"] in ("computed", "axiom", "result")
            assert (step["kind"] == "result") == bool(step["results"])
            assert (step["kind"] == "axiom") == (bool(step["applies"]) and not step["results"])
            assert len(step["fingerprint"]) == 64
            assert step["result"]
    assert set(rec["ledger"]) == set(AX.AXIOMS)


def test_every_lemma_file_is_in_the_record_in_chain_order():
    assert [f"{n}.py" for n in CHAIN_NAMES] == list(_record()["lemmas"])


# ------------------------------------- imports == applied == AXIOMS_USED (and the ledger itself)


def test_imported_applied_and_declared_ledger_names_are_the_same_set():
    rec = _record()["lemmas"]
    for mod in CHAIN:
        lemma = rec[f"{mod.__name__.split('.')[-1]}.py"]
        assert lemma["number"] == lemma_number(mod)
        applied = {name for step in lemma["steps"] for name in step["applies"]}
        assert set(lemma["imports"]) == applied == set(mod.AXIOMS_USED) == set(lemma["axioms_used"])
        for name in lemma["imports"]:
            assert name in AX.AXIOMS


def test_every_ledger_entry_is_an_importable_name_with_a_form_or_a_named_proposition():
    for name, entry in AX.AXIOMS.items():
        assert getattr(AX, name) is entry, f"{name} is not exposed as a module-level name"
        assert entry.has_form(), f"{name} has neither a SymPy form nor a named proposition"
        assert entry.relations() or entry.objects or entry.proposition
        if entry.proposition:
            assert not entry.relations() and entry.statement.strip()
        if entry.tag == AX.INHERITED:
            assert entry.citation.strip()


def test_ledger_fingerprints_are_stable_text_hashes():
    first, second = AX.fingerprints(), AX.fingerprints()
    assert first == second and set(first) == set(AX.AXIOMS)
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in first.values())
    assert len(set(first.values())) == len(first)  # distinct entries, distinct hashes


def test_a_result_sharing_a_file_owns_its_own_steps():
    """L14 proves Proposition 3 and the approximate-certificate corollary in one file: one tag
    sequence, two owners."""
    lemma = _record()["lemmas"]["lemma_14_assignment_stable.py"]
    owners = {s["tag"]: s["result"] for s in lemma["steps"]}
    assert set(owners.values()) == {"Proposition 3", "Approximate-certificate corollary"}
    assert len({s["tag"] for s in lemma["steps"]}) == len(lemma["steps"])
    assert (
        owners["L14.19"]
        == owners["L14.20"]
        == owners["L14.10"]
        == "Approximate-certificate corollary"
    )
    assert owners["L14.11"] == "Proposition 3"


# ----------------------------------- each kind of breakage makes the checker fail, naming the step


def test_a_changed_script_step_fails_naming_the_step(scratch):
    edit(scratch, "lemma_02_shift.py", 'assert r["term_diff"] == 0,', 'assert r["term_diff"] == 1,')
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py L2.4" in out and "script line changed" in out
    assert "L2.5" not in out  # only the broken step is named


def test_a_changed_prose_step_fails_naming_the_step(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "# [L2.4] per term, tau sum_j w_j (u_ij + c) - (tau s_i + tau c) is 0",
        "# [L2.4] per term, the shift is absorbed",
    )
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py L2.4" in out and "prose changed" in out


def test_swapped_tags_fail_naming_the_steps(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.4] per term", "# [L2.5] per term")
    edit(scratch, "lemma_02_shift.py", "# [L2.5] J_tau(U", "# [L2.4] J_tau(U")
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py L2.5" in out and "out of order" in out
    assert "lemma_02_shift.py L2.4" in out


def test_a_duplicate_tag_fails(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.5] J_tau(U", "# [L2.4] J_tau(U")
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py L2.4" in out and "duplicate tag" in out


def test_a_gap_in_the_numbering_fails(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.5] J_tau(U", "# [L2.9] J_tau(U")
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py L2.9" in out and "out of order" in out


def test_a_lemma_with_zero_tags_fails(scratch):
    path = scratch / "lemma_02_shift.py"
    path.write_text(re.sub(r"^\s*# \[L2\.\d+\].*\n", "", path.read_text(), flags=re.M))
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py: the lemma has no tagged steps" in out


def test_an_untagged_assert_in_verify_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        '    S = ctx["S"]\n    r = ctx["L2"]\n',
        '    S = ctx["S"]\n    r = ctx["L2"]\n    assert S.d.is_integer\n',
    )
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_02_shift.py" in out and "untagged assert in verify" in out


def test_removing_a_tag_from_a_step_fails(scratch):
    """An assert in verify that lost its tag is an untagged proof step, detected by name."""
    edit(
        scratch,
        "lemma_02_shift.py",
        "    # [L2.4] per term, tau sum_j w_j (u_ij + c) - (tau s_i + tau c) is 0\n",
        "",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "untagged assert in verify" in out


def test_a_ledger_import_that_no_step_applies_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "from derivation.axioms import A1, A2, A3",
        "from derivation.axioms import A1, A2, A3, I1",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py" in out and "imported ledger names" in out


def test_a_ledger_entry_applied_but_not_listed_in_axioms_used_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        'AXIOMS_USED = ["A1", "A2", "A3"]',
        'AXIOMS_USED = ["A1", "A2"]',
    )
    code, out = run_checker(scratch)
    assert code != 0 and "differ from AXIOMS_USED" in out


def test_a_ledger_entry_used_on_an_untagged_line_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "    s_i = sp.Sum(w[j] * u[i, j], (j, 1, d))\n",
        "    s_i = sp.Sum(w[j] * u[i, j], (j, 1, d))\n    _unused = A2.relations()\n",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "used on an untagged line" in out


def test_importing_a_name_that_is_not_a_ledger_entry_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "from derivation.axioms import A1, A2, A3",
        "from derivation.axioms import A1, A2, A3, A99",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "A99" in out and "not a ledger entry" in out


def test_a_changed_ledger_entry_fails(scratch):
    edit(
        scratch,
        "axioms.py",
        "the fit temperature is positive: tau > 0",
        "the fit temperature is nonnegative: tau >= 0",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "axioms.py A3" in out and "ledger entry" in out


def test_a_ledger_entry_without_a_form_fails(scratch):
    """Dropping a named proposition's declaration leaves an entry with no form at all."""
    edit(
        scratch,
        "axioms.py",
        'not at chosen sizes)",\n        proposition=True,\n',
        'not at chosen sizes)",\n',
    )
    code, out = run_checker(scratch)
    assert code != 0 and "axioms.py A0" in out and "no SymPy form" in out


def test_the_order_of_steps_in_the_file_is_the_tag_order(scratch):
    """Moving a tagged line past its successor reorders the steps, so the tags are out of order."""
    path = scratch / "lemma_02_shift.py"
    text = path.read_text()
    a = re.search(r"    # \[L2\.4\].*\n.*\n.*\n.*\n", text)  # the L2.4 comment and its assert
    assert a
    block3 = a.group(0)
    text = text.replace(block3, "", 1)
    # put the L2.4 block after the last step (the end of verify)
    path.write_text(text.rstrip("\n") + "\n" + block3)
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py" in out


# --------------------------------------------------------------------- refreshing is explicit


@pytest.mark.slow
def test_update_rewrites_the_record_and_prints_the_steps_that_moved(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        'assert r["term_diff"] == 0,',
        'assert r["term_diff"] == 0 and True,',
    )
    code, _ = run_checker(scratch)
    assert code != 0  # drift is not silent
    code, out = run_checker(scratch, "--update")
    assert code == 0 and "lemma_02_shift.py L2.4" in out  # the diff names exactly the moved step
    assert "L2.5" not in out
    code, out = run_checker(scratch)
    assert code == 0, out


def test_update_refuses_a_broken_proof_map(scratch):
    edit(scratch, "lemma_02_shift.py", "# [L2.5] J_tau(U", "# [L2.4] J_tau(U")
    code, out = run_checker(scratch, "--update")
    assert code != 0 and "not updated" in out


# ------------- principle 1 (WP10 Amendment 2): a listed entry is a dependency; negative controls
# Each licensed operation of the lemma scripts is called here with the entry withheld (or the wrong
# one given) and must fail, as L8's chain fails without I6. The controls use the shared symbols.

import sympy as sp  # noqa: E402

from derivation import symbols as _symbols  # noqa: E402
from derivation.axioms import A1, A2, A3, A4, A5, A6, A7, F5, F10, F12, I1, I5, I6, R2  # noqa: E402
from derivation.licence import LicenceError, licensed_power, log_expand  # noqa: E402
from derivation.sumtools import product_to_exp_sum  # noqa: E402

_S = _symbols.make_symbols()


def _prod(base):
    return sp.Product(base ** _S.w[_S.j], (_S.j, 1, _S.d))


def test_a_forced_log_with_no_licence_fails():
    with pytest.raises(LicenceError):
        product_to_exp_sum(_prod(_S.m[_S.j]))  # L1.2 without A1
    with pytest.raises(LicenceError):
        log_expand(sp.log(_S.m[_S.j]))


def test_the_power_of_m_needs_A1_not_another_entry():
    product_to_exp_sum(_prod(_S.m[_S.j]), A1)
    for wrong in (A2, A3, A4, A6):
        with pytest.raises(LicenceError):
            product_to_exp_sum(_prod(_S.m[_S.j]), wrong)  # L1.2, L1.3, L1.8, L10.8


def test_L2_log_of_the_shifted_sum_needs_A1_A2_and_A3_together():
    i, j, n, d, w, u, tau = _S.i, _S.j, _S.n, _S.d, _S.w, _S.u, _S.tau
    total = sp.exp(tau * _S.c) * sp.Sum(sp.exp(tau * sp.Sum(w[j] * u[i, j], (j, 1, d))), (i, 1, n))
    log_expand(sp.log(total / n), A1, A2, A3)
    for withheld in ((A2, A3), (A1, A3), (A1, A2)):  # u, w or tau no longer declared real
        with pytest.raises(LicenceError):
            log_expand(sp.log(total / n), *withheld)


def test_L5_log_split_needs_F5_for_the_real_scores_and_A3_for_tau():
    i, n, s, tau = _S.i, _S.n, _S.s, _S.tau
    lse_minus_lme = sp.log(sp.Sum(sp.exp(tau * s[i]), (i, 1, n))) / tau
    log_expand(lse_minus_lme, A3, F5)
    for wrong in ((A3,), (F5,), (A3, A2)):
        with pytest.raises(LicenceError):
            log_expand(lse_minus_lme, *wrong)


def test_L6_log_of_the_mgf_factor_needs_A2_A3_and_A5():
    factor = sp.exp(_S.sigma**2 * (_S.tau * _S.w[_S.j]) ** 2 / 2)
    log_expand(sp.log(factor), A2, A3, A5)
    for wrong in ((A3, A5), (A2, A5), (A2, A3)):
        with pytest.raises(LicenceError):
            log_expand(sp.log(factor), *wrong)


def test_L7_power_of_V_needs_A1_and_A2():
    w0 = _S.w[sp.Symbol("j0", integer=True)]
    logV = sp.Sum(_S.w[_S.j] * A1.real_base("u_pt")[_S.j], (_S.j, 1, _S.d))
    licensed_power(sp.exp(logV) ** (-1 / w0), A1, A2)
    for wrong in ((A1,), (A3,)):  # w is not declared real; or the wrong entries altogether
        with pytest.raises(LicenceError):
            licensed_power(sp.exp(logV) ** (-1 / w0), *wrong)
    unreal = sp.Sum(_S.w[_S.j] * sp.IndexedBase("u_pt")[_S.j], (_S.j, 1, _S.d))
    with pytest.raises(LicenceError):  # an undeclared (not real-valued) log-metric family
        licensed_power(sp.exp(unreal) ** (-1 / w0), A1, A2)


def test_L9_log_of_the_conditioned_attribute_needs_A4():
    raw = sp.IndexedBase("r")
    prod = sp.Product((_S.a[_S.j] + raw[_S.j]) ** (_S.w[_S.j] * _S.alpha[_S.j]), (_S.j, 1, _S.d))
    product_to_exp_sum(prod, A4)
    for wrong in (A1, A2, A6):
        with pytest.raises(LicenceError):
            product_to_exp_sum(prod, wrong)


def test_L10_log_of_the_extension_sum_needs_A1_and_A6():
    k, j, d, K, kappa = _S.k, _S.j, _S.d, _S.K, _S.kappa
    x = sp.Sum(_S.theta[k, j] * _S.u[j], (j, 1, d)) - _S.beta[k]
    expr = sp.log(sp.Sum(sp.exp(kappa * x), (k, 1, K)))
    log_expand(expr, A1, A6)
    for wrong in ((A1,), (A6,), (A2, A3)):
        with pytest.raises(LicenceError):
            log_expand(expr, *wrong)


def test_the_sign_of_tau_in_L4_L5_L10_is_taken_from_the_entry_that_declares_it():
    assert A3.positive(_S.tau) == _S.tau and A6.positive(_S.kappa) == _S.kappa
    for wrong, sym in ((A1, _S.tau), (A2, _S.tau), (A3, _S.kappa), (A6, _S.tau)):
        with pytest.raises(LicenceError):
            wrong.positive(sym)
    plain = sp.Symbol("tau", real=True)  # a non-positive tau: the L4 sign step has no conclusion
    assert (plain / 2 * sp.Symbol("x", nonnegative=True)).is_nonnegative is not True


def test_real_placeholders_and_slacks_come_only_from_entries_that_declare_them():
    assert A1.real_base("a").is_real is True
    with pytest.raises(LicenceError):
        A7.real_base("a")  # A7 (a matrix identity) declares nothing real
    with pytest.raises(LicenceError):
        A3.nonneg_base("v")  # A3 declares no nonnegative family
    with pytest.raises(LicenceError):
        I6.nonneg_symbol("s")  # I6 declares no inequality
    assert F5.nonneg_symbol("s").is_nonnegative is True
    assert R2.positive_symbol("g").is_positive is True
    with pytest.raises(LicenceError):
        A2.positive_symbol("g")  # A2 declares nothing strictly positive


def test_F5_and_F10_second_relation_gives_the_unit_term_and_nothing_else_does():
    k0, kappa, M = sp.Symbol("k0", integer=True), _S.kappa, _S.M
    xk = sp.IndexedBase("xk")
    assert sp.exp(kappa * (xk[k0] - M)).subs(*F10.rule(1)) == 1
    assert sp.exp(kappa * (xk[k0] - M)) != 1  # without the entry the term is not 1
    s_i0 = _S.s[_S.i0]
    assert sp.exp(_S.tau * (s_i0 - M)).subs(*F5.rule(1)) == 1
    assert sp.exp(_S.tau * (_S.s[_S.i] - M)).subs(*F5.rule(1)) != 1  # only the index i0


def test_L12_vertex_value_needs_F12_and_the_LP_gap_needs_I1():
    g, m, j0 = sp.IndexedBase("g"), sp.Symbol("m", real=True), _symbols.J0
    assert g[j0].subs(*F12.rule(1)) == m and g[j0] != m
    gap = I1.obj("primal") - I1.obj("dual")
    assert sp.simplify(I1.rewrite(gap)) == 0 and sp.simplify(gap) != 0


def test_L14_fixed_assignment_agreement_needs_R2():
    i, N = _S.i, sp.Symbol("N", integer=True, positive=True)
    sfix, Mx = sp.IndexedBase("sfix"), sp.IndexedBase("Mx")
    expr = sp.Sum(sfix[i] - Mx[i], (i, 1, N))
    assert sp.simplify(R2.rewrite(expr).doit()) == 0
    assert sp.simplify(expr.doit()) != 0  # the row maxima are not the scores on k(i) without R2


def test_L6_MGF_product_comes_from_I5():
    t = sp.Symbol("t", real=True)
    prod = I5.specialize(Mgf1=lambda arg: sp.exp(_S.sigma**2 * arg**2 / 2))
    assert isinstance(prod, sp.Product) and prod.limits[0] == (_S.j, 1, _S.d)
    assert I5.specialize(Other=lambda a: a) == I5.specialize()  # the product is the entry's form
    del t


# ------------- step 2 (WP10 Amendment 2): the steps that were prose are lines; negative controls
# The inherited and declared entries are applied by import; each control withholds the entry (or
# falsifies the fact the step rests on) and the step has no conclusion, as with I6 in L8.

from derivation.axioms import A8, I10, I11, I12, R1  # noqa: E402
from derivation.run import run_chain  # noqa: E402


@pytest.fixture(scope="module")
def chain_ctx():
    ctx, _ = run_chain(verbose=False)
    return ctx


def test_new_entries_carry_a_form_and_a_verified_citation():
    for name, section in (("I11", "3.1.4"), ("I12", "5.5.2")):
        entry = AX.get(name)
        assert entry.tag == AX.INHERITED and entry.has_form() and not entry.proposition
        assert "Boyd & Vandenberghe" in entry.citation and section in entry.citation
    assert AX.get("A8").tag == AX.POSITED and AX.get("A8").relations()
    i10 = AX.get("I10")  # re-based on the LICQ (no strong duality, no convexity)
    assert i10.tag == AX.INHERITED and i10.has_form() and not i10.proposition
    assert "Nocedal & Wright" in i10.citation and "Theorem 12.1" in i10.citation
    assert "Definition 12.4" in i10.citation
    assert "strong duality" not in i10.statement and "Slater" not in i10.statement


@pytest.mark.slow
def test_L3_licq_holds_on_the_simplex_and_fails_when_every_coordinate_is_zero(chain_ctx):
    lq = chain_ctx["L3"]["licq"]
    assert lq["whole_zero_set"] is sp.false  # A2: the zero set is a proper subset
    assert lq["solution"] == [{lq["al"]: 0, lq["gam"][_S.J0]: 0}]  # 1 and e_j independent
    assert lq["control"] != lq["solution"]  # Z = every coordinate: 1 - sum_j e_j = 0, dependent
    import derivation.lemma_03_gradient_kkt as L3

    ctx = dict(chain_ctx)
    ctx["L3"] = dict(chain_ctx["L3"], licq=dict(lq, solution=lq["control"]))
    with pytest.raises(AssertionError, match="LICQ on the simplex"):
        L3.verify(ctx)


def test_L3_KKT_conditions_come_from_I10_and_the_balance_needs_R1():
    wp, mu = R1.positive_symbol("wp"), I10.obj("mu")
    assert wp.is_nonzero is True
    zero = sp.simplify(I10.rule(2)[1] / wp)
    assert zero == 0 and I10.rule(2)[0] == _S.w[_S.j] * mu[_S.j]
    weak = I10.nonneg_symbol("wq")  # a coordinate that may be 0 (no R1): mu_j = 0 is not forced
    assert weak.is_nonzero is not True
    with pytest.raises(LicenceError):
        A2.positive_symbol("wp")  # A2 declares only w_j >= 0; only R1 licenses a positive wp
    # complementary slackness applied termwise is the zero sum; without I10 the sum is not zero
    w, gr, lam = _S.w, I10.obj("gradient"), I10.obj("lambda")
    body = sp.Sum(w[_S.j] * (sp.solve(I10.rule(0)[0], gr[_S.j])[0] - lam), (_S.j, 1, _S.d))
    assert I10.rewrite(body, only=(2,)).doit() == 0
    assert body.doit() != 0


def test_L3_the_balanced_step_fails_without_R1(chain_ctx):
    import derivation.lemma_03_gradient_kkt as L3

    ctx = dict(chain_ctx)
    ctx["L3"] = dict(chain_ctx["L3"])
    ctx["L3"]["KKT_boundary"] = dict(chain_ctx["L3"]["KKT_boundary"], positive_case_solution=[])
    with pytest.raises(IndexError):  # no multiplier is forced to 0, so no balanced conclusion
        L3.verify(ctx)


def test_L4_convexity_needs_I11_and_the_sign_of_the_second_derivative():
    P, Q = I11.obj("premise"), I11.obj("conclusion")
    assert I11.entails([sp.Equivalent(P, sp.true)], Q)
    assert not I11.entails([sp.Equivalent(P, sp.false)], Q)  # no sign, no convexity
    assert not I11.entails([], Q)


def test_L12_termwise_zero_needs_I12_and_the_support(chain_ctx):
    r = chain_ctx["L12"]
    assert r["support_zero"] == 0
    support = sp.Sum(
        _S.p[_S.i] * (_S.M - sp.Sum(_S.w[_S.j] * _S.u[_S.i, _S.j], (_S.j, 1, _S.d))),
        (_S.i, 1, _S.n),
    )
    assert I12.rewrite(support).doit() == 0
    assert support.doit() != 0  # without the entry the sum is not 0


def test_L14_regrouping_needs_the_partition_relation_A8(chain_ctx):
    r = chain_ctx["L14"]
    assert r["rows_to_cells"] == (0, 2) and r["cells_swap_equal"] and r["cell_regroup_ok"]
    assert r["F_regroup"] == 0
    chi, i, k, K = A8.obj("membership"), _S.i, _S.k, _S.K
    row_count = sp.Sum(chi[k, i], (k, 1, K))
    assert A8.rewrite(row_count, only=(0,)) == 1 and row_count != 1  # one cell per row, by A8
    # an A8-free count has no value, so the share is not nonnegative without the entry
    free = sp.IndexedBase("c")
    assert sp.Sum(free[k, i], (i, 1, A8.obj("rows"))).is_nonnegative is not True
    assert A8.rewrite(A8.obj("count")[k] / A8.obj("rows"), only=(2,)).is_nonnegative is True


@pytest.mark.parametrize(
    ("module", "key", "tamper", "message"),
    [
        ("lemma_02_shift", "L2", lambda r: r.update(shift_amount=r["shift_amount"] + 1), "L2 FAIL"),
        ("lemma_05_lse_lme", "L5", lambda r: r.update(other=sp.Integer(0)), "L5 FAIL"),
        (
            "lemma_11_pareto",
            "L11",
            lambda r: r.update(deductions=dict(r["deductions"], dominance_gains=sp.true)),
            "L11 FAIL",
        ),
        ("lemma_12_term_gap", "L12", lambda r: r.update(support_zero=sp.Integer(1)), "L12 FAIL"),
        ("lemma_14_assignment_stable", "L14", lambda r: r.update(F_regroup=1), "L14 FAIL"),
    ],
)
def test_a_falsified_fact_breaks_the_step_that_rests_on_it(chain_ctx, module, key, tamper, message):
    import importlib

    mod = importlib.import_module(f"derivation.{module}")
    ctx = {k: (dict(v) if isinstance(v, dict) else v) for k, v in chain_ctx.items()}
    tamper(ctx[key])
    with pytest.raises(AssertionError, match=message):
        mod.verify(ctx)


# ------------- step 3 (principle 3): no premise hides in a symbol; the checker fails on one


@pytest.mark.slow
def test_a_symbol_with_a_sign_assumption_made_directly_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "    base = J(S)\n",
        '    base = J(S)\n    _bad = sp.Symbol("bad", nonnegative=True)\n',
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_02_shift.py" in out and "unlicensed assuming symbol" in out
    assert "nonnegative=True on Symbol" in out


def test_a_family_declared_real_or_signed_directly_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "    base = J(S)\n",
        "    base = J(S)\n"
        '    _a = sp.IndexedBase("a", real=True)\n'
        '    _b = sp.symbols("b c", positive=True)\n',
    )
    code, out = run_checker(scratch)
    assert code != 0 and out.count("unlicensed assuming symbol") == 2


def test_a_hypothesis_must_quote_the_statement(scratch):
    edit(
        scratch,
        "lemma_14_assignment_stable.py",
        '"every w_k minimizes f_k")',
        '"every w_k is a global minimizer of everything")',
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_14_assignment_stable.py" in out
    assert "which is not in the lemma's STATEMENT or docstring" in out


def test_a_hypothesis_inside_a_function_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "    base = J(S)\n",
        '    base = J(S)\n    _h = hypothesis_symbol("h", "positive", "tau > 0")\n',
    )
    edit(
        scratch,
        "lemma_02_shift.py",
        "from derivation.licence import log_expand",
        "from derivation.licence import hypothesis_symbol, log_expand",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "a hypothesis must be declared at module level" in out


def test_a_do_nothing_application_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "    base = J(S)\n",
        "    base = A3.invoke(J(S))\n",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "a do-nothing application: Axiom.invoke" in out


def test_every_hypothesis_of_the_statements_is_listed_in_the_record():
    rec = _record()["lemmas"]
    listed = {(f, h["symbol"]) for f, lemma in rec.items() for h in lemma["hypotheses"]}
    assert ("lemma_11_pareto.py", "dl") in listed and (
        "lemma_14_assignment_stable.py",
        "dfk",
    ) in listed
    assert ("lemma_13_margin.py", "delta") in listed and ("lemma_12_term_gap.py", "c_nn") in listed
    for lemma in rec.values():
        for h in lemma["hypotheses"]:
            assert h["sign"] in ("positive", "nonnegative") and h["claim"].strip()


def test_no_lemma_script_creates_a_signed_symbol_directly():
    """The committed scripts pass principle 3 by the checker, and by this plain scan."""
    import ast

    for path in sorted(DERIVATION.glob("lemma_*.py")):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Call):
                for kw in node.keywords:
                    assert kw.arg not in proofmap.SIGN_KWARGS, (path.name, node.lineno)


# ------------- step 5: earlier lemmas' results by import, step kind "by a proved result"

from derivation.results import ProvedResult, UnprovedResultError  # noqa: E402


def test_the_four_dependencies_are_declared_by_import_and_applied_by_steps():
    rec = _record()["lemmas"]
    imported = {
        f: lem["proved_results_imported"]
        for f, lem in rec.items()
        if lem["proved_results_imported"]
    }
    assert imported == {
        "lemma_04_convexity.py": {"L3_RESULT": "lemma_03_gradient_kkt"},
        "lemma_07_elasticities.py": {"L1_RESULT": "lemma_01_homogeneity"},
        "lemma_12_term_gap.py": {"L4_RESULT": "lemma_04_convexity"},
        "lemma_14_assignment_stable.py": {
            "L12_RESULT": "lemma_12_term_gap",
            "L13_RESULT": "lemma_13_margin",
        },
        "lemma_15_descent.py": {
            "L12_RESULT": "lemma_12_term_gap",
            "L14_RESULT": "lemma_14_assignment_stable",
        },
    }
    exported = {f for f, lem in rec.items() if lem["proved_results_exported"]}
    assert exported == {
        "lemma_01_homogeneity.py",
        "lemma_03_gradient_kkt.py",
        "lemma_04_convexity.py",
        "lemma_12_term_gap.py",
        "lemma_13_margin.py",
        "lemma_14_assignment_stable.py",
    }
    for fname, names in imported.items():
        applied = {n for st in rec[fname]["steps"] if st["kind"] == "result" for n in st["results"]}
        assert applied == set(names)


def test_a_result_taken_before_it_is_proved_raises():
    result = ProvedResult("L3", "claim")
    with pytest.raises(UnprovedResultError):
        result.take({"L3": {"a0": 1}}, "a0")
    ctx = {"L3": {"a0": 1}}
    result.certify(ctx)
    assert result.take(ctx, "a0") == 1 and not result.holds(ctx, "a0")  # holds needs fact True
    with pytest.raises(UnprovedResultError):
        ProvedResult("L4", "c").family({"L4": {"convex": True}}, "convex", "x")  # uncertified


def test_a_lemma_may_import_nothing_but_a_proved_result_from_another_lemma(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "from derivation.lemma_03_gradient_kkt import L3_RESULT",
        "from derivation.lemma_03_gradient_kkt import L3_RESULT, linearize",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_04_convexity.py" in out
    assert "only its proved result, L3_RESULT" in out


def test_a_whole_lemma_script_cannot_be_imported(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "from derivation.lemma_03_gradient_kkt import L3_RESULT",
        "import derivation.lemma_03_gradient_kkt\n"
        "from derivation.lemma_03_gradient_kkt import L3_RESULT",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "imports the lemma script derivation.lemma_03_gradient_kkt" in out


def test_a_result_of_a_later_lemma_cannot_be_imported(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "from derivation.lemma_03_gradient_kkt import L3_RESULT",
        "from derivation.lemma_03_gradient_kkt import L3_RESULT\n"
        "from derivation.lemma_12_term_gap import L12_RESULT",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_12_term_gap is not earlier in the chain" in out


def test_an_imported_result_that_no_step_applies_fails(scratch):
    edit(
        scratch,
        "lemma_02_shift.py",
        "from derivation.axioms import A1, A2, A3",
        "from derivation.axioms import A1, A2, A3\n"
        "from derivation.lemma_01_homogeneity import L1_RESULT",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "imported proved results ['L1_RESULT'] differ" in out


def test_a_result_that_its_lemma_never_certifies_fails_for_exporter_and_importer(scratch):
    edit(scratch, "lemma_03_gradient_kkt.py", "    L3_RESULT.certify(ctx)\n", "")
    code, out = run_checker(scratch)
    assert code != 0
    assert "lemma_03_gradient_kkt.py: exports L3_RESULT but its verify never certifies it" in out
    assert "lemma_04_convexity.py" in out and "never certifies L3_RESULT" in out


def test_an_import_of_a_result_the_lemma_does_not_export_fails(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "from derivation.lemma_03_gradient_kkt import L3_RESULT",
        "from derivation.lemma_01_homogeneity import L1_RESULT\n"
        "from derivation.lemma_03_gradient_kkt import L3_RESULT",
    )
    edit(
        scratch,
        "lemma_01_homogeneity.py",
        "L1_RESULT = ProvedResult",
        "L1_NOT_RESULT = ProvedResult",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_01_homogeneity does not export L1_RESULT" in out


def test_a_proved_result_used_on_an_untagged_line_fails(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "    d, j, w, v, u = S.d, S.j, S.w, S.v, S.u\n",
        "    d, j, w, v, u = S.d, S.j, S.w, S.v, S.u\n    _ok = L3_RESULT.proved(ctx)\n",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "proved result L3_RESULT used on an untagged line" in out


# ---------------------- the one-term fit is a geometric program (L4.14 to L4.24)

from derivation.axioms import I13  # noqa: E402
from derivation.sumtools import posynomial_term  # noqa: E402


def _gp_facts(obj, eq, ineq):
    t = lambda b: sp.true if b else sp.false  # noqa: E731
    return [
        sp.Equivalent(I13.obj("objective"), t(obj)),
        sp.Equivalent(I13.obj("equalities"), t(eq)),
        sp.Equivalent(I13.obj("inequalities"), t(ineq)),
    ]


def test_I13_is_an_inherited_entry_citing_the_sections_read():
    assert I13.tag == AX.INHERITED and I13.has_form() and not I13.proposition
    for part in ("Boyd, Kim, Vandenberghe & Hassibi", "section 2.2", "section 2.5", "2007"):
        assert part in I13.citation
    assert (
        "several terms" in I13.failure_mode
    )  # the entry itself does not claim the several-term fit


def test_I13_concludes_a_geometric_program_only_when_all_three_premises_hold():
    goal = I13.obj("conclusion")
    assert I13.entails(_gp_facts(True, True, True), goal)
    for facts in ((False, True, True), (True, False, True), (True, True, False)):
        assert not I13.entails(_gp_facts(*facts), goal)  # a falsified fact: no conclusion


def test_posynomial_term_is_a_monomial_only_with_positive_coefficient_and_x_free_real_exponents():
    wn = A2.nonneg_base("wn")
    ur = A1.real_base("ur")
    n, tau, i, j = _S.n, _S.tau, _S.i, _S.j
    assert posynomial_term(1 / n, tau * ur[i, j], wn)  # the L4.17 term
    assert posynomial_term(sp.exp(-1), sp.Integer(1), wn)  # (1/e) prod x_j = 1
    assert not posynomial_term(-1 / n, tau * ur[i, j], wn)  # a negative coefficient
    assert not posynomial_term(1 / n, tau * wn[j], wn)  # an exponent that depends on x
    assert not posynomial_term(1 / n, tau * _S.u[i, j] * sp.I, wn)  # a non-real exponent
    assert not posynomial_term(1 / n, sp.Symbol("q"), wn)  # an exponent not known to be real


def test_the_L4_geometric_program_steps_take_their_licence_from_A2_and_A1():
    wn = A2.nonneg_base("wn")
    ur = A1.real_base("ur")
    prod = sp.Product(sp.exp(wn[_S.j]) ** (_S.tau * ur[_S.i, _S.j]), (_S.j, 1, _S.d))
    product_to_exp_sum(prod, A2)
    with pytest.raises(LicenceError):
        product_to_exp_sum(prod)  # no entry: the forced log is refused
    with pytest.raises(LicenceError):
        A3.nonneg_base("wn")  # A3 declares no nonnegative family: no x_j = exp(w_j) > 0
    with pytest.raises(LicenceError):
        A7.real_base("ur")


def test_L4_geometric_program_facts_are_computed_and_a_falsified_fact_fails(chain_ctx):
    assert chain_ctx["L4"]["geometric_program"] is True
    y = sp.Symbol("y", real=True)
    ok = sp.solve_univariate_inequality(sp.exp(y) >= 1, y, relational=False, domain=sp.S.Reals)
    assert ok == sp.Interval(0, sp.oo)
    bad = sp.solve_univariate_inequality(sp.exp(y) >= 2, y, relational=False, domain=sp.S.Reals)
    assert bad != sp.Interval(0, sp.oo)  # w_j >= 0 is x_j >= 1 and no other bound
    wn = A2.nonneg_base("wn")
    x_prod = sp.Product(sp.exp(wn[_S.j]), (_S.j, 1, _S.d))
    assert A2.rewrite(product_to_exp_sum(x_prod, A2), rename={_S.w: wn}) == sp.E
    assert A2.rewrite(product_to_exp_sum(x_prod, A2)) != sp.E  # the rename ties the simplex to wn


def test_a_scratch_L4_without_the_I13_import_or_with_a_falsified_step_fails(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "from derivation.axioms import A1, A2, A3, I11, I13",
        "from derivation.axioms import A1, A2, A3, I11",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "lemma_04_convexity.py" in out and "I13" in out


def test_a_scratch_L4_with_a_changed_geometric_program_step_fails_naming_the_step(scratch):
    edit(
        scratch,
        "lemma_04_convexity.py",
        "assert mono_eq, ",
        "assert not not mono_eq, ",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "L4.19" in out


def test_L4_geometric_program_steps_are_of_the_kinds_the_rules_allow():
    steps = {s["tag"]: s for s in _record()["lemmas"]["lemma_04_convexity.py"]["steps"]}
    assert len(steps) == 24 and steps["L4.13"]["fingerprint"]  # L4.1 to L4.13 keep their addresses
    kinds = {t: steps[t]["kind"] for t in (f"L4.{k}" for k in range(14, 25))}
    assert kinds["L4.14"] == kinds["L4.15"] == "axiom"
    assert steps["L4.14"]["applies"] == ["A2"] and steps["L4.15"]["applies"] == ["A1"]
    assert steps["L4.16"]["applies"] == ["A2"] and steps["L4.18"]["applies"] == ["A2"]
    assert steps["L4.22"]["applies"] == ["A2"] and steps["L4.24"]["applies"] == ["I13"]
    for t in ("L4.17", "L4.19", "L4.20", "L4.21", "L4.23"):
        assert kinds[t] == "computed"


# ------------- WP10 Amendment 5, R-41: L16, the soft-weight alternation (three scripted steps)
import importlib  # noqa: E402

from derivation.axioms import I14  # noqa: E402
from derivation.symbols import make_symbols  # noqa: E402

_L16 = "lemma_16_soft_fit_alternation.py"


def _l16_steps():
    return {s["tag"]: s for s in _record()["lemmas"][_L16]["steps"]}


def _run_L16():
    mod = importlib.import_module("derivation.lemma_16_soft_fit_alternation")
    ctx = {"S": make_symbols()}
    mod.derive(ctx)
    return ctx, mod


def test_L16_is_in_the_chain_with_its_exact_statement_and_new_entries():
    assert CHAIN_NAMES[CHAIN_NAMES.index("lemma_17_soft_fit_certificate") - 1] == (
        "lemma_16_soft_fit_alternation"
    )
    mod = importlib.import_module("derivation.lemma_16_soft_fit_alternation")
    assert mod.STATEMENT == (
        "Soft-weight alternation: with weights alpha_ik = softmax_k(kappa score_ik) from the "
        "current model, (i) a convex program symmetric in the terms attains its minimum with all "
        "terms equal, so the objective over all terms is not convex in them in general; (ii) the "
        "soft model's slack is bounded above by the fixed-weight objective, with equality at the "
        "weights' own model; (iii) the fixed-weight objective is a generalized posynomial in "
        "exp(w)."
    )
    assert set(mod.AXIOMS_USED) == {"A1", "A2", "A3", "A6", "I14", "I15"}
    for name, section in (("I14", "3.1.8"), ("I15", "5.3")):
        entry = AX.get(name)
        assert entry.tag == AX.INHERITED and entry.has_form() and not entry.proposition
        assert section in entry.citation and "web.stanford.edu" in entry.citation


def test_L16_steps_are_of_the_kinds_the_rules_allow():
    steps = _l16_steps()
    assert len(steps) == 49
    applies = {t: st["applies"] for t, st in steps.items() if st["kind"] == "axiom"}
    ledger_steps = {name: [t for t, a in applies.items() if name in a] for name in AX.AXIOMS}
    assert ledger_steps["I14"] == ["L16.6", "L16.8", "L16.14", "L16.21"]
    assert ledger_steps["I15"] == ["L16.31"]
    assert all(st["kind"] != "result" for st in steps.values())  # imports no earlier result


@pytest.mark.slow
def test_L16_verifies_and_each_falsified_fact_fails_loudly():
    ctx, mod = _run_L16()
    mod.verify(ctx)
    for key, bad in (
        ("shift_gap", 1),
        ("F_shift_gap", 1),
        ("average_gap", 1),
        ("alpha_sum", 1),
        ("mean_y", 1),
        ("gibbs_gap", 1),
        ("tight", 1),
        ("bound_gap", 1),
        ("rows_nonneg", None),
        ("regroup_gap", 1),
        ("posy", False),
        ("mono", False),
        ("power_positive", None),
        ("log_gap", 1),
        ("generalized_posynomial", False),
    ):
        ctx, mod = _run_L16()
        ctx["L16"][key] = bad
        with pytest.raises(AssertionError, match="L16 FAIL"):
            mod.verify(ctx)
    ctx, mod = _run_L16()
    ctx["L16"]["equal_value"] = ctx["L16"]["Fth"] + ctx["L16"]["J"]  # F(equal) above F(W)
    with pytest.raises(AssertionError, match="L16 FAIL"):
        mod.verify(ctx)
    ctx, mod = _run_L16()
    ins = dict(ctx["L16"]["instance"])
    ins["F_mid"] = ins["F"]  # a convex F would not rise at the midpoint
    ctx["L16"]["instance"] = ins
    with pytest.raises(AssertionError, match="L16 FAIL"):
        mod.verify(ctx)


def test_the_symmetric_convex_step_needs_convexity_and_the_gibbs_step_needs_I14():
    # Jensen's inequality (I14) is for a convex f: the slack of a concave f is negative
    a, b = sp.Rational(0), sp.Rational(2)
    f = lambda x: -(x**2)  # noqa: E731  (concave)
    mean_of_f = (f(a) + f(b)) / 2
    f_of_mean = f((a + b) / 2)
    assert I14.slack_expr(jen_f_of_mean=f_of_mean, jen_mean_of_f=mean_of_f) < 0
    g = lambda x: x**2  # noqa: E731  (convex)
    assert I14.slack_expr(jen_f_of_mean=g((a + b) / 2), jen_mean_of_f=(g(a) + g(b)) / 2) >= 0
    # the entry gives its nonnegative family only through its own relation
    assert I14.nonneg_base("Jf")[1].is_nonnegative is True
    with pytest.raises(LicenceError):
        A3.nonneg_base("Jf")
    # a withheld licence: log alpha with alpha = softmax(kappa x0) needs A1 (x0 real) and A6
    x0 = sp.IndexedBase("x0", real=True)
    z = sp.Sum(sp.exp(_S.kappa * x0[_S.i, _S.L]), (_S.L, 1, _S.K))
    alpha = sp.exp(_S.kappa * x0[_S.i, _S.k]) / z
    log_expand(sp.log(alpha), A1, A6)
    with pytest.raises(LicenceError):
        log_expand(sp.log(alpha), A1)  # kappa is not known to be real
    with pytest.raises(LicenceError):
        log_expand(sp.log(alpha))


def test_a_scratch_L16_without_the_I14_or_I15_import_fails_naming_the_ledger_entry(scratch):
    edit(
        scratch,
        _L16,
        "from derivation.axioms import A1, A2, A3, A6, I14, I15",
        "from derivation.axioms import A1, A2, A3, A6, I15",
    )
    code, out = run_checker(scratch)
    assert code != 0 and _L16 in out and "I14" in out


def test_a_scratch_L16_without_I15_fails(scratch):
    edit(
        scratch,
        _L16,
        "from derivation.axioms import A1, A2, A3, A6, I14, I15",
        "from derivation.axioms import A1, A2, A3, A6, I14",
    )
    code, out = run_checker(scratch)
    assert code != 0 and _L16 in out and "I15" in out


@pytest.mark.slow
def test_a_scratch_L16_with_a_changed_step_fails_naming_the_step(scratch):
    edit(scratch, _L16, 'assert r["tight"] == 0', 'assert r["tight"] != 0')
    code, out = run_checker(scratch)
    assert code != 0 and "L16.41" in out
    # a ledger entry whose citation changes is also named
    edit(
        scratch,
        "axioms.py",
        "section 3.1.8 (Jensen's inequality",
        "section 3.1.7 (Jensen's inequality",
    )
    code, out = run_checker(scratch)
    assert code != 0 and "I14" in out


def test_the_exact_instance_shows_the_objective_is_not_convex_in_the_terms():
    ctx, _ = _run_L16()
    ins = ctx["L16"]["instance"]
    assert abs(ins["F"] - ins["F_swapped"]) < sp.Float("1e-30")  # the swap is a symmetry of F
    assert ins["F_mid"] - ins["F"] > sp.Float("0.004")  # the midpoint is worse: not convex


# ------------- WP17 R-8: L17, the soft-fit certificate (the Hessian D - kappa M, second-order test)
_L17 = "lemma_17_soft_fit_certificate.py"
_L17_FACTS = (
    "beta1_gap",
    "beta2_gap",
    "y_gap",
    "z_gap",
    "row1_gap",
    "row2_gap",
    "alpha_sum",
    "p_sum",
    "grad_gap",
    "hess_gap",
    "var_generic",
    "D_var_gap",
    "M_var_gap",
    "affine_gap",
)


def _l17_steps():
    return {s["tag"]: s for s in _record()["lemmas"][_L17]["steps"]}


@pytest.fixture(scope="module")
def l17():
    mod = importlib.import_module("derivation.lemma_17_soft_fit_certificate")
    ctx = {"S": make_symbols()}
    mod.derive(ctx)
    return ctx, mod


def _l17_fresh(l17):
    ctx, mod = l17
    return {"S": ctx["S"], "L17": dict(ctx["L17"])}, mod


def test_L17_is_in_the_chain_with_its_exact_statement_and_the_new_entry():
    assert "lemma_17_soft_fit_certificate" in CHAIN_NAMES
    mod = importlib.import_module("derivation.lemma_17_soft_fit_certificate")
    assert mod.STATEMENT == (
        "Soft-fit certificate: at a feasible point of the soft-weight fit where the first-order "
        "(KKT) conditions hold, if the Hessian H = D - kappa M of the soft objective is positive "
        "definite on the tangent space of the active face, the point is a strict local minimizer; "
        "D and M are both positive semidefinite, D the weighted within-term curvature and kappa M "
        "the designs' ambiguity between terms."
    )
    assert set(mod.AXIOMS_USED) == {"A1", "A2", "A3", "A6", "I16"}
    entry = AX.get("I16")
    assert entry.tag == AX.INHERITED and entry.has_form() and not entry.proposition
    assert "Nocedal & Wright" in entry.citation and "Theorem 12.6" in entry.citation
    assert "to be confirmed by the author" in entry.citation
    assert "I10" in AX.AXIOMS and AX.get("I10").citation != entry.citation


def test_L17_steps_are_of_the_kinds_the_rules_allow():
    steps = _l17_steps()
    assert len(steps) == 52
    applies = {t: st["applies"] for t, st in steps.items() if st["kind"] == "axiom"}
    ledger_steps = {name: [t for t, a in applies.items() if name in a] for name in AX.AXIOMS}
    assert ledger_steps["I16"] == ["L17.21", "L17.22", "L17.23"]
    assert ledger_steps["A3"] == ledger_steps["A6"] == ["L17.17"]
    assert ledger_steps["A2"] == ["L17.2", "L17.18"]
    assert ledger_steps["A1"] == ["L17.1", "L17.3"]
    assert all(st["kind"] != "result" for st in steps.values())
    assert sum(st["kind"] == "computed" for st in steps.values()) == 52 - 8


@pytest.mark.slow
def test_L17_verifies_and_each_falsified_fact_fails_loudly(l17):
    ctx, mod = _l17_fresh(l17)
    mod.verify(ctx)
    for key in _L17_FACTS:
        ctx, mod = _l17_fresh(l17)
        ctx["L17"][key] = 1
        with pytest.raises(AssertionError, match="L17 FAIL"):
            mod.verify(ctx)
    for key, bad in (
        ("D_nonneg", None),
        ("M_nonneg", None),
        ("cone_in_face", False),
        ("restriction", False),
        ("certificate", False),
        ("certificate_without_kkt", True),
        ("certificate_without_curvature", True),
    ):
        ctx, mod = _l17_fresh(l17)
        ctx["L17"][key] = bad
        with pytest.raises(AssertionError, match="L17 FAIL"):
            mod.verify(ctx)


@pytest.mark.slow
def test_L17_numerical_endpoints_hold_and_a_falsified_endpoint_fails(l17):
    ctx, mod = _l17_fresh(l17)
    ins, eq = ctx["L17"]["instance"], ctx["L17"]["all_equal"]
    assert ins["grad_err"] < 1e-20 and ins["hess_err"] < 1e-20  # against finite differences
    assert (
        eq["one"]["gap"] < 1e-50
        and eq["one"]["lambda_min"] < -0.01 < 0.01 < eq["half"]["lambda_min"]
    )
    for patch in (
        {"instance": dict(ins, grad_err=sp.Float("1e-3"))},
        {"instance": dict(ins, hess_err=sp.Float("1e-3"))},
        {"instance": dict(ins, asymmetry=sp.Float("1e-3"))},
        {"all_equal": dict(eq, one=dict(eq["one"], gap=sp.Float("1e-3")))},
        {"all_equal": dict(eq, one=dict(eq["one"], lambda_min=sp.Float("0.5")))},
        {"all_equal": dict(eq, half=dict(eq["half"], lambda_min=sp.Float("-0.5")))},
        {"all_equal": dict(eq, one=dict(eq["one"], D_min=sp.Float("-0.5")))},
    ):
        ctx, mod = _l17_fresh(l17)
        ctx["L17"].update(patch)
        with pytest.raises(AssertionError, match="L17 FAIL"):
            mod.verify(ctx)


def test_the_hessian_D_plus_kappa_M_or_a_dropped_D_is_not_the_hessian(l17):
    # the formulas are checked, not assumed: the wrong sign of kappa M, or D alone, disagrees with
    # the finite differences of F at the exact instance
    _, mod = l17
    R = sp.Rational
    U = [(1, 0), (1, R(1, 2)), (0, 1), (R(1, 2), 1)]
    W = [(R(3, 4), R(1, 4)), (R(1, 5), R(4, 5))]
    one = sp.Integer(1)
    _, D, M, _ = mod._numbers(U, W, one, one)
    h = sp.Float("1e-12", 60)

    def second(a):
        Wp = [list(r) for r in W]
        Wm = [list(r) for r in W]
        Wp[a // 2][a % 2] += h
        Wm[a // 2][a % 2] -= h
        return (
            mod._F(U, Wp, one, one) - 2 * mod._F(U, W, one, one) + mod._F(U, Wm, one, one)
        ) / h**2

    for a in range(4):
        assert abs(second(a) - (D - M)[a, a]) < 1e-9
    assert any(abs(second(a) - (D + M)[a, a]) > 1e-3 for a in range(4))
    assert any(abs(second(a) - D[a, a]) > 1e-3 for a in range(4))


def test_the_cone_is_in_the_face_only_when_the_face_fixes_the_positive_multiplier_bounds():
    from sympy.logic.inference import satisfiable

    s, f, g = sp.symbols("s f g")
    assert not satisfiable(sp.And(sp.And(s, f, g), sp.Not(sp.And(s, f))))
    assert satisfiable(
        sp.And(sp.And(s, f, g), sp.Not(sp.And(s, g))) | sp.And(sp.And(s, g), sp.Not(sp.And(s, f)))
    )


def test_the_certificate_needs_both_premises_of_I16():
    kkt, curv, concl = (AX.I16.obj(key) for key in ("kkt", "curvature", "conclusion"))
    assert AX.I16.entails([kkt, curv], concl)
    assert not AX.I16.entails([kkt], concl) and not AX.I16.entails([curv], concl)
    assert not AX.I16.entails([], concl)


@pytest.mark.slow
@pytest.mark.parametrize("name", ["I16", "A3", "A6", "A2", "A1"])
def test_a_scratch_L17_without_a_ledger_import_fails_naming_the_entry(scratch, name):
    header = "from derivation.axioms import A1, A2, A3, A6, I16"
    names = [n for n in ("A1", "A2", "A3", "A6", "I16") if n != name]
    edit(scratch, _L17, header, "from derivation.axioms import " + ", ".join(names))
    code, out = run_checker(scratch)
    assert code != 0 and _L17 in out and name in out


@pytest.mark.slow
def test_a_scratch_L17_with_a_changed_step_fails_naming_the_step(scratch):
    edit(scratch, _L17, 'assert r["hess_gap"] == 0', 'assert r["hess_gap"] != 0')
    code, out = run_checker(scratch)
    assert code != 0 and "L17.35" in out
    edit(scratch, "axioms.py", "Theorem 12.6", "Theorem 12.5")
    code, out = run_checker(scratch)
    assert code != 0 and "I16" in out
