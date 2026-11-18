"""R-14: every relative link on CONTRIBUTING.md resolves to a file in the repository, so the
page cannot land without the files it links. The three admissibility pages, the code of
conduct and the security page are held to the same rule."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    ".github/ISSUE_ADMISSIBILITY.md",
    ".github/PR_ADMISSIBILITY.md",
    ".github/RELEASE_ADMISSIBILITY.md",
]
LINK = re.compile(r"\]\(([^)\s]+)\)")


def relative_targets(page):
    text = (ROOT / page).read_text(encoding="utf-8")
    for target in LINK.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
            continue
        yield target.split("#")[0]


@pytest.mark.parametrize("page", PAGES)
def test_every_relative_link_resolves_to_a_file(page):
    base = (ROOT / page).parent
    missing = [t for t in relative_targets(page) if not (base / t).is_file()]
    assert not missing, f"{page}: {missing}"


def test_contributing_links_the_files_the_sign_off_names():
    targets = set(relative_targets("CONTRIBUTING.md"))
    assert {
        "CODE_OF_CONDUCT.md",
        ".github/ISSUE_ADMISSIBILITY.md",
        ".github/ISSUE_TEMPLATE/scope-of-work.yml",
        ".github/PR_ADMISSIBILITY.md",
        ".github/pull_request_template.md",
        ".github/RELEASE_ADMISSIBILITY.md",
        "SECURITY.md",
        "docs/code-owners.md",
        ".python-version",
        "pyproject.toml",
        "uv.lock",
    } <= targets
