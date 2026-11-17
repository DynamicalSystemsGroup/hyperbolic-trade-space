"""The public-link metadata of the staged site (WP80): one source of values; description,
canonical address, Open Graph, Twitter card and JSON-LD on the root page, the history page, the
abstract page and every docs page; the preview image; ``robots.txt`` and the sitemap. The site is
composed once into a temporary directory (the abstract slot, offline) and served on 127.0.0.1 for
the address checks."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import tomllib
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import paper_abstract  # noqa: E402
import site_metadata  # noqa: E402
import stage_site  # noqa: E402

PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
CITATION = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
CONTRACT = tomllib.loads(
    (ROOT / "work-packages" / "interface-contract.toml").read_text(encoding="utf-8")
)
MKDOCS = yaml.safe_load(
    re.sub(r"!!python/name:\S+", "", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
)
VALUES = site_metadata.load()
PUBLIC = VALUES["url"]
HAVE_MKDOCS = all(
    importlib.util.find_spec(m) is not None
    for m in ("mkdocs", "material", "mkdocstrings", "mkdocs_bibtex")
)
ROOT_PAGES = ("index.html", "history.html", "paper/index.html")
DOCS_PAGES = ("docs/index.html", "docs/getting-started/index.html", "docs/theory/index.html")
OG = ("og:title", "og:description", "og:url", "og:image", "og:image:width", "og:image:height",
      "og:type", "og:site_name")  # fmt: skip
TWITTER = ("twitter:card", "twitter:title", "twitter:description", "twitter:image")


# --- the staged site ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def assembled(tmp_path_factory) -> Path:
    """The composed site (the abstract slot); slow and in the ``site`` group by its name."""
    if not HAVE_MKDOCS:
        pytest.skip("the docs dependency group is not installed (mkdocs not importable)")
    out = tmp_path_factory.mktemp("site")
    generated = tmp_path_factory.mktemp("generated")
    stage_site.stage(out, slot="abstract", generated_dir=generated)
    return out


@pytest.fixture(scope="module")
def served(assembled):
    """The staged site on 127.0.0.1; yields the base address."""
    server = stage_site.serve_in_thread(assembled)
    yield f"http://{stage_site.HOST}:{server.server_address[1]}"
    server.shutdown()
    server.server_close()


class _Head(HTMLParser):
    """The head's tags: ``meta`` by name or property, ``link`` by rel, the title, the JSON-LD."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, list[str]] = {}
        self.links: dict[str, list[str]] = {}
        self.title = ""
        self.json_ld: list[str] = []
        self._in = None
        self._in_head = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "head":
            self._in_head = True
        if not self._in_head:
            return
        if tag == "meta":
            key = d.get("name") or d.get("property")
            if key:
                self.meta.setdefault(key, []).append(d.get("content", ""))
        if tag == "link" and d.get("rel"):
            self.links.setdefault(d["rel"], []).append(d.get("href", ""))
        if tag == "title":
            self._in = "title"
        if tag == "script" and d.get("type") == "application/ld+json":
            self._in = "ld"
            self.json_ld.append("")

    def handle_endtag(self, tag):
        if tag == "head":
            self._in_head = False
        if tag in ("title", "script"):
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "ld":
            self.json_ld[-1] += data


def _head(path: Path) -> _Head:
    parser = _Head()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def _one(head: _Head, key: str) -> str:
    values = head.meta.get(key, [])
    assert len(values) == 1, f"{key}: {values}"
    return values[0]


def _exists(site: Path, address: str) -> bool:
    """The address is under the public address and its path is a file of the staged tree."""
    if not address.startswith(PUBLIC):
        return False
    rel = address.removeprefix(PUBLIC).split("#", 1)[0]
    target = site / rel
    if rel == "" or rel.endswith("/"):
        return (target / "index.html").is_file()
    return target.is_file()


# --- one source of values ----------------------------------------------------------------------


def test_values_agree_with_the_contract_pyproject_and_the_citation_file():
    """R-2: the address is the contract's and pyproject's home page and the citation file's; the
    description is pyproject's and equals the citation file's abstract; the author, ORCID and
    licence are the citation file's; the version is pyproject's."""
    assert PUBLIC == CONTRACT["build"]["public_url"] == PYPROJECT["urls"]["Homepage"]
    assert CITATION["url"] == PUBLIC
    assert VALUES["description"] == " ".join(PYPROJECT["description"].split())
    assert VALUES["description"] == " ".join(CITATION["abstract"].split())
    assert VALUES["version"] == PYPROJECT["version"] == str(CITATION["version"])
    assert VALUES["license"] == CITATION["license"] == PYPROJECT["license"]
    first = CITATION["authors"][0]
    assert VALUES["author"]["name"] == f"{first['given-names']} {first['family-names']}"
    assert VALUES["author"]["orcid"] == first["orcid"]
    assert VALUES["author"]["orcid"].startswith("https://orcid.org/")
    assert VALUES["repository"] == CITATION["repository-code"] == PYPROJECT["urls"]["Repository"]
    assert VALUES["name"] == PYPROJECT["name"] == MKDOCS["site_name"] == CITATION["title"]
    assert (VALUES["image_width"], VALUES["image_height"]) == (1200, 630)


def test_mkdocs_reads_the_description_and_the_metadata_from_the_hook():
    assert "site_description" not in MKDOCS, "the description has one source"
    assert "scripts/site_metadata.py" in MKDOCS["hooks"]
    assert MKDOCS["site_url"] == PUBLIC + "docs/"


def test_tracked_pages_hold_no_copy_of_the_metadata():
    """The composer writes the tags at compose time; the tracked HTML holds no stale copy."""
    for rel in ("site/index.html", "site/paper/abstract.html", "site/history.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert 'property="og:' not in text and 'name="twitter:' not in text, rel
        assert 'rel="canonical"' not in text and "ld+json" not in text, rel
    assert 'name="description"' not in (ROOT / "site" / "index.html").read_text(encoding="utf-8")


def test_apply_replaces_and_never_doubles():
    page = (
        '<!DOCTYPE html><html><head><title>A &amp; B</title>\n<meta name="description" '
        'content="Its own line.">\n<meta property="og:title" content="stale">\n'
        '<link rel="canonical" href="stale">\n</head><body>x</body></html>'
    )
    out = site_metadata.apply(page, "a/")
    assert out.count('name="description"') == 1 and "Its own line." in out
    assert out.count('property="og:title"') == 1 and "stale" not in out
    assert '<meta property="og:title" content="A &amp; B">' in out
    assert f'<link rel="canonical" href="{PUBLIC}a/">' in out
    assert out.endswith("</head><body>x</body></html>")
    assert site_metadata.apply(out, "a/") == out, "a second application changes nothing"
    with pytest.raises(ValueError, match="no </head>"):
        site_metadata.apply("<html><title>t</title>", "")


# --- the pages -----------------------------------------------------------------------------------


@pytest.mark.parametrize("rel", [*ROOT_PAGES, *DOCS_PAGES])
def test_page_carries_the_fields(assembled, rel):
    """R-1: description, canonical, the Open Graph set, the Twitter card and the WebSite JSON-LD on
    the root pages and the docs pages, each once; the addresses are the page's own."""
    head = _head(assembled / rel)
    path = "" if rel == "index.html" else rel.removesuffix("index.html")
    address = PUBLIC + path
    description = _one(head, "description")
    assert description and len(description) <= 320
    assert head.links.get("canonical") == [address]
    for key in OG:
        _one(head, key)
    for key in TWITTER:
        _one(head, key)
    assert _one(head, "og:url") == address
    assert _one(head, "og:title") == " ".join(head.title.split()) == _one(head, "twitter:title")
    assert _one(head, "og:description") == description == _one(head, "twitter:description")
    assert _one(head, "og:image") == PUBLIC + "preview.png" == _one(head, "twitter:image")
    assert (_one(head, "og:image:width"), _one(head, "og:image:height")) == ("1200", "630")
    assert _one(head, "og:type") == "website" and _one(head, "og:site_name") == "tradespace"
    assert _one(head, "twitter:card") == "summary_large_image"
    assert len(head.json_ld) == 1
    data = json.loads(head.json_ld[0])
    assert data["@context"] == "https://schema.org"
    types = [node["@type"] for node in data["@graph"]]
    assert types == (["SoftwareSourceCode", "WebSite"] if rel == "index.html" else ["WebSite"])
    website = data["@graph"][-1]
    assert website["url"] == PUBLIC and website["name"] == "tradespace"
    assert website["author"]["@id"] == VALUES["author"]["orcid"]


def test_descriptions_are_the_pages_own_or_the_sites(assembled):
    """The root page and the docs carry pyproject's description; the history page its own line;
    the abstract page the abstract's first sentence."""
    site = VALUES["description"]
    assert _one(_head(assembled / "index.html"), "description") == site
    for rel in DOCS_PAGES:
        assert _one(_head(assembled / rel), "description") == site, rel
    history = _one(_head(assembled / "history.html"), "description")
    assert history != site and history.startswith("An essay on")
    abstract = _one(_head(assembled / "paper" / "index.html"), "description")
    assert abstract == paper_abstract.first_sentence(paper_abstract.front_matter()["abstract"])


def test_root_page_json_ld_names_the_package(assembled):
    """R-2: the ``SoftwareSourceCode`` node carries the package's facts from their sources."""
    data = json.loads(_head(assembled / "index.html").json_ld[0])
    software = data["@graph"][0]
    assert software["@type"] == "SoftwareSourceCode"
    assert software["version"] == PYPROJECT["version"]
    assert software["name"] == PYPROJECT["name"]
    assert software["description"] == VALUES["description"]
    assert software["codeRepository"] == PYPROJECT["urls"]["Repository"]
    assert software["license"] == "https://spdx.org/licenses/" + CITATION["license"]
    assert software["programmingLanguage"] == "Python"
    assert software["url"] == PUBLIC
    assert software["author"]["@id"] == CITATION["authors"][0]["orcid"]
    assert software["author"]["name"] == VALUES["author"]["name"]


def test_every_served_page_has_description_canonical_title_and_image(assembled):
    """R-1 over every page of the staged site, docs pages included."""
    pages = sorted(assembled.rglob("*.html"))
    assert len(pages) > 20
    for page in pages:
        if page.name == "404.html":
            continue
        head = _head(page)
        rel = page.relative_to(assembled).as_posix()
        assert len(head.meta.get("description", [])) == 1, rel
        assert len(head.links.get("canonical", [])) == 1, rel
        assert len(head.meta.get("og:title", [])) == 1, rel
        assert len(head.meta.get("og:image", [])) == 1, rel
        assert len(head.json_ld) == 1, rel


def test_every_image_and_canonical_address_exists_in_the_tree_and_serves(assembled, served):
    """Every ``og:image``, ``twitter:image`` and canonical address is under the public address,
    names a file of the staged tree and answers 200 on the staged server."""
    addresses = set()
    for page in assembled.rglob("*.html"):
        if page.name == "404.html":
            continue
        head = _head(page)
        addresses.update(head.meta.get("og:image", []))
        addresses.update(head.meta.get("twitter:image", []))
        addresses.update(head.meta.get("og:url", []))
        addresses.update(head.links.get("canonical", []))
    assert addresses
    for address in sorted(addresses):
        assert _exists(assembled, address), address
        local = served + "/" + address.removeprefix(PUBLIC)
        with urllib.request.urlopen(local, timeout=10) as response:
            assert response.status == 200, address


# --- the preview image -----------------------------------------------------------------------


def test_preview_image_is_the_link_handlers_size_and_under_a_megabyte(assembled):
    """R-3: 1200 by 630 px, opaque, under 1 MB, generated at compose time."""
    from PIL import Image

    path = assembled / "preview.png"
    assert path.is_file() and not (ROOT / "site" / "preview.png").exists()
    with Image.open(path) as image:
        assert image.size == (1200, 630)
        assert image.mode == "RGB"
    assert 10_000 < path.stat().st_size < 1_000_000


# --- robots.txt and the sitemap ----------------------------------------------------------------


def test_robots_allows_everything_and_names_the_sitemap(assembled):
    text = (assembled / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *\nAllow: /\n" in text
    assert "Disallow" not in text
    assert f"Sitemap: {PUBLIC}sitemap.xml" in text


def test_sitemap_lists_the_root_pages_and_the_docs_and_every_address_exists(assembled):
    text = (assembled / "sitemap.xml").read_text(encoding="utf-8")
    assert text.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns=')
    locs = re.findall(r"<loc>(.*?)</loc>", text)
    assert len(locs) == len(set(locs)) > 20
    for address in locs:
        assert _exists(assembled, address), address
    assert {PUBLIC, PUBLIC + "history.html", PUBLIC + "paper/"} <= set(locs)
    docs = re.findall(r"<loc>(.*?)</loc>", (assembled / "docs" / "sitemap.xml").read_text("utf-8"))
    assert docs and set(docs) <= set(locs), "the docs' own sitemap is included"
    assert {PUBLIC + "docs/", PUBLIC + "docs/getting-started/", PUBLIC + "docs/theory/"} <= set(
        locs
    )
    for address in locs:
        assert urlparse(address).scheme == "https"
