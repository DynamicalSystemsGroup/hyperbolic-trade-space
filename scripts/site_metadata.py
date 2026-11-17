"""The metadata link handlers and search engines read off a page, from one source of values.

    uv run python scripts/site_metadata.py [--page PATH]

The values come from three files, none copied: ``site/metadata.toml`` (the name, the tagline, the
public address, the preview image and its size), ``pyproject.toml`` (the description, the version,
the licence, the repository address) and ``CITATION.cff`` (the author, the ORCID, the affiliation).
:func:`load` reads them once; :func:`apply` rewrites a page's ``<head>`` from them: a
``description``, a canonical address, the Open Graph set with the preview image, the Twitter card
and JSON-LD (``WebSite`` on every page; ``SoftwareSourceCode`` for the package on the root page).
A page that already carries one of these tags has it replaced, never doubled; a page's own
``<meta name="description">`` is kept as its description, the site's description is the fallback.

The composer (``scripts/assemble_site.py``) applies it to the root page, the history page and the
abstract page and writes ``robots.txt`` and the site's one ``sitemap.xml``; ``mkdocs.yml`` lists
this file under ``hooks`` so the docs build applies it to every docs page (``on_post_page``) and
takes the site's description from the same source (``on_config``). Without ``--page`` the script
prints the values; with it, the tags the page at that path (``""`` the root, ``docs/theory/``)
would carry.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VALUES_FILE = ROOT / "site" / "metadata.toml"
PYPROJECT = ROOT / "pyproject.toml"
CITATION = ROOT / "CITATION.cff"
ROBOTS_NAME, SITEMAP_NAME = "robots.txt", "sitemap.xml"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SPDX = "https://spdx.org/licenses/"

# The tags this module owns in a page's head: replaced on apply, never doubled.
_DESCRIPTION = re.compile(r'[ \t]*<meta name="description" content="([^"]*)"\s*/?>[ \t]*\n?')
_OWNED = re.compile(
    r'[ \t]*(?:<meta (?:property="og:|name="twitter:)[^>]*>|<link rel="canonical"[^>]*>|'
    r'<script type="application/ld\+json">.*?</script>)[ \t]*\n?',
    re.S,
)
_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
_LOC = re.compile(r"<loc>(.*?)</loc>", re.S)


def load(
    values_file: Path = VALUES_FILE, pyproject: Path = PYPROJECT, citation: Path = CITATION
) -> dict:
    """The site's values from their three sources, as one flat mapping.

    Keys: ``name``, ``tagline``, ``url``, ``description``, ``version``, ``license``,
    ``repository``, ``author`` (``name``, ``orcid``, ``affiliation``), ``image``,
    ``image_url``, ``image_width``, ``image_height``.
    """
    values = tomllib.loads(Path(values_file).read_text(encoding="utf-8"))
    if values.get("schema") != 1:
        raise ValueError(f"{values_file}: schema must be 1")
    for key in ("name", "tagline", "url", "image", "image_width", "image_height"):
        if not values.get(key):
            raise ValueError(f"{values_file}: {key} is missing or empty")
    if not values["url"].endswith("/"):
        raise ValueError(f"{values_file}: url ends with a slash")
    project = tomllib.loads(Path(pyproject).read_text(encoding="utf-8"))["project"]
    cff = yaml.safe_load(Path(citation).read_text(encoding="utf-8"))
    first = cff["authors"][0]
    author = {
        "name": f"{first['given-names']} {first['family-names']}",
        "orcid": first["orcid"],
        "affiliation": first.get("affiliation", ""),
    }
    return {
        "name": values["name"],
        "tagline": values["tagline"],
        "url": values["url"],
        "description": " ".join(project["description"].split()),
        "version": project["version"],
        "license": cff["license"],
        "repository": project["urls"]["Repository"],
        "author": author,
        "image": values["image"],
        "image_url": values["url"] + values["image"],
        "image_width": int(values["image_width"]),
        "image_height": int(values["image_height"]),
    }


def _person(values: dict) -> dict:
    author = values["author"]
    person = {"@type": "Person", "@id": author["orcid"], "name": author["name"]}
    if author["affiliation"]:
        person["affiliation"] = {"@type": "Organization", "name": author["affiliation"]}
    return person


def json_ld(path: str, values: dict | None = None) -> dict:
    """The structured data of the page at ``path``: ``WebSite`` on every page, and on the root
    page (``path == ""``) ``SoftwareSourceCode`` for the package as well."""
    values = values or load()
    website = {
        "@type": "WebSite",
        "@id": values["url"] + "#website",
        "name": values["name"],
        "url": values["url"],
        "description": values["description"],
        "author": _person(values),
    }
    graph = [website]
    if path == "":
        graph.insert(
            0,
            {
                "@type": "SoftwareSourceCode",
                "@id": values["url"] + "#software",
                "name": values["name"],
                "description": values["description"],
                "url": values["url"],
                "codeRepository": values["repository"],
                "license": SPDX + values["license"],
                "version": values["version"],
                "programmingLanguage": "Python",
                "author": _person(values),
            },
        )
    return {"@context": "https://schema.org", "@graph": graph}


def head(path: str, title: str, description: str | None = None, values: dict | None = None) -> str:
    """The tags for the page at ``path`` (relative to the site root, ``""`` for the root page),
    one per line, ending in a newline."""
    values = values or load()
    description = " ".join((description or values["description"]).split())
    url = values["url"] + path
    pairs = [
        ("name", "description", description),
        ("property", "og:type", "website"),
        ("property", "og:site_name", values["name"]),
        ("property", "og:url", url),
        ("property", "og:title", title),
        ("property", "og:description", description),
        ("property", "og:image", values["image_url"]),
        ("property", "og:image:width", str(values["image_width"])),
        ("property", "og:image:height", str(values["image_height"])),
        ("name", "twitter:card", "summary_large_image"),
        ("name", "twitter:title", title),
        ("name", "twitter:description", description),
        ("name", "twitter:image", values["image_url"]),
    ]
    lines = [f'<meta {attr}="{key}" content="{html.escape(value)}">' for attr, key, value in pairs]
    lines.insert(1, f'<link rel="canonical" href="{html.escape(url)}">')
    data = json.dumps(json_ld(path, values), indent=2, ensure_ascii=False).replace("</", "<\\/")
    lines.append(f'<script type="application/ld+json">\n{data}\n</script>')
    return "\n".join(lines) + "\n"


def apply(page: str, path: str, description: str | None = None, values: dict | None = None) -> str:
    """``page`` with its ``<head>`` carrying the tags of :func:`head` directly after ``<title>``.

    The page's own ``<meta name="description">`` (when ``description`` is not given) is its
    description and is moved into the block; any Open Graph, Twitter, canonical or JSON-LD tag
    already in the head is replaced.
    """
    end = page.find("</head>")
    if end < 0:
        raise ValueError("the page has no </head>")
    top, rest = page[:end], page[end:]
    found = _DESCRIPTION.search(top)
    if description is None and found:
        description = html.unescape(found.group(1))
    top = _OWNED.sub("", _DESCRIPTION.sub("", top))
    title = _TITLE.search(top)
    if not title:
        raise ValueError("the page has no <title>")
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).split())
    block = head(path, text, description, values)
    at = title.end()
    return top[:at] + "\n" + block + top[at:].lstrip("\n") + rest


# --- robots.txt and the sitemap ---------------------------------------------------------------


def robots_txt(values: dict | None = None) -> str:
    values = values or load()
    return f"User-agent: *\nAllow: /\n\nSitemap: {values['url']}{SITEMAP_NAME}\n"


def page_paths(site_dir: Path, docs_dir: str = "docs", values: dict | None = None) -> list[str]:
    """The site's page paths from the composed tree: ``""`` for ``index.html``, ``dir/`` for a
    directory's ``index.html``, else the file's path; the docs' pages from the sitemap MkDocs
    wrote under ``docs/``."""
    site_dir = Path(site_dir)
    values = values or load()
    paths = set()
    for page in site_dir.rglob("*.html"):
        rel = page.relative_to(site_dir)
        if rel.parts[0] == docs_dir:
            continue
        if rel.name == "index.html":
            parent = rel.parent.as_posix()
            paths.add("" if parent == "." else parent + "/")
        else:
            paths.add(rel.as_posix())
    docs_sitemap = site_dir / docs_dir / SITEMAP_NAME
    if docs_sitemap.is_file():
        for address in _LOC.findall(docs_sitemap.read_text(encoding="utf-8")):
            address = html.unescape(address.strip())
            if address.startswith(values["url"]):
                paths.add(address.removeprefix(values["url"]))
    return sorted(paths)


def sitemap_xml(paths: list[str], values: dict | None = None) -> str:
    values = values or load()
    urls = "".join(
        f"  <url><loc>{html.escape(values['url'] + p)}</loc></url>\n" for p in sorted(set(paths))
    )
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="{SITEMAP_NS}">\n{urls}</urlset>\n'
    )


def write_robots_and_sitemap(site_dir: Path) -> tuple[Path, Path]:
    """Write ``robots.txt`` and the whole site's ``sitemap.xml`` into the composed tree."""
    site_dir = Path(site_dir)
    values = load()
    robots = site_dir / ROBOTS_NAME
    sitemap = site_dir / SITEMAP_NAME
    robots.write_text(robots_txt(values), encoding="utf-8")
    sitemap.write_text(sitemap_xml(page_paths(site_dir, values=values), values), encoding="utf-8")
    return robots, sitemap


# --- the MkDocs hooks -------------------------------------------------------------------------


def on_config(config):
    """MkDocs hook: the docs' description is the site's; the docs' address is under the site's."""
    values = load()
    config.site_description = values["description"]
    if config.site_url != values["url"] + "docs/":
        from mkdocs.exceptions import ConfigurationError

        raise ConfigurationError(
            f"site_url is {config.site_url!r}; {VALUES_FILE.name} names {values['url']}docs/"
        )
    return config


def on_post_page(output, page, config):
    """MkDocs hook: every docs page carries the tags, at its address under ``docs/``."""
    return apply(output, "docs/" + page.url)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--page", help="print the tags for the page at this path instead")
    args = parser.parse_args(argv)
    values = load()
    if args.page is None:
        for key, value in values.items():
            print(f"{key}: {value}")
        return 0
    sys.stdout.write(head(args.page, values["name"], values=values))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
