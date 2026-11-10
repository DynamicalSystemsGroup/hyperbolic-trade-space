# Spike B: the fitted model alongside threshold requirements (WP23)

Question (supervisor, `WP23-decisions.md`, "Requirements and the trade study"): how does the fitted
model help a trade study run alongside a set of threshold requirements, including when the set is
infeasible, and might it justify a request to relax a requirement? Worked on the case with the four
chosen thresholds (peak slew power 2.6 W, pointing error 0.008495 degree, control effort
0.05922 N.m.s, launch budget 90,643 USD = 15.107 kg at 6,000 USD/kg), the data of record
(`examples/adcs/data/v2/`, primary 706 and baseline 780 feasible designs), and the fits of record
(`case.load_study`, `case.k_fits` at K = 1 and K = 3; the K = 1 band 1/tau is 0.02625 primary,
0.02189 baseline; 56 and 77 near-frontier designs). Read-only; scripts and logs in the session
scratchpad `spike-B/`.

**Answer in one paragraph.** Yes, with a bounded form. The fit prices a requirement at the frontier:
for a requirement on metric i, the exponents give the elasticity of every contending metric k along
the fitted surface (−w_i/w_k in the conditioned metrics; in attribute percents, scaled by the
conditioning), and the band says which near-frontier designs the requirement excludes. Put
together they give a request its three numbers: what meeting R_i costs at the frontier in the other
metrics, how many near-frontier designs relaxing R_i from a to b admits, and by how much the best
attainable value of a contending metric improves among them. On the case the argument has teeth in
the baseline regime (pointing error excludes 42 of 77 near-frontier designs; relaxing it from
0.008495 to 0.011814 degree admits 24 more and the best attainable control effort improves by 41 %)
and is weak in the primary regime (control effort excludes 18 of 56, but the K = 1 surface does not
price control effort, 16 of the 18 sit in the K = 3 term where its exponent is zero, and relaxing it
moves the best attainable energy balance by 8 % and nothing else). The method does not say a
requirement is wrong: it says what the requirement costs on this table's fitted frontier, under
this conditioning, and whether the frontier even trades the metric; the requirement's source (the
mission) is outside the model, and a requirement slack on the frontier can still be the one that
removes a whole wheel class inside it.

## 1. The four thresholds in the chart

A threshold a_i ≤ L is a level of one log-metric, u_i ≥ (−log L − μ_i)/s_i (all four are
smaller-is-better); in the chart it is a half-space crossing the band. The table reads each one on
the K = 1 fit of record; the pass fractions agree with the gate's (`WP23-review.md`), except pointing
error in the primary regime at 671/706 (one design within 1e-6 of the limit).

| Requirement | Pass, feasible (primary / baseline) | Band range of the attribute (primary; baseline) | Excludes, of the near-frontier band (primary; baseline) | Excludes, of the designs beyond V = 1 (65; 81) | K = 1 exponent (primary; baseline) |
|---|---|---|---|---|---|
| peak slew power ≤ 2.6 W | 62.2 % / 67.3 % | 1.30 to 2.60 W; 1.30 to 7.4 W | 0 of 56; 2 of 77 (both large wheels) | 0; 1 | 0; 0 |
| pointing error ≤ 0.008495 degree | 95.0 % / 63.7 % | 0.0006 to 0.0086; 0.0014 to 0.0173 | 1 of 56 (small/coarse); **42 of 77** (20 small/coarse, 7 small/medium, 10 medium, 3 large) | 0; 35 | 0.164; 0.039 |
| control effort ≤ 0.05922 N.m.s | 58.9 % / 90.0 % | 0.011 to 0.160; 0.002 to 0.086 | **18 of 56** (medium wheel: 9 fine, 9 medium tracker); 1 of 77 | 15; 1 | 0; 0.432 |
| total mass ≤ 15.107 kg | 94.9 % / 95.6 % | 12.31 to 14.70 kg; 12.02 to 15.91 kg | 0 of 56; 1 of 77 | 0; 1 | 0.358; 0 |
| **all four jointly** | 40.8 % / 38.7 % | | **37 of 56 pass (66 %); 34 of 77 pass (44 %)** | 50 of 65; 45 of 81 | |

The set is not jointly infeasible on the frontier in either regime: two thirds of the primary
band and under half of the baseline band pass all four. No primary near-frontier design fails more
than one requirement; in the baseline regime one fails two and one (the large/fine design 262)
fails three. At the K = 3 fit's own band (0.00883) the shares are 16 of 29 and 30 of 51, pointing
error again the baseline regime's cut (21 of 51).

Two requirements are slack on the frontier in both regimes: total mass (the band's heaviest design
is 14.70 kg primary, one baseline design at 15.91 kg) and peak slew power in the primary regime,
whose band holds no large wheel (the 267 feasible large-wheel designs it excludes all sit at
log V ≤ −0.040, one and a half band widths inside). The chosen 2.6 W is exactly the primary band's
largest value. Each regime has one requirement that cuts its band: control effort in the primary
regime (a third of the band), pointing error in the baseline regime (over half).

## 2. The cost of a binding requirement at the frontier

Along the K = 1 surface Σ w_j u_j is constant, so tightening metric i by Δu_i and paying with metric
k alone costs Δu_k = −(w_i/w_k) Δu_i; in attribute percents the elasticity is
−(w_i o_i/s_i)/(w_k o_k/s_k) with the conditioning's orientations and log scales. Meeting the
requirement with nothing else moved would raise log V by w_i Δu_i: the frontier's **price** of the
requirement, read against the band width. The table gives the median excluded near-frontier design
of each binding requirement, the K = 1 reading, and the K = 3 term in which the metric contends (its
largest exponent); costs are "paid by one metric at a time" and listed for co-contenders with
w_k ≥ 0.05.

| Regime, requirement | Median excluded design, tightening needed | K = 1: w_i; price in log V (band) | K = 1 cost, paid by one metric | K = 3 term where it contends (w_i); the excluded designs' cells | K = 3 cost in that term |
|---|---|---|---|---|---|
| primary, control effort | medium/medium, Kp 0.53, 0.083 N.m.s: 39 % too high | 0; **0 (free: the surface does not trade control effort)** | none priced | term 2 (0.397); 16 of 18 excluded sit in term 3, where w = 0 | settling time +49 % (elasticity −1.20); energy balance −53 % (+2.29) |
| primary, pointing error | small/coarse, 0.00858 degree: 1 % too high | 0.164; 0.0019 (0.07 of the band) | settling time +1.1 % (−1.16); depth of discharge +0.7 % (−0.69); energy balance −0.8 % (+0.86); mass +0.03 % | term 3 (0.227); in term 3 | settling time +4.1 % (−4.10); peak slew power +0.3 % (−0.28); mass +0.3 % |
| baseline, pointing error | small/coarse, Kp 0.067, 0.0108 degree: 26 % too high | 0.039; **0.012 (0.56 of the band)** | settling time +3.6 % (−0.154); control effort +2.6 % (−0.114); power margin −3.6 % (+0.159) | term 2 (0.190); excluded span all three terms (14 / 8 / 20) | total mass +2.4 % (−0.10); peak slew power +8.7 % (−0.36); power margin −32 % (+1.66); settling time +110 % (−3.26) |
| baseline, control effort | large/fine 262, 0.0856 N.m.s: 45 % too high | 0.432; **0.173 (7.9 bands)** | settling time +65 % (−1.36); power margin −40 % (+1.40) | term 1 (0.507) | settling time +66 % (−1.38); energy balance −90 % (+6.31) |
| baseline, peak slew power; total mass | the same design 262 (7.4 W; 15.91 kg) | 0; 0 (free at K = 1) | none priced | term 2 (0.428; 0.161) | mass +22 % for the power requirement; peak slew power +20 % for the mass requirement |

Reading. The price separates two situations the pass fraction cannot. The baseline regime's
control-effort requirement excludes one near-frontier design at a price of eight band widths: that
design (the large wheel with the fine tracker, the band's fastest slew) cannot meet it along the
frontier without giving up two thirds of its settling time. The same regime's pointing-error
requirement excludes 42 designs at half a band width each: cheap per design, because the surface
is nearly flat in pointing error (w 0.039), so these designs have near-frontier neighbours that
meet it. The primary regime's control-effort requirement has no price at K = 1 and, for 16 of its
18 excluded designs, none at K = 3: the frontier these designs sit on is not set by control effort,
which the ladder below confirms. Attribute-percent elasticities depend on the conditioning's log
scales (total mass has s = 0.066, so its attribute elasticities are small while its conditioned
ones are not); the report's own elasticity is the conditioned one. All of it is a feature of the
fitted model on this table, not a causal exchange.

## 3. The case for relaxing a requirement

The form the method supports, with the three numbers it supplies:

> Meeting R_i (a_i ≤ a) at the fitted frontier costs x % of metric j per the fitted elasticity, for
> a design that misses it by the median margin (price p in log V, against a band of 1/tau).
> Relaxing R_i from a to b admits n more near-frontier designs that meet the other requirements, and
> the best attainable j among the admitted designs improves by y %. The relaxed designs are
> [which cells and configurations].

Instance, the requirement that excludes the most near-frontier designs (baseline regime, pointing
error; the ladder's candidates are the gate's):

| Pointing error limit b (degree) | Pass, feasible | Near-frontier admitted, with the other three (of 77) | Best control effort among them (N.m.s) | Best total mass (kg) | Best settling time, energy balance, depth of discharge |
|---|---|---|---|---|---|
| 0.008495 (chosen) | 63.7 % | 34 | 0.00377 | 12.30 | 19.7 s, 43.8 Wh, 0.0455 |
| 0.011814 (admits 90 %) | 90.0 % | 58 (+24) | 0.00223 (−41 %) | 12.21 (−0.7 %) | unchanged; 0.0445 |
| 0.013561 (admits 95 %) | 95.0 % | 65 | 0.00223 | 12.02 (−2.2 %) | unchanged |
| 0.015535 (the baseline configuration's own) | 99.0 % | 73 | 0.00198 (−47 %) | 12.02 | unchanged |

Written out: meeting the pointing-error requirement at the baseline regime's frontier costs 2.6 %
of control effort or 3.6 % of settling time per the K = 1 elasticities for the median excluded
design (price 0.012 in log V, half the band); relaxing it from 0.008495 to 0.011814 degree admits
24 more near-frontier designs that meet the other three requirements, and the best attainable
control effort among them improves from 0.00377 to 0.00223 N.m.s (41 %); the admitted designs are
the coarse-tracker, low-gain corner (small wheel, Kp near its floor). The two numbers answer
different questions: the elasticity is the local exchange along the surface at one design, the
ladder the change in the admitted set's extreme.

The weak instance (primary regime, control effort, 18 of 56): relaxing 0.05922 to 0.0771 N.m.s
admits 6 (37 → 43), to 0.1308 admits 17 (54), to 0.1662 all but one (55); the best attainable
energy balance among the admitted improves 37.0 → 40.1 Wh (+8 %), depth of discharge 0.0446 →
0.0416 (−7 %), pointing error 0.00065 → 0.00061 (−7 %); settling time and mass do not move. The fit
had said so: control effort has zero exponent at K = 1 and the excluded designs sit in the K = 3
term where it has none. Here the method argues *against* relaxing: the requirement removes designs
without removing attainable extremes.

The converse, a slack requirement: peak slew power 2.6 W in the primary regime excludes 267 of 706
feasible designs and not one near-frontier design; the band's largest value is 2.6 W. The method
shows slackness on the frontier directly (zero exponent, zero excluded, the band's range inside the
limit). It does not show the requirement is idle: the 267 are the large wheels, all at least 1.5
band widths inside, and whether the requirement or the frontier is the reason to drop them is the
engineer's reading.

## 4. Ways of using the fit alongside requirements

| Use | Where it lives | The chart | The band | The exponents | The per-term report |
|---|---|---|---|---|---|
| **Filter, then fit** (constrained): feasible set ∩ requirements, then fit | spike A; Appendix D.4 | positions of the admitted designs only | the frontier of the admitted set | its contending set; on the *same* conditioning the primary exponents move by ≤ 0.013, the baseline regime flips the power-margin / energy-balance pair (0.178 + 0.019 → 0 + 0.214: one axis, spike-redundancy); **re-conditioning the subset moved peak slew power 0 → 0.24 in the primary regime, a conditioning artefact, not a finding** | per-term sets of the admitted designs |
| **Fit all, read requirements as regions** (unconstrained, then read) | this spike, section 1; Appendix D | each threshold a half-space crossing the band | which near-frontier designs each requirement excludes; the joint share (66 %, 44 %) | the price w_i Δu_i and the elasticities (section 2) | the term in which the metric contends, and whether the excluded designs sit in it |
| **Derive a threshold from the frontier** | Appendix D, one sentence; the docs' case page | | the band's extent in the attribute is the slack-on-the-frontier threshold (primary: 2.6 W, 0.0086 degree, 0.16 N.m.s, 14.7 kg) | at K = 1 the elasticity is constant on the surface, so nothing "turns"; at K = 3 it turns at a cell boundary | a boundary aligned with an attribute gives a threshold: the primary regime's term 3 (47 of the 56 band designs) holds every small and medium wheel and no large one, so any limit in (2.6, 6.3) W separates the term where peak slew power contends (w 0.61, against pointing error 0.23: the tracker trade) from the terms where it does not; the chosen 2.6 W is that boundary. Control effort and mass overlap across cells: no threshold is derived |
| **Relax a requirement** | this spike, section 3; Appendix D | | the ladder: admitted designs per candidate | the cost at the frontier per design | which cells the admitted designs come from |

What the method does not do, in every use: it does not say a requirement is wrong, or what the
mission needs; it prices the requirement on this table's fitted frontier under this conditioning;
its elasticities are features of the fit; the binding requirement changes with the regime; and
"slack on the frontier" is not "unnecessary". Hold the conditioning and tau fixed when
requirements are compared, or the comparison reads the conditioning.

Literature, described and not cited (no DOI verified here): systems-engineering requirements
analysis treats early-phase thresholds as negotiable; MDAO handles thresholds as inequality
constraints and reads the optimum's sensitivity to a constraint's bound (its multiplier) as the
constraint's cost. The elasticity along the fitted surface is the empirical analogue of a ratio of
such multipliers, from a fit on evaluated designs rather than an optimizer's conditions, and the
band replaces the single optimum by the set of near-frontier designs.

## 5. Presentation

Full case analysis (Appendix D, the docs' case page): one table, the requirements table of
section 1 extended with the price and the two largest elasticities (one row per requirement per
regime, one joint row), with a sentence per regime naming the cutting requirement and the slack
ones. At most one figure: the relaxation ladder of the baseline regime's pointing error (admitted
near-frontier designs and best attainable control effort against the limit); its sentence, "past
0.012 degree most of the band is admitted and the best control effort improves by 40 %; past
0.0155 nothing more", is also the table of section 3, so the figure is optional. The per-design
costs of section 2 are a paragraph, not a table.

The paper's Discussion: plain options.

- D1. One paragraph after "Three claims": the fit alongside requirements prices a requirement at
  the frontier and gives a relaxation request its numbers; it does not say a requirement is wrong;
  one pointer to Appendix D. About 90 words; a new use, so it widens the Discussion by one topic.
- D2. One sentence added to "Three claims" (the decision claim): that a threshold requirement can
  be read against the fit as a half-space of the chart, priced by the elasticities, with the
  numbers in Appendix D. No new paragraph.
- D3. Nothing in the paper; Appendix D and the docs' case page carry it.

Reproduction: `uv run --project <repo> python <scratchpad>/spike-B/analysis.py <repo>` and
`analysis2.py` (the scratchpad is the session's, not the repository); every number above is in
`run1.log` and `run2.log`.
