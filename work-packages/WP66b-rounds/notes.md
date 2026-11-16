# WP66b: choices where the specification is silent

Each choice is the smallest one that meets the specification's tests.

1. `scripts/paper_mode.py`: a missing key, a key of the wrong type and an unknown key are each named
   (`paper_mode: <field>: missing`, `must be an integer`, `unknown key`) and stop the other rules. A missing
   `--file` exits 2 (usage); a file that is not TOML exits 1. `check` prints `ok <mode> -` when the pin is empty.
   `parse` prints the mode and `name=value` per group the tag carries. `show` refuses a file that fails the tag
   stage. `banner()` omits the DOI part when `doi` is empty; the composer may import it.
2. `scripts/paper_pin.py`: `prepare` writes the mode file only; the section of `paper/CHANGES.md` is the person's
   (spec 2.4 lists what `prepare` writes). A working tag's date is taken from the tag; a `--date` that differs
   fails. `record` refuses a tag that is not the file's pin. `gh` is a callable (`main(argv, gh=...)`), so the
   test injects a fake; `--repo` defaults to `$GITHUB_REPOSITORY`, else `gh` infers it.
3. The rendered `paper/mode.toml` is the block of spec 3.1, comments included; both scripts write that form.
4. `paper/build_keys.py`: `--paper-dir` (hidden) points the script at a planted pair of notebooks for its tests.
   `--xref` strips `$BASE_URL` from the built URLs, since `paper.yml` sets it for the build.
5. `paper/pin_links.py`: exit 2 when the directory is missing or the ref is empty or holds a slash.
6. `.github/workflows/paper.yml`: `setup-uv` runs before the mode checks (they need `uv`); `actions/setup-node` is
   pinned to v5.0.0 (`a0853c24544627f65ddf259abe73b1d18a591444`, resolved with `gh api`). The release notes are
   built with `jq` and `awk` in the job. The clean-up's exit status is written into its report and the issue is
   opened whatever it is. `on-failure` also names cancelled jobs.
7. The `paper` marker: `tests/conftest.py` deselects through `pytest_deselected`, so pytest's summary counts
   them; the switch is `HTS_PAPER_TESTS=1` exactly. `pytest_plugins = ("pytester",)` is registered there for the
   cut's test.
8. `test_the_documented_bare_command_exits_zero_on_the_repository` (`tests/test_vocabulary.py`) is marked
   `paper`: the bare command covers both surfaces.
9. `test_every_row_is_in_exactly_one_surface` also checks that an id is used once across the register, since
   the two surface tests no longer see each other's ids. It reads no row's content beyond `file` and `id`.
10. `--views` and `--write-baseline` together are a usage error: the baseline is the whole report.
11. `test_key_manifest_equals_the_built_paper_labels` builds the paper in a temporary copy (as
    `test_myst_builds_the_html_site` does) rather than reading a `paper/_build` another command left; marked
    `slow`.
