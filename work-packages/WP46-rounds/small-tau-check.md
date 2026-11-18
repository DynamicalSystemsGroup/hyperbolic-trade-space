# WP46 D-3: the small-temperature fit against the minimum-variance fit on the simplex

Script: `work-packages/WP46-rounds/small_tau_check.py`; output: `small-tau-check-output.txt` (data of record,
primary regime, 2,134 designs, 13 metrics, K = 1, `random_state = 0`).

The log-metrics are centred (largest mean 3e-15) and of unit spread, so by L22 the leading term of the soft maximum
that depends on the exponents is (tau/2) w'Cw with C the covariance of the log-metrics. The check solves
min w'Cw on the simplex directly (SLSQP, converged) and compares it with the estimator at four temperatures.

| tau | largest gap, any exponent | agrees at three places |
|---|---|---|
| 0.01 | 0.0002 | no |
| 0.1 | 0.0001 | no |
| 1 | 0.0007 | no |
| 3 | 0.0021 | no |

At tau = 3 ten of the thirteen exponents agree at three places; total mass is 0.064 against 0.067, unit cost 0.225
against 0.224, fleet cost 0.148 against 0.149. The same eight metrics carry an exponent above 1e-3 in the minimum-variance fit and in the estimator at all four temperatures.

**Result:** the scope's criterion (the tau = 3 fit agrees with the direct fit "to the printed digits") is not met. The
lemma verifies (the expansion, `derivation/lemma_22_small_temperature.py`) but D-3 does not agree, so R-2 gives the
scope's fallback: the page calls the small-tau end a regularity the sweep shows, not a derived limit, and reports
the measured gap as a number on this table. The gaps are small and do not shrink monotonically with tau
(0.0002 at 0.01, 0.0001 at 0.1); the lemma does not bound the remainder, and this check does not separate the
estimator's solver tolerance from the third-moment term L22 names.
