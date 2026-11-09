#!/bin/sh
# Build the paper's HTML inside the container, with or without network (WP10, Appendix F).
#
#   docker run --rm --network none hts-paper sh paper/container/build-paper.sh
#
# MyST's session constructor asks registry.npmjs.org for the latest `mystmd` version (to print an
# "upgrade available" notice). With no network the request fails in a retry path that crashes the
# MyST process (a got/p-cancelable defect under Node 24: "The onCancel handler was attached after
# the promise settled"). The query only decorates the log, so this script points npm's registry
# setting at a stub on the loopback interface that answers 404 to everything: MyST then ignores the
# missing package and nothing else changes. Everything the build really needs (site template, web
# libraries, DOI lookups) was cached in paper/_build when the image was built. The one thing the
# build still asks the network for is the default site favicon (https://mystmd.org/favicon.ico);
# MyST treats it as an optional asset and continues, and this script restores the copy cached at
# image build time into the HTML output.
set -eu
PORT="${HTS_STUB_PORT:-48123}"
python - "$PORT" <<'PY' &
import http.server, sys
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_error(404)
    def log_message(self, *a):
        pass
http.server.HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
PY
STUB=$!
trap 'kill $STUB 2>/dev/null || true' EXIT
sleep 1
cd "$(dirname "$0")/../.."/paper
npm_config_registry="http://127.0.0.1:${PORT}/" uv run myst build --html
if [ ! -f _build/html/favicon.ico ] && [ -f _build/cache/favicon.ico ]; then
    cp _build/cache/favicon.ico _build/html/favicon.ico
fi
