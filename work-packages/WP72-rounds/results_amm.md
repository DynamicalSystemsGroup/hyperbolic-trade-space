# WP72 market maker: results

Uniswap v2 DAI/WETH pair, blocks 12959750 to 12989733: 4327 reserve updates ({'Swap': 4221, 'sync': 67, 'Burn': 25, 'Mint': 14}); 105 stretches of two or more rows.

| estimator | w (DAI, WETH) | note |
|---|---|---|
| invariant fit, stretches given | (0.4989, 0.5011) | within_share 6.28e-05, flatness 5.16e-03 |
| invariant fit, order fallback (no labels) | (0.5008, 0.4992) | 975 breaks found; 38 of the 106 recorded non-swap events and 38 of the 39 Mint and Burn events among them |
| invariant fit, no groups | (0.5200, 0.4800) | minimum variance on the simplex of the whole table |
| PCA within stretches, minor axis | (0.4989, 0.5011) | eigenvalues 4.87e-10 and 1.83e-05 |
| PCA pooled, minor axis | (0.5201, 0.4799) |  |
| frontier fit, tau = 152.6 (a tenth above) | (0.0000, 1.0000) | the boundary of the cloud, not the level |

## The level within and between stretches

- Per swap, within a stretch: median change of log V 1.06e-08, largest 1.36e-04; median absolute change of log(DAI/WETH) 7.82e-05, largest 7.34e-02.
- In exact integers, the product of the reserves rises at 4220 of 4220 swaps (the 0.3 per cent fee stays in the pool); the sum of the per-swap changes of log V over the window is 1.99e-03. Within-group variance of log V at (1/2, 1/2): 2.890e-10; at the fitted w: 2.435e-10; median within-stretch correlation of log(DAI WETH) with log(DAI/WETH): 0.16.
- At a Mint or Burn: median absolute change of log V 1.85e-05, largest 6.64e-03; 11 of 39 exceed the largest single-swap change. At a bare sync: largest absolute change 0.00e+00.
- Over the window: log V from 13.5629 to 13.5723; log(DAI/WETH) from 7.8425 to 8.0679.
