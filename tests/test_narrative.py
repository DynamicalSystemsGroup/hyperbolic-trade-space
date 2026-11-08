"""WP6 narrative hygiene: docs/method.md, why-and-how.md, limitations.md and spec section 6.

Offline; standard library, ``re`` and the project modules only. Checks structure and agreement
with the ledger and the code (formula tags resolve to lemma modules, every lemma is cited, the
conditions table equals the ledger's set with its role and failure-mode text, referenced
functions exist, citation keys resolve, the spec's axiom lists equal ``AXIOMS_USED``). It does
not judge the prose.
"""

import importlib
import re
from pathlib import Path

from derivation import axioms
from hyperbolic_trade_space import HyperbolicTradeSpace, coordinates, datasets, solvers

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
METHOD = DOCS / "method.md"
PAGES = [METHOD, DOCS / "why-and-how.md", DOCS / "limitations.md"]
SPEC = ROOT / "docs/superpowers/specs/2026-11-07-posynomial-invariant-form-design.md"
LEMMAS = {f"L{n}": next((ROOT / "derivation").glob(f"lemma_{n:02d}_*.py")) for n in range(1, 11)}

CITE_RE = re.compile(r"\[(@[^\]]+)\]")


def _text(path):
    return path.read_text(encoding="utf-8")


def _lemma_axioms(lemma_id):
    mod = importlib.import_module(f"derivation.{LEMMAS[lemma_id].stem}")
    return list(mod.AXIOMS_USED)


# ------------------------------------------------------------------ formula tags (R-2)
def _display_tags(text):
    """Return (n_displays, tags) with tags the comment text following each $$ block."""
    out = []
    for m in re.finditer(r"\$\$(.*?)\$\$", text, re.S):
        rest = text[m.end() :]
        nxt = re.match(r"[ \t]*\n(<!--\s*(.*?)\s*-->)", rest, re.S)
        out.append(nxt.group(2) if nxt else None)
    return out


def test_every_display_formula_is_tagged():
    tags = _display_tags(_text(METHOD))
    assert tags, "method.md has no displayed formulas"
    for t in tags:
        assert t is not None, "a display formula has no tag comment on the next line"
        assert t == "definition" or re.fullmatch(r"lemma:\s*L\d+(,\s*L\d+)*", t), t


def test_tags_resolve_and_all_lemmas_cited():
    cited = set()
    for t in _display_tags(_text(METHOD)):
        if t and t.startswith("lemma:"):
            cited |= set(re.findall(r"L\d+", t))
    for lid in cited:
        assert lid in LEMMAS, f"tag {lid} does not resolve to a lemma module"
        assert LEMMAS[lid].exists()
    assert cited == set(LEMMAS), f"lemmas never tagged: {sorted(set(LEMMAS) - cited)}"
    # every lemma also named in the visible text
    body = re.sub(r"<!--.*?-->", "", _text(METHOD))
    for lid in LEMMAS:
        assert re.search(rf"\b{lid}\b", body), f"{lid} not named in the prose"


# ------------------------------------------------------------ conditions table (R-4)
def _table_rows(text, header_start):
    lines = text.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith(header_start))
    rows = []
    for ln in lines[i + 2 :]:
        if not ln.startswith("|"):
            break
        rows.append([c.strip() for c in ln.strip().strip("|").split(" | ")])
    return rows


def test_conditions_table_equals_ledger_set():
    rows = _table_rows(_text(METHOD), "| id | statement |")
    ids = {r[0] for r in rows}
    expected = {a.name for a in axioms.by_tag(axioms.REGULARITY)}
    expected |= {a.name for a in axioms.fallbacks()}
    expected |= {"A4"}
    assert ids == expected == {"R1", "F5", "F10", "A4"}


def test_conditions_table_quotes_ledger_role_and_failure_mode():
    rows = {r[0]: r for r in _table_rows(_text(METHOD), "| id | statement |")}
    for name, row in rows.items():
        ax = axioms.get(name)
        assert row[1] == ax.statement, name
        if ax.role:
            assert row[2] == ax.role, name
            assert row[3] == ax.failure_mode, name
        else:  # A4: the ledger records none; the narrative must say so and supply text
            assert "ledger records none" in row[2] and row[3].strip()


# ---------------------------------------------------- implementation pointers (R-3)
def test_referenced_functions_exist():
    text = _text(METHOD)
    found = 0
    modules = {"solvers": solvers, "coordinates": coordinates, "datasets": datasets}
    for mod, name in re.findall(r"`(solvers|coordinates|datasets)\.(\w+)`", text):
        assert hasattr(modules[mod], name), f"{mod}.{name}"
        found += 1
    for name in re.findall(r"`HyperbolicTradeSpace\.(\w+)`", text):
        assert hasattr(HyperbolicTradeSpace, name) or name in {
            "exponents_",
            "log_offset_",
        }, f"HyperbolicTradeSpace.{name}"
        found += 1
    assert found >= 10


def test_no_wp3_signatures_quoted():
    # the analysis toolkit is described by concept; no WP3 API names appear
    for page in PAGES:
        t = _text(page)
        for name in ("knn_gap_scores", "find_holes", "tension_report", "select_temperature"):
            assert name not in t, f"{page.name} quotes {name}"


# ---------------------------------------------------------------- citations (R-10)
def test_citation_keys_resolve():
    keys = set(re.findall(r"@\w+\{(\w+),", _text(DOCS / "references.bib")))
    used = set()
    for page in PAGES:
        for group in CITE_RE.findall(_text(page)):
            for k in group.split(";"):
                used.add(k.strip().lstrip("@"))
    assert used, "no citations found"
    assert used <= keys, f"unknown keys: {sorted(used - keys)}"


# ---------------------------------------------------- terminology and hygiene (R-12, R-14)
def test_names_and_hygiene():
    for page in PAGES:
        t = _text(page)
        assert "Co-Authored" not in t and "Generated with" not in t
        assert not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", t), "emoji"
    method = _text(METHOD)
    assert "HyperbolicTradeSpace" in method
    assert "posynomial invariant form" in _text(PAGES[1])
    # beta is the log-mean-exp: the method states the normalization against the unnormalized sum
    assert "never the unnormalized sum" in method
    # required content of the conditions of the theory and the principle
    assert "All models are wrong and some are useful" in method
    assert "All models are wrong and some are useful" in _text(PAGES[2])
    assert "n-lemma" in method and "n-lemma" in _text(PAGES[1])
    assert "min_exponent" in method


# --------------------------------------------------- spec section 6 vs ledger (R-11)
def _spec_section6():
    text = _text(SPEC)
    i = text.index("## 6. Derivation scripts")
    j = text.index("\n## 7.", i)
    return text[i:j]


def test_spec_matches_ledger():
    sec = _spec_section6()
    # every ledger id is named in the axiom paragraph
    axiom_par = sec[sec.index("Axioms (equal to the ledger") : sec.index("Lemmas: L1")]
    for name in axioms.AXIOMS:
        assert re.search(rf"\b{name}\b", axiom_par), f"{name} missing from spec section 6"
    # per-lemma lists equal AXIOMS_USED
    lem_par = sec[sec.index("Lemmas: L1") : sec.index("SymPy pitfalls")]
    parsed = {}
    for m in re.finditer(r"\bL(\d+)\b[^\[\]]*?\[([A-Z0-9, ]+)\]", lem_par):
        parsed[f"L{m.group(1)}"] = [a.strip() for a in m.group(2).split(",")]
    assert set(parsed) == set(LEMMAS)
    for lid, listed in parsed.items():
        assert sorted(listed) == sorted(_lemma_axioms(lid)), lid
        for a in listed:
            assert a in axioms.AXIOMS
