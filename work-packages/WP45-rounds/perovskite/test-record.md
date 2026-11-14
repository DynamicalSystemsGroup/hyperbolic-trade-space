# WP45 test record: perovskite solar cells (Perovskite Database Project)

Written to test the method, not to convince; reported whether it passes or not (`WP45-scope-of-work.md`, R-7).

## 1. Expected n-lemma, written from the literature before any fit (2026-11-14)

No fit of this table had been run when this section was committed.

**Metrics (the default-scan JV attributes, all larger is better, no inversion):** open-circuit voltage Voc, short-circuit
current density Jsc, fill factor FF. Power conversion efficiency (PCE) is the product of the three over the input
power, so it is derived and set aside, as launch cost is in the cubesat case.

**The named trade-off.** Under the detailed-balance limit (Shockley and Queisser 1961, doi:10.1063/1.1736034, record
resolved through Crossref 2026-11-14; full text not read here) a wider band gap raises the voltage a cell can
deliver and lowers the current it can collect. Voc against Jsc is the dilemma. In that limit FF is a function of Voc
alone (it rises weakly with Voc), so FF rides with Voc and is not an independent third constraint.

**Expected n-lemma at tau = infinity, K = 1:** the contending set contains Voc and Jsc, with a negative elasticity
between them (a gain in one is paid in the other along the frontier). FF is expected outside the set or with a
small exponent; its inclusion would make a trilemma and is not excluded by the literature, only not expected.

**Pass:** Voc and Jsc both in the contending set. **Fail:** either missing from it. FF's membership and the exponents'
values are recorded either way. K = 2 is read the same way, per term (expected: the terms split by band-gap regime or
architecture, not asserted).

**Stated before the fit, as expected limits of the data:** devices are not a sampler (thousands of groups, a
publication bias toward high efficiency), so the frontier is the field's best practice and not a physical bound;
FF has a practical ceiling near 0.85 where many devices cluster.

## 2. Source (to be filled when fetched)
