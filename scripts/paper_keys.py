"""Reference keys from the docsite into the paper (WP8b D-6), resolved at build time.

A docs page cites the paper with one syntax, ``[text](paper:key)``, where ``key`` is a label the
paper defines. The keys are read from the paper's own sources, the two notebooks, so there is no
second list: a MyST directive's ``:label:`` line and a ``(key)=`` target in a markdown cell. The
build turns each citation into a relative link to the paper page that carries the label, with the
label as the anchor, and fails on a key the paper does not define. A section moved inside the paper
keeps its key, so a link does not break; a key removed or renamed fails the docs build, not the
reader.

``mkdocs.yml`` lists this file under ``hooks``; MkDocs calls ``on_page_markdown``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "paper"
# The notebook that defines a key, and the route of the page the paper's build gives it
# (under the site root, as ``paper/`` and ``paper/supporting-material/``).
PAGES = {
    "paper.ipynb": "paper/",
    "supporting_material.ipynb": "paper/supporting-material/",
}
KEY_CITATION = re.compile(r"\[([^\]]+)\]\(paper:([A-Za-z0-9_-]+)\)")
_LABEL_LINE = re.compile(r"^\s*:label:\s*([A-Za-z0-9_-]+)\s*$", re.M)
_TARGET_LINE = re.compile(r"^\(([A-Za-z0-9_-]+)\)=\s*$", re.M)
_FENCE = re.compile(r"(```.*?```)", re.S)


class UnknownPaperKey(ValueError):
    """A docs page cites a key the paper does not define."""


def paper_keys(paper_dir: Path = PAPER_DIR) -> dict[str, str]:
    """Map every key the paper defines to the route of its page (``paper/`` or a sub-page)."""
    keys: dict[str, str] = {}
    for notebook, route in PAGES.items():
        cells = json.loads((Path(paper_dir) / notebook).read_text())["cells"]
        for cell in cells:
            if cell["cell_type"] != "markdown":
                continue
            source = "".join(cell["source"])
            for key in _LABEL_LINE.findall(source) + _TARGET_LINE.findall(source):
                if keys.get(key, route) != route:
                    raise ValueError(f"paper key {key!r} is defined in two pages")
                keys[key] = route
    return keys


def resolve(markdown: str, page_url: str, keys: dict[str, str] | None = None) -> str:
    """Replace each ``[text](paper:key)`` outside code fences with a link to the paper.

    ``page_url`` is the page's route under ``docs/`` (``""`` for the home page, else
    ``"user-guide/fitting/"``), which fixes how many levels up the site root is.
    """
    keys = paper_keys() if keys is None else keys
    up = "../" * (page_url.count("/") + 1)

    def link(match: re.Match) -> str:
        text, key = match.groups()
        if key not in keys:
            raise UnknownPaperKey(f"the paper defines no key {key!r} (cited as [{text}])")
        return f"[{text}]({up}{keys[key]}#{key})"

    parts = _FENCE.split(markdown)
    return "".join(p if i % 2 else KEY_CITATION.sub(link, p) for i, p in enumerate(parts))


def on_page_markdown(markdown, page, config, files):
    """MkDocs hook: resolve the paper keys of one page; an unknown key fails the build."""
    try:
        return resolve(markdown, page.url)
    except UnknownPaperKey as exc:
        from mkdocs.exceptions import PluginError

        raise PluginError(f"{page.file.src_path}: {exc}") from exc
