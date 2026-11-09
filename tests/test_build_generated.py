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
    "src/hyperbolic_trade_space/solvers.py::hyperbolic_trade_space.solvers.f\n"
    "\n3 tests collected in 0.1s\n"
)


@pytest.fixture(scope="module")
def pages(tmp_path_factory):
    out = tmp_path_factory.mktemp("gen")
    docs_out = tmp_path_factory.mktemp("docsgen")
    build_generated.build(out, collect_runner=lambda: FAKE_COLLECT, docs_out=docs_out)
    return {
        "derivations": (out / "derivations.md").read_text(),
        "verification": (out / "verification.md").read_text(),
        "glossary": (docs_out / "glossary.md").read_text(),
    }


def test_every_lemma_title_and_statement(pages):
    for mod in R.CHAIN:
        n = R.lemma_number(mod)
        assert f"### L{n}\n" in pages["derivations"]
        assert mod.TITLE in pages["derivations"]
        assert mod.STATEMENT in pages["derivations"]
    assert len(R.CHAIN) == 14


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
    "facet gap",
    "assignment margin",
    "stable radius",
    "participation threshold",
    "numerically zero",
)


def _write(tmp_path, text):
    path = tmp_path / "g.yaml"
    path.write_text(text)
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
    assert len(bullets) + len(headings) + 1 == len(lines), "no free text beyond the yaml"
    assert len(bullets) == len(entries)
    for e in entries:
        assert f"- **{e['term'].strip()}**: {e['short'].strip()}" in bullets
    assert pages["glossary"] == build_generated.glossary_page(entries)
    # grouped alphabetically: headings ascend and each bullet sits under its own letter
    letters = [h[3:] for h in headings]
    assert letters == sorted(letters)
    current = None
    for ln in lines[1:]:
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
    }
    for label, entries in bad.items():
        with pytest.raises(ValueError):
            load(entries)
        assert label
    with pytest.raises(ValueError):
        build_generated.load_glossary(_write(tmp_path, yaml.safe_dump([_entry()])))


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


def test_assemble_with_fake_mkdocs(tmp_path, monkeypatch):
    site = tmp_path / "src_site"
    (site / "paper").mkdir(parents=True)
    (site / "index.html").write_text("<html>root</html>")
    (site / "paper" / "index.html").write_text("<html>paper</html>")
    monkeypatch.setattr(assemble_site, "ROOT_INDEX", site / "index.html")
    monkeypatch.setattr(assemble_site, "PAPER_PLACEHOLDER", site / "paper" / "index.html")
    seen = []

    def fake(cmd):
        seen.append(cmd)
        out = Path(cmd[cmd.index("-d") + 1])
        out.mkdir(parents=True)
        (out / "index.html").write_text("docs")

    out = assemble_site.assemble(
        tmp_path / "out",
        mkdocs_runner=fake,
        generated_dir=tmp_path / "gen",
        collect_runner=lambda: FAKE_COLLECT,
        docs_generated_dir=tmp_path / "docsgen",
    )
    assert (out / "index.html").read_text() == "<html>root</html>"
    assert (out / "docs" / "index.html").exists()
    assert (out / "paper" / "index.html").read_text() == "<html>paper</html>"
    assert (tmp_path / "gen" / "derivations.md").exists()
    assert (tmp_path / "docsgen" / "glossary.md").exists()
    assert "--strict" in seen[0] and "build" in seen[0]


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
        )


def test_assemble_refuses_repo_root():
    with pytest.raises(ValueError):
        assemble_site._check_out(ROOT)


def test_stage_server_serves_index_on_loopback(tmp_path):
    (tmp_path / "index.html").write_text("<html>hello</html>")
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
    assert stage_site.stage(tmp_path, build=False) == tmp_path
