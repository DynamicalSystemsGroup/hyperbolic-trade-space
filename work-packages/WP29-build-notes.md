# WP29 build notes (stages 3 and 4, branch `wp29`)

Derivation-side readout. Nothing here has reached `dev` (OD2 (b)).

## What was built

| Item | File | State |
|---|---|---|
| A3, L18 | `derivation/lemma_18_noise_covariance.py` (21 tagged steps) | passes |
| A1, L19 | `derivation/lemma_19_noise_shift_bound.py` (44 tagged steps) | passes |
| ledger | `derivation/axioms.py`: A9 (Gaussian vector with a covariance), A10 (multiplicative measurement error), A11 (row noise), I17 (expectation: linear, monotone, Jensen), F19 (maximum of the noise draws) | every new entry is consumed by a lemma |
| chain, record | `derivation/run.py`, `derivation/proof_map_record.json` | PROOF MAP OK, 19 files, 439 steps |
| tests | `tests/test_noise_lemmas.py` (seeds from `WP29_SEEDS`, default 0,1) | passes for seeds 0,1; 7,8; 21,22 |
| experiment | `examples/adcs/noise_injection.py` | reproduces the spike's `check3-output.txt` (every figure equal) and itself twice (identical output) |
| Appendix B | `paper/supporting_material.ipynb`, cells `tab-B-*` and `tab-F-commands` | see below |

Existing tests changed (requirement kept, position now relative to a named lemma instead of the end of the chain, count 17 to 19):
`tests/test_derivation.py` (two `CHAIN_NAMES[-n]` slices), `tests/test_proof_map.py` (two), `tests/test_build_generated.py`
(`len(R.CHAIN) == 19`).

## Held and dropped

- **A2** (the ridge reading): held as a tested-by-spike statement. Its check script stays at
  `work-packages/WP23-rounds/spikes/spike-E-noise/check2_noise_is_ridge.py` (output `check2-output.txt`). The gaps-ledger row
  is proposed in `WP29-placement-proposal.md`, not landed. No lemma built.
- **A4** (tau under noise) dropped; **A5** (risk-averse certainty equivalent) recorded only.

## Findings that move the statements

1. The spike read "loose by a factor of 2 to 6 at tau = 50 to 200" against the L6 branch alone. Against the smaller upper
   bound the planted cells give a ratio of 0.95 to 1.1 where tau v^2 / 2 is the smaller, and up to about 2.6 at tau = 200
   (L6 alone up to about 12). The lemma text and the test carry the corrected figures.
2. The lower bound mean(s) - LME(s) was at most 0 and weaker than Delta >= 0. Replaced (PM decision) by Delta >= 0: the
   tangent line with the softmax weights p_i of the clean scores gives LME(s+z) - LME(s) >= Sum_i p_i z_i, and E z_i = 0.
3. tau* = 2 sqrt(2 log n) / v is the crossing of tau v^2 / 2 with the closed-form bound v sqrt(2 log n), not with E max z
   (which is smaller): the cold read caught the misidentification and the lemma now says so.
4. The spike's "the isotropic A5 reading is off by 10 to 20 times everywhere" does not hold where the offset shift saturates:
   primary regime at 10 percent, shift 0.199, diagonal L6 5.665, isotropic 0.444. The diagonal form tracks the shift where
   tau w'Sigma w / 2 is below the max bound (primary 0.5 percent: 0.013 against 0.014; stock 2 percent: 0.001 against
   0.004) and overshoots beyond it. The table's claim is narrowed accordingly in the proposal.
5. s_j = 1/|alpha_j| is a definition (the convention of standardising conditioning), not a derived fact; the lemma says so.

## OD3

Foellmer-Knispel's page was not opened (403 earlier; an arXiv id guess and the arXiv search returned a wrong paper and no
result). Fallback (b): no citation. The proposal calls the entropic reading a derivation from L6. Boyd and Vandenberghe
section 3.1.8, inequality (3.5), f(E x) <= E f(x), was opened in the authors' PDF and is cited in I17.

## Open edges for the gate

- Appendix B placement: L18 and L19 fall into the second part ("The solver for K > 1 ...") because `PARTS` in
  `paper/generate_proofs.py` ends it at the last lemma. They belong with the fit and its geometry, or a third part. Not
  changed (the paper's file).
- Files marked "host-recorded, re-pin at the gate": none (no exact-equality reference was touched).
- Citations in I17 for monotonicity and linearity of E are the general Billingsley reference, in the style of I5; not opened.
