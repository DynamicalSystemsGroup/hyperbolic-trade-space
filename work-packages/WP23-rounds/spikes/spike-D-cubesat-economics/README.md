# Spike D: commercial CubeSat economics for the cost-to-build budget (H-2)

Question (the supervisor, `WP27-decisions.md`, "H-2", verbatim there): calibrate the cost-to-build budget so the
ballpark for parts, assembly and launch reads sanely to a professional who knows CubeSat economics; price per unit,
with the fleet size a configuration variable; two pricing metrics (unit cost, fleet cost = unit cost times the
number of units); every part and the assembly get a fixed base cost plus a curve whose unit cost falls as the
number of units rises, so the total grows at a decreasing rate. Read-only on the model, the data, the paper and the
docs. Script `economics.py` (this folder; run `uv run python work-packages/WP23-rounds/spikes/spike-D-cubesat-economics/economics.py`
from the repository root); its output is `economics-output.txt` and the budget shares are `admit-shares.txt`.
Sources opened on 2026-11-10 (the table in section 1): 29, each with a figure or a method used below.

**Answer in one paragraph.** The case's roll-up is in the right order of magnitude for the parts the configuration
swaps (wheels, tracker, panels, battery) and low on three things: the fine star tracker (155,000 against 40,000 to
82,400 for a 2 arcsec class unit), the solar panels (150,000 USD/m^2 is the low end of the catalogue; 250,000 sits
mid-range) and the battery (50 USD/Wh against 30 to 250). It has no assembly and integration line, and it prices a
fleet of one: one configuration at one price. A published 12U platform lists from 560,000 EUR (opened; a 449,000 USD figure for another vendor was seen in a search
summary only), so a single unit that reads as the case's 216,200 USD reads low to a
professional. With the proposed prices the baseline configuration costs 350,000 USD to build at n = 1 and 193,000
per unit at n = 10 (a 45 percent fall); the fleet of ten costs 1.93 million to build and 2.86 million with launch at
7,000 USD/kg. The evidence for the curves is one source family: the cost-estimating community's cumulative-average
learning rates for spacecraft (95 percent for 1 to 10 units, 90 for 11 to 50, 85 above) from Meisl and Morales as
quoted in source 24. No vendor publishes quantity tiers; the fixed shares are choices, not findings, and the
sensitivity table shows what they move. A defensible H-2 budget is a limit on the unit build cost between 300,000
and 450,000 USD (the two numbers the supervisor already named), with the baseline at 350,000 USD; where it falls
among the designs depends on n (section 6).

## 1. Sources (all opened 2026-11-10)

Kind: **L** vendor list price; **C** catalogue average cost (satcatalog.com, a vendor-reported "average cost" with the
fiscal year it states); **R** reported secondary figure; **M** method source. Prices as printed; EUR are not
converted. An entry marked "no FY" prints no fiscal year.

| # | Item | Figure | Kind | URL |
|---|---|---|---|---|
| 1 | Reaction wheel RW0, 137 g, 20 mNms; set 4RW0 (4 wheels) | 4,100 EUR each (MOQ 4); 18,400 EUR per set (4,600 per wheel) | L | https://nanoavionics.com/cubesat-components/cubesat-reaction-wheels-control-system-satbus-4rw/ |
| 2 | Reaction wheel RW-0.003, 50 g | 15,000 to 17,000 USD (FY2021) | C | https://www.satcatalog.com/component/rw-0003/ |
| 3 | Reaction wheel CubeWheel (SAVOMID), 80 g | 6,000 to 7,000 USD (FY2021) | C | https://www.satcatalog.com/component/cubewheel/ |
| 4 | GITAI star tracker 0.7 kg, 75 arcsec; reaction wheel 2.7 kg, 0.3 N.m | 12,000 USD; 30,000 USD | L | https://gitai.tech/satellite-components/ |
| 5 | Star tracker Twinkle (Arcsec), 40 g | 40,000 to 50,000 USD (FY2022) | C | https://www.satcatalog.com/component/twinkle-star-tracker/ |
| 6 | Star tracker STAR-T3 (Space Inventor), under 2 arcsec pitch and yaw | 82,400 USD (FY2021) | C | https://www.satcatalog.com/component/star-t3/ |
| 7 | Fine sun sensor TensorFSS-15M, 0.2 degree | 1,800 to 2,300 USD, updated 2026-11-03 | L | https://satsearch.co/products/tensortech-fss-15-fine-sun-sensor |
| 8 | Coarse sun sensor SunSense (TakeMe2Space) | 400 USD (no FY) | C | https://www.satcatalog.com/component/sunsense |
| 9 | Magnetorquers MTQ M6P (0.3 A.m^2) and MP42 (5 A.m^2) | 1,330 EUR (MOQ 6, page also says 3); 2,170 EUR (MOQ 3) | L | https://nanoavionics.com/cubesat-components/cubesat-magnetorquer-satbus-mtq/ |
| 10 | 3U solar panel, 8.4 W in LEO (EnduroSat) | 5,100 to 5,200 USD (FY2021) | C | https://www.satcatalog.com/component/3u-solar-panel/ |
| 11 | 6U deployable solar array, 19.2 W in LEO (EnduroSat) | 37,200 USD (FY2021) | C | https://www.satcatalog.com/component/6u-deployable-solar-array/ |
| 12 | Battery pack over 50 Wh, 0.36 kg (TakeMe2Space) | 1,500 USD (no FY) | C | https://www.satcatalog.com/component/powerbank-50wh-battery-pack/ |
| 13 | Battery matrix 350 Wh, 1.26 kg (Ecuadorian Space Agency) | 53,000 to 86,500 USD (FY2022) | C | https://satcatalog.com/component/titan-1-350whr-high-energy-density-battery-matrix |
| 14 | 12-unit structure, 2.0 kg (Innovative Solutions In Space) | 14,125 USD (FY2021) | C | https://satcatalog.com/component/12-unit-cubesat-structure |
| 15 | On-board computer OBC-P3 (Space Inventor) | 8,830 USD (FY2021) | C | https://www.satcatalog.com/component/obc-p3/ |
| 16 | ICEPS all-in-one core (EPS, OBC, 2 radios, IMU) | 22,000 to 70,000 USD (FY2022) | C | https://www.satcatalog.com/component/iceps-spacecraft-system-core-all-in-one/ |
| 17 | SmallSat EPS 2.0, 660 W (NanoAvionics), larger than a 12U needs | 70,700 to 99,140 EUR, MOQ 1 | L | https://nanoavionics.com/cubesat-components/cubesat-electrical-power-system-eps/ |
| 18 | 12U and 16U platform (Spacemanic), payload 16 kg (12U) | "From 560 000 EUR" | L | https://spacemanic.com/platforms/12u16u/ |
| 19 | SpaceX rideshare to SSO, price history | 5,500 (2022), about 6,000 (2024 to early 2025), 6,500 (Nov 2025), 7,000 USD/kg from 2026; 350,000 USD for up to 50 kg; the first-party page returns no text | R | https://newspaceeconomy.ca/2026/02/27/satellite-ridesharing-market-analysis-2026/ |
| 20 | Same, and "no public price list for a single CubeSat"; dedicated Electron about 9.2 M USD per launch (Rocket Lab average launch revenue, H1 2026, not a list price); 6U at 12 kg is 84,000 USD of launch mass | 350,000 USD / 50 kg, 7,000 USD/kg, as of October 2026 | R | https://spacenexus.us/guide/cost-to-launch/cubesat |
| 21 | Same: "350,000 USD for the first 50 kg, then 7,000 USD per additional kg"; a 12U of about 24 kg flies through an integrator whose price is not stated | as of September 2026 | R | https://spacenexus.us/blog/how-to-estimate-total-mission-cost-small-satellite |
| 22 | Electron, publicly stated price and capacity | about 7.5 M USD; about 300 kg to LEO, 200 kg to SSO; updated 2026-09-13 | R | https://orbitalradar.com/launch-vehicles/electron |
| 23 | Launch of a CubeSat, FY2022: SpaceX 275,000 USD / 50 kg; ISS deployment 90,000 USD per 1U (270,000 for 3U) | | R | https://www.satbase.com/articles/cubesat-launch-costs |
| 24 | Learning-rate guideline for spacecraft: cumulative-average (Wright) 95 percent for 1 to 10 units, 90 for 11 to 50, 85 for more than 50 (Meisl and Morales); the community "typically uses a relatively flat 95%" for small quantities; observed in industry 54 to 108 percent | | M | https://www.iceaaonline.com/wp-content/uploads/2018/07/MM01-Paper-Learning-Rate-Sensitivity-Model-Anderson.pdf |
| 25 | Spacecraft bus programs: individual slopes from 87 to 176 percent on cumulative average cost (small data) | | M | https://iceaaonline.com/?p=6891 |
| 26 | Example estimate for a 217 M USD small mission: spacecraft 53.6 M, systems integration and testing 9.0 M (one column; the others fold it into the spacecraft); lists SSCM, the small-spacecraft cost model | 9.0 / 53.6 = 17 percent | M | https://www.nasa.gov/sites/default/files/atoms/files/saing_nasa_and_smallsat_cost_estimation_overview_and_model_tools_s3vi_webinar_series_10_jun_2020.pdf |
| 27 | Building a second flight model costs about 33 percent of the planned program cost (CubeSat thesis, MIT 2016) | | M | https://dspace.mit.edu/handle/1721.1/105560 |
| 28 | 1U platform from 25,000 USD, 6U platform over 200,000 USD (EnduroSat slides, undated, as relayed) | | R | https://keeptrack.space/deep-dive/how-much-does-a-satellite-cost |
| 29 | CYGNSS: eight microsatellites of 28.9 kg, NASA sponsored it for 152 M USD (mission, not hardware) | | R | https://en.wikipedia.org/wiki/Cyclone_Global_Navigation_Satellite_System |

Opened and found to hold no usable number: SpaceX's own rideshare page (a script shell), GomSpace, ISISpace and
EnduroSat platform pages (no price), the BCT CubeSat marketing sheet (no price), NanoAvionics' 2025 constellation
release (50 power systems, no value), the PolSIR announcement (two 12U buses, no contract value; Military
Aerospace, 2024-06-13), the TROPICS and Starling pages (no cost). Not reachable on 2026-11-10: cubesatshop.com
(connection refused, so the CubeSpace and CubeWheel store prices are unconfirmed), EnduroSat's store (404),
web.archive.org (blocked here). Seen in search summaries only and not used: EnduroSat 12U XL platform 449,000 USD and
structure 13,000 USD, CubeSpace CubeStar Gen 2 17,600 USD, a "20 to 40 percent integration and test" rule (the page it
was said to come from, spacenexus.us/blog/how-to-estimate-total-mission-cost-small-satellite, source 21, holds no such
figure, so it is dropped).

**What the sources do not give.** No vendor publishes a quantity price tier; the only volume evidence is a minimum
order (sources 1 and 9) and the learning-rate guidance (24, 25). No source gives an assembly-and-integration price for
a 12U; the assembly line below rests on source 26 (17 percent, a larger class), source 27 and the gap between a
platform's list price (18) and its parts (14 to 17). No source gives the broker's fee for a single CubeSat; the
launch model is the wholesale per-kilogram rate (19 to 21).

## 2. Where the case stands now (read-only)

`stakeholders.sysml`, part `unitCosts` and calc `CostToBuild`: bus 60,000 + panels 150,000 USD/m^2 + battery
50 USD/Wh + antenna 15,000 + IMU 5,000 + 3 x (8,000 + 2,000,000 USD/(N.m) x peak torque) + tracker (5,000 + 300,000
USD.arcsec / accuracy). The doc says "chosen for plausibility ... never cited or calibrated". The launch cost is 6,000
USD/kg times the total mass (`cubesat.sysml`, `launchRate`); the launch budget is 90,643 USD (15.1 kg). The numbers
below recompute the roll-up from the formulas (`economics.py`): baseline 216,200, compact 158,500, agile 407,600 USD,
and 155,011 to 425,781 over the 1,000 designs (median 237,518). It prices one satellite, with no assembly, no fleet and
no curve.

| part (case's single-unit price) | sources | reading |
|---|---|---|
| wheels, 3 x (8,000 + 2.0e6 x torque): small 25,800; medium 36,000; large 84,000 | 1 to 4 | per wheel 8,600 / 12,000 / 28,000 against 4,100 to 6,500 (small), 6,000 to 17,000 (30 mNms), about 30,000 (a 0.3 N.m wheel): in band, kept |
| tracker, 5,000 + 300,000 / accuracy: 15,000 / 35,000 / 155,000 | 4 to 6 | coarse and medium in band (12,000 at 75 arcsec; 40,000 to 50,000); fine is high against 82,400 at 2 arcsec: halve the coefficient to 150,000 (10,000 / 20,000 / 80,000) |
| panels, 150,000 USD/m^2 | 10, 11 | a 3U face (0.034 m^2, the face area is my assumption, the page gives none) at 5,100 is 150,000; the 6U deployable at 37,200 for 19.2 W is dearer per watt (1,940 against 620 USD/W). The case's panels are deployed wings: 250,000 USD/m^2, inside a 150,000 to 400,000 range |
| battery, 50 USD/Wh | 12, 13 | 30 (1,500 / 50 Wh), 151 to 247 (53,000 to 86,500 / 350 Wh, FY2022 and the arithmetic is mine): 150 USD/Wh |
| bus 60,000 + antenna 15,000 + IMU 5,000 = 80,000 | 14 to 17 | structure 14,125 + OBC 8,830 + EPS and radios (22,000 to 70,000 for an all-in-one) = 45,000 to 93,000 before the antenna and harness: 80,000 kept |
| assembly and integration | 18, 26, 27 | absent: the platform list price (from 560,000 EUR, source 18) is more than twice the case's own part roll-up of 250,000 |

## 3. The pricing curves (proposal)

For a part p at the configuration x and a fleet of n units:

total_p(n; x) = u_p(x) [ f_p + (1 - f_p) n^(1 - b_p) ],  b_p = -log2(s_p)

- `u_p(x)` is the case's single-unit price relation (kept in shape; coefficients as in section 2), so `total_p(1) = u_p`.
- `f_p` is the fixed base, the share of the single-unit price paid once per fleet (qualification, tooling,
  procedures, the first unit's engineering); the remaining share scales with the units at the average unit cost
  `u_p n^(-b_p)` (Wright's cumulative-average form, the form of source 24).
- `s_p` is the learning slope: 95 percent is the community's flat default for small lots, 90 the 11 to 50 band.
  Source 24 gives these bands for a whole spacecraft; the split between parts below is a choice, not a finding.

| part | u_p(x) at n = 1 (USD) | fixed share f | slope s | b | total exponent 1 - b | why this curve |
|---|---|---|---|---|---|---|
| bus block (structure, OBC, EPS, radio, antenna, IMU) | 80,000 | 0.30 | 0.90 | 0.152 | 0.848 | integrated avionics, tooling and qualification; economies of scale in production |
| solar panels | 250,000 x area (m^2) | 0.15 | 0.90 | 0.152 | 0.848 | cell and layup production is repetitive |
| battery | 150 x capacity (Wh) | 0.10 | 0.90 | 0.152 | 0.848 | cells are bought in lots |
| reaction wheels (3) | 3 x (8,000 + 2.0e6 x torque) | 0.15 | 0.95 | 0.074 | 0.926 | precision bearings and balancing; relatively flat |
| star tracker | 5,000 + 150,000 / accuracy (arcsec) | 0.20 | 0.95 | 0.074 | 0.926 | optics, calibration and software per unit; relatively flat |
| assembly, integration and test | 100,000 | 0.50 | 0.90 | 0.152 | 0.848 | labour learning; a large fixed share for procedures, fixtures and the test campaign; 40 percent of the baseline's parts (source 26's 17 percent is a larger class; the platform price gap in section 2 suggests more) |

Flat means the 95 percent band; strong means 85 percent (b = 0.234). The supervisor asked for some parts relatively flat
and others strongly scaling: here 0.95 against 0.90, and `economics.py` shows the all-flat and all-strong envelopes
(unit build cost at n = 30: 197,779 flat, 160,910 as proposed, 115,993 strong). The sources do not support a spread wider
than 85 to 95 percent across a fleet of 1 to 30; a part with no learning at all (zero, source 24 notes "zero observed
learning" occurs) is the limit b = 0.

**Launch** (a separate line, linear in the fleet): launch(n) = 7,000 USD/kg x total mass x n. The 2026 rate is 7,000
(sources 19 to 21); the case's 6,000 is the 2024 to early 2025 figure. At the baseline mass (13.291 kg) that is
93,040 USD per satellite. A SpaceX booking has a 50 kg minimum slot (350,000 USD): at one to three satellites of
this class the true launch bill is 350,000 USD and fleets of four or more pay the linear rate (13.291 x 4 = 53 kg).
The minimum is a `max(.)`, not a posynomial in the metric; as a limit it is GP-expressible (max(p, q) <= B is the pair p <= B,
q <= B). A broker adds a dispenser, integration and a margin (sources 20, 21: no number published).

**The fleet-size variable.** n a positive number in the model (a geometric program needs real exponents) read as a
count. Proposed range 1 to 30. The learning guidance is stated to 50 units, most spacecraft programs hold two to five
units, and the cases in the sources are 2 (PolSIR) to 8 (CYGNSS); 1 to 10 is the conservative range and 1 to 50 the
widest the sources stand behind. The default for the three named configurations is n = 1 (priced as now).

**The two pricing metrics** (build + launch, or either alone; the supervisor's "manufacturing and launch costs of a
fleet"):
- fleet cost F(n, x) = sum over parts of total_p(n; x) + assembly(n) + launch(n);
- unit cost U(n, x) = F(n, x) / n.

F grows with n at a decreasing rate on the build part and linearly on the launch part; U falls. Both are traded or
budgeted per configuration; neither models the fleet's communication, range or networking.

## 4. The totals for a representative design

The baseline configuration (medium wheels, medium tracker, 0.6 m span, 80 Wh, 13.291 kg), proposed prices.

| n | build, fleet | build, per unit | launch, fleet | fleet cost | unit cost | unit cost against n = 1 |
|---|---|---|---|---|---|---|
| 1 | 350,000 | 350,000 | 93,040 | 443,040 | 443,040 | 1.00 |
| 3 | 745,393 | 248,464 | 279,120 | 1,024,513 | 341,504 | 0.77 |
| 10 | 1,926,934 | 192,693 | 930,400 | 2,857,334 | 285,733 | 0.64 |
| 30 | 4,827,305 | 160,910 | 2,791,200 | 7,618,505 | 253,950 | 0.57 |

Per-part totals at n = 1, 3, 10, 30 are in `economics-output.txt`. The fleet cost rises (443 thousand to 7.6 million)
while the unit cost falls (443 to 254 thousand), the pair the supervisor asked for. With the 50 kg minimum the launch
bill at n = 1 is 350,000, so the unit cost at n = 1 is 700,000 and at n = 3 it is 365,131.

The compact configuration is 281,300 USD to build at n = 1, the agile 501,000 (cases' current roll-up 158,500 and
407,600). The factor between compact and agile moves from 2.6 to 1.8 because the fixed block, the panels and the
assembly now weigh more than the tracker.

## 5. Does the case model's budget read sanely

A professional compares the whole build to a platform price. A single 12U with bus, ADCS and power at 350,000 USD
sits below a 12U platform list of 560,000 EUR (source 18) because the
case omits communications, the payload interface, flight software and a test campaign beyond the 100,000 assembly
line. That is a fair reading for a model of attitude control, power and structure. At n = 10 the 193,000 per unit
reads as a small constellation's production price (source 28 puts a 6U platform above 200,000).
Launch dominates the unit cost at fleet scale: 93,040 of 253,950 at n = 30 (37 percent).

## 6. The H-2 budget band

The budget is the supervisor's. The two limits he named, 300,000 and 450,000 USD, stay inside the evidence. The share of
the feasible designs a unit build cost limit admits (`admit-shares.txt`; 780 baseline-regime and 706 primary-regime
feasible designs; n is the fleet size at which the limit is read):

| limit on unit build cost | n = 1 | n = 3 | n = 10 | n = 30 |
|---|---|---|---|---|
| 300,000 | 9 to 10 % | 78 % | 99 % | 100 % |
| 350,000 | 37 to 40 % | 97 % | 100 % | 100 % |
| 450,000 | 91 % | 100 % | 100 % | 100 % |

Read at n = 1, 450,000 admits about 90 percent and 350,000 about 40 percent. Read at the fleet's n, a unit-cost limit stops binding for n of 3 or more, so a unit cost
budget plus a free n lets the optimizer buy discount with more units; a fleet cost budget does the opposite and caps n.
Each is a one-line GP constraint.

## 7. Fit to the posynomial and geometric-program form

total_p(n; x) = u_p(x) f_p + u_p(x) (1 - f_p) n^(1 - b_p) is a sum of a positive term and a positive monomial in n, times
`u_p(x)`. With u_p posynomial in x (area, capacity and 1/accuracy are monomials; the wheel and tracker prices are
a constant plus a monomial) every term is a posynomial in (n, x). The sum over parts, the launch term (a monomial in
n and the mass, itself a posynomial) and the fleet cost F are posynomials; U = F / n divides a posynomial by a monomial
and stays one; a limit F <= B or U <= B is a GP constraint. Exponents 1 - b are in (0, 1) so the total is concave in n
(growing at a decreasing rate) and the average cost falls as n^(-b). A learning slope fitted to the data is the exponent
of a monomial, which the fit already estimates. The 50 kg launch minimum and the integer count are outside the form.

## 8. Plain options for the driver

**A. Curve family**
1. Wright cumulative-average with a fixed share per part, as in section 3 (one slope per part).
2. The same with every part at one slope (95 percent), fixed shares kept.
3. A power law with no fixed share (`u1 n^(1 - b)`), which removes the fixed base the supervisor asked for.

**B. Fleet-size range**
1. 1 to 10.
2. 1 to 30.
3. 1 to 50.

**C. Budget**
1. A limit on unit build cost, read at the configuration's own n: 300,000, 350,000 or 450,000 USD.
2. A limit on the fleet cost (build and launch) with the fleet size free, set by the driver from section 4.
3. Both, a unit cost limit and a fleet cost limit.

**D. Launch**
1. 7,000 USD/kg linear (section 3), the case's 6,000 replaced.
2. The same with the 50 kg minimum slot as a second limit.
3. The case's 6,000 USD/kg kept.

**E. Prices for the swapped parts**
1. Update the three coefficients the sources move: tracker 150,000, panels 250,000 USD/m^2, battery 150 USD/Wh; add assembly 100,000.
2. Keep the current coefficients and add only the curves and the fleet variable.

Open items: the CubeSpace store prices (cubesatshop.com unreachable here) and a first-party SpaceX price page were not
confirmed; a vendor quote at 1, 10 and 30 units would replace the learning-rate guidance with data.
