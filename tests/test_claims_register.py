"""The claims register (WP10 Amendment 5, R-43; docs/superpowers/notes/claims-review.md).

``claims_register.toml`` at the repository root has one row per claim a reader can rely on. These
tests keep it from going stale silently: a sentence that is edited no longer matches its fragment
and fails here; a backing that is renamed or removed fails here. The checker is a function
(``check_register``) so that it is itself tested against deliberately broken registers.
"""

import ast
import json
import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "claims_register.toml"

KINDS = {"M", "R", "S", "L", "P"}
FIELDS = {
    "id",
    "fragment",
    "file",
    "anchor",
    "kind",
    "backing",
    "status",
    "disposition",
    "source",
    "note",
}
REQUIRED = {"id", "fragment", "file", "kind", "backing", "status", "disposition"}
DISPOSITIONS = {"keep", "narrow", "back"}
MIN_FRAGMENT_WORDS = 6


def load_register(path=REGISTER):
    """Return the register's rows (a list of dicts); a reader pass loads it the same way."""
    with open(path, "rb") as fh:
        return tomllib.load(fh).get("claim", [])


def _norm(text):
    """Collapse whitespace and drop LaTeX delimiters, so a fragment need not carry typesetting."""
    return re.sub(r"\s+", " ", text.replace("$", "").replace("\\", "")).strip()


def _sections(text):
    """Split Markdown into (heading, body) sections; a section runs to the next heading of the
    same or a higher level, so a heading's body includes its subsections."""
    lines = text.split("\n")
    heads = [
        (i, len(m.group(1)), m.group(2).strip())
        for i, ln in enumerate(lines)
        if (m := re.match(r"(#{1,6})\s+(.*)", ln))
    ]
    out = []
    for n, (i, level, title) in enumerate(heads):
        end = len(lines)
        for j, lvl2, _ in heads[n + 1 :]:
            if lvl2 <= level:
                end = j
                break
        out.append((_norm(title), _norm("\n".join(lines[i:end]))))
    return out


def _source_text(root, rel):
    path = root / rel
    if path.suffix == ".ipynb":
        nb = json.loads(path.read_text(encoding="utf-8"))
        return "\n\n".join(
            "".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"
        )
    return path.read_text(encoding="utf-8")


def _find_in_order(haystack, fragment):
    pos = 0
    for piece in fragment.split(" ... "):
        k = haystack.find(_norm(piece), pos)
        if k < 0:
            return False
        pos = k + len(_norm(piece))
    return True


def _check_fragment(root, row):
    rel, anchor = row["file"], row.get("anchor", "")
    if not (root / rel).is_file():
        return [f"source file missing: {rel}"]
    text = _source_text(root, rel)
    if not _find_in_order(_norm(text), row["fragment"]):
        return [f"fragment not found in {rel}: {row['fragment'][:60]!r}"]
    if not anchor:
        return []
    if Path(rel).suffix in {".md", ".ipynb"}:
        bodies = [b for t, b in _sections(text) if t == _norm(anchor)]
        if not bodies:
            return [f"anchor heading not in {rel}: {anchor!r}"]
        if not any(_find_in_order(b, row["fragment"]) for b in bodies):
            return [f"fragment not under heading {anchor!r} in {rel}"]
    elif _norm(anchor) not in _norm(text):
        return [f"anchor text not in {rel}: {anchor!r}"]
    return []


def _defs(root, rel):
    tree = ast.parse((root / rel).read_text(encoding="utf-8"))
    return {
        n.name
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


def _check_backing(root, item):
    kind, _, value = item.partition(":")
    if item == "reading":
        return None
    if kind == "lemma":
        record = json.loads((root / "derivation/proof_map_record.json").read_text(encoding="utf-8"))
        m = re.fullmatch(r"L(\d+)(?:\.(\d+))?", value)
        if not m:
            return f"bad lemma id {value!r}"
        lemmas = [v for v in record["lemmas"].values() if v["number"] == int(m.group(1))]
        if not lemmas:
            return f"lemma not in the proof-map record: {value}"
        if m.group(2) and value not in {s["tag"] for s in lemmas[0]["steps"]}:
            return f"step tag not in the proof-map record: {value}"
        return None
    if kind in {"test", "gen", "func"}:
        rel, _, name = value.partition("::")
        if not (root / rel).is_file():
            return f"file missing for {item}"
        if name not in _defs(root, rel):
            return f"{name} is not defined in {rel}"
        return None
    if kind == "file":
        return None if (root / value).is_file() else f"file missing: {value}"
    if kind == "bib":
        bib = (root / "docs/references.bib").read_text(encoding="utf-8")
        found = re.search(r"@\w+\{" + re.escape(value) + r"\s*,", bib)
        return None if found else f"bib key not in docs/references.bib: {value}"
    if kind == "glossary":
        gl = (root / "glossary.yaml").read_text(encoding="utf-8")
        found = re.search(r"id:\s*['\"]?" + re.escape(value) + r"['\"]?\s*$", gl, re.M)
        return None if found else f"glossary id not in glossary.yaml: {value}"
    return f"unknown backing type: {item!r}"


def check_register(rows, root=ROOT):
    """Return a list of problems with the rows (empty when the register holds)."""
    problems = []
    seen = set()
    for n, row in enumerate(rows):
        rid = row.get("id", f"#{n}")
        missing = REQUIRED - row.keys()
        if missing:
            problems.append(f"{rid}: missing fields {sorted(missing)}")
            continue
        if row.keys() - FIELDS:
            problems.append(f"{rid}: unknown fields {sorted(row.keys() - FIELDS)}")
        if rid in seen:
            problems.append(f"{rid}: duplicate id")
        seen.add(rid)
        if row["kind"] not in KINDS:
            problems.append(f"{rid}: kind {row['kind']!r} not in {sorted(KINDS)}")
        if row["status"] != "backed":
            problems.append(f"{rid}: status {row['status']!r} is not 'backed'")
        if row["disposition"] not in DISPOSITIONS:
            problems.append(f"{rid}: disposition {row['disposition']!r}")
        if len(_norm(row["fragment"]).split()) < MIN_FRAGMENT_WORDS:
            problems.append(f"{rid}: fragment shorter than {MIN_FRAGMENT_WORDS} words")
        problems += [f"{rid}: {p}" for p in _check_fragment(root, row)]
        backing = row["backing"]
        if not backing:
            problems.append(f"{rid}: no backing")
        for item in backing:
            if (bad := _check_backing(root, item)) is not None:
                problems.append(f"{rid}: {bad}")
        kinds = {b.partition(":")[0] for b in backing}
        if row["kind"] == "R":
            for need in ("gen", "test"):
                if need not in kinds:
                    problems.append(f"{rid}: kind R needs a {need}: backing")
        if "reading" in backing and row["kind"] != "P":
            problems.append(f"{rid}: 'reading' backs only kind P")
    return problems


def test_the_register_holds():
    rows = load_register()
    assert rows, "the register is empty"
    assert check_register(rows) == []


def test_the_notes_table_rows_are_migrated():
    ids = {r["id"] for r in load_register()}
    assert len(ids) >= 23
    note = (ROOT / "docs/superpowers/notes/claims-review.md").read_text(encoding="utf-8")
    assert "claims_register.toml" in note


# The checker itself: each broken register fails for the stated reason.


@pytest.fixture
def tree(tmp_path):
    (tmp_path / "derivation").mkdir()
    (tmp_path / "derivation/proof_map_record.json").write_text(
        json.dumps({"lemmas": {"lemma_01_x.py": {"number": 1, "steps": [{"tag": "L1.1"}]}}}),
        encoding="utf-8",
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/references.bib").write_text("@book{aaa2000bbb,\n title={x}\n}\n")
    (tmp_path / "glossary.yaml").write_text("terms:\n  - id: 'chart'\n", encoding="utf-8")
    (tmp_path / "page.md").write_text(
        "# Top\n\n## Sec\n\nThe quick brown fox jumps over the lazy dog.\n"
    )
    (tmp_path / "t.py").write_text(
        "def test_a():\n    pass\n\ndef make():\n    pass\n", encoding="utf-8"
    )
    return tmp_path


def _row(**kw):
    row = dict(
        id="C1",
        fragment="The quick brown fox jumps over the lazy dog",
        file="page.md",
        anchor="Sec",
        kind="M",
        backing=["lemma:L1.1"],
        status="backed",
        disposition="keep",
    )
    row.update(kw)
    return row


def test_checker_passes_a_good_row(tree):
    good = _row(backing=["lemma:L1", "test:t.py::test_a", "bib:aaa2000bbb", "glossary:chart"])
    assert check_register([good], tree) == []


@pytest.mark.parametrize(
    "change, expect",
    [
        (dict(fragment="The quick brown fox jumps over the sleepy dog"), "fragment not found"),
        (dict(anchor="Top2"), "anchor heading not in"),
        (dict(file="nope.md"), "source file missing"),
        (dict(backing=["lemma:L9"]), "lemma not in"),
        (dict(backing=["lemma:L1.7"]), "step tag not in"),
        (dict(backing=["test:t.py::test_b"]), "is not defined"),
        (dict(backing=["bib:zzz1999yyy"]), "bib key not in"),
        (dict(backing=["file:gone.txt"]), "file missing"),
        (dict(backing=["glossary:nothing"]), "glossary id not in"),
        (dict(backing=[]), "no backing"),
        (dict(backing=["reading"]), "backs only kind P"),
        (dict(kind="R"), "kind R needs a gen"),
        (dict(kind="Z"), "not in"),
        (dict(status="unbacked"), "is not 'backed'"),
        (dict(fragment="too short here"), "shorter than"),
    ],
)
def test_checker_rejects_a_broken_row(tree, change, expect):
    problems = check_register([_row(**change)], tree)
    assert any(expect in p for p in problems), problems


def test_checker_kind_r_with_generator_and_test_passes(tree):
    row = _row(kind="R", backing=["gen:t.py::make", "test:t.py::test_a"])
    assert check_register([row], tree) == []


def test_checker_rejects_duplicate_ids(tree):
    assert any("duplicate id" in p for p in check_register([_row(), _row()], tree))


def test_fragment_pieces_must_be_in_order(tree):
    ok = _row(fragment="The quick brown fox ... over the lazy dog")
    assert check_register([ok], tree) == []
    bad = _row(fragment="over the lazy dog ... The quick brown fox")
    assert any("fragment not found" in p for p in check_register([bad], tree))
