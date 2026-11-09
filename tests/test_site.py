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
CONTRACT = tomllib.loads((ROOT / "work-packages" / "interface-contract.toml").read_text())
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
    "index.md": 250,
    "getting-started.md": 400,
    "user-guide/overview.md": 500,
    "user-guide/conditioning.md": 700,
    "user-guide/fitting.md": 800,
    "user-guide/tensions.md": 700,
    "user-guide/chart.md": 600,
    "user-guide/prediction.md": 350,
    "user-guide/termination.md": 600,
    "user-guide/limitations.md": 500,
    "api.md": 300,
    "examples.md": 400,
    "theory.md": 700,
    "further-reading.md": 300,
}
TOTAL_BUDGET = 7600
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
    return yaml.load(path.read_text(), Loader=_Loader)


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
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(match.group(1)) if match else {}


def punch_list_urls() -> set[str]:
    """URLs under 'Expected-at-release links' of the punch list."""
    text = PUNCH_LIST.read_text()
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
    parser.feed(path.read_text())
    return parser.hrefs


MD_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def md_links(path: Path) -> list[str]:
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
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
    """Words of a page outside fenced code blocks, tables and HTML comments."""
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
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
        text = re.sub(r"```.*?```", "", page.read_text(), flags=re.S)
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
        assert not page.read_text().startswith("---"), page.name


def test_api_reference_names_equal_the_contract():
    text = (DOCS / "api-reference.md").read_text()
    names = re.findall(r"^::: hyperbolic_trade_space\.(\w+)\s*$", text, re.M)
    assert sorted(names) == sorted(CONTRACT["package"]["public_names"])
    assert len(names) == len(set(names))


def test_citations_resolve():
    bib = (DOCS / "references.bib").read_text()
    keys = set(re.findall(r"^@\w+\{([^,\s]+),", bib, re.M))
    cited = set()
    for path in source_pages():
        for group in re.findall(r"\[(@[^\]]+)\]", path.read_text()):
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
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
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


def test_docsite_pages_do_not_cite_into_the_paper():
    """G9 withdrawn: no link from a docsite page into a paper section; paper references by stable
    keys are deferred (punch list)."""
    for path in source_pages():
        for href in md_links(path):
            assert "paper/" not in href and "paper_sections" not in href, f"{path.name}: {href}"


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


def test_root_and_paper_links_classified():
    """Every link on the two hand-written pages is internal and resolvable, or external and
    either the repository or a punch-list URL."""
    expected = punch_list_urls()
    repo = "https://github.com/DynamicalSystemsGroup/hyperbolic-trade-space"
    for rel, page_url in (("index.html", "/"), ("paper/index.html", "/paper/")):
        for href in html_links(SITE / rel):
            if is_external(href):
                assert href.startswith(repo) or href in expected, f"{rel}: unlisted external {href}"
                continue
            route = _resolve_site_href(page_url, href)
            assert route.startswith(urlparse(PUBLIC_URL).path)
            sub = route[len(urlparse(PUBLIC_URL).path) :]
            if sub.startswith("docs/"):
                continue  # the docsite; checked on the assembled site
            assert _site_file_for(route, SITE) is not None, f"{rel}: {href} does not resolve"


def test_root_index_is_thin_and_has_the_cards():
    text = (SITE / "index.html").read_text()
    assert "<script" not in text.lower()
    assert "prefers-color-scheme: dark" in text
    assert "Start wherever suits you" in text
    low = text.lower()
    order = [
        low.index(k) for k in ("<h2>why</h2>", "<h2>what</h2>", "<h2>how</h2>", 'class="cards"')
    ]
    assert order == sorted(order), "order: why, what, how, cards"
    assert (
        "A map of the mathematics: assumptions, the single-term core, the chart and its uses, "
        "the multi-facet extension, the open questions"
    ) in text
    for needle in ("scikit-learn", "unsupervised", "feature engineering", "pca"):
        assert needle in low, needle
    for banned in ("sympy", "worked example", "chatgpt", "openai"):
        assert banned not in low, banned
    figure = [h for h in html_links(SITE / "index.html") if h.endswith(".webp")]
    assert figure and all((SITE / h).is_file() for h in figure)
    hrefs = html_links(SITE / "index.html")
    for href in ("paper/", "docs/", "docs/api-reference/"):
        assert href in hrefs
    assert any(h.endswith("hyperbolic-trade-space") for h in hrefs), "repository link"
    assert "New card" in text
    assert "pypi.org" not in text.lower()
    paper = (SITE / "paper" / "index.html").read_text()
    assert "The paper is in preparation" in paper
    assert "../docs/" in html_links(SITE / "paper" / "index.html")
    assert "../" in html_links(SITE / "paper" / "index.html")
    assert "working draft" not in (text + paper).lower()


def test_punch_list_covers_post_release_checks():
    text = PUNCH_LIST.read_text()
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
def assembled(tmp_path_factory) -> Path:
    if not HAVE_MKDOCS:
        pytest.skip("the docs dependency group is not installed (mkdocs not importable)")
    if not ASSEMBLE.is_file():
        pytest.skip("scripts/assemble_site.py has not been delivered yet")
    out = tmp_path_factory.mktemp("site")
    generated = tmp_path_factory.mktemp("generated")  # the paper's pages, kept out of build/
    result = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--out", str(out), "--generated-dir", str(generated)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]
    return out


def test_assembled_layout(assembled):
    for rel in ("index.html", "docs/index.html", "paper/index.html"):
        assert (assembled / rel).is_file(), rel
    assert (assembled / "index.html").read_text() == (SITE / "index.html").read_text()
    assert (assembled / "paper-map.webp").is_file()
    assert (assembled / "paper" / "index.html").read_text() == (
        SITE / "paper" / "index.html"
    ).read_text()


def test_every_link_in_the_assembled_site_resolves(assembled):
    expected = punch_list_urls()
    base = urlparse(PUBLIC_URL).path
    problems = []
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
                problems.append((rel_url, href))
    assert not problems, problems[:20]


def test_math_markers_in_built_pages(assembled):
    html = (assembled / "docs" / "theory" / "index.html").read_text()
    assert 'class="arithmatex"' in html
    assert "mathjax@" in html
    for page in source_pages():
        if re.search(r"\$[^$\n]+\$", page.read_text()):
            rel = page.relative_to(DOCS).with_suffix("").as_posix()
            built = (assembled / "docs" / rel / "index.html").read_text()
            assert 'class="arithmatex"' in built, f"{rel}: inline math is not rendered"


def test_no_world_lines_in_built_pages(assembled):
    for html in (assembled / "docs").rglob("index.html"):
        assert "world-line" not in html.read_text(), html


def test_citations_render_and_further_reading_lists_the_references(assembled):
    html = (assembled / "docs" / "further-reading" / "index.html").read_text()
    assert "[@" not in re.sub(r"<code.*?</code>", "", html, flags=re.S)
    assert "<ol" in html or '<li id="' in html or "references" in html.lower()
    for key_text in ("Boyd", "Hoburg"):
        assert key_text in html, key_text


def test_api_reference_renders_every_public_name(assembled):
    html = (assembled / "docs" / "api-reference" / "index.html").read_text()
    for name in CONTRACT["package"]["public_names"]:
        assert f"hyperbolic_trade_space.{name}" in html, name
    assert "doc-class" in html and "doc-function" in html


def test_generated_pages_in_the_build(assembled):
    for name in CONTRACT["docs"]["generated_pages"]:
        stem = name[: -len(".md")]
        assert (assembled / "docs" / "generated" / stem / "index.html").is_file()
    # OD1: derivations and verification are the paper's build, not the docsite's
    assert sorted(p.name for p in (assembled / "docs" / "generated").iterdir()) == ["glossary"]
    gen = CONTRACT["derivation"]["generated_dir"]
    for name in CONTRACT["derivation"]["generated_pages"]:
        assert (ROOT / gen / name).is_file()
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
    problems = {p.relative_to(DOCS).as_posix(): _refs(p.read_text()) for p in source_pages()}
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
        text = path.read_text()
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
    text = PUNCH_LIST.read_text()
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
