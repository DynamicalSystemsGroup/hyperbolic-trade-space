### primary: held-out measures, mean over five folds

| index | tau (full table) | train above | slack | above | band | rtail_slack | rtail_above | ltail_slack | ltail_above | d slack vs K1 | d rtail slack vs K1 | flagged folds | not optimal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 41.7158 | 0.1000 | 0.1400 | 0.0979 | 0.1069 | 0.1408 | 0.0604 | 0.1930 | 0.0267 | +0.0000 (0.0000) | +0.0000 (0.0000) | 0 | 0 |
| K1c | 41.7158 | 0.1007 | 0.1404 | 0.0984 | 0.1054 | 0.1412 | 0.0630 | 0.1932 | 0.0267 | +0.0004 (0.0002) | +0.0004 (0.0009) | 0 | 0 |
| K2 | 113.2193 | 0.0982 | 0.0978 | 0.0994 | 0.0872 | 0.1226 | 0.0354 | 0.1268 | 0.0290 | -0.0422 (0.0023) | -0.0181 (0.0041) | 0 | 0 |
| K2s | 113.2193 | 0.0743 | 0.1012 | 0.0755 | 0.0708 | 0.1276 | 0.0264 | 0.1312 | 0.0170 | -0.0388 (0.0024) | -0.0131 (0.0046) | 0 | 0 |
| K3 | 135.7564 | 0.1017 | 0.0803 | 0.0979 | 0.0750 | 0.0865 | 0.1288 | 0.0900 | 0.0453 | -0.0597 (0.0023) | -0.0543 (0.0046) | 0 | 0 |
| LQ | 403.4597 | 0.0988 | 0.0530 | 0.0984 | 0.0656 | 0.0435 | 0.1335 | 0.0745 | 0.0871 | -0.0870 (0.0032) | -0.0972 (0.0043) | 0 | 0 |
| LQm | 94.4236 | 0.1006 | 0.0864 | 0.1008 | 0.0942 | 0.0774 | 0.1062 | 0.1094 | 0.0740 | -0.0536 (0.0024) | -0.0633 (0.0027) | 0 | 0 |

Post hoc (amendment 2), the monotone log-quadratic term LQm, paired difference in slack (mean over folds, standard error):

| index | hugs better than K1 | minus K2 | minus K3 | minus LQ |
|---|---|---|---|---|
| all rows | True | -0.0114 (0.0012) | +0.0061 (0.0007) | +0.0335 (0.0012) |
| rtail_ | False | -0.0452 (0.0053) | -0.0091 (0.0035) | +0.0339 (0.0037) |

Verdict, all held-out rows: **a kernel's work**. Verdict, right tail: **a kernel's work**.


LQm on the whole table: rank of S 6, rows with a negative partial derivative 0.387.


LQ on the whole table: rank of S 9, rows with a negative partial derivative 1.000.


### stock: held-out measures, mean over five folds

| index | tau (full table) | train above | slack | above | band | rtail_slack | rtail_above | ltail_slack | ltail_above | d slack vs K1 | d rtail slack vs K1 | flagged folds | not optimal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 45.6794 | 0.1048 | 0.1324 | 0.1045 | 0.1223 | 0.1125 | 0.1896 | 0.1880 | 0.0473 | +0.0000 (0.0000) | +0.0000 (0.0000) | 0 | 0 |
| K1c | 45.6794 | 0.1045 | 0.1330 | 0.1053 | 0.1219 | 0.1134 | 0.1928 | 0.1885 | 0.0479 | +0.0005 (0.0002) | +0.0009 (0.0006) | 0 | 0 |
| K2 | 103.3952 | 0.1000 | 0.1136 | 0.0985 | 0.0777 | 0.1140 | 0.1008 | 0.0854 | 0.1399 | -0.0188 (0.0041) | +0.0015 (0.0058) | 0 | 0 |
| K2s | 103.3952 | 0.0745 | 0.1168 | 0.0739 | 0.0650 | 0.1180 | 0.0813 | 0.0876 | 0.0987 | -0.0156 (0.0040) | +0.0055 (0.0059) | 0 | 0 |
| K3 | 135.7564 | 0.1028 | 0.0888 | 0.0985 | 0.0701 | 0.0820 | 0.1200 | 0.0696 | 0.1266 | -0.0436 (0.0037) | -0.0304 (0.0041) | 0 | 0 |
| LQ | 162.7798 | 0.1035 | 0.0720 | 0.1049 | 0.0743 | 0.0853 | 0.1387 | 0.0656 | 0.1110 | -0.0605 (0.0028) | -0.0271 (0.0062) | 0 | 0 |
| LQm | 113.2193 | 0.0993 | 0.0942 | 0.1049 | 0.0824 | 0.0977 | 0.1422 | 0.0883 | 0.1232 | -0.0383 (0.0025) | -0.0147 (0.0043) | 0 | 0 |

Post hoc (amendment 2), the monotone log-quadratic term LQm, paired difference in slack (mean over folds, standard error):

| index | hugs better than K1 | minus K2 | minus K3 | minus LQ |
|---|---|---|---|---|
| all rows | True | -0.0194 (0.0017) | +0.0054 (0.0013) | +0.0222 (0.0003) |
| rtail_ | True | -0.0163 (0.0039) | +0.0157 (0.0013) | +0.0124 (0.0042) |

Verdict, all held-out rows: **a kernel's work**. Verdict, right tail: **more terms' work**.


LQm on the whole table: rank of S 8, rows with a negative partial derivative 0.098.


LQ on the whole table: rank of S 9, rows with a negative partial derivative 1.000.

