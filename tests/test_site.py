"""The site skeleton: configuration, links, workflow, root index, and the full build.

Everything here runs in the default ``uv run pytest`` with no network access. The full-build test
runs ``scripts/assemble_site.py`` into a temporary directory when ``mkdocs`` is importable and
skips with a stated reason when it is not.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlparse

import pytest
import yaml
from markdown.extensions.toc import slugify

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
PUNCH_LIST = ROOT / "work-packages" / "release-punch-list.md"
CONTRACT = tomllib.loads(
    (ROOT / "work-packages" / "interface-contract.toml").read_text(encoding="utf-8")
)
GENERATED_PAGES = {
    CONTRACT["docs"]["generated_dir"].removeprefix("docs/") + n
    for n in CONTRACT["docs"]["generated_pages"]
}
PUBLIC_URL = CONTRACT["build"]["public_url"]

# The navigation, in order (WP8a Amendment 2). The Glossary is the one generated page.
NAV_PAGES = [
    "index.md",
    "getting-started.md",
    "user-guide/overview.md",
    "user-guide/conditioning.md",
    "user-guide/fitting.md",
    "user-guide/choosing-k.md",
    "user-guide/tensions.md",
    "user-guide/chart.md",
    "user-guide/prediction.md",
    "user-guide/termination.md",
    "user-guide/limitations.md",
    "api.md",
    "api-reference.md",
    "examples.md",
    "theory.md",
    "generated/glossary.md",
    "further-reading.md",
]
# Word budgets of the hand-written pages (code blocks and tables excluded), total at most 7,600.
BUDGETS = {
    "index.md": 206,
    "getting-started.md": 351,
    "user-guide/overview.md": 399,
    "user-guide/conditioning.md": 610,
    "user-guide/fitting.md": 668,  # 800 until WP31 U2 and U3
    "user-guide/choosing-k.md": 573,  # 707 until WP33 (the cubesat block moved to Examples)
    "user-guide/tensions.md": 700,
    "user-guide/chart.md": 557,  # 600 until WP28 X-1; 561 until the holes block printed
    "user-guide/prediction.md": 350,
    "user-guide/termination.md": 743,  # 600 until WP28 S-10
    "user-guide/limitations.md": 493,
    "api.md": 300,
    "examples.md": 671,  # 720 until WP28 X-2 (the coordinates figure went); 676 until WP33
    "theory.md": 700,
    "further-reading.md": 300,
}
TOTAL_BUDGET = 7254  # 7472 until WP33 (Home, the cubesat block, what must hold, tops)
# Post-release live routes (the punch list names each; stage_site.REVIEW_PAGES follows them).
LIVE_ROUTES = (
    "docs/",
    "docs/getting-started/",
    "docs/user-guide/overview/",
    "docs/theory/",
    "docs/generated/glossary/",
    "docs/api-reference/",
    "docs/further-reading/",
    "paper/",
)

HAVE_MKDOCS = all(
    importlib.util.find_spec(m) is not None
    for m in ("mkdocs", "material", "mkdocstrings", "mkdocs_bibtex")
)
ASSEMBLE = ROOT / "scripts" / "assemble_site.py"


class _Loader(yaml.SafeLoader):
    """SafeLoader that accepts the custom tags MkDocs configurations use."""


_Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
_Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_Loader)


def flatten_nav(nav) -> list[str]:
    pages: list[str] = []
    for item in nav:
        if isinstance(item, str):
            pages.append(item)
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    pages.append(value)
                else:
                    pages.extend(flatten_nav(value))
    return pages


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(match.group(1)) if match else {}


def punch_list_urls() -> set[str]:
    """URLs under 'Expected-at-release links' of the punch list."""
    text = PUNCH_LIST.read_text(encoding="utf-8")
    section = text.split("## Expected-at-release links", 1)[1].split("\n## ", 1)[0]
    return set(re.findall(r"https?://[^\s)`]+", section))


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("a", "link") and d.get("href"):
            self.hrefs.append(d["href"])
        if tag in ("script", "img") and d.get("src"):
            self.hrefs.append(d["src"])


def html_links(path: Path) -> list[str]:
    parser = _Links()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.hrefs


MD_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def md_links(path: Path) -> list[str]:
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    return MD_LINK.findall(text)


def is_external(href: str) -> bool:
    return bool(urlparse(href).scheme) or href.startswith("//")


def source_pages() -> list[Path]:
    """The hand-written docsite pages, recursive (not the generated glossary, not the notes)."""
    return sorted(
        p
        for p in DOCS.rglob("*.md")
        if p.relative_to(DOCS).parts[0] not in ("generated", "superpowers")
    )


def prose_words(path: Path) -> int:
    """Words of a page outside fenced code blocks, tables, image alt text and HTML comments."""
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # alt text is not prose; captions count
    text = re.sub(r"^\|.*$", "", text, flags=re.M)
    return len(text.split())


@pytest.fixture(scope="session")
def mkdocs_config() -> dict:
    return load_yaml(ROOT / "mkdocs.yml")


# --- configuration -----------------------------------------------------------------------------


def test_mkdocs_config_parses(mkdocs_config):
    cfg = mkdocs_config
    assert cfg["site_url"] == PUBLIC_URL + "docs/"
    assert cfg["theme"]["name"] == "material"
    assert "custom_dir" not in cfg["theme"], "no template override: the world lines are gone"
    assert not (ROOT / "overrides").exists()
    assert cfg["docs_dir"] == "docs"
    exts = {next(iter(e)) if isinstance(e, dict) else e for e in cfg["markdown_extensions"]}
    assert "pymdownx.arithmatex" in exts
    plugins = {next(iter(p)) if isinstance(p, dict) else p for p in cfg["plugins"]}
    assert {"mkdocstrings", "bibtex"} <= plugins
    bibtex = next(p["bibtex"] for p in cfg["plugins"] if isinstance(p, dict) and "bibtex" in p)
    assert bibtex["bib_file"] == CONTRACT["docs"]["bibliography"]
    mathjax = [s for s in cfg["extra_javascript"] if "mathjax" in s]
    assert mathjax and re.search(r"mathjax@\d+\.\d+\.\d+/", mathjax[0]), "MathJax must be pinned"
    excluded = cfg["exclude_docs"]
    assert "superpowers/" in excluded and "references.bib" in excluded


def test_nav_pages_exist_and_cover_the_contract_pages(mkdocs_config):
    pages = flatten_nav(mkdocs_config["nav"])
    for page in pages:
        assert page in GENERATED_PAGES or (DOCS / page).is_file(), page
    assert pages == NAV_PAGES
    contract_pages = set(CONTRACT["docs"]["pages"])
    assert contract_pages <= set(pages)
    assert set(pages) >= GENERATED_PAGES
    assert {f"docs/{p}" for p in pages if p not in GENERATED_PAGES} == set(
        CONTRACT["docs"]["presentation_pages"]
    )
    # every hand-written page on disk is in the navigation, and nothing else
    on_disk = {p.relative_to(DOCS).as_posix() for p in source_pages()}
    assert on_disk == set(pages) - GENERATED_PAGES


def test_word_budgets_hold():
    over = {}
    total = 0
    for page, budget in BUDGETS.items():
        words = prose_words(DOCS / page)
        total += words
        if words > budget:
            over[page] = (words, budget)
    assert not over, over
    assert total <= TOTAL_BUDGET, total


def test_hand_written_pages_carry_no_review_or_proof_content():
    """No lemma block, proof, review prose or ledger-id citation on a docsite page; displayed
    formulas only on theory.md, at most six, none tagged."""
    forbidden = [
        r"^\*\*(Lemma|Proposition|Corollary)",
        r"\bWP\d+\b",
        r"supervisor",
        r"reviewer",
        r"abstraction-gaps",
        r"\bG-\d+\b",
        r"<!--\s*(lemma:|definition)",
        r"^\*\*Proof",
    ]
    for page in source_pages():
        text = re.sub(r"```.*?```", "", page.read_text(encoding="utf-8"), flags=re.S)
        for pattern in forbidden:
            assert not re.search(pattern, text, re.I | re.M), f"{page.name}: {pattern}"
        displays = re.findall(r"\$\$", text)
        if page.name != "theory.md":
            assert not displays, f"{page.name}: displayed formula outside theory.md"
        else:
            assert len(displays) // 2 <= 6, "theory.md: more than six displayed formulas"


def test_every_hand_written_page_is_free_of_front_matter():
    """No world key (or any front matter) on a docsite page."""
    for page in source_pages():
        assert not page.read_text(encoding="utf-8").startswith("---"), page.name


def test_no_table_needs_columns_on_a_phone(mkdocs_config):
    """D3: the hand-written pages use lists, and the API reference renders parameters as lists."""
    for page in source_pages():
        tables = [ln for ln in page.read_text(encoding="utf-8").splitlines() if ln.startswith("|")]
        assert not tables, f"{page.name}: a table (use a list)"
    handler = next(p["mkdocstrings"] for p in mkdocs_config["plugins"] if "mkdocstrings" in p)
    assert handler["handlers"]["python"]["options"]["docstring_section_style"] == "list"


def test_api_reference_names_equal_the_contract():
    text = (DOCS / "api-reference.md").read_text(encoding="utf-8")
    names = re.findall(r"^::: hyperbolic_trade_space\.(\w+)\s*$", text, re.M)
    assert sorted(names) == sorted(CONTRACT["package"]["public_names"])
    assert len(names) == len(set(names))


def test_citations_resolve():
    bib = (DOCS / "references.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"^@\w+\{([^,\s]+),", bib, re.M))
    cited = set()
    for path in source_pages():
        for group in re.findall(r"\[(@[^\]]+)\]", path.read_text(encoding="utf-8")):
            cited |= set(re.findall(r"@([\w:.\-/]+)", group))
    assert cited, "the docs should cite"
    assert cited <= keys, sorted(cited - keys)


# --- links -------------------------------------------------------------------------------------


def _doc_target_exists(page: Path, href: str) -> bool:
    target, _ = urldefrag(href)
    if not target:
        return True
    resolved = (page.parent / unquote(target)).resolve()
    if resolved.is_file():
        return True
    rel = resolved.relative_to(DOCS).as_posix() if resolved.is_relative_to(DOCS) else None
    return rel in GENERATED_PAGES


def _is_site_route(href: str) -> bool:
    """A link that leaves the docs tree for a published route (``../`` or ``../../paper/``)."""
    return href.startswith("../")


def test_docs_relative_links_resolve():
    external_expected = punch_list_urls()
    for path in source_pages():
        for href in md_links(path):
            if is_external(href):
                if href.startswith(PUBLIC_URL):
                    assert href in external_expected, f"{path.name}: {href} not on the punch list"
                continue
            if _is_site_route(href):
                continue  # published routes outside the docs tree; checked on the assembled site
            assert _doc_target_exists(path, href), f"{path.name}: broken link {href}"


def _heading_slugs(path: Path) -> set[str]:
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    return {slugify(h, "-") for h in re.findall(r"^#{1,6}\s+(.*?)\s*#*\s*$", text, re.M)}


def test_internal_anchors_resolve():
    """A link with a fragment to a docsite page names a heading that page has."""
    for path in source_pages():
        for href in md_links(path):
            if is_external(href) or href.startswith("../"):
                continue
            target, frag = urldefrag(href)
            if not frag:
                continue
            resolved = (path.parent / unquote(target)).resolve() if target else path
            assert resolved.is_file(), f"{path.name}: {href}"
            assert frag in _heading_slugs(resolved), f"{path.name}: no heading for {href}"


def _paper_keys_module():
    spec = importlib.util.spec_from_file_location("_paper_keys", ROOT / "scripts" / "paper_keys.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_docsite_cites_the_paper_only_through_keys():
    """D-6: a link into the paper is ``[text](paper:key)`` and nothing else; every cited key is a
    label the paper defines, and the docs cite the paper at least once."""
    keys = _paper_keys_module().paper_keys()
    cited = set()
    for path in source_pages():
        for href in md_links(path):
            if href.startswith("paper:"):
                cited.add(href.removeprefix("paper:"))
                continue
            assert "paper/" not in href and "paper_sections" not in href, f"{path.name}: {href}"
    assert cited, "the docs cite the paper"
    assert cited <= set(keys), sorted(cited - set(keys))


def test_paper_keys_resolve_to_relative_links_and_unknown_keys_fail():
    mod = _paper_keys_module()
    keys = mod.paper_keys()
    assert keys["thm-kkt"] == "paper/" and keys["appendix-b"] == "paper/supporting-material/"
    text = "[a](paper:thm-kkt) and [b](paper:appendix-b)"
    assert mod.resolve(text, "", keys) == (
        "[a](../paper/#thm-kkt) and [b](../paper/supporting-material/#appendix-b)"
    )
    assert mod.resolve("[a](paper:fig-nlemma)", "user-guide/fitting/", keys) == (
        "[a](../../../paper/#fig-nlemma)"
    )
    assert mod.resolve("[a\nb](paper:thm-kkt)", "", keys) == "[a\nb](../paper/#thm-kkt)"
    fenced = "```\n[a](paper:thm-kkt)\n```"
    assert mod.resolve(fenced, "", keys) == fenced, "a code fence is left as written"
    with pytest.raises(mod.UnknownPaperKey):
        mod.resolve("[a](paper:no-such-key)", "", keys)


def test_every_paper_key_is_a_label_of_the_built_paper():
    """The keys read from the notebooks are the labels the paper's build publishes, on the page
    the resolver names (needs a built paper: ``scripts/stage_site.py`` leaves one)."""
    xref = ROOT / "paper" / "_build" / "html" / "myst.xref.json"
    if not xref.is_file():
        pytest.skip("no built paper (run scripts/stage_site.py first)")
    import json

    refs = json.loads(xref.read_text(encoding="utf-8"))["references"]
    built = {r["identifier"]: r["url"].rstrip("/") for r in refs if "identifier" in r}
    for key, route in _paper_keys_module().paper_keys().items():
        page = "/" + route.removeprefix("paper/").rstrip("/")
        assert built.get(key) == (page if page != "/" else ""), (key, built.get(key), route)


def _resolve_site_href(page_url: str, href: str) -> str:
    """Resolve ``href`` against the public path of a page, returning an absolute site path."""
    base = urlparse(PUBLIC_URL).path  # /hyperbolic-trade-space/
    page_path = base.rstrip("/") + page_url
    return urlparse(urljoin(f"http://x{page_path}", href)).path


def _site_file_for(path_in_site: str, site_root: Path) -> Path | None:
    base = urlparse(PUBLIC_URL).path
    assert path_in_site.startswith(base), path_in_site
    rel = path_in_site[len(base) :]
    candidate = site_root / rel
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate if candidate.is_file() else None


# Images the assembled root page gets at build time (the paper's Figure 1, copied; the Why image,
# generated); they are not in site/ and are checked on the assembled site.
BUILT_IMAGES = {
    "figure1.png",
    "ternary-planted-light.png",
    "ternary-planted-dark.png",
}


def test_root_and_paper_links_classified():
    """Every link on the two hand-written pages is internal and resolvable, or external and
    either the repository or a punch-list URL."""
    expected = punch_list_urls()
    repo = "https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space"
    for rel, page_url in (("index.html", "/"), ("paper/index.html", "/paper/")):
        for href in html_links(SITE / rel):
            if href.startswith("data:"):
                continue  # the empty icon: the page asks the server for no /favicon.ico (404)
            if is_external(href):
                assert href.startswith(repo) or href in expected, f"{rel}: unlisted external {href}"
                continue
            if rel == "index.html" and href in BUILT_IMAGES:
                continue
            route = _resolve_site_href(page_url, href)
            assert route.startswith(urlparse(PUBLIC_URL).path)
            sub = route[len(urlparse(PUBLIC_URL).path) :]
            if sub.startswith(("docs/", "paper/supporting-material/")):
                continue  # docsite and built paper pages: checked on the assembled site
            assert _site_file_for(route, SITE) is not None, f"{rel}: {href} does not resolve"


def test_root_index_is_thin_and_routes_by_need():
    """WP33 G2, R-3: after the title, one whom-it-is-for sentence and at most five need-phrases,
    each a link; no cards. Then why, what."""
    text = (SITE / "index.html").read_text(encoding="utf-8")
    assert "<script" not in text.lower()
    assert "prefers-color-scheme: dark" in text
    assert 'class="cards"' not in text
    needs = re.search(r'<ul class="needs">(.*?)</ul>', text, re.S).group(1)
    items = re.findall(r"<li>(.*?)</li>", needs, re.S)
    assert 1 <= len(items) <= 5
    assert all(re.fullmatch(r'<a href="[^"]+">[^<]+</a>', i) for i in items), items
    assert text.count('class="whom"') == 1
    low = text.lower()
    order = [
        low.index(k) for k in ('class="whom"', 'class="needs"', "<h2>why</h2>", "<h2>what</h2>")
    ]
    assert order == sorted(order), "order: whom, needs, why, what"
    for needle in ("scikit-learn", "unsupervised", "feature engineering", "pca"):
        assert needle in low, needle
    for banned in ("sympy", "worked example", "chatgpt", "openai"):
        assert banned not in low, banned
    hrefs = html_links(SITE / "index.html")
    for href in ("paper/", "docs/getting-started/", "docs/user-guide/conditioning/"):
        assert href in hrefs
    assert any(h.endswith("hyperbolic-trade-space") for h in hrefs), "repository link"
    assert '<link rel="icon" href="data:,">' in text  # D6: no /favicon.ico request, no 404
    assert '<link rel="icon" href="data:,">' in (SITE / "paper" / "index.html").read_text(
        encoding="utf-8"
    )
    # R1: a wide figure may use a wide screen's width
    assert "min(94vw" in text and "figure.wide" in text
    assert "break-all" not in text and "anywhere" not in text
    # R3: the wording matches the thinned docsite
    for stale in ("page by page", "its mathematics", "in full"):
        assert stale not in text.lower(), stale
    assert "pypi.org" not in text.lower()
    paper = (SITE / "paper" / "index.html").read_text(encoding="utf-8")
    assert "The paper is in preparation" in paper
    assert "../docs/" in html_links(SITE / "paper" / "index.html")
    assert "../" in html_links(SITE / "paper" / "index.html")
    assert "working draft" not in (text + paper).lower()
    for stale in ("page by page", "its mathematics", "in full"):
        assert stale not in paper.lower(), stale


HISTORY = SITE / "history.html"


class _VisibleText(HTMLParser):
    """The visible words of a page: no head, style, script or markup."""

    def __init__(self):
        super().__init__()
        self.skip = 0
        self.words = []

    def handle_starttag(self, tag, attrs):
        if tag in ("head", "style", "script", "title"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("head", "style", "script", "title"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.words += data.split()


def _history_text() -> str:
    parser = _VisibleText()
    parser.feed(HISTORY.read_text(encoding="utf-8"))
    return " ".join(parser.words)


def _load_script(name):
    spec = importlib.util.spec_from_file_location(f"_{name}", ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


HISTORY_RECORD = _load_script("history_record")

THIRTEEN = (
    "Markus Koch",
    "Danilo Bernardineli",
    "Rohan Mehta",
    "Joshua Jodesty",
    "Jamsheed Shorish",
    "Kris Paruch",
    "Andrew Penland",
    "Jakob Hackel",
    "Emanuel Lima",
    "Andrew Clark",
    "Sean McOwen",
    "Carolina Riascos-\u00c1lvarez",
    "Matthew Barlin",
)


def test_history_record_holds_the_schema_and_every_entry_has_its_required_fields():
    """WP37 D-9: the record's schema is described at its top; every entry has the required fields
    and an https URL; ids and URLs are unique; the thirteen people each have an entry."""
    raw = (ROOT / "history.yaml").read_text(encoding="utf-8")
    head = raw.split("entries:")[0]
    for field in HISTORY_RECORD.REQUIRED + HISTORY_RECORD.OPTIONAL:
        assert re.search(rf"^#\s+{field}\b", head, re.M), f"schema description lacks {field}"
    entries = HISTORY_RECORD.load()
    assert HISTORY_RECORD.validate(entries) == []
    assert len(entries) >= 60
    persons = {e["title"] for e in entries if e["kind"] == "person"}
    assert persons == set(THIRTEEN)
    for e in entries:
        assert set(HISTORY_RECORD.REQUIRED) <= set(e), e["id"]
        assert e["url"].startswith("https://"), e["id"]


def test_history_record_flags_special_cases_and_keeps_the_register():
    """The Filecoin and RAI items carry the special-case flag; nothing else in a cryptocurrency
    setting is left unflagged by id."""
    entries = {e["id"]: e for e in HISTORY_RECORD.load()}
    for eid in ("2023-fip-0056", "2023-consensus-pledge", "2021-rai-design", "2024-edinburgh"):
        assert entries[eid].get("special_case") is True, eid


def test_history_record_validation_names_each_defect():
    good = {
        "id": "2020-x",
        "date": "2020",
        "kind": "paper",
        "title": "T",
        "url": "https://example.org/a",
        "read_on": "2026-11-12",
        "shows": "s",
        "claim": "sourced",
    }
    assert HISTORY_RECORD.validate([good]) == []
    for change, expect in (
        ({"url": "http://example.org/a"}, "https"),
        ({"date": "20"}, "date"),
        ({"kind": "blog"}, "kind"),
        ({"claim": "maybe"}, "claim"),
        ({"shows": ""}, "missing"),
        ({"people": [{"nom": "x"}]}, "people"),
        ({"special_case": "yes"}, "boolean"),
        ({"extra": 1}, "unknown"),
    ):
        bad = {**good, **change}
        problems = HISTORY_RECORD.validate([bad])
        assert any(expect in p for p in problems), (change, problems)
    twin = {**good, "id": "2020-y"}
    assert any("duplicate url" in p for p in HISTORY_RECORD.validate([good, twin]))


def test_history_page_is_one_screen_in_the_root_page_register():
    """WP37: a stand-alone page, light and dark like the root page, no script, about one screen."""
    raw = HISTORY.read_text(encoding="utf-8")
    assert "<script" not in raw.lower()
    assert "prefers-color-scheme: dark" in raw
    assert '<link rel="icon" href="data:,">' in raw
    assert "<h1>History and acknowledgements</h1>" in raw
    assert 250 <= len(_history_text().split()) <= 450


def test_history_page_is_linked_from_the_root_page_and_links_resolve():
    """The root page links to it once; its internal links resolve; its external links are plain
    absolute https URLs (the network check is scripts/check_history_links.py)."""
    assert html_links(SITE / "index.html").count("history.html") == 1
    seen = set()
    for href in html_links(HISTORY):
        if href.startswith("data:"):
            continue  # the empty icon
        if is_external(href):
            parts = urlparse(href)
            assert parts.scheme == "https" and parts.netloc and " " not in href, href
            assert href not in seen, f"duplicate external link {href}"
            seen.add(href)
            continue
        target, _ = urldefrag(href)
        if not target:
            continue
        route = _resolve_site_href("/history.html", target)
        assert _site_file_for(route, SITE) is not None, f"history.html: {href} does not resolve"


def test_history_page_uses_no_cryptocurrency_or_web3_vocabulary():
    """WP37 register rule: the page's own words avoid it (a linked source's title may carry it)."""
    text = _history_text().lower()
    for banned in (
        r"crypto",
        r"token",
        r"blockchain",
        r"smart contract",
        r"web3",
        r"\bdao\b",
        r"\bdefi\b",
        r"\bnft\b",
    ):
        assert not re.search(banned, text), banned
    # computer science is the supervisor's word for the team's backgrounds (WP37 decisions),
    # offered on the page as the team's own account of the team
    assert "in our own account of the team" in _history_text()


def test_history_page_credits_the_twelve_named_people():
    text = _history_text()
    for name in (
        "Markus Koch",
        "Danilo Bernardineli",
        "Rohan Mehta",
        "Joshua Jodesty",
        "Jamsheed Shorish",
        "Kris Paruch",
        "Penland",
        "Jakob Hackel",
        "Emanuel Lima",
        "Andrew Clark",
        "Sean McOwen",
        "Carolina Riascos-\u00c1lvarez",
    ):
        assert name in text, name


def test_history_page_marks_the_team_account_and_credits_cadcad_as_authors_txt_does():
    """WP37 W3 decisions: the team's own account is marked each time; cadCAD's designers are
    credited as AUTHORS.txt states them; Paruch is quoted in his own words."""
    text = _history_text()
    assert text.count("our own account") + text.count("the same account") >= 3
    assert "designed by Michael Zargham, Markus Koch and Matthew Barlin" in text
    assert "a mathematical background with focus on economic modeling" in text
    assert text.count("Barlin") == 1


def test_history_page_follows_the_supervisors_wording_rulings():
    """WP37 decisions, the last entries govern: the firm's description and the activities sentence
    verbatim; Generalized Dynamical Systems without 'Part I'; the Applied Network Science journal
    paper cited in place of the preprint; Carolina by name and GitHub handle, never LinkedIn; one
    sentence for the work on client projects that cannot be named."""
    text = _history_text()
    raw = HISTORY.read_text(encoding="utf-8")
    assert "contract research and engineering firm" in text
    assert (
        "We perform requirements, architecture, design, simulation and analysis for clients, "
        "all software-defined, studying the spaces of feasible designs of their systems under "
        "uncertain, strategic and adversarial users."
    ) in text
    assert "Part I" not in text and "generalized" not in text.lower().replace(
        "generalized dynamical systems", ""
    )
    assert "https://doi.org/10.1007/s41109-020-0254-9" in raw
    assert "1807.00955" not in raw
    assert "Zixuan Zhang" in text and "Victor Preciado" in text
    assert "https://github.com/CarolinaRiascos" in raw and "linkedin" not in raw.lower()
    assert "worked on client projects we cannot name" in text
    assert "cannot describe here" in text
    for ref in ("gds-axelrod", "10.1007/s10614-023-10445-9", "fip-0056", "vr6sIfjGmLQ"):
        assert ref in raw, ref
    assert "workshop in Edinburgh (ICMS), October 2024" in text


def test_paper_theme_is_pinned_to_a_commit():
    """A clean checkout must build the paper on the theme it was reviewed on (WP8b D-8): the
    article theme is a commit-pinned archive, not the name that follows the main branch."""
    template = load_yaml(ROOT / "paper" / "myst.yml")["site"]["template"]
    assert re.fullmatch(
        r"https://github\.com/myst-templates/article-theme/archive/[0-9a-f]{40}\.zip", template
    ), template


def test_punch_list_covers_post_release_checks():
    text = PUNCH_LIST.read_text(encoding="utf-8")
    for route in LIVE_ROUTES:
        assert f"`{route}`" in text, route
    assert "PyPI" in text and "release notes" in text.lower()
    assert "stable reference keys" in text, "the deferred paper-reference item stays recorded"


def test_stage_review_pages_follow_the_live_routes():
    spec = importlib.util.spec_from_file_location("_stage_site", ROOT / "scripts" / "stage_site.py")
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(ROOT / "scripts"))
    assert tuple(mod.REVIEW_PAGES) == ("/", *(f"/{r}" for r in LIVE_ROUTES))


# --- the Pages workflow ------------------------------------------------------------------------


@pytest.fixture(scope="module")
def workflow() -> dict:
    wf = load_yaml(ROOT / ".github" / "workflows" / "pages.yml")
    # PyYAML reads the key `on` as boolean True.
    wf["on"] = wf.get("on", wf.get(True))
    return wf


def test_workflow_triggers_release_tag_and_dispatch_only(workflow):
    triggers = workflow["on"]
    assert set(triggers) == {"push", "workflow_dispatch"}
    assert triggers["push"] == {"tags": ["v*"]}, "no push-to-branch trigger"


def test_workflow_build_and_deploy_jobs(workflow):
    jobs = workflow["jobs"]
    build_text = " ".join(
        str(step.get("uses", "")) + " " + str(step.get("run", ""))
        for step in jobs["build"]["steps"]
    )
    for needle in (
        "actions/checkout",
        "astral-sh/setup-uv",
        "uv sync --locked",
        "uv run pytest",
        "uv run python scripts/assemble_site.py",
        "actions/upload-pages-artifact",
    ):
        assert needle in build_text, needle
    upload = next(s for s in jobs["build"]["steps"] if "upload-pages-artifact" in s.get("uses", ""))
    assert upload["with"]["path"] == "_site"
    deploy = jobs["deploy"]
    assert deploy["needs"] == "build"
    assert deploy["if"] == "startsWith(github.ref, 'refs/tags/v')"
    assert deploy["permissions"] == {"pages": "write", "id-token": "write"}
    assert deploy["environment"]["name"] == "github-pages"
    assert any("actions/deploy-pages" in s.get("uses", "") for s in deploy["steps"])
    assert workflow["concurrency"]["group"] == "pages"


# --- the full build ----------------------------------------------------------------------------


@pytest.fixture(scope="session")
def generated_dir(tmp_path_factory) -> Path:
    """The paper's generated pages (derivations, verification), built here for the test that
    asserts them: a test never relies on a file another command left in ``build/``."""
    return tmp_path_factory.mktemp("generated")


@pytest.fixture(scope="session")
def assembled(tmp_path_factory, generated_dir) -> Path:
    if not HAVE_MKDOCS:
        pytest.skip("the docs dependency group is not installed (mkdocs not importable)")
    if not ASSEMBLE.is_file():
        pytest.skip("scripts/assemble_site.py has not been delivered yet")
    out = tmp_path_factory.mktemp("site")
    result = subprocess.run(
        [
            sys.executable,
            str(ASSEMBLE),
            "--out",
            str(out),
            "--generated-dir",
            str(generated_dir),
            "--paper",
            "placeholder",  # the real paper's build is a separate, slow step with its own tests
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]
    return out


@pytest.mark.slow
def test_assembled_layout(assembled):
    for rel in ("index.html", "docs/index.html", "paper/index.html"):
        assert (assembled / rel).is_file(), rel
    assert (assembled / "index.html").read_text(encoding="utf-8") == (
        SITE / "index.html"
    ).read_text(encoding="utf-8")
    for name in sorted(BUILT_IMAGES):
        assert (assembled / name).stat().st_size > 10_000, name
    assert (assembled / "figure1.png").read_bytes() == (
        ROOT / "paper" / "figures" / "figure1.png"
    ).read_bytes(), "the What image is the paper's Figure 1, copied, not regenerated"
    assert (assembled / "paper" / "index.html").read_text(encoding="utf-8") == (
        SITE / "paper" / "index.html"
    ).read_text(encoding="utf-8")


def test_assembled_site_carries_the_history_page(assembled):
    assert (assembled / "history.html").read_text(encoding="utf-8") == HISTORY.read_text(
        encoding="utf-8"
    )


def test_every_link_in_the_assembled_site_resolves(assembled):
    expected = punch_list_urls()
    base = urlparse(PUBLIC_URL).path
    problems = []
    # With the placeholder paper only ``paper/`` exists; the paper's other pages are checked by
    # the key test against the built paper (test_every_paper_key_is_a_label_of_the_built_paper).
    placeholder = (assembled / "paper" / "index.html").read_text(encoding="utf-8") == (
        SITE / "paper" / "index.html"
    ).read_text(encoding="utf-8")
    for page in assembled.rglob("*.html"):
        rel_url = "/" + page.relative_to(assembled).as_posix()
        page_url = rel_url[: -len("index.html")] if rel_url.endswith("index.html") else rel_url
        for href in html_links(page):
            if href.startswith(("#", "mailto:", "data:", "javascript:")):
                continue
            if is_external(href):
                if href.startswith(PUBLIC_URL) and href not in expected:
                    target = _site_file_for(urlparse(href).path, assembled)
                    if target is None:
                        problems.append((rel_url, href))
                continue
            target_path, _ = urldefrag(href)
            if not target_path:
                continue
            route = _resolve_site_href(page_url, target_path)
            if not route.startswith(base):
                continue
            if _site_file_for(route, assembled) is None:
                if placeholder and route.startswith(base + "paper/"):
                    continue
                problems.append((rel_url, href))
    assert not problems, problems[:20]


def test_math_markers_in_built_pages(assembled):
    html = (assembled / "docs" / "theory" / "index.html").read_text(encoding="utf-8")
    assert 'class="arithmatex"' in html
    assert "mathjax@" in html
    for page in source_pages():
        if re.search(r"\$[^$\n]+\$", page.read_text(encoding="utf-8")):
            rel = page.relative_to(DOCS).with_suffix("").as_posix()
            built = (assembled / "docs" / rel / "index.html").read_text(encoding="utf-8")
            assert 'class="arithmatex"' in built, f"{rel}: inline math is not rendered"


@pytest.mark.slow
def test_no_world_lines_in_built_pages(assembled):
    for html in (assembled / "docs").rglob("index.html"):
        assert "world-line" not in html.read_text(encoding="utf-8"), html


def test_citations_render_and_further_reading_lists_the_references(assembled):
    html = (assembled / "docs" / "further-reading" / "index.html").read_text(encoding="utf-8")
    assert "[@" not in re.sub(r"<code.*?</code>", "", html, flags=re.S)
    assert "<ol" in html or '<li id="' in html or "references" in html.lower()
    for key_text in ("Boyd", "Hoburg"):
        assert key_text in html, key_text


def test_api_reference_renders_every_public_name(assembled):
    html = (assembled / "docs" / "api-reference" / "index.html").read_text(encoding="utf-8")
    for name in CONTRACT["package"]["public_names"]:
        assert f"hyperbolic_trade_space.{name}" in html, name
    assert "doc-class" in html and "doc-function" in html


def test_generated_pages_in_the_build(assembled, generated_dir):
    for name in CONTRACT["docs"]["generated_pages"]:
        stem = name[: -len(".md")]
        assert (assembled / "docs" / "generated" / stem / "index.html").is_file()
    # OD1: derivations and verification are the paper's build, not the docsite's
    # the glossary page and the figures the pages embed
    assert sorted(p.name for p in (assembled / "docs" / "generated").iterdir()) == [
        "figures",
        "glossary",
    ]
    for name in CONTRACT["derivation"]["generated_pages"]:
        assert (generated_dir / name).is_file(), "built by the assemble step into the given dir"
        assert not (ROOT / "docs" / "generated" / name).exists()


# --- R-26: nothing refers to removed content ----------------------------------------------------

# Moved or removed content, as the patterns a reference to it would match.
REMOVED_REFERENCES = {
    "moved file names": r"\b(?:method|literature|why-and-how|preconditioning|case)\.md\b",
    "moved routes": r"docs/(?:method|literature|why-and-how|preconditioning|case|limitations)/",
    "generated pages under the docsite": r"generated/(?:derivations|verification)",
    "the Mathematics page": r"\]\(\s*method|see Mathematics|Mathematics page|\[Mathematics\]",
    "lemma tags": r"\bL(?:1[0-4]|[1-9])\b",
    "the world key": r"world-line|^world:|\bworld line\b",
}


def _refs(text: str) -> list[str]:
    found = []
    for label, pattern in REMOVED_REFERENCES.items():
        if re.search(pattern, text, re.M | re.I if label != "lemma tags" else re.M):
            found.append(label)
    return found


def test_r26_docsite_sources_refer_to_no_removed_content():
    problems = {
        p.relative_to(DOCS).as_posix(): _refs(p.read_text(encoding="utf-8")) for p in source_pages()
    }
    assert {k: v for k, v in problems.items() if v} == {}


def test_r26_root_page_navigation_and_site_scripts_refer_to_no_removed_content():
    scanned = [
        SITE / "index.html",
        SITE / "paper" / "index.html",
        ROOT / "mkdocs.yml",
        ROOT / "scripts" / "assemble_site.py",
        ROOT / "scripts" / "stage_site.py",
    ]
    problems = {}
    for path in scanned:
        text = path.read_text(encoding="utf-8")
        if path.name == "mkdocs.yml":
            text = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
            assert "overrides" not in text and "world" not in text.lower(), path.name
        hits = [h for h in _refs(text) if h != "lemma tags"]
        if hits:
            problems[path.name] = hits
    assert problems == {}


def test_r26_route_lists_refer_to_no_removed_content():
    assert _refs("\n".join(LIVE_ROUTES)) == []
    assert _refs("\n".join(NAV_PAGES)) == []
    assert not any("derivations" in r or "verification" in r for r in LIVE_ROUTES)
    text = PUNCH_LIST.read_text(encoding="utf-8")
    section = text.split("## Post-release live checks", 1)[1]
    assert _refs(section.split("- Deferred", 1)[0]) == []


def test_r26_no_removed_pages_on_disk():
    for name in ("method", "literature", "why-and-how", "preconditioning", "case", "limitations"):
        assert not (DOCS / f"{name}.md").exists(), name
    assert not (ROOT / "overrides").exists()
    assert not (DOCS / "generated" / "derivations.md").exists()
    assert not (DOCS / "generated" / "verification.md").exists()


def test_r26_built_docsite_refers_to_no_removed_content(assembled):
    problems = {}
    for html in sorted((assembled / "docs").rglob("index.html")):
        hrefs = [h for h in html_links(html) if not is_external(h)]
        bad = [h for h in hrefs if _refs(urldefrag(h)[0])]
        if bad:
            problems[html.relative_to(assembled).as_posix()] = bad
    assert problems == {}
    for removed in ("method", "literature", "why-and-how", "preconditioning", "case"):
        assert not (assembled / "docs" / removed).exists(), removed
    assert not (assembled / "docs" / "generated" / "derivations").exists()
    assert not (assembled / "docs" / "generated" / "verification").exists()


@pytest.mark.slow
def test_bare_mkdocs_build_leaves_the_root_site_directory_alone(mkdocs_config, assembled):
    """O-4: the default ``site_dir`` is not the tracked root ``site/`` directory."""
    assert Path(mkdocs_config["site_dir"]).resolve() != SITE.resolve()
    assert (ROOT / mkdocs_config["site_dir"]).resolve() != SITE.resolve()
    sys.path.insert(0, str(ROOT / "scripts"))
    import assemble_site

    with assemble_site._build_lock():  # the default site_dir is shared by parallel runs
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "-f", str(ROOT / "mkdocs.yml")],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    assert (SITE / "index.html").is_file()
    assert (SITE / "paper" / "index.html").is_file()


# --- the figures and the code columns ------------------------------------------------------------


def _docs_line_length():
    """The one setting of the code column: ruff's ``line-length`` in ``docs/ruff.toml``, which
    formats the Markdown code blocks (a code line that fits the column at 1280 px)."""
    import tomllib

    return tomllib.loads((DOCS / "ruff.toml").read_text(encoding="utf-8"))["line-length"]


CODE_COLUMN = _docs_line_length()
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)


def _figures_module():
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import build_figures

        return build_figures
    finally:
        sys.path.remove(str(ROOT / "scripts"))


def test_no_code_line_in_a_docsite_page_exceeds_the_column():
    """D2: the rendered column holds about 72 characters at 1280 px (measured in the browser pass),
    so no code line is longer; imports and comments are wrapped."""
    long_lines = {}
    for page in source_pages():
        for block in FENCE.findall(page.read_text(encoding="utf-8")):
            for line in block.splitlines():
                if len(line) > CODE_COLUMN:
                    long_lines.setdefault(page.name, []).append(line)
    assert long_lines == {}


def test_figures_are_few_captioned_and_in_both_colour_schemes():
    """D1: at most nine figures (WP18 OD2); each is a light and a dark image with the same alt text
    and one caption, directly below the code block that makes it."""
    bf = _figures_module()
    names = []
    for page in source_pages():
        text = page.read_text(encoding="utf-8")
        for name in re.findall(r"!\[[^\]]*\]\([^)\s#]*?([\w-]+)-light\.png#only-light\)", text):
            names.append(name)
            pair = re.findall(
                rf"!\[([^\]]+)\]\([^)\s#]*{name}-(light|dark)\.png#only-(?:light|dark)\)", text
            )
            assert sorted(k for _, k in pair) == ["dark", "light"], name
            assert pair[0][0] == pair[1][0] and len(pair[0][0].split()) >= 8, f"alt text: {name}"
            assert re.search(
                rf"{name}-dark\.png[^\n]*\n<figcaption>Figure \d+\. [^<]{{30,}}</figcaption>", text
            )
        assert [i for i, _ in bf.page_figures(page)] == sorted(i for i, _ in bf.page_figures(page))
    assert 1 <= len(names) <= bf.MAX_FIGURES == 8
    assert len(set(names)) == len(names)
    assert {"first-fit", "three-terms", "tension-report", "log-plane"} <= set(names)
    assert any(n.startswith("adcs-") for n in names), "an example from the case, on the frozen data"


def test_figure_numbers_run_one_to_n_in_navigation_order(mkdocs_config):
    """The captions' numbers are the docsite's own sequence (the paper has its own figures and
    numbers): read in the navigation's order they are 1, 2, ... with none missing or repeated, so a
    figure added or removed on one page cannot leave a stale number on the next."""
    numbers = []
    for name in flatten_nav(mkdocs_config["nav"]):
        path = DOCS / name
        if path.exists() and path in source_pages():
            text = path.read_text(encoding="utf-8")
            numbers += [int(n) for n in re.findall(r"<figcaption>Figure (\d+)\.", text)]
    assert numbers == list(range(1, len(numbers) + 1)), numbers


@pytest.mark.slow
def test_each_figure_is_produced_by_the_code_shown_above_it(tmp_path):
    """The runnable blocks of each page, executed by the figure builder, produce exactly the
    images the page embeds: present, non-blank, and different in the two colour schemes."""
    from PIL import Image

    bf = _figures_module()
    built = {}
    for page in bf.pages_with_figures(DOCS):
        written = bf.build_page(page, tmp_path)
        names = {name for _, name in bf.page_figures(page)}
        assert {p.name for p in written} == {
            f"{n}-{s}.png" for n in names for s in ("light", "dark")
        }
        built[page] = names
    for names in built.values():
        for name in names:
            images = {}
            for scheme in ("light", "dark"):
                im = Image.open(tmp_path / f"{name}-{scheme}.png").convert("RGBA")
                assert min(im.size) > 150, (name, im.size)
                alpha = im.getchannel("A")
                assert alpha.getextrema()[1] == 255
                colours = {c for _, c in im.getcolors(1_000_000)}
                assert len(colours) > 20, f"{name}-{scheme} looks blank"
                images[scheme] = im.tobytes()
            assert images["light"] != images["dark"], name
    embedded = set().union(*built.values())
    on_pages = set()
    for page in source_pages():
        on_pages |= set(
            re.findall(r"([\w-]+)-light\.png#only-light", page.read_text(encoding="utf-8"))
        )
    assert embedded == on_pages


# ---- the index page's images: Why, What --------------------------------------------------


class _Figures(HTMLParser):
    """The root page's figures: for each, its links, images (src, alt) and caption text."""

    def __init__(self) -> None:
        super().__init__()
        self.figures: list[dict] = []
        self._cap = False
        self._open = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "figure":
            self._open = True
            self.figures.append({"class": d.get("class", ""), "a": [], "img": [], "cap": ""})
        elif self._open and tag == "a":
            self.figures[-1]["a"].append(d.get("href"))
        elif self._open and tag == "img":
            self.figures[-1]["img"].append((d.get("src"), d.get("alt")))
        elif self._open and tag == "figcaption":
            self._cap = True

    def handle_endtag(self, tag):
        if tag == "figcaption":
            self._cap = False
        elif tag == "figure":
            self._open = False

    def handle_data(self, data):
        if self._cap:
            self.figures[-1]["cap"] += data


def _index_figures():
    parser = _Figures()
    parser.feed((SITE / "index.html").read_text(encoding="utf-8"))
    return parser.figures


def test_index_has_a_figure_each_for_why_what_and_how_in_that_order():
    text = (SITE / "index.html").read_text(encoding="utf-8")
    figures = _index_figures()
    # the supervisor's choice (WP28-decisions): the planted ternary is the story figure of the Why
    # section, and the plain Why image is gone (the assistant's call on the reviewer's first point)
    assert [f["class"].split()[0] if f["class"] else "" for f in figures] == ["why", "wide"]
    assert "story" in figures[0]["class"].split()
    srcs = [f["img"][0][0] for f in figures]
    assert srcs == ["ternary-planted-light.png", "figure1.png"]
    sections = [text.index(f"<h2>{h}</h2>") for h in ("Why", "What")]
    assert sections == sorted(sections)
    for h, f in zip(("Why", "What"), figures, strict=True):
        start = text.index(f"<h2>{h}</h2>")
        assert text.index(f["img"][0][0], start) < (
            text.index("<h2>", start + 5) if "<h2>" in text[start + 5 :] else len(text)
        ), f"{h}: the figure sits in its own section"
    assert "<script" not in text.lower()


def test_index_images_have_alt_text_captions_and_full_size_links():
    figures = _index_figures()
    story, what = figures
    assert [a for a in story["a"]] == ["ternary-planted-light.png", "ternary-planted-dark.png"]
    assert [i[0] for i in story["img"]] == ["ternary-planted-light.png", "ternary-planted-dark.png"]
    assert "constructed table" in story["cap"] and "three terms" in story["cap"]
    assert "larger when nearer the frontier" in story["cap"] and "full size" in story["cap"]
    assert story["cap"].count(". ") == 1  # one sentence, then the link note
    assert not any("why-regions" in i[0] for f in figures for i in f["img"])
    assert what["a"] == ["figure1.png"]
    for f in figures:
        assert all(alt and len(alt) > 60 for _, alt in f["img"]), "alt text names what is shown"
        assert len(f["cap"].strip()) > 40
    assert "black arrow" in what["img"][0][1] and "black arrow" in what["cap"]
    for f in figures:  # plain links: each figure's link is the file the image shows
        assert [i[0] for i in f["img"]] == f["a"]
    # in the dark scheme the light twin is hidden (and the dark one shown), by CSS alone
    css = (SITE / "index.html").read_text(encoding="utf-8")
    assert "figure.why .only-dark { display: none; }" in css
    assert "figure.why .only-light { display: none; }" in css


def test_assembled_index_images_exist_and_links_resolve(assembled):
    for f in _index_figures():
        for href in f["a"] + [i[0] for i in f["img"]]:
            assert (assembled / href).is_file(), href
            assert (assembled / href).stat().st_size > 10_000, href


# ---- the Why image generator ------------------------------------------------------------------


@pytest.fixture(scope="module")
def why_fit():
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_site_figures as bsf

    return bsf, bsf.fit_why()


def test_why_regions_partition_the_triangle_and_there_are_three_terms(why_fit):
    import numpy as np

    bsf, fit = why_fit
    assert fit["W"].shape == (3, 3) and np.allclose(fit["W"].sum(axis=1), 1.0, atol=1e-6)
    pts, reg = bsf.regions(fit, fit["spread"], n=120)
    assert np.allclose(pts.sum(axis=1), 1.0) and (pts > 0).all()  # inside the triangle
    assert set(np.unique(reg)) == {0, 1, 2}, "three regions, every one non-empty"
    # exact: each position is in the region of the term that is the largest affine piece there
    a = fit["W"] @ fit["colmean"] - fit["beta"]
    g = a + fit["spread"] * (np.log(pts) @ fit["W"].T)
    assert (g.argmax(axis=1) == reg).all()
    # the planar projection is the barycentric one: corners to corners, equal sides
    x, y = bsf.project([1, 0, 0], [0, 1, 0], [0, 0, 1])
    assert np.allclose(x, [0.5, 0, 1]) and np.allclose(y, [np.sqrt(3) / 2, 0, 0])


def test_why_labels_come_from_the_exponents(why_fit):
    import numpy as np

    bsf, fit = why_fit
    W = fit["W"]
    labels = {k: bsf.says(W[k]).replace("\n", " ") for k in range(3)}
    trade_all = [k for k in range(3) if labels[k] == "all three trade"]
    assert len(trade_all) == 1, labels
    assert (W[trade_all[0]] > bsf.BIG).all()
    for k in set(range(3)) - set(trade_all):
        big = [f"metric {j + 1}" for j in np.argsort(-W[k]) if W[k, j] > bsf.BIG]
        assert labels[k] == f"{big[0]} trades against {big[1]}", (labels[k], W[k])
    # the same words after permuting the metrics' names would follow the exponents, not a table
    assert bsf.says(np.array([0.1, 0.45, 0.45])) == "metric 2 trades\nagainst metric 3"
    assert bsf.says(np.array([0.3, 0.3, 0.4])) == "all three trade"
    assert bsf.colours(W)[trade_all[0]] == bsf.AMBER


@pytest.mark.slow
def test_why_figure_files_have_the_expected_size_and_no_overlay_by_default(tmp_path, why_fit):
    import inspect

    from PIL import Image

    bsf, fit = why_fit
    assert inspect.signature(bsf.build).parameters["lines"].default is False
    assert inspect.signature(bsf.draw).parameters["lines"].default is False
    plain = bsf.build(tmp_path / "plain", fit=fit)
    assert {p.name for p in plain.values()} == {
        "why-regions-light.png",
        "why-regions-dark.png",
    }
    for scheme, path in plain.items():
        with Image.open(path) as im:
            assert im.size == (round(bsf.FIGSIZE[0] * bsf.DPI), round(bsf.FIGSIZE[1] * bsf.DPI))
            assert im.mode == "RGBA" and im.getpixel((2, 2))[3] == 0, "transparent background"
        assert path.stat().st_size > 30_000, scheme
    # the default draws no line and no star; the option adds them (stars: one per term)
    import matplotlib.pyplot as plt

    fig = bsf.draw(fit, "light")
    ax = fig.axes[0]
    n_default = len(ax.collections)
    plt.close(fig)
    fig = bsf.draw(fit, "light", lines=True)
    ax = fig.axes[0]
    assert len(ax.collections) > n_default, "the option adds the contours and the stars"
    plt.close(fig)
    assert "--lines" in bsf.__doc__ and "off by default" in bsf.__doc__


@pytest.mark.slow
def test_story_figure_is_the_planted_table_with_the_overlay(tmp_path, why_fit):
    """The root page's story figure: the same planted fit as the Why image, drawn with lines."""
    bsf, fit = why_fit
    paths = bsf.build_story(tmp_path, fit=fit)
    assert {p.name for p in paths.values()} == {
        "ternary-planted-light.png",
        "ternary-planted-dark.png",
    }
    assert all(p.stat().st_size > 30_000 for p in paths.values())


def test_why_lines_overlay_is_the_fixed_total_function(why_fit):
    """Option on: at the total fixed, term k's exponent vector is where its own piece peaks."""
    import numpy as np

    bsf, fit = why_fit
    W = fit["W"]
    a = W @ fit["colmean"] - fit["beta"]
    comp = bsf.shares(fit, 1.0)
    assert np.allclose(comp.sum(axis=1), 1.0)
    # log V = s log L + f(c), exactly (the identity the overlay rests on)
    Y = np.exp(fit["U"] - fit["colmean"])
    f = (a + np.log(comp) @ W.T).max(axis=1)
    assert np.abs(np.log(Y.sum(axis=1)) + f - fit["logv"]).max() < 1e-8
    # each piece is largest at c = w_k among all c on the simplex (weighted vs arithmetic mean)
    rng = np.random.default_rng(0)
    c = rng.dirichlet(np.ones(3), size=2000)
    for k in range(3):
        wk = W[k]
        assert wk @ np.log(np.clip(wk, 1e-300, None)) >= (np.log(c) @ wk).max() - 1e-12


def _label_boxes(bsf, fit, scheme):
    """Each label's box in plane units (from the renderer), the regions' map and the triangle."""
    import matplotlib.pyplot as plt

    fig = bsf.draw(fit, scheme)
    ax = fig.axes[0]
    fig.canvas.draw()
    inv = ax.transData.inverted()
    boxes = {}
    for t in ax.texts:
        gid = t.get_gid() or ""
        if gid.startswith("why-label-"):
            bb = t.get_bbox_patch().get_window_extent(fig.canvas.get_renderer())
            (x0, y0), (x1, y1) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
            boxes[int(gid.rsplit("-", 1)[1])] = (x0, y0, x1, y1, t.get_text(), t.get_fontsize())
    plt.close(fig)
    return boxes


@pytest.mark.slow
@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_why_labels_lie_wholly_inside_their_own_region_and_do_not_overlap(why_fit, scheme):
    import numpy as np

    bsf, fit = why_fit
    boxes = _label_boxes(bsf, fit, scheme)
    assert set(boxes) == {0, 1, 2}
    for k, (x0, y0, x1, y1, text, size) in boxes.items():
        assert text.replace("\n", " ") == bsf.says(fit["W"][k]).replace("\n", " ")
        assert size >= 14.0, "legible when the page shrinks the image to a phone's width"
        # the box's corners, edge midpoints and a lattice inside it all fall in the label's region
        gx, gy = np.meshgrid(np.linspace(x0, x1, 9), np.linspace(y0, y1, 9))
        top = gy / bsf.SQ3
        right = gx - top / 2.0
        left = 1.0 - top - right
        assert (top > 0).all() and (left > 0).all() and (right > 0).all(), (
            k,
            "inside the triangle",
        )
        reg = bsf.region_of(fit, fit["spread"], top, left, right)[0]
        assert (reg == k).all(), (k, "the label crosses a border")
    for i in range(3):
        for j in range(i + 1, 3):
            a, b = boxes[i], boxes[j]
            assert a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1], (i, j)


@pytest.mark.slow
def test_why_label_placement_is_the_same_in_both_schemes(why_fit):
    bsf, fit = why_fit
    light, dark = _label_boxes(bsf, fit, "light"), _label_boxes(bsf, fit, "dark")
    assert light == dark


@pytest.mark.slow
def test_why_image_is_drawn_by_the_package_function(why_fit, monkeypatch):
    """WP18 R-3: one implementation, two consumers; no second projection in the script."""
    import matplotlib.pyplot as plt

    from hyperbolic_trade_space import plotting

    bsf, fit = why_fit
    text = (ROOT / "scripts" / "build_site_figures.py").read_text(encoding="utf-8")
    assert "def project" not in text and "def place_labels" not in text
    calls = []
    real = plotting.plot_ternary
    monkeypatch.setattr(bsf, "plot_ternary", lambda *a, **k: calls.append(k) or real(*a, **k))
    plt.close(bsf.draw(fit, "dark", lines=True))
    assert len(calls) == 1 and calls[0]["lines"] is True and calls[0]["scheme"] == "dark"
    assert bsf.project is plotting._ternary_project


def test_site_does_not_import_a_ternary_package():
    text = (ROOT / "scripts" / "build_site_figures.py").read_text(encoding="utf-8")
    assert "import mpltern" not in text and "projection=" not in text
    assert "mpltern" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
