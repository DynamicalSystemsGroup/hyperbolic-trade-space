"""Fetch every URL of the history record and report its HTTP status (network).

    uv run python scripts/check_history_links.py            # every URL of history.yaml
    uv run python scripts/check_history_links.py --page     # only the links of the page's prose

The default test suite checks the record and the page offline (``tests/test_site.py``); this script
is the network check, run by hand when the record or the page changes. A link counts as resolving on
a 2xx or 3xx answer; a 403 or 429 is reported as ``blocked`` (the host refuses automated requests;
open it in a browser) and anything else as ``FAIL``. Exit status is 1 when any link FAILs. No
credentials are sent: the check sees what any reader sees.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import history_record

PAGE = history_record.PAGE
AGENT = "Mozilla/5.0 (compatible; link-check)"


class _Hrefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs += [v for k, v in attrs if k == "href" and v]


def external_links(page=PAGE):
    """The distinct https links of a page's hand-written prose."""
    parser = _Hrefs()
    parser.feed(Path(page).read_text(encoding="utf-8"))
    return sorted({h for h in parser.hrefs if h.startswith(("http://", "https://"))})


def record_urls(entries):
    """The URL of every entry of the record, in record order."""
    return [e["url"] for e in entries]


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


def check(urls, fetch=status, workers=8):
    """``[(url, label, code)]`` for each URL; ``fetch(url)`` is injectable for tests."""
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fetch, urls))
    return [(u, label, code) for u, (label, code) in zip(urls, results, strict=True)]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    urls = external_links() if "--page" in argv else record_urls(history_record.load())
    rows = check(urls)
    for url, label, code in rows:
        print(f"{label:7} {code}  {url}")
    return 1 if any(label == "FAIL" for _, label, _ in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
