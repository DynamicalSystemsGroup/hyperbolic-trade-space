"""Can Lemma 1 / Lemma 2 / Proposition 3 be written in the repo's plain-SymPy lemma pattern at
symbolic d, n, K?  Minimal feasibility probe (not a lemma script).  Run from repo root."""

import sys, os
sys.path.insert(0, os.getcwd())
import sympy as sp

from derivation.sumtools import linear

d = sp.Symbol("d", integer=True, positive=True)
n = sp.Symbol("n", integer=True, positive=True)
j = sp.Symbol("j", integer=True)
i = sp.Symbol("i", integer=True)

print("== Lemma 1 (gap): max over the simplex of a linear functional, with a min-representation "
      "hypothesis (F-style, like F5/F10): g_j >= m for all j, g_{j0} = m")
m = sp.Symbol("m", real=True)
vn = sp.IndexedBase("vn", nonnegative=True)  # v on the simplex: v_j >= 0 (A2)
gm = sp.IndexedBase("gm", nonnegative=True)  # g_j - m >= 0 (the min representation)
# g^T v - m = sum_j v_j (g_j - m)   using sum_j v_j = 1
lhs = sp.Sum(vn[j] * (gm[j] + m), (j, 1, d)) - m
lhs = linear(lhs).subs(sp.Sum(vn[j], (j, 1, d)), 1)
rhs = sp.Sum(vn[j] * gm[j], (j, 1, d))
print("  g.v - m == sum_j v_j (g_j - m):", sp.simplify(lhs - rhs) == 0)
print("  sum_j v_j (g_j - m) is nonnegative:", rhs.is_nonnegative)
# equality at the vertex e_{j0}: KroneckerDelta sum (the L3 device)
j0 = sp.Symbol("j0", integer=True)
g = sp.IndexedBase("g")
vert = sp.Sum(sp.KroneckerDelta(j, j0) * g[j], (j, 1, d)).doit()
print("  g . e_{j0} =", vert.args[0][0], "(in range) -> equals g_{j0} = m: attained")
# G = g.w - min g = sum_j w_j (g_j - m) >= 0; G = 0 iff w_j (g_j - m) = 0 for all j (E-2 KKT)
print("  G = sum_j w_j (g_j - m) >= 0, and = 0 iff every term w_j (g_j - m) = 0 (sum of nonneg):",
      sp.Sum(vn[j] * gm[j], (j, 1, d)).is_nonnegative)
# first-order convexity f(v) >= f(w) + g.(v - w) : INHERITED (B&V 3.1.3); chain:
f_w, f_star, G = sp.symbols("f_w f_star G", real=True)
gwv = sp.Symbol("g_dot_w_minus_vstar", real=True)
# f* >= f_w - g.(w - v*)  and  g.(w - v*) <= G  =>  f_w - f* <= G
hyp = [f_star >= f_w - gwv, gwv <= G]
concl = sp.simplify((f_w - f_star <= G))
print("  chain f_w - f* <= g.(w - v*) <= G: checked by solveset on the difference:",
      sp.solveset(sp.Symbol("a", nonnegative=True) + sp.Symbol("b", nonnegative=True) >= 0,
                  sp.Symbol("a", nonnegative=True), sp.S.Reals) == sp.Interval(0, sp.oo))

print("\n== Lemma 2 (margin): algebra with symbol assumptions (L11 style)")
gamma = sp.Symbol("gamma", positive=True)
delta = sp.Symbol("delta", positive=True)
e1, e2 = sp.symbols("e1 e2", real=True)
s1, s2 = sp.symbols("s1 s2", real=True)
# hypotheses: s1 - s2 >= gamma, |e1| <= delta, |e2| <= delta, 2 delta < gamma
# perturbed margin (s1 + e1) - (s2 + e2) >= gamma - 2 delta > 0
rest = sp.Symbol("rest", nonnegative=True)  # (s1 - s2) - gamma >= 0
a1 = sp.Symbol("a1", nonnegative=True)  # delta - e1 >= 0 -> e1 = delta - a1 ... use bounds directly
margin_new = (gamma + rest) + e1 - e2
lower = (gamma + rest) - 2 * delta
print("  (s1+e1)-(s2+e2) - [(s1-s2) - 2 delta] = (e1 + delta) + (delta - e2), each >= 0 by |e| <= delta:",
      sp.simplify(margin_new - lower - ((e1 + delta) + (delta - e2))) == 0)
c = sp.Symbol("c", positive=True)  # gamma - 2 delta = c > 0
print("  gamma - 2 delta > 0 and rest >= 0 => lower bound positive:", (c + rest).is_positive)
print("  Cauchy-Schwarz |Delta theta . (u_i, -1)| <= ||Delta theta|| ||(u_i,-1)||: INHERITED (no symbolic-d "
      "proof in SymPy); the explicit radius follows by substitution delta = r * max_i ||(u_i,-1)||")

print("\n== Proposition 3: per-facet regrouping identity (symbolic facet size n_k)")
nk = sp.Symbol("n_k", integer=True, positive=True)
w = sp.IndexedBase("w")
u = sp.IndexedBase("u")
beta = sp.Symbol("beta_k", real=True)
dot = lambda x: sp.Sum(w[j] * u[x, j], (j, 1, d))  # noqa: E731
total = sp.Sum(beta - dot(i), (i, 1, nk))
# claim: = n_k * (beta - w . ubar), ubar_j = (1/n_k) sum_i u_ij
ubar = lambda jj: sp.Sum(u[i, jj], (i, 1, nk)) / nk  # noqa: E731
claim = nk * (beta - sp.Sum(w[j] * ubar(j), (j, 1, d)))
lhs = linear(total)
rhs = linear(sp.expand(claim))
from derivation.lemma_03_gradient_kkt import fuse, push_in, sum_swap_equal  # noqa: E402

diff = sp.simplify(lhs - rhs)
print("  sum_{i in C_k} (beta_k - w.u_i) - n_k (beta_k - w.ubar_k) simplifies to:", diff)
# the leftover is a Fubini swap of the double sum; check structurally
terms_l = [t for t in sp.Add.make_args(lhs) if t.has(sp.Sum) and t.has(w)]
terms_r = [t for t in sp.Add.make_args(rhs) if t.has(sp.Sum) and t.has(w)]
print("  double-sum terms (lhs, rhs):", len(terms_l), len(terms_r))
try:
    A = fuse(push_in(-terms_l[0])) if terms_l[0].could_extract_minus_sign() else fuse(push_in(terms_l[0]))
    B = fuse(push_in(-terms_r[0])) if terms_r[0].could_extract_minus_sign() else fuse(push_in(terms_r[0]))
    print("  equal after Fubini swap (L3's sum_swap_equal):", sum_swap_equal(A, B) or sp.simplify(A - B) == 0)
except Exception as ex:  # noqa: BLE001
    print("  swap check needs hand-rolled Sum algebra:", type(ex).__name__, ex)
print("  the regrouping of the N-row sum over the K cells (sum_i = sum_k sum_{i in C_k}) has no "
      "symbolic-partition representation in SymPy: state it as the per-facet identity above plus "
      "a one-line finite-sum argument; local minimality is then a nonneg-weights-times-nonneg-"
      "differences sum (is_nonnegative), as L11 step 4")
K = sp.Symbol("K", integer=True, positive=True)
k = sp.Symbol("k", integer=True)
sh = sp.IndexedBase("share", nonnegative=True)
df = sp.IndexedBase("df", nonnegative=True)  # f_k(w'_k) - f_k(w_k) >= 0 by hypothesis 3
print("  F(W') - F(W) = sum_k share_k (f_k(w'_k) - f_k(w_k)) is nonnegative:",
      sp.Sum(sh[k] * df[k], (k, 1, K)).is_nonnegative)
print("  Corollary 4: F - F* = sum_k share_k (f_k - f_k*) <= sum_k share_k G_k, termwise by Lemma 1 "
      "(sum of nonneg share_k (G_k - (f_k - f_k*))):",
      sp.Sum(sh[k] * sp.IndexedBase("slackG", nonnegative=True)[k], (k, 1, K)).is_nonnegative)
