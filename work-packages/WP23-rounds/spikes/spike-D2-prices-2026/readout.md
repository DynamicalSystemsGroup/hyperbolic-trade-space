# Spike D2: the cost model against 2026 prices

Question (the supervisor, `WP30-decisions.md`, 10:05, verbatim there): "recalibrate your research. i am not convinced you
did real desk work ... please focus your research on 2026 prices", and a 1,000,000 USD budget for 25 satellites is "more
than enough". No model change in this spike. Script `economics2026.py`, output `economics2026-output.txt` (same folder;
`uv run --no-project python economics2026.py`). All pages opened 2026-11-11. Prices as printed; EUR converted at an
assumed 1.10 USD per EUR (I did not look up a 2026 rate); every conversion is marked.

## 0. The numbers that matter

- **His two pages hold no number that moves a coefficient.** keeptrack and spacenexus price a 1U and a 6U bus (from
  undated EnduroSat slides), the Transporter rate and the big launchers. Neither prices a 12U, a part or a fleet. The
  launch rate they give (7,000 USD/kg, 350,000 USD for the 50 kg minimum) is the one WP30 already uses (D-1).
- **What the old spike did and did not have.** Launch was 2026 (sources 19 to 21). The part prices were mostly satcatalog
  "average cost" entries for fiscal years 2021 and 2022: that is the old data he suspected. This spike replaced them
  with 2026-dated vendor listings wherever one exists (section 2).
- **2026 platform prices by class, one vendor, one date** (TakeMe2Space, listed on satsearch, last updated 2026-08-26,
  "starts at", each with EPS, computer, attitude control, radios, sun sensors, GPS and, from 6U, reaction wheels and a
  star tracker): 1U 26,000; 3U 65,000; 6U 243,000; 12U 275,000; 16U 300,000 USD. Other 12U figures are higher
  (Spacemanic "from 560 000 EUR", EnduroSat 449,000 USD from a listing last updated 2024-02-05).
- **The baseline's build under 2026 figures** (parts re-priced, curves unchanged), build per unit:
  n = 1: 368,000 (spike D 350,000); 3: 262,000 (248,000); 10: 202,000 (193,000); 25: 173,000 (165,000); 30: 168,000
  (161,000). The 2026 range over the parts' own spread is 297,000 to 437,000 at n = 1. The change is plus 5 percent at the
  central values, inside the spread (section 3).
- **Launch is the larger line and it did not fall.** 7,000 USD/kg times the baseline's 13.291 kg is 93,000 per
  satellite; 25 of them are 2.33 million, before any dispenser or broker fee.
- **1,000,000 USD for 25 satellites** is 40,000 per satellite. The baseline (a 12U) costs about 266,000 per unit built
  and launched at n = 25: the budget buys 2 of them (3 on the lowest 2026 prices), not 25. It fits the 1U class: a 1U
  platform (25,000 to 26,000) plus 2 kg of rideshare mass (14,000) is 40,000, times 25 is 1,000,000, with nothing left
  for payload, dispenser, integration, licence or ground (section 4).

## 1. His two pages, read in full first

Fetched 2026-11-11 with the fetch tool (a model summarises the page, so the figures below are the tool's reading, not a
byte copy; the spacenexus ones repeat identically on four spacenexus pages, which is the only cross-check available).

**keeptrack.space/deep-dive/how-much-does-a-satellite-cost** (Theodore Kruczek; "published October 28, 2026",
"fact-checked October 21, 2026"). A deep-dive article: a secondary source.

| Figure | Where on the page | Date the page gives |
|---|---|---|
| 1U platform about 25,000 USD; 6U platform over 200,000 USD; bus only | intro; "How much does a small satellite cost?" | EnduroSat conference slides, undated ("INAF conference") |
| Launch 70,000 USD (1U), 450,000 USD (6U) | same section; "Build vs. launch vs. operate" | same slides, undated |
| 100 kg smallsat about 700,000 USD on Transporter at a reported 2026 rate of about 7,000 USD/kg | same section | 2026; the page calls it a secondary-source estimate |
| Falcon 9 list price 74 million USD | "Build vs. launch vs. operate" | 2026 |
| NanoAvionics: student cubesats "a few thousand dollars" | same section | January 2023 |
| SDA Tranche 1: 1.8 billion USD for 126 (9 to 17 million each) | "Government constellations" | February 2022 |
| GPS IIIF 514 million for two | "How much does a GPS satellite cost?" | 2026-06-15 |
| 2025 manufacturing revenue 20.4 billion USD over 4,434 satellites, about 4.6 million each (crude) | "Industry totals" | SIA, May 2026 |

**spacenexus.us/guide/space-launch-cost-comparison** ("Updated October 11, 2026"; prices "as of 2026-10-11"). A guide
page whose $/kg figures are its own arithmetic: a secondary aggregator.

| Figure | Where on the page | Date |
|---|---|---|
| Transporter 350,000 USD for 50 kg to SSO, 7,000 USD/kg; 5,500 (2023), 6,000 (2024), 6,500 (2025), 7,000 (2026), 7,500 (2027) | "Transporter Rideshare Pricing" | "SpaceX rideshare price list" |
| No Transporter reservations beyond late 2028 or early 2029 | same | June 2026 SpaceNews, via the Space Foundation |
| 150 kg satellite about 1 million USD on rideshare before integration | same, FAQ | 2026 |
| Falcon 9 dedicated about 74 million USD | vehicle table; "Falcon 9 and Falcon Heavy Details" | Spaceflight Now, Feb 2026 |
| Electron about 9.2 million USD, average revenue per launch, H1 2026 | vehicle table | Rocket Lab SEC filing; not a list price |
| Neutron 55 million (text) or 50 million (table); the page contradicts itself | same | target, unflown |
| Integration, insurance, range fees | "Hidden costs" | no dollar amounts given |

My check of the driver's read: confirmed on every point. Neither page prices a 12U cubesat or a fleet. The two pages are
not independent of what the old spike used: the EnduroSat slides are source 28 there.

## 2. 2026 sources, by part

Kind: **V26** vendor or marketplace listing carrying a 2026 "last updated" date; **VP** vendor price page, no date, live
on 2026-11-11 (a current price list, not provably 2026); **N** news or secondary; **OLD** before 2025, used only where no
2026 figure exists.

| Part | Figure | Kind, date | URL |
|---|---|---|---|
| Reaction wheel | SpaceWheel30 (TakeMe2Space), 30 mNms, 75 mN.m, 280 g: from 4,000 USD | V26, 2026-10-21 | https://satsearch.co/products/tm2s-rwa |
| | WHL-100 (Space Inventor), 100 mNms, 20 mN.m, 360 g: 25,000 EUR (about 27,500 USD) | V26, 2026-01-07 | https://satsearch.co/products/space-inventor-whl-50 |
| | RW0 (NanoAvionics), 20 mNms: 4,100 EUR each, MOQ 4; set of 4: 18,400 EUR (4,600 each) | VP | https://nanoavionics.com/cubesat-components/cubesat-reaction-wheels-control-system-satbus-4rw/ |
| | CubeWheel CW00500 11,450 USD (a search summary; the shop was unreachable) | N, undated | https://www.cubesatshop.com/?p=20823 |
| Star tracker | STR-P3 (Space Inventor), under 1.5 arcsec, 300 g: 85,000 EUR MSRP (about 93,500 USD) | VP, page titled "State of the art report 2025" | https://space-inventor.com/equipment/startracker |
| | Auriga optical head (Sodern): 50,000 EUR, "indicative, excluding NRE" (a search summary) | N, undated | https://www.cubesatshop.com/product/sodern-auriga-cp/ |
| | CubeStar Gen 2 (CubeSpace) 17,599 USD, MAI-SS 32,500 USD | OLD (satcatalog FY2023; shop, undated) | https://www.satcatalog.com/component/gen2-cubestar/ |
| | No 2026-dated tracker price found; CubeStar Gen 2 and KAIROSPACE listings say "request info" | gap | |
| Solar panels | 3U panel (EnduroSat), 8.4 W, 147 g: 6,900 USD | V26, 2026-07-14 | https://satsearch.co/products/endurosat-3u-cubesat-solar-panel |
| | 6U panel (EnduroSat), 19.2 W, 392 g: 17,100 USD | V26, 2026-07-14 | https://satsearch.co/products/endurosat-6u-solar-panel |
| | 6U deployable array (EnduroSat): 51,300 USD | V26, 2026-07-14 | https://satsearch.co/products/endurosat-6u-deployable-solar-array |
| | the same products in the old spike: 5,100 and 37,200 USD | OLD, FY2021 | https://www.satcatalog.com/component/3u-solar-panel/ |
| Battery | PowerBank 50 Wh (TakeMe2Space), 390 g: 1,200 USD | V26, 2026-10-31 | https://satsearch.co/products/tm2s-powerbank |
| | BAT-14-P4 (Space Inventor), 50 Wh, 314 g: 9,000 EUR | V26, 2026-01-08 | https://satsearch.co/products/space-inventor-bat-14-p4 |
| | CubeSat battery packs (NanoAvionics): 2,750 to 11,000 EUR for 23 to 161 Wh configurations (2S2P is about 46 Wh by my arithmetic) | VP | https://nanoavionics.com/cubesat-components/cubesat-smallsat-battery-pack/ |
| Structure | 12U frame (NanoAvionics): 10,000 EUR, MOQ 3; 6U 5,040; 8U 7,470; 16U 12,750 | VP | https://nanoavionics.com/cubesat-components/cubesat-structural-frame/ |
| | 12U XL structure (EnduroSat) 13,000 USD (a search summary; the store page returned 404 here) | N, undated | https://endurosat.com/cubesat-store/page/4/ |
| Computer | SatBus 3C2 main bus unit with computer (NanoAvionics): from 4,460 EUR, MOQ 3 | VP | https://nanoavionics.com/cubesat-components/satbus-3c2/ |
| | On-board computer (Space Inventor): 9,000 EUR MSRP | VP, "State of the art report 2025" | https://www.space-inventor.com/equipment/on-board-computer |
| | AICube GPU module from 11,000 USD (not a plain computer); CMCube from 4,800 USD; ZeroCube from 2,800 USD | V26 (AICube 2026-02-11, ZeroCube 2025-10-28) | https://satsearch.co/products/tm2s-aicube |
| Power system | CubeSat EPS 1.0 (NanoAvionics) from 8,470 EUR, MOQ 3; SmallSat EPS 2.0 70,700 to 99,140 EUR | VP | https://nanoavionics.com/cubesat-components/cubesat-electrical-power-system-eps/ |
| | EnduroSat EPS: "request info" (updated 2026-07-14) | gap | https://satsearch.co/products/endurosat-eps-i-electrical-power-system |

**Platforms by class**

| Class | Figure | Kind, date | URL |
|---|---|---|---|
| 1U / 3U / 6U / 12U / 16U | from 26,000 / 65,000 / 243,000 / 275,000 / 300,000 USD (TakeMe2Space; 12 h engineering support; bus only) | V26, 2026-08-26 | https://satsearch.co/products/tm2s-1u-cubesat (also -3u, -6u, -12u, -16u) |
| 12U, 16U | "from 560 000 EUR" (Spacemanic, 16 kg payload for the 12U) | VP, page footer 2026 | https://spacemanic.com/platforms/12u16u/ |
| 12U XL | 449,000 USD (EnduroSat store) | OLD, satsearch last updated 2024-02-05 | https://satsearch.co/products/endurosat-12u-platform |
| 1U, 6U | 25,000 and over 200,000 USD (EnduroSat slides, undated, as relayed) | N | keeptrack, above |
| 12U price on request | ISISpace; EnduroSat's current site lists 16U and 8U cubesats with no prices | gap | https://www.endurosat.com/products |

The 2026 platform list prices are lower than the old spike's single 12U data point (560,000 EUR) and agree with the model:
the 275,000 "from" price for a 12U with computer, power, attitude control and radios compares with the model's 350,000 for
a 12U with larger panels and a 100,000 assembly, integration and test line.

**Launch offers for cubesat classes**

| Item | Figure | Kind, date | URL |
|---|---|---|---|
| SpaceX Transporter | 350,000 USD for up to 50 kg, 7,000 USD/kg above; 325,000 at Transporter-15 (Nov 2025); 7,500 in 2027 | N: four 2026 pages repeat it; SpaceX's own page returns no text. Feb 2026 to Oct 2026 | https://newspaceeconomy.ca/2026/02/27/satellite-ridesharing-market-analysis-2026/ ; https://www.orbitalintel.org/satellites/how-much-does-it-cost-to-launch-a-satellite/ (updated 2026-10-08; says "published on SpaceX's rideshare portal") ; https://spacenexus.us/guide/cost-to-launch/cubesat (2026-10-11) |
| Next open Transporter slots | June and October 2027 (sun-synchronous, as of 2026-10-11); no reservations past late 2028 | N | spacenexus, above |
| Dedicated Falcon 9 | 74 million USD (January 2026 price card as summarised) | N | orbitalintel, above |
| Electron | about 9.2 million USD average revenue per launch, H1 2026, not a list price; 7.5 million "publicly stated" (updated 2026-09-13); Q2 analysis says 9.1 revenue, 4.4 cost per launch | N | https://orbitalradar.com/launch-vehicles/electron ; https://beancount.io/blog/2026/09/26/rocket-lab-q2-2026-earnings-analysis |
| Brokers (Exolaunch, ISILaunch, D-Orbit) | **no published per-U price anywhere.** Third-party guides disagree by an order of magnitude: 6U 22,000 to 40,000 (newspacemarket, "2026", no date, internally inconsistent: below the raw-mass cost at 7,000 USD/kg); 1U 40,000 to 80,000 and 3U 100,000 to 250,000 (a greenlaunch-type guide); EnduroSat slides 70,000 per 1U and 450,000 per 6U | weak | https://newspacemarket.com/guides/cubesat-launch-cost/ |
| ISS deployment | 90,000 USD per 1U (270,000 for 3U) | OLD, FY2022 (satbase); no 2026 Voyager price found | https://www.satbase.com/articles/cubesat-launch-costs |
| Momentus Vigoride | about 15,000 USD/kg, undated Wikipedia statement | OLD or undated; no 2026 price | https://en.wikipedia.org/wiki/Vigoride |
| Raw mass check | a 1U at the 2 kg limit is 14,000 USD of Transporter mass; a 6U at 12 kg 84,000 (spacenexus' own arithmetic) | N | https://spacenexus.us/guide/cost-to-launch/1u-cubesat |

**Volume and constellation pricing**

| Item | Figure | Kind, date | URL |
|---|---|---|---|
| NanoAvionics for SpinLaunch (Meridian) | 122.5 million EUR, 280 satellites of about 70 kg plus two prototypes, development and serial production included: about 437,000 EUR each by my arithmetic (an upper bound: it carries the development) | OLD: announced 2025-04-03; the nearest real per-satellite contract | https://www.microwavejournal.com/articles/43633-nanoavionics-secures-1225m-contract-to-build-280-satellites-for-meridian-space |
| EnduroSat | 24 buses for Vantor; 40 satellites for TrustPoint (2026-09); no contract values published | V/N, 2026-09 | https://satnews.com/2026/09/17/endurosat-secures-205-million-funding-round-and-wins-24-bus-contract-for-vantor-earth-observation-constellation/ |
| Starlink V2 Mini | about 400,000 USD each at volume (an estimate; SpaceX does not publish it) | N, 2026-04-13 | https://newspaceeconomy.ca/2026/04/13/the-satellite-manufacturing-market-after-starlink-how-mass-production-changed-the-economics-of-building-spacecraft/ |
| SDA Tranche 3 Tracking | 3.5 billion USD for four builders at 18 satellites each: about 49 million each by my arithmetic | N, 2026; a different class | same |
| Spire, Planet | no per-satellite figure found | gap | |
| Quantity tiers | no vendor publishes one; minimum order quantities only (NanoAvionics MOQ 3 or 4) | gap | |

## 3. The baseline priced under 2026 figures

Baseline: medium wheels (2 mN.m), medium tracker (10 arcsec), span 0.6 m (panel area 0.408 m^2), 80 Wh, 13.291 kg, a 12U.
Curves as in spike D, unchanged (fixed shares and slopes are spike D's choices). Only the single-unit coefficients move.

| Part | Old coefficient | 2026 central | 2026 low, high | Basis |
|---|---|---|---|---|
| bus block (structure, computer, power, radio, antenna, IMU) | 80,000 | 80,000 | same | 12U frame about 11,000 USD, computer 5,000 to 10,000, EPS 9,000 to 15,000 EUR, from VP pages; the radio has no price; sums to 40,000 to 60,000 before radios and harness. Not moved |
| solar panels | 250,000 USD/m^2 | 340,000 | 200,000 ; 340,000 | same-vendor 2021 to 2026 rise: 3U 5,100 to 6,900 (plus 35 percent), 6U deployable 37,200 to 51,300 (plus 38 percent); the old 250,000 times 1.366. Low: 6,900 over an assumed 0.034 m^2 face (the old spike's area assumption) is 203,000 |
| battery | 150 USD/Wh | 70 | 24 ; 200 | 1,200 USD over 50 Wh (24); NanoAvionics about 60 to 68 EUR/Wh (about 70); Space Inventor 9,000 EUR over 50 Wh (180 EUR, about 200) |
| reaction wheel, per wheel | 12,000 (medium) | 8,000 | 4,500 ; 27,500 | 4,000 USD (30 mNms) and 4,600 EUR (20 mNms) at the low end; 25,000 EUR (100 mNms) at the high end. Every 2026 wheel found is larger than the model's 2 mN.m medium wheel, so the band over-states the model's wheel |
| star tracker | 5,000 + 150,000/accuracy | same | same | at 1.5 arcsec the old relation gives 105,000 against 85,000 EUR (about 93,500 USD): holds. No 2026-dated price for the 10 arcsec grade |
| assembly, integration and test | 100,000 | 100,000 | same | no source prices it; unchanged (spike D's gap stands) |

Build per unit and launch for the baseline (USD; launch 7,000/kg times 13.291 kg is 93,037 per satellite, linear; with
the 50 kg slot the launch bill is 350,000 for n of 1 to 3):

| n | spike D build/unit | 2026 central | 2026 low | 2026 high | launch, fleet, linear | launch, fleet, 50 kg slot |
|---|---|---|---|---|---|---|
| 1 | 350,000 | 368,320 | 297,020 | 437,220 | 93,037 | 350,000 |
| 3 | 248,464 | 261,621 | 206,002 | 318,656 | 279,111 | 350,000 |
| 10 | 192,693 | 202,334 | 157,208 | 251,846 | 930,370 | 930,370 |
| 25 | 165,478 | 173,167 | 133,917 | 218,483 | 2,325,925 | 2,325,925 |
| 30 | 160,910 | 168,259 | 130,043 | 212,828 | 2,791,110 | 2,791,110 |

Fleet build (build per unit times n) at n = 25: 4.14 million (spike D), 4.33 (central), 3.35 (low), 5.46 (high).
Fleet with launch at n = 25 (linear): 6.46 / 6.66 / 5.67 / 7.79 million. Unit cost with launch at n = 25: 258,515 /
266,204 / 226,954 / 311,520. The spike D row reproduces WP30's R-5 values to the dollar (launch 93,037 here against
93,040 in R-5 is the rounding of 13.291 kg).

## 4. What 1,000,000 USD buys for 25 satellites in 2026

That is 40,000 USD per satellite, build and launch together, before payload, dispenser, integration, licence and ground
(a licence fee alone is 14,520 USD a year per smallsat call sign in the FY2026 FCC schedule, as relayed by orbitalintel).
For the baseline's 12U class the platform alone starts at 275,000 (2026-08-26) and the cheapest parts-based build at
n = 25 is 134,000 per unit (the low scenario), so the budget buys 2 baseline satellites with launch (3 on the lowest 2026
prices), or 4 (5) with launch left out. At n = 25 it covers about 15 percent of the baseline's unit cost with launch and
23 percent of the build alone. By scaling spike D's cheapest design (145,000 at n = 10) the cheapest of the 1,000 designs
is near 125,000 per unit at n = 25 (scaling, not computed on the data): 40,000 per unit admits none of them.

By class, no learning, list platform plus Transporter mass at the class limit (2 kg per U): 1U 25 x 40,000 = 1,000,000
(26,000 platform, 14,000 launch; 25 x 2 kg is exactly one 50 kg slot, 350,000, plus 25 x 26,000 = 650,000); 3U 2.68
million; 6U 8.2 million; 12U 11.1 million; 16U 13.1 million (16U mass assumed 32 kg). With EnduroSat's slide launch prices
a 1U fleet of 25 is 2.4 million and a 6U fleet 16 million. So the budget fits a fleet of 25 satellites of 1U class,
bus and rideshare mass only, and no larger class; it also fits a handful of 12U. It is "more than enough" only for the 1U
class and only if the broker's dispenser and integration cost less than the margin the 1,000,000 leaves, which is zero
on these numbers.

## 5. Moves against the old values

| Value in WP30 (E-1, D-1) | 2026 reading | Moves? |
|---|---|---|
| launch 7,000 USD/kg | confirmed by four 2026 pages; first-party page unreadable | no |
| 50 kg slot 350,000 USD | confirmed, same pages | no |
| tracker 150,000/accuracy | holds against the 85,000 EUR 1.5 arcsec unit | no |
| panels 250,000 USD/m^2 | the same vendor's panels are 35 to 38 percent dearer than the FY2021 entries; 340,000 | yes, up |
| battery 150 USD/Wh | 2026 listings span 24 to 200; the three-point geometric mean is 70 | within the band; lower at the centre |
| wheels 12,000 each | 2026 listings 4,000 to 27,500 for wheels larger than the model's | within the band |
| bus block 80,000 | inside 40,000 to 60,000 plus an unpriced radio | within the band |
| assembly 100,000, curves | no source | unchanged |
| the 12U single-unit price reading low (spike D, section 5) | a 2026 12U platform from 275,000 (and 560,000 EUR elsewhere) | the 350,000 sits above the cheap one, below the dear one |

## 6. Plain options for the driver

**A. The part coefficients**
1. Keep E-1 as set (panels 250,000, battery 150, wheels 12,000; baseline 350,000 at n = 1).
2. Move to the 2026 central values (panels 340,000, battery 70, wheels 8,000; baseline 368,320 at n = 1, 173,167 per unit at n = 25).
3. Move panels only (340,000) and leave the battery and wheels, which sit inside their 2026 bands; baseline 386,720 at n = 1 (panels 138,720, battery 12,000, wheels 36,000).

**B. The unit build cost limit, read at the configuration's own n** (placeholder 350,000)
1. Hold it; the central baseline is 5 percent higher at every n.
2. Re-run the pass-fraction ladder on the central coefficients at the gate before he sets it (the ladder is computed on
   data, not here).

**C. His 1,000,000 USD for 25 satellites**
1. Ask him which class he meant; the numbers fit a 1U-class fleet and not the 12U baseline.
2. Take it as a fleet cost limit on the baseline's class and say plainly in the ladder that it admits no design at
   n = 25 (a fleet limit with n free would pin n at 2 to 4).
3. Take a fleet limit from the ladder (the baseline fleet with launch is 6.7 million at n = 25) and record his 1,000,000 as
   the figure for a smaller class.

**D. Launch** (no change proposed): keep 7,000 USD/kg linear with the 50 kg slot as a note; or price the slot into the
unit cost for n below 4 (outside the form).

## 7. What I could not find

- Any broker's published per-U or per-satellite price for 2026 (Exolaunch, ISILaunch, D-Orbit, Momentus, Voyager ISS
  deployment): brokers quote per mission. The third-party per-U figures conflict by ten times and I used none.
- SpaceX's own rideshare page returns no text; the 7,000 USD/kg rests on four secondary pages that may share an origin.
- A 2026-dated price for a star tracker of the model's grades, an EPS or computer price carrying a 2026 date, and any
  assembly or test price.
- EnduroSat's store (404) and CubeSatShop (connection refused) were unreachable, so the CubeSpace and EnduroSat store prices
  come from search summaries only and are marked.
- Quantity tiers: none published; the learning curve still rests on the cost-estimating guideline (spike D source 24).
- Several "2026" guide pages (newspacemarket, spacenexus, newspaceeconomy, greenlaunch) are marketing or aggregator
  pages whose figures repeat each other or contradict themselves; I used them for the launch rate only, where four agree.

## 8. Sources by strength

1. **Vendor listing with a 2026 date and a USD price:** TakeMe2Space platforms and parts, EnduroSat panels, Space Inventor
   wheel and battery (satsearch, section 2). These are marketplace listings ("starts at"), the vendors' own entries.
2. **Vendor price page, live 2026-11-11, undated:** NanoAvionics (wheels, battery, EPS, computer, frame), Spacemanic,
   Space Inventor (tracker, computer).
3. **News and secondary, 2026:** the Transporter rate (four pages), Rocket Lab averages, Starlink and SDA figures.
4. **Weak or conflicting:** broker per-U guides, the EnduroSat slides, search-summary prices.
5. **Before 2025, used only for the comparison:** satcatalog FY2021 to FY2023 averages, satsearch 2024-02-05 (12U XL), the
   NanoAvionics 2025-04 contract, ISS FY2022.
