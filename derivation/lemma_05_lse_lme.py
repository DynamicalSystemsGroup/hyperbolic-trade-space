"""L5 - Log-sum-exp versus log-mean-exp: offset, bounds and the two temperature limits.

Setting: scores s_i = w.u_i (i = 1..n, symbolic n), tau > 0 (A3),
  LSE(tau) = (1/tau) log sum_i exp(tau s_i),   LME(tau) = (1/tau) log( (1/n) sum_i exp(tau s_i) ).
beta in the fit is the LME (R-6); the LSE appears only here and in L10.

What this proves (symbolic n):
  1. LSE = LME + (log n)/tau (Sum algebra, log of a quotient).
  2. LSE - max >= 0 with equality iff n = 1; LSE - max > 0 for n >= 2 (so the unnormalized LSE
     overshoots the maximum and diverges like (log n)/tau, which is why beta is the LME).
     NOTE: the spec writes "LSE - max > 0"; that is exact only for n >= 2 (at n = 1, LSE = s_1).
  3. mean <= LME <= max, with mean = (1/n) sum_i s_i. LME <= max: each exp(tau(s_i - M)) <= 1.
     mean <= LME: tangent-line bound e^x >= 1 + x on x_i = tau (s_i - mean) (Jensen, elementary).
  4. lim_{tau->0} LME = mean: N(tau) = log((1/n) sum_i e^{tau s_i}) has N(0) = 0, so
     LME = N(tau)/tau -> N'(0) = mean (sympy.limit cannot evaluate the symbolic Sum, so the
     difference quotient is evaluated through the derivative, computed by sympy in derive).
  5. lim_{tau->inf} LME = max by the squeeze M - (log n)/tau <= LME <= M, with both bounds'
     limits computed by sympy.limit in derive and recorded (mimics symproof
     library/topology.py continuous_at_point: limit computed outside the assertion, verify
     asserts the equality limit - value == 0).

Max representation (FALLBACK F5, listed in the ledger): sympy has no symbolic-n max, so the
maximum is the symbol M with hypotheses s_i <= M for all i and s_{i0} = M for some
i0 in {1..n}. Introduced because sympy.limit cannot see through Sum(exp(tau s_i), (i,1,n)).

Positivity (mimics symproof tactics.py signed_sum_lemmas): the per-term sign of each summand is
asserted with sympy (solveset), then the net bound on the Sum.

Remarks recorded, not proved here: (I2) the sample LME converges a.s. to the population
rho_tau(w) = (1/tau) log E exp(tau w.u) by the strong law of large numbers, and replication
of rows leaves LME unchanged; the tau->0 limit is then E[w.u]. (I3) as tau->inf, rho_tau
increases to the support function h_A(w) = ess sup w.u, and a closed convex set is determined
by its support function, so the fit reads conv A through its support function.

What this does NOT prove: consistency (I2), uniform convergence on the simplex, existence of
w* (L3/L4), or the LP duality of the tau = inf fit (I1, checked in pytest).
"""

import sympy as sp

from derivation.sumtools import linear

TITLE = "LSE = LME + log(n)/tau; mean <= LME <= max; tau limits"
STATEMENT = (
    "LSE = LME + (log n)/tau; LSE - max > 0 (n >= 2); lim_{tau->inf} LME = max; "
    "lim_{tau->0} LME = mean; mean <= LME <= max"
)
# I2 and I3 enter as recorded remarks (see docstring); F5 is the max representation fallback.
AXIOMS_USED = ["A3", "I2", "I3", "F5"]


def derive(ctx):
    S = ctx["S"]
    i, n, s, tau, M = S.i, S.n, S.s, S.tau, S.M
    lim = (i, 1, n)

    T_raw = sp.Sum(sp.exp(tau * s[i]), lim)
    LSE = sp.log(T_raw) / tau
    LME = sp.log(T_raw / n) / tau

    # 1. offset
    offset = sp.expand_log(LSE - LME, force=True)  # T_raw > 0: sum of exponentials

    # Shifted sum: T_raw = e^{tau M} T, T = sum_i exp(tau (s_i - M)).
    T = sp.Sum(sp.exp(tau * (s[i] - M)), lim)
    shift_check = sp.simplify(
        sp.powsimp(sp.expand(sp.exp(tau * M) * linear(sp.Sum(sp.expand(T.function), lim)) - T_raw))
    )

    # Per-term signs (signed_sum_lemmas pattern): x = tau (s_i - M) <= 0 for s_i <= M.
    x = sp.Symbol("x", real=True)
    term_positive = sp.solveset(sp.exp(x) > 0, x, sp.S.Reals)  # all reals
    term_le_one = sp.solveset(sp.exp(x) <= 1, x, sp.S.Reals)  # (-oo, 0]
    # Net bounds on T = sum_i exp(x_i): T <= sum_i 1 = n  and  T >= exp(0) = 1 (the i0 term).
    n_upper = sp.Sum(1, lim).doit()
    # tangent-line bound e^x >= 1 + x: minimum of e^x - 1 - x over R is 0.
    tangent_min = sp.calculus.util.minimum(sp.exp(x) - 1 - x, x, sp.S.Reals)
    # sum_i (s_i - mean) = 0 where mean = (1/n) sum_i s_i
    mean = sp.Sum(s[i], lim) / n
    centered = linear(sp.Sum(s[i] - mean, lim))
    # mean <= LME: sum_i e^{tau s_i} >= sum_i e^{tau mean} (1 + tau (s_i - mean)) = n e^{tau mean}
    tangent_sum = linear(sp.Sum(sp.exp(tau * mean) * (1 + tau * (s[i] - mean)), lim))
    lme_floor = sp.expand_log(sp.log(tangent_sum / n), force=True) / tau  # = mean
    # LME <= max: T <= n gives (1/tau) log(n/n); LME >= M - log(n)/tau: T >= 1 (the i0 term)
    lme_minus_M_upper = sp.log(n_upper / n) / tau
    lme_minus_M_lower = sp.log(sp.Integer(1) / n) / tau
    # LSE - M = (1/tau) log T >= (1/tau) log 1 = 0
    lse_minus_M_floor = sp.log(sp.Integer(1)) / tau

    # 4. tau -> 0: N(tau) = log((1/n) sum_i e^{tau s_i}); N(0) = 0; N'(0) = mean.
    N = sp.log(T_raw / n)
    N0 = sp.simplify(N.subs(tau, 0).doit())
    Nprime0 = sp.diff(N, tau).subs(tau, 0).doit()
    lim_zero = Nprime0  # lim N(tau)/tau = N'(0) since N(0) = 0

    # 5. tau -> oo: M - log(n)/tau <= LME <= M, i.e. LME - M in [-log(n)/tau, 0].
    lower_bound = M - sp.log(n) / tau
    upper_bound = M
    lim_lower = sp.limit(lower_bound, tau, sp.oo)
    lim_upper = sp.limit(upper_bound, tau, sp.oo)

    ctx["L5"] = {
        "LSE": LSE,
        "LME": LME,
        "offset": offset,
        "shift_check": shift_check,
        "term_positive": term_positive,
        "term_le_one": term_le_one,
        "n_upper": n_upper,
        "tangent_min": tangent_min,
        "centered": centered,
        "lme_floor": lme_floor,
        "lme_minus_M_upper": lme_minus_M_upper,
        "lme_minus_M_lower": lme_minus_M_lower,
        "lse_minus_M_floor": lse_minus_M_floor,
        "N0": N0,
        "lim_zero": lim_zero,
        "mean": mean,
        "lim_lower": lim_lower,
        "lim_upper": lim_upper,
        "max_symbol": M,
        "consistency_remark": (
            "I2: the sample LME -> rho_tau(w) a.s. (SLLN); as tau->0 the limit is E[w.u]."
        ),
        "support_function_remark": (
            "I3: rho_tau increases to the support function h_A(w) as tau->inf; "
            "a closed convex set is determined by its support function."
        ),
    }
    return ctx["L5"]


def verify(ctx):
    S = ctx["S"]
    r = ctx["L5"]
    tau, n = S.tau, S.n
    assert sp.simplify(r["offset"] - sp.log(n) / tau) == 0, "L5 FAIL: LSE - LME != log(n)/tau"
    assert r["shift_check"] == 0, "L5 FAIL: sum exp(tau s_i) != e^{tau M} sum exp(tau (s_i - M))"
    # per-term signs, then the net bounds
    assert r["term_positive"] == sp.S.Reals, "L5 FAIL: exp(x) > 0 not established per term"
    assert r["term_le_one"] == sp.Interval(-sp.oo, 0), "L5 FAIL: exp(x) <= 1 iff x <= 0"
    assert r["n_upper"] == n, "L5 FAIL: sum of n ones != n"
    # T in [1, n]  =>  (1/tau) log(T/n) in [-(log n)/tau, 0]  =>  LME in [M - log(n)/tau, M]
    # LSE - max = (1/tau) log T >= 0 since T >= 1, > 0 when T > 1 (some i != i0 term > 0, n >= 2,
    # each such term > 0 by term_positive).
    assert r["tangent_min"] == 0, "L5 FAIL: e^x >= 1 + x not established"
    assert r["centered"] == 0, "L5 FAIL: sum_i (s_i - mean) != 0"
    # mean <= LME (e^x >= 1 + x termwise, then the net sum): the floor equals the mean
    assert sp.simplify(r["lme_floor"] - r["mean"]) == 0, "L5 FAIL: LME floor != mean"
    # LME <= max, LME >= max - log(n)/tau, LSE >= max (T in [1, n])
    assert sp.simplify(r["lme_minus_M_upper"]) == 0, "L5 FAIL: LME <= max bound is not 0"
    assert sp.simplify(r["lme_minus_M_lower"] + sp.log(n) / tau) == 0, "L5 FAIL: lower bound"
    assert r["lse_minus_M_floor"] == 0, "L5 FAIL: LSE - max floor != 0"
    # limits (continuous_at_point pattern: limit computed in derive; assert equality here)
    assert r["N0"] == 0, "L5 FAIL: N(0) != 0"
    assert sp.simplify(r["lim_zero"] - r["mean"]) == 0, "L5 FAIL: lim_{tau->0} LME != mean"
    assert sp.simplify(r["lim_lower"] - r["max_symbol"]) == 0, "L5 FAIL: lower bound limit != max"
    assert sp.simplify(r["lim_upper"] - r["max_symbol"]) == 0, "L5 FAIL: upper bound limit != max"
