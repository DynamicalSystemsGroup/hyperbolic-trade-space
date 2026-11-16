# The K = 1 fit within each wheel class, both regimes

The one-term fit refitted on the designs of each wheel class. The table is `generate_results.refits_by_category`, read from the data of record and written by `uv run python paper/generate_supplement.py`.

Dataset cubesat-primary:

| wheel_class | designs | tau | frac_above_ | n_eff_ | n_lemma | contending set | largest exponent at |
|---|---|---|---|---|---|---|---|
| small | 548 | 234 | 0.09307 | 22.57 | 8 | pointing error, peak slew power, unit cost, fleet cost, available power, battery peak power ratio, settling time, control effort | pointing error |
| medium | 707 | 234 | 0.09335 | 12.02 | 8 | pointing error, peak slew power, unit cost, available power, fleet cost, battery peak power ratio, control effort, momentum headroom | pointing error |
| large | 879 | 113.2 | 0.1035 | 35.43 | 9 | pointing error, energy balance, unit cost, peak slew power, fleet cost, momentum headroom, depth of discharge, settling time, total mass | pointing error |

Dataset cubesat-stock:

| wheel_class | designs | tau | frac_above_ | n_eff_ | n_lemma | contending set | largest exponent at |
|---|---|---|---|---|---|---|---|
| small | 711 | 78.75 | 0.09001 | 16.4 | 8 | unit cost, available power, fleet cost, pointing error, momentum headroom, battery peak power ratio, settling time, peak slew power | unit cost |
| medium | 778 | 54.77 | 0.1003 | 18.6 | 8 | available power, momentum headroom, settling time, pointing error, unit cost, fleet cost, total mass, battery peak power ratio | momentum headroom |
| large | 866 | 65.68 | 0.097 | 26.84 | 8 | momentum headroom, available power, settling time, unit cost, pointing error, fleet cost, depth of discharge, total mass | momentum headroom |
