"""WP8a: generated pages, site assembly and the staging server (no network, no mkdocs)."""

import importlib.util
import sys
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_site  # noqa: E402
import build_generated  # noqa: E402
import stage_site  # noqa: E402

from derivation import axioms as AX  # noqa: E402
from derivation import run as R  # noqa: E402

FAKE_COLLECT = (
    "tests/test_derivation.py::test_a\n"
    "tests/test_estimator.py::test_b\n"
    "tests/test_sklearn_compat.py::test_sklearn_compatible_estimator[x-check_a]\n"
    "src/tradespace/solvers.py::tradespace.solvers.f\n"
    "\n3 tests collected in 0.1s\n"
)


@pytest.fixture(scope="module")
def pages(tmp_path_factory):
    out = tmp_path_factory.mktemp("gen")
    docs_out = tmp_path_factory.mktemp("docsgen")
    build_generated.build(out, collect_runner=lambda: FAKE_COLLECT, docs_out=docs_out)
    return {
        "derivations": (out / "derivations.md").read_text(encoding="utf-8"),
        "verification": (out / "verification.md").read_text(encoding="utf-8"),
        "glossary": (docs_out / "glossary.md").read_text(encoding="utf-8"),
    }


@pytest.mark.slow
def test_every_lemma_title_and_statement(pages):
    for mod in R.CHAIN:
        n = R.lemma_number(mod)
        assert f"### L{n}\n" in pages["derivations"]
        assert mod.TITLE in pages["derivations"]
        assert mod.STATEMENT in pages["derivations"]
    assert len(R.CHAIN) == 22  # L21 the tension (WP42), L22 the small-temperature lemma (WP46)


def test_ledger_equals_axioms(pages):
    text = pages["derivations"]
    for a in AX.AXIOMS.values():
        assert f"- **{a.name}** ({a.tag}): {a.statement}." in text
        for field in (a.role, a.failure_mode, a.citation):
            if field:
                assert field in text


def test_cited_context_reported_apart(pages):
    text = pages["derivations"]
    head = "### Cited context (no step depends on it)"
    assert head in text
    block = text[text.index(head) :]
    block = block[: block.index("\n### ", 1)] if "\n### " in block[1:] else block
    for name, why in AX.CITED_CONTEXT.items():
        assert f"- **{name}** (INHERITED)" in block
        assert f"Why no step depends on it: {why}." in block
        inherited = text[text.index("### INHERITED\n") : text.index(head)]
        assert f"- **{name}** (" not in inherited


def test_headings_present(pages):
    for h in build_generated.DERIVATION_HEADINGS:
        assert f"\n## {h}\n" in pages["derivations"]
    for h in build_generated.VERIFICATION_HEADINGS:
        assert f"\n## {h}\n" in pages["verification"]


def test_verification_content(pages):
    v = pages["verification"]
    assert "collects 4 tests" in v
    assert "| Derivation and ledger | 1 |" in v
    assert "| Package doctests | 1 |" in v
    assert "check_regressor_multioutput" in v  # documented expected failure with its reason
    assert "gaps ledger" in v and build_generated.GAPS_LEDGER in v
    for mod in R.CHAIN:
        assert f"L{R.lemma_number(mod)} PASS" in v


@pytest.mark.slow
def test_deterministic(tmp_path):
    for tag in ("a", "b"):
        build_generated.build(
            tmp_path / tag, collect_runner=lambda: FAKE_COLLECT, docs_out=tmp_path / (tag + "g")
        )
    for name in ("derivations.md", "verification.md"):
        assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes()
    assert (tmp_path / "ag" / "glossary.md").read_bytes() == (
        tmp_path / "bg" / "glossary.md"
    ).read_bytes()


def test_derivations_and_verification_leave_the_docsite():
    """OD1: the paper's build reads them from build/generated/, outside docs/ (mkdocs docs_dir)."""
    assert build_generated.DEFAULT_OUT == ROOT / "build" / "generated"
    assert not build_generated.DEFAULT_OUT.is_relative_to(ROOT / "docs")
    assert build_generated.DOCS_GENERATED == ROOT / "docs" / "generated"


# --- the glossary, compiled from glossary.yaml ----------------------------------------------------

GLOSSARY = ROOT / "glossary.yaml"
REGISTER_PHRASES = (
    "fitted reference surface",
    "supporting envelope",
    "Pareto boundary",
    "energy differential",
    "level offset",
    "term gap",
    "assignment margin",
    "stable radius",
    "participation threshold",
    "numerically zero",
)


def _write(tmp_path, text):
    path = tmp_path / "g.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def _entry(**over):
    e = {"id": "x", "term": "x", "short": "s", "register": "r", "formal": "f", "not": "n"}
    e.update(over)
    return e


def test_glossary_source_validates_and_has_every_register_phrase():
    entries = build_generated.load_glossary(GLOSSARY)
    terms = {e["term"].casefold() for e in entries}
    for phrase in REGISTER_PHRASES:
        assert phrase.casefold() in terms, phrase
    assert len(entries) >= 30


def test_glossary_page_is_exactly_the_yaml(pages):
    """Title, letter headings and one bullet per entry (term and short); nothing else."""
    entries = build_generated.load_glossary(GLOSSARY)
    lines = [ln for ln in pages["glossary"].splitlines() if ln.strip()]
    assert lines[0] == "# Glossary"
    bullets = [ln for ln in lines if ln.startswith("- ")]
    headings = [ln for ln in lines[1:] if ln.startswith("## ")]
    preamble = build_generated.load_glossary_preamble(GLOSSARY)
    assert lines[1] == " ".join(preamble.split()), "the preamble opens the page"
    assert len(bullets) + len(headings) + 2 == len(lines), "no free text beyond the yaml"
    assert len(bullets) == len(entries)
    for e in entries:
        assert f"- **{e['term'].strip()}**: {e['short'].strip()}" in bullets
    assert pages["glossary"] == build_generated.glossary_page(entries, preamble)
    # grouped alphabetically: headings ascend and each bullet sits under its own letter
    letters = [h[3:] for h in headings]
    assert letters == sorted(letters)
    current = None
    for ln in lines[2:]:  # lines[1] is the preamble
        if ln.startswith("## "):
            current = ln[3:]
        else:
            assert ln[len("- **")].upper() == current, ln
    terms = [ln[len("- **") : ln.index("**:")].casefold() for ln in bullets]
    assert terms == sorted(terms)


def test_glossary_validation_rejects_bad_sources(tmp_path):
    import yaml

    def load(entries):
        return build_generated.load_glossary(_write(tmp_path, yaml.safe_dump({"entries": entries})))

    assert load([_entry()])
    bad = {
        "missing field": [{k: v for k, v in _entry().items() if k != "formal"}],
        "unknown field": [_entry(extra="y")],
        "empty value": [_entry(short=" ")],
        "multi-line short": [_entry(short="a\nb")],
        "bad id": [_entry(id="Not A Slug")],
        "repeated id": [_entry(), _entry(term="y")],
        "repeated term": [_entry(), _entry(id="y")],
        "not a list": "text",
        "empty": [],
        "layer outside the three": [_entry(layer="nested")],
        "empty used_in": [_entry(used_in=" ")],
    }
    for label, entries in bad.items():
        with pytest.raises(ValueError):
            load(entries)
        assert label
    with pytest.raises(ValueError):
        build_generated.load_glossary(_write(tmp_path, yaml.safe_dump([_entry()])))
    # WP42: the layer, used_in and elsewhere fields and the preamble are accepted when well formed
    good = [_entry(layer="method", used_in="machine learning", elsewhere="optimization texts")]
    assert load(good)[0]["layer"] == "method"
    path = _write(tmp_path, yaml.safe_dump({"preamble": "Three layers.", "entries": good}))
    assert build_generated.load_glossary_preamble(path) == "Three layers."
    assert "Three layers." in build_generated.glossary_page(
        build_generated.load_glossary(path), "Three layers."
    )
    with pytest.raises(ValueError):
        build_generated.load_glossary(
            _write(tmp_path, yaml.safe_dump({"preamble": " ", "entries": good}))
        )


CLASS_WORDS = (
    "monomial",
    "posynomial",
    "generalized posynomial",
    "geometric program",
    "generalized geometric program",
)


def test_glossary_carries_the_class_words_and_the_withdrawn_phrases():
    """WP10 Amendment 4 (R-33, R-35): five class words are entries; the surface is posynomial
    and models the data, and the phrases withdrawn on the supervisor's direction are on its avoid
    list."""
    entries = {e["term"]: e for e in build_generated.load_glossary(GLOSSARY)}
    for term in CLASS_WORDS:
        assert term in entries, term
    assert "function" in entries["generalized posynomial"]["formal"]
    assert "problems" not in entries["generalized posynomial"]["formal"]
    surface = entries["fitted reference surface"]
    withdrawn = {a["phrase"] for a in surface["avoid"]}
    assert {"generalized posynomial reference surface", "model of the table"} <= withdrawn
    assert "data underlying the table" in surface["short"]
    lists = build_generated.load_glossary_lists(GLOSSARY)
    assert lists["stems"] and "posynomial" in lists["stems"]
    assert all(set(a) == {"term", "reason"} for a in lists["assumed"]) and lists["assumed"]


def test_generalized_geometric_program_is_the_sense_of_boyd_et_al_2007():
    """WP10 Amendment 5 (R-40): generalized posynomial objective and inequality constraints,
    monomial equalities (the tutorial's section 5.4); the older signomial use is in ``not``."""
    entries = {e["term"]: e for e in build_generated.load_glossary(GLOSSARY)}
    ggp = entries["generalized geometric program"]
    assert "section 5.4" in ggp["short"] and "Boyd et al. 2007" in ggp["short"]
    for part in ("generalized posynomial", "monomial constraints equal to one"):
        assert part in ggp["formal"], part
    assert "signomial" in ggp["not"] and "signomial" not in ggp["formal"]
    gp = entries["geometric program"]["not"]
    assert "assigning" not in gp and "not convex in the terms" in gp  # the fit is not membership


def test_glossary_page_shows_term_and_short_only_despite_the_new_fields():
    entries = build_generated.load_glossary(GLOSSARY)
    page = build_generated.glossary_page(entries)
    for e in entries:
        for item in e.get("avoid", []):
            assert item["reason"] not in page
        for alias in e.get("aliases", []):
            assert f"**{alias}**" not in page


def test_glossary_schema_aliases_avoid_assumed_stems(tmp_path):
    import yaml

    def load(entries, **lists):
        text = yaml.safe_dump({"entries": entries, **lists})
        return build_generated.load_glossary(_write(tmp_path, text))

    ok = _entry(aliases=["xs"], avoid=[{"phrase": "bad x", "reason": "why"}])
    assert load([ok], assumed=[{"term": "t", "reason": "r"}], stems=["s"])
    bad = {
        "alias not a list": [_entry(aliases="xs")],
        "empty alias list": [_entry(aliases=[])],
        "blank alias": [_entry(aliases=[" "])],
        "avoid without reason": [_entry(avoid=[{"phrase": "p"}])],
        "avoid as strings": [_entry(avoid=["p"])],
        "alias is another term": [_entry(), _entry(id="y", term="y", aliases=["x"])],
        "avoided phrase is a term": [_entry(avoid=[{"phrase": "x", "reason": "r"}])],
    }
    for label, entries in bad.items():
        with pytest.raises(ValueError):
            load(entries)
        assert label
    for lists in (
        {"assumed": [{"term": "t"}]},
        {"assumed": "t"},
        {"stems": [1]},
        {"stems": "s"},
        {"other": []},
    ):
        with pytest.raises(ValueError):
            load([_entry()], **lists)


def test_glossary_sorting_ignores_source_order(tmp_path):
    import yaml

    a = _entry(id="b", term="beta", short="second")
    b = _entry(id="a", term="alpha", short="first")
    p1 = _write(tmp_path, yaml.safe_dump({"entries": [a, b]}))
    page = build_generated.glossary_page(build_generated.load_glossary(p1))
    assert page == "# Glossary\n\n## A\n\n- **alpha**: first\n\n## B\n\n- **beta**: second\n"


def test_invalid_glossary_stops_the_build(tmp_path, capsys):
    bad = _write(tmp_path, "entries: []\n")
    with pytest.raises(ValueError):
        build_generated.build(
            tmp_path / "o",
            collect_runner=lambda: FAKE_COLLECT,
            docs_out=tmp_path / "d",
            glossary_path=bad,
        )
    assert not (tmp_path / "o" / "derivations.md").exists()


def test_expected_failures_loaded_match_test_module():
    spec = importlib.util.spec_from_file_location("sk", ROOT / "tests" / "test_sklearn_compat.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    got = build_generated.load_expected_failures()
    assert got["REGRESSOR_EXPECTED_FAILURES"] == mod.REGRESSOR_EXPECTED_FAILURES


def test_exit_nonzero_on_failing_lemma(monkeypatch, tmp_path, capsys):
    class Bad:
        __name__ = "derivation.lemma_99_bad"
        TITLE = "bad"
        STATEMENT = "bad"
        AXIOMS_USED = ()

        @staticmethod
        def derive(ctx):
            raise AssertionError("lemma failed")

        @staticmethod
        def verify(ctx):
            pass

    monkeypatch.setattr(R, "CHAIN", [Bad])
    assert build_generated.main(["--out", str(tmp_path / "o")]) == 1
    assert "FAILED" in capsys.readouterr().err
    assert not (tmp_path / "o" / "derivations.md").exists()


@pytest.mark.slow
def test_assemble_with_fake_mkdocs(tmp_path, monkeypatch):
    site = tmp_path / "src_site"
    site.mkdir()
    card = assemble_site.ROOT_CARD.format(assemble_site.ROOT_CARD_LINE_PINNED)
    (site / "index.html").write_text(f"<html>{card}</html>", encoding="utf-8")
    monkeypatch.setattr(assemble_site, "ROOT_INDEX", site / "index.html")
    seen, figures = [], []

    def fake(cmd):
        seen.append(cmd)
        out = Path(cmd[cmd.index("-d") + 1])
        out.mkdir(parents=True)
        (out / "index.html").write_text("docs", encoding="utf-8")

    out, slot = assemble_site.assemble(
        tmp_path / "out",
        mkdocs_runner=fake,
        generated_dir=tmp_path / "gen",
        collect_runner=lambda: FAKE_COLLECT,
        docs_generated_dir=tmp_path / "docsgen",
        figures_builder=figures.append,
        slot="abstract",
        renderer=lambda fallback=None: "<html>abstract</html>",
    )
    assert slot.slot == "abstract"
    assert figures == [tmp_path / "docsgen" / "figures"]
    assert (out / "index.html").read_text(encoding="utf-8") == (
        "<html>" + assemble_site.ROOT_CARD.format(assemble_site.ROOT_CARD_LINE_ABSTRACT) + "</html>"
    )
    assert (out / "docs" / "index.html").exists()
    assert (out / "paper" / "index.html").read_text(encoding="utf-8") == "<html>abstract</html>"
    assert (tmp_path / "gen" / "derivations.md").exists()
    assert (tmp_path / "docsgen" / "glossary.md").exists()
    assert "--strict" in seen[0] and "build" in seen[0]


@pytest.mark.slow
def test_assemble_fails_loudly_when_mkdocs_fails(tmp_path):
    def boom(cmd):
        raise RuntimeError("mkdocs failed")

    with pytest.raises(RuntimeError):
        assemble_site.assemble(
            tmp_path / "out",
            mkdocs_runner=boom,
            generated_dir=tmp_path / "gen",
            collect_runner=lambda: FAKE_COLLECT,
            docs_generated_dir=tmp_path / "docsgen",
            figures_builder=lambda out: None,
            slot="abstract",
        )


def _offline_stage(tmp_path, monkeypatch):
    """Stage with the slow steps faked (generated pages, figures, MkDocs) and the network refused,
    so a test sees only the slot the composer places."""
    monkeypatch.setattr(stage_site, "STAGE_DIR", tmp_path / "_stage")
    monkeypatch.setattr(assemble_site.build_generated, "build", lambda *a, **k: None)
    monkeypatch.setattr(assemble_site.build_figures, "build", lambda out: None)
    monkeypatch.setattr(assemble_site.build_site_figures, "build_all", lambda out: None)

    def fake_mkdocs(out_docs, runner=None, docs_slot="abstract"):
        Path(out_docs).mkdir(parents=True)
        (Path(out_docs) / "index.html").write_text(f"docs {docs_slot}", encoding="utf-8")

    def no_network(*args, **kwargs):
        raise AssertionError("staging reached for the network")

    monkeypatch.setattr(assemble_site, "run_mkdocs", fake_mkdocs)
    monkeypatch.setattr(assemble_site.urllib.request, "urlopen", no_network)


def test_stage_site_stages_the_abstract_page_offline(tmp_path, monkeypatch, capsys):
    _offline_stage(tmp_path, monkeypatch)
    assert stage_site.main([]) == 0
    assert "assemble_site: slot abstract - -" in capsys.readouterr().out
    stage = tmp_path / "_stage"
    page = (stage / "paper" / "index.html").read_text(encoding="utf-8")
    assert "<h1>Scaling Decision Analysis" in page and "iterated towards release" in page
    assert "hts-paper-banner" not in page and 'class="fallback"' not in page
    assert (stage / "docs" / "index.html").read_text(encoding="utf-8") == "docs abstract"
    assert "its abstract; the paper is iterated towards release" in (
        stage / "index.html"
    ).read_text(encoding="utf-8")
    assert stage_site.default_slot() == "abstract" and stage_site.default_slot("x") == "auto"


def test_stage_site_with_an_artefact_stages_the_pin(tmp_path, monkeypatch, capsys):
    import hashlib
    import io
    import tarfile

    _offline_stage(tmp_path, monkeypatch)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        data = b'<html><body><h2 id="thm-kkt">KKT</h2></body></html>'
        info = tarfile.TarInfo("./index.html")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    release = tmp_path / "release"
    release.mkdir()
    (release / "paper-html.tar.gz").write_bytes(buf.getvalue())
    keys = tmp_path / "paper-keys.json"
    keys.write_text(
        '{\n  "schema": 1,\n  "keys": {\n    "thm-kkt": "paper/"\n  }\n}\n', encoding="utf-8"
    )
    (release / "paper-keys.json").write_bytes(keys.read_bytes())
    mode = tmp_path / "mode.toml"
    mode.write_text(
        'schema = 1\nmode = "working"\npin = "paper-working-20261120"\nvenue = ""\nround = 0\n'
        'date = "2026-11-20"\ndoi = "10.5281/zenodo.123"\n'
        f'sha256 = "{hashlib.sha256(buf.getvalue()).hexdigest()}"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(assemble_site, "MODE_FILE", mode)
    monkeypatch.setattr(assemble_site, "KEYS_FILE", keys)
    assert stage_site.main(["--artefact", str(release / "paper-html.tar.gz")]) == 0
    assert "assemble_site: slot pin paper-working-20261120 -" in capsys.readouterr().out
    stage = tmp_path / "_stage"
    page = (stage / "paper" / "index.html").read_text(encoding="utf-8")
    assert "Working paper · paper-working-20261120 · 2026-11-20 · DOI 10.5281/zenodo.123" in page
    assert (stage / "docs" / "index.html").read_text(encoding="utf-8") == "docs pin"
    assert "the argument and the proofs" in (stage / "index.html").read_text(encoding="utf-8")


def test_assemble_refuses_repo_root():
    with pytest.raises(ValueError):
        assemble_site._check_out(ROOT)


def test_stage_server_serves_index_on_loopback(tmp_path):
    (tmp_path / "index.html").write_text("<html>hello</html>", encoding="utf-8")
    server = stage_site.serve_in_thread(tmp_path, port=0)
    try:
        host, port = server.server_address[:2]
        assert host == "127.0.0.1"
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as r:
            assert r.status == 200
            assert b"hello" in r.read()
    finally:
        server.shutdown()
        server.server_close()


def test_stage_no_build_reuses_existing(tmp_path):
    assert stage_site.stage(tmp_path, build=False) == (tmp_path, None)
