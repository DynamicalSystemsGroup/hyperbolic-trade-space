"""L19: a two-regime upper bound on the noise shift of the soft maximum (not tight).

Setting: clean scores s_i (i = 1..n, symbolic n, n >= 2), noise draws z_i = w.eps_i independent
N(0, v^2) with v > 0 (A11; v^2 = sigma^2 ||w||^2 under A5 and L6, v^2 = w'Sigma w under L18), tau
> 0 (A3), LME_tau(x) = (1/tau) log((1/n) Sum_i exp(tau x_i)) the log-mean-exp (L5), and the shift
Delta = E LME_tau(s + z) - LME_tau(s), E over the noise with the rows s fixed.

What this proves (symbolic n): 0 <= Delta <= min(tau v^2 / 2, E max_i z_i), and E max_i z_i <= v
sqrt(2 log n), so the shift is also at most min(tau v^2 / 2, v sqrt(2 log n)). The three parts:
the lower bound is the tangent line e^x >= 1 + x with the softmax weights p_i of the clean scores,
LME(s + z) - LME(s) >= Sum_i p_i z_i, and E z_i = 0, so Delta >= 0; the first upper bound is
Jensen's inequality for the concave logarithm with the moment generating function E exp(tau z_i) =
exp(tau^2 v^2 / 2) (the L6 value); the second is exp(tau (s_i + z_i)) <= exp(tau s_i) exp(tau max
z); and the maximum of the draws is bounded through Jensen for exp and a union bound, E max z <=
log(n)/lam + lam v^2 / 2 for every lam > 0, whose minimum over lam is v sqrt(2 log n). The L6
value tau v^2 / 2 and the closed-form bound v sqrt(2 log n) cross at tau* = 2 sqrt(2 log n) / v, a
rule of thumb for the temperature below which the L6 value is the smaller of the two (E max z
itself is below v sqrt(2 log n), so its crossing with tau v^2 / 2 is at a smaller tau).

What this does NOT prove: that the shift equals either bound, or is close to either. The bound is
an upper bound and is not tight: it is true and loose. In the planted cells of
tests/test_noise_lemmas.py (measured there, not proved here) the smaller bound is within a few
percent of the shift where tau v^2 / 2 is the smaller, and exceeds the shift by a factor of up to
about 2.6 at tau = 200 (the L6 value alone, by up to about 12). Nor does it prove a lower bound on
the shift beyond the mean; any statement for noise that is not independent Gaussian across rows,
or for scores that depend on the noise or weights w fitted to the noisy table; anything about the
exponents of a fit, which the shift of the offset does not determine; or consistency of the fit.

Route: sympy.stats for the Gaussian moment generating functions; the tangent-line minimum and the
sign of exp(x) - 1 as in L5; the inequality of exponentials with the maximum of the draws
represented by a symbol (F19, as F5 does for the maximum of the scores); the minimisation of the
Chernoff bound by solving g'(lam) = 0.
"""

import sympy as sp
from sympy.stats import E

from derivation.axioms import A3, A11, F5, F19, I17
from derivation.licence import hypothesis_symbol, log_expand
from derivation.sumtools import linear

TITLE = "Noise shift of the soft maximum: 0 <= shift <= min(tau v^2/2, E max z)"
STATEMENT = (
    "For clean scores s_i and independent N(0, v^2) noise draws z_i (A11), tau > 0, n >= 2 and "
    "LME the log-mean-exp: 0 <= E LME_tau(s + z) - LME_tau(s) <= "
    "min(tau v^2 / 2, E max_i z_i), and E max_i z_i <= v sqrt(2 log n) (from E max z <= "
    "log(n)/lam + lam v^2/2 for every lam > 0); tau v^2 / 2 and v sqrt(2 log n) cross at "
    "tau* = 2 sqrt(2 log n) / v. An upper bound that is not tight: the shift equals neither "
    "bound, and tau* is a rule of thumb, not a sharp threshold"
)
AXIOMS_USED = ["A3", "A11", "F5", "F19", "I17"]

lam = hypothesis_symbol("lam", "positive", "for every lam > 0")
ln = hypothesis_symbol("ln", "positive", "n >= 2")


def derive(ctx):
    S = ctx["S"]
    n, i, s = S.n, S.i, S.s
    lim = (i, 1, n)
    x = sp.Symbol("x", real=True)

    # [L19.1] A3: tau > 0
    tau = A3.positive(S.tau)
    # [L19.2] A11: one row's noise z ~ N(0, v^2) with v > 0
    Zrow, v = A11.obj("noise"), A11.rule(0)[0]
    # [L19.3] F19: the noise draws z_i, real, bounded above by their maximum Zm
    zi, Zm = F19.rule(0)
    z = zi.base
    # [L19.4] F19: the maximum is attained: z_{i0} = Zm for some i0
    z_top = F19.rule(1)[0]

    Ts = sp.Sum(sp.exp(tau * s[i]), lim)
    LMEs = sp.log(Ts / n) / tau
    Tx = sp.Sum(sp.exp(tau * (s[i] + z[i])), lim)
    k_ = sp.Symbol("k", integer=True)  # a second bound index, so the normaliser is constant in i
    Tk = sp.Sum(sp.exp(tau * s[k_]), (k_, 1, n))  # the normaliser, the same sum as Ts
    p = sp.exp(tau * s[i]) / Tk  # softmax weights of the clean scores
    zbar = sp.Sum(p * z[i], lim).subs(Tk, Ts)  # their weighted mean of the draws

    # --- the lower bound Delta >= 0: the shift is (1/tau) log Sum_i p_i e^{tau z_i} >= zbar
    # [L19.5] the tangent line e^x >= 1 + x: the minimum of e^x - 1 - x over R is 0
    tangent_min = sp.calculus.util.minimum(sp.exp(x) - 1 - x, x, sp.S.Reals)
    tangent_sum = sp.simplify(
        linear(sp.Sum(p * sp.exp(tau * zbar) * (1 + tau * (z[i] - zbar)), lim)).subs(Tk, Ts)
    )
    # [L19.6] A3, F5, F19: the logarithm is licensed: shift = (1/tau) log Sum p_i e^{tau z_i}
    shift_form = log_expand(sp.log(Tx / n) - sp.log(Ts / n), A3, F5, F19) / tau
    # [L19.7] A3, F5, F19: the same shift written with the softmax weights p_i of the clean scores
    shift_target = (
        log_expand(sp.log(linear(sp.Sum(p * sp.exp(tau * z[i]), lim)).subs(Tk, Ts)), A3, F5, F19)
        / tau
    )
    # [L19.8] A3, F5, F19: the tangent-line floor of that logarithm is tau zbar
    floor_x = log_expand(sp.log(tangent_sum), A3, F5, F19) / tau
    # [L19.9] A11: E z_i = 0, so E zbar = Sum_i p_i E z_i = 0
    Ez = E(Zrow)
    Ezbar = sp.Sum(p * Ez, lim)
    # [L19.10] I17: E is monotone, so LME(x) - LME(s) >= zbar pointwise gives Delta >= E zbar = 0
    lower_step = I17.entails([sp.Symbol("jx_X_le_Y_almost_surely")], sp.Symbol("jx_EX_le_EY"))

    # --- the first upper bound: Jensen for the concave logarithm with the L6 moment generating fn
    # [L19.11] A11: E exp(tau z_i) = exp(tau^2 v^2 / 2), the L6 value
    mgf_row = sp.simplify(E(sp.exp(tau * Zrow)))
    # [L19.12] A11: the term i of E[(1/n) Sum exp(tau (s_i + z_i))] is exp(tau s_i) exp(tau^2 v^2/2)
    term_E = sp.simplify(E(sp.exp(tau * (s[i] + Zrow))))
    EX = sp.Sum(term_E, lim) / n
    elog = sp.Symbol("ElogX", real=True)
    # [L19.13] I17: Jensen for f = -log: the slack E(-log X) + log(E X) of the row average X
    slack = I17.slack_expr(jx_f_of_mean=-sp.log(EX), jx_mean_of_f=-elog)
    # [L19.14] I17: the Jensen slack J is nonnegative
    J = I17.slack_symbol("J")
    elog_value = sp.solve(sp.Eq(slack, J), elog)[0]
    # [L19.15] A3, F5, F19: the logarithm is licensed: E LME(s + z) = LME(s) + tau v^2/2 - J/tau
    first_gap = sp.simplify(
        log_expand(elog_value, A3, F5, F19) / tau - (LMEs + tau * v**2 / 2 - J / tau)
    )

    # --- the second upper bound: exp(tau (s_i + z_i)) <= exp(tau s_i) exp(tau Zm)
    # [L19.16] F19: the slack Zm - z_i of z_i <= Zm is nonnegative
    slack_i = F19.nonneg_symbol("slack_i")
    term_shift = sp.simplify(
        sp.exp(tau * (s[i] + Zm - slack_i))
        - sp.exp(tau * s[i]) * sp.exp(tau * Zm) * sp.exp(-tau * slack_i)
    )
    # exp(y) <= 1 exactly when y <= 0 (as L5), here y = -tau slack_i
    term_le_one = sp.solveset(sp.exp(x) <= 1, x, sp.S.Reals)
    # [L19.17] A3: with slack_i >= 0 (F19), -tau slack_i <= 0: each term <= e^(tau s_i) e^(tau Zm)
    sign_ok = (-A3.positive(tau) * slack_i).is_nonpositive
    # [L19.18] A3, F5, F19: the sum bound T_x <= exp(tau Zm) T_s gives LME(x) <= LME(s) + Zm
    max_gap = sp.simplify(
        log_expand(sp.log(sp.exp(tau * Zm) * Ts / n), A3, F5, F19) / tau - (Zm + LMEs)
    )
    # [L19.19] I17: E is monotone, so LME(x) <= LME(s) + Zm gives E LME(x) <= LME(s) + E Zm
    upper_step = I17.entails([sp.Symbol("jx_X_le_Y_almost_surely")], sp.Symbol("jx_EX_le_EY"))

    # --- E Zm <= v sqrt(2 log n)
    EZm = sp.Symbol("EZm", real=True)
    Eexp = sp.Symbol("Eexp", real=True)
    # [L19.20] I17: Jensen for the convex exp: exp(lam E Zm) <= E exp(lam Zm); slack >= 0
    jensen_exp = I17.slack_expr(jx_f_of_mean=sp.exp(lam * EZm), jx_mean_of_f=Eexp)
    # [L19.21] F19: the term i0 of Sum_i exp(lam z_i) is exp(lam Zm)
    top_term = sp.exp(lam * z_top).subs(*F19.rule(1))
    # [L19.22] F19: a second term exp(lam z_k) over a real draw is positive
    other_term = sp.exp(lam * F19.real_base("zr")[sp.Symbol("k2", integer=True)])
    # [L19.23] A11: E exp(lam z_i) = exp(lam^2 v^2/2), so E Sum_i exp(lam z_i) = n exp(lam^2 v^2/2)
    union = n * sp.simplify(E(sp.exp(lam * Zrow)))
    # [L19.24] A3, F5, F19: log of the union bound n exp(lam^2 v^2/2) is log n + lam^2 v^2/2
    chernoff = sp.simplify(log_expand(sp.log(union), A3, F5, F19) - (sp.log(n) + lam**2 * v**2 / 2))
    g = ln / lam + lam * v**2 / 2
    lam_star = next(r for r in sp.solve(sp.diff(g, lam), lam) if r.is_positive)
    g_min = sp.simplify(g.subs(lam, lam_star))
    curvature = sp.diff(g, lam, 2).subs(lam, lam_star)

    # --- the crossover of the two upper bounds
    tau_star = sp.solve(sp.Eq(tau * v**2 / 2, v * sp.sqrt(2 * ln)), tau)[0]

    ctx["L19"] = {
        "tau": tau,
        "v": v,
        "tangent_min": tangent_min,
        "floor_x": floor_x,
        "shift_form": shift_form,
        "zbar": zbar,
        "shift_target": shift_target,
        "Ez": Ez,
        "Ezbar": Ezbar,
        "lower_step": lower_step,
        "mgf_row": mgf_row,
        "term_E": term_E,
        "slack": slack,
        "elog_value": elog_value,
        "first_gap": first_gap,
        "term_shift": term_shift,
        "term_le_one": term_le_one,
        "sign_ok": sign_ok,
        "max_gap": max_gap,
        "upper_step": upper_step,
        "jensen_exp": jensen_exp,
        "top_term": top_term,
        "other_term": other_term,
        "Zm": Zm,
        "chernoff": chernoff,
        "g_min": g_min,
        "curvature": curvature,
        "lam_star": lam_star,
        "tau_star": tau_star,
    }


def verify(ctx):
    S = ctx["S"]
    r = ctx["L19"]
    tau, v, n = r["tau"], r["v"], S.n
    ln_n = sp.log(n)
    # [L19.25] the minimum of e^x - 1 - x over R is 0: e^x >= 1 + x
    assert r["tangent_min"] == 0, "L19 FAIL tangent line"
    # [L19.26] LME(s + z) - LME(s) equals (1/tau) log Sum_i p_i e^{tau z_i}
    assert sp.simplify(sp.expand(r["shift_form"] - r["shift_target"], power_exp=True)) == 0, (
        "L19 FAIL shift form"
    )
    # [L19.27] the tangent-line floor of the logarithm equals zbar: the shift is at least zbar
    assert sp.simplify(r["floor_x"] - r["zbar"]) == 0, "L19 FAIL floor"
    # [L19.28] E z_i = 0, so E zbar = 0
    assert r["Ez"] == 0 and r["Ezbar"].doit() == 0, "L19 FAIL mean"
    # [L19.29] E is monotone, so Delta >= E zbar = 0: the lower bound
    assert r["lower_step"] is True, "L19 FAIL lower step"
    # [L19.30] the row moment generating function is the L6 value exp(tau^2 v^2 / 2)
    assert sp.simplify(r["mgf_row"] - sp.exp(tau**2 * v**2 / 2)) == 0, "L19 FAIL row MGF"
    # [L19.31] the term i of E X is exp(tau s_i) exp(tau^2 v^2 / 2)
    assert sp.simplify(r["term_E"] - sp.exp(tau * S.s[S.i]) * sp.exp(tau**2 * v**2 / 2)) == 0, (
        "L19 FAIL term of E X"
    )
    # [L19.32] Jensen: E LME(s + z) = LME(s) + tau v^2/2 - J/tau with the slack J >= 0
    assert r["first_gap"] == 0, "L19 FAIL Jensen with the L6 value"
    # [L19.33] the shifted term is exp(tau s_i) exp(tau Zm) exp(-tau slack_i)
    assert r["term_shift"] == 0, "L19 FAIL shifted term"
    # [L19.34] exp(y) <= 1 exactly when y <= 0
    assert r["term_le_one"] == sp.Interval(-sp.oo, 0), "L19 FAIL exp(y) <= 1 iff y <= 0"
    # [L19.35] each shifted term is at most exp(tau s_i) exp(tau Zm): -tau slack_i <= 0
    assert r["sign_ok"] is True, "L19 FAIL sign of the shifted exponent"
    # [L19.36] LME(s + z) <= LME(s) + Zm: the sum bound and the logarithm
    assert r["max_gap"] == 0, "L19 FAIL LME(x) <= LME(s) + Zm"
    # [L19.37] E is monotone, so E LME(s + z) <= LME(s) + E max z: the second upper bound
    assert r["upper_step"] is True, "L19 FAIL upper step"
    # [L19.38] Jensen for exp: the slack Eexp - exp(lam E Zm) is the nonnegative difference
    assert r["jensen_exp"] == sp.Symbol("Eexp", real=True) - sp.exp(
        lam * sp.Symbol("EZm", real=True)
    ), "L19 FAIL Jensen for exp"
    # [L19.39] exp(lam Zm) <= Sum_i exp(lam z_i): the term i0 is exp(lam Zm)
    assert r["top_term"] == sp.exp(lam * r["Zm"]), "L19 FAIL top term"
    # [L19.40] the other terms are positive, so the sum is at least the top term
    assert r["other_term"].is_positive is True, "L19 FAIL positivity of the other terms"
    # [L19.41] log of n exp(lam^2 v^2 / 2) is log n + lam^2 v^2 / 2: lam E Zm <= log n + lam^2 v^2/2
    assert r["chernoff"] == 0, "L19 FAIL Chernoff exponent"
    # [L19.42] the minimiser of log(n)/lam + lam v^2/2 is sqrt(2 log n)/v, with positive curvature
    assert (
        sp.simplify(r["lam_star"] - sp.sqrt(2 * ln) / v) == 0 and r["curvature"].is_positive is True
    ), "L19 FAIL minimiser"
    # [L19.43] the minimum is v sqrt(2 log n): E max z <= v sqrt(2 log n)
    assert sp.simplify(r["g_min"].subs(ln, ln_n) - v * sp.sqrt(2 * ln_n)) == 0, "L19 FAIL minimum"
    # [L19.44] tau v^2/2 and v sqrt(2 log n) cross at tau* = 2 sqrt(2 log n) / v
    assert sp.simplify(r["tau_star"] - 2 * sp.sqrt(2 * ln) / v) == 0, "L19 FAIL crossover"
