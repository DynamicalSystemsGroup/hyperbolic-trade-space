"""Reference keys from the docsite into the paper (WP8b D-6; WP65 specification, section 4).

A docs page cites the paper with one syntax, ``[text](paper:key)``, where ``key`` is a label the
paper defines. The keys come from one file, the committed manifest ``paper/paper-keys.json``,
written by ``paper/build_keys.py`` on the ``paper`` branch and carried to ``dev`` by the merge; the
docs build reads no notebook. The link a citation becomes depends on what ``/paper/`` holds (the
slot): in a pinned slot the paper page that carries the label, with the label as the anchor; in
``abstract`` mode (and in the composer's fallback) the abstract page, ``/paper/``, with no anchor.
A key the manifest does not hold fails the docs build in both slots.

``mkdocs.yml`` lists this file under ``hooks``; MkDocs calls ``on_page_markdown``. The composer
sets ``HTS_PAPER_SLOT`` (``pin`` or ``abstract``); a bare ``mkdocs build`` reads the slot from
``paper/mode.toml``.
"""

from __future__ import annotations

import json
import os
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "paper" / "paper-keys.json"
MODE_FILE = ROOT / "paper" / "mode.toml"
SLOT_VARIABLE = "HTS_PAPER_SLOT"
SLOTS = ("pin", "abstract")
ROUTES = ("paper/", "paper/supporting-material/")
KEY_CITATION = re.compile(r"\[([^\]]+)\]\(paper:([A-Za-z0-9_-]+)\)")
_KEY = re.compile(r"^[A-Za-z0-9_-]+$")
_FENCE = re.compile(r"(```.*?```)", re.S)


class UnknownPaperKey(ValueError):
    """A docs page cites a key the manifest does not hold."""


def canonical(keys: dict[str, str]) -> str:
    """The manifest's bytes for ``keys``: schema 1, keys sorted, two-space indent, one newline."""
    return json.dumps({"schema": 1, "keys": dict(sorted(keys.items()))}, indent=2) + "\n"


def load_manifest(path: Path = MANIFEST) -> dict[str, str]:
    """Map every key of the manifest to the route of its page; ``ValueError`` on a broken rule."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: not JSON ({exc})") from exc
    if not isinstance(data, dict) or set(data) != {"schema", "keys"}:
        raise ValueError(f"{path}: the manifest holds exactly 'schema' and 'keys'")
    if data["schema"] != 1:
        raise ValueError(f"{path}: schema must be 1, got {data['schema']!r}")
    keys = data["keys"]
    if not isinstance(keys, dict) or not keys:
        raise ValueError(f"{path}: 'keys' must be a non-empty object")
    for key, route in keys.items():
        if not _KEY.match(key):
            raise ValueError(f"{path}: key {key!r} does not match {_KEY.pattern}")
        if route not in ROUTES:
            raise ValueError(f"{path}: key {key!r} has route {route!r}, not one of {ROUTES}")
    if text != canonical(keys):
        raise ValueError(
            f"{path}: not in canonical form (keys sorted, two-space indent, one trailing newline)"
        )
    return dict(keys)


def slot(mode_file: Path = MODE_FILE) -> str:
    """``HTS_PAPER_SLOT`` when set; else ``abstract`` when the mode file says so, else ``pin``."""
    value = os.environ.get(SLOT_VARIABLE)
    if value:
        if value not in SLOTS:
            raise ValueError(f"{SLOT_VARIABLE} must be one of {SLOTS}, got {value!r}")
        return value
    mode = tomllib.loads(Path(mode_file).read_text(encoding="utf-8")).get("mode")
    return "abstract" if mode == "abstract" else "pin"


_read_slot = slot  # ``resolve`` takes a parameter of the same name


def resolve(
    markdown: str, page_url: str, keys: dict[str, str] | None = None, slot: str | None = None
) -> str:
    """Replace each ``[text](paper:key)`` outside code fences with a link into ``/paper/``.

    ``page_url`` is the page's route under ``docs/`` (``""`` for the home page, else
    ``"user-guide/fitting/"``), which fixes how many levels up the site root is. ``slot`` ``pin``
    links the label's anchor on its page; ``abstract`` links ``paper/`` with no anchor.
    """
    keys = load_manifest() if keys is None else keys
    slot = _read_slot() if slot is None else slot
    if slot not in SLOTS:
        raise ValueError(f"slot must be one of {SLOTS}, got {slot!r}")
    up = "../" * (page_url.count("/") + 1)

    def link(match: re.Match) -> str:
        text, key = match.groups()
        if key not in keys:
            raise UnknownPaperKey(f"the paper manifest holds no key {key!r} (cited as [{text}])")
        if slot == "abstract":
            return f"[{text}]({up}paper/)"
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
