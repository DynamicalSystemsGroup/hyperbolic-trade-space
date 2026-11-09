"""WP5 citation hygiene: docs/references.bib and docs/literature.md.

Offline and standard-library only. Live resolution of each entry was done in WP5 and is recorded
in the entry's ``verified`` field; this test keeps the files in that state.
"""

import re
from datetime import date
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
BIB = DOCS / "references.bib"
LIT = DOCS / "literature.md"
# WP10: keys added for the paper's prior-art section are cited in this source note, so the
# bibliography stays free of uncited keys whether or not literature.md survives WP8a's restructure.
SOURCES = DOCS / "superpowers" / "notes" / "paper-prior-art-sources.md"

KEY_RE = re.compile(r"^[a-z]+[0-9]{4}[a-z]+$")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
VERIFIED_RE = re.compile(r"^(\d{4}-\d{2}-\d{2});\s*(\S.*)$", re.DOTALL)
CITE_RE = re.compile(r"\[(@[^\]]+)\]")

REQUIRED = {
    "article": {"author", "title", "journal", "year", "volume"},
    "book": {"author", "title", "publisher", "year"},
    "inproceedings": {"author", "title", "booktitle", "year"},
    "incollection": {"author", "title", "booktitle", "publisher", "year"},
    "misc": {"author", "title"},
}


def _strip_comments(text: str) -> str:
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("%"))


def _read_braced(text: str, i: int) -> tuple[str, int]:
    """Return the content of the brace group opening at text[i] and the index after it."""
    assert text[i] == "{"
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1 : j], j + 1
    raise AssertionError("unbalanced braces")


def parse_bib(text: str) -> list[dict]:
    text = _strip_comments(text)
    entries = []
    pos = 0
    while (at := text.find("@", pos)) != -1:
        m = re.compile(r"@(\w+)\s*\{").match(text, at)
        assert m, f"malformed entry start near: {text[at : at + 40]!r}"
        body, end = _read_braced(text, m.end() - 1)
        key, _, rest = body.partition(",")
        fields: dict[str, str] = {}
        k = 0
        while True:
            fm = re.compile(r"\s*([A-Za-z]+)\s*=\s*").match(rest, k)
            if not fm:
                break
            k = fm.end()
            assert rest[k] == "{", f"{key.strip()}: field {fm.group(1)} value must be braced"
            val, k = _read_braced(rest, k)
            fields[fm.group(1).lower()] = val.strip()
            k = re.compile(r"\s*,?").match(rest, k).end()
        assert not rest[k:].strip(), f"{key.strip()}: unparsed text {rest[k:][:40]!r}"
        entries.append({"type": m.group(1).lower(), "key": key.strip(), "fields": fields})
        pos = end
    return entries


def _bib() -> list[dict]:
    return parse_bib(BIB.read_text(encoding="utf-8"))


def test_bib_parses_and_has_entries() -> None:
    assert len(_bib()) >= 30


def test_keys_unique_and_well_formed() -> None:
    keys = [e["key"] for e in _bib()]
    assert len(keys) == len(set(keys)), "duplicate keys"
    bad = [k for k in keys if not KEY_RE.match(k)]
    assert not bad, f"keys not in author<year><word> form: {bad}"


def test_required_fields_per_type() -> None:
    problems = []
    for e in _bib():
        assert e["type"] in REQUIRED, f"{e['key']}: unexpected entry type {e['type']}"
        missing = REQUIRED[e["type"]] - set(e["fields"])
        if e["type"] == "misc":
            missing -= {"year"}
        if missing:
            problems.append((e["key"], sorted(missing)))
    assert not problems, problems


def test_every_entry_has_doi_or_https_url() -> None:
    bad = []
    for e in _bib():
        f = e["fields"]
        doi, url = f.get("doi"), f.get("url")
        if doi is not None:
            ok = bool(DOI_RE.match(doi))
        else:
            ok = url is not None and url.startswith("https://")
        if not ok:
            bad.append(e["key"])
    assert not bad, f"no resolvable DOI or https URL: {bad}"


def test_every_entry_records_its_verification() -> None:
    bad = []
    for e in _bib():
        v = e["fields"].get("verified", "")
        m = VERIFIED_RE.match(v)
        if not m:
            bad.append(e["key"])
            continue
        try:
            date.fromisoformat(m.group(1))
        except ValueError:
            bad.append(e["key"])
        if "http" not in v:
            bad.append(e["key"])
    assert not bad, f"missing or malformed verified field: {sorted(set(bad))}"


def _cited_keys(md: str) -> set[str]:
    keys: set[str] = set()
    for group in CITE_RE.findall(md):
        for part in group.split(";"):
            part = part.strip()
            assert part.startswith("@"), f"malformed citation group: [{group}]"
            keys.add(part[1:].strip())
    return keys


def test_every_citation_resolves_to_the_bib() -> None:
    cited = _cited_keys(LIT.read_text(encoding="utf-8"))
    unknown = cited - {e["key"] for e in _bib()}
    assert not unknown, f"cited but not in references.bib: {sorted(unknown)}"


def test_every_bib_key_is_cited() -> None:
    cited = _cited_keys(LIT.read_text(encoding="utf-8")) | _cited_keys(
        SOURCES.read_text(encoding="utf-8")
    )
    uncited = {e["key"] for e in _bib()} - cited
    assert not uncited, f"in references.bib but never cited in literature.md: {sorted(uncited)}"
