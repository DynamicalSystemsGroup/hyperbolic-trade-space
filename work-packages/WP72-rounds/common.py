"""WP72 helpers shared by the scripts: a Markdown table without extra dependencies."""

from __future__ import annotations

import numpy as np


def md_table(df, fmt="{:.3g}"):
    """A pipe table of a DataFrame; floats by ``fmt``, nan as blank."""

    def cell(v):
        if isinstance(v, float | np.floating):
            return "" if np.isnan(v) else fmt.format(v)
        return str(v)

    head = "| " + " | ".join(map(str, df.columns)) + " |"
    rule = "|" + "|".join("---" for _ in df.columns) + "|"
    body = ["| " + " | ".join(cell(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([head, rule, *body])
