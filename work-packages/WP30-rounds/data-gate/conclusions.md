## primary regime

| config | feasible | metrics | K=1 tau/band/frac/n_eff | K=2 | K=3 |
|---|---|---|---|---|---|
| old8 | 706 | 8 | 38.10 / 0.0262 / 0.092 / 23.1 | 94.42 / 0.0106 / 0.095 / 16.2 | 113.22 / 0.0088 / 0.099 / 18.9 |
| new8 | 2134 | 8 | 26.50 / 0.0377 / 0.106 / 34.9 | 78.75 / 0.0127 / 0.108 / 42.3 | 113.22 / 0.0088 / 0.093 / 38.5 |
| new13 | 2134 | 13 | 41.72 / 0.0240 / 0.098 / 73.6 | 113.22 / 0.0088 / 0.095 / 33.1 | 135.76 / 0.0074 / 0.108 / 56.3 |


| config | K=1 contending set | n-lemma | near-frontier | leading | exponents |
|---|---|---|---|---|---|
| old8 | total mass, energy balance, pointing error, depth of discharge, settling time | 5 | 56 | total mass 0.358, energy balance 0.184, pointing error 0.164 | 0.136 0.164 0.358 0 0 0.184 7.4e-17 0.158 |
| new8 | total mass, energy balance, pointing error, depth of discharge, settling time | 5 | 252 | total mass 0.349, energy balance 0.187, pointing error 0.164 | 0.146 0.164 0.349 0 0 0.187 2.35e-16 0.155 |
| new13 | unit cost, available power, pointing error, fleet cost, momentum headroom, settling time, depth of discharge | 7 | 238 | unit cost 0.257, available power 0.197, pointing error 0.156 | 0.0681 0.156 0.0213 0 2.65e-17 1.79e-17 0 0.0424 0.107 0.197 0 0.257 0.151 |


| config | term | rows | share | K=2 contending set | n-lemma | near-frontier (report) | leading exponents | near rows at K1 band / own band | reach |
|---|---|---|---|---|---|---|---|---|---|
| old8 | 1 | 414 | 0.800 | peak slew power, pointing error, settling time, total mass, power margin | 5 | 73 | peak slew power 0.582, pointing error 0.222, total mass 0.072 | 73/24 | 0.5199 |
| old8 | 2 | 292 | 0.200 | settling time, control effort, energy balance, pointing error, total mass | 5 | 13 | settling time 0.364, control effort 0.344, energy balance 0.267 | 13/6 | 0.5627 |
| old8 | band | K = 1 band 1/tau = 0.026249 |  |  |  |  |  |  |  |
| new8 | 1 | 921 | 0.135 | settling time, control effort, energy balance, total mass, depth of discharge, pointing error | 6 | 38 | settling time 0.369, control effort 0.324, energy balance 0.287 | 38/17 | 0.5707 |
| new8 | 2 | 1213 | 0.865 | peak slew power, pointing error, settling time, total mass, power margin, depth of discharge | 6 | 382 | peak slew power 0.562, pointing error 0.227, total mass 0.080 | 382/109 | 0.5464 |
| new8 | band | K = 1 band 1/tau = 0.03774 |  |  |  |  |  |  |  |
| new13 | 1 | 934 | 0.262 | unit cost, available power, fleet cost, momentum headroom, pointing error, settling time, depth of discharge | 7 | 119 | unit cost 0.250, available power 0.216, fleet cost 0.142 | 119/45 | 0.2023 |
| new13 | 2 | 1200 | 0.738 | peak slew power, pointing error, unit cost, available power, fleet cost, momentum headroom, settling time, depth of discharge | 8 | 318 | peak slew power 0.426, pointing error 0.206, unit cost 0.122 | 318/127 | 0.3999 |
| new13 | band | K = 1 band 1/tau = 0.023972 |  |  |  |  |  |  |  |


| config | term | rows | share | K=3 contending set | n-lemma | near-frontier (report) | leading exponents | near rows at K1 band / own band | reach |
|---|---|---|---|---|---|---|---|---|---|
| old8 | 1 | 181 | 0.034 | control effort, settling time, energy balance, pointing error | 4 | 3 | control effort 0.397, settling time 0.367, energy balance 0.193 | 3/1 | 0.5664 |
| old8 | 2 | 162 | 0.241 | energy balance, total mass, settling time, pointing error, depth of discharge | 5 | 21 | energy balance 0.416, total mass 0.240, settling time 0.185 | 21/7 | 0.4952 |
| old8 | 3 | 363 | 0.724 | peak slew power, pointing error, settling time, total mass, energy balance | 5 | 73 | peak slew power 0.612, pointing error 0.227, total mass 0.059 | 73/21 | 0.5450 |
| old8 | band | K = 1 band 1/tau = 0.026249 |  |  |  |  |  |  |  |
| new8 | 1 | 507 | 0.144 | energy balance, total mass, settling time, depth of discharge, pointing error | 5 | 54 | energy balance 0.457, total mass 0.199, settling time 0.180 | 54/15 | 0.5882 |
| new8 | 2 | 1136 | 0.817 | peak slew power, pointing error, settling time, total mass, power margin, depth of discharge | 6 | 335 | peak slew power 0.600, pointing error 0.232, total mass 0.060 | 335/85 | 0.5803 |
| new8 | 3 | 491 | 0.038 | settling time, control effort, energy balance, pointing error, depth of discharge | 5 | 28 | settling time 0.454, control effort 0.391, energy balance 0.112 | 28/4 | 0.6579 |
| new8 | band | K = 1 band 1/tau = 0.03774 |  |  |  |  |  |  |  |
| new13 | 1 | 621 | 0.344 | energy balance, unit cost, fleet cost, momentum headroom, settling time, pointing error, depth of discharge | 7 | 188 | energy balance 0.384, unit cost 0.238, fleet cost 0.112 | 188/62 | 0.3172 |
| new13 | 2 | 1054 | 0.594 | peak slew power, pointing error, unit cost, available power, fleet cost, momentum headroom, settling time, depth of discharge | 8 | 297 | peak slew power 0.417, pointing error 0.208, unit cost 0.132 | 297/107 | 0.4077 |
| new13 | 3 | 459 | 0.061 | momentum headroom, settling time, total mass, available power, pointing error, depth of discharge, peak slew power, fleet cost | 8 | 50 | momentum headroom 0.223, total mass 0.214, settling time 0.211 | 50/11 | 0.2977 |
| new13 | band | K = 1 band 1/tau = 0.023972 |  |  |  |  |  |  |  |


| config | K | status | max gap | gamma | radius | mean slack (own tau) | mean slack (K=1 tau) | objective |
|---|---|---|---|---|---|---|---|---|
| old8 | 1 | not_applicable | 8.7e-06 | - | - | 0.2434 | 0.2434 | 0.2434 |
| old8 | 2 | certified | 3e-15 | 0.000697 | 6.95e-05 | 0.1823 | 0.1317 | 0.1823 |
| old8 | 3 | certified | 4.1e-15 | 0.00121 | 0.000121 | 0.1458 | 0.0875 | 0.1458 |
| new8 | 1 | not_applicable | 7.2e-06 | - | - | 0.2331 | 0.2331 | 0.2331 |
| new8 | 2 | certified | 2.2e-15 | 0.000855 | 7.93e-05 | 0.1907 | 0.1171 | 0.1907 |
| new8 | 3 | certified | 1.2e-14 | 0.000589 | 5.47e-05 | 0.1615 | 0.0673 | 0.1615 |
| new13 | 1 | not_applicable | 7e-06 | - | - | 0.1218 | 0.1218 | 0.1218 |
| new13 | 2 | certified | 4.1e-15 | 0.000377 | 2.55e-05 | 0.0874 | 0.0434 | 0.0874 |
| new13 | 3 | certified | 3.4e-15 | 0.000421 | 2.85e-05 | 0.0693 | 0.0201 | 0.0693 |


| pair (pearson (spearman)) | old8 | new8 | new13 |
|---|---|---|---|
| pointing error, control effort | -0.36 (-0.50) | -0.41 (-0.48) | -0.52 (-0.66) |
| settling time, pointing error | +0.03 (+0.15) | -0.10 (-0.07) | +0.36 (+0.47) |
| settling time, total mass | -0.50 (-0.50) | -0.19 (-0.14) | -0.46 (-0.46) |


| Spearman among feasible designs | old8 | new8 | new13 |
|---|---|---|---|
| power margin, energy balance | +0.9824 | +0.9817 | +0.9817 |
| available power, energy balance | +0.9996 | +0.9997 | +0.9997 |
| battery peak power ratio, depth of discharge | - | -0.9706 | -0.9706 |


| nondominated view | old8 | new8 | new13 |
|---|---|---|---|
| all attributes | 659 of 706 on 8 (0.9334) | 1868 of 2134 on 8 (0.8754) | 2134 of 2134 on 13 (1.0000) |
| four metrics | 126 of 706 on 4 (0.1785) | 236 of 2134 on 4 (0.1106) | 236 of 2134 on 4 (0.1106) |

## stock regime

| config | feasible | metrics | K=1 tau/band/frac/n_eff | K=2 | K=3 |
|---|---|---|---|---|---|
| old8 | 780 | 8 | 45.68 / 0.0219 / 0.104 / 14.6 | 71.92 / 0.0139 / 0.100 / 14.6 | 113.22 / 0.0088 / 0.091 / 17.3 |
| new8 | 2355 | 8 | 29.01 / 0.0345 / 0.096 / 13.3 | 50.02 / 0.0200 / 0.097 / 15.5 | 94.42 / 0.0106 / 0.096 / 17.1 |
| new13 | 2355 | 13 | 45.68 / 0.0219 / 0.106 / 47.9 | 103.40 / 0.0097 / 0.102 / 36.2 | 135.76 / 0.0074 / 0.096 / 34.5 |


| config | K=1 contending set | n-lemma | near-frontier | leading | exponents |
|---|---|---|---|---|---|
| old8 | control effort, settling time, power margin, pointing error, depth of discharge | 5 | 77 | control effort 0.432, settling time 0.319, power margin 0.178 | 0.319 0.0393 6.5e-17 0.432 0.178 0.0194 4.12e-19 0.012 |
| new8 | control effort, settling time, energy balance, pointing error, depth of discharge | 5 | 332 | control effort 0.435, settling time 0.318, energy balance 0.197 | 0.318 0.0421 0 0.435 0 0.197 4.11e-17 0.00744 |
| new13 | momentum headroom, available power, total mass, settling time, pointing error, depth of discharge, unit cost, fleet cost | 8 | 293 | available power 0.192, momentum headroom 0.181, settling time 0.159 | 0.159 0.0865 0.131 0.0756 0 0 0 0.0619 0.181 0.192 3.26e-20 0.0679 0.0445 |


| config | term | rows | share | K=2 contending set | n-lemma | near-frontier (report) | leading exponents | near rows at K1 band / own band | reach |
|---|---|---|---|---|---|---|---|---|---|
| old8 | 1 | 454 | 0.562 | energy balance, control effort, settling time, depth of discharge | 4 | 57 | control effort 0.363, energy balance 0.324, settling time 0.282 | 57/36 | 0.2553 |
| old8 | 2 | 326 | 0.438 | control effort, settling time, energy balance, pointing error, depth of discharge | 5 | 33 | control effort 0.508, settling time 0.374, energy balance 0.067 | 33/28 | 0.2847 |
| old8 | band | K = 1 band 1/tau = 0.021892 |  |  |  |  |  |  |  |
| new8 | 1 | 1217 | 0.298 | control effort, settling time, energy balance, total mass, depth of discharge | 5 | 131 | control effort 0.500, settling time 0.377, energy balance 0.117 | 131/78 | 0.2864 |
| new8 | 2 | 1138 | 0.702 | energy balance, control effort, settling time, pointing error, depth of discharge | 5 | 335 | energy balance 0.413, control effort 0.311, settling time 0.237 | 335/184 | 0.3452 |
| new8 | band | K = 1 band 1/tau = 0.034465 |  |  |  |  |  |  |  |
| new13 | 1 | 986 | 0.754 | peak slew power, pointing error, unit cost, available power, momentum headroom, fleet cost, settling time, depth of discharge | 8 | 292 | peak slew power 0.378, pointing error 0.174, unit cost 0.123 | 292/141 | 0.3813 |
| new13 | 2 | 1369 | 0.246 | available power, settling time, control effort, momentum headroom, unit cost, pointing error, fleet cost, total mass, depth of discharge | 9 | 92 | settling time 0.223, available power 0.204, control effort 0.185 | 92/46 | 0.1743 |
| new13 | band | K = 1 band 1/tau = 0.021892 |  |  |  |  |  |  |  |


| config | term | rows | share | K=3 contending set | n-lemma | near-frontier (report) | leading exponents | near rows at K1 band / own band | reach |
|---|---|---|---|---|---|---|---|---|---|
| old8 | 1 | 253 | 0.115 | control effort, settling time, energy balance, pointing error, depth of discharge | 5 | 20 | control effort 0.507, settling time 0.368, energy balance 0.074 | 20/6 | 0.3015 |
| old8 | 2 | 185 | 0.462 | peak slew power, pointing error, total mass, power margin, depth of discharge, settling time | 6 | 51 | peak slew power 0.424, pointing error 0.190, total mass 0.163 | 51/24 | 0.5928 |
| old8 | 3 | 342 | 0.423 | energy balance, control effort, settling time, depth of discharge | 4 | 50 | control effort 0.353, energy balance 0.348, settling time 0.277 | 50/22 | 0.2974 |
| old8 | band | K = 1 band 1/tau = 0.021892 |  |  |  |  |  |  |  |
| new8 | 1 | 668 | 0.587 | peak slew power, pointing error, settling time, power margin, total mass | 5 | 229 | peak slew power 0.534, pointing error 0.211, total mass 0.097 | 229/81 | 0.6590 |
| new8 | 2 | 880 | 0.370 | energy balance, control effort, settling time, pointing error, depth of discharge | 5 | 170 | energy balance 0.436, control effort 0.303, settling time 0.225 | 170/51 | 0.4064 |
| new8 | 3 | 807 | 0.043 | control effort, settling time, energy balance | 3 | 47 | control effort 0.507, settling time 0.369, energy balance 0.124 | 47/6 | 0.3362 |
| new8 | band | K = 1 band 1/tau = 0.034465 |  |  |  |  |  |  |  |
| new13 | 1 | 853 | 0.405 | energy balance, settling time, unit cost, control effort, momentum headroom, fleet cost, pointing error, depth of discharge | 8 | 175 | energy balance 0.371, settling time 0.146, control effort 0.133 | 175/66 | 0.2764 |
| new13 | 2 | 705 | 0.061 | control effort, settling time, available power, momentum headroom, pointing error, fleet cost, depth of discharge | 7 | 38 | control effort 0.373, settling time 0.354, available power 0.129 | 38/10 | 0.2473 |
| new13 | 3 | 797 | 0.534 | peak slew power, pointing error, unit cost, momentum headroom, available power, fleet cost, settling time, depth of discharge | 8 | 261 | peak slew power 0.371, pointing error 0.176, unit cost 0.132 | 261/87 | 0.3909 |
| new13 | band | K = 1 band 1/tau = 0.021892 |  |  |  |  |  |  |  |


| config | K | status | max gap | gamma | radius | mean slack (own tau) | mean slack (K=1 tau) | objective |
|---|---|---|---|---|---|---|---|---|
| old8 | 1 | not_applicable | 1.2e-05 | - | - | 0.1786 | 0.1786 | 0.1786 |
| old8 | 2 | certified | 4.4e-15 | 0.00141 | 0.000133 | 0.1417 | 0.1138 | 0.1417 |
| old8 | 3 | certified | 7.6e-15 | 0.00035 | 3.29e-05 | 0.0927 | 0.0462 | 0.0927 |
| new8 | 1 | not_applicable | 3e-05 | - | - | 0.1861 | 0.1861 | 0.1861 |
| new8 | 2 | certified | 5.8e-15 | 0.000297 | 2.6e-05 | 0.1652 | 0.1121 | 0.1652 |
| new8 | 3 | certified | 2.1e-15 | 0.000177 | 1.55e-05 | 0.1242 | 0.0376 | 0.1242 |
| new13 | 1 | not_applicable | 3.2e-05 | - | - | 0.1148 | 0.1148 | 0.1148 |
| new13 | 2 | certified | 5.5e-15 | 0.000263 | 1.75e-05 | 0.0996 | 0.0602 | 0.0996 |
| new13 | 3 | certified | 1.4e-14 | 0.0001 | 6.64e-06 | 0.0803 | 0.0296 | 0.0803 |


| pair (pearson (spearman)) | old8 | new8 | new13 |
|---|---|---|---|
| pointing error, control effort | -0.63 (-0.69) | -0.74 (-0.71) | -0.69 (-0.77) |
| settling time, pointing error | +0.63 (+0.70) | +0.72 (+0.70) | +0.68 (+0.76) |
| settling time, total mass | -0.10 (+0.05) | -0.05 (+0.09) | -0.16 (-0.14) |


| Spearman among feasible designs | old8 | new8 | new13 |
|---|---|---|---|
| power margin, energy balance | +0.9880 | +0.9874 | +0.9874 |
| available power, energy balance | +0.9997 | +0.9997 | +0.9997 |
| battery peak power ratio, depth of discharge | - | -0.9752 | -0.9752 |


| nondominated view | old8 | new8 | new13 |
|---|---|---|---|
| all attributes | 724 of 780 on 8 (0.9282) | 1976 of 2355 on 8 (0.8391) | 2355 of 2355 on 13 (1.0000) |
| four metrics | 152 of 780 on 4 (0.1949) | 306 of 2355 on 4 (0.1299) | 306 of 2355 on 4 (0.1299) |

## regime comparison table (case.regime_comparison)
### old8

| quantity | primary | stock |
|---|---|---|
| dataset | adcs_designs_cubesat_gains.csv | adcs_designs_cubesat.csv |
| feasible n | 706 (191 / 248 / 267) | 780 (239 / 279 / 262) |
| tau, frac_above_, n_eff_ | 38.1, 0.092, 23.1 | 45.7, 0.104, 14.6 |
| band 1/tau, near-frontier designs | 0.0262, 56 | 0.0219, 77 |
| n_lemma | 5 | 5 |
| contending set | total mass, energy balance, pointing error, depth of discharge, settling time | control effort, settling time, power margin, pointing error, depth of discharge |
| settling time, total mass | -0.50 (-0.50) | -0.10 (+0.05) |
| pointing error, control effort | -0.36 (-0.50) | -0.63 (-0.69) |
| settling time, pointing error | +0.03 (+0.15) | +0.63 (+0.70) |

### new8

| quantity | primary | stock |
|---|---|---|
| dataset | adcs_designs_cubesat_gains.csv | adcs_designs_cubesat.csv |
| feasible n | 2134 (548 / 707 / 879) | 2355 (711 / 778 / 866) |
| tau, frac_above_, n_eff_ | 26.5, 0.106, 34.9 | 29.0, 0.096, 13.3 |
| band 1/tau, near-frontier designs | 0.0377, 252 | 0.0345, 332 |
| n_lemma | 5 | 5 |
| contending set | total mass, energy balance, pointing error, depth of discharge, settling time | control effort, settling time, energy balance, pointing error, depth of discharge |
| settling time, total mass | -0.19 (-0.14) | -0.05 (+0.09) |
| pointing error, control effort | -0.41 (-0.48) | -0.74 (-0.71) |
| settling time, pointing error | -0.10 (-0.07) | +0.72 (+0.70) |

### new13

| quantity | primary | stock |
|---|---|---|
| dataset | adcs_designs_cubesat_gains.csv | adcs_designs_cubesat.csv |
| feasible n | 2134 (548 / 707 / 879) | 2355 (711 / 778 / 866) |
| tau, frac_above_, n_eff_ | 41.7, 0.098, 73.6 | 45.7, 0.106, 47.9 |
| band 1/tau, near-frontier designs | 0.0240, 238 | 0.0219, 293 |
| n_lemma | 7 | 8 |
| contending set | unit cost, available power, pointing error, fleet cost, momentum headroom, settling time, depth of discharge | momentum headroom, available power, total mass, settling time, pointing error, depth of discharge, unit cost, fleet cost |
| settling time, total mass | -0.46 (-0.46) | -0.16 (-0.14) |
| pointing error, control effort | -0.52 (-0.66) | -0.69 (-0.77) |
| settling time, pointing error | +0.36 (+0.47) | +0.68 (+0.76) |

## candidates (K = 1, primary)
### old8

| candidate | wheel_class | st_grade | log V | novelty V-1 | rank among training | tau*log V |
|---|---|---|---|---|---|---|
| fast_effort_hungry | large | medium | -0.1973 | -0.179 | 0.5326 | -7.516 |
| precise_heavy_sensor | large | fine | -0.153 | -0.1419 | 0.619 | -5.828 |
| light_slow | small | coarse | -0.1709 | -0.1571 | 0.5822 | -6.511 |

### new8

| candidate | wheel_class | st_grade | log V | novelty V-1 | rank among training | tau*log V |
|---|---|---|---|---|---|---|
| fast_effort_hungry | large | medium | -0.1673 | -0.1541 | 0.5722 | -4.433 |
| precise_heavy_sensor | large | fine | -0.1327 | -0.1243 | 0.6401 | -3.517 |
| light_slow | small | coarse | -0.1462 | -0.136 | 0.6134 | -3.874 |

### new13

| candidate | wheel_class | st_grade | log V | novelty V-1 | rank among training | tau*log V |
|---|---|---|---|---|---|---|
| fast_effort_hungry | large | medium | -0.1622 | -0.1497 | 0.328 | -6.767 |
| precise_heavy_sensor | large | fine | -0.1299 | -0.1219 | 0.4508 | -5.421 |
| light_slow | small | coarse | -0.4023 | -0.3312 | 0.006092 | -16.78 |

## propose-predict-check (primary)
### old8: regressor tau 10.6906, band 0.0935

| proposal | predicted log V | measured log V | difference | |diff| / band | log V within band | ||dZ|| | ||dZ|| / band | Z within band |
|---|---|---|---|---|---|---|---|---|
| proposal_1 | -0.09517 | -0.04681 | 0.04837 | 0.5171 | 1 | 0.09864 | 1.054 | 0 |
| proposal_2 | 0.02481 | 0.0567 | 0.03189 | 0.3409 | 1 | 0.04733 | 0.506 | 1 |
| proposal_3 | -0.09517 | -0.04681 | 0.04837 | 0.5171 | 1 | 0.09864 | 1.054 | 0 |


| name | wheel_class | st_grade | hole_score | distance_to_target | recorded log V | refit log V | max |recorded - refit| |
|---|---|---|---|---|---|---|---|
| proposal_1 | medium | fine | 4.848 | 0.5868 | -0.09517 | -0.09517 | 4.706e-09 |
| proposal_2 | medium | fine | 4.846 | 0.5795 | 0.02481 | 0.02481 | 1.35e-09 |
| proposal_3 | medium | fine | 4.835 | 0.5552 | -0.09517 | -0.09517 | 4.706e-09 |

### new13: regressor tau 10.6906, band 0.0935

| proposal | predicted log V | measured log V | difference | |diff| / band | log V within band | ||dZ|| | ||dZ|| / band | Z within band |
|---|---|---|---|---|---|---|---|---|
| proposal_1 | -0.03629 | 0.00615 | 0.04244 | 0.4537 | 1 | 0.01698 | 0.1815 | 1 |
| proposal_2 | 0.1031 | 0.1641 | 0.06108 | 0.653 | 1 | 0.07704 | 0.8236 | 1 |
| proposal_3 | -0.03629 | 0.00615 | 0.04244 | 0.4537 | 1 | 0.01698 | 0.1815 | 1 |


| name | wheel_class | st_grade | hole_score | distance_to_target | recorded log V | refit log V | max |recorded - refit| |
|---|---|---|---|---|---|---|---|
| proposal_1 | medium | fine | 7.302 | 0.6742 | -0.03629 | -0.03629 | 1.617e-06 |
| proposal_2 | medium | fine | 7.101 | 0.6782 | 0.1031 | 0.1031 | 1.634e-06 |
| proposal_3 | medium | fine | 7.032 | 0.6262 | -0.03629 | -0.03629 | 1.617e-06 |

## predictions and checks files
### old8

| name | wheel_class | st_grade | hole_score | distance_to_target | tau | band | pred_log_v |
|---|---|---|---|---|---|---|---|
| proposal_1 | medium | fine | 4.848 | 0.5868 | 10.69 | 0.09354 | -0.09517 |
| proposal_2 | medium | fine | 4.846 | 0.5795 | 10.69 | 0.09354 | 0.02481 |
| proposal_3 | medium | fine | 4.835 | 0.5552 | 10.69 | 0.09354 | -0.09517 |


| name | role | settled | momentum_ok | power_ok | dod_ok | settling_time_s | dod_eclipse | battery_wh |
|---|---|---|---|---|---|---|---|---|
| fast_effort_hungry | candidate | 1 | 1 | 1 | 1 | 15.56 | 0.0921 | 90 |
| precise_heavy_sensor | candidate | 1 | 1 | 1 | 1 | 14.87 | 0.06181 | 140 |
| light_slow | candidate | 1 | 1 | 1 | 1 | 71.67 | 0.1995 | 40 |
| proposal_1 | proposal | 1 | 1 | 1 | 0 | 55.7 | 0.3402 | 25.4 |
| proposal_2 | proposal | 1 | 1 | 1 | 0 | 42.98 | 0.3935 | 21.96 |
| proposal_3 | proposal | 1 | 1 | 1 | 0 | 55.7 | 0.3402 | 25.4 |

### new13

| name | wheel_class | st_grade | hole_score | distance_to_target | tau | band | pred_log_v |
|---|---|---|---|---|---|---|---|
| proposal_1 | medium | fine | 7.302 | 0.6742 | 10.69 | 0.09354 | -0.03629 |
| proposal_2 | medium | fine | 7.101 | 0.6782 | 10.69 | 0.09354 | 0.1031 |
| proposal_3 | medium | fine | 7.032 | 0.6262 | 10.69 | 0.09354 | -0.03629 |


| name | role | settled | momentum_ok | power_ok | dod_ok | settling_time_s | dod_eclipse | battery_wh |
|---|---|---|---|---|---|---|---|---|
| fast_effort_hungry | candidate | 1 | 1 | 1 | 1 | 15.56 | 0.0921 | 90 |
| precise_heavy_sensor | candidate | 1 | 1 | 1 | 1 | 14.87 | 0.06181 | 140 |
| light_slow | candidate | 1 | 1 | 1 | 1 | 71.67 | 0.1995 | 40 |
| proposal_1 | proposal | 1 | 1 | 1 | 0 | 42.98 | 0.3935 | 21.96 |
| proposal_2 | proposal | 1 | 1 | 1 | 0 | 32.25 | 0.3904 | 22.14 |
| proposal_3 | proposal | 1 | 1 | 1 | 0 | 42.98 | 0.3935 | 21.96 |

