# WP60: amniote page, figure record

Page `docs/examples/amniote.md`, Figure 8 (after Figure 7 of `examples.md`; the docsite then carries eight unique figures, the budget). Images: `amniote-figure-light.png`, `amniote-figure-dark.png`, built by `scripts/build_figures.py` from the page's `{.runnable}` block (the cached archive through `run.py`'s loader, a K = 1 fit to longevity, earliness and litters per year, `plot_ternary`). Both images rendered and read; light and dark differ.

## Sentence test

The sentence a reader takes from the figure alone: longevity trades against earliness (the region's label), because the numbered star sits on the longevity-earliness side, far from the litters-per-year corner, inside the closed lines of equal value. Checked from the image alone: it holds. The caption completes it: three of the four metrics, litter size not drawn, the star is the term's exponent vector, no groups of species. After the coordinator's revision (`lines=True`) the label box no longer covers the star.

## Findings from looking

- The fit to three metrics has one term, so the triangle is one tinted region; with `lines=True` the star and its number show, clear of the label box. Alt text and caption name the star and the lines.
- The figure uses litters per year as the third metric, with litter size named in prose (the page's default); a different three would change the picture.
- Corner labels read in both schemes; the dark scheme's corner labels are paler than the light scheme's but legible.
- Ink is data: species as points, near-frontier ones larger, no decorative element.

## Register

C876 to C889, kind S, anchored to headings of the page, each backed by `examples/amniote/results.json` or `variants.json`.
