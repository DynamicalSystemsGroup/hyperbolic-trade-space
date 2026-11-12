"""The history record and its view (WP37, D-9).

``history.yaml`` at the repository root is the record: one entry per dated reference and per
person, with the schema described at the top of that file. ``site/history.html`` is hand-written
prose, a view of the record for a human reader; at build time ``scripts/assemble_site.py`` inserts
a dated reference list rendered from the record at the page's marker (``<!-- history-list -->``).
This module holds the loader, the schema check, the list renderer, and the sentence trace::

    uv run python scripts/history_record.py            # validate the record
    uv run python scripts/history_record.py --trace    # write work-packages/WP37-rounds/trace.md
    uv run python scripts/history_record.py --check    # exit 1 if trace.md is not current
"""

from __future__ import annotations

import html
import itertools
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECORD = ROOT / "history.yaml"
PAGE = ROOT / "site" / "history.html"
TRACE = ROOT / "work-packages" / "WP37-rounds" / "trace.md"
MARKER = "<!-- history-list -->"

KINDS = ("paper", "repository", "post", "video", "talk", "role", "person")
CLAIMS = ("sourced", "link", "team-account")
REQUIRED = ("id", "date", "kind", "title", "url", "read_on", "shows", "claim")
OPTIONAL = ("people", "special_case", "listed", "note")
DATE = re.compile(r"\d{4}(-\d{2}(-\d{2})?)?")
DAY = re.compile(r"\d{4}-\d{2}-\d{2}")
#: the phrases that mark a sentence as the team's own account
TEAM_MARKS = ("our own account", "the same account")


def load(path=RECORD):
    """The record's entries (a list of dicts)."""
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["entries"]


def validate(entries):
    """The problems with the record (empty when it holds): required fields, kinds, claims, dates,
    unique ids and URLs, https URLs, people with a name and a role only as strings."""
    problems = []
    ids, urls = set(), set()
    for n, e in enumerate(entries):
        eid = e.get("id", f"#{n}") if isinstance(e, dict) else f"#{n}"
        if not isinstance(e, dict):
            problems.append(f"{eid}: not a mapping")
            continue
        missing = [k for k in REQUIRED if k not in e or e[k] in (None, "")]
        if missing:
            problems.append(f"{eid}: missing {missing}")
        extra = set(e) - set(REQUIRED) - set(OPTIONAL)
        if extra:
            problems.append(f"{eid}: unknown fields {sorted(extra)}")
        for k in REQUIRED:
            if k in e and not isinstance(e[k], str):
                problems.append(f"{eid}: {k} must be a string (quote dates)")
        if e.get("kind") not in KINDS:
            problems.append(f"{eid}: kind {e.get('kind')!r}")
        if e.get("claim") not in CLAIMS:
            problems.append(f"{eid}: claim {e.get('claim')!r}")
        if isinstance(e.get("date"), str) and not DATE.fullmatch(e["date"]):
            problems.append(f"{eid}: date {e['date']!r} is not YYYY, YYYY-MM or YYYY-MM-DD")
        if isinstance(e.get("read_on"), str) and not DAY.fullmatch(e["read_on"]):
            problems.append(f"{eid}: read_on {e['read_on']!r}")
        if e.get("id") in ids:
            problems.append(f"{eid}: duplicate id")
        ids.add(e.get("id"))
        url = e.get("url", "")
        if not (isinstance(url, str) and url.startswith("https://") and " " not in url):
            problems.append(f"{eid}: url {url!r} is not an https URL")
        if url in urls:
            problems.append(f"{eid}: duplicate url {url}")
        urls.add(url)
        for flag in ("special_case", "listed"):
            if flag in e and not isinstance(e[flag], bool):
                problems.append(f"{eid}: {flag} must be a boolean")
        for p in e.get("people", []) or []:
            if (
                not isinstance(p, dict)
                or not isinstance(p.get("name"), str)
                or set(p) - {"name", "role"}
                or ("role" in p and not isinstance(p["role"], str))
            ):
                problems.append(f"{eid}: bad people item {p!r}")
        if e.get("kind") == "person" and len(e.get("people", []) or []) != 1:
            problems.append(f"{eid}: a person entry names exactly one person")
    return problems


def year(entry):
    return entry["date"][:4]


def is_listed(entry):
    default = entry["kind"] not in ("person", "role")
    return bool(entry.get("listed", default))


def person_names(entries):
    """Every name the record holds: people lists and person titles."""
    return {p["name"] for e in entries for p in (e.get("people") or [])}


def render_list(entries):
    """The dated reference list: chronological, year, title as a link, people, and the special-case
    mark beside the entries that carry it. Only the link titles may carry a source's own words."""
    rows = sorted((e for e in entries if is_listed(e)), key=lambda e: (e["date"], e["id"]))
    out = [
        '<section class="record" id="record">',
        "  <h2>Dated references</h2>",
        '  <p class="note">The detail the text above leaves out, oldest first, from '
        "the history record (<code>history.yaml</code>).</p>",
        "  <ol>",
    ]
    for e in rows:
        names = ", ".join(html.escape(p["name"]) for p in e.get("people") or [])
        who = f' <span class="who">{names}</span>' if names else ""
        special = (
            ' <span class="special">a special case where the work was highly public</span>'
            if e.get("special_case")
            else ""
        )
        out.append(
            f'    <li><span class="yr">{year(e)}</span> '
            f'<a href="{html.escape(e["url"], quote=True)}">{html.escape(e["title"])}</a>'
            f"{who}{special}</li>"
        )
    out += ["  </ol>", "</section>"]
    return "\n".join(out)


def build_page(page_html, entries):
    """The page with the generated list inserted at its marker."""
    if page_html.count(MARKER) != 1:
        raise ValueError(f"the page must carry the marker {MARKER} exactly once")
    return page_html.replace(MARKER, render_list(entries))


def build_page_file(path=PAGE, record=RECORD):
    return build_page(Path(path).read_text(encoding="utf-8"), load(record))


# ---------------------------------------------------------------------------------------------
# The sentences of the prose, with the links each carries


class _Paragraphs(HTMLParser):
    """Text and links of each paragraph in <main> up to the marker or the footer."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paras = []  # list of {"text": str, "links": [(start, end, href)]}
        self._in_p = False
        self._text = ""
        self._links = []
        self._href = None
        self._start = 0
        self._main = False

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self._main = True
        if tag == "footer":
            self._main = False
        if self._main and tag == "p":
            self._in_p, self._text, self._links = True, "", []
        if self._in_p and tag == "a":
            self._href = dict(attrs).get("href")
            self._start = len(self._text)

    def handle_endtag(self, tag):
        if self._in_p and tag == "a" and self._href is not None:
            self._links.append((self._start, len(self._text), self._href))
            self._href = None
        if self._in_p and tag == "p":
            self._in_p = False
            self.paras.append({"text": self._text, "links": self._links})

    def handle_data(self, data):
        if self._in_p:
            self._text += data


def sentences(page_html):
    """The prose sentences: [{"text", "hrefs"}] in order (whitespace collapsed)."""
    parser = _Paragraphs()
    parser.feed(page_html)
    out = []
    for para in parser.paras:
        text = para["text"]
        # collapse whitespace while keeping the link offsets
        keep, idx = [], []
        prev_space = True
        for i, ch in enumerate(text):
            if ch.isspace():
                if prev_space:
                    continue
                ch, prev_space = " ", True
            else:
                prev_space = False
            keep.append(ch)
            idx.append(i)
        flat = "".join(keep).rstrip()
        # sentence boundaries: a full stop, then a space, then a capital or an opening quote
        cuts = [0] + [m.end() for m in re.finditer(r"(?<=[.?!])\s+(?=[A-Z“\"])", flat)]
        cuts.append(len(flat) + 1)
        for a, b in itertools.pairwise(cuts):
            seg = flat[a : b - 1].strip()
            if not seg:
                continue
            lo, hi = (
                idx[a] if a < len(idx) else len(text),
                (idx[b - 2] + 1 if 0 <= b - 2 < len(idx) else len(text)),
            )
            hrefs = [h for s, e, h in para["links"] if s >= lo and e <= hi and h]
            out.append({"text": seg, "hrefs": hrefs})
    return out


def classify(sentence, entries):
    """``(kinds, ids, marked, special, linked)`` for a prose sentence, derived from the record's
    claim kinds: the claim of each linked entry; ``team-account`` also where the sentence carries a
    mark or is in the firm's first person ("We ..."); ``page`` where nothing is linked or marked."""
    by_url = {e["url"]: e for e in entries}
    linked = [by_url[h] for h in sentence["hrefs"] if h in by_url]
    kinds = {e["claim"] for e in linked}
    marked = any(m in sentence["text"] for m in TEAM_MARKS)
    if marked or sentence["text"].startswith("We "):
        kinds.add("team-account")
    if not kinds:
        kinds.add("page")
    special = any(e.get("special_case") for e in linked)
    return sorted(kinds), [e["id"] for e in linked], marked, special, linked


def trace_table(page_html, entries):
    """The trace table (Markdown) for the page's prose."""
    lines = [
        "# WP37 trace: the page's sentences, their kinds, and what each lets a reader trace",
        "",
        "Generated by `uv run python scripts/history_record.py --trace` from `site/history.html`",
        "and `history.yaml`; `tests/test_site.py` checks it is current. Do not edit by hand.",
        "",
        "Kinds are derived from the record's claim of each linked entry: `sourced` (a source read",
        "states it), `link` (the link itself shows it), `team-account` (the team's own account:",
        "marked in the sentence, or in the firm's first person). `page` is the page's statement of",
        "its own purpose.",
        "",
        "| # | Sentence | Kind | Record ids | Marked | Special case | A reader can trace |",
        "|---|---|---|---|---|---|---|",
    ]
    for n, s in enumerate(sentences(page_html), 1):
        kinds, ids, marked, special, linked = classify(s, entries)
        trace = "; ".join(f"{year(e)} {e['title']}" for e in linked) or "-"
        text = s["text"].replace("|", "\\|")
        lines.append(
            f"| {n} | {text} | {', '.join(kinds)} | {', '.join(ids) or '-'} | "
            f"{'yes' if marked else 'no'} | {'yes' if special else 'no'} | "
            f"{trace.replace('|', '/')} |"
        )
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    entries = load()
    problems = validate(entries)
    for p in problems:
        print(p)
    if problems:
        return 1
    page = PAGE.read_text(encoding="utf-8")
    if "--trace" in argv:
        TRACE.write_text(trace_table(page, entries), encoding="utf-8")
        print(f"wrote {TRACE.relative_to(ROOT)}")
    elif "--check" in argv:
        current = TRACE.read_text(encoding="utf-8") if TRACE.is_file() else ""
        if current != trace_table(page, entries):
            print("trace.md is not current: run scripts/history_record.py --trace")
            return 1
    else:
        print(f"{len(entries)} entries; the record holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
