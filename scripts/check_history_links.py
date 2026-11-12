"""Fetch every external link on ``site/history.html`` and report its HTTP status (network).

    uv run python scripts/check_history_links.py

The default test suite checks the page offline (``tests/test_site.py``); this script is the network
check, run by hand when the page changes. A link counts as resolving on a 2xx or 3xx answer; a 403
or 429 is reported as ``blocked`` (the host refuses automated requests; open it in a browser) and
anything else as ``FAIL``. Exit status is 1 when any link FAILs.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "site" / "history.html"
AGENT = "Mozilla/5.0 (compatible; link-check)"


class _Hrefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs += [v for k, v in attrs if k == "href" and v]


def external_links(page=PAGE):
    parser = _Hrefs()
    parser.feed(Path(page).read_text(encoding="utf-8"))
    return sorted({h for h in parser.hrefs if h.startswith(("http://", "https://"))})


def status(url, timeout=25):
    """``(label, code)`` for ``url``: ok, blocked or FAIL."""
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return "ok", response.status
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405, 429, 501):
                continue  # some hosts refuse HEAD; try GET
            return ("blocked" if exc.code in (403, 429) else "FAIL"), exc.code
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return "FAIL", type(exc).__name__
    return "FAIL", "?"


def main():
    urls = external_links()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(status, urls))
    for url, (label, code) in zip(urls, results, strict=True):
        print(f"{label:7} {code}  {url}")
    return 1 if any(label == "FAIL" for label, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main())
