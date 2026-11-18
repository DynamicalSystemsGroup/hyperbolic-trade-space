"""The paper's prior-art figure: three layers, each resting on the one below.

Trade studies and decision analysis sit on machine learning, which sits on convex optimization
and generalized geometric programs. The drawing is a plain SVG assembled from the string
constants below (``LAYERS``, the glosses and the colours), so the layer names and their glosses
are edited here and the file is written again.

Run ``uv run python paper/figures/prior_art_layers.py`` to write ``fig-prior-art-layers.svg``
beside it.
"""
# ruff: noqa: E501  (the SVG text is held as written, one element to a line)

from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "fig-prior-art-layers.svg"

WIDTH, HEIGHT = 760, 400
INK, SUB, EDGE = "#111827", "#374151", "#374151"
# (comment, top, fill, name, gloss), top layer first.
LAYERS = (
    (
        "top: the decision problem",
        30,
        "#f3f4f6",
        "Trade studies, decision analysis and multi-criterion optimization",
        "which objectives trade, and a choice that can be defended",
    ),
    (
        "middle",
        155,
        "#e5e7eb",
        "Machine learning: dimensionality reduction and kernel methods",
        "a recognized, rigorous and reproducible technique",
    ),
    (
        "bottom",
        280,
        "#d1d5db",
        "Convex optimization and generalized geometric programs",
        "convergence and performance of the underlying fit",
    ),
)

HEAD = f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="Helvetica, Arial, sans-serif">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{EDGE}"/>
    </marker>
  </defs>
"""
LAYER = """\
  <!-- {comment} -->
  <rect x="60" y="{top}" width="640" height="90" rx="10" fill="{fill}" stroke="{edge}" stroke-width="1.5"/>
  <text x="380" y="{y_name}" text-anchor="middle" font-size="19" font-weight="600" fill="{ink}">{name}</text>
  <text x="380" y="{y_gloss}" text-anchor="middle" font-size="14" fill="{sub}">{gloss}</text>
"""
ARROWS = """\
  <!-- arrows: each layer rests on the one below -->
  <line x1="380" y1="152" x2="380" y2="124" stroke="{edge}" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="380" y1="277" x2="380" y2="249" stroke="{edge}" stroke-width="1.5" marker-end="url(#arrow)"/>
</svg>
"""


def svg() -> str:
    """Return the figure as SVG text.

    Returns
    -------
    str
        The drawing, ending in a newline.
    """
    parts = [HEAD]
    for comment, top, fill, name, gloss in LAYERS:
        parts.append(
            LAYER.format(
                comment=comment,
                top=top,
                fill=fill,
                edge=EDGE,
                ink=INK,
                sub=SUB,
                name=name,
                gloss=gloss,
                y_name=top + 38,
                y_gloss=top + 66,
            )
        )
    parts.append(ARROWS.format(edge=EDGE))
    return "".join(parts)


def main() -> None:
    """Write ``fig-prior-art-layers.svg`` beside this file."""
    OUT.write_text(svg(), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
