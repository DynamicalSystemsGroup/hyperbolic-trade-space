"""Render the abstract page served at ``/paper/`` in ``abstract`` mode (WP65 specification, 3.3).

    uv run python scripts/paper_abstract.py [--out FILE] [--fallback-pin TAG --fallback-reason R]

The title and the abstract come from the YAML front matter of the first cell of
``paper/paper.ipynb``; the author, with the affiliation, from ``project.authors`` of
``paper/myst.yml`` (the front matter has no author field). The page is the template
``site/paper/abstract.html`` with those values filled in, escaped as text, and its public-link
metadata (``scripts/site_metadata.py``) in ``<head>``, the abstract's first sentence as the
description. The abstract is plain
text: a ``$``, a MyST role, a link, an HTML tag or a backtick in it fails the render, so an abstract
with markup is a deliberate change to this script. The fallback form, used by the composer when a
pinned paper cannot be served, adds one line before the abstract naming the pin and the reason.
Without ``--out`` the page is printed.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import site_metadata

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "paper" / "paper.ipynb"
MYST_CONFIG = ROOT / "paper" / "myst.yml"
TEMPLATE = ROOT / "site" / "paper" / "abstract.html"
PATH = "paper/"  # the page's address under the site's
FIELDS = ("title", "author", "fallback", "abstract")

# Markup the abstract may not carry: the page renders it as text, not as MyST.
MARKUP = {
    "math ($)": re.compile(r"\$"),
    "a MyST role": re.compile(r"\{[A-Za-z][\w:-]*\}`"),
    "a link": re.compile(r"\[[^\]]*\]\([^)]*\)|<https?://|https?://"),
    "an HTML tag": re.compile(r"</?[A-Za-z!][^>]*>"),
    "a backtick": re.compile(r"`"),
}
_SENTENCE_END = re.compile(r"(?<=[.!?])\s")


class AbstractMarkupError(ValueError):
    """The abstract carries markup the page would not render."""


def front_matter(notebook: Path = NOTEBOOK) -> dict:
    """The YAML front matter of the notebook's first cell."""
    cells = json.loads(Path(notebook).read_text(encoding="utf-8"))["cells"]
    source = "".join(cells[0]["source"])
    match = re.match(r"\s*---\n(.*?)\n---\s*(?:\n|$)", source, re.S)
    if not match:
        raise ValueError(f"{notebook}: the first cell holds no YAML front matter")
    data = yaml.safe_load(match.group(1))
    for field in ("title", "abstract"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{notebook}: the front matter has no {field}")
    return data


def authors(config: Path = MYST_CONFIG) -> str:
    """``Name, Affiliation`` for each of ``project.authors``, joined by semicolons."""
    project = yaml.safe_load(Path(config).read_text(encoding="utf-8"))["project"]
    names = []
    for author in project.get("authors") or []:
        affiliations = [a for a in author.get("affiliations") or [] if isinstance(a, str)]
        names.append(", ".join([author["name"], *affiliations]))
    if not names:
        raise ValueError(f"{config}: project.authors names no author")
    return "; ".join(names)


def check_plain(text: str) -> None:
    """Raise ``AbstractMarkupError`` naming the first kind of markup found in ``text``."""
    for name, pattern in MARKUP.items():
        found = pattern.search(text)
        if found:
            raise AbstractMarkupError(
                f"the abstract carries {name} ({found.group(0)!r}); the abstract page renders "
                "plain text only"
            )


def paragraphs(text: str) -> list[str]:
    """The abstract's paragraphs (separated by blank lines), each joined onto one line."""
    check_plain(text)
    blocks = re.split(r"\n\s*\n", text.strip())
    return [" ".join(block.split()) for block in blocks if block.strip()]


def first_sentence(text: str) -> str:
    """The first sentence of the abstract's first paragraph (the page's description)."""
    first = paragraphs(text)[0]
    return _SENTENCE_END.split(first, maxsplit=1)[0]


def fallback_line(pin: str, reason: str) -> str:
    """The line the fallback form adds before the abstract."""
    return (
        f'  <p class="fallback">The pin <code>{html.escape(pin)}</code> was not reachable when the '
        f"site was composed (<code>{html.escape(reason)}</code>); its abstract follows.</p>\n"
    )


def render(
    fallback: tuple[str, str] | None = None,
    notebook: Path = NOTEBOOK,
    config: Path = MYST_CONFIG,
    template: Path = TEMPLATE,
) -> str:
    """The abstract page; ``fallback=(pin, reason)`` gives the fallback form."""
    data = front_matter(notebook)
    values = {
        "title": html.escape(" ".join(data["title"].split())),
        "author": html.escape(authors(config)),
        "fallback": fallback_line(*fallback) if fallback else "",
        "abstract": "\n".join(
            f"  <p>{html.escape(p, quote=False)}</p>" for p in paragraphs(data["abstract"])
        ),
    }
    page = Path(template).read_text(encoding="utf-8")
    for field in FIELDS:
        page = page.replace("{{" + field + "}}", values[field])
    left = re.findall(r"\{\{\w+\}\}", page)
    if left:
        raise ValueError(f"{template}: unfilled fields {left}")
    return site_metadata.apply(page, PATH, description=first_sentence(data["abstract"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--out", help="write the page here (default: print it)")
    parser.add_argument("--fallback-pin", help="the pin that could not be served")
    parser.add_argument("--fallback-reason", help="why it could not be served")
    args = parser.parse_args(argv)
    if (args.fallback_pin is None) != (args.fallback_reason is None):
        parser.error("--fallback-pin and --fallback-reason go together")
    fallback = (args.fallback_pin, args.fallback_reason) if args.fallback_pin is not None else None
    try:
        page = render(fallback)
    except (OSError, ValueError, KeyError) as exc:
        print(f"paper_abstract: FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(page, encoding="utf-8")
        print(f"paper_abstract: wrote {args.out}")
    else:
        sys.stdout.write(page)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
