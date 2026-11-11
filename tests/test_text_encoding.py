"""No text file is opened, read or written with the platform's default encoding (WP34, Windows).

Windows opens text in the ANSI code page (cp1252), which cannot decode the repository's UTF-8 files.
Every ``open``, ``read_text`` and ``write_text`` of text names ``encoding="utf-8"``; binary opens
are exempt. The check reads the Python files of the code directories as syntax trees.
"""

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DIRS = ("src", "tests", "scripts", "paper", "examples")
# Positional index of ``encoding`` in each call form.
# Receivers whose ``open`` is not a text opener.
NOT_A_PATH = {"tarfile", "zipfile", "Image", "webbrowser", "os", "io", "gzip", "bz2", "lzma"}
# Code files the experiment ledger hashes: none now (WP30's regeneration re-adopted the three that
# waited on their bare reads, WP34 stage 3 report).
LEDGER_FROZEN: set[str] = set()
ENCODING_POS = {"read_text": 0, "write_text": 1, "open": 3}


def _mode(call: ast.Call, name: str):
    if name != "open":
        return None
    node = call.args[1] if len(call.args) > 1 else None
    for kw in call.keywords:
        if kw.arg == "mode":
            node = kw.value
    return node.value if isinstance(node, ast.Constant) else ("?" if node else None)


def bare_text_calls(source: str):
    """Line numbers of text ``open``/``read_text``/``write_text`` calls without an encoding."""
    hits = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
        if name not in ENCODING_POS:
            continue
        # ``x.open(...)`` on a module or image class is not a text opener.
        if (
            name == "open"
            and isinstance(f, ast.Attribute)
            and isinstance(f.value, ast.Name)
            and f.value.id in NOT_A_PATH
        ):
            continue
        pos = ENCODING_POS[name] - (1 if name == "open" and isinstance(f, ast.Attribute) else 0)
        if any(kw.arg == "encoding" for kw in node.keywords) or len(node.args) > pos >= 0:
            continue
        mode = _mode(node, name) if not isinstance(f, ast.Attribute) else _attr_mode(node)
        if isinstance(mode, str) and "b" in mode:
            continue
        hits.append(node.lineno)
    return hits


def _attr_mode(call: ast.Call):
    node = call.args[0] if call.args else None
    for kw in call.keywords:
        if kw.arg == "mode":
            node = kw.value
    return node.value if isinstance(node, ast.Constant) else None


def test_the_detector_sees_the_bare_forms_and_passes_the_explicit_ones():
    bad = (
        "p.read_text()\np.write_text('x')\nopen('f')\nopen('f', 'w')\np.open()\n"
        "p.open('w')\nopen('f', mode='r')\n"
    )
    good = (
        "p.read_text(encoding='utf-8')\np.write_text('x', encoding='utf-8')\n"
        "open('f', encoding='utf-8')\nopen('f', 'rb')\np.open('wb')\nopen('f', 'wb')\n"
        "p.read_text('utf-8')\np.write_text('x', 'utf-8')\n"
    )
    assert bare_text_calls(bad) == [1, 2, 3, 4, 5, 6, 7]
    assert bare_text_calls(good) == []


def test_no_python_file_opens_text_without_an_encoding():
    offenders = []
    for d in DIRS:
        for path in sorted((REPO / d).rglob("*.py")):
            if ".venv" in path.parts or "_build" in path.parts:
                continue
            rel = path.relative_to(REPO).as_posix()
            if rel in LEDGER_FROZEN:
                continue
            for line in bare_text_calls(path.read_text(encoding="utf-8")):
                offenders.append(f"{rel}:{line}")
    assert offenders == []
