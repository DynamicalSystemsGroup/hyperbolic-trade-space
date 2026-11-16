"""Capture Figure 10 of the wheat page as rendered, light and dark, at 1,280 px.

    uv run --with playwright python work-packages/WP63-rounds/wheat-figure/capture.py OUT PORT [TAG]

Reads the docsite built by ``uv run mkdocs build -q`` (``build/docsite``) served at
``http://127.0.0.1:PORT/``; headless Chrome at 1,280 by 900. Writes ``TAG-light.png`` and
``TAG-dark.png`` (the figure and its caption, element screenshots) and prints the image's drawn
width in CSS pixels.
"""

import sys

from playwright.sync_api import sync_playwright

out, port = sys.argv[1], sys.argv[2]
tag = sys.argv[3] if len(sys.argv) > 3 else "after"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    for scheme in ("light", "dark"):
        pg = b.new_page(viewport={"width": 1280, "height": 900}, color_scheme=scheme)
        pg.goto(f"http://127.0.0.1:{port}/examples/wheat/", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        fig = pg.locator("figure").filter(has_text="Figure 10.")
        fig.scroll_into_view_if_needed()
        img = fig.locator(f"img[src*='-{scheme}.png']")
        print(scheme, "image width", img.evaluate("e => e.getBoundingClientRect().width"))
        fig.screenshot(path=f"{out}/{tag}-{scheme}.png")
        pg.close()
    b.close()
