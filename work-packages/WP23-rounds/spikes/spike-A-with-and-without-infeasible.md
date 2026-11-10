# Spike A: the fit with and without the infeasible designs (WP23)

Question (supervisor, `WP23-decisions.md`, "Requirements and the trade study"): the trade study
with and without the data for the infeasible designs; the fit without the requirements imposed,
then how it changes with the requirements pre-imposed (constrained against unconstrained). Data of
record `examples/adcs/data/v2/` (primary `adcs_designs_cubesat_gains.csv`, baseline
`adcs_designs_cubesat.csv`, 1000 designs each); fits through `case.py`'s own path (conditioning,
temperature by the fraction-above rule at each K, seed 0, K = 1 and 3); the four thresholds of
`WP23-decisions.md` "The four thresholds" read as `<=`. Scripts: the session scratchpad
`spike-A/spike_a.py`, `spike_a2.py` (not in the repository); every number below is theirs.

**Verdict in one paragraph.** Removing the infeasible designs changes the fit little; imposing the
four requirements changes it a lot. In the primary regime the unflagged and the feasible fits
share the contending set, the leading exponents (within 0.03), the zero set and the temperature,
and the three-term fit keeps its three term types: the flag failures lie inside the surface (11 of
76 near-frontier designs, none of the 20 highest V, all momentum failures). The
requirement-constrained set drops every large wheel (267 designs, none near the feasible frontier)
and, through the control effort limit, 18 of the 56 near-frontier designs, after which the
one-term fit is no longer a mass-energy-pointing trade but pointing error against peak slew power:
the feasible fit's largest three-term term (share 0.72) promoted to the whole surface. In the
baseline regime the flags do cut the frontier's ends (unsettled designs at the low-effort end,
momentum failures at the high-gain end: 5 of the 20 highest V), and the pointing error requirement
removes 42 of the 77 near-frontier designs (the coarse tracker), flattening the exponents to a
six-metric set with no leader. Constraining reveals no new trade; it removes the designs that
carried one and promotes another the unconstrained one-term fit blended away.

## The design sets

| set | definition | primary | baseline |
|---|---|---|---|
| U9 | every design whose nine attributes are positive; no flag applied | 869 | 869 |
| U8 | all designs, eight metrics (eclipse reserve dropped) | 1000 | 1000 |
| F | `case.feasible_mask`: settled, power_ok, momentum_ok and positivity | 706 | 780 |
| R | F and the four thresholds (2.6 W, 0.008495 degree, 0.05922 N·m·s, 15.107 kg) | 288 | 302 |

Two facts shape the sets. "All 1000 designs on the nine metrics" cannot be fitted: the eclipse
reserve is a signed slack, at or below zero on 131 designs per regime, exactly the `dod_ok`
failures (the identity of `spike-redundancy.md`, pair 1), and a metric must be positive. U is
therefore read two ways, U9 (positivity only) and U8 (the reserve dropped); the two agree
everywhere below (contending sets equal or differing by one trailing metric, exponents within
0.01). And the case's three flags with positivity are the four generation flags, `dod_ok` being
false if and only if the reserve is not positive, so F is 706 and 780 either way. The thresholds admit 364 and 372 of the 1000 designs, 288 of 706 (40.8 %) and 302
of 780 (38.7 %) of the feasible ones, more than the product of the four pass fractions (33 %, 37 %),
and no large wheel (2.6 W). The baseline configuration (medium wheels, medium tracker, 0.6 m,
80 Wh, Kp 0.03, Kd 0.3; measured once through `cubesat_model.measure`) fails the chosen pointing
error threshold (0.015535 > 0.008495 degree) and is not in R's region.

## The one-term fit by set

| regime | set | n | tau | n_eff_ | contending set (largest first) | leading exponents | zero at every tau of the sweep | signs of the leading pairs (near-frontier Pearson) |
|---|---|---|---|---|---|---|---|---|
| primary | U9 | 869 | 38.1 | 34.6 | total mass, energy balance, pointing error, depth of discharge, settling time | mass 0.332, energy 0.216, pointing 0.162 | power margin, eclipse reserve, peak slew power | mass/energy −0.57; mass/pointing −0.63; energy/pointing +0.15 |
| primary | U8 | 1000 | 38.1 | 35.0 | total mass, energy balance, pointing error, settling time, depth of discharge | mass 0.324, energy 0.221, pointing 0.160 | power margin, peak slew power | mass/energy −0.52; mass/pointing −0.60; energy/pointing −0.01 |
| primary | F | 706 | 38.1 | 23.1 | total mass, energy balance, pointing error, depth of discharge, settling time | mass 0.358, energy 0.184, pointing 0.164 | power margin, eclipse reserve, peak slew power | mass/energy −0.39; mass/pointing −0.56; energy/pointing −0.15 |
| primary | R | 288 | 65.7 | 7.6 | pointing error, peak slew power, total mass, power margin, settling time, depth of discharge | pointing 0.296, peak slew 0.240, mass 0.158 | energy balance, eclipse reserve | pointing/peak slew −0.96; pointing/mass −0.49; peak slew/mass +0.57 |
| baseline | U9 | 869 | 31.8 | 19.6 | control effort, settling time, energy balance, power margin, total mass, pointing error, depth of discharge | effort 0.402, settling 0.305, power margin 0.204 | peak slew power | effort/settling −0.94; effort/energy −0.33; settling/energy +0.01 |
| baseline | U8 | 1000 | 31.8 | 21.2 | control effort, settling time, power margin, pointing error, total mass | effort 0.407, settling 0.310, power margin 0.205 | peak slew power | effort/settling −0.94; effort/power margin −0.26; settling/power margin −0.07 |
| baseline | F | 780 | 45.7 | 14.6 | control effort, settling time, power margin, pointing error, depth of discharge | effort 0.432, settling 0.319, power margin 0.178 | peak slew power | effort/settling −0.95; effort/power margin −0.34; settling/power margin +0.03 |
| baseline | R | 302 | 31.8 | 11.0 | control effort, settling time, power margin, total mass, pointing error, depth of discharge | power margin 0.215, effort 0.205, mass 0.188 | energy balance, eclipse reserve, peak slew power | effort/settling −0.82; effort/power margin −0.33; settling/power margin −0.18 |

Fraction above V = 1 is 0.09 to 0.11 in every row (the rule). Three-term fits, all `certified`,
temperature re-selected at K = 3 (sets as the term's contending set, largest exponent first):

| regime | set | tau | shares | term 1 | term 2 | term 3 |
|---|---|---|---|---|---|---|
| primary | U9 | 135.8 | 0.85 / 0.00 / 0.15 | peak slew power 0.67, pointing error 0.24, settling time, power margin, total mass (96 rows near) | settling time 0.40, control effort 0.38, energy balance, pointing error (2 near: thin) | energy balance 0.39, total mass 0.22, settling time 0.22, pointing error, depth of discharge (29 near) |
| primary | F | 113.2 | 0.24 / 0.03 / 0.72 | energy balance 0.42, total mass 0.24, settling time 0.19, pointing error, depth of discharge (21 near) | control effort 0.40, settling time 0.37, energy balance, pointing error (3 near: thin) | peak slew power 0.61, pointing error 0.23, settling time, total mass, energy balance (73 near) |
| primary | R | 336.5 | 0.70 / 0.20 / 0.10 | pointing error 0.31, peak slew power 0.26, total mass 0.18, power margin, settling time, eclipse reserve, depth of discharge (24 near) | pointing error 0.23, energy balance 0.22, total mass 0.19, settling time, control effort, depth of discharge (11 near) | eclipse reserve 0.38, pointing error 0.21, peak slew power 0.16, total mass, settling time, power margin (15 near) |
| baseline | U9 | 94.4 | 0.76 / 0.07 / 0.17 | peak slew power 0.50, pointing error 0.21, total mass 0.11, power margin, settling time, depth of discharge (100 near) | control effort 0.50, settling time 0.36, pointing error, eclipse reserve, energy balance (17 near) | control effort 0.37, energy balance 0.31, settling time 0.29, pointing error, total mass, eclipse reserve (37 near) |
| baseline | F | 113.2 | 0.12 / 0.45 / 0.43 | control effort 0.51, settling time 0.37, energy balance, pointing error, depth of discharge (20 near) | peak slew power 0.43, pointing error 0.19, total mass 0.16, power margin, settling time, depth of discharge (52 near) | control effort 0.35, energy balance 0.35, settling time 0.28, depth of discharge (50 near) |
| baseline | R | 162.8 | 0.63 / 0.00 / 0.38 | energy balance 0.36, control effort 0.28, settling time 0.24, pointing error, peak slew power, depth of discharge (26 near) | control effort 0.44, settling time 0.30, power margin 0.16, pointing error, depth of discharge, peak slew power (20 near) | total mass 0.27, pointing error 0.21, power margin 0.16, peak slew power, depth of discharge, settling time (18 near) |

U8's three terms are U9's with the shares permuted (primary 0.08 / 0.72 / 0.21; baseline
0.07 / 0.66 / 0.27). Term signs where readable: peak slew power against pointing error is −0.97 to
−1.00 in every term that carries both (the tracker grade sets both); control effort against
settling time −0.95 to −1.00; energy balance against total mass −0.3 to −0.5.

## Who carried the frontier

Near-frontier designs of the wider fit (|log V| < 1/tau at K = 1) that the narrower set drops, by
the condition that drops them:

| step | regime | near-frontier dropped | of | by condition | cells dropped | of the 20 highest V dropped |
|---|---|---|---|---|---|---|
| U9 to F | primary | 11 | 76 | momentum_ok 11 | medium/fine 5, medium/medium 2, small ×4 | 0 |
| U8 to F | primary | 11 | 67 | momentum_ok 11; dod_ok 0 | as above | 0 |
| F to R | primary | 19 | 56 | control effort 18, pointing error 1; peak slew power 0, mass 0 | medium/fine 9, medium/medium 9, small/coarse 1 | 2 |
| U9 to F | baseline | 6 | 111 | settled 3, momentum_ok 3 | small/coarse 3, others 1 each | 5 |
| U8 to F | baseline | 27 | 134 | dod_ok 18, settled 7, momentum_ok 4 | spread over all nine cells | 6 |
| F to R | baseline | 43 | 77 | pointing error 42, peak slew power 2, effort 1, mass 1 | small/coarse 20, small/medium 7, medium/coarse 5, large ×4 | 7 |

Read in the F fit, the R designs keep F's highest log V in both regimes (+0.1205, +0.1112) and 37
of 56 (primary) and 34 of 77 (baseline) of its near-frontier designs: the requirements cut the
frontier's flanks, not its top. In the primary regime no large wheel is near the feasible K = 1
frontier (the mass exponent 0.36 keeps them inside), so the 2.6 W limit removes 267 designs and
no near-frontier one; the control effort limit does the cutting. In the baseline regime the
pointing error limit does: the coarse tracker's low-gain designs are the low-effort end of the
effort-against-settling-time trade (−0.95), and they fail 0.008495 degree.

Why the one-term R fit changes shape in the primary regime although the top survives: with the
large wheels gone, the peak slew power takes one value per small or medium cell (1.30 to 2.6 W),
so the tracker grade sets its spread as it sets the pointing error's; the −0.96 pair becomes the
surface's leading tension, and energy balance, which traded against mass over the large wheels,
drops to zero at every temperature. The constrained one-term surface is the feasible three-term
fit's largest term (peak slew power 0.61, pointing error 0.23, share 0.72) re-weighted. In the
baseline regime the loss of the coarse tracker takes the pointing error's spread with it and the
exponents flatten (five metrics between 0.10 and 0.22, n_eff_ 11).

## The baseline configuration, the candidates and the proposals

log V at K = 1 / K = 3 (rank among training designs at K = 1 in brackets); the band is 1/tau:

| design | primary U9 | primary F | primary R | baseline U9 | baseline F | baseline R |
|---|---|---|---|---|---|---|
| baseline configuration | −0.46 / −0.23 (0.11) | −0.52 / −0.25 (0.10) | −0.93 / −0.66 (0.00) | −0.07 / −0.12 (0.70) | −0.06 / −0.08 (0.75) | −0.26 / −0.20 (0.27) |
| fast_effort_hungry (large wheel) | −0.20 / −0.21 (0.48) | −0.20 / −0.23 (0.53) | −1.42 / −0.50 (0.00) | −0.14 / −0.15 (0.50) | −0.20 / −0.20 (0.32) | −0.40 / −0.42 (0.10) |
| precise_heavy_sensor (large wheel) | −0.15 / −0.04 (0.59) | −0.15 / −0.04 (0.62) | −1.06 / −0.32 (0.00) | +0.02 / +0.01 (0.93) | −0.06 / −0.04 (0.74) | −0.31 / −0.17 (0.20) |
| light_slow | −0.18 / +0.01 (0.54) | −0.17 / +0.02 (0.58) | −0.07 / −0.02 (0.65) | −0.34 / −0.00 (0.16) | −0.38 / −0.01 (0.11) | −0.24 / −0.03 (0.32) |
| proposals 1 = 3, 2 (nine metrics) | not placeable | not placeable | not placeable | not placeable | not placeable | not placeable |

The baseline configuration sits deep inside the primary surface (rank 0.10) and near the baseline
regime's (2.6 bands, rank 0.75); in the primary R fit it is below every training design, and it
fails the pointing error threshold anyway. The two large-wheel candidates, read in a surface fitted
with no large wheel, fall to log V −1.4 and −1.1 (rank 0.00): the constrained fit extrapolated to
designs the constraint excluded, about seven times further off than in F. light_slow is the one
candidate on a term in every three-term fit (|log V| at most 0.03).

The proposals (rows `proposal_1` and `proposal_3` are the same configuration) have a negative
eclipse reserve (depth of discharge 0.34 and 0.39 against 0.3), so no nine-metric fit can place
them: the conditioning refuses them, which is the depth-of-discharge requirement said by the
preconditioner. Where they can be read:

| view | set | K = 1 log V (rank) | K = 3 log V (term) |
|---|---|---|---|
| eight metrics, primary | U8 (1000) | −0.61, −0.71 (0.05, 0.02) | −0.011, −0.067 (the peak-slew/pointing term; 1.4 and 9 bands) |
| eight metrics, primary | F8 (706) | −0.57, −0.66 (0.07, 0.04) | −0.029, −0.081 (the peak-slew/pointing term; 3 and 9 bands) |
| four metrics (the proposal view), primary | U4 (1000) | +0.054, +0.129 (0.92, 0.95) | |
| four metrics, primary | F4 (706) | −0.047, +0.057 (0.87, 0.93); within 0.6 band | |
| eight metrics, baseline | U8 / F8 | −0.96, −0.79 / −1.15, −0.96 | −0.05, −0.11 / −0.12, −0.17 |

On the four metrics they were aimed at, the proposals sit on or beyond the surface whether or not
the infeasible designs are in the fit (U4: beyond by 0.6 and 1.4 bands; F4: within 0.6 band); on
the full metric set they are below the one-term surface and near its peak-slew/pointing term at
K = 3; and they are infeasible by depth of discharge. The answer to the pending popup is therefore
in the data: the proposals reached the four-metric frontier by spending the battery (25 and 22 Wh,
the bottom of the range), and the nine-metric fit cannot see them at all.

## Presentation: constrained against unconstrained in the full case analysis

The full case analysis is Appendix D of `paper/supporting_material.ipynb` and the case section of
`docs/examples.md`. Options, at most one table and one figure:

**Where.**
(a) Two rows per regime in D.5 "Sensitivity variants" (`case.sensitivity_table` already has the
shape: variant, setting, tau, frac_above_, n_eff_, contending set, largest exponent, shared with
baseline): "all designs (positive metrics)" and "designs meeting the four requirements". No new
section; the reading is one paragraph under the table.
(b) A new D.10 "The fit with and without the infeasible designs": the one-term table above (U, F,
R by regime) and the who-carried-the-frontier table merged into one (set, n, contending set,
leading exponents, near-frontier designs the step removed and by which condition).
(c) Both: the rows in D.5 for the fit, and the who-carried table in D.10 for the analysis.

**The one figure.**
(i) An exponent strip: metrics on the rows, U / F / R on the columns, one panel per regime, grey
by exponent (the K = 1 column of `tau_sweep_figure` repeated three times); shows the set change
and the zero set, nothing else.
(ii) The log-plane slice of pointing error against peak slew power in the primary regime with the
F and the R one-term surfaces drawn and the excluded designs in grey: shows the cut and the
promoted term in one picture; needs a new `case.py` figure function.
(iii) No figure: the table carries it (the ink is categorical).

**The paper's sentence, if any.**
(1) "Fitted on the feasible designs and on the designs that also meet the four requirements, the
one-term frontier changes its contending set in both regimes, because the requirements remove
designs that carry the frontier (18 of 56 and 42 of 77 near-frontier designs), while removing the
infeasible designs leaves it unchanged (Appendix D.10)."
(2) "Pre-imposing the four requirements changes the contending set; removing the infeasible designs
does not (Appendix D.5)."
(3) No sentence in the paper; the appendix and the docs carry it.

Two notes for the stream that takes this up. A signed slack as a metric blocks the unconstrained
fit outright, a second reason (beside `spike-redundancy.md`) to carry the eclipse energy as one
positive metric. And the constrained fit extrapolates where the constraint cut (the large-wheel
candidates at rank 0.00): a design a requirement excludes is read against the unconstrained
surface; the constrained one answers only for the admitted region.
