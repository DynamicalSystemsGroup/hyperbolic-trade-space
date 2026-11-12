# WP39 stage 1, research spike: the case ends in a decision

Reads and computations only. Nothing in paper/, src/, derivation/, the data or the model changed. Everything below is
computed on the data of record (`examples/adcs/data/v2`, loaded by `examples/adcs/case.py`: `load_study`, `k_fits`,
`requirement_mask`, `nondominated_mask`; the fit of record, K = 1 tau 41.7 band 0.0240, K = 2 tau 113.2 own band 0.0088).
The paper's near-frontier band is the K = 1 band at every K (Section 9, gap G-9), so "within the band" below means
|log V| < 0.0240 unless the row says "own band". The scripts are in the session scratchpad; the full list of designs is
`candidates.json` beside this file. The primary regime (aggressive gains) is the case; the baseline regime (stock gains)
is given in one row each for comparison.

## Head

1. The model's stakeholder layer has two stakeholders, the sponsor (price) and the operator (performance in operation),
   five concerns and six measures of effectiveness in the sense the model defines (pointing error, unit cost, fleet cost,
   and the launch cost derived from total mass). It maps onto the K = 2 terms only in part: term 1 (peak slew power
   0.43, pointing error 0.21) is 80 % operator-held metrics, but term 2 (unit cost 0.25, available power 0.22) is 40 %
   sponsor-held and 58 % operator-held, because available power and momentum headroom are the operator's. The mapping
   "term 1 is the operator, term 2 is the sponsor" is a reading, not in the model.
2. Of 2,134 feasible designs, 548 pass all six requirements (D.17's joint pass). Of those, 28 lie within the band of
   both the K = 1 and the K = 2 frontier (10 within the K = 2 fit's own, narrower band); all 28 are assigned to term 1's
   cell. The baseline regime: 523 of 2,355 pass six, 19 within both bands.
3. Pointing error is, in this table, a tracker-grade choice: the 28 split into fine (4 designs, 0.0007 to 0.0008 degree),
   medium (21, 0.0028 to 0.0036) and coarse (3, 0.0084, just under the 0.008495 limit). Cost is a fleet-size choice:
   unit cost falls and fleet cost rises with the fleet (Spearman -0.81 and +0.99 against fleet size).
4. The rules do not all agree, and where they disagree the disagreement is the debate: the operator alone picks
   medium wheel, fine tracker, fleet of 6 (0.00074 degree, 343,961 USD, 2.06 M USD); the sponsor alone picks, by fleet cost,
   small wheel, medium tracker, fleet of 4 (0.00295 degree, 281,866 USD, 1.13 M USD) and, by unit cost, medium wheel,
   medium tracker, fleet of 25 (233,852 USD, 5.85 M USD); the minimax-regret design between them is medium wheel, fine
   tracker, fleet of 5 (0.00080 degree, 337,228 USD, 1.69 M USD). Five designs of the 28 are nondominated on (pointing
   error, fleet cost).
5. What the fit adds: the nondominated designs on the two measures alone, over all 548 six-pass designs, are 11 (pointing,
   fleet cost) and 12 (pointing, unit cost); only 1 and 0 of them lie within both bands. The others buy their cost or
   pointing by falling well inside the surface (log V down to -0.25 at K = 2 and -0.36 at K = 1), that is by
   giving up the other metrics.
6. A problem the model has: it prices the fleet size and does not value it. "Cheapest fleet cost" is the smallest fleet
   (2 satellites among the near-K = 2 designs). The sponsor's measure needs either unit cost, or a fleet size the sponsors
   state as a need (not in the model). See the question at the end.

## (a) The stakeholder layer of the model

File: `examples/adcs/model_v2/stakeholders.sysml` (WP27), applied after `cubesat.sysml` and `views.sysml`; "Nothing here is
read by the oracle, the coverage table, the view generator, the data or the contract" (lines 17 to 19). So the layer
documents who cares and traces concerns to requirements; the data and the fit never read it. The view that draws it is
`view stakeholders` in `views.sysml` lines 95 to 112 (no rendered image of it is committed under `model_v2/views/`; the
committed images are the assembly and behavioural views).

| item | what the model says | where |
|---|---|---|
| Sponsor | "Pays for the mission and answers for it. Cares about price ... Reads rolled-up measures, not the engineers' detail." | stakeholders.sysml:30-34, instance :39 |
| Operator | "Flies the cubesat. Cares about how it performs during its operational life: slews, settles and points as asked, power and energy hold up." | :35-38, instance :40 |
| Sponsor concern lowCost | launchBudget (:74), unitCost (:75), fleetCost (:76); limits 350,000 USD per satellite, 6,000,000 USD per fleet (covered cost), sponsor's full fleet budget 8,000,000 USD, 2,000,000 USD allowance for what is not scoped | :56-77 |
| Sponsor concern longLife | depthOfDischarge (:84); effective life an illustrative roll-up | :78-85 |
| Operator concern pointingAndSlewing | pointingError (:91), settled (:92), controlEffort (:93), momentum (:94) | :86-95 |
| Operator concern powerAndEnergy | power (:103, the available power must be positive), powerMargin, energyBalance, peakSlewPower (:106), batteryPeakPower, eclipse depth of discharge (:108, shared with the sponsor's long life) | :96-109 |
| Verdict per named configuration | baseline fails pointing error (0.0155 against 0.0085 degree) and the unit cost; agile fails launch budget, control effort, peak slew power; compact fails pointing error (:111-222) | :111-222 |
| Roll-ups (illustrative, read by no output) | CostToBuild, EffectiveLife | :227-256 |
| Evidence | two verification cases pointing at ledger entry v2-primary@12 | :261-315 |

Measures of effectiveness (MoE) are defined in `cubesat.sysml` lines 67-70 ("a measure a stakeholder states without
knowing the design"). The three traded MoEs: pointing error (`calc def PointingError`, :688), unit cost (:540) and fleet
cost (:532); the launch cost (:367) is the MoE on total mass and is derived, not traded. The ten other traded metrics are
measures of performance. Budgets: `part budgets` at `cubesat.sysml` :840-874 (pointing error 0.008495 degree, control
effort 0.05922, peak slew power 2.6 W, launch budget 105,770 USD, unit cost limit 350,000 USD, fleet cost limit 6,000,000
USD).

Who holds what, by concern (the model's trace, `satisfy`/`concern` statements):

| stakeholder | holds (traded metrics) | MoE among them |
|---|---|---|
| sponsor | total mass (through the launch budget), unit cost, fleet cost; depth of discharge (shared) | unit cost, fleet cost |
| operator | settling time, pointing error, control effort, momentum headroom, power margin, energy balance, peak slew power, available power, battery peak power ratio; depth of discharge (shared) | pointing error |

Mapping onto the K = 2 terms (exponents at the fit temperature, normalised to sum 1, K = 2 fit of record):

| term (share of near-frontier designs) | leading exponents | sponsor-held share | operator-held share |
|---|---|---|---|
| 1 (0.74) | peak slew power 0.426, pointing error 0.206, unit cost 0.122, available power 0.083, fleet cost 0.070 | 0.19 | 0.80 |
| 2 (0.26) | unit cost 0.250, available power 0.216, fleet cost 0.142, momentum headroom 0.132, pointing error 0.119, settling time 0.113 | 0.40 | 0.58 |
| (K = 1, one term) | unit cost 0.257, available power 0.197, pointing error 0.156, fleet cost 0.151 | 0.43 | 0.53 |

(The remainder is depth of discharge, held by both.) Term 1 reads as the operator's term. Term 2 does not read as the
sponsor's: it is the term where cost and available power trade, and the operator holds the larger share of it. If the
narration says "term 1 is the operator's concern, term 2 the sponsor's" it overstates; "term 1 is led by the operator's
metrics, term 2 puts the sponsor's cost against the operator's available power" is what the exponents carry.

## (b) The designs that are feasible, pass all six requirements and lie within the band

Funnel, counts per regime (a design is counted once; "within a band" is |log V| < the K = 1 band, 0.0240 primary, 0.0219
baseline, for the fit named):

| set | primary | baseline |
|---|---|---|
| feasible designs | 2,134 | 2,355 |
| pass the four performance thresholds | 814 | 882 |
| pass all six requirements (D.17 joint pass) | 548 | 523 |
| six-pass and within the K = 1 band | 60 | 52 |
| six-pass and within the band at K = 2 | 210 | 135 |
| **six-pass and within both (the working set W)** | **28** | **19** |
| six-pass and within the K = 1 band and the K = 2 fit's own band (0.0088 / 0.0097) | 10 | 7 |
| six-pass, within both, on or beyond the surface (log V at least -band at both) | 86 | 60 |
| W by cell at K = 2 | term 1: 28 | term 1: 17, term 2: 2 |
| six-pass and within the K = 2 band, by cell | term 1: 186, term 2: 24 | term 1: 127, term 2: 8 |

W by tracker grade (primary): fine 4, medium 21, coarse 3; by wheel class: small 19, medium 9. The six-pass designs in
the term 2 cell (24 near the K = 2 surface) are all medium wheel, medium tracker, panel span 0.42 to 0.77 m.

The 28 designs of W, primary regime, ordered by fleet cost (`nd` marks nondominated on pointing error and fleet cost
(f) or on pointing error and unit cost (u); position is along the first principal direction of the near-frontier chart,
whose better end is lower unit cost, lower total mass and lower peak slew power; level is log V at K = 2, log V at K = 1
in the last column; all 28 are in term 1's cell). Panel in m, battery in Wh.

| id | wheel / tracker | panel | batt | Kp | Kd | fleet | pointing (deg) | unit cost (USD) | fleet cost (USD) | position | log V2 | log V1 | nd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 999 | small / medium | 0.37 | 52 | 0.46 | 1.07 | 4 | 0.00295 | 281,866 | 1,127,465 | +2.48 | +0.0164 | -0.0233 | f |
| 190 | small / medium | 0.51 | 112 | 0.46 | 0.79 | 5 | 0.00295 | 303,020 | 1,515,098 | +0.85 | +0.0179 | +0.0082 | f |
| 766 | medium / medium | 0.32 | 42 | 0.94 | 0.93 | 6 | 0.00282 | 266,193 | 1,597,160 | +2.17 | -0.0173 | +0.0209 | f |
| 1858 | medium / fine | 0.36 | 124 | 0.80 | 1.21 | 5 | 0.00080 | 337,228 | 1,686,142 | +0.31 | -0.0119 | -0.0099 | f |
| 1560 | small / medium | 0.56 | 112 | 0.23 | 0.55 | 6 | 0.00341 | 301,892 | 1,811,355 | +0.81 | -0.0110 | -0.0062 |  |
| 2429 | small / medium | 0.68 | 55 | 0.28 | 1.19 | 6 | 0.00322 | 316,493 | 1,898,956 | +0.63 | -0.0014 | -0.0070 |  |
| 2950 | medium / fine | 0.50 | 43 | 0.94 | 0.75 | 6 | 0.00074 | 343,961 | 2,063,765 | -0.67 | +0.0096 | +0.0198 | f u |
| 1112 | small / medium | 0.59 | 67 | 0.35 | 0.83 | 7 | 0.00307 | 296,608 | 2,076,256 | +0.89 | +0.0093 | -0.0008 |  |
| 740 | small / medium | 0.41 | 199 | 0.25 | 0.81 | 9 | 0.00332 | 270,255 | 2,432,293 | +1.76 | -0.0010 | -0.0112 |  |
| 186 | small / medium | 0.65 | 100 | 0.21 | 1.08 | 8 | 0.00351 | 304,375 | 2,434,999 | +0.71 | -0.0108 | +0.0030 |  |
| 34 | small / medium | 0.51 | 37 | 0.22 | 0.55 | 9 | 0.00345 | 270,645 | 2,435,802 | +1.79 | -0.0076 | -0.0181 |  |
| 2013 | medium / coarse | 0.47 | 99 | 0.39 | 1.07 | 9 | 0.00842 | 272,078 | 2,448,699 | +1.64 | -0.0178 | -0.0055 |  |
| 893 | small / medium | 0.60 | 104 | 0.23 | 1.05 | 10 | 0.00343 | 288,209 | 2,882,089 | +1.02 | +0.0014 | +0.0185 |  |
| 68 | small / medium | 0.50 | 33 | 0.20 | 0.58 | 12 | 0.00359 | 258,949 | 3,107,384 | +2.01 | -0.0038 | +0.0003 |  |
| 1282 | small / medium | 0.54 | 30 | 0.30 | 1.17 | 12 | 0.00318 | 265,736 | 3,188,833 | +1.87 | +0.0168 | +0.0011 |  |
| 1001 | small / medium | 0.49 | 88 | 0.32 | 0.54 | 15 | 0.00313 | 256,262 | 3,843,933 | +1.60 | +0.0065 | -0.0081 |  |
| 530 | small / medium | 0.44 | 75 | 0.30 | 1.13 | 18 | 0.00318 | 242,813 | 4,370,631 | +2.46 | +0.0206 | +0.0140 |  |
| 1191 | medium / fine | 0.43 | 90 | 0.87 | 0.63 | 15 | 0.00076 | 301,895 | 4,528,428 | -0.12 | -0.0098 | -0.0111 | u |
| 2252 | medium / coarse | 0.48 | 125 | 0.32 | 1.15 | 18 | 0.00846 | 255,321 | 4,595,786 | +1.79 | -0.0191 | -0.0117 |  |
| 2826 | medium / fine | 0.42 | 66 | 0.83 | 1.19 | 16 | 0.00078 | 295,736 | 4,731,771 | +0.41 | +0.0013 | +0.0099 | u |
| 864 | small / medium | 0.44 | 192 | 0.28 | 1.44 | 19 | 0.00323 | 251,463 | 4,777,789 | +2.01 | +0.0076 | -0.0084 |  |
| 47 | small / medium | 0.65 | 85 | 0.24 | 0.91 | 18 | 0.00337 | 272,743 | 4,909,380 | +0.98 | -0.0059 | -0.0005 |  |
| 613 | small / medium | 0.54 | 119 | 0.41 | 0.79 | 19 | 0.00299 | 259,863 | 4,937,399 | +1.18 | +0.0080 | -0.0131 |  |
| 2167 | small / medium | 0.49 | 36 | 0.35 | 1.49 | 22 | 0.00306 | 240,900 | 5,299,788 | +2.43 | +0.0239 | -0.0008 |  |
| 390 | small / medium | 0.49 | 134 | 0.54 | 1.21 | 22 | 0.00291 | 249,339 | 5,485,455 | +1.58 | +0.0180 | -0.0067 |  |
| 2100 | medium / coarse | 0.47 | 76 | 0.34 | 1.42 | 23 | 0.00844 | 242,973 | 5,588,371 | +2.31 | -0.0137 | -0.0119 |  |
| 2847 | small / medium | 0.52 | 131 | 0.32 | 1.43 | 23 | 0.00312 | 252,780 | 5,813,931 | +1.64 | +0.0185 | +0.0157 |  |
| 2356 | medium / medium | 0.39 | 33 | 1.27 | 1.46 | 25 | 0.00280 | 233,852 | 5,846,300 | +2.06 | -0.0221 | +0.0044 | u |

(A design with positive log V lies on or beyond the fitted surface; all are inside the band.) The full list, the
six-pass designs within either band (242 primary, 168 baseline) with their flags, is `work-packages/WP39-rounds/spike/candidates.json`.

For contrast, the baseline configuration: pointing error 0.0155 degree, unit cost 461,360 USD (fleet of 1), which fails
the pointing error and the unit cost limit (`CUBESAT.baseline_configuration`).

## (c) The decision rules, computed (working set W, primary regime)

Executives' measures: the operator's is pointing error; the sponsor's are unit cost and fleet cost (the model's three MoEs).
All 28 pass the pointing requirement already (it is one of the six), so "the cheapest design meeting the pointing
requirement" is the cheapest design of W.

| rule | design | configuration (wheel, tracker, panel m, battery Wh, Kp, Kd, fleet) | pointing (deg) | unit cost | fleet cost | log V2 / log V1 |
|---|---|---|---|---|---|---|
| R1a cheapest fleet cost meeting pointing | 999 | small, medium, 0.37, 52, 0.46, 1.07, 4 | 0.00295 | 281,866 | 1,127,465 | +0.016 / -0.023 |
| R1b cheapest unit cost meeting pointing | 2356 | medium, medium, 0.39, 33, 1.27, 1.46, 25 | 0.00280 | 233,852 | 5,846,300 | -0.022 / +0.004 |
| R2 balanced between the terms (smallest gap of the two term levels) | 766 | medium, medium, 0.32, 42, 0.94, 0.93, 6 | 0.00282 | 266,193 | 1,597,160 | -0.017 / +0.021 |
| R3a operator alone (smallest pointing error) | 2950 | medium, fine, 0.50, 43, 0.94, 0.75, 6 | 0.00074 | 343,961 | 2,063,765 | +0.010 / +0.020 |
| R3b sponsor alone (smallest fleet cost / smallest unit cost) | 999 / 2356 | as R1a / R1b | | | | |
| R3c between them, minimax regret on (pointing, fleet cost) | 1858 | medium, fine, 0.36, 124, 0.80, 1.21, 5 | 0.00080 | 337,228 | 1,686,142 | -0.012 / -0.010 |
| R3c' between them, minimax regret on (pointing, unit cost) | 2356 | as R1b | | | | |
| R4 nondominated on (pointing, fleet cost) | 190, 766, 999, 1858, 2950 | 5 designs | | | | |
| R4' nondominated on (pointing, unit cost) | 1191, 2356, 2826, 2950 | 4 designs | | | | |
| R4'' nondominated on (pointing, unit cost, fleet cost) | 15 designs | | | | | |

(Minimax regret: each measure scaled 0 to 1 over W, the design whose larger scaled shortfall is smallest. "Balanced":
the design where term 1's and term 2's levels are closest, |s1 - s2| = 0.032; the design at the same gap over the wider
set of 210 near the K = 2 surface is 1230, medium wheel, medium tracker, fleet of 5, 1,659,912 USD, gap 0.0015, but it lies
at log V1 +0.093, outside the K = 1 band.)

Pointing asks, the price of a tighter pointing requirement in USD on W (cheapest design that meets an ask; the pointing
error is a step in the tracker grade, so the table has two plateaus):

| pointing ask (degree) | designs of W meeting it | cheapest fleet cost | cheapest unit cost |
|---|---|---|---|
| 0.008495 (the requirement) | 28 | 999: 1,127,465 | 2356: 233,852 |
| 0.005 or 0.003 | 25, then 10 | 999: 1,127,465 | 2356: 233,852 |
| 0.002 or 0.001 | 4 | 1858: 1,686,142 (fleet 5) | 2826: 295,736 (fleet 16) |

So the one step an operator can ask for, about a factor of 3.7 in pointing error (0.0030 to 0.0008 degree), is a fine
tracker, and in this table it costs 0.56 M USD of fleet cost at the cheapest end (1.13 M to 1.69 M USD) or 62,000 USD of
unit cost (233,852 to 295,736 USD, fleet 25 to 16). Whether the model's tracker price is right is the engineers' to say
(Appendix C.8: tracker price from a listed unit, "illustrative").

Do the rules agree? On the fine tracker, yes: R3a and R3c both choose it, and 2950 and 1858 are the two nondominated fine
designs on (pointing, fleet cost); they differ by 0.0001 degree, 0.38 M USD of fleet cost and 6,700 USD a satellite, and
by log V (2950 beyond the K = 1 surface by 0.020, 1858 inside it by 0.010). Across the tracker grade, no: the sponsor
alone and the operator alone disagree by the tracker grade, which is the decision. R2 (balanced between the terms) picks a
medium tracker, R4's five designs include both tracker grades. The rules agree on a family and disagree inside it; none
selects one design without a statement of how much pointing is worth, which is the executives' call. Baseline regime:
operator 1247 (medium wheel, fine tracker, fleet 13), sponsor 2195 (fleet cost) or 2122 (unit cost), between 979;
nondominated on (pointing, fleet cost) 287, 979, 1247, 2195, 2924. The same shape: the tracker grade is the decision.

What the fit adds, computed: over all 548 six-pass designs the nondominated designs on (pointing, fleet cost) are 11,
and on (pointing, unit cost) 12 (a two-measure view needs no fit). Only 1 and 0 of them lie within both bands; their log V
runs from -0.19 to +0.02 at K = 2 and from -0.22 to +0.03 at K = 1 on the first set, and to -0.36 on the second. The
designs that look best on the two executives' measures alone are mostly well inside the surface: they buy cost or pointing
by giving up others of the thirteen metrics. The band is what keeps them out, and "feasible, on or near the frontier" is
therefore a real filter, not a decoration.

## (d) Fit to the body's budget

Counted today (`tests/test_paper.py`, words_by_section): Section 9 "Case analysis" 1,557 words against a ceiling of 1,603
(slack 46); Section 8 "Case construction" 1,328 of 1,330; the discussion 752 of 755; the whole paper 10,193 against a total
ceiling of 12,073 (the section ceilings bind first). Tables are not counted (the ledger counts a table's title only); a
small table adds almost no counted words. A closing subsection of one paragraph (about 130 to 150 words) and one small
table (six rows) needs a [[raise]] row for Section 9 of about the paragraph's words, less any cuts.

### Draft options for the paragraph (Section 9, last part, "A decision"), each number traced

The table (one option, all drafts): six rows, columns the rule, the configuration (wheel, tracker, panel, battery, gains,
fleet size), pointing error, unit cost, fleet cost, level log V; rows: baseline configuration; sponsor alone (999); operator
alone (2950); between them (1858); balanced between the terms (766); cheapest unit cost (2356).

**Draft 1 (the reduction in order).**
"**A decision.** Two stakeholders hold the three measures of effectiveness: the operator the pointing error, the sponsor
the unit cost and the fleet cost. Of the 2,134 feasible designs 548 pass all six requirements, and 28 of these lie within
the near-frontier band of the K = 1 and the K = 2 fit. They differ in two ways: the tracker grade sets the pointing error
(0.0008 degree for the fine grade, 0.003 for the medium) and the fleet size sets the cost. The operator alone would take a
medium wheel and a fine tracker with a fleet of 6 (0.0007 degree, 2.06 M USD); the sponsor alone a small wheel and a
medium tracker with a fleet of 4 (0.003 degree, 1.13 M USD); a medium wheel and a fine tracker with a fleet of 5 gives up
the least of either (0.0008 degree, 1.69 M USD, 337,000 USD a satellite). The fit does not choose among them. It shows
that the choice is a tracker grade and a fleet size, that each of the 28 is feasible, near the frontier and inside both
budgets, and what the fine tracker costs: 0.56 M USD of fleet cost for a pointing error a factor 3.7 smaller."
(Numbers: 2,134, 548, 28; 0.0008/0.0030 (W by tracker); 2950 and 999 and 1858 rows; 0.56 M = 1,686,142 - 1,127,465; 3.7 =
0.0030/0.0008 from the pointing asks. "Inside both budgets": 6 M and 350,000 USD.)

**Draft 2 (the debate, not the picks).**
"**What the executives decide.** Suppose the operator cares about the pointing error and the sponsor about the unit cost
and the fleet cost, and neither about the subsystems. The requirements and the frontier cut 2,134 feasible designs to 28
that pass all six requirements and lie within the band of both fits. Among those, one question remains and it is theirs:
whether a fine star tracker, which brings the pointing error from about 0.003 to 0.0008 degree, is worth about 0.56 M USD
of a 6 M USD fleet budget. If it is, five designs trade the two measures without one beating another, and the fleet of 5
medium-wheel, fine-tracker satellites at 1.69 M USD, 337,000 USD each, is the one that regrets least; if it is not, the
fleet of 4 small-wheel, medium-tracker satellites at 1.13 M USD is cheapest. The method names the question and prices it;
it does not answer it, and nothing in the 548 designs outside the band would have made it easier, since the designs that look
best on these two measures alone mostly lie well inside the frontier."
(Numbers as Draft 1 plus: 11 nondominated over all 548, 1 inside both bands; "about 0.003": medium 0.0028 to 0.0036.)

**Draft 3 (shortest, the sentence the key wants).**
"**The call.** The fit does not decide; it narrows. Of 548 designs that pass all six requirements 28 sit on or near the
frontier of both fits, and on them the two executives' measures separate into one choice, a fine or a medium tracker
(0.0008 or 0.003 degree), priced at 0.56 M USD of the fleet cost, and one range, a fleet of 4 to 25. Any of the five
designs that neither beats the other on pointing error and fleet cost is a defensible call; the paper shows which are
feasible and near the frontier and leaves the call to them."
(Numbers: 548, 28, 0.56 M, fleet 4 to 25 from W, 5 nondominated.)

Each draft says explicitly what the method does not decide. Draft 3 carries the least; Draft 2 the most of the executives'
side. None uses a design id or a log V in the paragraph (the table carries them). The register note: "defensible" is the
supervisor's word; the glossary term for the decision problem is to be checked at the build.

### What gives way, by marginal value to a decision maker (Section 9 unless stated)

| rank | text (cells in `paper/paper.ipynb`) | words | serves | ledger and cascade if cut |
|---|---|---|---|---|
| 1 | "Three metrics at a time" paragraph, the ternary figure (Figure 9) with caption and its shows/does-not-show lines: cells 87-89 | 151 | the reader who wants to see two terms in a triangle; the executive gets nothing from it | [[cut]] row -151 (and the figure's caption rows are in the ledger already); cascade: `fig-ternary-pair` and its two tests in `tests/test_paper.py` (caption test at the ternary figure; the lines test), `tests/test_paper_static_figures.py`, `paper/figures/ternary_pair.py`, claims-register rows near 5451, 5463, 5633, 5645 (two of them are the Examples page's and stay), `docs/examples.md` keeps its own copy; the figure number shifts for later figures |
| 2 | "Candidates" paragraph and its generated sentence: cells 92 and 94 | 48 | the hand-named candidates all miss the thresholds (P8 F4); the new shortlist replaces them as the case's concrete designs | [[cut]] -48; D.7 keeps the table and the candidate sentences; claims rows backed by `candidates_sentence` stay, as the sentence still exists in the generator unless removed with it |
| 3 | "Two regimes" and its generated sentence: cells 90, 91 | 134 | the method reader (problem against gains); the decision maker reads one case | [[cut]] -134 and more cascade: the regime figure and tests are not in Section 9 cells but `regime_sentence` has claims rows, a perturbation entry in `paper_perturb.py`, and Section 1's pointer; larger than rank 1 |
| 4 | "Propose, predict, check" and its generated sentence: cells 95, 98 | 169 | the method reader judging the regressor | the cascade is large (the proposals' claims, the discussion's sentence on them in Section 10, D.10); would also change the discussion's pointer; not recommended as a first cut |
| 5 | "Two terms" K-choice sentence and the temperatures sentence: cells 76, 78 | 165 | the practitioner choosing K; the decision maker accepts K = 2 as given | shortening, not cutting: both carry the case's choice of K and the band convention that W uses, so the new subsection depends on them |
| 6 | Shows/does-not-show lines of Figure 5 (plane), Figure 6 (chart), Figure 8 (association): cells 75, 80, 83 | 180 | readers of the figures; required by the figure-review rule | these were added by decision (WP19); cutting them would need a ruling on that rule, not a spike's choice |

The supervisor said the existing text gives way first where it serves the decision maker less: rank 1 serves the decision
maker least and is the cleanest cut (151 words against the paragraph's 130 to 150, so net neutral on the ledger). Rank 2 is a
replacement, not a loss. Ranks 3 and 4 serve the method reader, who has the appendices. Section 8's body paragraph on the
six requirements (cell 59) is the other candidate for the decision-maker reader and stays: it is where the limits are
stated.

## (e) Acceptance criteria from the final reads (quoted)

From `work-packages/WP30-rounds/persona-final/P8-final.md` (new-space executive), findings F2 and F3 and the verdict:

- F2: "No decision is shown that the method changes." Says: the paper "stops short of selecting a design, which falls to
  experts"; section 9: "The finding: the terms' sets differ." "Business: the case has no sentence of the form 'with this
  reading we would relax X or buy Y'. ... Severity: changes the decision (I cannot tell what I would do differently on
  Monday)."
- F3: "Requirement prices are in bands and log V, not in program currency; only the limits are in USD." "Business: the unit
  cost limit is by far the most expensive requirement to meet (5.31 bands against 1.50 and 0.24) and that is the finding I
  need, but it is not converted to dollars per satellite or satellites per fleet. ... Severity: changes the decision (cannot
  negotiate a requirement in bands)."
- Section 5: "Would the method change a decision I make? Not from the paper as written; it would change how I prepare one.
  The mechanism I could use is the requirements reading ..., provided its prices come in dollars."
- Section 7: "Whether the method changes a decision: not shown (F2, F3, F6)." And on the first screens: "The abstract and the
  first screens give an executive no number and no money."

From `P7-final.md` (systems engineer, flight hardware), the trust question (section 3): "Would I trust the trade reading on
my own program: No, and the paper does not ask me to. I would trust the form of the reading: a contending set with
elasticities, read from a table I can regenerate, with a cost axis that is not a constant times mass. I would not use any
ranking from this model; the three things that decide a flight bus here are pointing budget, momentum management and
margins, and each is missing or nominal." And section 4: "The body should carry one sentence naming what is nominal and
where C.8 is." And the verdict: "the body does not carry the toy statements next to the findings that rest on them."

Criteria for the section that follow, each testable by the persona reads:

1. A sentence of the form the executive asks for: what we would relax or buy, in program currency (here: a fine tracker for
   0.56 M USD of fleet cost; the fleet size range). Currency, not bands or log V (F2, F3).
2. The narration is readable without the subsystem detail: the executives' measures are named in their words (pointing
   error, unit cost, fleet cost), the subsystem choices appear as configuration (wheel, tracker, fleet) and the exponents
   and terms stay in the appendix (P8 section 1 "Lost").
3. It does not ask to be trusted as a ranking: it says the model is a demonstration with nominal values and says where
   (a clause pointing at C.8, next to the design table, as P7 asks), and that it prices options and does not choose
   (P7 section 3; the supervisor's own statement).
4. It states what the method does not tell: schedule and risk, what to buy beyond the modelled parts, the value of fleet size
   (P8 section 5, "What the method does not tell me").
5. The test the supervisor set (WP39-decisions.md): P8 and P7 cold-read the finished section, whether they could follow the
   reduction to the call and whether it made the decision easier or harder, with the sentence that did it quoted.
6. Machine side: every number in the subsection is a claims-register row backed by a generated value (the generator
   would live in `paper/generate_findings.py` or `case.py`; the table is generated from the same function).

## Problem-level questions and plain options

Q1. The model prices a fleet and does not value one. The sponsor's "fleet cost" measure favours the smallest fleet (2 or 4
satellites); the unit cost favours the largest (25). Which sponsor measure does the narration use?
- (a) Unit cost with the fleet cost as the budget: the sponsor's pick is the largest fleet the budget allows (2356, fleet 25,
  5.85 M of the 6 M budget).
- (b) Fleet cost, with a fleet size the sponsors state as a need (for example at least 8 satellites, giving 740 at 2.43 M).
- (c) Both measures shown, the fleet size named as the third thing the model does not value.

Q2. Which working set is the shortlist?
- (a) The 28 within the band of both fits (the paper's band at every K).
- (b) The 10 within the K = 1 band and the K = 2 fit's own narrower band (picks: cheapest fleet 2429, best pointing 2826,
  between 1001).
- (c) The 86 on or beyond the surface within the band (adds designs above V = 1, picks: best pointing 1247).

Q3. Which mapping of terms to executives, if any, does the narration state?
- (a) None: the executives' measures are read from the model's stakeholder layer and the terms stay in the K = 2 paragraph.
- (b) "Term 1 is led by the operator's metrics; term 2 puts the sponsor's cost against the operator's available power"
  (what the exponents carry).
- (c) A stakeholder-to-term table in Appendix D with the shares above.

Q4. Which cut pays for the paragraph and table?
- (a) The ternary pair paragraph and Figure 9 (151 words, rank 1).
- (b) The Candidates paragraph (48 words) plus a shortening of the K-choice sentences.
- (c) A raise of Section 9's ceiling with no cut.

## Checks

Whole-repo `uv run ruff check .` and `uv run ruff format --check .`, `uv lock --check` and
`tests/test_text_encoding.py` are run before the push; this readout and `candidates.json` are the only files added.
