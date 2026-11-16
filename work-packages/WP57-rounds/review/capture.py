"""WP57 D-3 captures: the paper and the supporting material as rendered, at 1,280 px wide.

    uv run --with playwright python work-packages/WP57-rounds/review/capture.py text OUT
    uv run --with playwright python work-packages/WP57-rounds/review/capture.py shots OUT

Reads the site served read-only at ``http://localhost:8797/paper``; headless Chrome at 1,280 by
900. ``text`` writes the inner text of both pages and every link of the paper to an appendix with
its paragraph (``pointers.json``). ``shots`` writes the PNGs listed in ``SHOTS``: each scrolls to an
element id, or to the first paragraph holding a phrase, and captures one screen.
"""

import json
import sys

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8797/paper"
PAPER, SUPP = f"{BASE}/", f"{BASE}/supporting-material/"

# (file name, page, element id or None, phrase or None, pixels above the target)
LANDINGS = [
    "appendix-a",
    "sub-b-11",
    "appendix-c",
    "appendix-d",
    "appendix-e",
    "sub-b-3",
    "sub-f-4",
    "sub-b-7",
    "sub-e-2",
    "sub-b-8",
    "sub-b-13",
    "sub-b-9",
    "sub-b-4",
    "appendix-g",
    "appendix-f",
    "sub-f-1",
    "sub-f-6",
    "sub-b-5",
    "appendix-b",
    "sub-b-10",
    "sub-f-7",
    "sub-b-1",
    "sub-b-2",
    "sub-b-6",
    "sub-b-12",
    "sub-b-14",
    "sub-h-3",
    "sub-h-2",
    "appendix-h",
]
SHOTS: list[tuple[str, str, str | None, str | None, int]] = [
    # every landing of a paper pointer, as the reader first sees it (depth 1 to 3)
    *((f"landing-{t}", "supp", t, None, 0) for t in LANDINGS),
    # depth 5: each boundary, the end of one appendix above the start of the next
    *(
        (f"boundary-{a}{b}", "supp", f"appendix-{b}", None, 560)
        for a, b in zip("abcdefg", "bcdefgh", strict=True)
    ),
    # depth 4 and the findings
    ("A-depth4-hyperbolic-graph", "supp", None, "The hyperbolic graph measure of efficiency", 0),
    (
        "A-depth4-entropic-risk",
        "supp",
        None,
        "The log-mean-exp soft maximum is the sample version",
        300,
    ),
    ("B-depth4-b1-k3", "supp", None, "Dataset cubesat-primary, K = 3:", 0),
    ("B-depth4-b2-rows", "supp", "sub-b-2", None, 0),
    ("B-depth4-b3-baseline", "supp", "tab-B-sensitivity_variants", None, 40),
    ("B-depth4-b6-proposals", "supp", "tab-B-propose_predict_check", None, 120),
    ("B-depth4-b7-moving", "supp", None, "The printed quantities that move", 0),
    (
        "B-depth4-b12-checkdesigns",
        "supp",
        None,
        "The baseline configuration and the check designs",
        0,
    ),
    ("B-depth4-b13", "supp", "tab-B-injected_noise", None, 200),
    ("B-depth4-b1-link-f5", "supp", None, "Of the thirteen traded metrics, two", 0),
    ("C-depth4-table1", "supp", "tab-C-hypothesis-caption", None, 120),
    ("C-depth4-reading-limits", "supp", "sub-c-4", None, 0),
    ("D-depth4-defined-in", "supp", None, "Prediction from configuration; WP41 note", 500),
    ("D-depth4-conditioning-row", "supp", "tab-D-register", None, 0),
    ("E-depth4-preamble", "supp", "appendix-e", None, 0),
    ("E-depth4-step-table", "supp", "proof-l2", None, 0),
    ("E-depth4-l17", "supp", "proof-l17", None, 0),
    ("F-depth4-feasibility", "supp", "sub-f-3", None, 0),
    ("F-depth4-f2-files", "supp", "tab-F-attribute_sources", None, 60),
    ("F-depth4-f5-rule", "supp", "sub-f-5", None, 0),
    ("F-depth4-f6-names", "supp", "sub-f-6", None, 0),
    ("G-depth4-g2-section9", "supp", None, "One term is tangent at one place", 300),
    ("G-depth4-gaps-g8", "supp", None, "The tangent step and the penalty outside", 200),
    ("G-depth4-g3", "supp", "sub-g-3", None, 0),
    ("G-depth4-table2", "supp", "tab-G-assumptions-caption", None, 0),
    ("H-depth4-h4", "supp", "sub-h-4", None, 0),
    (
        "paper-table2-order",
        "paper",
        None,
        "The traded metrics of the SysML v2 model in the order",
        420,
    ),
    (
        "paper-section9-limits",
        "paper",
        None,
        "Limits. The fitted reference surface is log-convex",
        200,
    ),
    (
        "paper-s6-l17-pointer",
        "paper",
        None,
        "the tangent space of the active face (positive-multiplier",
        200,
    ),
    ("paper-s5-f4-pointer", "paper", None, "Conditioning (stage 2).", 100),
    ("paper-s8-b6-pointer", "paper", None, "Of 3 proposals, the predicted", 200),
    ("paper-s6-b13-pointer", "paper", None, "sets it against noise injected", 300),
    (
        "broken-link-404",
        "url:http://localhost:8797/paper/supporting-material/supporting-material/#sub-f-5",
        None,
        None,
        0,
    ),
]
OUTLINE = "outline-open"


def load(pg, url: str) -> None:
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(4000)


def scroll_to(pg, el: str | None, phrase: str | None, up: int) -> bool:
    if el:
        top = pg.evaluate(
            f"(()=>{{const e=document.getElementById({json.dumps(el)});"
            " return e? e.getBoundingClientRect().top+scrollY : null})()"
        )
    else:
        top = pg.evaluate(
            "(p=>{const e=[...document.querySelectorAll('p, li, td, h2, h3, figcaption, caption,"
            " div.caption, span')].find(x=>x.innerText && x.innerText.includes(p));"
            " return e? e.getBoundingClientRect().top+scrollY : null})",
            phrase,
        )
    if top is None:
        print("missing", el or phrase)
        return False
    pg.evaluate(f"window.scrollTo(0,{top}-20-{up})")
    pg.wait_for_timeout(700)
    return True


def text(out: str, pg) -> None:
    load(pg, PAPER)
    with open(f"{out}/paper-text.txt", "w") as f:
        f.write(pg.evaluate("document.body.innerText"))
    links = pg.evaluate(
        "[...document.querySelectorAll('article a, main a')]"
        ".filter(a=>/supporting-material/.test(a.getAttribute('href')||''))"
        ".map(a=>{const p=a.closest('p, li, td, figcaption, div');"
        " const h=[...document.querySelectorAll('h1,h2,h3')].filter(x=>"
        "x.compareDocumentPosition(a)&Node.DOCUMENT_POSITION_FOLLOWING).pop();"
        " return {text:a.innerText, href:a.getAttribute('href'),"
        " section:h? h.innerText:null, para:p? p.innerText:null}})"
    )
    with open(f"{out}/pointers.json", "w") as f:
        json.dump(links, f, indent=1)
    load(pg, SUPP)
    with open(f"{out}/supporting-text.txt", "w") as f:
        f.write(pg.evaluate("document.body.innerText"))
    print(len(links), "links to the supporting material")


def shots(out: str, pg) -> None:
    load(pg, SUPP)
    pg.get_by_text("In this article", exact=False).first.click()
    pg.wait_for_timeout(1500)
    pg.screenshot(path=f"{out}/{OUTLINE}.png")
    current = None
    for name, page, el, phrase, up in SHOTS:
        url = page[4:] if page.startswith("url:") else PAPER if page == "paper" else SUPP
        if url != current:
            load(pg, url)
            current = url
        if page.startswith("url:") or scroll_to(pg, el, phrase, up):
            pg.screenshot(path=f"{out}/{name}.png")


if __name__ == "__main__":
    mode, out = sys.argv[1], sys.argv[2]
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        (text if mode == "text" else shots)(out, pg)
        b.close()
