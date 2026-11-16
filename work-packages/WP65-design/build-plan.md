# WP65 D-2: the build plan (G7)

Three build units from `specification.md`, built in parallel from one `dev` head, one worktree and branch each
(`wp66a`, `wp66b`, `wp66c`), then quality control (WP67), integration (WP68) and the cascade review (WP69). A unit
edits only its own files; a file another unit owns is read, never written.

## 1. The units and their file sets

### WP66a, the software model

| File | Change |
|---|---|
| `.github/workflows/release.yml` | rewritten (spec 1.2) |
| `.github/workflows/test.yml` | pull-request trigger; shards `fast`, `slow`, `docs`; `not paper` (spec 5.3) |
| `.github/workflows/pages.yml` | deleted |
| `scripts/release_cleanup.py` | new (spec 1.4) |
| `scripts/release_checks.py` | subcommands `tag`, `merge`, `pypi` |
| `tests/test_release_workflows.py` | new |
| `tests/test_release_cleanup.py` | new |
| `tests/test_release_checks.py` | tests for the three subcommands |
| `tests/test_ci_shards.py` | rewritten for the new triggers and shards |
| `.github/RELEASE_ADMISSIBILITY.md` | rows for the merge (spec 6.2) |
| `docs/code-owners.md` | the flow, settings, cutting a release (spec 6.2, both drifts) |
| `CHANGELOG.md` | the entry and the WP34 line (spec 6.2) |
| `CITATION.cff` | new |
| `work-packages/interface-contract.md`, `work-packages/interface-contract.toml`, `tests/test_interface_contract.py` | amendment 29 (spec 6.1) |
| `work-packages/README.md` | Branching paragraph (spec 6.2) |
| `work-packages/WP8b-release-checklist.md` | deleted |
| `work-packages/release-checklist-software.md` | new (spec 6.3) |
| `work-packages/release-candidate.md` | the dated section (spec 6.4) |

The contract amendment sits with WP66a because it lands last and describes the state all three units leave; it
retires `pages.yml`, whose contract test (`test_r7_pages_workflow`) the same unit replaces.

### WP66b, the paper model

| File | Change |
|---|---|
| `.github/workflows/paper.yml` | new (spec 2.2) |
| `paper/mode.toml` | new, `abstract` |
| `paper/paper-keys.json` | new, written by `paper/build_keys.py` |
| `paper/build_keys.py` | new (spec 2.6) |
| `paper/pin_links.py` | new (spec 2.7) |
| `paper/CHANGES.md` | new, header only (spec 2.8) |
| `scripts/paper_mode.py` | new (spec 3.1) |
| `scripts/paper_pin.py` | new (spec 2.4) |
| `scripts/check_vocabulary.py` | `--surface` |
| `scripts/check_residuals.py` | `--views` |
| `tests/conftest.py` | the `paper` marker and its deselection |
| `tests/test_paper.py`, `tests/test_paper_static_figures.py`, `tests/test_container.py` | module `pytestmark = pytest.mark.paper` |
| `tests/test_claims_register.py` | split by surface |
| `tests/test_vocabulary.py` | split by surface |
| `tests/test_residuals.py` | the views filter |
| `tests/test_paper_model.py` | new |
| `work-packages/release-checklist-paper.md` | new (spec 6.3) |

### WP66c, the composer, the abstract page and the docs' keys

| File | Change |
|---|---|
| `.github/workflows/site.yml` | new (spec 3.5) |
| `.github/workflows/pages-deploy.yml` | new (spec 3.5) |
| `scripts/assemble_site.py` | the slot; no paper build (spec 3.4) |
| `scripts/stage_site.py` | `--slot`, `--artefact` |
| `scripts/paper_keys.py` | the manifest and the slot (spec 4) |
| `scripts/paper_abstract.py` | new (spec 3.3) |
| `site/paper/index.html` | deleted (the placeholder) |
| `site/paper/abstract.html` | new template |
| `tests/test_site.py` | keys, layout, the site workflows; three tests removed (spec 5.2) |
| `tests/test_build_generated.py` | the eight paper-build tests replaced |
| `tests/test_paper_slot.py` | new |

### The disjointness check (R-4)

The three file sets have empty pairwise intersections, by this check over `build-plan.md`:

```
uv run --no-project python - <<'EOF'
import re, itertools, pathlib
text = pathlib.Path("work-packages/WP65-design/build-plan.md").read_text()
units = {}
for name, body in re.findall(r"### (WP66[abc])[^\n]*\n(.*?)(?=\n### |\Z)", text, re.S):
    units[name] = {p for row in re.findall(r"^\| (`[^|]+`) \|", body, re.M) for p in re.findall(r"`([^`]+)`", row)}
for a, b in itertools.combinations(sorted(units), 2):
    print(a, b, sorted(units[a] & units[b]) or "disjoint")
print({k: len(v) for k, v in units.items()})
EOF
```

Output at WP65's commit:

```
WP66a WP66b disjoint
WP66a WP66c disjoint
WP66b WP66c disjoint
{'WP66a': 20, 'WP66b': 19, 'WP66c': 11}
```

Two moves cross units and are split so that no file is shared: the built-keys test and the theme test leave
`tests/test_site.py` (WP66c deletes them) and enter `tests/test_paper_model.py` (WP66b adds them).

## 2. The tests each unit adds

Every new test is unmarked (in the software gate) unless "paper" is written.

**WP66a.** `tests/test_release_workflows.py`:
`test_release_triggers_are_pull_request_push_to_main_and_qc_and_dispatch` (triggers exactly as spec 1.2, no `tags`
key); `test_no_workflow_triggers_on_a_v_tag` (across `.github/workflows/`, `push.tags` appears only in `paper.yml`,
equal to `["paper-*"]`); `test_no_job_waits_on_a_tag_event` (no `ref_type == 'tag'` or `refs/tags/` in `release.yml`,
`site.yml`, `pages-deploy.yml`); `test_release_job_graph` (each job's `needs` as in the table of spec 1.2);
`test_release_steps_run_only_on_a_push_to_main` (`tag`, `publish-pypi`, `deploy-site`, `publish-release` carry the
`RELEASE` condition); `test_pypi_jobs_are_jobs_of_release_yml` (environment `pypi`/`testpypi`, `id-token: write`, the
publish action; no `uses:` at job level); `test_site_jobs_are_called_workflows` (`site` and `deploy-site` call the two
files; `deploy-site` has `pages: write`, `id-token: write`); `test_on_failure_cleans_up_and_opens_an_issue` (the `if`,
the cleanup command with `--tag`, `gh issue`, permissions); `test_top_level_permissions_read_only`;
`test_concurrency_never_cancels_a_release`; `test_pages_yml_is_gone`.
`tests/test_release_cleanup.py` (a fake `gh` and a fake PyPI injected as callables):
`test_removes_the_draft_then_the_tag_when_pypi_lacks_the_version`, `test_dry_run_removes_nothing`,
`test_keeps_everything_when_pypi_holds_the_version` (exit 3, the rerun line),
`test_refuses_a_published_release` (exit 3), `test_nothing_to_clean_exits_zero`,
`test_a_paper_tag_never_asks_pypi`, `test_a_bad_tag_is_a_usage_error` (exit 2),
`test_a_failed_deletion_exits_one_and_reports_what_was_removed`, `test_json_report_has_its_fields`.
`tests/test_release_checks.py`: `test_tag_state_new_ours_taken`, `test_merge_commit_needs_two_parents_from_dev`,
`test_pypi_hashes_must_equal_the_dist`.
`tests/test_ci_shards.py`: `test_workflow_runs_on_dispatch_call_and_pull_requests_to_main`,
`test_three_shards_cover_every_software_test` (`fast`, `slow`, `docs`; `not paper` in each command),
`test_docs_modules_exist_and_hold_no_paper_module`, `test_no_shard_sets_the_paper_switch`,
`test_windows_never_runs_on_a_pull_request`.
`tests/test_interface_contract.py`: `test_r7_release_and_site_workflows` (replaces `test_r7_pages_workflow`),
`test_r6_reference_keys_from_the_manifest`, `test_r7_paper_branch_workflow_and_modes_pinned`, ownership entries of
amendment 29 checked by the existing ownership tests.

**WP66b.** `tests/test_paper_model.py`: `test_mode_file_is_valid_for_serving` (the committed file, `--stage
served`); `test_each_broken_mode_field_is_named` (parametrized over the rules of spec 3.1);
`test_tag_shapes_parse` and `test_no_paper_tag_matches_v_star`; `test_key_manifest_is_canonical` (schema, routes,
sorted, bytes); `test_key_manifest_equals_the_notebooks_labels` (paper; `build_keys.py --check`);
`test_key_manifest_equals_the_built_paper_labels` (paper; needs `PAPER_BUILD` and a build);
`test_paper_theme_is_pinned_to_a_commit` (paper; moved); `test_paper_workflow_triggers_and_tag_filter`;
`test_paper_workflow_release_job_publishes_two_assets_from_a_draft`; `test_paper_workflow_never_deploys`;
`test_paper_workflow_failure_runs_the_cleanup`; `test_pin_links_rewrites_blob_main_to_the_tag`;
`test_paper_pin_prepare_and_record_write_the_mode_file` (fake `gh`); `test_paper_tests_are_deselected_without_the_switch`
(pytester). The split tests of spec 5.2 in `test_claims_register.py`, `test_vocabulary.py`, `test_residuals.py`.

**WP66c.** `tests/test_paper_slot.py`: `test_abstract_page_has_the_title_author_abstract_and_build_line`;
`test_abstract_page_has_no_forbidden_word_and_no_date`; `test_abstract_page_has_the_docs_and_root_cards`;
`test_abstract_page_has_no_script_and_both_colour_schemes`; `test_abstract_with_markup_fails_the_render`;
`test_a_pinned_slot_unpacks_the_artefact_with_one_banner_line_per_page`; `test_banner_names_mode_tag_date_and_doi`
(per mode); `test_checksum_mismatch_falls_back_and_says_so`; `test_unreachable_artefact_falls_back_and_says_so`;
`test_keys_mismatch_falls_back`; `test_strict_slot_turns_a_fallback_into_exit_one`;
`test_the_composer_never_runs_myst`; `test_root_card_line_per_mode`; `test_paper_flag_is_gone` (exit 2).
`tests/test_site.py`: `test_docsite_cites_the_paper_only_through_keys` (against the manifest);
`test_keys_resolve_to_anchors_in_a_pinned_slot_and_to_the_abstract_otherwise`; `test_unknown_key_fails_in_both_slots`;
`test_assembled_layout` (the abstract page); `test_root_and_paper_links_classified` (the template);
`test_site_workflow_composes_and_never_deploys`; `test_pages_deploy_workflow_is_called_only`.
`tests/test_build_generated.py`: `test_stage_site_stages_the_abstract_page_offline`,
`test_stage_site_with_an_artefact_stages_the_pin`.

## 3. The local checks every unit runs before it hands back

`uv run pytest` (the software suite: paper tests deselected), `HTS_PAPER_TESTS=1 uv run pytest -m "paper and not
slow"` for WP66b, `uv run ruff check .`, `uv run ruff format --check .`, `uv lock --check`, `uv run python
scripts/check_vocabulary.py --surface software`, the attribution grep, `uv run python
scripts/release_checks.py pins`; WP66c also `uv run python scripts/stage_site.py --serve` and a look at `/paper/`
in a browser, desktop and 375 px, light and dark, screenshots in its record; WP66a also
`uv run --no-project python scripts/release_cleanup.py --tag v0.0.0 --dry-run` against the live repository (read
only: it finds nothing and exits 0).

## 4. Quality control (WP67): runs and the browser pass

No dispatch of `release.yml` or `paper.yml` is possible before the first merge (spec section 9, item 1). The runs:

| Run | How | Expected |
|---|---|---|
| Release dry run | push `dev`'s head to `qc/release` | `check`, `test`, `build`, `site` green; `tag`, `publish-*`, `deploy-site`, `publish-release`, `on-failure` skipped; the summary names the slot `abstract` |
| Release dry run that fails | push to `qc/release-fail` a commit whose `CHANGELOG.md` lacks the entry | `check` fails, naming the changelog; nothing after it runs; no issue (not `main`) |
| Site build | the `site` job of the dry run | `_site` artefact downloaded and staged locally; `/paper/` is the abstract page |
| Paper branch build | push `dev`'s head (with WP66b) to `qc/paper/build` | every paper test, the HTML build, the keys check green; the `paper-release` artefact holds two files |
| Paper failure path | push to `qc/paper/broken` a commit that breaks one paper test | `build` fails, the summary names the step; no release, no issue |
| Clean-up by hand | `release_cleanup.py --tag v0.0.0 --dry-run` and `--tag paper-working-20000101 --dry-run` | exit 0, "nothing to remove" |
| Machinery diff | `machinery.toml` of WP64 diffed against the built tree | every row changed, removed or added is explained in the QC record |

The browser pass per mode: stage with `--slot abstract`; then with `--artefact` pointing at the `paper-release`
artefact of the QC paper build and a temporary `paper/mode.toml` (uncommitted) in each of `working`, `submitted` and
`revision` with test values for `doi` and `sha256`; then the fallback (a wrong checksum). For each: `/`, `/paper/`,
`/paper/supporting-material/`, one docs page with a citation (the link lands on the anchor or on `/paper/`), desktop
and 375 px, light and dark, captures in the record, the banner read in each mode, the console free of errors.

## 5. Landing order on `dev`

1. **WP66b** first: it adds the marker, the mode file, the manifest and the paper's workflow; nothing on `dev`
   reads them yet, and the conftest deselection takes the paper's tests out of `uv run pytest` at once (C4 cut).
2. **WP66c** second, rebased on 1: the composer reads `paper/mode.toml` and `paper/paper-keys.json`; `pages.yml`
   still exists and still calls the composer (now offline and without the paper).
3. **WP66a** last, rebased on 2: the release workflow calls `site.yml` and `pages-deploy.yml`, `pages.yml` goes, the
   contract records the whole.

Each landing re-runs the unit's local checks on the rebased branch, lands with `git merge --no-ff`, and is recorded
in `work-packages/driver-log.md`. WP67 runs after the third landing.

## 6. The first merge into `main` since e7fd1165 (WP68)

Before the pull request: his keyboard items (`his-items.md`) done and read back with `gh api` (rulesets,
environments, Pages source, Zenodo switch on); the PyPI and TestPyPI pending publishers registered; a TestPyPI
publish is not possible before the merge either (dispatch), so the first TestPyPI run, if he wants one, follows it.

The pull request from `dev` into `main` carries: every commit since e7fd1165 (2,018 and the build's); version 0.1.0
in `pyproject.toml`, `uv.lock` and `__version__`; `CHANGELOG.md`'s `[0.1.0] - <date>`; `paper/mode.toml` in
`abstract`; the new workflows, so the dispatch buttons exist after it; the records. It closes a release issue
"Release 0.1.0". Its required checks run on the pull request (a `pull_request` run uses the workflow files of the
pull request's merge ref). The staged-site review is recorded in the release issue.

The merge runs `release.yml` on `main`: tag `v0.1.0`, PyPI 0.1.0, the site with the abstract page at `/paper/`, the
GitHub release published, Zenodo's first archive. Then the `paper` branch is created from the merge's `dev` side:
`git branch paper dev && git push origin paper`, and its ruleset applied.

What the first live runs confirm (not establishable before): the tag pushed by the workflow raises nothing; the
`github-pages` environment admits the deploy from `main`; Zenodo archives on publication of the draft and assigns
the software and later the paper to one record or two; the execution test on a hosted runner.

## 7. Where each record of G6 is amended

| Record | Unit | Spec |
|---|---|---|
| `work-packages/interface-contract.md`, `.toml`, `tests/test_interface_contract.py` | WP66a | 6.1 |
| `work-packages/README.md` (CI triggers; three branches) | WP66a | 6.2 |
| `docs/code-owners.md` (`:27` against `:76`; `:30-32`) | WP66a | 6.2 |
| checklist G2 (private) and the split | WP66a (software list, the old file removed), WP66b (paper list) | 6.2, 6.3 |
| `CHANGELOG.md` | WP66a; the `[0.1.0]` heading at WP68 | 6.2 |
| `.github/RELEASE_ADMISSIBILITY.md`, `CITATION.cff` | WP66a | 6.2 |
| `paper/CHANGES.md` | WP66b | 2.8 |
| `work-packages/release-candidate.md` | WP66a | 6.4 |
| `work-packages/release-punch-list.md` (version, first deployment) | WP68 | |
| `work-packages/reviewers-guide/` recut | WP69 | 6.5 |
| `CLAUDE.md`'s Branching line ("`main` gets `git merge --no-ff dev` when content merits a CI run"), which now describes a release | WP68, on his read (his file) | |
| `work-packages/INDEX.md`, `driver-log.md` | each landing | |
