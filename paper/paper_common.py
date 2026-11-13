"""Shared helpers of the paper's generators: Markdown output and tables.

Every generator returns an :class:`Md`, a ``str`` that a notebook renders as Markdown, so the
tests read the same text the reader sees.
"""

# ruff: noqa: RUF001  (the TeX tables map names to the Greek and mathematical characters themselves)
from __future__ import annotations

import math
import re

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


def thousands(x) -> str:
    """A count with the thousands separator in digits; in a text, every whole number of four or
    more digits that is not part of a decimal or a longer token.

    >>> thousands(2134), thousands(706), thousands("145 to 2200")
    ('2,134', '706', '145 to 2,200')
    """
    if isinstance(x, str):
        return re.sub(r"(?<![\w.,])\d{4,}(?![\w.]|,\d)", lambda m: f"{int(m.group()):,}", x)
    return f"{int(x):,}"


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


# ---- inline mathematics for an HTML output ------------------------------------------------------
# The static site shows a notebook's HTML output as given: it typesets no ``$...$`` in it. A table
# that carries mathematics therefore writes each span as MathML, which the browser typesets itself.

_TEX_GREEK = {
    "tau": "τ", "gamma": "γ", "beta": "β", "sigma": "σ", "kappa": "κ",
    "varepsilon": "ε", "epsilon": "ϵ",
}  # fmt: skip
_TEX_UPRIGHT = {"Phi": "Φ", "Sigma": "Σ", "infty": "∞", "top": "⊤"}
_TEX_FUNCTION = ("log", "max", "min")
_TEX_OPERATOR = {
    "times": "×", "cdot": "⋅", "le": "≤", "ge": "≥", "ne": "≠", "in": "∈", "sum": "∑",
    "lVert": "‖", "rVert": "‖", "lvert": "|", "rvert": "|", "|": "‖",
}  # fmt: skip
_TEX_DOUBLE_STRUCK = {"R": "ℝ"}
_TEX_TOKEN = re.compile(r"\s*(\\[A-Za-z]+|\\.|\d+(?:\.\d+)?|.)", re.S)


def _mx(tag: str, text: str = "", **attrs) -> str:
    inner = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f"<{tag}{extra}>{inner}</{tag}>"


class _TexParser:
    """A reader of the small subset of TeX that the paper's tables use, writing MathML."""

    def __init__(self, tex: str):
        self.tokens = _TEX_TOKEN.findall(tex.strip())
        self.i = 0
        self.function = False

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def sequence(self, end: str | None = None) -> str:
        out = []
        while self.peek() is not None and self.peek() != end:
            out.append(self.scripted())
        if end is not None and self.take() != end:
            raise ValueError(f"unclosed group in TeX: {end!r} missing")
        return "".join(out)

    def argument(self) -> str:
        """One argument: a braced group, or the next single atom."""
        tok = self.take()
        if tok is None:
            raise ValueError("missing TeX argument")
        if tok == "{":
            return "<mrow>" + self.sequence("}") + "</mrow>"
        self.i -= 1
        return self.atom()

    def scripted(self) -> str:
        self.function = False
        base = self.atom()
        function = self.function
        self.function = False
        sub = sup = None
        while self.peek() in ("_", "^"):
            kind = self.take()
            arg = self.argument()
            if kind == "_":
                sub = arg
            else:
                sup = arg
        if sub and sup:
            base = f"<msubsup>{base}{sub}{sup}</msubsup>"
        elif sub:
            base = f"<msub>{base}{sub}</msub>"
        elif sup:
            base = f"<msup>{base}{sup}</msup>"
        # the invisible function application, so that "log m" and "log 0" are spaced as functions
        return base + _mx("mo", "\u2061") if function else base

    def literal(self) -> str:
        """The characters of a braced group, as plain text (for ``\\text`` and ``\\mathrm``)."""
        if self.take() != "{":
            raise ValueError("TeX: a braced argument was expected")
        chars = []
        while self.peek() not in ("}", None):
            chars.append(self.take())
        self.take()
        return "".join(chars)

    def atom(self) -> str:
        tok = self.take()
        if tok is None:
            raise ValueError("TeX ended where an atom was expected")
        if tok == "{":
            return "<mrow>" + self.sequence("}") + "</mrow>"
        if tok[0].isdigit():
            return _mx("mn", tok)
        if tok.isalpha() and len(tok) == 1:
            return _mx("mi", tok)
        if tok == "-":
            return _mx("mo", "−")
        if tok == "*":
            return _mx("mo", "∗")
        if tok == ":" and self.peek() == "=":
            self.take()
            return _mx("mo", ":=")
        if tok in "=+/<>()[],:.|":
            return _mx("mo", tok)
        if tok[0] != "\\":
            raise ValueError(f"TeX: unsupported character {tok!r}")
        name = tok[1:]
        if name == ",":
            return '<mspace width="0.17em"></mspace>'
        if name in _TEX_GREEK:
            return _mx("mi", _TEX_GREEK[name])
        if name in _TEX_UPRIGHT:
            return _mx("mi", _TEX_UPRIGHT[name], mathvariant="normal")
        if name in _TEX_FUNCTION:
            self.function = True
            return _mx("mi", name, mathvariant="normal")
        if name in _TEX_OPERATOR:
            return _mx("mo", _TEX_OPERATOR[name])
        if name == "text":
            return _mx("mtext", self.literal())
        if name == "mathrm":
            return _mx("mi", self.literal(), mathvariant="normal")
        if name == "mathbb":
            return _mx("mi", "".join(_TEX_DOUBLE_STRUCK[c] for c in self.literal()))
        if name == "tfrac":
            return f"<mfrac>{self.argument()}{self.argument()}</mfrac>"
        if name == "bar":
            return f'<mover accent="true">{self.argument()}{_mx("mo", "‾")}</mover>'
        if name == "overline":
            return f"<mover>{self.argument()}{_mx('mo', '‾')}</mover>"
        raise ValueError(f"TeX: unsupported command {tok!r}")


def tex_to_mathml(tex: str) -> str:
    r"""One inline TeX span as MathML, for the small subset of TeX that the tables use.

    >>> tex_to_mathml(r"w_j>0")
    '<math><msub><mi>w</mi><mi>j</mi></msub><mo>&gt;</mo><mn>0</mn></math>'
    >>> tex_to_mathml(r"\tau=\infty")
    '<math><mi>τ</mi><mo>=</mo><mi mathvariant="normal">∞</mi></math>'
    """
    return "<math>" + _TexParser(tex).sequence() + "</math>"


class MdMath(Md):
    """An :class:`Md` whose HTML writes each ``$...$`` span of ``raw`` as MathML.

    The string is the Markdown a notebook viewer typesets itself (escaped for the Markdown step of a
    page); ``raw`` is the same table with each span as written, which the page's HTML is made from.
    """

    raw: str

    def __new__(cls, text: str, raw: str):
        self = super().__new__(cls, text)
        self.raw = raw
        return self

    def _repr_html_(self) -> str:
        spans: list[str] = []

        def keep(m: re.Match) -> str:
            spans.append(m.group(1))
            return f"MATHSPAN{len(spans) - 1}X"

        masked = re.sub(r"\$([^$]+)\$", keep, self.raw)
        page = Md(masked)._repr_html_()
        return re.sub(r"MATHSPAN(\d+)X", lambda m: tex_to_mathml(spans[int(m.group(1))]), page)
