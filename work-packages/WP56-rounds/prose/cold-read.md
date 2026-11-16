# WP56 second unit: Sections 7 to 9 as rendered, and the unit's own cold read

Built with `cd paper && BASE_URL=/paper uv run --frozen myst build --html` (exit 0, no warning in the log) on the
branch `wp56p` after the final re-execution of `paper/paper.ipynb`, served at `http://127.0.0.1:8857/paper/`,
captured in the light theme at 1,280 px over the Chrome DevTools protocol in tiles of 1,500 px
(a scratch script adapted from the first unit's capture): `s7-1.png` to `s7-4.png`
(Section 7), `s8-1.png` to `s8-5.png` (Section 8), `s9-1.png` (Section 9). The read is the author's own, page by
page, as a reader at depth three (figure, caption and the prose around it); a fresh-context reader was not run.

## Section 7, Case construction

- Opens with the case in one sentence and the SysML v2 system model named, the CADRE precedent, then the problem
  as a displayed triple (maximize, with respect to, subject to); the display is numbered (26).
- The configuration sentence and Figure 4 agree (swap the wheel and the tracker, tune the panel, battery and gains;
  the fleet size not drawn).
- The requirements paragraph names the order and Table 2 shows it: four feasibility conditions, six after the fit,
  three met everywhere, and the derived coverage probability as the fourth MoE. Table 2 reads at a glance; the
  launch-budget row wraps to two lines at this width.
- Figure 5 (behavioural view) sits between Table 2 and the provenance paragraph; its caption is the first unit's and
  is long (about 230 words). Not changed (captions untouched unless a sentence of this unit made one wrong).
- Provenance in one paragraph: the oracle, the two regimes, Appendix C.6 for the commands, conditioning, and the
  temperature rule with Figure 6.
- The baseline configuration: its design variables, its two failing attributes and the two shares; it is named as
  Table 3's first row, where it returns.
- Fixed after the first capture: "carried through each step of the case" (it is carried from evaluation to the
  decision's table, not through the fit's figures) became "the first row of the decision's table".

## Section 8, Case analysis

- The generated nondominated sentence opens the section and the next sentence says what it leaves (nondominance
  keeps every design), so it opens the reading and stays.
- One term, Figure 7, two terms, Figures 8 and 9: the terms sentence now agrees with Figure 9's panels (8 and 7
  contend; total mass drawn on term 2 outside its contending set; peak slew power named by its largest exponent,
  not as the first row) and the elasticity sentence names the drawn cell (-2.8 per unit against -0.9 per percent),
  with $\alpha_i/\alpha_j$ set as math and Theorem 8, the pull-back, cited by its built number.
- "worth most on the term" is defined in one sentence before Figure 9 is read.
- The requirements after the fit, with their excluded counts, sit before the decision; the design-sets sentence
  follows them.
- "Three stakeholders" introduces Figure 10 with his sentences; the identity and the two-term refit are printed
  beside their call under the figure; the revised cost scaling is one sentence.
- The decision paragraph reads in order: the shortlist, the manufacturer's and operator's common pick and why, the
  sponsor's pick, the question, the design between them. Table 3 follows with five rows; the manufacturer's and the
  operator's rows are identical, which the caption says.
- Fixed after the first capture: a restatement flagged by the residual checker ("The sponsor picks ..." after the
  common pick) and four sentences over 35 words, split.

## Section 9, Discussion

- Four paragraphs: interpretation as human validation with the case's own check, what the case showed against
  Section 1's contribution, the three layers of Section 2, the limits in one passage at the end.
- The limits passage ends on trade-offs the sampling never exercised and white space, which leads into Section 10's
  "Searching the design space".
- Fixed after the first capture: "the stakeholders who hold them" (the SysML v2 model names two stakeholders, the
  decision three) became "with one stakeholder per objective of the decision".

## Left for the driver

- Figure 5's and Figure 8's captions are long (230 and 194 words) and are the first unit's.
- No fresh-context reader was run on this unit's pages; the driver's soft-confirm reads these captures.
