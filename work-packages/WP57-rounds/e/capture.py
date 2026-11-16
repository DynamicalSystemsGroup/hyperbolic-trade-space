"""WP57e captures: the supporting page's navigation, the eight appendix openings, two pointers.

    uv run --with playwright python work-packages/WP57-rounds/e/capture.py OUT PORT

Reads the site built by ``cd paper && BASE_URL=/paper uv run --frozen myst build --html`` and
served at ``http://127.0.0.1:PORT/paper``; headless Chrome at 1,280 by 900. Prints the page checks
as JSON: the order of the appendix headings, every new anchor present, no in-page link to a missing
id, no old anchor left, the page's scroll width.
"""

import json
import sys

from playwright.sync_api import sync_playwright

out, port = sys.argv[1], sys.argv[2]
base = f"http://127.0.0.1:{port}/paper"
ANCHORS = ["appendix-" + x for x in "abcdefgh"] + [
    *(f"sub-a-{i}" for i in range(1, 2)),
    *(f"sub-b-{i}" for i in range(1, 15)),
    *(f"sub-c-{i}" for i in range(1, 5)),
    *(f"sub-e-{i}" for i in range(1, 4)),
    *(f"sub-f-{i}" for i in range(1, 9)),
    *(f"sub-g-{i}" for i in range(1, 4)),
    *(f"sub-h-{i}" for i in range(1, 5)),
    "tab-g-assumptions-1",
    "tab-g-cited-1",
    "tab-g-gaps-1",
    "tab-c-hypothesis-1",
]
OLD = ["sub-d-3", "sub-d-16", "sub-d-19", "sub-c-8", "sub-g-4", "sub-h-5", "sub-e-4"]


def shoot(pg, el: str, name: str, up: int = 0) -> bool:
    top = pg.evaluate(
        f"(()=>{{const e=document.getElementById('{el}'); "
        "return e? e.getBoundingClientRect().top+scrollY : null})()"
    )
    if top is None:
        print("missing", el)
        return False
    pg.evaluate(f"window.scrollTo(0,{top}-20-{up})")
    pg.wait_for_timeout(800)
    pg.screenshot(path=f"{out}/{name}.png")
    return True


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.goto(f"{base}/supporting-material/", wait_until="networkidle")
    pg.wait_for_timeout(5000)
    heads = pg.evaluate(
        "[...document.querySelectorAll('h2')].map(h=>h.innerText.trim())"
        ".filter(t=>/^Appendix [A-H]\\./.test(t))"
    )
    checks = {
        "appendix_headings": heads,
        "anchors_missing": pg.evaluate(
            f"{json.dumps(ANCHORS)}.filter(id=>!document.getElementById(id))"
        ),
        "old_anchors_present": pg.evaluate(
            f"{json.dumps(OLD)}.filter(id=>document.getElementById(id))"
        ),
        "unresolved_refs": pg.evaluate(
            "[...document.querySelectorAll('a')].filter(a=>/^#/.test(a.getAttribute('href')||'')"
            " && !document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))))"
            ".map(a=>a.getAttribute('href')).slice(0,20)"
        ),
        "scrollWidth": pg.evaluate("document.documentElement.scrollWidth"),
    }
    # the "In this article" navigation: its entries in order
    toc = pg.evaluate(
        "(()=>{const n=[...document.querySelectorAll('nav, aside')].find(x=>/In this article/i"
        ".test(x.innerText)); return n? n.innerText : null})()"
    )
    checks["in_this_article"] = toc
    print(json.dumps(checks, indent=1))
    pg.evaluate("window.scrollTo(0,0)")
    pg.wait_for_timeout(800)
    pg.screenshot(path=f"{out}/nav-top.png")
    nav = pg.evaluate(
        "(()=>{const n=[...document.querySelectorAll('nav, aside')].find(x=>/In this article/i"
        ".test(x.innerText)); if(!n) return null; const r=n.getBoundingClientRect();"
        " return [r.x, r.y, r.width, r.height, n.scrollHeight]})()"
    )
    print("nav box", nav)
    pg.get_by_text("In this article", exact=False).first.click()  # the outline opens on a click
    pg.wait_for_timeout(1500)
    print(
        "in this article, open:",
        pg.evaluate(
            "(()=>{const n=[...document.querySelectorAll('nav, aside')].find(x=>/In this article/i"
            ".test(x.innerText)); return n? n.innerText : null})()"
        ),
    )
    pg.screenshot(path=f"{out}/nav-open.png", full_page=False)
    for x in "abcdefgh":
        shoot(pg, f"appendix-{x}", f"{x.upper()}-opening")
    with open(f"{out}/supporting-text.txt", "w") as f:
        f.write(pg.evaluate("document.body.innerText"))
    # the two pointers of good enough, followed from the paper's page
    pg.goto(f"{base}/", wait_until="networkidle")
    pg.wait_for_timeout(4000)
    pointers = (
        ("pointer-s2-b11", "sub-b-11", "use PCA as a downstream step"),
        ("pointer-s6-g", "appendix-g", "records what the results leave open"),
    )
    for name, label, words in pointers:
        link = pg.locator(f"p:has-text('{words}') a[href*='#{label}']").first
        print(name, "link text:", link.inner_text(), "href:", link.get_attribute("href"))
        link.scroll_into_view_if_needed()
        pg.wait_for_timeout(500)
        pg.screenshot(path=f"{out}/{name}-source.png")
        link.click()
        pg.wait_for_timeout(4000)
        print(name, "landed at:", pg.url)
        shoot(pg, label, f"{name}-target")
        pg.goto(f"{base}/", wait_until="networkidle")
        pg.wait_for_timeout(3000)
    b.close()
