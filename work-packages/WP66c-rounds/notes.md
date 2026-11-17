# WP66c — choices where the specification is silent

The contract is `work-packages/WP65-design/specification.md`, sections 3.2 to 3.5 and 4. Each row is a choice the
text did not fix, with the reading taken.

| # | Where | The specification | The choice |
|---|---|---|---|
| 1 | 3.4 step 1 | "Any failure gives the fallback abstract page with the reason" | Read literally: a mode file that is missing, unreadable or fails its check also gives the fallback (with `--strict-slot`, exit 1). The fallback line names the pin as the file writes it, or `-` when it names none. |
| 2 | 3.4 step 1, 3.1 | "read `paper/mode.toml` (`check --stage served`)" | The composer runs `scripts/paper_mode.py check --stage served --file <path>` when the script exists (WP66b's validator, its command line as 3.1 fixes it) and also checks the fields it relies on itself: schema 1, the mode one of four, and in a pinned mode the pin, the DOI and the SHA-256 in their shapes. |
| 3 | 3.4 step 1 | the artefact's checks: reachable, checksum, keys | An artefact that does not unpack, holds no `index.html`, or holds an `.html` file that is not UTF-8 (macOS `tar` adds `._*` resource files under the same names) is a failure of the same kind and falls back. The tarball unpacks with `tarfile`'s `data` filter. The slot is unpacked and bannered in a temporary directory before the docs build, so the docs' slot always matches what `/paper/` gets. |
| 4 | 3.4, exit codes | "1 ... a fallback under `--strict-slot`" | Under `--strict-slot` the composer stops after resolving the slot: the slot line and the warning are printed, nothing is composed. |
| 5 | 3.2 | "a `<p class="hts-paper-banner">` linked to `https://doi.org/<doi>`" | The whole line is the link. A short inline `style` (system font, centred, a hairline below) keeps it legible inside the paper's theme in both colour schemes; the artefact gets no stylesheet or script. Files without a `<body>` tag are left as they are. |
| 6 | 3.4 step 5 | "with `--summary FILE` append it as Markdown" | A `### Paper slot` heading with three bullets: slot, pin, reason. |
| 7 | 3.3 | "a `$`, a role or a link in it fails the render" | Also refused: a bare URL, an HTML tag and a backtick. Paragraphs are split on blank lines and each is joined onto one line. |
| 8 | 3.3 | "two cards in the root page's style: `../docs/getting-started/` ("Use the code") and `../` (the root page)" | The cards copy the root page's `.doors` and `.card` rules; the second is labelled "Project home" with the line "the method in brief, the docs and the package". A small "Abstract" label precedes the abstract; the footer has the source code and documentation links. |
| 9 | 3.3 | "the existing meta tags" | Title tag `<title>: hyperbolic-trade-space`, `og:title` the paper's title, description and `og:description` the abstract's first sentence. |
| 10 | 3.4 | the composer's return value | `assemble()` returns `(out, Slot)`; `stage()` returns `(out, Slot)`, or `(out, None)` when an existing stage is reused. `assemble()` takes a slot already resolved (`resolved=`), so the command line resolves once. |
| 11 | 4 | `slot()`: "abstract when `paper/mode.toml` says so and `pin` otherwise" | A missing mode file is an error, not `pin` (the docs build fails naming the file). |
| 12 | 4 | the manifest's rules | `load_manifest` checks the bytes equal the canonical form (`json.dumps(..., indent=2)` with `schema` first and the keys sorted, one trailing newline), which covers "sorted", "two-space indent" and "one trailing newline" in one comparison. |
| 13 | build plan, section 2 | "the eight `build_paper` and strict-paper tests (`:412` to `:529`)" | The test at `:529` (`test_stage_builds_the_paper_for_the_root_route`) asserted the paper's build route, which no longer exists; it is removed with the eight. `test_assemble_with_fake_mkdocs`, `test_assemble_fails_loudly_when_mkdocs_fails` and `test_stage_no_build_reuses_existing` were kept and moved to the new interface. |
| 14 | 3.5 | outputs "read from the composer's stdout line" | `site.yml` tees the composer's output and reads the third and fourth fields of the `assemble_site: slot` line; a pin of `-` becomes the empty string. |
| 15 | branch state | `paper/mode.toml` and `paper/paper-keys.json` are WP66b's | Not committed here. The worktree carries uncommitted copies (the mode `abstract`; the manifest written from the notebooks by the old parse in the canonical form) so the docs build and the checks run before WP66b lands; the slot tests write their own mode files, artefacts and manifests under `tmp_path` and use the committed manifest when it exists. |

Left as it was: the root page's lead paragraph ("The paper makes the argument and gives the proofs; ...") is outside
3.4, which changes only the card's line; in `abstract` mode it says more than `/paper/` holds. The abstract page links
`tree/paper`, which answers 404 until the `paper` branch is created at the first merge (build plan, section 6).

## The browser pass (G6)

Headless Chrome through Playwright, served by `uv run python scripts/stage_site.py --serve` on 127.0.0.1 (ports 8892
and 8893), each server stopped after its captures. No page scrolls sideways at 1,280 px or 375 px.

| Capture | Stage | What it shows |
|---|---|---|
| `captures/abstract-paper-{1280,375}-{light,dark}.png` | `--slot abstract` (the default, offline) | `/paper/`: the title, "Michael Zargham, Dynamical Systems Group", the approved abstract as one paragraph, the build line with the branch link and the command, the cards "Use the code" and "Project home", the footer; both colour schemes from the root page's tokens |
| `captures/abstract-root-1280-light.png`, `abstract-root-375-dark.png` | the same | `/`: the paper card reads "its abstract; the paper is iterated towards release" |
| `captures/pin-paper-{1280,375}-{light,dark}-top.png` | `--artefact` with a local `paper-html.tar.gz` of the manifest's labels and a temporary `paper/mode.toml` in `working` mode (restored to `abstract` after) | `/paper/`: the banner line "Working paper · paper-working-20261120 · 2026-11-20 · DOI 10.5281/zenodo.123", linked to the DOI, directly above the page |
| `captures/pin-paper-supporting-material-{1280,375}-{light,dark}-top.png` | the same | `/paper/supporting-material/`: the same banner, one per page |
| `captures/pin-root-1280-light.png`, `pin-root-375-dark.png` | the same | `/`: the paper card keeps "the argument and the proofs" |
| `captures/pin-docs-theory-1280-light.png`, `pin-docs-theory-375-dark.png` | the same | a docs page with eight citations; in this slot they link `../../paper/#<key>` (in the abstract slot `../../paper/`) |

Console: no error on the abstract page or the root page. The docs pages log one 404, the theme's request for
`api.github.com/repos/.../releases/latest`, which answers 404 until the first release (as on `dev`); the fabricated
artefact has no icon, so its first page logs a `/favicon.ico` 404. A first artefact made with macOS `tar` carried
`._*` resource files named `*.html`; the composer then stopped on a decoding error instead of falling back, which is
now a fallback with the reason (row 3 above) and a test.
