"""WP63 captures: the four example pages, top to bottom in screens, and their text.

    uv run --with playwright python work-packages/WP63-rounds/capture.py OUT PORT

Reads the docsite built by ``uv run mkdocs build -q`` (``build/docsite``) and served at
``http://127.0.0.1:PORT/``; headless Chrome at 1,280 by 900, light scheme. Writes
``<page>-NN.png`` per screen and ``<page>.txt``, the page's article text (for the cold reads), and
prints each page's height and scroll width.
"""

import sys

from playwright.sync_api import sync_playwright

out, port = sys.argv[1], sys.argv[2]
PAGES = {
    "cubesat": "examples/",
    "perovskite": "examples/perovskite/",
    "amniote": "examples/amniote/",
    "wheat": "examples/wheat/",
}
H = 900

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 1280, "height": H}, color_scheme="light")
    for name, path in PAGES.items():
        pg.goto(f"http://127.0.0.1:{port}/{path}", wait_until="networkidle")
        pg.wait_for_timeout(1500)
        height = pg.evaluate("document.documentElement.scrollHeight")
        width = pg.evaluate("document.documentElement.scrollWidth")
        print(name, "height", height, "scrollWidth", width)
        n, y = 0, 0
        while y < height:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(400)
            n += 1
            pg.screenshot(path=f"{out}/{name}-{n:02d}.png")
            y += H - 100
        with open(f"{out}/{name}.txt", "w") as f:
            f.write(pg.evaluate("document.querySelector('article').innerText"))
    b.close()
