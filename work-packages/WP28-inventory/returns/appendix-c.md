# appendix-c

## Q1
It follows the cubesat model from its configuration space through evaluation, feasibility and conditioning to the table of metrics, and names the datasets and the planted example, so a reader can judge whether the case is a fair test and build a comparable one.

## Q2
Main-results item 7 (on a cubesat model coupling power, mass and attitude control...), and the abstract's last sentence ("On a cubesat model coupling power, mass and attitude control, one term blends..."). It also supplies the table the Contribution paragraph counts (706 feasible of 1000).

## Q3
Verdict: advances. The story rests on the cubesat case, and a reader who wants to judge it needs how the metrics were made from configurations; the main text keeps this to a short section and points here five times (C.1, C.4, C.7 twice, and the general sentence). No other unit that I can see from the list carries the construction. The one weak part is the associations table, below.

## Q4
Not "repeats" as a whole. (For the associations table alone, see Q7.)

## Q7
- tab-C-configuration_space: points from main text: yes (C.1). Reader looks for it: yes, the design-variable ranges and covariate levels. advances (ranges the model view does not draw).
- tab-C-evaluation: points: no (only a general sentence on the evaluation). Reader looks for it: yes, the eight attributes, their units and direction, and the scenario constants. advances (the full version of "eight attributes").
- tab-C-attribute_sources: points: no. Reader looks for it: yes, which file produces each attribute and whether it is measured or computed (the black-box point). advances.
- tab-C-feasibility: points: no. Reader looks for it: yes, how 1000 sampled designs became 706 (and 780 for stock). advances.
- tab-C-conditioning: points: yes (Section 5, C.4). Reader looks for it: yes, orientation, raw ranges and log-spread for each attribute. advances.
- tab-C-metric_table: points: no. Reader looks for it: partly, the formula for m_j (carried in the text above the table); the five sample rows only show the shape. does not advance (the rows; the repository holds the data and the formula is in the prose).
- tab-C-metric_associations: points: no from C (Section 9 points to D.3 for the same Spearman values). Reader looks for it: yes, for the strongest pair and the 0.99 test. repeats appendix-d (D.3, which the main text cites for these Spearman values; I have not read D.3, so this is from the pointer). The 28-pair listing may be its only full home, in which case it advances.
- tab-C-datasets: points: no directly ("names each dataset" is general). Reader looks for it: yes, file, command, counts and hashes to rebuild the data. advances (it may overlap Appendix F's commands and rows, which I have not read).
- tab-C-planted_example: points: yes (C.7, twice). Reader looks for it: yes, the generator arguments and planted exponents. advances (its arguments are also in the planted row of the datasets table, but the exponent matrix reads clearly here).

## Q9
- "The association of every pair of traded metrics ... is the step that would find two metrics the data cannot tell apart": placed it in the end, but it sits in the middle of the metric-table section and the link to the formula above it is unclear.
- "cubesat-stock ... Kp 0.03011 ... 0.999" against declared 0.2 to 2: the stock regime's gain range is outside the declared range and the appendix does not say why here.
- "peak slew power ... m min 0.2554" equals design 0's value in the sample rows: no problem, but the repeated values (2.191, 3.591, 1.998) in that column look like ties and are not explained.
