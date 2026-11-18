"""The paper slot at ``/paper/`` (WP65 specification, 3.2 to 3.4): the abstract page, a pinned
artefact with its banner line, the fallback, the root card's line per mode, and a composer that
never builds the paper. No network: a fetch is a fake, and an unreachable URL is a patched
``urlopen``."""

from __future__ import annotations

import hashlib
import html
import io
import json
import re
import sys
import tarfile
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_site  # noqa: E402
import paper_abstract  # noqa: E402
import paper_keys  # noqa: E402
import site_metadata  # noqa: E402
import stage_site  # noqa: E402

REPO = "https://github.com/DynamicalSystemsGroup/tradespace"
MODES = {
    "working": {
        "pin": "paper-working-20261120",
        "venue": "",
        "round": 0,
        "date": "2026-11-20",
        "banner": "Working paper · paper-working-20261120 · 2026-11-20 · DOI 10.5281/zenodo.123",
    },
    "submitted": {
        "pin": "paper-submitted-ieee-tse",
        "venue": "ieee-tse",
        "round": 0,
        "date": "2026-12-01",
        "banner": "Submitted to ieee-tse · paper-submitted-ieee-tse · 2026-12-01 · DOI "
        "10.5281/zenodo.123",
    },
    "revision": {
        "pin": "paper-revision-ieee-tse-r2",
        "venue": "ieee-tse",
        "round": 2,
        "date": "2027-03-15",
        "banner": "Revision 2 for ieee-tse · paper-revision-ieee-tse-r2 · 2027-03-15 · DOI "
        "10.5281/zenodo.123",
    },
}
DOI = "10.5281/zenodo.123"
PAGES = {
    "index.html": '<!DOCTYPE html><html><head><title>p</title></head><body class="x">'
    '<h2 id="thm-kkt">KKT</h2></body></html>',
    "supporting-material/index.html": '<html><body><h2 id="appendix-e">E</h2></body></html>',
    "build/app.js": "console.log(1)",
}


# --- fixtures: a manifest, a mode file, an artefact ------------------------------------------


def _keys_file(tmp_path) -> Path:
    """The committed manifest when it exists, else a manifest of the two keys the pages carry."""
    path = tmp_path / "committed-keys.json"
    if paper_keys.MANIFEST.is_file():
        path.write_bytes(paper_keys.MANIFEST.read_bytes())
    else:
        path.write_text(
            paper_keys.canonical({"appendix-e": "paper/supporting-material/", "thm-kkt": "paper/"}),
            encoding="utf-8",
        )
    return path


def _tarball(pages=PAGES) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for name, text in pages.items():
            data = text.encode("utf-8")
            info = tarfile.TarInfo(f"./{name}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def _artefact(tmp_path, keys: bytes, pages=PAGES) -> Path:
    """``paper-html.tar.gz`` with ``paper-keys.json`` beside it, as the pin's release holds them."""
    folder = tmp_path / "release"
    folder.mkdir(exist_ok=True)
    (folder / "paper-html.tar.gz").write_bytes(_tarball(pages))
    (folder / "paper-keys.json").write_bytes(keys)
    return folder / "paper-html.tar.gz"


def _mode_file(tmp_path, mode="working", sha256="") -> Path:
    path = tmp_path / "mode.toml"
    if mode == "abstract":
        fields = {"pin": "", "venue": "", "round": 0, "date": ""}
        doi = ""
    else:
        fields = MODES[mode]
        doi = DOI
    path.write_text(
        "schema = 1\n"
        f'mode = "{mode}"\n'
        f'pin = "{fields["pin"]}"\n'
        f'venue = "{fields["venue"]}"\n'
        f"round = {fields['round']}\n"
        f'date = "{fields["date"]}"\n'
        f'doi = "{doi}"\n'
        f'sha256 = "{sha256}"\n',
        encoding="utf-8",
    )
    return path


def _pinned(tmp_path, mode="working", sha256=None, keys=None):
    """A mode file in ``mode``, the committed keys and an artefact whose checksum it records."""
    keys_file = _keys_file(tmp_path)
    artefact = _artefact(tmp_path, keys if keys is not None else keys_file.read_bytes())
    digest = hashlib.sha256(artefact.read_bytes()).hexdigest()
    mode_file = _mode_file(tmp_path, mode, sha256 or digest)
    return mode_file, keys_file, artefact


def _visible(page: str) -> str:
    """The text a reader sees: the body, inline tags dropped, block tags as spaces."""
    body = page.split("<body", 1)[-1].split(">", 1)[-1] if "<body" in page else page
    body = re.sub(r"</?(?:a|code|strong|span|em|b)\b[^>]*>", "", body)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", body)).split())


# --- the abstract page (3.3) -----------------------------------------------------------------


@pytest.fixture(scope="module")
def abstract_page() -> str:
    return paper_abstract.render()


def test_abstract_page_has_the_title_author_abstract_and_build_line(abstract_page):
    data = paper_abstract.front_matter()
    title = " ".join(data["title"].split())
    assert f"<h1>{html.escape(title)}</h1>" in abstract_page
    assert '<p class="byline">Michael Zargham, Dynamical Systems Group</p>' in abstract_page
    paragraphs = paper_abstract.paragraphs(data["abstract"])
    assert paragraphs and all(
        f"<p>{html.escape(p, quote=False)}</p>" in abstract_page for p in paragraphs
    )
    first = paper_abstract.first_sentence(data["abstract"])
    assert first.endswith(".") and first in paragraphs[0]
    assert f'<meta name="description" content="{html.escape(first)}">' in abstract_page
    assert (
        "The paper is iterated towards release on the paper branch of the repository and builds "
        "from it with uv run myst build --html in paper/."
    ) in _visible(abstract_page)
    assert f'<a href="{REPO}/tree/paper"><code>paper</code> branch</a>' in abstract_page
    assert 'class="fallback"' not in abstract_page


def test_abstract_page_has_no_forbidden_word_and_no_date(abstract_page):
    template = paper_abstract.TEMPLATE.read_text(encoding="utf-8")
    for text in (abstract_page, template):
        low = text.lower()
        for word in ("forthcoming", "in preparation", "coming soon", "working draft"):
            assert word not in low, word
        visible = _visible(text)
        assert not re.search(r"\b(?:19|20)\d{2}\b", visible), "a year"
        assert not re.search(r"\b\d{4}-\d{2}-\d{2}\b", visible), "an ISO date"
        months = "January|February|March|April|May|June|July|August|September|October|November"
        assert not re.search(rf"\b(?:{months}|December)\s+\d", visible), "a month and day"


def test_abstract_page_has_the_docs_and_root_cards(abstract_page):
    doors = re.search(r'<div class="doors">(.*?)</div>', abstract_page, re.S).group(1)
    cards = re.findall(r'<a class="card" href="([^"]+)">(.*?)</a>', doors, re.S)
    assert [href for href, _ in cards] == ["../docs/getting-started/", "../"], cards
    assert all(re.fullmatch(r"<strong>[^<]+</strong><span>[^<]+</span>", b) for _, b in cards)
    assert cards[0][1].startswith("<strong>Use the code</strong>")
    root = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    for rule in (".doors {", ".card {", ".card strong {", ".card span {"):
        root_rule = re.search(re.escape(rule) + r"[^}]*}", root).group(0)
        assert root_rule in abstract_page, f"the card style is the root page's: {rule}"


def test_abstract_page_has_no_script_and_both_colour_schemes(abstract_page):
    """No executable script: the one ``<script>`` is the JSON-LD data block of the metadata."""
    low = re.sub(r'<script type="application/ld\+json">.*?</script>', "", abstract_page, flags=re.S)
    low = low.lower()
    assert "<script" not in low and "javascript:" not in low and " on" + "click" not in low
    assert abstract_page.count("<script") == 1
    assert "color-scheme: light dark" in abstract_page
    assert "@media (prefers-color-scheme: dark)" in abstract_page
    root = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    tokens = re.search(
        r":root \{.*?\n  \}\n  @media \(prefers-color-scheme: dark\) \{.*?\n  \}", root, re.S
    )
    assert tokens.group(0) in abstract_page, "the root page's colour tokens, light and dark"
    assert '<link rel="icon" href="data:,">' in abstract_page
    assert '<meta property="og:url" content="' in abstract_page


@pytest.mark.parametrize(
    "abstract",
    [
        "The cost is $x^2$ here.",
        "As {cite:p}`boyd2007` shows.",
        "See [the docs](https://example.org).",
        "See https://example.org for more.",
        "A <b>bold</b> claim.",
        "A `code` span.",
    ],
)
def test_abstract_with_markup_fails_the_render(tmp_path, abstract):
    nb = json.loads(paper_abstract.NOTEBOOK.read_text(encoding="utf-8"))
    nb["cells"] = [
        {
            "cell_type": "markdown",
            "id": "frontmatter",
            "metadata": {},
            "source": ["---\n", "title: A title\n", "abstract: |\n", f"  {abstract}\n", "---\n"],
        }
    ]
    path = tmp_path / "paper.ipynb"
    path.write_text(json.dumps(nb), encoding="utf-8")
    with pytest.raises(paper_abstract.AbstractMarkupError):
        paper_abstract.render(notebook=path)
    plain = tmp_path / "plain.ipynb"
    nb["cells"][0]["source"][3] = "  A plain first paragraph.\n\n  A second one.\n"
    plain.write_text(json.dumps(nb), encoding="utf-8")
    page = paper_abstract.render(notebook=plain)
    assert "<p>A plain first paragraph.</p>\n  <p>A second one.</p>" in page


# --- a pinned slot (3.2) ---------------------------------------------------------------------


def test_a_pinned_slot_unpacks_the_artefact_with_one_banner_line_per_page(tmp_path):
    mode_file, keys_file, artefact = _pinned(tmp_path)
    slot = assemble_site.resolve_slot("auto", artefact, mode_file, keys_file)
    assert (slot.slot, slot.pin, slot.reason) == ("pin", MODES["working"]["pin"], "")
    assert slot.docs_slot == "pin"
    out = tmp_path / "out"
    assemble_site.place_slot(out, slot)
    pages = sorted((out / "paper").rglob("*.html"))
    assert [p.relative_to(out / "paper").as_posix() for p in pages] == [
        "index.html",
        "supporting-material/index.html",
    ]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        assert text.count('class="hts-paper-banner"') == 1, page
        # The banner is installed by a script once the page has loaded (the theme's hydration
        # removes a static element placed after <body>; WP67's browser pass); the installer sits
        # directly before </body>.
        installer = assemble_site.banner_installer(assemble_site.banner_html(slot.mode))
        assert text.endswith(installer + "</body>\n</html>") or installer + "</body>" in text, page
        assert '<template id="hts-paper-banner-source"><style>' in text, page
        assert '</style><p class="hts-paper-banner"' in text, page
    assert (out / "paper" / "build" / "app.js").read_text(encoding="utf-8") == "console.log(1)"
    assert 'id="thm-kkt"' in (out / "paper" / "index.html").read_text(encoding="utf-8")
    assert not slot.staged.exists(), "the staging directory is removed once placed"


@pytest.mark.parametrize("mode", sorted(MODES))
def test_banner_names_mode_tag_date_and_doi(tmp_path, mode):
    mode_file, keys_file, artefact = _pinned(tmp_path, mode)
    slot = assemble_site.resolve_slot("auto", artefact, mode_file, keys_file)
    assert slot.slot == "pin", slot.reason
    assemble_site.place_slot(tmp_path / "out", slot)
    text = (tmp_path / "out" / "paper" / "index.html").read_text(encoding="utf-8")
    banner = re.search(r'<p class="hts-paper-banner"[^>]*>(.*?)</p>', text).group(1)
    assert banner == f'<a href="https://doi.org/{DOI}">{MODES[mode]["banner"]}</a>'
    assert assemble_site.banner_line(slot.mode) == MODES[mode]["banner"]


def _fallback_said(slot, out, capsys, why):
    """The fallback is said on the page (the abstract page, with the pin and the reason) and in
    the run (the slot line and a warning annotation)."""
    assert slot.slot == "fallback" and slot.docs_slot == "abstract"
    assert why in slot.reason
    assemble_site.place_slot(out, slot)
    page = (out / "paper" / "index.html").read_text(encoding="utf-8")
    assert "hts-paper-banner" not in page
    line = re.search(r'<p class="fallback">(.*?)</p>', page).group(1)
    assert _visible(line) == (
        f"The pin {slot.pin} was not reachable when the site was composed ({slot.reason}); "
        "its abstract follows."
    )
    assert page.index('class="fallback"') < page.index('class="label">Abstract')
    summary = out / "summary.md"
    assemble_site.report(slot, summary)
    printed = capsys.readouterr().out
    assert f"assemble_site: slot fallback {slot.pin} {slot.reason}" in printed
    assert "::warning" in printed
    assert "`fallback`" in summary.read_text(encoding="utf-8")


def test_checksum_mismatch_falls_back_and_says_so(tmp_path, capsys):
    mode_file, keys_file, artefact = _pinned(tmp_path, sha256="0" * 64)
    slot = assemble_site.resolve_slot("auto", artefact, mode_file, keys_file)
    assert slot.pin == MODES["working"]["pin"]
    _fallback_said(slot, tmp_path / "out", capsys, "checksum mismatch")


def test_unreachable_artefact_falls_back_and_says_so(tmp_path, capsys, monkeypatch):
    mode_file, keys_file, _ = _pinned(tmp_path)
    # a local artefact that is not there
    slot = assemble_site.resolve_slot("auto", tmp_path / "nowhere.tar.gz", mode_file, keys_file)
    _fallback_said(slot, tmp_path / "local", capsys, "unreachable")
    # the release, over the network: two attempts, then the fallback
    calls = []

    def refuse(url, timeout):
        calls.append((url, timeout))
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(assemble_site.urllib.request, "urlopen", refuse)
    monkeypatch.setattr(assemble_site.time, "sleep", lambda s: None)
    slot = assemble_site.resolve_slot("auto", None, mode_file, keys_file)
    _fallback_said(slot, tmp_path / "remote", capsys, "unreachable")
    pin = MODES["working"]["pin"]
    assert calls == [(f"{REPO}/releases/download/{pin}/paper-html.tar.gz", 60)] * 2
    # an artefact that unpacks but cannot be read as pages is as good as unreachable
    broken = {"index.html": "<html><body></body></html>", "._index.html": "\udcff"}
    bad = tmp_path / "bad"
    bad.mkdir()
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode="w:gz") as tar:
        for name, text in broken.items():
            raw = text.encode("utf-8", "surrogateescape")
            info = tarfile.TarInfo(f"./{name}")
            info.size = len(raw)
            tar.addfile(info, io.BytesIO(raw))
    (bad / "paper-html.tar.gz").write_bytes(data.getvalue())
    (bad / "paper-keys.json").write_bytes(keys_file.read_bytes())
    mode_file = _mode_file(tmp_path, "working", hashlib.sha256(data.getvalue()).hexdigest())
    slot = assemble_site.resolve_slot("auto", bad / "paper-html.tar.gz", mode_file, keys_file)
    _fallback_said(slot, tmp_path / "unreadable", capsys, "is not UTF-8 text")


def test_keys_mismatch_falls_back(tmp_path, capsys):
    mode_file, keys_file, artefact = _pinned(
        tmp_path, keys=paper_keys.canonical({"only-key": "paper/"}).encode("utf-8")
    )
    slot = assemble_site.resolve_slot("auto", artefact, mode_file, keys_file)
    _fallback_said(slot, tmp_path / "out", capsys, "keys mismatch")
    # the release's manifest is fetched beside the artefact and compared byte for byte
    fetched = {
        "paper-html.tar.gz": artefact.read_bytes(),
        "paper-keys.json": keys_file.read_bytes() + b" ",
    }
    slot = assemble_site.resolve_slot(
        "auto", None, mode_file, keys_file, fetcher=lambda url: fetched[url.rsplit("/", 1)[1]]
    )
    assert slot.slot == "fallback" and "keys mismatch" in slot.reason


def test_strict_slot_turns_a_fallback_into_exit_one(tmp_path, monkeypatch, capsys):
    mode_file, keys_file, artefact = _pinned(tmp_path, sha256="0" * 64)
    monkeypatch.setattr(assemble_site, "MODE_FILE", mode_file)
    monkeypatch.setattr(assemble_site, "KEYS_FILE", keys_file)
    composed = []
    monkeypatch.setattr(
        assemble_site,
        "assemble",
        lambda out, **kw: composed.append(kw["resolved"]) or (Path(out), kw["resolved"]),
    )
    out = tmp_path / "site"
    argv = ["--out", str(out), "--artefact", str(artefact)]
    assert assemble_site.main([*argv, "--strict-slot"]) == 1
    assert composed == [], "nothing is composed under --strict-slot"
    said = capsys.readouterr()
    assert "slot fallback" in said.out and "--strict-slot" in said.err
    assert assemble_site.main(argv) == 0, "without the flag a fallback still composes"
    assert [s.slot for s in composed] == ["fallback"]


def test_the_composer_never_runs_myst(tmp_path, monkeypatch):
    source = (ROOT / "scripts" / "assemble_site.py").read_text(encoding="utf-8")
    assert "myst" not in source.lower() and "execute_notebooks" not in source
    commands = []
    real_run = assemble_site.subprocess.run

    def record(cmd, *args, **kwargs):
        commands.append([str(c) for c in cmd])
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(assemble_site.subprocess, "run", record)
    monkeypatch.setattr(assemble_site.build_generated, "build", lambda *a, **k: None)
    slots = []

    def fake_mkdocs(cmd):
        commands.append(cmd)
        slots.append(assemble_site.os.environ[paper_keys.SLOT_VARIABLE])
        out = Path(cmd[cmd.index("-d") + 1])
        out.mkdir(parents=True)
        (out / "index.html").write_text("docs", encoding="utf-8")

    mode_file, keys_file, artefact = _pinned(tmp_path)
    for name, kwargs in (
        ("abstract", {"slot": "abstract"}),
        ("pin", {"artefact": artefact, "mode_file": mode_file, "keys_file": keys_file}),
    ):
        out, slot = assemble_site.assemble(
            tmp_path / name,
            mkdocs_runner=fake_mkdocs,
            generated_dir=tmp_path / "gen",
            docs_generated_dir=tmp_path / "docsgen",
            figures_builder=lambda out: None,
            site_figures_builder=lambda out: None,
            **kwargs,
        )
        assert slot.slot == name and (out / "paper" / "index.html").is_file()
    assert slots == ["abstract", "pin"], "the docs build sees the slot /paper/ holds"
    assert all("myst" not in " ".join(c).lower() for c in commands), commands


def test_root_card_line_per_mode():
    source = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    card = r'<a class="card" href="paper/"><strong>Read the paper</strong><span>([^<]+)</span></a>'
    assert re.findall(card, source) == ["the argument and the proofs"]
    source = site_metadata.apply(source, "")  # the composer's metadata block in the head
    pinned = assemble_site.root_page(assemble_site.Slot("pin", pin="paper-working-20261120"))
    assert pinned == source
    for slot in (assemble_site.Slot("abstract"), assemble_site.Slot("fallback", "p", "r")):
        page = assemble_site.root_page(slot)
        assert re.findall(card, page) == ["its abstract; the paper is iterated towards release"]
        assert (
            page.replace(
                "its abstract; the paper is iterated towards release", "the argument and the proofs"
            )
            == source
        ), "only the card's line changes"


def test_paper_flag_is_gone(capsys):
    for main in (assemble_site.main, stage_site.main):
        for argv in (["--paper", "placeholder"], ["--paper", "strict"], ["--paper"]):
            with pytest.raises(SystemExit) as exc:
                main(argv)
            assert exc.value.code == 2, (main, argv)
    assert "--paper" in capsys.readouterr().err
    for script in ("assemble_site.py", "stage_site.py"):
        assert "--paper" not in (ROOT / "scripts" / script).read_text(encoding="utf-8"), script
