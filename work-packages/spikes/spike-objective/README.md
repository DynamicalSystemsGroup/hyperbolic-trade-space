# Research spike round 2 (2026-11-08): the objective of the K > 1 alternation

Throwaway. Nothing in the repository was changed. All code and outputs are in this folder, `<folder>` = `work-packages/spikes/spike-objective` (spike code, not part of the package and not imported by it). Round 1's `methods.py` (steps B, D, the loop, matching, scoring, initializations) is
imported unchanged from `docs/superpowers/notes/spike-facet-refit/`. Every command is run from the
repository root. (The subagent's harness refused to write this file; the driver saved the report
from the subagent's message verbatim.)

| command | writes | time |
|---|---|---|
| `uv run python <folder>/bench_ab.py` | `ab.txt`, `mono.csv`, `planted_vs_found.csv`, `restarts_all.csv` (tables 1, 2) | ~3 min |
| `uv run python <folder>/bench_c.py` then `uv run python <folder>/fail_seeds.py` | `c.txt`, `recovery_single.csv`, `recovery_restarts.csv` (tables 3, 4; `fail_seeds.py` prints the fail-seed lists that `bench_c.py` printed empty because `d.select` is a DataFrame method) | ~8 min |
| `uv run python <folder>/bench_cubesat2.py` | `cubesat2.txt`, `cubesat2.csv` (table 5) | ~1.5 min |
| `uv run python <folder>/check_identifiability.py` | stdout (section 2) | seconds |

Settings as round 1: `make_frontier_data(400, 4, n_terms=3, random_state=s)`, s = 0..19 (noise 0, frontier fraction 0.3, so 120 frontier rows), tau in {inf, 50}; pass = exponent error (max abs after Hungarian matching) < 0.05 and >= 90 % of frontier rows on the right facet (R-1). Single init: the built solver's (seed 12345) or planted labels with 20 % flips (seed s). Restarts: the built solver's five seeds (`check_random_state(0).randint(0, 2**31-1, 5)`). Cubesat primary table: N = 706, d = 10, tau = 38.10, band 0.0262.

## 1. The objectives, precisely (`objectives.py`)

All are functions of `(U, W, beta, labels, tau)` with `slack_i = beta_{k(i)} - w_{k(i)} . u_i`, `beta_k = J_tau(U w_k)` the support value over all rows, band = 1/tau (0.1 at tau = inf).

| | definition | at tau = inf | sign |
|---|---|---|---|
| O0 | mean_i slack_i (built) | fine | >= 0 at inf; < 0 possible at finite tau (rows above the soft frontier) |
| O1 | mean of slack_i over rows with abs(slack_i) < band | fine | as O0 |
| T | number of rows with abs(slack_i) < band (larger better) | fine | integer |
| T0 | number of rows with slack_i < 1e-9 (larger better) | exact touches, incl. LP-vertex interior rows | at finite tau counts rows at or above the soft frontier (a frac_above count), not touches |
| O2 | sum_i p_i slack_i, p = softmax(-tau slack) | identically 0 (uniform on rows of zero slack) | <= 0 at finite tau |
| O3 | -(1/tau) log mean_i exp(-tau slack_i) | identically 0 (min slack) | <= 0 |
| O4 | sum_k [J_tau(U w_k) - LME_{i in k}(U w_k)] | identically 0 (the support row of facet k is assigned to k by the argmax) | <= 0 when a facet's own rows are its top scorers |
| O5 (own) | -T + 0.1 O0: lexicographic (band touch count, then mean slack) | fine | edge first, interior to break ties |

Identities, verified numerically (seed 1, tau = 50: -0.019581 both sides): O4's facet term is the entropic soft minimum of the facet's own-row slacks, and `O3 = -(1/tau) log sum_k (n_k/N) exp(-tau O4_k)`. The per-facet step minimizing O4's term is `min_w J_tau(Uw) - LME_own(Uw)`: step B with the facet mean replaced by the facet soft maximum (B is its tau_own -> 0 limit; step A is the same term without the support part). Built as step G (`make_refit_G`: B warm start, SLSQP on the difference of convex functions, accepted only if the term decreases, `beta_k` the support value at the real tau; at tau = inf the term is flat so the step uses t = 1/band = 10).

Degeneracies found: O2, O3, O4 are identically zero at tau = inf; at finite tau they are negative and more negative the further a facet's own rows reach above its support relative to the rest (discriminative, not edge tightness). G on seed 1, tau 50: O2 -0.115, O3 -0.022, O4 -0.068 vs planted -0.037, -0.020, -0.038, with exponent error 0.395 and 5 of 400 rows in the band; on the cubesat G attains the lowest O3 of all variants (-0.0288) with mean slack 0.435 vs B's 0.053 and 14 near rows vs 228. O1 at finite tau rewards the most negative band mean: on the cubesat it selects the seed-1 outlier (-0.0024 vs -0.0010 to -0.0014).

## 2. Why seeds 1 and 16 fail (`check_identifiability.py`; B, init 12345, tau = inf)

| seed | sparse facet: frontier rows (affine rank) | free parameters of a hyperplane through them (R^4, sum w = 1) | matched found facet: slack on those rows | its exponent error | run err / right |
|---|---|---|---|---|---|
| 1 | 3 (3) | 1 | 0.042, 0.000, 0.049 | 0.113 | 0.113 / 0.97 |
| 3 | 6 (4) | 0 | 0.23, 0.04, 0.10, 0.11, 0.07, 0.01 | 0.200 | 0.200 / 0.53 |
| 8 | 11 (4) | 0 | 0.00, 0.09, 0.19, 0.08, 0.08, 0.17, 0.17, 0.09, 0.14, 0.06, 0.17 | 0.108 | 0.108 / 0.91 |
| 16 | 2 (2) | 2 | 0.50, 1.09 | 0.402 | 0.402 / 0.97 |

Seed 1: the two large found facets are exactly the planted planes (58/58 and 59/59 exact touches, error 0.000); the three sparse rows are split 1/1/1 across found facets; the third found facet touches one of them plus LP-vertex interior rows, so exact touches tie at 120. A facet with fewer than d frontier rows is not identifiable from them; every edge-only objective is flat across the family; only interior rows locate it (round 1's oracle with true labels: 0.018–0.035). Seeds 3 and 8 are identifiable; a passing restart exists. Seeds 1 and 16: no passing restart for B or D at either tau (0/5).

## 3. Measurements

### Table 1 (a). Fraction of half-steps in which the objective got worse (round 1's loop, both inits pooled; B 291/231 full iterations at inf/50, D 639/295)

| objective | inf: B assign / refit | inf: D assign / refit | 50: B assign / refit | 50: D assign / refit |
|---|---|---|---|---|
| O0 | 0.000 / 0.000 | 0.000 / 0.501 | 0.000 / 0.000 | 0.000 / 0.349 |
| O1 | 0.038 / 0.041 | 0.017 / 0.576 | 0.177 / 0.528 | 0.142 / 0.532 |
| T | 0.000 / 0.007 | 0.000 / 0.139 | 0.212 / 0.377 | 0.136 / 0.217 |
| T0 | 0.000 / 0.038 | 0.000 / 0.243 | 0.000 / 0.152 | 0.000 / 0.017 |
| O2 | constant | constant | 0.511 / 0.519 | 0.190 / 0.753 |
| O3 | constant | constant | 0.000 / 0.398 | 0.000 / 0.647 |
| O4 | constant | constant | 0.329 / 0.416 | 0.122 / 0.719 |
| O5 | 0.000 / 0.007 | 0.000 / 0.495 | 0.212 / 0.377 | 0.136 / 0.532 |

### Table 2 (b). Planted (support offsets recomputed) | found (B, init 12345) | best of 5 B restarts | best of 5 D restarts; `*` planted strictly better than found

tau = inf:

| obj | seed 1 | seed 3 | seed 8 | seed 16 |
|---|---|---|---|---|
| O0 | 0.6554 \| 0.6552 \| 0.6510 \| 0.6573 | 0.7333 \|*0.7420 \| 0.7310 \| 0.7453 | 0.6757 \|*0.6791 \| 0.6745 \| 0.6870 | 0.6638 \| 0.6634 \| 0.6636 \| 0.6703 |
| O1 | 0.0090 \|*0.0091 \| 0.0091 \| 0.0151 | 0.0089 \|*0.0103 \| 0.0089 \| 0.0207 | 0.0084 \|*0.0114 \| 0.0084 \| 0.0189 | 0.0083 \|*0.0085 \| 0.0083 \| 0.0159 |
| T | 149 \| 149 \| 152 \| 152 | 147 \|*145 \| 148 \| 145 | 145 \|*142 \| 146 \| 143 | 148 \| 148 \| 149 \| 149 |
| T0 | 120 \| 120 \| 120 \| 6 | 120 \|*114 \| 118 \| 3 | 120 \|*110 \| 120 \| 4 | 120 \|*118 \| 120 \| 5 |
| O2/O3/O4 | 0 everywhere | | | |
| O5 | -148.93 \| -148.93 \| -151.93 \| -151.93 | -146.93 \|*-144.93 \| -147.93 \| -144.93 | -144.93 \|*-141.93 \| -145.93 \| -142.93 | -147.93 \| -147.93 \| -148.93 \| -148.93 |

found B err/right: s1 0.113/0.98, s3 0.200/0.52, s8 0.108/0.91, s16 0.402/0.97.

tau = 50:

| obj | seed 1 | seed 3 | seed 8 | seed 16 |
|---|---|---|---|---|
| O0 | 0.6152 \| 0.6152 \| 0.6113 \| 0.6124 | 0.6911 \| 0.6884 \| 0.6884 \| 0.6891 | 0.6347 \| 0.6305 \| 0.6338 \| 0.6346 | 0.6252 \| 0.6241 \| 0.6231 \| 0.6248 |
| O1 | -0.0004 \| -0.0017 \| -0.0030 \| -0.0038 | -0.0026 \| -0.0036 \| -0.0036 \| -0.0022 | -0.0003 \| -0.0039 \| -0.0101 \| -0.0043 | 0.0014 \| -0.0010 \| -0.0007 \| -0.0034 |
| T | 16 \|*13 \| 17 \| 17 | 9 \| 9 \| 9 \| 10 | 9 \| 19 \| 19 \| 7 | 12 \| 14 \| 14 \| 14 |
| T0 | 134 \| 134 \| 137 \| 139 | 132 \|*131 \| 131 \| 132 | 131 \|*128 \| 132 \| 134 | 133 \| 134 \| 134 \| 133 |
| O2 | -0.0463 \|*-0.0441 \| -0.0533 \| -0.0498 | -0.0471 \| -0.0511 \| -0.0511 \| -0.0518 | -0.0458 \| -0.0524 \| -0.0487 \| -0.0468 | -0.0450 \|*-0.0436 \| -0.0474 \| -0.0434 |
| O3 | -0.0196 \|*-0.0192 \| -0.0211 \| -0.0208 | -0.0206 \| -0.0212 \| -0.0212 \| -0.0210 | -0.0205 \| -0.0209 \| -0.0203 \| -0.0206 | -0.0191 \|*-0.0189 \| -0.0197 \| -0.0177 |
| O4 | -0.0667 \|*-0.0617 \| -0.0853 \| -0.0822 | -0.0677 \| -0.0722 \| -0.0725 \| -0.0712 | -0.0704 \| -0.0731 \| -0.0676 \| -0.0718 | -0.0720 \|*-0.0601 \| -0.0671 \| -0.0584 |

found B err/right: s1 0.132/0.85, s3 0.112/0.94, s8 0.210/0.52, s16 0.265/0.80.

Seeds (of 20) where planted is strictly better than (i) found, (ii) best of 5 B restarts:

| obj | inf (i) | inf (ii) | 50 (i) | 50 (ii) |
|---|---|---|---|---|
| O0 | 6 [3,7,8,9,11,14] | 0 | 2 [7,14] | 0 |
| O1 | 8 [1,3,7,8,9,11,14,16] | 2 [1,16] | 10 | 9 |
| T | 6 | 0 | 6 | 5 |
| T0 | 7 [3,7,8,9,11,14,16] | 1 [3] | 7 | 4 |
| O2 | 0 | 0 | 2 [1,16] | 0 |
| O3 | 0 | 0 | 6 [0,1,9,10,16,18] | 6 [0,7,8,9,10,18] |
| O4 | 0 | 0 | 7 | 7 |
| O5 | 6 | 0 | 6 | 5 |

Passing restarts of 5 on the bad seeds: inf: s1 B 0 D 0; s3 B 3 D 3; s8 B 2 D 3; s16 0/0. tau 50: s1 0/0; s3 B 0 D 3; s8 B 0 D 5; s16 0/0. Seeds with >= 1 passing restart: 18/20 (B, D at inf); 16 (B) / 18 (D) at 50.

### Table 3 (c). Single init, pass/20 (pass on {1,3,8,16}) [errors on 1,3,8,16]

| variant | solver, inf | solver, 50 | flipped, inf | flipped, 50 |
|---|---|---|---|---|
| B (= guard:O0) | 12 (0) [0.113,0.200,0.108,0.402] | 14 (0) [0.132,0.112,0.210,0.265] | 19 (3: 1,3,8) [0.011,0.001,0.044,0.437] | 17 (1: 8) [0.051,0.112,0.027,0.337] |
| D | 16 (1: 8) [0.195,0.111,0.014,0.281] | 16 (1: 3) [0.141,0.022,0.224,0.279] | 18 (2: 3,8) | 18 (2: 3,8) |
| G | 0 [0.818,0.602,0.594,0.570] | 0 [0.395,0.364,0.231,0.435] | 0 | 0 |
| B best:O1 | 12 (0) | 7 (0) | 16 (3) | 4 (1) |
| B guard:O1 | 11 (0) | 4 (0), 2.0 iters | 16 (3) | 3 (1), 1.2 iters |
| B best:T | 12 (0) | 0 (0) | 19 (3) | 2 (0) |
| B guard:T | 12 (0) | 0 (0), 1.2 iters | 19 (3) | 3 (0) |
| B best:O2 | 0 (constant obj.) | 0 (0) | 0 | 4 (1) |
| B guard:O2 | 12 (never fires) | 0 (0), 1.2 iters | 19 (3) | 4 (1) |
| B best:O3 | 0 (constant) | 13 (0) | 0 | 17 (1) |
| B guard:O3 | 12 (never fires) | 8 (0), 4.4 iters | 19 (3) | 17 (1) |
| B best:O4 | 0 (constant) | 5 (0) | 0 | 17 (1) |
| B guard:O4 | 12 (never fires) | 3 (0) | 19 (3) | 18 (2: 3,8) |
| B best:O5 | 12 (0) | 0 (0) | 19 (3) | 3 (0) |
| B guard:O5 | 12 (0) | 0 (0), 1.2 iters | 19 (3) | 3 (0) |

Runtime per run: B 0.03–0.11 s, D 0.08–0.15, G 0.08–1.0.

### Table 4 (c). Five restarts, selection by each objective, pass/20 (fail seeds)

| selection | B, inf | D, inf | B, 50 | D, 50 |
|---|---|---|---|---|
| O0 (built) | 16 (1,3,8,16) | 17 (1,3,16) | 16 (1,3,8,16) | 17 (1,3,16) |
| O1 | 18 (1,16) | 18 (1,16) | 15 (1,3,8,14,16) | 16 (1,3,16,18) |
| T | 16 (1,3,8,16) | 18 (1,16) | 14 (1,3,8,14,16,18) | 16 (1,3,16,18) |
| T0 | 18 (1,16) | 14 (0,1,3,8,16,18) | 16 (1,3,8,16) | 18 (1,16) |
| O2 | 17 (1,8,16) | 16 (0,1,3,16) | 14 | 16 |
| O3 | 17 (1,8,16) | 16 (0,1,3,16) | 15 | 17 (1,3,16) |
| O4 | 17 (1,8,16) | 16 (0,1,3,16) | 14 | 17 (1,3,16) |
| O5 | 16 (1,3,8,16) | 18 (1,16) | 14 | 16 |
| G, any | 0 | | 0 | |

Errors on 1,3,8,16 for the 18/20 rows: B sel:O1 inf [0.512, 0.023, 0.000, 0.359]; B sel:T0 inf [0.512, 0.001, 0.000, 0.262]; D sel:T0 at 50 [0.492, 0.022, 0.042, 0.330].

### Table 5 (d). Cubesat primary, K = 3, seeds 0..4, one init per seed

| variant | O0 mean (sd) | T mean | O3 mean | conv/5 | iters | s/run | signatures | dev vs seed 0 (seeds 1..4) | dev vs B seed 0 (seeds 0..4) |
|---|---|---|---|---|---|---|---|---|---|
| B | 0.0568 (0.0086) | 227.6 | -0.0274 | 5 | 11.2 | 0.25 | 2/5 | 0.526, 0.003, 0.003, 0.005 | 0, 0.526, 0.003, 0.003, 0.005 |
| D | 0.0592 (0.0086) | 223.8 | -0.0276 | 4 | 20.6 | 0.55 | 2/5 | 0.475, 0.016, 0.015, 0.021 | 0.088, 0.475, 0.095, 0.095, 0.070 |
| G | 0.4350 (0.0777) | 14.0 | -0.0288 | 0 | 50 | 1.93 | 5/5 | 0.255, 0.423, 0.393, 0.433 | 0.43, 0.43, 0.38, 0.30, 0.38 |
| B best:O1 | 0.0568 | 223.0 | -0.0274 | 5 | 11.2 | 0.27 | 3/5 | 0.520, 0.012, 0.004, 0.014 | 0.001, 0.520, 0.013, 0.005, 0.015 |
| B guard:O1 | 0.0792 (0.0227) | 185.4 | -0.0271 | 5 | 2.0 | 0.07 | 5/5 | 0.233, 0.271, 0.209, 0.156 | 0.274, 0.259, 0.013, 0.103, 0.234 |
| B best:T | 0.0586 (0.0126) | 234.0 | -0.0275 | 5 | 11.2 | 0.26 | 2/5 | 0.450, 0.003, 0.003, 0.003 | 0.003, 0.452, 0.003, 0.003, 0.002 |
| B guard:T | 0.0623 | 222.8 | -0.0273 | 5 | 5.6 | 0.14 | 4/5 | 0.332, 0.149, 0.149, 0.089 | 0.149, 0.452, 0.003, 0.003, 0.099 |
| B best:O2 = guard:O2 | 0.0892 (0.0122) | 163.2 | -0.0269 | 5 | 11.2 / 1.0 | 0.26 / 0.05 | 5/5 | 0.233, 0.164, 0.185, 0.156 | 0.274, 0.259, 0.200, 0.195, 0.234 |
| B best:O3 | 0.0568 (0.0087) | 227.8 | -0.0275 | 5 | 11.2 | 0.26 | 3/5 | 0.501, 0.004, 0.004, 0.006 | 0.001, 0.501, 0.005, 0.005, 0.005 |
| B guard:O3 | 0.0580 | 219.2 | -0.0274 | 5 | 7.2 | 0.18 | 4/5 | 0.440, 0.098, 0.104, 0.105 | 0.105, 0.501, 0.008, 0.005, 0.005 |
| B best:O4 | 0.0699 (0.0254) | 213.0 | -0.0273 | 5 | 11.2 | 0.26 | 3/5 | 0.228, 0.274, 0.274, 0.274 | 0.274, 0.452, 0.003, 0.003, 0.002 |
| B guard:O4 | 0.0717 | 207.8 | -0.0272 | 5 | 5.0 | 0.13 | 4/5 | 0.228, 0.274, 0.274, 0.216 | 0.274, 0.452, 0.003, 0.003, 0.099 |
| B best:O5 | 0.0586 (0.0126) | 234.0 | -0.0275 | 5 | 11.2 | 0.25 | 2/5 | 0.452, 0.003, 0.003, 0.004 | 0.000, 0.452, 0.003, 0.003, 0.004 |
| B guard:O5 | 0.0623 | 222.8 | -0.0273 | 5 | 5.6 | 0.14 | 4/5 | 0.332, 0.149, 0.149, 0.089 | as guard:T |

B's main basin (seeds 0, 2, 3, 4): shares 0.67/0.22/0.11, n-lemmas 5/4/3, sets {control effort, slew time, energy balance, pointing error} | {energy balance, control effort, slew time} | {peak slew power, pointing error, total mass, slew time, power margin}; seed 1: shares 0.67/0.17/0.16, n-lemmas 6/5/3 (round 1's other local optimum). Selection among the five B fits: O0 -> basin (0.0529), T -> basin (240), O2/O3/O4/O5 -> basin; O1 -> seed 1 (-0.0024 vs -0.0010 to -0.0014); T0 -> seed 1 (286 vs 269–270). Per-seed shares, sets and all objective values: `cubesat2.txt`, `cubesat2.csv`.

### (e) Code lines (non-blank, docstrings stripped, ast count)

`slacks` 2, O0 2, O1 4, T 3, T0 3, O2 8, O3 5, O4 15 (10 + 5), O5 2. Restart selection by another objective: 1 line in `solve_terms` + the objective. Best-iterate: 3 lines. Guard with another objective: 1 line changed. Step G: 29 (`_gap_fun` 10 + `make_refit_G` 19). Traced loop `alternate_traced`: 29. Round 1: B 9, D +26, E +29.

## 4. Assessment

Spirit of K = 1: the K = 1 objective is the reach `J_tau(w)`; its weights sit on the edge but the value is the envelope's size. At K > 1 the sum of reaches is degenerate (round 1's C); the non-degenerate size of a K-facet envelope against the whole cloud is the mean slack (one-sided L1 volume, Magnani–Boyd): O0 is the honest analogue and its interior rows are the only information locating a facet with < d frontier rows. Touch counts and band means (T, T0, O1, O5) are flat on the non-identifiable seeds at tau = inf and at finite tau reward rows above the soft frontier because `J_tau < max`. Entropic candidates (O2, O3, O4) are identically zero at tau = inf and discriminative at finite tau; their exact minimizer G destroys the fit on planted and cubesat data. Monotone: O0 under B only; O3 under reassignment only; T, O5 almost under B at inf. Sparse seeds: 3 and 8 recovered by an edge selector at tau = inf (18/20, B or D); 1 and 16 unrecoverable by any objective or rule (non-identifiable; 0/5 passing restarts). R-1 can certify 16/20 (built), 17/20 (D), 18/20 (edge selector at tau = inf; D sel:T0 at tau 50 is not robust); 20/20 is not reachable on these seeds. Costs: selector 1 line + objective + one tolerance; best-iterate 3 lines, no gain; guards on non-monotone objectives harmful; G 29 lines, 0/20; D +26, non-monotone.

## 5. Ranking (comparison for the supervisor, not a decision)

1. Keep O0 in the loop; change only the restart selection to an edge count with O0 as tie-break (exact touches or O1 at tau = inf; the rule must be stated at tau = inf or with a band, not a frac_above count, since O1/T0 at finite tau pick the cubesat outlier): 18/20, cubesat basin unchanged, 4–5 lines + one tolerance; 1 and 16 remain.
2. Keep everything; fix the test data or the claim: require >= d+1 (better 2d) frontier rows per planted facet in R-1's generator, or state R-1 conditionally with the identifiability argument. Zero solver code.
3. D (round 1's rank 1) with O0 (17/20) or an edge selector (18/20): non-monotone step in every objective measured; round 1's guard trade-off.
4. Drop O2, O4 and step G; O3 as a loop objective (harmless selector, no gain); O1 as a loop objective (at most a tau = inf selector, where T0 is sharper).

## 6. Open questions a package would have to settle

- Band: 0.1 is too coarse to separate passing from failing restarts on seeds 3/8 (the T-best restart on seed 3 fails with error 0.344); 1e-9 exact touches work only at noise 0 and tau = inf; at finite tau any "slack < c" count includes rows above the soft frontier. A noise > 0 planted test (absent in both rounds and R-1) decides whether any touch count survives.
- Restart rule: how many restarts (seeds 3 and 8 have 2–3 passing of 5); O0 vs edge-with-O0-tie-break; whether the envelope's `n_eff` (1/sum p^2 of the support weights) is the principled touch count.
- Interaction with D: D raises O0 in 35–50 % of its refits; an O0 guard removes its gain; D with an edge selector gives 18/20 at inf. Whether a non-monotone step with a documented selector is acceptable.
- Generator: should `make_frontier_data(n_terms=K)` guarantee >= d+1 frontier rows per facet, and should R-1 state the condition; seeds 1 and 16 are a property of the data.
- G-7: at tau = 50 the planted band holds 9–19 of 400 rows while 128–139 rows sit above the soft frontier, so a tau selected for K = 1's 10 % above lets a K = 3 envelope put a third of the rows above V = 1 and every finite-tau edge criterion behaves differently from its tau = inf form. Whether tau should be re-selected at K, and whether R-1 should be stated at tau = inf, where the planted exponents are the optimum.
- Whether `tension_report`'s per-facet contending set should follow the fitted `w_k` (round 1's question, unchanged).
