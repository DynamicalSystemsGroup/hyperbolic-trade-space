"""Shared helpers of the paper's generators: Markdown output and tables.

Every generator returns an :class:`Md`, a ``str`` that a notebook renders as Markdown, so the
tests read the same text the reader sees.
"""

from __future__ import annotations

import math

import paper_paths  # noqa: F401  (puts the repository on sys.path)

SCROLL_STYLE = "overflow-x:auto;max-width:100%"
LINK_STYLE = "color:inherit;text-decoration:underline"
"""A link in an output cell takes the text colour and is underlined, so it reads in both themes."""


def appendix_link(label: str, text: str) -> str:
    """A link from the paper's page to a subsection of the supporting material (``sub-d-11``).

    The generated sentences are output cells, which the site does not parse for cross-reference
    roles; the link is plain HTML to the target that the supporting page's heading carries.
    """
    return f'<a href="supporting-material/#{label}" target="_self" style="{LINK_STYLE}">{text}</a>'


class Md(str):
    """A string that Jupyter renders as Markdown."""

    def _repr_markdown_(self) -> str:
        return str(self)

    def _repr_html_(self) -> str:
        """The same text as HTML, because the static site shows a Markdown output as raw text."""
        from markdown_it import MarkdownIt

        html = MarkdownIt("commonmark").enable("table").render(str(self))
        # a wide table scrolls inside the column instead of widening the page on a phone
        return html.replace("<table>", f'<div style="{SCROLL_STYLE}"><table>').replace(
            "</table>", "</table></div>"
        )


class Scroll(str):
    """An HTML table in a container that scrolls sideways, so a wide table never overflows a page.

    The static site shows a pandas table at its natural width; on a phone the table is then wider
    than the column. The wrapper keeps the table inside its container and lets it scroll.
    """

    def _repr_html_(self) -> str:
        return f'<div style="{SCROLL_STYLE}">{self}</div>'

    def _repr_markdown_(self) -> str:
        return str(self)


def cell_text(value, floatfmt: str = ".4g") -> str:
    """One table cell as text: floats formatted, newlines and pipes made safe."""
    if isinstance(value, bool):
        text = str(value)
    elif isinstance(value, float):
        text = "nan" if math.isnan(value) else format(value, floatfmt)
    else:
        text = str(value)
    return " ".join(text.split()).replace("|", "\\|")


def md_table(headers, rows, floatfmt: str = ".4g") -> str:
    """A pipe table from headers and an iterable of row sequences."""
    out = ["| " + " | ".join(cell_text(h) for h in headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]  # fmt: skip
    for row in rows:
        out.append("| " + " | ".join(cell_text(c, floatfmt) for c in row) + " |")
    return "\n".join(out)


def frame_table(df, index: bool = False, floatfmt: str = ".4g") -> str:
    """A pipe table from a pandas DataFrame."""
    if index:
        df = df.reset_index()
    return md_table([str(c) for c in df.columns], df.itertuples(index=False, name=None), floatfmt)


def write_environment_reference() -> None:
    """Write the reference arrays that tests compare within tolerance off the environment of record.

    Run in the environment of record (``uv run python paper/paper_common.py``); the arrays are the
    planted table and the data of Figure 1, listed with their tolerances in
    ``environment_values.toml``.
    """
    import pathlib

    import generate_model
    import numpy as np
    from figures import figure1

    X, _ = generate_model.planted_table()
    arrays = {"planted_X": X}
    arrays.update({f"figure1_{k}": np.asarray(v) for k, v in figure1.figure1_data().items()})
    np.savez_compressed(pathlib.Path(__file__).with_name("environment_reference.npz"), **arrays)


if __name__ == "__main__":
    write_environment_reference()
