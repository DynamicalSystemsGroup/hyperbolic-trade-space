# WP42 figure review: the term's tension matrix, the redraw of Figure 7

Images (committed with the generating code, `figure.py`): `images/before.png` (Figure 7 on dev, the association among
each term's near-frontier designs), `images/after-replace.png` (the tension matrix per term, in place of it),
`images/after-compact.png` (the same cut to the metrics that carry an exponent), `images/after-beside.png` (both, side
by side), `images/after-replace-dark.png`. The numbers are the K = 2 fit's, primary regime, at each term's balanced point.

## The recipe (written before the read)

- **Question.** Which metrics trade against which on each term, at what local rate, and which pairs the term does not
  speak about.
- **Intended takeaway.** Each term names eight of the thirteen metrics; between two of them a cell says how much the
  column metric gives way when the row metric rises by one unit along the term (always a loss, so every number is
  negative); the cells for a metric the term does not carry are empty or zero, not guessed.
- **Sentence (test 2).** "On each term eight of the thirteen metrics carry an exponent; for any two of them the matrix
  says how much one falls when the other rises by a unit along the term, and the other five metrics are left out."

## The readers' words (final round, `WP11-final/reports/`), on the panel it replaces

- F02, item 13: "I expected an n-lemma to be at most 3 as in Figure 1. Here a term has eight metrics in contention, which
  is not a dilemma or trilemma in the plain sense. I could not tell how to read "8-lemma"".
- F07, item 11: "The matrix shows 13 rows with only 8 black, and the caption says "an outlined metric can be grey and a
  black one not outlined". In term 1, total mass and control effort are grey and not outlined. In term 2, "settling
  time w=0.11" is black and outlined. I could follow the logic after reading it twice."
- F13, item 12: "That is a double encoding I had to read twice."
- F02, item 14: "the white-on-black outlined diagonal cells and the grey labels are hard to tell apart from the
  correlations."
- F05, item 9: "Selecting designs near a surface w·u = β induces negative correlation among the metrics even for independent
  metrics (selection on a sum). I could not tell whether the "tension" reading separates that effect."
- F05 item 8 and F08 item h (collinear metrics: the exponent split among them cannot be read separately).
- The triage names the three-cell finding: Figure 7's panel titles ("exact-maximum support") and the caption's "contending
  set" name one object, one name (`WP11-final/triage/wave-6.md`, item 153).

What the redraw does with them: one encoding only (a metric carries an exponent or not, read from the fit's exponents),
so the outline, the grey-versus-black rule and the "n-lemma" title are gone from this panel; the selection effect does
not arise because no cell is a correlation of the data; the collinear groups show as they are in the fit (only available
power carries an exponent of the power group, so the others are empty columns, with no claim about which is the cause).

## The five tests, as the author judges them (the cold read, test 1, is not done: see the brief below)

1. **Cold read.** Not run in this scope (no sub-agents). Brief below; the PM runs it on `after-replace.png` and
   `after-compact.png`, image alone, then the caption.
2. **Sentence test.** The sentence above carries the structure (which cells are empty and why) but not the magnitudes;
   the figure earns its place by the magnitudes (which pairs are steep and which shallow, mirrored across the diagonal).
   Honest limit: the cell is -(w_i/w_j)(m*_j/m*_i), so much of the picture is the exponent ratio already in the
   elasticity sentence; the figure adds the units' scale (m_j/m_i at the balanced point) and the pairs side by side.
3. **Ink is data.** In `after-replace.png` a panel has 169 cells: 56 carry a number (33 %), 40 are zero rows (24 %), 60
   are empty (36 %), 13 are the diagonal. The zero rows repeat what the grey labels say (w = 0.00); `after-compact.png`
   drops them and the empty columns and names the five absent metrics in one line, which is the negative edit the
   brief asks to consider (the cost: the reader no longer sees the empty and zero cells that the definition names).
4. **Legible where it is read.** Type 9 pt and larger at 8 in, light and dark (`after-replace-dark.png` looked at); cell
   numbers have two significant digits; "-0.06" cells in the dark brown are the tightest. Not checked in a browser
   page (there is no page in this scope).
5. **Shows, does not show, good for.** Shows: for each term, the local rate at which one metric gives way for another
   at the term's balanced point, and which metrics the term leaves out. Does not show: designs, the exponents' uncertainty,
   causation, or the rate at any other point of the term (the elasticity is constant on the term, the tension changes
   with the ratio m_j/m_i). Good for: naming the pairs a term trades steeply and reading one cell as a rate.

Choices a reader would not guess, stated: the colour is the size of the tension on a log scale centred on 1 (orange side
below 1, teal above), because every drawn cell is negative, so the default's signed scale would show one colour family and
nothing else; the sign is in the printed number. The reciprocal cell across the diagonal is the mirror in log scale
(0.92 and 1.1). Metrics are sorted by the term's exponent, so the figure does not share Figure 7's row order.

## Brief for the cold reader (Haiku, fresh context)

Give the image alone (`images/after-replace.png`, then `images/after-compact.png` to a second reader): "This is a figure
from a paper on trade studies of a small satellite. In one sentence say what it shows and what you take from it; then say
what an empty cell, a cell with 0 and a coloured cell each mean, and which two metrics trade most steeply on term 1."
Then the caption (draft: "The tension matrix of each term of the K = 2 fit: each cell is how much the column metric changes
when the row metric rises by one unit along the term, at the term's balanced point, in the conditioned metrics. Empty:
the column metric carries no exponent on this term. 0: the row metric carries none. The colour is the size on a log
scale; every drawn cell is negative.") and ask whether it changed the reading. Record whether the reader takes the
numbers as data or as the model, and whether the "unit" is understood.
