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

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
PUNCH_LIST = ROOT / "work-packages" / "release-punch-list.md"
CONTRACT = tomllib.loads((ROOT / "work-packages" / "interface-contract.toml").read_text())
GENERATED_PAGES = {f"generated/{n}" for n in CONTRACT["derivation"]["generated_pages"]}
PUBLIC_URL = CONTRACT["build"]["public_url"]
WORLDS = {"embodied", "symbolic", "formal"}

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
    return sorted(p for p in DOCS.glob("*.md"))


@pytest.fixture(scope="session")
def mkdocs_config() -> dict:
    return load_yaml(ROOT / "mkdocs.yml")


# --- configuration -----------------------------------------------------------------------------


def test_mkdocs_config_parses(mkdocs_config):
    cfg = mkdocs_config
    assert cfg["site_url"] == PUBLIC_URL + "docs/"
    assert cfg["theme"]["name"] == "material"
    assert cfg["theme"]["custom_dir"] == "overrides"
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
    assert pages == [
        "index.md",
        "why-and-how.md",
        "method.md",
        "generated/derivations.md",
        "preconditioning.md",
        "case.md",
        "generated/verification.md",
        "api.md",
        "api-reference.md",
        "limitations.md",
        "literature.md",
    ]
    contract_pages = set(CONTRACT["docs"]["pages"])
    assert contract_pages <= set(pages)
    assert set(pages) >= GENERATED_PAGES


def test_world_key_on_every_page():
    for path in source_pages():
        if path.name == "index.md":
            continue  # the home page maps all three worlds
        world = front_matter(path).get("world")
        assert world in WORLDS, f"{path.name}: front-matter world must be one of {sorted(WORLDS)}"


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
    for route in (
        "docs/",
        "docs/method/",
        "docs/generated/derivations/",
        "docs/generated/verification/",
        "docs/api-reference/",
        "docs/literature/",
        "paper/",
    ):
        assert f"`{route}`" in text, route
    assert "PyPI" in text and "release notes" in text.lower()


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
    result = subprocess.run(
        [sys.executable, str(ASSEMBLE), "--out", str(out)],
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
    for name in ("method", "preconditioning"):
        html = (assembled / "docs" / name / "index.html").read_text()
        assert 'class="arithmatex"' in html, name
    assert "mathjax@" in (assembled / "docs" / "method" / "index.html").read_text()


def test_world_lines_render(assembled):
    for name in (
        "why-and-how",
        "method",
        "preconditioning",
        "case",
        "api",
        "api-reference",
        "limitations",
        "literature",
        "generated/derivations",
        "generated/verification",
    ):
        html = (assembled / "docs" / name / "index.html").read_text()
        assert 'class="world-line"' in html, name


def test_citations_render_and_literature_lists_the_bibliography(assembled):
    html = (assembled / "docs" / "literature" / "index.html").read_text()
    bib = (DOCS / "references.bib").read_text()
    keys = re.findall(r"^@\w+\{([^,\s]+),", bib, re.M)
    assert len(keys) > 5
    assert "[@" not in re.sub(r"<code.*?</code>", "", html, flags=re.S)
    assert "<ol" in html or '<li id="' in html or "references" in html.lower()


def test_api_reference_renders_every_public_name(assembled):
    html = (assembled / "docs" / "api-reference" / "index.html").read_text()
    for name in CONTRACT["package"]["public_names"]:
        assert f"hyperbolic_trade_space.{name}" in html, name
    assert "doc-class" in html and "doc-function" in html


def test_generated_pages_in_the_build(assembled):
    for name in CONTRACT["derivation"]["generated_pages"]:
        stem = name[: -len(".md")]
        assert (assembled / "docs" / "generated" / stem / "index.html").is_file()
